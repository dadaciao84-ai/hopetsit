"""
HopeTSIT — Guide complet pour builder l'app iOS sur Mac.

Sortie : ~/Downloads/HopeTSIT_iOS_Build_Guide_v23.1.146.pdf

Couvre :
  - Pré-requis (Mac, Xcode, Flutter, CocoaPods, Apple Developer)
  - Récup du code source (zip + git)
  - Setup Flutter + iOS dependencies
  - Configuration signing (Team J7259479JR, bundle com.hopetsit.app)
  - Activation Associated Domains (Universal Links)
  - Push notifications (Firebase APNs)
  - Build TestFlight (archive + upload)
  - Build App Store final
  - Troubleshooting fréquent
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    KeepTogether,
)

# ─── Output ────────────────────────────────────────────────────────────────
OUTPUT = os.path.join(
    os.path.expanduser("~"),
    "Downloads",
    "HopeTSIT_iOS_Build_Guide_v23.1.169.pdf",
)

# ─── Brand colors ──────────────────────────────────────────────────────────
ORANGE = HexColor("#EF4324")
DARK_INK = HexColor("#111827")
GREY_MUTED = HexColor("#6B7280")
GREY_SOFT = HexColor("#F3F4F6")
GREEN = HexColor("#16A34A")
RED = HexColor("#DC2626")
BLUE = HexColor("#1A73E8")

# ─── Styles ────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

H1 = ParagraphStyle(
    "H1", parent=base["Heading1"], fontSize=22, textColor=ORANGE,
    spaceAfter=10, spaceBefore=12, fontName="Helvetica-Bold",
)
H2 = ParagraphStyle(
    "H2", parent=base["Heading2"], fontSize=16, textColor=DARK_INK,
    spaceAfter=8, spaceBefore=18, fontName="Helvetica-Bold",
)
H3 = ParagraphStyle(
    "H3", parent=base["Heading3"], fontSize=12, textColor=DARK_INK,
    spaceAfter=6, spaceBefore=10, fontName="Helvetica-Bold",
)
BODY = ParagraphStyle(
    "Body", parent=base["BodyText"], fontSize=10, textColor=DARK_INK,
    leading=14, spaceAfter=6,
)
NOTE = ParagraphStyle(
    "Note", parent=base["BodyText"], fontSize=9, textColor=GREY_MUTED,
    leading=12, spaceAfter=6, leftIndent=10,
)
CODE = ParagraphStyle(
    "Code", parent=base["Code"], fontName="Courier", fontSize=8.5,
    textColor=DARK_INK, leading=11, leftIndent=8, rightIndent=8,
    spaceAfter=8, spaceBefore=4,
    backColor=GREY_SOFT, borderColor=GREY_MUTED, borderWidth=0.5,
    borderPadding=6,
)
WARN = ParagraphStyle(
    "Warn", parent=base["BodyText"], fontSize=9.5, textColor=RED,
    leading=13, spaceAfter=6, leftIndent=6, fontName="Helvetica-Bold",
)
OK = ParagraphStyle(
    "OK", parent=base["BodyText"], fontSize=9.5, textColor=GREEN,
    leading=13, spaceAfter=6, leftIndent=6, fontName="Helvetica-Bold",
)
TITLE = ParagraphStyle(
    "Title", parent=base["Title"], fontSize=28, textColor=ORANGE,
    alignment=TA_CENTER, spaceAfter=10, fontName="Helvetica-Bold",
)
SUBTITLE = ParagraphStyle(
    "Subtitle", parent=base["BodyText"], fontSize=13, textColor=GREY_MUTED,
    alignment=TA_CENTER, spaceAfter=20,
)


# ─── Helpers ───────────────────────────────────────────────────────────────
def p(text, style=BODY):
    """Crée un paragraphe en remplaçant les chars dangereux pour reportlab."""
    safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Réactive certaines balises markup simples
    safe = safe.replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
    safe = safe.replace("&lt;i&gt;", "<i>").replace("&lt;/i&gt;", "</i>")
    safe = safe.replace("&lt;br/&gt;", "<br/>")
    return Paragraph(safe, style)


def code_block(text):
    """Block de code monospace avec fond gris clair."""
    # Échappe < et >, mais garde les sauts de ligne
    escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    escaped = escaped.replace("\n", "<br/>")
    return Paragraph(escaped, CODE)


def bullet(text):
    """• puce simple."""
    return p("• " + text)


def warn(text):
    return p("⚠ " + text, WARN)


def ok(text):
    return p("✓ " + text, OK)


# ─── Document ──────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="HopeTSIT — iOS Build Guide v23.1.169",
        author="HopeTSIT",
    )
    story = []

    # ─── Page de titre ─────────────────────────────────────────────────────
    story.append(Spacer(1, 4 * cm))
    story.append(p("HopeTSIT", TITLE))
    story.append(p("Guide complet — Build iOS App sur Mac", SUBTITLE))
    story.append(Spacer(1, 0.5 * cm))
    story.append(
        Table(
            [
                ["Version", "23.1.168"],
                ["Bundle ID", "com.hopetsit.app"],
                ["Team ID Apple", "J7259479JR"],
                ["Cible Flutter SDK", "^3.9.2"],
                ["Cible iOS minimum", "13.0"],
                ["Date du guide", datetime.now().strftime("%d %B %Y")],
            ],
            colWidths=[5 * cm, 9 * cm],
            style=TableStyle([
                ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
                ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 10),
                ("TEXTCOLOR", (0, 0), (0, -1), DARK_INK),
                ("TEXTCOLOR", (1, 0), (1, -1), GREY_MUTED),
                ("BACKGROUND", (0, 0), (-1, -1), GREY_SOFT),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [GREY_SOFT, None]),
                ("BOX", (0, 0), (-1, -1), 0.5, GREY_MUTED),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, GREY_MUTED),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]),
        )
    )
    story.append(Spacer(1, 2 * cm))
    story.append(
        p(
            "Ce guide te prend par la main, de l'installation de Xcode jusqu'à "
            "la soumission App Store. Suis les étapes dans l'ordre. Quand "
            "quelque chose marche, coche la case à gauche du titre.",
            NOTE,
        )
    )
    story.append(PageBreak())

    # ─── Changelog v146 → v169 ─────────────────────────────────────────────
    story.append(p("Nouveautés depuis v23.1.146", H1))
    story.append(p(
        "Ce build iOS doit être généré sur la base du code source <b>v23.1.169</b>. "
        "Voici les corrections et améliorations majeures introduites entre les "
        "deux versions. Toutes sont déjà appliquées dans le ZIP source que tu "
        "as reçu : tu n'as rien à modifier côté code, juste à rebuilder.",
        BODY,
    ))

    story.append(p("v23.1.169 — Derniers bugs i18n (screenshots Daniel)", H3))
    story.append(bullet("Facture PDF : maintenant générée dans la langue de "
                        "l'app (6 langues) au lieu de toujours en français. "
                        "Le symbole € est maintenant lisible grâce à la fonte "
                        "Noto Sans embarquée (le glyphe manquait dans "
                        "Helvetica par défaut du package pdf)."))
    story.append(bullet("PawFollow store : carte \"Chat entre amis\" "
                        "(titre + description + état actif) maintenant "
                        "traduite dans les 6 langues."))
    story.append(bullet("PawSpot store : titre \"Emplacement de ton PawSpot\", "
                        "boutons \"Changer\" / \"Choisir mon spot\", tooltips "
                        "et messages d'alerte (fallback / aucune position / "
                        "loading) maintenant traduits dans les 6 langues."))
    story.append(bullet("Fiche pet : la catégorie (\"Chien\", \"Chat\"...) "
                        "et l'état de vaccination (\"À jour\"...) s'adaptent "
                        "à la langue courante même si la valeur a été stockée "
                        "en français dans la DB."))
    story.append(bullet("Affichage hauteur pet : sanitization de \".100 cm\" "
                        "vers \"0.100 cm\" (typo / virgule décimale FR "
                        "convertie en point par l'IME). Aussi nettoyé "
                        "au save côté controllers."))
    story.append(bullet("Header \"Demande de réservation\" sur post : la "
                        "string FR brute en DB est maintenant remappée vers "
                        "la locale courante (les 6 variantes acceptées)."))
    story.append(bullet("Bouton Partager / Compartir sur écran post ouvert "
                        "depuis une notification : était inerte (callback "
                        "onShare non câblé), maintenant lance SharePlus avec "
                        "le post + lien deep-link <i>hopetsit.com/post/:id</i>."))

    story.append(p("Paiements Airwallex", H3))
    story.append(bullet("Fix de la page blanche qui bloquait certains paiements : "
                        "les Payment Intents en état CANCELLED ne sont plus "
                        "réutilisés."))
    story.append(bullet("customer_id correctement attaché aux PI subscription / "
                        "boost / mapBoost (les cartes enregistrées s'affichent "
                        "à nouveau)."))
    story.append(bullet("Walker peut maintenant être payé via le même flow "
                        "Pay-In + Payout que les sitters."))

    story.append(p("Règle d'annulation 72h", H3))
    story.append(bullet("Owner, sitter et walker peuvent annuler une "
                        "réservation jusqu'à 72h avant le début, avec "
                        "remboursement automatique."))
    story.append(bullet("Bouton <b>Annuler</b> visible dans les 3 écrans "
                        "Réservations (owner / sitter / walker)."))
    story.append(bullet("Notifications envoyées aux 2 parties à l'annulation "
                        "(booking_cancelled_by_owner / _by_provider)."))

    story.append(p("PawSpot & carte interactive", H3))
    story.append(bullet("Couleur des halos par tier corrigée : bronze / silver "
                        "/ gold / platinum + anneau couleur par rôle "
                        "(vert walker, bleu sitter, orange owner)."))
    story.append(bullet("Le halo se rafraîchit immédiatement quand on active "
                        "Map Boost ou qu'on change de tier."))
    story.append(bullet("Le suivi walker depuis le chat centre la carte "
                        "sur la position du walker en temps réel."))

    story.append(p("Universal Links (emails → app)", H3))
    story.append(bullet("Tous les boutons des emails (réservation, paiement, "
                        "chat, walk, wallet, abonnement, PawSpot) ouvrent "
                        "désormais l'app iOS via <b>https://hopetsit.com/...</b> "
                        "au lieu de l'ancien scheme <i>hopetsit://</i>."))
    story.append(bullet("Le fichier <b>.well-known/apple-app-site-association</b> "
                        "est déjà servi par le site Next.js (Vercel). Tu n'as "
                        "qu'à activer la capability <b>Associated Domains</b> "
                        "dans Xcode (voir section 7 de ce guide)."))

    story.append(p("Factures (PDF + HTML)", H3))
    story.append(bullet("Le mot \"Invoice\" est traduit en 6 langues "
                        "(FR / EN / ES / DE / IT / PT) dans la facture HTML."))
    story.append(bullet("Bouton \"Enregistrer la facture PDF dans les "
                        "fichiers du téléphone\" ajouté."))

    story.append(p("Onboarding redesign", H3))
    story.append(bullet("Nouvelle page d'accueil : 3 cartes blanches "
                        "(Pet-sitting / PawMap / PawFollow) avec icône, "
                        "titre et description courte sous chaque carte."))
    story.append(bullet("Logo plus grand (130w), titre 36sp, bouton "
                        "S'inscrire avec icône patte + flèche."))
    story.append(bullet("Descriptions raccourcies et lisibles dans les "
                        "6 langues (\"Sitters de confiance près de toi\", "
                        "\"Lieux pet-friendly autour de toi\", "
                        "\"Suis les aventures de ton animal\")."))
    story.append(bullet("Gradient orange/blanc bien en arrière-plan, ne "
                        "couvre plus les cartes."))

    story.append(p("UX divers", H3))
    story.append(bullet("Barre de nav système (Android Samsung) en gris "
                        "#E5E7EB pour rester visible quand on change de langue."))
    story.append(bullet("Auto-logout au expiry du token : supprimé, l'app "
                        "reste connectée."))
    story.append(bullet("Tarifs walker : champs 90min + 120min ajoutés."))
    story.append(bullet("PawFollow : noms et descriptions des plans "
                        "traduits en 6 langues."))
    story.append(bullet("Bouton \"Send request\" remis sur la page détail "
                        "d'un post."))

    story.append(Spacer(1, 0.5 * cm))
    story.append(p(
        "Côté iOS, aucune action manuelle requise : tu vas builder normalement "
        "à partir du dossier <b>frontend/</b>. La seule chose à vérifier dans "
        "Xcode reste la capability <b>Associated Domains</b> (section 7) qui "
        "doit lister <i>applinks:hopetsit.com</i> et <i>applinks:www.hopetsit.com</i>.",
        NOTE,
    ))
    story.append(PageBreak())

    # ─── Sommaire ──────────────────────────────────────────────────────────
    story.append(p("Sommaire", H1))
    story.append(p("1. Pré-requis matériels et comptes", H3))
    story.append(p("2. Installer Xcode + outils", H3))
    story.append(p("3. Installer Flutter sur Mac", H3))
    story.append(p("4. Récupérer le code source HopeTSIT", H3))
    story.append(p("5. Setup iOS — premier `pod install`", H3))
    story.append(p("6. Configuration signing dans Xcode", H3))
    story.append(p("7. Activer Associated Domains (Universal Links)", H3))
    story.append(p("8. Push notifications (APNs + Firebase)", H3))
    story.append(p("9. Build de test sur appareil physique", H3))
    story.append(p("10. Archive + upload TestFlight", H3))
    story.append(p("11. Soumission App Store finale", H3))
    story.append(p("12. Troubleshooting fréquent", H3))
    story.append(PageBreak())

    # ─── 1. Pré-requis ─────────────────────────────────────────────────────
    story.append(p("1. Pré-requis matériels et comptes", H1))
    story.append(p("Matériel", H3))
    story.append(bullet("Mac avec macOS 13 (Ventura) ou plus récent."))
    story.append(bullet("Au moins 50 Go d'espace disque libre (Xcode = 15 Go, "
                        "+ caches Flutter/CocoaPods)."))
    story.append(bullet("RAM minimum 8 Go ; 16 Go recommandé pour Xcode."))
    story.append(bullet("Un iPhone réel pour tester les Universal Links "
                        "(le simulateur ne supporte pas tous les flows)."))
    story.append(p("Comptes obligatoires", H3))
    story.append(bullet("<b>Apple ID</b> avec authentification à 2 facteurs activée."))
    story.append(bullet("<b>Apple Developer Program</b> payant 99 €/an "
                        "(obligatoire pour distribuer sur l'App Store). "
                        "Inscris-toi sur developer.apple.com/programs/enroll."))
    story.append(bullet("<b>Compte Firebase</b> pour les push notifs (déjà "
                        "configuré dans le projet, GoogleService-Info.plist "
                        "fourni)."))
    story.append(warn(
        "Sans Apple Developer Program tu peux builder l'app pour ton iPhone "
        "perso mais l'app expire au bout de 7 jours et tu ne peux PAS faire "
        "TestFlight ni soumettre à l'App Store."
    ))

    # ─── 2. Xcode ──────────────────────────────────────────────────────────
    story.append(p("2. Installer Xcode + outils", H1))
    story.append(p("2.1 Xcode depuis l'App Store", H3))
    story.append(bullet("Ouvre l'App Store → cherche \"Xcode\" → Installer."))
    story.append(bullet("Téléchargement ~10-15 Go. Compte 1-2 h selon ta "
                        "connexion."))
    story.append(bullet("Ouvre Xcode une fois → accepte la licence → laisse "
                        "installer les Additional Components."))

    story.append(p("2.2 Command Line Tools", H3))
    story.append(code_block("xcode-select --install"))
    story.append(p("Une fenêtre Apple va s'ouvrir. Click \"Installer\". "
                   "5-10 min.", NOTE))

    story.append(p("2.3 CocoaPods", H3))
    story.append(p("Gestionnaire de dépendances iOS utilisé par Flutter. "
                   "Vérifie qu'il est installé :", BODY))
    story.append(code_block("pod --version"))
    story.append(p("Si commande non trouvée :", BODY))
    story.append(code_block("sudo gem install cocoapods\npod setup"))
    story.append(p("Le `pod setup` télécharge le specs repo, première fois "
                   "ça prend 15-30 min. Sois patient.", NOTE))

    story.append(p("2.4 Homebrew (optionnel mais utile)", H3))
    story.append(code_block(
        '/bin/bash -c "$(curl -fsSL '
        'https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    ))

    story.append(PageBreak())

    # ─── 3. Flutter ────────────────────────────────────────────────────────
    story.append(p("3. Installer Flutter sur Mac", H1))
    story.append(p("Le projet HopeTSIT cible Flutter SDK ^3.9.2.", BODY))
    story.append(p("3.1 Télécharger Flutter", H3))
    story.append(bullet("Va sur docs.flutter.dev/get-started/install/macos"))
    story.append(bullet("Télécharge le ZIP pour Apple Silicon (M1/M2/M3) "
                        "ou Intel selon ton Mac."))
    story.append(bullet("Dézippe dans ton home, par exemple :"))
    story.append(code_block(
        "cd ~/development\nunzip ~/Downloads/flutter_macos_*.zip"
    ))
    story.append(p("3.2 Ajouter au PATH", H3))
    story.append(p("Édite ~/.zshrc et ajoute :", BODY))
    story.append(code_block('export PATH="$PATH:$HOME/development/flutter/bin"'))
    story.append(p("Recharge :", BODY))
    story.append(code_block("source ~/.zshrc"))
    story.append(p("3.3 Vérifier l'installation", H3))
    story.append(code_block("flutter doctor"))
    story.append(p("Tu dois voir <b>tous les checkmarks</b> pour la section "
                   "iOS. Si l'un est en rouge, suis les instructions affichées "
                   "(souvent: licence Xcode pas acceptée, run "
                   "<i>flutter doctor --android-licenses</i> n'est pas "
                   "nécessaire si tu ne touches pas Android).", BODY))

    # ─── 4. Code source ────────────────────────────────────────────────────
    story.append(p("4. Récupérer le code source HopeTSIT", H1))
    story.append(p("4.1 Depuis le ZIP fourni", H3))
    story.append(p("Tu as reçu un fichier <b>HopeTSIT_FINAL.zip</b> dans "
                   "Téléchargements. Dézippe-le où tu veux :", BODY))
    story.append(code_block(
        "cd ~/Projects\nunzip ~/Downloads/HopeTSIT_FINAL.zip"
    ))
    story.append(p("4.2 Ou depuis Git (plus propre)", H3))
    story.append(p("Si tu as accès au repo GitHub HopeTSIT :", BODY))
    story.append(code_block(
        "cd ~/Projects\n"
        "git clone https://github.com/hopetsit/hopetsit.git\n"
        "cd hopetsit"
    ))
    story.append(p("4.3 Structure du projet", H3))
    story.append(bullet("<b>frontend/</b> — code Flutter (Android + iOS)"))
    story.append(bullet("<b>backend/</b> — Node.js Express (Render)"))
    story.append(bullet("<b>website/</b> — Next.js (Vercel, hopetsit.com)"))
    story.append(p("Pour iOS, tu travailleras uniquement dans <b>frontend/</b>.",
                   NOTE))

    story.append(PageBreak())

    # ─── 5. Setup iOS ──────────────────────────────────────────────────────
    story.append(p("5. Setup iOS — premier `pod install`", H1))
    story.append(p("5.1 Récupérer les dépendances Flutter", H3))
    story.append(code_block("cd frontend\nflutter pub get"))
    story.append(p("5.2 Lancer pod install", H3))
    story.append(code_block("cd ios\npod install"))
    story.append(p("Première fois : 5-15 min (téléchargement des libs Firebase, "
                   "Google Maps, etc.). Tu dois voir à la fin :", NOTE))
    story.append(code_block("Pod installation complete!"))
    story.append(p("5.3 Désigner l'IDE", H3))
    story.append(p("À partir de maintenant, tu ouvres <b>uniquement</b> le "
                   "fichier <b>Runner.xcworkspace</b> (PAS Runner.xcodeproj) :",
                   BODY))
    story.append(code_block("open Runner.xcworkspace"))
    story.append(warn("Si tu ouvres Runner.xcodeproj, les pods CocoaPods ne "
                      "seront PAS liés et le build échouera avec des erreurs "
                      "de symboles introuvables."))

    # ─── 6. Signing ────────────────────────────────────────────────────────
    story.append(p("6. Configuration signing dans Xcode", H1))
    story.append(p("Dans Xcode, sélectionne le target <b>Runner</b> en haut "
                   "à gauche, puis onglet <b>Signing &amp; Capabilities</b>.",
                   BODY))
    story.append(p("6.1 Team", H3))
    story.append(bullet("Coche <b>Automatically manage signing</b>."))
    story.append(bullet("Sélectionne ton Team Apple Developer "
                        "(<b>J7259479JR</b> si c'est ton Team)."))
    story.append(bullet("Xcode va automatiquement créer un provisioning "
                        "profile lié à ton compte."))
    story.append(p("6.2 Bundle Identifier", H3))
    story.append(bullet("Vérifie qu'il est sur <b>com.hopetsit.app</b>."))
    story.append(bullet("Si une erreur \"already registered to another team\" "
                        "apparaît, c'est qu'un autre dev a déjà ce bundle. "
                        "Soit tu utilises son Team, soit tu changes le "
                        "bundle (déconseillé — les push Firebase ne "
                        "marcheront plus)."))
    story.append(p("6.3 iOS Deployment Target", H3))
    story.append(bullet("Onglet General → Deployment Info → iOS 13.0 minimum."))

    # ─── 7. Associated Domains ─────────────────────────────────────────────
    story.append(p("7. Activer Associated Domains (Universal Links)", H1))
    story.append(p("Sans cette étape, les liens <i>https://hopetsit.com/...</i> "
                   "ouvriront Safari au lieu de l'app.", BODY))
    story.append(p("7.1 Ajouter la capability", H3))
    story.append(bullet("Dans <b>Signing &amp; Capabilities</b>, click "
                        "<b>+ Capability</b> en haut."))
    story.append(bullet("Cherche \"Associated Domains\" → double-click."))
    story.append(bullet("Xcode lit automatiquement le fichier "
                        "<b>ios/Runner/Runner.entitlements</b> qui contient "
                        "déjà :"))
    story.append(code_block(
        "applinks:hopetsit.com\n"
        "applinks:www.hopetsit.com\n"
        "applinks:app.hopetsit.com"
    ))
    story.append(p("7.2 Vérifier apple-app-site-association", H3))
    story.append(p("Le fichier est déjà hébergé sur Vercel. Vérifie-le avec :",
                   BODY))
    story.append(code_block(
        "curl https://hopetsit.com/.well-known/apple-app-site-association"
    ))
    story.append(p("Tu dois voir du JSON avec <i>J7259479JR.com.hopetsit.app</i>. "
                   "Si curl retourne 404, push le site Next.js d'abord.", NOTE))
    story.append(p("7.3 Test sur iPhone réel", H3))
    story.append(bullet("Désinstalle l'app HopeTSIT sur ton iPhone si "
                        "présente (Apple cache les Universal Links agressivement)."))
    story.append(bullet("Build et installe l'app fraîche via Xcode."))
    story.append(bullet("Envoie-toi un mail avec un lien "
                        "<i>https://hopetsit.com/pay/abc</i>."))
    story.append(bullet("Appuie longuement sur le lien dans Mail → tu dois "
                        "voir l'option \"Ouvrir dans HoPetSit\"."))

    story.append(PageBreak())

    # ─── 8. Push notifications ─────────────────────────────────────────────
    story.append(p("8. Push notifications (APNs + Firebase)", H1))
    story.append(p("L'app utilise Firebase Cloud Messaging (FCM) pour les push "
                   "Android et iOS. Sur iOS, FCM passe par APNs (Apple Push "
                   "Notification Service).", BODY))
    story.append(p("8.1 APNs Key dans Apple Developer", H3))
    story.append(bullet("Va sur developer.apple.com → Certificates → Keys."))
    story.append(bullet("Click \"+ Add\" → Apple Push Notifications service "
                        "(APNs)."))
    story.append(bullet("Télécharge le fichier .p8 (UNE SEULE FOIS — garde-le "
                        "précieusement)."))
    story.append(bullet("Note le <b>Key ID</b> et ton <b>Team ID</b> "
                        "(J7259479JR)."))
    story.append(p("8.2 Uploader le .p8 dans Firebase", H3))
    story.append(bullet("Va sur console.firebase.google.com → projet HopeTSIT."))
    story.append(bullet("Project Settings → Cloud Messaging → onglet Apple."))
    story.append(bullet("Upload le .p8 + remplis Key ID + Team ID."))
    story.append(p("8.3 Capability Push dans Xcode", H3))
    story.append(bullet("Dans <b>Signing &amp; Capabilities</b>, ajoute la "
                        "capability <b>Push Notifications</b>."))
    story.append(bullet("Ajoute aussi <b>Background Modes</b> et coche "
                        "<i>Remote notifications</i>."))

    # ─── 9. Build sur device ───────────────────────────────────────────────
    story.append(p("9. Build de test sur appareil physique", H1))
    story.append(p("9.1 Connecter ton iPhone", H3))
    story.append(bullet("Branche ton iPhone au Mac en USB."))
    story.append(bullet("Sur l'iPhone, accepte \"Faire confiance à cet "
                        "ordinateur\"."))
    story.append(bullet("Dans Xcode, sélectionne ton iPhone dans le menu "
                        "device en haut."))
    story.append(p("9.2 Run", H3))
    story.append(code_block("flutter run --release -d &lt;device-id&gt;"))
    story.append(p("Ou directement dans Xcode : <b>Product → Run</b> "
                   "(Cmd+R).", BODY))
    story.append(p("9.3 Erreur \"Untrusted Developer\"", H3))
    story.append(p("Sur l'iPhone : Réglages → Général → VPN et gestion des "
                   "appareils → ton Apple ID → Faire confiance.", BODY))

    # ─── 10. TestFlight ────────────────────────────────────────────────────
    story.append(p("10. Archive + upload TestFlight", H1))
    story.append(p("TestFlight = bêta publique avant App Store. Permet à "
                   "100 testeurs externes + ton équipe interne de tester.",
                   BODY))
    story.append(p("10.1 Bump la version", H3))
    story.append(p("Édite <b>pubspec.yaml</b> ligne 4 :", BODY))
    story.append(code_block("version: 23.1.146+146"))
    story.append(p("Format : <i>nom.affiché+build.number</i>. Pour TestFlight, "
                   "incrémente le build.number à chaque upload (147, 148...).",
                   NOTE))
    story.append(p("10.2 Build IPA", H3))
    story.append(code_block(
        "cd frontend\n"
        "flutter build ipa --release"
    ))
    story.append(p("Sortie : <b>build/ios/ipa/HopeTSIT.ipa</b>.", BODY))
    story.append(p("10.3 Upload via Transporter", H3))
    story.append(bullet("Télécharge <b>Transporter</b> depuis l'App Store Mac."))
    story.append(bullet("Connecte-toi avec ton Apple ID."))
    story.append(bullet("Drag &amp; drop le fichier .ipa."))
    story.append(bullet("Click \"Deliver\". Upload 5-15 min selon ta connexion."))
    story.append(p("10.4 Activer le build sur TestFlight", H3))
    story.append(bullet("Va sur appstoreconnect.apple.com → ton app → "
                        "TestFlight."))
    story.append(bullet("Attends 5-15 min que le build soit \"Processed\"."))
    story.append(bullet("Renseigne ce qui manque (changelog, contact "
                        "tester...) → soumets pour Beta App Review."))
    story.append(bullet("Beta review approuve en 24-48 h (généralement plus "
                        "souple que la review App Store)."))

    story.append(PageBreak())

    # ─── 11. App Store ─────────────────────────────────────────────────────
    story.append(p("11. Soumission App Store finale", H1))
    story.append(p("11.1 Préparer la fiche App Store", H3))
    story.append(p("Dans App Store Connect, prépare :", BODY))
    story.append(bullet("Screenshots 6.7\" (iPhone 15 Pro Max) — 3 à 10 par "
                        "langue."))
    story.append(bullet("Description (4000 caractères max), keywords "
                        "(100 chars), URL de support, URL marketing."))
    story.append(bullet("Catégorie principale : <i>Lifestyle</i> ou "
                        "<i>Travel</i>."))
    story.append(bullet("Privacy Policy URL : <i>https://hopetsit.com/privacy</i>."))
    story.append(bullet("Age rating : remplis le questionnaire honnêtement."))
    story.append(p("11.2 Data Privacy déclarations", H3))
    story.append(p("Onglet App Privacy → déclare ce qui est collecté :", BODY))
    story.append(bullet("Contact Info → Email Address, Phone Number "
                        "(linked to user identity, used for App "
                        "Functionality)."))
    story.append(bullet("Location → Precise Location "
                        "(linked, App Functionality — live walk tracking)."))
    story.append(bullet("Identifiers → User ID (linked, App Functionality)."))
    story.append(bullet("Diagnostics → Crash Data, Performance Data "
                        "(not linked, Analytics)."))
    story.append(p("11.3 Submit", H3))
    story.append(bullet("Sélectionne le build TestFlight déjà approuvé."))
    story.append(bullet("Add for Review."))
    story.append(bullet("Review prend en moyenne 24-72 h."))

    # ─── 12. Troubleshooting ───────────────────────────────────────────────
    story.append(p("12. Troubleshooting fréquent", H1))

    story.append(p("Erreur \"No matching profiles found\"", H3))
    story.append(bullet("Va dans Xcode → Preferences → Accounts → ton "
                        "Apple ID → Download Manual Profiles."))
    story.append(bullet("Ou refais : Signing &amp; Capabilities → décoche / "
                        "recoche Automatically manage signing."))

    story.append(p("Erreur CocoaPods \"sandbox not in sync\"", H3))
    story.append(code_block(
        "cd ios\n"
        "pod deintegrate\n"
        "pod install"
    ))

    story.append(p("Build crash au lancement \"missing privacy manifest\"", H3))
    story.append(p("iOS 17.5+ demande un PrivacyInfo.xcprivacy pour certaines "
                   "API. Si Xcode te le signale, ajoute le fichier suggéré "
                   "(Xcode propose un template).", BODY))

    story.append(p("Universal Links n'ouvrent pas l'app", H3))
    story.append(bullet("Vérifie que <i>https://hopetsit.com/.well-known/apple-app-site-association</i> "
                        "retourne du JSON avec ton AppID."))
    story.append(bullet("Désinstalle puis réinstalle l'app (iOS cache "
                        "agressivement)."))
    story.append(bullet("Ne tape PAS l'URL dans Safari direct (ça ouvre "
                        "toujours Safari). Clique-la depuis Mail, Notes ou "
                        "Messages."))
    story.append(bullet("Sur l'iPhone : Réglages → ton compte → iCloud → "
                        "désactive puis réactive Private Relay (parfois bloque "
                        "la vérification d'Apple)."))

    story.append(p("Push notifications ne s'affichent pas", H3))
    story.append(bullet("Vérifie que la capability Push Notifications est "
                        "activée dans Xcode."))
    story.append(bullet("Vérifie que le .p8 est uploadé dans Firebase."))
    story.append(bullet("Sur l'iPhone : Réglages → HoPetSit → Notifications → "
                        "Autoriser."))
    story.append(bullet("Teste avec Firebase Console → Cloud Messaging → "
                        "Send test message → colle le FCM token de "
                        "l'appareil (affiché dans les logs flutter run)."))

    story.append(p("Erreur \"App requires App Sandbox\" sur upload", H3))
    story.append(p("C'est macOS, pas iOS. Vérifie que tu builds bien pour "
                   "<b>iOS Device</b> et pas <b>My Mac</b>.", BODY))

    story.append(Spacer(1, 1 * cm))
    story.append(p("Si tu coinces : appelle Claude 🤖. Joins la sortie complète "
                   "de la commande qui plante + une capture d'écran de Xcode.",
                   NOTE))

    # ─── Build ─────────────────────────────────────────────────────────────
    doc.build(story)
    print(f"OK PDF généré : {OUTPUT}")
    print(f"Taille : {os.path.getsize(OUTPUT) // 1024} Ko")


if __name__ == "__main__":
    build()
