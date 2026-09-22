---
name: component-audit
description: "Audit a design system's component library for health, producing a findings-based assessment of usage, complexity, duplication, and coverage gaps with actionable recommendations. This produces a deep, single-dimension audit of the component library, NOT a cross-cutting system health assessment. Trigger when someone says: audit my components, component health, what components do I have, unused components, component coverage, component review, assess my library, or anything about evaluating the quality and health of a component library. Do NOT trigger for building machine-readable index files or dependency graphs for AI agents — use codebase-index for those. Do NOT trigger for a holistic health summary — use system-health for that."
references:
  - ../../knowledge-notes/component-governance.md
  - ../../knowledge-notes/component-bestiary-reference.md
  - ../../knowledge-notes/output-discipline.md
---

# Component audit

A skill for auditing a design system's component library across four dimensions: usage signals, complexity distribution, duplication, and coverage gaps. Produces an inventory with tiered findings and a prioritised action list.

## Context

Component libraries accumulate silently. New components arrive through contributions. Old components persist because nobody wants to be the one who removes them. Variants proliferate because each edge case adds one more. The result is a library that grows in mass without growing proportionally in value.

A component audit brings the library back into focus: what is there, what is used, what duplicates what, and what is missing that teams have been building around. It is the maintenance work that makes the next year of development faster.

---

## Configuration

Before producing output, check for a `.ds-ops-config.yml` file in the project root. If present, load:
- `system.framework` — pre-selects framework-specific inventory guidance
- `system.component_count` — pre-populates the small-system gate
- `severity.*` — overrides for finding severity ratings
- `integrations.*` — enables auto-pull for component data (see below)
- `recurring.*` — enables comparison with previous audit

## Auto-pull integrations

If integrations are configured in `.ds-ops-config.yml`, pull data automatically:

**Figma MCP** (`integrations.figma.enabled: true`):
- Read the published library from `integrations.figma.file_key` via Figma MCP
- Extract the component inventory: names, variant counts, description status
- Use Figma library analytics (if available via REST API) to pull detach rates per component — high detach rates are a direct usage signal
- Cross-reference the Figma inventory against the code inventory to detect components that exist in design but not in code (or vice versa)

**npm registry** (`integrations.npm.enabled: true`):
- Pull download statistics for `integrations.npm.package_name` (or each package in `integrations.npm.scoped_packages` for monorepos) using `npm view [package] --json` or the npm registry API
- Use download trends (last 30 days, last 90 days) as a usage signal in Dimension 1
- For monorepos: note that per-package downloads are unreliable (see monorepo handling) — use as a directional signal only

**Storybook** (`integrations.storybook.enabled: true`):
- Fetch the story index from `integrations.storybook.url/index.json`
- Extract component list, story counts per component, and documentation status
- Components with zero stories are likely undocumented — flag in Dimension 1

**GitHub** (`integrations.github.enabled: true`):
- Use `gh api search/code` to count import references for each component across consuming repositories
- Pull PR activity for the component library — components with no PRs in 12+ months are likely stale
- Pull open issues tagged with component names to surface known problems

**Documentation platform** (`integrations.documentation.enabled: true`):
- If platform is `zeroheight`: use the Zeroheight API to pull page list and last-updated dates per component
- If platform is `supernova`: use the Supernova API to pull component documentation coverage
- If platform is `storybook`: same as Storybook integration above (docs tab status)
- Map documentation coverage to the component inventory — components without docs pages are flagged in Dimension 3

If an integration fails, log it and proceed with manual input.

## Step 0: Identify what you're looking at

Before auditing components, determine what kind of shared UI this is. The library type changes which dimensions matter and how findings should be framed.

**Classify from codebase signals:**

