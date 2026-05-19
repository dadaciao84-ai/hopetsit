"""
HopeTSIT — Addendum v23.1.148 (PawMap geoloc + adresse veto autocomplete +
staff Premium badge persistance).

Sortie : ~/Downloads/HopeTSIT_v23.1.148_Fixes_iOS_Guide.pdf

Couvre les 3 bugs traités apres le pousse v147 :
  - PawMap mobile s'ouvre sur Paris au lieu de la geoloc user
  - Champs adresse veto dans modifier animal sans autocomplete
  - PawFollow Premium badge invisible pour les comptes staff

C'est un addendum independant du PDF v147 : tu peux le lire seul. Le guide
iOS reprend les memes etapes (git pull + flutter pub get + pod install +
flutter build ipa) ; seules les zones a re-tester changent.
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
    "HopeTSIT_v23.1.148_Fixes_iOS_Guide.pdf",
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


def warn(text):
    return p("! " + text, WARN)


def ok_line(text):
    return p("v " + text, OK)


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
        title="HopeTSIT v23.1.148 - Addendum fixes + iOS guide",
        author="HopeTSIT",
    )
    story = []

    # Page de titre
    story.append(Spacer(1, 3 * cm))
    story.append(p("HopeTSIT v23.1.148", TITLE))
    story.append(p("Addendum des fixes apres v147", SUBTITLE))
    story.append(p("+ Guide build iOS sur Mac", SUBTITLE))
    story.append(Spacer(1, 0.5 * cm))
    story.append(make_table([
        ["Version", "23.1.148 (commit 0bfee7a)"],
        ["Date", datetime.now().strftime("%d %B %Y")],
        ["Bugs corriges", "3 (PawMap geoloc / adresse veto / staff Premium)"],
        ["Codebases touchees", "Backend (1 route) + App Flutter (3 fichiers)"],
        ["Cible app", "Android (deja rebuilde) + iOS (a rebuilder sur Mac)"],
    ], col_widths=[5 * cm, 9 * cm]))
    story.append(Spacer(1, 1.5 * cm))
    story.append(p(
        "Cette session courte couvre 3 bugs remontes apres la livraison v147 : "
        "<b>PawMap</b> qui s'ouvrait sur Paris au lieu de la position GPS de "
        "l'utilisateur, <b>champs adresse veto</b> sans autocomplete dans "
        "Modifier mon animal, et <b>badge Premium PawFollow</b> qui ne "
        "s'affichait pas en mode staff.",
        BODY,
    ))
    story.append(PageBreak())

    # Sommaire
    story.append(p("Sommaire", H1))
    sections = [
        ("1. Vue d'ensemble v148", "3 fixes en 1 commit"),
        ("2. Bug PawMap ouvre sur Paris", "Timeout geoloc + attente map controller"),
        ("3. Adresse veto autocomplete", "Nouveau widget AddressAutocompleteField"),
        ("4. Badge Premium staff", "Backend persiste UserSubscription pour staff"),
        ("5. Action Daniel iOS Mac", "Procedure rebuild identique a v147"),
        ("6. Checklist tests v148", "Liste a valider apres le rebuild"),
    ]
    for title, desc in sections:
        story.append(p(f"<b>{title}</b> - {desc}", BODY))
    story.append(PageBreak())

    # 1. Vue d'ensemble
    story.append(p("1. Vue d'ensemble v148", H1))
    story.append(p("Bugs remontes par capture / vocal :", H3))
    bugs = [
        ("PawMap s'ouvre sur Paris au lieu de ma geoloc", "Flutter map", "Timeout 8s + await map controller"),
        ("Regler adresse auto dans modifier animal", "Flutter form", "Nouveau widget Nominatim autocomplete"),
        ("PawFollow ne s'affiche pas (badge Premium absent)", "Backend subscription", "Persiste UserSubscription pour staff"),
    ]
    rows = [["Bug remonte", "Couche", "Solution"]] + bugs
    story.append(make_table(rows, col_widths=[7 * cm, 4 * cm, 5 * cm]))

    story.append(p("Metriques", H3))
    story.append(bullet("4 fichiers modifies (3 frontend + 1 backend)"))
    story.append(bullet("1 nouveau widget reutilisable (AddressAutocompleteField)"))
    story.append(bullet("Commit : <b>0bfee7a</b> sur origin/main"))
    story.append(p("Bugs egalement examines mais deja OK :", H3))
    story.append(bullet(
        "Cadre boost owner cote sitter/walker : <i>pet_post_card.dart</i> a "
        "deja un border rouge + ruban URGENT (v23.1 part 116). Le backend "
        "<i>postController.js</i> enrichit deja <i>isOwnerBoosted</i> sur "
        "<i>listPosts</i> + <i>getRequestPosts</i>. Si ca s'affiche pas, "
        "verifier que le boost a bien ete achete et que boostExpiry est > now."
    ))
    story.append(bullet(
        "PawSpot mode staff : le bypass dans <i>mapBoostRoutes.js</i> sauve "
        "deja <i>mapBoostExpiry</i> + tier en DB (lignes 162-192). Le FE "
        "<i>map_boost_controller.dart</i> handle bien la reponse staff. "
        "Si \"ca marche pas\", il faut le detail precis : snackbar erreur ? "
        "pin dore absent sur la carte ? badge profil absent ?"
    ))

    story.append(PageBreak())

    # 2. PawMap Paris
    story.append(p("2. Bug PawMap s'ouvre sur Paris", H1))
    story.append(p("Symptome", H3))
    story.append(p(
        "Tu as dit \"fais que la paw map souvre sur notre geoloc pas a paris\" : "
        "la carte PawMap mobile affichait Paris au lieu de centrer sur la "
        "position GPS de l'utilisateur, meme apres autorisation de la geoloc.",
        BODY,
    ))
    story.append(p("Cause", H3))
    story.append(p(
        "Dans <i>frontend/lib/views/map/paw_map_screen.dart</i>, la methode "
        "<i>_bootstrap()</i> avait 2 problemes :",
        BODY,
    ))
    story.append(bullet(
        "Timeout geoloc a 4s : trop court sur iPhone froid (GPS pas encore "
        "fixe au lancement de l'app)."
    ))
    story.append(bullet(
        "Animation camera skip si <i>_mapCtl.isCompleted == false</i> : "
        "souvent la geoloc resolved AVANT que GoogleMap.onMapCreated ait "
        "fire le Completer, donc l'animateCamera etait jamais appelle - "
        "le _currentCenter etait bien update mais la camera restait sur "
        "le initialCameraPosition (Paris)."
    ))
    story.append(p("Fix", H3))
    story.append(code_block(
        "// AVANT\n"
        "final loc = await LocationService()\n"
        "    .getCurrentLocation()\n"
        "    .timeout(const Duration(seconds: 4), onTimeout: () => null);\n"
        "// ...\n"
        "if (_mapCtl.isCompleted) {  // <-- souvent false !\n"
        "  final ctl = await _mapCtl.future;\n"
        "  await ctl.animateCamera(CameraUpdate.newLatLng(center));\n"
        "}\n\n"
        "// APRES\n"
        "final loc = await LocationService()\n"
        "    .getCurrentLocation()\n"
        "    .timeout(const Duration(seconds: 8), onTimeout: () => null);\n"
        "// ...\n"
        "// Attend explicitement que le controller soit pret (timeout 6s)\n"
        "final ctl = await _mapCtl.future.timeout(\n"
        "  const Duration(seconds: 6),\n"
        "  onTimeout: () => throw TimeoutException('map controller not ready'),\n"
        ");\n"
        "await ctl.animateCamera(CameraUpdate.newLatLngZoom(center, 13));"
    ))
    story.append(p(
        "Le fallback Paris reste comme initial value pour que la 1re frame "
        "rende qqch (au lieu d'un ecran blanc), mais des que la geoloc + le "
        "map controller sont prets, on anime vers la vraie position user.",
        NOTE,
    ))

    story.append(PageBreak())

    # 3. Adresse veto autocomplete
    story.append(p("3. Adresse veto avec autocomplete", H1))
    story.append(p("Symptome", H3))
    story.append(p(
        "Tu as dit \"regler adresse auto ds modifier animal\" : les champs "
        "\"Veterinaire habituel - Adresse\" et \"Veterinaire d'urgence - "
        "Adresse\" etaient de simples TextField sans suggestion, donc faute "
        "de frappe ou ville mal ecrite, l'adresse n'etait pas exploitable.",
        BODY,
    ))
    story.append(p("Solution", H3))
    story.append(bullet(
        "Nouveau widget <b>frontend/lib/widgets/address_autocomplete_field."
        "dart</b> : TextField avec autocomplete Nominatim (OpenStreetMap, "
        "gratuit, pas de cle API a payer)."
    ))
    story.append(bullet(
        "Debounce 400ms, declenche apres 3 caracteres tapes, max 5 suggestions "
        "dans un dropdown sous le champ."
    ))
    story.append(bullet(
        "Tap sur une suggestion = remplit le TextField avec l'adresse complete "
        "+ remonte (lat, lon) via callback <i>onAddressSelected</i> (non "
        "stocke en DB pour l'instant mais dispo si on veut afficher les "
        "vetos sur la PawMap plus tard)."
    ))
    story.append(p("Integration", H3))
    story.append(p(
        "Dans <i>frontend/lib/views/profile/edit_pet_screen.dart</i>, les 2 "
        "appels <i>tf(controller.regularVetAddressController, ...)</i> et "
        "<i>tf(controller.emergencyVetAddressController, ...)</i> ont ete "
        "remplaces par :",
        BODY,
    ))
    story.append(code_block(
        "AddressAutocompleteField(\n"
        "  controller: controller.regularVetAddressController,\n"
        "  label: 'common_address'.tr,\n"
        ")"
    ))
    story.append(p(
        "Service utilise : <b>https://nominatim.openstreetmap.org/search</b> "
        "(meme service que CityLocationPicker pour le champ Ville profil). "
        "Pas de cle API a payer / configurer.",
        NOTE,
    ))

    story.append(PageBreak())

    # 4. Badge Premium staff
    story.append(p("4. Badge Premium PawFollow staff", H1))
    story.append(p("Symptome", H3))
    story.append(p(
        "Tu as dit \"pawfollow ne saffiche pas\" : le badge etoile Premium "
        "(jaune) qui devrait apparaitre dans le header du profil au-dessus "
        "des badges Boost / PawSpot n'apparaissait pas en mode staff.",
        BODY,
    ))
    story.append(p("Cause", H3))
    story.append(p(
        "Le widget <i>ActiveBenefitsRow</i> (header profil owner/sitter/"
        "walker) lit ses flags depuis <i>GET /users/me/benefits</i> qui "
        "calcule <i>isPremium</i> de 2 facons :",
        BODY,
    ))
    story.append(bullet("user.isPremium (champ Owner.isPremium en DB)"))
    story.append(bullet(
        "<i>subscriptionActive</i> = il existe une UserSubscription en "
        "status active dont currentPeriodEnd &gt; now"
    ))
    story.append(p(
        "Probleme : le bypass staff dans <i>POST /subscriptions/subscribe</i> "
        "retournait juste <i>{staff: true, activated: true}</i> SANS rien "
        "persister. Du coup les 2 verifications echouaient :",
        BODY,
    ))
    story.append(bullet("Owner.isPremium = false (jamais update)"))
    story.append(bullet("Aucune UserSubscription en DB pour le user staff"))
    story.append(bullet("Resultat : <i>/users/me/benefits</i> retourne <i>isPremium: false</i>"))
    story.append(p("Fix", H3))
    story.append(p(
        "<i>backend/src/routes/subscriptionRoutes.js</i> ligne ~152 : on "
        "upsert maintenant une vraie UserSubscription active pour le staff, "
        "avec currentPeriodEnd = now + intervalDays (ce qui simule un vrai "
        "achat). La prochaine lecture de /users/me/benefits voit la sub "
        "active et retourne isPremium=true.",
        BODY,
    ))
    story.append(code_block(
        "// AVANT (subscriptionRoutes.js)\n"
        "if (staffUser && staffUser.isStaff) {\n"
        "  return res.json({ staff: true, activated: true, plan, ... });\n"
        "  // <-- rien persiste !\n"
        "}\n\n"
        "// APRES\n"
        "if (staffUser && staffUser.isStaff) {\n"
        "  let sub = await UserSubscription.findOne({ userId, userModel });\n"
        "  const now = new Date();\n"
        "  const startFrom = sub?.currentPeriodEnd > now\n"
        "    ? new Date(sub.currentPeriodEnd) : now;\n"
        "  const newPeriodEnd = new Date(\n"
        "    startFrom.getTime() + pricing.intervalDays * 86_400_000);\n"
        "  if (!sub) sub = new UserSubscription({ userId, userModel });\n"
        "  sub.plan = plan;\n"
        "  sub.status = 'active';\n"
        "  sub.currentPeriodEnd = newPeriodEnd;\n"
        "  sub.features = { ...PREMIUM_FEATURES_DEFAULT };\n"
        "  sub.payments.push({\n"
        "    plan, amount: 0, currency, paidAt: now,\n"
        "    paymentProvider: 'staff_free', ...\n"
        "  });\n"
        "  await sub.save();  // <-- maintenant persiste !\n"
        "  return res.json({ staff: true, activated: true, ... });\n"
        "}"
    ))
    story.append(p(
        "Aucune action requise cote iOS : c'est 100% backend. Apres ce push, "
        "des que tu cliques \"Acheter Premium\" en mode staff, le badge "
        "etoile Premium apparait immediatement dans le header du profil.",
        NOTE,
    ))

    story.append(PageBreak())

    # 5. Action iOS sur Mac
    story.append(p("5. Ce qu'il te reste a faire sur Mac (iOS)", H1))
    story.append(p("Identique a v147 - juste un git pull + rebuild", H3))
    story.append(p(
        "Toutes les modifs Flutter sont du <b>code Dart partage Android/iOS</b>. "
        "Le widget <i>AddressAutocompleteField</i> utilise <i>package:http</i> "
        "qui est deja dans pubspec.yaml. Aucune nouvelle dependance native.",
        BODY,
    ))
    story.append(p("Etape 1 - Recuperer le code v148", H3))
    story.append(code_block(
        "# Sur ton Mac, dans le dossier HopeTSIT_FINAL\n"
        "git pull --rebase\n"
        "# Tu dois voir : 0bfee7a v23.1.148 fixes...\n\n"
        "cd frontend\n"
        "flutter pub get\n"
        "cd ios\n"
        "pod install\n"
        "open Runner.xcworkspace"
    ))
    story.append(p("Etape 2 - Tester sur device avant TestFlight", H3))
    story.append(bullet("Connecte ton iPhone en USB"))
    story.append(bullet("Selectionne ton iPhone dans la barre Xcode"))
    story.append(bullet("Product -> Run (Cmd+R)"))
    story.append(bullet(
        "Va dans PawMap : ca doit centrer sur ta position (Mallorca/Pedreguer) "
        "pas Paris."
    ))
    story.append(bullet(
        "Va dans Profil -> Modifier l'animal -> Veterinaire habituel : tape 3 "
        "lettres dans Adresse, les suggestions doivent apparaitre."
    ))
    story.append(bullet(
        "Achete PawFollow Premium (gratuit pour toi en mode staff) : le "
        "badge etoile jaune doit apparaitre dans le header de ton profil."
    ))
    story.append(p("Etape 3 - Bump version pour TestFlight", H3))
    story.append(p("Dans <b>frontend/pubspec.yaml</b> ligne 4 :", BODY))
    story.append(code_block(
        "# Avant\n"
        "version: 23.1.147+147\n\n"
        "# Apres\n"
        "version: 23.1.148+148"
    ))
    story.append(p("Etape 4 - Archive + upload Transporter", H3))
    story.append(code_block(
        "cd frontend\n"
        "flutter build ipa --release\n"
        "# .ipa dans build/ios/ipa/HopeTSIT.ipa\n"
        "# Drag&drop dans Transporter -> Deliver"
    ))

    story.append(PageBreak())

    # 6. Checklist tests v148
    story.append(p("6. Checklist tests apres installation iOS v148", H1))
    story.append(p(
        "Apres rebuild + install sur device, valide chacun de ces points :",
        BODY,
    ))

    tests = [
        ("PawMap au lancement (1re fois)", "Centre sur ta position GPS, pas Paris"),
        ("PawMap apres avoir refuse la geoloc", "Reste sur Paris (fallback OK)"),
        ("Modifier animal -> Veto habituel adresse", "Tape '5 rue', suggestions apparaissent"),
        ("Click suggestion adresse", "Champ se remplit avec l'adresse complete"),
        ("Modifier animal -> Veto urgence adresse", "Meme comportement"),
        ("Profil owner -> Acheter Premium (staff = gratuit)", "Snackbar 'Premium active'"),
        ("Apres l'achat -> Badge etoile Premium visible", "Dans le header avec Boost / PawSpot"),
        ("Pull-refresh profil", "Badge Premium toujours la"),
        ("Profil sitter -> Acheter Premium (staff)", "Meme badge apparait"),
        ("Profil walker -> Acheter Premium (staff)", "Meme badge apparait"),
        ("Tests v147 toujours OK", "Cadre boost, slider 20km, delete task, i18n ES"),
    ]
    rows = [["Test", "Attendu"]] + tests
    story.append(make_table(rows, col_widths=[8 * cm, 8 * cm]))

    story.append(p("Si un test echoue", H3))
    story.append(bullet("Capture d'ecran + courte description"))
    story.append(bullet("Indique : langue active, role (owner/sitter/walker), staff oui/non"))
    story.append(bullet("Envoie tout ca, je corrige"))

    story.append(Spacer(1, 1 * cm))
    story.append(p(
        "Commit : 0bfee7a sur origin/main. Render auto-deploy le backend ; "
        "le frontend doit etre rebuilde manuellement (Android deja fait par "
        "Claude, iOS a faire par toi sur Mac via les etapes 1-4 ci-dessus).",
        NOTE,
    ))

    doc.build(story)
    print(f"OK PDF v148 fixes recap genere : {OUTPUT}")
    print(f"   Taille : {os.path.getsize(OUTPUT) // 1024} Ko")


if __name__ == "__main__":
    build()
