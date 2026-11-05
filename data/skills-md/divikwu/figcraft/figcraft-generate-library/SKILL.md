---
name: figcraft-generate-library
description: "Build or update the design system itself in Figma — variables/tokens, component libraries, theming (light/dark modes), foundations documentation. Use when creating the system, not just using it. Triggers: 'build component library', 'create design tokens', 'set up theming', 'reconcile code and Figma'. Uses FigCraft declarative tools — no use_figma required. Do NOT use for assembling screens from existing system (use figcraft-generate-design)."
disable-model-invocation: false
---

# Design System Builder

Build professional-grade design systems in Figma that match code. This skill orchestrates multi-phase workflows using FigCraft declarative tools, enforcing quality patterns from real-world design systems (Material 3, Polaris, Figma UI3, Simple DS).

## Design Direction

Design rules are delivered by `_workflow.designPreflight` (from `get_mode`). For detailed rules by category, call `get_design_guidelines(category)`.

## Skill Boundaries

- Use this skill to **build a full design system** (variables, components, styles) in Figma.
- If the task is **building screens** (from an existing design system or from scratch), switch to [figma-create-ui](../figma-create-ui/SKILL.md).
- If the task is **auditing an existing design system**, switch to [design-system-audit](../design-system-audit/SKILL.md).
- If the task is **migrating between design system versions**, switch to [migration-assistant](../migration-assistant/SKILL.md).

---

## 1. The One Rule That Matters Most

**This is NEVER a one-shot task.** Building a design system requires multiple tool calls across multiple phases, with mandatory user checkpoints between them. Break every operation to the smallest useful unit, validate, get feedback, proceed.

---

## 2. Mandatory Workflow

Every design system build follows this phase order. Skipping or reordering phases causes structural failures that are expensive to undo.

```
Phase 0: DISCOVERY (always first — no writes yet)
  0a. Verify plugin connection → call get_mode (if it fails → STOP, do not fall back)
  0b. Analyze codebase → extract tokens, components, naming conventions
  0c. Inspect Figma file → get_document_info, get_current_page, variables_ep(method:"list"), components(method:"list")
  0d. Search subscribed libraries → search_design_system for reusable assets
  0e. Lock v1 scope → agree on exact token set + component list before any creation
  0f. Map code → Figma → resolve conflicts (code and Figma disagree = ask user)
  ✋ USER CHECKPOINT: present full plan, await explicit approval

Phase 1: FOUNDATIONS (tokens first — always before components)
  1a. variables_ep(method:"create_collection") → create collections with modes
  1b. variables_ep(method:"batch_create") → create primitive variables (raw values)
  1c. create_variable_alias → create semantic variables (aliased to primitives, mode-aware)
  1d. set scopes via batch_create(scopes:[...]) or variables_ep(method:"update", scopes:[...])
  1e. variables_ep(method:"set_code_syntax") → set code syntax on ALL variables
  1f. styles_ep(method:"create_text") + styles_ep(method:"create_effect") → create text and effect styles
  → Exit criteria: every token from the agreed plan exists, all scopes set, all code syntax set
  ✋ USER CHECKPOINT: show variable summary, await approval

Phase 2: FILE STRUCTURE (before components)
  2a. load_toolset("pages") → create_page for each: Cover → Getting Started → Foundations → --- → Components → --- → Utilities
  2b. create_frame + create_text → build foundations documentation pages (color swatches, type specimens, spacing bars)
  → Exit criteria: all planned pages exist, foundations docs are navigable
  ✋ USER CHECKPOINT: show page list + export_image, await approval

Phase 3: COMPONENTS (one at a time — never batch)
  ⚡ Steps 3b-3e use core tools (no load_toolset needed).
  ⚡ Steps 3f-3g need load_toolset("components-advanced") for property management.
  For EACH component (in dependency order: atoms before molecules):
    3a. create_page → dedicated page, then set_current_page to switch to it
    3b. create_component → base component with auto-layout, children, variable bindings (CORE)
    3c. nodes(method:"clone") → clone base for each variant, nodes(method:"update") to rename (e.g. "Size=Small, Style=Primary")
    3d. create_component_set → combineAsVariants + auto-layout + auto-position (CORE, all automatic)
    3f. load_toolset("components-advanced") → add_component_property for TEXT, BOOLEAN, INSTANCE_SWAP, SLOT
    3g. bind_component_property → wire properties to child nodes across all variants
    3h. variables_ep(method:"batch_bind") → bind variables to all variant properties in one call
    3i. create_frame + create_text → page documentation
    3j. export_image + audit_node → validate structure and visual
    → Exit criteria: variant count correct, all bindings verified, screenshot looks right
    ✋ USER CHECKPOINT per component: show screenshot, await approval before next

Phase 4: INTEGRATION + QA (final pass)
  4a. lint_fix_all → auto-fix violations
  4b. audit_components → structural health check
  4c. Accessibility audit (contrast ≥ 4.5:1, min touch targets 44px)
  4d. Unresolved bindings audit — no hardcoded fills/strokes where variables exist
  4e. export_image per page → final review screenshots
  4f. Optional: finalize Code Connect mappings
  ✋ USER CHECKPOINT: complete sign-off
```

