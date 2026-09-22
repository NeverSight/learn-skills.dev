---
name: token-compliance
description: "Check a codebase or implementation for token compliance — finding hardcoded values, wrong-tier token references, and inconsistent token application in consuming code. This checks how tokens are used in code, NOT how the tokens themselves are defined or structured. Trigger when someone says: are we using tokens correctly, find hardcoded values, token compliance check, find raw values, token misuse, are there any hex values in the code, checking token usage, or anything about whether tokens are being used consistently and correctly. Do NOT trigger for auditing the token definitions themselves — use token-audit for that."
references:
  - ../../knowledge-notes/token-architecture.md
  - ../../knowledge-notes/output-discipline.md
---

# Token compliance

A skill for identifying token compliance violations in a codebase or implementation: hardcoded raw values where tokens should be used, wrong-tier token references, and inconsistent token application. Produces a violation report with file references and remediation guidance.

## Context

Token compliance problems compound quietly. A single hardcoded hex value does not break anything. Two hundred of them, distributed across a codebase by dozens of contributors over two years, mean that a brand refresh or a dark mode implementation becomes a manual find-and-replace operation through thousands of files rather than a token update.

The compliance check exists to catch violations before they accumulate, and to understand the pattern of violations when they already have. The pattern matters: if hardcoded values are concentrated in one product area or one team's contribution, the response is different than if they are evenly distributed.

---

## Configuration

Before producing output, check for a `.ds-ops-config.yml` file in the project root. If present, load:
- `severity.*` — overrides for violation severity. Especially: `hardcoded_color`, `wrong_tier_reference`, `tier_leakage`
- `system.theming` — if true, elevate hardcoded colour violations to the configured severity (typically `critical`)
- `system.styling` — pre-selects the detection approach
- `integrations.github` — if enabled, auto-search for violations across the repo (see below)
- `integrations.style_dictionary` — if enabled, use the parsed token tree as the reference for what tokens exist and their correct tiers
- `gates.*` — if running as part of `component-to-release`, these determine which violations block release

## Auto-pull integrations

**GitHub** (`integrations.github.enabled: true`):
- Before running the manual compliance checks, do a broad search of `integrations.github.repo` for hardcoded values:
  - `gh api search/code -q "repo:[repo] language:css #[0-9a-fA-F]{6}"` — hex colours in CSS
  - `gh api search/code -q "repo:[repo] language:scss #[0-9a-fA-F]{6}"` — hex colours in SCSS
  - Search for `px` values in styling files as a spacing compliance signal
- Use the results to quantify scope before the detailed audit — "approximately 340 hardcoded hex values across 47 files" is a useful framing for the report summary

**Style Dictionary v4** (`integrations.style_dictionary.enabled: true`):
- Parse the token tree to build a complete map of available tokens per tier
- Use this as the authoritative "what token should this reference?" lookup when flagging violations
- If a hardcoded value exactly matches a known token's resolved value, include the token name in the remediation guidance automatically

**Figma MCP** (`integrations.figma.enabled: true`):
- Pull Figma variable definitions as a cross-reference — if a colour is defined as a Figma variable but hardcoded in code, that is a compliance violation with a known correct token

If an integration fails, log it and proceed with manual input.

## Step 0b: Messy codebase protocol

Token compliance has the most value on messy codebases — the ones with years of accumulated hardcoded values, inconsistent styling approaches, and multiple token migration attempts. For these codebases, apply the extended detection protocol:

**Indicators of a messy codebase:**
- Multiple styling approaches in the same project (CSS custom properties AND SCSS variables AND inline styles)
- Token files exist but significant portions of the codebase pre-date them
- Multiple naming conventions visible in style files (camelCase, kebab-case, BEM — mixed)
- Legacy colour palettes coexisting with current tokens
- Inline `style=` attributes in component templates

**Extended detection for messy codebases:**

1. **Legacy value mapping.** Before flagging violations, build a map of legacy values to current tokens. Many hardcoded values in legacy code were correct at the time they were written — they pre-date the token system. Map `#0066CC` to `var(--color-action-primary)` so remediation guidance is specific, not just "use a token."

2. **Violation age estimation.** Use git blame or file modification dates to estimate when violations were introduced. Group violations by era:
   - **Pre-token era** (before the token system existed) — these are expected debt, not compliance failures
   - **Migration era** (during token adoption) — partially migrated files where some values use tokens and others do not
   - **Post-token era** (after tokens were established) — these are genuine compliance failures and should be higher severity

