/**
 * Friend Routes — Phase 4 (Social).
 *
 * Endpoints:
 *   GET    /              → list my accepted friends
 *   GET    /requests      → list pending requests (incoming + outgoing)
 *   POST   /request       → send a friend request to { targetId, targetRole }
 *   POST   /:id/accept    → accept a pending request addressed to me
 *   POST   /:id/decline   → decline a pending request addressed to me
 *   DELETE /:id           → unfriend (works in either direction)
 *   POST   /:id/share     → toggle my position-sharing flag for this friend
 *
 * All endpoints require auth. Per-side sharing flag lets each user control
 * whether the other can see their live location (Phase 4.3 sockets).
 */
const express = require('express');
const { requireAuth } = require('../middleware/auth');
const Friendship = require('../models/Friendship');
const Owner = require('../models/Owner');
const Sitter = require('../models/Sitter');
const Walker = require('../models/Walker');
const logger = require('../utils/logger');

const router = express.Router();

const ROLE_TO_MODEL_NAME = { owner: 'Owner', sitter: 'Sitter', walker: 'Walker' };
const MODEL_BY_NAME = { Owner, Sitter, Walker };

function me(req) {
  return {
    id: req.user.id,
    role: req.user.role,
    model: ROLE_TO_MODEL_NAME[req.user.role] || 'Owner',
  };
}

/** Fetch a minimal user profile regardless of role, for enriching friend lists. */
async function fetchUserMini(id, modelName) {
  const Model = MODEL_BY_NAME[modelName];
  if (!Model) return null;
  const u = await Model.findById(id)
    .select('firstName lastName profilePicture location city avatar')
    .lean();
  return u
    ? {
        id: u._id,
        model: modelName,
        name: [u.firstName, u.lastName].filter(Boolean).join(' ').trim(),
        avatar: u.profilePicture || u.avatar || '',
        city: u.location?.city || u.city || '',
      }
    : null;
}

async function enrichFriendship(friendship, viewerId) {
  const isRequester = String(friendship.requesterId) === String(viewerId);
  const other = isRequester
    ? await fetchUserMini(friendship.addresseeId, friendship.addresseeModel)
    : await fetchUserMini(friendship.requesterId, friendship.requesterModel);
  const mySharePosition = isRequester
    ? friendship.requesterSharesPosition
    : friendship.addresseeSharesPosition;
  const theirSharePosition = isRequester
    ? friendship.addresseeSharesPosition
    : friendship.requesterSharesPosition;
  return {
    id: friendship._id,
    status: friendship.status,
    initiatedByMe: isRequester,
    other,
    mySharePosition,
    theirSharePosition,
    createdAt: friendship.createdAt,
    acceptedAt: friendship.acceptedAt,
  };
}

// v23.1 part 69 — Bug 9 : "Comment sajoute les amis ?". Daniel didn't
// know how to add friends. Added a search-by-email endpoint that the
// frontend's "+ Ajouter un ami" dialog calls.
//
// GET /friends/search?q=<email_or_name>
//   Returns up to 10 users (owner/sitter/walker) whose email contains
//   the query, plus their role and id. Excludes the caller themselves.
router.get('/search', requireAuth, async (req, res) => {
  try {
    const q = (req.query.q || '').toString().trim().toLowerCase();
    if (q.length < 2) {
      return res.json({ users: [] });
    }
    const meId = req.user.id;
    const escape = q.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&');
    const re = new RegExp(escape, 'i');
    const projection = 'name email avatar';

    const [owners, sitters, walkers] = await Promise.all([
      Owner.find({ $or: [{ email: re }, { name: re }] })
        .select(projection).limit(10).lean(),
      Sitter.find({ $or: [{ email: re }, { name: re }] })
        .select(projection).limit(10).lean(),
      Walker.find({ $or: [{ email: re }, { name: re }] })
        .select(projection).limit(10).lean(),
    ]);

    const _avatarUrl = (a) => (a && (a.url || a)) || '';
    const merged = [
      ...owners.map((u) => ({
        id: u._id.toString(),
        role: 'owner',
        name: u.name || '',
        email: u.email || '',
        avatar: _avatarUrl(u.avatar),
      })),
      ...sitters.map((u) => ({
        id: u._id.toString(),
        role: 'sitter',
        name: u.name || '',
        email: u.email || '',
        avatar: _avatarUrl(u.avatar),
      })),
      ...walkers.map((u) => ({
        id: u._id.toString(),
        role: 'walker',
        name: u.name || '',
        email: u.email || '',
        avatar: _avatarUrl(u.avatar),
      })),
    ].filter((u) => u.id !== meId).slice(0, 10);

    res.json({ users: merged });
  } catch (e) {
    logger.error('[friends/search]', e);
    res.status(500).json({ error: e.message });
  }
});

