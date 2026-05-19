"""
HopeTSIT v23.1.151 - Audit i18n exhaustif PawMap + CreateReportSheet.

Daniel : "paw spot le bouton publier signalement et aussi pas traduit ... et
verifie les traductions aussi de tte les langue".

Cette passe finale balaie create_report_sheet.dart et paw_map_screen.dart
pour trouver TOUTES les strings hardcoded FR restantes :
  - 'Envoi...' / 'Publier le signalement' (bouton submit)
  - 'Acheter abonnement' / 'pour signaler...' (premium upsell)
  - autres strings detectees a l'audit
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

TRANSLATIONS = {
    # Submit button
    "pawmap_btn_submit_sending": {
        "fr": "Envoi…",
        "en": "Sending…",
        "es": "Enviando…",
        "de": "Wird gesendet…",
        "it": "Invio…",
        "pt": "A enviar…",
    },
    "pawmap_btn_submit": {
        "fr": "Publier le signalement",
        "en": "Publish report",
        "es": "Publicar señalamiento",
        "de": "Meldung veröffentlichen",
        "it": "Pubblica segnalazione",
        "pt": "Publicar sinalização",
    },
    # Time ago short labels (used in InfoWindow snippets)
    "pawmap_time_min_short": {
        "fr": "@n min",
        "en": "@n min",
        "es": "@n min",
        "de": "@n Min.",
        "it": "@n min",
        "pt": "@n min",
    },
    "pawmap_time_hours_short": {
        "fr": "@n h",
        "en": "@n h",
        "es": "@n h",
        "de": "@n Std.",
        "it": "@n h",
        "pt": "@n h",
    },
    "pawmap_time_days_short": {
        "fr": "@n j",
        "en": "@n d",
        "es": "@n d",
        "de": "@n T.",
        "it": "@n g",
        "pt": "@n d",
    },
    "pawmap_remaining_hours_label": {
        "fr": "@hours h restantes",
        "en": "@hours h left",
        "es": "@hours h restantes",
        "de": "@hours Std. übrig",
        "it": "@hours h rimaste",
        "pt": "@hours h restantes",
    },
    # Default provider name fallback
    "pawmap_default_walker": {
        "fr": "Walker",
        "en": "Walker",
        "es": "Paseador",
        "de": "Walker",
        "it": "Walker",
        "pt": "Walker",
    },
    "pawmap_default_sitter": {
        "fr": "Sitter",
        "en": "Sitter",
        "es": "Cuidador",
        "de": "Sitter",
        "it": "Sitter",
        "pt": "Sitter",
    },
    "pawmap_default_request": {
        "fr": "Demande",
        "en": "Request",
        "es": "Solicitud",
        "de": "Anfrage",
        "it": "Richiesta",
        "pt": "Pedido",
    },
}


def dart_escape(s):
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")


def inject_into_lang_file(lang_code):
    path = LANG_DIR / f"{lang_code}.dart"
    text = path.read_text(encoding="utf-8")

    # Try multiple anchors in order
    anchor = (
        re.search(r"('mapboost_info_visibility':\s*'[^']*',\s*\n)", text)
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
    print("== Inject final remaining i18n keys ==")
    for lang in ["en", "fr", "es", "de", "it", "pt"]:
        inject_into_lang_file(lang)

    print()
    print("== Patch create_report_sheet.dart ==")
    patch_source(
        "create_report_sheet",
        SOURCE_FILES["create_report_sheet"],
        [
            (
                "text: submitting ? 'Envoi…' : 'Publier le signalement',",
                "text: submitting ? 'pawmap_btn_submit_sending'.tr : 'pawmap_btn_submit'.tr,",
            ),
        ],
    )

    print()
    print("== Patch paw_map_screen.dart ==")
    patch_source(
        "paw_map_screen",
        SOURCE_FILES["paw_map_screen"],
        [
            # time ago short labels
            (
                "if (diff.inMinutes < 60) return '${diff.inMinutes} min';",
                "if (diff.inMinutes < 60) return 'pawmap_time_min_short'.trParams({'n': diff.inMinutes.toString()});",
            ),
            (
                "if (diff.inHours < 24) return '${diff.inHours} h';",
                "if (diff.inHours < 24) return 'pawmap_time_hours_short'.trParams({'n': diff.inHours.toString()});",
            ),
            (
                "return '${diff.inDays} j';",
                "return 'pawmap_time_days_short'.trParams({'n': diff.inDays.toString()});",
            ),
            # InfoWindow snippet for reports
            (
                "'${r.liveHoursRemaining.toStringAsFixed(0)}h restantes · ${r.confirmationsCount} confirmation(s)',",
                "'${'pawmap_remaining_hours_label'.trParams({'hours': r.liveHoursRemaining.toStringAsFixed(0)})} · ${'pawmap_confirmations'.trParams({'count': r.confirmationsCount.toString()})}',",
            ),
            # Default walker/sitter fallback names in marker title
            (
                "'${role == 'walker' ? '🐕' : '🐾'} ${name.isNotEmpty ? name : (role == 'walker' ? 'Walker' : 'Sitter')}'",
                "'${role == 'walker' ? '🐕' : '🐾'} ${name.isNotEmpty ? name : (role == 'walker' ? 'pawmap_default_walker'.tr : 'pawmap_default_sitter'.tr)}'",
            ),
            # Request default name fallback
            (
                "'📣 ${req.ownerName.isNotEmpty ? req.ownerName : 'Demande'}'",
                "'📣 ${req.ownerName.isNotEmpty ? req.ownerName : 'pawmap_default_request'.tr}'",
            ),
        ],
    )
    print()
    print("== DONE ==")


if __name__ == "__main__":
    main()
