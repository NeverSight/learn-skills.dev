---
name: token-audit
description: "Audit a design system's token definitions for naming violations, missing semantic tiers, and structural debt. This audits how tokens are defined and organised, NOT how they are consumed in code. Trigger when someone says: audit my tokens, token naming review, are my tokens consistent, token health check, review my token architecture, or anything involving token quality or structure. Do NOT trigger for checking whether code uses tokens correctly — use token-compliance for that."
references:
  - ../../knowledge-notes/token-architecture.md
  - ../../knowledge-notes/output-discipline.md
---

# Token audit

A skill for auditing design token architecture across whichever tiers are in use — typically primitives and semantics, with component tokens where the system uses them. Produces a structured report with severity-rated findings and a prioritised remediation list.

## Context

This skill draws on the tiered token architecture model: primitives encode raw values, semantic tokens encode intent, and — where present — component tokens map intent to specific UI contexts. Not every system uses component tokens, and the absence of a component tier is not a finding. Most token debt accumulates when tiers blur — when component contexts reference primitives directly, when semantic names describe appearance rather than purpose, or when the primitive layer is treated as the only layer.

The audit is not about enforcing a particular naming convention. It's about identifying where the token structure is working against the teams using it.

---

## Configuration

Before producing output, check for a `.ds-ops-config.yml` file in the project root. If present, load:
- `severity.*` — overrides for finding severity ratings (e.g. `hardcoded_color: critical` instead of the default `high`)
- `system.theming` — if true, elevate hardcoded colour findings to the severity specified in config
- `system.styling` — pre-selects the format-specific guidance to apply
- `integrations.style_dictionary` — if enabled, auto-parse tokens via Style Dictionary v4 (see auto-pull below)
- `integrations.figma` — if enabled, pull Figma variables as an additional token source
- `recurring.*` — if this is a recurring run, load the previous report for trend comparison (see recurring workflow below)

If no config file exists, proceed with defaults and manual input as before.

## Auto-pull integrations

If integrations are configured in `.ds-ops-config.yml`, pull data automatically before asking the user for manual input:

**Style Dictionary v4** (`integrations.style_dictionary.enabled: true`):
- Parse the config at `integrations.style_dictionary.config_path`
- Extract the full token tree with resolved references and tier structure
- Use this as the primary token source — skip the manual "provide your token files" question
- If Style Dictionary v4 is installed, run `npx style-dictionary build --config [path] --dry-run` to validate references without writing output

**Figma variables** (`integrations.figma.enabled: true`):
- Use the Figma MCP server to read variables from the file at `integrations.figma.file_key`
- Extract variable collections, modes, and resolved values
- Cross-reference Figma variables against code token files to detect mismatches (Figma says `--color-primary` is `#0066CC` but the code says `#0064CC` — that is a finding)

**GitHub** (`integrations.github.enabled: true`):
- Search the repository for hardcoded colour/spacing values using `gh api search/code` to quantify the scope of violations before the detailed audit
- Pull the token file directly from the default branch if no local file is provided

If an integration is configured but fails (e.g. auth error, rate limit), log the failure and fall back to manual input. Never block the audit because an integration is unavailable.

## Step 0: Token discovery

Before asking the user for files, search the codebase for token-like patterns. This step lowers activation energy for teams where tokens exist but are not centralised — the user does not have to know where all their tokens live.

**What to search for:**

