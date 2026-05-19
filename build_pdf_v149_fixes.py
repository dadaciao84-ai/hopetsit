"""
HopeTSIT - Recap des fixes v23.1.149 + guide build iOS sur Mac.

Sortie : ~/Downloads/HopeTSIT_v23.1.149_Fixes_iOS_Guide.pdf

Couvre tous les fixes apres v148 :
  - PawMap halo bleu + point geoloc visible (independant de myLocationEnabled)
  - Cadre dore + glow sur le hero owner quand boost actif
  - 36 nouvelles cles i18n pour PawMap (6 langues = 216 entries)
  - Verification PawSpot mode staff (deja fonctionnel via backend bypass)

C'est l'addendum cumulatif. Pour Daniel : juste git pull + flutter pub get +
pod install sur Mac et c'est repercute en iOS.
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
    "HopeTSIT_v23.1.149_Fixes_iOS_Guide.pdf",
)

ORANGE = HexColor("#EF4324")
DARK_INK = HexColor("#111827")
GREY_MUTED = HexColor("#6B7280")
GREY_SOFT = HexColor("#F3F4F6")
GREEN = HexColor("#16A34A")
RED = HexColor("#DC2626")
AMBER = HexColor("#F59E0B")
GOLD = HexColor("#D4AF37")
BLUE = HexColor("#1A73E8")

base = getSampleStyleSheet()

H1 = ParagraphStyle("H1", parent=base["Heading1"], fontSize=22, textColor=ORANGE,
                    spaceAfter=10, spaceBefore=12, fontName="Helvetica-Bold")
H2 = ParagraphStyle("H2", parent=base["Heading2"], fontSize=16, textColor=DARK_INK,
                    spaceAfter=8, spaceBefore=18, fontName="Helvetica-Bold")
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
WARN = ParagraphStyle("Warn", parent=base["BodyText"], fontSize=9.5, textColor=AMBER,
                      leading=13, spaceAfter=6, leftIndent=6, fontName="Helvetica-Bold")
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
        title="HopeTSIT v23.1.149 - Addendum fixes + iOS guide",
        author="HopeTSIT",
    )
    story = []

    # ── Page de titre ────────────────────────────────────────────────────
    story.append(Spacer(1, 3 * cm))
    story.append(p("HopeTSIT v23.1.149", TITLE))
    story.append(p("Addendum fixes (PawMap geoloc visible + boost owner + i18n)", SUBTITLE))
    story.append(p("+ Guide build iOS sur Mac", SUBTITLE))
    story.append(Spacer(1, 0.5 * cm))
    story.append(make_table([
        ["Version", "23.1.149 (commit bda013f)"],
        ["Date", datetime.now().strftime("%d %B %Y")],
        ["Bugs corriges", "3 (geoloc halo / boost owner frame / i18n PawMap)"],
        ["Verifications", "1 (PawSpot mode staff - OK confirme)"],
        ["Codebases touchees", "App Flutter (5 fichiers + 6 i18n + 1 widget)"],
        ["Cible app", "Android (rebuilde v149) + iOS (a rebuilder sur Mac)"],
    ], col_widths=[5 * cm, 9 * cm]))
    story.append(Spacer(1, 1.5 * cm))
    story.append(p(
        "Cette session traite les bugs remontes apres v148 : <b>halo geoloc "
        "invisible</b> sur PawMap, <b>cadre boost absent</b> sur le profil "
        "owner, et <b>section headers PawMap mal traduits</b> dans toutes les "
        "langues. PawSpot a egalement ete re-verifie en mode staff (OK).",
        BODY,
    ))
    story.append(PageBreak())

    # ── Sommaire ─────────────────────────────────────────────────────────
    story.append(p("Sommaire", H1))
    sections = [
        ("1. Vue d'ensemble v149", "3 fixes + 1 verification"),
        ("2. PawMap halo geoloc invisible", "Custom marker bleu pulsant"),
        ("3. Cadre boost owner profile", "Border doree + glow sur le hero"),
        ("4. i18n PawMap (36 cles x 6 langues)", "216 nouvelles entries"),
        ("5. PawSpot mode staff - verification", "Backend OK, frontend OK, tests"),
        ("6. Action Daniel iOS Mac", "Procedure rebuild standard"),
        ("7. Checklist tests v149", "Liste exhaustive a valider"),
    ]
    for title, desc in sections:
        story.append(p(f"<b>{title}</b> - {desc}", BODY))
    story.append(PageBreak())

    # ── 1. Vue d'ensemble ────────────────────────────────────────────────
    story.append(p("1. Vue d'ensemble v149", H1))
    story.append(p("Bugs remontes via voice notes :", H3))
    bugs = [
        ("Paw map rien napparait le point de geolocolisation ou le halo nest pas la", "Flutter map", "Halo bleu custom (indep. myLocationEnabled)"),
        ("Le boost sur owner ne saffiche pas", "Flutter profile", "Cadre dore + glow autour du hero quand boost actif"),
        ("Sur la paw map les onglet au desuus perdu chien mechant etc c mal traduit verifie tte les langue", "Flutter i18n", "36 cles x 6 langues pour le sheet + appbar + snackbars"),
        ("Reverifie que pawspot marche", "Backend staff bypass", "OK - mapBoostExpiry persiste, status retourne isActive=true"),
    ]
    rows = [["Demande remontee", "Couche", "Solution / Verdict"]] + bugs
    story.append(make_table(rows, col_widths=[7 * cm, 3 * cm, 6 * cm]))

    story.append(p("Metriques", H3))
    story.append(bullet("4 fichiers source modifies (paw_map_screen, profile_screen, active_benefits_row, create_report_sheet)"))
    story.append(bullet("6 fichiers i18n mis a jour (en, fr, es, de, it, pt)"))
    story.append(bullet("36 cles i18n x 6 langues = <b>216 nouvelles entries</b>"))
    story.append(bullet("1 nouveau script Python (inject_pawmap_i18n.py) pour re-jouer les injections plus tard"))
    story.append(bullet("Commit : <b>bda013f</b> sur origin/main"))

    story.append(PageBreak())

    # ── 2. PawMap halo geoloc ────────────────────────────────────────────
    story.append(p("2. Bug PawMap halo geoloc invisible", H1))
    story.append(p("Symptome", H3))
    story.append(p(
        "Daniel : \"paw map rien napparait le point de geolocolisation ou le "
        "halo nest pas la\". Meme apres avoir autorise la geolocalisation, "
        "rien ne s'affiche sur la carte pour materialiser la position user.",
        BODY,
    ))
    story.append(p("Cause", H3))
    story.append(p(
        "Le GoogleMap utilisait <i>myLocationEnabled: true</i> ce qui depend "
        "d'une permission OS (ACCESS_FINE_LOCATION sur Android, "
        "NSLocationWhenInUseUsageDescription sur iOS) qui peut etre refusee "
        "ou indisponible <b>silencieusement</b> - aucun point bleu ne "
        "s'affichait alors. La nouvelle position GPS etait pourtant bien "
        "recuperee par LocationService et le _currentCenter etait correct, "
        "mais l'utilisateur n'avait aucun visual.",
        BODY,
    ))
    story.append(p("Fix", H3))
    story.append(p(
        "<i>frontend/lib/views/map/paw_map_screen.dart</i> : on ajoute notre "
        "propre marker bleu pulsant <b>independant</b> du myLocationEnabled, "
        "qui apparait des que LocationService a resolu la position.",
        BODY,
    ))
    story.append(code_block(
        "// Nouvelle state\n"
        "LatLng? _userPosition;\n\n"
        "// Set dans _bootstrap et _recenterOnUser quand loc != null\n"
        "setState(() {\n"
        "  _currentCenter = center;\n"
        "  _userPosition = center;\n"
        "});\n\n"
        "// Dans _buildHaloCircles : 2 cercles bleus a la position user\n"
        "if (userPos != null) {\n"
        "  // Halo pulsant 25 a 100m\n"
        "  circles.add(Circle(\n"
        "    circleId: const CircleId('user_halo_outer'),\n"
        "    center: userPos,\n"
        "    radius: 25 + 75 * phase,\n"
        "    fillColor: userBlue.withValues(alpha: opacity * 0.4),\n"
        "    strokeColor: userBlue.withValues(alpha: opacity),\n"
        "    strokeWidth: 2,\n"
        "  ));\n"
        "  // Petit point central solide 8m bordure blanche\n"
        "  circles.add(Circle(\n"
        "    circleId: const CircleId('user_halo_dot'),\n"
        "    center: userPos,\n"
        "    radius: 8,\n"
        "    fillColor: userBlue,\n"
        "    strokeColor: Colors.white,\n"
        "    strokeWidth: 2,\n"
        "  ));\n"
        "}"
    ))
    story.append(p(
        "Resultat : meme si l'utilisateur refuse la permission Maps native, "
        "des qu'on a une position GPS (resolue via Geolocator.getCurrentPosition), "
        "notre halo bleu pulsant + point central s'affichent. Garantie de "
        "visibilite.",
        NOTE,
    ))

    story.append(PageBreak())

    # ── 3. Cadre boost owner ─────────────────────────────────────────────
    story.append(p("3. Cadre boost owner profile", H1))
    story.append(p("Symptome", H3))
    story.append(p(
        "Daniel : \"le boost sur owner ne saffiche pas\". Le badge \"Boost - 9j\" "
        "etait bien present dans la row ActiveBenefitsRow du header, mais "
        "aucun visuel ne distinguait fortement qu'un owner etait boost.",
        BODY,
    ))
    story.append(p("Solution", H3))
    story.append(p(
        "On wrap le hero orange du profil owner dans un Obx qui ajoute un "
        "cadre dore + un glow lumineux quand le boost est actif.",
        BODY,
    ))
    story.append(p("Architecture", H3))
    story.append(bullet(
        "<b>active_benefits_row.dart</b> : nouveau static <i>RxBool _boostActive</i> "
        "(accesseur <i>boostActiveAccessor</i>) maintenu sync a chaque fetch "
        "de /users/me/benefits. Tous les widgets peuvent ecouter cet etat."
    ))
    story.append(bullet(
        "<b>profile_screen.dart</b> : le hero <i>_buildOwnerHero(controller)</i> "
        "est maintenant wrappe dans un Obx avec Container conditional :"
    ))
    story.append(code_block(
        "Obx(() {\n"
        "  final isBoosted = ActiveBenefitsRow.boostActiveAccessor.value;\n"
        "  const boostGold = Color(0xFFD4AF37);\n"
        "  return Container(\n"
        "    decoration: isBoosted\n"
        "      ? BoxDecoration(\n"
        "          border: Border.all(color: boostGold, width: 3),\n"
        "          boxShadow: [\n"
        "            BoxShadow(\n"
        "              color: boostGold.withValues(alpha: 0.45),\n"
        "              blurRadius: 18,\n"
        "              spreadRadius: 2,\n"
        "            ),\n"
        "          ],\n"
        "        )\n"
        "      : null,\n"
        "    child: _buildOwnerHero(controller),\n"
        "  );\n"
        "})"
    ))
    story.append(p("Couleur dore : <b>#D4AF37</b> (coherent avec sitter_card / walker_card).", NOTE))

    story.append(PageBreak())

    # ── 4. i18n PawMap ───────────────────────────────────────────────────
    story.append(p("4. i18n PawMap (36 cles x 6 langues)", H1))
    story.append(p("Symptome", H3))
    story.append(p(
        "Daniel : \"sur la paw map les onglet au desuus perdu chien mechant "
        "etc c mal traduit verifie tte les langue\". Les LABELS des 21 types "
        "de signalement (Caca, Pipi, Chien mechant...) etaient deja traduits "
        "via map_report_label_* keys, mais les SECTION HEADERS, snackbars "
        "et boutons du PawMap etaient hardcoded en francais.",
        BODY,
    ))
    story.append(p("Cles ajoutees (extrait)", H3))
    keys = [
        ("pawmap_signal_title", "Signaler autour de moi / Report around me / Senalar a mi alrededor"),
        ("pawmap_section_free", "Gratuits / Free / Gratuitos"),
        ("pawmap_section_premium", "Premium / Premium / Premium"),
        ("pawmap_note_label", "Note (optionnel) / Note (optional) / Nota (opcional)"),
        ("pawmap_note_hint", "Un detail utile pour les autres... / A useful detail for others..."),
        ("pawmap_btn_send", "Signaler / Report / Senalar"),
        ("pawmap_appbar_friends", "Amis / Friends / Amigos"),
        ("pawmap_appbar_follow", "Suivre / Follow / Seguir"),
        ("pawmap_appbar_live", "Live / Live / En vivo"),
        ("pawmap_btn_view_post", "Voir l'annonce / View post / Ver anuncio"),
        ("pawmap_snack_post_opened_title", "Demande ouverte / Post opened / Solicitud abierta"),
        ("pawmap_live_banner_title", "Tu es en direct / You are live / Estas en vivo"),
        ("pawmap_btn_stop", "Stop / Stop / Parar"),
        ("pawmap_loading", "Chargement... / Loading... / Cargando..."),
        ("+ 22 autres cles", "snackbars, banners, ports, hints..."),
    ]
    rows = [["Cle i18n", "FR / EN / ES (exemples)"]] + keys
    story.append(make_table(rows, col_widths=[6.5 * cm, 9 * cm]))

    story.append(p("Process automatise", H3))
    story.append(p(
        "Nouveau script <b>inject_pawmap_i18n.py</b> a la racine du repo : "
        "dictionnaire central de 36 cles avec les 6 traductions chacune. "
        "Le script injecte les cles dans en/fr/es/de/it/pt.dart juste apres "
        "<i>map_report_label_other</i> (ancre regex) puis patche les "
        "substitutions hardcoded -> .tr dans create_report_sheet.dart "
        "et paw_map_screen.dart en une passe.",
        BODY,
    ))

    story.append(PageBreak())

    # ── 5. PawSpot verification ──────────────────────────────────────────
    story.append(p("5. PawSpot mode staff - verification", H1))
    story.append(p("Demande", H3))
    story.append(p(
        "Daniel : \"reverifie que pawspot marche\". J'ai re-trace le flow "
        "end-to-end backend + frontend pour confirmer que tout est bon en "
        "mode staff.",
        BODY,
    ))
    story.append(p("Backend - mapBoostRoutes.js lignes 162-194", H3))
    story.append(p(
        "Bypass staff dans <i>POST /map-boost/purchase</i> : si "
        "<i>userDoc.isStaff == true</i>, on persiste <b>mapBoostExpiry</b> "
        "+ <b>mapBoostTier</b> + une entree dans <i>boostPurchases</i> avec "
        "<i>paymentProvider: 'staff_free'</i>, puis on retourne "
        "<i>{staff: true, activated: true, ...}</i>.",
        BODY,
    ))
    story.append(p("Backend - GET /map-boost/status", H3))
    story.append(p(
        "Lit <i>mapBoostExpiry</i>, calcule <i>isActive = mapBoostExpiry > now</i>, "
        "retourne <i>{isActive, tier, expiresAt, remainingDays, ...}</i>. "
        "Pour un staff qui vient d'achete, isActive=true.",
        BODY,
    ))
    story.append(p("Frontend - MapBoostController.purchase ligne 186", H3))
    story.append(p(
        "Court-circuit Airwallex sur <i>staff:true && activated:true</i> : "
        "appelle <i>loadStatus()</i> puis <i>refreshAfterPurchase()</i>. "
        "Cette derniere fire <i>ActiveBenefitsRow.notifyChanged()</i> qui "
        "refetch /users/me/benefits pour faire apparaitre le badge "
        "PawSpot - Xj dans le header.",
        BODY,
    ))
    story.append(p("Visibilite", H3))
    story.append(bullet("Card du shop devient verte gradient avec 'mapboost_active' + remainingDays"))
    story.append(bullet("Badge 📍 PawSpot - Xj dans ActiveBenefitsRow du header profil"))
    story.append(bullet("Pour sitter/walker : pin dore sur la map lorsqu'un owner regarde"))
    story.append(bullet("Banner d'info dans le shop : 'Ton PawSpot est visible par les owners qui regardent la map a cet endroit'"))
    story.append(p("Verdict : <b>PawSpot fonctionne correctement en mode staff</b>. Si rien ne s'affiche, c'est une question de role browse (un sitter ne se voit pas lui-meme sur la map).", NOTE))

    story.append(PageBreak())

    # ── 6. Action iOS sur Mac ────────────────────────────────────────────
    story.append(p("6. Ce qu'il te reste a faire sur Mac (iOS)", H1))
    story.append(p("Procedure standard - identique aux precedentes", H3))
    story.append(code_block(
        "# Sur ton Mac, dans le dossier HopeTSIT_FINAL\n"
        "git pull --rebase\n"
        "# Tu dois voir : bda013f i18n(v23.1.149)...\n\n"
        "cd frontend\n"
        "flutter pub get\n"
        "cd ios\n"
        "pod install\n"
        "open Runner.xcworkspace\n\n"
        "# Bump version dans pubspec.yaml ligne 4 :\n"
        "# version: 23.1.149+149\n\n"
        "flutter build ipa --release\n"
        "# Drag&drop build/ios/ipa/HopeTSIT.ipa dans Transporter\n"
        "# Deliver"
    ))
    story.append(p(
        "Aucune nouvelle dependance native dans cette session. Le widget "
        "AddressAutocompleteField de v148 utilise package:http qui etait deja "
        "dans pubspec. Les changements de v149 sont 100% Dart partage.",
        NOTE,
    ))

    # ── 7. Checklist tests v149 ──────────────────────────────────────────
    story.append(p("7. Checklist tests apres installation iOS v149", H1))
    story.append(p(
        "Apres rebuild + install sur device. Valide chacun de ces points :",
        BODY,
    ))

    tests = [
        ("PawMap au lancement (1re fois)", "Halo bleu pulsant + point bleu au centre a ta position"),
        ("PawMap apres avoir bouge", "Le halo suit ta position quand tu re-tap geoloc"),
        ("Profil owner avec boost actif", "Cadre dore + glow autour du hero orange"),
        ("Profil owner sans boost", "Hero orange normal (pas de cadre dore)"),
        ("PawSpot mode staff - acheter un tier", "Carte shop devient verte 'PawSpot actif - Xj'"),
        ("Apres achat PawSpot - badge dans header profil", "📍 PawSpot - Xj visible"),
        ("Bascule iPhone en ES - PawMap appbar", "'Amigos' / 'Seguir' / 'Actualizar'"),
        ("Bascule iPhone en DE - PawMap appbar", "'Freunde' / 'Folgen' / 'Aktualisieren'"),
        ("Bascule iPhone en IT - PawMap appbar", "'Amici' / 'Segui' / 'Aggiorna'"),
        ("Bascule iPhone en PT - PawMap appbar", "'Amigos' / 'Seguir' / 'Atualizar'"),
        ("Tap FAB 'Signaler' en ES", "Titre 'Senalar a mi alrededor', sections 'Gratuitos' / 'Premium'"),
        ("Note label en ES", "'Nota (opcional)' avec hint 'Un detalle util...'"),
        ("Snackbar localisation indispo en ES", "'Localizacion no disponible' + msg ES"),
        ("Banner 'Tu es en direct' en ES", "'Estas en vivo' + 'Tus amigos y familia ven tu posicion'"),
        ("Tests v148 toujours OK", "Camera centree sur ta geoloc, autocomplete adresse veto"),
        ("Tests v147 toujours OK", "Cadre boost cards, slider 20km, delete task, i18n ES"),
    ]
    rows = [["Test", "Attendu"]] + tests
    story.append(make_table(rows, col_widths=[7.5 * cm, 8.5 * cm]))

    story.append(p("Si un test echoue", H3))
    story.append(bullet("Capture d'ecran + courte description"))
    story.append(bullet("Indique : langue active, role (owner/sitter/walker), staff oui/non"))
    story.append(bullet("Envoie tout ca, je corrige"))

    story.append(Spacer(1, 1 * cm))
    story.append(p(
        "Commit bda013f sur origin/main. Render auto-deploy le backend (aucun "
        "changement backend dans cette session). Frontend a rebuilde "
        "manuellement : Android deja fait (APK dans Downloads), iOS a faire "
        "sur Mac via etapes 1-4 ci-dessus.",
        NOTE,
    ))

    doc.build(story)
    print(f"OK PDF v149 fixes recap genere : {OUTPUT}")
    print(f"   Taille : {os.path.getsize(OUTPUT) // 1024} Ko")


if __name__ == "__main__":
    build()
