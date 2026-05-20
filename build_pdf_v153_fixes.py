"""
HopeTSIT - Recap des fixes v23.1.153 + guide build iOS sur Mac.

Sortie : ~/Downloads/HopeTSIT_v23.1.153_Fixes_iOS_Guide.pdf

Daniel : "bug surtout pour le paiement de nouveau bloquer ds le spublication
et demande direct resous tousa".

4 demandes traitees :
  1. Airwallex payment - VERIFICATION (fix de v23.1.61 deja en place)
  2. Tarifs walker 90 + 120 min - AJOUTES
  3. Bouton "demande direct" toujours visible - FIX
  4. Traductions PawFollow Famille/Mensuel/Annuel + descriptions - AJOUTEES
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
    "HopeTSIT_v23.1.153_Fixes_iOS_Guide.pdf",
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
        title="HopeTSIT v23.1.153 - Paiement + tarifs walker + demande directe + PawFollow",
        author="HopeTSIT",
    )
    story = []

    # Page de titre
    story.append(Spacer(1, 3 * cm))
    story.append(p("HopeTSIT v23.1.153", TITLE))
    story.append(p("Paiement + tarifs walker 90/120min + demande directe + PawFollow i18n", SUBTITLE))
    story.append(p("+ Guide build iOS sur Mac", SUBTITLE))
    story.append(Spacer(1, 0.5 * cm))
    story.append(make_table([
        ["Version", "23.1.153"],
        ["Date", datetime.now().strftime("%d %B %Y")],
        ["Demandes traitees", "4 (paiement / tarifs / demande directe / PawFollow i18n)"],
        ["Verifications", "1 (Airwallex fix v23.1.61 toujours en place)"],
        ["i18n ajoutees", "13 cles x 6 langues = 78 entries"],
        ["Codebases touchees", "App Flutter (5 fichiers + 6 i18n)"],
    ], col_widths=[5 * cm, 9 * cm]))
    story.append(Spacer(1, 1.5 * cm))
    story.append(p(
        "Daniel : <i>\"bug surtout pour le paiement de nouveau bloquer ds le "
        "spublication et demande direct resous tousa\"</i> + 4 captures "
        "d'ecran (Airwallex empty page, tarifs walker incomplets, bouton "
        "demande directe absent, PawFollow \"Famille\" en FR dans Spanish UI).",
        BODY,
    ))
    story.append(PageBreak())

    # Sommaire
    story.append(p("Sommaire", H1))
    sections = [
        ("1. Vue d'ensemble v153", "4 demandes traitees + 1 verification"),
        ("2. Airwallex paiement - verification", "Fix v23.1.61 en place, restart app + Render"),
        ("3. Tarifs walker 90 + 120 minutes", "Form etendu de 2 a 4 durees"),
        ("4. Bouton 'Demande directe' - toujours visible", "Callback non-null + validation interne"),
        ("5. PawFollow plan names + descriptions", "Famille/Mensuel/Annuel traduits 6 langues"),
        ("6. Action Daniel iOS Mac", "Procedure rebuild standard"),
        ("7. Checklist tests v153", "Validation 4 fixes + paiement"),
    ]
    for title, desc in sections:
        story.append(p(f"<b>{title}</b> - {desc}", BODY))
    story.append(PageBreak())

    # 1. Vue d'ensemble
    story.append(p("1. Vue d'ensemble v153", H1))
    rows = [
        ["Demande Daniel", "Couche", "Solution / Verdict"],
        ("Paiement Airwallex bloque (que amount, pas de form)", "Backend", "Fix v23.1.61 OK - redeploy + restart app"),
        ("Faltan tarifas 90 + 120 min pour walker", "Flutter form", "Ajout 2 _RateField + 2 controllers"),
        ("Bouton demande directe absent post detail", "Flutter sitter home", "Callback toujours non-null + validation"),
        ("Traductions PawFollow Famille manquantes", "Flutter coin_shop + i18n", "13 nouvelles cles plan + subtitle"),
    ]
    story.append(make_table(rows, col_widths=[7 * cm, 3 * cm, 6 * cm]))

    story.append(p("Total i18n session entiere (v149-v153)", H3))
    story.append(bullet("v149 : 36 cles (sheet + appbar + snacks geoloc)"))
    story.append(bullet("v150 : 22 cles (PawSpot tiers + confirm dialog + marker tooltips)"))
    story.append(bullet("v151 : 30 cles (bouton submit + filter chips + validation + time formats)"))
    story.append(bullet("v152 : 0 cles (hues PawSpot uniquement)"))
    story.append(bullet("v153 : 13 cles (walker rates 90/120 + post_incomplete + PawFollow plans)"))
    story.append(bullet("<b>Total : 101 cles x 6 langues = 606 entries</b>"))

    story.append(PageBreak())

    # 2. Airwallex
    story.append(p("2. Airwallex paiement - verification", H1))
    story.append(p("Symptome", H3))
    story.append(p(
        "Daniel : Airwallex HPP affiche header + montant + footer mais "
        "AUCUN champ de carte. Le user ne peut rien entrer.",
        BODY,
    ))
    story.append(p("Diagnostic - fix deja en place", H3))
    story.append(p(
        "Le bug etait en v23.1.58 : le PI etait cree avec un "
        "<i>payment_consent: { type: 'recurring' }</i> systematiquement, "
        "ce qui faisait croire a Airwallex que c'etait un setup et non "
        "une charge. Resultat : HPP supprimait le form. Le fix est en "
        "v23.1.61 (commit 00e2be9, 6 mai) : on ne joint le payment_consent "
        "QUE si l'utilisateur tique \"Sauvegarder ma carte\".",
        BODY,
    ))
    story.append(p("Backend bookingController.js ligne 2473 - actuel", H3))
    story.append(code_block(
        "...(airwallexCustomerId ? {\n"
        "  customer_id: airwallexCustomerId,\n"
        "  // FIX : attach payment_consent ONLY when user wants to save card\n"
        "  ...(wantsSaveCard && !selectedConsentId ? {\n"
        "    payment_consent: {\n"
        "      type: 'recurring',\n"
        "      next_triggered_by: 'customer',\n"
        "      merchant_trigger_reason: 'unscheduled',\n"
        "    },\n"
        "  } : {}),\n"
        "} : {})"
    ))
    story.append(p("Pourquoi Daniel voit encore le bug", H3))
    story.append(bullet("<b>Cache app</b> : la WebView peut afficher l'ancienne page. Force-quit + relance l'app"))
    story.append(bullet("<b>Render pas redeploye</b> : verifier sur dashboard.render.com qu'il y a un deploy recent (commit b514245 ou plus recent)"))
    story.append(bullet("<b>Test propre</b> : faire le paiement APRES restart app + verification Render deploye"))
    story.append(p("Si le bug persiste apres ces 2 verifications, c'est un NOUVEAU bug et il faut ouvrir les Render logs (cliquer Logs sur le dashboard) au moment ou tu cliques Pay. Le log devrait montrer la PI cree avec ou sans payment_consent.", WARN))

    story.append(PageBreak())

    # 3. Tarifs walker
    story.append(p("3. Tarifs walker 90 + 120 minutes", H1))
    story.append(p("Symptome", H3))
    story.append(p(
        "Daniel : <i>\"Faltarian las tarifas para 90 y 120 minutos\"</i>. Le form "
        "Mes tarifs walker n'avait que 30 min et 60 min.",
        BODY,
    ))
    story.append(p("Backend - aucun changement", H3))
    story.append(p(
        "Le Walker model accepte deja n'importe quelle duree multiple de 15 "
        "entre 15 et 300 minutes. La validation backend "
        "(<i>walkerController.js:421</i>) est conforme. ZERO changement "
        "backend necessaire.",
        BODY,
    ))
    story.append(p("Frontend - 2 nouveaux controllers + 2 _RateField", H3))
    story.append(make_table([
        ["Fichier", "Changement"],
        ("edit_walker_profile_controller.dart", "ninetyMinRateController + twoHourRateController (TextEditingController)"),
        ("edit_walker_profile_controller.dart loadProfileData", "Lit duration=90 et =120 depuis getMyWalkerRates"),
        ("edit_walker_profile_controller.dart updateRatesOnly", "Helper upsertOrRemove(duration, parsed) - vide les durees nullies"),
        ("my_rates_screen.dart", "+2 _RateField widgets entre 60min et bouton Save"),
        ("i18n 6 langues", "walker_rate_90min_label / 120min_label + hint_22/30"),
    ], col_widths=[8 * cm, 8 * cm]))
    story.append(p("Comportement : si tu remplis 90+120 mais vides 30, on retire l'entree 30 du tableau walkRates. Si tu remplis tout, les 4 sont sauvegardes. Au moins 1 doit etre rempli (validation client-side).", NOTE))

    story.append(PageBreak())

    # 4. Demande directe
    story.append(p("4. Bouton 'Demande directe' toujours visible", H1))
    story.append(p("Symptome", H3))
    story.append(p(
        "Daniel : sur le post detail (vu par sitter/walker), seuls les "
        "boutons \"Me gusta\" + \"Compartir\" apparaissent. Le bouton "
        "\"Envoyer une demande\" est absent.",
        BODY,
    ))
    story.append(p("Cause", H3))
    story.append(p(
        "Dans <i>sitter_homescreen.dart ligne 1110</i>, le callback "
        "<i>onSendRequest</i> est defini comme :",
        BODY,
    ))
    story.append(code_block(
        "// AVANT - callback NULL si donnees incompletes\n"
        "onSendRequest: ownerId.isNotEmpty &&\n"
        "    petId != null &&\n"
        "    post.serviceTypes.isNotEmpty\n"
        "  ? () async { ... }\n"
        "  : null,  // <- bouton invisible quand donnees incompletes !\n\n"
        "// Et dans PetPostCard ligne 369 :\n"
        "if (onViewPetDetails != null || onSendRequest != null) {\n"
        "  // ... render le bouton\n"
        "}"
    ))
    story.append(p(
        "Si le post n'a pas <i>ownerId</i>, <i>petId</i>, ou "
        "<i>serviceTypes</i>, le callback etait null → le bouton "
        "disparaissait silencieusement → sitter/walker sans recours.",
        BODY,
    ))
    story.append(p("Fix", H3))
    story.append(code_block(
        "// APRES - callback TOUJOURS non-null, validation a l'interieur\n"
        "onSendRequest: () async {\n"
        "  if (ownerId.isEmpty ||\n"
        "      petId == null ||\n"
        "      post.serviceTypes.isEmpty) {\n"
        "    CustomSnackbar.showError(\n"
        "      title: 'common_error'.tr,\n"
        "      message: 'post_incomplete_for_request'.tr,\n"
        "    );\n"
        "    return;\n"
        "  }\n"
        "  // ... appel _handleSendRequest normal\n"
        "},"
    ))
    story.append(p(
        "Resultat : le bouton est toujours visible. Si la publication est "
        "incomplete, l'utilisateur recoit un snackbar explicite "
        "(\"Cette publication n'a pas toutes les informations necessaires\"). "
        "Le bouton n'est plus invisible silencieusement.",
        OK,
    ))

    story.append(PageBreak())

    # 5. PawFollow i18n
    story.append(p("5. PawFollow plan names + descriptions traduits", H1))
    story.append(p("Symptome", H3))
    story.append(p(
        "Daniel : capture d'ecran avec l'UI en espagnol qui montre toujours "
        "<i>\"PawFollow Famille\"</i> (FR) au lieu de \"Familia\" (ES). De plus, "
        "les sous-titres \"Jusqu'a 5 membres\", \"Facture 1x par an\", "
        "\"Facture tous les mois\" etaient hardcoded FR.",
        BODY,
    ))
    story.append(p("Architecture choisie", H3))
    story.append(p(
        "Le backend (UserSubscription.js:40-44) renvoie <i>label: 'PawFollow "
        "Famille'</i> dans la response /subscriptions/plans. Plutot que "
        "modifier le backend (risque de breaking change), on override sur "
        "le frontend en utilisant <i>plan.plan</i> (clef tech 'monthly'/'yearly'/"
        "'family') comme cle i18n :",
        BODY,
    ))
    story.append(code_block(
        "// coin_shop_screen.dart ligne ~1162\n"
        "// AVANT - utilise le label backend tel quel\n"
        "text: '${plan.label}$savings',  // 'PawFollow Famille'\n\n"
        "// APRES - lookup i18n via la cle technique\n"
        "text: '${('pawfollow_plan_${plan.plan}').tr}$savings',\n"
        "//        ↑ pawfollow_plan_family → 'PawFollow Familia' (ES)"
    ))
    story.append(p("Traductions par langue", H3))
    rows = [
        ["Langue", "Mensuel", "Annuel", "Famille"],
        ("FR", "Mensuel", "Annuel", "Famille"),
        ("EN", "Monthly", "Yearly", "Family"),
        ("ES", "Mensual", "Anual", "Familia"),
        ("DE", "Monatlich", "Jährlich", "Familie"),
        ("IT", "Mensile", "Annuale", "Famiglia"),
        ("PT", "Mensal", "Anual", "Família"),
    ]
    story.append(make_table(rows, col_widths=[2 * cm, 3.5 * cm, 3.5 * cm, 3.5 * cm]))
    story.append(p("Subtitles : \"Facture tous les mois\" devient \"Billed monthly\"/\"Facturado mensualmente\"/etc.", NOTE))
    story.append(p("Suffixe : \"/jour\" devient \"/day\"/\"/día\"/\"/Tag\"/etc.", NOTE))

    story.append(PageBreak())

    # 6. Action iOS
    story.append(p("6. Ce qu'il te reste a faire sur Mac (iOS)", H1))
    story.append(p("Procedure standard", H3))
    story.append(code_block(
        "# Sur ton Mac, dans le dossier HopeTSIT_FINAL\n"
        "git pull --rebase\n"
        "# Tu dois voir le commit v23.1.153\n\n"
        "cd frontend\n"
        "flutter pub get\n"
        "cd ios && pod install\n"
        "open Runner.xcworkspace\n\n"
        "# Bump pubspec.yaml : version: 23.1.153+153\n"
        "flutter build ipa --release\n"
        "# Drag&drop build/ios/ipa/HopeTSIT.ipa dans Transporter"
    ))
    story.append(p("Aucune nouvelle dependance native dans cette session.", NOTE))

    # 7. Checklist
    story.append(p("7. Checklist tests v153", H1))
    tests = [
        ("Force-quit l'app + relance", "Vide le cache de la WebView (preconditions paiement)"),
        ("Verifier sur dashboard.render.com que backend est deploye", "Date du dernier deploy < 5 min"),
        ("Owner achete un walker (10 EUR test)", "Airwallex HPP affiche le form de carte (PAS empty)"),
        ("Walker - Mes tarifs - voir les 4 champs", "30 min / 60 min / 90 min / 120 min"),
        ("Walker - remplir 90 min + 120 min seulement", "Sauvegarde OK, snackbar succes"),
        ("Walker - vider 30 min + 60 min puis save", "Suppression de ces entrees en DB"),
        ("Sitter - voir post avec donnees completes", "Bouton 'Envoyer demande' visible et fonctionnel"),
        ("Sitter - voir post avec petId manquant", "Bouton visible mais click affiche snackbar 'incomplete'"),
        ("Boutique PawFollow - bascule en ES", "'PawFollow Familia' (au lieu de Famille)"),
        ("Boutique PawFollow - bascule en DE/IT/PT", "Labels traduits dans chaque langue"),
        ("Subtitle 'Jusqu'a 5 membres' en ES", "'Hasta 5 miembros • mensual'"),
        ("Suffixe '/jour' en ES", "'/día' (et '/day' en EN, '/Tag' en DE)"),
        ("Tests v152 toujours OK", "Cadre URGENT owner home tab + couleurs PawSpot"),
        ("Tests v151 toujours OK", "Bouton submit traduit + filter chips"),
    ]
    rows = [["Test", "Attendu"]] + tests
    story.append(make_table(rows, col_widths=[7.5 * cm, 8 * cm]))

    story.append(p("Si Airwallex reste bloque apres restart + redeploy", H3))
    story.append(p(
        "Ouvrir Render dashboard → Logs (live tail) → faire un paiement → "
        "chercher la ligne <i>[booking.createPaymentIntent]</i>. Verifier que "
        "<i>wantsSaveCard=false</i> est passe dans le log et que <i>selectedConsent=none</i>. "
        "Si tu vois un payment_consent dans la response Airwallex (chercher "
        "<i>airwallex PI created</i>), c'est qu'il y a une regression. Envoie-moi "
        "le log et je corrige.",
        BODY,
    ))

    story.append(Spacer(1, 1 * cm))
    story.append(p(
        "Cette v153 cloture les 4 demandes Daniel : paiement verifie, tarifs "
        "walker etendus, demande directe toujours visible, PawFollow traduit. "
        "606 entries i18n cumule sur 5 sessions (v149-v153).",
        NOTE,
    ))

    doc.build(story)
    print(f"OK PDF v153 fixes recap genere : {OUTPUT}")
    print(f"   Taille : {os.path.getsize(OUTPUT) // 1024} Ko")


if __name__ == "__main__":
    build()
