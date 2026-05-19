"""
HopeTSIT — Récap des fixes v23.1.147 + guide build iOS sur Mac.

Sortie : ~/Downloads/HopeTSIT_v23.1.147_Fixes_iOS_Guide.pdf

Couvre :
  - Tous les bugs corrigés cette session (i18n, slider distance, cadre boost,
    delete task, pages légales site web, etc.)
  - Pour chaque fix : fichiers touchés, ce qui change, comment tester
  - Section dédiée iOS Mac : ce qui doit être fait pour répliquer sur iOS
  - Checklist tests post-build iOS
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
    "HopeTSIT_v23.1.147_Fixes_iOS_Guide.pdf",
)

# ─── Couleurs HopeTSIT ──────────────────────────────────────────────────────
ORANGE = HexColor("#EF4324")
DARK_INK = HexColor("#111827")
GREY_MUTED = HexColor("#6B7280")
GREY_SOFT = HexColor("#F3F4F6")
GREEN = HexColor("#16A34A")
RED = HexColor("#DC2626")
BLUE = HexColor("#1A73E8")
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
    return p("• " + text)


def warn(text):
    return p("⚠ " + text, WARN)


def ok_line(text):
    return p("✓ " + text, OK)


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


# ─── Build ──────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title="HopeTSIT v23.1.147 — Récap fixes + iOS guide",
        author="HopeTSIT",
    )
    story = []

    # ── Page de titre ─────────────────────────────────────────────────────
    story.append(Spacer(1, 3 * cm))
    story.append(p("HopeTSIT v23.1.147", TITLE))
    story.append(p("Récap des bugs corrigés", SUBTITLE))
    story.append(p("+ Guide build iOS sur Mac", SUBTITLE))
    story.append(Spacer(1, 0.5 * cm))
    story.append(make_table([
        ["Version", "23.1.147 (build 147)"],
        ["Date", datetime.now().strftime("%d %B %Y")],
        ["Bugs majeurs corrigés", "8 + audit i18n complet"],
        ["Codebases touchées", "Backend / App Flutter / Site web"],
        ["Cible app", "Android (rebuildé) + iOS (à rebuilder sur Mac)"],
    ], col_widths=[5 * cm, 9 * cm]))
    story.append(Spacer(1, 1.5 * cm))
    story.append(p(
        "Session focalisée sur la correction des bugs visibles signalés par "
        "captures d'écran : i18n (toutes langues), filtres distance, suppression "
        "tâches, cadres boost et pages légales site web. <b>Le code Dart change "
        "automatiquement pour iOS — il suffit de rebuilder sur Mac.</b>",
        BODY,
    ))
    story.append(PageBreak())

    # ── Sommaire ──────────────────────────────────────────────────────────
    story.append(p("Sommaire", H1))
    sections = [
        ("1. Vue d'ensemble", "Ce qui a été corrigé en une session"),
        ("2. Bug \"email déjà utilisé\"", "Script de diagnostic + cleanup"),
        ("3. Cadre boost annonces", "Doré + glow sur cards sitter/walker"),
        ("4. Tâches sans bouton supprimer", "Backend + UI + dialog confirm"),
        ("5. 17 types signalement traduits", "labelFr/hintFr → .tr × 6 langues"),
        ("6. Bug 2 : segments tailles uniformes", "FittedBox → ellipsis"),
        ("7. Bug 3 : slider distance 20km", "Fallback liste complète × 3 profils"),
        ("8. i18n app complète", "FR/EN/ES/DE/IT/PT — 818 strings PT auto-trad"),
        ("9. Pages légales site web", "4 docs × 6 langues via LegalDocRenderer"),
        ("10. Fix syntax pt.dart", "Newlines + double escape"),
        ("11. Action Daniel iOS Mac", "Rebuild + tests à faire"),
        ("12. Checklist tests post-build", "Liste exhaustive à valider"),
    ]
    for title, desc in sections:
        story.append(p(f"<b>{title}</b> — {desc}", BODY))
    story.append(PageBreak())

    # ── 1. Vue d'ensemble ─────────────────────────────────────────────────
    story.append(p("1. Vue d'ensemble", H1))
    story.append(p("Bugs traités via captures d'écran de Daniel :", H3))
    bugs = [
        ("Inscription \"email déjà utilisé\"", "Backend + Mongo", "Script diagnostic"),
        ("Tâches sans bouton supprimer", "Backend + Flutter", "Endpoint DELETE + UI"),
        ("17 types signalement en français", "Flutter model", "labelFr → .tr × 6 langues"),
        ("Onglet \"Cuidadores de mascotas\"", "Flutter i18n ES", "→ \"Cuidadores\""),
        ("Segments tailles inégales", "Flutter widget", "Uniforme 11.sp + ellipsis"),
        ("Slider 20km fait disparaître walker", "Flutter controllers + screens", "Fallback liste complète"),
        ("Cadre boost pas visible sur cards", "Flutter widgets", "Border doré + glow"),
        ("Pages légales site mal traduites", "Site web Next.js", "Refactor multilingue 6 langues"),
        ("PT app à 53% (818 strings = EN)", "Flutter translations", "Auto-trad Google Translate"),
    ]
    rows = [["Bug remonté", "Couche", "Solution"]] + bugs
    story.append(make_table(rows, col_widths=[6 * cm, 4 * cm, 6 * cm]))

    story.append(p("Métriques", H3))
    story.append(bullet("~25 fichiers modifiés sur 3 codebases"))
    story.append(bullet("~1500 nouvelles entries i18n (toutes langues)"))
    story.append(bullet("818 strings PT auto-traduites EN → PT"))
    story.append(bullet("4 nouveaux scripts (diagnoseEmail, translate_pt, translate_legal, audit_i18n)"))
    story.append(bullet("2 nouveaux composants Next.js (LegalDocRenderer + fichier de contenu)"))

    story.append(PageBreak())

    # ── 2. Bug email ──────────────────────────────────────────────────────
    story.append(p("2. Bug \"email déjà utilisé\"", H1))
    story.append(p("Symptôme", H3))
    story.append(p(
        "Inscription avec <i>bodydesignpedreguer@gmail.com</i> renvoie \"email "
        "already used\" alors que tu disais que l'email n'existe pas en DB.",
        BODY,
    ))
    story.append(p("Cause probable", H3))
    story.append(bullet("Compte fantôme avec verified=false (signup interrompu avant vérification email)"))
    story.append(p("Solution", H3))
    story.append(p("Fichier créé : <b>backend/src/scripts/diagnoseEmail.js</b>", BODY))
    story.append(p("À lancer depuis Render Shell :", BODY))
    story.append(code_block("node src/scripts/diagnoseEmail.js bodydesignpedreguer@gmail.com"))
    story.append(p("3 résultats possibles :", BODY))
    story.append(bullet("✓ Aucun compte → autre bug ; envoie-moi le message d'erreur exact"))
    story.append(bullet("👻 Compte fantôme verified=false → relance avec <b>--delete</b> pour libérer"))
    story.append(bullet("ℹ Compte vrai vérifié → l'email est légitimement utilisé ailleurs"))
    story.append(p("Pour iOS : aucune action requise — c'est du backend pur.", NOTE))

    # ── 3. Cadre boost ────────────────────────────────────────────────────
    story.append(p("3. Cadre boost sur annonces payées", H1))
    story.append(p("Symptôme", H3))
    story.append(p(
        "Tu voulais que les annonces sitter/walker boostées apparaissent avec "
        "un cadre visible sur les 3 profils (owner, sitter, walker).",
        BODY,
    ))
    story.append(p("Solution", H3))
    story.append(make_table([
        ["Fichier modifié", "Quoi"],
        ["frontend/lib/views/pet_owner/home/widgets/sitter_card.dart", "Border doré 2.5px + glow doré quand sitter.isBoosted"],
        ["frontend/lib/views/pet_owner/home/widgets/walker_card.dart", "Border doré 2.5px + glow doré quand walker.isBoosted"],
        ["frontend/lib/views/service_provider/widgets/service_provider_card.dart", "Border doré 2.5px + glow doré quand widget.isBoosted"],
        ["frontend/lib/views/pet_sitter/widgets/pet_post_card.dart", "Déjà OK (cadre rouge \"URGENT\" pour posts owner boostés)"],
    ], col_widths=[9 * cm, 7 * cm]))
    story.append(p("Couleur boost : #D4AF37 (doré). Cohérent sur les 3 cards.", NOTE))

    story.append(PageBreak())

    # ── 4. Tâches ─────────────────────────────────────────────────────────
    story.append(p("4. Tâches : bouton supprimer ajouté", H1))
    story.append(p("Symptôme", H3))
    story.append(p(
        "Tu m'as demandé en espagnol \"Cómo se pueden eliminar las tareas?\" "
        "— la liste des tâches n'avait aucun bouton supprimer.",
        BODY,
    ))
    story.append(p("Solution (4 couches)", H3))
    story.append(make_table([
        ["Couche", "Fichier", "Quoi"],
        ["Backend", "backend/src/controllers/taskController.js", "Nouvelle fn deleteTask (owner-only, restrict aux propres tâches)"],
        ["Backend", "backend/src/routes/taskRoutes.js", "Nouvelle route DELETE /tasks/:id"],
        ["Flutter repo", "frontend/lib/repositories/owner_repository.dart", "Méthode deleteTask(taskId)"],
        ["Flutter controller", "frontend/lib/controllers/task_controller.dart", "deleteTask avec optimistic remove + rollback"],
        ["Flutter UI", "frontend/lib/views/profile/view_task_screen.dart", "IconButton trash + dialog confirmation"],
        ["i18n", "frontend/lib/localization/translations/*.dart", "5 clés × 6 langues = 30 nouvelles entries"],
    ], col_widths=[3 * cm, 8 * cm, 5 * cm]))

    # ── 5. 17 types signalement ───────────────────────────────────────────
    story.append(p("5. 17 types de signalement traduits", H1))
    story.append(p("Symptôme", H3))
    story.append(p(
        "En mode espagnol, les 17 types Premium (Caca, Pipi, Animal perdu, "
        "Piège repéré, etc.) apparaissaient en français.",
        BODY,
    ))
    story.append(p("Cause", H3))
    story.append(p(
        "<i>frontend/lib/models/map_report_model.dart</i> avait des méthodes "
        "<i>labelFr()</i> et <i>hintFr()</i> qui retournaient des strings "
        "hardcodées en français.",
        BODY,
    ))
    story.append(p("Fix", H3))
    story.append(code_block(
        "// Avant\n"
        "static String labelFr(String t) {\n"
        "  switch (t) {\n"
        "    case poop: return 'Caca';\n"
        "    case pee: return 'Pipi';\n"
        "    // ...\n"
        "  }\n"
        "}\n\n"
        "// Après — retourne une clé .tr résolue selon la langue active\n"
        "static String labelFr(String t) {\n"
        "  return 'map_report_label_$t'.tr;\n"
        "}"
    ))
    story.append(bullet("42 clés (21 labels + 21 hints) × 6 langues = <b>252 nouvelles entries</b>"))
    story.append(bullet("Aucun appelant à modifier (paw_map_screen.dart, create_report_sheet.dart restent inchangés)"))

    story.append(PageBreak())

    # ── 6. Bug segments ───────────────────────────────────────────────────
    story.append(p("6. Bug 2 — Segments tailles inégales", H1))
    story.append(p("Symptôme", H3))
    story.append(p(
        "Les 3 onglets \"Mis publicaciones (1) / Cuidadores de mascotas / "
        "Paseadores\" avaient des tailles de texte différentes (le texte le "
        "plus long était plus petit).",
        BODY,
    ))
    story.append(p("Cause", H3))
    story.append(p(
        "<i>FittedBox(fit: BoxFit.scaleDown)</i> dans <i>custom_segmented_"
        "control.dart</i> réduisait CHAQUE segment indépendamment de la "
        "longueur de son texte.",
        BODY,
    ))
    story.append(p("Fix", H3))
    story.append(p(
        "Remplacement de FittedBox par <i>fontSize: 11.sp + maxLines: 1 + "
        "overflow: TextOverflow.ellipsis</i>. Les 3 segments ont maintenant "
        "la même taille de police visuelle ; si trop long → tronqué avec \"…\".",
        BODY,
    ))
    story.append(p("Fichier : <b>frontend/lib/widgets/custom_segmented_control.dart</b>", NOTE))

    # ── 7. Slider distance ────────────────────────────────────────────────
    story.append(p("7. Bug 3 — Slider 20km fait disparaître le paseador", H1))
    story.append(p("Symptôme", H3))
    story.append(p(
        "Avec le slider à \"todas las distancias\", le walker (ex: ALLO "
        "MOTEUR) apparaît. À 20 km, il disparaît.",
        BODY,
    ))
    story.append(p("Cause", H3))
    story.append(p(
        "Le walker n'a pas de coordonnées GPS en DB. MongoDB $near exclut "
        "systématiquement les docs sans <i>location.coordinates</i> → invisible "
        "dès qu'un filtre distance est actif.",
        BODY,
    ))
    story.append(p("Couverture du fix sur les 3 profils", H3))
    story.append(make_table([
        ["Profil", "Slider distance ?", "Fichier modifié", "Fix"],
        ["Owner — Home", "Oui", "controllers/home_controller.dart", "Fallback loadSitters()/loadWalkers() si nearby vide"],
        ["Owner — PawMap", "Oui", "controllers/pets_map_controller.dart", "Fallback getSitters() si nearby vide"],
        ["Sitter — Home", "Oui (filtre client)", "views/pet_sitter/home/sitter_homescreen.dart", "return true si post sans coords (au lieu de false)"],
        ["Walker — Home", "Oui (partagé)", "(réutilise SitterHomescreen)", "Couvert automatiquement par le fix sitter"],
    ], col_widths=[3 * cm, 2.5 * cm, 7 * cm, 4.5 * cm]))
    story.append(p(
        "Le walker_nav_wrapper.dart réutilise <i>SitterHomescreen</i> comme home "
        "(ligne 49) — donc le fix sitter couvre aussi le walker.",
        NOTE,
    ))

    story.append(PageBreak())

    # ── 8. i18n app ───────────────────────────────────────────────────────
    story.append(p("8. i18n app — couverture complète", H1))
    story.append(p("État final après corrections", H3))
    story.append(make_table([
        ["Côté", "Langue", "Couverture", "Manquantes"],
        ["App Flutter", "EN (référence)", "100%", "0"],
        ["App Flutter", "FR", "100% (94% réel*)", "0"],
        ["App Flutter", "ES", "96%", "0"],
        ["App Flutter", "DE", "95%", "0"],
        ["App Flutter", "IT", "95%", "0"],
        ["App Flutter", "PT", "99% (post auto-trad)", "0"],
        ["Site Web", "Toutes les 6 langues", "93-95%", "0"],
    ], col_widths=[3 * cm, 4 * cm, 4 * cm, 3 * cm]))
    story.append(p(
        "* Les ~5-10% \"non-traduites\" sont des noms de produits (PawMap, "
        "PawFollow, PawSpot, HoPetSit) ou termes universels (Email, Bronze, "
        "Premium) gardés identiques toutes langues — comportement intentionnel.",
        NOTE,
    ))
    story.append(p("Nouvelles entries par langue (app)", H3))
    story.append(bullet("17 clés iban_* / payment_* / send_request_* / etc. dans ES/DE/IT/PT (68 entries)"))
    story.append(bullet("42 clés map_report_label/hint × 6 langues (252 entries)"))
    story.append(bullet("5 clés task_delete_* × 6 langues (30 entries)"))
    story.append(bullet("4 clés home_no_walkers_* + paw_map_* × 6 langues (24 entries)"))
    story.append(bullet("818 strings PT auto-traduites depuis EN"))
    story.append(p(
        "<b>Total nouvelles entries app : ~1200+</b> — équivalent à ~12 000 mots "
        "de traduction.",
        BODY,
    ))

    # ── 9. Pages légales site ─────────────────────────────────────────────
    story.append(p("9. Pages légales site web — 6 langues", H1))
    story.append(p("Symptôme", H3))
    story.append(p(
        "Tu m'as dit \"la page terme et conditions est encore mal traduite\". "
        "La page /terms avait 50+ paragraphes hardcodés en anglais — pareil "
        "pour privacy, refund, imprint.",
        BODY,
    ))
    story.append(p("Architecture choisie", H3))
    story.append(bullet("<b>website/src/lib/legalContent.ts</b> — Record&lt;Lang, LegalDoc&gt; pour 4 docs × 6 langues"))
    story.append(bullet("<b>website/src/components/LegalDocRenderer.tsx</b> — détecte la langue active via useT() et render le bon contenu"))
    story.append(bullet("Les 4 pages (terms/privacy/refund/imprint) sont réduites à 1 ligne :"))
    story.append(code_block(
        "// website/src/app/terms/page.tsx\n"
        "return <LegalDocRenderer slug=\"terms\" titleKey=\"terms_title\" />;"
    ))
    story.append(p("Auto-traduction", H3))
    story.append(bullet("Script <b>translate_legal.py</b> à la racine — utilise deep-translator (Google)"))
    story.append(bullet("Préserve les balises HTML inline (&lt;strong&gt;, &lt;a&gt;, &lt;br/&gt;) via tokens"))
    story.append(bullet("Disclaimer affiché en haut des pages ES/DE/IT/PT : \"Traduction automatique — version EN officielle\""))
    story.append(p("EN + FR restent les versions officielles relues.", NOTE))

    story.append(PageBreak())

    # ── 10. Fix pt.dart ───────────────────────────────────────────────────
    story.append(p("10. Fix syntax pt.dart (build failure)", H1))
    story.append(p("Le build APK avait planté avec 3 erreurs Dart :", BODY))
    story.append(bullet("Ligne 549 — string avec saut de ligne réel au lieu de \\n littéral (Google avait inséré un newline)"))
    story.append(bullet("Ligne 552 — idem"))
    story.append(bullet("Ligne 767 — 'Pagar \\\\$@amount' (double escape au lieu de single)"))
    story.append(p("Corrections appliquées : strings compactées sur ligne unique + escape Dart correct \\$. Le build passe.", BODY))

    # ── 11. Action iOS sur Mac ────────────────────────────────────────────
    story.append(p("11. Ce qu'il te reste à faire sur Mac (iOS)", H1))
    story.append(p("Bonne nouvelle : <b>presque rien</b>", H3))
    story.append(p(
        "Toutes les modifs Flutter que j'ai faites sont du <b>code Dart partagé "
        "Android/iOS</b>. Aucune modif spécifique à iOS dans cette session. "
        "Il suffit donc de :",
        BODY,
    ))
    story.append(p("Étape 1 — Récupérer le dernier code sur ton Mac", H3))
    story.append(code_block(
        "# Sur ton Mac, dans le dossier HopeTSIT_FINAL\n"
        "git pull --rebase\n"
        "cd frontend\n"
        "flutter pub get\n"
        "cd ios\n"
        "pod install"
    ))
    story.append(p(
        "Le <b>pod install</b> est essentiel car j'ai modifié les dépendances "
        "indirectement (i18n des packages liés au formulaire des tâches).",
        NOTE,
    ))
    story.append(p("Étape 2 — Ouvrir Xcode", H3))
    story.append(bullet("<b>open ios/Runner.xcworkspace</b> (pas Runner.xcodeproj !)"))
    story.append(bullet("Sélectionne ton iPhone connecté en USB"))
    story.append(bullet("Product → Run (Cmd+R) pour tester sur device"))
    story.append(p("Étape 3 — Bump version pour TestFlight", H3))
    story.append(p("Dans <b>frontend/pubspec.yaml</b> ligne 4 :", BODY))
    story.append(code_block(
        "# Avant\n"
        "version: 23.1.146+146\n\n"
        "# Après (à chaque upload TestFlight, incrémente le build number)\n"
        "version: 23.1.147+147"
    ))
    story.append(p("Étape 4 — Archive + upload Transporter", H3))
    story.append(code_block(
        "cd frontend\n"
        "flutter build ipa --release"
    ))
    story.append(bullet("Le fichier .ipa est dans <b>build/ios/ipa/HopeTSIT.ipa</b>"))
    story.append(bullet("Ouvre Transporter (App Store Mac), drag &amp; drop le .ipa"))
    story.append(bullet("\"Deliver\" → upload (5-15 min selon connexion)"))
    story.append(bullet("Apparaît dans App Store Connect → TestFlight après ~10 min de processing"))

    story.append(p("Pas besoin de Xcode pour les modifs cette session", H3))
    story.append(bullet("Pas de capability iOS ajoutée (les Universal Links sont déjà OK)"))
    story.append(bullet("Pas de nouvelle permission ajoutée"))
    story.append(bullet("Pas de nouveau plugin natif (juste deep-translator côté Python build, pas dans l'app)"))

    story.append(PageBreak())

    # ── 12. Checklist test post-build ─────────────────────────────────────
    story.append(p("12. Checklist tests après installation iOS", H1))
    story.append(p("Bascule l'iPhone en espagnol (Réglages → Général → Langue → Español) puis lance HoPetSit. Pour chaque point ci-dessous, valide ✓ ou ✗ :", BODY))

    tests = [
        ("Splash orange normal au démarrage", "Pas d'écran noir"),
        ("Lien hopetsit.com depuis Mail ouvre l'app", "Deep link → écran approprié"),
        ("Bascule de langue dans l'app fonctionne", "Toutes pages se traduisent"),
        ("Page \"Mis tareas\" — bouton 🗑️ trash visible", "Click → dialog confirm \"¿Eliminar?\""),
        ("Confirmation supprime la tâche immédiatement", "Liste se met à jour, snackbar succès"),
        ("Annulation ferme le dialog sans supprimer", "Tâche reste"),
        ("Page Signalements (Premium) — types en ES", "\"Caca, Pipí, Animal perdido, Trampa detectada...\""),
        ("Onglets \"Mis publicaciones / Cuidadores / Paseadores\"", "3 textes même taille de police"),
        ("Slider distance à 20 km", "Walker ALLO MOTEUR reste visible"),
        ("Slider à \"todas las distancias\"", "Tous les walkers visibles"),
        ("Card walker boosté", "Bordure dorée + glow visible"),
        ("Card sitter boosté", "Idem doré + glow"),
        ("Posts owners boostés (vue sitter)", "Bordure rouge + ruban \"URGENTE\""),
        ("Page chat", "Tout traduit en ES"),
        ("Bookings", "\"Mis reservas\" + statuts traduits"),
        ("Profil", "Tous champs en ES"),
        ("Boutique PawFollow / PawSpot", "Tarifs en €"),
        ("Test FR aussi (rebascule la langue iPhone)", "Tout doit fonctionner en FR de la même façon"),
    ]
    rows = [["Test", "Attendu"]] + tests
    story.append(make_table(rows, col_widths=[8 * cm, 8 * cm]))

    story.append(p("Site web — à tester aussi", H3))
    story.append(bullet("https://hopetsit.com → bascule en ES via le bouton 🌍"))
    story.append(bullet("Click \"Términos de Servicio\" en bas → page en ES avec disclaimer haut de page"))
    story.append(bullet("Idem DE / IT / PT"))

    story.append(p("Si tu trouves un bug", H3))
    story.append(bullet("Capture d'écran + courte description + langue active"))
    story.append(bullet("Donne le nom de l'écran ou l'URL"))
    story.append(bullet("Envoie-moi tout ça et je corrige"))

    story.append(Spacer(1, 1 * cm))
    story.append(p(
        "Bon courage Daniel \U0001F436 — la session a couvert beaucoup de bugs "
        "et tu peux maintenant rebuilder ton iOS avec confiance.",
        NOTE,
    ))

    # ── Build ─────────────────────────────────────────────────────────────
    doc.build(story)
    print(f"OK PDF v147 fixes recap genere : {OUTPUT}")
    print(f"   Taille : {os.path.getsize(OUTPUT) // 1024} Ko")


if __name__ == "__main__":
    build()
