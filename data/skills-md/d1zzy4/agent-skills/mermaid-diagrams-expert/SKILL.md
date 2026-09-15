---
name: mermaid-diagrams-expert
description: >
  Create maintainable Mermaid diagrams for software documentation, including flowcharts,
  sequence, class, ER, C4, state, git, gantt, and chart diagrams. Trigger when structure,
  relationships, sequencing, or architecture would be clearer visually, especially for
  persistent README, wiki, PR, or design-document diagrams. Verify the target renderer and
  Mermaid version before using version-sensitive syntax.
license: SSPL-1.0
metadata:
  version: 1.4.2
  author: D1ZZY4
  priority: medium
---

# Mermaid Diagrams Expert

## Purpose

Create maintainable Mermaid diagrams for software documentation when structure,
relationships, sequencing, or architecture would be clearer visually: flowcharts, sequence,
class, ER, C4, state, git, gantt, and chart diagrams. Verify the target renderer and Mermaid
version before using version-sensitive syntax. Load the references needed for the chosen
diagram type.

## Step 0: Decide whether a diagram earns its keep

Use a diagram when the reader must reason about relationships, sequence, state, topology,
branching, or dependencies. Do not force a diagram onto a simple fact that prose explains
more clearly.

For persistent documentation, treat the target renderer as a compatibility constraint.

## Step 1: Choose the diagram type

Read `references/diagram-type-selection.md`. Match the diagram to the structure being modeled:

| Structure | Preferred type |
|---|---|
| Process or decision tree | Flowchart |
| Interactions over time | Sequence |
| Domain objects and relationships | Class or ER |
| Service architecture | C4 or architecture flowchart |
| Lifecycle | State |
| Repository history | Git graph |
| Schedule | Gantt |
| Simple proportions | Pie or chart |

Use a specialized diagram only when its semantics help the reader.

## Step 2: Establish compatibility

Identify the target renderer and Mermaid version when the diagram will live in a repository.
If the renderer is unknown, avoid syntax known to be version-sensitive and state the assumption.

Read the relevant advanced-feature reference before using newer syntax, directives, or themes.

## Step 3: Model before styling

Define nodes, edges, labels, direction, and boundaries first. Keep labels short and meaningful.
Use subgraphs or C4 boundaries to make ownership and system boundaries explicit.

Avoid decorative complexity. A diagram is documentation, not a small hostage negotiation with
the reader.

## Step 4: Validate

Read `references/advanced-features.md` and the diagram-type reference as needed. Check:

- syntax parses in the target renderer,
- labels are unambiguous,
- direction and edge semantics are correct,
- IDs are stable and unique,
- special characters are safely quoted,
- the diagram is readable at its intended size,
- no sensitive data is embedded accidentally.

If a renderer is available, render-test it. Otherwise perform static syntax checks and clearly
label the result as unrendered.

## Step 5: Deliver for the destination

For chat, provide the Mermaid block plus a short interpretation when useful. For README/wiki/PR
content, preserve the exact fenced block and any required surrounding explanation.

## Anti-patterns

- Assuming Mermaid support is identical across platforms.
- Using new syntax without checking renderer/version compatibility.
- Turning every paragraph into a diagram.
- Overloading nodes with prose.
- Encoding secrets, credentials, or real personal data into examples.
- Claiming a diagram was rendered when it was only linted.
- Using em dashes in documentation.

## Bundled references

Load `references/diagram-type-selection.md`, the chosen diagram-type reference, and any advanced
feature reference needed for the requested syntax:

- `references/diagram-type-selection.md`: decision guide for choosing the right diagram type based
  on what is being modeled.
- `references/flowcharts.md`: flowchart syntax, structure, and common patterns.
- `references/sequence-diagrams.md`: sequence diagram syntax, actor/participant patterns, and
  common idioms.
- `references/class-diagrams.md`: class diagram syntax, relationships, and common patterns.
- `references/erd-diagrams.md`: ER diagram syntax, cardinality, and common patterns.
- `references/c4-diagrams.md`: C4 model syntax, context/container/component boundaries, and common
  patterns.
- `references/architecture-diagrams.md`: architecture diagram syntax, cloud/deployment topology, and
  common patterns.
- `references/misc-diagrams.md`: state diagrams, git graphs, gantt charts, and pie/bar charts.
- `references/advanced-features.md`: newer syntax, directives, themes, and version-sensitive
  features.
- `references/renderer-adapters.md`: target renderer and version compatibility checks.
- `references/validation-and-rendering.md`: how to validate diagrams before delivering, common
  pitfalls, export options, and where diagrams render without export.
- `references/proactive-trigger.md`: when to reach for a diagram without being asked, and when to
  stay quiet.
- `references/verification-and-failure.md`: shared verification and failure-handling principles.
