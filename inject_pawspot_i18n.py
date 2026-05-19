"""
HopeTSIT v23.1.150 - Inject PawSpot/MapBoost i18n keys + patch source files.

Daniel : "que tout les option du halo dans pawspot fonctionne reverifie par
option". Verification par tier :
  - bronze   -> hueAzure  (bleu)   - 'Visible (24h)'
  - silver   -> hueViolet (violet) - 'Pin surligne (7j)'
  - gold     -> hueYellow (jaune)  - 'Pin dore (15j)'
  - platinum -> hueOrange + halo   - 'Pin dore + halo (30j)'

Les visuels par tier marchent (verifie dans paw_map_screen.dart _buildMarkers
et _buildHaloCircles). Mais beaucoup de strings du flux d'achat etaient
hardcoded en FR :
  - Descriptions des tiers dans la boutique
  - Confirm dialog ("Acheter PawSpot... ?", "Tier:", "Duree:", "Prix:")
  - Marker tooltips ("Visible (24h)", "Pin dore (15j)"...)
  - Snackbars de succes/echec

Ce script :
  1. Injecte 18 nouvelles cles dans les 6 fichiers de translation
  2. Patche coin_shop_screen.dart et paw_map_screen.dart pour utiliser .tr
"""

import os
import re
from pathlib import Path

ROOT = Path(__file__).parent
LANG_DIR = ROOT / "frontend" / "lib" / "localization" / "translations"
SOURCE_FILES = {
    "coin_shop": ROOT / "frontend" / "lib" / "views" / "boost" / "coin_shop_screen.dart",
    "paw_map": ROOT / "frontend" / "lib" / "views" / "map" / "paw_map_screen.dart",
}

