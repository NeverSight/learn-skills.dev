---
name: systems-decomposition
description: Break down complex products, features, or systems into fundamental primitives and building blocks. Use when someone says "break down X", "decompose this", "what are the primitives for Y", "building blocks of Z", or needs to understand a complex system from first principles. Outputs human-readable lists with ASCII diagrams showing relationships.
---

# Systems Decomposition

Break complex products/features/systems into fundamental primitives - transferable, learnable building blocks that can be clearly explained and delineated.

## Process

### 1. Build Mental Model First

Before decomposing, ensure deep understanding of the target system:
- What problem does it solve?
- Who are the users?
- What are the core workflows?

If understanding is unclear, ask clarifying questions. Do not proceed without a clear mental model.

### 2. Apply First Principles

Think from the user's perspective through their journey:
- What discrete actions do they take?
- What are the atomic operations that can't be broken down further?
- What skills/capabilities are reusable across different workflows?

### 3. Identify Primitives

A good primitive is:
- **Transferable**: Useful in multiple contexts
- **Learnable**: Can be explained clearly
- **Delineable**: Has clear boundaries
- **Composable**: Can combine with other primitives

### 4. Output Format

```
## Primitives

### 1. [Primitive Name]
**Purpose**: What it does
**Triggers**: When it activates
**Inputs**: What it needs
**Outputs**: What it produces

### 2. [Next Primitive]
...

## How They Fit Together

[ASCII diagram showing relationships]

┌─────────────┐     ┌─────────────┐
│ Primitive A │────▶│ Primitive B │
└─────────────┘     └─────────────┘
        │
        ▼
┌─────────────┐
│ Primitive C │
└─────────────┘
```

## Examples

**Car driving primitives**: parallel parking, highway overtaking, lane changing, emergency braking - high-level skills that are transferable and clearly delineated.

**Software architecture primitives**: database query optimization, authentication flow, frontend component composition, API request handling.

**E-commerce marketing primitives**: audience segmentation, campaign scheduling, content generation, performance analysis.

## Input Template

Use this structure when invoking:

```
<product>
[Description of the product/system being analyzed]
</product>

<feature_request>
[Current feature or area of focus]
</feature_request>

<product_journey>
[Optional: Example user journey to analyze]
</product_journey>
```

## Key Questions to Ask

If context is insufficient:
- What does the product do at its core?
- Walk me through a typical user session
- What are the main workflows?
- What integrations/dependencies exist?
