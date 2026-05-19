"""
v23.1.147 — Traduit les 4 docs légaux du fichier `legalContent.ts` du EN
vers FR/ES/DE/IT/PT.

Lit le fichier, parse les `TERMS_EN_SECTIONS`, `PRIVACY_EN_SECTIONS`,
`REFUND_EN_SECTIONS`, `IMPRINT_EN_SECTIONS`, traduit chaque entrée html
via deep-translator (Google), puis réécrit le fichier en remplaçant les
`placeholder(XXX_EN_SECTIONS)` par des objets avec sections traduites.

Préserve les balises HTML inline (<strong>, <a href>, <br/>) en les
protégeant par des tokens avant traduction.

Run : python translate_legal.py
Durée : ~10-15 min (rate-limit Google ~1 req/s, ~200 sections × 5 langues)
"""

import re
import time
import sys
from pathlib import Path

# SSL fix Windows
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
_orig_get = requests.get


def patched_get(*a, **kw):
    kw["verify"] = False
    return _orig_get(*a, **kw)


requests.get = patched_get
from deep_translator import GoogleTranslator  # noqa: E402

ROOT = Path(__file__).resolve().parent
LEGAL_FILE = ROOT / "website" / "src" / "lib" / "legalContent.ts"

TARGET_LANGS = ["fr", "es", "de", "it", "pt"]
# deep-translator language codes (most are ISO 639-1, EN/FR/ES/DE/IT identiques)
LANG_CODES = {
    "fr": "fr",
    "es": "es",
    "de": "de",
    "it": "it",
    "pt": "pt",
}

DOC_NAMES = ["TERMS", "PRIVACY", "REFUND", "IMPRINT"]
# Dates lastUpdated par langue (sera utilisé pour générer chaque LegalDoc)
LAST_UPDATED_BY_LANG = {
    "en": "April 25, 2026",
    "fr": "25 avril 2026",
    "es": "25 de abril de 2026",
    "de": "25. April 2026",
    "it": "25 aprile 2026",
    "pt": "25 de abril de 2026",
}

# Patterns à protéger pendant la traduction.
# - Balises HTML inline : <strong>...</strong>, <a href="...">...</a>, <br/>
# - Tokens à conserver tels quels : ©, &amp;, &mdash;, etc.
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")


def protect_html(text: str):
    """Remplace les balises HTML par des tokens uniques avant traduction."""
    tokens = {}
    counter = [0]

    def replace(m):
        token = f"XHTML{counter[0]}X"
        tokens[token] = m.group(0)
        counter[0] += 1
        return token

    protected = HTML_TAG_PATTERN.sub(replace, text)
    return protected, tokens


def restore_html(text: str, tokens: dict) -> str:
    for token, original in tokens.items():
        text = re.sub(re.escape(token), original, text, flags=re.IGNORECASE)
        text = re.sub(re.escape(token.lower()), original, text)
    return text


def translate_text(text: str, target: str, translator: GoogleTranslator) -> str:
    """Traduit un texte en protégeant les balises HTML."""
    if not text.strip():
        return text
    protected, tokens = protect_html(text)
    try:
        translated = translator.translate(protected)
        if not translated:
            return text
        return restore_html(translated, tokens)
    except Exception as e:
        print(f"   ⚠ translate error: {e}")
        return text


# Parser ULTRA-simple pour extraire les sections EN du fichier TS.
# Format attendu :
#   const XXX_EN_SECTIONS: LegalSection[] = [
#     { type: "p", html: `...` },
#     { type: "h2", html: `...` },
#     { type: "ul", html: [`...`, `...`] },
#     ...
#   ];
SECTION_RE = re.compile(
    r'\{\s*type:\s*"(h2|p|ul)"\s*,\s*html:\s*(.*?)\s*\}',
    re.DOTALL,
)


def parse_html_value(raw: str):
    """Parse le `html:` d'une section. Soit un backtick-string, soit une liste."""
    raw = raw.strip()
    if raw.startswith("`"):
        # Single backtick string : `...`
        # Trouve la fermeture du premier backtick
        end = raw.index("`", 1)
        return raw[1:end]
    if raw.startswith("["):
        # Liste de backtick-strings : [`a`, `b`, ...]
        items = re.findall(r"`([^`]*)`", raw)
        return items
    return raw


def extract_en_sections(text: str, doc_name: str):
    """Extrait la liste de sections EN pour un doc donné (ex: 'TERMS')."""
    # Cherche `const <DOC>_EN_SECTIONS: LegalSection[] = [...];`
    pattern = re.compile(
        rf"const {doc_name}_EN_SECTIONS:\s*LegalSection\[\]\s*=\s*\[(.*?)\];",
        re.DOTALL,
    )
    m = pattern.search(text)
    if not m:
        print(f"⚠ Could not find {doc_name}_EN_SECTIONS")
        return []
    block = m.group(1)

    sections = []
    for sm in SECTION_RE.finditer(block):
        kind = sm.group(1)
        raw_value = sm.group(2)
        value = parse_html_value(raw_value)
        sections.append({"type": kind, "html": value})
    return sections