1. **CSS custom properties** — scan all `.css` files for `:root` blocks or `--` prefixed properties. Include scoped variants (`.dark`, `[data-theme="..."]`, `.theme-*`).
2. **SCSS/Sass variables** — scan all `.scss` and `.sass` files for `$`-prefixed names. Follow `@import` and `@use` chains to find partial files (`_colors.scss`, `_variables.scss`, `_tokens.scss`).
3. **JSON/YAML token files** — scan for files matching common token naming patterns: `tokens.json`, `tokens.yaml`, `*.tokens.json`, `design-tokens/**`, `src/tokens/**`, `tokens/**`. Also look for DTCG-formatted files containing `$type` or `$value` keys.
4. **Style Dictionary configs** — scan for `style-dictionary.config.json`, `config.json` in a `style-dictionary/` directory, or `.style-dictionary.json`.
5. **TypeScript/JavaScript token objects** — scan `.ts` and `.js` files for exports matching common patterns: `export const tokens`, `export const theme`, `export default { color`, `as const` typed objects with token-like key hierarchies.
6. **Tailwind configurations** — scan for `tailwind.config.js`, `tailwind.config.ts`, or `tailwind.config.mjs` and extract the `theme` and `extend` blocks.
7. **Figma Tokens / Tokens Studio** — scan for `tokens.json` in a `.tokens` or `tokens` directory, or files exported from Tokens Studio.

**How to search:**

Use file system access (glob patterns, file reads) to scan the project. If GitHub integration is configured, use `gh api search/code` as a secondary source. If Figma integration is configured, pull Figma variables as an additional token source.

Prioritise by specificity: a dedicated `tokens/` directory is more reliable than scattered CSS files. A Style Dictionary config is more reliable than raw JSON. But collect everything — fragmented token sources are themselves a finding.

**Discovery output:**

Produce a brief inventory before continuing:

```
Token sources found:
- src/tokens/colors.json (94 tokens, JSON, likely primitives)
- src/tokens/semantic.json (67 tokens, JSON, likely semantic tier)
- src/styles/variables.scss (43 variables, SCSS)
- tailwind.config.ts (theme block with 28 custom values)
Total: ~232 token-like declarations across 4 sources
```

If discovery finds nothing, proceed to Step 1 and ask the user for manual input. If discovery finds scattered sources across multiple formats, flag this as a finding: "Tokens exist in [N] different formats across [M] files. This fragmentation is structural debt — consider centralising to a single source of truth."

Present the discovered sources to the user and ask: "I found these token sources. Should I audit all of them, or focus on specific files?" This gives the user control without requiring them to have assembled the inventory manually.

---

## Step 0b: Orphan detection checkpoint

Before running the full audit, do a quick pass to identify token usage:

1. **Declared tokens** — count every token found in Step 0 (or provided manually in Step 1).
2. **Referenced tokens** — search the codebase for references to each declared token. For CSS custom properties, search for `var(--token-name)`. For SCSS variables, search for `$variable-name` outside their declaration files. For JSON/DTCG tokens, search for alias references (`{token.path}`). For TypeScript objects, search for import and access patterns (`tokens.color.primary`, `theme.spacing.md`).
3. **Orphaned tokens** — tokens declared but never referenced anywhere in the codebase.

Produce a checkpoint summary:

```
Orphan detection:
- 232 tokens declared
- 189 tokens referenced (at least once)
- 43 tokens orphaned (declared but unreferenced)
  Top orphans: --color-legacy-teal, --spacing-xl-deprecated, $font-heading-alt (3 more)
```

This tells the user the scale of the problem before the full audit begins. Orphaned tokens are maintenance burden without value — they clutter autocomplete, confuse new team members, and inflate the token count. Include orphaned tokens as findings in the main audit (category: Coverage, severity: Low unless count exceeds 20% of total, then Medium).

If the orphan count is high (>30% of total tokens), flag this prominently: "Over a third of declared tokens are unreferenced. Before auditing token quality, consider whether a cleanup pass would simplify the architecture."

---

## Step 1: Gather the token source

