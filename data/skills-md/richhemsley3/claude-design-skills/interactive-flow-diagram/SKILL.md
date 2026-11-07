---
name: interactive-flow-diagram
description: "Build interactive user flow diagrams as standalone HTML files using D3.js. Use this skill whenever the user wants to create a visual user flow, interaction diagram, screen flow map, or workflow visualization. Also trigger when the user says 'flow diagram', 'interactive flow', 'user flow', 'flow chart', or asks to turn a flow/journey into something visual and explorable. This is distinct from static Mermaid diagrams — use this when the user wants a rich, interactive, browser-based visualization they can pan, scroll, and explore."
---

# Interactive User Flow Diagram Builder

Build horizontally-scrolling, single-canvas user flow diagrams as standalone HTML files powered by D3.js. All nodes render at full detail on one flat canvas — no multi-level zoom, no phase grouping.

## CRITICAL: Use the Complete Template Below

**Copy the FULL HTML template from the "Complete Template" section below.** Only modify the `flowData` object to match the user's flow. Do NOT restructure the rendering code, do NOT add phases/levels, do NOT change the node rendering functions.

## Node Types & Colors (from Figma reference)

| Type | Shape | Fill | Stroke | Text Color |
|------|-------|------|--------|------------|
| `start` | Stadium pill 272×106, rx=53 | `#40454A` | `#B8BCC0` | `#FFFFFF` (white) |
| `end` | Stadium pill 272×106, rx=53 | `#FCF5B1` | `#B29B24` | `#333333` |
| `process` | Rect 272×106, rx=6 | `#C1DDE3` | `#77B2C7` | `#333333` |
| `decision` | Diamond 120×120 (rotated rect) | `#E6E6E6` | `#B8B8B8` | `#333333` |
| `user-decision` | Circle r=50 | `#FFFFFF` | `#B8B8B8` | `#333333` |
| `error` | Rect 272×106, rx=6 | `#EEA79E` | `#DB7060` | `#333333` |
| `confirmation` | Rect 272×106, rx=6 | `#E2EDCC` | `#7A9A01` | `#333333` |
| `alt-flow` | Rect 272×106, rx=6 | `#C39DE3` | `#805AA1` | `#333333` |
| `note` | Square 160×160, no stroke | `#FFD966` | none | `#333333` |

All rectangular/pill nodes: 4px inside stroke. Canvas background: `#FAF8F5`.
Node labels: 20px Semi Bold (Inter). Decision text: 16px Medium.

## Choosing Node Types

- **start**: Entry point. One per flow. Dark background, white text.
- **end**: Terminal nodes. Yellow background. Can have multiple.
- **process**: Screens, pages, forms, actions. Blue-teal. Default type.
- **decision**: System checks (validation, auth, API). Diamond shape. "Yes/No" or "Pass/Fail".
- **user-decision**: User choices between paths. Circle shape.
- **error**: Error states, failures, blocked paths. Salmon/red.
- **confirmation**: Success screens, completion. Green.
- **alt-flow**: Alternative/optional paths. Purple.
- **note**: Annotations, not part of flow. Yellow sticky.

## Connectors

- **Default**: `#B8B8B8`, 2px, orthogonal right-angle paths
- **Happy path**: `#7A9A01`, 2.5px — primary user journey
- **Error path**: `#CF6253`, 2px, dashed (`6,4`)
- **Arrowheads**: Filled triangles via SVG `<marker>`, 10×7px
- **No port dots** — arrows touch node edges directly, zero gap
- **Edge labels**: 12px, `#666666`, white background pill

## Layout Rules

- Primary axis: left to right. Happy path = center row.
- Branches go down (errors) or up (alt flows) from decision nodes.
- Horizontal gap: 160px between nodes. Vertical gap: 160px between rows.
- Column width: 432px (272px node + 160px gap).
- Row height: 280px (106px node + ~160px gap + room for diamonds).

## Accepting User Input

Parse user content (markdown, bullets, Mermaid, verbal description) into the `flowData` format. For each step: identify type, connections, labels, happy path, and error/alt branches.

