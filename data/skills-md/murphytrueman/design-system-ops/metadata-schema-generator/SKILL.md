---
name: metadata-schema-generator
description: "Generate structured JSON metadata schemas for design system components — machine-readable constraint definitions that encode props, behavioural rules, composition constraints, prohibited combinations, and accessibility contracts as programmatic data. This produces JSON files for tooling (MCP servers, linters, code generators, test frameworks), NOT text descriptions for humans or Figma. Trigger when someone says: generate metadata schema, JSON schema for components, component contract as JSON, structured metadata for tooling, prop constraints as data, machine-readable component rules, or anything about producing JSON/structured data that tools consume programmatically. Do NOT trigger for Figma descriptions, component documentation, or AI-readable text — use ai-component-description for those."
references:
  - ../../knowledge-notes/ai-readiness.md
  - ../../knowledge-notes/component-bestiary-reference.md
---

# Metadata schema generator

A skill for generating structured JSON metadata schemas for design system components. These schemas encode everything an AI agent, MCP server, code generator, or testing framework needs to work with a component programmatically — props, behavioural rules, composition constraints, accessibility contracts, and business context — in a format that does not require natural language parsing.

## Context

Component documentation serves humans. Component metadata serves machines. The distinction matters because the information needs are different, the format requirements are different, and the failure modes are different.

A human reading a component's documentation can infer that "this button triggers the primary action" means it should be visually prominent and placed in the expected location. A code generation agent reading that same string cannot infer any of that — it needs explicit data: `{ "role": "primary_action", "visual_weight": "high", "placement": ["form_footer", "dialog_footer", "page_header"] }`.

Most design systems have one layer of machine-readable data: TypeScript interfaces or PropTypes declarations that define prop names and types. This is necessary but insufficient. A TypeScript interface tells a tool that a Button accepts a `variant` prop of type `"primary" | "secondary" | "ghost"` — but it does not tell the tool when to use `primary` vs `secondary`, which combinations of props are prohibited, where the component can be placed in a layout, or what accessibility contract it must honour.

Structured metadata fills this gap. It encodes the knowledge layer between "what the component accepts" (TypeScript) and "how the component should be used" (documentation) as machine-readable data that tooling consumes directly.

The `ai-component-description` skill produces text descriptions optimised for LLM consumption. This skill produces structured data optimised for programmatic consumption. Together they serve the two modes of AI interaction: conversational (descriptions) and deterministic (metadata).

## Boundaries

This skill generates structured JSON metadata schemas for tooling consumption — not human-readable documentation (use `usage-guidelines` or `pattern-documentation` for that) or LLM-facing descriptions (use `ai-component-description`). If the system has no component inventory yet, run `component-audit` or `codebase-index` first. If the team has no current need for machine-readable metadata (no MCP server, no code generation, no linting integration), this skill adds overhead without value — discuss the use case before generating.

---

## Configuration

Before producing output, check for a `.ds-ops-config.yml` file in the project root. If present, load:
- `system.framework` — determines prop extraction approach (React, Vue, Svelte, etc.)
- `system.component_paths` — directs scanning to component source files
- `integrations.*` — enables auto-pull for component data
- `metadata.schema_version` — locks the output schema version for compatibility
- `metadata.output_directory` — overrides default output location
- `metadata.include_business_context` — toggles the business intelligence section (default: true)

## Auto-pull integrations

If integrations are configured in `.ds-ops-config.yml`, pull data automatically:

**Figma MCP** (`integrations.figma.enabled: true`):
- Read component properties, variant structures, and descriptions from `integrations.figma.file_key`
- Cross-reference Figma component properties against code props to detect mismatches
- Extract accessibility annotations if present

**Storybook** (`integrations.storybook.enabled: true`):
- Fetch prop tables and arg types from story metadata
- Extract documented states and control definitions
- Pull interaction test definitions if available

**TypeScript/Source** (always attempted):
- Parse TypeScript interfaces or PropTypes from component source files
- Extract JSDoc/TSDoc annotations for prop descriptions
- Identify generic type parameters for polymorphic components

If an integration fails, log it and proceed with available sources.

---

## Step 1: Select components and assess existing metadata

Ask for or confirm (skip questions already answered by auto-pull):
- Which components need metadata schemas? (Specific components, a category, or the full library)
- Where do component source files live?
- Is there existing structured metadata in any format (JSON, YAML, Custom Elements Manifest)?

