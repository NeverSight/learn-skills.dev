---
name: opc-symlink-skill
description: Package an AI builder or one-person-company operator into a public-facing personal homepage. Use when the user wants a packaging interview, positioning help, audience and offer discovery, AI builder profile metadata, product/service promotion, proof-first personal branding, or a standalone homepage generated from workspace context and confirmed public facts.
---

# OPC Symlink Skill

## Overview

Use this skill as a packaging consultant for AI builder style OPCs. The goal is
not to collect a profile form; it is to turn workspace clues and conversation
into a credible public narrative that promotes the user, their products, and
their collaboration value.

Treat workspace memory as unverified raw material. Summarize it as packaging
hypotheses, ask the user to confirm the direction and public boundary, then
interview deeply enough to understand who they help, what pain they solve, what
they can offer, and why a visitor should trust them.

## Non-Negotiable Render Gate

Do not deliver, claim completion, or describe the homepage as generated until
you have run both of these commands as separate steps:

```bash
node /path/to/opc-symlink-skill/scripts/render-homepage.mjs \
  metadata.json \
  personal-homepage.html \
  --template product-led
node /path/to/opc-symlink-skill/scripts/verify-homepage.mjs \
  metadata.json \
  personal-homepage.html
```

If rendering or verification fails, fix the metadata or command usage and run
the commands again. Do not create, patch, translate, or "quick fix" the HTML by
hand as a fallback.

## Workflow

1. Scan workspace context and recent memory.
2. Summarize the inferred public packaging angle as hypotheses.
3. Run a deep packaging interview using
   `references/packaging-interview-playbook.md`.
4. Confirm the positioning, public facts, target audience, offers, and privacy
   boundary. Do not ask the user to review raw JSON.
5. Internally create AI builder metadata that follows
   `references/metadata-schema.md`.
6. Ask the user to choose a homepage template:
   `product-led`, `builder-os`, or `proof-first`.
7. Generate bilingual metadata by default: write Chinese and English copy
   separately under `locales.zh-CN` and `locales.en`. Only skip bilingual
   metadata if the user explicitly asks for a single-language homepage. Do not
   mix languages in the same visible copy block.
8. Compress visible metadata copy to the display budgets in
   `references/metadata-schema.md`. Long CTA labels, headlines, cards, pills,
   and list items will fail rendering; shorten metadata instead of relying on
   the HTML to absorb long text.
9. Render and verify the standalone HTML using the bundled scripts, then
   deliver the HTML path, metadata path, selected template, verification result,
   and a short note about assumptions or missing proof.

Source-of-truth rule: only modify metadata JSON when changing homepage content.
Treat generated HTML as a disposable build artifact. Do not hand-edit generated
HTML.

## Scan Context

Run the scanner from the current workspace unless the user points elsewhere:

```bash
node /path/to/opc-symlink-skill/scripts/scan-context.mjs . --json
```

Look especially for files named like `user.md`, `memory.md`, `soul.md`,
`profile.md`, `about.md`, `bio.md`, `README.md`, blog posts, docs, product
descriptions, pitch notes, and public launch notes.

Also scan directories named `memory` or `memories`, but only use files modified
within the last 3 months. Treat older memory files as stale unless the user
explicitly asks to include a longer history.

Use scanner output to decide which files to read. Do not read secrets, env
files, private keys, credential stores, dependency folders, build artifacts, or
large unrelated files. If a file appears sensitive, ask before using it.

## Packaging Interview

Start by saying what the workspace suggests, using language like:

- "I infer that your current public angle might be..."
- "The strongest product-facing signal seems to be..."
- "The audience is still unclear to me..."
- "Before I package this, what should I correct or keep private?"

Then interview as a packaging consultant. Ask 2-4 questions per round, make
judgment calls, and adapt based on the user's answers. Do not ask the user to
fill fields.

Cover these decisions before rendering:

