"""
HopeTSIT v23.1.149 — Inject PawMap i18n keys + patch source files.

Daniel : "sur la paw map les onglet au desuus perdu chien mechant etc c mal
traduit verifie tte les langue". Les labels (Caca, Pipi, Chien mechant...)
etaient deja traduits via map_report_label_* keys, mais les SECTION HEADERS
et autres strings UI du PawMap etaient hardcodes en FR :
  - 'Signaler autour de moi' (titre du bottom sheet)
  - 'Gratuits' / 'Premium' (sections)
  - 'Note (optionnel)' / 'Un detail utile pour les autres...'
  - 'Amis' / 'Suivre' / 'Live' / 'Refresh' (appbar actions)
  - 'Voir l\'annonce' / 'Demande ouverte' / 'Confirmer +12h'
  - etc.

Ce script :
  1. Injecte les cles i18n dans les 6 fichiers de translation
  2. Remplace les strings hardcoded dans create_report_sheet.dart et
     paw_map_screen.dart par des appels .tr

Sortie : modifie 8 fichiers en place. Le commit suivant doit etre verifie
au build avant de rebuild l'APK.
"""

import os
import re
from pathlib import Path

ROOT = Path(__file__).parent
LANG_DIR = ROOT / "frontend" / "lib" / "localization" / "translations"
SOURCE_FILES = {
    "create_report_sheet": ROOT / "frontend" / "lib" / "views" / "map" / "widgets" / "create_report_sheet.dart",
    "paw_map_screen": ROOT / "frontend" / "lib" / "views" / "map" / "paw_map_screen.dart",
}

