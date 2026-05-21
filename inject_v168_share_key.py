"""HopeTSIT v23.1.168 - Add the share-message fallback key for 6 langs."""

import re
from pathlib import Path

ROOT = Path(__file__).parent
LANG_DIR = ROOT / "frontend" / "lib" / "localization" / "translations"

TRANSLATIONS = {
    "post_card_default_share_message": {
        "fr": "Découvre cette annonce sur HoPetSit !",
        "en": "Check out this listing on HoPetSit!",
        "es": "¡Mira este anuncio en HoPetSit!",
        "de": "Schau dir diese Anzeige auf HoPetSit an!",
        "it": "Dai un'occhiata a questo annuncio su HoPetSit!",
        "pt": "Vê este anúncio na HoPetSit!",
    },
}


def dart_escape(s):
    return s.replace("\\", "\\\\").replace("'", "\\'")


def inject(lang):
    path = LANG_DIR / f"{lang}.dart"
    text = path.read_text(encoding="utf-8")
    anchor = re.search(r"('post_card_reservation_request':\s*'[^']*',\s*\n)", text)
    if not anchor:
        print(f"  [SKIP] {lang}")
        return 0
    if "'post_card_default_share_message'" in text:
        return 0
    insert_at = anchor.end()
    line = f"      'post_card_default_share_message': '{dart_escape(TRANSLATIONS['post_card_default_share_message'][lang])}',\n"
    new_text = text[:insert_at] + line + text[insert_at:]
    path.write_text(new_text, encoding="utf-8")
    print(f"  [{lang}] +1 key")
    return 1


for lang in ["en", "fr", "es", "de", "it", "pt"]:
    inject(lang)
