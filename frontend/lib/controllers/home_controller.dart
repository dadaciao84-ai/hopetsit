import 'dart:io';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:hopetsit/data/network/api_client.dart';
import 'package:hopetsit/data/network/api_exception.dart';
import 'package:hopetsit/models/sitter_model.dart';
import 'package:hopetsit/models/walker_model.dart';
import 'package:hopetsit/repositories/owner_repository.dart';
import 'package:hopetsit/repositories/walker_repository.dart';
import 'package:hopetsit/services/location_service.dart';
import 'package:hopetsit/utils/logger.dart';
import 'package:hopetsit/widgets/custom_snackbar_widget.dart';

class HomeController extends GetxController {
  HomeController({
    OwnerRepository? ownerRepository,
    WalkerRepository? walkerRepository,
  })  : _ownerRepository = ownerRepository ?? Get.find<OwnerRepository>(),
        _walkerRepository = walkerRepository ??
            (Get.isRegistered<WalkerRepository>()
                ? Get.find<WalkerRepository>()
                : WalkerRepository(
                    Get.isRegistered<ApiClient>()
                        ? Get.find<ApiClient>()
                        : ApiClient(),
                  ));

  final OwnerRepository _ownerRepository;
  final WalkerRepository _walkerRepository;

  // Post state (legacy)
  final RxBool canPost = false.obs;
  final RxBool isLoading = false.obs;
  final TextEditingController postController = TextEditingController();
  final RxList<File> selectedImages = <File>[].obs;

  // Sitters
  final RxList<SitterModel> sitters = <SitterModel>[].obs;
  final RxBool isLoadingSitters = false.obs;

  // Walkers (same "Promeneurs" tab layout as sitters — the Near Me slider
  // is shared with sitters via nearMeRadiusKm below).
  final RxList<WalkerModel> walkers = <WalkerModel>[].obs;
  final RxBool isLoadingWalkers = false.obs;

  // FIX #2 — Offers Near Me state
  final RxBool offersNearMeEnabled = false.obs;
  final RxDouble nearMeRadiusKm = 50.0.obs;

  @override
  void onInit() {
    super.onInit();
    postController.addListener(_onTextChanged);
    loadSitters();
    loadWalkers();
  }

  @override
  void onClose() {
    postController.dispose();
    super.onClose();
  }

  void _onTextChanged() {
    canPost.value =
        postController.text.trim().isNotEmpty || selectedImages.isNotEmpty;
  }

  /// Loads all sitters (default, no location filter)
  Future<void> loadSitters() async {
    isLoadingSitters.value = true;
    offersNearMeEnabled.value = false;
    try {
      final sittersList = await _ownerRepository.getSitters();
      sitters.assignAll(sittersList);
    } on ApiException catch (error) {
      AppLogger.logError('Failed to load sitters', error: error.message);
      sitters.clear();
    } catch (error) {
      AppLogger.logError('Failed to load sitters', error: error);
      sitters.clear();
    } finally {
      isLoadingSitters.value = false;
    }
  }

  /// FIX #2 — Toggle "Offers Near Me": uses GPS to filter nearby sitters
  Future<void> toggleOffersNearMe(BuildContext context) async {
    if (offersNearMeEnabled.value) {
      // Turn off → reload all sitters
      await loadSitters();
      return;
    }
    await loadNearbySitters(radiusKm: nearMeRadiusKm.value.round());
  }

  /// FIX #2 — Load sitters filtered by GPS distance radius
  Future<void> loadNearbySitters({required int radiusKm}) async {
    isLoadingSitters.value = true;
    try {
      final locationService = LocationService();
      final position = await locationService.getCurrentLocation();
      if (position == null) {
        // v23.1.147 — Daniel : "si on met 20 km le paseador disparaît".
        // Avant : on affichait juste une erreur, la liste restait vide.
        // Maintenant : fallback sur la liste complète pour ne pas frustrer
        // l'utilisateur dont la géoloc n'est pas dispo.
        await loadSitters();
        return;
      }

      final list = await _ownerRepository.getNearbySitters(
        lat: position.latitude,
        lng: position.longitude,
        radiusInMeters: radiusKm * 1000,
      );
      // v23.1.147 — fallback si la liste nearby est vide. C'est typique
      // pour les sitters sans coordonnées GPS en DB (MongoDB $near les
      // exclut systématiquement). Plutôt qu'un écran vide, on affiche la
      // liste complète pour que l'utilisateur les voie quand même.
      if (list.isEmpty) {
        await loadSitters();
        return;
      }
      sitters.assignAll(list);
      offersNearMeEnabled.value = true;
      nearMeRadiusKm.value = radiusKm.toDouble();
    } on ApiException catch (error) {
      AppLogger.logError('Failed to load nearby sitters', error: error.message);
      // Fallback sur la liste complète en cas d'erreur API.
      await loadSitters();
    } catch (error) {
      AppLogger.logError('Failed to load nearby sitters', error: error);
      await loadSitters();
    } finally {
      isLoadingSitters.value = false;
    }
  }

  // ==========================================================================
  // Walkers (Promeneurs) — same UX as sitters: full list by default, optional
  // Near Me filter reusing the same radius slider.
  // ==========================================================================

  /// Loads all walkers (default, no location filter).
  Future<void> loadWalkers() async {
    isLoadingWalkers.value = true;
    try {
      final list = await _walkerRepository.getAllWalkers();
      walkers.assignAll(list);
    } on ApiException catch (error) {
      AppLogger.logError('Failed to load walkers', error: error.message);
      walkers.clear();
    } catch (error) {
      AppLogger.logError('Failed to load walkers', error: error);
      walkers.clear();
    } finally {
      isLoadingWalkers.value = false;
    }
  }

  /// Loads walkers filtered by GPS distance radius.
  Future<void> loadNearbyWalkers({required int radiusKm}) async {
    isLoadingWalkers.value = true;
    try {
      final locationService = LocationService();
      final position = await locationService.getCurrentLocation();
      if (position == null) {
        // v23.1.147 — Daniel : "si on met 20 km le paseador disparaît".
        // Fallback sur la liste complète au lieu d'écran vide + erreur.
        await loadWalkers();
        return;
      }

      final list = await _walkerRepository.getNearbyWalkers(
        lat: position.latitude,
        lng: position.longitude,
        radiusInMeters: radiusKm * 1000,
      );
      // v23.1.147 — fallback si la liste nearby est vide (cas walker sans
      // coordonnées GPS en DB → exclu par MongoDB $near). Affiche tous
      // les walkers au lieu d'écran vide.
      if (list.isEmpty) {
        await loadWalkers();
        return;
      }
      walkers.assignAll(list);
    } on ApiException catch (error) {
      AppLogger.logError('Failed to load nearby walkers', error: error.message);
      await loadWalkers();
    } catch (error) {
      AppLogger.logError('Failed to load nearby walkers', error: error);
      await loadWalkers();
    } finally {
      isLoadingWalkers.value = false;
    }
  }

  /// Blocks a sitter
  Future<void> blockSitter(String sitterId) async {
    try {
      await _ownerRepository.blockSitter(sitterId: sitterId);
      CustomSnackbar.showSuccess(
        title: 'common_success'.tr,
        message: 'snackbar_text_sitter_blocked_successfully',
      );
    } on ApiException catch (error) {
      CustomSnackbar.showError(
        title: 'common_error'.tr,
        message: error.message,
      );
    } catch (error) {
      CustomSnackbar.showError(
        title: 'common_error'.tr,
        message: 'common_error_generic'.tr,
      );
    }
  }
}
