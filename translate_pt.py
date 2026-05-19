"""
Auto-traduit les 818 strings du fichier `pt.dart` qui sont restées en anglais
(copies du fichier en.dart non traduites).

Méthode :
  1. Parse en.dart pour extraire {key: english_value}
  2. Parse pt.dart pour extraire {key: portuguese_value}
  3. Pour chaque clé où PT == EN (= probable copie non traduite) :
     a. Détecte les placeholders (@xxx, {xxx}, \\n, {0}, etc.)
     b. Les remplace par des tokens uniques pour les protéger
     c. Appelle Google Translate (en → pt)
     d. Remet les placeholders à leur place
  4. Réécrit pt.dart avec les nouvelles valeurs
  5. Crée un backup pt.dart.before-autotranslate

Run : python translate_pt.py
Durée : ~5-10 min (rate-limit Google ~1 req/s)
"""

import re
import time
import shutil
import sys
from pathlib import Path

# ─── SSL fix Windows ────────────────────────────────────────────────────────
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
_orig_get = requests.get


def patched_get(*a, **kw):
    kw['verify'] = False
    return _orig_get(*a, **kw)


requests.get = patched_get

from deep_translator import GoogleTranslator  # noqa: E402

ROOT = Path(__file__).resolve().parent
APP_DIR = ROOT / "frontend" / "lib" / "localization" / "translations"
EN_FILE = APP_DIR / "en.dart"
PT_FILE = APP_DIR / "pt.dart"

# Regex Dart key:value (gère single quotes principalement, le fichier est en ').
DART_KV = re.compile(
    r"""['"]([a-zA-Z0-9_]+)['"]\s*:\s*(['"])([\s\S]*?)\2\s*,""",
    re.MULTILINE,
)

# Placeholders à protéger pendant la traduction.
# Patterns : @count, @name, @rating | {0}, {name} | \\n, \\t
PLACEHOLDER_PATTERNS = [
    re.compile(r"@[a-zA-Z_][a-zA-Z0-9_]*"),  # @count, @name
    re.compile(r"\{[a-zA-Z0-9_]*\}"),         # {0}, {name}
    re.compile(r"\\[ntr]"),                   # \n, \t, \r
    re.compile(r"\\\$"),                      # \$
]


def parse_dart(path: Path):
    text = path.read_text(encoding="utf-8")
    out = {}
    for m in DART_KV.finditer(text):
        key = m.group(1)
        value = m.group(3)
        out[key] = value
    return out


def protect_placeholders(text: str):
    """Remplace les placeholders par des tokens uniques pour la traduction."""
    placeholders = {}
    counter = [0]

    def replace(m):
        token = f"XPLH{counter[0]}X"
        placeholders[token] = m.group(0)
        counter[0] += 1
        return token

    protected = text
    for pat in PLACEHOLDER_PATTERNS:
        protected = pat.sub(replace, protected)
    return protected, placeholders


def restore_placeholders(text: str, placeholders: dict):
    """Remet les tokens à leur valeur originale."""
    for token, original in placeholders.items():
        # Google peut renvoyer le token en minuscules ou avec espaces
        text = re.sub(re.escape(token), original, text, flags=re.IGNORECASE)
        # Variantes parfois retournées
        text = re.sub(re.escape(token.lower()), original, text)
    return text


def is_translatable(value: str) -> bool:
    """Skip les strings vides, juste des emojis, ou très courtes."""
    stripped = value.strip()
    if len(stripped) < 4:
        return False
    # Si c'est juste des emojis + ponctuation, skip.
    if not any(c.isalpha() for c in stripped):
        return False
    return True


def main():
    if not EN_FILE.exists() or not PT_FILE.exists():
        print(f"❌ Fichiers introuvables ({EN_FILE} et/ou {PT_FILE})")
        sys.exit(1)

    print(f"📖 Parse {EN_FILE.name}…")
    en_dict = parse_dart(EN_FILE)
    print(f"   {len(en_dict)} clés EN trouvées")

    print(f"📖 Parse {PT_FILE.name}…")
    pt_dict = parse_dart(PT_FILE)
    print(f"   {len(pt_dict)} clés PT trouvées")

    # Identifie les clés à traduire : PT == EN et translatable.
    to_translate = []
    for key, en_value in en_dict.items():
        pt_value = pt_dict.get(key)
        if pt_value == en_value and is_translatable(en_value):
            to_translate.append(key)

    print(f"\n🌐 {len(to_translate)} strings à traduire (EN → PT)")
    print(f"   Délai estimé : ~{len(to_translate) // 60 + 1} min "
          f"(rate-limit Google ~1/sec)")
    print()

    if not to_translate:
        print("✅ Rien à traduire.")
        return

    # Backup pt.dart
    backup = PT_FILE.with_suffix(".dart.before-autotranslate")
    shutil.copy(PT_FILE, backup)
    print(f"💾 Backup : {backup.name}")

    translator = GoogleTranslator(source="en", target="pt")
    pt_text = PT_FILE.read_text(encoding="utf-8")

    translated = 0
    failed = 0
    skipped = 0

    for i, key in enumerate(to_translate, 1):
        en_value = en_dict[key]
        protected, placeholders = protect_placeholders(en_value)

        try:
            translation = translator.translate(protected)
            if not translation or translation == protected:
                skipped += 1
                continue
            translation = restore_placeholders(translation, placeholders)
            # Replace dans pt_text — utilise une regex stricte pour matcher
            # uniquement la valeur de cette clé.
            old_pattern = re.compile(
                rf"(['\"]{re.escape(key)}['\"]\s*:\s*['\"])"
                + re.escape(en_value)
                + r"(['\"]\s*,)"
            )
            # Échappe les caractères dart-spéciaux dans la nouvelle valeur :
            # principalement les single-quotes si la valeur est entre 'single'
            # quotes. On utilise des double quotes si la trad contient des
            # single quotes.
            new_value = translation.replace("\\", "\\\\")
            if "'" in new_value:
                # Switch vers double quotes pour éviter d'échapper les '.
                # Et on échappe les " déjà présents.
                new_value = new_value.replace('"', '\\"')
                # Le pattern accepte les 2 sortes de quotes via les groupes.
                pt_text, n = old_pattern.subn(
                    lambda m: f"'{key}': \"{new_value}\",",
                    pt_text,
                )
            else:
                pt_text, n = old_pattern.subn(
                    lambda m: f"'{key}': '{new_value}',",
                    pt_text,
                )

            if n == 0:
                # Fallback : pas matché (peut-être value sur plusieurs lignes).
                # On skip et on log.
                failed += 1
            else:
                translated += 1

        except Exception as e:
            failed += 1
            print(f"   ⚠ {key}: {e}")

        # Progress chaque 25 strings
        if i % 25 == 0:
            print(f"   [{i:4}/{len(to_translate)}] "
                  f"{translated} traduites, {failed} échouées, {skipped} skip")

        # Rate-limit : 0.3s entre requêtes pour ne pas se faire ban
        time.sleep(0.3)

    # Écrit le résultat
    PT_FILE.write_text(pt_text, encoding="utf-8")

    print()
    print("=" * 50)
    print(f"✅ Terminé : {translated} traduites, "
          f"{failed} échouées, {skipped} skip")
    print(f"   Fichier mis à jour : {PT_FILE}")
    print(f"   Backup conservé    : {backup}")
    print("=" * 50)
    print()
    print("👉 Relance `python audit_i18n.py` pour confirmer le résultat.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹  Interrompu par l'utilisateur.")
        sys.exit(1)
