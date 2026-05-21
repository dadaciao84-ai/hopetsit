"""
HopeTSIT - PDF iOS consolide v23.1.149 -> v23.1.164.

Sortie : ~/Downloads/HopeTSIT_v23.1.164_Fixes_iOS_Guide.pdf

Marathon de 16 versions, ~27 bugs fixes. Document de reference pour
le rebuild iOS sur Mac.
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
    "HopeTSIT_v23.1.164_Fixes_iOS_Guide.pdf",
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
WARN = ParagraphStyle("Warn", parent=base["BodyText"], fontSize=9.5, textColor=AMBER,
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
        title="HopeTSIT v23.1.149-164 - Marathon iOS guide",
        author="HopeTSIT",
    )
    story = []

    # Page de titre
    story.append(Spacer(1, 2.5 * cm))
    story.append(p("HopeTSIT v23.1.164", TITLE))
    story.append(p("Marathon iOS consolide v149 -> v164", SUBTITLE))
    story.append(p("16 versions, ~27 bugs fixes, ~900 entries i18n", SUBTITLE))
    story.append(Spacer(1, 0.5 * cm))
    story.append(make_table([
        ["Version finale", "23.1.164 (commit 0e85691)"],
        ["Date", datetime.now().strftime("%d %B %Y")],
        ["Sessions couvertes", "v149 -> v164 (16 versions)"],
        ["Themes majeurs", "Airwallex 3 itérations, 72h cancel, halos, deep links, i18n exhaustif"],
        ["Codebases", "Backend (10 fichiers) + Frontend (20 fichiers) + 6 locales"],
        ["i18n session totale", "~150 nouvelles cles x 6 langues = ~900 entries"],
        ["Templates email", "12 nouveaux (booking_cancelled x 2 x 6 langues)"],
    ], col_widths=[5 * cm, 9 * cm]))
    story.append(Spacer(1, 1 * cm))
    story.append(p(
        "Cette session marathon a traite : tous les bugs Airwallex paiement "
        "(saga 3 versions), regle 72h cancellation pour les 3 profils avec "
        "notifs cross, halos PawSpot 4 tiers + role-color always-on, app "
        "auto-logout desactive, emails universal links, factures HTML "
        "localisees backend, walker rates 90/120min, bouton Suivre chat, "
        "bouton Annuler 72h sur 3 ecrans, Samsung nav bar grise persistante.",
        BODY,
    ))
    story.append(PageBreak())

    # Sommaire
    story.append(p("Sommaire", H1))
    sections = [
        ("1. Timeline v149 -> v164", "16 versions, statut par version"),
        ("2. Theme Airwallex paiement", "Saga 3 versions (156/157/158)"),
        ("3. Theme 72h cancellation 3 profils", "v160-v161 + notifs cross"),
        ("4. Theme Halo PawSpot", "v149-v163 (3 root causes empilees)"),
        ("5. Theme Email universal links", "v155 + factures HTML localisees"),
        ("6. Theme UX / details", "Suivre walker / Samsung nav / save invoice"),
        ("7. Theme i18n exhaustif", "~150 cles ajoutees / 6 langues"),
        ("8. Action Daniel iOS Mac", "Procedure rebuild standard"),
        ("9. Checklist tests v164 finale", "Validation cumulee 16 versions"),
    ]
    for title, desc in sections:
        story.append(p(f"<b>{title}</b> - {desc}", BODY))
    story.append(PageBreak())

    # 1. Timeline
    story.append(p("1. Timeline v149 -> v164", H1))
    rows = [
        ["Version", "Theme principal", "Bugs traites"],
        ("v149", "Halo geoloc PawMap + cadre boost owner", "2"),
        ("v150", "PawSpot tier verification + i18n shop", "1 (verif) + i18n"),
        ("v151", "Bouton submit signalement + i18n audit", "1 + i18n exhaustif"),
        ("v152", "URGENT frame home tab + couleurs hues PawSpot", "2"),
        ("v153", "Walker rates 90/120 + Send request + PawFollow plans", "3"),
        ("v154", "No auto-logout + PawSpot halo + invoice save", "3"),
        ("v155", "Email universal links + 50 replacements", "1 (gros chantier)"),
        ("v156", "Airwallex customer_id retire (mauvaise piste reverte)", "0 (revert)"),
        ("v157", "PI CANCELLED detect + enum bug 'cancelled_by_user'", "2 (VRAI fix)"),
        ("v158", "customer_id restaure pour saved cards", "1"),
        ("v159", "Chat Suivre walker -> LiveWalkMapScreen + role halo", "2"),
        ("v160", "72h cancel pour 3 profils + notifs cross", "3"),
        ("v161", "Halo always-on + Annuler 72h 3 ecrans + Samsung orange", "3"),
        ("v162", "i18n 4 strings hardcoded FR + facture HTML locale", "4"),
        ("v163", "VRAI root cause halos Obx + Samsung dark + Firebase diag", "3"),
        ("v164", "Samsung nav grey persistent + Invoice label localise", "2"),
    ]
    story.append(make_table(rows, col_widths=[2 * cm, 8.5 * cm, 4 * cm]))

    story.append(PageBreak())

    # 2. Theme Airwallex
    story.append(p("2. Theme Airwallex - saga 3 versions", H1))
    story.append(p("Symptome initial", H3))
    story.append(p(
        "Daniel : 'le paiement est tjr bloquer jpeux pas payer'. Page "
        "Airwallex affichait header + montant + footer mais aucun formulaire "
        "carte. 3 iterations pour trouver la vraie cause via les logs Render.",
        BODY,
    ))

    story.append(p("v156 - Mauvaise piste (REVERTE)", H3))
    story.append(p(
        "Theorie : customer_id avec consents PENDING_VERIFICATION fait planter "
        "le rendu HPP. Fix tente : retirer customer_id par defaut. Resultat : "
        "page blanche debloquee MAIS cartes sauvegardees devenues invisibles "
        "(effet de bord). Mauvaise direction.",
        WARN,
    ))

    story.append(p("v157 - VRAIE cause via les logs Render", H3))
    story.append(p(
        "Daniel a partage les logs. Diagnostic complet :",
        BODY,
    ))
    story.append(bullet("PI int_hkpdtpwjmhip7omewbw etait en status CANCELLED cote Airwallex"))
    story.append(bullet("Backend reutilisait aveuglement ce PI mort -> HPP vide"))
    story.append(bullet("Tap 'Annuler' renvoyait Error 500 (enum 'cancelled_by_user' invalide, valeurs valides : pending/paid/failed/refunded/cancelled/refund)"))

    story.append(p("Fix bookingController.js:2318", H3))
    story.append(code_block(
        "// On detecte le status reel du PI avant de le reutiliser\n"
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
        "// -> tombe dans la creation d'un nouveau PI ci-dessous\n\n"
        "// Fix enum line 4126\n"
        "booking.paymentStatus = 'cancelled';  // au lieu de 'cancelled_by_user'"
    ))

    story.append(p("v158 - Restore customer_id", H3))
    story.append(p(
        "Une fois v157 deploye et le PI cancelled handle proprement, on peut "
        "restaurer customer_id sans risque. Les cartes sauvegardees fonctionnent "
        "a nouveau. 4 fichiers backend :",
        BODY,
    ))
    story.append(bullet("bookingController.js:2471"))
    story.append(bullet("subscriptionRoutes.js (PawFollow)"))
    story.append(bullet("boostRoutes.js (Boost profil)"))
    story.append(bullet("mapBoostRoutes.js (PawSpot)"))

    story.append(PageBreak())

    # 3. 72h cancellation
    story.append(p("3. Theme 72h cancellation 3 profils", H1))
    story.append(p("Symptome", H3))
    story.append(p(
        "Daniel : 'owner walker au sitter peuvent annuler jusqua 72h avant'. "
        "Audit a revele 3 gros bugs :",
        BODY,
    ))
    story.append(bullet("Walker n'avait AUCUN endpoint pour annuler (asymetrie critique)"))
    story.append(bullet("Owner 'escape hatch' DELETE /:id/cancel bypassait le 72h check"))
    story.append(bullet("Aucune notification envoyee aux 2 parties sur cancel"))

    story.append(p("Fix v160 backend - selfCancelWithRefund", H3))
    story.append(code_block(
        "// Avant : isOwner || isSitter\n"
        "// Apres : isOwner || isSitter || isWalker\n\n"
        "const cancellerRole = isOwner ? 'owner'\n"
        "  : isSitter ? 'sitter' : 'walker';\n"
        "booking.cancelledBy = cancellerRole;\n\n"
        "// + sendNotification a l'autre partie :\n"
        "if (isOwner) {\n"
        "  // type='booking_cancelled_by_owner' au provider\n"
        "} else {\n"
        "  // type='booking_cancelled_by_provider' a l'owner\n"
        "}"
    ))

    story.append(p("v161 - 3 ecrans avec bouton 'Annuler (72h)'", H3))
    story.append(make_table([
        ["Profil", "Fichier", "Avant", "Apres v161"],
        ("Owner", "owner_bookings_screen.dart", "Aucun bouton", "Bouton rouge si paid + >72h"),
        ("Sitter", "sitter_bookings_screen.dart", "Existait pour pending/agreed", "+ nouveau bouton pour PAID >72h"),
        ("Walker", "walker_bookings_screen.dart", "AUCUN bouton", "Bouton pleine largeur"),
    ], col_widths=[2 * cm, 4.5 * cm, 4 * cm, 4 * cm]))

    story.append(p("12 templates email ajoutes (2 types x 6 langues)", H3))
    story.append(bullet("booking_cancelled_by_owner (push provider) : 'Reservation annulee, pas de penalite'"))
    story.append(bullet("booking_cancelled_by_provider (push owner) : 'Remboursement integral 5-10 jours'"))

    story.append(p("Verification scheduler skip", H3))
    story.append(bullet("payoutScheduler query : payoutStatus:'scheduled' -> ne match plus apres cancel"))
    story.append(bullet("processProviderPayoutForBooking ligne 894 : guard status=='paid' AND paymentStatus=='paid' -> bloque payout meme race-condition"))

    story.append(PageBreak())

    # 4. Halo PawSpot
    story.append(p("4. Theme Halo PawSpot - 3 root causes empilees", H1))
    story.append(p("Symptome", H3))
    story.append(p(
        "Daniel : 'la couleur des halo marche pas'. Repete plusieurs fois "
        "malgre des fix incrementaux. Au final, 3 root causes empilees ont "
        "ete identifiees.",
        BODY,
    ))

    story.append(p("Root cause #1 (v149) - Daniel ne voyait pas son propre halo", H3))
    story.append(p(
        "_buildHaloCircles iterait UNIQUEMENT _nearbyProviders, jamais la "
        "position user. Daniel ne voyait jamais son propre halo PawSpot. "
        "Fix : ajout du bloc self-halo lit MapBoostController.status.value.tier "
        "et dessine un halo a userPos dans la couleur du tier.",
        BODY,
    ))

    story.append(p("Root cause #2 (v161) - Anneau role-color invisible", H3))
    story.append(p(
        "v159 avait ajoute l'anneau role-color (vert walker / bleu sitter) MAIS "
        "DANS le if(isMapBoosted). Donc visible uniquement quand le provider a "
        "PawSpot actif. Comme personne autour de Daniel n'avait PawSpot, il ne "
        "voyait jamais l'anneau. Fix v161 : sortir l'anneau du if -> visible "
        "pour TOUS les providers (boosted ou non).",
        BODY,
    ))

    story.append(p("Root cause #3 (v163) - VRAI bug : Obx ne re-rendait pas", H3))
    story.append(p(
        "L'Obx wrapper du GoogleMap ne declarait PAS _nearbyProviders.length "
        "ni _showProviders.value comme dependance. Donc :",
        BODY,
    ))
    story.append(bullet("La map rebuildait uniquement au tick halo (5fps)"))
    story.append(bullet("Quand /walkers/nearby + /sitters/nearby retournaient via _nearbyProviders.assignAll(), le widget restait sur l'ancienne liste vide"))
    story.append(bullet("_buildHaloCircles s'executait sur _nearbyProviders=[] -> rien dessine"))

    story.append(code_block(
        "// v163 fix - ajout de 2 dependances dans l'Obx\n"
        "_haloPhase.value;\n"
        "_nearbyProviders.length;    // <- AJOUTE\n"
        "_showProviders.value;       // <- AJOUTE\n"
        "return GoogleMap(...);"
    ))

    story.append(p("+ Bug subtil bonus : MapBoostController jamais initialise", H3))
    story.append(p(
        "MapBoostController etait init uniquement a la 1re visite de la "
        "boutique. Donc le self-halo (qui lit son status) ne pouvait jamais "
        "s'afficher avant cette visite. Fix : Get.put(MapBoostController()) + "
        "loadStatus() forces au mount de PawMap.",
        BODY,
    ))

    story.append(p("Resultat final apres v163+v164", H3))
    story.append(bullet("Halo bleu visible a la position user (geoloc indicator)"))
    story.append(bullet("Self-halo couleur du tier PawSpot (bronze/silver/gold/platinum)"))
    story.append(bullet("Anneau role-color (vert/bleu) AUTOUR de chaque pin provider"))
    story.append(bullet("Halo tier pulsant par-dessus si PawSpot actif"))

    story.append(PageBreak())

    # 5. Email universal links
    story.append(p("5. Theme Email universal links + factures localisees", H1))
    story.append(p("Symptome v155", H3))
    story.append(p(
        "Tous les liens dans les emails pointaient vers hopetsit://... "
        "(custom scheme). Sur desktop : erreur 'app non trouvee'. Sur mobile "
        "sans app : meme erreur. Liens perdus.",
        BODY,
    ))

    story.append(p("Solution v155 - buildEmailLink helper", H3))
    story.append(bullet("Nouveau backend/src/utils/emailLinkBuilder.js avec 10 types"))
    story.append(bullet("notificationSender.js injecte {{emailLink}} automatiquement"))
    story.append(bullet("50 remplacements hopetsit:// -> {{emailLink}} dans 6 langues"))
    story.append(bullet("Universal links iOS / App Links Android (verifies via .well-known/)"))
    story.append(bullet("6 nouvelles routes dans deep_link_service.dart (walk, post, wallet, etc.)"))

    story.append(p("Facture HTML localisee (v162 + v164)", H3))
    story.append(p(
        "Le backend genere la page HTML de la facture. Initialement tout etait "
        "en anglais hardcoded. v162 a ajoute la table T avec ~13 strings par "
        "langue (titres, headers tableau, totaux, footer). v164 a complete avec "
        "le label 'Invoice' dans le <title> et le numero.",
        BODY,
    ))

    story.append(p("Label invoiceLabel par langue", H3))
    story.append(make_table([
        ["FR", "Facture"],
        ["EN", "Invoice"],
        ["ES", "Factura"],
        ["DE", "Rechnung"],
        ["IT", "Fattura"],
        ["PT", "Fatura"],
    ], col_widths=[2 * cm, 5 * cm]))

    story.append(PageBreak())

    # 6. UX details
    story.append(p("6. Theme UX / details", H1))

    story.append(p("Bouton 'Suivre' chat (v159)", H3))
    story.append(p(
        "individual_chat_screen.dart:225 ouvrait PawMapScreen() (la map "
        "generale POIs) au lieu de LiveWalkMapScreen(bookingId). Fix : remplace "
        "par LiveWalkMapScreen qui subscribe au socket walk.position et anime "
        "la camera pour suivre la position GPS du walker en temps reel.",
        BODY,
    ))

    story.append(p("Bouton 'Save Invoice to Files' (v154)", H3))
    story.append(p(
        "invoice_viewer_screen.dart AppBar avait actions:[] vide. Ajout d'un "
        "IconButton save_alt qui appelle _triggerPrint() -> ouvre le share "
        "sheet OS avec 'Save to Files' (iOS) ou 'Save to Downloads' (Android). "
        "Tooltip traduit en 6 langues ('invoice_save_to_files').",
        BODY,
    ))

    story.append(p("Samsung nav bar (v161 -> v163 -> v164)", H3))
    story.append(p(
        "3 iterations pour trouver la bonne config :",
        BODY,
    ))
    story.append(bullet("v161 : edge-to-edge -> manual + orange + icones blanches. Probleme : white-on-orange contraste moyen Samsung One UI."))
    story.append(bullet("v163 : orange + icones noires. Probleme : Get.updateLocale() reset le style -> retour icones blanches au changement de langue."))
    story.append(bullet("v164 (final) : GRIS #E5E7EB + icones sombres + wrap dans AnnotatedRegion<SystemUiOverlayStyle> au root MaterialApp -> persistent dans toutes les langues."))

    story.append(p("App no auto-logout (v154)", H3))
    story.append(p(
        "Avant : tout 401/403 d'API call entrainait logout() + redirect "
        "LoginScreen. Maintenant : auth_controller.handleLoginRequiredError() "
        "affiche un snackbar one-shot (lock 30s) et garde l'user connecte. "
        "splash_screen retire aussi le check exp() -> l'user reste connecte "
        "meme avec JWT expire (les API renverront 401, le user reste sur "
        "l'app). Seul le bouton 'Deconnecter' manuel declenche un vrai logout.",
        BODY,
    ))

    story.append(PageBreak())

    # 7. i18n
    story.append(p("7. Theme i18n exhaustif", H1))
    story.append(p(
        "Cette session a ajoute environ 150 nouvelles cles dans les 6 fichiers "
        "de traduction = ~900 entries au total. Repartition :",
        BODY,
    ))

    rows = [
        ["Version", "Theme i18n", "Cles ajoutees"],
        ("v149", "PawMap (chips, snackbars, banner)", "36 x 6 = 216"),
        ("v150", "PawSpot tier descriptions + dialog confirm", "22 x 6 = 132"),
        ("v151", "Filter chips + validation snacks + time formats", "30 x 6 = 180"),
        ("v153", "Walker rates 90/120 + post_incomplete + PawFollow plans", "13 x 6 = 78"),
        ("v154", "Session expired + invoice save tooltip", "5 x 6 = 30"),
        ("v160", "Cancellation emails 2 types", "12 templates (HTML)"),
        ("v161", "Cancel 72h dialog", "4 x 6 = 24"),
        ("v162", "Banner payment + invoice viewer + live walk", "10 x 6 = 60"),
        ("Backend", "Facture HTML T table", "~13 x 6 = 78"),
    ]
    story.append(make_table(rows, col_widths=[2 * cm, 9.5 * cm, 3 * cm]))

    story.append(p("Process automatise", H3))
    story.append(p(
        "8 scripts Python d'injection (inject_*.py) a la racine du repo. "
        "Chaque script :",
        BODY,
    ))
    story.append(bullet("Dictionnaire centralise des traductions par langue"))
    story.append(bullet("Anchor regex pour inserer apres une cle existante"))
    story.append(bullet("Dart-escape les apostrophes et caracteres speciaux"))
    story.append(bullet("Idempotent (skip si la cle existe deja)"))
    story.append(bullet("Output par langue avec count des inserts"))

    story.append(PageBreak())

    # 8. Action iOS
    story.append(p("8. Action Daniel iOS Mac", H1))
    story.append(p("Procedure rebuild", H3))
    story.append(code_block(
        "# Sur ton Mac, dans HopeTSIT_FINAL\n"
        "git pull --rebase  # -> commit 0e85691 (v23.1.164)\n"
        "cd frontend && flutter pub get\n"
        "cd ios && pod install\n"
        "open Runner.xcworkspace\n\n"
        "# Bump pubspec.yaml : version: 23.1.164+164\n"
        "flutter build ipa --release\n"
        "# Drag&drop build/ios/ipa/HopeTSIT.ipa dans Transporter -> Deliver"
    ))
    story.append(p(
        "Aucune dependance native ajoutee dans cette session. Tout est du "
        "Dart partage + i18n + backend (Render auto-deploy). Le rebuild iOS "
        "est juste un re-empacquetage des nouveaux .tr keys + le AnnotatedRegion "
        "Samsung nav bar.",
        NOTE,
    ))

    # 9. Checklist
    story.append(p("9. Checklist tests v164 finale", H1))
    story.append(p("Apres rebuild iOS + Android (force-quit + reinstall) :", BODY))

    tests = [
        ("Paiement booking - card form visible", "Plus de page blanche Airwallex"),
        ("Paiement booking - cartes sauvegardees", "Liste affichee par Airwallex HPP"),
        ("Tap 'Pay' apres tap 'Cancel'", "Nouveau PI cree (pas reuse du cancelled)"),
        ("Email confirmation - bouton 'Voir reservation'", "Ouvre /bookings/:id (app si installee, web sinon)"),
        ("Chat walker - tap 'Suivre'", "Ouvre LiveWalkMapScreen, suit GPS live"),
        ("PawMap mode owner", "Anneaux verts/bleus autour de tous les pins providers"),
        ("PawSpot active - voir son propre halo", "Halo couleur du tier (cuivre/argent/dore/ambre)"),
        ("3 profils - Bouton 'Annuler (72h)'", "Visible si paid + service >72h"),
        ("Walker annule - owner recoit notif", "'Prestation annulee + remboursement'"),
        ("Owner annule - provider recoit notif", "'Reservation annulee, pas de penalite'"),
        ("Facture HTML - bascule ES", "Tout traduit : 'Factura HOP-XXXX', 'Descripcion', 'Importe'..."),
        ("Facture HTML - bascule DE", "'Rechnung HOP-XXXX', 'Beschreibung', 'Betrag'..."),
        ("Samsung nav bar - tte langue", "Fond gris #E5E7EB + icones sombres persistantes"),
        ("App reste connectee apres JWT expire", "Pas d'auto-logout, snackbar 'Session expiree'"),
        ("Save facture PDF", "Icone save_alt -> share sheet 'Save to Files'"),
        ("Walker rates - voir 4 champs", "30/60/90/120 min"),
        ("Bouton 'Send request' post detail", "Toujours visible + snackbar si donnees incompletes"),
    ]
    rows = [["Test", "Attendu"]] + tests
    story.append(make_table(rows, col_widths=[7 * cm, 8.5 * cm]))

    story.append(p("Si un test echoue", H3))
    story.append(bullet("Capture d'ecran + courte description"))
    story.append(bullet("Indique : langue active, role (owner/sitter/walker), staff oui/non"))
    story.append(bullet("Pour Airwallex : ouvrir Render logs (Live tail) pendant le test"))
    story.append(bullet("Envoie tout ca, on corrige"))

    story.append(Spacer(1, 0.5 * cm))
    story.append(p(
        "Cette session marathon a couvert 16 versions sur ~48h, ~27 bugs "
        "fixes, ~900 entries i18n nouvelles, 0 dependance native ajoutee. "
        "L'app est maintenant stable sur Airwallex, complete en 6 langues, "
        "avec un flux 72h cancellation symetrique pour les 3 profils. Tu "
        "peux rebuilder iOS avec confiance avec les commandes section 8.",
        NOTE,
    ))

    doc.build(story)
    print(f"OK PDF v164 consolide genere : {OUTPUT}")
    print(f"   Taille : {os.path.getsize(OUTPUT) // 1024} Ko")


if __name__ == "__main__":
    build()
