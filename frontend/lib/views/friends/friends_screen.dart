import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';
import 'package:hopetsit/controllers/auth_controller.dart';
import 'package:hopetsit/controllers/friend_controller.dart';
import 'package:hopetsit/models/friendship_model.dart';
import 'package:hopetsit/utils/app_colors.dart';
import 'package:hopetsit/utils/storage_keys.dart';
import 'package:hopetsit/views/boost/coin_shop_screen.dart';
import 'package:hopetsit/views/map/paw_map_screen.dart';
import 'package:hopetsit/widgets/app_text.dart';
import 'package:hopetsit/widgets/custom_snackbar_widget.dart';
import 'package:get_storage/get_storage.dart';
import 'package:share_plus/share_plus.dart';

/// Friends management screen — 2 tabs.
///   1. Mes amis — accepted friendships with a per-friend "share my position"
///      toggle and an "unfriend" option.
///   2. Demandes — incoming requests (accept/decline) + outgoing (pending).
class FriendsScreen extends StatelessWidget {
  const FriendsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final FriendController controller = Get.isRegistered<FriendController>()
        ? Get.find<FriendController>()
        : Get.put(FriendController());

    // v23.1.172 — Daniel : "le truc de famille je le vois pas". On ajoute
    // un 3e onglet "Famille" qui montre les membres de PawFollow Famille
    // + permet d'inviter / retirer depuis la liste d'amis acceptés.
    // On précharge la famille à l'ouverture de l'écran.
    controller.loadFamily();
    return DefaultTabController(
      length: 3,
      child: Scaffold(
        backgroundColor: AppColors.scaffold(context),
        appBar: AppBar(
          backgroundColor: AppColors.appBar(context),
          elevation: 0,
          title: Row(
            children: [
              Text('👥', style: TextStyle(fontSize: 20.sp)),
              SizedBox(width: 8.w),
              InterText(
                text: 'friends_screen_title'.tr,
                fontSize: 18.sp,
                fontWeight: FontWeight.w700,
                color: AppColors.textPrimary(context),
              ),
            ],
          ),
          // v23.1.170 — Daniel : "la demande inviter mais normal ou par
          // mail ne marche pas, il faut corriger". On ajoute un bouton
          // partage en haut à droite qui balance un message d'invitation
          // + lien deep-link via SharePlus (le destinataire peut le coller
          // dans WhatsApp/email/sms etc.).
          actions: [
            IconButton(
              icon: Icon(Icons.ios_share_rounded,
                  color: AppColors.primaryColor, size: 22.sp),
              tooltip: 'friends_invite_link_tooltip'.tr,
              onPressed: () async {
                try {
                  // v23.1.170 — On lit le profil utilisateur depuis le
                  // GetStorage (clé canonique 'user_profile') pour extraire
                  // id + name. Fallback générique si pas trouvé.
                  String myId = '';
                  String myName = '';
                  try {
                    final raw = GetStorage().read(StorageKeys.userProfile);
                    if (raw is Map) {
                      myId = (raw['id'] ?? raw['_id'] ?? '').toString();
                      myName = (raw['name'] ?? '').toString();
                    }
                  } catch (_) {/* noop */}
                  final link = myId.isNotEmpty
                      ? 'https://hopetsit.com/invite?from=$myId'
                      : 'https://hopetsit.com';
                  final text = 'friends_invite_message'.trParams({
                    'name': myName.isEmpty ? 'HoPetSit' : myName,
                    'link': link,
                  });
                  await SharePlus.instance.share(ShareParams(
                    text: text,
                    subject: 'friends_invite_subject'.tr,
                  ));
                } catch (e) {
                  CustomSnackbar.showError(
                    title: 'common_error'.tr,
                    message: e.toString(),
                  );
                }
              },
            ),
          ],
          bottom: TabBar(
            labelColor: AppColors.primaryColor,
            unselectedLabelColor: AppColors.greyText,
            indicatorColor: AppColors.primaryColor,
            tabs: [
              Tab(icon: const Icon(Icons.people_rounded),
                  text: 'friends_tab_friends'.tr),
              Tab(
                icon: Obx(() {
                  final n = controller.incomingRequests.length;
                  return Stack(
                    clipBehavior: Clip.none,
                    children: [
                      const Icon(Icons.mail_outline_rounded),
                      if (n > 0)
                        Positioned(
                          right: -6,
                          top: -6,
                          child: Container(
                            padding: EdgeInsets.all(3.w),
                            decoration: const BoxDecoration(
                              color: Colors.red,
                              shape: BoxShape.circle,
                            ),
                            constraints: BoxConstraints(minWidth: 14.w, minHeight: 14.w),
                            child: Center(
                              child: Text(
                                '$n',
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 9.sp,
                                  fontWeight: FontWeight.w700,
                                ),
                              ),
                            ),
                          ),
                        ),
                    ],
                  );
                }),
                text: 'friends_tab_requests'.tr,
              ),
              // v23.1.172 — Onglet Famille (PawFollow Famille).
              Tab(
                icon: const Icon(Icons.family_restroom_rounded),
                text: 'friends_tab_family'.tr,
              ),
            ],
          ),
        ),
        body: TabBarView(
          children: [
            _FriendsTab(controller: controller),
            _RequestsTab(controller: controller),
            _FamilyTab(controller: controller),
          ],
        ),
        // v23.1 part 69 — Bug 9 : Daniel "Comment sajoute les amis ?".
        // Adds a clear "+ Ajouter un ami" FAB that opens a search-by-
        // email dialog. The empty state was just text so the user had
        // no idea how to find people. FAB is always visible.
        floatingActionButton: FloatingActionButton.extended(
          backgroundColor: AppColors.primaryColor,
          icon: const Icon(Icons.person_add_alt_1_rounded, color: Colors.white),
          label: Text(
            'Ajouter un ami',
            style: TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.w700,
              fontSize: 14.sp,
            ),
          ),
          onPressed: () => _showAddFriendDialog(context, controller),
        ),
      ),
    );
  }

  /// v23.1 part 69 — Bug 9 : add-friend dialog with email/name search.
  void _showAddFriendDialog(BuildContext context, FriendController controller) {
    final searchCtrl = TextEditingController();
    final results = <Map<String, dynamic>>[].obs;
    final loading = false.obs;

    showDialog<void>(
      context: context,
      builder: (ctx) => Dialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20.r)),
        child: Padding(
          padding: EdgeInsets.all(20.w),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Row(
                children: [
                  Icon(Icons.person_add_alt_1_rounded,
                      color: AppColors.primaryColor, size: 24.sp),
                  SizedBox(width: 8.w),
                  Expanded(
                    child: InterText(
                      text: 'Ajouter un ami',
                      fontSize: 16.sp,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                  IconButton(
                    icon: Icon(Icons.close_rounded, size: 22.sp),
                    onPressed: () => Navigator.of(ctx).pop(),
                  ),
                ],
              ),
              SizedBox(height: 8.h),
              InterText(
                text: 'Cherche par email ou nom (min. 2 caractères)',
                fontSize: 12.sp,
                color: AppColors.greyText,
              ),
              SizedBox(height: 12.h),
              TextField(
                controller: searchCtrl,
                autofocus: true,
                decoration: InputDecoration(
                  hintText: 'ami@example.com ou Daniel',
                  prefixIcon: const Icon(Icons.search_rounded),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(14.r),
                  ),
                ),
                onChanged: (q) async {
                  if (q.length < 2) {
                    results.clear();
                    return;
                  }
                  loading.value = true;
                  results.assignAll(await controller.searchUsers(q));
                  loading.value = false;
                },
              ),
              SizedBox(height: 12.h),
              SizedBox(
                height: 240.h,
                child: Obx(() {
                  if (loading.value) {
                    return const Center(child: CircularProgressIndicator());
                  }
                  if (results.isEmpty) {
                    return Center(
                      child: InterText(
                        text: searchCtrl.text.isEmpty
                            ? 'Tape un email ou un nom'
                            : 'Aucun résultat',
                        fontSize: 13.sp,
                        color: AppColors.greyText,
                      ),
                    );
                  }
                  return ListView.separated(
                    itemCount: results.length,
                    separatorBuilder: (_, __) => Divider(
                      height: 1,
                      color: AppColors.divider(context),
                    ),
                    itemBuilder: (_, i) {
                      final u = results[i];
                      final id = (u['id'] ?? '').toString();
                      final role = (u['role'] ?? '').toString();
                      final name = (u['name'] ?? '').toString();
                      final email = (u['email'] ?? '').toString();
                      final avatar = (u['avatar'] ?? '').toString();
                      return ListTile(
                        leading: CircleAvatar(
                          radius: 18.r,
                          backgroundColor:
                              AppColors.primaryColor.withValues(alpha: 0.15),
                          backgroundImage:
                              avatar.isNotEmpty ? NetworkImage(avatar) : null,
                          child: avatar.isEmpty
                              ? Icon(Icons.person,
                                  size: 18.sp, color: AppColors.primaryColor)
                              : null,
                        ),
                        title: Text(name.isNotEmpty ? name : email),
                        subtitle: Text('$role · $email'),
                        trailing: ElevatedButton(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: AppColors.primaryColor,
                            foregroundColor: Colors.white,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(20.r),
                            ),
                            padding: EdgeInsets.symmetric(
                                horizontal: 12.w, vertical: 6.h),
                          ),
                          onPressed: () async {
                            // v23.1.172 — Daniel : "quand je demande
                            // invitation amis sa met erreur impossible".
                            // On lit maintenant le code d'erreur backend
                            // pour expliquer la VRAIE cause au user.
                            final err = await controller.sendRequest(id, role);
                            if (!context.mounted) return;
                            if (err.isEmpty) {
                              Navigator.of(ctx).pop();
                              CustomSnackbar.showSuccess(
                                title: 'friends_invite_sent_title'.tr,
                                message: 'friends_invite_sent_msg'
                                    .trParams({'name': name}),
                              );
                            } else {
                              final msg = err == 'ALREADY_PENDING'
                                  ? 'friends_invite_err_already_pending'.tr
                                  : err == 'ALREADY_ACCEPTED'
                                      ? 'friends_invite_err_already_accepted'.tr
                                      : err == 'SELF'
                                          ? 'friends_invite_err_self'.tr
                                          : err;
                              CustomSnackbar.showError(
                                title: 'common_error'.tr,
                                message: msg,
                              );
                            }
                          },
                          child: const Text('Inviter',
                              style: TextStyle(fontSize: 12)),
                        ),
                      );
                    },
                  );
                }),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _FriendsTab extends StatelessWidget {
  const _FriendsTab({required this.controller});
  final FriendController controller;

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      onRefresh: controller.refresh,
      child: Obx(() {
        if (controller.isLoading.value && controller.friends.isEmpty) {
          return const Center(child: CircularProgressIndicator());
        }
        if (controller.friends.isEmpty) {
          return ListView(
            physics: const AlwaysScrollableScrollPhysics(),
            padding: EdgeInsets.all(24.w),
            children: [
              SizedBox(height: 40.h),
              Center(
                child: Column(
                  children: [
                    Text('🐾', style: TextStyle(fontSize: 50.sp)),
                    SizedBox(height: 12.h),
                    InterText(
                      text: 'Pas encore d\'amis',
                      fontSize: 16.sp,
                      fontWeight: FontWeight.w700,
                      color: AppColors.textPrimary(context),
                    ),
                    SizedBox(height: 4.h),
                    InterText(
                      text: 'Ajoute des amis pour les voir en temps réel sur la PawMap.',
                      fontSize: 13.sp,
                      color: AppColors.greyText,
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              ),
            ],
          );
        }
        return ListView.separated(
          padding: EdgeInsets.all(12.w),
          physics: const AlwaysScrollableScrollPhysics(),
          itemCount: controller.friends.length,
          separatorBuilder: (_, __) => SizedBox(height: 10.h),
          itemBuilder: (_, i) => _FriendTile(
            friendship: controller.friends[i],
            controller: controller,
          ),
        );
      }),
    );
  }
}

class _FriendTile extends StatelessWidget {
  const _FriendTile({required this.friendship, required this.controller});

  final Friendship friendship;
  final FriendController controller;

  @override
  Widget build(BuildContext context) {
    final other = friendship.other!;
    final roleColor = {
      'Owner': AppColors.primaryColor,
      'Sitter': AppColors.sitterAccent,
      'Walker': AppColors.greenColor,
    }[other.model] ?? AppColors.primaryColor;

    // v23.1.170 — Daniel : "si une famille veux se suivre que juste en
    // cliquand sur le nom ds sa liste damis par exemplet sa le geoloclaise".
    // Tap sur la card → vérifie via /friends/:id/track-access si on peut
    // tracker (famille PawFollow Famille auto, OU friend share-position
    // activé), puis ouvre la PawMap. Sinon snackbar + lien upsell.
    return InkWell(
      borderRadius: BorderRadius.circular(16.r),
      onTap: () async {
        // Quick local check : si l'ami partage avec moi → on évite l'aller-retour.
        if (friendship.theirSharePosition) {
          Get.to(() => const PawMapScreen());
          return;
        }
        // Sinon on demande au backend (la famille bypass le share flag).
        final access = await controller.checkTrackAccess(other.id);
        final canTrack = access['canTrack'] == true;
        if (canTrack) {
          Get.to(() => const PawMapScreen());
          return;
        }
        CustomSnackbar.showInfo(
          title: 'friends_tap_not_shared_title'.tr,
          message: 'friends_tap_not_shared_msg'
              .trParams({'name': other.name.isEmpty ? '—' : other.name}),
        );
      },
      child: Container(
      padding: EdgeInsets.all(12.w),
      decoration: BoxDecoration(
        color: AppColors.card(context),
        borderRadius: BorderRadius.circular(16.r),
        boxShadow: AppColors.cardShadow(context),
      ),
      child: Row(
        children: [
          CircleAvatar(
            radius: 24.r,
            backgroundColor: roleColor.withValues(alpha: 0.15),
            child: other.avatar.isNotEmpty
                ? ClipOval(
                    child: CachedNetworkImage(
                      imageUrl: other.avatar,
                      width: 48.r,
                      height: 48.r,
                      fit: BoxFit.cover,
                      errorWidget: (_, __, ___) =>
                          Icon(Icons.person, color: roleColor, size: 22.sp),
                    ),
                  )
                : Icon(Icons.person, color: roleColor, size: 22.sp),
          ),
          SizedBox(width: 12.w),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                InterText(
                  text: other.name.isEmpty ? 'Utilisateur' : other.name,
                  fontSize: 14.sp,
                  fontWeight: FontWeight.w700,
                  color: AppColors.textPrimary(context),
                ),
                SizedBox(height: 2.h),
                Row(
                  children: [
                    Container(
                      padding: EdgeInsets.symmetric(horizontal: 6.w, vertical: 1.h),
                      decoration: BoxDecoration(
                        color: roleColor.withValues(alpha: 0.15),
                        borderRadius: BorderRadius.circular(6.r),
                      ),
                      child: InterText(
                        text: other.model,
                        fontSize: 9.sp,
                        fontWeight: FontWeight.w700,
                        color: roleColor,
                      ),
                    ),
                    if (other.city.isNotEmpty) ...[
                      SizedBox(width: 6.w),
                      InterText(
                        text: other.city,
                        fontSize: 11.sp,
                        color: AppColors.greyText,
                      ),
                    ],
                  ],
                ),
              ],
            ),
          ),
          // v18.9.8 — Share position toggle : couleur selon rôle actif
          // (orange owner / bleu sitter / vert walker) au lieu de toujours
          // orange hardcodé.
          Column(
            children: [
              Transform.scale(
                scale: 0.75,
                child: Switch(
                  value: friendship.mySharePosition,
                  activeThumbColor: AppColors.roleAccent(
                    Get.find<AuthController>().userRole.value,
                  ),
                  onChanged: (v) => controller.setSharePosition(friendship.id, v),
                ),
              ),
              InterText(
                text: 'friends_share_position_label'.tr,
                fontSize: 9.sp,
                color: AppColors.greyText,
              ),
            ],
          ),
          SizedBox(width: 4.w),
          PopupMenuButton<String>(
            icon: Icon(Icons.more_vert, size: 18.sp, color: AppColors.greyText),
            onSelected: (v) async {
              if (v == 'unfriend') {
                final ok = await controller.unfriend(friendship.id);
                if (ok) {
                  CustomSnackbar.showSuccess(
                    title: 'Suppression',
                    message: 'Ami retiré de ta liste.',
                  );
                }
              }
            },
            itemBuilder: (_) => const [
              PopupMenuItem(value: 'unfriend', child: Text('Retirer')),
            ],
          ),
        ],
      ),
      ),
    );
  }
}

