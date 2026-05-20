"""
HopeTSIT v23.1.155 - Migrate email templates from hopetsit:// custom scheme
to universal links via {{emailLink}} template variable.

Daniel : "connecte les boutons quon recois par mail a lapp ou le web".

Avant : "hopetsit://pay/123" -> ouvre l'app si installee, sinon erreur navigateur.
Apres : "{{emailLink}}" -> rendu en https://hopetsit.com/pay?bookingId=123
        -> universal link iOS/Android (ouvre l'app si installee), sinon site web.

6 locale files updated : en/fr/es/de/it/pt notifications.json.
"""

import re
from pathlib import Path

LOCALES_DIR = Path(__file__).parent / "backend" / "src" / "locales"

# Fallback text translated per language (we update the "Si le bouton ne
# fonctionne pas, ouvrez l'app HoPetSit manuellement." sentence to point
# at the actual link instead of telling user to "open the app manually").
FALLBACK_TEXT = {
    "fr": "Si le bouton ne fonctionne pas, copiez-collez ce lien dans votre navigateur : {{emailLink}}",
    "en": "If the button doesn't work, copy this link into your browser: {{emailLink}}",
    "es": "Si el botón no funciona, copia este enlace en tu navegador: {{emailLink}}",
    "de": "Wenn der Button nicht funktioniert, kopiere diesen Link in deinen Browser: {{emailLink}}",
    "it": "Se il pulsante non funziona, copia questo link nel tuo browser: {{emailLink}}",
    "pt": "Se o botão não funcionar, copia este link no teu navegador: {{emailLink}}",
}

OLD_FALLBACK = {
    "fr": [
        "Si le bouton ne fonctionne pas, ouvrez l'app HoPetSit manuellement.",
        "Si le bouton ne fonctionne pas, ouvrez l'application HoPetSit manuellement.",
    ],
    "en": [
        "If the button doesn't work, open the HoPetSit app manually.",
        "If the button does not work, open the HoPetSit app manually.",
    ],
    "es": [
        "Si el botón no funciona, abre la app HoPetSit manualmente.",
    ],
    "de": [
        "Wenn der Button nicht funktioniert, öffnen Sie die HoPetSit-App manuell.",
        "Wenn der Button nicht funktioniert, öffne die HoPetSit-App manuell.",
    ],
    "it": [
        "Se il pulsante non funziona, apri l'app HoPetSit manualmente.",
    ],
    "pt": [
        "Se o botão não funcionar, abra a app HoPetSit manualmente.",
        "Se o botão não funcionar, abre a app HoPetSit manualmente.",
    ],
}


def patch_file(lang_code):
    path = LOCALES_DIR / lang_code / "notifications.json"
    if not path.exists():
        print(f"  [SKIP] {lang_code}: {path} not found")
        return 0
    text = path.read_text(encoding="utf-8")
    original = text

    # Replace ALL hopetsit:// patterns with {{emailLink}}.
    # Common forms found in templates:
    #   hopetsit://pay/{{bookingId}}
    #   hopetsit://bookings/{{bookingId}}
    #   hopetsit://bookings
    #   hopetsit://chat/{{conversationId}}
    # We use a single regex that catches all of them.
    pattern = re.compile(r"hopetsit://[a-zA-Z]+(/\{\{[a-zA-Z]+\}\})?")
    matches = pattern.findall(text)
    new_text = pattern.sub("{{emailLink}}", text)

    # Replace old fallback text with new (link-aware) version.
    fallback_replacements = 0
    for old in OLD_FALLBACK.get(lang_code, []):
        if old in new_text:
            new_text = new_text.replace(old, FALLBACK_TEXT[lang_code])
            fallback_replacements += 1

    if new_text == original:
        print(f"  [{lang_code}] no changes needed")
        return 0

    # Count hopetsit:// replacements
    url_replacements = len(pattern.findall(original))

    path.write_text(new_text, encoding="utf-8")
    print(
        f"  [{lang_code}] {url_replacements} URL replacements + "
        f"{fallback_replacements} fallback text replacements"
    )
    return url_replacements + fallback_replacements


def main():
    print("== Migrate email templates to universal links ==")
    total = 0
    for lang in ["en", "fr", "es", "de", "it", "pt"]:
        total += patch_file(lang)
    print(f"== DONE — {total} replacements across 6 locale files ==")


if __name__ == "__main__":
    main()