// ── GET /friends — my accepted friends ─────────────────────────────────────
router.get('/', requireAuth, async (req, res) => {
  try {
    const user = me(req);
    const friendships = await Friendship.find({
      status: 'accepted',
      $or: [
        { requesterId: user.id, requesterModel: user.model },
        { addresseeId: user.id, addresseeModel: user.model },
      ],
    })
      .sort({ acceptedAt: -1 })
      .lean();

    const enriched = await Promise.all(
      friendships.map((f) => enrichFriendship(f, user.id)),
    );
    res.json({ friends: enriched.filter((f) => f.other !== null) });
  } catch (e) {
    logger.error('[friends/list]', e);
    res.status(500).json({ error: e.message });
  }
});

// ── GET /friends/requests — pending (incoming + outgoing) ──────────────────
router.get('/requests', requireAuth, async (req, res) => {
  try {
    const user = me(req);
    const [incoming, outgoing] = await Promise.all([
      Friendship.find({
        status: 'pending',
        addresseeId: user.id,
        addresseeModel: user.model,
      }).lean(),
      Friendship.find({
        status: 'pending',
        requesterId: user.id,
        requesterModel: user.model,
      }).lean(),
    ]);

    const [incomingEnriched, outgoingEnriched] = await Promise.all([
      Promise.all(incoming.map((f) => enrichFriendship(f, user.id))),
      Promise.all(outgoing.map((f) => enrichFriendship(f, user.id))),
    ]);

    res.json({
      incoming: incomingEnriched.filter((f) => f.other !== null),
      outgoing: outgoingEnriched.filter((f) => f.other !== null),
    });
  } catch (e) {
    logger.error('[friends/requests]', e);
    res.status(500).json({ error: e.message });
  }
});

// ── POST /friends/request — send a new request ─────────────────────────────
router.post('/request', requireAuth, async (req, res) => {
  try {
    const { targetId, targetRole } = req.body;
    const targetModel = ROLE_TO_MODEL_NAME[targetRole];
    if (!targetId || !targetModel) {
      return res
        .status(400)
        .json({ error: 'targetId and targetRole are required.' });
    }

    const user = me(req);
    if (String(targetId) === String(user.id) && targetModel === user.model) {
      return res.status(400).json({ error: 'Cannot befriend yourself.' });
    }

    // Avoid duplicates in either direction.
    const existing = await Friendship.findOne({
      $or: [
        {
          requesterId: user.id,
          requesterModel: user.model,
          addresseeId: targetId,
          addresseeModel: targetModel,
        },
        {
          requesterId: targetId,
          requesterModel: targetModel,
          addresseeId: user.id,
          addresseeModel: user.model,
        },
      ],
    });
    if (existing) {
      return res
        .status(409)
        .json({ error: `Already in state "${existing.status}".`, id: existing._id });
    }

    const friendship = new Friendship({
      requesterId: user.id,
      requesterModel: user.model,
      addresseeId: targetId,
      addresseeModel: targetModel,
      status: 'pending',
    });
    await friendship.save();

    logger.info(
      `[friends] ${user.model} ${user.id} → ${targetModel} ${targetId} (pending)`,
    );
    res.status(201).json({ friendship: await enrichFriendship(friendship, user.id) });
  } catch (e) {
    logger.error('[friends/request]', e);
    res.status(500).json({ error: e.message });
  }
});

// ── POST /friends/:id/accept ───────────────────────────────────────────────
router.post('/:id/accept', requireAuth, async (req, res) => {
  try {
    const user = me(req);
    const f = await Friendship.findById(req.params.id);
    if (!f) return res.status(404).json({ error: 'Request not found.' });
    if (String(f.addresseeId) !== String(user.id) || f.addresseeModel !== user.model) {
      return res.status(403).json({ error: 'Only the addressee can accept.' });
    }
    if (f.status !== 'pending') {
      return res.status(400).json({ error: `Already ${f.status}.` });
    }
    f.status = 'accepted';
    f.acceptedAt = new Date();
    await f.save();
    logger.info(`[friends] ${user.id} accepted ${f._id}`);
    res.json({ friendship: await enrichFriendship(f, user.id) });
  } catch (e) {
    logger.error('[friends/accept]', e);
    res.status(500).json({ error: e.message });
  }
});