If Step 0 discovered token sources, use them as the primary input — skip the manual question unless the user wants to override. If Step 0 found nothing (or was skipped because no codebase access was available), ask for the token source. Acceptable inputs:
- A JSON, YAML, or DTCG-formatted token file
- A Figma file or Tokens Studio export
- A pasted list of token names and values
- A Style Dictionary configuration
- A CSS file with custom properties (e.g. `:root { --color-primary: #5e4890; }` or theme variants scoped to `.dark { }`, `[data-theme="dark"]`, or similar selectors)
- An SCSS/Sass file with variables (e.g. `$color-primary: #5e4890;`)
- A TypeScript or JavaScript token object (e.g. `export const tokens = { color: { ... } }`)
- A Tailwind CSS configuration file (`tailwind.config.js` or `tailwind.config.ts`) with a `theme` or `extend` block defining custom tokens

**Format-specific guidance:**

For **CSS custom properties**: treat each `--` prefixed property as a token. Infer tier from naming patterns — properties like `--color-blue-500` are likely primitives, `--color-action-primary` are semantic, `--button-background-default` are component-tier. Where properties are scoped to selectors (`:root`, `.dark`, `[data-theme="dark"]`), treat each scope as a theme variant. References between CSS custom properties using `var(--other-token)` indicate tier relationships — map these the same way as JSON token references.

For **SCSS variables**: treat each `$` prefixed variable as a token. SCSS variables that reference other variables (e.g. `$color-primary: $blue-500`) indicate tier relationships. If variables are split across partials (`_colors.scss`, `_spacing.scss`), the file organisation may signal tier structure.

For **TypeScript/JavaScript objects**: treat the exported object's key hierarchy as the token structure. Nested objects map to tiers the same way JSON tokens do. For Emotion or styled-components themes, the theme object is the token source. Common patterns include: flat exports (`export const backgroundColor = { scene: '#FFF', primary: '#206EF6' }`), `as const` typed objects (`const tokens = { ... } as const`), aggregated barrel exports (`export const tokens = { breakpoint, fontSize, spacing }`), and theme-to-CSS-variable mapping functions (`mapThemeToVars()`). Helper functions like `mapSpacing()` or `packs.underline` that resolve to token values are valid token references.

For **Tailwind configurations**: the `theme` block defines primitives, `extend` adds semantic overrides. Tailwind utility classes that reference custom tokens (e.g. `bg-primary`, `text-color-content-default`) are token references, not hardcoded values. Arbitrary values in square brackets (e.g. `h-[12px]`, `bg-[#ff0000]`) are the actual hardcoded violations.

If the person pastes raw token names without values, proceed with a naming and structure audit only. Note in the output that value analysis was not possible.

## Step 2: Map the tier structure

Identify which tiers are present:

**Primitive tier** — raw values, no semantic meaning. Examples: `color.blue.500`, `spacing.4`, `font-size.base`

**Semantic tier** — intent-driven references. Examples: `color.action.primary`, `spacing.component.gap`, `text.body.size`

**Component tier** — scoped to a specific component context. Examples: `button.background.default`, `card.padding.inner`

Flag if any tier is missing. A system with only primitives has no semantic contract. A system with only semantic tokens has no single source of truth for raw values. Both are structural problems worth naming.

## Step 3: Run the audit checks

For each check, produce a PASS, WARN, or FAIL rating with specific examples.

### Naming checks

**Descriptive vs prescriptive naming**
Semantic tokens should describe purpose, not appearance.
- FAIL example: `color.semantic.blue` — describes colour, not intent
- PASS example: `color.action.primary` — describes role

**Tier leakage**
Component tokens should reference semantic tokens, not primitives.
- FAIL example: `button.background.default: {color.blue.500}` — skips the semantic tier
- PASS example: `button.background.default: {color.action.primary}` — correct reference chain

**Ambiguity flags**
Token names that could mean multiple things or require context to interpret:
- Examples to flag: `default`, `base`, `normal`, `alt`, `variant`, `misc`, `other`
- Each flagged token should include a suggested rename

**Platform suffix abuse**
Token names that encode platform specifics in the name rather than in the transformation layer:
- Examples: `color.primary.ios`, `spacing.mobile.gap` — these belong in transforms, not names

