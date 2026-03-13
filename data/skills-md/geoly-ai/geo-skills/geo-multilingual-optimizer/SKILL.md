---
name: geo-multilingual-optimizer
description: >
  Multilingual GEO content adaptation and alignment orchestrator. Use this skill whenever the user
  mentions translating, localizing, or adapting GEO-focused content across multiple languages or
  regions, wants AI models to consistently cite the same brand or page in different languages, or
  needs to diagnose why non-English AI answers diverge from their canonical English (or other
  source-language) content. Always consider this skill when GEO and AI citation goals explicitly
  involve more than one language, locale, or market.
---

# GEO Multilingual Optimizer

A workflow skill for **multilingual GEO content adaptation** that ensures:

1. One or more **canonical source assets** (often in English) are clearly defined.
2. Target **languages, locales, and markets** are explicitly mapped.
3. Content is **adapted, not just translated** — preserving GEO intent, entities, and claims.
4. AI-facing signals (structure, schemas, llms.txt, internal links) stay **aligned across languages**.

This skill focuses on **cross-language consistency, localization quality, and AI citation alignment**.
It complements, not replaces, other GEO skills (optimizers, schema generators, llms.txt designers, etc.).

---

## When to use this skill

Invoke this skill **whenever**:

- The user:
  - Has one or more **source-language GEO pages** (often English) and wants **localized versions**.
  - Notices that **AI answers differ by language** (e.g., English vs. Spanish ChatGPT answers).
  - Wants to **expand GEO presence** from one primary language into multiple markets.
  - Needs to **synchronize messaging and entities** across locales (brand names, product names, key terms).
- The request explicitly mentions more than one:
  - **Language** (e.g., English, Spanish, German, Japanese, Arabic, etc.).
  - **Locale or market** (e.g., US, UK, DE, BR, JP, MENA, LATAM).
  - **Script** (e.g., Latin vs. Cyrillic vs. Kanji/Kana vs. Arabic).
- The user asks to:
  - “Make sure AI answers are consistent across languages.”
  - “Localize this GEO page for X, Y, Z languages or countries.”
  - “Fix mismatches between English and non-English AI search / citations.”

Do **not** limit triggering only to obvious keywords like “translate” or “localize”. Trigger whenever
the **intent** is: “Make GEO and AI citation behavior work correctly across multiple languages.”

If the user’s request is **strictly monolingual** (only one language in scope, no cross-language concerns),
prefer using other GEO skills (e.g., `geo-content-optimizer`, `geo-structured-writer`) instead.

---

## Relationship to other GEO skills

When available, this skill should **coordinate** with these skills:

- `geo-studio`: for overall GEO strategy, prioritization of markets, and SoM goals per language.
- `geo-content-optimizer`: to optimize the **source-language** asset before localization.
- `geo-structured-writer`: to ensure each localized page uses AI-readable structure.
- `geo-schema-gen`: to generate per-locale Schema.org JSON-LD (e.g., hreflang, localized metadata).
- `geo-llms-txt`: to expose localized content and language hubs to AI crawlers.
- `geo-multimodal-tagger`: to localize alt text, filenames, and media descriptions by language.

If some of these skills are not present, still follow the **same workflow shape** and:

- Clearly explain what would be done by those skills.
- Provide concrete, copy-pasteable outputs (headings, text blocks, schema templates, llms.txt snippets).

---

## High-level workflow

When this skill is used, follow this **8-step workflow** unless the user explicitly asks for
only a subset.

### 1. Clarify multilingual GEO context

Briefly but explicitly identify:

- **Source language(s) and canonical assets**:
  - Which page(s) or document(s) are considered the **source of truth**?
  - In which language(s) are they currently available?
- **Target languages and locales**:
  - e.g., “Spanish (ES + LATAM)”, “German (DE)”, “Brazilian Portuguese (pt-BR)”, “Japanese (ja-JP)”.
- **Primary GEO goals**:
  - e.g., “Be the default AI answer for [topic] in English + Spanish + German.”
  - “Align product messaging across US, EU, and LATAM markets.”
- **AI behavior today (if known)**:
  - Are there examples where English answers are correct but other languages are wrong or incomplete?
