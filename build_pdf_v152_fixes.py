"""
HopeTSIT - Recap des fixes v23.1.152 + guide build iOS sur Mac.

Sortie : ~/Downloads/HopeTSIT_v23.1.152_Fixes_iOS_Guide.pdf

Daniel : "tout marche sauf la couluer des paw spot, pawspot dore etc, et
surtout pour la 5eme fois ds owner le cadre urgend sur ma publication
naparait pa".

Cette session :
  1. CADRE URGENT cote owner - 5e tentative -> VRAIE cause trouvee : c'etait
     home_screen.dart line 468 (home tab Owner) qui ne forwardait pas
     isOwnerBoosted au PetPostCard. v151 avait fixe my_posts_screen.dart mais
     Daniel regardait le HOME TAB.
  2. COULEURS PAWSPOT - les hues Google Maps predefinies (hueYellow, hueAzure)
     ne correspondaient pas aux noms des tiers ("dore" = jaune pale, "bronze"
     = bleu). Refondu avec des hues bruts pour avoir les bonnes couleurs.
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
    "HopeTSIT_v23.1.152_Fixes_iOS_Guide.pdf",
)

ORANGE = HexColor("#EF4324")
DARK_INK = HexColor("#111827")
GREY_MUTED = HexColor("#6B7280")
GREY_SOFT = HexColor("#F3F4F6")
GREEN = HexColor("#16A34A")
RED = HexColor("#DC2626")
AMBER = HexColor("#F59E0B")
GOLD = HexColor("#D4AF37")

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
OK = ParagraphStyle("OK", parent=base["BodyText"], fontSize=9.5, textColor=GREEN,
                    leading=13, spaceAfter=6, leftIndent=6, fontName="Helvetica-Bold")
WARN = ParagraphStyle("Warn", parent=base["BodyText"], fontSize=9.5, textColor=RED,
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
        title="HopeTSIT v23.1.152 - URGENT frame (vraie cause) + couleurs PawSpot",
        author="HopeTSIT",
    )
    story = []

    # Page de titre
    story.append(Spacer(1, 3 * cm))
    story.append(p("HopeTSIT v23.1.152", TITLE))
    story.append(p("Cadre URGENT owner (vraie cause) + couleurs PawSpot", SUBTITLE))
    story.append(p("+ Guide build iOS sur Mac", SUBTITLE))
    story.append(Spacer(1, 0.5 * cm))
    story.append(make_table([
        ["Version", "23.1.152"],
        ["Date", datetime.now().strftime("%d %B %Y")],
        ["Fixes", "2 (cadre urgent home_screen + hues PawSpot)"],
        ["Codebases touchees", "App Flutter (2 fichiers)"],
        ["Cible app", "Android (rebuilde v152) + iOS (a rebuilder sur Mac)"],
    ], col_widths=[5 * cm, 9 * cm]))
    story.append(Spacer(1, 1.5 * cm))
    story.append(p(
        "Daniel : <i>\"tout marche sauf la couluer des paw spot, pawspot dore "
        "etc, et surtout pour la 5eme fois ds owner le cadre urgend sur ma "
        "publication naparait pa\"</i>",
        BODY,
    ))
    story.append(Spacer(1, 0.5 * cm))
    story.append(p(
        "<b>Mea culpa</b> sur le cadre URGENT : j'avais fixe MyPostsScreen "
        "dans v151 mais Daniel regarde une AUTRE liste, dans le HOME TAB "
        "Owner (home_screen.dart). Cette v152 fixe la vraie source.",
        WARN,
    ))
    story.append(PageBreak())

    # Sommaire
    story.append(p("Sommaire", H1))
    sections = [
        ("1. Vue d'ensemble v152", "2 fixes prioritaires"),
        ("2. Cadre URGENT owner - vraie cause", "home_screen.dart (pas my_posts_screen)"),
        ("3. Couleurs PawSpot - refondues", "Hues bruts coherents avec les noms tiers"),
        ("4. Tableau hues avant / apres", "Bronze 210->15, Silver 270->195, Gold 60->45..."),
        ("5. Audit des PetPostCard - autres ecrans", "Verification exhaustive"),
        ("6. Action Daniel iOS Mac", "Procedure rebuild standard"),
        ("7. Checklist tests v152", "Validation owner + PawSpot par tier"),
    ]
    for title, desc in sections:
        story.append(p(f"<b>{title}</b> - {desc}", BODY))
    story.append(PageBreak())

    # 1. Vue d'ensemble
    story.append(p("1. Vue d'ensemble v152", H1))
    rows = [
        ["Demande Daniel", "Couche", "Solution"],
        ("Cadre URGENT sur mon post owner (5e fois)", "Flutter home_screen", "isOwnerBoosted forward dans HOME TAB (pas MyPostsScreen)"),
        ("Couleurs PawSpot mal traduites (dore etc)", "Flutter paw_map_screen", "Hues bruts par tier au lieu de constantes Google"),
    ]
    story.append(make_table(rows, col_widths=[7 * cm, 3 * cm, 6 * cm]))

    story.append(p("Recap des tentatives precedentes sur le cadre URGENT", H3))
    story.append(p(
        "v148 : ajout de la classe PetPostCard avec param isOwnerBoosted (deja fait).<br/>"
        "v149 : verification que backend enrichit isOwnerBoosted (OK).<br/>"
        "v150 : verification ActiveBenefitsRow expose boostActive (OK).<br/>"
        "v151 : fix MyPostsScreen pour forwarder isOwnerBoosted au PetPostCard.<br/>"
        "v152 : <b>FIX HOME_SCREEN.DART qui etait la VRAIE source affichee a Daniel</b>.",
        BODY,
    ))
    story.append(p(
        "Pourquoi tant de tentatives ? Le frontend Flutter a 2 ecrans qui "
        "affichent les posts de l'owner : MyPostsScreen (ecran complet "
        "separe) et le HOME TAB Owner (home_screen.dart, le tab par defaut "
        "quand l'owner ouvre l'app). Les precedentes versions corrigeaient "
        "MyPostsScreen, mais Daniel regardait le HOME TAB - d'ou le bug "
        "persistant.",
        NOTE,
    ))

    story.append(PageBreak())

    # 2. Cadre URGENT owner
    story.append(p("2. Cadre URGENT owner - vraie cause", H1))
    story.append(p("Symptome", H3))
    story.append(p(
        "Daniel : pour la 5e fois, je ne vois pas le cadre URGENT sur mes "
        "propres annonces dans le profil owner, alors que sitters et walkers "
        "le voient bien.",
        BODY,
    ))
    story.append(p("Cause - 2 ecrans differents", H3))
    story.append(make_table([
        ["Fichier", "Quand affiche", "Fix v151", "Fix v152"],
        ("my_posts_screen.dart", "Ecran complet via menu profil", "isOwnerBoosted ajoute (2 calls)", "Deja OK"),
        ("home_screen.dart", "TAB 'Mes publications' du home owner", "Pas touche - oublie !", "isOwnerBoosted ajoute"),
    ], col_widths=[5 * cm, 5 * cm, 3 * cm, 3 * cm]))

    story.append(p("Le diff v152", H3))
    story.append(code_block(
        "// home_screen.dart ligne 480-489 - PetPostCard du HOME TAB\n"
        "PetPostCard(\n"
        "  // ... autres params\n"
        "  isReserved: post.reservedBy != null,\n"
        "  reservedProviderRole: post.reservedBy?.providerRole,\n"
        "  ownerViewOfOwnPost: true,\n"
        "  // v23.1.152 - AJOUTE\n"
        "  isOwnerBoosted: post.isOwnerBoosted,\n"
        "  ownerBoostTier: post.ownerBoostTier,\n"
        "  onDelete: () => _confirmAndDeletePost(context, post.id),\n"
        "  // ...\n"
        ")"
    ))
    story.append(p("Comment je l'ai trouve", H3))
    story.append(p(
        "Grep <i>'PetPostCard\\(' sur tout le projet</i> = 5 fichiers. J'ai "
        "elimine sitter_homescreen.dart (vue sitter), pet_post_card.dart "
        "(definition du widget), notification_post_view_screen.dart (vue "
        "notif). Restent <b>my_posts_screen.dart</b> (deja fixe v151) ET "
        "<b>home_screen.dart</b> (le coupable). Lecon : grep large des le "
        "depart, pas juste l'ecran le plus evident.",
        BODY,
    ))
    story.append(p("Verdict : URGENT frame s'affichera maintenant DES le retour sur le home tab apres achat du boost.", OK))

    story.append(PageBreak())

    # 3. Couleurs PawSpot
    story.append(p("3. Couleurs PawSpot - refondues", H1))
    story.append(p("Symptome", H3))
    story.append(p(
        "Daniel : \"tout marche sauf la couluer des paw spot, pawspot dore "
        "etc\". Les pins boostes ne se distinguaient pas visuellement, et le "
        "tier \"dore\" (gold) ne ressemblait pas a du dore.",
        BODY,
    ))
    story.append(p("Cause", H3))
    story.append(p(
        "Le code utilisait les constantes <i>BitmapDescriptor.hueXxx</i> de "
        "Google Maps. Ces hues prefigent ont des valeurs fixes qui ne "
        "correspondent pas forcement aux attentes :",
        BODY,
    ))
    story.append(make_table([
        ["Constante", "Valeur hue", "Couleur reelle"],
        ("hueYellow", "60", "Jaune pale (canari)"),
        ("hueOrange", "30", "Orange"),
        ("hueAzure", "210", "Bleu ciel"),
        ("hueViolet", "270", "Violet"),
    ], col_widths=[3 * cm, 2 * cm, 5 * cm]))

    story.append(p("Probleme : <b>hueYellow 60</b> = jaune fade, pas dore. Et <b>hueAzure 210</b> = bleu, pas bronze.", WARN))

    story.append(p("Fix - hues bruts par tier", H3))
    story.append(code_block(
        "// AVANT (v151)\n"
        "case 'platinum': hue = BitmapDescriptor.hueOrange;  // 30\n"
        "case 'gold':     hue = BitmapDescriptor.hueYellow;  // 60 (pale)\n"
        "case 'silver':   hue = BitmapDescriptor.hueViolet;  // 270\n"
        "case 'bronze':   hue = BitmapDescriptor.hueAzure;   // 210 (bleu !)\n\n"
        "// APRES (v152)\n"
        "case 'platinum': hue = 30.0;   // orange chaud\n"
        "case 'gold':     hue = 45.0;   // ambre dore (vrai gold)\n"
        "case 'silver':   hue = 195.0;  // bleu-gris argent\n"
        "case 'bronze':   hue = 15.0;   // rouge-cuivre"
    ))

    story.append(PageBreak())

    # 4. Tableau hues avant / apres
    story.append(p("4. Tableau visuel hues avant / apres", H1))

    rows = [
        ["Tier", "Avant (v151)", "Apres (v152)", "Visuel attendu"],
        ("Bronze", "210 - bleu ciel", "15 - rouge-cuivre", "Pin couleur cuivre/bronze patine"),
        ("Silver", "270 - violet", "195 - bleu-gris", "Pin argente legerement bleute"),
        ("Gold", "60 - jaune pale", "45 - ambre dore", "Pin couleur or chaud (vraiment dore)"),
        ("Platinum", "30 - orange", "30 - orange + HALO ANIME", "Pin orange + cercle pulsant gold autour"),
    ]
    story.append(make_table(rows, col_widths=[2.5 * cm, 4 * cm, 4 * cm, 5 * cm]))

    story.append(p("Pourquoi pas un pin custom asset ?", H3))
    story.append(p(
        "Google Maps Flutter accepte uniquement un asset PNG via "
        "<i>BitmapDescriptor.fromAsset</i> ou un hue 0-360 via "
        "<i>BitmapDescriptor.defaultMarkerWithHue</i>. Pour avoir un vrai "
        "pin dore custom il faudrait 4 PNG (1 par tier) + gestion du chargement "
        "async + des tailles. Les hues bruts sont une solution propre et "
        "instantanee. Si Daniel veut des pins customs plus tard, on a une "
        "extension claire (charger 4 assets au lieu de hardcoder un hue).",
        BODY,
    ))

    story.append(p("Note - Halo Platinum inchange", H3))
    story.append(p(
        "Le halo anime autour des pins Platinum n'a pas change : il pulse "
        "toujours en couleur <i>#FFAA00</i> (or chaud), radius 30->160m, "
        "cycle 2.4s. Avec le pin orange en dessous, le visuel est tres "
        "premium.",
        NOTE,
    ))

    story.append(PageBreak())

    # 5. Audit PetPostCard
    story.append(p("5. Audit exhaustif des PetPostCard", H1))
    story.append(p("Pour ne PLUS rater un appel", H3))
    rows = [
        ["Fichier", "Role qui voit", "isOwnerBoosted", "Statut v152"],
        ("pet_post_card.dart", "Definition", "Param accepte", "OK (deja existe)"),
        ("sitter_homescreen.dart", "Sitter/Walker", "Oui (line 1102)", "OK (deja existant)"),
        ("home_screen.dart", "Owner (HOME TAB)", "Oui (line 489) - v152", "FIX v152"),
        ("my_posts_screen.dart", "Owner (ecran separe)", "Oui (2 calls) - v151", "OK (v151)"),
        ("notification_post_view_screen.dart", "Notification deep-link", "Non - par design", "OK (ne montre pas boost)"),
    ]
    story.append(make_table(rows, col_widths=[5 * cm, 3 * cm, 4 * cm, 3 * cm]))

    story.append(p("Maintenant les 3 vues principales (owner home + owner my_posts + sitter/walker home) ont le cadre URGENT.", OK))

    story.append(p("Si Daniel ouvre un post via notification (deep link)", H3))
    story.append(p(
        "Le notification_post_view_screen.dart est un cas d'usage marginal "
        "(ouvrir une annonce via une notif push) - on ne montre pas l'etat "
        "boost dedans car c'est une vue de details, pas une liste. Si Daniel "
        "veut aussi voir le cadre dans cette vue, on pourra ajouter en v153.",
        BODY,
    ))

    story.append(PageBreak())

    # 6. Action iOS
    story.append(p("6. Ce qu'il te reste a faire sur Mac (iOS)", H1))
    story.append(p("Procedure standard - 2 fichiers a recompiler", H3))
    story.append(code_block(
        "# Sur ton Mac, dans le dossier HopeTSIT_FINAL\n"
        "git pull --rebase\n"
        "# Tu dois voir le commit v23.1.152\n\n"
        "cd frontend\n"
        "flutter pub get\n"
        "cd ios && pod install\n"
        "open Runner.xcworkspace\n\n"
        "# Bump pubspec.yaml : version: 23.1.152+152\n"
        "flutter build ipa --release\n"
        "# Drag&drop build/ios/ipa/HopeTSIT.ipa dans Transporter"
    ))
    story.append(p(
        "Aucune dependance native ajoutee. Tout est du Dart partage.",
        NOTE,
    ))

    # 7. Checklist
    story.append(p("7. Checklist tests v152", H1))
    tests = [
        ("Owner sans boost - home tab", "Mes publications : cards normales, pas de bordure rouge"),
        ("Owner achete BRONZE en mode staff", "Snackbar succes, badge bronze dans profil"),
        ("Owner retour home tab apres achat bronze", "Cards avec bordure rouge URGENT autour"),
        ("Owner ouvre MyPostsScreen (icon \"Mes publications\")", "Meme cards avec bordure URGENT (deja OK v151)"),
        ("PawSpot map - acheter BRONZE", "Pin rouge-cuivre sur la carte (pas bleu)"),
        ("PawSpot map - acheter SILVER", "Pin bleu-gris argente (pas violet)"),
        ("PawSpot map - acheter GOLD", "Pin ambre dore (vraiment dore, pas jaune pale)"),
        ("PawSpot map - acheter PLATINUM", "Pin orange chaud + halo pulsant dore autour"),
        ("Differencier visuellement bronze vs gold", "Bronze plus rouge, gold plus jaune-orange"),
        ("Differencier silver vs platinum sans halo", "Silver bleu-gris, platinum orange"),
        ("Tests v151 toujours OK", "Bouton submit traduit, filter chips traduits"),
        ("Tests v150 toujours OK", "4 tiers PawSpot, confirm dialog traduit"),
        ("Tests v149 toujours OK", "Halo geoloc bleu, i18n PawMap"),
    ]
    rows = [["Test", "Attendu"]] + tests
    story.append(make_table(rows, col_widths=[7 * cm, 8.5 * cm]))

    story.append(p("Si le cadre URGENT n'apparait TOUJOURS pas", H3))
    story.append(p(
        "1. Verifier qu'on est bien sur le HOME TAB Owner (pas dans \"Mes "
        "publications\" via le menu)<br/>"
        "2. Verifier que le boost est actif en regardant le badge ActiveBenefitsRow "
        "(\"Boost - 9j\" doit etre visible dans le header du profil)<br/>"
        "3. Pull-to-refresh le home tab pour forcer un re-fetch<br/>"
        "4. Si toujours rien : ouvrir Render logs, chercher la requete "
        "GET /posts/my et verifier que isOwnerBoosted=true dans la response",
        BODY,
    ))

    story.append(Spacer(1, 1 * cm))
    story.append(p(
        "Cette v152 cloture les 2 demandes. Le cadre URGENT cote owner sera "
        "visible dans LES 2 ecrans (home tab + my_posts_screen). Les 4 tiers "
        "PawSpot ont des couleurs visuellement distinctes et le tier Gold "
        "ressemble enfin a du dore.",
        NOTE,
    ))

    doc.build(story)
    print(f"OK PDF v152 fixes recap genere : {OUTPUT}")
    print(f"   Taille : {os.path.getsize(OUTPUT) // 1024} Ko")


if __name__ == "__main__":
    build()
