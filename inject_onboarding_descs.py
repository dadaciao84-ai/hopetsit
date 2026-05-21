"""
HopeTSIT v23.1.166 - Onboarding feature descriptions.

Daniel mockup : chaque carte (Pet-sitting / PawMap / PawFollow) a un titre
+ une description courte en-dessous. On ajoute 3 cles i18n x 6 langues.
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent
LANG_DIR = ROOT / "frontend" / "lib" / "localization" / "translations"

TRANSLATIONS = {
    "onboarding_feature_trusted_desc": {
        "fr": "Trouvez des pet-sitters de confiance près de chez vous.",
        "en": "Find trusted pet-sitters near you.",
        "es": "Encuentra cuidadores de confianza cerca de ti.",
        "de": "Finde vertrauenswürdige Tiersitter in deiner Nähe.",
        "it": "Trova pet-sitter di fiducia vicino a te.",
        "pt": "Encontra pet-sitters de confiança perto de ti.",
    },
    "onboarding_feature_chat_desc": {
        "fr": "Explorez les lieux pet-friendly autour de vous sur la carte interactive.",
        "en": "Explore pet-friendly places around you on the interactive map.",
        "es": "Explora los lugares pet-friendly a tu alrededor en el mapa interactivo.",
        "de": "Entdecke tierfreundliche Orte in deiner Nähe auf der interaktiven Karte.",
        "it": "Esplora i luoghi pet-friendly intorno a te sulla mappa interattiva.",
        "pt": "Explora os locais pet-friendly à tua volta no mapa interativo.",
    },
    "onboarding_feature_nearby_desc": {
        "fr": "Suivez les aventures de votre animal et partagez ses moments.",
        "en": "Follow your pet's adventures and share its moments.",
        "es": "Sigue las aventuras de tu mascota y comparte sus momentos.",
        "de": "Verfolge die Abenteuer deines Tieres und teile seine Momente.",
        "it": "Segui le avventure del tuo animale e condividi i suoi momenti.",
        "pt": "Segue as aventuras do teu animal e partilha os seus momentos.",
    },
}


def dart_escape(s):
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")


def inject(lang):
    path = LANG_DIR / f"{lang}.dart"
    text = path.read_text(encoding="utf-8")
    # Anchor : onboarding_feature_nearby (la 3eme cle existante)
    anchor = re.search(r"('onboarding_feature_nearby':\s*'[^']*',\s*\n)", text)
    if not anchor:
        print(f"  [SKIP] {lang}: anchor not found")
        return 0
    new_entries = []
    skipped = 0
    for key, langs in TRANSLATIONS.items():
        if f"'{key}'" in text:
            skipped += 1
            continue
        new_entries.append(f"      '{key}': '{dart_escape(langs[lang])}',")
    if not new_entries:
        return 0
    insert_at = anchor.end()
    new_text = text[:insert_at] + "\n".join(new_entries) + "\n" + text[insert_at:]
    path.write_text(new_text, encoding="utf-8")
    print(f"  [{lang}] +{len(new_entries)} keys (skipped {skipped})")
    return len(new_entries)


def main():
    print("== Inject onboarding feature descriptions ==")
    for lang in ["en", "fr", "es", "de", "it", "pt"]:
        inject(lang)
    print("== DONE ==")


if __name__ == "__main__":
    main()
