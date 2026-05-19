"use client";

/**
 * v23.1.147 — Composant générique qui render un doc légal multilingue.
 *
 * Prend un slug ('terms' | 'privacy' | 'refund' | 'imprint') et lit le
 * contenu depuis `lib/legalContent.ts` selon la langue active du
 * LanguageProvider.
 *
 * Inclut un disclaimer pour les langues auto-traduites (toutes sauf EN
 * et FR qui sont les versions officielles relues par Daniel).
 *
 * Usage :
 *   <LegalDocRenderer slug="terms" titleKey="terms_title" />
 */

import { LegalPage } from "@/components/LegalPage";
import { useT } from "@/lib/i18n/LanguageProvider";
import { LEGAL_DOCS, type LegalDocSlug, type LegalSection } from "@/lib/legalContent";

const OFFICIAL_LANGS = new Set(["en", "fr"]);

export function LegalDocRenderer({
  slug,
  titleKey,
}: {
  slug: LegalDocSlug;
  titleKey: string;
}) {
  // v23.1.147 — useT() expose { lang, setLang, t } — pas besoin d'un hook séparé.
  const { t, lang } = useT();
  const doc = LEGAL_DOCS[slug][lang] ?? LEGAL_DOCS[slug].en;
  const isAutoTranslated = !OFFICIAL_LANGS.has(lang);

  return (
    <LegalPage title={t(titleKey)} lastUpdated={doc.lastUpdated}>
      {isAutoTranslated && (
        <div
          className="mb-6 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-900"
          role="note"
        >
          ℹ️ {t("legal_auto_translated_notice")}
        </div>
      )}
      {doc.sections.map((s, i) => renderSection(s, i))}
    </LegalPage>
  );
}

function renderSection(section: LegalSection, key: number) {
  if (section.type === "h2") {
    return (
      <h2 key={key} dangerouslySetInnerHTML={{ __html: section.html }} />
    );
  }
  if (section.type === "p") {
    return (
      <p key={key} dangerouslySetInnerHTML={{ __html: section.html }} />
    );
  }
  if (section.type === "ul") {
    return (
      <ul key={key}>
        {section.html.map((item, j) => (
          <li key={j} dangerouslySetInnerHTML={{ __html: item }} />
        ))}
      </ul>
    );
  }
  return null;
}
