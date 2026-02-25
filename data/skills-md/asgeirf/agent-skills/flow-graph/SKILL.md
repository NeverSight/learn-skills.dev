---
name: flow-graph
description: Generate animated GIF/WebM videos of graph visualizations from natural language descriptions
triggers:
  - animated graph
  - flow diagram
  - process visualization
  - graph GIF
  - graph video
  - flow chart animation
  - graph animation
---

# Flow Graph Skill

Generate graph visualizations rendered as GIF and WebM video files with animated traffic flowing along edges. You describe a process or graph in natural language, then this skill produces a video of the diagram.

## Workflow

### 1. Understand the Request

Parse the user's description to identify:
- **Nodes** — entities, states, steps, or concepts
- **Edges** — relationships, transitions, data flows
- **Layout** — flowchart (top-down), pipeline (left-right), state machine (radial), etc.
- **Mode** — static with traffic (default) or step-by-step build-up (only if user explicitly asks)

### 2. Generate Graph JSON

Create a `graph-data.json` file. **Default to static mode** — define all nodes and edges upfront. The engine renders the complete graph immediately with animated traffic flowing along edges.

**Static mode** (default — use this unless asked for build-up animation):

```json
{
  "settings": {
    "width": 1280, "height": 720,
    "background": "#1a1a2e",
    "duration": 5000,
    "traffic": true
  },
  "nodes": [
    { "id": "a", "label": "Start", "position": [400, 50] },
    { "id": "b", "label": "Process", "position": [400, 200] },
    { "id": "c", "label": "End", "position": [400, 350] }
  ],
  "edges": [
    { "id": "e1", "source": "a", "target": "b" },
    { "id": "e2", "source": "b", "target": "c" }
  ]
}
```

**Step mode** (advanced — only when user asks for build-up sequences):

```json
{
  "settings": {
    "width": 1280, "height": 720,
    "background": "#1a1a2e",
    "animationDuration": 500,
    "fitViewOnComplete": true
  },
  "steps": [
    { "type": "addNode", "node": { "id": "1", "label": "Start", "position": [200, 100] }, "delay": 600 },
    { "type": "addEdge", "edge": { "id": "e1-2", "source": "1", "target": "2", "animated": true }, "delay": 400 },
    { "type": "highlight", "ids": ["1"], "color": "#e94560", "delay": 800 },
    { "type": "fitView", "padding": 0.2, "delay": 500 },
    { "type": "wait", "delay": 1500 }
  ]
}
```

**Step types:** `addNode`, `addEdge`, `highlight`, `moveNode`, `removeNode`, `removeEdge`, `updateStyle`, `fitView`, `zoom`, `pan`, `wait`

See [references/graph-schema.md](references/graph-schema.md) for full details on both modes.

### 3. Write the JSON File

Write the graph JSON to a temporary file, e.g. `/tmp/my-graph.json`.

### 4. Setup (first run only)

Install the skill's dependencies if not yet done:

```bash
cd <skill-dir> && npm install --prefer-offline --no-audit --no-fund
cd <skill-dir>/assets/flow-template && npm install --prefer-offline --no-audit --no-fund
npx playwright install chromium
```

Where `<skill-dir>` is the directory containing this SKILL.md file.

### 5. Record the Animation

Run the recording script:

```bash
node <skill-dir>/scripts/record.mjs /tmp/my-graph.json ./output --format both
```

This will produce `output.webm` and `output.gif` in the current directory.

## Layout Patterns

**Top-down flowchart** — Increment Y by ~150 per row, center X:
```json
{ "id": "a", "label": "Step 1", "position": [400, 50] }
{ "id": "b", "label": "Step 2", "position": [400, 200] }
```

**Left-to-right pipeline** — Increment X by ~200, same Y:
```json
{ "id": "src", "label": "Source", "position": [50, 150] }
{ "id": "dst", "label": "Dest",   "position": [250, 150] }
```

**Branching / decision** — Fork at the decision node with different X offsets:
```json
{ "id": "decide", "position": [400, 300] }
{ "id": "yes",    "position": [250, 450] }
{ "id": "no",     "position": [550, 450] }
```

## Recording Options

```
node record.mjs <graph-data.json> <output-path> [options]

Options:
  --format gif|webm|both   Output format (default: both)
  --width  <number>        Viewport width override
  --height <number>        Viewport height override
```

The script handles everything: copies the template to a temp directory, injects the graph data, starts a Vite dev server, records with Playwright, converts via ffmpeg, and cleans up.

## Design Tips

### Static mode (default)
- Set `duration` to 4000-6000ms for a good looping clip
- Traffic animation flows automatically on all edges — no per-edge config needed
- Set `"traffic": false` in settings if you want a still diagram
- Style key nodes with colored backgrounds or borders to show roles (source, sink, decision)
- Use edge `label` to annotate relationships

### Step mode (build-up animation)
- Use `delay: 400-800` for node/edge additions (fast enough to be engaging, slow enough to follow)
- Add a `highlight` step after key nodes appear to draw attention
- End with `fitView` + `wait` to show the complete graph for 1-2 seconds
- Use `animated: true` on edges to show data flow direction
- Style decision nodes with `borderRadius: "50%"` for diamond/circle shapes
- Keep total animation under 15 seconds for best GIF file size

## Prerequisites

- **Node.js** 20+
- **ffmpeg** (for GIF conversion) — `brew install ffmpeg`
- **Playwright** browsers — `npx playwright install chromium`