---

## 3. Tool Reference — Phase by Phase

### Phase 0: Discovery

| Task | Tool |
|------|------|
| File structure | `get_document_info`, `get_current_page(maxDepth:1)` |
| List variables | `load_toolset("variables")` → `variables_ep(method:"list")` |
| List collections | `variables_ep(method:"list_collections")` |
| List components | `components(method:"list")` |
| List styles | `load_toolset("styles")` → `styles_ep(method:"list")` |
| Search libraries | `search_design_system(query:"button")` |

### Phase 1: Foundations

| Task | Tool |
|------|------|
| Create collection + modes | `variables_ep(method:"create_collection", collectionName, modeNames:["Light","Dark"])` |
| Batch create primitives | `variables_ep(method:"batch_create", collectionName, variables:[{name, type, value, scopes}])` |
| Create semantic aliases | `create_variable_alias(variableId, targetVariableId, modeId)` |
| Set multi-mode values | `variables_ep(method:"set_values_multi_mode", variableId, valuesByMode:{Light:"#FFF", Dark:"#1A1A1A"})` |
| Set code syntax | `variables_ep(method:"set_code_syntax", variableId, syntax:{WEB:"var(--color-primary)"})` |
| Create text style | `styles_ep(method:"create_text", name, fontFamily, fontSize, fontWeight, lineHeight)` |
| Create effect style | `styles_ep(method:"create_effect", name, effects:[{type:"DROP_SHADOW", color, blur, offsetY}])` |

### Phase 3: Components

| Task | Tool |
|------|------|
| Create base component | `create_component(name, layoutMode, padding, children:[...])` |
| Clone for variants | `nodes(method:"clone", items:[{id, name:"Size=Small, Style=Primary"}])` |
| Adjust variant bindings | `variables_ep(method:"batch_bind", bindings:[{nodeId, field, variableId}])` — after combineAsVariants |
| Combine as variants | `create_component_set(componentIds:[...], name:"Button")` |
| **Add a single variant to existing set** *(see note below)* | `nodes(method:"clone", items:[{id:"<existingVariantId>", name:"Size=XL, Style=Primary", parentId:"<componentSetId>"}])` then `layout_component_set(nodeId:"<componentSetId>")` |
| Grid layout | `layout_component_set(nodeId, columnAxis:"State", gap:20)` |
| Add properties | `add_component_property(nodeId, propertyName:"Label", type:"TEXT", defaultValue:"Button")` |
| Wire to children | `bind_component_property(nodeId, propertyName:"Label", targetNodeSelector:"label", nodeProperty:"characters")` — accepts `bindings:[]` array to wire multiple properties in one call |
| Update description | `update_component(nodeId, description:"...")` |
| Pre-publish health check | `preflight_library_publish()` — scans components, variables, styles; returns blockers/warnings with fix suggestions |

> **Incremental variant addition**: There is no dedicated `add_variant_to_set` handler — use `nodes(method:"clone")` with `parentId` set to the ComponentSet's id. The clone is automatically reparented into the set, Figma re-derives the variant axes from the new variant's name (which MUST follow `Property=Value, Property=Value` format), then `layout_component_set` re-grids everything. Works because `ComponentSetNode` extends `BaseFrameMixin → ChildrenMixin` so it accepts `appendChild` directly.

---

## 4. Critical Rules

