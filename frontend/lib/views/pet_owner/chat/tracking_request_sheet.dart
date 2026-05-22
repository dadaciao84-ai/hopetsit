// v23.1.192 — Daniel mockup SUIVI EN DIRECT (cote OWNER) : ecran qui
// s'ouvre quand l'owner tape "Suivre en direct mon animal" dans le chat.
//
// Contenu (mockup) :
//   - Pet card (avatar, name, breed, dates, "En garde" badge)
//   - "Suivi en direct • Disponible" + gros bouton orange "Suivre mon
//     animal"
//   - "Informations pratiques" : sitter / walker nom + photo + message
//     + telephone + adresse de depart
//   - Banner "Transparence & confiance" en bas
//
// Au tap "Suivre mon animal" → declenche le callback onConfirm qui
// envoie la pawfollow_request (controleur de chat). Au tap "Plus tard"
// → ferme sans envoyer.

import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';

import 'package:hopetsit/models/booking_model.dart' show BookingModel;
import 'package:hopetsit/utils/app_colors.dart';
import 'package:hopetsit/widgets/app_text.dart';

class TrackingRequestSheet extends StatelessWidget {
  const TrackingRequestSheet({
    super.key,
    required this.booking,
    required this.onConfirm,
  });

  /// Booking lie a la conversation (pet, dates, sitter/walker info).
  final BookingModel booking;

  /// Callback declenche au tap "Suivre mon animal".
  final Future<void> Function() onConfirm;

  static const _orange = Color(0xFFEF4324);
  static const _orangeBg = Color(0xFFFFF1ED);

  String _formatDateRange() {
    // BookingModel n'a que `date` (string) et `timeSlot` (string), pas
    // de DateTime end. On affiche juste la date + creneau pour le
    // moment ; un futur sprint pourra parser et formatter.
    final d = booking.date;
    final t = booking.timeSlot;
    if (d.isEmpty && t.isEmpty) return '';
    return [d, t].where((s) => s.isNotEmpty).join(' · ');
  }