- **Localization constraints**:
  - Legal, regulatory, tone sensitivity, terminology that must not change.
  - Preferences about transliteration vs. translation of brand/product names.

Output a short **“Multilingual Brief”** section summarizing this in 5–10 bullet points.

### 2. Inventory and normalize source content

- Determine whether the **source asset** is:
  - Already GEO-optimized (structured headings, FAQs, schemas, internal links).
  - Still a draft that needs optimization before localization.
- If optimization is needed:
  - Conceptually apply `geo-content-optimizer` and/or `geo-structured-writer`.
  - Ensure the source has:
    - A clear definition section for the topic/entity.
    - Stable terminology for key concepts and product names.
    - A concise FAQ that AI can safely quote.
- Identify **canonical entities and terms** that must be preserved across languages:
  - Brand name, product line, feature names.
  - Legal or regulated phrases that must not be loosely adapted.

Produce a concise **“Source Content Readiness”** section with:

- Key strengths and gaps for multilingual GEO.
- The list of **must-preserve entities/terms** (with short English explanations).
- A note on whether you will optimize inline or assume another skill handles it.

### 3. Design language and locale mapping

Create a **language–market mapping plan** that connects each source asset to its localized
variants and target markets.

- For each target language/locale, define:
  - **Market role** (primary vs. secondary; strategic vs. experimental).
  - **Preferred writing style** (formal vs. informal, B2B vs. B2C, local jargon tolerance).
  - **Localization depth**:
    - “Light translation” for informational parity.
    - “Full localization” with local examples, pricing, references.
  - **AI citation target**:
    - Which URL(s) should be the main citation targets in that language?
- Map hreflang and canonical relationships conceptually:
  - Which page is canonical per language?
  - Which pages are alternates across locales?

Output this as a **markdown table**, e.g.:

```markdown
| Language / Locale | Market Role | Depth of Localization | Target GEO URL             | Notes                         |
|-------------------|------------|------------------------|----------------------------|-------------------------------|
| en-US             | Primary    | Full                   | https://example.com/en-us  | Canonical source              |
| en-GB             | Secondary  | Light                  | https://example.com/en-gb  | Shares content with en-US     |
| es-ES             | Primary    | Full                   | https://example.com/es-es  | Local examples, EU compliance |
| es-MX             | Primary    | Full                   | https://example.com/es-mx  | LATAM focus                   |
```

### 4. Build a multilingual terminology and style guide

To avoid fragmented AI answers and inconsistent citations, define a **multilingual term map**.

- For each key entity or concept, specify:
  - **Source term** (usually English).
  - Approved translations or transliterations per language.
  - Notes on when to keep the English term (e.g., product names, trademarks).
  - Tone/style notes (e.g., avoid slang in DE B2B content).
- Include:
  - How to handle abbreviations and acronyms.
  - How to write numbers, dates, and currencies per locale.
  - Sensitive topics or claims that must be softened or expanded in certain markets.

Output:

- A section `## Multilingual Terminology Map` with a markdown table per language.
- Clear instructions to **reuse these exact forms** when generating localized content and schemas.

### 5. Generate localized GEO page structures

For each target language/locale, design or refine **page outlines and key sections** that are:

- Structurally parallel to the source (so AI can map them).
- Adapted for local expectations (examples, legal notes, CTAs).
- Friendly for AI citation:
  - Clear definitions.
  - Self-contained explanations.
  - Localized FAQs.

For each language/locale, output under `## Localized Page Blueprints`:

- `### [Language / Locale]`
  - A short description of audience and tone.
  - A markdown outline like:

```markdown
# [Localized H1 focused on the same entity/topic]
## Summary
- 2–4 bullets in the target language.

## What is [Topic]?
Localized explanation that preserves the factual meaning.

## Why it matters in [Market]
Local-angle benefits, risks, regulations if relevant.

## How [Brand/Product] helps
Localized positioning, proof, and CTA.

## FAQ
Q1 (localized):
A1 (localized, fact-focused).

Q2 (localized):
A2 (localized).
```

Emphasize where content can diverge (local proof points) vs. where it must stay aligned
(core definitions, core claims).

### 6. Align structured data and AI signals across languages

For web and longform surfaces, design a **multilingual structured data plan**:

- Conceptually apply `geo-schema-gen` to:
  - Generate `WebPage`, `Article`, `FAQPage`, or `Product` schemas per language.
  - Ensure localized `headline`, `description`, and `inLanguage` fields.
  - Define canonical + `alternate` relationships where relevant.
- Include recommendations for:
  - `hreflang` annotations.
  - `lang` attributes on HTML tags.
  - Consistent URL patterns per locale (e.g., `/en/`, `/es/`, `/de/`).
- For media:
  - Use or conceptually apply `geo-multimodal-tagger` to propose localized:
    - Alt text.
    - File names (where appropriate).
    - `ImageObject` / `VideoObject` metadata per language.

Output:

- A section `## Multilingual Structured Data Package` including:
  - Example JSON-LD snippets for at least two languages.
  - A table mapping “Language/Locale → URL → Schema Types → hreflang group”.

### 7. Plan AI crawler and llms.txt exposure for localized content

Design how localized content should be **surfaced to AI crawlers and generative engines**:

- Sitemaps:
  - Recommend per-locale sitemaps or language-segmented sections.
  - Ensure all localized URLs appear with correct `lastmod` and priority (if used).
- `llms.txt` and AI hubs:
  - Conceptually apply `geo-llms-txt` to:
    - Group localized content into language-specific sections.
    - Highlight “canonical” documents by language for AI ingestion.
  - Recommend one or more **AI-facing index pages** per language (e.g., `/en/ai-hub`, `/es/ai-hub`).
- Internal links:
  - Suggest cross-language linking patterns (e.g., “View this page in English / Spanish / German”).
  - Highlight a few **high-authority pages per language** that should link to the localized GEO pages.

Output a section `## AI & Crawler Multilingual Signaling Plan` with:

- Bullet checklists for sitemaps, llms.txt, and internal/external linking.
- Example `llms.txt` fragments or index-page sections for at least two languages.

### 8. Summarize into an execution-ready multilingual GEO plan

Summarize all of the above into a **single plan** that a team can execute:

- **Timeline**:
  - Recommended sequencing (e.g., “optimize English source → localize top 3 markets → expand further”).
- **Scope per iteration**:
  - Start with 2–3 high-priority languages before expanding.
- **Roles / ownership** (if known or inferable):
  - Who handles translation/localization vs. legal review vs. web implementation.
- **Success metrics**:
  - AI answer consistency across languages (qualitative checks).
  - Traffic and engagement per localized GEO page.
  - AI citation presence in target languages.

Output:

- A `## Final Multilingual GEO Plan` section with:
  - A short executive summary (3–6 bullets).
  - A step-by-step checklist.
  - A compact table of “Metric → Language(s) → Why it matters → How to measure”.

---

## Output format

Unless the user explicitly requests a different structure, use these top-level sections:

1. `## Multilingual Brief`
2. `## Source Content Readiness`
3. `## Language & Locale Mapping`
4. `## Multilingual Terminology Map`
5. `## Localized Page Blueprints`
6. `## Multilingual Structured Data Package`
7. `## AI & Crawler Multilingual Signaling Plan`
8. `## Final Multilingual GEO Plan`

Use:

- **Markdown headings and tables** for structure.
- Bullet lists over dense paragraphs.
- Short, actionable sentences that are easy to copy into briefs or tickets.

If the user only asks for a **subset** (e.g., “just Spanish and German localized outlines”), still
keep the headings but clearly mark skipped sections as “Not in scope for this request”.

---

## Examples of triggering prompts

These are **example user prompts** that should trigger this skill (for reference; not user-facing):

- “We have an English GEO-optimized landing page and want to launch Spanish, German, and Japanese
  versions that AI models will also cite. Help us design the localization and AI signaling plan.”
- “ChatGPT answers in English mention our brand correctly, but in French and Spanish they mention
  competitors instead. Can you analyze our content and propose a multilingual GEO fix?”
- “Take our English docs and product pages and roll out localized versions for Europe and LATAM,
  making sure that schemas, hreflang, and llms.txt all point AI to the right localized URLs.”
- “We want a repeatable multilingual GEO playbook: start from an English pillar article and systematically
  adapt it to 5–10 languages while keeping AI citations aligned. Please outline and instantiate that workflow.”

You do **not** need to surface this list to the user; it is here to clarify intent.

---