class _RequestsTab extends StatelessWidget {
  const _RequestsTab({required this.controller});
  final FriendController controller;

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      onRefresh: controller.refresh,
      child: Obx(() {
        final incoming = controller.incomingRequests;
        final outgoing = controller.outgoingRequests;
        if (incoming.isEmpty && outgoing.isEmpty) {
          return ListView(
            physics: const AlwaysScrollableScrollPhysics(),
            padding: EdgeInsets.all(24.w),
            children: [
              SizedBox(height: 60.h),
              Center(
                child: InterText(
                  text: 'friends_no_pending_request'.tr,
                  fontSize: 13.sp,
                  color: AppColors.greyText,
                ),
              ),
            ],
          );
        }
        return ListView(
          padding: EdgeInsets.all(12.w),
          children: [
            if (incoming.isNotEmpty) ...[
              _sectionHeader(context, 'Reçues'),
              ...incoming.map(
                (f) => _IncomingTile(friendship: f, controller: controller),
              ),
              SizedBox(height: 20.h),
            ],
            if (outgoing.isNotEmpty) ...[
              _sectionHeader(context, 'Envoyées'),
              ...outgoing.map((f) => _OutgoingTile(friendship: f)),
            ],
          ],
        );
      }),
    );
  }

  Widget _sectionHeader(BuildContext context, String text) {
    return Padding(
      padding: EdgeInsets.only(bottom: 8.h, top: 4.h, left: 4.w),
      child: InterText(
        text: text,
        fontSize: 12.sp,
        fontWeight: FontWeight.w700,
        color: AppColors.greyText,
      ),
    );
  }
}