For each component, scan for existing metadata sources:
- TypeScript interface or PropTypes declaration
- JSDoc/TSDoc annotations
- Storybook arg types and controls
- Existing metadata files (`.metadata.json`, `.metadata.ts`)
- Figma component description

Produce a source assessment per component:

| Component | TS interface | JSDoc | Storybook | Figma | Existing metadata | Gaps |
|---|---|---|---|---|---|---|
| Button | complete | partial | complete | yes | none | composition, behaviour |
| Card | complete | none | partial | yes | none | all semantic layers |

---

## Step 2: Generate the base schema from source

For each component, extract the prop layer automatically from TypeScript or equivalent:

```json
{
  "$schema": "https://designsystemops.com/schemas/metadata/v1.json",
  "component": "Button",
  "version": "1.0.0",
  "status": "stable",
  "props": [
    {
      "name": "variant",
      "type": "enum",
      "values": ["primary", "secondary", "ghost"],
      "default": "primary",
      "required": false,
      "description": "Visual weight of the button",
      "semantic": {
        "primary": "Use for the single most important action on the page or in a section",
        "secondary": "Use for supporting actions alongside a primary action",
        "ghost": "Use for tertiary actions or actions within dense UI"
      }
    },
    {
      "name": "size",
      "type": "enum",
      "values": ["sm", "md", "lg"],
      "default": "md",
      "required": false,
      "description": "Controls button height and text size"
    },
    {
      "name": "disabled",
      "type": "boolean",
      "default": false,
      "required": false,
      "description": "Prevents interaction and applies disabled styling"
    },
    {
      "name": "children",
      "type": "ReactNode",
      "required": true,
      "description": "Button label content"
    }
  ]
}
```

**Extraction rules:**
- Every prop in the TypeScript interface must appear in the schema
- Types should be normalised to a standard set: `string`, `number`, `boolean`, `enum`, `ReactNode`, `function`, `object`, `array`
- Enum values must be listed explicitly, not as a type reference
- Default values must be the actual defaults, not TypeScript `undefined`
- If a prop has JSDoc, use it as the description. If not, flag the prop for manual description.

---

## Step 3: Add the semantic layer

The semantic layer encodes meaning that TypeScript types cannot express. For each component, add:

### Behavioural rules

```json
{
  "behaviour": {
    "states": ["default", "hover", "active", "focus", "disabled", "loading"],
    "transitions": {
      "default_to_loading": {
        "trigger": "Form submission or async action",
        "visual": "Replace label with spinner, disable interaction",
        "duration": "Until async operation completes or times out"
      }
    },
    "constraints": [
      "A form must have exactly one primary variant Button",
      "Loading state must disable all sibling interactive elements",
      "Icon-only buttons must have an aria-label prop"
    ]
  }
}
```

### Composition rules

```json
{
  "composition": {
    "valid_parents": ["Form", "Card", "Dialog", "Toolbar", "PageHeader"],
    "valid_children": ["Icon", "text"],
    "prohibited_nesting": ["Button may not contain another Button"],
    "slot_contract": {
      "children": {
        "accepts": ["string", "Icon"],
        "max_elements": 2,
        "pattern": "Optional leading Icon + text label"
      }
    },
    "common_combinations": [
      { "pattern": "Primary + Secondary pair", "context": "Dialog footer, form actions" },
      { "pattern": "Icon-only in Toolbar", "context": "Dense action bars" }
    ]
  }
}
```

### Accessibility contract

```json
{
  "accessibility": {
    "role": "button",
    "aria_required": [],
    "aria_conditional": [
      { "prop": "aria-label", "when": "children is Icon only (no visible text)" },
      { "prop": "aria-expanded", "when": "button controls a collapsible region" },
      { "prop": "aria-haspopup", "when": "button opens a menu or dialog" }
    ],
    "keyboard": {
      "Enter": "Activate button",
      "Space": "Activate button"
    },
    "focus": {
      "receives_focus": true,
      "focus_visible": "Required — uses system focus ring token",
      "tab_order": "Follows DOM order unless explicitly managed"
    },
    "screen_reader": {
      "announcement": "Button label + role",
      "state_changes": "Announces disabled state change"
    }
  }
}
```

---

## Step 4: Add the business context layer

The business context layer connects the component to product outcomes. This layer is optional but recommended for components that directly influence conversion, engagement, or retention.

