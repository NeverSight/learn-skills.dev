---
name: codebase-index
description: "Generate a pre-computed component index from a design system codebase — YAML infrastructure files containing a component inventory, relationship graph, and summary statistics that AI agents and MCP servers consume. This produces machine-readable index files in .ai/index/, NOT a health report or quality assessment. Trigger when someone says: index my codebase, build a relationship graph, create a component map, codebase index, what depends on what, dependency graph, map component relationships, or anything about producing queryable infrastructure files for AI agents or developer tooling. Do NOT trigger for component health assessments, quality scores, or audit reports — use component-audit for those."
references:
  - ../../knowledge-notes/ai-readiness.md
  - ../../knowledge-notes/component-governance.md
---

# Codebase index

A skill for generating a pre-computed, machine-readable index of a design system's codebase. The index contains three pieces: a component inventory, a relationship graph, and summary statistics. Together they form a queryable map that eliminates the need for AI agents or developers to explore the codebase from scratch every time they need to understand the system.

## Context

When an AI agent needs to work with a design system codebase, it has two options: explore or navigate. Exploration means scanning directories, grepping for imports, reading files one by one. Navigation means loading a pre-computed index and reasoning over cached data.

The difference matters. Exploration is slow, incomplete, and non-deterministic. An agent scanning `src/components` might miss components in `src/layouts`, `src/pages`, or utility directories that don't follow naming conventions. It might report a deeply-nested component as "unused" because it can't trace the dependency chain. It might recreate an existing component because it didn't find it.

A pre-computed index front-loads this cost. The agent loads the index once — typically a few thousand tokens — and gets a complete picture of what exists, where things live, and how they relate. Follow-up questions become cheap because the agent reasons over cached data instead of triggering new file reads.

This skill generates that index. Run it after adding or removing components, and commit the output alongside the code.

---

## Configuration

Before producing output, check for a `.ds-ops-config.yml` file in the project root. If present, load:
- `system.framework` — pre-selects framework detection (React, Vue, Svelte, Astro, Angular, etc.)
- `system.component_paths` — overrides default component directory scanning
- `system.category_model` — atomic design, functional, or custom categorisation
- `integrations.*` — enables auto-pull for component data
- `recurring.*` — enables comparison with previous index

## Auto-pull integrations

If integrations are configured in `.ds-ops-config.yml`, pull data automatically:

**Figma MCP** (`integrations.figma.enabled: true`):
- Read the published library from `integrations.figma.file_key`
- Cross-reference the Figma component inventory against the code inventory to detect components that exist in design but not in code (or vice versa)
- Pull description status per component to populate the metadata coverage field

**Storybook** (`integrations.storybook.enabled: true`):
- Fetch the story index from `integrations.storybook.url/index.json`
- Extract component list and documentation status
- Use as a secondary source for component discovery

**GitHub** (`integrations.github.enabled: true`):
- Use `gh api search/code` to count import references across consuming repositories
- Pull PR activity for recency signals

If an integration fails, log it and proceed with manual scanning.

---

## Step 1: Detect the framework and structure

Scan the project root to determine:
- **Framework**: React (JSX/TSX), Vue (SFC), Svelte, Astro, Angular, Web Components, or mixed
- **Component directories**: Where components live — scan common locations: `src/components/`, `src/lib/`, `components/`, `packages/`, and any paths in `tsconfig.json` or framework config
- **Category model**: How components are organised — atomic design (`atoms/`, `molecules/`, `organisms/`), functional (`forms/`, `navigation/`, `feedback/`), flat, or monorepo packages
- **Styling approach**: CSS modules, CSS-in-JS, Tailwind, SCSS, or design tokens — this determines how to trace token dependencies

Ask for or confirm (skip questions already answered by config or detection):
- The component source root if auto-detection finds multiple candidates
- Whether there are components in non-standard locations (e.g., a shared `utils/` directory with reusable UI primitives)
- Whether to include internal/private components in the index (underscore-prefixed, `internal/` directories, components not re-exported from barrel files)

**Framework detection rules:**

| Signal | Framework |
|---|---|
| `.jsx` / `.tsx` files with JSX returns | React |
| `.vue` files with `<template>` blocks | Vue |
| `.svelte` files | Svelte |
| `.astro` files | Astro |
| `.component.ts` with `@Component` decorator | Angular |
| `customElements.define()` | Web Components |
| Mixed signals | Ask the user |

