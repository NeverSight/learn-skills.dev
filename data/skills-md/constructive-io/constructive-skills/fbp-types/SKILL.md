---
name: fbp-types
description: Flow-Based Programming TypeScript types and GraphSchemata specification. Use when working with FBP type definitions, graph schemata, or the @fbp/types package.
---

Flow-Based Programming TypeScript types and GraphSchemata specification.

## Installation

```bash
pnpm add @fbp/types
```

## Overview

`@fbp/types` provides TypeScript types for a Houdini-inspired, merkle-friendly graph specification. The core design principles are explicitness over magic, composable subgraphs, stable content-addressable structure, and clear separation between dataflow and configuration.

## Core Concepts

### Everything is a Node

The entire document is a single Node. Nodes may contain other nodes and edges, forming nested graphs (subnets). A node becomes a subnet simply by containing `nodes[]` and `edges[]`. There is no separate "graph" type.

### Identity Model

Node identity equals name within parent scope. Names may be hierarchical paths by convention (`some/subnet/node`). Rename or move equals identity change. This model is compatible with merkle/content-addressable versioning.

## Type Definitions

### Graph

```typescript
interface Graph {
  name?: string;
  nodes: Node[];
  edges: Edge[];
  definitions?: NodeDefinition[];
  meta?: NodeMeta;
}
```

### Node

```typescript
interface Node {
  name: string;               // Unique within parent scope
  type: string;               // References a NodeDefinition
  meta?: NodeMeta;            // Position and metadata
  props?: PropValue[];        // Property values
  nodes?: Node[];             // Child nodes (makes this a subnet)
  edges?: Edge[];             // Edges within this scope
}
```

### Edge

```typescript
interface Edge {
  src: PortRef;               // Source (output port)
  dst: PortRef;               // Destination (input port)
  channel?: string;           // Optional channel (default: "main")
}

interface PortRef {
  node: string;               // Node name within scope
  port: string;               // Port name
}
```

### NodeDefinition

```typescript
interface NodeDefinition {
  type: string;               // Unique identifier (e.g., "math/add")
  context?: string;           // Namespace (e.g., "math", "ui")
  category?: string;          // Palette category
  inputs?: PortDef[];         // Input port definitions
  outputs?: PortDef[];        // Output port definitions
  props?: PropDef[];          // Property definitions
  icon?: string;
  description?: string;
}
```

### Port and Prop Definitions

```typescript
interface PortDef {
  name: string;
  type?: string;              // Data type (e.g., "string", "number", "any")
  multi?: boolean;            // Accepts multiple connections
  description?: string;
}

interface PropDef {
  name: string;
  type?: string;
  default?: any;
  description?: string;
}

interface PropValue {
  name: string;
  value?: any;
  ref?: boolean;              // If true, value is a reference path
}
```

## Ports (No Lanes)

Ports are named, typed, and singular. There is no lane or index dimension. Branching uses multiple named output ports (e.g., `true`, `false`, `error`). Fan-in is never implicit — multiple values must be combined via explicit nodes (`Merge`, `Collect`, etc.).

## Props vs Dataflow

Props are not dataflow. They configure node behavior and are not connected by edges. They may reference other parameters via `Ref`:

```json
{ "ref": "../config/apiKey" }
```

## Boundary Nodes

Boundary nodes define a subnet's interface:

| Node Type | Purpose | Properties |
|-----------|---------|------------|
| `graphInput` | Input port | `portName`, `dataType` |
| `graphOutput` | Output port | `portName`, `dataType` |
| `graphProp` | Configuration property | `propName`, `dataType`, `default` |

Reserved names `@in`, `@out`, `@props` are used for canonical boundary nodes.

## Channels

Edges may specify a `channel` for namespacing:

```typescript
{
  src: { node: 'A', port: 'out' },
  dst: { node: 'B', port: 'in' },
  channel: 'error'
}
```

Default channel is `"main"`. Non-main channels are for error routing, control edges, metadata propagation.

## Validation Rules

- Node names must be unique within a scope
- Node names starting with `@` are reserved for boundary nodes
- Port names must be unique within inputs, outputs, and props
- Edges must reference existing ports
- Fan-in requires explicit merge nodes
- Branching requires explicit output ports
