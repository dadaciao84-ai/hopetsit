"""
HopeTSIT v23.1.153 - Add post_incomplete_for_request i18n key.

Daniel : "demande direct" bouton manquant. Solution : on rend le bouton
toujours visible et on snackbar si donnees incompletes.
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent
LANG_DIR = ROOT / "frontend" / "lib" / "localization" / "translations"

TRANSLATIONS = {
    "post_incomplete_for_request": {
        "fr": "Cette publication n'a pas toutes les informations nécessaires pour envoyer une demande directe.",
        "en": "This post is missing some details needed to send a direct request.",
        "es": "Esta publicación no tiene todos los datos necesarios para enviar una solicitud directa.",
        "de": "Diesem Beitrag fehlen einige Angaben, um eine direkte Anfrage zu senden.",
        "it": "A questa pubblicazione mancano alcuni dettagli per inviare una richiesta diretta.",
        "pt": "Esta publicação não tem todos os dados necessários para enviar um pedido direto.",
    },
}


def dart_escape(s):
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")


def inject_into_lang_file(lang_code):
    path = LANG_DIR / f"{lang_code}.dart"
    text = path.read_text(encoding="utf-8")

    # Anchor: walker_rate_hint_30 (v153 just added it) or fallback
    anchor = (
        re.search(r"('walker_rate_hint_30':\s*'[^']*',\s*\n)", text)
        or re.search(r"('walker_rate_hint_15':\s*'[^']*',\s*\n)", text)
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
        value = dart_escape(langs[lang_code])
        new_entries.append(f"      '{key}': '{value}',")

    if not new_entries:
        return 0

    insert_at = anchor.end()
    block = "\n".join(new_entries) + "\n"
    new_text = text[:insert_at] + block + text[insert_at:]
    path.write_text(new_text, encoding="utf-8")
    print(f"  [{lang_code}] inserted {len(new_entries)} keys")
    return len(new_entries)


def main():
    print("== Inject post_incomplete_for_request key ==")
    for lang in ["en", "fr", "es", "de", "it", "pt"]:
        inject_into_lang_file(lang)
    print("== DONE ==")


if __name__ == "__main__":
    main()
