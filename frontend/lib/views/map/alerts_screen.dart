// v23.1.186 — Daniel mockup : ecran Alertes dedie avec tabs (Tous /
// Perdus / Danger / Accident / Autres) et badges de severite (Urgent /
// Moyen / Info). Liste verticale de cartes signalements + CTA "Signaler
// un animal perdu" en bas.

import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';

import 'package:hopetsit/data/network/api_client.dart';
import 'package:hopetsit/models/map_report_model.dart';
import 'package:hopetsit/utils/app_colors.dart';
import 'package:hopetsit/views/map/widgets/create_report_sheet.dart';
import 'package:hopetsit/widgets/app_text.dart';

class AlertsScreen extends StatelessWidget {
  const AlertsScreen({super.key});

  static const _tabs = <_TabDef>[
    _TabDef(key: 'all', labelKey: 'alerts_tab_all', filter: null),
    _TabDef(key: 'lost', labelKey: 'alerts_tab_lost', filter: [
      ReportTypes.lostPet,
    ]),
    _TabDef(key: 'danger', labelKey: 'alerts_tab_danger', filter: [
      ReportTypes.aggressiveDog,
      ReportTypes.hazard,
    ]),
    _TabDef(key: 'accident', labelKey: 'alerts_tab_accident', filter: [
      ReportTypes.deadAnimal,
    ]),
    _TabDef(key: 'other', labelKey: 'alerts_tab_other', filter: [
      ReportTypes.foundPet,
      ReportTypes.waterActive,
      ReportTypes.waterBroken,
      ReportTypes.poop,
      ReportTypes.other,
    ]),
  ];

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: _tabs.length,
      child: Scaffold(
        backgroundColor: AppColors.scaffold(context),
        appBar: AppBar(
          backgroundColor: AppColors.appBar(context),
          elevation: 0,
          title: Row(
            children: [
              Icon(Icons.notifications_active_rounded,
                  color: const Color(0xFFF59E0B), size: 22.sp),
              SizedBox(width: 8.w),
              InterText(
                text: 'alerts_screen_title'.tr,
                fontSize: 18.sp,
                fontWeight: FontWeight.w700,
                color: AppColors.textPrimary(context),
              ),
            ],
          ),
          bottom: TabBar(
            isScrollable: true,
            labelColor: AppColors.primaryColor,
            unselectedLabelColor: AppColors.greyText,
            indicatorColor: AppColors.primaryColor,
            tabs: _tabs
                .map((t) => Tab(text: t.labelKey.tr))
                .toList(),
          ),
        ),
        body: TabBarView(
          children: _tabs
              .map((t) => _AlertsList(filterTypes: t.filter))
              .toList(),
        ),
        floatingActionButton: FloatingActionButton.extended(
          backgroundColor: const Color(0xFFDC2626),
          icon: const Icon(Icons.add_alert_rounded, color: Colors.white),
          label: InterText(
            text: 'alerts_report_lost_btn'.tr,
            fontSize: 13.sp,
            fontWeight: FontWeight.w800,
            color: Colors.white,
          ),
          onPressed: () async {
            await CreateReportSheet.show(
              context,
              preselectedType: ReportTypes.lostPet,
            );
          },
        ),
      ),
    );
  }
}

class _TabDef {
  final String key;
  final String labelKey;
  final List<String>? filter;
  const _TabDef({required this.key, required this.labelKey, required this.filter});
}

class _AlertsList extends StatefulWidget {
  const _AlertsList({required this.filterTypes});
  final List<String>? filterTypes;

  @override
  State<_AlertsList> createState() => _AlertsListState();
}

