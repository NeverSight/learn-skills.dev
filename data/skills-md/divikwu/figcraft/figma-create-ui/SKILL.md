---
name: figma-create-ui
description: "Create UI in Figma using FigCraft declarative tools (create_frame, create_text, create_component). Use when: create/design/build/make + Figma/UI/screen/page/component/button/variant WITHOUT an existing design system. IMPORTANT: Use create_frame for screens, create_component for reusable components. Never use use_figma for UI creation. Do NOT use when assembling screens from existing design system (use figcraft-generate-design) or building a full design system (use figcraft-generate-library)."
---

# FigCraft UI Creation

Use FigCraft declarative tools for UI creation — NOT use_figma. `create_frame` includes an **Opinion Engine** that auto-handles sizing inference, FILL ordering, token binding, and failure cleanup. This eliminates common Figma API pitfalls that `use_figma` scripts must handle manually.

## How This Skill Works

This SKILL.md is a **lightweight entry point**. The detailed, context-aware creation guidance is delivered at runtime by `get_mode._workflow`. Call `get_mode` first — it returns a `_workflow` object containing:

- `designPreflight` — blocking checklist (purpose, platform, language, density, tone, color/typography rules)
- `creationSteps` — ordered steps with tool-specific guidance
- `toolBehavior` — key rules for batch tools and ordered execution
- `references` — links to on-demand guides via MCP tools
- `searchBehavior` — whether `search_design_system` is available in current mode
- `nextAction` — what to do immediately

**Follow `_workflow` as your primary guide.** This SKILL.md provides the boundaries, decision rules, and best practices that `_workflow` does not cover.

## Workflow

1. **`get_mode`** → read `_workflow` (designPreflight + creationSteps + references). **If `get_mode` fails (plugin not connected) → STOP. Do not fall back to other MCP servers.** Tell user: open Figma → Plugins → FigCraft → wait for connection, then retry.
2. **Complete `_workflow.designPreflight`** → present design proposal to user → ⛔ **WAIT for explicit confirmation**
3. **`get_current_page(maxDepth=1)`** → inspect existing content, find placement position
4. **`create_frame` + `children`** → build the design declaratively (one call per screen/element)
5. **`export_image(scale:0.5)`** → visual verification
6. **`lint_fix_all`** → auto-check and fix violations (supports `dryRun:true` to preview)

## Skill Boundaries

- Use this skill to **create new UI** using declarative tools (`create_frame`, `create_text`).
- This skill covers **both** simple layouts and **library component assembly**. In library mode, use `search_design_system` and `type:"instance"` as described in the Library Components section below.
- This skill also covers **creating new reusable components** (buttons, inputs, cards). See the Component Authoring section below.
- If the task is **building a full design system** (variables + components + theming), switch to [figcraft-generate-library](../figcraft-generate-library/SKILL.md).
- If the task is **reviewing existing designs**, switch to [design-review](../design-review/SKILL.md).
- If the task is **implementing code from Figma**, switch to [figcraft-implement-design](../figcraft-implement-design/SKILL.md).

## Library Components — Reuse Design System

When `get_mode` returns `libraryComponents`, **always prefer component instances over hand-built frames**.

### Component Discovery

⛔ **MANDATORY: Always search before building.** The design system likely has the component you need.

1. **Check `libraryComponents` from `get_mode`** — it lists all component sets (name, key, containingFrame, propertyNames) and standalone components. Use this as your starting inventory.

2. **Search for specific components** via `search_design_system`:
   ```
   search_design_system(query: "button")
   search_design_system(query: "input")
   ```

3. **Disambiguate with `containingFrame`** — property names like "Placeholder"/"Size" appear across unrelated component types:
   - `containingFrame: "Forms"` → form components (inputs, selects, checkboxes)
   - `containingFrame: "Avatars"` → profile/user image components — NEVER use for form inputs
   - For form inputs, verify **State/Error/Focused** variants — Avatars never have these.

4. **Inspect variant details** when needed:
   ```
   components(method: "list_properties", nodeId: "<component-id>")
   ```

5. **Build a component map** before creating:
   ```
   Component Map:
   - Button → key: "abc123", variants: Type=Primary/Secondary, Size=Small/Medium/Large
   - Input  → key: "def456", variants: Size=md/lg, State=Default/Focused/Error
   - Card   → key: "ghi789", standalone component
   ```

