---
name: architecture-research
version: 1.0.0
description: Research the architecture of a codebase or system. Reads source code, finds external context, explains design decisions, and produces ELK diagrams. Use when asked to understand, explain, or diagram how a repo/system is built.
compatibility: "Requires: diagrams skill (clawhub install diagrams)"
---

# Architecture Research

## Trigger

Activate when the user wants to:
- Understand how a repo or system is architected
- Get diagrams of a codebase's structure or data flow
- Understand design decisions and trade-offs in a project

## Workflow

### 1. Read the Source

Clone or browse the repo. Read actual code — module structure, entry points, key abstractions. Don't rely solely on READMEs.

Focus on:
- Directory structure and module boundaries
- Entry points and public APIs
- Data models and storage
- Config and dependency injection patterns
- Build/deploy setup

### 2. Find External Context

Search for official docs, blog posts, conference talks, design docs, ADRs, and community discussions that explain the *why* behind the architecture.

Cite what you find. If you're inferring rationale (no source), say so explicitly.

### 3. Explain from Multiple Angles

Cover at least these perspectives:

| Angle | What to show |
|-------|-------------|
| **System overview** | Major components and how they connect |
| **Data/control flow** | What happens for a key operation (e.g., a request, a build, a deploy) |
| **Design decisions** | What they chose, the obvious alternative, and why |

### 4. Produce ELK Diagrams (with SVG rendering)

For each major angle, generate an **ELK JSON graph** (elkjs format), then **render it to SVG** so it displays inline in markdown.

#### ELK JSON structure
```json
{
  "id": "root",
  "layoutOptions": {
    "elk.algorithm": "layered",
    "elk.direction": "DOWN",
    "elk.spacing.nodeNode": "40"
  },
  "children": [
    { "id": "node1", "width": 150, "height": 60, "labels": [{ "text": "Component A" }] }
  ],
  "edges": [
    { "id": "e1", "sources": ["node1"], "targets": ["node2"], "labels": [{ "text": "calls" }] }
  ]
}
```

#### Rendering to SVG

This skill uses the **diagrams** skill for rendering. Install it if you haven't:

```bash
clawhub install diagrams
```

Then render ELK JSON → SVG using the diagrams skill's renderer:

```bash
# Single file
node <diagrams-skill-dir>/scripts/render-elk.mjs diagram.json output.svg

# Batch: all .json files in a folder → svg/ subfolder
node <diagrams-skill-dir>/scripts/render-elk.mjs --dir <folder>

# Batch + PNG (macOS only)
node <diagrams-skill-dir>/scripts/render-elk.mjs --dir <folder> --png
```

Replace `<diagrams-skill-dir>` with the path to the installed diagrams skill directory.

> **Note:** elkjs must be installed locally where you run the script. See the diagrams skill's SKILL.md for full setup.

**Workflow for each diagram:**
1. Write the ELK JSON to a `.json` file in the research folder
2. Render: `node <diagrams-skill-dir>/scripts/render-elk.mjs diagram.json diagram.svg`
3. Embed in the markdown doc: `![System Overview](system-overview.svg)`
4. Keep both the `.json` (source of truth) and `.svg` (rendered) in the research folder

#### Tips
- Use `elk.algorithm: "layered"` for flow/dependency diagrams
- Use `elk.algorithm: "force"` for peer-relationship diagrams
- Group related nodes with compound nodes (children inside a parent)
- Label edges with the relationship (calls, imports, emits, reads, etc.)
- Keep node counts under ~20 per diagram — split into multiple if needed

### 5. Output

Create a research folder and markdown doc:

```
<output-dir>/<repo-slug>-architecture/
├── prompt.md          # Original question
├── architecture.md    # The deliverable
├── *.json             # ELK JSON source files (editable)
└── *.svg              # Rendered SVG diagrams (embedded in architecture.md)
```

Place output wherever makes sense for your workspace (e.g., a `research/` directory).

**architecture.md** format:

```markdown
# [Repo Name] — Architecture

**Repo:** <url>
**Researched:** <date>

## Overview
<1-2 paragraph summary of what this thing is and how it's built>

## System Diagram
![System Overview](system-overview.svg)
<Prose explanation>

## Data/Control Flow
<Pick a key operation, walk through it>
![Request Flow](request-flow.svg)

## Design Decisions

| Decision | Alternative | Rationale | Source |
|----------|------------|-----------|--------|
| ... | ... | ... | link or "inferred" |

## Key Abstractions
<The core types/interfaces/patterns that make the system tick>

## Sources
<Links to docs, posts, talks cited above>
```

### 6. Deliver

Send a brief summary (L2 — 75-150 words) in chat with key findings. Attach or link the full doc. Offer PDF export if wanted.

## Notes

- **Don't make stuff up.** If you can't find why a decision was made, say "inferred" or "no source found."
- **Excalidraw:** If the user asks for Excalidraw output instead of ELK, you can try, but ELK JSON is the default.
- **Mermaid fallback:** If the user's tooling can't render ELK, offer Mermaid as a fallback.
- **Scope control:** For large repos, focus on the architectural skeleton first. Offer to go deeper into specific subsystems on request.