3. **Hotspot detection.** Identify the 5–10 files with the most violations. These are the high-value remediation targets — fixing them reduces the violation count disproportionately. Present as:
   ```
   Compliance hotspots:
   1. src/legacy/checkout/styles.scss — 47 hardcoded values (pre-token era)
   2. src/components/Card/Card.styles.ts — 23 hardcoded values (migration era)
   3. src/pages/Dashboard/index.tsx — 19 inline styles (post-token era — PRIORITY)
   ```

4. **Intentional override detection.** Not every hardcoded value is a violation. Look for patterns that indicate intentional overrides:
   - Comments like `/* override */`, `/* intentional */`, `/* custom */`
   - Values that do not correspond to any token in the system (they may be one-off design requirements)
   - Values in test files, storybook decorators, or development-only code
   Flag these separately as "Reviewed — intentional" rather than as violations.

---

## Step 1: Define the scope and access

Ask for or confirm (skip questions already answered by auto-pull):
- What is being assessed? (Full codebase, specific product area, specific component set)
- Access to the implementation: codebase, Figma file, Storybook, or described properties
- The token system in use: what tokens exist, what tiers are defined, and how tokens are consumed in code
- The styling approach: CSS custom properties (`var(--token)`), SCSS variables (`$token`), Tailwind utility classes, CSS-in-JS theme objects, or a mix
- Any known compliance hotspots the check should prioritise
- Whether this is a baseline audit or a follow-up to a previous check
- **Codebase age and migration history:** When were tokens introduced? Has there been a previous migration? Are there known legacy areas? (This determines whether the messy codebase protocol applies.)

**Styling approach matters for how violations are detected:**

- **CSS custom properties:** Token references look like `var(--color-action-primary)`. Hardcoded values are raw hex/rgb/px values outside of `var()`.
- **SCSS variables:** Token references look like `$color-action-primary` or `map-get($tokens, 'action-primary')`. Hardcoded values are raw literals not using `$` variables.
- **Tailwind utility classes:** Token references are utility classes that map to the design system's Tailwind config (e.g. `bg-primary`, `text-color-content-default`, `gap-4`). These are NOT hardcoded values — they are token references expressed as utility classes. Hardcoded values in Tailwind are arbitrary value brackets: `h-[12px]`, `bg-[#ff0000]`, `p-[7px]`. Flag arbitrary values as violations; do not flag standard utility classes that resolve to configured tokens.
- **CSS-in-JS (Emotion, styled-components):** Token references look like `theme.colors.action.primary` or `tokens.spacing[4]`. Hardcoded values are raw literals in style objects.

**Framework-specific detection notes:**

- **If using Vue SFC:** Token violations appear inside `<style lang="scss" scoped>` blocks. Look for raw `px` values where `$token` variables or `var(--token)` should be used. Vue's scoped styles may also contain token references via `v-bind()` for dynamic CSS — these are valid token usage if bound to a token-backed prop.
- **If using Twig/Fractal:** Token violations appear as inline `style=""` attributes in templates (e.g. `style="background-color: {{ item.color }}"`), hardcoded hex values in SVG `fill`/`stroke` attributes, and raw pixel values in HTML dimension attributes. Twig components typically reference tokens via BEM utility classes — audit the SCSS that backs those classes, not just the template.
- **If using Emotion/styled-components with TypeScript tokens:** Token references look like `boxPalette.foregroundAction`, `mapSpacing(0.5)`, or `theme.colors.primary`. Hardcoded violations are string literals in style objects: `color: '#FF0000'`, `padding: '16px'`. Also check for tokens accessed via helper functions (e.g. `mapSpacing()`, `packs.underline`) — these are valid token usage.

## Step 2: Run the compliance checks

### Check 1: Hardcoded colour values

Find and flag all colour values that are not token references:
- Hex values (e.g. `#0066CC`, `#FFF`)
- RGB and RGBA values (e.g. `rgb(0, 102, 204)`, `rgba(0,0,0,0.5)`)
- HSL values
- Named colour values (e.g. `red`, `white`, `transparent` — note that `transparent` is sometimes acceptable; flag it as WARN rather than FAIL and assess context)

For each finding: file reference or context, the raw value found, and the token it should reference.

If the assessment is conducted against a design file rather than code: look for any colour styles applied as raw values rather than library styles.

### Check 2: Hardcoded spacing values

