"""HopeTSIT v23.1.170 - Final 3 i18n keys (visible/premium tiers + auth msg)."""

import re
from pathlib import Path

ROOT = Path(__file__).parent
LANG_DIR = ROOT / "frontend" / "lib" / "localization" / "translations"

TRANSLATIONS = {
    "map_boost_tier_visible": {
        "fr": "Visible", "en": "Visible", "es": "Visible",
        "de": "Sichtbar", "it": "Visibile", "pt": "Visível",
    },
    "map_boost_tier_map_premium": {
        "fr": "Map Premium", "en": "Map Premium", "es": "Map Premium",
        "de": "Map Premium", "it": "Map Premium", "pt": "Map Premium",
    },
    "auth_multiple_roles_msg": {
        "fr": "Tu es ouvert en @role. Tu peux switcher depuis Profil → Switch rôle.",
        "en": "You are signed in as @role. Switch roles from Profile → Switch role.",
        "es": "Estás conectado como @role. Cambia de rol desde Perfil → Cambiar rol.",
        "de": "Du bist als @role angemeldet. Wechsle in Profil → Rolle wechseln.",
        "it": "Sei connesso come @role. Cambia ruolo da Profilo → Cambia ruolo.",
        "pt": "Estás ligado como @role. Muda de papel em Perfil → Mudar papel.",
    },
}

def inject(lang):
    path = LANG_DIR / f"{lang}.dart"
    text = path.read_text(encoding="utf-8")
    anchor = re.search(r"('common_close':\s*'[^']*',\s*\n)", text)
    if not anchor:
        return 0
    new_entries = []
    for key, langs in TRANSLATIONS.items():
        if f"'{key}'" in text:
            continue
        new_entries.append(f"      '{key}': '{langs[lang]}',")
    if not new_entries:
        return 0
    new_text = text[:anchor.end()] + "\n".join(new_entries) + "\n" + text[anchor.end():]
    path.write_text(new_text, encoding="utf-8")
    print(f"  [{lang}] +{len(new_entries)} keys")
    return len(new_entries)

for lang in ["en", "fr", "es", "de", "it", "pt"]:
    inject(lang)
print("DONE")
