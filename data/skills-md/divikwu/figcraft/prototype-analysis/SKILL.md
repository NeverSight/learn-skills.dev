---
name: prototype-analysis
description: "Analyze prototype interactions and generate flow documentation. Use when: analyze/inspect/review + prototype/flow/interactions/navigation, or when checking for dead ends, missing navigation, or generating flow diagrams."
---

# Prototype Analysis — Flow Inspection & Documentation

Analyze prototype interactions in Figma files. Produces a directed flow graph, Mermaid diagram, and identifies navigation issues (dead ends, loops, missing back navigation). Can also batch-connect screens to fix flow gaps.

## Skill Boundaries

- Use this skill to **analyze and document existing prototype flows**.
- If the task is **creating new prototype interactions from scratch**, use `load_toolset("prototype")` directly with `add_reaction` or `connect_screens`.
- If the task is **reviewing visual design quality**, switch to [design-review](../design-review/SKILL.md).
- If the task is **creating UI screens**, switch to [figma-create-ui](../figma-create-ui/SKILL.md).

## Workflow

### Step 1: Connect and Load Tools

```
ping                                          → verify plugin connection
load_toolset("prototype")                     → enable prototype analysis tools
```

**If `ping` fails (plugin not connected):** STOP. Do not fall back to other MCP servers. Tell user: open Figma → Plugins → FigCraft → wait for connection, then retry.

### Step 2: Analyze Flow

```
analyze_prototype_flow                        → scan current page for all interactions
```

Optional parameters:
- `nodeId` — analyze a specific subtree instead of the full page
- `format` — `"all"` for complete output (graph + mermaid + markdown)

Returns:
- Directed graph of screens/nodes with connections
- Entry points (screens with outgoing interactions but no incoming — starting screens)
- Dead ends (screens with incoming interactions but no outgoing — user gets stuck)
- Loops (circular navigation paths)
- Trigger/action statistics
- Mermaid flow diagram
- Markdown documentation

### Step 3: Present Summary

Report the flow health:

```
📊 Flow Summary:
- Screens: X total
- Interactions: Y connections
- Entry points: [list]
- Dead ends: [list] ⚠️
- Loops: [list]
- Trigger types: ON_CLICK (N), ON_HOVER (M), ...
```

### Step 4: Show Flow Diagram

Present the Mermaid diagram for visual understanding of the navigation structure.

### Step 5: Highlight Issues

Flag navigation problems:

- ⚠️ Dead ends — screens with no outgoing interactions (user gets stuck)
- ⚠️ Missing back navigation — screens reachable only one-way
- ⚠️ Trapping loops — circular paths with no exit
- ⚠️ Single trigger type — screens with only ON_CLICK (consider adding hover/keyboard alternatives for accessibility)
- ⚠️ Orphan screens — screens with no connections at all

### Step 6: Fix Flow Gaps (Optional)

If the user wants to fix issues, use `connect_screens` to batch-wire missing connections:

```
connect_screens(connections: [
  { sourceId: "1:23", destinationId: "4:56", trigger: "ON_CLICK" },
  { sourceId: "4:56", destinationId: "1:23", trigger: "ON_CLICK" }
])
```

After connecting, `connect_screens` automatically re-runs `analyze_prototype_flow` to validate the updated flow.

## Available Tools

| Tool | Purpose |
|------|---------|
| `analyze_prototype_flow` | Full flow analysis with graph, mermaid, and docs |
| `get_reactions` | Inspect interactions on a specific node or all nodes |
| `connect_screens` | Batch-connect screens with prototype interactions |
| `add_reaction` | Add a single interaction to a node |
| `remove_reaction` | Remove interactions from a node |
| `set_reactions` | Replace all interactions on a node |

## Integration

Prototype analysis is typically used:
- After building multi-screen flows with `figma-create-ui`
- During design review to verify navigation completeness
- Before handoff to ensure all flows are documented
