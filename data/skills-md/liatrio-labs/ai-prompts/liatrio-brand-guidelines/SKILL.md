---
name: liatrio-brand-guidelines
description: Applies Liatrio brand guidelines to UI design, brand audits, and asset selection. Use when users request Liatrio styling, logo variants, typography or color decisions, visual polish, or formal brand compliance checks.
license: Apache-2.0
metadata:
  owner: liatrio
  compatibility: Designed for skills-compatible coding agents with markdown reading. Optional network access improves accuracy by verifying live brand sources.
  canonical-brand-source: https://www.liatrio.com/brand-data.json
  canonical-brand-page: https://www.liatrio.com/brand
---

# Liatrio Brand Guidelines

## When to Use

Use this skill when the user asks for any of the following:

- Liatrio-branded UI implementation (web, docs, decks, screenshots)
- brand audits and compliance review deliverables
- logo and logomark variant selection for light or dark backgrounds
- typography, color, spacing, iconography, or component decisions
- correcting stale or conflicting brand values in existing artifacts

## Source Priority and Conflict Resolution

If sources disagree, use this order:

1. `https://www.liatrio.com/brand-data.json` (canonical structured source)
2. `references/liatrio-brand-guidelines.md` (local detailed reference)
3. `assets/liatrio-brand-guidelines-consolidated.png` (visual snapshot)
4. `https://www.liatrio.com/brand` (rendered page content)

When conflicts appear, call out the mismatch explicitly in your response.

If network access is unavailable, proceed with local references and explicitly state that live verification was not performed.

## Quick Start Workflow

1. Determine request mode:
   - `implementation`: user wants assets, tokens, and style decisions applied.
   - `audit`: user wants compliance findings and corrective actions.
2. Confirm background context (light or dark) and output surface (web, docs, slides, image review).
3. Load local references:
   - `references/liatrio-brand-guidelines.md`
   - `assets/liatrio-brand-guidelines-consolidated.png`
4. If precision or freshness matters, verify live source values:
   - `bash scripts/fetch-brand-data.sh`
5. Apply brand rules and run the verification loop before final output.

## Core Rules

### Typography

- Primary typeface: DM Sans for all brand-facing text.
- Weights: Bold and SemiBold for headlines; Regular and Medium for body and UI.
- Size targets: H1 48-60px, H2 36-40px, H3 28-32px, Body 16-18px.

### Colors

- Hero brand color: `#24AE1D` (Primary Green).
- Accent highlight: `#89DF00` (Bright Green), used sparingly.
- Core text contrast on light surfaces: `#111111`.
- Dark mode surfaces: `#1A1F23` and `#1E2327`.
- Use live reference values for full primary, secondary, tertiary, and background palettes.

### Logo Usage

- Maintain clear space around the logo equal to the height of the "L" in Liatrio.
- Never distort, rotate, or recolor the logo.
- Use variants by background brightness:
  - Light: `logo_Liatrio.svg` (default) or `logo_Liatrio_black.svg`
  - Dark: `logo_Liatrio_reverse-preferred.svg` (preferred) or `logo_Liatrio_reverse.svg`
- For logomarks, avoid green backgrounds and use the square logomark when equal padding is required.

### Accessibility

- Contrast ratios: 4.5:1 for normal text, 3:1 for large text.
- Do not rely on color alone to convey information.
- Provide alt text for all logos and images.

## UI Styling Defaults

Use these defaults unless the user requests otherwise:

- Spacing rhythm: multiples of 4px (4, 8, 12, 16, 24, 32, 48, 64).
- Border radius scale: 0, 6px, 10px, 14px, 20px, 28px, 999px (full).
- Shadows: soft, dark-mode friendly; avoid harsh drop shadows.

## Component and Layout Guidance

Apply brand-consistent patterns that match the Brand page system:

- Buttons: use Primary Green for key CTA actions; use destructive red only for destructive actions.
- Alerts and messages: success, information, and error states must use both color and text semantics.
- Inputs and cards: keep clean contrast, restrained borders, and subtle elevation.
- Spacing rhythm: preserve 4px increments across padding, gaps, and vertical flow.

## Output Contracts

### Brand Audit Format

Use this exact structure for brand audits:

```markdown
## Brand Audit

- Scope: [screens/files/components reviewed]
- Compliant: [what matches Liatrio standards]
- Issues: [specific mismatches with source references]
- Fixes: [exact token and asset substitutions]
- Verification: [contrast/logo/background checks performed]
- Source Validation: [live JSON checked or local-only fallback]
```

### Implementation Decision Format

Use this exact structure for direct implementation tasks:

```markdown
## Implementation Decision

- Context: [surface + light/dark + component/page]
- Token Choices: [exact hex/type/spacing values]
- Asset Choices: [exact logo/logomark file variants]
- Rationale: [1-3 bullets tied to brand rules]
- Verification: [contrast + variant + conflict checks]
```

## Verification Loop

Before finalizing, run this loop:

1. Draft recommendation or implementation choices.
2. Check against `references/liatrio-brand-guidelines.md` for exact values.
3. If freshness matters, run `bash scripts/fetch-brand-data.sh` and compare values.
4. Confirm logo variant matches background brightness.
5. Verify accessibility constraints (contrast and non-color-only semantics).
6. Report any source conflicts or inability to verify live data.

## Workflow Checklist

- [ ] Confirm light or dark background context.
- [ ] Apply DM Sans and typography sizes.
- [ ] Choose Primary Green for key actions.
- [ ] Use Bright Green only as a highlight.
- [ ] Verify contrast ratios and add alt text.
- [ ] Use correct logo variant and clear space rules.
- [ ] Confirm outputs align with the PNG visual snapshot.
- [ ] If precision is required, verify against the markdown guide values.
- [ ] If sources conflict, apply the source-priority order and note the conflict.
- [ ] State whether live verification was performed.

## Optional Maintenance Scripts

- `scripts/fetch-brand-data.sh`
  - Reads and prints current structured data from `brand-data.json`.
- `scripts/download-brand-assets.sh`
  - Downloads logo files referenced by live JSON into `assets/logos/`.
  - Use when refreshing bundled logo assets.

## References

- `assets/liatrio-brand-guidelines-consolidated.png`
- `references/liatrio-brand-guidelines.md`
- `assets/logos/` (if populated)
- `https://www.liatrio.com/brand`
- `https://www.liatrio.com/brand-data.json`
