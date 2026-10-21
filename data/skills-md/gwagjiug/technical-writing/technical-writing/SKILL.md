---
name: technical-writing
description: Draft, review, restructure, and polish developer-facing technical documentation and technical articles. Use when Codex needs to work on tutorials, how-to guides, troubleshooting docs, API/reference docs, conceptual explanations, release or migration guides, or technical blog/article drafts; evaluate audience fit, information architecture, headings, overview, concrete examples, terminology consistency, compactness, and sentence-level clarity while preserving facts, code, commands, API names, versions, warnings, and product behavior.
---

# Technical Writing

## Core Workflow

1. Identify the audience, task, and document type before editing. If the user already gave enough context, proceed with the best matching type.
2. Select the structure from `references/document-types.md` and the matching template from `assets/templates/` when creating or reorganizing a draft.
3. Apply the information architecture principles in `references/structure-principles.md`: one topic per page, value first, effective headings, overview, predictable order, and sufficient background.
4. Polish sentences with `references/sentence-style.md`: clear subjects, active voice, compactness, concreteness, natural expression, and terminology consistency.
5. Review with `references/review-rubric.md`; report findings before broad rewrites when the user asks for a review.

## Task Routing

- **Draft or rewrite a full document**: read `document-types.md`, choose one template, then draft directly with placeholders resolved from the user's context.
- **Review an existing draft**: read `review-rubric.md`; return severity-ranked findings with concrete fixes and a short summary.
- **Restructure notes or a rough draft**: read `structure-principles.md`; produce an outline first, then rewrite only if asked.
- **Polish prose**: read `sentence-style.md`; keep the original meaning and technical surface intact.
- **Create prompts or AI-assisted workflows**: read `prompt-workflows.md`; generate reusable prompts for drafting, structuring, or reviewing.
- **Check source/license boundaries**: read `source-map.md`.

## Guardrails

- Preserve code blocks, commands, API identifiers, parameter names, version numbers, warnings, error messages, dates, metrics, and product behavior unless the user explicitly asks to change them.
- Do not invent missing technical facts. Mark gaps as questions or TODOs.
- Prefer concrete examples, conditions, prerequisites, and expected results over vague benefits.
- Keep headings predictable and keyword-rich; avoid clever titles when users need searchability.
- Put the reader's value or outcome before implementation details.
- For Korean-language drafts, apply the Korean-specific naturalness notes in `sentence-style.md`; for English drafts, preserve idiomatic English and avoid literal translationese.

## Output Defaults

- For reviews: provide findings first, ordered by severity, with file/section references when available.
- For drafts: provide the finished draft unless the user asks for only an outline.
- For outlines: include the intended reader, document type, section list, and cross-link suggestions.
- For rewrites: mention preserved constraints and any unresolved factual gaps.