### Creating with Library Components

Use `create_frame` with `type:"instance"` in children:

| Build manually | Import from design system |
|----------------|--------------------------|
| Page wrapper frame | **Components**: buttons, cards, inputs, toggles, tabs, etc. |
| Section container frames | **Variables**: colors (`fillVariableId` PREFERRED / `fillVariableName`), spacing, radii |
| Layout structure (rows, columns) | **Text styles**: `textStyleName: "body-md"` |
| Dividers, spacers | **Effect styles**: `effectStyleName: "elevation-200"` |

### Instance Properties

- **`variantProperties`** — selects which variant to instantiate from a component **set**:
  ```json
  { "type": "instance", "componentSetKey": "abc123", "variantProperties": { "Type": "Primary", "Size": "Large" } }
  ```

- **`properties`** — sets instance overrides (text, booleans) on a **single component** or after variant selection:
  ```json
  { "type": "instance", "componentKey": "abc123", "properties": { "Label": "Sign In" } }
  ```

- **`componentKey`** — imports a single component from the library
- **`componentSetKey`** — imports a full variant set (use with `variantProperties`)
- **`componentId`** — references a local component by node ID

### Example: Login Screen (ID-first — preferred)

**Before creating**: call `get_design_context` to grab variable IDs from `defaults.*.id` — each subsequent call that uses the ID path skips name resolution entirely.

```json
// Assume get_design_context returned:
//   defaults.surfacePrimary.id = "VariableID:123:45"
//   defaults.textPrimary.id    = "VariableID:123:67"
//   defaults.textSecondary.id  = "VariableID:123:68"
{
  "name": "Screen / Login",
  "width": 402, "height": 874,
  "layoutMode": "VERTICAL",
  "primaryAxisAlignItems": "SPACE_BETWEEN",
  "role": "screen",
  "fillVariableId": "VariableID:123:45",
  "children": [
    {
      "type": "frame", "name": "Top Content",
      "layoutMode": "VERTICAL", "itemSpacing": 32,
      "padding": 24, "paddingTop": 80,
      "children": [
        { "type": "text", "content": "Welcome back", "textStyleName": "display-md", "fontColorVariableId": "VariableID:123:67" },
        { "type": "text", "content": "Sign in to your account", "textStyleName": "body-md", "fontColorVariableId": "VariableID:123:68" },
        {
          "type": "instance", "componentKey": "INPUT_KEY",
          "properties": { "Placeholder": "your@email.com", "Size": "lg" }
        },
        {
          "type": "instance", "componentKey": "INPUT_KEY",
          "properties": { "Placeholder": "Password", "Size": "lg" }
        }
      ]
    },
    {
      "type": "frame", "name": "Bottom Content",
      "layoutMode": "VERTICAL", "itemSpacing": 16,
      "padding": 24, "paddingBottom": 48,
      "children": [
        {
          "type": "instance", "componentKey": "BUTTON_KEY",
          "properties": { "Label": "Sign In", "Type": "Primary", "Size": "Large" },
          "layoutSizingHorizontal": "FILL"
        }
      ]
    }
  ]
}
```

## Component Authoring — Creating New Reusable Components

When the task is creating **new reusable components** (buttons, inputs, cards with variants) — not assembling screens from existing library components — use `create_component` instead of `create_frame`.

### Why `create_component` over `create_frame`

- `create_component` **delegates to `create_frame` internally** — you get all Opinion Engine inferences (sizing, FILL ordering, token auto-binding) for free
- It converts the frame to a component and auto-binds TEXT component properties via `componentPropertyName`
- Avoids the error-prone `create_frame` → `create_component_from_node` two-step conversion

### Workflow

All 5 tools below are core — no `load_toolset` needed.

