---
name: figcraft-generate-design
description: "Create screens in Figma by REUSING an existing design system's components, variables, and styles. REQUIRES a published library or local components. Triggers: 'create a screen', 'build a landing page using the design system', 'push page to Figma', 'create designs from code', 'update the Figma screen'. Extends figma-create-ui with mandatory design system discovery. Do NOT use for no-library creation (use figma-create-ui) or building a new design system (use figcraft-generate-library)."
disable-model-invocation: false
---

# Build / Update Screens from Design System

Use this skill to create or update full-page screens in Figma by **reusing the design system** — components, variables, and styles — rather than drawing primitives with hardcoded values.

**Key insight**: The Figma file likely has a published design system with components, color/spacing variables, and text/effect styles. Find and use those instead of hardcoding hex colors and pixel values.

**This skill extends [figma-create-ui](../figma-create-ui/SKILL.md).** It adds a mandatory design system discovery phase before creation. For creation mechanics (Opinion Engine, `create_frame` syntax, instance properties, best practices), refer to `figma-create-ui`.

## Skill Boundaries

| When to use | Alternative |
|-------------|-------------|
| Build a screen from design system components | — |
| Update an existing screen (swap instances, update content) | — |
| Create a page from code/description using existing assets | — |
| Create new reusable components or variants | → `figcraft-generate-library` |
| Create UI without a design system (no library) | → `figma-create-ui` |
| Generate code from a Figma design | → `figcraft-implement-design` |

## Mandatory Workflow

**Follow these steps in order. Do not skip steps.**

### Step 0: Connect and Get Workflow

```
get_mode  → verifies connection, gets _workflow, lists available components/variables
```

**If `get_mode` fails (plugin not connected):** STOP. Do not fall back to other MCP servers. Tell user: open Figma → Plugins → FigCraft → wait for connection, then retry.

Complete `_workflow.designPreflight` → present design proposal → **WAIT for user confirmation**.

This step also reveals whether the file has a library selected, local components, or both. Use this to plan your discovery strategy in Step 2.

### Step 1: Understand the Screen

Before touching Figma, understand what you're building:

1. Read source code or user description to understand the page structure
2. Identify major sections (Header, Hero, Content, Pricing, FAQ, Footer, etc.)
3. For each section, list the UI components involved (buttons, inputs, cards, nav, etc.)
4. Check source code default props — `<Button size="small">` with no variant prop may default to `variant="primary"` in the component definition

### Step 2: Discover Design System Assets

This is the core differentiator of this skill. You need three things: **components**, **variables**, and **styles**. Never hardcode values when design system tokens exist.

#### 2a: Discover components

**Preferred: check `get_mode` response first.** `libraryComponents` (library mode) or `localComponents` (local mode) lists available component sets with keys and variant properties.

**Then search broadly:**

```
search_design_system(query: "button", includeComponents: true)
search_design_system(query: "card", includeComponents: true)
search_design_system(query: "input", includeComponents: true)
search_design_system(query: "nav", includeComponents: true)
```

Try synonyms — a "NavigationPill" might be found under "pill", "nav", "tab", or "chip".

**Note the component keys.** For component sets (`isSet: true`), use `componentSetKey` + `variantProperties`. For standalone components, use `componentKey`. Check `containingFrame` to verify component category (e.g., "Forms" vs "Avatars").

**Inspect variant details** when needed:

```
components(method: "list_properties", nodeId: "<component-id>")
```

**Build a component map** before creating:

```
Component Map:
- Button → setKey: "abc123", variants: Type=Primary/Secondary, Size=Small/Medium/Large
- Input  → setKey: "def456", variants: Size=md/lg, State=Default/Focused/Error
- Card   → key: "ghi789", standalone component (no variants)
```

#### 2b: Discover variables (colors, spacing, radii)

```
search_design_system(query: "background", includeVariables: true)
search_design_system(query: "spacing", includeVariables: true)
search_design_system(query: "radius", includeVariables: true)
```

**WARNING**: `variables_ep(method: "list")` only returns **local** variables. Library variables are invisible to this API. Always use `search_design_system` to check for library variables too.

**Query strategy** — search by variable name fragments:
- Primitive colors: "gray", "red", "blue", "brand"
- Semantic colors: "background", "foreground", "border", "surface"
- Spacing/sizing: "space", "radius", "gap", "padding"