class _AlertsListState extends State<_AlertsList>
    with AutomaticKeepAliveClientMixin {
  final RxBool _loading = true.obs;
  final RxList<MapReport> _reports = <MapReport>[].obs;
  final RxnString _error = RxnString();

  @override
  bool get wantKeepAlive => true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    _loading.value = true;
    _error.value = null;
    try {
      final api = Get.find<ApiClient>();
      // /map/reports/nearby renvoie tous les reports proches du user.
      // Sans coords, on fallback sur ?lat=0&lng=0 ne marche pas → on
      // utilise la version /list si dispo, sinon /nearby avec un grand
      // radius pour avoir tout.
      String path = '/map/reports/nearby?radiusKm=50';
      if (widget.filterTypes != null && widget.filterTypes!.isNotEmpty) {
        path += '&type=${widget.filterTypes!.join(',')}';
      }
      final r = await api.get(path, requiresAuth: true);
      List raw = const [];
      if (r is Map && r['reports'] is List) raw = r['reports'] as List;
      else if (r is List) raw = r;
      _reports.assignAll(
        raw
            .whereType<Map>()
            .map((m) => MapReport.fromJson(Map<String, dynamic>.from(m)))
            .toList(),
      );
    } catch (e) {
      _error.value = e.toString();
      _reports.clear();
    } finally {
      _loading.value = false;
    }
  }

  @override
  Widget build(BuildContext context) {
    super.build(context);
    return RefreshIndicator(
      onRefresh: _load,
      child: Obx(() {
        if (_loading.value && _reports.isEmpty) {
          return const Center(child: CircularProgressIndicator());
        }
        if (_reports.isEmpty) {
          return ListView(
            physics: const AlwaysScrollableScrollPhysics(),
            padding: EdgeInsets.all(24.w),
            children: [
              SizedBox(height: 60.h),
              Center(
                child: Column(
                  children: [
                    Icon(Icons.shield_outlined,
                        size: 50.sp,
                        color: AppColors.greyText.withValues(alpha: 0.5)),
                    SizedBox(height: 10.h),
                    InterText(
                      text: 'alerts_empty_title'.tr,
                      fontSize: 15.sp,
                      fontWeight: FontWeight.w700,
                      color: AppColors.textPrimary(context),
                    ),
                    SizedBox(height: 6.h),
                    InterText(
                      text: 'alerts_empty_msg'.tr,
                      fontSize: 12.sp,
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
          padding: EdgeInsets.fromLTRB(12.w, 12.h, 12.w, 90.h),
          itemCount: _reports.length,
          separatorBuilder: (_, __) => SizedBox(height: 8.h),
          itemBuilder: (_, i) => _ReportCard(report: _reports[i]),
        );
      }),
    );
  }
}

class _ReportCard extends StatelessWidget {
  const _ReportCard({required this.report});
  final MapReport report;

  /// Severity tag : urgent (rouge) / moyen (orange) / info (vert/gris).
  ({Color color, String label}) _severity() {
    switch (report.type) {
      case ReportTypes.lostPet:
      case ReportTypes.aggressiveDog:
      case ReportTypes.deadAnimal:
        return (color: const Color(0xFFDC2626), label: 'alerts_severity_urgent'.tr);
      case ReportTypes.hazard:
      case ReportTypes.poop:
      case ReportTypes.waterBroken:
        return (color: const Color(0xFFF59E0B), label: 'alerts_severity_medium'.tr);
      default:
        return (color: const Color(0xFF16A34A), label: 'alerts_severity_info'.tr);
    }
  }

  String _typeLabel() {
    final key = 'map_report_label_${report.type}';
    final tr = key.tr;
    return tr == key ? report.type : tr;
  }

  String _timeAgo(DateTime dt) {
    final diff = DateTime.now().difference(dt);
    if (diff.inMinutes < 1) return 'time_just_now'.tr;
    if (diff.inMinutes < 60) return '${diff.inMinutes}m';
    if (diff.inHours < 24) return '${diff.inHours}h';
    return '${diff.inDays}j';
  }

  @override
  Widget build(BuildContext context) {
    final sev = _severity();
    final emoji = ReportTypes.emoji(report.type);
    return Container(
      padding: EdgeInsets.all(12.w),
      decoration: BoxDecoration(
        color: AppColors.card(context),
        borderRadius: BorderRadius.circular(14.r),
        boxShadow: AppColors.cardShadow(context),
        border: Border.all(color: AppColors.divider(context)),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Vignette photo ou emoji.
          ClipRRect(
            borderRadius: BorderRadius.circular(10.r),
            child: Container(
              width: 60.w,
              height: 60.w,
              color: sev.color.withValues(alpha: 0.10),
              child: report.photoUrl.isNotEmpty
                  ? CachedNetworkImage(
                      imageUrl: report.photoUrl,
                      fit: BoxFit.cover,
                      errorWidget: (_, __, ___) => Center(
                        child: Text(emoji, style: TextStyle(fontSize: 28.sp)),
                      ),
                    )
                  : Center(
                      child: Text(emoji, style: TextStyle(fontSize: 28.sp)),
                    ),
            ),
          ),
          SizedBox(width: 12.w),
          // Texte.
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                InterText(
                  text: _typeLabel(),
                  fontSize: 13.sp,
                  fontWeight: FontWeight.w800,
                  color: sev.color,
                  maxLines: 1,
                ),
                SizedBox(height: 4.h),
                if (report.note.isNotEmpty)
                  InterText(
                    text: report.note,
                    fontSize: 11.sp,
                    color: AppColors.textSecondary(context),
                    maxLines: 2,
                  ),
                SizedBox(height: 6.h),
                Row(
                  children: [
                    if (report.city.isNotEmpty) ...[
                      Icon(Icons.location_on_outlined,
                          size: 12.sp, color: AppColors.greyText),
                      SizedBox(width: 3.w),
                      Flexible(
                        child: InterText(
                          text: report.city,
                          fontSize: 10.sp,
                          color: AppColors.greyText,
                          maxLines: 1,
                        ),
                      ),
                      SizedBox(width: 8.w),
                    ],
                    InterText(
                      text: _timeAgo(report.createdAt),
                      fontSize: 10.sp,
                      color: AppColors.greyText,
                    ),
                  ],
                ),
              ],
            ),
          ),
          SizedBox(width: 8.w),
          Container(
            padding: EdgeInsets.symmetric(horizontal: 8.w, vertical: 3.h),
            decoration: BoxDecoration(
              color: sev.color.withValues(alpha: 0.15),
              borderRadius: BorderRadius.circular(10.r),
              border: Border.all(color: sev.color.withValues(alpha: 0.4)),
            ),
            child: InterText(
              text: sev.label,
              fontSize: 9.sp,
              fontWeight: FontWeight.w800,
              color: sev.color,
            ),
          ),
        ],
      ),
    );
  }
}