Find and flag spacing values that are not token references:
- Raw pixel values in padding, margin, gap, width, or height properties (e.g. `padding: 16px`, `gap: 8px`)
- Rem values that correspond to spacing scale values (e.g. `1rem` when there is a spacing token for `16px/1rem`)
- Percentage values where a spacing token would be more appropriate

Note: not all pixel values are compliance violations. Border widths, minimum touch targets, and other fixed dimensions may be intentionally hardcoded. Assess context and flag as WARN where intent is ambiguous.

### Check 3: Hardcoded typography values

Find and flag typography values that are not token references:
- Raw font-size values (e.g. `font-size: 14px`)
- Raw font-weight values (e.g. `font-weight: 700`)
- Raw line-height values (e.g. `line-height: 1.5`)
- Raw font-family values (e.g. `font-family: 'Inter', sans-serif`)
- Raw letter-spacing values

### Check 4: Wrong-tier token references

Find and flag component-level code that references primitive tokens directly rather than routing through semantic tokens:

FAIL example: `background-color: var(--color-blue-500)` in a button implementation
Should be: `background-color: var(--color-action-primary)` → `var(--color-blue-500)`

This is the subtlest compliance violation and the most architecturally damaging. It appears correct on the surface — the right colour is being used — but it breaks the semantic contract and means a semantic change (e.g. changing what "action primary" means) does not propagate to the component.

For each finding: the token being referenced, the semantic token that should be used instead, and the context.

### Check 5: Inconsistent token application

Find and flag cases where the same visual property is implemented differently across components or contexts:
- The same semantic role implemented with different tokens in different components (e.g. `color.action.primary` in some places, `color.brand.500` in others, for the same role)
- The same spacing context using different spacing tokens across similar components
- Interactive states (hover, focus, active) implemented differently across components that should share the same token

These violations are often invisible in a per-component review but surface clearly when components are compared.

## Step 3: Produce the violation report

---

### Token compliance report

Open with a headline sentence that tells the reader the overall state and where to focus.

**Date:** [date]
**Scope:** [what was assessed]
**Assessment method:** [codebase / design file / Storybook / described properties]

---

#### Summary

Overall compliance picture. What is the most significant finding? Is the violation pattern concentrated or distributed?

---

#### Violation counts

| Check | Violations found | 🔴 Critical | 🟠 High | 🟡 Medium | ⚪ Low |
|---|---|---|---|---|---|
| Hardcoded colour values | | | | | |
| Hardcoded spacing values | | | | | |
| Hardcoded typography values | | | | | |
| Wrong-tier token references | | | | | |
| Inconsistent token application | | | | | |
| **Total** | | | | | |

---

#### Violation log

Group by check type. For each violation:

| ID | Check | Severity | Location | Raw value / incorrect reference | Correct token | Notes |
|---|---|---|---|---|---|---|
| TC-01 | Colour | 🔴 FAIL | [file path or context] | `#0066CC` | `var(--color-action-primary)` | |

---

#### Context-aware violation severity

Not all violations carry equal weight. Adjust severity based on component importance. This is the feature that distinguishes a compliance check from a simple grep — without context-aware severity, every violation looks the same.

**Elevated severity (upgrade one level):**
- Violations in components on critical user paths (checkout, authentication, primary navigation)
- Violations in components with high fan-in (used by 5+ other components — from the component-audit dependency graph)
- Violations in components that are theming-sensitive (brand-facing surfaces, dark mode targets)
- Violations in post-token-era code (introduced after the token system was established — these are active compliance failures, not inherited debt)

**Standard severity:**
- Violations in general-purpose components with moderate usage
- Violations in migration-era code (partially migrated — compliance improvement is in progress)

**Reduced severity (downgrade one level):**
- Violations in internal/utility components not directly user-facing
- Violations in components that are already scheduled for deprecation
- Violations in legacy code areas with a known migration timeline
- Violations in pre-token-era code (introduced before the token system existed — these are expected debt)
- Layout utilities that use raw pixel values for structural concerns unrelated to design tokens (e.g., `max-width: 1200px` for a container, `height: 1px` for a divider) — flag as INFO, not WARN

**Contextual discrimination examples:**

To exercise the severity system properly, the skill must distinguish between:

| Found value | Context | Verdict | Reason |
|---|---|---|---|
| `color: #0066CC` | In a component's hover state | 🔴 FAIL (elevated) | Hardcoded colour on an interactive state — breaks theming |
| `color: #0066CC` | In a legacy page template | ⚠️ WARN (reduced) | Pre-token era code — known debt, not active failure |
| `border: 1px solid` | In a divider utility | ℹ️ INFO | Structural value — not a token concern |
| `padding: 16px` | In a component's spacing | 🔴 FAIL | Should use spacing token |
| `padding: 16px` | In a test file's wrapper | ℹ️ INFO | Test infrastructure — not user-facing |
| `max-width: 960px` | In a layout container | ℹ️ INFO | Layout constraint — intentional fixed value |
| `background: transparent` | In a ghost button reset | ℹ️ INFO | CSS reset value — not a token violation |

Apply the adjustment after the initial severity assignment. Note the adjustment and reason in the violation log — "Severity upgraded from Medium to High: component is on the checkout critical path" or "Severity downgraded to INFO: layout utility using structural pixel value."

This weighting ensures remediation effort focuses on violations with the highest real-world impact, and prevents clean codebases from generating false-positive noise on values that are correctly hardcoded.

#### Pattern analysis

Step back from individual violations and describe the pattern:
- Are violations concentrated in specific files, components, or product areas?
- Are there recurring raw values that appear frequently and clearly correspond to a specific token?
- Is there a particular check type that dominates the violation count?

Pattern analysis turns a violation log into actionable intelligence. "Hardcoded spacing violations are concentrated in the legacy product area — likely pre-dates the token system" leads to a different response than "hardcoded spacing violations are evenly distributed and increasing — the token system is not being adopted."

---

#### Remediation priority

**Immediate:** Wrong-tier token references and any hardcoded values that would break under theming or brand change. These have architectural impact.

**Planned:** Consistent hardcoded values that correspond clearly to existing tokens. These can be resolved in a systematic pass.

**Review:** Ambiguous values (raw percentages, context-dependent px values, intentional overrides). These need human judgment before remediation.

---

#### Remediation approach

Recommend the most efficient approach for the volume and pattern of violations found:

- If violations are high-volume and repetitive: a migration script or codemod is more efficient than manual correction
- If violations are concentrated in a specific area: a focused refactoring sprint on that area
- If violations are sparse and distributed: add to the team's ongoing code review criteria and address as work touches each area
- If wrong-tier references are significant: a token architecture review may be warranted before remediation to ensure the semantic tier is complete enough to reference correctly

---

## Check 6: DTCG 2025.10 compliance (staff-level)

If the token source declares DTCG format compliance, or if the team is targeting DTCG alignment, run these additional checks:

**Type declaration compliance.** Every token should have a `$type` field. Flag tokens without type declarations. Validate that declared types match the DTCG 2025.10 type list (color, dimension, fontFamily, fontWeight, duration, cubicBezier, number, strokeStyle, border, transition, shadow, gradient, typography).

**Composite type sub-value compliance.** For composite tokens (typography, shadow, border, transition, gradient), validate that every sub-value is either a proper token reference or a correctly typed literal. A typography token with `fontSize: "14px"` instead of `fontSize: "{font-size.base}"` is a compliance violation at the sub-value level.

**Resolver coverage.** If resolver files exist, validate that every semantic token has a value in every declared mode. Missing mode values are theming bugs waiting to happen — the system will fall back unpredictably when a consumer activates a mode where the token isn't defined.

**Alias chain integrity.** Follow every alias chain from component → semantic → primitive. Flag broken chains (aliases that reference non-existent tokens), circular references, and chains that skip tiers.

Include DTCG findings as a separate section in the report. These are informational for teams not targeting DTCG, and compliance-level for teams that are.

## Check 7: Cross-system token consistency (staff-level)

For organisations with multiple systems that share token primitives or semantic naming:

- Do tokens with the same name resolve to the same value across systems?
- If systems share a primitive tier, are semantic tokens referencing the same primitives for the same intent?
- Are there naming collisions (same name, different meaning) across systems?

Cross-system token inconsistency creates confusion when teams work across products or when components from different systems appear on the same page.

---

## Quality checks

- All check types are covered (five core + DTCG and cross-system if applicable)
- Wrong-tier references are checked separately from hardcoded values — they are a different category of violation
- Pattern analysis section exists and describes the distribution of violations, not just the total
- Remediation priority distinguishes between architectural violations and surface-level ones
- The report is specific enough to act on: file references or context for each violation, not just "hardcoded values found"
- If DTCG checks were run, composite sub-value compliance is verified, not just top-level token compliance
- If cross-system checks were run, naming collision analysis is included
