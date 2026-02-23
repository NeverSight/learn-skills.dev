---
name: flowzap-diagrams
description: >
  Generate, validate and publish workflow, sequence and architecture diagrams, using FlowZap Code DSL.
  Use when the user asks to create a workflow, flowchart, sequence diagram, process map or an architecture diagram.
  Produces .fz code and shareable playground URLs via the FlowZap MCP server.
---

# FlowZap Diagram Skill

Generate valid FlowZap Code (.fz) diagrams from natural-language descriptions,
validate them, and return shareable playground URLs — all without leaving your
coding agent.

## When to use this skill

- User asks for a **workflow**, **flowchart**, **process diagram**, **sequence diagram**, or **achitecture diagram**.
- User pastes HTTP logs, OpenAPI specs, or code and wants them visualised.
- User wants to **compare** two diagram versions (diff) or **patch** an existing diagram.

## MCP server setup (one-time)

If the FlowZap MCP server is not already configured, install it:

```bash
# Claude Code
claude mcp add --transport stdio flowzap -- npx -y flowzap-mcp@1.3.5

# Or add to .mcp.json / claude_desktop_config.json / cursor / windsurf config:
{
  "mcpServers": {
    "flowzap": {
      "command": "npx",
      "args": ["-y", "flowzap-mcp@1.3.5"]
    }
  }
}
```

Compatible tools: Claude Desktop, Claude Code, Cursor, Windsurf, OpenAI Codex,
Warp, Zed, Cline, Roo Code, Continue.dev, Sourcegraph Cody.

**Not compatible:** Replit, Lovable.dev.

## Available MCP tools

| Tool | Purpose |
|------|---------|
| `flowzap_validate` | Check .fz syntax before sharing |
| `flowzap_create_playground` | Get a shareable playground URL |
| `flowzap_get_syntax` | Retrieve full DSL docs at runtime |
| `flowzap_export_graph` | Export diagram as structured JSON (lanes, nodes, edges) |
| `flowzap_artifact_to_diagram` | Parse HTTP logs / OpenAPI / code → diagram + playground URL |
| `flowzap_diff` | Structured diff between two .fz versions |
| `flowzap_apply_change` | Patch a diagram (insert/remove/update nodes/edges) |

## FlowZap Code DSL — quick reference

FlowZap Code is **not** Mermaid, **not** PlantUML. It is a unique DSL offering a simple syntax for a triple-view option to workflow, sequence and architecture diagrams.

### Shapes (only 4)

| Shape | Use for |
|-------|---------|
| `circle` | Start / End events |
| `rectangle` | Process steps / actions |
| `diamond` | Decisions (Yes/No branching) |
| `taskbox` | Assigned tasks (`owner`, `description`, `system`) |

### Syntax rules

- **Node IDs** are globally unique, sequential, no gaps: `n1`, `n2`, `n3` …
- **Node attributes** use colon: `label:"Text"`
- **Edge labels** use equals inside brackets: `[label="Text"]`
- **Handles** are required on every edge: `n1.handle(right) -> n2.handle(left)`
- **Directions**: `left`, `right`, `top`, `bottom`
- **Cross-lane edges**: prefix target with lane name: `sales.n5.handle(top)`
- **Lane display label**: one `# Label` comment right after opening brace
- **Loops**: `loop [condition] n1 n2 n3` — flat, inside a lane block
- **Layout**: prefer horizontal left→right; use top/bottom only for cross-lane hops

### Gotchas — never do these

- Do NOT use `label="Text"` on nodes (must be `label:"Text"`).
- Do NOT use `label:"Text"` on edges (must be `[label="Text"]`).
- Do NOT skip node numbers (n1, n3 → invalid; must be n1, n2).
- Do NOT omit lane prefix on cross-lane edges.
- Do NOT output Mermaid, PlantUML, or any other syntax.
- Do NOT add comments except the single `# Display Label` per lane.
- Do NOT place `loop` outside a lane's braces.
- Do NOT use a `taskbox` shape unless the user explicitly requests it.

### Minimal templates

**Single lane:**

```
process { # Process
n1: circle label:"Start"
n2: rectangle label:"Step"
n3: circle label:"End"
n1.handle(right) -> n2.handle(left)
n2.handle(right) -> n3.handle(left)
}
```

**Two lanes with cross-lane edge:**

```
user { # User
n1: circle label:"Start"
n2: rectangle label:"Submit"
n1.handle(right) -> n2.handle(left)
n2.handle(bottom) -> app.n3.handle(top) [label="Send"]
}

app { # App
n3: rectangle label:"Process"
n4: circle label:"Done"
n3.handle(right) -> n4.handle(left)
}
```

**Decision branch:**

```
flow { # Flow
n1: rectangle label:"Check"
n2: diamond label:"OK?"
n3: rectangle label:"Fix"
n4: rectangle label:"Proceed"
n1.handle(right) -> n2.handle(left)
n2.handle(bottom) -> n3.handle(top) [label="No"]
n2.handle(right) -> n4.handle(left) [label="Yes"]
}
```

**For the full DSL specification and advanced multi-lane examples**: See [references/syntax.md](references/syntax.md)

## Workflow: how to generate a diagram

1. Identify the **actors/systems** (→ lanes) and **steps** (→ nodes) from the user's description.
2. Write FlowZap Code following all rules above.
3. Call `flowzap_validate` to verify syntax.
4. If valid, call `flowzap_create_playground` to get a shareable URL.
5. Return the FlowZap Code **and** the playground URL to the user.
6. Always output **only** raw FlowZap Code when showing the diagram — no Markdown fences wrapping .fz content, no extra commentary mixed in.

Full MCP documentation: [flowzap.xyz/docs/mcp](https://flowzap.xyz/docs/mcp)

## Further resources

- [FlowZap Code full spec](https://flowzap.xyz/flowzap-code)
- [LLM context file](https://flowzap.xyz/llms-full.txt)
- [JSON syntax schema](https://flowzap.xyz/api/flowzap-code-schema.json)
- [200+ workflow templates](https://flowzap.xyz/templates)
- [MCP server docs](https://flowzap.xyz/docs/mcp)
- [npm package — flowzap-mcp v1.3.5](https://www.npmjs.com/package/flowzap-mcp)
- [GitHub](https://github.com/flowzap-xyz/flowzap-mcp)
