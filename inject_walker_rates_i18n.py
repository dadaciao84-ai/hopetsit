"""
HopeTSIT v23.1.153 - Add 90min + 120min walker rate i18n keys.

Daniel : "Faltarian las tarifas para 90 y 120 minutos" - le form Walker
n'avait que 30 et 60. On rajoute les 2 durees populaires.
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent
LANG_DIR = ROOT / "frontend" / "lib" / "localization" / "translations"

TRANSLATIONS = {
    "walker_rate_90min_label": {
        "fr": "Tarif pour 90 min de balade",
        "en": "Rate for 90 min walk",
        "es": "Tarifa por 90 min de paseo",
        "de": "Tarif für 90 Min. Spaziergang",
        "it": "Tariffa per 90 min di passeggiata",
        "pt": "Tarifa para 90 min de passeio",
    },
    "walker_rate_120min_label": {
        "fr": "Tarif pour 120 min de balade",
        "en": "Rate for 120 min walk",
        "es": "Tarifa por 120 min de paseo",
        "de": "Tarif für 120 Min. Spaziergang",
        "it": "Tariffa per 120 min di passeggiata",
        "pt": "Tarifa para 120 min de passeio",
    },
    "walker_rate_hint_22": {
        "fr": "Ex : 22",
        "en": "e.g. 22",
        "es": "Ej: 22",
        "de": "z.B. 22",
        "it": "Es: 22",
        "pt": "Ex: 22",
    },
    "walker_rate_hint_30": {
        "fr": "Ex : 30",
        "en": "e.g. 30",
        "es": "Ej: 30",
        "de": "z.B. 30",
        "it": "Es: 30",
        "pt": "Ex: 30",
    },
}


def dart_escape(s):
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")


def inject_into_lang_file(lang_code):
    path = LANG_DIR / f"{lang_code}.dart"
    text = path.read_text(encoding="utf-8")

    # Use walker_rate_hint_15 as anchor (the last existing walker_rate key)
    anchor = re.search(r"('walker_rate_hint_15':\s*'[^']*',\s*\n)", text)
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
        print(f"  [{lang_code}] already up to date (skipped {skipped})")
        return 0

    insert_at = anchor.end()
    block = "\n".join(new_entries) + "\n"
    new_text = text[:insert_at] + block + text[insert_at:]
    path.write_text(new_text, encoding="utf-8")
    print(f"  [{lang_code}] inserted {len(new_entries)} keys (skipped {skipped})")
    return len(new_entries)


def main():
    print("== Inject walker rates 90/120 min i18n keys ==")
    for lang in ["en", "fr", "es", "de", "it", "pt"]:
        inject_into_lang_file(lang)
    print("== DONE ==")


if __name__ == "__main__":
    main()