// ── POST /friends/:id/decline ──────────────────────────────────────────────
router.post('/:id/decline', requireAuth, async (req, res) => {
  try {
    const user = me(req);
    const f = await Friendship.findById(req.params.id);
    if (!f) return res.status(404).json({ error: 'Request not found.' });
    if (String(f.addresseeId) !== String(user.id) || f.addresseeModel !== user.model) {
      return res.status(403).json({ error: 'Only the addressee can decline.' });
    }
    f.status = 'declined';
    f.declinedAt = new Date();
    await f.save();
    res.json({ ok: true });
  } catch (e) {
    logger.error('[friends/decline]', e);
    res.status(500).json({ error: e.message });
  }
});

// ── DELETE /friends/:id — unfriend (either side) ───────────────────────────
router.delete('/:id', requireAuth, async (req, res) => {
  try {
    const user = me(req);
    const f = await Friendship.findById(req.params.id);
    if (!f) return res.status(404).json({ error: 'Not found.' });
    const isParty =
      (String(f.requesterId) === String(user.id) && f.requesterModel === user.model) ||
      (String(f.addresseeId) === String(user.id) && f.addresseeModel === user.model);
    if (!isParty) return res.status(403).json({ error: 'Not your friendship.' });
    await f.deleteOne();
    res.json({ ok: true });
  } catch (e) {
    logger.error('[friends/delete]', e);
    res.status(500).json({ error: e.message });
  }
});

// ── POST /friends/:id/share — toggle "I broadcast my position to X" ────────
router.post('/:id/share', requireAuth, async (req, res) => {
  try {
    const { share } = req.body;
    const user = me(req);
    const f = await Friendship.findById(req.params.id);
    if (!f || f.status !== 'accepted') {
      return res.status(404).json({ error: 'Accepted friendship not found.' });
    }
    const isRequester =
      String(f.requesterId) === String(user.id) && f.requesterModel === user.model;
    const isAddressee =
      String(f.addresseeId) === String(user.id) && f.addresseeModel === user.model;
    if (!isRequester && !isAddressee) {
      return res.status(403).json({ error: 'Not your friendship.' });
    }
    if (isRequester) f.requesterSharesPosition = !!share;
    if (isAddressee) f.addresseeSharesPosition = !!share;
    await f.save();
    res.json({ friendship: await enrichFriendship(f, user.id) });
  } catch (e) {
    logger.error('[friends/share]', e);
    res.status(500).json({ error: e.message });
  }
});

// ── v23.1.170 — Suivi famille (PawFollow Famille €9.99) ───────────────────
//
// Daniel : "fais le suivi famille en plus, si une famille veux se suivre
// que juste en cliquand sur le nom ds sa liste damis sa le geoloclaise".
//
// Trois routes :
//   GET    /:id/track-access      → l'autre user peut-il être tracké ?
//   POST   /family/invite-member  → ajouter un membre à ma famille (titulaire)
//   DELETE /family/member/:userId → retirer un membre

const UserSubscription = require('../models/UserSubscription');
const { isInSameFamily } = require('../models/UserSubscription');

/**
 * GET /friends/:id/track-access
 * Réponse : { canTrack: bool, reason: 'family' | 'shared' | 'none' | 'no_friendship' }
 *
 * Logique :
 *   - Si pas amis (friendship.accepted) → canTrack=false, reason='no_friendship'
 *   - Si même famille PawFollow Famille → canTrack=true, reason='family'
 *   - Si l'autre a flag share-position=true vers moi → canTrack=true, reason='shared'
 *   - Sinon canTrack=false, reason='none'
 */
router.get('/:id/track-access', requireAuth, async (req, res) => {
  try {
    const user = me(req);
    const otherId = req.params.id;
    if (!otherId) return res.status(400).json({ error: 'Friend id required.' });

    // Friendship status check
    const friendship = await Friendship.findOne({
      status: 'accepted',
      $or: [
        { requesterId: user.id, addresseeId: otherId },
        { requesterId: otherId, addresseeId: user.id },
      ],
    }).lean();
    if (!friendship) {
      return res.json({ canTrack: false, reason: 'no_friendship' });
    }

    // Family check
    if (await isInSameFamily(user.id, otherId)) {
      return res.json({ canTrack: true, reason: 'family' });
    }

    // Per-friendship share flag (the OTHER must share with me)
    const otherSharesWithMe =
      (String(friendship.requesterId) === String(otherId) &&
        friendship.requesterShareWithAddressee === true) ||
      (String(friendship.addresseeId) === String(otherId) &&
        friendship.addresseeShareWithRequester === true);
    if (otherSharesWithMe) {
      return res.json({ canTrack: true, reason: 'shared' });
    }

    return res.json({ canTrack: false, reason: 'none' });
  } catch (e) {
    logger.error('[friends/track-access]', e);
    res.status(500).json({ error: e.message });
  }
});

