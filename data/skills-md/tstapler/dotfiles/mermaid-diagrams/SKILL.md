---
name: mermaid-diagrams
description: Generate beautiful, well-styled Mermaid diagrams. Use when asked to create architecture diagrams, flowcharts, sequence diagrams, state machines, ER schemas, or any visual diagram using Mermaid syntax. Produces professional output with correct syntax, appropriate diagram type selection, and polished styling. To review or improve a diagram that already exists (legend, shape/color notation, C4 abstraction level, post-render readability) rather than generate a new one, use diagram-design-review.
---

# Mermaid Diagram Generator

Generate professional Mermaid diagrams with correct syntax, good styling, and appropriate type selection.

## Diagram Type Selection

| Use Case | Type | Opening Keyword |
|---|---|---|
| Process flow / algorithm / decision tree | Flowchart | `flowchart LR` or `flowchart TD` |
| API calls / system interaction / request lifecycle | Sequence | `sequenceDiagram` |
| Object model / domain model / class relationships | Class | `classDiagram` |
| Auth flows / UI states / lifecycle / FSM | State | `stateDiagram-v2` |
| Database schema / data model | ER | `erDiagram` |
| Git branching / release strategy | Git Graph | `gitGraph` |
| System context / containers / microservices topology | C4 | `C4Context` |
| Cloud / infra topology | Architecture | `architecture-beta` |
| Project timeline | Gantt | `gantt` |
| Prioritization / 2x2 matrix | Quadrant | `quadrantChart` |

**Quick rules:**
- Ordered interactions over time → Sequence
- "What states can this be in" → State
- "What exists and how it relates" → ER or Class
- "How the system is structured" → C4 or Architecture (not Flowchart)
- Default to `TD` for flowcharts. Only reach for `LR` when nodes are a genuinely sequential handoff (a short pipeline of 3-5 steps) — not merely because a diagram has many parallel branches.
- More than ~15 nodes flat → decompose into subgraphs, not a switch to `LR`

**When the diagram will be embedded in a fixed-width document** (e.g. pushed to Google Docs via docspan, or any page/PDF target): prefer `TD`/vertical layouts even more strongly. A page's width is capped but its height isn't, and a rendered diagram gets scaled as a whole to fit that fixed width — a wide `LR` diagram with many parallel branches gets crushed down until its text is illegible, while the same content in `TD` grows downward instead, keeping text at a readable size. Widen with subgraphs stacked vertically rather than spreading nodes horizontally.

## Styling: Always Apply These

### 1. Init directive (use `base` theme for custom colors)

```
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#1E293B',
  'primaryTextColor': '#F1F5F9',
  'primaryBorderColor': '#334155',
  'lineColor': '#64748B',
  'edgeLabelBackground': '#F8FAFC',
  'fontFamily': 'ui-sans-serif, system-ui',
  'fontSize': '14px'
}}}%%
```

**Critical:** Only `base` theme accepts `themeVariables`. Using `default` silently ignores all overrides.

### 2. classDef for reusable node styles

```
classDef primary fill:#3B82F6,stroke:#1D4ED8,color:#fff,stroke-width:2px
classDef success fill:#10B981,stroke:#065F46,color:#fff,stroke-width:2px
classDef warning fill:#F59E0B,stroke:#92400E,color:#fff,stroke-width:2px
classDef danger  fill:#EF4444,stroke:#991B1B,color:#fff,stroke-width:2px
classDef ghost   fill:#F9FAFB,stroke:#D1D5DB,color:#374151,stroke-dasharray:5 5
```

Apply inline: `NodeId:::className`

### 3. Subgraphs with direction override

```
subgraph frontend["Frontend Layer"]
  direction LR
  UI[React UI] --> Store[State]
end
style frontend fill:#EFF6FF,stroke:#BFDBFE
```

### 4. linkStyle for edge appearance (0-indexed, in declaration order)

```
linkStyle 0 stroke:#3B82F6,stroke-width:2px
linkStyle 1 stroke:#EF4444,stroke-dasharray:5 5
linkStyle default stroke:#94A3B8,stroke-width:1.5px
```

## Ready-to-Use Templates

See `templates.md` for four copy-paste templates: architecture flowchart, API sequence, state machine, ER schema.

## Key Syntax Rules

- Node labels with special chars must be quoted: `A["label (with parens)"]`
- `%%` is a comment
- Sequence `autonumber` adds step numbers automatically
- ER attribute syntax: `type name PK/FK/UK`
- State machines: use `stateDiagram-v2`, not the v1 syntax
- Subgraph direction overrides only work when no node inside links outside

## Anti-Patterns to Avoid

- ❌ Long sentences as node labels — use 2–5 words max
- ❌ Using `default` theme with `themeVariables` — use `base`
- ❌ `style` on many nodes individually — use `classDef` for 2+ nodes
- ❌ Using Flowchart for object relationships — use Class or ER
- ❌ Using Sequence for static structure — use Architecture or C4
- ❌ CamelCase node IDs as display labels — always provide `[Human Label]`
- ❌ Low-contrast colors (light text on light fill)
- ❌ More than 15 nodes flat — decompose into subgraphs
- ❌ Color as the only semantic signal — combine with shape or label text

> To publish the generated diagrams to Confluence, apply the `knowledge-confluence-sync` skill.

## Generation Workflow

1. **Identify the diagram type** from the use case (use table above)
2. **Choose orientation**: default to `TD` (vertical); use `LR` only for a short, genuinely sequential pipeline (3-5 steps) — see the fixed-width-document rule above if this diagram is headed for a page-width target
3. **Draft the nodes and edges** with clear, short labels
4. **Apply `%%{init}%%`** with `base` theme + color variables matching the site's palette
5. **Define `classDef` groups** for semantic categories (primary, success, warning, danger)
6. **Apply classes** with `:::className` inline notation
7. **Add subgraphs** for logical groupings with `style` for fill/border
8. **Review anti-patterns** before finalizing

For the personal website (tyler.staplerstation.com), default palette:
- Primary blue: `#1a6fad`
- Dark background: `#1E293B`
- Light surface: `#F8FAFC`
- Border: `#E2E8F0`

For detailed templates: see `templates.md`

---

## Related Skills

| Skill | When to apply |
|-------|--------------|
| `knowledge-confluence-sync` | Publish markdown with Mermaid diagrams to Confluence |
| `knowledge-synthesis` | Add diagrams to Zettelkasten notes or concept maps |
| `code-architecture-best-practices` | Document architecture decisions with C4 or flowchart diagrams |
| `diagram-design-review` | Review an existing diagram for legend, shape/color notation, C4 level, and readability once rendered |
