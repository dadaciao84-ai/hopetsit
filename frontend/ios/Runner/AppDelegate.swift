import Flutter
import UIKit
import GoogleMaps

@main
@objc class AppDelegate: FlutterAppDelegate, FlutterImplicitEngineDelegate {
  override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    // v23.1 part 150 — provideAPIKey à appeler AVANT toute création de
    // GMSMapView, sinon GMSServices raise une NSException et l'app crash
    // dès qu'un écran avec carte s'affiche (post-login screen typiquement).
    // Cf crash report 2026-05-16 17:42 : FGMGoogleMapFactory ->
    // GMSServices.checkServicePreconditions abort.
    // Si la clé est rejetée (HTTP 403 dans les logs Maps), créer une nouvelle
    // clé iOS sur Google Cloud Console avec restriction Bundle ID
    // = com.cardellihermanos.hopetsit + Maps SDK for iOS activé.
    // v23.1 part 161 — DEBUG : verbose logging pour voir POURQUOI Maps SDK
    // ne genere aucune metrique GCP malgre cle valide + APIs activees +
    // restrictions enlevees. Les logs vont sortir dans Console.app sur Mac
    // quand l'iPhone est branche en USB → on saura le vrai message d'erreur.
    GMSServices.provideAPIKey("AIzaSyCD1k2cJ8kRgT4jsTWy598iDKz0d_aELxc")
    // Active verbose logging (visible via Console.app sur Mac)
    print("[HOPETSIT] GoogleMaps SDK version: \(GMSServices.sdkVersion())")
    print("[HOPETSIT] GoogleMaps SDK openSourceLicenseInfo: ready")
    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }

  func didInitializeImplicitFlutterEngine(_ engineBridge: FlutterImplicitEngineBridge) {
    GeneratedPluginRegistrant.register(with: engineBridge.pluginRegistry)
  }
}
