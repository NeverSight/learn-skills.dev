---
name: design-handoff
description: "Design handoff — annotate designs with specs, export spacing/color/typography info for developers. Use when: handoff/annotate/spec/redline + design/screen/component, or when preparing designs for developer implementation."
---

# Design Handoff — Annotation & Spec Export

Annotate Figma designs with implementation specs (spacing, colors, typography, component properties) for developer handoff. Uses annotations to add structured notes directly on design nodes.

## Skill Boundaries

- Use this skill to **annotate and prepare designs for developer handoff**.
- If the task is **implementing code from Figma**, switch to [figcraft-implement-design](../figcraft-implement-design/SKILL.md).
- If the task is **reviewing design quality**, switch to [design-review](../design-review/SKILL.md).
- If the task is **connecting components to code**, switch to [figcraft-code-connect](../figcraft-code-connect/SKILL.md).

## Workflow

### Step 1: Connect and Load Tools

```
ping                                          → verify plugin connection
load_toolset("annotations")                   → enable annotation tools
```

**If `ping` fails (plugin not connected):** STOP. Do not fall back to other MCP servers. Tell user: open Figma → Plugins → FigCraft → wait for connection, then retry.

### Step 2: Inspect the Design

```
get_current_page(maxDepth: 2)                 → overview of page structure
nodes(method: "get", nodeId: "...")            → detailed properties of target nodes
```

For each key element, extract:
- Spacing: padding, itemSpacing, gaps
- Colors: fill hex values, variable bindings
- Typography: fontFamily, fontSize, fontWeight, lineHeight
- Dimensions: width, height, cornerRadius
- Layout: layoutMode, sizing, alignment

### Step 3: Annotate Key Elements

Add structured annotations to important nodes:

```
set_annotation(nodeId: "...", label: "**Spacing**: padding 16px, gap 12px\n**Fill**: var(--color-bg-primary) #FFFFFF\n**Radius**: 8px")
```

For batch annotation:

```
set_multiple_annotations(items: [
  { nodeId: "1:23", label: "**Button**: height 44px, padding 0 16px, radius 8px, fill var(--color-primary)" },
  { nodeId: "4:56", label: "**Input**: height 48px, padding 12px 16px, stroke 1px var(--color-border)" },
  { nodeId: "7:89", label: "**Heading**: Inter 24px/32px Semibold, fill var(--color-text-primary)" }
])
```

Annotations support Markdown formatting for readability.

### Step 4: Export Visual Reference

```
export_image(nodeId: "...", scale: 2)         → high-res screenshot of annotated design
```

### Step 5: Generate Spec Summary

Compile a structured handoff document:

```markdown
## Screen: [Name]

### Colors
- Background: var(--color-bg-primary) → #FFFFFF
- Primary text: var(--color-text-primary) → #111827
- Accent: var(--color-primary) → #3B82F6

### Typography
- Heading: Inter 24px/32px Semibold
- Body: Inter 16px/24px Regular
- Caption: Inter 12px/16px Regular

### Spacing
- Section padding: 24px
- Card gap: 16px
- Button padding: 0 16px

### Components
- Button: height 44px, radius 8px, primary/secondary/ghost variants
- Input: height 48px, radius 8px, stroke 1px
```

### Step 6: Clean Up (Optional)

To remove annotations after handoff:

```
clear_annotations                             → remove all annotations from page
clear_annotations(nodeIds: ["1:23"])          → remove from specific nodes
```

## Available Annotation Tools

| Tool | Purpose |
|------|---------|
| `get_annotations` | Read existing annotations on page or node |
| `set_annotation` | Add/replace annotation on a single node |
| `set_multiple_annotations` | Batch annotate multiple nodes |
| `clear_annotations` | Remove annotations from nodes or page |

## What to Annotate

Focus annotations on information developers need most:

- Spacing values (especially non-obvious padding and gaps)
- Color tokens and their resolved values
- Typography specs (font, size, weight, line-height)
- Interactive states (hover, active, disabled — if not obvious)
- Responsive behavior notes (how elements adapt across breakpoints)
- Component property mappings (which props control what)

## Integration

```
figma-create-ui → design-review → design-handoff → figcraft-implement-design
(create)          (review)         (this skill)      (implement)
```

After review and approval, annotate the design for handoff, then use figcraft-implement-design to generate code.