## Step 2: Scan and build the component inventory

For every component file found, extract:

- **Name**: The component's exported name
- **Path**: Relative path from project root
- **Category**: Based on the category model (atom, molecule, organism, etc.) or functional category (navigation, form, feedback, layout, data display)
- **Metadata status**: Whether the component has structured metadata (a `.metadata.ts`, `.metadata.json`, description in Storybook, JSDoc/TSDoc block, or Figma description)
- **Export type**: Default export, named export, or re-exported through a barrel file

**What counts as a component:**
- Files that export a renderable element (JSX, template, render function)
- Files explicitly registered in a component index, barrel file, or Storybook config
- Exclude: pure utility functions, hooks/composables (unless they return JSX), type definitions, test files, story files

**Category assignment:**
- If the directory structure encodes categories (atomic design folders, functional folders), use directory position
- If the structure is flat, infer from component characteristics: components with no child components are atoms/primitives, components that compose other system components are compounds, components with significant built-in logic or product-specific context are features
- If uncertain, assign `uncategorised` and flag for manual review

### Inventory format

Produce the inventory in YAML for readability and token efficiency:

```yaml
components:
  Button:
    path: src/components/atoms/Button/Button.tsx
    category: atoms
    metadata: true
  Card:
    path: src/components/molecules/Card/Card.tsx
    category: molecules
    metadata: true
  DataTable:
    path: src/components/organisms/DataTable/DataTable.tsx
    category: organisms
    metadata: false
```

## Step 3: Build the relationship graph

For every component in the inventory, trace two relationships:

- **uses**: Which other system components does this component import and render?
- **usedBy**: Which other system components import and render this component?

**How to trace relationships:**
1. Parse import statements in each component file
2. Filter to imports that reference other components in the inventory (ignore external package imports, utility imports, type imports)
3. For each import, verify it's actually rendered in the template/JSX (an unused import is not a relationship)
4. Record the relationship bidirectionally — if Card imports Button, then Card `uses` Button and Button `usedBy` Card

**Deep tracing rules:**
- Follow dependency chains to their leaves. If a page imports a layout, and the layout imports a nav, and the nav imports a link and an icon — the full chain matters for understanding which atoms actually appear on that page.
- Components with `uses: []` (empty) are leaf nodes — they have no internal dependencies on other system components. These are the terminal nodes in the graph.
- Components with `usedBy: []` (empty) are root nodes — nothing else in the system depends on them. If they're also not used directly in pages, they're orphan candidates.

**Instance counting:**
Import count and instance count are different metrics. A page might import Button once but render it five times. Instance counting requires parsing templates, not just import statements.
- Count `<ComponentName` tags in templates/JSX for instance counts
- Detect slot/children components: if Button contains a `<slot />` and someone writes `<Button><Icon /></Button>`, the Icon instance belongs to the parent scope, not to Button's internals. Don't recurse into slot content for instance counting.

### Relationship graph format

```yaml
relationships:
  Card:
    uses: [Text, Button, Icon]
    usedBy: [ProductCard, UserProfile]
  Button:
    uses: [Icon]
    usedBy: [Card, Form, Nav, Modal, Dialog, Header]
  Icon:
    uses: []
    usedBy: [Button, Card, Nav, MenuItem, Alert]
  Tooltip:
    uses: []
    usedBy: [CopyButton]
  CopyButton:
    uses: [Tooltip]
    usedBy: [CodeBlock]
```

This format makes dependency chains explicit. An agent reading this graph knows immediately that Tooltip is actively used (by CopyButton, which is used by CodeBlock) even though no page imports Tooltip directly.

## Step 4: Generate summary statistics

Compute aggregate metrics that give an at-a-glance picture of system health:

```yaml
summary:
  totalComponents: 55
  componentsWithMetadata: 54
  relationshipsMapped: 302
  categories:
    atoms: 18
    molecules: 15
    organisms: 12
    templates: 4
    pages: 6
  orphanedComponents: 2
  mostDependedOn:
    - name: Icon
      fanIn: 14
    - name: Button
      fanIn: 11
    - name: Text
      fanIn: 9
  highestFanOut:
    - name: Header
      fanOut: 8
    - name: ProductCard
      fanOut: 6
  metadataCoverage: 98%
  averageInstancesPerComponent: 9.6
```