```
1. create_section(name:"Button") → organize components (auto-positions below existing content)
2. create_component({items:[...]}) → batch-create variants (library mode: prefer fillVariableId/fontColorVariableId from get_design_context; fall back to *Name only when ID unavailable)
   ⛔ EXPLICIT PARAMS: itemSpacing, padding, cornerRadius MUST be set in every item — do NOT rely on Opinion Engine inference across batches
   ⛔ ICON COLOR: colorVariableName on stroke-based icons (lucide etc.) will be silently skipped due to scope mismatch — plan for post-creation binding
   ⛔ BOOLEAN: children with visibility toggles MUST declare componentPropertyReferences:{visible:"PropName"} inline — properties:[] alone is orphaned
   ⛔ FULL-WIDTH: use explicit width (e.g. 360) for full-width button variants — FILL is not supported inside ComponentSet
3. create_component_set → combine + auto-layout + auto-position
4. bind_component_property({nodeId:"<setId>", variantFilter:{Type:"Emphasis"}, bindings:[...]}) → post-creation icon color binding per Type group using nodeProperty:"iconColor"
5. export_image → verify a representative variant's icon color and visibility BEFORE proceeding
```

For component property management (add_component_property, update_component_property), `load_toolset("components-advanced")`. Note: `bind_component_property` is a core tool — no toolset loading needed.

### Variant Matrix Planning (MANDATORY for ≥8 variants)

⛔ **When the target component has 8 or more variants, you MUST output a markdown difference matrix BEFORE calling any `create_component` / `nodes(method:"clone")` / `bind_component_property`.** Skipping this step is the single largest failure mode for multi-variant component creation — it produces clone-then-patch chains where each fix exposes another inconsistency, and the agent burns 10+ rounds chasing variant drift.

⛔ **Before filling the matrix, define each unique structure as a children tree.** A structure label like "std" is NOT sufficient — you must specify the full nesting with layoutMode, sizing, and alignment for every level. Example:

```
Structure "std" (button with optional icons):
Button (HORIZONTAL, CENTER, FILL, padding 16)
└── Content (HORIZONTAL, CENTER, FILL, itemSpacing 4)
    ├── Icon-left (16px, BOOLEAN hidden)
    ├── Label (HUG)
    └── Icon-right (16px, BOOLEAN hidden)

Structure "spinner-only" (loading state):
Button (HORIZONTAL, CENTER, FILL)
└── Spinner (20px SVG)
```

The `structure` column in the matrix references these defined trees by name:

| Variant | base fill | textColor | iconColor | padding | structure | notes |
|---------|-----------|-----------|-----------|---------|-----------|-------|
| Emphasis / Default / sm | `button/emphasis` | `text/inverse` | `text/inverse` | 12/6 | std | — |
| Emphasis / Default / md | `button/emphasis` | `text/inverse` | `text/inverse` | 16/8 | std | — |
| Tertiary / Default / md | `transparent` | `text/primary` | `text/primary` | 16/8 | std | no fill |
| * / Loading / md | inherit | inherit | — | inherit | **spinner-only** | replaces children |
| * / Disabled / md | `surface/disabled` | `text/disabled` | `text/disabled` | inherit | std | — |

Without this matrix you will:
- clone the wrong base
- forget that Tertiary needs `iconColor` rebound (icon Vectors stay on Emphasis color after clone)
- miss that Loading is a structural variant (see below)
- write 31 cells of padding=0 because the base had no padding default

After the matrix is filled in, build in this order: (1) batch-create all std variants per Type×Size×State using `create_component({items:[...]})`, (2) batch-create all Loading variants separately (different children structure), (3) `create_component_set` to combine all, (4) `bind_component_property` with `variantFilter` to bind iconColor per Type slice.

**Loading is a STRUCTURAL variant, not a visual variant.** Loading replaces `children` with a spinner — it's not just a different color/state of the standard structure. Build Loading variants separately:

```
1. Build base "Default" with [icon-left, label, icon-right]
2. Clone Default → Hover / Active / Pressed / Focused (5 visual states share structure)
3. Build SEPARATE base "Loading" with [spinner] children
4. Clone Loading → Loading × Type matrix
5. Combine all into one ComponentSet
```

If you try to clone Default → Loading and then "hide icon-left, hide label, show spinner", you will end up with 8 broken Loading variants whose children don't match the rest of the design system's spinner spec.

### Variant-Aware Binding (use `variantFilter`)

`bind_component_property` accepts `variantFilter: { Type: "Tertiary" }` (or any property combo) to limit a binding to a subset of variants. Use this whenever Type/State/Size determines a different value:

