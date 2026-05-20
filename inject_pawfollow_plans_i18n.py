"""
HopeTSIT v23.1.153 - Translate PawFollow plan names + descriptions.

Daniel : "Faltan traducciones" - le label "PawFollow Famille" (FR) restait
visible meme en ES/DE/IT/PT, et les descriptions de plan etaient hardcoded
en francais ("Jusqu'a 5 membres", "Facture 1x par an", "Facture tous les mois").

Strategie : on garde les labels backend (changement de DB risque) et on
override en frontend via des cles i18n par plan key.
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent
LANG_DIR = ROOT / "frontend" / "lib" / "localization" / "translations"
COIN_SHOP = ROOT / "frontend" / "lib" / "views" / "boost" / "coin_shop_screen.dart"

TRANSLATIONS = {
    # Plan names (override backend labels)
    "pawfollow_plan_monthly": {
        "fr": "PawFollow Mensuel",
        "en": "PawFollow Monthly",
        "es": "PawFollow Mensual",
        "de": "PawFollow Monatlich",
        "it": "PawFollow Mensile",
        "pt": "PawFollow Mensal",
    },
    "pawfollow_plan_yearly": {
        "fr": "PawFollow Annuel",
        "en": "PawFollow Yearly",
        "es": "PawFollow Anual",
        "de": "PawFollow Jährlich",
        "it": "PawFollow Annuale",
        "pt": "PawFollow Anual",
    },
    "pawfollow_plan_family": {
        "fr": "PawFollow Famille",
        "en": "PawFollow Family",
        "es": "PawFollow Familia",
        "de": "PawFollow Familie",
        "it": "PawFollow Famiglia",
        "pt": "PawFollow Família",
    },
    # Plan subtitles
    "pawfollow_subtitle_monthly": {
        "fr": "Facturé tous les mois",
        "en": "Billed monthly",
        "es": "Facturado mensualmente",
        "de": "Monatlich abgerechnet",
        "it": "Fatturato mensilmente",
        "pt": "Faturado mensalmente",
    },
    "pawfollow_subtitle_yearly": {
        "fr": "Facturé 1x par an",
        "en": "Billed once a year",
        "es": "Facturado 1 vez al año",
        "de": "1x pro Jahr abgerechnet",
        "it": "Fatturato 1 volta all'anno",
        "pt": "Faturado 1x por ano",
    },
    "pawfollow_subtitle_family": {
        "fr": "Jusqu'à 5 membres • mensuel",
        "en": "Up to 5 members • monthly",
        "es": "Hasta 5 miembros • mensual",
        "de": "Bis zu 5 Mitglieder • monatlich",
        "it": "Fino a 5 membri • mensile",
        "pt": "Até 5 membros • mensal",
    },
    "pawfollow_yearly_savings": {
        "fr": " (35% off)",
        "en": " (35% off)",
        "es": " (35% off)",
        "de": " (35% off)",
        "it": " (35% off)",
        "pt": " (35% off)",
    },
    "pawfollow_per_day_suffix": {
        "fr": "/jour",
        "en": "/day",
        "es": "/día",
        "de": "/Tag",
        "it": "/giorno",
        "pt": "/dia",
    },
}


def dart_escape(s):
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")


def inject_into_lang_file(lang_code):
    path = LANG_DIR / f"{lang_code}.dart"
    text = path.read_text(encoding="utf-8")

    anchor = (
        re.search(r"('post_incomplete_for_request':\s*'[^']*',\s*\n)", text)
        or re.search(r"('walker_rate_hint_30':\s*'[^']*',\s*\n)", text)
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
    print(f"  [{lang_code}] inserted {len(new_entries)} keys (skipped {skipped})")
    return len(new_entries)


def patch_coin_shop():
    text = COIN_SHOP.read_text(encoding="utf-8")
    original = text
    substitutions = [
        # Plan label → translated key based on plan.plan
        (
            "final savings = isYearly ? ' (35% off)' : '';",
            "final savings = isYearly ? 'pawfollow_yearly_savings'.tr : '';",
        ),
        (
            "text: '${plan.label}$savings',",
            "text: '${('pawfollow_plan_${plan.plan}').tr}$savings',",
        ),
        # Subtitle hardcoded -> translated keys
        (
            "text: isFamily\n                              ? \"Jusqu'à 5 membres • mensuel\"\n                              : isYearly\n                                  ? 'Facturé 1x par an'\n                                  : 'Facturé tous les mois',",
            "text: isFamily\n                              ? 'pawfollow_subtitle_family'.tr\n                              : isYearly\n                                  ? 'pawfollow_subtitle_yearly'.tr\n                                  : 'pawfollow_subtitle_monthly'.tr,",
        ),
        # /jour suffix
        (
            "text: '${CurrencyHelper.format(plan.currency, plan.amountPerDay)}/jour',",
            "text: '${CurrencyHelper.format(plan.currency, plan.amountPerDay)}${'pawfollow_per_day_suffix'.tr}',",
        ),
    ]
    changes = 0
    for old, new in substitutions:
        if old in text:
            text = text.replace(old, new, 1)
            changes += 1
        else:
            print(f"  [WARN] coin_shop: not found -> {old[:80]!r}")
    if text != original:
        COIN_SHOP.write_text(text, encoding="utf-8")
        print(f"  [coin_shop] applied {changes} substitutions")
    return changes


def main():
    print("== Inject PawFollow plan i18n keys ==")
    for lang in ["en", "fr", "es", "de", "it", "pt"]:
        inject_into_lang_file(lang)
    print()
    print("== Patch coin_shop_screen.dart ==")
    patch_coin_shop()
    print("== DONE ==")


if __name__ == "__main__":
    main()
