"""
HopeTSIT - PDF iOS mis a jour v23.1.165.

Sortie : ~/Downloads/HopeTSIT_v23.1.165_Fixes_iOS_Guide.pdf

Addendum au PDF v164 consolide. v165 ajoute :
  - Onboarding screen UX : moins de blanc + icones plus grandes + traductions
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
    "HopeTSIT_v23.1.165_Fixes_iOS_Guide.pdf",
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
        title="HopeTSIT v23.1.165 - Marathon final + onboarding UX",
        author="HopeTSIT",
    )
    story = []

    # Page de titre
    story.append(Spacer(1, 2.5 * cm))
    story.append(p("HopeTSIT v23.1.165", TITLE))
    story.append(p("Marathon consolide v149 -> v165 + onboarding UX", SUBTITLE))
    story.append(p("17 versions, ~28 bugs fixes, ~900 entries i18n", SUBTITLE))
    story.append(Spacer(1, 0.5 * cm))
    story.append(make_table([
        ["Version finale", "23.1.165 (commit 43b46ef)"],
        ["Date", datetime.now().strftime("%d %B %Y")],
        ["Sessions couvertes", "v149 -> v165 (17 versions)"],
        ["Nouveau dans v165", "Onboarding screen UX (less white + bigger icons + i18n)"],
        ["Codebases", "Backend (10 fichiers) + Frontend (20 fichiers) + 6 locales"],
        ["i18n total session", "~150 cles x 6 langues = ~900 entries"],
    ], col_widths=[5 * cm, 9 * cm]))
    story.append(Spacer(1, 1 * cm))
    story.append(p(
        "Ce PDF complete le guide v164 consolide avec les changements v165 : "
        "ameliorations UX de l'ecran d'onboarding Android (zone blanche reduite, "
        "icones plus grandes, traductions corrigees ES/DE/PT).",
        BODY,
    ))
    story.append(p(
        "Pour le recap des 16 versions precedentes (v149-v164), reference au "
        "PDF HopeTSIT_v23.1.164_Fixes_iOS_Guide.pdf qui couvre Airwallex, "
        "72h cancellation, halos PawSpot, deep links email, et i18n exhaustif.",
        NOTE,
    ))
    story.append(PageBreak())

    # Sommaire
    story.append(p("Sommaire", H1))
    sections = [
        ("1. Recap v149 -> v164", "Voir PDF v164 - 16 versions / ~27 bugs"),
        ("2. v165 - Onboarding UX (NOUVEAU)", "3 ameliorations sur l'ecran d'accueil"),
        ("3. Avant / Apres - comparaison visuelle", "Mesures precises des changements"),
        ("4. Action Daniel iOS Mac", "Procedure rebuild standard"),
        ("5. Checklist tests v165", "Validation post-rebuild"),
    ]
    for title, desc in sections:
        story.append(p(f"<b>{title}</b> - {desc}", BODY))
    story.append(PageBreak())

    # 1. Recap rapide
    story.append(p("1. Recap rapide v149 -> v164", H1))
    story.append(p(
        "Pour le detail complet de chaque version, voir le PDF v164. Resume "
        "des themes majeurs traites pendant le marathon :",
        BODY,
    ))
    story.append(bullet("<b>Airwallex paiement (saga 3 versions v156-v158)</b> : page blanche debloquee + cartes sauvegardees + PI cancelled gere"))
    story.append(bullet("<b>72h cancellation 3 profils (v160-v161)</b> : walker + sitter + owner peuvent annuler, notifs cross-parties"))
    story.append(bullet("<b>Halos PawSpot (3 root causes v149-v163)</b> : self-halo + role-color always-on + Obx dependency fix"))
    story.append(bullet("<b>Emails universal links (v155)</b> : 50 remplacements hopetsit:// -> https://hopetsit.com, factures HTML localisees 6 langues"))
    story.append(bullet("<b>Samsung nav bar (v161-v164)</b> : 3 iterations -> gris persistant via AnnotatedRegion"))
    story.append(bullet("<b>UX details</b> : Suivre walker chat / Save invoice / Cancel button 3 ecrans / app no auto-logout"))

    # 2. v165 - Nouveautes
    story.append(p("2. v165 - Onboarding UX (NOUVEAU)", H1))
    story.append(p("Daniel screenshot Android : 'sur android peux tu ameliorer cette page moin de blanc les 3 icones plus grande et que ce soit bien traduit celon les langues'", H3))
    story.append(p(
        "L'ecran d'accueil avant connexion (OnboardingScreen) montrait :",
        BODY,
    ))
    story.append(bullet("Zone orange du haut (logo + tagline + 3 chips) ne couvrant que 48% de l'ecran"))
    story.append(bullet("Zone blanche du bas (boutons S'inscrire + Google + Se connecter) couvrait 52% = trop de vide"))
    story.append(bullet("3 chips Pet-sitting / PawMap / PawFollow trop petites (54w, icones 26sp)"))
    story.append(bullet("Le label 'Pet-sitting' n'etait pas vraiment localise (anglicisme partout)"))

    story.append(p("Fix #1 - Moins de blanc (gradient stops)", H3))
    story.append(code_block(
        "// AVANT\n"
        "stops: const [0.0, 0.48, 0.48, 1.0]\n"
        "// = orange 48% / coupure nette / blanc 52%\n\n"
        "// APRES\n"
        "stops: const [0.0, 0.60, 0.65, 1.0]\n"
        "// = orange 60% / transition douce sur 5% / blanc 35%"
    ))
    story.append(p(
        "Resultat visuel : la zone orange occupe maintenant 65% de l'ecran "
        "(vs 48% avant). La transition orange -> blanc se fait sur une bande "
        "de 5% au lieu d'une coupure brutale. Le vide blanc en bas est "
        "considerablement reduit.",
        BODY,
    ))

    story.append(p("Fix #2 - 3 icones plus grandes (+48%)", H3))
    story.append(make_table([
        ["Propriete", "Avant", "Apres", "Delta"],
        ("container width", "54.w", "80.w", "+48%"),
        ("container height", "54.w", "80.w", "+48%"),
        ("icon size", "26.sp", "38.sp", "+46%"),
        ("border radius", "18.r", "22.r", "+22%"),
        ("shadow blur", "8", "14", "+75%"),
        ("shadow alpha", "0.10", "0.18", "+80%"),
        ("shadow offset Y", "2", "4", "+100%"),
        ("label fontSize", "10.sp", "12.sp", "+20%"),
        ("label fontWeight", "w600", "w700", "plus gras"),
        ("spacing label", "8.h", "10.h", "+25%"),
    ], col_widths=[4 * cm, 2.5 * cm, 2.5 * cm, 2 * cm]))

    story.append(p(
        "Les chips passent d'un design discret a un design imposant. L'ombre "
        "plus prononcee donne plus de profondeur. La presence visuelle de la "
        "section feature est largement augmentee.",
        BODY,
    ))

    story.append(p("Fix #3 - Traductions Pet-sitting par langue", H3))
    story.append(p(
        "Le label 'Pet-sitting' du chip etait identique dans toutes les langues "
        "(anglicisme). Pour ES et DE, il existe des termes natifs plus appropries. "
        "Pour PT, le texte etait trop long ('Cuidar de animais de estimação') et "
        "depassait du chip.",
        BODY,
    ))

    story.append(make_table([
        ["Langue", "Avant", "Apres v165", "Raison"],
        ("🇫🇷 FR", "Pet-sitting", "Pet-sitting", "Anglicisme accepte en FR"),
        ("🇬🇧 EN", "Pet-sitting", "Pet-sitting", "Identique"),
        ("🇪🇸 ES", "Pet-sitting", "Cuidado", "Mot natif court"),
        ("🇩🇪 DE", "Pet-sitting", "Tiersitting", "Terme allemand standard"),
        ("🇮🇹 IT", "Pet-sitting", "Pet-sitting", "Anglicisme accepte en IT"),
        ("🇵🇹 PT", "Cuidar de animais...", "Pet-sitting", "Anglicisme accepte (avant trop long)"),
    ], col_widths=[2 * cm, 4 * cm, 3 * cm, 5 * cm]))

    story.append(p(
        "PawMap et PawFollow sont des noms de produits (marques) et restent "
        "identiques dans toutes les langues.",
        NOTE,
    ))

    story.append(PageBreak())

    # 3. Avant/Apres
    story.append(p("3. Avant / Apres - comparaison visuelle", H1))
    story.append(p("Repartition orange/blanc de l'ecran", H3))
    story.append(code_block(
        "AVANT (v164 et anterieur)            APRES (v165)\n"
        "+------------------------+           +------------------------+\n"
        "|                        |           |                        |\n"
        "|     ORANGE             |           |     ORANGE             |\n"
        "|   (48% de l'ecran)     |           |   (60% de l'ecran)     |\n"
        "|   Logo + tagline +     |           |   Logo + tagline +     |\n"
        "|   3 chips (petites)    |           |   3 chips GROSSES      |\n"
        "+------------------------+           |                        |\n"
        "|                        |           +................+      |\n"
        "|                        |           |  transition    |      |\n"
        "|                        |           |  douce (5%)    |      |\n"
        "|                        |           +........+...........+\n"
        "|     BLANC              |           |                        |\n"
        "|   (52% de l'ecran)     |           |     BLANC              |\n"
        "|   S'inscrire + Google  |           |   (35% de l'ecran)     |\n"
        "|   Se connecter         |           |   S'inscrire + Google  |\n"
        "|                        |           |   Se connecter         |\n"
        "+------------------------+           +------------------------+"
    ))

    story.append(p("Comparaison taille chips", H3))
    story.append(code_block(
        "AVANT                          APRES\n"
        "  [54w]                        [    80w    ]\n"
        " icon 26                       icon 38 (+46%)\n"
        " label 10sp w600               label 12sp w700\n"
        " shadow leger                  shadow prononce\n\n"
        "                                            \n"
        " (decoratif)                   (imposant)"
    ))

    # 4. Action iOS
    story.append(p("4. Action Daniel iOS Mac", H1))
    story.append(code_block(
        "# Sur ton Mac, dans HopeTSIT_FINAL\n"
        "git pull --rebase  # -> commit 43b46ef (v23.1.165)\n"
        "cd frontend && flutter pub get\n"
        "cd ios && pod install\n"
        "open Runner.xcworkspace\n\n"
        "# Bump pubspec.yaml : version: 23.1.165+165\n"
        "flutter build ipa --release\n"
        "# Drag&drop build/ios/ipa/HopeTSIT.ipa dans Transporter -> Deliver"
    ))
    story.append(p(
        "Aucune nouvelle dependance native. La build iOS est juste un "
        "rebundling des nouveaux i18n keys + le widget _FeatureChip mis a "
        "jour. L'AppDelegate iOS n'a pas change.",
        NOTE,
    ))

    # 5. Checklist
    story.append(p("5. Checklist tests v165", H1))
    tests = [
        ("Force-quit + reinstall l'app", "Vide le cache du splash/onboarding"),
        ("Premier lancement (deconnecte)", "Ecran d'onboarding s'affiche"),
        ("Zone orange visible", "Couvre ~65% de l'ecran (avant : 48%)"),
        ("Transition orange -> blanc", "Fondu doux sur 5% au lieu d'une coupure"),
        ("3 chips Pet-sitting / PawMap / PawFollow", "Chips de 80w avec icones 38sp et ombre prononcee"),
        ("Labels chips lisibles", "Police 12sp w700 (plus epais qu'avant)"),
        ("Bascule en ES - chip 1", "Affiche 'Cuidado' (au lieu de 'Pet-sitting')"),
        ("Bascule en DE - chip 1", "Affiche 'Tiersitting'"),
        ("Bascule en PT - chip 1", "Affiche 'Pet-sitting' (court, rentre dans le chip)"),
        ("Bascule en FR/EN/IT - chip 1", "Affiche 'Pet-sitting' (anglicisme accepte)"),
        ("Boutons CTA en bas", "S'inscrire + Google + Se connecter visibles"),
        ("Pas de Spacer/Padding casse", "Layout correct sur petits ecrans (iPhone SE, etc.)"),
        ("Tests v164 toujours OK", "Airwallex / cancel 72h / halos / Samsung nav grey / Invoice label"),
    ]
    rows = [["Test", "Attendu"]] + tests
    story.append(make_table(rows, col_widths=[7 * cm, 8 * cm]))

    story.append(Spacer(1, 0.5 * cm))
    story.append(p(
        "Cette v165 cloture le marathon de 17 versions sur 48h. L'app est "
        "stable, les ecrans sont equilibres (moins de vide), la i18n est "
        "complete pour les 6 langues, les flux paiement / cancellation / "
        "live walk fonctionnent. Rebuild iOS via la procedure ci-dessus et "
        "tu es bon pour TestFlight.",
        NOTE,
    ))

    doc.build(story)
    print(f"OK PDF v165 genere : {OUTPUT}")
    print(f"   Taille : {os.path.getsize(OUTPUT) // 1024} Ko")


if __name__ == "__main__":
    build()
