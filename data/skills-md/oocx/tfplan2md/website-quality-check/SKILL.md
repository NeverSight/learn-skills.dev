---
name: website-quality-check
description: Run a lightweight, repeatable quality checklist for the website (including style guide adherence).
---

# Skill Instructions

## Purpose
Provide a lightweight, repeatable quality checklist for website changes in the Eleventy site under `website/`.

## Hard Rules
### Must
- [ ] Verify the change follows `website/README.md`, `website/specification.md`, and `website/architecture.md`.
- [ ] If the change touches examples or authoring structure, read the relevant website ADRs before finalizing the change.
- [ ] If files under `website/` changed, run `scripts/website-verify.sh --all` and fix failures.
- [ ] If local preview is available, open the changed pages via the VS Code preview server (`http://127.0.0.1:3000/website/dist/`) and use the `browser/*` tools to ensure the rendered page and browser console are sane.
- [ ] Do quick link/navigation sanity checks on changed pages.
- [ ] Do basic accessibility spot checks (headings, landmarks, labels, keyboard navigation where relevant).
- [ ] Validate the authored source, not only the rendered output: when a shared layout, component, partial, `_data` module, or example directory changes, verify at least one representative page that consumes it.

### Must Not
- [ ] Do not hand off or claim completion without completing the checklist for the changed pages and any affected shared building blocks.

## Golden Example

```text
Checklist (per changed page):
- Shared docs: README/specification/architecture still match the implementation
- Content model: page entrypoints, _data modules, includes, and examples are updated in the correct source files
- Links: no broken relative links introduced
- Browser preview: verify layout, interaction, and console are clean
```

## Actions
1. Identify which authored sources changed under `website/`:
   - `website/src/pages/` for page entrypoints
   - `website/src/_data/` for structured page content and navigation
   - `website/src/_includes/` for shared layouts, components, and partials
   - `website/src/examples/` for interactive example fragments
   - `website/src/styles/`, `website/src/style.css`, and `website/src/site-assets/` for shared presentation and behavior
2. For each changed page, verify:
   - Alignment with `website/README.md`, `website/specification.md`, and `website/architecture.md`
   - Link/navigation sanity
   - Accessibility basics
3. If a shared authored source changed, verify representative consuming pages in `website/dist/`.
4. If issues are found, fix them or record them with a clear plan.
