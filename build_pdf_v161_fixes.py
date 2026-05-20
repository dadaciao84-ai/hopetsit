"""
HopeTSIT - Recap consolide v23.1.155 -> v23.1.161 + guide build iOS sur Mac.

Sortie : ~/Downloads/HopeTSIT_v23.1.161_Fixes_iOS_Guide.pdf

Couvre 7 versions de fixes en une session marathon :
  v155 : email universal links (https://hopetsit.com/...)
  v156 : customer_id retire (mauvaise piste, reverte v158)
  v157 : detection PI cancelled + enum cancelled_by_user
  v158 : customer_id restaure pour saved cards
  v159 : Suivre walker chat + role halo (dans isMapBoosted)
  v160 : 72h cancellation rule pour 3 profils + notifs both ways
  v161 : halo always-on + cancel button 3 profils + Samsung nav orange
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
    "HopeTSIT_v23.1.161_Fixes_iOS_Guide.pdf",
)

ORANGE = HexColor("#EF4324")
DARK_INK = HexColor("#111827")
GREY_MUTED = HexColor("#6B7280")
GREY_SOFT = HexColor("#F3F4F6")
GREEN = HexColor("#16A34A")
RED = HexColor("#DC2626")
AMBER = HexColor("#F59E0B")
BLUE = HexColor("#1A73E8")

base = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=base["Heading1"], fontSize=20, textColor=ORANGE,
                    spaceAfter=10, spaceBefore=12, fontName="Helvetica-Bold")
H2 = ParagraphStyle("H2", parent=base["Heading2"], fontSize=15, textColor=DARK_INK,
                    spaceAfter=8, spaceBefore=14, fontName="Helvetica-Bold")
H3 = ParagraphStyle("H3", parent=base["Heading3"], fontSize=11, textColor=DARK_INK,
                    spaceAfter=6, spaceBefore=10, fontName="Helvetica-Bold")
BODY = ParagraphStyle("Body", parent=base["BodyText"], fontSize=10, textColor=DARK_INK,
                      leading=14, spaceAfter=6)
NOTE = ParagraphStyle("Note", parent=base["BodyText"], fontSize=9, textColor=GREY_MUTED,
                      leading=12, spaceAfter=6, leftIndent=10)
CODE = ParagraphStyle("Code", parent=base["Code"], fontName="Courier", fontSize=8,
                      textColor=DARK_INK, leading=11, leftIndent=8, rightIndent=8,
                      spaceAfter=8, spaceBefore=4, backColor=GREY_SOFT,
                      borderColor=GREY_MUTED, borderWidth=0.5, borderPadding=6)
OK = ParagraphStyle("OK", parent=base["BodyText"], fontSize=9.5, textColor=GREEN,
                    leading=13, spaceAfter=6, leftIndent=6, fontName="Helvetica-Bold")
WARN = ParagraphStyle("Warn", parent=base["BodyText"], fontSize=9.5, textColor=RED,
                      leading=13, spaceAfter=6, leftIndent=6, fontName="Helvetica-Bold")
TITLE = ParagraphStyle("Title", parent=base["Title"], fontSize=26, textColor=ORANGE,
                       alignment=TA_CENTER, spaceAfter=10, fontName="Helvetica-Bold")
SUBTITLE = ParagraphStyle("Subtitle", parent=base["BodyText"], fontSize=12, textColor=GREY_MUTED,
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
        title="HopeTSIT v23.1.155-161 - Marathon fixes consolides",
        author="HopeTSIT",
    )
    story = []

    # Page de titre
    story.append(Spacer(1, 2.5 * cm))
    story.append(p("HopeTSIT v23.1.161", TITLE))
    story.append(p("Recap consolide v155 -> v161 (7 versions, 17 fixes)", SUBTITLE))
    story.append(p("+ Guide build iOS sur Mac", SUBTITLE))
    story.append(Spacer(1, 0.5 * cm))
    story.append(make_table([
        ["Version cible", "23.1.161 (commit 79bef16)"],
        ["Date", datetime.now().strftime("%d %B %Y")],
        ["Sessions couvertes", "v155 -> v161 (7 versions)"],
        ["Fixes prioritaires", "Airwallex paiement, 72h cancel, halos, deep links, Suivre walker"],
        ["Codebases", "Backend (5 fichiers) + Frontend (10 fichiers) + 6 locales"],
        ["i18n session totale", "~120 nouvelles cles x 6 langues"],
    ], col_widths=[5 * cm, 9 * cm]))
    story.append(Spacer(1, 1 * cm))
    story.append(p(
        "Cette session marathon a traite tous les bugs Airwallex (page blanche, "
        "carte sauvegardee invisible, PI cancelled), ajoute la regle 72h de "
        "cancellation pour les 3 profils, fixe les halos PawSpot/role, branche "
        "le bouton Suivre du chat vers la map live du walker, et reglo la "
        "barre de navigation Samsung en orange.",
        BODY,
    ))
    story.append(PageBreak())

    # Sommaire
    story.append(p("Sommaire", H1))
    sections = [
        ("1. Vue d'ensemble session v155-v161", "Timeline des 17 fixes"),
        ("2. v155 - Emails universal links", "buildEmailLink helper + 50 replacements"),
        ("3. v156-v158 - Airwallex saga (3 versions)", "page blanche + PI cancelled + saved cards"),
        ("4. v159 - Chat Suivre walker + role halo", "LiveWalkMapScreen + anneau colore"),
        ("5. v160 - Regle 72h cancellation 3 profils", "Walker peut annuler + notifs both ways"),
        ("6. v161 - Halo always-on + cancel button + nav bar", "3 derniers fixes finaux"),
        ("7. Action Daniel iOS Mac", "Procedure rebuild standard"),
        ("8. Checklist tests v161 complete", "Validation cumulee 7 versions"),
    ]
    for title, desc in sections:
        story.append(p(f"<b>{title}</b> - {desc}", BODY))
    story.append(PageBreak())

    # 1. Vue d'ensemble
    story.append(p("1. Vue d'ensemble - 7 versions, 17 fixes", H1))
    rows = [
        ["Version", "Date", "Fix(es) principal(aux)", "Statut"],
        ("v155", "May 20", "Emails -> universal links (app ou web)", "OK"),
        ("v156", "May 20", "customer_id retire (mauvaise piste)", "Reverte"),
        ("v157", "May 20", "PI cancelled detect + enum bug 'cancelled_by_user'", "OK"),
        ("v158", "May 20", "customer_id restaure pour saved cards", "OK"),
        ("v159", "May 20", "Chat Suivre -> LiveWalkMapScreen + role halo", "OK"),
        ("v160", "May 20", "72h cancel pour 3 profils + notifs both ways", "OK"),
        ("v161", "May 20", "Halo always-on + cancel button 3 profils + nav orange", "OK"),
    ]
    story.append(make_table(rows, col_widths=[2 * cm, 2.5 * cm, 7.5 * cm, 2.5 * cm]))

    story.append(p("Recap par theme", H3))
    story.append(bullet("<b>Airwallex paiement (v156-158)</b> : 3 iterations pour trouver la vraie cause (PI cancelled reutilise + enum bug, pas customer_id)"))
    story.append(bullet("<b>72h cancellation (v160-161)</b> : backend + UI sur les 3 profils owner/sitter/walker + notifs cross"))
    story.append(bullet("<b>Halo couleur (v159-161)</b> : 2 iterations - role color sort du if(isMapBoosted) pour etre always-on"))
    story.append(bullet("<b>Email links universels (v155)</b> : 50 remplacements x 6 locales + helper centralise"))
    story.append(bullet("<b>UX details (v159, v161)</b> : bouton Suivre walker chat + Samsung nav bar orange"))

    story.append(PageBreak())

    # 2. v155 - Emails
    story.append(p("2. v155 - Emails universal links (app ou web)", H1))
    story.append(p("Symptome", H3))
    story.append(p(
        "Tous les liens dans les emails (Voir la reservation, Payer maintenant, "
        "Ouvrir la conversation, etc.) pointaient vers <i>hopetsit://...</i> "
        "custom scheme. Sur desktop : erreur 'app non trouvee'. Sur mobile "
        "sans l'app : meme erreur. Liens perdus.",
        BODY,
    ))
    story.append(p("Solution", H3))
    story.append(p(
        "Nouveau helper <i>backend/src/utils/emailLinkBuilder.js</i> avec une "
        "table de routage par type (booking, pay, chat, walk, post, wallet, "
        "subscription, paw_spot...). Genere des URLs <i>https://hopetsit.com/...</i> "
        "qui sont des Universal Links iOS / App Links Android verifies via "
        "apple-app-site-association + assetlinks.json. Resultat : l'OS "
        "intercepte automatiquement et ouvre l'app si installee, sinon le "
        "site web. UN seul lien, deux comportements.",
        BODY,
    ))
    story.append(p("Implementation", H3))
    story.append(bullet("buildEmailLink(type, params) - 10 types supportes"))
    story.append(bullet("buildEmailLinkFromNotification(type, data) - wrapper qui mappe les types de notifs aux URLs"))
    story.append(bullet("notificationSender.js injecte {{emailLink}} automatiquement dans le render context"))
    story.append(bullet("Migration de 42 URLs hopetsit:// + 8 textes fallback = 50 remplacements dans 6 fichiers locale"))
    story.append(bullet("Texte fallback en bas de mail : 'copiez ce lien dans votre navigateur : {{emailLink}}'"))
    story.append(bullet("deep_link_service.dart ajoute 6 routes : walk, book/post, wallet, subscription, paw-spot, profile"))

    story.append(PageBreak())

    # 3. v156-v158 Airwallex saga
    story.append(p("3. v156-v158 - Airwallex paiement (3 iterations)", H1))
    story.append(p("Daniel : 'le paiement est tjr bloquer jpeux pas payer'", H3))
    story.append(p(
        "Page Airwallex affichait seulement header + montant 9.60 EUR + "
        "footer mais aucun formulaire carte au milieu. 3 iterations pour "
        "trouver la vraie cause.",
        BODY,
    ))
    story.append(p("v156 - Mauvaise piste : retirer customer_id", H3))
    story.append(p(
        "Theorie : customer_id avec consents PENDING_VERIFICATION → HPP "
        "rend vide. Fix : retirer customer_id par defaut. Resultat : page "
        "blanche debloquee MAIS cartes sauvegardees invisibles (effet de "
        "bord). Etait une mauvaise piste.",
        WARN,
    ))
    story.append(p("v157 - VRAIE cause via les logs Render", H3))
    story.append(p(
        "Daniel a partage les logs Render. Diagnostic :",
        BODY,
    ))
    story.append(bullet("PI int_hkpdtpwjmhip7omewbw etait en status CANCELLED cote Airwallex"))
    story.append(bullet("Backend reutilisait aveuglement ce PI mort → bridge ouvrait HPP sur un PI cancelled = page blanche"))
    story.append(bullet("Tap 'Annuler' renvoyait Error 500 (enum 'cancelled_by_user' invalide, valeurs ok: pending/paid/failed/refunded/cancelled/refund)"))
    story.append(p("Fix bookingController.js:2318", H3))
    story.append(code_block(
        "// On detecte le status reel du PI existant avant de le reutiliser\n"
        "const reusableStatuses = new Set([\n"
        "  'REQUIRES_PAYMENT_METHOD',\n"
        "  'REQUIRES_CONFIRMATION',\n"
        "  'REQUIRES_CUSTOMER_ACTION',\n"
        "]);\n"
        "if (reusableStatuses.has(existingStatus)) {\n"
        "  return existingPI;  // reuse OK\n"
        "}\n"
        "// Sinon (CANCELLED / EXPIRED / SUCCEEDED autre) :\n"
        "booking.airwallexPaymentIntentId = null;\n"
        "await booking.save();\n"
        "// → cree un nouveau PI fresh\n\n"
        "// Fix enum line 4126\n"
        "booking.paymentStatus = 'cancelled';  // au lieu de 'cancelled_by_user'"
    ))
    story.append(p("v158 - Restore customer_id", H3))
    story.append(p(
        "Une fois v157 deploye, on a pu restaurer customer_id (le vrai bug "
        "etait le PI cancelled, pas customer_id). Cartes sauvegardees "
        "fonctionnent a nouveau. 4 fichiers backend touches :",
        BODY,
    ))
    story.append(bullet("bookingController.js:2471"))
    story.append(bullet("subscriptionRoutes.js (PawFollow)"))
    story.append(bullet("boostRoutes.js (Boost profil)"))
    story.append(bullet("mapBoostRoutes.js (PawSpot)"))

    story.append(PageBreak())

    # 4. v159 - Suivre walker + role halo
    story.append(p("4. v159 - Chat 'Suivre' walker + role halo", H1))
    story.append(p("Bug 1 : Bouton Suivre du chat ouvre la mauvaise map", H3))
    story.append(p(
        "Daniel : 'quand jappuis suivre sa me renvoi sur ma map au lieu "
        "de voir sa geoloclation a lui'. Le bouton Suivre dans le chat "
        "owner ouvrait <i>PawMapScreen()</i> (la map generale de l'owner "
        "avec POIs et reports) au lieu d'ouvrir l'ecran live du walker.",
        BODY,
    ))
    story.append(p("Fix individual_chat_screen.dart:225", H3))
    story.append(code_block(
        "// AVANT\n"
        "Get.to(() => const PawMapScreen());  // ouvre TA map\n\n"
        "// APRES\n"
        "Get.to(() => LiveWalkMapScreen(bookingId: bookingId));"
    ))
    story.append(p(
        "LiveWalkMapScreen existait deja - fetch /walks/active?bookingId=X + "
        "subscribe au socket 'walk.position' + anime la camera pour suivre "
        "la position GPS du walker en temps reel.",
        NOTE,
    ))

    story.append(p("Bug 2 : Halo PawSpot pas de role color", H3))
    story.append(p(
        "Daniel : 'assure toi que le halo est aussi dune differente couleur "
        "pour le voir vert si walker, bleu si sitter'. v159 ajoutait un "
        "anneau role-color (vert/bleu) MAIS DANS le if(isMapBoosted). "
        "Resultat : seuls les providers avec PawSpot avaient l'anneau, "
        "et comme personne dans la zone de Daniel a PawSpot, il ne voyait "
        "JAMAIS le halo. Fix complet en v161 (sortie du if).",
        BODY,
    ))

    story.append(PageBreak())

    # 5. v160 - 72h cancellation
    story.append(p("5. v160 - Regle 72h cancellation pour 3 profils", H1))
    story.append(p("Daniel : 'owner walker au sitter peuvent annuler jusqua 72h avant'", H3))
    story.append(p(
        "Audit a revele 3 gros bugs :",
        BODY,
    ))
    story.append(bullet("<b>Walker n'avait AUCUN endpoint pour annuler</b> - asymetrie critique"))
    story.append(bullet("<b>Owner 'escape hatch'</b> - DELETE /:id/cancel bypass le 72h check"))
    story.append(bullet("<b>Aucune notification</b> envoyee aux 2 parties sur cancel"))

    story.append(p("Fix backend - selfCancelWithRefund", H3))
    story.append(code_block(
        "// Avant : isOwner || isSitter\n"
        "// Apres : isOwner || isSitter || isWalker\n\n"
        "const cancellerRole = isOwner ? 'owner'\n"
        "  : isSitter ? 'sitter' : 'walker';\n"
        "booking.cancelledBy = cancellerRole;\n\n"
        "// + sendNotification a l'autre partie :\n"
        "if (isOwner) {\n"
        "  // notif provider type='booking_cancelled_by_owner'\n"
        "} else {\n"
        "  // notif owner type='booking_cancelled_by_provider'\n"
        "}"
    ))

    story.append(p("Templates ajoutes (2 types x 6 langues = 12)", H3))
    story.append(bullet("<b>booking_cancelled_by_owner</b> (push provider) : 'Reservation annulee + pas de penalite'"))
    story.append(bullet("<b>booking_cancelled_by_provider</b> (push owner) : 'Remboursement integral 5-10 jours + bouton trouver autre prestataire'"))
    story.append(bullet("Emails avec {{emailLink}} (universal link vers /bookings/:id)"))

    story.append(p("Verification scheduler skip", H3))
    story.append(bullet("payoutScheduler.js query : payoutStatus:'scheduled' → ne match plus apres cancel (status devient 'cancelled')"))
    story.append(bullet("processProviderPayoutForBooking ligne 894 : guard <i>status=='paid' AND paymentStatus=='paid'</i> → bloque le payout meme en race condition"))

    story.append(PageBreak())

    # 6. v161 - 3 derniers fixes
    story.append(p("6. v161 - Halo always-on + cancel button + Samsung nav", H1))
    story.append(p("Fix #1 - Halo couleur (vraie cause)", H3))
    story.append(p(
        "L'anneau role-color de v159 etait DANS le if(isMapBoosted). En v161 "
        "on le sort de la condition → visible pour TOUS les providers sur "
        "la map (boosted ou pas). Daniel voit toujours vert/bleu autour des "
        "pins, et le halo tier pulsant (PawSpot) reste par-dessus quand "
        "isMapBoosted=true.",
        BODY,
    ))
    story.append(code_block(
        "// v161 - Restructure\n"
        "for (final p in _nearbyProviders) {\n"
        "  // Anneau role-color 25m POUR TOUS (boosted ou non)\n"
        "  final role = (p['_role'] ?? '').toString().toLowerCase();\n"
        "  final roleColor = role == 'walker'\n"
        "    ? Color(0xFF16A34A)   // vert\n"
        "    : role == 'sitter'\n"
        "      ? Color(0xFF2563EB) // bleu\n"
        "      : Color(0xFFEF4324); // orange fallback\n"
        "  circles.add(Circle(radius: 25, fillColor: ..., strokeColor: ...));\n\n"
        "  // Halo tier pulsant DESSUS si PawSpot actif\n"
        "  if (!isMapBoosted) continue;\n"
        "  // ... halo tier (bronze/silver/gold/platinum)\n"
        "}"
    ))

    story.append(p("Fix #2 - Bouton Annuler 72h sur 3 ecrans", H3))
    story.append(make_table([
        ["Profil", "Fichier", "Avant v161", "Apres v161"],
        ("Owner", "owner_bookings_screen.dart", "Aucun bouton", "Bouton rouge 'Annuler (72h)' si paid + >72h"),
        ("Sitter", "sitter_bookings_screen.dart", "Existait pour pending/agreed (requestCancellation)", "+ Nouveau bouton 'Annuler (72h)' pour PAID >72h (selfCancelBooking)"),
        ("Walker", "walker_bookings_screen.dart", "AUCUN bouton", "Bouton pleine largeur 'Annuler (72h)'"),
    ], col_widths=[2 * cm, 5 * cm, 4 * cm, 5 * cm]))

    story.append(p("Fix #3 - Barre nav Samsung orange", H3))
    story.append(code_block(
        "// AVANT main.dart\n"
        "SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge);\n"
        "systemNavigationBarColor: Colors.transparent,\n"
        "systemNavigationBarIconBrightness: Brightness.dark,\n"
        "// → 3 boutons Home/Back/Recent invisibles sur fond blanc\n\n"
        "// APRES\n"
        "SystemChrome.setEnabledSystemUIMode(\n"
        "  SystemUiMode.manual,\n"
        "  overlays: SystemUiOverlay.values,\n"
        ");\n"
        "systemNavigationBarColor: Color(0xFFEF4324),  // orange HoPetSit\n"
        "systemNavigationBarIconBrightness: Brightness.light,  // icones blanches"
    ))

    story.append(PageBreak())

    # 7. Action iOS Mac
    story.append(p("7. Action Daniel iOS Mac", H1))
    story.append(code_block(
        "# Sur ton Mac, dans HopeTSIT_FINAL\n"
        "git pull --rebase  # → commit 79bef16 (v23.1.161)\n"
        "cd frontend && flutter pub get\n"
        "cd ios && pod install\n"
        "open Runner.xcworkspace\n\n"
        "# Bump pubspec.yaml : version: 23.1.161+161\n"
        "flutter build ipa --release\n"
        "# Drag&drop build/ios/ipa/HopeTSIT.ipa dans Transporter"
    ))
    story.append(p(
        "Aucune dependance native ajoutee. Tout est du Dart partage + "
        "changements backend deployes via Render auto-deploy. Le PDF v154 "
        "+ ce PDF v161 couvrent ensemble toutes les modifs depuis le "
        "premier rebuild iOS.",
        NOTE,
    ))

    # 8. Checklist
    story.append(p("8. Checklist tests v161 complete", H1))
    story.append(p("Apres rebuild iOS + install Android :", BODY))

    tests = [
        ("Paiement booking", "Page Airwallex affiche le form de carte (pas blanche)"),
        ("Paiement saved card", "Tes cartes sauvegardees apparaissent dans HPP"),
        ("Email confirmation paiement - desktop", "Bouton 'Voir reservation' ouvre /bookings/:id sur web"),
        ("Email confirmation paiement - mobile avec app", "Bouton ouvre l'app directement (universal link)"),
        ("Chat avec walker apres paiement", "Auto-message 'Paiement confirme' visible"),
        ("Chat walker - tap 'Suivre'", "Ouvre LiveWalkMapScreen centree sur sa position GPS (pas TA map)"),
        ("PawMap mode owner", "Anneaux verts/bleus visibles autour de chaque pin walker/sitter"),
        ("PawMap - provider avec PawSpot actif", "Anneau role + halo tier pulsant par-dessus"),
        ("Owner Mes reservations - booking paid >72h", "Bouton rouge 'Annuler (72h)' visible"),
        ("Sitter Mes reservations - booking paid >72h", "Bouton 'Annuler (72h)' visible (en plus du 'Annuler' pending)"),
        ("Walker Mes reservations - booking paid >72h", "Bouton 'Annuler (72h)' pleine largeur visible"),
        ("Tap 'Annuler (72h)' → dialog confirm", "Message clair + boutons Annuler/Confirmer traduits"),
        ("Confirm cancel - walker", "Owner recoit push 'Prestation annulee + remboursement integral'"),
        ("Confirm cancel - owner", "Provider recoit push 'Reservation annulee, pas de penalite'"),
        ("Barre nav Samsung Android", "3 boutons Home/Back/Recent sur fond orange #EF4324"),
        ("App reste connectee apres expiration JWT", "Pas d'auto-logout (v154)"),
        ("Save facture PDF", "Icone save_alt dans AppBar facture, share sheet → Save to Files"),
    ]
    rows = [["Test", "Attendu"]] + tests
    story.append(make_table(rows, col_widths=[7 * cm, 8 * cm]))

    story.append(p("Recap volumes session", H3))
    story.append(bullet("17 fixes dans 7 versions (v155 -> v161)"))
    story.append(bullet("5 fichiers backend modifies"))
    story.append(bullet("10 fichiers frontend modifies"))
    story.append(bullet("~120 nouvelles cles i18n x 6 langues = ~720 entries"))
    story.append(bullet("12 nouveaux templates email (booking_cancelled x 2 x 6 langues)"))
    story.append(bullet("Aucune dependance native ajoutee - pod install standard"))

    story.append(Spacer(1, 0.5 * cm))
    story.append(p(
        "Cette session marathon cloture les bugs Airwallex paiement bloque "
        "(saga 3 versions), met en place la regle 72h cancellation symetrique "
        "pour les 3 profils avec notifs both ways, fixe les halos couleur "
        "always-on, et regle les details UX (bouton Suivre walker chat, "
        "Samsung nav orange). Tu peux maintenant rebuilder iOS avec confiance.",
        NOTE,
    ))

    doc.build(story)
    print(f"OK PDF v161 consolide genere : {OUTPUT}")
    print(f"   Taille : {os.path.getsize(OUTPUT) // 1024} Ko")


if __name__ == "__main__":
    build()
