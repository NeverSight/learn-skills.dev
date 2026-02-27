---
name: svelte-flow
description: Build node-based editors, interactive diagrams, and flow visualizations using Svelte Flow. Use when creating workflow editors, data flow diagrams, organizational charts, mindmaps, process visualizations, DAG editors, or any interactive node-graph UI. Supports custom nodes/edges, layouts (dagre, hierarchical), animations, and advanced features like proximity connect, floating edges, and contextual zoom.
keywords: [svelte-flow, visualization, nodes, graph-editor, diagrams, interactive-ui]
---

# Svelte Flow

Expert guide for building node-based UIs with Svelte Flow (@xyflow/svelte).

## Installation

```bash
npm install @xyflow/svelte
```

## Core Setup

```svelte
<script lang="ts">
  import { SvelteFlow, Background } from '@xyflow/svelte';
  import '@xyflow/svelte/dist/style.css';
  
  // Use $state.raw for nodes and edges (Svelte 5)
  let nodes = $state.raw([
    { id: '1', data: { label: 'Node 1' }, position: { x: 0, y: 0 } },
    { id: '2', data: { label: 'Node 2' }, position: { x: 0, y: 100 } }
  ]);
  
  let edges = $state.raw([
    { id: 'e1-2', source: '1', target: '2' }
  ]);
</script>

<SvelteFlow bind:nodes bind:edges fitView>
  <Background />
</SvelteFlow>
```

## Key Concepts

### Nodes

Each node requires:
- `id`: Unique identifier
- `position`: `{ x: number, y: number }`
- `data`: Object with custom properties (typically includes `label`)
- Optional: `type`, `style`, `hidden`, `width`, `height`, `sourcePosition`, `targetPosition`

```typescript
const node = {
  id: '1',
  type: 'custom',
  position: { x: 100, y: 100 },
  data: { label: 'My Node', color: '#ff0000' },
  style: 'background: #f0f0f0',
  width: 150,
  height: 100
};
```

### Edges

Each edge requires:
- `id`: Unique identifier
- `source`: Source node ID
- `target`: Target node ID
- Optional: `type`, `label`, `animated`, `markerEnd`, `markerStart`, `style`, `hidden`

```typescript
const edge = {
  id: 'e1-2',
  source: '1',
  target: '2',
  type: 'smoothstep',
  label: 'connects to',
  animated: true,
  markerEnd: { type: MarkerType.ArrowClosed }
};
```

### Built-in Types

**Edge Types:**
- `default`: Straight line
- `smoothstep`: Smooth 90-degree turns
- `step`: Hard 90-degree turns
- `straight`: Alias for default
- `bezier`: Curved bezier line

**Node Types:**
- `default`: Basic rectangle node
- `input`: Node with only source handles
- `output`: Node with only target handles

## Custom Nodes

```svelte
<!-- CustomNode.svelte -->
<script lang="ts" module>
  import type { Node, NodeProps } from '@xyflow/svelte';
  
  export type CustomNodeType = Node<{
    label: string;
    color?: string;
  }>;
</script>

<script lang="ts">
  import { Handle, Position } from '@xyflow/svelte';
  
  let { data }: NodeProps<CustomNodeType> = $props();
</script>

<div class="custom-node" style:background={data.color}>
  <Handle type="target" position={Position.Left} />
  <div>{data.label}</div>
  <Handle type="source" position={Position.Right} />
</div>

<style>
  .custom-node {
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ddd;
  }
</style>
```

Register custom nodes:

```svelte
<script lang="ts">
  import CustomNode from './CustomNode.svelte';
  
  const nodeTypes = {
    custom: CustomNode
  };
  
  let nodes = $state.raw([
    { id: '1', type: 'custom', data: { label: 'Custom', color: '#ff7000' }, position: { x: 0, y: 0 } }
  ]);
</script>

<SvelteFlow bind:nodes {nodeTypes} bind:edges fitView />
```

## Custom Edges