```json
{
  "nodeId": "<componentSetId>",
  "variantFilter": { "Type": "Tertiary" },
  "bindings": [
    { "targetNodeSelector": "Icon-left", "nodeProperty": "iconColor", "value": "icon/primary" },
    { "targetNodeSelector": "Icon-right", "nodeProperty": "iconColor", "value": "icon/primary" }
  ]
}
```

`nodeProperty: "iconColor"` is a build-time bulk-apply — it walks the matched node's Vector descendants and rebinds their fills/strokes. Use it INSTEAD of cloning + manually editing each variant's icon. Value auto-detection: `#hex` → hex, `VariableID:...` → direct ID binding, bare name → variable name lookup.

### Key Rules

- **Token binding (library mode, ID-first)**: Prefer `fillVariableId` / `fontColorVariableId` from `get_design_context.defaults.*.id`. Fall back to `*Name` only when the ID is unavailable. figcraft returns a "next time use `fontColorVariableId`" typed hint after a successful name lookup — use it on subsequent calls. Text binding failures write a magenta sentinel fill so black-on-black bugs are visible in screenshots.
- **Icon color binding (post-creation MANDATORY)**: `colorVariableName` on icon children is silently skipped when the variable's scopes exclude `STROKE_COLOR` (most `text/*` variables). After `create_component_set`, you MUST call `bind_component_property` with `nodeProperty:"iconColor"` per Type group using `variantFilter`. This is the ONLY reliable path for stroke-based icons (lucide, tabler, etc.). Skipping this step leaves all icons hardcoded black — visually broken on dark backgrounds.
- **BOOLEAN visibility binding**: declare `properties:[{type:"BOOLEAN", propertyName:"Icon", defaultValue:false}]` AND `componentPropertyReferences:{visible:"Icon"}` on the child whose visibility you want to control. Both sides are required — property alone creates an orphaned toggle that does nothing; reference alone is a no-op. The child must have a `name` field. figcraft auto-wires + syncs node visibility with `defaultValue`. See `create_component` schema for the full example.
- **Explicit params in batch mode**: When using `create_component({items:[...]})`, explicitly set `itemSpacing`, `padding*`, and `cornerRadius` in every item. Opinion Engine inference can produce different values across batches (e.g. `itemSpacing: 8` vs `4`), causing inconsistency within the same ComponentSet.
- **Full-width buttons in ComponentSet**: Variants inside a ComponentSet cannot use `layoutSizingHorizontal:"FILL"` (Figma platform limitation — ComponentSet uses absolute positioning). Use explicit `width` (e.g. `360`) to represent full-width intent. Consumers apply FILL when placing instances.
- **Variant naming**: Each component must follow `Property=Value, Property=Value` format (e.g., `"Size=Small, Style=Primary, State=Default"`).
- **Variant cap**: `create_component_set` enforces a soft 30-variant cap. Pass `variantLimit:0` to disable for legitimate large matrices. Consider extracting high-cardinality axes (icons, colors) into `INSTANCE_SWAP` properties instead.
- **Batch cap**: `create_component({items:[...]})` is capped at **10 items per call** (lowered from 20 after timeout incidents). For 32-variant components, split into ⌈N/10⌉ sequential calls.
- **`strokes` / `fills` are NOT figcraft params**. Use `strokeColor` / `fill` (singular, hex string) or the `*VariableId` / `*VariableName` aliases. Passing the raw plural Plugin API names will throw a self-correcting error pointing at the right alias.
- For full component library builds (multiple components + variables + theming), switch to [figcraft-generate-library](../figcraft-generate-library/SKILL.md).

### Advanced Component Patterns

For components with 3+ variants or complex variant matrices, reference these patterns:

- **Building Blocks** — extract sub-elements with independent state machines into `.Building Blocks/` component sets to prevent variant explosion (see [component-creation reference](../figcraft-generate-library/references/component-creation.md) Section 1)
- **Dependency ordering** — atoms (Icon, Badge) → molecules (Button, Input) → organisms (Card, Dialog)
- **Full variable binding** — beyond fill/fontColor: bind strokes, padding, spacing, cornerRadius via `variables_ep(method:"batch_bind")`
- **Text + Effect styles** — `textStyleName` for typography, `effectStyleName` for shadows
- **Per-component verification** — `audit_node(nodeId)` + `export_image` after each component set
- **Private components** — `__` prefix for internal helpers, `.` prefix for hidden from assets panel

