---
name: openspec-design
description: Extends OpenSpec with design asset integration. Use when the user asks to "run openspec-design", "enhance openspec design", or "apply openspec-design". When invoked, updates the project's openspec/AGENTS.md to extend the proposal flow with Figma MCP, design asset directory, and design-map.md.
---

# OpenSpec Design Extension

Adds design asset integration to OpenSpec's proposal stage: when the user's prompt includes Figma links or images, automatically fetch design data, save to `design/`, and generate a design summary document.

---

## Updating AGENTS.md on Execution

**When the user invokes this skill**, read the project's `openspec/AGENTS.md` and make two updates:

1. **Workflow step**: In the "Creating Changes" workflow, between "Choose change-id" and "Scaffold", insert: "Design Extension (if Figma in prompt): If the prompt contains a Figma link, the agent MUST call `call_mcp_tool` to run Figma MCP, create `design/`, and generate `design-map.md`. Do not skip."

2. **Design Extension section**: Between "Proposal Structure" and "Spec File Format", insert the following Design Extension section. If it already exists, overwrite it.

---

## Full Fragment to Insert into AGENTS.md

Insert the following content into `openspec/AGENTS.md` at the locations above:

```markdown
### Design Extension (Figma & Images)

When the proposal's user prompt contains **Figma information** or **images**, the agent **MUST** use `call_mcp_tool` to actively call Figma MCP—do not merely describe it. When a Figma link is detected, **do not skip** the MCP call.

**Figma detection** (any of the following):
- Figma links (`figma.com/file/`, `figma.com/design/`), e.g. `https://www.figma.com/design/pxhnkHfGrSwHbxT1pfV0T4/xxx?node-id=2496-1199`
- Parse from URL: file key = `pxhnkHfGrSwHbxT1pfV0T4` in the path, node-id = query param `2496-1199`

**Figma MCP tools** (via call_mcp_tool):
- `parse_figma_url`: Parse URL to extract file key, node id
- `get_file`: Get file info
- `get_node`: Get node/frame details
- `export_images`: Export images (PNG/JPG/SVG)

**Extension flow**:
1. Create `design/` under `changes/[change-id]/`
2. If Figma: **MUST** call Figma MCP (parse_figma_url → get_file/get_node → export_images), save exported images to `design/`
3. If prompt has attachment images or local image paths: copy them to `design/` as context assets
4. Generate `design/design-map.md` with asset list and design summary

**Note**: `design/` is the design asset directory, distinct from sibling `design.md` (technical design doc). If Figma MCP fails, prompt the user to check MCP config; without MCP, only process local images.
```

---

## Design Extension Flow Details

### 1. Create design/ Directory

Create `design/` under `changes/<change-id>/`, alongside `proposal.md`, `tasks.md`, `design.md`, and `specs/`.

### 2. Figma MCP Call (Must Execute Explicitly)

**MUST call via `call_mcp_tool`**—do not only describe. Do not skip when a Figma link is detected.

**Figma MCP tools**:
- `parse_figma_url`: Parse URL to extract file key, node id
- `get_file`: Get file info
- `get_node`: Get node/frame details
- `export_images`: Export images (PNG/JPG/SVG)

**Call flow**:
1. Parse Figma link from prompt (e.g. `figma.com/design/pxhnkHfGrSwHbxT1pfV0T4/xxx?node-id=2496-1199`)
2. Use `parse_figma_url` or manual parse to get file key, node-id
3. Call `get_file` / `get_node` to fetch design details
4. Call `export_images` to export images
5. Save exports to `design/`, naming convention: `figma-<node-name>-<index>.png`

### 3. Image Asset Collection

- User-attached images: save directly to `design/`
- Local paths referenced in prompt: copy to `design/`
- Use semantic naming to avoid collisions

### 4. design-map.md Generation

Generate `design-map.md` under `design/`. Recommended structure:

```markdown
# Design Map

## Asset List

| File | Source | Description |
|------|--------|-------------|
| figma-hero-1.png | Figma MCP | Homepage hero |
| screenshot-1.png | User attachment | Reference screenshot |

## Design Summary

- [Key design decisions extracted from designs/images]
```

---

## design-map.md Template

```markdown
# Design Map

## Asset List

| File | Source | Description |
|------|--------|-------------|
| (filename) | Figma MCP / User attachment / Local | (brief description) |

## Design Summary

- (Point 1)
- (Point 2)
```

---

## Dependencies

- **Figma MCP**: Requires Figma MCP Server configured in the project. If not configured, the skill prompts the user to configure it, or only processes local/attached images.