```svelte
<!-- CustomEdge.svelte -->
<script lang="ts">
  import { BaseEdge, EdgeLabel, getStraightPath, type EdgeProps } from '@xyflow/svelte';
  
  let { id, sourceX, sourceY, targetX, targetY, label }: EdgeProps = $props();
  
  let [edgePath, labelX, labelY] = $derived(
    getStraightPath({ sourceX, sourceY, targetX, targetY })
  );
</script>

<BaseEdge {id} path={edgePath} />
{#if label}
  <EdgeLabel x={labelX} y={labelY}>
    <div class="edge-label">{label}</div>
  </EdgeLabel>
{/if}
```

Path helpers available:
- `getStraightPath()`
- `getBezierPath()`
- `getSmoothStepPath()`

Register custom edges:

```svelte
<script lang="ts">
  const edgeTypes = {
    custom: CustomEdge
  };
</script>

<SvelteFlow bind:nodes bind:edges {edgeTypes} fitView />
```

## Updating State

**Critical:** Nodes and edges are immutable. Create new objects to trigger updates.

```svelte
<script lang="ts">
  // ❌ Won't work - direct mutation
  nodes[0].position.x = 100;
  
  // ✅ Works - create new array
  nodes = nodes.map((node) => {
    if (node.id === '1') {
      return { ...node, position: { ...node.position, x: 100 } };
    }
    return node;
  });
  
  // ✅ Also works - using helper from useSvelteFlow
  import { useSvelteFlow } from '@xyflow/svelte';
  const { updateNode } = useSvelteFlow();
  
  updateNode('1', (node) => ({
    ...node,
    position: { ...node.position, x: 100 }
  }));
</script>
```

## Event Handling

Common event handlers:

```svelte
<SvelteFlow
  bind:nodes
  bind:edges
  onnodeclick={(event) => console.log('node clicked', event.targetNode)}
  onnodedrag={(event) => console.log('node dragging', event.targetNode)}
  onnodedragstop={(event) => console.log('drag ended', event.targetNode)}
  onedgeclick={(event) => console.log('edge clicked', event.edge)}
  onconnect={(params) => {
    edges = [...edges, { id: `e${params.source}-${params.target}`, ...params }];
  }}
/>
```

Available events:
- `onnodeclick`, `onnodedoubleclick`
- `onnodedrag`, `onnodedragstart`, `onnodedragstop`
- `onedgeclick`, `onedgedoubleclick`
- `onconnect`, `onconnectstart`, `onconnectend`
- `onbeforedelete` (async, can prevent deletion)
- `oninit`, `onmove`, `onmovestart`, `onmoveend`

## Layout Algorithms

### Dagre (Hierarchical)

```typescript
import dagre from '@dagrejs/dagre';
import { Position } from '@xyflow/svelte';

function getLayoutedElements(nodes: Node[], edges: Edge[], direction = 'TB') {
  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));
  
  const isHorizontal = direction === 'LR';
  dagreGraph.setGraph({ rankdir: direction });
  
  const nodeWidth = 172;
  const nodeHeight = 36;
  
  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
  });
  
  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });
  
  dagre.layout(dagreGraph);
  
  const layoutedNodes = nodes.map((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    return {
      ...node,
      targetPosition: isHorizontal ? Position.Left : Position.Top,
      sourcePosition: isHorizontal ? Position.Right : Position.Bottom,
      position: {
        x: nodeWithPosition.x - nodeWidth / 2,
        y: nodeWithPosition.y - nodeHeight / 2,
      },
    };
  });
  
  return { nodes: layoutedNodes, edges };
}
```

## Advanced Features

### Floating Edges

Edges that dynamically connect to the closest point on node boundaries:

```svelte
<!-- FloatingEdge.svelte -->
<script lang="ts">
  import { BaseEdge, getBezierPath, type EdgeProps } from '@xyflow/svelte';
  import { getEdgeParams } from './utils';
  
  let { id, source, target, markerEnd }: EdgeProps = $props();
  
  const { sx, sy, tx, ty, sourcePos, targetPos } = $derived(
    getEdgeParams(source, target)
  );
  
  let [edgePath] = $derived(
    getBezierPath({
      sourceX: sx,
      sourceY: sy,
      sourcePosition: sourcePos,
      targetX: tx,
      targetY: ty,
      targetPosition: targetPos,
    })
  );
</script>

<BaseEdge {id} path={edgePath} {markerEnd} />
```

Register with `ConnectionMode.Loose`:

