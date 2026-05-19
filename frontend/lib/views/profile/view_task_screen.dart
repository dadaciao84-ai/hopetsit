import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';
import 'package:hopetsit/controllers/profile_controller.dart';
import 'package:hopetsit/controllers/task_controller.dart';
import 'package:hopetsit/models/task_model.dart';
import 'package:hopetsit/utils/app_colors.dart';
import 'package:hopetsit/widgets/app_text.dart';
import 'package:intl/intl.dart';

class ViewTaskScreen extends StatelessWidget {
  const ViewTaskScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final TaskController controller = Get.put(TaskController());
    final ProfileController profileController = Get.put(ProfileController());

    return Scaffold(
      backgroundColor: AppColors.scaffold(context),
      floatingActionButton: FloatingActionButton(
        backgroundColor: AppColors.primaryColor,
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(60.r),
        ),
        onPressed: profileController.navigateToAddTasks,
        child: Icon(Icons.add, color: AppColors.whiteColor),
      ),
      appBar: AppBar(
        backgroundColor: AppColors.appBar(context),
        elevation: 0,
        scrolledUnderElevation: 0.5,
        surfaceTintColor: Colors.transparent,
        iconTheme: IconThemeData(color: AppColors.primaryColor),
        leading: BackButton(),
        title: PoppinsText(
          text: 'view_task_title'.tr,
          fontSize: 18.sp,
          fontWeight: FontWeight.w700,
          color: AppColors.textPrimary(context),
        ),
      ),
      body: SafeArea(
        child: Obx(() {
          if (controller.isFetching.value) {
            return const Center(child: CircularProgressIndicator());
          }

          if (controller.tasks.isEmpty) {
            return Center(
              child: PoppinsText(
                text: 'view_task_empty'.tr,
                fontSize: 16.sp,
                fontWeight: FontWeight.w500,
                color: AppColors.textSecondary(context),
              ),
            );
          }

          return ListView.builder(
            padding: EdgeInsets.symmetric(horizontal: 20.w, vertical: 16.h),
            itemCount: controller.tasks.length,
            itemBuilder: (context, index) {
              final task = controller.tasks[index];
              return _buildTaskCard(task, controller);
            },
          );
        }),
      ),
    );
  }

  // v23.1.147 — Daniel : "Cómo se pueden eliminar las tareas?".
  // Ajout d'un IconButton trash à droite du titre, avec dialog de
  // confirmation avant suppression. Le controller gère l'optimistic
  // removal + rollback côté API failure.
  Widget _buildTaskCard(TaskModel task, TaskController controller) {
    // Parse date
    DateTime? createdAt;
    try {
      createdAt = DateTime.parse(task.createdAt);
    } catch (e) {
      createdAt = null;
    }

    final formattedDate = createdAt != null
        ? DateFormat('MMM dd, yyyy • hh:mm a').format(createdAt)
        : 'view_task_date_not_available'.tr;

    return Builder(
      builder: (context) => Container(
        margin: EdgeInsets.only(bottom: 16.h),
        padding: EdgeInsets.all(16.w),
        decoration: BoxDecoration(
          color: AppColors.card(context),
          borderRadius: BorderRadius.circular(12.r),
          boxShadow: [
            BoxShadow(
              color: AppColors.textPrimary(context).withValues(alpha: 0.05),
              blurRadius: 4,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Title + bouton supprimer
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: PoppinsText(
                    text: task.title,
                    fontSize: 16.sp,
                    fontWeight: FontWeight.w600,
                    color: AppColors.textPrimary(context),
                  ),
                ),
                IconButton(
                  icon: Icon(
                    Icons.delete_outline,
                    size: 22.sp,
                    color: AppColors.textSecondary(context),
                  ),
                  visualDensity: VisualDensity.compact,
                  padding: EdgeInsets.zero,
                  constraints: BoxConstraints(
                    minWidth: 32.w,
                    minHeight: 32.h,
                  ),
                  tooltip: 'task_delete_button'.tr,
                  onPressed: () => _confirmDelete(context, task, controller),
                ),
              ],
            ),
            SizedBox(height: 8.h),
            // Description
            if (task.description.isNotEmpty)
              PoppinsText(
                text: task.description,
                fontSize: 14.sp,
                fontWeight: FontWeight.w400,
                color: AppColors.textSecondary(context),
              ),
            if (task.description.isNotEmpty) SizedBox(height: 12.h),
            // Date
            Row(
              children: [
                Icon(
                  Icons.calendar_today,
                  size: 14.sp,
                  color: AppColors.textSecondary(context),
                ),
                SizedBox(width: 6.w),
                InterText(
                  text: formattedDate,
                  fontSize: 12.sp,
                  fontWeight: FontWeight.w400,
                  color: AppColors.textSecondary(context),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  /// v23.1.147 — Dialog de confirmation avant suppression d'une tâche.
  /// Évite les delete accidentels et donne un feedback clair.
  void _confirmDelete(
    BuildContext context,
    TaskModel task,
    TaskController controller,
  ) {
    showDialog(
      context: context,
      builder: (dialogCtx) => AlertDialog(
        title: PoppinsText(
          text: 'task_delete_confirm_title'.tr,
          fontSize: 16.sp,
          fontWeight: FontWeight.w700,
          color: AppColors.textPrimary(dialogCtx),
        ),
        content: InterText(
          text: 'task_delete_confirm_message'.tr.replaceAll('@title', task.title),
          fontSize: 14.sp,
          color: AppColors.textSecondary(dialogCtx),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(dialogCtx).pop(),
            child: InterText(
              text: 'common_cancel'.tr,
              fontSize: 14.sp,
              fontWeight: FontWeight.w500,
              color: AppColors.textSecondary(dialogCtx),
            ),
          ),
          TextButton(
            onPressed: () {
              Navigator.of(dialogCtx).pop();
              controller.deleteTask(task);
            },
            child: InterText(
              text: 'common_delete'.tr,
              fontSize: 14.sp,
              fontWeight: FontWeight.w700,
              color: AppColors.primaryColor,
            ),
          ),
        ],
      ),
    );
  }
}