- **Design system** — Full template applies. All four audit dimensions (usage, complexity, duplication, coverage) plus composition graph and AI readiness.
- **Component library** — Focus on complexity distribution, duplication, and coverage gaps. Usage signals may not exist yet — note this rather than flagging it as a problem. Skip AI readiness unless the team has signalled interest.
- **Pattern library** — Focus on duplication and documentation completeness per pattern. Complexity distribution is less meaningful because patterns are reference implementations, not consumed packages. Coverage gaps should be framed as "patterns your team builds frequently but hasn't documented" rather than "components missing from the system."
- **Utility collection** — Focus on duplication and naming consistency. A utility collection with overlapping helpers is actively harmful; one with clear, non-overlapping utilities is doing its job. Skip coverage gaps — a utility collection is not trying to be comprehensive.

**Include the classification in the report header** as "Library type: [Design system / Component library / Pattern library / Utility collection]" and skip dimensions that don't apply.

---

## Step 1: Gather the component inventory

Ask for or confirm (skip questions already answered by auto-pull):
- Access to the component library: Figma library, Storybook, npm package, or component documentation
- The framework and component format: React (JSX/TSX), Vue SFC (`.vue`), Twig/Fractal (`.twig`), Svelte (`.svelte`), or Web Components
- Whether this is a monorepo or single-package library (see monorepo handling below)
- Any usage data available: adoption signals, access logs, consumer surveys, or engineering usage stats
- Any known problem areas: components teams avoid, components with open bug reports, components that frequently generate support questions

If usage data is not available, the audit focuses on structural assessment rather than usage analysis. Note in the output which findings are based on direct analysis and which are inferred from structure.

**Small-system note (fewer than 5 components):** With 1–4 components, the audit shifts from pattern detection to per-component deep dive. Skip complexity distribution analysis (Step 3, Dimension 2) — it is not meaningful at this scale. Instead, focus on: completeness of each component's API and state coverage, documentation status per component, and whether the system covers the team's highest-frequency needs. The coverage gaps dimension (Step 3, Dimension 4) becomes the most valuable — what common patterns are teams building locally because the system does not yet provide them? The answer to that question is the system's roadmap.

## Step 1b: Define usage signals

Before proceeding to inventory and audit, establish which usage signals will ground the assessment in Dimension 1. Ask the user:

"Which usage signals will you track to assess component usage? Select all that apply:"

- **Figma instantiations** — Detach rates on design library components (high detach rates indicate a component that does not serve its consumers well)
- **Code imports** — References to component imports across the codebase, counted by frequency
- **Production shipping** — Components present in actively deployed products vs. unused/experimental
- **Support tickets** — Questions, bug reports, or support volume per component
- **Download stats** — npm downloads (if applicable) or analytics from a component documentation platform
- **User surveys** — Direct feedback from consuming teams about component utility

Document which signals are available for this audit. Usage assessment in Dimension 1 is only as strong as the signals used — if only one signal is available, note that the usage assessment is based on limited data and may be incomplete.

**Monorepo handling:**

Monorepo structures break standard usage signals. A component published as `@system/button` in its own package may show high npm downloads while `@system/date-picker` shows low — but the download count reflects bundling behaviour, not actual component usage by teams. Apply these adjustments:

- **Per-package download counts are unreliable.** In monorepos, teams often install the umbrella package or a subset of packages. Use import analysis across consuming products instead of download counts where possible.
- **Detect versioning patterns:** Components with `-next` or `-v2` suffixes (e.g. `button-next`, `DataTableV2`) indicate in-flight migrations. Count both versions but flag the pair — the older version is a deprecation candidate, the newer is not yet fully adopted. Neither version's usage number is accurate in isolation.
- **Classify private vs. public components:** Components with underscore prefixes (`_InternalBase`, `_LayoutHelper`), components in directories named `internal/`, `private/`, or `utils/`, and components not re-exported from the package's public barrel file (`index.ts`) are internal implementation details. Exclude them from the public component count and from coverage gap analysis. Count them separately as "internal utilities."
- **Distinguish utility components from user-facing components:** Layout primitives (`Box`, `Stack`, `Flex`, `Grid`, `VisuallyHidden`, `Portal`) are infrastructure components, not user-facing UI. They should be counted in the inventory but categorised separately. A library with 30 components where 15 are layout utilities and 15 are UI components has a different health profile than one with 30 UI components.

**Framework-specific inventory notes:**

