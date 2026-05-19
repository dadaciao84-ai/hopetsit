"""
Audit complet i18n :
  - App Flutter : 6 fichiers `frontend/lib/localization/translations/*.dart`
  - Site Next.js : `website/src/lib/i18n/translations.ts` (6 blocs en 1 fichier)

Pour chaque langue (FR, ES, DE, IT, PT) compare avec EN (référence) et liste :
  1. Les clés présentes en EN mais MANQUANTES dans la langue
  2. Les clés présentes mais où la valeur est IDENTIQUE à EN
     (= probablement copie non traduite)

Sortie : `Downloads/HopeTSIT_i18n_audit.txt` lisible humain.
"""

import re
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP_DIR = ROOT / "frontend" / "lib" / "localization" / "translations"
WEB_FILE = ROOT / "website" / "src" / "lib" / "i18n" / "translations.ts"
OUTPUT = Path.home() / "Downloads" / "HopeTSIT_i18n_audit.txt"

LANGS = ["en", "fr", "es", "de", "it", "pt"]

# ─── Regex pour extraire les clés/valeurs ──────────────────────────────────
# Dart : 'key': 'value', OR "key": "value", (avec quotes simples ou doubles)
# Multi-line aussi (avec triple-quotes ou continuation '...').
DART_KV = re.compile(
    r"""['"]([a-zA-Z0-9_]+)['"]\s*:\s*(['"])([\s\S]*?)\2\s*,""",
    re.MULTILINE,
)

# TypeScript : key: 'value', OR "key": "value",
# v23.1.147 fix : la regex précédente exigeait `\n\s+` avant chaque clé,
# donc elle ratait les blocs compacts comme `key1: 'v1', key2: 'v2',` sur
# la même ligne. Cette nouvelle version match après un séparateur souple
# (début de ligne, espace, virgule ou tab).
TS_KV = re.compile(
    r"""(?:^|[\s,{])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(['"`])([\s\S]*?)\2""",
    re.MULTILINE,
)


def parse_dart(path):
    """Extrait dict {key: value} d'un fichier Dart de traductions."""
    text = path.read_text(encoding="utf-8")
    out = {}
    for m in DART_KV.finditer(text):
        key, _, value = m.group(1), m.group(2), m.group(3)
        # Concatène les "+ '...'" en ligne (rare mais arrive)
        out[key] = value.strip()
    return out


def parse_ts_blocks(path):
    """
    Extrait les dicts pour chaque langue dans translations.ts.
    Le fichier a 6 blocs `<lang>: { ... },` dans l'objet `t: Bundle`.
    """
    text = path.read_text(encoding="utf-8")
    result = {}
    for lang in LANGS:
        # Cherche `<lang>: {` puis match jusqu'au `},` de fermeture.
        # On utilise un parser balanced-braces simple.
        m = re.search(rf"\n  {lang}: \{{", text)
        if not m:
            continue
        start = m.end()
        depth = 1
        i = start
        while i < len(text) and depth > 0:
            c = text[i]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
            i += 1
        block = text[start:i-1]
        # Maintenant parse les key: 'value' dans ce bloc
        out = {}
        for mm in TS_KV.finditer(block):
            key, _, value = mm.group(1), mm.group(2), mm.group(3)
            out[key] = value.strip()
        result[lang] = out
    return result


def write_report(lines):
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Rapport généré : {OUTPUT}")
    print(f"   Taille : {OUTPUT.stat().st_size // 1024} Ko")


