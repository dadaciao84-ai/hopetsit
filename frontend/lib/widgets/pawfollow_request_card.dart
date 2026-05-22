// v23.1.176 — Daniel : "demande suivre votre animale ds le chat ya pas".
//
// Widget partagé pour la carte chat de type 'pawfollow_request' (utilisé
// dans individual_chat_screen côté owner ET sitter_individual_chat_screen
// côté walker/sitter). Affiche un header, un badge de statut, et 2 boutons
// Accepter/Refuser si on est le responder + status pending.

import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';
import 'package:hopetsit/utils/app_colors.dart';
import 'package:hopetsit/widgets/app_text.dart';

class PawfollowRequestCard extends StatelessWidget {
  const PawfollowRequestCard({
    super.key,
    required this.messageId,
    required this.requesterRole,
    required this.responderRole,
    required this.status,
    required this.myRole,
    required this.onAccept,
    required this.onRefuse,
  });

  final String messageId;
  final String requesterRole; // 'owner' | 'sitter' | 'walker'
  final String responderRole; // 'owner' | 'sitter' | 'walker'
  final String status; // 'pending' | 'accepted' | 'refused'
  final String myRole; // current user role
  final VoidCallback onAccept;
  final VoidCallback onRefuse;

  @override
  Widget build(BuildContext context) {
    final isResponder = responderRole == myRole;
    final isRequester = requesterRole == myRole;

    // Couleur halo correspondante :
    //   - responder=walker → vert (walker en prestation, suivi par owner)
    //   - responder=sitter → bleu
    //   - responder=owner  → orange (owner suivi par provider)
    Color accent;
    if (responderRole == 'walker') {
      accent = const Color(0xFF16A34A);
    } else if (responderRole == 'sitter') {
      accent = const Color(0xFF2563EB);
    } else {
      accent = AppColors.primaryColor;
    }

    String headerText;
    if (isRequester) {
      headerText = 'pawfollow_request_sent_header'.tr;
    } else if (isResponder) {
      headerText = requesterRole == 'owner'
          ? 'pawfollow_request_owner_wants_to_follow'.tr
          : 'pawfollow_request_provider_wants_to_share'.tr;
    } else {
      headerText = 'pawfollow_request_generic'.tr;
    }

    String statusBadge;
    Color statusColor;
    if (status == 'accepted') {
      statusBadge = 'pawfollow_status_accepted'.tr;
      statusColor = const Color(0xFF16A34A);
    } else if (status == 'refused') {
      statusBadge = 'pawfollow_status_refused'.tr;
      statusColor = AppColors.errorColor;
    } else {
      statusBadge = 'pawfollow_status_pending'.tr;
      statusColor = const Color(0xFFF59E0B);
    }

    return Padding(
      padding: EdgeInsets.symmetric(vertical: 6.h, horizontal: 16.w),
      child: Container(
        padding: EdgeInsets.all(14.w),
        decoration: BoxDecoration(
          color: accent.withValues(alpha: 0.08),
          borderRadius: BorderRadius.circular(14.r),
          border: Border.all(color: accent.withValues(alpha: 0.35), width: 1),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.location_on_rounded, color: accent, size: 22.sp),
                SizedBox(width: 8.w),
                Expanded(
                  child: InterText(
                    text: headerText,
                    fontSize: 13.sp,
                    fontWeight: FontWeight.w800,
                    color: AppColors.textPrimary(context),
                  ),
                ),
                Container(
                  padding: EdgeInsets.symmetric(
                      horizontal: 8.w, vertical: 3.h),
                  decoration: BoxDecoration(
                    color: statusColor.withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(10.r),
                  ),
                  child: InterText(
                    text: statusBadge,
                    fontSize: 10.sp,
                    fontWeight: FontWeight.w700,
                    color: statusColor,
                  ),
                ),
              ],
            ),
            if (status == 'pending' && isResponder) ...[
              SizedBox(height: 12.h),
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton(
                      style: OutlinedButton.styleFrom(
                        foregroundColor: AppColors.errorColor,
                        side: BorderSide(color: AppColors.errorColor),
                        padding: EdgeInsets.symmetric(vertical: 10.h),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10.r),
                        ),
                      ),
                      onPressed: onRefuse,
                      child: Text('pawfollow_refuse'.tr),
                    ),
                  ),
                  SizedBox(width: 8.w),
                  Expanded(
                    child: ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: accent,
                        foregroundColor: Colors.white,
                        padding: EdgeInsets.symmetric(vertical: 10.h),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10.r),
                        ),
                      ),
                      onPressed: onAccept,
                      child: Text('pawfollow_accept'.tr),
                    ),
                  ),
                ],
              ),
            ],
          ],
        ),
      ),
    );
  }
}