- **Vue SFC:** Each `.vue` file in the components directory is typically one component. Check for `<script setup>` vs Options API — mixed patterns across the library are a consistency finding.
- **Twig/Fractal:** Components are organised by Atomic Design convention (`01-atoms/`, `02-molecules/`, `03-organisms/`). The Fractal config (`fractal.config.js`) defines the component engine and paths. Each `.twig` file with an associated `.config.yml` or `.config.js` is a component.
- **Emotion/CSS-in-JS:** Components may be split across multiple files (`Component.tsx` + `styles.ts`). Count by exported component, not by file. Monorepo packages like `@system/core` may contain dozens of components in subdirectories.

## Step 2: Build the inventory

Create a working inventory of all components:
- Component name
- Category (navigation, form, feedback, layout, data display, etc.)
- Variants/configurations available
- Last updated (if accessible)
- Known usage status (actively used / unknown / suspected unused)
- Documentation status (complete / partial / none)

If the inventory does not yet exist, building it is Step 1 of the audit and may be the most valuable output in its own right.

## Step 3: Audit across four dimensions

### Dimension 1: Usage signals

Assess what usage data is available and what it suggests.

Direct signals (if available):
- npm download stats or package consumption data
- Figma library detach rates (high detach rates indicate a component that does not serve its consumers well)
- Storybook visit data
- Support channel questions and frequency

Indirect signals (structural inference):
- Components with no documentation are less likely to be found and used
- Components added more than twelve months ago with no subsequent updates in an active system may be unused
- Components with naming that diverges from the system's conventions may have been added before conventions were established — often early experiments that were never removed

For each component, assign a usage status: Actively used / Likely used / Unknown / Likely unused / Confirmed unused

Flag all "Likely unused" and "Confirmed unused" for the action list.

### Dimension 2: Complexity distribution

Assess the distribution of component complexity across the library.

**Foundational components** — primitives that serve as building blocks. Buttons, inputs, checkboxes, typography elements, icons. These should make up the largest portion of the library.

**Compound components** — compositions of foundational components. Cards, modals, dropdowns, navigation bars. These should be fewer than foundational components.

**Feature components** — components with significant built-in logic or high specificity to a particular product context. These are the category most likely to proliferate and least likely to be reusable.

Flag any library where:
- The ratio of feature components to foundational components is high — this suggests the system has accumulated product-specific work that belongs locally
- Compound components outnumber foundational components — this often indicates missing foundational pieces that teams have compensated for by building up rather than down
- Components at the same level of the complexity hierarchy have highly inconsistent prop counts — outlier complexity often indicates a component trying to do too many jobs

### Dimension 3: Duplication

Find components that solve the same problem with different implementations.

Look for:
- Multiple components with overlapping use cases (e.g. `Toast`, `Snackbar`, and `Alert` all in the same system without clear distinctions)
- Components that are effectively variants of another component rather than distinct components
- Multiple components with names that suggest similar roles (`Modal` and `Dialog`, `Popover` and `Tooltip` — flag these for disambiguation even if they are genuinely distinct, because the distinction needs to be explicit)

For each duplication finding: describe what overlaps, note whether the components are genuinely distinct or redundant, and recommend either documenting the distinction or deprecating the redundant one.

#### Deduplication decision rubric

For each potential duplication finding, use this worksheet to make the decision systematically:

**For each pair of overlapping components (Component A and Component B):**

1. **Problem definition:**
   - What problem does Component A solve? (Be specific: e.g., "Transient feedback to user actions" vs. "Persistent notifications")
   - What problem does Component B solve?
   - Are these the same problem or different problems?

2. **If the problems are the same:**
   - Which component has the better API? (More intuitive prop names, fewer required props, easier to configure the common case)
   - Which has better accessibility? (Keyboard navigation, ARIA attributes, focus management, semantic HTML)
   - Which has wider adoption across consuming teams?
   - **Decision:** Keep the component that is strongest across these three dimensions. Deprecate the other with a migration path.