**Design system rules**:
1. **Variables BEFORE components** — components bind to variables. No token = no component.
2. **Inspect before creating** — discover existing conventions via read tools. Match them.
3. **One page per component** *(default)* — exception: tightly related families may share a page.
4. **Bind visual properties to variables** *(default)* — fills, strokes, padding, radius, gap.
5. **Scopes on every variable** — NEVER leave as `ALL_SCOPES`. Background: `FRAME_FILL, SHAPE_FILL`. Text: `TEXT_FILL`. Border: `STROKE_COLOR`. Spacing: `GAP`. Radii: `CORNER_RADIUS`. Primitives: `[]` (hidden).
6. **Code syntax on every variable** — WEB syntax MUST use `var()` wrapper: `var(--color-bg-primary)`. ANDROID/iOS do NOT use a wrapper.
7. **Alias semantics to primitives** — use `create_variable_alias`. Never duplicate raw values in semantic layer.
8. **Position variants after combineAsVariants** — use `layout_component_set` (auto-handles grid layout + resize).
9. **INSTANCE_SWAP for icons** — never create a variant per icon. Use SLOT for flexible content areas. Cap variant matrices at 30 combinations.
10. **Validate before proceeding** — `export_image` after every create, `audit_node` for structural checks. Verify with `nodes(method:"get", nodeId:"...")` that node exists, has expected type/name/child count.
11. **Never hallucinate Node IDs** — always use IDs from previous tool responses.
12. **Explicit phase approval** — at each checkpoint, name the next phase explicitly.
13. **Cleanup on failure** — if a build run fails mid-way, identify orphaned nodes via `get_current_page(maxDepth:2)`, then remove with `nodes(method:"delete")`. For orphaned variables: `variables_ep(method:"list")` → filter by naming convention → `variables_ep(method:"delete")`.


---

## 5. State Management (Long Workflows)

For design systems with 10+ components, maintain a state ledger tracking created entity IDs:

```json
{
  "phase": "phase3",
  "step": "component-button",
  "entities": {
    "collections": { "primitives": "VariableCollectionId:1:2", "color": "VariableCollectionId:1:5" },
    "variables": { "color/bg/primary": "VariableID:1:30", "spacing/sm": "VariableID:1:40" },
    "pages": { "Cover": "0:1", "Button": "5:1" },
    "components": { "Button": "80:1" }
  },
  "completedSteps": ["phase0", "phase1", "phase2", "component-avatar"]
}
```

**Write the ledger to disk** (`/tmp/dsb-state.json`) at each phase boundary. Re-read at the start of every turn. In long workflows, conversation context will be truncated — the file is the source of truth.

**Session recovery** (when resuming after interruption): Rebuild state by inventorying existing entities:
1. `get_document_info()` → list all pages
2. `variables_ep(method:"list_collections")` + `variables_ep(method:"list")` → existing variables
3. `styles_ep(method:"list")` → existing styles
4. `components(method:"list")` per page → existing components
Match against the state ledger to determine which steps are already complete.

**Idempotency**: before creating any entity, check if it already exists by name. `batch_create_variables` and `styles_ep(method:"create_text")` are already idempotent (skip duplicates). For components, check `components(method:"list")` first.

---

## 6. Variable Discovery — Critical Pitfall

> **`variables_ep(method:"list")` only returns LOCAL variables defined in the current file.** If this returns empty, it does NOT mean no variables exist. Remote/published library variables are invisible to this API.

Always also run `search_design_system(query:"color")`, `search_design_system(query:"spacing")` etc. to check for library variables before deciding to create your own.

**Three-way priority**: local existing → subscribed library import → create new.

---

## 7. search_design_system — Reuse Decision Matrix

Search FIRST in Phase 0, then again immediately before each component creation.

**Reuse if** all of these are true:
- Component property API matches your needs (same variant axes, compatible types)
- Token binding model is compatible (uses same or aliasable variables)
- Naming conventions match the target file

