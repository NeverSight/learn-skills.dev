---
name: design-system-docs
description: Writes documentation pages for design system components and patterns, covering purpose, numbered anatomy, variants, states, paired do and avoid examples, content rules, keyboard and screen reader behavior, props table, tokens, and changelog. Use when asked to document a component, write usage guidelines, create a Storybook or MDX docs page, or audit docs for gaps. Not for building the components themselves, which is component-library.
---

# Design System Docs

Produces a complete, consistently structured documentation page for one component or pattern: a Markdown/MDX file that tells designers when to use it and engineers how to implement it correctly.

## When to use
- "Document our Button / Modal / Tabs component."
- A component exists in code or Figma but has no usage guidance, or the docs only list props.
- Writing a Storybook Docs, Docusaurus, or Nextra MDX page, or a standalone guideline page.
- Standardizing many inconsistent docs pages onto one template.
- Reviewing existing docs for missing states, accessibility notes, or outdated examples.

## Workflow
1. Gather sources: component code (props, types, defaults), design file or screenshots, existing docs, and the token source. If nothing is provided, ask for the component code or a screenshot; otherwise proceed and mark guesses as TODO.
2. Write the purpose in 1–2 sentences: the problem it solves and its most common use. Add "Use when" and "Don't use when", naming the alternative component for each "don't".
3. Define the anatomy: number every visible part (1 Container, 2 Leading icon, 3 Label, 4 Trailing icon) and mark each required or optional. Reference the numbers in a labeled image or ASCII sketch.
4. Document variants (primary, secondary, ghost) and sizes separately from states. Give each variant one sentence on when to choose it, plus hierarchy rules such as one primary button per view.
5. List the states that apply: default, hover, focus-visible, active/pressed, selected, disabled, loading, error, read-only. For each, state what changes visually and behaviorally.
6. Write 3–6 do/don't pairs. Each pair shows the same situation done right and wrong, with a one-line reason.
7. Add content guidelines (label length, casing, punctuation; defer wording rules to ux-writing), accessibility, props/API table, tokens used, related components, and changelog.
8. Verify that every code example matches the real API and every token name exists in the token source. Report design/code mismatches instead of silently picking one.

## Rules
**Structure**
- Use the same section order on every page so readers can scan: Overview, Anatomy, Variants, Sizes, States, Behavior, Content, Do/Don't, Accessibility, API, Tokens, Related, Changelog.
- Put a live example or image above the first block of text.
- Every variant needs a distinct use case; a variant without one is a removal candidate, so say so.

**Accuracy**
- Props table columns: Name, Type, Default, Required, Description. Copy types from source; do not paraphrase them.
- Token tables list semantic tokens (`color.action.primary.bg`, `space.3`), with raw values only as a secondary column (see design-tokens).
- Code examples are minimal, copy-pasteable, and use the real import path.

**Accessibility**
- Include a keyboard table (Key, Action) covering Tab, Shift+Tab, Enter, Space, Escape, and arrow keys as applicable; follow the WAI-ARIA Authoring Practices Guide pattern for composite widgets (tabs, menus, comboboxes, dialogs).
- State what a screen reader announces (role, name, state, value) and where the accessible name comes from (visible label, `aria-labelledby`, `aria-label`).
- Document focus behavior: where focus goes on open, close, and delete, and whether focus is trapped (modal dialogs only).
- Note target size (at least 24×24 CSS px, WCAG 2.2 AA 2.5.8) and contrast (4.5:1 text, 3:1 for borders and icons that convey state).

**Maintenance**
- Version with semver: breaking prop or behavior change = major, new prop or variant = minor, fix = patch. Breaking entries include a migration note.
- Show status at the top: Draft, Beta, Stable, or Deprecated (with replacement and planned removal version).

## Output
- One Markdown file per component, or MDX if the project uses Storybook, Docusaurus, or Nextra. Skeleton:
```
# ComponentName
Status · Version · Design link · Source link
## Overview        purpose, use when, don't use when (with alternatives)
## Anatomy         table: # | Part | Required | Notes
## Variants        ## Sizes        ## States
## Behavior        interaction, responsive, overflow and truncation
## Content guidelines
## Do / Don't      paired examples with reasons
## Accessibility   role, keyboard table, screen reader output, focus
## API             props table
## Tokens          ## Related components        ## Changelog
```
- A short list of TODOs and design/code mismatches found.

## Avoid
- Props-only docs with no guidance on when or why to use the component.
- Do/don't pairs built from unrelated examples, so the contrast teaches nothing.
- Describing states only visually ("turns blue") without behavior or announcement.
- Raw hex values and pixel sizes where a token exists.
- Marketing language ("a beautiful, powerful button").
- Redundant ARIA on native elements, such as `role="button"` on a `<button>`.
- Examples that no longer match the current API.

## Final check
- [ ] Purpose, use when, and don't use when (with alternatives) are present.
- [ ] Anatomy parts are numbered and marked required or optional.
- [ ] Every variant has a when-to-use sentence; states include focus-visible and disabled.
- [ ] Keyboard table, screen reader output, and focus behavior are specified.
- [ ] Props table types and defaults match the source code.
- [ ] All token names exist; no raw values where tokens apply.
- [ ] Status, version, and a changelog entry are present.
