"""HopeTSIT v23.1.172 - Inject all new i18n keys for labels Suivre + UI Famille + erreurs invite."""

import re
from pathlib import Path

ROOT = Path(__file__).parent
LANG_DIR = ROOT / "frontend" / "lib" / "localization" / "translations"

TRANSLATIONS = {
    # Bouton owner — Suivre en direct mon animal
    "follow_button_live_my_pet": {
        "fr": "Suivre en direct mon animal",
        "en": "Track my pet live",
        "es": "Seguir a mi mascota en vivo",
        "de": "Mein Tier live verfolgen",
        "it": "Segui il mio animale in diretta",
        "pt": "Seguir o meu animal ao vivo",
    },
    # Bouton walker/sitter — Partager ma position en direct
    "follow_share_position_button": {
        "fr": "Partager ma position en direct",
        "en": "Share my live position",
        "es": "Compartir mi ubicación en vivo",
        "de": "Meinen Live-Standort teilen",
        "it": "Condividi la mia posizione live",
        "pt": "Partilhar a minha posição ao vivo",
    },

    # Onglets friends_screen
    "friends_tab_friends": {
        "fr": "Amis", "en": "Friends", "es": "Amigos",
        "de": "Freunde", "it": "Amici", "pt": "Amigos",
    },
    "friends_tab_requests": {
        "fr": "Demandes", "en": "Requests", "es": "Solicitudes",
        "de": "Anfragen", "it": "Richieste", "pt": "Pedidos",
    },
    "friends_tab_family": {
        "fr": "Famille", "en": "Family", "es": "Familia",
        "de": "Familie", "it": "Famiglia", "pt": "Família",
    },

    # Erreurs invitation amis
    "friends_invite_sent_title": {
        "fr": "Demande envoyée",
        "en": "Request sent",
        "es": "Solicitud enviada",
        "de": "Anfrage gesendet",
        "it": "Richiesta inviata",
        "pt": "Pedido enviado",
    },
    "friends_invite_sent_msg": {
        "fr": "On préviendra @name dès qu\\'iel accepte.",
        "en": "We\\'ll notify @name as soon as they accept.",
        "es": "Avisaremos a @name en cuanto acepte.",
        "de": "Wir benachrichtigen @name, sobald die Anfrage angenommen wird.",
        "it": "Avviseremo @name appena accetta.",
        "pt": "Avisaremos @name assim que aceitar.",
    },
    "friends_invite_err_already_pending": {
        "fr": "Une demande est déjà en attente avec cette personne.",
        "en": "A request is already pending with this person.",
        "es": "Ya hay una solicitud pendiente con esta persona.",
        "de": "Eine Anfrage ist bereits ausstehend bei dieser Person.",
        "it": "C\\'è già una richiesta in attesa con questa persona.",
        "pt": "Já existe um pedido pendente com esta pessoa.",
    },
    "friends_invite_err_already_accepted": {
        "fr": "Vous êtes déjà amis.",
        "en": "You are already friends.",
        "es": "Ya sois amigos.",
        "de": "Ihr seid bereits Freunde.",
        "it": "Siete già amici.",
        "pt": "Já são amigos.",
    },
    "friends_invite_err_self": {
        "fr": "Tu ne peux pas t\\'ajouter toi-même.",
        "en": "You cannot add yourself.",
        "es": "No puedes añadirte a ti mismo.",
        "de": "Du kannst dich nicht selbst hinzufügen.",
        "it": "Non puoi aggiungere te stesso.",
        "pt": "Não podes adicionar-te a ti próprio.",
    },

    # Famille — État sans abo
    "family_no_plan_title": {
        "fr": "PawFollow Famille",
        "en": "PawFollow Family",
        "es": "PawFollow Familia",
        "de": "PawFollow Familie",
        "it": "PawFollow Famiglia",
        "pt": "PawFollow Família",
    },
    "family_no_plan_desc": {
        "fr": "Active PawFollow Famille (€9.99/mois) pour suivre jusqu\\'à 5 personnes de ta famille en direct sur la carte.",
        "en": "Activate PawFollow Family (€9.99/month) to track up to 5 family members live on the map.",
        "es": "Activa PawFollow Familia (€9.99/mes) para seguir hasta 5 personas de tu familia en directo en el mapa.",
        "de": "Aktiviere PawFollow Familie (€9.99/Monat), um bis zu 5 Familienmitglieder live auf der Karte zu verfolgen.",
        "it": "Attiva PawFollow Famiglia (€9.99/mese) per seguire fino a 5 membri della famiglia in diretta sulla mappa.",
        "pt": "Ativa PawFollow Família (€9.99/mês) para seguir até 5 membros da família ao vivo no mapa.",
    },
    "family_no_plan_cta": {
        "fr": "Souscrire PawFollow Famille",
        "en": "Subscribe to PawFollow Family",
        "es": "Suscribirse a PawFollow Familia",
        "de": "PawFollow Familie abonnieren",
        "it": "Abbonati a PawFollow Famiglia",
        "pt": "Subscrever PawFollow Família",
    },

    # Famille — État actif
    "family_header_title": {
        "fr": "PawFollow Famille actif",
        "en": "PawFollow Family active",
        "es": "PawFollow Familia activo",
        "de": "PawFollow Familie aktiv",
        "it": "PawFollow Famiglia attivo",
        "pt": "PawFollow Família ativo",
    },
    "family_slots": {
        "fr": "@used / @total membres ajoutés",
        "en": "@used / @total members added",
        "es": "@used / @total miembros añadidos",
        "de": "@used / @total Mitglieder hinzugefügt",
        "it": "@used / @total membri aggiunti",
        "pt": "@used / @total membros adicionados",
    },
    "family_empty_msg": {
        "fr": "Tu n\\'as pas encore ajouté de membre. Tape « Inviter un ami » ci-dessous.",
        "en": "You haven\\'t added any member yet. Tap « Add a friend » below.",
        "es": "Aún no has añadido ningún miembro. Toca « Añadir un amigo » abajo.",
        "de": "Du hast noch kein Mitglied hinzugefügt. Tippe unten auf « Freund hinzufügen ».",
        "it": "Non hai ancora aggiunto alcun membro. Tocca « Aggiungi un amico » qui sotto.",
        "pt": "Ainda não adicionaste nenhum membro. Toca em « Adicionar um amigo » abaixo.",
    },
    "family_full_msg": {
        "fr": "Famille pleine (4 membres + toi).",
        "en": "Family full (4 members + you).",
        "es": "Familia llena (4 miembros + tú).",
        "de": "Familie voll (4 Mitglieder + du).",
        "it": "Famiglia piena (4 membri + tu).",
        "pt": "Família cheia (4 membros + tu).",
    },
    "family_add_member_btn": {
        "fr": "+ Inviter un ami à ma famille",
        "en": "+ Add a friend to my family",
        "es": "+ Invitar a un amigo a mi familia",
        "de": "+ Freund zu meiner Familie hinzufügen",
        "it": "+ Invita un amico nella mia famiglia",
        "pt": "+ Convidar um amigo para a minha família",
    },
    "family_add_member_title": {
        "fr": "Ajouter à ma famille",
        "en": "Add to my family",
        "es": "Añadir a mi familia",
        "de": "Zu meiner Familie hinzufügen",
        "it": "Aggiungi alla mia famiglia",
        "pt": "Adicionar à minha família",
    },
    "family_add_member_pick": {
        "fr": "Choisis un ami parmi tes amis acceptés.",
        "en": "Choose a friend from your accepted friends list.",
        "es": "Elige un amigo de tu lista de amigos aceptados.",
        "de": "Wähle einen Freund aus deiner Liste akzeptierter Freunde.",
        "it": "Scegli un amico dalla lista degli amici accettati.",
        "pt": "Escolhe um amigo da tua lista de amigos aceites.",
    },
    "family_add_member_no_friends": {
        "fr": "Tu n\\'as pas encore d\\'ami accepté à ajouter.",
        "en": "You have no accepted friends to add yet.",
        "es": "Aún no tienes amigos aceptados para añadir.",
        "de": "Du hast noch keine akzeptierten Freunde zum Hinzufügen.",
        "it": "Non hai ancora amici accettati da aggiungere.",
        "pt": "Ainda não tens amigos aceites para adicionar.",
    },
    "family_add_btn": {
        "fr": "Ajouter", "en": "Add", "es": "Añadir",
        "de": "Hinzufügen", "it": "Aggiungi", "pt": "Adicionar",
    },
    "family_remove_member_tooltip": {
        "fr": "Retirer de la famille",
        "en": "Remove from family",
        "es": "Quitar de la familia",
        "de": "Aus Familie entfernen",
        "it": "Rimuovi dalla famiglia",
        "pt": "Remover da família",
    },
    "family_member_added_title": {
        "fr": "Membre ajouté",
        "en": "Member added",
        "es": "Miembro añadido",
        "de": "Mitglied hinzugefügt",
        "it": "Membro aggiunto",
        "pt": "Membro adicionado",
    },
    "family_member_added_msg": {
        "fr": "@name fait maintenant partie de ta famille PawFollow.",
        "en": "@name is now part of your PawFollow family.",
        "es": "@name ya forma parte de tu familia PawFollow.",
        "de": "@name ist nun Teil deiner PawFollow Familie.",
        "it": "@name fa ora parte della tua famiglia PawFollow.",
        "pt": "@name faz agora parte da tua família PawFollow.",
    },
    "family_member_removed_title": {
        "fr": "Membre retiré",
        "en": "Member removed",
        "es": "Miembro eliminado",
        "de": "Mitglied entfernt",
        "it": "Membro rimosso",
        "pt": "Membro removido",
    },
    "family_member_removed_msg": {
        "fr": "@name a été retiré de ta famille.",
        "en": "@name has been removed from your family.",
        "es": "@name ha sido eliminado de tu familia.",
        "de": "@name wurde aus deiner Familie entfernt.",
        "it": "@name è stato rimosso dalla tua famiglia.",
        "pt": "@name foi removido da tua família.",
    },
    "family_err_full": {
        "fr": "Famille pleine. Retire un membre avant d\\'en ajouter un nouveau.",
        "en": "Family full. Remove a member before adding a new one.",
        "es": "Familia llena. Elimina un miembro antes de añadir uno nuevo.",
        "de": "Familie voll. Entferne ein Mitglied, bevor du ein neues hinzufügst.",
        "it": "Famiglia piena. Rimuovi un membro prima di aggiungerne uno nuovo.",
        "pt": "Família cheia. Remove um membro antes de adicionar um novo.",
    },
    "family_err_already_member": {
        "fr": "Cette personne fait déjà partie de ta famille.",
        "en": "This person is already in your family.",
        "es": "Esta persona ya forma parte de tu familia.",
        "de": "Diese Person ist bereits in deiner Familie.",
        "it": "Questa persona fa già parte della tua famiglia.",
        "pt": "Esta pessoa já faz parte da tua família.",
    },
    "family_err_plan_required": {
        "fr": "Abonnement PawFollow Famille requis.",
        "en": "PawFollow Family subscription required.",
        "es": "Se requiere suscripción PawFollow Familia.",
        "de": "PawFollow Familie Abonnement erforderlich.",
        "it": "Abbonamento PawFollow Famiglia richiesto.",
        "pt": "Subscrição PawFollow Família necessária.",
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
