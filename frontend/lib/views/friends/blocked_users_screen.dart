// v23.1.174 — Daniel : "Manque boutons Bloquer et Supprimer dans la liste
// d'amis [...] Liste des bloqués accessible via paramètres".
//
// Écran simple qui affiche les users que j'ai bloqués via GET /blocks et
// permet de les débloquer un par un (DELETE /blocks/:id).

import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';
import 'package:hopetsit/controllers/friend_controller.dart';
import 'package:hopetsit/utils/app_colors.dart';
import 'package:hopetsit/widgets/app_text.dart';
import 'package:hopetsit/widgets/custom_snackbar_widget.dart';

class BlockedUsersScreen extends StatefulWidget {
  const BlockedUsersScreen({super.key});

  @override
  State<BlockedUsersScreen> createState() => _BlockedUsersScreenState();
}

class _BlockedUsersScreenState extends State<BlockedUsersScreen> {
  late final FriendController controller;

  @override
  void initState() {
    super.initState();
    controller = Get.isRegistered<FriendController>()
        ? Get.find<FriendController>()
        : Get.put(FriendController());
    // Refresh la liste à l'ouverture.
    WidgetsBinding.instance.addPostFrameCallback((_) {
      controller.loadBlocked();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.scaffold(context),
      appBar: AppBar(
        backgroundColor: AppColors.appBar(context),
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.arrow_back,
              color: AppColors.primaryColor, size: 24.sp),
          onPressed: () => Get.back(),
        ),
        title: PoppinsText(
          text: 'friend_blocked_list'.tr,
          fontSize: 18.sp,
          fontWeight: FontWeight.w700,
          color: AppColors.textPrimary(context),
        ),
      ),
      body: RefreshIndicator(
        onRefresh: () => controller.loadBlocked(),
        child: Obx(() {
          final blocked = controller.blockedUsers;
          if (blocked.isEmpty) {
            return ListView(
              physics: const AlwaysScrollableScrollPhysics(),
              padding: EdgeInsets.all(24.w),
              children: [
                SizedBox(height: 60.h),
                Center(
                  child: Icon(Icons.block_rounded,
                      size: 64.sp, color: AppColors.greyText),
                ),
                SizedBox(height: 12.h),
                Center(
                  child: InterText(
                    text: 'friend_blocked_empty'.tr,
                    fontSize: 14.sp,
                    color: AppColors.greyText,
                  ),
                ),
              ],
            );
          }
          return ListView.separated(
            padding: EdgeInsets.all(12.w),
            physics: const AlwaysScrollableScrollPhysics(),
            itemCount: blocked.length,
            separatorBuilder: (_, __) => SizedBox(height: 10.h),
            itemBuilder: (_, i) {
              final b = blocked[i];
              // Le backend renvoie { id, blocked: { id, name, avatar, ... },
              //                      blockedRole, createdAt }
              final blockedUser = (b['blocked'] is Map)
                  ? Map<String, dynamic>.from(b['blocked'] as Map)
                  : <String, dynamic>{};
              final name = (blockedUser['name'] ?? '').toString();
              final avatar = (blockedUser['avatar'] is Map)
                  ? ((blockedUser['avatar'] as Map)['url'] ?? '').toString()
                  : (blockedUser['avatar'] ?? '').toString();
              final blockedRole = (b['blockedRole'] ?? '').toString();
              final userId = (blockedUser['id'] ?? '').toString();
              return Container(
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
                      backgroundColor:
                          AppColors.greyText.withValues(alpha: 0.15),
                      child: avatar.isNotEmpty
                          ? ClipOval(
                              child: CachedNetworkImage(
                                imageUrl: avatar,
                                width: 44.r,
                                height: 44.r,
                                fit: BoxFit.cover,
                                errorWidget: (_, __, ___) => Icon(
                                  Icons.person,
                                  color: AppColors.greyText,
                                  size: 20.sp,
                                ),
                              ),
                            )
                          : Icon(Icons.person,
                              color: AppColors.greyText, size: 22.sp),
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
                            color: AppColors.textPrimary(context),
                          ),
                          SizedBox(height: 2.h),
                          InterText(
                            text: blockedRole,
                            fontSize: 11.sp,
                            color: AppColors.greyText,
                          ),
                        ],
                      ),
                    ),
                    ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.primaryColor,
                        foregroundColor: Colors.white,
                        padding: EdgeInsets.symmetric(
                            horizontal: 12.w, vertical: 6.h),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(20.r),
                        ),
                      ),
                      onPressed: () async {
                        final ok = await controller.unblockUser(userId);
                        if (!mounted) return;
                        if (ok) {
                          CustomSnackbar.showSuccess(
                            title: 'friend_unblocked_title'.tr,
                            message: 'friend_unblocked_msg'
                                .trParams({'name': name}),
                          );
                        } else {
                          CustomSnackbar.showError(
                            title: 'common_error'.tr,
                            message: 'friend_unblock_failed'.tr,
                          );
                        }
                      },
                      child: Text('friend_unblock'.tr,
                          style: TextStyle(fontSize: 12.sp)),
                    ),
                  ],
                ),
              );
            },
          );
        }),
      ),
    );
  }
}