For full design system builds (10+ components + variables + theming), switch to [figcraft-generate-library](../figcraft-generate-library/SKILL.md).

## Opinion Engine

`create_frame` includes an Opinion Engine that automatically infers best practices. Key behaviors:

1. **layoutMode inference** — auto-set to VERTICAL when padding/spacing/alignment/children are present
2. **Sizing defaults** — cross-axis FILL, primary-axis HUG inside auto-layout parents
3. **FILL ordering** — internally sets FILL after appendChild (avoids Figma API error)
4. **Token auto-binding** — `fillVariableId`/`strokeVariableId` (PREFERRED, from `get_design_context`) or `fillVariableName`/`strokeVariableName` (fallback) matched to library variables
5. **Conflict detection** — rejects contradictory params (e.g., FILL + explicit width)
6. **Per-child error cleanup** — failed child creation auto-removes orphan nodes

Use `dryRun:true` to preview all inferences before creating nodes. For full details: `get_creation_guide(topic:"opinion-engine")`.

## Best Practices

- **Root screen frames** MUST include `layoutSizingHorizontal:"FIXED"` + `layoutSizingVertical:"FIXED"`. Without this, Opinion Engine infers HUG and the frame collapses.
- **Semantic role**: Screen containers MUST include `role: "screen"`. Buttons SHOULD include `role: "button"`. This enables deterministic lint identification instead of name-regex guessing, especially important for non-English names.
- **SPACE_BETWEEN children**: Direct child of a SPACE_BETWEEN parent MUST declare `layoutSizingVertical: "FILL"` explicitly — Opinion Engine defaults to HUG which defeats SPACE_BETWEEN.
- **Placeholders** for logos/avatars/charts: use `type:"frame"` (not `"rectangle"`), because rectangles cannot have children.
- **Icons**: use `icon_search` + `icon_create` with `index` param for ordering. NEVER text characters as placeholders. See [iconography](../iconography/SKILL.md).
- **Content**: realistic, contextually appropriate text. NEVER "Lorem ipsum", "Button", "Title".
- **dryRun:true** for complex or ambiguous parameters — preview before committing.
- **After first failure**, review ALL remaining planned payloads for the same pattern before retrying.
- **Icon ordering (CRITICAL)**: `icon_create` appends to END by default — use `index: 0` to place BEFORE text. Array order = visual order in auto-layout. Full patterns: `get_creation_guide(topic:"iconography")`.
- **Always search before building** in library mode. Manual construction should be the exception, not the rule.
- **Prefer component instances over manual builds.** Instances stay linked to the source component and update automatically.
- **Validate visually after each screen.** Use `export_image` to catch issues early.
- **Match existing conventions.** If the file already has screens, match their naming and layout patterns.

## Updating an Existing Screen

When updating rather than creating:

1. `nodes(method: "get", nodeId: "<screen-id>")` — inspect current structure
2. `nodes(method: "update", patches: [...])` — update properties, swap variants
3. `nodes(method: "delete", nodeId: "<old-section>")` — remove deprecated sections
4. Create new sections with `create_frame(parentId: "<screen-id>", ...)`
5. Validate with `export_image` after each modification

## On-Demand Guides

Call these MCP tools when you need deeper guidance on a specific topic:

| Guide | When to load |
|-------|-------------|
| `get_creation_guide(topic:"layout")` | Structural layout rules (39 rules from Quality Engine) |
| `get_creation_guide(topic:"multi-screen")` | Multi-screen flow details (skill `multi-screen-flow` is auto-loaded at STEP 4) |
| `get_creation_guide(topic:"batching")` | Context budget and batching strategy |
| `get_creation_guide(topic:"opinion-engine")` | Full Opinion Engine auto-inference documentation |
| `get_creation_guide(topic:"ui-patterns", uiType:"xxx")` | UI type templates (login, dashboard, settings, etc.) |
| `get_creation_guide(topic:"responsive")` | Responsive web breakpoints + auto-layout |
| `get_creation_guide(topic:"content-states")` | Empty/loading/error state patterns |
| `get_design_guidelines(category)` | Design direction rules (color, typography, spacing, etc.) |

## Design Direction

Design rules are delivered by `_workflow.designPreflight` (from `get_mode`). For detailed rules by category, call `get_design_guidelines(category)`.
