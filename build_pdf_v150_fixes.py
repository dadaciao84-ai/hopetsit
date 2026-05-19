"""
HopeTSIT - Recap des fixes v23.1.150 + guide build iOS sur Mac.

Sortie : ~/Downloads/HopeTSIT_v23.1.150_Fixes_iOS_Guide.pdf

Daniel : "que tout les option du halo dans pawspot fonctionne reverifie par
option". Cette session :
  - Verification par tier PawSpot (bronze/silver/gold/platinum) - tous OK
  - 22 nouvelles cles i18n pour le flux PawSpot/MapBoost (descriptions tiers,
    confirm dialog, tooltips markers, snackbars) - 132 entries
  - PDF iOS a jour avec la verification tier par tier
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
    "HopeTSIT_v23.1.150_Fixes_iOS_Guide.pdf",
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
VIOLET = HexColor("#8B5CF6")
YELLOW = HexColor("#FFD600")

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
        title="HopeTSIT v23.1.150 - Addendum PawSpot tier verification + iOS guide",
        author="HopeTSIT",
    )
    story = []

    # ── Page de titre ────────────────────────────────────────────────────
    story.append(Spacer(1, 3 * cm))
    story.append(p("HopeTSIT v23.1.150", TITLE))
    story.append(p("Verification PawSpot tier par tier + i18n", SUBTITLE))
    story.append(p("+ Guide build iOS sur Mac", SUBTITLE))
    story.append(Spacer(1, 0.5 * cm))
    story.append(make_table([
        ["Version", "23.1.150"],
        ["Date", datetime.now().strftime("%d %B %Y")],
        ["Demande", "Verifier que toutes les options PawSpot fonctionnent"],
        ["Verdict", "4/4 tiers fonctionnent + 22 cles i18n ajoutees"],
        ["Codebases touchees", "App Flutter (2 fichiers + 6 i18n)"],
        ["Cible app", "Android (rebuilde v150) + iOS (a rebuilder sur Mac)"],
    ], col_widths=[5 * cm, 9 * cm]))
    story.append(Spacer(1, 1.5 * cm))
    story.append(p(
        "Daniel : <i>\"que tout les option du halo dans pawspot fonctionne "
        "reverifie par option\"</i>. J'ai trace chaque tier PawSpot du backend "
        "jusqu'au visuel sur la map. <b>Les 4 tiers fonctionnent</b>. En bonus "
        "j'ai aussi traduit dans 6 langues toutes les strings hardcoded du "
        "flux d'achat (descriptions, confirm dialog, tooltips markers, "
        "snackbars).",
        BODY,
    ))
    story.append(PageBreak())

    # ── Sommaire ─────────────────────────────────────────────────────────
    story.append(p("Sommaire", H1))
    sections = [
        ("1. Vue d'ensemble v150", "Verification PawSpot + i18n"),
        ("2. PawSpot Bronze (24h)", "Pin bleu azure - OK"),
        ("3. PawSpot Silver (7j)", "Pin violet - OK"),
        ("4. PawSpot Gold (15j)", "Pin jaune - OK"),
        ("5. PawSpot Platinum (30j)", "Pin orange + halo anime - OK"),
        ("6. Halo platinum - mecanique", "Cycle 0->1 toutes les 2.4s, 5fps"),
        ("7. i18n PawSpot (22 cles x 6 langues)", "132 nouvelles entries"),
        ("8. Action Daniel iOS Mac", "Procedure rebuild standard"),
        ("9. Checklist tests v150", "Test chaque tier en mode staff"),
    ]
    for title, desc in sections:
        story.append(p(f"<b>{title}</b> - {desc}", BODY))
    story.append(PageBreak())

    # ── 1. Vue d'ensemble ────────────────────────────────────────────────
    story.append(p("1. Vue d'ensemble v150", H1))
    story.append(p("Tableau de correspondance backend - frontend - visuel", H3))
    tiers = [
        ("bronze",   "1 jour (24h)", "1.99 EUR",  "Visible (24h)",       "Bleu azure"),
        ("silver",   "7 jours",      "8.99 EUR",  "Pin surligne (7j)",   "Violet"),
        ("gold",     "15 jours",     "14.99 EUR", "Pin dore (15j)",      "Jaune"),
        ("platinum", "30 jours",     "24.99 EUR", "Pin dore + halo (30j)", "Orange + halo pulsant"),
    ]
    rows = [["Tier", "Duree backend", "Prix EUR", "Label affiche", "Pin map"]] + tiers
    story.append(make_table(rows, col_widths=[2.5 * cm, 3 * cm, 2.5 * cm, 4 * cm, 4 * cm]))

    story.append(p("Source de verite backend", H3))
    story.append(bullet("<b>mapBoostRoutes.js:37-41</b> definit MAP_BOOST_PACKAGES avec days par tier"))
    story.append(bullet("<b>mapBoostRoutes.js:47-52</b> definit MAP_BOOST_PRICING avec amount par currency"))
    story.append(bullet("Staff bypass lignes 162-194 persiste mapBoostExpiry + mapBoostTier en DB"))

    story.append(p("Frontend visuel par tier", H3))
    story.append(bullet("<b>paw_map_screen.dart _buildMarkers</b> ligne 586-601 : hue different par tier"))
    story.append(bullet("<b>paw_map_screen.dart _buildHaloCircles</b> ligne 528-532 : halo SEULEMENT pour platinum"))
    story.append(bullet("<b>coin_shop_screen.dart _mapBoostTierLabel/Description</b> : labels + descriptions traduits"))

    story.append(PageBreak())

    # ── 2. Bronze ────────────────────────────────────────────────────────
    story.append(p("2. PawSpot Bronze (24h / 1.99 EUR)", H1))
    story.append(p("Backend", H3))
    story.append(code_block(
        "bronze: { days: 1, label: '24h' }\n"
        "EUR: { bronze: 1.99 }"
    ))
    story.append(p("Frontend marker", H3))
    story.append(code_block(
        "case 'bronze':\n"
        "default:\n"
        "  hue = BitmapDescriptor.hueAzure; // bleu"
    ))
    story.append(p("Frontend InfoWindow tooltip", H3))
    story.append(p("<b>FR :</b> 'Visible (24h)' / <b>EN :</b> 'Visible (24h)' / <b>ES :</b> 'Visible (24h)' / <b>DE :</b> 'Sichtbar (24 Std.)' / <b>IT :</b> 'Visibile (24h)' / <b>PT :</b> 'Visível (24h)'", NOTE))
    story.append(p("Description shop card", H3))
    story.append(p("<b>FR :</b> 'Testez la visibilité carte' / <b>EN :</b> 'Try map visibility' / <b>ES :</b> 'Prueba la visibilidad en el mapa' / <b>DE :</b> 'Karten-Sichtbarkeit testen' / <b>IT :</b> 'Prova la visibilità sulla mappa' / <b>PT :</b> 'Experimenta a visibilidade no mapa'", NOTE))
    story.append(p("Status : OK - aucun halo (par design), pin bleu visible sur la map.", OK))

    # ── 3. Silver ────────────────────────────────────────────────────────
    story.append(p("3. PawSpot Silver (7 jours / 8.99 EUR)", H1))
    story.append(p("Backend", H3))
    story.append(code_block(
        "silver: { days: 7, label: '1 week' }\n"
        "EUR: { silver: 8.99 }"
    ))
    story.append(p("Frontend marker", H3))
    story.append(code_block(
        "case 'silver':\n"
        "  hue = BitmapDescriptor.hueViolet; // violet"
    ))
    story.append(p("Frontend InfoWindow tooltip", H3))
    story.append(p("<b>FR :</b> 'Pin surligné (7j)' / <b>EN :</b> 'Highlighted pin (7d)' / <b>ES :</b> 'Pin destacado (7d)' / <b>DE :</b> 'Hervorgehobener Pin (7 T.)' / <b>IT :</b> 'Pin evidenziato (7g)' / <b>PT :</b> 'Pin destacado (7d)'", NOTE))
    story.append(p("Status : OK - aucun halo (par design), pin violet visible sur la map.", OK))

    story.append(PageBreak())

    # ── 4. Gold ──────────────────────────────────────────────────────────
    story.append(p("4. PawSpot Gold (15 jours / 14.99 EUR)", H1))
    story.append(p("Backend", H3))
    story.append(code_block(
        "gold: { days: 15, label: '2 weeks' }\n"
        "EUR: { gold: 14.99 }"
    ))
    story.append(p("Frontend marker", H3))
    story.append(code_block(
        "case 'gold':\n"
        "  hue = BitmapDescriptor.hueYellow; // jaune"
    ))
    story.append(p("Frontend InfoWindow tooltip", H3))
    story.append(p("<b>FR :</b> 'Pin doré (15j)' / <b>EN :</b> 'Golden pin (15d)' / <b>ES :</b> 'Pin dorado (15d)' / <b>DE :</b> 'Goldener Pin (15 T.)' / <b>IT :</b> 'Pin dorato (15g)' / <b>PT :</b> 'Pin dourado (15d)'", NOTE))
    story.append(p("Description shop card", H3))
    story.append(p("<b>FR :</b> 'Pin doré, top des résultats carte'", NOTE))
    story.append(p("Badge popularite : Gold est marque <i>isPopular = true</i> donc card avec bordure dore + glow.", NOTE))
    story.append(p("Status : OK - aucun halo (par design), pin jaune + carte mise en avant.", OK))

    # ── 5. Platinum ──────────────────────────────────────────────────────
    story.append(p("5. PawSpot Platinum (30 jours / 24.99 EUR)", H1))
    story.append(p("Backend", H3))
    story.append(code_block(
        "platinum: { days: 30, label: '1 month' }\n"
        "EUR: { platinum: 24.99 }"
    ))
    story.append(p("Frontend marker + halo", H3))
    story.append(code_block(
        "// Marker hue\n"
        "case 'platinum':\n"
        "  hue = BitmapDescriptor.hueOrange;\n"
        "  break;\n\n"
        "// Halo dans _buildHaloCircles\n"
        "if (mapTier != 'platinum') continue;\n"
        "final phase = _haloPhase.value; // 0..1\n"
        "final radius = 30.0 + 130.0 * phase; // 30 -> 160 m\n"
        "final opacity = (0.45 * (1.0 - phase)).clamp(0.0, 1.0);\n"
        "final fill = const Color(0xFFFFAA00).withValues(alpha: opacity * 0.55);\n"
        "circles.add(Circle(\n"
        "  circleId: CircleId('halo_$id'),\n"
        "  center: LatLng(lat, lng),\n"
        "  radius: radius,\n"
        "  fillColor: fill,\n"
        "  strokeColor: stroke,\n"
        "  strokeWidth: 2,\n"
        "));"
    ))
    story.append(p("Frontend InfoWindow tooltip", H3))
    story.append(p("<b>FR :</b> 'Pin doré + halo (30j)' / <b>EN :</b> 'Golden pin + halo (30d)' / <b>ES :</b> 'Pin dorado + halo (30d)' / <b>DE :</b> 'Goldener Pin + Halo (30 T.)' / <b>IT :</b> 'Pin dorato + alone (30g)' / <b>PT :</b> 'Pin dourado + halo (30d)'", NOTE))
    story.append(p("Status : OK - halo orange pulsant 30m a 160m visible autour du pin platinum.", OK))

    story.append(PageBreak())

    # ── 6. Halo mecanique ────────────────────────────────────────────────
    story.append(p("6. Halo Platinum - mecanique de l'animation", H1))
    story.append(p("Timer de phase", H3))
    story.append(p(
        "Au mount de PawMap, on lance un Timer.periodic de 200ms qui "
        "incremente _haloPhase de 1/12 (= 12 ticks). En 200ms x 12 = 2.4s, "
        "_haloPhase fait un cycle complet 0 -> 1 -> 0. Resultat : 5 fps "
        "(0.2 update/sec), assez fluide pour un effet de pulsation paisible "
        "sans surcharger le GPU.",
        BODY,
    ))
    story.append(code_block(
        "_haloTimer = Timer.periodic(const Duration(milliseconds: 200), (_) {\n"
        "  if (!mounted) return;\n"
        "  _haloPhase.value = (_haloPhase.value + 1.0 / 12.0) % 1.0;\n"
        "});"
    ))
    story.append(p("Animation du cercle", H3))
    story.append(bullet("Radius : <b>30m -> 160m</b> (grandit)"))
    story.append(bullet("Opacity : <b>0.45 -> 0</b> (s'estompe en grandissant)"))
    story.append(bullet("Fill : Color(0xFFFFAA00) * opacity * 0.55 - dore chaud"))
    story.append(bullet("Stroke : Color(0xFFFFAA00) * opacity - meme couleur, opacite plus haute"))
    story.append(bullet("Au moment ou le cercle atteint 160m (presque transparent), il revient brutalement a 30m (cycle re-debute)"))

    story.append(p("Visibilite seulement pour les OWNERS qui regardent la map", H3))
    story.append(p(
        "Le halo n'apparait pas si <i>_isSitterOrWalker == true</i>. C'est "
        "voulu : un sitter ne se voit pas lui-meme sur la map. Seul un owner "
        "qui browse la map a la position du Platinum-boosted voit le halo.",
        BODY,
    ))

    story.append(PageBreak())

    # ── 7. i18n PawSpot ──────────────────────────────────────────────────
    story.append(p("7. i18n PawSpot (22 cles x 6 langues)", H1))
    story.append(p("Strings hardcoded trouvees", H3))
    keys = [
        ("mapboost_desc_bronze", "Testez la visibilité carte / Try map visibility..."),
        ("mapboost_desc_silver", "Pin surligné, portée moyenne / Highlighted pin..."),
        ("mapboost_desc_gold", "Pin doré, top des résultats carte / Golden pin..."),
        ("mapboost_desc_platinum", "Pin doré + halo animé permanent / Golden pin + halo..."),
        ("mapboost_days_count", "@count jour(s) / @count day(s)"),
        ("mapboost_confirm_title", "Acheter PawSpot @tier ? / Buy PawSpot @tier?"),
        ("mapboost_confirm_tier_label", "Tier / Tier / Nivel / Stufe..."),
        ("mapboost_confirm_duration_label", "Durée / Duration / Duración..."),
        ("mapboost_confirm_price_label", "Prix / Price / Precio..."),
        ("mapboost_confirm_description", "Ton PawSpot sera mis en avant..."),
        ("common_confirm", "Confirmer / Confirm / Confirmar..."),
        ("common_service_unavailable", "Service indisponible / Service unavailable..."),
        ("mapboost_location_updated", "PawSpot mis à jour : @label / PawSpot updated: @label..."),
        ("premium_activated_title", "Premium activé ! / Premium activated!..."),
        ("premium_activated_msg", "Profitez de toutes les fonctionnalités."),
        ("mapboost_marker_bronze/silver/gold/platinum", "Tooltips InfoWindow par tier"),
        ("mapboost_marker_active", "PawSpot actif (fallback)"),
        ("mapboost_marker_profile_boosted", "Profil boosté"),
        ("mapboost_info_visibility", "Ton PawSpot est visible par les owners..."),
    ]
    rows = [["Cle i18n", "Exemples de valeurs"]] + keys
    story.append(make_table(rows, col_widths=[6.5 * cm, 9 * cm]))

    story.append(p("Process automatise", H3))
    story.append(p(
        "Nouveau script <b>inject_pawspot_i18n.py</b> a la racine du repo : "
        "dictionnaire central de 22 cles avec les 6 traductions chacune. "
        "Le script injecte les cles dans en/fr/es/de/it/pt.dart juste apres "
        "<i>pawmap_confirmations</i> (ancre regex, fallback "
        "<i>map_report_label_other</i>) puis patche 11 substitutions "
        "hardcoded -> .tr dans coin_shop_screen.dart et 1 dans "
        "paw_map_screen.dart en une passe.",
        BODY,
    ))

    story.append(PageBreak())

    # ── 8. Action iOS sur Mac ────────────────────────────────────────────
    story.append(p("8. Ce qu'il te reste a faire sur Mac (iOS)", H1))
    story.append(p("Procedure standard - identique aux precedentes", H3))
    story.append(code_block(
        "# Sur ton Mac, dans le dossier HopeTSIT_FINAL\n"
        "git pull --rebase\n"
        "# Tu dois voir le commit v23.1.150 PawSpot i18n\n\n"
        "cd frontend\n"
        "flutter pub get\n"
        "cd ios\n"
        "pod install\n"
        "open Runner.xcworkspace\n\n"
        "# Bump version dans pubspec.yaml ligne 4 :\n"
        "# version: 23.1.150+150\n\n"
        "flutter build ipa --release\n"
        "# Drag&drop build/ios/ipa/HopeTSIT.ipa dans Transporter -> Deliver"
    ))
    story.append(p(
        "Aucune nouvelle dependance native. Tout est du Dart partage "
        "Android/iOS. Le rebuilt iOS doit juste re-emballer les nouveaux "
        ".tr keys dans le bundle.",
        NOTE,
    ))

    # ── 9. Checklist tests v150 ──────────────────────────────────────────
    story.append(p("9. Checklist tests apres installation iOS v150", H1))
    story.append(p(
        "En mode staff, achete chaque tier dans l'ordre et valide :",
        BODY,
    ))

    tests = [
        ("Bronze - shop card", "Description 'Testez la visibilité carte' (ou ES/DE/IT/PT)"),
        ("Bronze - confirm dialog", "Titre 'Acheter PawSpot BRONZE ?', boutons Annuler/Confirmer traduits"),
        ("Bronze - snackbar succes", "Toast 'common_success' + 'map_boost_purchase_success'"),
        ("Bronze - badge profil", "📍 PawSpot - 1j visible dans ActiveBenefitsRow"),
        ("Bronze - regarder en mode Owner sur la map", "Pin BLEU AZURE a la position PawSpot"),
        ("Silver - shop card", "Description 'Pin surligné, portée moyenne' (et traductions)"),
        ("Silver - badge profil", "📍 PawSpot - 8j (1 + 7 cumule)"),
        ("Silver - map mode Owner", "Pin VIOLET"),
        ("Gold - shop card", "Description + badge 'Top map' (gold = isPopular)"),
        ("Gold - badge profil", "📍 PawSpot - 23j (1 + 7 + 15 cumule)"),
        ("Gold - map mode Owner", "Pin JAUNE"),
        ("Platinum - shop card", "Description 'Pin doré + halo animé permanent'"),
        ("Platinum - badge profil", "📍 PawSpot - 53j (1 + 7 + 15 + 30 cumule)"),
        ("Platinum - map mode Owner", "Pin ORANGE + HALO PULSANT autour"),
        ("Halo - rythme", "1 pulsation toutes les 2.4 sec, paisible"),
        ("Bascule iPhone en ES - shop tiers", "Descriptions en espagnol"),
        ("Bascule en DE/IT/PT - confirm dialog", "Tier/Duree/Prix traduits"),
        ("Tests v149 toujours OK", "Halo geoloc bleu, cadre owner boost, i18n PawMap"),
    ]
    rows = [["Test", "Attendu"]] + tests
    story.append(make_table(rows, col_widths=[6.5 * cm, 9.5 * cm]))

    story.append(p("Important - visibilite du halo", H3))
    story.append(p(
        "Tu ne peux PAS voir ton propre halo Platinum en mode sitter/walker "
        "(par design, le halo s'affiche pour les owners qui regardent la map). "
        "Pour tester : achete Platinum en mode sitter, puis bascule role -> "
        "owner et ouvre PawMap. Tu verras le halo a ta position.",
        BODY,
    ))

    story.append(Spacer(1, 1 * cm))
    story.append(p(
        "Commit v23.1.150 sur origin/main. Aucun changement backend dans "
        "cette session - PawSpot fonctionnait deja correctement, on a "
        "juste verifie + traduit les strings UI manquantes.",
        NOTE,
    ))

    doc.build(story)
    print(f"OK PDF v150 fixes recap genere : {OUTPUT}")
    print(f"   Taille : {os.path.getsize(OUTPUT) // 1024} Ko")


if __name__ == "__main__":
    build()