TRANSLATIONS = {
    # Tier descriptions dans la boutique PawSpot
    "mapboost_desc_bronze": {
        "fr": "Testez la visibilité carte",
        "en": "Try map visibility",
        "es": "Prueba la visibilidad en el mapa",
        "de": "Karten-Sichtbarkeit testen",
        "it": "Prova la visibilità sulla mappa",
        "pt": "Experimenta a visibilidade no mapa",
    },
    "mapboost_desc_silver": {
        "fr": "Pin surligné, portée moyenne",
        "en": "Highlighted pin, medium reach",
        "es": "Pin destacado, alcance medio",
        "de": "Hervorgehobener Pin, mittlere Reichweite",
        "it": "Pin evidenziato, copertura media",
        "pt": "Pin destacado, alcance médio",
    },
    "mapboost_desc_gold": {
        "fr": "Pin doré, top des résultats carte",
        "en": "Golden pin, top of map results",
        "es": "Pin dorado, top de resultados del mapa",
        "de": "Goldener Pin, top der Kartenergebnisse",
        "it": "Pin dorato, top dei risultati mappa",
        "pt": "Pin dourado, topo dos resultados do mapa",
    },
    "mapboost_desc_platinum": {
        "fr": "Pin doré + halo animé permanent",
        "en": "Golden pin + permanent animated halo",
        "es": "Pin dorado + halo animado permanente",
        "de": "Goldener Pin + permanenter animierter Halo",
        "it": "Pin dorato + alone animato permanente",
        "pt": "Pin dourado + halo animado permanente",
    },
    # Jour/Jours suffix
    "mapboost_days_count": {
        "fr": "@count jour(s)",
        "en": "@count day(s)",
        "es": "@count día(s)",
        "de": "@count Tag(e)",
        "it": "@count giorno/i",
        "pt": "@count dia(s)",
    },
    # Confirm dialog d'achat PawSpot
    "mapboost_confirm_title": {
        "fr": "Acheter PawSpot @tier ?",
        "en": "Buy PawSpot @tier?",
        "es": "¿Comprar PawSpot @tier?",
        "de": "PawSpot @tier kaufen?",
        "it": "Comprare PawSpot @tier?",
        "pt": "Comprar PawSpot @tier?",
    },
    "mapboost_confirm_tier_label": {
        "fr": "Tier",
        "en": "Tier",
        "es": "Nivel",
        "de": "Stufe",
        "it": "Livello",
        "pt": "Nível",
    },
    "mapboost_confirm_duration_label": {
        "fr": "Durée",
        "en": "Duration",
        "es": "Duración",
        "de": "Dauer",
        "it": "Durata",
        "pt": "Duração",
    },
    "mapboost_confirm_price_label": {
        "fr": "Prix",
        "en": "Price",
        "es": "Precio",
        "de": "Preis",
        "it": "Prezzo",
        "pt": "Preço",
    },
    "mapboost_confirm_description": {
        "fr": "Ton PawSpot sera mis en avant pendant la durée choisie.",
        "en": "Your PawSpot will be highlighted for the chosen duration.",
        "es": "Tu PawSpot estará destacado durante el tiempo elegido.",
        "de": "Dein PawSpot wird für die gewählte Dauer hervorgehoben.",
        "it": "Il tuo PawSpot sarà evidenziato per la durata scelta.",
        "pt": "O teu PawSpot será destacado durante a duração escolhida.",
    },
    # Common
    "common_confirm": {
        "fr": "Confirmer",
        "en": "Confirm",
        "es": "Confirmar",
        "de": "Bestätigen",
        "it": "Conferma",
        "pt": "Confirmar",
    },
    "common_service_unavailable": {
        "fr": "Service indisponible.",
        "en": "Service unavailable.",
        "es": "Servicio no disponible.",
        "de": "Dienst nicht verfügbar.",
        "it": "Servizio non disponibile.",
        "pt": "Serviço indisponível.",
    },
    # Snackbar PawSpot location updated
    "mapboost_location_updated": {
        "fr": "PawSpot mis à jour : @label",
        "en": "PawSpot updated: @label",
        "es": "PawSpot actualizado: @label",
        "de": "PawSpot aktualisiert: @label",
        "it": "PawSpot aggiornato: @label",
        "pt": "PawSpot atualizado: @label",
    },
    # Premium activation snackbar
    "premium_activated_title": {
        "fr": "Premium activé !",
        "en": "Premium activated!",
        "es": "¡Premium activado!",
        "de": "Premium aktiviert!",
        "it": "Premium attivato!",
        "pt": "Premium ativado!",
    },
    "premium_activated_msg": {
        "fr": "Profitez de toutes les fonctionnalités.",
        "en": "Enjoy all features.",
        "es": "Disfruta de todas las funcionalidades.",
        "de": "Genieße alle Funktionen.",
        "it": "Goditi tutte le funzionalità.",
        "pt": "Aproveita todas as funcionalidades.",
    },
    # Marker tooltips PawMap (infoWindow)
    "mapboost_marker_bronze": {
        "fr": "Visible (24h)",
        "en": "Visible (24h)",
        "es": "Visible (24h)",
        "de": "Sichtbar (24 Std.)",
        "it": "Visibile (24h)",
        "pt": "Visível (24h)",
    },
    "mapboost_marker_silver": {
        "fr": "Pin surligné (7j)",
        "en": "Highlighted pin (7d)",
        "es": "Pin destacado (7d)",
        "de": "Hervorgehobener Pin (7 T.)",
        "it": "Pin evidenziato (7g)",
        "pt": "Pin destacado (7d)",
    },
    "mapboost_marker_gold": {
        "fr": "Pin doré (15j)",
        "en": "Golden pin (15d)",
        "es": "Pin dorado (15d)",
        "de": "Goldener Pin (15 T.)",
        "it": "Pin dorato (15g)",
        "pt": "Pin dourado (15d)",
    },
    "mapboost_marker_platinum": {
        "fr": "Pin doré + halo (30j)",
        "en": "Golden pin + halo (30d)",
        "es": "Pin dorado + halo (30d)",
        "de": "Goldener Pin + Halo (30 T.)",
        "it": "Pin dorato + alone (30g)",
        "pt": "Pin dourado + halo (30d)",
    },
    "mapboost_marker_active": {
        "fr": "PawSpot actif",
        "en": "PawSpot active",
        "es": "PawSpot activo",
        "de": "PawSpot aktiv",
        "it": "PawSpot attivo",
        "pt": "PawSpot ativo",
    },
    "mapboost_marker_profile_boosted": {
        "fr": "Profil boosté",
        "en": "Boosted profile",
        "es": "Perfil destacado",
        "de": "Geboostetes Profil",
        "it": "Profilo in evidenza",
        "pt": "Perfil destacado",
    },
    # Long help text in shop
    "mapboost_info_visibility": {
        "fr": "Ton PawSpot est visible par les owners qui regardent la map à cet endroit. Passe en mode Propriétaire et ouvre la map pour le vérifier toi-même.",
        "en": "Your PawSpot is visible to owners looking at the map in this area. Switch to Owner mode and open the map to check it yourself.",
        "es": "Tu PawSpot es visible para los propietarios que miran el mapa en esta zona. Cambia al modo Propietario y abre el mapa para verificarlo tú mismo.",
        "de": "Dein PawSpot ist für Besitzer sichtbar, die die Karte an diesem Ort ansehen. Wechsle in den Besitzer-Modus und öffne die Karte, um es selbst zu überprüfen.",
        "it": "Il tuo PawSpot è visibile ai proprietari che guardano la mappa in questa zona. Passa alla modalità Proprietario e apri la mappa per verificarlo.",
        "pt": "O teu PawSpot é visível pelos proprietários que estão a ver o mapa nesta zona. Muda para o modo Proprietário e abre o mapa para verificares tu mesmo.",
    },
}


def dart_escape(s):
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")


def inject_into_lang_file(lang_code):
    path = LANG_DIR / f"{lang_code}.dart"
    text = path.read_text(encoding="utf-8")

    anchor = re.search(r"('pawmap_confirmations':\s*'[^']*',\s*\n)", text)
    if not anchor:
        # fallback : insert after map_report_label_other
        anchor = re.search(
            r"('map_report_label_other':\s*'[^']*',\s*\n)",
            text,
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
            print(f"  [WARN] {name}: substring not found -> {old[:80]!r}")
    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"  [{name}] applied {changes} substitutions")
    return changes


