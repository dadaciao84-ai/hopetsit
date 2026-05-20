"""
HopeTSIT v23.1.161 - Inject 72h cancel button i18n keys.
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent
LANG_DIR = ROOT / "frontend" / "lib" / "localization" / "translations"

TRANSLATIONS = {
    "cancel_72h_button": {
        "fr": "Annuler (72h)",
        "en": "Cancel (72h)",
        "es": "Cancelar (72h)",
        "de": "Stornieren (72 Std.)",
        "it": "Annulla (72h)",
        "pt": "Cancelar (72h)",
    },
    "cancel_72h_dialog_title": {
        "fr": "Annuler la réservation ?",
        "en": "Cancel booking?",
        "es": "¿Cancelar reserva?",
        "de": "Buchung stornieren?",
        "it": "Annullare la prenotazione?",
        "pt": "Cancelar a reserva?",
    },
    "cancel_72h_dialog_message": {
        "fr": "Tu peux annuler gratuitement car le service est dans plus de 72h. L'owner sera intégralement remboursé.",
        "en": "You can cancel for free because the service is more than 72h away. The owner will be fully refunded.",
        "es": "Puedes cancelar gratis porque el servicio es a más de 72h. El propietario recibirá un reembolso íntegro.",
        "de": "Du kannst kostenlos stornieren, da der Service in mehr als 72 Std. stattfindet. Der Besitzer wird vollständig erstattet.",
        "it": "Puoi annullare gratuitamente perché il servizio è a più di 72h. Il proprietario sarà rimborsato integralmente.",
        "pt": "Podes cancelar gratuitamente porque o serviço é em mais de 72h. O proprietário receberá um reembolso integral.",
    },
    "cancel_72h_dialog_confirm": {
        "fr": "Annuler la réservation",
        "en": "Cancel booking",
        "es": "Cancelar reserva",
        "de": "Buchung stornieren",
        "it": "Annulla prenotazione",
        "pt": "Cancelar reserva",
    },
    "cancel_72h_success": {
        "fr": "Réservation annulée. Remboursement en cours.",
        "en": "Booking cancelled. Refund in progress.",
        "es": "Reserva cancelada. Reembolso en curso.",
        "de": "Buchung storniert. Rückerstattung in Bearbeitung.",
        "it": "Prenotazione annullata. Rimborso in corso.",
        "pt": "Reserva cancelada. Reembolso em curso.",
    },
    "cancel_72h_error": {
        "fr": "Impossible d'annuler. Réessaie ou contacte le support.",
        "en": "Could not cancel. Try again or contact support.",
        "es": "No se pudo cancelar. Inténtalo de nuevo o contacta con soporte.",
        "de": "Stornierung fehlgeschlagen. Versuche es erneut oder kontaktiere den Support.",
        "it": "Impossibile annullare. Riprova o contatta il supporto.",
        "pt": "Não foi possível cancelar. Tenta novamente ou contacta o suporte.",
    },
}


def dart_escape(s):
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")


def inject(lang):
    path = LANG_DIR / f"{lang}.dart"
    text = path.read_text(encoding="utf-8")
    # Pick the last reliable anchor we've added in previous sessions
    anchor = (
        re.search(r"('invoice_download_preparing_msg':\s*'[^']*',\s*\n)", text)
        or re.search(r"('pawfollow_per_day_suffix':\s*'[^']*',\s*\n)", text)
        or re.search(r"('walker_rate_hint_30':\s*'[^']*',\s*\n)", text)
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
    print("== Inject cancel_72h i18n keys ==")
    for lang in ["en", "fr", "es", "de", "it", "pt"]:
        inject(lang)
    print("== DONE ==")


if __name__ == "__main__":
    main()