### Value checks (if values are available)

**Hardcoded values at semantic or component tier**
Any semantic or component token with a raw value rather than a reference is structural debt.
- Flag each occurrence with: token name, raw value found, and suggested reference target

**Duplicate raw values without token aliases**
Identical raw values appearing at the primitive tier under different names without explanation.
- Flag potential duplicates and ask whether the distinction is intentional

**Out-of-tier references**
Any token referencing a token from a higher-specificity tier.
- Example: a semantic token referencing a component token — this inverts the dependency direction

### Coverage checks

**Missing interaction states**
Review whether semantic tokens exist for all standard states: default, hover, active, disabled, focus, error, success, warning.

**Missing dark mode / theme aliases**
If the system intends to support theming, check whether semantic tokens exist as theme-aware aliases or whether raw values are used directly.

**Inconsistent component tier (only if the system uses component tokens)**
If the system has adopted component tokens and they exist for some components but not others in the same category, flag the inconsistency. If the system does not use component tokens at all, this is not a finding — a two-tier architecture (primitives and semantics) is a valid and common choice.

## Step 3b: DTCG 2025.10 alignment assessment (conditional — include only if relevant)

**Skip this section entirely** if the token source is not DTCG format and the team has not mentioned DTCG migration. Most teams don't need this. Include it when the token source uses DTCG format, when the team asks about DTCG compliance, or when migration planning is the purpose of the audit.

If the token source uses DTCG format, or if the team is considering DTCG migration, run these additional checks:

**Type declarations.** Check whether tokens include `$type` fields. DTCG 2025.10 requires one of 13 types: color, dimension, fontFamily, fontWeight, duration, cubicBezier, number, strokeStyle, border, transition, shadow, gradient, typography. Flag tokens without type declarations. Flag tokens with `$type` values not in the DTCG type list. Classification: tokens missing `$type` are WARN if the team is pre-DTCG (informational — count for migration estimate), FAIL if the team has declared DTCG adoption (these tokens break tooling interoperability).

**Composite token integrity.** For composite types (typography, shadow, border, transition, gradient), validate sub-value compliance. A typography token where `fontSize` is a hardcoded value (`"16px"`) but `fontFamily` is a proper reference (`{font.family.body}`) is a partial violation — the composite is inconsistent. A typography token where all sub-values are hardcoded is a full violation — it cannot participate in theming. Report sub-value compliance rate per composite type. Example finding: `TA-14 | WARN | Composite integrity | typography.body: fontSize hardcoded (16px), fontFamily references {font.family.body} — partial violation. Remap fontSize to {dimension.font.size.body}.`

**Resolver and set coverage.** If `.resolver.json` files exist, validate that every semantic token has a value in every declared mode. A semantic token declared in a resolver but missing a mode-specific value is a FAIL — the system will fall back to the default mode unpredictably, which may produce incorrect contrast ratios or broken layouts in the missing mode. Map which sets are composed and identify orphaned tokens (declared but not included in any resolver). Severity: missing mode values for colour tokens are FAIL (contrast risk), missing mode values for spacing tokens are WARN (visual inconsistency but not an accessibility failure).

**Color space declarations.** DTCG 2025.10 supports modern color spaces. Check whether color tokens declare their color space explicitly or rely on implicit sRGB. Flag tokens using hex values where the system could benefit from wider gamut (P3, Lab, OKLab). Severity: INFO for all color space findings — this is a forward-looking check, not a compliance failure.

**Migration readiness (informational).** For teams not yet on DTCG format, produce a detailed migration assessment:

Migration scope quantification:
- Count tokens needing `$type` annotations (total and by tier)
- Count composite tokens needing sub-value restructuring
- Count naming changes required for DTCG compatibility
- Estimate total migration effort with the calibrated effort format from the remediation section

Migration sequence — produce a step-by-step migration plan, not just a numbered list:

