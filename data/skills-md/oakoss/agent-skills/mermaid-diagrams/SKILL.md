---
name: mermaid-diagrams
description: 'Mermaid diagram syntax for flowcharts, sequence diagrams, ERDs, class diagrams, and more. Use when creating diagrams in markdown, generating architecture visuals, or documenting system flows. Use for mermaid, diagram, flowchart, sequence, ERD, class-diagram, gantt, pie-chart, mindmap.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: 'https://mermaid.js.org/intro/'
---

# Mermaid Diagrams

## Overview

Mermaid is a JavaScript-based diagramming tool that renders Markdown-inspired text definitions into SVG diagrams. It supports flowcharts, sequence diagrams, ER diagrams, class diagrams, state diagrams, Gantt charts, pie charts, mindmaps, and git graphs directly inside Markdown files.

**When to use:** Documenting system architecture, visualizing data models, illustrating request flows, creating project timelines, embedding diagrams in GitHub/GitLab READMEs or docs sites.

**When NOT to use:** Pixel-perfect design mockups, interactive dashboards, diagrams requiring custom artwork or complex spatial layouts beyond hierarchical/relational structures.

## Quick Reference

| Diagram        | Declaration          | Key Points                                           |
| -------------- | -------------------- | ---------------------------------------------------- |
| Flowchart      | `flowchart TD`       | Directions: TB, TD, BT, RL, LR. Supports subgraphs   |
| Sequence       | `sequenceDiagram`    | Participants, messages, loops, alt/opt/par blocks    |
| ER Diagram     | `erDiagram`          | Crow's foot notation, PK/FK/UK attributes            |
| Class Diagram  | `classDiagram`       | UML relationships, visibility modifiers, annotations |
| State Diagram  | `stateDiagram-v2`    | Transitions, composite states, forks/joins, choice   |
| Gantt Chart    | `gantt`              | Sections, tasks with dates/durations, milestones     |
| Pie Chart      | `pie`                | Labels with numeric values, optional title           |
| Mindmap        | `mindmap`            | Indentation-based hierarchy, multiple node shapes    |
| Git Graph      | `gitGraph`           | Commits, branches, merges, cherry-picks, tags        |
| Architecture   | `architecture-beta`  | Services in groups, directional edges (T/B/L/R)      |
| Block Diagram  | `block-beta`         | Column layout, block arrows, nested blocks           |
| Timeline       | `timeline`           | Time periods with events, sections for grouping      |
| Sankey         | `sankey-beta`        | Flow quantities between nodes, CSV-like data format  |
| XY Chart       | `xychart-beta`       | Bar and line charts with x/y axes                    |
| Quadrant Chart | `quadrantChart`      | Four-quadrant plot with labeled axes and data points |
| Kanban         | `kanban`             | Columns with task cards, assignees, priorities       |
| Packet         | `packet-beta`        | Network packet structure with bit-range fields       |
| Requirement    | `requirementDiagram` | Requirements, elements, and verification links       |
| C4 Diagram     | `C4Context`          | C4 model: Context, Container, Component, Deployment  |

## Common Mistakes

| Mistake                                   | Correct Pattern                                            |
| ----------------------------------------- | ---------------------------------------------------------- |
| Using `graph` instead of `flowchart`      | Use `flowchart` for subgraph edges and newer features      |
| Missing space after arrow in sequences    | `Alice->>Bob: msg` not `Alice->>Bob:msg`                   |
| Wrong cardinality order in ER diagrams    | Left cardinality, then line, then right cardinality        |
| Forgetting `end` after subgraph/loop/alt  | Every block keyword requires a matching `end`              |
| Using reserved words as node IDs          | Wrap reserved words in quotes or use aliases               |
| Bare code blocks without language tag     | Always use ` ```mermaid ` as the language specifier        |
| Mixing v1 and v2 state diagram syntax     | Use `stateDiagram-v2` consistently for current features    |
| Unquoted labels with special characters   | Wrap labels containing special characters in double quotes |
| Missing `dateFormat` in Gantt charts      | Always declare `dateFormat` before task definitions        |
| Using tabs instead of spaces for mindmaps | Mindmap indentation requires spaces, not tabs              |

## Delegation

- **Diagram discovery and exploration**: Use `Explore` agent to find existing diagrams in the codebase
- **Diagram review**: Use `Task` agent to verify diagram accuracy against code
- **Architecture documentation**: Use `code-reviewer` agent for doc quality checks

## References

- [Flowcharts: nodes, edges, subgraphs, directions, and styling](references/flowcharts.md)
- [Sequence diagrams: participants, messages, activations, and control flow](references/sequence-diagrams.md)
- [Entity-relationship diagrams: entities, attributes, and cardinality](references/entity-relationship.md)
- [Class diagrams: classes, methods, relationships, and annotations](references/class-diagrams.md)
- [Other diagrams: Gantt, pie, mindmap, state, and git graph](references/other-diagrams.md)
- [Architecture, block, timeline, Sankey, XY chart, quadrant, kanban, packet, requirement, and C4 diagrams](references/extended-diagrams.md)