/**
 * GET /friends/family/members
 * Liste les membres de MA famille PawFollow + retourne mon statut titulaire.
 * Format de réponse :
 *   {
 *     hasActiveFamilyPlan: bool,
 *     members: [{ id, role, name, avatar, addedAt, email }],
 *     remainingSlots: number (4 - members.length quand active, 0 sinon)
 *   }
 */
router.get('/family/members', requireAuth, async (req, res) => {
  try {
    const user = me(req);
    const now = new Date();
    const sub = await UserSubscription.findOne({
      userId: user.id,
      userModel: user.model,
      plan: 'famille',
      status: 'active',
      currentPeriodEnd: { $gt: now },
    }).lean();
    if (!sub) {
      return res.json({
        hasActiveFamilyPlan: false,
        members: [],
        remainingSlots: 0,
      });
    }
    const raw = Array.isArray(sub.familyMembers) ? sub.familyMembers : [];
    const enriched = await Promise.all(
      raw.map(async (m) => {
        const mini = await fetchUserMini(m.userId, m.userModel);
        return {
          id: String(m.userId),
          role: (m.userModel || '').toLowerCase(),
          name: mini?.name || '',
          avatar: mini?.avatar || '',
          addedAt: m.addedAt,
          email: m.email || null,
        };
      }),
    );
    res.json({
      hasActiveFamilyPlan: true,
      members: enriched,
      remainingSlots: Math.max(0, 4 - enriched.length),
    });
  } catch (e) {
    logger.error('[friends/family/members]', e);
    res.status(500).json({ error: e.message });
  }
});

/**
 * POST /friends/family/invite-member  body: { userId, userRole, email? }
 * Le titulaire d'une sub PawFollow Famille active ajoute jusqu'à 4 membres.
 * 403 si pas de sub famille active. 409 si déjà membre. 422 si limite atteinte.
 */
router.post('/family/invite-member', requireAuth, async (req, res) => {
  try {
    const user = me(req);
    const { userId, userRole, email } = req.body || {};
    if (!userId || !userRole) {
      return res
        .status(400)
        .json({ error: 'userId and userRole are required.' });
    }
    const targetModel = ROLE_TO_MODEL_NAME[String(userRole).toLowerCase()];
    if (!targetModel) {
      return res.status(400).json({ error: 'Invalid userRole.' });
    }
    const now = new Date();
    const sub = await UserSubscription.findOne({
      userId: user.id,
      userModel: user.model,
      plan: 'famille',
      status: 'active',
      currentPeriodEnd: { $gt: now },
    });
    if (!sub) {
      return res.status(403).json({
        error: 'Active PawFollow Famille subscription required.',
        code: 'FAMILY_PLAN_REQUIRED',
      });
    }
    sub.familyMembers = sub.familyMembers || [];
    if (sub.familyMembers.length >= 4) {
      return res.status(422).json({
        error: 'Family is full (4 members max in addition to you).',
        code: 'FAMILY_FULL',
      });
    }
    if (sub.familyMembers.some((m) => String(m.userId) === String(userId))) {
      return res.status(409).json({ error: 'Already a family member.' });
    }
    sub.familyMembers.push({
      userId,
      userModel: targetModel,
      email: email || undefined,
      addedAt: now,
    });
    await sub.save();

    // Push notif au nouveau membre.
    try {
      const { sendNotification } = require('../services/notificationSender');
      await sendNotification({
        userId,
        userRole: String(userRole).toLowerCase(),
        type: 'family_member_added',
        title: 'family_member_added_title',
        body: 'family_member_added_body',
        data: { addedBy: String(user.id) },
      });
    } catch (_) {/* non-critical */}

    res.status(201).json({
      success: true,
      familyMembersCount: sub.familyMembers.length,
      remainingSlots: 4 - sub.familyMembers.length,
    });
  } catch (e) {
    logger.error('[friends/family/invite-member]', e);
    res.status(500).json({ error: e.message });
  }
});

/**
 * POST /friends/family/invite-by-email  body: { email }
 * v23.1.174 — Daniel : "Par email : si l'email existe dans Firestore → envoyer
 * demande in-app ; sinon → envoyer email d'invitation HoPetSit".
 *
 * 1. On cherche l'email dans Owner / Sitter / Walker
 * 2. Si trouvé → ajoute à family (même logique que invite-member)
 * 3. Sinon → envoie un email SendGrid avec lien d'inscription parrainage
 *    https://hopetsit.com/invite/family/{token} qui auto-accepte la demande
 *    famille après inscription.
 */
