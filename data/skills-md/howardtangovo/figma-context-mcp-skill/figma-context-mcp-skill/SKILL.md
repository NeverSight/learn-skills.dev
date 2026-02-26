---
name: Figma-Context-MCP-Skill
description: Translate Figma nodes into production-ready code with 1:1 visual fidelity using Framelink Figma-Context-MCP (get_figma_data and download_figma_images). Trigger when the user provides Figma URLs or node IDs, or asks to implement components/pages that must match Figma precisely, and the workflow should use Figma-Context-MCP instead of the official Figma MCP server.
---

# Implement Design (Context MCP)

## Overview

Use this skill to implement Figma designs with high fidelity by using **Figma-Context-MCP** (`figma-developer-mcp`) as the data source.
Treat MCP output as design truth, then translate it into project conventions (components, tokens, styling, architecture).

## Prerequisites

- Figma-Context-MCP server is configured and reachable in the current client
- User provides a Figma URL or explicit `fileKey` + `nodeId`
- A Figma personal access token is available (`FIGMA_API_KEY`)

### Typical MCP server config (stdio)

```json
{
  "mcpServers": {
    "Framelink MCP for Figma": {
      "command": "npx",
      "args": ["-y", "figma-developer-mcp", "--figma-api-key=YOUR-KEY", "--stdio"]
    }
  }
}
```

## Required Workflow

Follow these steps in order.

### Step 1: MCP Connectivity Probe (Required)

Before implementation, verify the MCP connection by calling `get_figma_data` directly.

Use the target node when available:

```text
get_figma_data(fileKey="<fileKey>", nodeId="<nodeId>")
```

Success criteria:

- tool returns node data (metadata/layout/styles), even if partial/truncated
- no MCP transport/auth error

Failure handling:

- if call fails, stop implementation and report the exact error
- explicitly state that "enabled in config" may still mean "not connected in current session"
- ask user to fix MCP session/config/token, then retry probe

### Step 2: Parse Figma Link

Extract from URL:

- `fileKey`: segment after `/design/` or `/file/`
- `nodeId`: value of `node-id` query parameter

Convert `nodeId` to MCP-accepted format when needed:

- URL often gives `1-2`
- tool accepts `1:2` and also supports `-`; both are generally valid

### Step 3: Fetch Node Context with `get_figma_data`

Call:

```text
get_figma_data(fileKey="<fileKey>", nodeId="<nodeId>")
```

Use output for:

- layout structure and auto layout rules
- typography and color styles
- component hierarchy and variants
- image/vector node references for asset extraction

If payload is too large:

- request target child node IDs from current result, then fetch child nodes individually with `get_figma_data`
- only use `depth` when the user explicitly asks for constrained traversal

### Step 4: Download Assets with `download_figma_images`

When `get_figma_data` returns image/vector references, call:

```text
download_figma_images(fileKey="<fileKey>", nodes=[...], localPath="<absolute-path>")
```

Rules:

- only use assets from Figma output
- do not replace with third-party icon packs
- use absolute paths for `localPath`
- preserve exported filenames and suffixes for traceability

### Step 5: Translate to Project Conventions

- map Figma styles to existing design tokens
- replace generated/raw structures with project components
- keep framework idioms (state, routing, data flow, styling system)
- avoid hardcoded constants when token/component exists

### Step 6: Achieve 1:1 Visual Fidelity

Validate against Figma node data and proportions:

- spacing and sizing
- typography (family, size, weight, line-height)
- colors, borders, radius, shadows
- interaction states
- responsive behavior

If exact parity conflicts with system constraints, keep system primitives and apply minimal targeted overrides.

### Step 7: Final Validation Checklist

- [ ] layout and alignment match Figma
- [ ] text and typography match Figma
- [ ] colors/effects match Figma
- [ ] image/vector assets are complete and not substituted
- [ ] interactions and responsiveness are implemented
- [ ] accessibility baseline is preserved

## Implementation Rules

- Reuse existing project components before creating new ones
- Keep components composable and typed
- Prefer tokenized values over literals
- Document intentional deviations briefly in code comments

## Quick Example

User request:

```text
Implement this page: https://figma.com/design/AbC12345XYZ/MyPage?node-id=10-22
```

Execution outline:

1. extract `fileKey=AbC12345XYZ`, `nodeId=10-22`
2. run MCP connectivity probe: `get_figma_data(fileKey="AbC12345XYZ", nodeId="10-22")`
3. if probe succeeds, fetch/expand node context with additional `get_figma_data` calls as needed
4. collect image/vector nodes from response
5. call `download_figma_images(...)` to project assets directory
6. implement with existing component system and tokens
7. verify fidelity and interaction behavior
