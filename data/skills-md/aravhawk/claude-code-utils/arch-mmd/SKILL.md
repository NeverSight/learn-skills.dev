---
name: arch-mmd
description: Creates/updates an ARCHITECTURE.mmd file mapping out the codebase/product. Use whenever the user asks to see the architecture of the codebase/product or when the architecture changes and the current ARCHITECTURE.mmd file is out of date.
---

# Architecture Diagram Generator

Create or update an `ARCHITECTURE.mmd` Mermaid diagram that maps out the codebase's high-level architecture. The goal is a **clean, readable overview** — not an exhaustive map of every file.

---

## PHASE 1: EXPLORE THE CODEBASE

Scan the project to understand its architecture at a **high level**:

1. **Identify project type** — framework, language, monorepo vs single app
2. **Find the entry point(s)** — what kicks things off (CLI, web server, main function)
3. **Identify the core modules** — the 5-15 key components that form the backbone (not every file)
4. **Trace the main data flow** — the primary happy path from input to output
5. **Find external dependencies** — databases, APIs, third-party services (only the important ones)
6. **Note major boundaries** — client/server, package boundaries in monorepos

---

## PHASE 2: BUILD THE DIAGRAM

Use `graph TD` (top-down) as the default direction. Use `graph LR` only if the architecture is clearly pipeline-shaped.

### Simplicity is paramount

The diagram should be **immediately readable on a single screen**. Think of it as an architecture overview you'd sketch on a whiteboard — not a full system blueprint.

- **Target 8-20 nodes** for most projects. Small projects may have fewer, large monorepos may stretch to ~25 max. If you're exceeding 20, you're almost certainly too granular.
- **Do NOT use `subgraph`** — they add visual clutter and nesting complexity. Use color coding to group related nodes instead.
- **Minimize edge crossings** — structure nodes so the flow reads cleanly top-to-bottom (or left-to-right). If connections are crisscrossing everywhere, reorganize.
- **One level of detail** — pick a consistent abstraction level. Don't mix "the entire frontend" as one node alongside individual Python files as separate nodes.

### Node labels

Include the **file/module name** and a **brief description** using `<br/>` for multi-line labels:

```
ENGINE["engine.py<br/>CodeLoader + Orchestrator"]
CLI["cli.py<br/>Arg parsing + validation"]
```

For simple/obvious nodes, a single-line label is fine:

```
DB[(PostgreSQL)]
```

Keep labels short — max ~5-6 words per line.

### Node IDs

Use short, uppercase IDs: `CLI`, `ENGINE`, `AUTH`, `DB`, `API`

### Connections

- Use `-->` for standard flow
- Label edges **sparingly** — only when the relationship isn't obvious from context: `-->|"REST"|`, `-->|"WebSocket"|`
- Use `&` fan-in syntax when multiple nodes feed into one target:

```
P1 & P2 & P3 --> AGENT
```

- **Avoid excessive connections.** Not every interaction needs an arrow. Show the primary architectural flow, not every function call.

### Color coding with `style`

Color-code nodes by their **role** to make the diagram scannable at a glance. Pick a small, consistent palette (4-6 colors max). Always include `color:#fff` for readability.

Role-to-color suggestions (adapt to the project):

| Role | Color | Example |
|---|---|---|
| Entry point / user-facing | `#e74c3c` (red) | CLI, UI, API gateway |
| Core engine / orchestrator | `#2980b9` (blue) | Main engine, coordinator |
| Agent / processor | `#8e44ad` (purple) | Workers, agents, handlers |
| External service / API | `#e67e22` (orange) | Third-party APIs, LLMs |
| Output / result | `#27ae60` (green) | Reports, exports, responses |
| Infrastructure / runtime | `#16a085` (teal) | Runners, browsers, terminals |

Example:
```
style ENGINE fill:#2980b9,color:#fff
style REPORT fill:#27ae60,color:#fff
```

### Node shapes

- `["Label"]` — default rectangle for most components
- `[(Database)]` — databases and data stores only
- `(["Label"])` — stadium shape for entry points (optional, use sparingly)
- No other shapes needed; keep it uniform

---

## PHASE 3: WRITE THE FILE

1. Write the diagram to `ARCHITECTURE.mmd` in the project root
2. If `ARCHITECTURE.mmd` already exists, read it first, then update it to reflect the current state — don't start from scratch unless the existing diagram is fundamentally wrong
3. The file should contain ONLY the Mermaid diagram — no markdown fences, no frontmatter, no prose

---

## CONSTRAINTS

**Readability over completeness — this is the #1 rule.**

- **Keep it simple** — if the diagram looks complex, it IS too complex. Collapse groups of related files into a single node (e.g., "API Routes" instead of listing every route file). The diagram should be a clean high-level overview.
- **8-20 nodes for most projects** — this is a hard guideline. Fewer is often better. Only exceed ~20 for genuinely large/complex systems, and never exceed ~25.
- **No subgraphs** — use color coding to visually group nodes instead.
- **Map real modules, not abstractions** — nodes should correspond to actual files, packages, or services, not vague concepts like "Business Logic Layer"
- **Brief descriptions** — use `<br/>` in labels so someone unfamiliar can understand each node's role
- **Always color-code** — a diagram without `style` directives is incomplete
- **No orphan nodes** — every node must connect to at least one other node
- **Accuracy over completeness** — only include components confirmed to exist; leave out anything marginal
- **Update, don't recreate** — when updating an existing diagram, preserve structural choices and only change what's outdated