**Rebuild if** any of these:
- API incompatibility (different property names, wrong variant model)
- Token model incompatible (hardcoded values, different variable schema)
- Ownership issue (can't modify the library)

**Wrap if** visual match but API incompatible:
- Import the library component as a nested instance inside a new wrapper component
- Expose a clean API on the wrapper

---

## 8. User Checkpoints

Mandatory. Design decisions require human judgment.

| After | Required artifacts | Ask |
|-------|-------------------|-----|
| Discovery + scope lock | Token list, component list, gap analysis | "Here's my plan. Approve before I create anything?" |
| Foundations | Variable summary (N collections, M vars, K modes), style list | "All tokens created. Review before file structure?" |
| File structure | Page list + screenshot | "Pages set up. Review before components?" |
| Each component | export_image of component page | "Here's [Component] with N variants. Correct?" |
| Each conflict (code ≠ Figma) | Show both versions | "Code says X, Figma has Y. Which wins?" |
| Final QA | Per-page screenshots + audit report | "Complete. Sign off?" |

**If user rejects**: fix before moving on. Never build on rejected work.

---

## 9. Naming Conventions

Match existing file conventions. If starting fresh:

**Variables** (slash-separated):
```
color/bg/primary     color/text/secondary    color/border/default
spacing/xs  spacing/sm  spacing/md  spacing/lg  spacing/xl  spacing/2xl
radius/none  radius/sm  radius/md  radius/lg  radius/full
```

**Primitives**: `blue/50` → `blue/900`, `gray/50` → `gray/900`

**Component names**: `Button`, `Input`, `Card`, `Avatar`, `Badge`, `Checkbox`, `Toggle`

**Variant names**: `Property=Value, Property=Value` — e.g., `Size=Medium, Style=Primary, State=Default`

> Full naming reference: [naming-conventions.md](references/naming-conventions.md)

---

## 10. Token Architecture

| Complexity | Pattern |
|-----------|---------|
| < 50 tokens | Single collection, 2 modes (Light/Dark) |
| 50–200 tokens | **Standard**: Primitives (1 mode) + Color semantic (Light/Dark) + Spacing (1 mode) |
| 200+ tokens | **Advanced**: Multiple semantic collections, 4–8 modes. Use `variables_ep(method:"extend_collection")` for multi-brand theming (Enterprise). |

Standard pattern:
```
Collection: "Primitives"    modes: ["Value"]
  blue/500 = #3B82F6, gray/900 = #111827, ...

Collection: "Color"         modes: ["Light", "Dark"]
  color/bg/primary → alias Primitives/white (Light), alias Primitives/gray-900 (Dark)

Collection: "Spacing"       modes: ["Value"]
  spacing/xs = 4, spacing/sm = 8, spacing/md = 16, ...
```

---

## 11. Per-Phase Anti-Patterns

**Phase 0:**
- ❌ Starting to create anything before scope is locked with user
- ❌ Ignoring existing file conventions
- ❌ Skipping `search_design_system` before planning
- ❌ Concluding "no variables exist" based solely on `variables_ep(method:"list")` returning empty

**Phase 1:**
- ❌ Using `ALL_SCOPES` on any variable
- ❌ Duplicating raw values in semantic layer instead of aliasing
- ❌ Not setting code syntax (breaks Dev Mode)

**Phase 3:**
- ❌ Creating components before foundations exist
- ❌ Hardcoding any fill/stroke/spacing/radius value in a component
- ❌ Creating a variant per icon (use INSTANCE_SWAP or SLOT)
- ❌ Skipping `layout_component_set` after `create_component_set` (variants stack at 0,0)
- ❌ Building variant matrix > 30 without splitting

**General:**
- ❌ Building on unvalidated work from the previous step
- ❌ Skipping user checkpoints
- ❌ Guessing node IDs from memory

---

## 12. Reference Docs

Load on demand — each reference is authoritative for its phase. Note: reference docs contain `use_figma` Plugin API code examples for context. When building, use the declarative tools listed in Section 3 instead.

| Doc | Phase | Load when |
|-----|-------|-----------|
| [discovery-phase.md](references/discovery-phase.md) | 0 | Starting any build |
| [token-creation.md](references/token-creation.md) | 1 | Creating variables, collections, modes, styles |
| [documentation-creation.md](references/documentation-creation.md) | 2 | Creating cover page, foundations docs |
| [component-creation.md](references/component-creation.md) | 3 | Creating any component or variant |
| [code-connect-setup.md](references/code-connect-setup.md) | 3–4 | Setting up Code Connect |
| [naming-conventions.md](references/naming-conventions.md) | Any | Naming anything |
| [error-recovery.md](references/error-recovery.md) | Any | On error |
