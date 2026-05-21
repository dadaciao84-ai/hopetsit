"""HopeTSIT v23.1.170 - Inject friends_*, create_report_*, sitter_app_*,
coin_shop_boost_*, auth_*, map_boost_* i18n keys (6 langs)."""

import re
from pathlib import Path

ROOT = Path(__file__).parent
LANG_DIR = ROOT / "frontend" / "lib" / "localization" / "translations"

TRANSLATIONS = {
    # Friends screen
    "friends_screen_title": {
        "fr": "Mes amis", "en": "My friends", "es": "Mis amigos",
        "de": "Meine Freunde", "it": "I miei amici", "pt": "Os meus amigos",
    },
    "friends_invite_link_tooltip": {
        "fr": "Inviter un ami", "en": "Invite a friend", "es": "Invitar un amigo",
        "de": "Freund einladen", "it": "Invita un amico", "pt": "Convidar um amigo",
    },
    "friends_invite_subject": {
        "fr": "Rejoins-moi sur HoPetSit !",
        "en": "Join me on HoPetSit!",
        "es": "¡Únete a mí en HoPetSit!",
        "de": "Komm zu mir auf HoPetSit!",
        "it": "Unisciti a me su HoPetSit!",
        "pt": "Junta-te a mim no HoPetSit!",
    },
    "friends_invite_message": {
        "fr": "@name t\\'invite sur HoPetSit ! Télécharge l\\'app et retrouve-le sur la PawMap : @link",
        "en": "@name is inviting you to HoPetSit! Download the app and meet up on the PawMap: @link",
        "es": "@name te invita a HoPetSit! Descarga la app y encuéntrale en la PawMap: @link",
        "de": "@name lädt dich zu HoPetSit ein! Lade die App und triff ihn auf der PawMap: @link",
        "it": "@name ti invita su HoPetSit! Scarica l\\'app e incontralo sulla PawMap: @link",
        "pt": "@name convida-te para o HoPetSit! Descarrega a app e encontra-o na PawMap: @link",
    },
    "friends_tap_not_shared_title": {
        "fr": "Position non partagée",
        "en": "Position not shared",
        "es": "Ubicación no compartida",
        "de": "Position nicht geteilt",
        "it": "Posizione non condivisa",
        "pt": "Localização não partilhada",
    },
    "friends_tap_not_shared_msg": {
        "fr": "@name ne partage pas encore sa position avec toi. Demande-lui d\\'activer son partage.",
        "en": "@name is not yet sharing their location with you. Ask them to enable sharing.",
        "es": "@name aún no comparte su ubicación contigo. Pídele que active el compartir.",
        "de": "@name teilt seinen Standort noch nicht mit dir. Bitte ihn, das Teilen zu aktivieren.",
        "it": "@name non condivide ancora la sua posizione con te. Chiedigli di attivare la condivisione.",
        "pt": "@name ainda não partilha a localização contigo. Pede-lhe para ativar a partilha.",
    },

    # PawMap Premium signalement (create_report_sheet.dart:86)
    "pawmap_snack_premium_only_msg": {
        "fr": "Ce type de signalement est réservé aux membres Premium. Passe Premium pour débloquer tous les types.",
        "en": "This report type is reserved for Premium members. Go Premium to unlock all types.",
        "es": "Este tipo de aviso es solo para miembros Premium. Hazte Premium para desbloquear todos los tipos.",
        "de": "Diese Meldungsart ist nur für Premium-Mitglieder verfügbar. Werde Premium, um alle Typen freizuschalten.",
        "it": "Questo tipo di segnalazione è riservato ai membri Premium. Passa a Premium per sbloccare tutti i tipi.",
        "pt": "Este tipo de aviso está reservado a membros Premium. Passa para Premium para desbloquear todos os tipos.",
    },

    # Sitter application status chips
    "sitter_app_status_accepted": {
        "fr": "Acceptée", "en": "Accepted", "es": "Aceptada",
        "de": "Angenommen", "it": "Accettata", "pt": "Aceite",
    },
    "sitter_app_status_paid": {
        "fr": "Payée", "en": "Paid", "es": "Pagada",
        "de": "Bezahlt", "it": "Pagata", "pt": "Paga",
    },
    "sitter_app_status_cancelled": {
        "fr": "Annulée", "en": "Cancelled", "es": "Cancelada",
        "de": "Storniert", "it": "Annullata", "pt": "Cancelada",
    },

    # CoinShop boost wallet snackbars (coin_shop_screen.dart:233 + :319)
    "coin_shop_boost_wallet_confirm_msg": {
        "fr": "Débiter @amount de ton wallet pour activer le boost ?",
        "en": "Debit @amount from your wallet to activate the boost?",
        "es": "¿Cobrar @amount de tu wallet para activar el boost?",
        "de": "@amount von deinem Wallet abbuchen, um den Boost zu aktivieren?",
        "it": "Addebitare @amount dal tuo wallet per attivare il boost?",
        "pt": "Cobrar @amount da tua wallet para ativar o boost?",
    },
    "coin_shop_boost_wallet_success": {
        "fr": "Boost activé avec ton solde wallet 💰",
        "en": "Boost activated with your wallet balance 💰",
        "es": "Boost activado con tu saldo de wallet 💰",
        "de": "Boost mit deinem Wallet-Guthaben aktiviert 💰",
        "it": "Boost attivato con il tuo saldo wallet 💰",
        "pt": "Boost ativado com o teu saldo wallet 💰",
    },

    # AuthController role chooser
    "auth_multiple_roles_title": {
        "fr": "Tu as plusieurs rôles",
        "en": "You have multiple roles",
        "es": "Tienes varios roles",
        "de": "Du hast mehrere Rollen",
        "it": "Hai più ruoli",
        "pt": "Tens vários papéis",
    },

    # MapBoost controller labels
    "map_boost_tier_discovery": {
        "fr": "Découverte", "en": "Discovery", "es": "Descubrimiento",
        "de": "Entdeckung", "it": "Scoperta", "pt": "Descoberta",
    },
    "map_boost_tier_gold_pin": {
        "fr": "Pin Doré", "en": "Gold Pin", "es": "Pin Dorado",
        "de": "Goldener Pin", "it": "Pin d\\'Oro", "pt": "Pin Dourado",
    },
}


def inject(lang):
    path = LANG_DIR / f"{lang}.dart"
    text = path.read_text(encoding="utf-8")
    anchor = re.search(r"('common_close':\s*'[^']*',\s*\n)", text)
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
    print("== Inject v23.1.170 misc i18n keys ==")
    for lang in ["en", "fr", "es", "de", "it", "pt"]:
        inject(lang)
    print("== DONE ==")


if __name__ == "__main__":
    main()
