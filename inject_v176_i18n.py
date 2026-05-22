"""HopeTSIT v23.1.176 - Inject i18n keys for pawfollow_request chat card."""

import re
from pathlib import Path

ROOT = Path(__file__).parent
LANG_DIR = ROOT / "frontend" / "lib" / "localization" / "translations"

TRANSLATIONS = {
    # En-têtes selon le sens
    "pawfollow_request_sent_header": {
        "fr": "Demande de suivi en direct envoyée",
        "en": "Live tracking request sent",
        "es": "Solicitud de seguimiento enviada",
        "de": "Live-Tracking-Anfrage gesendet",
        "it": "Richiesta di tracciamento inviata",
        "pt": "Pedido de rastreamento enviado",
    },
    "pawfollow_request_owner_wants_to_follow": {
        "fr": "Le propriétaire souhaite suivre ta position en direct",
        "en": "The owner wants to track your position live",
        "es": "El propietario quiere seguir tu posición en vivo",
        "de": "Der Besitzer möchte deinen Standort live verfolgen",
        "it": "Il proprietario vuole seguire la tua posizione in diretta",
        "pt": "O proprietário quer seguir a tua posição ao vivo",
    },
    "pawfollow_request_provider_wants_to_share": {
        "fr": "Le walker / sitter veut partager sa position avec toi",
        "en": "The walker / sitter wants to share their position with you",
        "es": "El paseador / cuidador quiere compartir su posición contigo",
        "de": "Der Walker / Sitter möchte seinen Standort mit dir teilen",
        "it": "Il walker / sitter vuole condividere la sua posizione con te",
        "pt": "O walker / sitter quer partilhar a sua posição contigo",
    },
    "pawfollow_request_generic": {
        "fr": "Demande de suivi en direct",
        "en": "Live tracking request",
        "es": "Solicitud de seguimiento en vivo",
        "de": "Live-Tracking-Anfrage",
        "it": "Richiesta di tracciamento in diretta",
        "pt": "Pedido de rastreamento ao vivo",
    },
    # Statut
    "pawfollow_status_pending": {
        "fr": "En attente", "en": "Pending", "es": "Pendiente",
        "de": "Ausstehend", "it": "In attesa", "pt": "Pendente",
    },
    "pawfollow_status_accepted": {
        "fr": "Accepté", "en": "Accepted", "es": "Aceptado",
        "de": "Angenommen", "it": "Accettato", "pt": "Aceite",
    },
    "pawfollow_status_refused": {
        "fr": "Refusé", "en": "Refused", "es": "Rechazado",
        "de": "Abgelehnt", "it": "Rifiutato", "pt": "Recusado",
    },
    # Boutons
    "pawfollow_accept": {
        "fr": "Accepter", "en": "Accept", "es": "Aceptar",
        "de": "Annehmen", "it": "Accetta", "pt": "Aceitar",
    },
    "pawfollow_refuse": {
        "fr": "Refuser", "en": "Refuse", "es": "Rechazar",
        "de": "Ablehnen", "it": "Rifiuta", "pt": "Recusar",
    },
    # Snackbars
    "pawfollow_request_sent_title": {
        "fr": "Demande envoyée",
        "en": "Request sent",
        "es": "Solicitud enviada",
        "de": "Anfrage gesendet",
        "it": "Richiesta inviata",
        "pt": "Pedido enviado",
    },
    "pawfollow_request_sent_msg": {
        "fr": "Une carte avec Accepter / Refuser vient d\\'apparaître dans le chat.",
        "en": "An Accept / Refuse card now appears in the chat.",
        "es": "Aparece ahora una tarjeta Aceptar / Rechazar en el chat.",
        "de": "Eine Annehmen / Ablehnen Karte erscheint jetzt im Chat.",
        "it": "Ora compare una scheda Accetta / Rifiuta nella chat.",
        "pt": "Aparece agora um cartão Aceitar / Recusar no chat.",
    },
    "pawfollow_accepted_title": {
        "fr": "Demande acceptée",
        "en": "Request accepted",
        "es": "Solicitud aceptada",
        "de": "Anfrage angenommen",
        "it": "Richiesta accettata",
        "pt": "Pedido aceite",
    },
    "pawfollow_accepted_msg": {
        "fr": "Le suivi en direct est désormais actif.",
        "en": "Live tracking is now active.",
        "es": "El seguimiento en vivo está ahora activo.",
        "de": "Live-Tracking ist jetzt aktiv.",
        "it": "Il tracciamento in diretta è ora attivo.",
        "pt": "O rastreamento ao vivo está agora ativo.",
    },
    "pawfollow_refused_title": {
        "fr": "Demande refusée",
        "en": "Request refused",
        "es": "Solicitud rechazada",
        "de": "Anfrage abgelehnt",
        "it": "Richiesta rifiutata",
        "pt": "Pedido recusado",
    },
    "pawfollow_refused_msg": {
        "fr": "La personne ne souhaite pas activer le suivi en direct.",
        "en": "The person does not want to enable live tracking.",
        "es": "La persona no quiere activar el seguimiento en vivo.",
        "de": "Die Person möchte das Live-Tracking nicht aktivieren.",
        "it": "La persona non vuole attivare il tracciamento in diretta.",
        "pt": "A pessoa não quer ativar o rastreamento ao vivo.",
    },
}


def inject(lang):
    path = LANG_DIR / f"{lang}.dart"
    text = path.read_text(encoding="utf-8")
    anchor = re.search(r"('common_close':\s*'[^']*',\s*\n)", text)
    if not anchor:
        return 0
    new_entries = []
    skipped = 0
    for key, langs in TRANSLATIONS.items():
        if f"'{key}'" in text:
            skipped += 1
            continue
        new_entries.append(f"      '{key}': '{langs[lang]}',")
    if not new_entries:
        print(f"  [{lang}] all {skipped} keys already present")
        return 0
    new_text = text[:anchor.end()] + "\n".join(new_entries) + "\n" + text[anchor.end():]
    path.write_text(new_text, encoding="utf-8")
    print(f"  [{lang}] +{len(new_entries)} keys (skipped {skipped})")
    return len(new_entries)


for lang in ["en", "fr", "es", "de", "it", "pt"]:
    inject(lang)
print("DONE")
