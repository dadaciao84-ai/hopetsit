"""
HopeTSIT v23.1.160 - Inject cancellation notification templates.

Daniel : "car owner walker au sitter peuvent annuler jusqua 72h avant c les
regles du paiement". On notifie les 2 parties quand quelqu'un annule un
booking paye (avec refund). 2 nouveaux types : booking_cancelled_by_owner
(provider notif) + booking_cancelled_by_provider (owner notif), en 6 langues.
"""

import json
from pathlib import Path

LOCALES_DIR = Path(__file__).parent / "backend" / "src" / "locales"

# CTA color for cancellation: red (signals action / loss)
RED = "#DC2626"

TEMPLATES = {
    "fr": {
        "booking_cancelled_by_owner": {
            "title": "Réservation annulée",
            "body": "Le propriétaire vient d'annuler la réservation (>72h avant le service). Aucune action requise.",
            "emailSubject": "Réservation annulée — HoPetSit",
            "emailBody": "<p>Bonjour,</p><p>Le propriétaire vient d'annuler une réservation à plus de 72h du service. <strong>Vous ne serez pas payé pour cette mission</strong>, mais aucune pénalité ne s'applique de votre côté.</p><p><a href=\"{{emailLink}}\" style=\"display:inline-block;padding:12px 24px;background:%s;color:#FFFFFF;text-decoration:none;border-radius:8px;font-weight:700;font-family:sans-serif;\">Voir la réservation</a></p><p style=\"color:#666;font-size:12px;\">Si le bouton ne fonctionne pas, copiez-collez ce lien dans votre navigateur : {{emailLink}}</p>" % RED,
        },
        "booking_cancelled_by_provider": {
            "title": "Prestation annulée par le prestataire",
            "body": "Le prestataire vient d'annuler la réservation. Vous serez intégralement remboursé sous 5-10 jours.",
            "emailSubject": "Votre réservation a été annulée — HoPetSit",
            "emailBody": "<p>Bonjour,</p><p>Le prestataire vient d'annuler votre réservation à plus de 72h du service. <strong>Un remboursement intégral est en cours</strong> (5-10 jours selon votre banque). Vous pouvez rebooker un autre prestataire sur l'app.</p><p><a href=\"{{emailLink}}\" style=\"display:inline-block;padding:12px 24px;background:#EF4324;color:#FFFFFF;text-decoration:none;border-radius:8px;font-weight:700;font-family:sans-serif;\">Trouver un autre prestataire</a></p><p style=\"color:#666;font-size:12px;\">Si le bouton ne fonctionne pas, copiez-collez ce lien dans votre navigateur : {{emailLink}}</p>",
        },
    },
    "en": {
        "booking_cancelled_by_owner": {
            "title": "Booking cancelled",
            "body": "The owner just cancelled the booking (>72h before service). No action needed on your side.",
            "emailSubject": "Booking cancelled — HoPetSit",
            "emailBody": "<p>Hi,</p><p>The owner just cancelled a booking more than 72h before service. <strong>You will not be paid for this mission</strong>, but no penalty applies on your side.</p><p><a href=\"{{emailLink}}\" style=\"display:inline-block;padding:12px 24px;background:%s;color:#FFFFFF;text-decoration:none;border-radius:8px;font-weight:700;font-family:sans-serif;\">View booking</a></p><p style=\"color:#666;font-size:12px;\">If the button doesn't work, copy this link into your browser: {{emailLink}}</p>" % RED,
        },
        "booking_cancelled_by_provider": {
            "title": "Service cancelled by provider",
            "body": "The provider just cancelled the booking. You will be fully refunded within 5-10 days.",
            "emailSubject": "Your booking has been cancelled — HoPetSit",
            "emailBody": "<p>Hi,</p><p>The provider just cancelled your booking more than 72h before service. <strong>A full refund is in progress</strong> (5-10 days depending on your bank). You can book another provider on the app.</p><p><a href=\"{{emailLink}}\" style=\"display:inline-block;padding:12px 24px;background:#EF4324;color:#FFFFFF;text-decoration:none;border-radius:8px;font-weight:700;font-family:sans-serif;\">Find another provider</a></p><p style=\"color:#666;font-size:12px;\">If the button doesn't work, copy this link into your browser: {{emailLink}}</p>",
        },
    },
    "es": {
        "booking_cancelled_by_owner": {
            "title": "Reserva cancelada",
            "body": "El propietario acaba de cancelar la reserva (>72h antes del servicio). No se requiere acción.",
            "emailSubject": "Reserva cancelada — HoPetSit",
            "emailBody": "<p>Hola,</p><p>El propietario acaba de cancelar una reserva con más de 72h de antelación. <strong>No recibirás pago por esta misión</strong>, pero no se aplica ninguna penalización.</p><p><a href=\"{{emailLink}}\" style=\"display:inline-block;padding:12px 24px;background:%s;color:#FFFFFF;text-decoration:none;border-radius:8px;font-weight:700;font-family:sans-serif;\">Ver reserva</a></p><p style=\"color:#666;font-size:12px;\">Si el botón no funciona, copia este enlace en tu navegador: {{emailLink}}</p>" % RED,
        },
        "booking_cancelled_by_provider": {
            "title": "Servicio cancelado por el prestador",
            "body": "El prestador acaba de cancelar la reserva. Recibirás un reembolso íntegro en 5-10 días.",
            "emailSubject": "Tu reserva ha sido cancelada — HoPetSit",
            "emailBody": "<p>Hola,</p><p>El prestador acaba de cancelar tu reserva con más de 72h de antelación. <strong>Se está procesando un reembolso íntegro</strong> (5-10 días según tu banco). Puedes reservar a otro prestador en la app.</p><p><a href=\"{{emailLink}}\" style=\"display:inline-block;padding:12px 24px;background:#EF4324;color:#FFFFFF;text-decoration:none;border-radius:8px;font-weight:700;font-family:sans-serif;\">Buscar otro prestador</a></p><p style=\"color:#666;font-size:12px;\">Si el botón no funciona, copia este enlace en tu navegador: {{emailLink}}</p>",
        },
    },
    "de": {
        "booking_cancelled_by_owner": {
            "title": "Buchung storniert",
            "body": "Der Besitzer hat die Buchung gerade storniert (>72 Std. vor Service). Keine Aktion erforderlich.",
            "emailSubject": "Buchung storniert — HoPetSit",
            "emailBody": "<p>Hallo,</p><p>Der Besitzer hat eine Buchung mehr als 72 Std. vor dem Service storniert. <strong>Du erhältst keine Bezahlung für diesen Auftrag</strong>, aber es entstehen dir keine Nachteile.</p><p><a href=\"{{emailLink}}\" style=\"display:inline-block;padding:12px 24px;background:%s;color:#FFFFFF;text-decoration:none;border-radius:8px;font-weight:700;font-family:sans-serif;\">Buchung ansehen</a></p><p style=\"color:#666;font-size:12px;\">Wenn der Button nicht funktioniert, kopiere diesen Link in deinen Browser: {{emailLink}}</p>" % RED,
        },
        "booking_cancelled_by_provider": {
            "title": "Dienst vom Anbieter storniert",
            "body": "Der Anbieter hat die Buchung gerade storniert. Du erhältst eine vollständige Rückerstattung innerhalb von 5-10 Tagen.",
            "emailSubject": "Deine Buchung wurde storniert — HoPetSit",
            "emailBody": "<p>Hallo,</p><p>Der Anbieter hat deine Buchung mehr als 72 Std. vor dem Service storniert. <strong>Eine vollständige Rückerstattung wird bearbeitet</strong> (5-10 Tage je nach Bank). Du kannst einen anderen Anbieter in der App buchen.</p><p><a href=\"{{emailLink}}\" style=\"display:inline-block;padding:12px 24px;background:#EF4324;color:#FFFFFF;text-decoration:none;border-radius:8px;font-weight:700;font-family:sans-serif;\">Anderen Anbieter finden</a></p><p style=\"color:#666;font-size:12px;\">Wenn der Button nicht funktioniert, kopiere diesen Link in deinen Browser: {{emailLink}}</p>",
        },
    },
    "it": {
        "booking_cancelled_by_owner": {
            "title": "Prenotazione annullata",
            "body": "Il proprietario ha appena annullato la prenotazione (>72h prima del servizio). Nessuna azione richiesta.",
            "emailSubject": "Prenotazione annullata — HoPetSit",
            "emailBody": "<p>Ciao,</p><p>Il proprietario ha annullato una prenotazione con più di 72h di anticipo. <strong>Non riceverai il pagamento per questo lavoro</strong>, ma non ci sono penalità per te.</p><p><a href=\"{{emailLink}}\" style=\"display:inline-block;padding:12px 24px;background:%s;color:#FFFFFF;text-decoration:none;border-radius:8px;font-weight:700;font-family:sans-serif;\">Vedi prenotazione</a></p><p style=\"color:#666;font-size:12px;\">Se il pulsante non funziona, copia questo link nel tuo browser: {{emailLink}}</p>" % RED,
        },
        "booking_cancelled_by_provider": {
            "title": "Servizio annullato dal prestatore",
            "body": "Il prestatore ha appena annullato la prenotazione. Riceverai un rimborso completo entro 5-10 giorni.",
            "emailSubject": "La tua prenotazione è stata annullata — HoPetSit",
            "emailBody": "<p>Ciao,</p><p>Il prestatore ha annullato la tua prenotazione con più di 72h di anticipo. <strong>È in corso un rimborso completo</strong> (5-10 giorni a seconda della banca). Puoi prenotare un altro prestatore nell'app.</p><p><a href=\"{{emailLink}}\" style=\"display:inline-block;padding:12px 24px;background:#EF4324;color:#FFFFFF;text-decoration:none;border-radius:8px;font-weight:700;font-family:sans-serif;\">Trova un altro prestatore</a></p><p style=\"color:#666;font-size:12px;\">Se il pulsante non funziona, copia questo link nel tuo browser: {{emailLink}}</p>",
        },
    },
    "pt": {
        "booking_cancelled_by_owner": {
            "title": "Reserva cancelada",
            "body": "O proprietário acabou de cancelar a reserva (>72h antes do serviço). Nenhuma ação necessária.",
            "emailSubject": "Reserva cancelada — HoPetSit",
            "emailBody": "<p>Olá,</p><p>O proprietário acabou de cancelar uma reserva com mais de 72h de antecedência. <strong>Não receberás pagamento por este trabalho</strong>, mas não há penalidade para ti.</p><p><a href=\"{{emailLink}}\" style=\"display:inline-block;padding:12px 24px;background:%s;color:#FFFFFF;text-decoration:none;border-radius:8px;font-weight:700;font-family:sans-serif;\">Ver reserva</a></p><p style=\"color:#666;font-size:12px;\">Se o botão não funcionar, copia este link no teu navegador: {{emailLink}}</p>" % RED,
        },
        "booking_cancelled_by_provider": {
            "title": "Serviço cancelado pelo prestador",
            "body": "O prestador acabou de cancelar a reserva. Receberás um reembolso integral em 5-10 dias.",
            "emailSubject": "A tua reserva foi cancelada — HoPetSit",
            "emailBody": "<p>Olá,</p><p>O prestador acabou de cancelar a tua reserva com mais de 72h de antecedência. <strong>Está em curso um reembolso integral</strong> (5-10 dias dependendo do banco). Podes reservar outro prestador na app.</p><p><a href=\"{{emailLink}}\" style=\"display:inline-block;padding:12px 24px;background:#EF4324;color:#FFFFFF;text-decoration:none;border-radius:8px;font-weight:700;font-family:sans-serif;\">Encontrar outro prestador</a></p><p style=\"color:#666;font-size:12px;\">Se o botão não funcionar, copia este link no teu navegador: {{emailLink}}</p>",
        },
    },
}


def patch_lang(lang):
    path = LOCALES_DIR / lang / "notifications.json"
    if not path.exists():
        print(f"  [SKIP] {lang}: {path} not found")
        return 0
    data = json.loads(path.read_text(encoding="utf-8"))
    added = 0
    for key, tmpl in TEMPLATES[lang].items():
        if key in data:
            continue
        data[key] = tmpl
        added += 1
    if added > 0:
        # Preserve formatting: indent=2, no_ascii preserved
        path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"  [{lang}] added {added} templates")
    else:
        print(f"  [{lang}] already up to date")
    return added


def main():
    print("== Inject cancel templates (booking_cancelled_by_owner/provider) ==")
    total = 0
    for lang in ["en", "fr", "es", "de", "it", "pt"]:
        total += patch_lang(lang)
    print(f"== DONE - {total} templates added across 6 locales ==")


if __name__ == "__main__":
    main()