---

## Complete Template

**COPY THIS ENTIRE TEMPLATE.** Only change the `flowData` object and the `<title>` tag. Everything else works as-is.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>[Flow Name] — Interactive Flow</title>
  <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: #FAF8F5;
      color: #1C1A17;
      font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      overflow: hidden;
      width: 100vw;
      height: 100vh;
    }
    #header {
      position: fixed; top: 0; left: 0; right: 0;
      height: 48px;
      background: #FFFFFF;
      border-bottom: 1px solid #E0DCD3;
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 24px;
      z-index: 100;
      font-family: Inter, sans-serif;
    }
    #header .title {
      font-size: 15px; font-weight: 600; color: #1C1A17;
      text-transform: uppercase; letter-spacing: 0.5px;
    }
    #header .controls {
      display: flex; gap: 4px;
    }
    #header .controls button {
      width: 32px; height: 32px; border: 1px solid #E0DCD3;
      background: #FFFFFF; border-radius: 6px; cursor: pointer;
      font-size: 16px; color: #333; display: flex; align-items: center; justify-content: center;
    }
    #header .controls button:hover { background: #F5F3F0; }
    #flow-svg { display: block; }
    .node { cursor: pointer; }
    .node:hover rect, .node:hover circle { filter: brightness(0.97); }
    .node:hover { filter: drop-shadow(0 2px 8px rgba(0,0,0,0.1)); }

    /* Sidebar */
    #sidebar {
      position: fixed; top: 48px; right: -380px; bottom: 0; width: 380px;
      background: #FFFFFF; border-left: 1px solid #E0DCD3;
      z-index: 90; transition: right 0.3s ease;
      overflow-y: auto; padding: 32px 24px;
      font-family: Inter, sans-serif;
    }
    #sidebar.open { right: 0; }
    #sidebar .close-btn {
      position: absolute; top: 16px; right: 16px; width: 28px; height: 28px;
      border: none; background: none; cursor: pointer; font-size: 20px; color: #999;
    }
    #sidebar .close-btn:hover { color: #333; }
    #sidebar .node-type-badge {
      display: inline-block; padding: 3px 10px; border-radius: 12px;
      font-size: 11px; font-weight: 600; text-transform: uppercase;
      letter-spacing: 0.5px; margin-bottom: 12px;
    }
    #sidebar h2 { font-size: 20px; font-weight: 600; color: #1C1A17; margin-bottom: 20px; }
    #sidebar .section { margin-bottom: 20px; }
    #sidebar .section-label {
      font-size: 11px; font-weight: 600; text-transform: uppercase;
      letter-spacing: 0.5px; color: #999; margin-bottom: 6px;
    }
    #sidebar .section-content { font-size: 14px; color: #333; line-height: 1.6; }
    #sidebar .exit-list { list-style: none; padding: 0; }
    #sidebar .exit-list li {
      padding: 6px 0; border-bottom: 1px solid #F0EDE8;
      font-size: 13px; color: #333;
    }
    #sidebar .exit-list li strong { color: #013D5B; }

    /* Edge label pills */
    .edge-label-bg { fill: #FFFFFF; rx: 4; opacity: 0.95; }
    .edge-label-text { font-size: 12px; fill: #666666; font-family: Inter, sans-serif; }
  </style>
</head>
<body>
  <div id="header">
    <div class="title" id="flow-title"></div>
    <div class="controls">
      <button onclick="zoomIn()" title="Zoom in">+</button>
      <button onclick="zoomOut()" title="Zoom out">−</button>
      <button onclick="fitAll()" title="Fit all">⊡</button>
    </div>
  </div>
  <svg id="flow-svg"></svg>
  <div id="sidebar">
    <button class="close-btn" onclick="closeSidebar()">✕</button>
    <div id="sidebar-content"></div>
  </div>

<script>
// ═══════════════════════════════════════════════════════════════
//  FLOW DATA — MODIFY THIS SECTION ONLY
//  Change nodes[] and edges[] to match the user's flow.
//  Everything below this section renders automatically.
// ═══════════════════════════════════════════════════════════════
const flowData = {
  title: "Example Flow",
  nodes: [
    { id: "start", type: "start", label: "Start", description: "Entry point of the flow." },
    { id: "step1", type: "process", label: "Step 1", description: "First step in the process.", userAction: "User does something", edgeCases: ["Edge case 1"] },
    { id: "check", type: "decision", label: "Valid?", description: "System validates input." },
    { id: "step2", type: "process", label: "Step 2", description: "Continue on success." },
    { id: "error1", type: "error", label: "Error", description: "Validation failed." },
    { id: "end", type: "end", label: "Done", description: "Flow complete." }
  ],
  edges: [
    { from: "start", to: "step1", isHappyPath: true },
    { from: "step1", to: "check", isHappyPath: true },
    { from: "check", to: "step2", label: "Yes", isHappyPath: true },
    { from: "check", to: "error1", label: "No", isError: true },
    { from: "error1", to: "step1", label: "Retry" },
    { from: "step2", to: "end", isHappyPath: true }
  ]
};

// ═══════════════════════════════════════════════════════════════
//  DO NOT MODIFY BELOW THIS LINE
//  Rendering engine — handles layout, drawing, interactions.
// ═══════════════════════════════════════════════════════════════

// ─── Node style definitions ───
const NODE_STYLES = {
  'start':         { fill: '#40454A', stroke: '#B8BCC0', textColor: '#FFFFFF' },
  'end':           { fill: '#FCF5B1', stroke: '#B29B24', textColor: '#333333' },
  'process':       { fill: '#C1DDE3', stroke: '#77B2C7', textColor: '#333333' },
  'decision':      { fill: '#E6E6E6', stroke: '#B8B8B8', textColor: '#333333' },
  'user-decision': { fill: '#FFFFFF', stroke: '#B8B8B8', textColor: '#333333' },
  'error':         { fill: '#EEA79E', stroke: '#DB7060', textColor: '#333333' },
  'confirmation':  { fill: '#E2EDCC', stroke: '#7A9A01', textColor: '#333333' },
  'alt-flow':      { fill: '#C39DE3', stroke: '#805AA1', textColor: '#333333' },
  'note':          { fill: '#FFD966', stroke: 'none',    textColor: '#333333' }
};

function getStyle(type) { return NODE_STYLES[type] || NODE_STYLES['process']; }

// ─── Node dimensions (from Figma reference) ───
const NODE_W = 272, NODE_H = 106, PILL_RX = 53, RECT_RX = 6;
const DIAMOND_SIZE = 85; // half-side length before rotation — gives ~120px visual diagonal
const CIRCLE_R = 50;
const NOTE_SIZE = 140;

function getNodeWidth(node) {
  if (node.type === 'decision') return DIAMOND_SIZE * 2 * 1.414; // rotated diagonal
  if (node.type === 'user-decision') return CIRCLE_R * 2;
  if (node.type === 'note') return NOTE_SIZE;
  return NODE_W;
}
function getNodeHeight(node) {
  if (node.type === 'decision') return DIAMOND_SIZE * 2 * 1.414; // rotated diagonal
  if (node.type === 'user-decision') return CIRCLE_R * 2;
  if (node.type === 'note') return NOTE_SIZE;
  return NODE_H;
}

// ─── Layout algorithm ───
const COL_GAP = 160, ROW_GAP = 160;
const COL_W = NODE_W + COL_GAP; // 432
const ROW_H = NODE_H + ROW_GAP; // 266

function layoutNodes(nodes, edges) {
  // Build adjacency from edges
  const adj = {};
  const inDegree = {};
  nodes.forEach(n => { adj[n.id] = []; inDegree[n.id] = 0; });
  edges.forEach(e => {
    adj[e.from] = adj[e.from] || [];
    adj[e.from].push(e);
    inDegree[e.to] = (inDegree[e.to] || 0) + 1;
  });

  // Find start node
  let startNode = nodes.find(n => n.type === 'start');
  if (!startNode) startNode = nodes.find(n => inDegree[n.id] === 0) || nodes[0];

  // BFS to assign columns and rows
  const visited = new Set();
  const queue = [{ id: startNode.id, col: 0, row: 0 }];
  const positions = {};
  const colUsed = {}; // track which rows are used per column

  while (queue.length > 0) {
    const { id, col, row } = queue.shift();
    if (visited.has(id)) continue;
    visited.add(id);
    positions[id] = { col, row };

    // Track column usage
    if (!colUsed[col]) colUsed[col] = new Set();
    colUsed[col].add(row);

    const outEdges = adj[id] || [];
    // Sort: happy path first, then normal, then error
    const sorted = [...outEdges].sort((a, b) => {
      if (a.isHappyPath && !b.isHappyPath) return -1;
      if (!a.isHappyPath && b.isHappyPath) return 1;
      if (a.isError && !b.isError) return 1;
      if (!a.isError && b.isError) return -1;
      return 0;
    });

    let branchOffset = 1;
    sorted.forEach((edge, i) => {
      if (visited.has(edge.to)) return;
      if (i === 0 && (edge.isHappyPath || sorted.length === 1)) {
        // Happy path or only path — same row, next column
        queue.push({ id: edge.to, col: col + 1, row: row });
      } else {
        // Branch — offset row. Errors go down, alt goes up.
        const dir = edge.isError ? 1 : (edge.isAltFlow ? -1 : branchOffset);
        queue.push({ id: edge.to, col: col + 1, row: row + dir });
        branchOffset++;
      }
    });
  }

  // Handle unvisited nodes (disconnected)
  let maxCol = 0;
  Object.values(positions).forEach(p => { if (p.col > maxCol) maxCol = p.col; });
  nodes.forEach(n => {
    if (!visited.has(n.id)) {
      maxCol++;
      positions[n.id] = { col: maxCol, row: 0 };
    }
  });

  // Convert grid positions to pixel coordinates
  const START_X = 200;
  const CENTER_Y = 400;
  nodes.forEach(n => {
    const pos = positions[n.id];
    n.col = pos.col;
    n.row = pos.row;
    n.x = START_X + pos.col * COL_W;
    n.y = CENTER_Y + pos.row * ROW_H;
  });
}

// ─── Edge center for connector attachment ───
function getEdgePoint(node, side) {
  const w = getNodeWidth(node);
  const h = getNodeHeight(node);
  switch (side) {
    case 'right':  return { x: node.x + w / 2, y: node.y };
    case 'left':   return { x: node.x - w / 2, y: node.y };
    case 'bottom': return { x: node.x, y: node.y + h / 2 };
    case 'top':    return { x: node.x, y: node.y - h / 2 };
  }
}

// ─── Build orthogonal path ───
function buildPath(srcNode, tgtNode) {
  const sameRow = Math.abs(srcNode.y - tgtNode.y) < 10;
  const goingRight = tgtNode.x > srcNode.x;

  if (sameRow && goingRight) {
    // Straight horizontal line
    const src = getEdgePoint(srcNode, 'right');
    const tgt = getEdgePoint(tgtNode, 'left');
    return `M${src.x},${src.y} L${tgt.x},${tgt.y}`;
  }

  if (goingRight) {
    // Different row, going right — exit right, bend, enter left
    const src = getEdgePoint(srcNode, 'right');
    const tgt = getEdgePoint(tgtNode, 'left');
    const midX = src.x + COL_GAP * 0.4;
    return `M${src.x},${src.y} H${midX} V${tgt.y} H${tgt.x}`;
  }

  // Going LEFT (loop back) — route cleanly around the bottom
  const src = getEdgePoint(srcNode, 'bottom');
  const tgt = getEdgePoint(tgtNode, 'bottom');
  const loopY = Math.max(src.y, tgt.y) + ROW_GAP * 0.6;
  return `M${src.x},${src.y} V${loopY} H${tgt.x} V${tgt.y}`;
}

// ─── Rendering ───
const width = window.innerWidth;
const height = window.innerHeight - 48;

document.getElementById('flow-title').textContent = flowData.title;

const svg = d3.select('#flow-svg')
  .attr('width', width)
  .attr('height', height)
  .style('background', '#FAF8F5')
  .style('margin-top', '48px');

const defs = svg.append('defs');

// Arrowhead markers
function addMarker(id, color) {
  defs.append('marker')
    .attr('id', id)
    .attr('viewBox', '0 0 10 7')
    .attr('refX', 10).attr('refY', 3.5)
    .attr('markerWidth', 10).attr('markerHeight', 7)
    .attr('orient', 'auto')
    .append('path')
    .attr('d', 'M0,0 L10,3.5 L0,7 Z')
    .attr('fill', color);
}
addMarker('arrow-default', '#B8B8B8');
addMarker('arrow-happy', '#7A9A01');
addMarker('arrow-error', '#CF6253');

const container = svg.append('g').attr('class', 'canvas-container');

// Zoom
const zoomBehavior = d3.zoom()
  .scaleExtent([0.15, 3])
  .on('zoom', (event) => container.attr('transform', event.transform));
svg.call(zoomBehavior);

// Zoom controls
window.zoomIn = () => svg.transition().duration(300).call(zoomBehavior.scaleBy, 1.3);
window.zoomOut = () => svg.transition().duration(300).call(zoomBehavior.scaleBy, 0.75);
window.fitAll = () => fitToContent();

// ─── Layout ───
layoutNodes(flowData.nodes, flowData.edges);

// Build node lookup
const nodeMap = {};
flowData.nodes.forEach(n => nodeMap[n.id] = n);

// ─── Draw edges ───
const edgesGroup = container.append('g').attr('class', 'edges');

flowData.edges.forEach(edge => {
  const src = nodeMap[edge.from];
  const tgt = nodeMap[edge.to];
  if (!src || !tgt) return;

  const isHappy = edge.isHappyPath;
  const isErr = edge.isError;
  const color = isHappy ? '#7A9A01' : (isErr ? '#CF6253' : '#B8B8B8');
  const strokeW = isHappy ? 2.5 : 2;
  const marker = isHappy ? 'url(#arrow-happy)' : (isErr ? 'url(#arrow-error)' : 'url(#arrow-default)');
  const dashArray = isErr ? '6,4' : 'none';

  const path = buildPath(src, tgt);

  edgesGroup.append('path')
    .attr('d', path)
    .attr('fill', 'none')
    .attr('stroke', color)
    .attr('stroke-width', strokeW)
    .attr('stroke-dasharray', dashArray)
    .attr('marker-end', marker);

  // Edge label
  if (edge.label) {
    const midX = (src.x + tgt.x) / 2;
    const midY = (src.y + tgt.y) / 2;
    // Offset labels above horizontal lines, beside vertical segments
    const offsetY = Math.abs(src.y - tgt.y) < 10 ? -16 : 0;
    const offsetX = Math.abs(src.y - tgt.y) < 10 ? 0 : 14;

    const labelG = edgesGroup.append('g')
      .attr('transform', `translate(${midX + offsetX}, ${midY + offsetY})`);

    labelG.append('rect')
      .attr('class', 'edge-label-bg')
      .attr('x', -24).attr('y', -12)
      .attr('width', 48).attr('height', 24)
      .attr('rx', 12)
      .attr('fill', '#FFFFFF')
      .attr('stroke', '#E0DCD3')
      .attr('stroke-width', 1);

    labelG.append('text')
      .attr('class', 'edge-label-text')
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .attr('font-size', '13px')
      .attr('font-weight', '500')
      .attr('fill', '#555555')
      .text(edge.label);

    // Auto-size background to text
    const textNode = labelG.select('text').node();
    if (textNode) {
      const bbox = textNode.getBBox();
      labelG.select('rect')
        .attr('x', bbox.x - 10)
        .attr('y', bbox.y - 5)
        .attr('width', bbox.width + 20)
        .attr('height', bbox.height + 10);
    }
  }
});

// ─── Draw nodes ───
const nodesGroup = container.append('g').attr('class', 'nodes');

flowData.nodes.forEach(node => {
  const style = getStyle(node.type);
  const g = nodesGroup.append('g')
    .attr('class', `node node-${node.type}`)
    .attr('transform', `translate(${node.x}, ${node.y})`)
    .style('cursor', 'pointer')
    .on('click', () => showSidebar(node));

  if (node.type === 'decision') {
    // Diamond — rotated rect. DIAMOND_SIZE = half side length
    g.append('rect')
      .attr('x', -DIAMOND_SIZE).attr('y', -DIAMOND_SIZE)
      .attr('width', DIAMOND_SIZE * 2).attr('height', DIAMOND_SIZE * 2)
      .attr('rx', 6)
      .attr('fill', style.fill)
      .attr('stroke', style.stroke)
      .attr('stroke-width', 4)
      .attr('transform', 'rotate(45)');
    // Text NOT rotated — wrap if needed
    const words = node.label.split(/\s+/);
    if (words.length <= 2) {
      g.append('text')
        .attr('text-anchor', 'middle')
        .attr('dy', '0.35em')
        .attr('fill', style.textColor)
        .attr('font-size', '16px')
        .attr('font-weight', '500')
        .text(node.label);
    } else {
      // Multi-line for longer labels
      const mid = Math.ceil(words.length / 2);
      g.append('text').attr('text-anchor', 'middle').attr('dy', '-0.3em')
        .attr('fill', style.textColor).attr('font-size', '15px').attr('font-weight', '500')
        .text(words.slice(0, mid).join(' '));
      g.append('text').attr('text-anchor', 'middle').attr('dy', '1.1em')
        .attr('fill', style.textColor).attr('font-size', '15px').attr('font-weight', '500')
        .text(words.slice(mid).join(' '));
    }

  } else if (node.type === 'user-decision') {
    // Circle
    g.append('circle')
      .attr('r', CIRCLE_R)
      .attr('fill', style.fill)
      .attr('stroke', style.stroke)
      .attr('stroke-width', 4);
    g.append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .attr('fill', style.textColor)
      .attr('font-size', '16px')
      .attr('font-weight', '500')
      .text(node.label);

  } else if (node.type === 'start' || node.type === 'end') {
    // Stadium pill
    g.append('rect')
      .attr('x', -NODE_W / 2).attr('y', -NODE_H / 2)
      .attr('width', NODE_W).attr('height', NODE_H)
      .attr('rx', PILL_RX)
      .attr('fill', style.fill)
      .attr('stroke', style.stroke)
      .attr('stroke-width', 4);
    g.append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .attr('fill', style.textColor)
      .attr('font-size', '20px')
      .attr('font-weight', '600')
      .text(node.label);

  } else if (node.type === 'note') {
    // Yellow sticky note
    g.append('rect')
      .attr('x', -NOTE_SIZE / 2).attr('y', -NOTE_SIZE / 2)
      .attr('width', NOTE_SIZE).attr('height', NOTE_SIZE)
      .attr('fill', style.fill);
    g.append('text')
      .attr('x', -NOTE_SIZE / 2 + 12).attr('y', -NOTE_SIZE / 2 + 20)
      .attr('fill', style.textColor)
      .attr('font-size', '11px')
      .attr('font-weight', '600')
      .text('NOTE');
    // Wrap body text
    const words = (node.label || '').split(' ');
    let line = '', lineNum = 0;
    words.forEach(word => {
      const test = line ? line + ' ' + word : word;
      if (test.length > 18) {
        g.append('text')
          .attr('x', -NOTE_SIZE / 2 + 12)
          .attr('y', -NOTE_SIZE / 2 + 40 + lineNum * 16)
          .attr('fill', style.textColor)
          .attr('font-size', '12px')
          .text(line);
        line = word;
        lineNum++;
      } else {
        line = test;
      }
    });
    if (line) {
      g.append('text')
        .attr('x', -NOTE_SIZE / 2 + 12)
        .attr('y', -NOTE_SIZE / 2 + 40 + lineNum * 16)
        .attr('fill', style.textColor)
        .attr('font-size', '12px')
        .text(line);
    }

  } else {
    // Default rectangle: process, error, confirmation, alt-flow
    g.append('rect')
      .attr('x', -NODE_W / 2).attr('y', -NODE_H / 2)
      .attr('width', NODE_W).attr('height', NODE_H)
      .attr('rx', RECT_RX)
      .attr('fill', style.fill)
      .attr('stroke', style.stroke)
      .attr('stroke-width', 4);
    g.append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .attr('fill', style.textColor)
      .attr('font-size', '20px')
      .attr('font-weight', '500')
      .text(node.label);
  }

  // Hover effect
  g.on('mouseenter', function() {
    d3.select(this).select('rect, circle').transition().duration(150)
      .attr('stroke-width', 5);
  }).on('mouseleave', function() {
    d3.select(this).select('rect, circle').transition().duration(150)
      .attr('stroke-width', 4);
  });
});

// ─── Sidebar ───
const sidebar = document.getElementById('sidebar');
const sidebarContent = document.getElementById('sidebar-content');

function showSidebar(node) {
  const style = getStyle(node.type);
  const typeName = node.type.replace('-', ' ').replace(/\b\w/g, c => c.toUpperCase());

  let html = `<div class="node-type-badge" style="background:${style.fill};color:${style.textColor};border:1px solid ${style.stroke}">${typeName}</div>`;
  html += `<h2>${node.label}</h2>`;

  if (node.description) {
    html += `<div class="section"><div class="section-label">Description</div><div class="section-content">${node.description}</div></div>`;
  }
  if (node.userAction) {
    html += `<div class="section"><div class="section-label">User Action</div><div class="section-content">${node.userAction}</div></div>`;
  }
  if (node.edgeCases && node.edgeCases.length) {
    html += `<div class="section"><div class="section-label">Edge Cases</div><ul class="exit-list">${node.edgeCases.map(e => `<li>${e}</li>`).join('')}</ul></div>`;
  }

  // Show exits
  const exits = flowData.edges.filter(e => e.from === node.id);
  if (exits.length) {
    html += `<div class="section"><div class="section-label">Exits</div><ul class="exit-list">`;
    exits.forEach(e => {
      const tgt = nodeMap[e.to];
      html += `<li>${e.label ? `<strong>${e.label}</strong> → ` : '→ '}${tgt ? tgt.label : e.to}</li>`;
    });
    html += `</ul></div>`;
  }

  sidebarContent.innerHTML = html;
  sidebar.classList.add('open');
}

window.closeSidebar = () => sidebar.classList.remove('open');

// Click empty canvas to close sidebar
svg.on('click', (event) => {
  if (event.target === svg.node()) closeSidebar();
});

// ─── Fit to content on load ───
function fitToContent() {
  const bounds = container.node().getBBox();
  if (bounds.width === 0 || bounds.height === 0) return;
  const pad = 100;
  const bw = bounds.width + pad * 2;
  const bh = bounds.height + pad * 2;
  const scale = Math.min(width / bw, height / bh, 1.2);
  const tx = (width - bounds.width * scale) / 2 - bounds.x * scale;
  const ty = (height - bounds.height * scale) / 2 - bounds.y * scale;
  svg.transition().duration(600)
    .call(zoomBehavior.transform, d3.zoomIdentity.translate(tx, ty).scale(scale));
}

// Initial fit after a small delay to let fonts load
setTimeout(fitToContent, 100);

</script>
</body>
</html>
```

## Iteration Prompts

| User says | What to do |
|-----------|-----------|
| "add edge labels" | Add `label` property to edges in `flowData` |
| "highlight the happy path" | Set `isHappyPath: true` on primary journey edges |
| "add error handling" | Add error nodes + edges with `isError: true` |
| "add a note" | Add a node with `type: "note"` |
| "add [step]" | Add to `flowData.nodes[]` and `flowData.edges[]` |