```svelte
<script lang="ts">
  import { ConnectionMode } from '@xyflow/svelte';
</script>

<SvelteFlow
  bind:nodes
  bind:edges
  edgeTypes={{ floating: FloatingEdge }}
  connectionMode={ConnectionMode.Loose}
  fitView
/>
```

### Proximity Connect

Auto-connect nodes when dragged close together:

```svelte
<script lang="ts">
  const MIN_DISTANCE = 150;
  
  function getClosestEdge(node: Node, nodes: Node[]) {
    const closestNode = nodes.reduce(
      (res, n) => {
        if (n.id !== node.id) {
          const dx = n.position.x - node.position.x;
          const dy = n.position.y - node.position.y;
          const d = Math.sqrt(dx * dx + dy * dy);
          
          if (d < res.distance && d < MIN_DISTANCE) {
            res.distance = d;
            res.node = n;
          }
        }
        return res;
      },
      { distance: Number.MAX_VALUE, node: null }
    );
    
    if (!closestNode.node) return null;
    
    const closeNodeIsSource = closestNode.node.position.x < node.position.x;
    
    return {
      id: closeNodeIsSource
        ? `${node.id}-${closestNode.node.id}`
        : `${closestNode.node.id}-${node.id}`,
      source: closeNodeIsSource ? closestNode.node.id : node.id,
      target: closeNodeIsSource ? node.id : closestNode.node.id,
      class: 'temp',
    };
  }
  
  function onNodeDrag({ targetNode: node }) {
    const closestEdge = getClosestEdge(node, nodes);
    
    edges = edges.filter(e => e.class !== 'temp');
    
    if (closestEdge && !edges.some(e => e.source === closestEdge.source && e.target === closestEdge.target)) {
      edges = [...edges, closestEdge];
    }
  }
  
  function onNodeDragStop() {
    edges = edges.map((edge) => 
      edge.class === 'temp' ? { ...edge, class: '' } : edge
    );
  }
</script>

<SvelteFlow
  bind:nodes
  bind:edges
  onnodedrag={onNodeDrag}
  onnodedragstop={onNodeDragStop}
  fitView
/>
```

### Edge Reconnection

Allow users to drag edge endpoints to different nodes:

```svelte
<!-- ReconnectableEdge.svelte -->
<script lang="ts">
  import {
    BaseEdge,
    EdgeReconnectAnchor,
    getBezierPath,
    type EdgeProps
  } from '@xyflow/svelte';
  
  let { sourceX, sourceY, targetX, targetY, selected, ...props }: EdgeProps = $props();
  
  const [edgePath] = $derived(
    getBezierPath({ sourceX, sourceY, targetX, targetY })
  );
  
  let reconnecting = $state(false);
</script>

{#if !reconnecting}
  <BaseEdge path={edgePath} {...props} />
{/if}

{#if selected}
  <EdgeReconnectAnchor
    bind:reconnecting
    type="source"
    position={{ x: sourceX, y: sourceY }}
  />
  <EdgeReconnectAnchor
    bind:reconnecting
    type="target"
    position={{ x: targetX, y: targetY }}
  />
{/if}
```

### Delete Node and Reconnect Edges

```svelte
<script lang="ts">
  import { getIncomers, getOutgoers, getConnectedEdges, type OnBeforeDelete } from '@xyflow/svelte';
  
  const onbeforedelete: OnBeforeDelete = async ({ nodes: deletedNodes }) => {
    let remainingNodes = [...nodes];
    
    edges = deletedNodes.reduce((acc, node) => {
      const incomers = getIncomers(node, remainingNodes, acc);
      const outgoers = getOutgoers(node, remainingNodes, acc);
      const connectedEdges = getConnectedEdges([node], acc);
      
      const remainingEdges = acc.filter((edge) => !connectedEdges.includes(edge));
      
      const createdEdges = incomers.flatMap(({ id: source }) =>
        outgoers.map(({ id: target }) => ({
          id: `${source}->${target}`,
          source,
          target,
        }))
      );
      
      remainingNodes = remainingNodes.filter((rn) => rn.id !== node.id);
      
      return [...remainingEdges, ...createdEdges];
    }, edges);
    
    nodes = remainingNodes;
    
    return true;
  };
</script>

<SvelteFlow bind:nodes bind:edges {onbeforedelete} fitView />
```

