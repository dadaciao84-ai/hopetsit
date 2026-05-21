"""
HopeTSIT v23.1.168 - Inject i18n keys for the screenshot bugs Daniel reported.

Adds:
  - coin_shop_chat_friends_title / _desc / _active  (PawFollow Chat entre amis)
  - coin_shop_pawspot_location_title / _change / _choose / _reset_tooltip
  - coin_shop_pawspot_summary_custom / _custom_coords / _fallback / _none / _loading
  - invoice_pdf_* (PDF labels for InvoicePdfGenerator)
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent
LANG_DIR = ROOT / "frontend" / "lib" / "localization" / "translations"

TRANSLATIONS = {
    # PawFollow Chat entre amis
    "coin_shop_chat_friends_title": {
        "fr": "Chat entre amis",
        "en": "Chat with friends",
        "es": "Chat entre amigos",
        "de": "Freunde-Chat",
        "it": "Chat tra amici",
        "pt": "Chat entre amigos",
    },
    "coin_shop_chat_friends_desc": {
        "fr": "Débloque le chat avec tes amis acceptés — 30 jours",
        "en": "Unlock chat with your accepted friends — 30 days",
        "es": "Desbloquea el chat con tus amigos aceptados — 30 días",
        "de": "Schalte den Chat mit deinen Freunden frei — 30 Tage",
        "it": "Sblocca la chat con i tuoi amici accettati — 30 giorni",
        "pt": "Desbloqueia o chat com os teus amigos aceites — 30 dias",
    },
    "coin_shop_chat_friends_active": {
        "fr": "Actif · renouvelle le chat entre amis",
        "en": "Active · renew chat with friends",
        "es": "Activo · renueva el chat entre amigos",
        "de": "Aktiv · Freunde-Chat verlängern",
        "it": "Attivo · rinnova la chat tra amici",
        "pt": "Ativo · renova o chat entre amigos",
    },

    # PawSpot location card
    "coin_shop_pawspot_location_title": {
        "fr": "Emplacement de ton PawSpot",
        "en": "Your PawSpot location",
        "es": "Ubicación de tu PawSpot",
        "de": "Standort deines PawSpots",
        "it": "Posizione del tuo PawSpot",
        "pt": "Localização do teu PawSpot",
    },
    "coin_shop_pawspot_change_btn": {
        "fr": "Changer",
        "en": "Change",
        "es": "Cambiar",
        "de": "Ändern",
        "it": "Cambia",
        "pt": "Alterar",
    },
    "coin_shop_pawspot_choose_btn": {
        "fr": "Choisir mon spot",
        "en": "Choose my spot",
        "es": "Elegir mi spot",
        "de": "Spot wählen",
        "it": "Scegli il mio spot",
        "pt": "Escolher o meu spot",
    },
    "coin_shop_pawspot_reset_tooltip": {
        "fr": "Revenir à mon adresse perso",
        "en": "Back to my home address",
        "es": "Volver a mi dirección personal",
        "de": "Zurück zu meiner Heimadresse",
        "it": "Torna al mio indirizzo personale",
        "pt": "Voltar à minha morada pessoal",
    },
    "coin_shop_pawspot_summary_custom": {
        "fr": "📍 PawSpot : @label",
        "en": "📍 PawSpot: @label",
        "es": "📍 PawSpot: @label",
        "de": "📍 PawSpot: @label",
        "it": "📍 PawSpot: @label",
        "pt": "📍 PawSpot: @label",
    },
    "coin_shop_pawspot_summary_custom_coords": {
        "fr": "📍 PawSpot personnalisé (@lat, @lng)",
        "en": "📍 Custom PawSpot (@lat, @lng)",
        "es": "📍 PawSpot personalizado (@lat, @lng)",
        "de": "📍 Eigener PawSpot (@lat, @lng)",
        "it": "📍 PawSpot personalizzato (@lat, @lng)",
        "pt": "📍 PawSpot personalizado (@lat, @lng)",
    },
    "coin_shop_pawspot_summary_fallback": {
        "fr": "⚠️ PawSpot utilise ton adresse perso. Choisis un emplacement spécifique pour mieux apparaître sur la carte.",
        "en": "⚠️ PawSpot is using your home address. Pick a specific location to stand out on the map.",
        "es": "⚠️ PawSpot usa tu dirección personal. Elige una ubicación específica para destacar en el mapa.",
        "de": "⚠️ PawSpot nutzt deine Heimadresse. Wähle einen spezifischen Standort, um auf der Karte besser sichtbar zu sein.",
        "it": "⚠️ PawSpot usa il tuo indirizzo personale. Scegli una posizione specifica per essere più visibile sulla mappa.",
        "pt": "⚠️ O PawSpot está a usar a tua morada pessoal. Escolhe um local específico para te destacares no mapa.",
    },
    "coin_shop_pawspot_summary_none": {
        "fr": "❌ Aucune position définie. Ton PawSpot est invisible sur la carte tant que tu ne choisis pas un emplacement.",
        "en": "❌ No location set. Your PawSpot stays invisible on the map until you pick a spot.",
        "es": "❌ No hay ubicación definida. Tu PawSpot está invisible en el mapa hasta que elijas un sitio.",
        "de": "❌ Kein Standort festgelegt. Dein PawSpot bleibt auf der Karte unsichtbar, bis du einen Ort wählst.",
        "it": "❌ Nessuna posizione impostata. Il tuo PawSpot resta invisibile sulla mappa finché non scegli un punto.",
        "pt": "❌ Nenhuma localização definida. O teu PawSpot fica invisível no mapa até escolheres um local.",
    },
    "coin_shop_pawspot_summary_loading": {
        "fr": "Position non chargée.",
        "en": "Location not loaded.",
        "es": "Ubicación no cargada.",
        "de": "Position nicht geladen.",
        "it": "Posizione non caricata.",
        "pt": "Localização não carregada.",
    },

    # Invoice PDF labels
    "invoice_pdf_label": {
        "fr": "FACTURE", "en": "INVOICE", "es": "FACTURA",
        "de": "RECHNUNG", "it": "FATTURA", "pt": "FATURA",
    },
    "invoice_pdf_issued": {
        "fr": "Émise le", "en": "Issued on", "es": "Emitida el",
        "de": "Ausgestellt am", "it": "Emessa il", "pt": "Emitida em",
    },
    "invoice_pdf_paid": {
        "fr": "Payée le", "en": "Paid on", "es": "Pagada el",
        "de": "Bezahlt am", "it": "Pagata il", "pt": "Paga em",
    },
    "invoice_pdf_refunded": {
        "fr": "Remboursée le", "en": "Refunded on", "es": "Reembolsada el",
        "de": "Erstattet am", "it": "Rimborsata il", "pt": "Reembolsada em",
    },
    "invoice_pdf_bill_to": {
        "fr": "FACTURÉ À", "en": "BILL TO", "es": "FACTURADO A",
        "de": "RECHNUNG AN", "it": "FATTURATO A", "pt": "FATURADO A",
    },
    "invoice_pdf_owner_role": {
        "fr": "Propriétaire", "en": "Owner", "es": "Propietario",
        "de": "Besitzer", "it": "Proprietario", "pt": "Proprietário",
    },
    "invoice_pdf_provider": {
        "fr": "PRESTATAIRE", "en": "SERVICE PROVIDER", "es": "PRESTADOR",
        "de": "DIENSTLEISTER", "it": "PRESTATORE", "pt": "PRESTADOR",
    },
    "invoice_pdf_desc": {
        "fr": "Description", "en": "Description", "es": "Descripción",
        "de": "Beschreibung", "it": "Descrizione", "pt": "Descrição",
    },
    "invoice_pdf_service_dates": {
        "fr": "Date(s) de service", "en": "Service date(s)", "es": "Fecha(s) del servicio",
        "de": "Servicedatum(en)", "it": "Data del servizio", "pt": "Data(s) do serviço",
    },
    "invoice_pdf_pets": {
        "fr": "Animal(aux)", "en": "Pet(s)", "es": "Mascota(s)",
        "de": "Tier(e)", "it": "Animale(i)", "pt": "Animal(ais)",
    },
    "invoice_pdf_status": {
        "fr": "Statut", "en": "Status", "es": "Estado",
        "de": "Status", "it": "Stato", "pt": "Estado",
    },
    "invoice_pdf_gross": {
        "fr": "Montant brut", "en": "Gross amount", "es": "Importe bruto",
        "de": "Bruttobetrag", "it": "Importo lordo", "pt": "Valor bruto",
    },
    "invoice_pdf_commission": {
        "fr": "Commission HoPetSit (20%)", "en": "HoPetSit fee (20%)", "es": "Comisión HoPetSit (20%)",
        "de": "HoPetSit Gebühr (20%)", "it": "Commissione HoPetSit (20%)", "pt": "Comissão HoPetSit (20%)",
    },
    "invoice_pdf_net_provider": {
        "fr": "Net au prestataire", "en": "Net to provider", "es": "Neto al prestador",
        "de": "Netto an Anbieter", "it": "Netto al prestatore", "pt": "Líquido para o prestador",
    },
    "invoice_pdf_total_paid": {
        "fr": "Total payé", "en": "Total paid", "es": "Total pagado",
        "de": "Gesamt bezahlt", "it": "Totale pagato", "pt": "Total pago",
    },
    "invoice_pdf_footer": {
        "fr": "Cette facture est générée automatiquement par HoPetSit. Toute question : contact@hopetsit.com",
        "en": "This invoice is generated automatically by HoPetSit. Questions: contact@hopetsit.com",
        "es": "Esta factura se genera automáticamente por HoPetSit. Consultas: contact@hopetsit.com",
        "de": "Diese Rechnung wird automatisch von HoPetSit erstellt. Fragen: contact@hopetsit.com",
        "it": "Questa fattura è generata automaticamente da HoPetSit. Domande: contact@hopetsit.com",
        "pt": "Esta fatura é gerada automaticamente pela HoPetSit. Questões: contact@hopetsit.com",
    },
    "invoice_pdf_service_walk": {
        "fr": "Promenade chien", "en": "Dog walk", "es": "Paseo de perros",
        "de": "Gassi gehen", "it": "Passeggiata cane", "pt": "Passeio de cão",
    },
    "invoice_pdf_service_daycare": {
        "fr": "Garderie", "en": "Day care", "es": "Guardería",
        "de": "Tagesbetreuung", "it": "Asilo", "pt": "Creche",
    },
    "invoice_pdf_service_boarding": {
        "fr": "Garde nuit", "en": "Overnight boarding", "es": "Hospedaje nocturno",
        "de": "Übernachtungspflege", "it": "Pensione notturna", "pt": "Hospedagem noturna",
    },
    "invoice_pdf_service_sitting": {
        "fr": "Pet-sitting", "en": "Pet-sitting", "es": "Pet-sitting",
        "de": "Pet-Sitting", "it": "Pet-sitting", "pt": "Pet-sitting",
    },
    "invoice_pdf_service_generic": {
        "fr": "Service", "en": "Service", "es": "Servicio",
        "de": "Service", "it": "Servizio", "pt": "Serviço",
    },
    "invoice_pdf_subject": {
        "fr": "Facture HoPetSit",
        "en": "HoPetSit invoice",
        "es": "Factura HoPetSit",
        "de": "HoPetSit Rechnung",
        "it": "Fattura HoPetSit",
        "pt": "Fatura HoPetSit",
    },
}


def dart_escape(s):
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")


def inject(lang):
    path = LANG_DIR / f"{lang}.dart"
    text = path.read_text(encoding="utf-8")
    # Use the existing 'invoice_viewer_title' key as anchor, fallback to onboarding_or
    anchor = re.search(r"('onboarding_or':\s*'[^']*',\s*\n)", text)
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
        print(f"  [{lang}] all {skipped} keys already present")
        return 0
    insert_at = anchor.end()
    new_text = text[:insert_at] + "\n".join(new_entries) + "\n" + text[insert_at:]
    path.write_text(new_text, encoding="utf-8")
    print(f"  [{lang}] +{len(new_entries)} keys (skipped {skipped})")
    return len(new_entries)


def main():
    print("== Inject v23.1.168 i18n keys ==")
    for lang in ["en", "fr", "es", "de", "it", "pt"]:
        inject(lang)
    print("== DONE ==")


if __name__ == "__main__":
    main()
