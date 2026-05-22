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

    // v23.1.179 — Daniel : "faire beau bouton orange clair et respecter
    // les traduction par langues". On unifie sur un orange clair brand
    // pour TOUS les rôles (cohérent avec le reste de l'app), tout en
    // gardant une discrète couleur halo en fond pour différencier qui
    // est le responder.
    const orangeBrand = Color(0xFFEF4324);
    const orangeLight = Color(0xFFFF8E5C);
    // Couleur fond/halo correspondante :
    //   - responder=walker → vert pâle (walker en prestation)
    //   - responder=sitter → bleu pâle
    //   - responder=owner  → orange pâle
    Color haloAccent;
    if (responderRole == 'walker') {
      haloAccent = const Color(0xFF16A34A);
    } else if (responderRole == 'sitter') {
      haloAccent = const Color(0xFF2563EB);
    } else {
      haloAccent = AppColors.primaryColor;
    }
    final accent = orangeBrand; // bouton/icone toujours orange brand
    final accentLight = orangeLight;

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
      padding: EdgeInsets.symmetric(vertical: 8.h, horizontal: 16.w),
      child: Container(
        padding: EdgeInsets.all(16.w),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [
              accentLight.withValues(alpha: 0.18),
              accent.withValues(alpha: 0.08),
            ],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(18.r),
          border: Border.all(
            color: accent.withValues(alpha: 0.45),
            width: 1.5,
          ),
          boxShadow: [
            BoxShadow(
              color: accent.withValues(alpha: 0.12),
              blurRadius: 12,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  padding: EdgeInsets.all(8.w),
                  decoration: BoxDecoration(
                    color: accent,
                    shape: BoxShape.circle,
                  ),
                  child: Icon(Icons.pets_rounded,
                      color: Colors.white, size: 18.sp),
                ),
                SizedBox(width: 10.w),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      InterText(
                        text: headerText,
                        fontSize: 14.sp,
                        fontWeight: FontWeight.w800,
                        color: AppColors.textPrimary(context),
                      ),
                      SizedBox(height: 4.h),
                      Container(
                        padding: EdgeInsets.symmetric(
                            horizontal: 10.w, vertical: 3.h),
                        decoration: BoxDecoration(
                          color: statusColor.withValues(alpha: 0.15),
                          borderRadius: BorderRadius.circular(10.r),
                          border: Border.all(
                            color: statusColor.withValues(alpha: 0.35),
                            width: 0.8,
                          ),
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
                ),
                // Pastille couleur halo pour visualiser qui est le responder.
                Container(
                  width: 10.w,
                  height: 10.w,
                  decoration: BoxDecoration(
                    color: haloAccent,
                    shape: BoxShape.circle,
                  ),
                ),
              ],
            ),
            if (status == 'pending' && isResponder) ...[
              SizedBox(height: 14.h),
              Row(
                children: [
                  Expanded(
                    flex: 1,
                    child: OutlinedButton.icon(
                      icon: Icon(Icons.close_rounded,
                          color: AppColors.errorColor, size: 16.sp),
                      label: Text('pawfollow_refuse'.tr),
                      style: OutlinedButton.styleFrom(
                        foregroundColor: AppColors.errorColor,
                        side: BorderSide(
                            color: AppColors.errorColor, width: 1.5),
                        padding: EdgeInsets.symmetric(vertical: 12.h),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12.r),
                        ),
                        textStyle: TextStyle(
                          fontSize: 13.sp,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                      onPressed: onRefuse,
                    ),
                  ),
                  SizedBox(width: 10.w),
                  Expanded(
                    flex: 2,
                    child: ElevatedButton.icon(
                      icon: const Icon(
                        Icons.check_circle_rounded,
                        color: Colors.white,
                      ),
                      label: Text('pawfollow_accept'.tr),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: accent,
                        foregroundColor: Colors.white,
                        elevation: 3,
                        shadowColor: accent.withValues(alpha: 0.5),
                        padding: EdgeInsets.symmetric(vertical: 12.h),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12.r),
                        ),
                        textStyle: TextStyle(
                          fontSize: 13.sp,
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                      onPressed: onAccept,
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
