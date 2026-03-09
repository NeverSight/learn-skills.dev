---
name: docs-quality
description: Write and revamp product documentation to a high editorial standard using Mintlify, with strong information architecture, precise titles/descriptions, parameter-level clarity, cross-linking, and maintainable examples. Use when creating new docs pages, refactoring existing docs, improving docs structure/navigation, or standardizing docs quality across a repository.
---

# Docs Quality

Use this skill to produce documentation that is accurate, scannable, and complete enough for first-time and advanced users.

## Workflow

1. Read `docs/docs.json` first to understand IA, tabs, and existing groups.
2. Research source-of-truth implementation details before writing:
   - scan relevant files under `src/`
   - read `/src/types.ts` for public types/options/contracts
   - read `/schema/isol8.config.schema.json` for config keys/defaults/enums
3. Read the target page(s) and at least 2 neighboring pages to match tone and structure.
4. Load the `mintlify` skill and check whether a better component exists to represent the current content (instead of defaulting to plain Markdown).
5. Choose the page archetype (`overview`, `how-to`, `reference`, `guide`, `faq`, `troubleshooting`, `api`).
6. Apply the standards in `references/docs-quality-manual.md`.
7. If adding pages, update navigation in `docs/docs.json`.
8. Add cross-links to adjacent conceptual and reference pages.
9. Run checks from `references/review-checklist.md`.
10. Optionally run `scripts/docs_qc.sh` for quick structural linting.

## Which reference file to load

- **Complete standards**: `references/docs-quality-manual.md`
- **Page skeletons**: `references/page-templates.md`
- **Final QA gate**: `references/review-checklist.md`
- **Mintlify component decisions**: `references/component-playbook.md`
- **Ollama structural references**: `references/ollama-reference-notes.md`

## Non-negotiables

- Every page must have clear `title` and `description` frontmatter.
- Use explicit parameter/flag coverage for reference pages.
- Examples must be realistic and runnable-looking.
- Include expected output/behavior only when the snippet has a meaningful observable result to validate.
- When documenting explicit input/output pairs, group them in a single `<CodeGroup>` (for example: `Command` + `Expected output`) instead of separating them into distant blocks.
- When CLI + Library + API examples appear together, present them in `<Tabs>` (one tab per interface).
- For substantial “Related pages” sections, use a `<CardGroup>` with descriptive cards instead of plain bullet links.
- Diagrams must be readable on standard viewport (prefer vertical/simple over wide dense graphs).
- New/changed pages must be cross-linked from related pages.
- Avoid parser pitfalls in Markdown tables (especially unescaped pipe characters in inline code cells).
- End substantial pages with page-relevant FAQ and troubleshooting guidance (or links to dedicated FAQ/troubleshooting pages when full sections would be redundant).
- Callouts must follow intent: `<Warning>` for risk/breakage, `<Info>` for operational context, `<Tip>` for best-practice recommendations, `<Note>` for important but non-risk caveats, `<Check>` for explicit success confirmation.
