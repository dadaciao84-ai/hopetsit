const mongoose = require('mongoose');

// v18.6 — walker conversation support.
// Avant v18.6 : sitterId required + unique{ownerId, sitterId}, donc les
// walkers ne pouvaient pas discuter avec owner (chat skip au moment de
// l'accept). Maintenant : EXACTEMENT un des deux (sitterId OU walkerId)
// est défini, enforcé par pre('validate'). Compound indexes séparés.
const conversationSchema = new mongoose.Schema(
  {
    // Booking-based conversation (legacy) : ownerId + sitter XOR walker.
    ownerId: { type: mongoose.Schema.Types.ObjectId, ref: 'Owner', default: null },
    sitterId: { type: mongoose.Schema.Types.ObjectId, ref: 'Sitter', default: null },
    walkerId: { type: mongoose.Schema.Types.ObjectId, ref: 'Walker', default: null },
    lastMessage: { type: String, default: '' },
    lastMessageAt: { type: Date, default: Date.now },
    ownerUnreadCount: { type: Number, default: 0 },
    sitterUnreadCount: { type: Number, default: 0 },
    ownerLastReadAt: { type: Date, default: null },
    sitterLastReadAt: { type: Date, default: null },

    // v23.1.201 — Daniel : "PawFollow → chat se debloque ds amis famille".
    // Support des conversations entre amis (any-role↔any-role). Cas usage :
    //   - 2 owners amis qui veulent chatter
    //   - Owner Daniel + Sitter Emma amis en dehors d'un booking
    //   - 3 walkers amis qui se retrouvent sur la PawMap
    // Quand friendChat=true, on utilise participants[] au lieu de
    // ownerId/sitter/walkerId. chatAccess autorise si meme famille
    // PawFollow OU si une friendship 'accepted' lie les 2 participants.
    friendChat: { type: Boolean, default: false },
    participants: [
      {
        userId: { type: mongoose.Schema.Types.ObjectId, required: false },
        userModel: {
          type: String,
          enum: ['Owner', 'Sitter', 'Walker'],
          required: false,
        },
        unreadCount: { type: Number, default: 0 },
        lastReadAt: { type: Date, default: null },
      },
    ],
  },
  { timestamps: true }
);

// Booking chats : owner + (sitter XOR walker).
// Friend chats : friendChat=true + exactement 2 participants.
conversationSchema.pre('validate', function (next) {
  if (this.friendChat === true) {
    if (!Array.isArray(this.participants) || this.participants.length !== 2) {
      return next(
        new Error('Friend conversation must have exactly 2 participants.'),
      );
    }
    return next();
  }
  // Legacy booking conversation : owner + sitter XOR walker.
  if (!this.ownerId) {
    return next(new Error('Booking conversation must have ownerId.'));
  }
  const hasSitter = !!this.sitterId;
  const hasWalker = !!this.walkerId;
  if (hasSitter && hasWalker) {
    return next(
      new Error('Conversation cannot target both a sitter and a walker.'),
    );
  }
  if (!hasSitter && !hasWalker) {
    return next(
      new Error('Conversation must target either a sitter or a walker.'),
    );
  }
  next();
});

// Unique per (owner, sitter) when sitterId is set — partial index.
conversationSchema.index(
  { ownerId: 1, sitterId: 1 },
  { unique: true, partialFilterExpression: { sitterId: { $type: 'objectId' } } }
);
// Unique per (owner, walker) when walkerId is set — partial index.
conversationSchema.index(
  { ownerId: 1, walkerId: 1 },
  { unique: true, partialFilterExpression: { walkerId: { $type: 'objectId' } } }
);

module.exports = mongoose.model('Conversation', conversationSchema);