- Positioning: how strangers should understand the user in one sentence.
- Audience: who the homepage should attract and who it should not attract.
- Pain: what target visitors struggle with now.
- Transformation: what the user helps them become able to do.
- Offer: product, advisory, delivery, training, co-building, or another route.
- Proof: projects, public content, customer outcomes, metrics, testimonials.
- CTA: default to booking a conversation unless the user chooses otherwise.
- Boundary: what facts, customers, numbers, or personal details stay private.

Stop interviewing when the homepage can make a specific, truthful, and useful
promise to a visitor. Vague proof is acceptable only if it is phrased as focus,
direction, or current work rather than achievement.

## Metadata

Create metadata internally after the user has confirmed the packaging direction
and public boundary. Follow `references/metadata-schema.md`.

Do not show the raw JSON for approval unless the user asks. Instead, summarize
the public narrative in plain language, then write the JSON yourself.

Keep claims truthful. Do not invent partners, customers, metrics, logos,
credentials, testimonials, or product maturity. Keep `privacy.exclude` out of
the rendered homepage.

Create two localized metadata entries by default: `locales.zh-CN` and
`locales.en`. Translate the user's positioning, audience, offers, proof, CTA,
and navigation-facing copy into each language. Keep shared links, colors,
template choice, and privacy rules at the top level when they are identical.
Only create single-language metadata when the user explicitly asks for it.

Before rendering, make metadata concise enough for the selected templates. Use
short CTA labels such as "预约沟通" or "Book a call"; put explanation in
`cta.note`. English locale copy must be English or transliterated, not Chinese
sentences mixed into English template labels.

## Render Homepage

Save the metadata as JSON, then render with the selected template:

```bash
node /path/to/opc-symlink-skill/scripts/render-homepage.mjs \
  metadata.json \
  personal-homepage.html \
  --template product-led
```

Immediately verify the rendered file:

```bash
node /path/to/opc-symlink-skill/scripts/verify-homepage.mjs \
  metadata.json \
  personal-homepage.html
```

Read `references/rendering-rules.md` before modifying an existing generated
homepage.

Templates:

- `product-led`: product and value proposition first; best default for booking
  calls and B2B collaboration.
- `builder-os`: AI builder workbench; emphasizes projects, tools, systems, and
  experiments.
- `proof-first`: trust and outcomes first; emphasizes cases, results, and
  delivery credibility.

The renderer creates a standalone HTML file with embedded CSS and metadata.
When the user asks for changes, update the metadata JSON and run the renderer
again as a separate command, then run the verifier. Do not edit generated HTML
directly and do not combine metadata writing plus rendering in one complex shell
command.

If rendering fails with metadata copy validation errors, shorten or translate
the metadata fields named in the error output, then run render and verify again.
Do not bypass this by editing HTML or by letting long copy overflow.

Because the default metadata should include `locales.zh-CN` and `locales.en`,
the renderer normally creates one HTML file with an in-page language switcher.
If the user explicitly requested a single-language page and metadata only has
one locale, pass `--single-language`; the renderer still localizes template UI
labels based on `locale`. Pass the same `--single-language` flag to the
verifier.

Keep only one final HTML file. Reuse and overwrite the same output path, such
as `personal-homepage.html`, for every revision. Do not create `v2`, `new`,
`final`, timestamped, or template-specific HTML copies unless the user
explicitly asks for multiple deliverables.

If the user asks to integrate with an existing frontend repository, adapt the
content to that stack instead of using the standalone renderer.

After rendering, inspect the HTML in a browser when practical. Check that text
does not overflow, links are correct, private content is absent, and the first
viewport makes the audience, value, proof, and CTA clear.

## Output

Return:

- The generated HTML file path.
- The metadata JSON path.
- The selected template.
- The render and verification result.
- A short note listing missing proof or assumptions.

Prefer the user's language. If the user writes in Chinese, interview and write
the homepage in Chinese unless they request another language.
