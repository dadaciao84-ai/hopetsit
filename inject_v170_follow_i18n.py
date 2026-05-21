"""HopeTSIT v23.1.170 - Inject follow_* + live_tracking_* i18n keys (6 langs)."""

import re
from pathlib import Path

ROOT = Path(__file__).parent
LANG_DIR = ROOT / "frontend" / "lib" / "localization" / "translations"

TRANSLATIONS = {
    # Bouton owner - Suivre walker / Suivre sitter
    "follow_button_walker": {
        "fr": "Suivre walker", "en": "Follow walker", "es": "Seguir paseador",
        "de": "Walker folgen", "it": "Segui dog-walker", "pt": "Seguir walker",
    },
    "follow_button_sitter": {
        "fr": "Suivre sitter", "en": "Follow sitter", "es": "Seguir cuidador",
        "de": "Sitter folgen", "it": "Segui sitter", "pt": "Seguir sitter",
    },
    "follow_button_generic": {
        "fr": "Suivre", "en": "Follow", "es": "Seguir",
        "de": "Folgen", "it": "Segui", "pt": "Seguir",
    },
    # Bouton sitter/walker - Suis-moi
    "follow_me_button": {
        "fr": "Suis-moi", "en": "Follow me", "es": "Sígueme",
        "de": "Folge mir", "it": "Seguimi", "pt": "Segue-me",
    },
    # Snackbar : aucun booking en cours
    "follow_no_booking_title": {
        "fr": "Pas de réservation à suivre",
        "en": "No booking to track",
        "es": "Sin reserva que seguir",
        "de": "Keine Buchung zum Verfolgen",
        "it": "Nessuna prenotazione da seguire",
        "pt": "Nenhuma reserva para seguir",
    },
    "follow_no_booking_msg": {
        "fr": "Aucune réservation payée en cours avec @name. Le suivi en direct s\\'active après paiement.",
        "en": "No paid booking in progress with @name. Live tracking activates after payment.",
        "es": "No hay reserva pagada en curso con @name. El seguimiento se activa tras el pago.",
        "de": "Keine bezahlte Buchung in Bearbeitung mit @name. Live-Tracking startet nach Zahlung.",
        "it": "Nessuna prenotazione pagata in corso con @name. Il tracking parte dopo il pagamento.",
        "pt": "Nenhuma reserva paga em curso com @name. O rastreamento ativa-se após o pagamento.",
    },
    # Snackbar : PawFollow requis
    "follow_pawfollow_required_title": {
        "fr": "PawFollow requis",
        "en": "PawFollow required",
        "es": "PawFollow necesario",
        "de": "PawFollow erforderlich",
        "it": "PawFollow richiesto",
        "pt": "PawFollow necessário",
    },
    "follow_pawfollow_required_msg": {
        "fr": "Active PawFollow pour suivre ton walker ou sitter en direct.",
        "en": "Activate PawFollow to track your walker or sitter live.",
        "es": "Activa PawFollow para seguir a tu paseador o cuidador en directo.",
        "de": "Aktiviere PawFollow, um deinen Walker oder Sitter live zu verfolgen.",
        "it": "Attiva PawFollow per seguire il tuo walker o sitter in diretta.",
        "pt": "Ativa PawFollow para seguir o teu walker ou sitter ao vivo.",
    },
    # Snackbar : position pas encore partagée
    "follow_no_position_title": {
        "fr": "Position pas encore partagée",
        "en": "Position not yet shared",
        "es": "Ubicación aún no compartida",
        "de": "Position noch nicht geteilt",
        "it": "Posizione non ancora condivisa",
        "pt": "Localização ainda não partilhada",
    },
    "follow_no_position_msg": {
        "fr": "Le prestataire n\\'a pas encore activé son partage de position.",
        "en": "The provider hasn\\'t yet enabled location sharing.",
        "es": "El prestador aún no ha activado el compartir ubicación.",
        "de": "Der Dienstleister hat die Standortfreigabe noch nicht aktiviert.",
        "it": "Il prestatore non ha ancora attivato la condivisione della posizione.",
        "pt": "O prestador ainda não ativou a partilha de localização.",
    },
    # Snackbar : erreur générique suivi indispo
    "follow_unavailable_title": {
        "fr": "Suivi indisponible",
        "en": "Tracking unavailable",
        "es": "Seguimiento no disponible",
        "de": "Tracking nicht verfügbar",
        "it": "Tracciamento non disponibile",
        "pt": "Rastreamento indisponível",
    },
    # Snackbar : demande "Suis-moi" envoyée
    "follow_request_sent_title": {
        "fr": "Demande envoyée",
        "en": "Request sent",
        "es": "Solicitud enviada",
        "de": "Anfrage gesendet",
        "it": "Richiesta inviata",
        "pt": "Pedido enviado",
    },
    "follow_request_sent_msg": {
        "fr": "Le propriétaire a été notifié et peut maintenant te suivre en direct.",
        "en": "The owner has been notified and can now follow you live.",
        "es": "El propietario ha sido notificado y ahora puede seguirte en directo.",
        "de": "Der Besitzer wurde benachrichtigt und kann dir jetzt live folgen.",
        "it": "Il proprietario è stato notificato e può ora seguirti in diretta.",
        "pt": "O proprietário foi notificado e pode agora seguir-te ao vivo.",
    },
    # Push notif côté owner
    "live_tracking_request_title": {
        "fr": "Demande de suivi en direct",
        "en": "Live tracking request",
        "es": "Solicitud de seguimiento",
        "de": "Live-Tracking-Anfrage",
        "it": "Richiesta di tracciamento",
        "pt": "Pedido de rastreamento",
    },
    "live_tracking_request_body": {
        "fr": "Ton walker / sitter t\\'invite à suivre sa position en direct.",
        "en": "Your walker / sitter is inviting you to track their location live.",
        "es": "Tu paseador / cuidador te invita a seguir su ubicación en directo.",
        "de": "Dein Walker / Sitter lädt dich ein, seinen Standort live zu verfolgen.",
        "it": "Il tuo walker / sitter ti invita a seguire la sua posizione in diretta.",
        "pt": "O teu walker / sitter convida-te a seguir a sua localização ao vivo.",
    },
}


def dart_escape(s):
    return s.replace("\\\\", "\\\\\\\\").replace("'", "\\'")


def inject(lang):
    path = LANG_DIR / f"{lang}.dart"
    text = path.read_text(encoding="utf-8")
    # Anchor : juste après common_close (présent partout)
    anchor = re.search(r"('common_close':\s*'[^']*',\s*\n)", text)
    if not anchor:
        # fallback : juste avant la fermeture du Map
        anchor = re.search(r"(\}\s*;\s*\n\s*\}\s*\}\s*$)", text)
        if not anchor:
            print(f"  [SKIP] {lang}: anchor not found")
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
    insert_at = anchor.end()
    new_text = text[:insert_at] + "\n".join(new_entries) + "\n" + text[insert_at:]
    path.write_text(new_text, encoding="utf-8")
    print(f"  [{lang}] +{len(new_entries)} keys (skipped {skipped})")
    return len(new_entries)


def main():
    print("== Inject v23.1.170 follow_* + live_tracking_* keys ==")
    for lang in ["en", "fr", "es", "de", "it", "pt"]:
        inject(lang)
    print("== DONE ==")


if __name__ == "__main__":
    main()
