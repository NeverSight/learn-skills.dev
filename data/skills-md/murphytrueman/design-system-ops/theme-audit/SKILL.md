---
name: theme-audit
description: "Audit theme coverage and consistency across a design system's semantic and component token tiers. Triggers: audit my themes, check theme coverage, are all tokens defined across themes, dark mode audit, brand variant check, do themes have parity, theme consistency check, light/dark token coverage, or anything about whether themes are complete and internally consistent. Use this when launching a new theme, after a rebrand, adopting dark mode, or when token-audit reveals tier leakage that defeats theming."
references:
  - ../../knowledge-notes/token-architecture.md
---

# Theme audit

A skill for auditing theme coverage and visual consistency across multiple design system themes. Identifies tokens missing from specific themes, component tier propagation failures, internal consistency violations within each theme, DTCG resolver coverage gaps, and components likely to break on theme switches. Produces a theme coverage report with severity-rated findings.

## Context

Theming is where the three-tier token architecture proves its value or reveals its failures. When a system switches themes correctly, the change ripples through every component that references the semantic tier. When it does not — when components hardcode primitives or when the semantic tier is incomplete — a theme switch becomes a hunt through hundreds of files for missed overrides.

A theme audit is not about validating a single theme's visual appearance. It is about ensuring every token consumed by every component exists and is correctly defined across every theme the system claims to support. It is about catching cases where the component tier skips the semantic tier entirely, making theme switches invisible to that component.

The audit surfaces three categories of problems: coverage gaps (token defined in Theme A but not Theme B), architectural failures (component tokens that bypass the semantic tier), and internal consistency breaks (within a single theme, visual logic is violated — e.g. in dark mode, surface colours are lighter than background).

## Configuration

Before producing output, check for a `.ds-ops-config.yml` file in the project root. If present, load:

- `system.theming` — if false, exit early with a note that this skill applies only to systems with theming enabled. If true, proceed.
- `severity.*` — overrides for theme-specific findings (e.g. `missing_theme_value: critical` for a system about to launch dark mode)
- `integrations.style_dictionary` — if enabled, parse tokens via Style Dictionary v4 to auto-extract all semantic and component tokens and their resolver-defined mode values
- `integrations.figma` — if enabled, pull Figma variables and their modes as the theme source
- `recurring.*` — if this is a recurring run, load the previous theme audit for trend comparison

If no config file exists, proceed with defaults and ask for manual input.

## Step 0: Theme discovery and scope

Before auditing, discover what themes the system actually defines:

**Discover themes:**
1. **Resolver files** — if DTCG format, scan the project for `.resolver.json` files and extract mode names (e.g. `light`, `dark`, `brand-a`, `brand-b`)
2. **CSS custom property scopes** — if using CSS variables, scan for theme selectors like `:root`, `.dark`, `[data-theme="light"]`, `[data-theme="dark"]`, `[data-brand="brand-a"]` — each scope is a theme variant
3. **SCSS variable maps** — if using SCSS, look for `$themes: (...)` or separate theme files (`_theme-light.scss`, `_theme-dark.scss`)
4. **JavaScript theme objects** — if using CSS-in-JS, look for exported theme objects or theme switching functions (e.g. `export const lightTheme = { ... }; export const darkTheme = { ... }`)
5. **Tailwind mode declarations** — check `tailwind.config.js` or `tailwind.config.ts` for `darkMode` configuration and any theme extends
6. **Figma modes** — if Figma integration is configured, list all variable modes in the linked file

**Present discovered themes to user:**

Produce a brief inventory:
```
Themes discovered:
- Light (default, CSS root scope, Figma mode)
- Dark (CSS .dark scope, Figma mode)
- Brand A (data-theme="brand-a" scope)
- Brand B (data-theme="brand-b" scope)
Total: 4 themes
```

Ask: "I found these [N] themes. Should I audit all of them, or focus on specific variants?"

If no themes are discovered and theming is marked as `true` in config, ask the user to name the themes they intend to support.

## Step 1: Identify tokens in scope

Gather the semantic and component tiers across all discovered themes:

**For DTCG format:**
- Parse resolver files and extract all semantic tokens and their mode-specific values
- Extract all component tokens and their mode-specific values
- Verify that every token in every set has values defined for every declared mode

**For CSS custom properties:**
- Extract `:root` (or default theme scope) as the reference set of all semantic tokens
- Extract theme-scoped selectors (`.dark`, `[data-theme="dark"]`, etc.) and their token definitions
- Map which tokens are defined in each scope

**For SCSS variables:**
- Extract variables from the base/default theme file as the reference set
- Extract variables from each theme file
- Identify which variables are redefined per theme

**For JavaScript theme objects:**
- Extract the reference theme object's keys as the token inventory
- For each theme variant, identify which tokens are redefined

**For Tailwind:**
- Extract `theme` and `darkMode` blocks
- Identify which theme values are overridden in each mode
- Note which breakpoints or variants redefine token values

Output a token inventory:
```
Semantic tokens: 156 total
- Defined in all themes: 144
- Defined in light only: 5
- Defined in dark only: 4
- Defined in brand-a only: 3

Component tokens: 287 total
- Defined in all themes: 278
- Coverage gaps: 9
```

This checkpoint reveals the scale of coverage problems before the detailed audit.

## Step 2: Theme coverage check

For each semantic token, verify it is defined across ALL themes:

**Coverage matrix:**

Build a matrix: rows are semantic tokens, columns are themes. Mark each cell as:
- ✓ Defined (token has a value in this theme)
- ✗ Missing (token is defined in other themes but not this one)
- ∅ Not applicable (some tokens may be theme-specific by design — note intent)

**Identify missing semantic tokens per theme:**

```
Light theme: 156/156 semantic tokens ✓
Dark theme: 152/156 semantic tokens (missing: --color-feedback-info, --color-feedback-warning, --spacing-dense-gap, --text-decorative-label)
Brand A: 151/156 (missing: --color-feedback-warning, --spacing-dense-gap, --text-decorative-label, --text-heading-display)
Brand B: 156/156 ✓
```

For each missing token, flag:
- Finding ID (e.g. TC-01)
- Severity: Critical if the token is used by component tokens; High if used by multiple components; Medium if used by few components; Low if orphaned
- Description: Semantic token [name] is not defined in [theme]
- Impact: Which components depend on this token and may render incorrectly
- Recommended action: Define the token in the missing theme. If the token should not apply to this theme, document that decision.

## Step 3: Component tier propagation check

Verify that component tokens correctly inherit from the semantic tier across all themes:

**For each component token:**
1. Trace its reference — does it point to a semantic token, or to a primitive?
2. If it points to a primitive: this is tier leakage. The component token bypasses theming.
3. If it points to a semantic token: verify that the semantic token has values defined in all themes where the component is used.

**Tier leakage detection:**

Flag any component token that references a primitive (rather than a semantic token):

```
TC-10 | Critical | Tier leakage | button.background.default references {color.blue.500} (primitive) instead of semantic tier
- Impact: Button background will not change on theme switch (dark mode will show blue on blue)
- Recommended action: Redefine as button.background.default: {color.action.primary}
```

Quantify the scope:
```
Component tokens examined: 287
- Correctly reference semantic tier: 276
- Tier leakage (reference primitives): 11
```

Tier leakage is the most dangerous category of theme bug — everything appears to work until someone activates a new theme.

## Step 4: Visual consistency check within each theme

For each theme, validate internal logical consistency:

**Consistency rules (apply per theme, not across themes):**

For **light theme:**
- Surface colours should be lighter than background colours
- Text colours should have sufficient contrast against their backgrounds
- Action colours should be visually distinct from neutral colours
- Hover states should be visually different from default states (e.g. darker, not lighter)

For **dark theme:**
- Surface colours should be darker than background colours (or use the same value with appropriate contrast)
- Lighter text on dark backgrounds is appropriate; darker text on light backgrounds is not
- Action colours may need adjustment to maintain contrast in dark mode

For **brand variants:**
- Primary action colour should be consistent with brand guidelines
- Secondary actions should be visually subordinate to primary actions
- Error/warning/success states should be visually distinct from brand primary

**Consistency violations to flag:**