# ─── Translations dictionary ────────────────────────────────────────────────
# Format : key -> {lang: translated_string}
TRANSLATIONS = {
    "pawmap_signal_title": {
        "fr": "Signaler autour de moi",
        "en": "Report around me",
        "es": "Señalar a mi alrededor",
        "de": "In meiner Nähe melden",
        "it": "Segnala intorno a me",
        "pt": "Sinalizar à minha volta",
    },
    "pawmap_signal_subtitle_premium": {
        "fr": "Visible 48h par les utilisateurs à proximité.",
        "en": "Visible for 48h to nearby users.",
        "es": "Visible 48h para los usuarios cercanos.",
        "de": "48 Std. für Nutzer in der Nähe sichtbar.",
        "it": "Visibile 48h agli utenti vicini.",
        "pt": "Visível 48h para utilizadores próximos.",
    },
    "pawmap_signal_subtitle_free": {
        "fr": "@count types gratuits. Les autres réservés Premium.",
        "en": "@count free types. Others reserved for Premium.",
        "es": "@count tipos gratuitos. Otros reservados Premium.",
        "de": "@count kostenlose Typen. Andere nur für Premium.",
        "it": "@count tipi gratuiti. Gli altri riservati Premium.",
        "pt": "@count tipos gratuitos. Outros reservados Premium.",
    },
    "pawmap_section_free": {
        "fr": "Gratuits",
        "en": "Free",
        "es": "Gratuitos",
        "de": "Kostenlos",
        "it": "Gratuiti",
        "pt": "Gratuitos",
    },
    "pawmap_section_free_subtitle": {
        "fr": "· accessible à tous",
        "en": "· accessible to all",
        "es": "· accesible para todos",
        "de": "· für alle zugänglich",
        "it": "· accessibile a tutti",
        "pt": "· acessível a todos",
    },
    "pawmap_section_premium": {
        "fr": "Premium",
        "en": "Premium",
        "es": "Premium",
        "de": "Premium",
        "it": "Premium",
        "pt": "Premium",
    },
    "pawmap_section_premium_unlocked": {
        "fr": "· @count types débloqués",
        "en": "· @count types unlocked",
        "es": "· @count tipos desbloqueados",
        "de": "· @count Typen freigeschaltet",
        "it": "· @count tipi sbloccati",
        "pt": "· @count tipos desbloqueados",
    },
    "pawmap_section_premium_locked": {
        "fr": "· @count types réservés",
        "en": "· @count types reserved",
        "es": "· @count tipos reservados",
        "de": "· @count Typen reserviert",
        "it": "· @count tipi riservati",
        "pt": "· @count tipos reservados",
    },
    "pawmap_note_label": {
        "fr": "Note (optionnel)",
        "en": "Note (optional)",
        "es": "Nota (opcional)",
        "de": "Notiz (optional)",
        "it": "Nota (opzionale)",
        "pt": "Nota (opcional)",
    },
    "pawmap_note_hint": {
        "fr": "Un détail utile pour les autres…",
        "en": "A useful detail for others…",
        "es": "Un detalle útil para los demás…",
        "de": "Ein nützliches Detail für andere…",
        "it": "Un dettaglio utile per gli altri…",
        "pt": "Um detalhe útil para os outros…",
    },
    "pawmap_btn_send": {
        "fr": "Signaler",
        "en": "Report",
        "es": "Señalar",
        "de": "Melden",
        "it": "Segnala",
        "pt": "Sinalizar",
    },
    "pawmap_appbar_friends": {
        "fr": "Amis",
        "en": "Friends",
        "es": "Amigos",
        "de": "Freunde",
        "it": "Amici",
        "pt": "Amigos",
    },
    "pawmap_appbar_follow": {
        "fr": "Suivre",
        "en": "Follow",
        "es": "Seguir",
        "de": "Folgen",
        "it": "Segui",
        "pt": "Seguir",
    },
    "pawmap_appbar_live": {
        "fr": "Live",
        "en": "Live",
        "es": "En vivo",
        "de": "Live",
        "it": "Live",
        "pt": "Ao vivo",
    },
    "pawmap_appbar_refresh": {
        "fr": "Rafraîchir",
        "en": "Refresh",
        "es": "Actualizar",
        "de": "Aktualisieren",
        "it": "Aggiorna",
        "pt": "Atualizar",
    },
    "pawmap_btn_view_post": {
        "fr": "Voir l'annonce",
        "en": "View post",
        "es": "Ver anuncio",
        "de": "Anzeige ansehen",
        "it": "Vedi annuncio",
        "pt": "Ver anúncio",
    },
    "pawmap_snack_post_opened_title": {
        "fr": "Demande ouverte",
        "en": "Post opened",
        "es": "Solicitud abierta",
        "de": "Anfrage geöffnet",
        "it": "Richiesta aperta",
        "pt": "Pedido aberto",
    },
    "pawmap_snack_post_opened_msg": {
        "fr": "Retrouve l'annonce complète dans l'onglet Accueil.",
        "en": "Find the full post in the Home tab.",
        "es": "Encuentra el anuncio completo en la pestaña Inicio.",
        "de": "Den vollständigen Beitrag im Home-Tab ansehen.",
        "it": "Trova l'annuncio completo nella scheda Home.",
        "pt": "Encontra o anúncio completo no separador Início.",
    },
    "pawmap_btn_confirm_extend": {
        "fr": "Confirmer +12h",
        "en": "Confirm +12h",
        "es": "Confirmar +12h",
        "de": "Bestätigen +12h",
        "it": "Conferma +12h",
        "pt": "Confirmar +12h",
    },
    "pawmap_btn_report_abuse": {
        "fr": "Signaler abus",
        "en": "Report abuse",
        "es": "Denunciar abuso",
        "de": "Missbrauch melden",
        "it": "Segnala abuso",
        "pt": "Denunciar abuso",
    },
    "pawmap_snack_thanks_title": {
        "fr": "Merci !",
        "en": "Thanks!",
        "es": "¡Gracias!",
        "de": "Danke!",
        "it": "Grazie!",
        "pt": "Obrigado!",
    },
    "pawmap_snack_reported_title": {
        "fr": "Signalé",
        "en": "Reported",
        "es": "Denunciado",
        "de": "Gemeldet",
        "it": "Segnalato",
        "pt": "Denunciado",
    },
    "pawmap_snack_no_loc_title": {
        "fr": "Localisation indisponible",
        "en": "Location unavailable",
        "es": "Localización no disponible",
        "de": "Standort nicht verfügbar",
        "it": "Posizione non disponibile",
        "pt": "Localização indisponível",
    },
    "pawmap_snack_no_loc_msg": {
        "fr": "Activez le GPS et les permissions.",
        "en": "Enable GPS and permissions.",
        "es": "Activa el GPS y los permisos.",
        "de": "GPS und Berechtigungen aktivieren.",
        "it": "Attiva GPS e autorizzazioni.",
        "pt": "Ativa o GPS e as permissões.",
    },
    "pawmap_snack_city_not_found": {
        "fr": "Ville introuvable",
        "en": "City not found",
        "es": "Ciudad no encontrada",
        "de": "Stadt nicht gefunden",
        "it": "Città non trovata",
        "pt": "Cidade não encontrada",
    },
    "pawmap_snack_search_failed": {
        "fr": "Recherche impossible",
        "en": "Search failed",
        "es": "Búsqueda imposible",
        "de": "Suche fehlgeschlagen",
        "it": "Ricerca impossibile",
        "pt": "Pesquisa impossível",
    },
    "pawmap_snack_tracking_off_title": {
        "fr": "Suivi désactivé",
        "en": "Tracking disabled",
        "es": "Seguimiento desactivado",
        "de": "Tracking deaktiviert",
        "it": "Tracciamento disattivato",
        "pt": "Seguimento desativado",
    },
    "pawmap_snack_tracking_on_title": {
        "fr": "Suivi activé",
        "en": "Tracking enabled",
        "es": "Seguimiento activado",
        "de": "Tracking aktiviert",
        "it": "Tracciamento attivato",
        "pt": "Seguimento ativado",
    },
    "pawmap_live_banner_title": {
        "fr": "Tu es en direct",
        "en": "You are live",
        "es": "Estás en vivo",
        "de": "Du bist live",
        "it": "Sei in diretta",
        "pt": "Estás ao vivo",
    },
    "pawmap_live_banner_msg": {
        "fr": "Tes amis & ta famille voient ta position",
        "en": "Friends & family see your position",
        "es": "Tus amigos y familia ven tu posición",
        "de": "Freunde & Familie sehen deine Position",
        "it": "Amici e familiari vedono la tua posizione",
        "pt": "Amigos e família veem a tua posição",
    },
    "pawmap_btn_stop": {
        "fr": "Stop",
        "en": "Stop",
        "es": "Parar",
        "de": "Stopp",
        "it": "Stop",
        "pt": "Parar",
    },
    "pawmap_loading": {
        "fr": "Chargement…",
        "en": "Loading…",
        "es": "Cargando…",
        "de": "Lädt…",
        "it": "Caricamento…",
        "pt": "A carregar…",
    },
    "pawmap_time_just_now": {
        "fr": "à l'instant",
        "en": "just now",
        "es": "ahora mismo",
        "de": "gerade eben",
        "it": "proprio ora",
        "pt": "agora mesmo",
    },
    "pawmap_distance_km": {
        "fr": "@km km",
        "en": "@km km",
        "es": "@km km",
        "de": "@km km",
        "it": "@km km",
        "pt": "@km km",
    },
    "pawmap_hours_remaining_label": {
        "fr": "@hours h restantes",
        "en": "@hours h left",
        "es": "@hours h restantes",
        "de": "@hours Std. übrig",
        "it": "@hours h rimaste",
        "pt": "@hours h restantes",
    },
    "pawmap_confirmations": {
        "fr": "@count confirmation(s)",
        "en": "@count confirmation(s)",
        "es": "@count confirmación(es)",
        "de": "@count Bestätigung(en)",
        "it": "@count conferma/e",
        "pt": "@count confirmação(ões)",
    },
}


