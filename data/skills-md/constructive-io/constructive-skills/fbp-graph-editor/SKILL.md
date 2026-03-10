---
name: fbp-graph-editor
description: Houdini-inspired graph editor for Flow-Based Programming built with React. Use when building or customizing a visual graph editor, working with the @fbp/graph-editor package.
---

Houdini-inspired graph editor for Flow-Based Programming built with React.

## Installation

```bash
pnpm add @fbp/graph-editor
```

## Overview

`@fbp/graph-editor` is a React component for visual editing of FBP graphs. It features an SVG-based canvas with pan/zoom, node rendering with fully-qualified type paths, Bezier edge connections, selection system, properties panel, and subgraph navigation.

## Basic Usage

```tsx
import { GraphEditor } from '@fbp/graph-editor';
import type { Graph, NodeDefinition } from '@fbp/types';

const graph: Graph = {
  name: 'my-graph',
  definitions: [
    {
      context: 'js',
      category: 'math',
      type: 'js/math/add',
      inputs: [
        { name: 'a', type: 'number' },
        { name: 'b', type: 'number' }
      ],
      outputs: [
        { name: 'sum', type: 'number' }
      ]
    }
  ],
  nodes: [
    { name: 'add1', type: 'js/math/add', meta: { x: 100, y: 100 } }
  ],
  edges: []
};

function App() {
  return (
    <div className="h-screen">
      <GraphEditor graph={graph} />
    </div>
  );
}
```

## Features

### SVG-Based Canvas

The editor uses SVG for rendering, providing crisp visuals at any zoom level. Pan and zoom are supported via mouse/trackpad gestures.

### Node Rendering

Nodes display their fully-qualified type paths (e.g., `js/math/add`) and show input/output ports based on their definition.

### Bezier Edge Connections

Edges are rendered as smooth Bezier curves connecting output ports to input ports. Click and drag from a port to create new connections.

### Selection System

- Click to select a single node
- Shift+click to add/remove from selection
- Box select with Shift+drag
- Cmd/Ctrl+A to select all
- Escape to clear selection
- Cmd/Ctrl+D to duplicate selection

### Properties Panel

Auto-generated from `PropDefinition`. When a node is selected, its properties are displayed in a panel for editing.

### Subgraph Navigation

- Enter to dive into a selected subnet
- U to go up from a subnet

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Delete/Backspace | Delete selected nodes/edges |
| Cmd/Ctrl+D | Duplicate selection |
| Cmd/Ctrl+A | Select all |
| Escape | Clear selection |
| Enter | Dive into selected subnet |
| U | Go up from subnet |
| Shift+Drag | Box select |
| Alt+Drag or Middle Mouse | Pan canvas |
| Ctrl/Cmd+Scroll | Zoom |

## Channel Reference Detection

The editor detects channel references in property values using patterns like `ch("...")` and `$VAR`, enabling visual feedback for connected parameters.

## Styling

The editor uses Tailwind CSS for styling. Ensure your project has Tailwind configured:

```tsx
// tailwind.config.js
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx}',
    './node_modules/@fbp/graph-editor/**/*.{js,ts,jsx,tsx}'
  ],
  // ...
};
```

## Props

```typescript
interface GraphEditorProps {
  graph: Graph;
  onChange?: (graph: Graph) => void;
  definitions?: NodeDefinition[];
  readOnly?: boolean;
}
```

| Prop | Type | Description |
|------|------|-------------|
| `graph` | `Graph` | The graph to display and edit |
| `onChange` | `(graph: Graph) => void` | Callback when graph changes |
| `definitions` | `NodeDefinition[]` | Additional node type definitions |
| `readOnly` | `boolean` | Disable editing |

## Peer Dependencies

```json
{
  "peerDependencies": {
    "react": ">=18.0.0",
    "react-dom": ">=18.0.0"
  }
}
```

## Example: Complete Editor Setup

```tsx
import { useState } from 'react';
import { GraphEditor } from '@fbp/graph-editor';
import type { Graph } from '@fbp/types';

const initialGraph: Graph = {
  name: 'calculator',
  definitions: [
    {
      type: 'js/const/number',
      context: 'js',
      category: 'const',
      props: [{ name: 'value', type: 'number', default: 0 }],
      outputs: [{ name: 'value', type: 'number' }]
    },
    {
      type: 'js/math/add',
      context: 'js',
      category: 'math',
      inputs: [
        { name: 'a', type: 'number' },
        { name: 'b', type: 'number' }
      ],
      outputs: [{ name: 'sum', type: 'number' }]
    }
  ],
  nodes: [
    { name: 'num1', type: 'js/const/number', meta: { x: 50, y: 50 }, props: [{ name: 'value', value: 5 }] },
    { name: 'num2', type: 'js/const/number', meta: { x: 50, y: 150 }, props: [{ name: 'value', value: 3 }] },
    { name: 'add', type: 'js/math/add', meta: { x: 250, y: 100 } }
  ],
  edges: [
    { src: { node: 'num1', port: 'value' }, dst: { node: 'add', port: 'a' } },
    { src: { node: 'num2', port: 'value' }, dst: { node: 'add', port: 'b' } }
  ]
};

function App() {
  const [graph, setGraph] = useState(initialGraph);

  return (
    <div className="h-screen flex flex-col">
      <header className="p-4 border-b">
        <h1 className="text-xl font-bold">{graph.name}</h1>
      </header>
      <main className="flex-1">
        <GraphEditor 
          graph={graph} 
          onChange={setGraph}
        />
      </main>
    </div>
  );
}
```