Run visual spot-checks on high-impact token groups:
- Does `color.feedback.error` have adequate contrast against `color.background.default` in this theme?
- Are `color.surface.primary` and `color.background.default` visually distinct (same value is sometimes OK, but should be documented as intentional)?
- Is `color.action.primary` visually more prominent than `color.action.secondary` in this theme?

Flag violations:
```
TC-22 | Medium | Consistency | Dark theme: color.background.default and color.surface.primary are identical (#121212)
- This may be intentional (both are neutral backgrounds), but it reduces visual hierarchy
- Recommended action: Review with design team. If intentional, document the decision. If not, adjust surface token.
```

## Step 5: DTCG resolver validation

If the system uses DTCG format with resolver files:

**Resolver file structure check:**
1. Verify `.resolver.json` files exist and are well-formed JSON
2. Extract the `sets` and `modes` blocks
3. Verify that every semantic token listed in `sets` has a value defined for every declared `mode`

**Mode coverage per token:**

For each semantic token:
```
color.action.primary:
  light: {color.blue.500}    ✓
  dark:  {color.blue.300}    ✓
  brand-a: {color.purple.600}  ✓
  brand-b: [missing]         ✗
```

Flag missing mode values:
```
TC-30 | Critical | Resolver coverage | color.action.primary missing value in brand-b mode
- When brand-b theme is active, color.action.primary will resolve to light mode default (fallback)
- Recommended action: Add mode-specific value to brand-b mode in resolver
```

**Set composition check:**
- Verify that all semantic tokens are included in at least one resolver set
- Identify orphaned tokens (declared in token files but not included in any resolver)
- If component tokens exist, verify they are composed into the same resolver sets as their semantic dependencies

Orphaned tokens in resolver files are maintenance burden — they appear in IDE autocomplete but produce no runtime value.

## Step 6: Theme switching regression check

Identify patterns in the codebase that are likely to break on theme switch:

**Regression patterns:**

Search for common failures:

1. **Hardcoded values in component code** — even if tokens exist, if components use raw colours/spacing instead of tokens, theme switches are invisible to those components
2. **Opacity hacks** — patterns like `rgba(var(--color-action-primary), 0.5)` work for colour tokens but may fail if the theme switches the token value to a different format
3. **CSS calc() on token values** — patterns like `padding: calc(var(--spacing-component-gap) * 2)` assume the token value is a plain number; if the token includes units, the calc fails
4. **Inline styles with theme assumptions** — `style={{ backgroundColor: isDark ? darkColor : lightColor }}` is not using the token system at all
5. **Missing component variants for theme-specific rendering** — some components may need different structures or properties per theme (e.g. borders visible in dark mode but not light)

**Regression output:**

Flag high-risk patterns:
```
TC-40 | High | Regression | Found 23 instances of hardcoded hex values in component code
- These will NOT change on theme switch even though token values exist
- Recommended action: Replace hardcoded values with token references

TC-41 | Medium | Regression | Found 7 instances of opacity hacks (rgba with token + literal opacity)
- These work but are fragile if token format changes
- Recommended action: Create composite opacity tokens (e.g., color.action.primary-75%) if opacity variations are needed
```

## Step 7: Produce the theme audit report

Structure the report as follows:

---

### Theme audit report

**Date:** [date]
**Scope:** [themes audited]
**System theming enabled:** [yes/no from config]

---

#### Summary

Overall theme health. What is the most significant gap? Is coverage consistent across themes, or are some themes neglected? Are component tokens correctly inheriting from semantic tier?

One paragraph. Honest about severity.

---

#### Theme discovery

List all themes discovered and confirmed in scope:
- Light (default, CSS root)
- Dark (CSS .dark scope)
- Brand A (data-theme="brand-a")
- Brand B (data-theme="brand-b")

---

#### Token inventory

| Category | Total | Coverage |
|---|---|---|
| Semantic tokens | 156 | 152/156 in all themes |
| Component tokens | 287 | 278/287 correctly reference semantic tier |
| Tier leakage instances | — | 9 component tokens reference primitives |

---

#### Coverage findings

**Semantic token coverage matrix:**

