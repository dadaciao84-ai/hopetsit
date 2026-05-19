"""
HopeTSIT - Recap des fixes v23.1.151 + guide build iOS sur Mac.

Sortie : ~/Downloads/HopeTSIT_v23.1.151_Fixes_iOS_Guide.pdf

Daniel : "paw spot le bouton publier signalement et aussi pas traduit , sur
la version 149 le boost sur la page publication dans le profil owner je vois
pas mon annonce avec cadre urgent comme sur walker et sitter vois je veux
comme sa fais le et verifie les traductions aussi de tte les langue".

Cette session :
  1. Owner voit ses propres posts boostes avec cadre URGENT rouge dans
     "Mes publications" (MyPostsScreen)
  2. Bouton 'Publier le signalement' + 'Envoi...' traduits
  3. AUDIT EXHAUSTIF des strings hardcoded restantes dans paw_map_screen
     et create_report_sheet : 30 nouvelles cles x 6 langues = 180 entries
     (filter chips, snackbars, validation messages, time formats, fallback
     names)
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
    "HopeTSIT_v23.1.151_Fixes_iOS_Guide.pdf",
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
        title="HopeTSIT v23.1.151 - Owner boost frame + audit i18n final",
        author="HopeTSIT",
    )
    story = []

    # Page de titre
    story.append(Spacer(1, 3 * cm))
    story.append(p("HopeTSIT v23.1.151", TITLE))
    story.append(p("Owner voit ses posts boostes + audit i18n exhaustif", SUBTITLE))
    story.append(p("+ Guide build iOS sur Mac", SUBTITLE))
    story.append(Spacer(1, 0.5 * cm))
    story.append(make_table([
        ["Version", "23.1.151"],
        ["Date", datetime.now().strftime("%d %B %Y")],
        ["Fixes", "2 (owner boost frame + bouton publier traduit)"],
        ["Audit i18n", "30 nouvelles cles x 6 langues = 180 entries"],
        ["Total i18n session", "v149: 36 + v150: 22 + v151: 30 = 88 nouvelles cles"],
        ["Codebases touchees", "App Flutter (3 fichiers + 6 i18n)"],
    ], col_widths=[5 * cm, 9 * cm]))
    story.append(Spacer(1, 1.5 * cm))
    story.append(p(
        "Daniel : <i>\"paw spot le bouton publier signalement et aussi pas "
        "traduit, sur la version 149 le boost sur la page publication dans "
        "le profil owner je vois pas mon annonce avec cadre urgent comme "
        "sur walker et sitter vois je veux comme sa fais le et verifie les "
        "traductions aussi de tte les langue\"</i>",
        BODY,
    ))
    story.append(PageBreak())

    # Sommaire
    story.append(p("Sommaire", H1))
    sections = [
        ("1. Vue d'ensemble v151", "2 fixes + audit i18n exhaustif"),
        ("2. Owner voit son propre post boost", "Cadre URGENT rouge dans MyPostsScreen"),
        ("3. Bouton 'Publier le signalement'", "Traduit + bouton 'Envoi...' pendant submit"),
        ("4. Audit i18n PawMap final", "Filter chips, snackbars, time formats..."),
        ("5. Tableau recap des cles ajoutees", "30 nouvelles cles dans cette session"),
        ("6. Action Daniel iOS Mac", "Procedure rebuild standard"),
        ("7. Checklist tests v151", "Owner boost frame + langues sur PawMap"),
    ]
    for title, desc in sections:
        story.append(p(f"<b>{title}</b> - {desc}", BODY))
    story.append(PageBreak())

    # 1. Vue d'ensemble
    story.append(p("1. Vue d'ensemble v151", H1))
    story.append(p("Demandes traitees", H3))
    rows = [
        ["Demande", "Couche", "Solution"],
        ("Bouton 'Publier le signalement' pas traduit", "Flutter sheet", "+2 cles i18n (Envoi.../Publier...)"),
        ("Owner voit pas son post boost avec cadre URGENT", "Flutter profile", "MyPostsScreen passe isOwnerBoosted au PetPostCard"),
        ("Verifie traductions de toutes les langues", "Flutter i18n", "Audit exhaustif 30 cles x 6 langues"),
    ]
    story.append(make_table(rows, col_widths=[7 * cm, 3 * cm, 6 * cm]))

    story.append(p("Strings hardcoded trouvees par l'audit", H3))
    story.append(bullet("Filter chips au-dessus de la map (POIs / Signalements 48h / Amis / Demandes / Perdu / Chien méchant / Point d'eau)"))
    story.append(bullet("Validation snackbars CreateReportSheet (Premium requis / Type requis / Signalement envoye / Envoi impossible)"))
    story.append(bullet("Bouton submit du CreateReportSheet (Envoi.. / Publier le signalement)"))
    story.append(bullet("Snackbars PawMap (Aucune position trouvee pour..., Tes amis ne voient plus..., Signalement prolonge de 12h, Merci un moderateur..)"))
    story.append(bullet("Time-ago labels (X min, X h, X j)"))
    story.append(bullet("Default fallback names (Walker / Sitter / Demande)"))
    story.append(bullet("Confirmations inline (X confirmation(s))"))

    story.append(PageBreak())

    # 2. Owner boost frame
    story.append(p("2. Owner voit son propre post boost", H1))
    story.append(p("Symptome", H3))
    story.append(p(
        "Daniel : sur v149, le cadre rouge URGENT autour des posts boostes "
        "n'apparaissait que cote sitter / walker. L'owner, en regardant ses "
        "propres publications dans \"Mes publications\", ne voyait pas de "
        "difference visuelle entre un post boost et un post normal.",
        BODY,
    ))
    story.append(p("Cause", H3))
    story.append(p(
        "Dans <i>frontend/lib/views/pet_owner/posts/my_posts_screen.dart</i>, "
        "les 2 appels a <i>PetPostCard</i> (un par chemin de rendu : avec et "
        "sans pet image) ne passaient PAS le parametre <i>isOwnerBoosted</i>. "
        "Le widget recevait donc isOwnerBoosted=false par defaut, et la "
        "bordure URGENT ne s'affichait jamais.",
        BODY,
    ))
    story.append(p("Fix", H3))
    story.append(code_block(
        "// MyPostsScreen - 2 PetPostCard calls\n"
        "PetPostCard(\n"
        "  userName: post.owner.name,\n"
        "  // ... autres params\n"
        "  ownerViewOfOwnPost: true,\n"
        "  // v23.1.151 - NOUVEAU\n"
        "  isOwnerBoosted: post.isOwnerBoosted,\n"
        "  ownerBoostTier: post.ownerBoostTier,\n"
        ")"
    ))
    story.append(p(
        "Le backend <i>postRoutes.js /posts/my</i> route deja vers le meme "
        "controller <i>listPosts</i> qui enrichit <i>isOwnerBoosted</i>. "
        "Donc post.isOwnerBoosted est correct cote frontend - il fallait "
        "juste le forwarder au widget.",
        NOTE,
    ))
    story.append(p("Resultat visuel quand boost actif :", H3))
    story.append(bullet("Bordure rouge 2px (#E8472A) autour du post card"))
    story.append(bullet("Boxshadow rouge subtil (blur 16px)"))
    story.append(bullet("Ruban URGENT en haut de la card (FR: 'URGENT', et traduit dans les autres langues via la cle existante)"))
    story.append(bullet("Daniel voit ainsi visuellement que son achat de boost a bien pris effet"))

    story.append(PageBreak())

    # 3. Bouton publier
    story.append(p("3. Bouton 'Publier le signalement' traduit", H1))
    story.append(p("Symptome", H3))
    story.append(p(
        "Daniel : \"paw spot le bouton publier signalement et aussi pas "
        "traduit\". Le bouton submit du CreateReportSheet (qui s'affiche "
        "quand on tape \"Signaler\" sur la PawMap) etait hardcoded en "
        "francais.",
        BODY,
    ))
    story.append(p("Fix", H3))
    story.append(code_block(
        "// Avant\n"
        "text: submitting ? 'Envoi...' : 'Publier le signalement',\n\n"
        "// Apres\n"
        "text: submitting\n"
        "    ? 'pawmap_btn_submit_sending'.tr\n"
        "    : 'pawmap_btn_submit'.tr,"
    ))
    story.append(p("Traductions par langue", H3))
    rows = [
        ["Langue", "Etat 'Envoi...'", "Etat repos 'Publier le signalement'"],
        ["FR", "Envoi...", "Publier le signalement"],
        ["EN", "Sending...", "Publish report"],
        ["ES", "Enviando...", "Publicar senalamiento"],
        ["DE", "Wird gesendet...", "Meldung veroeffentlichen"],
        ["IT", "Invio...", "Pubblica segnalazione"],
        ["PT", "A enviar...", "Publicar sinalizacao"],
    ]
    story.append(make_table(rows, col_widths=[2 * cm, 4 * cm, 8 * cm]))

    story.append(PageBreak())

    # 4. Audit i18n
    story.append(p("4. Audit i18n PawMap final", H1))
    story.append(p("Strategie - grep + 3 passes d'injection", H3))
    story.append(p(
        "1ere passe (v149) : section headers du sheet + appbar PawMap + "
        "snackbars geoloc - 36 cles<br/>"
        "2eme passe (v150) : descriptions tiers PawSpot + confirm dialog + "
        "marker tooltips - 22 cles<br/>"
        "3eme passe (v151, cette session) : bouton submit + filter chips + "
        "validation snacks + time formats + fallback names - 30 cles",
        BODY,
    ))
    story.append(p("Verification par grep apres patch", H3))
    story.append(code_block(
        "# Recherche strings hardcoded restantes\n"
        "grep -nE '(text|title|message): \"[^\"]{3,}\"' \\\n"
        "  paw_map_screen.dart \\\n"
        "  create_report_sheet.dart | grep -v '.tr'\n\n"
        "# Resultat apres v151 : seules restent les chaines non-UI\n"
        "# (URLs, emojis, format de coordonnees, etc.)"
    ))

    story.append(p("Strings restantes (NON-UI, ignorees a dessein)", H3))
    story.append(bullet("'PawMap' (nom du produit - non traduit par design)"))
    story.append(bullet("'POIs' (acronyme accepte dans toutes les langues)"))
    story.append(bullet("Format '${count}' / '${km} km' (juste des nombres)"))
    story.append(bullet("Coordonnees lat/lng (format technique)"))

    story.append(PageBreak())

    # 5. Tableau recap des 30 cles
    story.append(p("5. Tableau recap des 30 nouvelles cles", H1))
    keys = [
        ("pawmap_btn_submit", "Publier le signalement / Publish report..."),
        ("pawmap_btn_submit_sending", "Envoi... / Sending..."),
        ("pawmap_time_min_short", "@n min / @n min (DE: @n Min.)"),
        ("pawmap_time_hours_short", "@n h / @n h (DE: @n Std.)"),
        ("pawmap_time_days_short", "@n j / @n d (IT: @n g, DE: @n T.)"),
        ("pawmap_remaining_hours_label", "@hours h restantes / @hours h left"),
        ("pawmap_default_walker/sitter/request", "Walker / Sitter / Demande (et traductions)"),
        ("pawmap_filter_pois/reports_48h/friends/requests", "POIs / Signalements 48h / Amis / Demandes"),
        ("pawmap_filter_lost/aggressive_dog/water_point", "Perdu / Chien mechant / Point d'eau"),
        ("pawmap_snack_premium_required", "Premium requis / Premium required..."),
        ("pawmap_snack_type_required_title/msg", "Type requis + 'Choisis un type...'"),
        ("pawmap_snack_sent_title/msg", "Signalement envoye + 'Visible 48h...'"),
        ("pawmap_snack_send_failed_title/msg", "Envoi impossible + 'Reessaie dans un instant.'"),
        ("pawmap_snack_city_not_found_msg", "'Aucune position trouvee pour @city.'"),
        ("pawmap_snack_search_failed_msg", "'Verifiez votre connexion et reessayez.'"),
        ("pawmap_snack_tracking_off/on_msg", "'Tes amis ne voient plus...' / 'Tes amis voient...'"),
        ("pawmap_snack_extended_msg", "'Signalement prolonge de 12h.'"),
        ("pawmap_snack_reported_msg", "'Merci, un moderateur va verifier.'"),
        ("pawmap_confirmations_inline", "@count confirmation(s)"),
    ]
    rows = [["Cle i18n", "Texte FR / traductions exemples"]] + keys
    story.append(make_table(rows, col_widths=[7.5 * cm, 8 * cm]))

    story.append(PageBreak())

    # 6. Action iOS
    story.append(p("6. Ce qu'il te reste a faire sur Mac (iOS)", H1))
    story.append(p("Procedure standard", H3))
    story.append(code_block(
        "# Sur ton Mac, dans le dossier HopeTSIT_FINAL\n"
        "git pull --rebase\n"
        "# Tu dois voir le commit v23.1.151\n\n"
        "cd frontend\n"
        "flutter pub get\n"
        "cd ios && pod install\n"
        "open Runner.xcworkspace\n\n"
        "# Bump pubspec.yaml : version: 23.1.151+151\n"
        "flutter build ipa --release\n"
        "# Drag&drop build/ios/ipa/HopeTSIT.ipa dans Transporter"
    ))
    story.append(p("Aucune nouvelle dependance native dans cette session.", NOTE))

    # 7. Checklist
    story.append(p("7. Checklist tests v151", H1))

    tests = [
        ("Profil owner - Mes publications - post sans boost", "Card normale, pas de bordure rouge"),
        ("Profil owner - Acheter boost en mode staff", "Snackbar succes"),
        ("Profil owner - Mes publications (retourner)", "Card avec bordure rouge + ruban URGENT en haut"),
        ("Acheter Platinum boost - mes publications", "Ruban 'URGENT - Boost Platinum'"),
        ("Boost expire - mes publications", "Card revient en mode normal (refresh)"),
        ("PawMap - tap FAB Signaler - bouton submit", "'Publier le signalement' (FR) ou traduction"),
        ("Bouton submit pendant envoi", "'Envoi...' avec spinner"),
        ("Bascule EN - bouton submit", "'Publish report' / 'Sending...'"),
        ("Bascule ES - bouton submit", "'Publicar senalamiento' / 'Enviando...'"),
        ("Bascule DE - bouton submit", "'Meldung veroeffentlichen' / 'Wird gesendet...'"),
        ("Bascule IT - bouton submit", "'Pubblica segnalazione' / 'Invio...'"),
        ("Bascule PT - bouton submit", "'Publicar sinalizacao' / 'A enviar...'"),
        ("PawMap - filter chips au-dessus de la map", "Tous traduits selon la langue active"),
        ("PawMap - snackbar 'Suivi active' apres tap Live", "Titre + message traduits"),
        ("CreateReportSheet sans choisir type, tap submit", "Snackbar 'Type requis' traduit"),
        ("Tests v150 toujours OK", "4 tiers PawSpot, descriptions, confirm dialog"),
        ("Tests v149 toujours OK", "Halo geoloc bleu, cadre owner boost, i18n PawMap"),
    ]
    rows = [["Test", "Attendu"]] + tests
    story.append(make_table(rows, col_widths=[7.5 * cm, 8 * cm]))

    story.append(Spacer(1, 1 * cm))
    story.append(p(
        "Cette v151 cloture l'audit i18n exhaustif de la PawMap (sheet "
        "Signaler, filter chips, snackbars, time formats). Le PawSpot est "
        "couvert depuis v150 (4 tiers + descriptions + dialog). Daniel peut "
        "maintenant tester toutes les langues sur ces ecrans en confiance.",
        NOTE,
    ))

    doc.build(story)
    print(f"OK PDF v151 fixes recap genere : {OUTPUT}")
    print(f"   Taille : {os.path.getsize(OUTPUT) // 1024} Ko")


if __name__ == "__main__":
    build()