  @override
  Widget build(BuildContext context) {
    final providerName = booking.sitter.name;
    final providerAvatar = booking.sitter.avatar.url;
    final petName = (booking.pets.isNotEmpty
        ? booking.pets.first.petName
        : booking.petName);
    final petBreed = booking.pets.isNotEmpty
        ? booking.pets.first.breed
        : '';
    final petAvatar = booking.pets.isNotEmpty
        ? booking.pets.first.avatar.url
        : '';

    return Scaffold(
      backgroundColor: AppColors.scaffold(context),
      appBar: AppBar(
        backgroundColor: AppColors.appBar(context),
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.arrow_back_rounded,
              color: _orange, size: 24.sp),
          onPressed: () => Navigator.of(context).pop(),
        ),
        title: InterText(
          text: 'tracking_sheet_title'.tr,
          fontSize: 17.sp,
          fontWeight: FontWeight.w800,
          color: AppColors.textPrimary(context),
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: ListView(
          padding: EdgeInsets.fromLTRB(16.w, 16.h, 16.w, 24.h),
          children: [
            // ── Pet card ────────────────────────────────────────────
            _buildPetCard(context, petName, petBreed, petAvatar),
            SizedBox(height: 14.h),

            // ── Suivi en direct + CTA ──────────────────────────────
            _buildLiveTrackingPanel(context),
            SizedBox(height: 14.h),

            // ── Infos pratiques ─────────────────────────────────────
            _buildPracticalInfo(context, providerName, providerAvatar),
            SizedBox(height: 14.h),

            // ── Transparence & confiance ────────────────────────────
            _buildTrustBanner(context),
          ],
        ),
      ),
    );
  }

  Widget _buildPetCard(BuildContext context, String name, String breed, String avatar) {
    final dates = _formatDateRange();
    return Container(
      padding: EdgeInsets.all(14.w),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18.r),
        border: Border.all(color: AppColors.divider(context)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 12,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        children: [
          Row(
            children: [
              ClipOval(
                child: Container(
                  width: 56.w,
                  height: 56.w,
                  color: _orange.withValues(alpha: 0.12),
                  child: avatar.isNotEmpty
                      ? CachedNetworkImage(
                          imageUrl: avatar,
                          fit: BoxFit.cover,
                          errorWidget: (_, __, ___) =>
                              Icon(Icons.pets, color: _orange, size: 28.sp),
                        )
                      : Icon(Icons.pets, color: _orange, size: 28.sp),
                ),
              ),
              SizedBox(width: 12.w),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Flexible(
                          child: InterText(
                            text: name.isEmpty ? '—' : name,
                            fontSize: 16.sp,
                            fontWeight: FontWeight.w800,
                            color: AppColors.textPrimary(context),
                            maxLines: 1,
                          ),
                        ),
                        SizedBox(width: 6.w),
                        Text('🐾', style: TextStyle(fontSize: 14.sp)),
                      ],
                    ),
                    if (breed.isNotEmpty) ...[
                      SizedBox(height: 2.h),
                      InterText(
                        text: breed,
                        fontSize: 12.sp,
                        color: AppColors.greyText,
                      ),
                    ],
                  ],
                ),
              ),
              Container(
                padding: EdgeInsets.symmetric(
                    horizontal: 10.w, vertical: 4.h),
                decoration: BoxDecoration(
                  color: _orangeBg,
                  borderRadius: BorderRadius.circular(12.r),
                  border: Border.all(color: _orange.withValues(alpha: 0.3)),
                ),
                child: InterText(
                  text: 'tracking_sheet_in_care_badge'.tr,
                  fontSize: 10.sp,
                  fontWeight: FontWeight.w800,
                  color: _orange,
                ),
              ),
            ],
          ),
          if (dates.isNotEmpty) ...[
            SizedBox(height: 10.h),
            Container(
              width: double.infinity,
              padding: EdgeInsets.symmetric(horizontal: 10.w, vertical: 8.h),
              decoration: BoxDecoration(
                color: _orangeBg,
                borderRadius: BorderRadius.circular(10.r),
              ),
              child: Row(
                children: [
                  Icon(Icons.calendar_today_rounded,
                      color: _orange, size: 14.sp),
                  SizedBox(width: 8.w),
                  Expanded(
                    child: InterText(
                      text: dates,
                      fontSize: 12.sp,
                      fontWeight: FontWeight.w600,
                      color: AppColors.textPrimary(context),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildLiveTrackingPanel(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(14.w),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18.r),
        border: Border.all(color: AppColors.divider(context)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 12,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: InterText(
                  text: 'tracking_sheet_panel_title'.tr,
                  fontSize: 15.sp,
                  fontWeight: FontWeight.w800,
                  color: AppColors.textPrimary(context),
                ),
              ),
              Container(
                padding: EdgeInsets.symmetric(horizontal: 8.w, vertical: 3.h),
                decoration: BoxDecoration(
                  color: const Color(0xFF16A34A).withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(12.r),
                  border: Border.all(
                      color: const Color(0xFF16A34A).withValues(alpha: 0.4)),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Container(
                      width: 6.w,
                      height: 6.w,
                      decoration: const BoxDecoration(
                        color: Color(0xFF16A34A),
                        shape: BoxShape.circle,
                      ),
                    ),
                    SizedBox(width: 4.w),
                    InterText(
                      text: 'tracking_sheet_available'.tr,
                      fontSize: 10.sp,
                      fontWeight: FontWeight.w800,
                      color: const Color(0xFF16A34A),
                    ),
                  ],
                ),
              ),
            ],
          ),
          SizedBox(height: 4.h),
          InterText(
            text: 'tracking_sheet_panel_desc'.tr,
            fontSize: 12.sp,
            color: AppColors.textSecondary(context),
          ),
          SizedBox(height: 12.h),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: () async {
                await onConfirm();
                if (context.mounted) Navigator.of(context).pop(true);
              },
              icon: const Icon(Icons.location_on_rounded, color: Colors.white),
              label: Padding(
                padding: EdgeInsets.symmetric(vertical: 4.h),
                child: InterText(
                  text: 'tracking_sheet_follow_btn'.tr,
                  fontSize: 14.sp,
                  fontWeight: FontWeight.w800,
                  color: Colors.white,
                ),
              ),
              style: ElevatedButton.styleFrom(
                backgroundColor: _orange,
                foregroundColor: Colors.white,
                padding: EdgeInsets.symmetric(vertical: 12.h),
                elevation: 3,
                shadowColor: _orange.withValues(alpha: 0.5),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(14.r),
                ),
              ),
            ),
          ),
          SizedBox(height: 6.h),
          SizedBox(
            width: double.infinity,
            child: OutlinedButton(
              onPressed: () => Navigator.of(context).pop(),
              style: OutlinedButton.styleFrom(
                side: BorderSide(color: _orange.withValues(alpha: 0.4)),
                padding: EdgeInsets.symmetric(vertical: 12.h),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(14.r),
                ),
              ),
              child: InterText(
                text: 'tracking_sheet_later'.tr,
                fontSize: 13.sp,
                fontWeight: FontWeight.w700,
                color: _orange,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPracticalInfo(BuildContext context, String name, String avatar) {
    return Container(
      padding: EdgeInsets.all(14.w),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18.r),
        border: Border.all(color: AppColors.divider(context)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 12,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          InterText(
            text: 'tracking_sheet_practical_info'.tr,
            fontSize: 15.sp,
            fontWeight: FontWeight.w800,
            color: AppColors.textPrimary(context),
          ),
          SizedBox(height: 12.h),
          // Provider row.
          Row(
            children: [
              ClipOval(
                child: Container(
                  width: 44.w,
                  height: 44.w,
                  color: _orange.withValues(alpha: 0.10),
                  child: avatar.isNotEmpty
                      ? CachedNetworkImage(
                          imageUrl: avatar,
                          fit: BoxFit.cover,
                          errorWidget: (_, __, ___) =>
                              Icon(Icons.person, color: _orange, size: 22.sp),
                        )
                      : Icon(Icons.person, color: _orange, size: 22.sp),
                ),
              ),
              SizedBox(width: 10.w),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    InterText(
                      text: 'tracking_sheet_sitter_walker'.tr,
                      fontSize: 10.sp,
                      color: AppColors.greyText,
                    ),
                    SizedBox(height: 1.h),
                    InterText(
                      text: name.isEmpty ? '—' : name,
                      fontSize: 13.sp,
                      fontWeight: FontWeight.w700,
                      color: AppColors.textPrimary(context),
                    ),
                  ],
                ),
              ),
            ],
          ),
          SizedBox(height: 10.h),
          Divider(height: 1, color: AppColors.divider(context)),
          SizedBox(height: 10.h),
          // Note de transparence (telephone + adresse pas exposes pour
          // privacy — l'owner contacte via chat ; on garde la place pour
          // un futur module ou ils sont opt-in).
          Row(
            children: [
              Icon(Icons.chat_bubble_outline_rounded,
                  color: _orange, size: 18.sp),
              SizedBox(width: 8.w),
              Expanded(
                child: InterText(
                  text: 'tracking_sheet_contact_via_chat'.tr,
                  fontSize: 11.sp,
                  color: AppColors.textSecondary(context),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildTrustBanner(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(12.w),
      decoration: BoxDecoration(
        color: _orangeBg,
        borderRadius: BorderRadius.circular(14.r),
      ),
      child: Row(
        children: [
          Icon(Icons.shield_rounded, color: _orange, size: 22.sp),
          SizedBox(width: 10.w),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                InterText(
                  text: 'tracking_sheet_trust_title'.tr,
                  fontSize: 12.sp,
                  fontWeight: FontWeight.w800,
                  color: _orange,
                ),
                SizedBox(height: 2.h),
                InterText(
                  text: 'tracking_sheet_trust_msg'.tr,
                  fontSize: 11.sp,
                  color: AppColors.textSecondary(context),
                  maxLines: 3,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
