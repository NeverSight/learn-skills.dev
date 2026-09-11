---
name: archdraw-diagram
description: Create, refine, validate, and export software architecture diagrams in ArchDraw. Use for architecture views, system maps, repository-informed diagrams, and architecture change documentation; do not use for generic flowcharts or UI mockups.
---

# ArchDraw Diagram

Use ArchDraw when a user needs a clear, editable software architecture diagram or wants to turn codebase knowledge into a shared architecture view. ArchDraw is for system context, service boundaries, request and event flows, data stores, external dependencies, and proposed architecture changes.

## Prerequisite — for both user and agent

**Check first:** verify ArchDraw MCP tools (`generate_diagram`, `validate_diagram`, etc.) are listed. If missing, do not invent a diagram — guide installation, then retry.

**Fast path (recommended for both):** one command installs the skill and wires the MCP for every detected agent:
```bash
npx archdraw-agent setup --dry-run  # preview
npx archdraw-agent setup             # Codex + Claude + OpenCode
npx archdraw-agent setup --agent codex --dry-run
```

**Agent behavior:** if you have shell access, you MAY attempt setup yourself (`npx archdraw-agent setup` or the per-agent commands below). On success, tell the user a restart is required and re-check tools. On failure or no shell, **do not loop** — output the exact commands for the user, wait for confirmation, then re-check. Never substitute another diagram tool.

**Per-agent commands (for user to run, or agent to run when `archdraw-agent` is unavailable):**

**Codex**
```bash
codex mcp add archdraw -- npx -y @hiabhee/archdraw-mcp-server
```

**Claude Code**
```bash
claude mcp add archdraw -- npx -y @hiabhee/archdraw-mcp-server
```

**Claude Desktop** — add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "archdraw": {
      "command": "npx",
      "args": ["-y", "@hiabhee/archdraw-mcp-server"]
    }
  }
}
```

**OpenCode** — add to `opencode.json`:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "archdraw": {
        "type": "local",
        "command": ["npx", "-y", "@hiabhee/archdraw-mcp-server"]
      }
    }
  }
}
```
Copy the skill for OpenCode to `.opencode/skills/archdraw-diagram/` (project) or `~/.config/opencode/skills/archdraw-diagram/` (global). Then restart and verify:
```bash
opencode mcp list
# or: codex mcp list / claude mcp list
```
OpenCode prefixes tools as `archdraw_generate_diagram`, etc. For other agents, use the same stdio command `npx -y @hiabhee/archdraw-mcp-server`. Default connects to `https://archdraw.hiabhee.online` — set `API_BASE_URL` for self-hosted. Requires Node.js 18+ and a client restart.

## Working with codebases

When the user asks for a diagram of a repository, use the codebase context already available to you when permitted. Identify entry points, services, routes, jobs, data stores, external services, and important request or event paths. Do not claim that a relationship is verified unless supporting code, configuration, or documentation provides evidence.

If the user supplies a GitHub URL and asks for ArchDraw's hosted Repo2Diagram analysis, use that workflow only when the connected ArchDraw MCP exposes a repository-analysis tool. Otherwise, explain that you can create a repository-informed diagram from the code context available to you, then generate it through ArchDraw.

## Workflow

1. Clarify the intended view: current state or proposed state; audience; and scope (whole system, service boundary, request flow, or change).
2. For repository-informed work, inspect accessible code and documentation before modelling. Prefer evidence over inference and call out uncertainty.
3. Produce Mermaid that expresses the architecture clearly. Use `graph LR` for most service maps and `graph TD` when a top-down flow is clearer. Use subgraphs for meaningful boundaries such as client, edge, services, data, and external systems.
4. Call `generate_diagram` with the Mermaid, the user's original request in `userPrompt`, and any explicit technologies in `techStack`. Mermaid is the preferred MCP input mode.
5. If generation reports validation or topology errors, correct the Mermaid and retry with the reported issue addressed. Stop and explain the failure if it cannot be resolved safely.
6. Use `validate_diagram` for a final check when the diagram will be shared or used for a decision. Use `fix_layout` only when the generated layout needs adjustment.
7. Share the returned ArchDraw URL and summarize what the view shows, what evidence supports it, and any assumptions or gaps.

## Diagram quality

- Model a coherent story, not an inventory of boxes. Make the main flow legible first.
- Label edges with the important interaction when it clarifies the relationship; distinguish synchronous calls from asynchronous events where known.
- Group only genuine boundaries. Avoid decorative layers or groups that conceal the flow.
- Keep the scope appropriate to the audience. Create separate views instead of one unreadable all-in-one diagram.
- Preserve explicit technologies and names from the user or repository. Never invent infrastructure, services, or integrations.
- Use ArchDraw's semantic shapes when helpful: gateways/load balancers, people/clients, external systems, security components, and data stores should be visually distinct.

## Architecture changes

For a proposed refactor, migration, or feature, create a clearly labelled proposed-state view. Explain changed components, new dependencies, affected data or event paths, and assumptions that require human review. Do not present a proposal as the repository's current architecture.

## Useful MCP tools

- `generate_diagram` — create a diagram from Mermaid (preferred) or legacy structured JSON.
- `validate_diagram` — validate the current diagram.
- `fix_layout` — re-layout an existing diagram.
- `update_diagram` — make targeted changes to the active diagram.
- `get_diagram_state`, `save_checkpoint`, `load_checkpoint` — inspect or preserve the current working diagram.
- `export_diagram` — export a finished diagram.
- `list_node_types`, `list_templates`, `apply_template`, `read_me` — discover ArchDraw's available building blocks and guidance.

## Output contract

Treat the work as complete only after the diagram is generated successfully and the response includes the ArchDraw URL. For repository-informed diagrams, state the evidence basis and any material assumptions. For changes, distinguish current state from proposed state.