def main():
    print("== Inject PawSpot/MapBoost i18n keys ==")
    for lang in ["en", "fr", "es", "de", "it", "pt"]:
        inject_into_lang_file(lang)

    print()
    print("== Patch coin_shop_screen.dart ==")
    patch_source(
        "coin_shop",
        SOURCE_FILES["coin_shop"],
        [
            # _mapBoostTierDescription
            (
                "      case 'bronze':\n        return 'Testez la visibilité carte';\n      case 'silver':\n        return 'Pin surligné, portée moyenne';\n      case 'gold':\n        return 'Pin doré, top des résultats carte';\n      case 'platinum':\n      case 'diamond':\n        return 'Pin doré + halo animé permanent';",
                "      case 'bronze':\n        return 'mapboost_desc_bronze'.tr;\n      case 'silver':\n        return 'mapboost_desc_silver'.tr;\n      case 'gold':\n        return 'mapboost_desc_gold'.tr;\n      case 'platinum':\n      case 'diamond':\n        return 'mapboost_desc_platinum'.tr;",
            ),
            # day count badge
            (
                "'${pkg.days} jour${pkg.days > 1 ? \"s\" : \"\"}'",
                "'mapboost_days_count'.trParams({'count': pkg.days.toString()})",
            ),
            # daysLabel in dialog
            (
                "final daysLabel = pkg != null ? '${pkg.days} jours' : '?';",
                "final daysLabel = pkg != null ? 'mapboost_days_count'.trParams({'count': pkg.days.toString()}) : '?';",
            ),
            # Confirm dialog title
            (
                "title: Text('Acheter PawSpot ${tier.toUpperCase()} ?'),",
                "title: Text('mapboost_confirm_title'.trParams({'tier': tier.toUpperCase()})),",
            ),
            # Confirm dialog content
            (
                "content: Text(\n          'Tier : ${tier.toUpperCase()}\\n'\n          'Durée : $daysLabel\\n'\n          'Prix : $priceLabel\\n\\n'\n          'Ton PawSpot sera mis en avant pendant la durée choisie.',\n        ),",
                "content: Text(\n          '${'mapboost_confirm_tier_label'.tr} : ${tier.toUpperCase()}\\n'\n          '${'mapboost_confirm_duration_label'.tr} : $daysLabel\\n'\n          '${'mapboost_confirm_price_label'.tr} : $priceLabel\\n\\n'\n          '${'mapboost_confirm_description'.tr}',\n        ),",
            ),
            # Annuler / Confirmer buttons
            (
                "child: const Text('Annuler'),",
                "child: Text('common_cancel'.tr),",
            ),
            (
                "child: const Text('Confirmer'),",
                "child: Text('common_confirm'.tr),",
            ),
            # Premium activated snackbar
            (
                "title: 'Premium activé !',\n          message: 'Profitez de toutes les fonctionnalités.',",
                "title: 'premium_activated_title'.tr,\n          message: 'premium_activated_msg'.tr,",
            ),
            # Service indisponible
            (
                "msg = 'Service indisponible.';",
                "msg = 'common_service_unavailable'.tr;",
            ),
            # PawSpot location updated
            (
                "message: 'PawSpot mis à jour : $label',",
                "message: 'mapboost_location_updated'.trParams({'label': label}),",
            ),
            # Info visibility banner
            (
                "text:\n                                'Ton PawSpot est visible par les owners qui regardent la map à cet endroit. Passe en mode Propriétaire et ouvre la map pour le vérifier toi-même.',",
                "text: 'mapboost_info_visibility'.tr,",
            ),
        ],
    )

    print()
    print("== Patch paw_map_screen.dart ==")
    patch_source(
        "paw_map",
        SOURCE_FILES["paw_map"],
        [
            # tierLabel for InfoWindow
            (
                "final tierLabel = isMapBoosted\n            ? ({\n                'bronze': 'Visible (24h)',\n                'silver': 'Pin surligné (7j)',\n                'gold': 'Pin doré (15j)',\n                'platinum': 'Pin doré + halo (30j)',\n              }[mapTier] ?? 'PawSpot actif')\n            : (isBoosted ? 'Profil boosté' : '');",
                "final tierLabel = isMapBoosted\n            ? ({\n                'bronze': 'mapboost_marker_bronze'.tr,\n                'silver': 'mapboost_marker_silver'.tr,\n                'gold': 'mapboost_marker_gold'.tr,\n                'platinum': 'mapboost_marker_platinum'.tr,\n              }[mapTier] ?? 'mapboost_marker_active'.tr)\n            : (isBoosted ? 'mapboost_marker_profile_boosted'.tr : '');",
            ),
        ],
    )
    print()
    print("== DONE ==")


if __name__ == "__main__":
    main()