**Key metrics to compute:**
- **totalComponents**: Count of all components in the inventory
- **componentsWithMetadata**: Count of components with structured metadata files or descriptions
- **relationshipsMapped**: Total number of relationship edges in the graph (sum of all `uses` arrays)
- **categories**: Breakdown by category model
- **orphanedComponents**: Components with both `uses: []` and `usedBy: []` — these are standalone and may be unused
- **mostDependedOn**: Top components by fan-in count (usedBy length). These are foundation components — changes propagate widely
- **highestFanOut**: Top components by fan-out count (uses length). These are integration points — fragile to upstream changes
- **metadataCoverage**: Percentage of components with structured metadata
- **averageInstancesPerComponent**: Total instances across all pages divided by total components (if instance counting was performed)

## Step 5: Produce the index output

Generate three output files to be committed alongside the codebase:

### File 1: `component-inventory.yml`
The full component inventory from Step 2.

### File 2: `component-relationships.yml`
The full relationship graph from Step 3 plus the summary statistics from Step 4.

### File 3: `query-protocols.md`
A markdown file with instructions for how to use the index. This file teaches AI agents (or developers) how to read the map:

```markdown
# Query protocols

When answering questions about the design system codebase:

1. Check the index first. Before reading any source file, check whether the
   answer exists in component-inventory.yml or component-relationships.yml.

2. Never re-read relationship files. If the relationship graph has already
   been loaded in this session, reason over the cached data.

3. Follow-up questions should be cheap. After the initial index load,
   subsequent questions should require zero or minimal file reads.

## Common query patterns

### "What components exist?"
→ Read component-inventory.yml. The full list with paths and categories.

### "Where is [Component] used?"
→ Check component-relationships.yml → relationships → [Component] → usedBy.

### "What does [Component] depend on?"
→ Check component-relationships.yml → relationships → [Component] → uses.

### "Is [Component] actually used?"
→ Check usedBy. If usedBy is non-empty, it's used. If usedBy is empty,
  check whether it appears in any page or layout file directly.

### "What atoms appear on [Page]?"
→ Trace the dependency chain: Page → imports → their imports → ...
  until you reach components with uses: []. Those are the atoms.

### "If I change [Component], what breaks?"
→ Follow the usedBy chain recursively. Direct consumers are in usedBy.
  Indirect consumers are the usedBy of those consumers. Continue until
  you reach page/layout level.

### "Should I create a new component for [pattern]?"
→ Check the inventory for existing components that might serve the need.
  Check relationships to understand composition options. A new component
  is warranted only if no existing component or composition covers it.
```

## Step 6: Output location and integration

**Default output location**: `.ai/index/` in the project root. This keeps the index files co-located with the codebase and clearly namespaced.

```
.ai/
  index/
    component-inventory.yml
    component-relationships.yml
    query-protocols.md
```

**Recommend to the user:**
- Commit these files to version control alongside the code
- Re-run the index after adding, removing, or significantly restructuring components
- Add an npm script or CI step to regenerate the index on changes to the component directories
- Reference the query-protocols.md in any AI agent configuration or system prompt that interacts with the codebase

## Recurring workflow

If `recurring.enabled: true` in config, compare the new index against the previous one and produce a delta report:

- **Added components**: Components in the new index that were not in the previous one
- **Removed components**: Components in the previous index that are no longer present
- **New relationships**: Dependency edges that did not exist before
- **Broken relationships**: Dependency edges that existed before but are now gone
- **Metadata coverage change**: Did coverage go up or down?
- **New orphans**: Components that became orphaned since last index

This delta is valuable for tracking system evolution over time and catching unintentional structural changes.

---

## Quality checks

- Every component file in the scanned directories is accounted for in the inventory — no files are silently skipped
- Relationship graph is bidirectional — if A uses B, then B's usedBy includes A
- Summary statistics are consistent with the inventory and graph data (totals match, percentages are accurate)
- Category assignment is based on the detected or configured model, not assumed
- Internal/private components are either included or excluded consistently based on user preference
- The query-protocols.md is tailored to the specific project's structure, not generic