class _IncomingTile extends StatelessWidget {
  const _IncomingTile({required this.friendship, required this.controller});
  final Friendship friendship;
  final FriendController controller;

  @override
  Widget build(BuildContext context) {
    final other = friendship.other;
    return Container(
      margin: EdgeInsets.only(bottom: 10.h),
      padding: EdgeInsets.all(12.w),
      decoration: BoxDecoration(
        color: AppColors.card(context),
        borderRadius: BorderRadius.circular(14.r),
        boxShadow: AppColors.cardShadow(context),
      ),
      child: Row(
        children: [
          CircleAvatar(
            radius: 22.r,
            backgroundColor: AppColors.primaryColor.withValues(alpha: 0.15),
            child: Icon(Icons.person, color: AppColors.primaryColor, size: 22.sp),
          ),
          SizedBox(width: 12.w),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                InterText(
                  text: other?.name ?? 'Utilisateur',
                  fontSize: 13.sp,
                  fontWeight: FontWeight.w700,
                  color: AppColors.textPrimary(context),
                ),
                SizedBox(height: 2.h),
                InterText(
                  text: 'souhaite être ami avec toi',
                  fontSize: 11.sp,
                  color: AppColors.greyText,
                ),
              ],
            ),
          ),
          IconButton(
            icon: Icon(Icons.check_circle, color: Colors.green, size: 26.sp),
            onPressed: () async {
              final ok = await controller.accept(friendship.id);
              if (ok) {
                CustomSnackbar.showSuccess(
                  title: 'Accepté',
                  message: 'Vous êtes maintenant amis.',
                );
              }
            },
          ),
          IconButton(
            icon: Icon(Icons.cancel, color: Colors.red, size: 26.sp),
            onPressed: () => controller.decline(friendship.id),
          ),
        ],
      ),
    );
  }
}

