"""
HopeTSIT - Recap des fixes v23.1.155 + guide build iOS sur Mac.

Sortie : ~/Downloads/HopeTSIT_v23.1.155_Fixes_iOS_Guide.pdf

Daniel : "connecte les boutons quon recois par mail a lapp ou le web".

Les boutons CTA des emails (Voir la reservation, Payer maintenant, Voir la
candidature, Ouvrir la conversation, etc.) ouvraient des liens custom
scheme hopetsit:// qui plantaient sur desktop. Maintenant ils utilisent
des universal links https://hopetsit.com/... qui ouvrent l'app si
installee, sinon le site web.
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle,
)

OUTPUT = os.path.join(
    os.path.expanduser("~"),
    "Downloads",
    "HopeTSIT_v23.1.155_Fixes_iOS_Guide.pdf",
)

ORANGE = HexColor("#EF4324")
DARK_INK = HexColor("#111827")
GREY_MUTED = HexColor("#6B7280")
GREY_SOFT = HexColor("#F3F4F6")
GREEN = HexColor("#16A34A")
RED = HexColor("#DC2626")
AMBER = HexColor("#F59E0B")

base = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=base["Heading1"], fontSize=22, textColor=ORANGE,
                    spaceAfter=10, spaceBefore=12, fontName="Helvetica-Bold")
H3 = ParagraphStyle("H3", parent=base["Heading3"], fontSize=12, textColor=DARK_INK,
                    spaceAfter=6, spaceBefore=10, fontName="Helvetica-Bold")
BODY = ParagraphStyle("Body", parent=base["BodyText"], fontSize=10, textColor=DARK_INK,
                      leading=14, spaceAfter=6)
NOTE = ParagraphStyle("Note", parent=base["BodyText"], fontSize=9, textColor=GREY_MUTED,
                      leading=12, spaceAfter=6, leftIndent=10)
CODE = ParagraphStyle("Code", parent=base["Code"], fontName="Courier", fontSize=8.5,
                      textColor=DARK_INK, leading=11, leftIndent=8, rightIndent=8,
                      spaceAfter=8, spaceBefore=4, backColor=GREY_SOFT,
                      borderColor=GREY_MUTED, borderWidth=0.5, borderPadding=6)
OK = ParagraphStyle("OK", parent=base["BodyText"], fontSize=9.5, textColor=GREEN,
                    leading=13, spaceAfter=6, leftIndent=6, fontName="Helvetica-Bold")
TITLE = ParagraphStyle("Title", parent=base["Title"], fontSize=28, textColor=ORANGE,
                       alignment=TA_CENTER, spaceAfter=10, fontName="Helvetica-Bold")
SUBTITLE = ParagraphStyle("Subtitle", parent=base["BodyText"], fontSize=13, textColor=GREY_MUTED,
                          alignment=TA_CENTER, spaceAfter=20)


def p(text, style=BODY):
    safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    safe = safe.replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
    safe = safe.replace("&lt;i&gt;", "<i>").replace("&lt;/i&gt;", "</i>")
    safe = safe.replace("&lt;br/&gt;", "<br/>")
    return Paragraph(safe, style)


def code_block(text):
    escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    escaped = escaped.replace("\n", "<br/>")
    return Paragraph(escaped, CODE)


def bullet(text):
    return p("- " + text)


def make_table(rows, col_widths=None):
    if col_widths is None:
        col_widths = [4 * cm] + [3 * cm] * (len(rows[0]) - 1)
    t = Table(rows, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "Helvetica", 9),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
        ("TEXTCOLOR", (0, 0), (-1, 0), DARK_INK),
        ("BACKGROUND", (0, 0), (-1, 0), GREY_SOFT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [None, GREY_SOFT]),
        ("BOX", (0, 0), (-1, -1), 0.5, GREY_MUTED),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, GREY_MUTED),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def build():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title="HopeTSIT v23.1.155 - Email universal links",
        author="HopeTSIT",
    )
    story = []

    story.append(Spacer(1, 3 * cm))
    story.append(p("HopeTSIT v23.1.155", TITLE))
    story.append(p("Email CTA buttons → universal links (app or web)", SUBTITLE))
    story.append(p("+ Guide build iOS sur Mac", SUBTITLE))
    story.append(Spacer(1, 0.5 * cm))
    story.append(make_table([
        ["Version", "23.1.155"],
        ["Date", datetime.now().strftime("%d %B %Y")],
        ["Demande", "Connecter les boutons des emails a l'app OU au web"],
        ["Codebases touchees", "Backend (1 helper + 1 service + 6 locales) + Frontend (1 service)"],
        ["Remplacements", "50 dans les 6 fichiers locale notifications.json"],
    ], col_widths=[5 * cm, 9 * cm]))
    story.append(Spacer(1, 1.5 * cm))
    story.append(p(
        "Daniel : <i>\"connecte les boutons quon recois par mail a lapp ou "
        "le web\"</i>. Avant cette session, les boutons CTA des emails "
        "pointaient vers des liens custom-scheme <i>hopetsit://...</i> qui "
        "marchaient seulement sur mobile avec l'app installee. Maintenant "
        "tous les boutons utilisent des universal links HTTPS qui "
        "fonctionnent partout.",
        BODY,
    ))
    story.append(PageBreak())

    story.append(p("Sommaire", H1))
    sections = [
        ("1. Vue d'ensemble v155", "1 demande, 4 sous-taches"),
        ("2. Probleme + solution", "Custom scheme → universal links"),
        ("3. emailLinkBuilder.js helper", "Routage centralise par type"),
        ("4. Templates email migres", "50 remplacements x 6 langues"),
        ("5. Routes deep link app etendues", "+6 chemins (walk/book/wallet/...)"),
        ("6. Action Daniel iOS Mac", "Procedure rebuild standard"),
        ("7. Checklist tests v155", "Verification cross-platform"),
    ]
    for title, desc in sections:
        story.append(p(f"<b>{title}</b> - {desc}", BODY))
    story.append(PageBreak())

    # 1. Vue d'ensemble
    story.append(p("1. Vue d'ensemble v155", H1))
    rows = [
        ["Sous-tache", "Fichiers", "Statut"],
        ("Helper buildEmailLink(type, params)", "backend/src/utils/emailLinkBuilder.js", "Cree (200 lignes)"),
        ("Migration templates 6 langues", "backend/src/locales/<lang>/notifications.json", "50 replacements"),
        ("Injection emailLink dans render context", "backend/src/services/notificationSender.js", "1 hook ajoute"),
        ("Routes deep link app etendues", "frontend/lib/services/deep_link_service.dart", "+6 routes"),
    ]
    story.append(make_table(rows, col_widths=[6 * cm, 7 * cm, 3 * cm]))

    story.append(p("Architecture", H3))
    story.append(p(
        "Le helper <i>buildEmailLink</i> est l'unique source de verite "
        "pour TOUTES les URLs des emails. Il est appele automatiquement "
        "par <i>notificationSender.js</i> qui derive le type de lien "
        "depuis le type de notification (booking_paid → /bookings/:id, "
        "new_message → /chat/:id, payout_succeeded → /wallet, etc.). "
        "Le resultat est injecte comme variable <i>{{emailLink}}</i> "
        "dans le template, qui l'utilise pour le <i>href</i> du bouton "
        "ET pour le texte de fallback en bas (\"copiez ce lien : ...\").",
        BODY,
    ))

    story.append(PageBreak())

    # 2. Probleme + solution
    story.append(p("2. Probleme + solution", H1))
    story.append(p("Avant - tout en hopetsit://", H3))
    story.append(code_block(
        "<!-- backend/src/locales/fr/notifications.json -->\n"
        "<a href=\"hopetsit://pay/{{bookingId}}\">Payer maintenant</a>\n\n"
        "<!-- Resultat sur desktop : 'app non trouvee' -->\n"
        "<!-- Resultat sur mobile sans app : 'app non trouvee' -->\n"
        "<!-- Resultat sur mobile avec app : OK (ouvre l'app) -->"
    ))
    story.append(p("Apres - universal link", H3))
    story.append(code_block(
        "<!-- backend/src/locales/fr/notifications.json -->\n"
        "<a href=\"{{emailLink}}\">Payer maintenant</a>\n\n"
        "<!-- Rendu en https://hopetsit.com/pay?bookingId=abc -->\n"
        "<!-- Resultat sur desktop : ouvre le site web (page /pay) -->\n"
        "<!-- Resultat sur mobile sans app : ouvre le site web -->\n"
        "<!-- Resultat sur mobile avec app : ouvre l'app directement\n"
        "     via Universal Link iOS / App Link Android verifie -->"
    ))
    story.append(p("Pre-requis deja en place", H3))
    story.append(bullet("iOS Runner.entitlements declare applinks:hopetsit.com (v23.1 part 146)"))
    story.append(bullet("Android AndroidManifest.xml a intent-filter avec android:autoVerify=true"))
    story.append(bullet("Site web sert .well-known/apple-app-site-association et assetlinks.json"))
    story.append(bullet("deep_link_service.dart whitelist hopetsit.com / www.hopetsit.com / app.hopetsit.com"))

    story.append(PageBreak())

    # 3. emailLinkBuilder
    story.append(p("3. backend/src/utils/emailLinkBuilder.js helper", H1))
    story.append(p("Table de routage par type", H3))
    rows = [
        ["Type", "URL generee", "Use case email"],
        ("booking", "/bookings/:id", "booking_new / booking_accepted / booking_paid"),
        ("application", "/bookings/:id", "application_new (owner voit la candidature)"),
        ("pay", "/pay?bookingId=:id", "payment_required (relance owner)"),
        ("chat", "/chat/:conversationId", "new_message / chat_created"),
        ("walk", "/walk/:bookingId", "walk_started / walk_finished (live tracking)"),
        ("post", "/book/:postId", "post_new / post_application_eligible"),
        ("wallet", "/wallet", "payout_succeeded / withdrawal_completed"),
        ("subscription", "/subscription", "subscription_renewed / subscription_canceled"),
        ("paw_spot", "/paw-spot", "map_boost_active / map_boost_expired"),
        ("notifications", "/notifications", "fallback notifications inbox"),
    ]
    story.append(make_table(rows, col_widths=[3 * cm, 5 * cm, 7.5 * cm]))

    story.append(p("Helper buildEmailLinkFromNotification(type, data)", H3))
    story.append(p(
        "Wrapper qui prend le type de notification (string comme 'booking_paid') "
        "et le payload data ({bookingId, conversationId, ...}) et retourne la "
        "bonne URL. C'est ce qu'utilise notificationSender — pas besoin que "
        "chaque caller connaisse la table de routage.",
        BODY,
    ))

    story.append(PageBreak())

    # 4. Templates email migres
    story.append(p("4. Templates email migres", H1))
    story.append(p("Script automatise migrate_email_links.py", H3))
    story.append(p(
        "Script Python qui scanne les 6 fichiers <i>backend/src/locales/&lt;"
        "lang&gt;/notifications.json</i> et remplace 2 motifs :",
        BODY,
    ))
    story.append(bullet("Regex <i>hopetsit://[a-zA-Z]+(/\\{\\{[a-zA-Z]+\\}\\})?</i> → {{emailLink}}"))
    story.append(bullet("Texte de fallback \"ouvrez l'app HoPetSit manuellement\" → \"copiez ce lien : {{emailLink}}\""))

    story.append(p("Resultats par langue", H3))
    rows = [
        ["Langue", "URL replacements", "Fallback text replacements"],
        ("en", "7", "1"),
        ("fr", "7", "2"),
        ("es", "7", "1"),
        ("de", "7", "1"),
        ("it", "7", "1"),
        ("pt", "7", "2"),
        ("Total", "42", "8 = 50 replacements"),
    ]
    story.append(make_table(rows, col_widths=[3 * cm, 4 * cm, 5 * cm]))

    story.append(p("Templates touches (7 par langue)", H3))
    story.append(bullet("<b>booking_accepted</b> (provider) : 'Voir la demande' → /bookings/:id"))
    story.append(bullet("<b>booking_new</b> (owner) : 'Voir la reservation' → /bookings/:id"))
    story.append(bullet("<b>booking_accepted</b> (owner) : 'Payer maintenant' → /pay?bookingId="))
    story.append(bullet("<b>application_new</b> (owner) : 'Voir la candidature' → /bookings/:id"))
    story.append(bullet("<b>NEW_MESSAGE</b> : 'Ouvrir la conversation' → /chat/:id"))
    story.append(bullet("<b>booking_paid</b> (provider) : 'Voir la reservation' → /bookings/:id"))
    story.append(bullet("<b>booking_paid_owner</b> (owner) : 'Voir la reservation' → /bookings/:id"))

    story.append(PageBreak())

    # 5. Routes deep link app
    story.append(p("5. Routes deep link app etendues", H1))
    story.append(p(
        "frontend/lib/services/deep_link_service.dart gerait 5 chemins. "
        "On en ajoute 6 nouveaux pour matcher toutes les URLs que peut "
        "generer emailLinkBuilder.",
        BODY,
    ))
    story.append(p("Routes avant (v23.1 part 146)", H3))
    story.append(bullet("/pay/:bookingId → ecran paiement"))
    story.append(bullet("/chat[/:conversationId] → tab chat"))
    story.append(bullet("/bookings[/:bookingId] → tab reservations"))
    story.append(bullet("/notifications → tab notifications"))
    story.append(bullet("/auth?ott=... → bridge session web → app"))

    story.append(p("Routes ajoutees v23.1.155", H3))
    story.append(bullet("<b>/walk/:bookingId</b> → tab reservations (live walk integre dedans)"))
    story.append(bullet("<b>/book/:postId</b> ou <b>/post/:postId</b> → home (posts dans le feed)"))
    story.append(bullet("<b>/wallet</b> → tab profil (carte Mes paiements)"))
    story.append(bullet("<b>/subscription</b> ou <b>/paw-spot</b> → tab shop"))
    story.append(bullet("<b>/profile</b> → tab profil"))

    story.append(p("Pay accepte aussi ?bookingId= en query", H3))
    story.append(p(
        "Le helper backend genere /pay?bookingId=X (et non /pay/X) pour "
        "harmoniser avec la page web existante. On accepte donc les 2 "
        "formats dans le handler app : si segs.last == 'pay' (donc pas "
        "de path arg), on lit uri.queryParameters['bookingId'].",
        BODY,
    ))

    story.append(PageBreak())

    # 6. Action iOS
    story.append(p("6. Ce qu'il te reste a faire sur Mac (iOS)", H1))
    story.append(code_block(
        "# Sur ton Mac\n"
        "git pull --rebase  # → commit 95d303d (v23.1.155)\n"
        "cd frontend && flutter pub get\n"
        "cd ios && pod install\n"
        "open Runner.xcworkspace\n\n"
        "# Bump pubspec.yaml : version: 23.1.155+155\n"
        "flutter build ipa --release\n"
        "# Drag&drop .ipa dans Transporter"
    ))
    story.append(p(
        "Aucune dependance native ajoutee. C'est principalement un changement "
        "backend (Render auto-deploy s'occupe du serveur) + une petite "
        "extension du service deep_link cote frontend.",
        NOTE,
    ))
    story.append(p("Render deploy", H3))
    story.append(p(
        "Backend pushe sur main → Render auto-deploy demarre. Verifier sur "
        "dashboard.render.com que le deploy contient le commit 95d303d ou "
        "plus recent. Une fois deploye, les prochains emails utilisent "
        "automatiquement {{emailLink}}.",
        BODY,
    ))

    # 7. Checklist
    story.append(p("7. Checklist tests v155", H1))
    tests = [
        ("Owner paie un booking (declenche booking_paid_owner email)", "Email recu avec bouton 'Voir la reservation'"),
        ("Click bouton sur DESKTOP", "Navigateur ouvre https://hopetsit.com/bookings/X"),
        ("Click bouton sur mobile AVEC app installee", "App ouvre directement sur le booking"),
        ("Click bouton sur mobile SANS app installee", "Navigateur ouvre le site /bookings/X"),
        ("Provider recoit booking_paid email", "Bouton 'Voir la reservation' fonctionne aussi"),
        ("Owner recoit application_new email", "Bouton 'Voir la candidature' → /bookings/:id"),
        ("Owner recoit booking_accepted email", "Bouton 'Payer maintenant' → /pay?bookingId=X"),
        ("Owner ou Provider recoit NEW_MESSAGE email", "Bouton 'Ouvrir la conversation' → /chat/:id"),
        ("Provider recoit payout_succeeded email", "Bouton → /wallet (tab profil dans l'app)"),
        ("Email en EN/ES/DE/IT/PT", "Bouton fonctionne identiquement (URL meme dans toutes les langues)"),
        ("Texte fallback en bas d'email", "Contient 'copiez ce lien : https://hopetsit.com/...'"),
        ("Plus de hopetsit:// dans aucun email", "grep hopetsit:// dans les 6 locales → 0 result"),
        ("Tests v154 toujours OK", "No auto-logout, halo PawSpot, invoice save"),
    ]
    rows = [["Test", "Attendu"]] + tests
    story.append(make_table(rows, col_widths=[7.5 * cm, 8 * cm]))

    story.append(Spacer(1, 1 * cm))
    story.append(p(
        "Cette v155 cloture la demande Daniel : tous les boutons des emails "
        "fonctionnent maintenant cross-platform (app si installee, sinon web). "
        "Architecture extensible — pour rajouter un nouveau type d'email avec "
        "un nouveau bouton, il suffit de :<br/>"
        "1. Ajouter le mapping dans emailLinkBuilder.buildEmailLinkFromNotification<br/>"
        "2. Mettre {{emailLink}} dans le template HTML<br/>"
        "3. Ajouter le path correspondant dans deep_link_service.dart si besoin",
        NOTE,
    ))

    doc.build(story)
    print(f"OK PDF v155 fixes recap genere : {OUTPUT}")
    print(f"   Taille : {os.path.getsize(OUTPUT) // 1024} Ko")


if __name__ == "__main__":
    build()
