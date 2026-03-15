---
name: fbp-evaluator
description: Lazy graph evaluator for Flow-Based Programming. Use when evaluating FBP graphs, running dataflow computations, or working with the @fbp/evaluator package.
---

Lazy graph evaluator for Flow-Based Programming.

## Installation

```bash
pnpm add @fbp/evaluator
```

## Overview

`@fbp/evaluator` provides a lazy evaluation engine for FBP graphs. It only evaluates nodes that are needed for the requested output, making it efficient for large graphs where only a subset of nodes contribute to the result.

## Basic Usage

```typescript
import { evaluate } from '@fbp/evaluator';
import type { Graph } from '@fbp/types';
import type { NodeDefinitionWithImpl } from '@fbp/evaluator';

// Define node implementations
const addDef: NodeDefinitionWithImpl = {
  context: 'js',
  category: 'math',
  type: 'js/math/add',
  inputs: [
    { name: 'a', type: 'number' },
    { name: 'b', type: 'number' }
  ],
  outputs: [{ name: 'sum', type: 'number' }],
  impl: (inputs) => ({
    sum: (inputs.a ?? 0) + (inputs.b ?? 0)
  })
};

const constNumberDef: NodeDefinitionWithImpl = {
  context: 'js',
  category: 'const',
  type: 'js/const/number',
  props: [{ name: 'value', type: 'number' }],
  outputs: [{ name: 'value', type: 'number' }],
  impl: (inputs, props) => ({
    value: props.value ?? 0
  })
};

// Create a graph
const graph: Graph = {
  name: 'simple-add',
  nodes: [
    { name: 'num1', type: 'js/const/number', props: [{ name: 'value', value: 5 }] },
    { name: 'num2', type: 'js/const/number', props: [{ name: 'value', value: 3 }] },
    { name: 'add', type: 'js/math/add' }
  ],
  edges: [
    { src: { node: 'num1', port: 'value' }, dst: { node: 'add', port: 'a' } },
    { src: { node: 'num2', port: 'value' }, dst: { node: 'add', port: 'b' } }
  ]
};

// Evaluate the graph
const result = evaluate(graph, {
  definitions: [constNumberDef, addDef],
  outputNode: 'add',
  outputPort: 'sum'
});

console.log(result); // 8
```

## Node Definition with Implementation

```typescript
interface NodeDefinitionWithImpl extends NodeDefinition {
  impl: (
    inputs: Record<string, any>,
    props: Record<string, any>
  ) => Record<string, any>;
}
```

The `impl` function receives:
- `inputs`: Values from connected input ports
- `props`: Property values set on the node instance

It returns an object with output port names as keys.

## API

### `evaluate(graph, options)`

Evaluates a graph starting from the specified output node/port.

```typescript
const result = evaluate(graph, {
  definitions: NodeDefinitionWithImpl[],  // Node definitions with implementations
  outputNode: string,                      // Node to get output from
  outputPort: string,                      // Port to get output from
  inputs?: Record<string, any>,            // External inputs for graphInput nodes
  props?: Record<string, any>              // Props for graphProp nodes
});
```

## Features

### Lazy Evaluation

Only evaluates nodes that are needed for the output. If a node's output isn't connected to the requested output path, it won't be evaluated.

### Multi-Input Ports

Supports ports that accept multiple incoming edges. Values are collected in edge array order:

```typescript
const mergeDef: NodeDefinitionWithImpl = {
  type: 'js/array/merge',
  inputs: [{ name: 'items', type: 'any', multi: true }],
  outputs: [{ name: 'array', type: 'any[]' }],
  impl: (inputs) => ({
    array: inputs.items  // Array of all connected values
  })
};
```

### Boundary Nodes

Supports `graphInput`, `graphOutput`, and `graphProp` boundary nodes for graph inputs/outputs/props:

```typescript
// Provide external inputs
const result = evaluate(graph, {
  definitions,
  outputNode: 'output_result',
  outputPort: 'value',
  inputs: { a: 10, b: 20 },  // Keyed by portName
  props: { scale: 2.0 }       // Keyed by propName
});
```

## Example: Building a Node Library

```typescript
const mathNodes: NodeDefinitionWithImpl[] = [
  {
    context: 'js',
    category: 'math',
    type: 'js/math/add',
    inputs: [
      { name: 'a', type: 'number' },
      { name: 'b', type: 'number' }
    ],
    outputs: [{ name: 'sum', type: 'number' }],
    impl: (inputs) => ({ sum: (inputs.a ?? 0) + (inputs.b ?? 0) })
  },
  {
    context: 'js',
    category: 'math',
    type: 'js/math/multiply',
    inputs: [
      { name: 'a', type: 'number' },
      { name: 'b', type: 'number' }
    ],
    outputs: [{ name: 'product', type: 'number' }],
    impl: (inputs) => ({ product: (inputs.a ?? 1) * (inputs.b ?? 1) })
  },
  {
    context: 'js',
    category: 'math',
    type: 'js/math/negate',
    inputs: [{ name: 'value', type: 'number' }],
    outputs: [{ name: 'negated', type: 'number' }],
    impl: (inputs) => ({ negated: -(inputs.value ?? 0) })
  }
];
```

## Best Practices

1. Use descriptive type paths like `context/category/name` (e.g., `js/math/add`)
2. Always provide default values in `impl` functions for missing inputs
3. Keep node implementations pure — no side effects
4. Use `multi: true` for ports that should accept multiple connections
