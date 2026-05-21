"""
HopeTSIT v23.1.166 - PDF explicatif COMPLET du backup.

Sortie : ~/Downloads/HopeTSIT_FULL_BACKUP_GUIDE_v23.1.166.pdf

Contenu :
  - Vue d'ensemble du projet (3 codebases)
  - Comment restaurer le backup
  - Architecture technique (Flutter / Node.js / Next.js)
  - Variables d'environnement requises
  - Procedure de deploiement (Render + iOS + Android + Vercel)
  - Recap des 18 versions v149 -> v166
  - Conventions de code + scripts d'injection i18n
  - Liens utiles + acces externes
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
    "HopeTSIT_FULL_BACKUP_GUIDE_v23.1.166.pdf",
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
WARN = ParagraphStyle("Warn", parent=base["BodyText"], fontSize=9.5, textColor=RED,
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
        title="HopeTSIT FULL BACKUP GUIDE v23.1.166",
        author="HopeTSIT",
    )
    story = []

    # Page de titre
    story.append(Spacer(1, 2.5 * cm))
    story.append(p("HopeTSIT v23.1.166", TITLE))
    story.append(p("Guide complet du backup + restauration", SUBTITLE))
    story.append(p("Marketplace pet-sitting Flutter / Node.js / Next.js", SUBTITLE))
    story.append(Spacer(1, 0.5 * cm))
    story.append(make_table([
        ["Fichier backup", "HopeTSIT_FULL_BACKUP_v23.1.166.zip (323 MB)"],
        ["Version", "23.1.166 (commit b68882d)"],
        ["Date backup", datetime.now().strftime("%d %B %Y")],
        ["Fichiers inclus", "1439 (376 MB raw, 323 MB zippes)"],
        ["3 codebases", "backend (Node.js) + frontend (Flutter) + website (Next.js)"],
        ["Git history", "Inclus (.git 192 MB)"],
        ["Exclusions", "node_modules / build / .gradle / .dart_tool / .next / .env"],
    ], col_widths=[5 * cm, 9 * cm]))
    story.append(Spacer(1, 1 * cm))
    story.append(p(
        "Ce document accompagne le backup complet du projet HopeTSIT (marketplace "
        "de pet-sitting multi-platforme). Il explique l'architecture, la procedure "
        "de restauration, les variables d'environnement requises, et le recap des "
        "18 versions developpees pendant le marathon (v149 -> v166).",
        BODY,
    ))
    story.append(PageBreak())

    # Sommaire
    story.append(p("Sommaire", H1))
    sections = [
        ("1. Vue d'ensemble du projet", "Marketplace + 3 codebases + stack technique"),
        ("2. Restauration du backup", "Comment extraire et relancer le projet"),
        ("3. Architecture - Backend Node.js", "Express + MongoDB Atlas + Airwallex + FCM"),
        ("4. Architecture - Frontend Flutter", "GetX + 6 langues + Android/iOS"),
        ("5. Architecture - Website Next.js", "Vercel + universal links + pages legales"),
        ("6. Variables d'environnement", "Backend + Frontend + Website"),
        ("7. Procedure de deploiement", "Render + TestFlight + Play Store + Vercel"),
        ("8. Recap des 18 versions v149 -> v166", "~29 bugs / ~920 entries i18n"),
        ("9. Scripts utiles dans le repo", "8 injection i18n + 7 PDF builders"),
        ("10. Comptes & acces externes", "Render / Vercel / Airwallex / Firebase / GitHub"),
        ("11. Travail restant / known issues", "Apres TestFlight v166"),
    ]
    for title, desc in sections:
        story.append(p(f"<b>{title}</b> - {desc}", BODY))
    story.append(PageBreak())

    # 1. Vue d'ensemble
    story.append(p("1. Vue d'ensemble du projet", H1))
    story.append(p("HopeTSIT - Marketplace pet-sitting", H3))
    story.append(p(
        "App mobile multi-roles (owner / sitter / walker) qui connecte les "
        "proprietaires d'animaux avec des prestataires de confiance pour la "
        "garde, le pet-sitting, et les promenades. Features cles :",
        BODY,
    ))
    story.append(bullet("Marketplace de reservations avec paiement integre (Airwallex)"))
    story.append(bullet("PawMap : carte interactive des POIs pet-friendly (vetos, parcs...)"))
    story.append(bullet("PawSpot : boost de visibilite sur la map (4 tiers bronze/silver/gold/platinum)"))
    story.append(bullet("PawFollow : abonnement Premium (Monthly / Yearly / Family)"))
    story.append(bullet("Live tracking en temps reel pendant les promenades (Socket.io)"))
    story.append(bullet("Chat in-app entre owner et provider apres paiement"))
    story.append(bullet("Notifications push + email + in-app (FCM + Nodemailer)"))
    story.append(bullet("72h cancellation rule pour les 3 roles avec refund integral"))
    story.append(bullet("App disponible en 6 langues : EN / FR / ES / DE / IT / PT"))

    story.append(p("Structure des codebases", H3))
    story.append(code_block(
        "HopeTSIT_FINAL/\n"
        " backend/        - Node.js Express API (deployed on Render)\n"
        "  src/\n"
        "   controllers/    (~30 controllers : booking, post, payment...)\n"
        "   models/         (Mongoose schemas)\n"
        "   routes/         (Express routes)\n"
        "   services/       (Airwallex, PayPal, FCM, etc.)\n"
        "   middleware/     (auth, ownerContext, etc.)\n"
        "   locales/        (i18n notifications.json 6 langues)\n"
        " frontend/       - Flutter app (Android + iOS)\n"
        "  lib/\n"
        "   views/          (Screens par role : owner / sitter / walker)\n"
        "   controllers/    (GetX state mgmt)\n"
        "   repositories/   (API client wrappers)\n"
        "   models/         (Dart models)\n"
        "   services/       (Socket, location, deep_link, etc.)\n"
        "   widgets/        (Custom widgets reutilisables)\n"
        "   localization/   (translations/ : 6 fichiers .dart)\n"
        " website/        - Next.js 14 (deployed on Vercel)\n"
        "  src/app/         (App router routes : terms/privacy/...)\n"
        "  src/lib/         (LegalDocRenderer + i18n)\n"
        "  public/.well-known/ (apple-app-site-association + assetlinks.json)\n"
        " inject_*.py     - Scripts d'injection i18n (8 scripts)\n"
        " build_pdf_*.py  - Scripts de generation PDF (7 scripts)\n"
        " create_backup.py - Ce script de backup"
    ))

    story.append(PageBreak())

    # 2. Restauration
    story.append(p("2. Restauration du backup", H1))
    story.append(p("Etape 1 - Extraire le ZIP", H3))
    story.append(code_block(
        "# Windows (PowerShell)\n"
        "Expand-Archive -Path ~/Downloads/HopeTSIT_FULL_BACKUP_v23.1.166.zip ^\n"
        "  -DestinationPath ~/HopeTSIT_RESTORED\n\n"
        "# Mac / Linux\n"
        "unzip ~/Downloads/HopeTSIT_FULL_BACKUP_v23.1.166.zip ^\n"
        "  -d ~/HopeTSIT_RESTORED"
    ))

    story.append(p("Etape 2 - Reinstaller les dependances (3 sous-projets)", H3))
    story.append(code_block(
        "cd ~/HopeTSIT_RESTORED\n\n"
        "# Backend Node.js\n"
        "cd backend && npm install\n"
        "# (Recree node_modules - 312 MB exclu du backup)\n\n"
        "# Frontend Flutter\n"
        "cd ../frontend && flutter pub get\n"
        "# (Recree .dart_tool - 108 MB exclu du backup)\n\n"
        "# Website Next.js\n"
        "cd ../website && npm install\n"
        "# (Recree node_modules - 478 MB exclu du backup)"
    ))

    story.append(p("Etape 3 - Restaurer les variables d'env", H3))
    story.append(p(
        "Le backup EXCLUT les fichiers .env (donnees sensibles). Il faut les "
        "restaurer manuellement depuis ton password manager (1Password, "
        "Bitwarden, etc.). Voir section 6 pour la liste complete des vars.",
        WARN,
    ))

    story.append(p("Etape 4 - Tester localement", H3))
    story.append(code_block(
        "# Backend\n"
        "cd backend && npm run dev   # Express sur localhost:3000\n\n"
        "# Frontend Flutter (emulateur Android ou device)\n"
        "cd frontend && flutter run\n\n"
        "# Website Next.js\n"
        "cd website && npm run dev   # localhost:3001"
    ))

    story.append(p("Etape 5 - Verifier que git history est intact", H3))
    story.append(code_block(
        "cd ~/HopeTSIT_RESTORED\n"
        "git log --oneline | head -20\n"
        "# Tu dois voir les derniers commits v149 -> v166\n"
        "# Ex : b68882d docs: v23.1.166 PDF iOS\n"
        "#      f3bea26 feat(v23.1.166): onboarding redesign\n"
        "#      ..."
    ))

    story.append(PageBreak())

    # 3. Backend
    story.append(p("3. Architecture - Backend Node.js", H1))
    story.append(p("Stack technique", H3))
    story.append(bullet("<b>Runtime</b> : Node.js 20.x"))
    story.append(bullet("<b>Framework</b> : Express 4.x"))
    story.append(bullet("<b>Base de donnees</b> : MongoDB Atlas (cloud)"))
    story.append(bullet("<b>ORM</b> : Mongoose"))
    story.append(bullet("<b>Auth</b> : JWT (HS256, 30 jours)"))
    story.append(bullet("<b>Payment</b> : Airwallex (Pay-In + Payout)"))
    story.append(bullet("<b>Email</b> : Nodemailer (SMTP)"))
    story.append(bullet("<b>Push</b> : Firebase Cloud Messaging (FCM)"))
    story.append(bullet("<b>Real-time</b> : Socket.io"))
    story.append(bullet("<b>Hosting</b> : Render.com (Web Service auto-deploy)"))
    story.append(bullet("<b>Storage</b> : Cloudinary (images) + Airwallex (payment data)"))

    story.append(p("Endpoints principaux (~80 routes)", H3))
    story.append(make_table([
        ["Categorie", "Endpoints"],
        ("Auth", "/auth/login, /auth/signup, /auth/google, /auth/apple, /auth/exchange"),
        ("Users", "/owners/me, /sitters/me, /walkers/me, /users/me/benefits"),
        ("Bookings", "/bookings, /bookings/:id/create-payment-intent, /bookings/:id/self-cancel"),
        ("Posts (annonces)", "/posts, /posts/my, /posts/requests, /posts/media"),
        ("Applications", "/applications, /applications/my, /applications/:id/respond"),
        ("Map", "/map-pois/nearby, /map-reports/nearby, /walkers/nearby, /sitters/nearby"),
        ("Payment", "/airwallex/checkout, /airwallex/webhook, /owner/payments/methods"),
        ("Premium", "/subscriptions/plans, /subscriptions/subscribe, /subscriptions/status"),
        ("Boost", "/boost/purchase, /boost/status, /map-boost/purchase, /map-boost/status"),
        ("Chat", "/chats, /chats/:id/messages, /chats/:id/mark-read"),
        ("Notifications", "/notifications/my, /notifications/mark-read"),
        ("Walk live", "/walks/start, /walks/active, /walks/end (+ socket walk.position)"),
        ("Invoices", "/invoices/my, /invoices/:id, /invoices/:id/html"),
    ], col_widths=[3.5 * cm, 12 * cm]))

    story.append(PageBreak())

    # 4. Frontend Flutter
    story.append(p("4. Architecture - Frontend Flutter", H1))
    story.append(p("Stack technique", H3))
    story.append(bullet("<b>Framework</b> : Flutter 3.27.x (Dart 3.6)"))
    story.append(bullet("<b>State management</b> : GetX (lightweight, reactive)"))
    story.append(bullet("<b>HTTP client</b> : http package + custom ApiClient"))
    story.append(bullet("<b>Storage</b> : GetStorage (local cache) + flutter_secure_storage (JWT)"))
    story.append(bullet("<b>Maps</b> : google_maps_flutter"))
    story.append(bullet("<b>i18n</b> : GetX translations (6 langues)"))
    story.append(bullet("<b>Push</b> : firebase_messaging + flutter_local_notifications"))
    story.append(bullet("<b>WebView</b> : webview_flutter (paiement Airwallex)"))
    story.append(bullet("<b>Payment SDK</b> : Airwallex Components SDK (via WebView)"))
    story.append(bullet("<b>Deep links</b> : app_links (universal links iOS + app links Android)"))
    story.append(bullet("<b>Image picker</b> : image_picker, image_cropper"))

    story.append(p("Roles et navigation", H3))
    story.append(code_block(
        "lib/views/\n"
        "  splash/         - Splash + auth check\n"
        "  onboarding/     - Ecran d'accueil (v23.1.166 redesign)\n"
        "  auth/           - Login / Signup\n"
        "  pet_owner/      - Tabs Owner :\n"
        "    home/         (Accueil owner)\n"
        "    booking/      (Mes reservations)\n"
        "    chat/         (Conversations)\n"
        "    walk/         (Live walk tracking)\n"
        "    posts/        (Mes annonces)\n"
        "  pet_sitter/     - Tabs Sitter :\n"
        "    home/         (Sitter homescreen avec posts disponibles)\n"
        "    booking/      (Mes reservations sitter)\n"
        "    profile/      (Sitter profile)\n"
        "  pet_walker/     - Tabs Walker :\n"
        "    home/         (Walker homescreen)\n"
        "    booking/      (Mes reservations walker)\n"
        "    profile/      (Walker profile)\n"
        "  map/            - PawMap screen partagee (3 roles)\n"
        "  profile/        - Profil generique\n"
        "  invoices/       - Mes factures\n"
        "  boost/          - Boutique Boost + PawSpot + PawFollow"
    ))

    story.append(p("Localisation - 6 langues", H3))
    story.append(p(
        "Chaque fichier lib/localization/translations/<lang>.dart contient ~2000 cles. "
        "Synchronisation via les scripts inject_*.py a la racine du repo. "
        "Total ~12k entries i18n (~2000 cles x 6 langues).",
        BODY,
    ))

    story.append(PageBreak())

    # 5. Website
    story.append(p("5. Architecture - Website Next.js", H1))
    story.append(p("Stack technique", H3))
    story.append(bullet("<b>Framework</b> : Next.js 14 (App Router)"))
    story.append(bullet("<b>Language</b> : TypeScript"))
    story.append(bullet("<b>Styling</b> : Tailwind CSS"))
    story.append(bullet("<b>i18n</b> : Custom LanguageProvider context (6 langues)"))
    story.append(bullet("<b>Hosting</b> : Vercel (auto-deploy depuis main branch)"))
    story.append(bullet("<b>Domaine</b> : hopetsit.com"))

    story.append(p("Pages principales (29 routes)", H3))
    story.append(make_table([
        ["Route", "But"],
        ("/", "Landing page marketing"),
        ("/login", "Login bridge (one-time token vers app)"),
        ("/signup", "Signup web"),
        ("/pay", "Bridge paiement Airwallex"),
        ("/pay/done", "Confirmation paiement"),
        ("/walk/[bookingId]", "Live walk tracking public"),
        ("/book/[id]", "Detail annonce public"),
        ("/bookings", "Liste reservations user"),
        ("/chat", "Chat web"),
        ("/notifications", "Inbox notifications"),
        ("/terms / /privacy / /refund / /imprint", "Pages legales (6 langues via LegalDocRenderer)"),
        ("/.well-known/apple-app-site-association", "Universal links iOS"),
        ("/.well-known/assetlinks.json", "App links Android"),
    ], col_widths=[5 * cm, 10 * cm]))

    story.append(p("Universal links / App links", H3))
    story.append(p(
        "Le site sert 2 fichiers JSON dans /.well-known/ qui declarent que les "
        "URLs hopetsit.com/* doivent etre interceptees par l'app mobile si "
        "installee. Permet aux emails de contenir des liens https://hopetsit.com/... "
        "qui ouvrent l'app sur mobile et le site sur desktop. Voir backend/src/utils/"
        "emailLinkBuilder.js pour le helper qui genere ces URLs.",
        BODY,
    ))

    story.append(PageBreak())

    # 6. Env vars
    story.append(p("6. Variables d'environnement", H1))
    story.append(p("backend/.env", H3))
    story.append(code_block(
        "# Database\n"
        "MONGODB_URI=mongodb+srv://user:pwd@cluster/dbname\n\n"
        "# Auth\n"
        "JWT_SECRET=<random 64 hex>\n"
        "JWT_EXPIRES_IN=30d\n\n"
        "# Airwallex\n"
        "AIRWALLEX_CLIENT_ID=<from dashboard>\n"
        "AIRWALLEX_API_KEY=<from dashboard>\n"
        "AIRWALLEX_BASE_URL=https://api.airwallex.com\n"
        "AIRWALLEX_WEBHOOK_SECRET=<from dashboard - IMPORTANT pour consents>\n\n"
        "# Cloudinary\n"
        "CLOUDINARY_CLOUD_NAME=hopetsit\n"
        "CLOUDINARY_API_KEY=<...>\n"
        "CLOUDINARY_API_SECRET=<...>\n\n"
        "# Email (Nodemailer SMTP)\n"
        "SMTP_HOST=smtp.gmail.com\n"
        "SMTP_PORT=587\n"
        "SMTP_USER=noreply@hopetsit.com\n"
        "SMTP_PASS=<app password>\n\n"
        "# Firebase (push)\n"
        "FIREBASE_PROJECT_ID=hopetsit\n"
        "FIREBASE_CLIENT_EMAIL=<service account>\n"
        "FIREBASE_PRIVATE_KEY=<service account key>\n\n"
        "# PayPal\n"
        "PAYPAL_CLIENT_ID=<...>\n"
        "PAYPAL_CLIENT_SECRET=<...>\n"
        "PAYPAL_PAYOUT_ENV=live\n\n"
        "# Misc\n"
        "WEBSITE_URL=https://hopetsit.com\n"
        "PORT=3000"
    ))

    story.append(p("frontend/.env", H3))
    story.append(code_block(
        "API_BASE_URL=https://hopetsit-backend.onrender.com/api/v1\n"
        "GOOGLE_MAPS_API_KEY=<from Google Cloud Console>\n"
        "AIRWALLEX_ENV=prod\n"
        "SENTRY_DSN=<...>"
    ))

    story.append(p("website/.env.local", H3))
    story.append(code_block(
        "NEXT_PUBLIC_API_URL=https://hopetsit-backend.onrender.com/api/v1\n"
        "NEXT_PUBLIC_GA_ID=<Google Analytics>"
    ))

    story.append(p("Variables Render (production)", H3))
    story.append(p(
        "Sur Render dashboard, les vars sont configurees dans l'environnement "
        "du service hopetsit-backend. Si tu as perdu le password manager, tu "
        "peux les retrouver via Render → Environment → masque les valeurs.",
        NOTE,
    ))

    story.append(PageBreak())

    # 7. Deploiement
    story.append(p("7. Procedure de deploiement", H1))
    story.append(p("Backend - Render auto-deploy", H3))
    story.append(p(
        "Render est connecte au repo GitHub. Chaque push sur main declenche "
        "automatiquement un deploy. Duree ~2-4 min selon la taille du diff. "
        "Tu n'as RIEN a faire manuellement, sauf surveiller les logs si "
        "quelque chose plante.",
        BODY,
    ))

    story.append(p("Frontend Android - APK release", H3))
    story.append(code_block(
        "cd frontend\n"
        "flutter pub get\n"
        "flutter build apk --release\n"
        "# APK genere dans build/app/outputs/flutter-apk/app-release.apk\n"
        "# (Pour signed bundle Google Play : flutter build appbundle --release)"
    ))

    story.append(p("Frontend iOS - sur Mac uniquement", H3))
    story.append(code_block(
        "# Sur ton Mac\n"
        "git pull --rebase\n"
        "cd frontend\n"
        "flutter pub get\n"
        "cd ios && pod install\n"
        "open Runner.xcworkspace\n"
        "# Dans Xcode : Product -> Archive -> Distribute via Transporter\n"
        "# OU en CLI : flutter build ipa --release\n"
        "# Drag&drop build/ios/ipa/HopeTSIT.ipa dans Transporter -> Deliver"
    ))
    story.append(p("Bump pubspec.yaml ligne 4 a chaque release (ex: 23.1.166+166)", NOTE))

    story.append(p("Website - Vercel auto-deploy", H3))
    story.append(p(
        "Comme Render, Vercel est connecte au repo. Push sur main = deploy "
        "automatique du website. Build Next.js dure ~1-2 min.",
        BODY,
    ))

    story.append(PageBreak())

    # 8. Recap 18 versions
    story.append(p("8. Recap des 18 versions v149 -> v166", H1))
    rows = [
        ["Version", "Theme", "Bugs"],
        ("v149", "PawMap geoloc halo + cadre boost owner", "2"),
        ("v150", "PawSpot tier verif + i18n shop", "1"),
        ("v151", "Submit signalement + i18n exhaustif", "1+"),
        ("v152", "URGENT frame home tab + hues PawSpot", "2"),
        ("v153", "Walker rates 90/120 + Send req + PawFollow plans", "3"),
        ("v154", "No auto-logout + halo + invoice save", "3"),
        ("v155", "Email universal links + 50 replacements", "1"),
        ("v156", "customer_id retire (reverte)", "0"),
        ("v157", "PI CANCELLED detect + enum bug", "2"),
        ("v158", "customer_id restaure pour saved cards", "1"),
        ("v159", "Chat Suivre walker + role halo", "2"),
        ("v160", "72h cancel 3 profils + notifs cross", "3"),
        ("v161", "Halo always-on + Annuler 72h + nav orange", "3"),
        ("v162", "i18n 4 strings hardcoded FR + facture HTML", "4"),
        ("v163", "VRAI fix halo Obx + Samsung dark + Firebase", "3"),
        ("v164", "Samsung nav grey persistant + Invoice label", "2"),
        ("v165", "Onboarding UX initial (less white + bigger chips)", "1"),
        ("v166", "Onboarding redesign complet mockup + descriptions", "1"),
    ]
    story.append(make_table(rows, col_widths=[2 * cm, 11 * cm, 2 * cm]))

    story.append(p("Total : ~35 bugs fixes / ~920 entries i18n / 0 nouvelle dep native", OK))

    story.append(PageBreak())

    # 9. Scripts
    story.append(p("9. Scripts utiles dans le repo", H1))
    story.append(p("Scripts d'injection i18n (8)", H3))
    story.append(make_table([
        ["Script", "But"],
        ("inject_pawmap_i18n.py", "v149 - PawMap chips + appbar + snacks (36 cles)"),
        ("inject_pawspot_i18n.py", "v150 - PawSpot tiers + confirm dialog (22 cles)"),
        ("inject_final_i18n.py", "v151 - submit button + filter chips (30 cles)"),
        ("inject_walker_rates_i18n.py", "v153 - 90/120 min + Pet-sitting (13 cles)"),
        ("inject_post_request_i18n.py", "v153 - post_incomplete_for_request"),
        ("inject_pawfollow_plans_i18n.py", "v153 - Plans Premium 6 langs"),
        ("inject_v154_i18n.py", "v154 - session expired + invoice save"),
        ("inject_cancel_templates.py", "v160 - 12 templates email cancellation"),
        ("inject_cancel_72h_i18n.py", "v161 - cancel_72h dialog 4 cles"),
        ("inject_i18n_v162.py", "v162 - 4 strings hardcoded screenshots"),
        ("inject_onboarding_descs.py", "v166 - 3 descriptions cartes onboarding"),
    ], col_widths=[5 * cm, 10 * cm]))

    story.append(p("Scripts de generation PDF (7)", H3))
    story.append(make_table([
        ["Script", "PDF genere"],
        ("build_pdf_v147_fixes.py", "v147 recap (pre-marathon)"),
        ("build_pdf_v148-v153_fixes.py", "v148 a v153 individuellement"),
        ("build_pdf_v154-v155_fixes.py", "v154 et v155"),
        ("build_pdf_v161_fixes.py", "v161 (consolide v155-v161)"),
        ("build_pdf_v164_fixes.py", "v164 (consolide v149-v164)"),
        ("build_pdf_v165_fixes.py", "v165 (addendum onboarding UX)"),
        ("build_pdf_v166_fixes.py", "v166 (onboarding redesign + i18n verif)"),
        ("build_pdf_full_backup_guide.py", "Ce PDF - guide complet backup"),
    ], col_widths=[6 * cm, 9 * cm]))

    story.append(p("create_backup.py", H3))
    story.append(p(
        "Script qui a genere ce backup. Re-executable a tout moment pour creer "
        "un nouveau snapshot. Exclusions configurables dans EXCLUDED_DIR_NAMES.",
        BODY,
    ))

    story.append(PageBreak())

    # 10. Accès externes
    story.append(p("10. Comptes & acces externes", H1))
    story.append(p("Services tiers utilises", H3))
    story.append(make_table([
        ["Service", "URL dashboard", "But"],
        ("GitHub", "github.com/hopetsit/hopetsit", "Source code + main branch auto-deploys"),
        ("Render.com", "dashboard.render.com", "Backend Node.js Web Service"),
        ("Vercel", "vercel.com/dashboard", "Website Next.js"),
        ("MongoDB Atlas", "cloud.mongodb.com", "Database (hopetsit-cluster)"),
        ("Airwallex", "dashboard.airwallex.com", "Payments (Pay-In + Payout)"),
        ("Firebase", "console.firebase.google.com", "FCM push + Auth Google/Apple"),
        ("Cloudinary", "console.cloudinary.com", "Storage images"),
        ("Google Cloud", "console.cloud.google.com", "Maps API + Sign-in OAuth"),
        ("Apple Developer", "developer.apple.com", "iOS certs + Universal Links"),
        ("Google Play", "play.google.com/console", "Android release"),
        ("App Store Connect", "appstoreconnect.apple.com", "iOS TestFlight + release"),
    ], col_widths=[3 * cm, 5.5 * cm, 6.5 * cm]))

    story.append(p("Compte HoPetSit Hong Kong", H3))
    story.append(bullet("Societe operatrice : CARDELLI HERMANOS LIMITED"))
    story.append(bullet("Hong Kong Company No. n-2671528"))
    story.append(bullet("Email contact : contact@hopetsit.com"))

    story.append(PageBreak())

    # 11. Known issues
    story.append(p("11. Travail restant / known issues", H1))
    story.append(p("Fixes en place mais a verifier sur device", H3))
    story.append(bullet("Halo PawSpot : verifie en code mais besoin de tester sur device avec PawSpot active pour valider visuellement"))
    story.append(bullet("Samsung nav grey : marche en v164/v166 mais a confirmer apres reinstall complet"))
    story.append(bullet("Universal links iOS : depend de la propagation du apple-app-site-association (24-48h apres deploy Vercel)"))

    story.append(p("Bugs non bloquants connus", H3))
    story.append(bullet("Vieux emails pre-v155 contiennent encore des hopetsit:// links → erreur Firebase si cliques. Solution : utiliser uniquement des emails post-v155 ou purger l'inbox"))
    story.append(bullet("Warnings deprecation withOpacity / Share.shareXFiles : a refactor en .withValues / SharePlus.instance.share (~30 occurrences). Non bloquant."))
    story.append(bullet("2 unused _PremiumUpsell + _MapBoostUpsell dans paw_map_screen.dart : dead code reste apres refactor v23.1 part 75. A nettoyer."))

    story.append(p("Features pas encore implementees", H3))
    story.append(bullet("Annulation mutuelle dans la fenetre 72h (currently 409 + message generique)"))
    story.append(bullet("Notification settings granulaires (currently tout ON/OFF)"))
    story.append(bullet("Multi-pet selection dans booking (currently 1 pet par booking)"))
    story.append(bullet("Avis / ratings system apres prestation"))
    story.append(bullet("Dispute resolution flow"))

    story.append(p("Securite a auditer", H3))
    story.append(bullet("Rate limiting actuel : 20 req/60s. Verifier si suffisant pour DDoS protection."))
    story.append(bullet("CSP backend : actuellement strict mais a re-verifier post-changes"))
    story.append(bullet("Webhook Airwallex : signature verifiee SI AIRWALLEX_WEBHOOK_SECRET set. Verifier que c'est le cas sur Render."))

    story.append(Spacer(1, 0.5 * cm))
    story.append(p("Bonne continuation Daniel 🐶 - ton projet est solide.", OK))

    doc.build(story)
    print(f"OK PDF guide complet genere : {OUTPUT}")
    print(f"   Taille : {os.path.getsize(OUTPUT) // 1024} Ko")


if __name__ == "__main__":
    build()
