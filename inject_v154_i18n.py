"""
HopeTSIT v23.1.154 - Inject i18n keys for session-expired snack +
invoice save-to-files tooltip + invoice download progress.
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent
LANG_DIR = ROOT / "frontend" / "lib" / "localization" / "translations"

TRANSLATIONS = {
    "auth_session_expired_title": {
        "fr": "Session expirée",
        "en": "Session expired",
        "es": "Sesión caducada",
        "de": "Sitzung abgelaufen",
        "it": "Sessione scaduta",
        "pt": "Sessão expirada",
    },
    "auth_session_expired_msg": {
        "fr": "Pour continuer, va dans Profil > Déconnecter et reconnecte-toi.",
        "en": "To continue, go to Profile > Logout and sign in again.",
        "es": "Para continuar, ve a Perfil > Cerrar sesión y vuelve a iniciar sesión.",
        "de": "Um fortzufahren, gehe zu Profil > Abmelden und melde dich erneut an.",
        "it": "Per continuare, vai a Profilo > Disconnetti e accedi di nuovo.",
        "pt": "Para continuar, vai a Perfil > Sair e inicia sessão novamente.",
    },
    "invoice_save_to_files": {
        "fr": "Enregistrer dans Fichiers",
        "en": "Save to Files",
        "es": "Guardar en Archivos",
        "de": "In Dateien speichern",
        "it": "Salva su File",
        "pt": "Guardar em Ficheiros",
    },
    "invoice_download_preparing_title": {
        "fr": "Téléchargement…",
        "en": "Downloading…",
        "es": "Descargando…",
        "de": "Wird heruntergeladen…",
        "it": "Scaricamento…",
        "pt": "A descarregar…",
    },
    "invoice_download_preparing_msg": {
        "fr": "Préparation du PDF",
        "en": "Preparing PDF",
        "es": "Preparando PDF",
        "de": "PDF wird vorbereitet",
        "it": "Preparazione PDF",
        "pt": "A preparar PDF",
    },
}


def dart_escape(s):
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")


def inject_into_lang_file(lang_code):
    path = LANG_DIR / f"{lang_code}.dart"
    text = path.read_text(encoding="utf-8")

    anchor = (
        re.search(r"('pawfollow_per_day_suffix':\s*'[^']*',\s*\n)", text)
        or re.search(r"('post_incomplete_for_request':\s*'[^']*',\s*\n)", text)
        or re.search(r"('walker_rate_hint_30':\s*'[^']*',\s*\n)", text)
    )
    if not anchor:
        print(f"  [SKIP] {lang_code}: anchor not found")
        return 0

    new_entries = []
    skipped = 0
    for key, langs in TRANSLATIONS.items():
        if f"'{key}'" in text:
            skipped += 1
            continue
        value = dart_escape(langs[lang_code])
        new_entries.append(f"      '{key}': '{value}',")

    if not new_entries:
        return 0

    insert_at = anchor.end()
    block = "\n".join(new_entries) + "\n"
    new_text = text[:insert_at] + block + text[insert_at:]
    path.write_text(new_text, encoding="utf-8")
    print(f"  [{lang_code}] inserted {len(new_entries)} keys (skipped {skipped})")
    return len(new_entries)


def main():
    print("== Inject v23.1.154 i18n keys ==")
    for lang in ["en", "fr", "es", "de", "it", "pt"]:
        inject_into_lang_file(lang)
    print("== DONE ==")


if __name__ == "__main__":
    main()
