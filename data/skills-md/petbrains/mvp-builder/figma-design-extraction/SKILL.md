---
name: figma-design-extraction
description: Extract design tokens, screen structure, and visual references from Figma files. Use whenever a figma.com URL appears in the conversation, when someone mentions Figma tokens, variables, design system extraction, or screen captures. Also use when calling get_variable_defs, get_design_context, get_metadata, or get_screenshot — this skill defines how to use them effectively. Trigger for phrases like "get from Figma", "extract design", "Figma variables", "design tokens from Figma", "capture screens", or any figma.com/design link. Even if the user just pastes a Figma link without instructions, use this skill to parse it and decide what to extract.
allowed-tools: Read, Write, Bash(*), mcp__figma__whoami, mcp__figma__get_metadata, mcp__figma__get_screenshot, mcp__figma__get_variable_defs, mcp__figma__get_design_context
---

# Figma Design Extraction

Extract design tokens, screen structure, and visual references from Figma files.

Process: **CHECK → PARSE → DISCOVER → EXTRACT → ORGANIZE**

The goal is to pull structured, source-tracked design data from Figma for use in design-setup pipelines, conflict resolution, and downstream code generation. Every extracted value carries its source tag — this matters because downstream consumers (like design-setup Phase 3) need to know whether a token came from an explicit Figma Variable definition or was inferred from applied styles, since that affects conflict resolution priority.

## Step 0: CHECK — Verify MCP Connection

Before any extraction, verify the Figma MCP server responds:

```
whoami()
```

If this fails or isn't available, warn the user and skip all Figma steps. Don't attempt tool calls that will error out — it wastes context and confuses the workflow.

## Step 1: PARSE — Get IDs from URL

### URL Formats
```
https://figma.com/design/:fileKey/:fileName?node-id=X-Y
https://figma.com/file/:fileKey/:fileName?node-id=X-Y
https://figma.com/proto/:fileKey/:fileName?node-id=X-Y
```

### What to Extract
- **fileKey**: segment after `/design/`, `/file/`, or `/proto/`
- **nodeId**: `node-id` query param, convert dash → colon (`1-2` → `1:2`)

```
URL: https://figma.com/design/kL9xQn2VwM8pYrTb4ZcHjF/MyApp?node-id=42-15
  → fileKey: kL9xQn2VwM8pYrTb4ZcHjF
  → nodeId: 42:15
```

### Decision Rules

| Condition | Action |
|---|---|
| URL has `/design/`, `/file/`, `/proto/` | Parse and proceed |
| URL has `/board/` (FigJam) | Warn: "FigJam not supported" → skip |
| URL has `/slides/` | Warn: "Slides not supported" → skip |
| No URL, MCP connected | Can still extract variables — see "No URL Available" below |
| No URL, MCP not connected | Warn: "No Figma source available" → skip |
| nodeId missing in URL | Fetch root pages first, then navigate |

### No URL Available

If there's no Figma URL but the `figma` MCP is connected (Step 0 passed), `get_variable_defs` still works — it returns all variables for the file without a specific node. You can extract tokens without screenshots or screen discovery. For screen-level extraction (screenshots, design context), a URL with a nodeId or page reference is needed.

## Step 2: DISCOVER — Map File Structure

### 2.1 Fetch Page Overview

Call `get_metadata` to get XML structure with node IDs, layer types, names, positions, sizes.

**Depth strategy matters** because large files overwhelm in a single call:
1. Start at the provided nodeId (or page level like `0:1`) to get top-level frames
2. If response is too large or truncated → narrow to individual pages
3. For each page, identify top-level frames — these are your screens

### 2.2 Build Screen Inventory

Extract from metadata:
```
SCREENS[] = [{
  nodeId: "X:Y",
  name: "Login Screen",
  page: "Authentication",
  width: N,
  height: N,
  slug: "login-screen"    ← kebab-case for pipeline references
}]
```

**Slug normalization:**
- "Login Screen" → `login-screen`
- "Dashboard / Overview" → `dashboard-overview`
- "01 - Onboarding Flow" → `onboarding-flow`
- Strip leading numbers and separators, convert spaces/slashes to hyphens

### 2.3 Large File Strategy

If the file has many pages:
1. Fetch page-level metadata first
2. For each page, fetch frame-level children separately
3. Focus on top-level frames — skip deeply nested component internals
4. Log skipped content: "Skipped N nested components in page X"

## Step 3: EXTRACT — Pull Design Data

Three independent extraction types. Run what the consumer needs.

### 3.1 Variables (Primary Token Source)

`get_variable_defs` returns variable definitions — a flat map of paths to values.

**Categorize by inspecting the path structure.** Figma variable paths vary wildly between teams — there's no universal naming convention. Common patterns include:

