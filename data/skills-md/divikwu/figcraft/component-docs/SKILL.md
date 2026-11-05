---
name: component-docs
description: "Generate documentation for Figma components — properties, variants, usage guidance, and structural health audit. Use when: document/describe/catalog + components/variants/library, or when auditing component quality for design system maintenance."
---

# Component Docs — Automated Component Documentation

Scan Figma components, audit their structural health, and generate structured Markdown documentation including properties, variants, dimensions, and usage guidance. Pairs with `figcraft-generate-library` for the "build → document" design system workflow.

## Skill Boundaries

- Use this skill to **document and audit existing components**.
- If the task is **creating new components or variants**, switch to [figcraft-generate-library](../figcraft-generate-library/SKILL.md) or [figcraft-use](../figcraft-use/SKILL.md).
- If the task is **connecting components to code**, switch to [figcraft-code-connect](../figcraft-code-connect/SKILL.md).
- If the task is **reviewing overall design quality**, switch to [design-review](../design-review/SKILL.md).

## Workflow

### Step 1: Connect and Load Tools

```
ping                                          → verify plugin connection
load_toolset("components-advanced")           → enable audit + property tools
```

**If `ping` fails (plugin not connected):** STOP. Do not fall back to other MCP servers. Tell user: open Figma → Plugins → FigCraft → wait for connection, then retry.

### Step 2: Audit Components

```
audit_components                              → scan all components on current page
```

This returns a structural health summary:
- Total components and component sets
- Missing descriptions
- Unexposed text nodes (text not editable via properties)
- Empty components
- Single-variant sets (may not need to be a set)
- Property counts per component

### Step 3: Get Detailed Component Info

For each component (or the ones the user cares about):

```
components(method: "get", nodeId: "...")              → full component details
components(method: "list_properties", nodeId: "...")   → all properties with types and defaults
```

For component sets, also inspect variant combinations to document all available options.

### Step 4: Generate Documentation

Output structured Markdown for each component:

```markdown
## ComponentName

**Description:** [from component description, or flag as missing]
**Dimensions:** W × H

**Properties:**

| Name | Type | Default | Options |
|------|------|---------|---------|
| variant | VARIANT | Primary | Primary, Secondary, Ghost |
| size | VARIANT | Medium | Small, Medium, Large |
| label | TEXT | "Button" | — |
| hasIcon | BOOLEAN | false | — |
| icon | INSTANCE_SWAP | — | [swap targets] |

**Variants:** [list all variant combinations if component set]

**Usage:** [brief guidance on when/how to use]
```

### Step 5: Report Issues

Flag structural issues found during audit:

- ⚠️ Missing description — component has no description text
- ⚠️ Unexposed text — text nodes not editable via component properties
- ⚠️ Empty component — component has no visible children
- ⚠️ Single-variant set — component set with only one variant (consider simplifying)
- ⚠️ Unbound properties — properties defined but not connected to child layers

### Step 6: Suggest Improvements

Based on audit findings, suggest concrete improvements:
- Add descriptions to undocumented components
- Expose hidden text nodes as TEXT properties
- Remove or merge single-variant sets
- Connect unbound properties to child layers

## Output Formats

The documentation can be output as:
- Inline Markdown in chat (default)
- Saved to a file if the user requests it

## Integration with Design System Workflow

```
figcraft-generate-library → component-docs → figcraft-code-connect
(build components)       (this skill)      (connect to code)
```

After building components with figcraft-generate-library, run component-docs to generate documentation and catch structural issues before publishing.
