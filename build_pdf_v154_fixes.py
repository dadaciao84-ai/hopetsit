"""
HopeTSIT - Recap des fixes v23.1.154 + guide build iOS sur Mac.

Sortie : ~/Downloads/HopeTSIT_v23.1.154_Fixes_iOS_Guide.pdf

Daniel : "les couleurs du halo pour pawspot marche pas, faite que lapli ne
se ferme que si on met manuelment deconnecter et faite que je puis
enregistrer mon pdf facture ds fichier du tel".

3 demandes resolues en une session :
  1. PawSpot halo - couleurs + self-halo
  2. App ne se ferme PLUS automatiquement (session expiree = snackbar
     discret, pas de logout force)
  3. Bouton "Enregistrer dans Fichiers" sur la page facture
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
    "HopeTSIT_v23.1.154_Fixes_iOS_Guide.pdf",
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
        title="HopeTSIT v23.1.154 - No auto-logout + PawSpot halo + Invoice save",
        author="HopeTSIT",
    )
    story = []

    # Page de titre
    story.append(Spacer(1, 3 * cm))
    story.append(p("HopeTSIT v23.1.154", TITLE))
    story.append(p("No auto-logout + PawSpot halo per tier + invoice save-to-files", SUBTITLE))
    story.append(p("+ Guide build iOS sur Mac", SUBTITLE))
    story.append(Spacer(1, 0.5 * cm))
    story.append(make_table([
        ["Version", "23.1.154"],
        ["Date", datetime.now().strftime("%d %B %Y")],
        ["Fixes", "3 (halo PawSpot / no auto-logout / invoice save button)"],
        ["i18n", "5 nouvelles cles x 6 langues = 30 entries"],
        ["Codebases touchees", "App Flutter (4 fichiers + 6 i18n)"],
    ], col_widths=[5 * cm, 9 * cm]))
    story.append(Spacer(1, 1.5 * cm))
    story.append(p(
        "Daniel : <i>\"les couleurs du halo pour pawspot marche pas, faite "
        "que lapli ne se ferme que si on met manuelment deconnecter et faite "
        "que je puis enregistrer mon pdf facture ds fichier du tel\"</i>",
        BODY,
    ))
    story.append(PageBreak())

    # Sommaire
    story.append(p("Sommaire", H1))
    sections = [
        ("1. Vue d'ensemble v154", "3 fixes prioritaires"),
        ("2. PawSpot halo - couleurs par tier + self-halo", "Bronze/Silver/Gold/Platinum + user voit le sien"),
        ("3. App ne se ferme PLUS automatiquement", "Snackbar discret au lieu de logout force"),
        ("4. Bouton 'Enregistrer dans Fichiers' sur facture", "AppBar IconButton explicit + tooltip"),
        ("5. Action Daniel iOS Mac", "Procedure rebuild standard"),
        ("6. Checklist tests v154", "Validation 3 fixes"),
    ]
    for title, desc in sections:
        story.append(p(f"<b>{title}</b> - {desc}", BODY))
    story.append(PageBreak())

    # 1. Vue d'ensemble
    story.append(p("1. Vue d'ensemble v154", H1))
    rows = [
        ["Demande Daniel", "Couche", "Solution"],
        ("Couleurs du halo PawSpot marche pas", "Flutter map", "Halo par tier (4 couleurs+tailles) + user voit son propre halo"),
        ("App ne se ferme que si manuel Deconnecter", "Flutter auth", "401/403 -> snackbar, JWT expire -> garde connecte"),
        ("Enregistrer PDF facture dans Fichiers tel", "Flutter invoices", "AppBar IconButton 'save_alt' + tooltip clair"),
    ]
    story.append(make_table(rows, col_widths=[7 * cm, 3 * cm, 6 * cm]))

    story.append(PageBreak())

    # 2. PawSpot halo
    story.append(p("2. PawSpot halo - couleurs par tier + self-halo", H1))
    story.append(p("Symptome", H3))
    story.append(p(
        "Daniel : les couleurs du halo PawSpot ne fonctionnent pas. Avant : "
        "seul Platinum avait un halo, en couleur or fixe. Les autres tiers "
        "n'avaient aucun halo et l'utilisateur ne voyait jamais son PROPRE "
        "halo (le code iterait <i>_nearbyProviders</i> qui exclut le user lui-meme).",
        BODY,
    ))
    story.append(p("Fix #1 - halos pour TOUS les tiers", H3))
    story.append(p(
        "Le code <i>_buildHaloCircles()</i> avait <i>if (mapTier != 'platinum') continue;</i> "
        "qui filtrait tous les non-Platinum. Maintenant les 4 tiers ont un "
        "halo distinct, avec couleur ET rayon specifiques :",
        BODY,
    ))
    rows = [
        ["Tier", "Couleur halo", "Rayon max", "Effet visuel"],
        ("bronze", "#B87333 (cuivre)", "40 m", "Halo discret, anneau cuivre"),
        ("silver", "#B0B0B0 (argent)", "80 m", "Halo gris argent moyen"),
        ("gold", "#FFD700 (jaune dore)", "120 m", "Halo dore brillant, evident"),
        ("platinum", "#FFAA00 (ambre)", "160 m", "Halo ambre intense, premium"),
    ]
    story.append(make_table(rows, col_widths=[2 * cm, 4 * cm, 2.5 * cm, 6 * cm]))

    story.append(p("Fix #2 - self-halo (user voit son propre PawSpot)", H3))
    story.append(p(
        "Nouveau bloc qui lit <i>MapBoostController.status</i> et dessine "
        "un halo a la position du user (<i>_userPosition</i>) s'il a un map_boost "
        "actif. Couleur = celle du tier de l'user. Resultat : l'utilisateur "
        "voit son propre halo PawSpot sur la carte des qu'il ouvre PawMap "
        "(avant : il ne voyait que les halos des autres providers).",
        BODY,
    ))
    story.append(code_block(
        "// Nouveau dans _buildHaloCircles - juste apres le halo bleu de geoloc\n"
        "final mapBoostCtl = Get.isRegistered<MapBoostController>()\n"
        "    ? Get.find<MapBoostController>() : null;\n"
        "final mapBoostStatus = mapBoostCtl?.status.value;\n"
        "final selfTier = mapBoostStatus?.tier?.toLowerCase();\n"
        "if (userPos != null && mapBoostStatus != null &&\n"
        "    mapBoostStatus.isActive && selfTier != null && selfTier.isNotEmpty) {\n"
        "  final selfColor = tierColor(selfTier);\n"
        "  final selfMax = tierMaxRadius(selfTier);\n"
        "  final selfRadius = 30.0 + (selfMax - 30.0) * phase;\n"
        "  circles.add(Circle(\n"
        "    circleId: const CircleId('self_pawspot_halo'),\n"
        "    center: userPos, radius: selfRadius,\n"
        "    fillColor: selfColor.withValues(alpha: opacity * 0.5),\n"
        "    strokeColor: selfColor.withValues(alpha: opacity),\n"
        "    strokeWidth: 2,\n"
        "  ));\n"
        "}"
    ))

    story.append(PageBreak())

    # 3. No auto-logout
    story.append(p("3. App ne se ferme PLUS automatiquement", H1))
    story.append(p("Symptome", H3))
    story.append(p(
        "Daniel : <i>\"faite que lapli ne se ferme que si on met manuelment "
        "deconnecter\"</i>. L'app revenait a l'ecran de login dans 2 cas :",
        BODY,
    ))
    story.append(bullet("1. Au lancement : si le JWT exp etait passe → splash_screen reroutait vers Onboarding"))
    story.append(bullet("2. En cours d'utilisation : tout 401/403 d'une API call → AuthController.handleLoginRequiredError() → logout()"))
    story.append(p("Fix #1 - splash_screen.dart - JWT expire = on garde connecte", H3))
    story.append(code_block(
        "// AVANT\n"
        "if (json is Map && json['exp'] is num) {\n"
        "  final expSec = (json['exp'] as num).toInt();\n"
        "  final nowSec = DateTime.now().millisecondsSinceEpoch ~/ 1000;\n"
        "  if (expSec <= nowSec) return null;  // -> Onboarding force\n"
        "}\n\n"
        "// APRES\n"
        "if (json is Map && json['exp'] is num) {\n"
        "  final expSec = (json['exp'] as num).toInt();\n"
        "  final nowSec = DateTime.now().millisecondsSinceEpoch ~/ 1000;\n"
        "  if (expSec <= nowSec) {\n"
        "    debugPrint('[HOPETSIT] JWT exp passed - keeping user logged in');\n"
        "    // pas de return null - on continue avec le role\n"
        "  }\n"
        "}"
    ))
    story.append(p("Fix #2 - auth_controller.dart - 401/403 = snackbar pas logout", H3))
    story.append(code_block(
        "// AVANT - tout 401/403 entrainait logout + redirect LoginScreen\n"
        "static Future<void> handleLoginRequiredError() async {\n"
        "  await authController.logout();\n"
        "  // ... redirection forcee vers LoginScreen\n"
        "}\n\n"
        "// APRES - juste un snackbar (one-shot par 30s)\n"
        "static bool _sessionExpiredSnackShown = false;\n"
        "static Future<void> handleLoginRequiredError() async {\n"
        "  if (_sessionExpiredSnackShown) return;\n"
        "  _sessionExpiredSnackShown = true;\n"
        "  CustomSnackbar.showWarning(\n"
        "    title: 'auth_session_expired_title'.tr,\n"
        "    message: 'auth_session_expired_msg'.tr,\n"
        "    // 'Session expiree' / 'Va dans Profil > Deconnecter et reconnecte-toi.'\n"
        "  );\n"
        "  Future.delayed(const Duration(seconds: 30), () {\n"
        "    _sessionExpiredSnackShown = false;\n"
        "  });\n"
        "  // PAS de logout - PAS de redirect\n"
        "}"
    ))
    story.append(p(
        "Comportement utilisateur : Daniel peut continuer a utiliser l'app "
        "meme apres expiration JWT. Les ecrans qui ont besoin de l'API "
        "afficheront leurs propres erreurs gracieusement. Pour effectivement "
        "se reconnecter, il doit aller dans Profil > Deconnecter (bouton "
        "explicite) puis se re-login. ZERO logout automatique.",
        OK,
    ))

    story.append(PageBreak())

    # 4. Invoice save
    story.append(p("4. Bouton 'Enregistrer dans Fichiers' sur facture", H1))
    story.append(p("Symptome", H3))
    story.append(p(
        "Daniel : <i>\"faite que je puis enregistrer mon pdf facture ds "
        "fichier du tel\"</i>. La fonction existait deja (<i>_triggerPrint()</i> "
        "genere un PDF + ouvre le share sheet avec option \"Save to Files\"), "
        "mais l'entree etait masquee : <i>actions: []</i> dans l'AppBar et "
        "les boutons HTML internes etaient peu visibles.",
        BODY,
    ))
    story.append(p("Fix", H3))
    story.append(p(
        "On reintroduit un <i>IconButton</i> dans l'AppBar avec une icone "
        "<i>Icons.save_alt</i> (universelle pour 'enregistrer/telecharger') "
        "et un tooltip clair <i>'Enregistrer dans Fichiers'</i> traduit en 6 "
        "langues. Tap → ouvre le share sheet → user choisit 'Save to Files' "
        "(iOS) ou 'Save to Downloads' (Android).",
        BODY,
    ))
    story.append(code_block(
        "// invoice_viewer_screen.dart - AppBar.actions\n"
        "actions: [\n"
        "  IconButton(\n"
        "    tooltip: 'invoice_save_to_files'.tr,\n"
        "    icon: const Icon(Icons.save_alt, color: Colors.white),\n"
        "    onPressed: _saveToFiles,  // appelle _triggerPrint()\n"
        "  ),\n"
        "],"
    ))
    story.append(p("Traductions du tooltip", H3))
    rows = [
        ["FR", "Enregistrer dans Fichiers"],
        ["EN", "Save to Files"],
        ["ES", "Guardar en Archivos"],
        ["DE", "In Dateien speichern"],
        ["IT", "Salva su File"],
        ["PT", "Guardar em Ficheiros"],
    ]
    story.append(make_table(rows, col_widths=[2 * cm, 8 * cm]))

    story.append(PageBreak())

    # 5. Action iOS
    story.append(p("5. Action Daniel iOS Mac", H1))
    story.append(code_block(
        "# Sur ton Mac\n"
        "git pull --rebase  # -> commit v23.1.154\n"
        "cd frontend && flutter pub get\n"
        "cd ios && pod install\n"
        "open Runner.xcworkspace\n\n"
        "# Bump pubspec.yaml : version: 23.1.154+154\n"
        "flutter build ipa --release\n"
        "# Drag&drop .ipa dans Transporter"
    ))
    story.append(p("Aucune dependance native ajoutee.", NOTE))

    # 6. Checklist
    story.append(p("6. Checklist tests v154", H1))
    tests = [
        ("Owner achete PawSpot Bronze (24h)", "Pin rouge-cuivre (15 hue) + halo cuivre 40m visible"),
        ("Owner achete PawSpot Silver (7j)", "Pin bleu-gris (195 hue) + halo argent 80m"),
        ("Owner achete PawSpot Gold (15j)", "Pin dore (45 hue) + halo dore brillant 120m"),
        ("Owner achete PawSpot Platinum (30j)", "Pin orange + halo ambre 160m pulsant"),
        ("User voit son PROPRE halo sur PawMap", "Halo PawSpot apparait a sa position (sa couleur de tier)"),
        ("App ouverte apres 12h (JWT typiquement expire)", "Pas de logout, on reste sur le home"),
        ("Naviguer dans l'app, appel API echoue (401)", "Snackbar 'Session expiree - va dans Profil>Deconnecter'"),
        ("Re-faire un appel API apres le snackbar", "Pas de nouveau snackbar (one-shot 30s) - 30s plus tard reactif"),
        ("Profil > Deconnecter (manuel)", "Vrai logout - retour a Login - WAI"),
        ("Tap une facture dans Mes paiements", "Page InvoiceViewer avec WebView + AppBar"),
        ("Tap icone save_alt en haut a droite", "Share sheet ouvert -> options 'Save to Files' visible"),
        ("iOS - Save to Files", "PDF visible dans Files app dossier 'HoPetSit'"),
        ("Android - Save to Downloads", "PDF dans Downloads/HoPetSit-*.pdf"),
        ("Bascule en ES - tooltip", "'Guardar en Archivos'"),
        ("Bascule en DE - snackbar session", "'Sitzung abgelaufen' + 'Profil > Abmelden'"),
        ("Tests v153 toujours OK", "Tarifs walker 90/120min + bouton demande directe + PawFollow plans"),
    ]
    rows = [["Test", "Attendu"]] + tests
    story.append(make_table(rows, col_widths=[7.5 * cm, 8 * cm]))

    story.append(Spacer(1, 1 * cm))
    story.append(p(
        "Cette v154 cloture les 3 demandes Daniel. L'app se comporte "
        "maintenant comme une vraie app native : on ne ferme JAMAIS la "
        "session sans action explicite de l'utilisateur, le halo PawSpot "
        "est visible pour les 4 tiers + soi-meme, et le PDF facture peut "
        "etre enregistre dans Fichiers iOS / Downloads Android via un "
        "bouton dedie.",
        NOTE,
    ))

    doc.build(story)
    print(f"OK PDF v154 fixes recap genere : {OUTPUT}")
    print(f"   Taille : {os.path.getsize(OUTPUT) // 1024} Ko")


if __name__ == "__main__":
    build()
