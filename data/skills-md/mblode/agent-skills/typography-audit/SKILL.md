---
name: typography-audit
description: Audits web typography for punctuation, font selection, sizing, spacing, OpenType features, hierarchy, layout, typeface pairing, brand identity, and display type. Use when writing CSS/HTML for text, selecting or pairing typefaces, reviewing typography in web designs, configuring font-feature-settings, building a type system, or auditing typographic quality. Triggers on tasks involving font-family, font-size, line-height, letter-spacing, @font-face, font pairing, or typographic correctness.
---

# Typography Audit

89 rules across 10 categories for web typography quality. Focuses on concrete issues with concrete fixes.

## Audit Workflow

Copy and track this checklist during the audit:

```text
Audit progress:
- [ ] Step 1: Scope changed surfaces and select relevant categories
- [ ] Step 2: Run CRITICAL checks (punctuation, font setup)
- [ ] Step 3: Run HIGH checks (sizing, spacing)
- [ ] Step 4: Run MEDIUM+ checks for remaining categories in scope
- [ ] Step 5: Report findings with file:line and concrete fixes
```

1. Audit only changed files unless a full sweep is requested.
2. Scan CSS for font-family, @font-face, font-feature-settings, and sizing/spacing properties to identify relevant categories.
3. Load rule files progressively by category prefix — read only what applies.
4. Prioritize CRITICAL and HIGH findings before medium-priority polish.
5. After fixes, rerun the relevant rules before finalizing.

## Rule Categories by Priority

| Priority | Category | Impact | Prefix | Rules |
|----------|----------|--------|--------|-------|
| 1 | Punctuation & Special Characters | CRITICAL | `punct-` | 12 |
| 2 | Font Selection & Weights | CRITICAL | `font-` | 10 |
| 3 | Sizing & Measure | HIGH | `size-` | 7 |
| 4 | Spacing & Rhythm | HIGH | `spacing-` | 10 |
| 5 | OpenType Features | MEDIUM-HIGH | `opentype-` | 8 |
| 6 | Hierarchy & Scale | MEDIUM-HIGH | `hierarchy-` | 8 |
| 7 | Alignment & Layout | MEDIUM | `layout-` | 8 |
| 8 | Typeface Pairing | MEDIUM | `pairing-` | 10 |
| 9 | Brand & Identity | LOW-MEDIUM | `brand-` | 8 |
| 10 | Display & Headlines | LOW-MEDIUM | `display-` | 8 |

## Quick Reference

Read only what is needed for the current audit scope:
- Category map and impact rationale: `rules/_sections.md`
- Rule-level guidance and examples: `rules/<prefix>-*.md`

Example rule files:

```
rules/punct-smart-quotes.md
rules/font-true-styles.md
rules/size-line-height.md
```

Each rule file contains:
- Why the rule matters
- Incorrect example
- Correct example

## Review Output Contract

Report findings in this format:

```markdown
## Typography Audit Findings

### path/to/file.css
- [CRITICAL] `punct-smart-quotes`: Straight quotes used in heading text.
  - Fix: Replace `"` with `&ldquo;`/`&rdquo;` entities.

### path/to/clean-file.css
- ✓ pass
```

- Group findings by file.
- Use `file:line` when line numbers are available.
- State issue and propose a concrete fix.
- Include clean files as `✓ pass`.
