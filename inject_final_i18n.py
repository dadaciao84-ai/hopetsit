"""
HopeTSIT v23.1.151 - Passe finale i18n PawMap.

Reste des strings hardcoded apres injection 1 + 2 :
  - Filter chips au-dessus de la map (POIs / Signalements 48h / Amis /
    Demandes / Perdu / Chien mechant / Point d'eau)
  - Snackbar errors (ville introuvable etc.)
  - CreateReportSheet validation snacks (Type requis, Signalement envoye)
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent
LANG_DIR = ROOT / "frontend" / "lib" / "localization" / "translations"
SOURCE_FILES = {
    "create_report_sheet": ROOT / "frontend" / "lib" / "views" / "map" / "widgets" / "create_report_sheet.dart",
    "paw_map_screen": ROOT / "frontend" / "lib" / "views" / "map" / "paw_map_screen.dart",
}

TRANSLATIONS = {
    # Filter chips above the map
    "pawmap_filter_pois": {
        "fr": "POIs", "en": "POIs", "es": "POIs", "de": "POIs", "it": "POIs", "pt": "POIs",
    },
    "pawmap_filter_reports_48h": {
        "fr": "Signalements 48h",
        "en": "48h reports",
        "es": "Señalamientos 48h",
        "de": "48-Std.-Meldungen",
        "it": "Segnalazioni 48h",
        "pt": "Sinalizações 48h",
    },
    "pawmap_filter_friends": {
        "fr": "Amis",
        "en": "Friends",
        "es": "Amigos",
        "de": "Freunde",
        "it": "Amici",
        "pt": "Amigos",
    },
    "pawmap_filter_requests": {
        "fr": "Demandes",
        "en": "Requests",
        "es": "Solicitudes",
        "de": "Anfragen",
        "it": "Richieste",
        "pt": "Pedidos",
    },
    "pawmap_filter_lost": {
        "fr": "Perdu",
        "en": "Lost",
        "es": "Perdido",
        "de": "Verloren",
        "it": "Smarrito",
        "pt": "Perdido",
    },
    "pawmap_filter_aggressive_dog": {
        "fr": "Chien méchant",
        "en": "Aggressive dog",
        "es": "Perro agresivo",
        "de": "Aggressiver Hund",
        "it": "Cane aggressivo",
        "pt": "Cão agressivo",
    },
    "pawmap_filter_water_point": {
        "fr": "Point d'eau",
        "en": "Water point",
        "es": "Punto de agua",
        "de": "Wasserstelle",
        "it": "Punto d'acqua",
        "pt": "Ponto de água",
    },
    # CreateReportSheet snackbars
    "pawmap_snack_premium_required": {
        "fr": "Premium requis",
        "en": "Premium required",
        "es": "Premium requerido",
        "de": "Premium erforderlich",
        "it": "Premium richiesto",
        "pt": "Premium necessário",
    },
    "pawmap_snack_type_required_title": {
        "fr": "Type requis",
        "en": "Type required",
        "es": "Tipo requerido",
        "de": "Typ erforderlich",
        "it": "Tipo richiesto",
        "pt": "Tipo necessário",
    },
    "pawmap_snack_type_required_msg": {
        "fr": "Choisis un type de signalement avant d'envoyer.",
        "en": "Choose a report type before sending.",
        "es": "Elige un tipo de señalamiento antes de enviar.",
        "de": "Wähle einen Meldungstyp vor dem Senden.",
        "it": "Scegli un tipo di segnalazione prima di inviare.",
        "pt": "Escolhe um tipo de sinalização antes de enviar.",
    },
    "pawmap_snack_sent_title": {
        "fr": "Signalement envoyé",
        "en": "Report sent",
        "es": "Señalamiento enviado",
        "de": "Meldung gesendet",
        "it": "Segnalazione inviata",
        "pt": "Sinalização enviada",
    },
    "pawmap_snack_sent_msg": {
        "fr": "Visible 48h autour de vous. Merci !",
        "en": "Visible for 48h around you. Thanks!",
        "es": "Visible 48h a tu alrededor. ¡Gracias!",
        "de": "48 Std. um dich sichtbar. Danke!",
        "it": "Visibile 48h intorno a te. Grazie!",
        "pt": "Visível 48h à tua volta. Obrigado!",
    },
    "pawmap_snack_send_failed_title": {
        "fr": "Envoi impossible",
        "en": "Send failed",
        "es": "Envío imposible",
        "de": "Senden fehlgeschlagen",
        "it": "Invio impossibile",
        "pt": "Envio falhou",
    },
    "pawmap_snack_send_failed_msg": {
        "fr": "Réessaie dans un instant.",
        "en": "Try again in a moment.",
        "es": "Inténtalo de nuevo en un momento.",
        "de": "Versuche es gleich nochmal.",
        "it": "Riprova tra un momento.",
        "pt": "Tenta novamente daqui a pouco.",
    },
    # PawMap snackbars
    "pawmap_snack_city_not_found_msg": {
        "fr": "Aucune position trouvée pour \"@city\".",
        "en": "No position found for \"@city\".",
        "es": "No se encontró ninguna posición para \"@city\".",
        "de": "Keine Position für \"@city\" gefunden.",
        "it": "Nessuna posizione trovata per \"@city\".",
        "pt": "Nenhuma posição encontrada para \"@city\".",
    },
    "pawmap_snack_search_failed_msg": {
        "fr": "Vérifiez votre connexion et réessayez.",
        "en": "Check your connection and try again.",
        "es": "Comprueba tu conexión y vuelve a intentarlo.",
        "de": "Verbindung prüfen und erneut versuchen.",
        "it": "Controlla la connessione e riprova.",
        "pt": "Verifica a tua ligação e tenta novamente.",
    },
    "pawmap_snack_tracking_off_msg": {
        "fr": "Tes amis ne voient plus ta position.",
        "en": "Your friends no longer see your position.",
        "es": "Tus amigos ya no ven tu posición.",
        "de": "Deine Freunde sehen deine Position nicht mehr.",
        "it": "I tuoi amici non vedono più la tua posizione.",
        "pt": "Os teus amigos já não veem a tua posição.",
    },
    "pawmap_snack_tracking_on_msg": {
        "fr": "Tes amis voient ta position et celle de ton animal en live.",
        "en": "Your friends see your position and your pet's live.",
        "es": "Tus amigos ven tu posición y la de tu mascota en vivo.",
        "de": "Deine Freunde sehen deine Position und die deines Tieres live.",
        "it": "I tuoi amici vedono la tua posizione e quella del tuo animale in diretta.",
        "pt": "Os teus amigos veem a tua posição e a do teu animal ao vivo.",
    },
    # Confirm extend / report abuse snackbars
    "pawmap_snack_extended_msg": {
        "fr": "Signalement prolongé de 12h.",
        "en": "Report extended by 12h.",
        "es": "Señalamiento prolongado 12h.",
        "de": "Meldung um 12 Std. verlängert.",
        "it": "Segnalazione prolungata di 12h.",
        "pt": "Sinalização prolongada por 12h.",
    },
    "pawmap_snack_reported_msg": {
        "fr": "Merci, un modérateur va vérifier.",
        "en": "Thanks, a moderator will check.",
        "es": "Gracias, un moderador lo revisará.",
        "de": "Danke, ein Moderator prüft das.",
        "it": "Grazie, un moderatore controllerà.",
        "pt": "Obrigado, um moderador vai verificar.",
    },
    # Confirmations on InfoWindow
    "pawmap_confirmations_inline": {
        "fr": "@count confirmation(s)",
        "en": "@count confirmation(s)",
        "es": "@count confirmación(es)",
        "de": "@count Bestätigung(en)",
        "it": "@count conferma/e",
        "pt": "@count confirmação(ões)",
    },
}


def dart_escape(s):
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")


def inject_into_lang_file(lang_code):
    path = LANG_DIR / f"{lang_code}.dart"
    text = path.read_text(encoding="utf-8")

    anchor = (
        re.search(r"('pawmap_default_request':\s*'[^']*',\s*\n)", text)
        or re.search(r"('mapboost_info_visibility':\s*'[^']*',\s*\n)", text)
        or re.search(r"('pawmap_confirmations':\s*'[^']*',\s*\n)", text)
        or re.search(r"('map_report_label_other':\s*'[^']*',\s*\n)", text)
    )
    if not anchor:
        print(f"  [SKIP] {lang_code}: anchor not found")
        return 0

    new_entries = []
    skipped = 0
    for key, langs in TRANSLATIONS.items():
        if f"'{key}'" in text:
            skipped += 1
            continue
        if lang_code not in langs:
            continue
        value = dart_escape(langs[lang_code])
        new_entries.append(f"      '{key}': '{value}',")

    if not new_entries:
        print(f"  [{lang_code}] already up to date (skipped {skipped})")
        return 0

    insert_at = anchor.end()
    block = "\n".join(new_entries) + "\n"
    new_text = text[:insert_at] + block + text[insert_at:]
    path.write_text(new_text, encoding="utf-8")
    print(f"  [{lang_code}] inserted {len(new_entries)} keys (skipped {skipped})")
    return len(new_entries)


def patch_source(name, path, substitutions):
    text = path.read_text(encoding="utf-8")
    original = text
    changes = 0
    for old, new in substitutions:
        if old in text:
            text = text.replace(old, new, 1)
            changes += 1
        else:
            print(f"  [WARN] {name}: not found -> {old[:80]!r}")
    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"  [{name}] applied {changes} substitutions")
    return changes


def main():
    print("== Inject final i18n keys ==")
    for lang in ["en", "fr", "es", "de", "it", "pt"]:
        inject_into_lang_file(lang)

    print()
    print("== Patch paw_map_screen.dart ==")
    patch_source(
        "paw_map_screen",
        SOURCE_FILES["paw_map_screen"],
        [
            # Filter chips
            (
                "label: 'POIs',",
                "label: 'pawmap_filter_pois'.tr,",
            ),
            (
                "label: 'Signalements 48h',",
                "label: 'pawmap_filter_reports_48h'.tr,",
            ),
            (
                "label: 'Amis',",
                "label: 'pawmap_filter_friends'.tr,",
            ),
            (
                "label: 'Demandes',",
                "label: 'pawmap_filter_requests'.tr,",
            ),
            (
                "label: 'Perdu',",
                "label: 'pawmap_filter_lost'.tr,",
            ),
            (
                "label: 'Chien méchant',",
                "label: 'pawmap_filter_aggressive_dog'.tr,",
            ),
            (
                "label: 'Point d\\'eau',",
                "label: 'pawmap_filter_water_point'.tr,",
            ),
            # Snackbar messages
            (
                "message: 'Aucune position trouvée pour \"$trimmed\".',",
                "message: 'pawmap_snack_city_not_found_msg'.trParams({'city': trimmed}),",
            ),
            (
                "message: 'Vérifiez votre connexion et réessayez.',",
                "message: 'pawmap_snack_search_failed_msg'.tr,",
            ),
            (
                "message: 'Tes amis ne voient plus ta position.',",
                "message: 'pawmap_snack_tracking_off_msg'.tr,",
            ),
            (
                "message: 'Tes amis voient ta position et celle de ton animal en live.',",
                "message: 'pawmap_snack_tracking_on_msg'.tr,",
            ),
            (
                "message: 'Signalement prolongé de 12h.',",
                "message: 'pawmap_snack_extended_msg'.tr,",
            ),
            (
                "message: 'Merci, un modérateur va vérifier.',",
                "message: 'pawmap_snack_reported_msg'.tr,",
            ),
            # Confirmations text (under reports)
            (
                "text: '${report.confirmationsCount} confirmation(s)',",
                "text: 'pawmap_confirmations_inline'.trParams({'count': report.confirmationsCount.toString()}),",
            ),
        ],
    )

    print()
    print("== Patch create_report_sheet.dart ==")
    patch_source(
        "create_report_sheet",
        SOURCE_FILES["create_report_sheet"],
        [
            (
                "title: 'Premium requis',",
                "title: 'pawmap_snack_premium_required'.tr,",
            ),
            (
                "title: 'Type requis',\n        message: 'Choisis un type de signalement avant d\\'envoyer.',",
                "title: 'pawmap_snack_type_required_title'.tr,\n        message: 'pawmap_snack_type_required_msg'.tr,",
            ),
            (
                "title: 'Signalement envoyé',\n        message: 'Visible 48h autour de vous. Merci !',",
                "title: 'pawmap_snack_sent_title'.tr,\n        message: 'pawmap_snack_sent_msg'.tr,",
            ),
            (
                "title: 'Envoi impossible',\n        message: 'Réessaie dans un instant.',",
                "title: 'pawmap_snack_send_failed_title'.tr,\n        message: 'pawmap_snack_send_failed_msg'.tr,",
            ),
        ],
    )
    print()
    print("== DONE ==")


if __name__ == "__main__":
    main()