def main():
    lines = []
    lines.append("=" * 70)
    lines.append("AUDIT i18n HopeTSIT — Comparaison de toutes les langues vs EN")
    lines.append("=" * 70)
    lines.append("")

    # ─── 1. App Flutter ─────────────────────────────────────────────────
    lines.append("┌" + "─" * 68 + "┐")
    lines.append("│ APP FLUTTER (frontend/lib/localization/translations/)" + " " * 13 + "│")
    lines.append("└" + "─" * 68 + "┘")
    lines.append("")

    dicts = {}
    for lang in LANGS:
        f = APP_DIR / f"{lang}.dart"
        if not f.exists():
            lines.append(f"⚠ Fichier manquant : {f}")
            continue
        dicts[lang] = parse_dart(f)
        lines.append(f"  · {lang}.dart → {len(dicts[lang])} clés parsées")
    lines.append("")

    en_keys = set(dicts.get("en", {}).keys())
    en_dict = dicts.get("en", {})

    for lang in LANGS:
        if lang == "en":
            continue
        if lang not in dicts:
            continue
        d = dicts[lang]
        keys = set(d.keys())

        missing = sorted(en_keys - keys)
        # Clés présentes mais valeur identique à EN (probable non-traduit)
        same_as_en = []
        for k in en_keys & keys:
            if d[k] == en_dict.get(k) and len(en_dict.get(k, "")) > 3:
                # ignore les emojis ou strings courts type "OK"
                same_as_en.append(k)

        lines.append("─" * 70)
        lines.append(f"📋 {lang.upper()}.dart ({len(d)} clés)")
        lines.append("─" * 70)
        lines.append(f"  ❌ Clés MANQUANTES (présentes en EN, absentes ici) : {len(missing)}")
        for k in missing[:40]:  # limit affichage
            lines.append(f"     · {k}  →  EN: \"{en_dict[k][:60]}\"")
        if len(missing) > 40:
            lines.append(f"     ... (+ {len(missing) - 40} autres)")
        lines.append("")
        lines.append(f"  ⚠ Clés NON TRADUITES (valeur identique à EN) : {len(same_as_en)}")
        for k in same_as_en[:30]:
            lines.append(f"     · {k}  =  \"{en_dict[k][:60]}\"")
        if len(same_as_en) > 30:
            lines.append(f"     ... (+ {len(same_as_en) - 30} autres)")
        lines.append("")

    # ─── 2. Site web Next.js ────────────────────────────────────────────
    lines.append("")
    lines.append("┌" + "─" * 68 + "┐")
    lines.append("│ SITE WEB (website/src/lib/i18n/translations.ts)" + " " * 19 + "│")
    lines.append("└" + "─" * 68 + "┘")
    lines.append("")

    web_dicts = parse_ts_blocks(WEB_FILE)
    for lang in LANGS:
        if lang in web_dicts:
            lines.append(f"  · {lang} → {len(web_dicts[lang])} clés parsées")
    lines.append("")

    en_web = web_dicts.get("en", {})
    en_web_keys = set(en_web.keys())

    for lang in LANGS:
        if lang == "en" or lang not in web_dicts:
            continue
        d = web_dicts[lang]
        keys = set(d.keys())

        missing = sorted(en_web_keys - keys)
        same_as_en = []
        for k in en_web_keys & keys:
            if d[k] == en_web.get(k) and len(en_web.get(k, "")) > 3:
                same_as_en.append(k)

        lines.append("─" * 70)
        lines.append(f"📋 site {lang.upper()} ({len(d)} clés)")
        lines.append("─" * 70)
        lines.append(f"  ❌ Clés MANQUANTES : {len(missing)}")
        for k in missing[:30]:
            lines.append(f"     · {k}  →  EN: \"{en_web[k][:60]}\"")
        if len(missing) > 30:
            lines.append(f"     ... (+ {len(missing) - 30} autres)")
        lines.append("")
        lines.append(f"  ⚠ Clés NON TRADUITES (= EN) : {len(same_as_en)}")
        for k in same_as_en[:20]:
            lines.append(f"     · {k}  =  \"{en_web[k][:60]}\"")
        if len(same_as_en) > 20:
            lines.append(f"     ... (+ {len(same_as_en) - 20} autres)")
        lines.append("")

    # ─── 3. Récap ───────────────────────────────────────────────────────
    lines.append("")
    lines.append("=" * 70)
    lines.append("RÉCAP")
    lines.append("=" * 70)
    lines.append("")
    lines.append("App Flutter — total clés EN : " + str(len(en_keys)))
    for lang in LANGS:
        if lang == "en" or lang not in dicts:
            continue
        d = dicts[lang]
        m = len(en_keys - set(d.keys()))
        s = sum(1 for k in en_keys & set(d.keys())
                if d[k] == en_dict.get(k) and len(en_dict.get(k, "")) > 3)
        pct = 100 * (len(en_keys) - m - s) / len(en_keys) if en_keys else 0
        lines.append(f"  · {lang.upper()} : {len(d)} clés | "
                     f"{m} manquantes | {s} non-traduites | "
                     f"{pct:.0f}% couverture réelle")

    lines.append("")
    lines.append("Site Web — total clés EN : " + str(len(en_web_keys)))
    for lang in LANGS:
        if lang == "en" or lang not in web_dicts:
            continue
        d = web_dicts[lang]
        m = len(en_web_keys - set(d.keys()))
        s = sum(1 for k in en_web_keys & set(d.keys())
                if d[k] == en_web.get(k) and len(en_web.get(k, "")) > 3)
        pct = 100 * (len(en_web_keys) - m - s) / len(en_web_keys) if en_web_keys else 0
        lines.append(f"  · {lang.upper()} : {len(d)} clés | "
                     f"{m} manquantes | {s} non-traduites | "
                     f"{pct:.0f}% couverture réelle")

    write_report(lines)


if __name__ == "__main__":
    main()
