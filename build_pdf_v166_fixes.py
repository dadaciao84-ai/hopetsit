"""
HopeTSIT - PDF iOS mis a jour v23.1.166.

Sortie : ~/Downloads/HopeTSIT_v23.1.166_Fixes_iOS_Guide.pdf

Addendum au PDF v164/v165. v166 ajoute :
  - Redesign complet onboarding selon mockup Daniel
  - Logo + titre plus grands, 3 cartes blanches au lieu de chips
  - Bouton S'inscrire avec icone patte + fleche
  - 3 nouvelles cles i18n descriptions x 6 langues
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
    "HopeTSIT_v23.1.166_Fixes_iOS_Guide.pdf",
)

ORANGE = HexColor("#EF4324")
DARK_INK = HexColor("#111827")
GREY_MUTED = HexColor("#6B7280")
GREY_SOFT = HexColor("#F3F4F6")
GREEN = HexColor("#16A34A")
RED = HexColor("#DC2626")
AMBER = HexColor("#F59E0B")

base = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=base["Heading1"], fontSize=20, textColor=ORANGE,
                    spaceAfter=10, spaceBefore=12, fontName="Helvetica-Bold")
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
        title="HopeTSIT v23.1.166 - Onboarding redesign + verif i18n",
        author="HopeTSIT",
    )
    story = []

    # Page de titre
    story.append(Spacer(1, 2.5 * cm))
    story.append(p("HopeTSIT v23.1.166", TITLE))
    story.append(p("Onboarding redesign complet selon mockup Daniel", SUBTITLE))
    story.append(p("+ Verification i18n 6 langues + Guide iOS", SUBTITLE))
    story.append(Spacer(1, 0.5 * cm))
    story.append(make_table([
        ["Version finale", "23.1.166 (commit f3bea26)"],
        ["Date", datetime.now().strftime("%d %B %Y")],
        ["Nouveau dans v166", "Onboarding redesign + i18n descriptions"],
        ["Verif i18n", "11 cles onboarding x 6 langues = 66 entries verifiees"],
        ["Codebases", "Frontend uniquement (1 fichier + 6 locales)"],
    ], col_widths=[5 * cm, 9 * cm]))
    story.append(Spacer(1, 1 * cm))
    story.append(p(
        "Ce PDF complete les guides v164/v165 avec les changements v166 : "
        "redesign complet de l'ecran d'onboarding suite au mockup envoye "
        "par Daniel. Les 3 chips horizontales sont remplacees par 3 cartes "
        "blanches verticales avec icone circulaire + titre + description.",
        BODY,
    ))
    story.append(PageBreak())

    # Sommaire
    story.append(p("Sommaire", H1))
    sections = [
        ("1. Recap v149 -> v165", "16 versions precedentes - voir PDF v164/v165"),
        ("2. v166 - Onboarding redesign mockup", "5 changements majeurs"),
        ("3. Verification i18n 11 cles x 6 langues", "Tableau complet de validation"),
        ("4. Avant / Apres - comparaison visuelle", "ASCII art des deux designs"),
        ("5. Action Daniel iOS Mac", "Procedure rebuild standard"),
        ("6. Checklist tests v166", "Validation post-rebuild"),
    ]
    for title, desc in sections:
        story.append(p(f"<b>{title}</b> - {desc}", BODY))
    story.append(PageBreak())

    # 1. Recap rapide
    story.append(p("1. Recap rapide v149 -> v165", H1))
    story.append(p(
        "Pour le detail des 17 versions precedentes, voir le PDF v164 "
        "consolide + l'addendum v165 (onboarding UX initial). Resume :",
        BODY,
    ))
    story.append(bullet("v149-v154 : PawMap halo + i18n + invoice save + no auto-logout"))
    story.append(bullet("v155 : Universal links emails (50 replacements x 6 langs)"))
    story.append(bullet("v156-v158 : Airwallex saga (page blanche -> PI cancelled -> saved cards)"))
    story.append(bullet("v159-v161 : 72h cancel 3 profils + halos colors + Samsung nav"))
    story.append(bullet("v162-v164 : i18n exhaustif + Samsung nav grey persistant + Invoice label"))
    story.append(bullet("v165 : Onboarding UX initial (less white + bigger chips)"))
    story.append(bullet("<b>v166 : Onboarding REDESIGN COMPLET selon mockup Daniel</b>"))

    story.append(PageBreak())

    # 2. v166 - Nouveautes
    story.append(p("2. v166 - Onboarding redesign mockup", H1))
    story.append(p("Daniel a fourni un mockup demandant 5 changements :", H3))

    story.append(p("Changement #1 - Gradient orange dominant", H3))
    story.append(code_block(
        "// AVANT v165\n"
        "stops: [0.0, 0.60, 0.65, 1.0]\n"
        "// orange 65% / transition 5% / blanc 35%\n\n"
        "// APRES v166\n"
        "stops: [0.0, 0.55, 0.78, 1.0]\n"
        "colors: [\n"
        "  AppColors.primaryColor,  // #EF4324\n"
        "  Color(0xFFFF6B45),       // orange mid\n"
        "  Color(0xFFFF9B7A),       // orange clair\n"
        "  Colors.white,            // blanc bas\n"
        "]"
    ))
    story.append(bullet("Orange dominant sur 78% (vs 65% en v165, 48% avant)"))
    story.append(bullet("Transition douce sur 22% avec 4 stops degrades"))
    story.append(bullet("Effet visuel plus harmonieux, pas de coupure nette"))

    story.append(p("Changement #2 - Logo et titre plus grands", H3))
    story.append(make_table([
        ["Propriete", "Avant v165", "Apres v166", "Delta"],
        ("Logo width", "88.w (-> 80 v165)", "130.w", "+48% / +63%"),
        ("Border radius", "22.r", "32.r", "+45%"),
        ("Shadow blur", "20", "24", "+20%"),
        ("Padding logo", "8.w", "10.w", "+25%"),
        ("Titre 'HoPetSit' fontSize", "28.sp", "36.sp", "+28%"),
        ("Tagline fontWeight", "w400", "w500", "plus lisible"),
    ], col_widths=[4.5 * cm, 3 * cm, 3 * cm, 2.5 * cm]))

    story.append(p("Changement #3 - 3 cartes au lieu de chips", H3))
    story.append(p(
        "AVANT (v165) : chip vertical = carre blanc 80w + label en-dessous, "
        "fond orange. Layout horizontal Row.<br/>"
        "APRES (v166) : carte blanche complete avec :",
        BODY,
    ))
    story.append(bullet("Container white + borderRadius 20 + shadow blur 14"))
    story.append(bullet("Icone circulaire orange-tinted (12% alpha) - taille 56w"))
    story.append(bullet("Icon size 28sp couleur orange"))
    story.append(bullet("Titre PoppinsText 14sp w700 NOIR (lisibilite optimale)"))
    story.append(bullet("Description InterText 11sp w400 GRIS (4 lignes max)"))
    story.append(bullet("IntrinsicHeight parent pour egaliser les hauteurs des 3 cartes"))

    story.append(p("Changement #4 - Bouton S'inscrire stylé", H3))
    story.append(code_block(
        "// CustomButton avec child Row spaceBetween :\n"
        "child: Row(\n"
        "  mainAxisAlignment: MainAxisAlignment.spaceBetween,\n"
        "  children: [\n"
        "    Container(width: 36, decoration: circle white-alpha)\n"
        "      .child(Icon Icons.pets size 18 white),       // patte\n"
        "    PoppinsText('onboarding_signup'.tr 16sp w700 white), // texte\n"
        "    Icon(arrow_forward_ios_rounded size 16 white),  // fleche\n"
        "  ],\n"
        ")"
    ))
    story.append(p(
        "Resultat : bouton orange avec icone patte ronde a gauche, texte "
        "centre, fleche a droite. Plus engageant que l'ancien bouton "
        "texte-seul.",
        BODY,
    ))

    story.append(p("Changement #5 - 3 nouvelles cles i18n descriptions", H3))
    story.append(p("Chaque carte a maintenant un titre + une description. 3 nouvelles cles ajoutees :", BODY))
    story.append(bullet("onboarding_feature_trusted_desc : description Pet-sitting"))
    story.append(bullet("onboarding_feature_chat_desc : description PawMap"))
    story.append(bullet("onboarding_feature_nearby_desc : description PawFollow"))
    story.append(p("Total 18 entries injectees (3 cles x 6 langues) via script Python inject_onboarding_descs.py.", NOTE))

    story.append(PageBreak())

    # 3. Verification i18n
    story.append(p("3. Verification i18n 11 cles x 6 langues", H1))
    story.append(p("Verification post-injection executee sur tous les fichiers locale :", H3))

    # Headers tableau
    rows = [
        ["Cle", "FR", "EN", "ES", "DE", "IT", "PT"],
        ("tagline (extrait)", "suivi animal", "live tracking", "seguimiento", "Tracking Ihres Tieres", "tracciamento", "acompanhamento"),
        ("feature_trusted (chip 1)", "Pet-sitting", "Pet-sitting", "Cuidado", "Tiersitting", "Pet-sitting", "Pet-sitting"),
        ("feature_chat (chip 2)", "PawMap", "PawMap", "PawMap", "PawMap", "PawMap", "PawMap"),
        ("feature_nearby (chip 3)", "PawFollow", "PawFollow", "PawFollow", "PawFollow", "PawFollow", "PawFollow"),
        ("feature_trusted_desc", "Trouvez...", "Find...", "Encuentra...", "Finde...", "Trova...", "Encontra..."),
        ("feature_chat_desc", "Explorez...", "Explore...", "Explora...", "Entdecke...", "Esplora...", "Explora..."),
        ("feature_nearby_desc", "Suivez...", "Follow...", "Sigue...", "Verfolge...", "Segui...", "Segue..."),
        ("signup (bouton)", "S'inscrire", "Sign up", "Registrarse", "Registrieren", "Registrati", "Registar"),
        ("continue_with_google", "Continuer avec Google", "Continue with Google", "Continuar con Google", "Mit Google fortfahren", "Continua con Google", "Continuar com o Google"),
        ("have_account", "Vous avez un compte ?", "Have an account?", "Tienes una cuenta?", "Hast du ein Konto?", "Hai un account?", "Tem uma conta?"),
        ("or", "ou", "or", "o", "oder", "o", "ou"),
    ]
    story.append(make_table(rows, col_widths=[3.5 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm]))

    story.append(p("Conclusion : 11 cles couvertes dans les 6 langues = 66 entries valides. PawMap + PawFollow restent identiques (noms de produits / marques).", OK))

    story.append(PageBreak())

    # 4. Avant/Apres ASCII
    story.append(p("4. Avant / Apres - comparaison visuelle", H1))
    story.append(p("Repartition ecran et type d'elements", H3))
    story.append(code_block(
        "AVANT v165                          APRES v166 (mockup)\n"
        "+------------------------+          +------------------------+\n"
        "|     ORANGE             |          |     ORANGE FONCE       |\n"
        "|   Logo 88w (small)     |          |   Logo 130w (big)      |\n"
        "|   HoPetSit 28sp        |          |   HoPetSit 36sp        |\n"
        "|   tagline              |          |   tagline              |\n"
        "|   [chip][chip][chip]   |          |                        |\n"
        "|   (small chips)        |          |   ORANGE MID           |\n"
        "+------------------------+          | +----+ +----+ +----+   |\n"
        "|                        |          | |card| |card| |card|   |\n"
        "|                        |          | | ⭕ | | ⭕ | | ⭕ |   |\n"
        "|     BLANC              |          | |titl| |titl| |titl|   |\n"
        "|   S'inscrire           |          | |desc| |desc| |desc|   |\n"
        "|   Google btn           |          | +----+ +----+ +----+   |\n"
        "|   Se connecter         |          |                        |\n"
        "+------------------------+          |   ORANGE CLAIR + WHITE |\n"
        "                                    | [🐾 S'inscrire   ›]    |\n"
        "                                    | [G Continuer Google]   |\n"
        "                                    | ou - Vous avez compte? |\n"
        "                                    +------------------------+"
    ))

    story.append(p("Comparaison composants 'feature'", H3))
    story.append(code_block(
        "v165 chip (carre + label)       v166 card (carte complete)\n"
        "  [80w]                            +-----------+\n"
        " icon 28sp                         |           |\n"
        " Pet-sitting (12sp blanc)          |    ⭕     |  56w cercle orange-12%\n"
        "                                   |  icon 28  |\n"
        "                                   |           |\n"
        "                                   | Pet-sit.. |  titre 14sp w700 noir\n"
        "                                   |           |\n"
        "                                   | Trouvez   |  desc 11sp w400 gris\n"
        "                                   | des pet-  |\n"
        "                                   | sitters.. |\n"
        "                                   +-----------+"
    ))

    story.append(PageBreak())

    # 5. Action iOS
    story.append(p("5. Action Daniel iOS Mac", H1))
    story.append(code_block(
        "# Sur ton Mac, dans HopeTSIT_FINAL\n"
        "git pull --rebase  # -> commit f3bea26 (v23.1.166)\n"
        "cd frontend && flutter pub get\n"
        "cd ios && pod install\n"
        "open Runner.xcworkspace\n\n"
        "# Bump pubspec.yaml : version: 23.1.166+166\n"
        "flutter build ipa --release\n"
        "# Drag&drop build/ios/ipa/HopeTSIT.ipa dans Transporter -> Deliver"
    ))
    story.append(p(
        "Aucune dependance native ajoutee. C'est uniquement du redesign Dart "
        "+ ajout de 3 cles i18n. Le rebuild iOS est rapide (pas de nouveaux "
        "pods, pas de capability iOS ajoutee).",
        NOTE,
    ))

    # 6. Checklist
    story.append(p("6. Checklist tests v166", H1))
    tests = [
        ("Force-quit + reinstall l'app", "Vide le cache du splash/onboarding"),
        ("Premier lancement (deconnecte)", "Ecran d'onboarding s'affiche"),
        ("Logo HoPetSit", "Tres grand (130w), bordure blanche, shadow prononce"),
        ("Titre 'HoPetSit'", "36sp, blanc, gras (visible de loin)"),
        ("Gradient orange", "Dominant ~78%, transition douce vers blanc en bas"),
        ("3 cartes visibles", "Blanches avec icone circulaire orange-tinted"),
        ("Cards Pet-sitting / PawMap / PawFollow", "Meme hauteur (IntrinsicHeight)"),
        ("Description sous chaque titre", "Texte gris 11sp en 4 lignes max"),
        ("Bouton S'inscrire", "Orange avec patte ronde + texte + fleche"),
        ("Bouton Google", "Blanc avec bordure orange + logo Google"),
        ("Bascule en ES - card 1", "'Cuidado' + 'Encuentra cuidadores...'"),
        ("Bascule en DE - card 1", "'Tiersitting' + 'Finde vertrauenswurdige...'"),
        ("Bascule en EN - card 2", "'PawMap' + 'Explore pet-friendly places...'"),
        ("Bascule en IT - card 3", "'PawFollow' + 'Segui le avventure...'"),
        ("Bascule en PT - tagline", "'Pet-sitting, PawMap e acompanhamento...'"),
        ("Pas de Spacer/Padding casse", "Layout correct sur petits ecrans"),
        ("Tests v165 toujours OK", "Samsung nav gris + Invoice label localise"),
        ("Tests v164 toujours OK", "Airwallex / cancel 72h / halos / no auto-logout"),
    ]
    rows = [["Test", "Attendu"]] + tests
    story.append(make_table(rows, col_widths=[7 * cm, 8 * cm]))

    story.append(Spacer(1, 0.5 * cm))
    story.append(p(
        "Cette v166 cloture le marathon avec un onboarding screen polish "
        "selon le mockup designe par Daniel. L'app est maintenant prete "
        "pour TestFlight iOS et un release Android. Rebuild iOS via la "
        "procedure section 5.",
        NOTE,
    ))

    doc.build(story)
    print(f"OK PDF v166 genere : {OUTPUT}")
    print(f"   Taille : {os.path.getsize(OUTPUT) // 1024} Ko")


if __name__ == "__main__":
    build()