3. **If the problems are different:**
   - Document the distinction explicitly in both components' descriptions. The distinction needs to be clear enough that a new team member chooses correctly without asking for help.
   - Flag if the names could be clearer (if they still suggest similarity, rename one or both for clarity).

Document this worksheet as part of the audit output. It makes deduplication decisions defensible and repeatable.

### Dimension 4: Coverage gaps

Identify common patterns that teams regularly need but the system does not provide.

Sources for gap identification:
- Components that appear in consumer codebases but not in the system (drift detection is a more focused version of this analysis)
- Patterns referenced in design documentation or prototypes that have no component equivalent
- Common UI patterns (date pickers, data tables, drag-and-drop, infinite scroll) that the system lacks
- Components that are present but lack key variants or states that teams consistently add locally

For each gap: assess whether it is a genuine system gap (the need is common enough to belong in the system) or a local need (one team's requirement that is appropriately local).

#### Tie-in to drift detection: Coverage gaps as system signals

Coverage gaps identified in this dimension often correspond to **Classification E (system gap)** findings in drift-detection. If running both skills in the same session:

- Cross-reference coverage gaps identified here against drift detection findings
- A coverage gap that already has drift evidence is a stronger candidate for system addition than one identified structurally alone
- For example: if the component audit flags "date picker" as a gap, and drift-detection finds three products with local date picker implementations, that is stronger evidence than the gap alone
- Document this cross-reference in the action list: which gaps have supporting drift evidence, and which are identified from structural assessment only

This connection improves prioritisation — gaps with drift evidence indicate teams are already solving the problem locally, which raises the urgency of system provision.

## Step 3b: Composition dependency graph

Build a dependency graph of component composition relationships. This is the blast-radius view for component changes.

**How to build the graph.** Use whatever source is available, in order of reliability: (1) Component source code — look for import statements that reference other system components, JSX/template renders of system components, and component-tier token references in styled-components, CSS modules, or Tailwind classes. (2) Storybook story index — stories often reveal composition through `subcomponents` declarations and story decorators. (3) Figma component variants — layer structure shows composition visually. (4) Manual inventory — if none of the above are accessible, ask the team to list composition relationships. The skill should state which method was used, as it affects confidence.

**For each component, identify:**
- **Composes** — which other system components does this component render internally? (e.g., `Card` composes `Text`, `Button`, `Icon`)
- **Composed in** — which other system components render this component? (e.g., `Icon` is composed in `Button`, `Card`, `NavItem`, `Alert`)
- **Fan-in count** — how many other components depend on this component? High fan-in = high blast radius for breaking changes
- **Fan-out count** — how many other components does this component use? High fan-out = high coupling, fragile to upstream changes

**Identify critical path components:**
- Root components (fan-in of 0) — these are leaf components; changes are isolated
- Foundation components (fan-in of 5+) — changes propagate widely; these are the system's load-bearing primitives
- Hub components (high fan-in AND high fan-out) — these are integration risks; they both depend on many things and are depended on by many things
- Leaf components (fan-out of 0, fan-in of 0) — these are standalone; often candidates for removal if unused

**Token-to-component dependency:**
- Map which tokens each component binds to (from the component's source or from component-tier token names)
- Identify shared token hotspots — tokens referenced by 10+ components are the most dangerous to change
- Cross-reference with the token-audit's dependency map if both audits are running in the same session

**Answering "if I change X, what breaks?"** The graph should be queryable. For any component or token, the report should make it possible to trace: (1) direct consumers — components that import/compose this component, (2) indirect consumers — components that compose the direct consumers, and (3) product-level impact — if integration data is available, which products/teams are affected. Example: "Changing `Icon` directly affects 14 components (Button, Card, NavItem, Alert, ...). Indirectly affects 23 components through Button alone. Products affected: Checkout (12 Icon instances), Dashboard (34 instances), Mobile (8 instances)."

Include the composition graph as a section in the report. For systems with 20+ components, produce a summarised version (top 10 highest fan-in, all hub components, orphaned components) with the full graph available as a supplementary output.

## Step 3c: AI-readiness assessment

Assess the library's readiness for AI consumption. This identifies what work is needed to make the system machine-readable.

**Per-component checklist:**
For each component, check whether the following exist:
- **Purpose clarity:** Does the component have a description that distinguishes it from similar components?
- **Prop documentation:** Are all props documented with types, defaults, and intent?
- **Anti-pattern coverage:** Are component-specific misuse patterns documented?
- **Composition rules:** Are placement constraints and containment rules explicit?
- **Accessibility documentation:** Are keyboard patterns, ARIA contracts, and focus management documented?

**System-level indicators:**
- Component manifest: Does a machine-readable JSON index of components exist? (Y/N)
- Structured metadata: Do most components have machine-readable metadata beyond text descriptions?
- Description consistency: Do most components follow a consistent description format?
- Figma-code sync: Do Figma descriptions match code documentation?
- Challenge Rating coverage: Do components have an assigned CR for documentation depth calibration?

Produce a summary table showing which components have which checklist items. Flag components missing three or more items as priorities for AI-readiness work. Include specific recommendations for each missing area.

## Step 3d: Maturity level assessment

Based on the audit findings across all dimensions, assess the system's maturity level:

**Ad-hoc:** Components exist but are ungoverned. No consistent naming, no contribution process, inconsistent documentation.
**Managed:** Library exists with some governance. Token architecture established. Documentation exists but varies in depth.
**Systematic:** Consistent API contracts. Standard documentation format. Contribution and deprecation processes documented. Predictable release cadence.
**Measured:** Adoption tracked quantitatively. Drift detected and classified. Health assessed across dimensions. Recurring reviews on a cadence.
**Optimised:** Platform infrastructure. Versioned APIs with semver. Machine-readable manifests. Consumer contract testing. Calibrated quality bar.

Assess each dimension (usage, complexity, duplication, coverage, dependency graph, AI-readiness) against these maturity stages. The system's overall maturity is the lowest stage where it meets criteria across all dimensions — a system that is measured on usage but ad-hoc on documentation is effectively ad-hoc.

Include the maturity assessment in the report with: current stage, evidence for the assessment, and specific actions needed to reach the next stage.

## Step 4: Produce the audit report

---

### Component audit report

Open with a headline sentence that tells the reader the overall state and where to focus.

**Date:** [date]
**Library size:** [total component count]
**Audit method:** [direct inspection / structural inference / combined]

---

#### Summary

One paragraph. What is the library's overall condition? What is the most significant finding across the four dimensions?

---

#### Inventory summary

| Category | Count | Actively used | Unknown | Likely/confirmed unused |
|---|---|---|---|---|
| Navigation | | | | |
| Forms | | | | |
| Feedback | | | | |
| Layout | | | | |
| Data display | | | | |
| Other | | | | |
| **Total** | | | | |

---

#### Findings by dimension

Findings formatted as: ID, component or category, finding description, recommended action, priority.

**Severity key:** 🔴 Critical / 🟠 High / 🟡 Medium / ⚪ Low

---

#### Action list

Prioritised:

**Immediate:**
- Components to deprecate (confirmed unused with no migration risk)
- Duplicates to resolve

**Planned:**
- Documentation gaps to address
- Coverage gaps to assess for contribution

**Review:**
- Components with unknown usage status (need usage data before action)
- Feature components that may belong locally

---

## Closing note (include in every report)

End the report with:

> **A note on context:** This audit sees your component library — it does not see the product decisions, team constraints, or historical context behind it. Some findings may flag patterns your team chose deliberately. If any finding describes an intentional decision, let me know — I'll exclude it from future runs and learn your system's conventions. The goal is to surface problems you haven't seen yet, not to second-guess choices you've already made.

---

## Quality checks

- Inventory is complete — no components are described generically ("there are many button variants") without being enumerated
- Usage status is based on available signals, not assumed
- Duplication findings distinguish between genuinely overlapping components and components that are distinct but similarly named
- Coverage gaps are assessed for whether they belong in the system, not just listed
- Action list prioritises by impact, not by ease
- The closing note about intentional deviations is present