#### 2c: Discover styles (text, effects)

```
search_design_system(query: "heading", includeStyles: true)
search_design_system(query: "body", includeStyles: true)
search_design_system(query: "shadow", includeStyles: true)
```

### Step 3: Create the Screen

Follow the creation workflow from [figma-create-ui](../figma-create-ui/SKILL.md):

1. **Create wrapper frame** with `role: "screen"`, fixed size, vertical auto-layout
2. **Build each section** using `create_frame` with `children` — one call per section
3. **Use design system assets** discovered in Step 2 — **ID-first is preferred**:
   - **`fillVariableId` / `strokeVariableId` / `fontColorVariableId`** for colors (PREFERRED — zero name resolution, from `get_design_context` `defaults.*.id` or `search_design_system` result IDs)
   - `fillVariableName` / `fontColorVariableName` as fallback when ID not available
   - `textStyleName` for typography
   - `effectStyleName` for shadows
   - `type: "instance"` with `componentSetKey` + `variantProperties` for components

**Why ID-first**: Name lookup is fragile across libraries (unpublished variables, unsubscribed collections, separator variants). Passing the variable ID directly from `get_design_context.defaults.surfacePrimary.id` bypasses all name resolution and never fails silently. If you resolve a variable by name on one call, figcraft returns a `"next time use fillVariableId"` hint with the ID — use it.

**Example: Hero section using discovered assets (ID-first)**

```json
// Assume get_design_context returned:
//   defaults.surfacePrimary.id = "VariableID:123:45"
//   defaults.textPrimary.id    = "VariableID:123:67"

create_frame({
  name: "Hero Section",
  parentId: "<wrapper-id>",
  layoutMode: "VERTICAL",
  layoutSizingHorizontal: "FILL",
  padding: 64,
  itemSpacing: 24,
  primaryAxisAlignItems: "CENTER",
  counterAxisAlignItems: "CENTER",
  fillVariableId: "VariableID:123:45",
  children: [
    {
      type: "text",
      content: "Build something amazing",
      textStyleName: "Heading/H1",
      fontColorVariableId: "VariableID:123:67",
      textAlignHorizontal: "CENTER"
    },
    {
      type: "frame",
      name: "Button Group",
      layoutMode: "HORIZONTAL",
      itemSpacing: 16,
      children: [
        {
          type: "instance",
          componentSetKey: "<from-component-map>",
          variantProperties: { "Size": "Large", "Style": "Primary" },
          properties: { "Label": "Get Started" }
        },
        {
          type: "instance",
          componentSetKey: "<from-component-map>",
          variantProperties: { "Size": "Large", "Style": "Secondary" },
          properties: { "Label": "Learn More" }
        }
      ]
    }
  ]
})
```

### Step 4: Validate

```
verify_design(nodeId: "<wrapper-id>")
```

This runs lint + screenshot in one call. Check for:
- Placeholder text not overridden
- Wrong component variants
- Missing variable bindings (hardcoded colors where tokens exist)
- Layout issues (cropped text, overlapping elements)

### Step 5: Updating an Existing Screen

When updating rather than creating from scratch:

1. **Inspect**: `nodes(method: "get", nodeId: "<screen-id>")`
2. **Update properties**: `nodes(method: "update", patches: [{ nodeId: "...", props: {...} }])`
3. **Add sections**: `create_frame(parentId: "<screen-id>", ...)`
4. **Remove sections**: `nodes(method: "delete", nodeIds: [...])`
5. **Validate**: `export_image` after each modification

## What to Build Manually vs Import

| Build manually | Import from design system |
|----------------|--------------------------|
| Page wrapper frame | **Components** via `type: "instance"` |
| Section container frames | **Variables** via `fillVariableId` (preferred) / `fillVariableName` |
| Layout grids (rows, columns) | **Text styles** via `textStyleName` |
| Decorative elements | **Effect styles** via `effectStyleName` |

**Never hardcode hex colors or pixel spacing when a design system variable exists.**

## Error Recovery

`create_frame` is atomic — if a call fails, nothing is created. Previous sections remain intact.

1. Read the `_recovery` field for actionable suggestions
2. Check state with `get_current_page(maxDepth: 1)`
3. Use `dryRun: true` to preview Opinion Engine inferences before retrying