```
color/primary/500          → color token
primitives/color/blue/500  → color token
semantic/text/primary       → color token (semantic layer)
font/body/size             → typography token
text/heading/weight        → typography token
spacing/lg                 → spacing token
space/4                    → spacing token
radius/md                  → border-radius token
shadow/card                → shadows token
breakpoint/md              → breakpoints token
duration/fast              → animation token
easing/default             → animation token
```

**Categorization strategy:** Look at the value type first (hex color → color, numeric with px/rem → typography/spacing, shadow definition → shadows), then use the path as a naming hint. Don't force paths into a rigid taxonomy — let the actual data guide categorization.

Mark all values with `source: "figma-variables"` — these are intentional design decisions by the designer, not just what happened to be applied to a frame. This distinction drives conflict resolution downstream: a variable definition is stronger evidence than an applied style.

**When variables come back empty** — this is common. Many Figma files use local styles instead of Variables. Don't treat this as an error. Fall back to design context (3.2).

### 3.2 Design Context (Fallback Token Source)

`get_design_context` returns rich structured data: layout, typography, colors, component structure, spacing, padding.

**Use this when:**
- Variables (3.1) returned empty or sparse
- You need applied-style values (what's actually on frames, not just defined)
- Understanding component patterns (Auto Layout, constraints, variants)

**Extract token-like values from:**
- Color fills → color tokens
- Text styles (font family, size, weight, line-height) → typography tokens
- Auto Layout spacing/padding → spacing tokens
- Corner radius → border-radius tokens
- Effects (shadows, blurs) → shadows tokens
- Transition/animation properties → animation tokens

**Extract component information from:**
- Named component instances → component name, variant properties
- Auto Layout containers with semantic names → layout components
- Repeated patterns across screens → shared components

Mark all values with `source: "figma-context"` — these are inferred from usage, not declared as variables. They're valid design data but carry less authority in conflict resolution because a designer might have applied a one-off value to a frame without intending it as a system token.

**Truncation handling** (critical for complex designs):
1. If response is too large → call `get_metadata` first to get the node map
2. Identify specific child nodes from metadata
3. Fetch children individually with `get_design_context`
4. Merge results

### 3.3 Screenshots (Visual References)

`get_screenshot` renders the node as an image. Return screenshot data for each screen — the caller specifies save paths.

For each screen in `SCREENS[]`, capture a screenshot. These serve as visual truth during implementation and validation.

**Practical notes:**
- Capture all top-level screens identified in DISCOVER
- If a screen screenshot fails → log warning, continue with remaining screens
- Very large frames may timeout → try child frames as fallback
- Screenshots are supplementary — extraction continues even if screenshots fail

## Step 4: ORGANIZE — Structure Results

### Where to Save

The caller decides the output path — this skill extracts and structures data, it doesn't own the file layout. If no path is specified, return the data structures in-memory for the caller to place where it needs them.

### 4.1 Unified Token Map

Merge tokens from all sources into a single map. Source tracking enables downstream conflict resolution when file-based tokens disagree with Figma tokens.

```
FIGMA_TOKENS = {
  colors: {
    "primary-500": { value: "#3B82F6", source: "figma-variables" },
    "surface":     { value: "#FFFFFF", source: "figma-context" }
  },
  typography: {
    "body-size":   { value: "16px", source: "figma-variables" },
    "heading-weight": { value: "700", source: "figma-context" }
  },
  spacing: { ... },
  "border-radius": { ... },
  shadows: { ... },
  animation: { ... },
  breakpoints: { ... }
}
```

**Merge priority:** `figma-variables` wins over `figma-context` when both provide the same token. Variables are explicit declarations; context values are inferred from usage.

### 4.2 Component List

Extract component information from design context responses into a structured list:

```
FIGMA_COMPONENTS = [{
  figmaName: "Button / Primary",
  dsName: "Button",
  variants: ["primary", "secondary", "ghost"],
  confidence: "high",
  source: "figma-context"
}]
```

**Confidence levels:**
- `high` — named component instance with clear variant properties
- `medium` — repeated pattern with consistent naming
- `low` — inferred from layout structure, name is ambiguous

If design context returned no component data → `FIGMA_COMPONENTS = []` (empty, not error).

### 4.3 Screen Index

```
FIGMA_SCREENS = [{
  slug: "login-screen",
  nodeId: "42:15",
  name: "Login Screen",
  page: "Authentication",
  dimensions: "375×812",
  hasScreenshot: true,
  hasDesignContext: true
}]
```

### 4.4 Extraction Summary

Output a summary after extraction so the calling command (or the user) can quickly assess what data is available without parsing the full token map. This is especially important when extraction is partial — the consumer needs to know which data sources succeeded and which gaps remain.

Include these fields:

```
Figma Extraction Summary
Source: [URL or "no URL — variables only"]
Screens: [N] discovered, [N] with screenshots
Tokens: [N] from Variables, [N] from Context, [N] total unique
Components: [N] discovered
Warnings: [list if any]
```

## Workflows

### Full Extraction (design-setup)

The default workflow when design-setup provides a Figma URL:

```
CHECK:    whoami → verify connection
PARSE:    URL → fileKey + nodeId
DISCOVER: get_metadata → SCREENS[]
EXTRACT:  get_variable_defs → tokens (primary)
          get_design_context on the most visually complex screens → tokens (fallback) + components
            Pick screens with the most child nodes in metadata — they tend to have
            richer style diversity (forms, dashboards > splash screens, empty states).
            Start with 2-3 screens; add more if token yield is sparse.
          get_screenshot for each screen → visual references (caller saves to disk)
ORGANIZE: Merge token map, build component list, build screen index, output summary
```

### Token-Only (validation/comparison)

When you just need to compare Figma tokens against file-based tokens:

```
CHECK:    whoami → verify connection
PARSE:    URL → fileKey + nodeId
EXTRACT:  get_variable_defs → tokens
          If sparse (<5 tokens): get_design_context on 1-2 complex screens → more tokens
ORGANIZE: Token map with sources for conflict resolution
```

### Screen Catalog (ux/ui commands)

When you need screen structure and visuals, not tokens:

```
CHECK:    whoami → verify connection
PARSE:    URL → fileKey + nodeId
DISCOVER: get_metadata → SCREENS[]
EXTRACT:  get_screenshot for each screen (caller saves to disk)
ORGANIZE: Screen index with screenshots
```

## Example: Full Extraction

Given URL: `https://figma.com/design/kL9xQn2VwM8pYrTb4ZcHjF/MyApp?node-id=0-1`

```
Step 0: whoami() → ✓ connected as "design-team@example.com"

Step 1: Parse URL
  fileKey: kL9xQn2VwM8pYrTb4ZcHjF
  nodeId: 0:1

Step 2: get_metadata(fileKey, nodeId: "0:1")
  → Page "Auth" has frames: Login (42:15, 375×812), Register (42:30, 375×812)
  → Page "Main" has frames: Dashboard (50:1, 1440×900), Settings (50:20, 1440×900)
  SCREENS = [
    { nodeId: "42:15", slug: "login", page: "Auth" },
    { nodeId: "42:30", slug: "register", page: "Auth" },
    { nodeId: "50:1",  slug: "dashboard", page: "Main" },
    { nodeId: "50:20", slug: "settings", page: "Main" }
  ]

Step 3a: get_variable_defs(fileKey)
  → 12 variables found: color/primary/500=#3B82F6, color/neutral/100=#F5F5F5,
    spacing/sm=8, spacing/md=16, spacing/lg=24, radius/md=8, ...
  → All tagged source: "figma-variables"

Step 3b: get_design_context(fileKey, nodeId: "50:1")  ← Dashboard has most children
  → Found additional: font-family=Inter, heading-size=24px, body-size=14px,
    shadow-card=0 2px 4px rgba(0,0,0,0.1)
  → Components: Button/Primary (3 variants), Card, Input, Avatar
  → All tagged source: "figma-context"

Step 3c: get_screenshot for each of 4 screens
  → 4/4 captured, returned to caller for saving

Step 4: Merge → 12 variable tokens + 4 context tokens = 16 total unique
  Components: 4 discovered (Button: high, Card: medium, Input: medium, Avatar: low)
  Summary: 4 screens, 16 tokens, 4 components, 4 screenshots, 0 warnings
```

## Error Handling

Figma extraction is **enrichment, not requirement**. The pipeline continues without Figma data — it just has less information for conflict resolution.

| Error | Response |
|---|---|
| `whoami` fails (Step 0) | MCP not connected → warn user, skip all Figma steps |
| Invalid URL format | Warn with supported formats → skip |
| FigJam/Slides URL | Warn "not supported for token extraction" → skip |
| Empty variables | Normal — fall back to design context (3.2) |
| Truncated response | Narrow scope → fetch children individually |
| Screenshot timeout | Log warning → try smaller child frames → continue |
| Permission denied | Warn "check Figma file sharing settings" → skip |
| All extractions fail | Warn → continue pipeline without Figma data |

## Quick Reference

| Step | Tool | Purpose |
|---|---|---|
| CHECK | `whoami` | Verify MCP connection |
| DISCOVER | `get_metadata` | File structure, pages, frames, node IDs |
| EXTRACT tokens | `get_variable_defs` | Design Variables (primary token source) |
| EXTRACT context | `get_design_context` | Applied styles, layout, components (fallback) |
| EXTRACT visuals | `get_screenshot` | Visual reference for each screen |

| Source Tag | Meaning | Priority |
|---|---|---|
| `figma-variables` | Explicitly defined Figma Variable | Higher |
| `figma-context` | Inferred from applied styles on frames | Lower |