```json
{
  "business_context": {
    "function": "conversion",
    "metrics": {
      "primary": "Click-through rate",
      "secondary": ["Form completion rate"]
    },
    "experimentation": {
      "safe_to_test": ["label text", "variant within brand palette"],
      "never_test": ["removing disabled state logic", "removing aria attributes"],
      "requires_review": ["changing size scale", "adding new variants"]
    },
    "usage_analytics": {
      "track_renders": true,
      "track_interactions": true,
      "track_errors": true,
      "custom_events": [
        { "event": "cta_click", "data": ["variant", "page", "position"] }
      ]
    }
  }
}
```

**When to include business context:**
- Always: conversion components (CTAs, forms, checkout elements)
- Always: high-traffic components (buttons, cards, navigation)
- Recommended: engagement components (interactive elements, content surfaces)
- Optional: utility components (spacers, dividers, layout helpers)

---

## Step 5: Add prohibited combinations

Encode prop combinations that are technically valid but semantically wrong:

```json
{
  "prohibited_combinations": [
    {
      "combination": { "variant": "ghost", "size": "lg" },
      "reason": "Ghost buttons at large size create false visual hierarchy — they appear as primary actions despite being tertiary",
      "severity": "warning"
    },
    {
      "combination": { "disabled": true, "loading": true },
      "reason": "Redundant states — loading already prevents interaction. Use loading alone.",
      "severity": "error"
    }
  ]
}
```

**Severity levels:**
- `error` — this combination is prohibited and tools should refuse to generate it
- `warning` — this combination is discouraged and tools should flag it for review
- `info` — this combination has nuances the developer should be aware of

---

## Step 6: Produce the complete schema

Assemble all layers into the complete metadata schema per component.

### Output structure

```
.ai/metadata/
  schema.json          # JSON Schema definition for validation
  Button.metadata.json
  Card.metadata.json
  Modal.metadata.json
  ...
  manifest.json        # Index of all metadata files
```

### Manifest format

```json
{
  "$schema": "https://designsystemops.com/schemas/metadata/v1.json",
  "generated": "[date]",
  "system": "[design system name]",
  "component_count": 55,
  "coverage": {
    "props": "100%",
    "semantic": "85%",
    "accessibility": "90%",
    "business_context": "40%",
    "prohibited_combinations": "60%"
  },
  "components": [
    { "name": "Button", "file": "Button.metadata.json", "status": "stable" },
    { "name": "Card", "file": "Card.metadata.json", "status": "stable" }
  ]
}
```

---

## Step 7: Validate the schemas

Run validation checks on the generated schemas:

**Structural validation:**
- Every schema is valid JSON
- Every schema conforms to the base schema definition
- Every prop in the TypeScript interface appears in the schema (no missing props)
- Every enum value listed in the schema exists in the TypeScript type (no phantom values)

**Semantic validation:**
- Every prop has a description (not just a type)
- Every enum prop has per-value semantic descriptions (not just a list of values)
- Composition rules reference components that exist in the system (no broken references)
- Accessibility contracts are complete for all interactive components

**Cross-reference validation:**
- Component names in metadata match component names in code
- Prop names and types match TypeScript interfaces
- Composition references are bidirectional (if Card lists Button as valid_child, Button lists Card as valid_parent)
- Status fields are consistent with the component's actual lifecycle status

**Coverage reporting:**
- What percentage of components have complete metadata schemas?
- What percentage of props have semantic descriptions beyond the TypeScript type?
- What percentage of interactive components have accessibility contracts?
- What percentage of conversion-related components have business context?

---

## Recommend to the user

- Co-locate metadata files with component source files or in a dedicated `.ai/metadata/` directory
- Automate prop extraction from TypeScript interfaces to keep the base layer in sync
- Treat semantic, accessibility, and composition layers as manually authored — these encode knowledge that cannot be automatically extracted
- Run validation as part of CI to catch metadata drift from source
- Use the manifest as the entry point for all tooling that consumes component metadata
- Regenerate after adding components, changing props, or updating accessibility contracts

---

## Quality checks

- Every generated schema is valid JSON and parseable by standard JSON parsers
- Prop types are normalised to the standard type set, not raw TypeScript types
- Semantic descriptions add information beyond what the prop name and type convey
- Composition rules form a consistent graph (no contradictions between parent and child declarations)
- Accessibility contracts cover all interactive components, not just the most common ones
- Prohibited combinations cite specific reasons, not generic advice
- The manifest accurately reflects the actual set of generated schema files
- Business context is included for all conversion-critical components, not arbitrarily omitted
