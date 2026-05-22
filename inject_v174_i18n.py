"""HopeTSIT v23.1.174 - Inject i18n keys for Block, Family invite email, common."""

import re
from pathlib import Path

ROOT = Path(__file__).parent
LANG_DIR = ROOT / "frontend" / "lib" / "localization" / "translations"

TRANSLATIONS = {
    # common_cancel — fallback
    "common_cancel": {
        "fr": "Annuler", "en": "Cancel", "es": "Cancelar",
        "de": "Abbrechen", "it": "Annulla", "pt": "Cancelar",
    },

    # Friend block/remove
    "friend_block": {
        "fr": "Bloquer", "en": "Block", "es": "Bloquear",
        "de": "Blockieren", "it": "Blocca", "pt": "Bloquear",
    },
    "friend_remove": {
        "fr": "Supprimer", "en": "Remove", "es": "Eliminar",
        "de": "Entfernen", "it": "Rimuovi", "pt": "Remover",
    },
    "friend_block_confirm": {
        "fr": "Bloquer cet ami ?",
        "en": "Block this friend?",
        "es": "¿Bloquear este amigo?",
        "de": "Diesen Freund blockieren?",
        "it": "Bloccare questo amico?",
        "pt": "Bloquear este amigo?",
    },
    "friend_block_confirm_desc": {
        "fr": "@name ne pourra plus t\\'envoyer de message ni de demande.",
        "en": "@name won\\'t be able to message or send you requests anymore.",
        "es": "@name ya no podrá enviarte mensajes ni solicitudes.",
        "de": "@name kann dir keine Nachrichten oder Anfragen mehr senden.",
        "it": "@name non potrà più inviarti messaggi o richieste.",
        "pt": "@name já não poderá enviar-te mensagens nem pedidos.",
    },
    "friend_remove_confirm": {
        "fr": "Supprimer cet ami ?",
        "en": "Remove this friend?",
        "es": "¿Eliminar este amigo?",
        "de": "Diesen Freund entfernen?",
        "it": "Rimuovere questo amico?",
        "pt": "Remover este amigo?",
    },
    "friend_remove_confirm_desc": {
        "fr": "@name sera retiré de ta liste d\\'amis des deux côtés.",
        "en": "@name will be removed from your friends list on both sides.",
        "es": "@name será eliminado de tu lista de amigos en ambos lados.",
        "de": "@name wird auf beiden Seiten aus deiner Freundesliste entfernt.",
        "it": "@name verrà rimosso dalla lista amici da entrambe le parti.",
        "pt": "@name será removido da tua lista de amigos em ambos os lados.",
    },
    "friend_blocked_title": {
        "fr": "Ami bloqué",
        "en": "Friend blocked",
        "es": "Amigo bloqueado",
        "de": "Freund blockiert",
        "it": "Amico bloccato",
        "pt": "Amigo bloqueado",
    },
    "friend_blocked_msg": {
        "fr": "@name est désormais bloqué.",
        "en": "@name is now blocked.",
        "es": "@name está ahora bloqueado.",
        "de": "@name ist jetzt blockiert.",
        "it": "@name è ora bloccato.",
        "pt": "@name está agora bloqueado.",
    },
    "friend_removed_title": {
        "fr": "Ami retiré",
        "en": "Friend removed",
        "es": "Amigo eliminado",
        "de": "Freund entfernt",
        "it": "Amico rimosso",
        "pt": "Amigo removido",
    },
    "friend_removed_msg": {
        "fr": "Ami retiré de ta liste.",
        "en": "Friend removed from your list.",
        "es": "Amigo eliminado de tu lista.",
        "de": "Freund aus deiner Liste entfernt.",
        "it": "Amico rimosso dalla tua lista.",
        "pt": "Amigo removido da tua lista.",
    },

    # Blocked users screen
    "friend_blocked_list": {
        "fr": "Utilisateurs bloqués",
        "en": "Blocked users",
        "es": "Usuarios bloqueados",
        "de": "Blockierte Benutzer",
        "it": "Utenti bloccati",
        "pt": "Utilizadores bloqueados",
    },
    "friend_blocked_empty": {
        "fr": "Tu n\\'as bloqué personne.",
        "en": "You haven\\'t blocked anyone.",
        "es": "No has bloqueado a nadie.",
        "de": "Du hast niemanden blockiert.",
        "it": "Non hai bloccato nessuno.",
        "pt": "Não bloqueaste ninguém.",
    },
    "friend_unblock": {
        "fr": "Débloquer", "en": "Unblock", "es": "Desbloquear",
        "de": "Entsperren", "it": "Sblocca", "pt": "Desbloquear",
    },
    "friend_unblocked_title": {
        "fr": "Utilisateur débloqué",
        "en": "User unblocked",
        "es": "Usuario desbloqueado",
        "de": "Benutzer entsperrt",
        "it": "Utente sbloccato",
        "pt": "Utilizador desbloqueado",
    },
    "friend_unblocked_msg": {
        "fr": "@name est désormais débloqué.",
        "en": "@name is now unblocked.",
        "es": "@name está ahora desbloqueado.",
        "de": "@name ist jetzt entsperrt.",
        "it": "@name è ora sbloccato.",
        "pt": "@name está agora desbloqueado.",
    },
    "friend_unblock_failed": {
        "fr": "Impossible de débloquer pour le moment.",
        "en": "Unable to unblock right now.",
        "es": "No se puede desbloquear ahora.",
        "de": "Entsperren derzeit nicht möglich.",
        "it": "Impossibile sbloccare ora.",
        "pt": "Não foi possível desbloquear agora.",
    },

    # Family add by name/email tabs
    "family_add_by_name": {
        "fr": "Par nom", "en": "By name", "es": "Por nombre",
        "de": "Nach Name", "it": "Per nome", "pt": "Por nome",
    },
    "family_add_by_email": {
        "fr": "Par email", "en": "By email", "es": "Por email",
        "de": "Nach E-Mail", "it": "Per email", "pt": "Por email",
    },
    "family_add_by_email_desc": {
        "fr": "Si l\\'email a déjà un compte HoPetSit, l\\'invitation arrive in-app. Sinon on envoie un email d\\'invitation.",
        "en": "If the email has a HoPetSit account, the invite arrives in-app. Otherwise we send an email invitation.",
        "es": "Si el email tiene cuenta HoPetSit, la invitación llega in-app. Si no, enviamos un email de invitación.",
        "de": "Wenn die E-Mail ein HoPetSit-Konto hat, kommt die Einladung in der App. Sonst senden wir eine Einladungs-E-Mail.",
        "it": "Se l\\'email ha un account HoPetSit, l\\'invito arriva in-app. Altrimenti inviamo un\\'email d\\'invito.",
        "pt": "Se o email tem conta HoPetSit, o convite chega in-app. Caso contrário, enviamos um email de convite.",
    },
    "family_invite_send_btn": {
        "fr": "Envoyer l\\'invitation",
        "en": "Send invitation",
        "es": "Enviar invitación",
        "de": "Einladung senden",
        "it": "Invia invito",
        "pt": "Enviar convite",
    },
    "family_invite_invalid_email": {
        "fr": "Email invalide.",
        "en": "Invalid email.",
        "es": "Email no válido.",
        "de": "Ungültige E-Mail.",
        "it": "Email non valida.",
        "pt": "Email inválido.",
    },
    "family_invite_sent": {
        "fr": "Invitation envoyée",
        "en": "Invitation sent",
        "es": "Invitación enviada",
        "de": "Einladung gesendet",
        "it": "Invito inviato",
        "pt": "Convite enviado",
    },
    "family_invite_existing_user_msg": {
        "fr": "Membre ajouté à ta famille.",
        "en": "Member added to your family.",
        "es": "Miembro añadido a tu familia.",
        "de": "Mitglied zu deiner Familie hinzugefügt.",
        "it": "Membro aggiunto alla tua famiglia.",
        "pt": "Membro adicionado à tua família.",
    },
    "family_invite_email_sent_msg": {
        "fr": "Email d\\'invitation envoyé à @email.",
        "en": "Invitation email sent to @email.",
        "es": "Email de invitación enviado a @email.",
        "de": "Einladungs-E-Mail an @email gesendet.",
        "it": "Email d\\'invito inviata a @email.",
        "pt": "Email de convite enviado para @email.",
    },

    # Chat lock states (Daniel asked for these)
    "chat_locked_after_service": {
        "fr": "Conversation terminée",
        "en": "Conversation ended",
        "es": "Conversación finalizada",
        "de": "Konversation beendet",
        "it": "Conversazione terminata",
        "pt": "Conversa terminada",
    },
    "chat_locked_payment_required": {
        "fr": "Le chat s\\'ouvre après confirmation du paiement",
        "en": "Chat opens after payment confirmation",
        "es": "El chat se abre tras la confirmación del pago",
        "de": "Chat öffnet sich nach Zahlungsbestätigung",
        "it": "La chat si apre dopo la conferma del pagamento",
        "pt": "O chat abre após a confirmação do pagamento",
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
