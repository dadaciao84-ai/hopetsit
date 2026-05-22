// v23.1.186 — Daniel mockup : ecran Signaler en grille 2x3 avec 6
// grosses categories colorees (Animal perdu / Danger / Chien mechant /
// Accident / Poison / Autre). Tap → ouvre CreateReportSheet avec le type
// pre-selectionne.

import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:geolocator/geolocator.dart';
import 'package:get/get.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

import 'package:hopetsit/models/map_report_model.dart';
import 'package:hopetsit/utils/app_colors.dart';
import 'package:hopetsit/views/map/widgets/create_report_sheet.dart';
import 'package:hopetsit/widgets/app_text.dart';

class ReportCategoryGridScreen extends StatelessWidget {
  const ReportCategoryGridScreen({super.key});

  static const _categories = <_CategoryDef>[
    _CategoryDef(
      type: ReportTypes.lostPet,
      labelKey: 'report_cat_lost_pet',
      icon: Icons.pets_rounded,
      color: Color(0xFFEC407A),
    ),
    _CategoryDef(
      type: ReportTypes.hazard,
      labelKey: 'report_cat_hazard',
      icon: Icons.warning_amber_rounded,
      color: Color(0xFFF59E0B),
    ),
    _CategoryDef(
      type: ReportTypes.aggressiveDog,
      labelKey: 'report_cat_aggressive_dog',
      icon: Icons.report_problem_rounded,
      color: Color(0xFFE53935),
    ),
    _CategoryDef(
      type: ReportTypes.deadAnimal,
      labelKey: 'report_cat_accident',
      icon: Icons.medical_services_rounded,
      color: Color(0xFFDC2626),
    ),
    _CategoryDef(
      type: ReportTypes.poop,
      labelKey: 'report_cat_poison',
      icon: Icons.dangerous_rounded,
      color: Color(0xFF795548),
    ),
    _CategoryDef(
      type: ReportTypes.other,
      labelKey: 'report_cat_other',
      icon: Icons.more_horiz_rounded,
      color: Color(0xFF6B7280),
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.scaffold(context),
      appBar: AppBar(
        backgroundColor: AppColors.appBar(context),
        elevation: 0,
        title: Row(
          children: [
            Icon(Icons.add_circle_rounded,
                color: const Color(0xFFDC2626), size: 22.sp),
            SizedBox(width: 8.w),
            InterText(
              text: 'report_screen_title'.tr,
              fontSize: 18.sp,
              fontWeight: FontWeight.w700,
              color: AppColors.textPrimary(context),
            ),
          ],
        ),
      ),
      body: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: EdgeInsets.fromLTRB(20.w, 14.h, 20.w, 6.h),
              child: Align(
                alignment: Alignment.centerLeft,
                child: InterText(
                  text: 'report_what_to_report'.tr,
                  fontSize: 16.sp,
                  fontWeight: FontWeight.w800,
                  color: AppColors.textPrimary(context),
                ),
              ),
            ),
            Padding(
              padding: EdgeInsets.symmetric(horizontal: 20.w),
              child: Align(
                alignment: Alignment.centerLeft,
                child: InterText(
                  text: 'report_pick_category_hint'.tr,
                  fontSize: 12.sp,
                  color: AppColors.greyText,
                ),
              ),
            ),
            SizedBox(height: 14.h),
            Expanded(
              child: GridView.builder(
                padding: EdgeInsets.fromLTRB(16.w, 6.h, 16.w, 24.h),
                gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  crossAxisSpacing: 12.w,
                  mainAxisSpacing: 12.h,
                  childAspectRatio: 1.05,
                ),
                itemCount: _categories.length,
                itemBuilder: (_, i) => _buildCategoryTile(
                  context,
                  _categories[i],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCategoryTile(BuildContext context, _CategoryDef cat) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        borderRadius: BorderRadius.circular(20.r),
        onTap: () async {
          LatLng point = const LatLng(0, 0);
          try {
            final pos = await Geolocator.getCurrentPosition(
              locationSettings: const LocationSettings(
                accuracy: LocationAccuracy.high,
                timeLimit: Duration(seconds: 6),
              ),
            );
            point = LatLng(pos.latitude, pos.longitude);
          } catch (_) {/* fallback */}
          if (!context.mounted) return;
          final created = await CreateReportSheet.show(
            context,
            initialPoint: point,
            preselectedType: cat.type,
          );
          if (created && context.mounted) {
            Navigator.of(context).pop(true);
          }
        },
        child: Container(
          padding: EdgeInsets.all(14.w),
          decoration: BoxDecoration(
            color: cat.color.withValues(alpha: 0.08),
            borderRadius: BorderRadius.circular(20.r),
            border: Border.all(
              color: cat.color.withValues(alpha: 0.25),
              width: 1.3,
            ),
            boxShadow: [
              BoxShadow(
                color: cat.color.withValues(alpha: 0.12),
                blurRadius: 12,
                offset: const Offset(0, 4),
              ),
            ],
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                width: 58.w,
                height: 58.w,
                decoration: BoxDecoration(
                  color: cat.color,
                  shape: BoxShape.circle,
                  boxShadow: [
                    BoxShadow(
                      color: cat.color.withValues(alpha: 0.5),
                      blurRadius: 10,
                      offset: const Offset(0, 3),
                    ),
                  ],
                ),
                child: Icon(cat.icon, color: Colors.white, size: 28.sp),
              ),
              SizedBox(height: 12.h),
              InterText(
                text: cat.labelKey.tr,
                fontSize: 13.sp,
                fontWeight: FontWeight.w800,
                color: cat.color,
                textAlign: TextAlign.center,
                maxLines: 2,
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _CategoryDef {
  final String type;
  final String labelKey;
  final IconData icon;
  final Color color;
  const _CategoryDef({
    required this.type,
    required this.labelKey,
    required this.icon,
    required this.color,
  });
}