**Phase 1 — Annotate primitives (lowest risk)**
Add `$type` fields to all primitive tokens. This is additive — it changes no resolved values and breaks no consumers. Validate with `npx style-dictionary build --dry-run` after each batch.
Estimated effort: [range] hours for [N] primitive tokens, assuming [assumptions].

**Phase 2 — Restructure composites**
Convert typography, shadow, border, and transition tokens from flat values to DTCG composite objects. This changes the token file structure but should not change resolved output if the build tool is correctly configured.
For each composite type, produce a before/after example:
```
Before: { "typography-body": { "value": "400 16px/1.5 Inter" } }
After:  { "typography-body": { "$type": "typography", "$value": { "fontFamily": "{font.family.body}", "fontSize": "{dimension.font.size.body}", "fontWeight": "{font.weight.regular}", "lineHeight": "{dimension.line-height.body}" } } }
```
Estimated effort: [range] hours for [N] composite tokens.

**Phase 3 — Add resolver files**
Create `.resolver.json` files mapping semantic tokens to mode-specific values (light, dark, high-contrast). This is the step that enables multi-theme support.
Estimated effort: [range] hours, scaling with number of modes × number of semantic tokens.

**Phase 4 — Validate with DTCG-compatible tooling**
Run the migrated tokens through Style Dictionary v4 or another DTCG-compatible tool. Fix any remaining validation errors. Produce a diff showing resolved output before and after migration — the resolved values should be identical.
Estimated effort: [range] hours for validation and fix pass.

**Total estimated migration effort:** [sum range] hours, confidence [High/Medium/Low], assumes [key assumptions].

## Step 3c: Token dependency map (conditional — include when codebase access is available)

**Skip this section** if there is no codebase access or if the audit is focused on token naming/structure only. Include it when the user has a codebase connected and wants to understand blast radius before making changes.

Build a map of which components depend on which tokens. This is the blast radius view — before changing `color.action.primary`, you need to know every component that binds to it.

- List each semantic token with its consuming component tokens (direct references)
- List each component token with the component(s) it belongs to
- Identify high-fan-out tokens (referenced by 10+ components) — these are the most dangerous to change
- Identify orphaned tokens (declared but not referenced by any component) — these are maintenance burden without value
- If Figma integration is available, cross-reference: tokens that exist in code but not in Figma (or vice versa) are consistency gaps

Include the dependency map as a section in the report, or as a supplementary output if the map is large.

## Step 4: Produce the audit report

Open with a headline sentence that tells the reader the overall state and where to focus. Example: "Your token architecture has three structural issues — two in the semantic tier and a missing component tier. Here's the full breakdown."

Structure the report as follows:

---

### Token audit report

**Summary**
One paragraph. What is the overall state of the token architecture? What is the most urgent problem? Write this like a peer review, not a compliance filing.

**Tier structure**
- Primitive tier: ✅ present / ⚠️ partial / ❌ absent
- Semantic tier: ✅ present / ⚠️ partial / ❌ absent
- Component tier: ✅ present / ⚠️ partial / ❌ absent
- Tier leakage instances: [count]

**Findings**

List each finding with:
- Finding ID (e.g. TA-01)
- Severity: 🔴 Critical / 🟠 High / 🟡 Medium / ⚪ Low
- Check category: Naming / Value / Coverage
- Description: One sentence
- Example: Specific token or tokens affected
- Recommended action: Specific and actionable

**Remediation priority**
Group findings into three tiers:
1. Fix first — structural problems affecting downstream consumers
2. Fix next — naming debt that compounds over time
3. Address eventually — coverage gaps and nice-to-haves

**Effort estimates**
For each remediation tier, provide calibrated effort estimates with explicit assumptions and caveats:

| Finding | Estimated effort | Assumptions | Confidence |
|---|---|---|---|
| [Finding ID] | [range, e.g. 4–8 hours] | [what this estimate assumes] | [High/Medium/Low] |

