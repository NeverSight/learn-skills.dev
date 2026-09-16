---
name: understand-anything-knowledge-graph
description: Turn any codebase into an interactive knowledge graph using Claude Code skills — explore, search, and ask questions about any project visually.
triggers:
  - "analyze my codebase with understand anything"
  - "build a knowledge graph of this project"
  - "help me understand this codebase"
  - "install understand anything plugin"
  - "explore codebase visually"
  - "explain how this code is structured"
  - "run understand-dashboard"
  - "generate onboarding guide for my project"
---

# Understand Anything — Codebase Knowledge Graph

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Understand Anything is a [Claude Code](https://docs.anthropic.com/en/docs/claude-code) plugin that runs a multi-agent pipeline over your project, builds a knowledge graph of every file, function, class, and dependency, and opens an interactive React dashboard for visual exploration. It produces plain-English summaries of every node so anyone — developer, PM, or designer — can understand the codebase.

---

## Installation

### Via Claude Code plugin marketplace

```bash
/plugin marketplace add Lum1104/Understand-Anything
/plugin install understand-anything
```

### From source (development)

```bash
git clone https://github.com/Lum1104/Understand-Anything
cd Understand-Anything
pnpm install
pnpm --filter @understand-anything/core build
pnpm --filter @understand-anything/skill build
pnpm --filter @understand-anything/dashboard build
```

---

## Core Skills / Commands

| Command | What it does |
|---|---|
| `/understand` | Run the full multi-agent analysis pipeline on the current project |
| `/understand-dashboard` | Open the interactive knowledge graph dashboard |
| `/understand-chat <question>` | Ask anything about the codebase in natural language |
| `/understand-diff` | Analyze impact of current uncommitted changes |
| `/understand-explain <path>` | Deep-dive explanation of a specific file or function |
| `/understand-onboard` | Generate an onboarding guide for new team members |

---

## Typical Workflow

### 1. Analyze a project

```bash
# Inside any project directory, in Claude Code:
/understand
```

This orchestrates 5 agents in sequence (with file-analyzers running up to 3 concurrent):

1. **project-scanner** — discovers files, detects languages/frameworks
2. **file-analyzer** — extracts functions, classes, imports; builds graph nodes and edges
3. **architecture-analyzer** — groups nodes into architectural layers (API, Service, Data, UI, Utility)
4. **tour-builder** — generates ordered learning tours
5. **graph-reviewer** — validates referential integrity

Output is saved to `.understand-anything/knowledge-graph.json` in your project root.

### 2. Open the dashboard

```bash
/understand-dashboard
```

The React + Vite dashboard opens in your browser. Features:
- **Graph view** — React Flow canvas, color-coded by layer, zoom/pan
- **Node inspector** — click any node for code, relationships, LLM summary
- **Search** — fuzzy + semantic search across all nodes
- **Tours** — guided walkthroughs ordered by dependency
- **Persona mode** — toggle detail level (Junior Dev / PM / Power User)

### 3. Ask questions

```bash
/understand-chat How does authentication work in this project?
/understand-chat What calls the payment service?
/understand-chat Which files are most depended on?
```

### 4. Review diff impact before committing

```bash
# After making changes:
/understand-diff
```

Returns a list of affected nodes in the knowledge graph — shows ripple effects before you push.

### 5. Explain a specific file

```bash
/understand-explain src/auth/login.ts
/understand-explain src/services/PaymentService.ts
```

---

## Knowledge Graph Schema

The graph is stored at `.understand-anything/knowledge-graph.json`. Key types (from `packages/core`):

```typescript
// packages/core/src/types.ts

interface GraphNode {
  id: string;                    // unique: "file:src/auth/login.ts"
  type: "file" | "function" | "class" | "module";
  name: string;
  filePath: string;
  layer: ArchitectureLayer;      // "api" | "service" | "data" | "ui" | "utility"
  summary: string;               // LLM-generated plain-English description
  code?: string;                 // raw source snippet
  language?: string;
  concepts?: LanguageConcept[];  // e.g. "generics", "closures", "decorators"
  metadata?: Record<string, unknown>;
}

interface GraphEdge {
  id: string;
  source: string;                // node id
  target: string;                // node id
  type: "imports" | "calls" | "extends" | "implements" | "uses";
  label?: string;
}

interface KnowledgeGraph {
  version: string;
  generatedAt: string;
  projectRoot: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
  tours: GuidedTour[];
}

type ArchitectureLayer = "api" | "service" | "data" | "ui" | "utility" | "unknown";

type LanguageConcept =
  | "generics"
  | "closures"
  | "decorators"
  | "async-await"
  | "interfaces"
  | "higher-order-functions"
  | "dependency-injection"
  | "observers"
  | "iterators"
  | "pattern-matching"
  | "monads"
  | "currying";
```

---

## Working with the Core Package Programmatically

```typescript
import { loadKnowledgeGraph, searchGraph, buildTour } from "@understand-anything/core";

// Load the persisted graph
const graph = await loadKnowledgeGraph(".understand-anything/knowledge-graph.json");

// Fuzzy search across all nodes
const results = searchGraph(graph, "payment processing");
console.log(results.map(r => `${r.type}:${r.name} (${r.filePath})`));

// Find all callers of a function
const paymentNode = graph.nodes.find(n => n.name === "processPayment");
const callers = graph.edges
  .filter(e => e.target === paymentNode?.id && e.type === "calls")
  .map(e => graph.nodes.find(n => n.id === e.source));

// Get all nodes in the service layer
const serviceNodes = graph.nodes.filter(n => n.layer === "service");

// Build a guided tour starting from a specific node
const tour = buildTour(graph, { startNodeId: "file:src/index.ts" });
tour.steps.forEach((step, i) => {
  console.log(`Step ${i + 1}: ${step.node.name} — ${step.node.summary}`);
});
```

---

## Dashboard Development

```bash
# Start the dashboard dev server (hot reload)
pnpm dev:dashboard

# Build for production
pnpm --filter @understand-anything/dashboard build
```

The dashboard is a Vite + React 18 app using:
- **React Flow** — graph canvas rendering
- **Zustand** — graph state management
- **TailwindCSS v4** — styling
- **Fuse.js** — fuzzy search
- **web-tree-sitter** — in-browser AST parsing
- **Dagre** — automatic graph layout

---

## Project Structure

```
understand-anything-plugin/
├── .claude-plugin/          # Plugin manifest (read by Claude Code)
├── agents/                  # Agent definitions (project-scanner, file-analyzer, etc.)
├── skills/                  # Skill definitions (/understand, /understand-chat, etc.)
├── src/                     # Plugin TypeScript source
│   ├── context-builder.ts   # Builds LLM context from the graph
│   └── diff-analyzer.ts     # Git diff → affected nodes
├── packages/
│   ├── core/                # Analysis engine
│   │   ├── src/
│   │   │   ├── types.ts     # GraphNode, GraphEdge, KnowledgeGraph
│   │   │   ├── persistence.ts
│   │   │   ├── search.ts    # Fuzzy + semantic search
│   │   │   ├── tours.ts     # Tour generation
│   │   │   ├── schema.ts    # Zod validation schemas
│   │   │   └── tree-sitter.ts
│   │   └── tests/
│   └── dashboard/           # React dashboard app
│       └── src/
```

---

## Incremental Updates

Re-running `/understand` only re-analyzes files that changed since the last run (based on mtime and content hash stored in the graph metadata). For large monorepos this makes subsequent runs fast.

To force a full re-analysis:

```bash
rm -rf .understand-anything/
/understand
```

---

## Development Commands

```bash
pnpm install                                        # Install all dependencies
pnpm --filter @understand-anything/core build       # Build core package
pnpm --filter @understand-anything/core test        # Run core tests
pnpm --filter @understand-anything/skill build      # Build plugin package
pnpm --filter @understand-anything/skill test       # Run plugin tests
pnpm --filter @understand-anything/dashboard build  # Build dashboard
pnpm dev:dashboard                                  # Dashboard dev server with HMR
```

---

## Common Patterns

### Before a code review

```bash
# See what your diff actually touches in the architecture
/understand-diff
```

### Onboarding a new engineer

```bash
# Generate a structured onboarding doc grounded in the real code
/understand-onboard
```

### Researching a feature area

```bash
/understand-chat What are all the entry points for the GraphQL API?
/understand-explain src/graphql/resolvers/
```

### Understanding an unfamiliar module

```bash
/understand-explain src/workers/queue-processor.ts
# Returns: summary, key functions, what calls it, what it calls, concepts used
```

---

## Troubleshooting

**`/understand` times out on large repos**
- The file-analyzer runs up to 3 workers concurrently. Very large repos (>50k files) may need patience. Delete `.understand-anything/` and re-run if a previous run was interrupted.

**Dashboard doesn't open**
- Run `pnpm --filter @understand-anything/dashboard build` first if working from source, then retry `/understand-dashboard`.

**Stale graph after major refactor**
- Delete `.understand-anything/knowledge-graph.json` to force full re-analysis: `rm .understand-anything/knowledge-graph.json && /understand`

**`pnpm install` fails with workspace errors**
- Ensure you are using pnpm v8+: `pnpm --version`. The project uses pnpm workspaces defined in `pnpm-workspace.yaml`.

**Search returns no results**
- Confirm the graph was generated: `cat .understand-anything/knowledge-graph.json | head -5`. If empty or missing, run `/understand` first.

---

## Contributing

```bash
# Fork, then:
git checkout -b feature/my-feature
pnpm --filter @understand-anything/core test   # must pass
# open a PR — file an issue first for major changes
```

License: MIT © [Lum1104](https://github.com/Lum1104)
