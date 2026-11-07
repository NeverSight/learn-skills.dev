---
name: design-review
description: "Review existing Figma designs against design quality rules. Outputs structured violation report with actionable fixes. Use when: review/audit/check/critique/analyze/inspect/diagnose + design/screen/page/component, analyze issues/problems with components, or after UI creation to verify quality."
---

# Design Review — Structured Quality Audit

Review existing Figma designs against design quality rules. Produces a structured violation report with concrete fix suggestions. Pairs with `design-lint` for the automated fix step, forming a "create → review → fix" quality loop.

## Skill Boundaries

- Use this skill to **review and critique** existing designs against quality rules.
- If the task is **automated lint + auto-fix**, switch to [design-lint](../design-lint/SKILL.md).
- If the task is **creating new UI**, switch to [figma-create-ui](../figma-create-ui/SKILL.md).
- If the task is **implementing code from Figma**, switch to [figcraft-implement-design](../figcraft-implement-design/SKILL.md).

## Design Direction

Design rules are delivered by `_workflow.designPreflight` (from `get_mode`). For detailed rules by category, call `get_design_guidelines(category)`.

## Workflow

Follow all steps in sequence without stopping:

### Step 1: Connect and Discover Context

```
ping                          → verify plugin connection
get_mode                      → determine mode + selected library
```

**If `ping` fails (plugin not connected):** STOP the review workflow. Do NOT fall back to other MCP servers (figma-desktop, figma-remote) — they lack `audit_node`, `lint_fix_all`, and `get_design_guidelines`, making a meaningful design review impossible. Instead, inform the user:

1. The FigCraft plugin must be running in Figma for design review
2. Open the Figma file → Plugins → FigCraft → wait for channel ID
3. Then retry the review

### Step 2: Identify Review Targets

```
get_selection                 → get selected nodes
  └─ if nothing selected → get_current_page(maxDepth=2) → use top-level children
```

### Step 3: Read Node Properties

**Start with `audit_node(nodeId)`** — it returns everything in one call:
- Lint violations with severity, suggestions, auto-fix availability
- Variable bindings summary (which properties are token-bound vs hardcoded)
- Text content summary (all text nodes with content)
- Structural notes (layout issues, child count)
- Quality score

**Only drill deeper if audit_node reveals specific issues:**
- For multiple child nodes: `nodes(method:"get_batch", nodeIds:["id1","id2","id3"])` — one call, not N calls
- For large nodes with `_degraded: true`: drill into specific children, not all
- Limit `export_image` to 1-2 key screenshots (the full component + one detail)

**Avoid these patterns:**
- Do NOT call `nodes(method:"get")` individually for each child — use `get_batch`
- Do NOT call `variables_ep` for each variable — audit_node includes bindings summary
- Do NOT call `text_scan` separately — audit_node includes text summary

### Step 4: Apply Design Rules

Load the appropriate design guidelines based on mode:

**If library selected (Design Guardian):**
- `get_design_guidelines()` for full ruleset, or `get_design_guidelines(category)` for focused review
- Review focus:
  - Are colors/fonts bound to library tokens? Flag hardcoded values when tokens exist
  - Is there a clear visual hierarchy and focal point?
  - Is composition intentional (asymmetry where appropriate, no uniform grids)?
  - Is spacing consistent and using library tokens (or 4px-grid spacing scale)?
  - Are text contents realistic and contextually appropriate (not placeholder)?
  - Are icons consistent in style (outline/filled/duotone not mixed)?
  - Are shadow levels consistent and within ≤ 3 tiers?
  - Does node structure complexity match the design tone?
  - Are accessibility standards met (contrast ≥ 4.5:1, touch targets)?

**If no library (Design Creator):**
- `get_design_guidelines()` for full ruleset
- Review focus:
  - Is there a clear design intent (not just AI defaults)?
  - Do color choices serve a purpose (≤ 5 colors, 60% dominant)?
  - Are fonts chosen with intention (not just Inter without reason)?
  - Is spacing rhythmic, consistent, based on a clear base unit?
  - Is there a clear visual focal point?
  - Are text contents realistic (no "Lorem ipsum", no "Button")?
  - Are icons consistent in style?
  - Are shadow levels consistent?
  - Are accessibility standards met?

### Step 5: Output Structured Report

For each violation found, output:

```
- **violation**: [node name] → [property]: [current value]
- **why**: [one sentence explaining the problem]
- **fix**: [concrete fix with MCP tool call example]
```

### Step 6: Summarize

```
✅ X passed  |  ⚠️ Y violations  |  🔧 Z auto-fixable
```

### Step 7: Auto-Fix

Run `lint_fix_all` to auto-fix what's possible, then report remaining violations that need manual attention.

## Review Categories

Use `get_design_guidelines(category)` for focused reviews:

| Category | What it checks |
|----------|---------------|
| `color` | Token binding, palette restraint, contrast |
| `typography` | Text styles, hierarchy, font choice |
| `spacing` | 4px grid, token usage, rhythm |
| `layout` | Auto-layout, sizing, overflow |
| `composition` | Focal point, asymmetry, whitespace |
| `content` | Realistic text, no placeholders |
| `accessibility` | Contrast, touch targets, text size |
| `buttons` | Structure, padding, height |
| `inputs` | Structure, stroke, placeholder |

## Integration with Quality Loop

This skill is designed to chain with other skills:

```
figma-create-ui → design-review → design-lint
                   (this skill)    (auto-fix)
```

After creation, run design-review to catch quality issues. Then run design-lint for automated fixes. This forms the complete quality assurance loop.