Effort estimation rules:
- Always provide a range, never a point estimate. "4–8 hours" not "6 hours."
- State what the estimate assumes: team familiarity with the codebase, no unexpected downstream breakage, tokens are in a single source file vs. scattered, etc.
- Rate confidence as High (similar work has been done before), Medium (reasonable extrapolation from known scope), or Low (significant unknowns remain — flag what would need scoping before commitment).
- If the token count exceeds 200 or the codebase has more than 3 consuming applications, note that estimates should be validated with a timeboxed spike before being committed to sprint planning.
- Never present hours as days without stating the conversion (e.g. "2–3 days assumes 6 productive hours per day").
- For "Fix first" items affecting downstream consumers, include a dependency note: "This estimate covers the token-side change only. Consumer migration adds [X] hours per consuming team — see blast radius."

The goal is estimates a project manager can defend in sprint planning, not optimistic targets that erode trust when overrun.

---

## Recurring workflow

If `recurring` is configured in `.ds-ops-config.yml`:

1. **Before producing output**, check `recurring.output_directory` for a previous token audit report matching the `{skill}-{date}` naming pattern.
2. **If a previous report exists**, load it and compare:
   - Total violation count: increasing, stable, or decreasing?
   - New findings since last run (findings present now but not before)
   - Resolved findings (findings present before but not now)
   - Persistent findings (still present — flag if unaddressed for 2+ cycles)
3. **Add a "Trend since last audit" section** to the report header:
   - Date of previous audit
   - Violation count delta (+/- n)
   - One sentence: "Token health is improving / stable / declining since [date]"
   - List of newly introduced violations (these are the priority — they are recent debt)
4. **Save the output** to `recurring.output_directory` using the `recurring.naming_pattern`.
5. **Prune old reports** if the count exceeds `recurring.retain_count`.

If no previous report exists, note "This is the baseline audit. Trend analysis will be available from the next run." and save the output for future comparison.

## Step 5: Sync with Figma variables (when Figma Console MCP is available)

If the Figma Console MCP from Southleft is connected (check for `figma_get_variables` and `figma_create_variable` tool availability), extend the audit to include Figma variable synchronisation.

**Read:** Use `figma_get_variables` to pull the full variable set from Figma, including resolved values and mode data. Compare against the code token files audited in Steps 1–4. Flag discrepancies — tokens that exist in code but not Figma, tokens that exist in Figma but not code, and value mismatches between the two.

**Export:** Use `figma_get_variables` with `export_formats` to export Figma variables as CSS custom properties, Sass variables, Tailwind config, or TypeScript objects. Present these alongside audit findings so the user can see the exact Figma values in their code's format.

**Create missing variables:** If the audit identified missing semantic-tier tokens (Step 3), offer to create them in Figma using `figma_create_variable`. Only create variables that were explicitly identified as gaps — do not speculatively generate new tokens. Confirm with the user before creating: "The audit found 4 missing semantic colour tokens. Want me to create them in Figma?"

**When the standard Figma MCP is connected (read-only):** The read and export steps work, but variable creation does not. Note which tokens would need to be created manually.

## Closing note (include in every report)

End the report with:

> **A note on context:** This audit sees your token files — it does not see the decisions behind them. Some findings may flag patterns your team chose deliberately. If any finding describes an intentional decision, let me know — I'll exclude it from future runs and learn your system's conventions. The goal is to surface problems you haven't seen yet, not to second-guess choices you've already made.

## Quality checks

- Every finding has a specific example, not a generic description
- The summary paragraph is honest about severity rather than diplomatic
- Remediations are specific: "rename `color.semantic.blue` to `color.action.primary`" not "improve naming"
- The tier structure assessment covers all three tiers
- If values were not available, the report notes which checks were skipped and why they matter
- If Figma variables were compared, code-vs-Figma discrepancies are listed with specific variable names
- The closing note about intentional deviations is present