| Token | Light | Dark | Brand A | Brand B |
|---|---|---|---|---|
| color.action.primary | ✓ | ✓ | ✓ | ✓ |
| color.feedback.info | ✓ | ✗ | ✗ | ✓ |
| spacing.dense.gap | ✓ | ✗ | ✗ | ✓ |

For each missing token, include:
- Finding ID
- Severity
- Token name and which themes are missing it
- Components that depend on this token
- Recommended action

---

#### Component tier check

**Tier propagation:**
- Component tokens examined: 287
- Correctly reference semantic tier: 276
- Tier leakage (reference primitives): 11

**Tier leakage violations:**

For each violation:
- Finding ID
- Component token name
- Primitive it references instead of semantic
- Severity: Critical (blocks theming entirely)
- Recommended action

---

#### Visual consistency check

**Light theme consistency:** [Pass/Warn/Fail]
**Dark theme consistency:** [Pass/Warn/Fail]
**Brand variant consistency:** [Pass/Warn/Fail]

List any violations:
- Finding ID
- Consistency rule violated
- Specific token values at fault
- Recommended action

---

#### DTCG resolver status (if applicable)

**Resolver files found:** [count and paths]
**Mode coverage:** [summary of mode-to-token coverage]
**Orphaned tokens:** [count and examples]
**Missing mode values:** [count and severity by theme]

Include resolver-specific findings with severity ratings.

---

#### Regression risk assessment

**Hardcoded values in components:** [count by severity]
**Opacity hacks:** [count and pattern examples]
**Calc() on tokens:** [count and contexts]
**Missing theme-specific variants:** [count and affected components]

Each category should include:
- Count of instances found
- Risk level (High/Medium/Low)
- Recommended remediation approach (codemod, manual refactoring, architectural change)

---

#### Remediation priority

**Tier 1 — Fix immediately:**
- Tier leakage (blocks theme switching entirely)
- Missing semantic tokens in active themes (causes fallback errors)
- Resolver coverage gaps in production modes

**Tier 2 — Fix before next theme launch:**
- Visual consistency violations within themes
- Coverage gaps in beta or upcoming themes
- Regression patterns in high-fan-out components

**Tier 3 — Address in polish phase:**
- Orphaned tokens
- Hardcoded values in low-usage components
- Opacity and calc() fragility

---

#### Small-system note

If `system.component_count` in config is < 5, or if component count is inferred to be small from theme coverage:

"This is a small system. Component-tier propagation problems (tier leakage) have outsize impact because each component token affects user-facing surfaces directly. Prioritise tier leakage findings even if absolute violation count is low."

---

## Recurring workflow

If `recurring` is configured in `.ds-ops-config.yml`:

1. **Before producing output**, check `recurring.output_directory` for a previous theme audit report
2. **If a previous report exists**, load it and compare:
   - Coverage gap count: increasing, stable, or decreasing?
   - New coverage gaps (themes missing tokens that previously had them)
   - Resolved gaps (tokens now defined in previously missing themes)
   - Tier leakage count: stable or growing?
   - Regression risk patterns: new hardcoded values appearing?
3. **Add a "Trend since last audit" section** to report header:
   - Date of previous audit
   - Coverage delta (+/- n semantic tokens missing across all themes)
   - Tier leakage delta (+/- n instances)
   - Regression risk delta (+/- n hardcoded values)
   - One sentence: "Theme health is improving / stable / declining since [date]"
   - List newly introduced tier leakage (these are recent regressions)
4. **Save the output** to `recurring.output_directory` using the `recurring.naming_pattern`
5. **Prune old reports** if count exceeds `recurring.retain_count`

If no previous report exists, note "This is the baseline theme audit. Trend analysis will be available from the next run."

## Quality checks

- Coverage matrix includes all semantic tokens and all discovered themes
- Tier leakage findings are clearly separated from coverage gaps — they are architectural problems, not just missing values
- Visual consistency checks reference specific token values, not generic observations
- Regression patterns include specific code examples or counts, not abstract descriptions
- Remediation priority is honest about which findings actually block theming
- DTCG resolver findings (if applicable) validate mode-to-token coverage, not just file structure
- Small-system note is present and contextualised if applicable
- If values were not available for visual consistency check, the report notes which checks were skipped