## Components

### Controls

```svelte
<script lang="ts">
  import { SvelteFlow, Controls } from '@xyflow/svelte';
</script>

<SvelteFlow bind:nodes bind:edges fitView>
  <Controls showLock={false} showFitView={true} showZoom={true} />
</SvelteFlow>
```

### MiniMap

```svelte
<script lang="ts">
  import { SvelteFlow, MiniMap } from '@xyflow/svelte';
</script>

<SvelteFlow bind:nodes bind:edges fitView>
  <MiniMap />
</SvelteFlow>
```

### Background

```svelte
<script lang="ts">
  import { SvelteFlow, Background, BackgroundVariant } from '@xyflow/svelte';
</script>

<SvelteFlow bind:nodes bind:edges fitView>
  <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
</SvelteFlow>
```

Variants: `Dots`, `Lines`, `Cross`

### Panel (Custom Controls)

```svelte
<script lang="ts">
  import { SvelteFlow, Panel } from '@xyflow/svelte';
</script>

<SvelteFlow bind:nodes bind:edges fitView>
  <Panel position="top-left">
    <button>Custom Button</button>
  </Panel>
</SvelteFlow>
```

Positions: `top-left`, `top-center`, `top-right`, `bottom-left`, `bottom-center`, `bottom-right`

## Utility Functions

```typescript
import {
  getConnectedEdges,
  getIncomers,
  getOutgoers,
  addEdge,
  applyEdgeChanges,
  applyNodeChanges
} from '@xyflow/svelte';

// Get edges connected to nodes
const connectedEdges = getConnectedEdges(nodes, edges);

// Get nodes that connect TO a node
const incomers = getIncomers(targetNode, nodes, edges);

// Get nodes that a node connects TO
const outgoers = getOutgoers(sourceNode, nodes, edges);

// Add edge with validation
edges = addEdge(connection, edges);
```

## Store Management (Alternative)

For centralized state:

```javascript
// store.svelte.js
let nodes = $state.raw([...]);
let edges = $state.raw([...]);

export const getNodes = () => nodes;
export const getEdges = () => edges;
export const setNodes = (newNodes) => nodes = newNodes;
export const setEdges = (newEdges) => edges = newEdges;
```

```svelte
<!-- Component.svelte -->
<script>
  import { getNodes, getEdges, setNodes, setEdges } from './store.svelte.js';
</script>

<SvelteFlow bind:nodes={getNodes, setNodes} bind:edges={getEdges, setEdges} />
```

## Export to Image

```svelte
<script lang="ts">
  import { useSvelteFlow } from '@xyflow/svelte';
  
  const { toObject, getViewport } = useSvelteFlow();
  
  async function downloadImage() {
    const { toPng } = await import('html-to-image');
    const dataUrl = await toPng(document.querySelector('.svelte-flow'));
    const a = document.createElement('a');
    a.setAttribute('download', 'flow.png');
    a.setAttribute('href', dataUrl);
    a.click();
  }
</script>
```

## Performance Tips

- Use `$state.raw` for nodes and edges (prevents deep reactivity)
- For large graphs (1000+ nodes), set `elevateNodesOnSelect={false}` and `elevateEdgesOnSelect={false}`
- Use `minZoom` and `maxZoom` to limit zoom levels
- Consider virtualization for extremely large graphs

## Common Props

```svelte
<SvelteFlow
  bind:nodes
  bind:edges
  nodeTypes={customNodeTypes}
  edgeTypes={customEdgeTypes}
  defaultEdgeOptions={{ animated: true, type: 'smoothstep' }}
  connectionLineType={ConnectionLineType.Straight}
  connectionMode={ConnectionMode.Loose}
  fitView
  minZoom={0.1}
  maxZoom={2}
  snapToGrid={true}
  snapGrid={[15, 15]}
  elevateNodesOnSelect={true}
  elevateEdgesOnSelect={true}
  deleteKeyCode="Delete"
  selectionKeyCode="Shift"
  multiSelectionKeyCode="Meta"
  panOnScroll={true}
  zoomOnScroll={true}
  zoomOnDoubleClick={true}
  zoomOnPinch={true}
  panOnDrag={true}
/>
```
