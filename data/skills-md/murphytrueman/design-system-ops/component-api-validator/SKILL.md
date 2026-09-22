---
name: component-api-validator
description: "Audit component APIs for consistency, breaking changes, TypeScript coverage, and contract compliance across a component library. Trigger when someone says: component prop review, verify component types are exported, component API audit, check our component interfaces, are our props consistent, API consistency check, prop naming review, breaking change detection, or anything about checking whether component APIs are structurally sound and consistent across the library."
references:
  - ../../knowledge-notes/design-to-code-contract.md
  - ../../knowledge-notes/component-governance.md
---

# Component API validator

A skill for auditing the public API surface of a component library — prop naming consistency, type coverage, default value patterns, breaking change detection, and alignment with the design-to-code contract. Treats the component API as infrastructure: the public contract that consuming teams depend on.

## Context

A component library's most important output is not its visual rendering — it is its API. The props, types, defaults, and composition patterns form a contract with every consuming team. When that contract is inconsistent (some components use `variant`, others use `type`, others use `appearance` for the same concept), unclear (prop types are `any` or undocumented), or unstable (breaking changes ship without versioning), consuming teams lose trust. And when trust erodes, teams start wrapping system components in local abstractions, which is the beginning of drift.

API validation is not about enforcing a single naming convention. It is about detecting where the library's public surface is working against the teams consuming it. A library where every component follows the same patterns for sizing, variants, event handlers, and composition is a library that teams can learn once and apply everywhere. A library where each component invents its own conventions is a library that requires re-learning for every component.

This skill evaluates the API surface as a whole — not one component at a time, but the patterns that emerge across the library. Individual component reviews are useful but miss the cross-library inconsistencies that frustrate consumers most.

---

## Configuration

Check for `.ds-ops-config.yml` in the project root. If present, load:
- `system.framework` — React, Vue, Web Components, Svelte, Angular, etc. (determines prop extraction method)
- `system.styling` — CSS Modules, Styled Components, Tailwind, Emotion, etc.
- `severity.api_*` — overrides for API finding severity
- `integrations.github` — if enabled, pull component source directly from the repo
- `integrations.storybook` — if enabled, extract prop metadata from Storybook's component analysis

## Auto-pull integrations

**GitHub** (`integrations.github.enabled: true`):
- Pull component source files from the configured repository
- Identify the last change date and recent PRs for each component to assess API stability

**Storybook** (`integrations.storybook.enabled: true`):
- Extract argTypes metadata for structured prop information
- Cross-reference Storybook's prop documentation with source code types

**Figma** (`integrations.figma.enabled: true`):
- Pull component property definitions from Figma
- Cross-reference Figma properties against code props for design-to-code alignment

If an integration fails, log it and proceed with manual input.

---

## Step 1: Gather component sources

Ask for or confirm:

1. **Component source path** — directory containing component files (e.g., `src/components/`)
2. **Framework** — React (TSX/JSX), Vue (SFC), Web Components, Svelte, Angular, or other
3. **TypeScript usage** — full TypeScript, JSDoc types, PropTypes, or untyped
4. **Current version** — the published version of the library (for breaking change context)
5. **Previous version source** (optional) — for breaking change comparison. Can be: a git tag, a previous release branch, or the npm-published version

## Step 2: Extract API surface

For each component in the source path:

1. **Identify exported components** — components that are part of the public API (exported from index files or package entry points)
2. **Extract props/attributes**:
   - **React:** TypeScript interfaces, PropTypes, or JSDoc annotations
   - **Vue:** defineProps, props option, or TypeScript interfaces
   - **Web Components:** observed attributes, properties, events, slots, CSS custom properties
   - **Svelte:** exported let declarations, events, slots
3. **For each prop, capture:**
   - Name
   - Type (specific type or `any`/`unknown`/untyped)
   - Required or optional
   - Default value (if any)
   - Description (from JSDoc, TSDoc, or inline comment)
4. **Identify composition patterns:**
   - Does the component accept `children`/`slots`?
   - Does it forward refs?
   - Does it spread remaining props to a root element?
   - Does it accept render props or scoped slots?

## Step 3: Assess cross-library consistency

This is the core of the skill. Evaluate patterns across the entire library, not within individual components.

### 3a. Prop naming consistency

Look for the same concept implemented with different names across components:

| Concept | Consistent pattern | Inconsistent examples |
|---------|-------------------|----------------------|
| Visual variant | All use `variant` | Some use `variant`, others `type`, others `appearance`, others `kind` |
| Size | All use `size` | Some use `size`, others `scale`, others `dimension` |
| Disabled state | All use `disabled` | Some use `disabled`, others `isDisabled` |
| Loading state | All use `loading` | Some use `loading`, others `isLoading`, others `pending` |
| Event handlers | All use `onAction` | Some use `onChange`, others `handleChange`, others `onValueChange` |
| Colour/intent | All use `intent` | Some use `intent`, others `color`, others `severity`, others `status` |

For each inconsistency, report:
- The concept
- Which convention is most common (the likely "correct" one)
- Which components deviate
- Suggested normalisation

### 3b. Boolean prop patterns

Boolean props are a common source of API inconsistency:

1. **Prefix convention** — does the library use `isDisabled` or `disabled`? Pick one, flag deviations.
2. **Negative booleans** — props like `noWrap`, `hideLabel`, `disableAnimation` are harder to reason about than their positive equivalents (`wrap`, `showLabel`, `animate`). Flag negative booleans and suggest positive alternatives where the inversion doesn't lose clarity.
3. **Boolean vs. enum** — a prop that started as boolean (`compact`) but should be an enum (`density: 'compact' | 'default' | 'comfortable'`). Flag booleans that limit future extensibility.

### 3c. Default value patterns

1. **Presence** — do all optional props have explicit defaults? Missing defaults are implicit API decisions.
2. **Consistency** — does `size` default to `'medium'` in some components and `'md'` in others?
3. **Sensible defaults** — does `variant` default to the most common use case? Flag surprising defaults.

### 3d. Type coverage

1. **TypeScript/PropTypes completeness** — what percentage of props have explicit types?
2. **Specificity** — are types specific (`'sm' | 'md' | 'lg'`) or vague (`string`)?
3. **Exported types** — are component prop types exported for consumers who need them?
4. **Generic patterns** — if some components use generics (e.g., `Select<T>`), are they consistently applied?

### 3e. Event handler patterns

1. **Naming convention** — `onChange` vs `onValueChange` vs `handleChange`. Identify the library's convention and flag deviations.
2. **Callback signature** — do event handlers pass the event, the value, or both? Is this consistent?
3. **Controlled vs. uncontrolled** — if the library supports controlled components, is the pattern consistent (`value`/`onChange` vs `defaultValue`)?

### 3f. Composition patterns

1. **Children vs. render props** — is the composition model consistent across components?
2. **Ref forwarding** — do all interactive components forward refs?
3. **Prop spreading** — do components spread remaining props? Is this consistent?
4. **Slot naming** (Vue/Web Components) — are slot names consistent across components?

## Step 4: Breaking change detection

If a previous version is available:

1. **Removed props** — props that existed in the previous version but are gone
2. **Renamed props** — props with different names but same purpose (detected by type + position similarity)
3. **Type narrowing** — prop type changed from wider to narrower (`string` → `'a' | 'b'`)
4. **Default value changes** — default changed in a way that alters existing behaviour
5. **Required prop additions** — new props that are required (existing consumers will break)
6. **Behavioural changes** — same prop name but different behaviour (hardest to detect — flag for manual review)

Classify each:
- **Breaking** — consuming code will fail at compile time or behave differently at runtime
- **Potentially breaking** — may break depending on usage pattern (flag for review)
- **Non-breaking** — addition only, existing code unaffected

## Step 5: Design-to-code contract alignment

Cross-reference the API surface against the design-to-code contract:

1. **Prop coverage vs. design spec** — does every design variant have a corresponding prop? Are there props with no design equivalent (engineering-added functionality)?
2. **State coverage** — does the API support all specified states (default, hover, focus, disabled, loading, error)?
3. **Token alignment** — do any props accept raw values (colours, spacing) that should reference tokens?
4. **Accessibility props** — does the API include necessary accessibility props (aria-label, role, etc.)?

## Step 6: Produce the validation report

```
# Component API Validation Report

## Executive Summary
[Library name, component count, framework, TypeScript coverage, headline findings]

## API Inventory
| Component | Props | Typed | Required | Optional | Defaults | Description coverage |
|-----------|-------|-------|----------|----------|----------|---------------------|
[One row per component]

## Cross-Library Consistency

### Prop Naming
[Table of concept → convention → deviations]
Consistency score: X% (Y/Z props follow the dominant convention)

### Boolean Patterns
[Findings: negative booleans, boolean-should-be-enum, prefix inconsistency]

### Default Values
[Findings: missing defaults, inconsistent defaults]

### Type Coverage
[Overall: X% of props are explicitly typed]
[Breakdown: full TypeScript / JSDoc / PropTypes / untyped per component]

### Event Handlers
[Convention identified, deviations listed]

### Composition Patterns
[Ref forwarding coverage, children vs render props consistency, slot naming]

## Breaking Change Analysis
[If previous version available]
| Change | Component | Prop | Type | Impact |
|--------|-----------|------|------|--------|
[One row per change]

## Design-to-Code Contract
[Findings: design variants without props, props without design equivalents, missing state coverage]

## Findings Summary
[All findings with IDs (AV-01, AV-02, etc.), severity, and remediation]

## Prioritised Recommendations
[Grouped: critical (breaking/type safety) → high (consistency) → medium (documentation) → low (style)]
```

---

## Quality checks

Before delivering the report, verify:

1. **Every exported component is included** — no components skipped
2. **Cross-library patterns are identified** — the report doesn't just list individual component issues but identifies library-wide patterns
3. **Consistency score is quantified** — not "some props are inconsistent" but "73% of components use `variant`, 4 use `type`, 1 uses `appearance`"
4. **Breaking changes are correctly classified** — removals are breaking, additions are non-breaking, type changes depend on direction
5. **Fix suggestions include the specific rename or type change** — not "make this consistent" but "rename `type` to `variant` in AlertDialog, Badge, Toast"
6. **TypeScript type coverage is measured per-component** — not just a library-wide average
7. **Findings reference specific component and prop names** — never "some components have inconsistent naming"

## Small-system note

For libraries with fewer than 10 components: run the same analysis but present as a single consolidated view. Every finding gets individual attention. Consistency is easier to achieve in a small library — the bar should be 100% consistency, not "mostly consistent."