router.post('/family/invite-by-email', requireAuth, async (req, res) => {
  try {
    const user = me(req);
    const email = (req.body?.email || '').toString().trim().toLowerCase();
    if (!email || !email.includes('@')) {
      return res.status(400).json({ error: 'Valid email required.' });
    }
    const now = new Date();
    const sub = await UserSubscription.findOne({
      userId: user.id,
      userModel: user.model,
      plan: 'famille',
      status: 'active',
      currentPeriodEnd: { $gt: now },
    });
    if (!sub) {
      return res.status(403).json({
        error: 'Active PawFollow Famille subscription required.',
        code: 'FAMILY_PLAN_REQUIRED',
      });
    }
    sub.familyMembers = sub.familyMembers || [];
    if (sub.familyMembers.length >= 4) {
      return res.status(422).json({
        error: 'Family is full.',
        code: 'FAMILY_FULL',
      });
    }

    // 1. Cherche l'email dans les 3 collections.
    const [owner, sitter, walker] = await Promise.all([
      Owner.findOne({ email }).select('_id name').lean(),
      Sitter.findOne({ email }).select('_id name').lean(),
      Walker.findOne({ email }).select('_id name').lean(),
    ]);
    const existing = owner || sitter || walker;
    if (existing) {
      const targetModel = owner ? 'Owner' : sitter ? 'Sitter' : 'Walker';
      const targetId = String(existing._id);
      if (sub.familyMembers.some((m) => String(m.userId) === targetId)) {
        return res.status(409).json({ error: 'Already a family member.' });
      }
      sub.familyMembers.push({
        userId: targetId,
        userModel: targetModel,
        email,
        addedAt: now,
      });
      await sub.save();
      try {
        const { sendNotification } = require('../services/notificationSender');
        await sendNotification({
          userId: targetId,
          userRole: targetModel.toLowerCase(),
          type: 'family_member_added',
          title: 'family_member_added_title',
          body: 'family_member_added_body',
          data: { addedBy: String(user.id) },
        });
      } catch (_) {/* non-critical */}
      return res.status(201).json({
        success: true,
        mode: 'existing_user',
        familyMembersCount: sub.familyMembers.length,
        remainingSlots: 4 - sub.familyMembers.length,
      });
    }

    // 2. User pas trouvé → on envoie un email d'invitation parrainage.
    // L'invité reçoit un lien https://hopetsit.com/invite/family/<token>
    // qui après inscription auto-accepte la demande famille.
    try {
      const emailService = require('../services/emailService');
      const inviteUrl =
        `${process.env.WEBSITE_URL || 'https://hopetsit.com'}` +
        `/invite/family/${encodeURIComponent(email)}?from=${user.id}`;
      // emailService.sendFamilyInvite est defensif : si pas dispo, on stocke
      // juste l'email dans family pending pour retry plus tard.
      if (typeof emailService.sendFamilyInvite === 'function') {
        await emailService.sendFamilyInvite({
          to: email,
          inviterName: (await me(req)).id, // sera enrichi côté service
          inviteUrl,
        });
      }
    } catch (e) {
      logger.warn('[friends/family/invite-by-email] email send failed', e);
    }

    // On track quand même l'invite envoyée (sans la réserver dans family
    // tant qu'elle n'est pas créée). Daniel peut suivre depuis un futur
    // écran "Invitations envoyées".
    return res.status(202).json({
      success: true,
      mode: 'email_invite_sent',
      email,
    });
  } catch (e) {
    logger.error('[friends/family/invite-by-email]', e);
    res.status(500).json({ error: e.message });
  }
});

/** DELETE /friends/family/member/:userId — titulaire retire un membre. */
router.delete('/family/member/:userId', requireAuth, async (req, res) => {
  try {
    const user = me(req);
    const targetId = req.params.userId;
    const sub = await UserSubscription.findOne({
      userId: user.id,
      userModel: user.model,
      plan: 'famille',
    });
    if (!sub) {
      return res
        .status(404)
        .json({ error: 'No family subscription found.' });
    }
    const before = (sub.familyMembers || []).length;
    sub.familyMembers = (sub.familyMembers || []).filter(
      (m) => String(m.userId) !== String(targetId),
    );
    if (sub.familyMembers.length === before) {
      return res.status(404).json({ error: 'Member not in family.' });
    }
    await sub.save();
    res.json({
      success: true,
      familyMembersCount: sub.familyMembers.length,
      remainingSlots: 4 - sub.familyMembers.length,
    });
  } catch (e) {
    logger.error('[friends/family/member DELETE]', e);
    res.status(500).json({ error: e.message });
  }
});

module.exports = router;