def render_sections_ts(sections: list, indent: str = "  ") -> str:
    """Rend une liste de sections sous forme de TS code."""
    lines = ["["]
    for s in sections:
        if s["type"] == "ul":
            items = ",\n".join(
                f'{indent}    `{escape_backticks(it)}`' for it in s["html"]
            )
            lines.append(f'{indent}  {{ type: "ul", html: [')
            lines.append(items)
            lines.append(f"{indent}  ]}},")
        else:
            content = escape_backticks(s["html"])
            lines.append(
                f'{indent}  {{ type: "{s["type"]}", html: `{content}` }},'
            )
    lines.append(f"{indent}]")
    return "\n".join(lines)


def escape_backticks(s: str) -> str:
    # Évite les backticks dans le contenu (rare mais possible après traduction)
    return s.replace("`", "\\`").replace("${", "\\${")


def main():
    print(f"📖 Reading {LEGAL_FILE}")
    text = LEGAL_FILE.read_text(encoding="utf-8")

    # Backup
    backup = LEGAL_FILE.with_suffix(".ts.before-translate")
    backup.write_text(text, encoding="utf-8")
    print(f"💾 Backup → {backup.name}\n")

    # 1) Extract EN sections for each doc
    en_sections_by_doc = {}
    for doc in DOC_NAMES:
        sections = extract_en_sections(text, doc)
        en_sections_by_doc[doc] = sections
        print(f"   {doc}: {len(sections)} sections EN parsed")

    # 2) Translate each doc into each target lang
    translated = {}  # translated[doc][lang] = list of sections
    for doc in DOC_NAMES:
        translated[doc] = {"en": en_sections_by_doc[doc]}

    total_units = sum(
        sum(1 if isinstance(s["html"], str) else len(s["html"])
            for s in en_sections_by_doc[d])
        for d in DOC_NAMES
    ) * len(TARGET_LANGS)
    print(f"\n🌐 Total units to translate: ~{total_units} ({len(TARGET_LANGS)} langs × ~{total_units // len(TARGET_LANGS)} units/lang)")
    print(f"   Estimated duration: ~{total_units // 60 + 1} min (rate-limit)\n")

    unit_count = 0
    for lang in TARGET_LANGS:
        code = LANG_CODES[lang]
        translator = GoogleTranslator(source="en", target=code)
        print(f"── Translating to {lang.upper()} ──")
        for doc in DOC_NAMES:
            new_sections = []
            for s in en_sections_by_doc[doc]:
                if s["type"] == "ul":
                    new_items = []
                    for it in s["html"]:
                        unit_count += 1
                        new_items.append(translate_text(it, code, translator))
                        time.sleep(0.25)
                    new_sections.append({"type": "ul", "html": new_items})
                else:
                    unit_count += 1
                    new_sections.append({
                        "type": s["type"],
                        "html": translate_text(s["html"], code, translator),
                    })
                    time.sleep(0.25)
            translated[doc][lang] = new_sections
            print(f"   · {doc}: done ({unit_count} units total)")
        print()

    # 3) Replace placeholder() calls in the file with the translated content
    for doc in DOC_NAMES:
        doc_key = doc.lower()
        rendered = {}
        for lang in ["en", "fr", "es", "de", "it", "pt"]:
            sections_ts = render_sections_ts(translated[doc][lang], indent="  ")
            last_up = LAST_UPDATED_BY_LANG[lang]
            rendered[lang] = (
                f'{{\n'
                f'    lastUpdated: "{last_up}",\n'
                f'    sections: {sections_ts},\n'
                f'  }}'
            )

        # Find and replace the export block for this doc
        doc_var = doc
        export_pattern = re.compile(
            rf"export const {doc_var}: LegalDocByLang = \{{[^}}]+placeholder\([^)]+\),\s*"
            rf"[^}}]+placeholder\([^)]+\),\s*"
            rf"[^}}]+placeholder\([^)]+\),\s*"
            rf"[^}}]+placeholder\([^)]+\),\s*"
            rf"[^}}]+placeholder\([^)]+\),\s*"
            rf"[^}}]+placeholder\([^)]+\),?\s*\}};",
            re.DOTALL,
        )
        new_block = (
            f"export const {doc_var}: LegalDocByLang = {{\n"
            f"  en: {rendered['en']},\n"
            f"  fr: {rendered['fr']},\n"
            f"  es: {rendered['es']},\n"
            f"  de: {rendered['de']},\n"
            f"  it: {rendered['it']},\n"
            f"  pt: {rendered['pt']},\n"
            f"}};"
        )
        text, n = export_pattern.subn(new_block, text)
        print(f"   {doc} export block replaced: {n} matches")

    # 4) Write final file
    LEGAL_FILE.write_text(text, encoding="utf-8")
    print(f"\n✅ Done. {LEGAL_FILE} updated.")
    print(f"   Backup kept at: {backup}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹  Interrupted.")
        sys.exit(1)