def dart_escape(s):
    """Escape a string for Dart single-quoted literal."""
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")


def inject_into_lang_file(lang_code):
    path = LANG_DIR / f"{lang_code}.dart"
    text = path.read_text(encoding="utf-8")

    # Find the 'map_report_label_other' line to inject after the labels block
    anchor = re.search(
        r"('map_report_label_other':\s*'[^']*',\s*\n)",
        text,
    )
    if not anchor:
        print(f"  [SKIP] {lang_code}: anchor not found")
        return 0

    # Check what's already present to avoid duplicates
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
        print(f"  [{lang_code}] already up to date ({skipped} keys already present)")
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
            print(f"  [WARN] {name}: substring not found -> {old[:60]!r}")
    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"  [{name}] applied {changes} substitutions")
    return changes


def main():
    print("== Inject PawMap i18n keys ==")
    for lang in ["en", "fr", "es", "de", "it", "pt"]:
        inject_into_lang_file(lang)

    print()
    print("== Patch create_report_sheet.dart ==")
    patch_source(
        "create_report_sheet",
        SOURCE_FILES["create_report_sheet"],
        [
            (
                "text: 'Signaler autour de moi',",
                "text: 'pawmap_signal_title'.tr,",
            ),
            (
                "? 'Visible 48h par les utilisateurs à proximité.'\n                    : '${freeTypes.length} types gratuits. Les autres réservés Premium.',",
                "? 'pawmap_signal_subtitle_premium'.tr\n                    : 'pawmap_signal_subtitle_free'.trParams({'count': freeTypes.length.toString()}),",
            ),
            (
                "text: 'Gratuits',",
                "text: 'pawmap_section_free'.tr,",
            ),
            (
                "text: '· accessible à tous',",
                "text: 'pawmap_section_free_subtitle'.tr,",
            ),
            (
                "text: 'Premium',",
                "text: 'pawmap_section_premium'.tr,",
            ),
            (
                "text: _isPremium\n                  ? '· ${types.length} types débloqués'\n                  : '· ${types.length} types réservés',",
                "text: _isPremium\n                  ? 'pawmap_section_premium_unlocked'.trParams({'count': types.length.toString()})\n                  : 'pawmap_section_premium_locked'.trParams({'count': types.length.toString()}),",
            ),
            (
                "text: 'Note (optionnel)',",
                "text: 'pawmap_note_label'.tr,",
            ),
            (
                "hintText: 'Un détail utile pour les autres…',",
                "hintText: 'pawmap_note_hint'.tr,",
            ),
        ],
    )

    print()
    print("== Patch paw_map_screen.dart ==")
    patch_source(
        "paw_map_screen",
        SOURCE_FILES["paw_map_screen"],
        [
            (
                "text: 'Amis',",
                "text: 'pawmap_appbar_friends'.tr,",
            ),
            (
                "text: on ? 'Live' : 'Suivre',",
                "text: on ? 'pawmap_appbar_live'.tr : 'pawmap_appbar_follow'.tr,",
            ),
            (
                "tooltip: 'Rafraîchir',",
                "tooltip: 'pawmap_appbar_refresh'.tr,",
            ),
            (
                "text: 'Signaler',",
                "text: 'pawmap_btn_send'.tr,",
            ),
            (
                "text: 'Voir l\\'annonce',",
                "text: 'pawmap_btn_view_post'.tr,",
            ),
            (
                "title: 'Demande ouverte',",
                "title: 'pawmap_snack_post_opened_title'.tr,",
            ),
            (
                "message:\n                        'Retrouve l\\'annonce complète dans l\\'onglet Accueil.',",
                "message: 'pawmap_snack_post_opened_msg'.tr,",
            ),
            (
                "text: 'Confirmer +12h',",
                "text: 'pawmap_btn_confirm_extend'.tr,",
            ),
            (
                "text: 'Signaler abus',",
                "text: 'pawmap_btn_report_abuse'.tr,",
            ),
            (
                "title: 'Merci !',",
                "title: 'pawmap_snack_thanks_title'.tr,",
            ),
            (
                "title: 'Signalé',",
                "title: 'pawmap_snack_reported_title'.tr,",
            ),
            (
                "title: 'Localisation indisponible',",
                "title: 'pawmap_snack_no_loc_title'.tr,",
            ),
            (
                "message: 'Activez le GPS et les permissions.',",
                "message: 'pawmap_snack_no_loc_msg'.tr,",
            ),
            (
                "title: 'Ville introuvable',",
                "title: 'pawmap_snack_city_not_found'.tr,",
            ),
            (
                "title: 'Recherche impossible',",
                "title: 'pawmap_snack_search_failed'.tr,",
            ),
            (
                "title: 'Suivi désactivé',",
                "title: 'pawmap_snack_tracking_off_title'.tr,",
            ),
            (
                "title: 'Suivi activé',",
                "title: 'pawmap_snack_tracking_on_title'.tr,",
            ),
            (
                "text: 'Tu es en direct',",
                "text: 'pawmap_live_banner_title'.tr,",
            ),
            (
                "text: 'Tes amis & ta famille voient ta position',",
                "text: 'pawmap_live_banner_msg'.tr,",
            ),
            (
                "text: 'Stop',",
                "text: 'pawmap_btn_stop'.tr,",
            ),
            (
                "text: 'Chargement…',",
                "text: 'pawmap_loading'.tr,",
            ),
            (
                "if (diff.inMinutes < 1) return \"à l'instant\";",
                "if (diff.inMinutes < 1) return 'pawmap_time_just_now'.tr;",
            ),
        ],
    )
    print()
    print("== DONE ==")


if __name__ == "__main__":
    main()
