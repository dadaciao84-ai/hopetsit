"""
HopeTSIT v23.1.162 - Inject i18n keys for hardcoded FR strings found in
Daniel's screenshots (banner Paiement recu, bottom sheet, facture title,
live walk screen).
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent
LANG_DIR = ROOT / "frontend" / "lib" / "localization" / "translations"

TRANSLATIONS = {
    # Banner "Paiement reçu !" (home_quick_action_bar line 380)
    "payment_received_banner_title": {
        "fr": "Paiement reçu !",
        "en": "Payment received!",
        "es": "¡Pago recibido!",
        "de": "Zahlung erhalten!",
        "it": "Pagamento ricevuto!",
        "pt": "Pagamento recebido!",
    },
    "payment_received_banner_title_extra": {
        "fr": "Paiement reçu ! (+@count autre(s))",
        "en": "Payment received! (+@count more)",
        "es": "¡Pago recibido! (+@count más)",
        "de": "Zahlung erhalten! (+@count weitere)",
        "it": "Pagamento ricevuto! (+@count altri)",
        "pt": "Pagamento recebido! (+@count mais)",
    },
    "payment_received_subtitle": {
        "fr": "@name a payé @amount",
        "en": "@name paid @amount",
        "es": "@name pagó @amount",
        "de": "@name hat @amount bezahlt",
        "it": "@name ha pagato @amount",
        "pt": "@name pagou @amount",
    },
    # Bottom sheet button "Voir mes factures"
    "view_my_invoices_button": {
        "fr": "Voir mes factures",
        "en": "View my invoices",
        "es": "Ver mis facturas",
        "de": "Meine Rechnungen ansehen",
        "it": "Vedi le mie fatture",
        "pt": "Ver as minhas faturas",
    },
    # Banner "Voir détails" CTA
    "view_details_cta": {
        "fr": "Voir détails",
        "en": "View details",
        "es": "Ver detalles",
        "de": "Details ansehen",
        "it": "Vedi dettagli",
        "pt": "Ver detalhes",
    },
    # Invoice viewer AppBar title
    "invoice_viewer_title": {
        "fr": "Facture HoPetSit",
        "en": "HoPetSit Invoice",
        "es": "Factura HoPetSit",
        "de": "HoPetSit Rechnung",
        "it": "Fattura HoPetSit",
        "pt": "Fatura HoPetSit",
    },
    # LiveWalkMapScreen - clés totalement manquantes
    "live_walk_title": {
        "fr": "Balade en direct",
        "en": "Live walk",
        "es": "Paseo en directo",
        "de": "Live-Spaziergang",
        "it": "Passeggiata in diretta",
        "pt": "Passeio em direto",
    },
    "live_walk_no_active": {
        "fr": "Aucune balade en cours",
        "en": "No active walk",
        "es": "Sin paseo activo",
        "de": "Kein aktiver Spaziergang",
        "it": "Nessuna passeggiata attiva",
        "pt": "Sem passeio ativo",
    },
    "live_walk_loading": {
        "fr": "Recherche de la position...",
        "en": "Searching position...",
        "es": "Buscando posición...",
        "de": "Position wird gesucht...",
        "it": "Ricerca posizione...",
        "pt": "A procurar posição...",
    },
    "live_walk_error": {
        "fr": "Impossible de récupérer la balade",
        "en": "Could not load walk",
        "es": "No se pudo cargar el paseo",
        "de": "Spaziergang konnte nicht geladen werden",
        "it": "Impossibile caricare la passeggiata",
        "pt": "Não foi possível carregar o passeio",
    },
}


def dart_escape(s):
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")


def inject(lang):
    path = LANG_DIR / f"{lang}.dart"
    text = path.read_text(encoding="utf-8")
    anchor = (
        re.search(r"('cancel_72h_dialog_confirm':\s*'[^']*',\s*\n)", text)
        or re.search(r"('cancel_72h_button':\s*'[^']*',\s*\n)", text)
        or re.search(r"('invoice_download_preparing_msg':\s*'[^']*',\s*\n)", text)
    )
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
    print("== Inject v162 i18n keys ==")
    for lang in ["en", "fr", "es", "de", "it", "pt"]:
        inject(lang)
    print("== DONE ==")


if __name__ == "__main__":
    main()