class _OutgoingTile extends StatelessWidget {
  const _OutgoingTile({required this.friendship});
  final Friendship friendship;

  @override
  Widget build(BuildContext context) {
    final other = friendship.other;
    return Container(
      margin: EdgeInsets.only(bottom: 8.h),
      padding: EdgeInsets.all(12.w),
      decoration: BoxDecoration(
        color: AppColors.card(context),
        borderRadius: BorderRadius.circular(14.r),
        border: Border.all(color: AppColors.divider(context)),
      ),
      child: Row(
        children: [
          CircleAvatar(
            radius: 20.r,
            backgroundColor: Colors.grey.shade200,
            child: Icon(Icons.schedule, color: AppColors.greyText, size: 18.sp),
          ),
          SizedBox(width: 10.w),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                InterText(
                  text: other?.name ?? 'Utilisateur',
                  fontSize: 12.sp,
                  fontWeight: FontWeight.w600,
                  color: AppColors.textPrimary(context),
                ),
                InterText(
                  text: 'En attente…',
                  fontSize: 11.sp,
                  color: AppColors.greyText,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// ── v23.1.172 — Famille tab (PawFollow Famille €9.99) ─────────────────────
//
// Daniel : "le truc de famille je le vois pas non plus". Cet onglet montre :
//   - Si pas d'abo Famille actif : CTA "Souscris PawFollow Famille"
//   - Si abo actif : liste des membres + bouton "+ Inviter un ami" (filtre
//     parmi les amis acceptés) + bouton "Retirer" par membre.

class _FamilyTab extends StatelessWidget {
  const _FamilyTab({required this.controller});
  final FriendController controller;

  @override
  Widget build(BuildContext context) {
    final accent = AppColors.roleAccent(
      Get.find<AuthController>().userRole.value,
    );
    return RefreshIndicator(
      onRefresh: () => controller.loadFamily(),
      child: Obx(() {
        if (!controller.hasFamilyPlan.value) {
          return ListView(
            physics: const AlwaysScrollableScrollPhysics(),
            padding: EdgeInsets.all(24.w),
            children: [
              SizedBox(height: 40.h),
              Container(
                padding: EdgeInsets.all(20.w),
                decoration: BoxDecoration(
                  color: accent.withValues(alpha: 0.08),
                  borderRadius: BorderRadius.circular(16.r),
                  border: Border.all(color: accent.withValues(alpha: 0.25)),
                ),
                child: Column(
                  children: [
                    Icon(Icons.family_restroom_rounded,
                        size: 56.sp, color: accent),
                    SizedBox(height: 12.h),
                    InterText(
                      text: 'family_no_plan_title'.tr,
                      fontSize: 16.sp,
                      fontWeight: FontWeight.w800,
                      color: AppColors.textPrimary(context),
                    ),
                    SizedBox(height: 8.h),
                    InterText(
                      text: 'family_no_plan_desc'.tr,
                      fontSize: 12.sp,
                      color: AppColors.textSecondary(context),
                    ),
                    SizedBox(height: 16.h),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton.icon(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: accent,
                          foregroundColor: Colors.white,
                          padding: EdgeInsets.symmetric(vertical: 12.h),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12.r),
                          ),
                        ),
                        icon: const Icon(Icons.shopping_cart_rounded),
                        label: Text('family_no_plan_cta'.tr),
                        onPressed: () =>
                            Get.to(() => const CoinShopScreen(initialTab: 1)),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          );
        }
        final members = controller.familyMembers;
        return ListView(
          padding: EdgeInsets.all(12.w),
          physics: const AlwaysScrollableScrollPhysics(),
          children: [
            Container(
              padding: EdgeInsets.all(14.w),
              decoration: BoxDecoration(
                color: accent.withValues(alpha: 0.08),
                borderRadius: BorderRadius.circular(14.r),
                border: Border.all(color: accent.withValues(alpha: 0.25)),
              ),
              child: Row(
                children: [
                  Icon(Icons.verified_user_rounded, color: accent, size: 24.sp),
                  SizedBox(width: 10.w),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        InterText(
                          text: 'family_header_title'.tr,
                          fontSize: 13.sp,
                          fontWeight: FontWeight.w800,
                          color: AppColors.textPrimary(context),
                        ),
                        SizedBox(height: 2.h),
                        InterText(
                          text: 'family_slots'.trParams({
                            'used': members.length.toString(),
                            'total': '4',
                          }),
                          fontSize: 11.sp,
                          color: AppColors.textSecondary(context),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            SizedBox(height: 16.h),
            if (members.isEmpty)
              Padding(
                padding: EdgeInsets.symmetric(vertical: 24.h),
                child: Center(
                  child: InterText(
                    text: 'family_empty_msg'.tr,
                    fontSize: 13.sp,
                    color: AppColors.greyText,
                  ),
                ),
              )
            else
              ...members.map((m) => _FamilyMemberTile(
                    member: m,
                    controller: controller,
                  )),
            SizedBox(height: 12.h),
            if (controller.familyRemainingSlots.value > 0)
              SizedBox(
                width: double.infinity,
                child: OutlinedButton.icon(
                  icon: const Icon(Icons.person_add_alt_1_rounded),
                  label: Text('family_add_member_btn'.tr),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: accent,
                    side: BorderSide(color: accent),
                    padding: EdgeInsets.symmetric(vertical: 12.h),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12.r),
                    ),
                  ),
                  onPressed: () => _showAddMemberSheet(context, controller),
                ),
              )
            else
              Padding(
                padding: EdgeInsets.symmetric(vertical: 8.h),
                child: Center(
                  child: InterText(
                    text: 'family_full_msg'.tr,
                    fontSize: 12.sp,
                    color: AppColors.greyText,
                  ),
                ),
              ),
          ],
        );
      }),
    );
  }

  void _showAddMemberSheet(
    BuildContext context,
    FriendController controller,
  ) {
    final eligibleFriends = controller.friends
        .where((f) =>
            f.other != null &&
            !controller.familyMembers
                .any((m) => m['id'] == f.other!.id))
        .toList();
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (ctx) => Container(
        padding: EdgeInsets.all(16.w),
        constraints: BoxConstraints(maxHeight: 400.h),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Row(
              children: [
                Icon(Icons.family_restroom_rounded,
                    color: AppColors.primaryColor, size: 24.sp),
                SizedBox(width: 8.w),
                Expanded(
                  child: InterText(
                    text: 'family_add_member_title'.tr,
                    fontSize: 16.sp,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.close_rounded),
                  onPressed: () => Navigator.of(ctx).pop(),
                ),
              ],
            ),
            SizedBox(height: 8.h),
            InterText(
              text: eligibleFriends.isEmpty
                  ? 'family_add_member_no_friends'.tr
                  : 'family_add_member_pick'.tr,
              fontSize: 12.sp,
              color: AppColors.greyText,
            ),
            SizedBox(height: 12.h),
            Expanded(
              child: ListView.separated(
                itemCount: eligibleFriends.length,
                separatorBuilder: (_, __) => const Divider(height: 1),
                itemBuilder: (_, i) {
                  final f = eligibleFriends[i];
                  final other = f.other!;
                  return ListTile(
                    leading: CircleAvatar(
                      radius: 18.r,
                      backgroundColor:
                          AppColors.primaryColor.withValues(alpha: 0.15),
                      backgroundImage: other.avatar.isNotEmpty
                          ? NetworkImage(other.avatar)
                          : null,
                      child: other.avatar.isEmpty
                          ? Icon(Icons.person, size: 18.sp)
                          : null,
                    ),
                    title: Text(other.name.isEmpty ? 'Utilisateur' : other.name),
                    subtitle: Text(other.model),
                    trailing: ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.primaryColor,
                        foregroundColor: Colors.white,
                      ),
                      onPressed: () async {
                        final err = await controller.addFamilyMember(
                          userId: other.id,
                          userRole: other.model.toLowerCase(),
                        );
                        if (!context.mounted) return;
                        if (err.isEmpty) {
                          Navigator.of(ctx).pop();
                          CustomSnackbar.showSuccess(
                            title: 'family_member_added_title'.tr,
                            message: 'family_member_added_msg'
                                .trParams({'name': other.name}),
                          );
                        } else {
                          final msg = err == 'FAMILY_FULL'
                              ? 'family_err_full'.tr
                              : err == 'ALREADY_MEMBER'
                                  ? 'family_err_already_member'.tr
                                  : err == 'FAMILY_PLAN_REQUIRED'
                                      ? 'family_err_plan_required'.tr
                                      : err;
                          CustomSnackbar.showError(
                            title: 'common_error'.tr,
                            message: msg,
                          );
                        }
                      },
                      child: Text('family_add_btn'.tr),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _FamilyMemberTile extends StatelessWidget {
  const _FamilyMemberTile({required this.member, required this.controller});
  final Map<String, dynamic> member;
  final FriendController controller;

  @override
  Widget build(BuildContext context) {
    final name = (member['name'] ?? '').toString();
    final avatar = (member['avatar'] ?? '').toString();
    final role = (member['role'] ?? '').toString();
    final id = (member['id'] ?? '').toString();
    return Container(
      margin: EdgeInsets.only(bottom: 10.h),
      padding: EdgeInsets.all(12.w),
      decoration: BoxDecoration(
        color: AppColors.card(context),
        borderRadius: BorderRadius.circular(14.r),
        boxShadow: AppColors.cardShadow(context),
      ),
      child: Row(
        children: [
          CircleAvatar(
            radius: 22.r,
            backgroundColor: AppColors.primaryColor.withValues(alpha: 0.15),
            backgroundImage: avatar.isNotEmpty ? NetworkImage(avatar) : null,
            child: avatar.isEmpty
                ? Icon(Icons.person, color: AppColors.primaryColor, size: 20.sp)
                : null,
          ),
          SizedBox(width: 12.w),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                InterText(
                  text: name.isEmpty ? '—' : name,
                  fontSize: 14.sp,
                  fontWeight: FontWeight.w700,
                ),
                SizedBox(height: 2.h),
                InterText(
                  text: role,
                  fontSize: 11.sp,
                  color: AppColors.greyText,
                ),
              ],
            ),
          ),
          IconButton(
            icon: Icon(Icons.person_remove_rounded,
                color: AppColors.errorColor, size: 20.sp),
            tooltip: 'family_remove_member_tooltip'.tr,
            onPressed: () async {
              final ok = await controller.removeFamilyMember(id);
              if (!context.mounted) return;
              if (ok) {
                CustomSnackbar.showSuccess(
                  title: 'family_member_removed_title'.tr,
                  message: 'family_member_removed_msg'
                      .trParams({'name': name}),
                );
              }
            },
          ),
        ],
      ),
    );
  }
}
