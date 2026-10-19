---
name: mermaid-charts
description: Write accurate Mermaid charts by understanding critical syntax rules and selecting the appropriate chart type for your visualization needs. Use when creating or reviewing flowcharts, sequence diagrams, class diagrams, state machines, ER diagrams, Gantt charts, or any of 24+ diagram types. Includes syntax pitfalls, chart selection guide, and links to official documentation.
---

# Mermaid Chart Writing

Write accurate Mermaid diagrams by mastering critical syntax rules and selecting the right chart type for your use case.

## Critical Syntax Rules

These rules must be followed to avoid breaking diagrams:

### Node IDs and Text

- **No spaces in node IDs** → Use `camelCase` or `snake_case`
  - Bad: `A -x-> B` (the `x` is treated as a connection style)
  - Good: `nodeA --> nodeB`

- **Quote node labels with special characters** → Use `A["Process (main)"]` not `A[Process (main)]`
  - Parentheses, colons, commas need quotes

- **No HTML `<br/>` tags** → They render as literal text
  - Bad: `node["Line 1<br/>Line 2"]`
  - Good: Use literal newlines in markdown strings or configure markdown wrapping

### Reserved Keywords

Avoid these as node IDs (they break diagram parsing):
- `end`, `subgraph`, `graph`, `flowchart`
- Workaround: Capitalize (`End`, `END`) or apply other patterns

### Subgraph Syntax

- **Correct**: `subgraph id [Label]` (no spaces in id)
- **Wrong**: `subgraph my subgraph [Label]` (spaces cause parsing issues)

### Edge Labels

- **Quote labels with special characters** → `|"O(1) lookup"|` or `|"1:M"|`
- Parentheses, pipes, math notation need quotes

### Styling

- **NO explicit colors** → `style A fill:#fff` breaks dark mode
  - Mermaid uses theme-based colors automatically
- **NO click events** → Disabled for security (even with `securityLevel='loose'`)
- **Use classDef instead** → Define reusable styles and apply with `class` statement

### Common Gotchas by Diagram Type

- **Flowchart**: Node shapes use delimiters `()`, `[]`, `{}`, etc. Don't mix them
- **Sequence Diagram**: Participants render in order of appearance. Use `participant` keyword to reorder
- **Class Diagram**: Use `classDef` for styling nodes, not direct `style` statements
- **State Diagram**: `[*]` is reserved for start/end; use regular nodes for other states
- **ER Diagram**: Relationships use pipes for cardinality: `|o`, `||`, `}o`, `}|`, etc.

---

## Chart Type Selection Guide

Choose the right chart type based on your visualization goal:

### 1. Flowchart (`flowchart`/`graph`)
**Purpose**: Process flows, decision trees, algorithms, workflows  
**Best for**: Step-by-step procedures, conditional logic, data pipelines  
**Features**: Subgraphs, 30+ node shapes, styling, links, icons  
**Complexity**: Low to high  
**Docs**: https://mermaid.js.org/syntax/flowchart.html

### 2. Sequence Diagram (`sequenceDiagram`)
**Purpose**: Message passing between actors/systems over time  
**Best for**: API calls, authentication flows, microservice communication  
**Features**: Loops, alt/opt, parallel blocks, notes, activation bars  
**Complexity**: Medium  
**Docs**: https://mermaid.js.org/syntax/sequenceDiagram.html

### 3. Class Diagram (`classDiagram`)
**Purpose**: OOP class structures, inheritance, relationships  
**Best for**: Software architecture, UML, design documentation  
**Features**: Attributes, methods, visibility, cardinality, annotations  
**Complexity**: Medium  
**Docs**: https://mermaid.js.org/syntax/classDiagram.html

### 4. State Diagram (`stateDiagram-v2`)
**Purpose**: Finite state machines, object lifecycles  
**Best for**: State-based behavior, workflows with multiple paths  
**Features**: Composite states, forks/joins, choice, concurrency  
**Complexity**: Medium  
**Docs**: https://mermaid.js.org/syntax/stateDiagram.html

### 5. Entity Relationship Diagram (`erDiagram`)
**Purpose**: Database schema design, data modeling  
**Best for**: Relational database structure, entity relationships  
**Features**: Crow's foot notation, cardinality, attributes with keys (PK/FK/UK)  
**Complexity**: Medium  
**Docs**: https://mermaid.js.org/syntax/entityRelationshipDiagram.html

### 6. User Journey (`journey`)
**Purpose**: UX mapping, task completion flows  
**Best for**: User experience documentation, customer journey mapping  
**Features**: Scores (1-5), actors, sections  
**Complexity**: Low  
**Docs**: https://mermaid.js.org/syntax/userJourney.html

### 7. Gantt Chart (`gantt`)
**Purpose**: Project timelines, task scheduling, milestones  
**Best for**: Project management, timeline visualization  
**Features**: Dependencies, sections, milestone markers, exclude weekends  
**Complexity**: Low to medium  
**Docs**: https://mermaid.js.org/syntax/gantt.html

### 8. Pie Chart (`pie`)
**Purpose**: Simple proportional data visualization  
**Best for**: Part-to-whole relationships (market share, budget allocation)  
**Features**: Labels, positive numeric values only  
**Complexity**: Low  
**Docs**: https://mermaid.js.org/syntax/pie.html

### 9. Quadrant Chart (`quadrantChart`)
**Purpose**: 2x2 matrix analysis  
**Best for**: Priority/effort assessment, risk matrices, importance/urgency  
**Features**: Labeled axes, quadrant regions, data points (0-1 range)  
**Complexity**: Low  
**Docs**: https://mermaid.js.org/syntax/quadrantChart.html

### 10. Requirement Diagram (`requirementDiagram`)
**Purpose**: SysML requirements traceability  
**Best for**: System requirements documentation, compliance tracking  
**Features**: Requirement types, elements, relationship types (satisfies, verifies, derives)  
**Complexity**: Medium  
**Docs**: https://mermaid.js.org/syntax/requirementDiagram.html

### 11. GitGraph (`gitGraph`)
**Purpose**: Git branch visualization, commit history  
**Best for**: Git workflow documentation, branching strategy  
**Features**: Branches, commits, merges, cherry-picks, tags  
**Complexity**: Low to medium  
**Docs**: https://mermaid.js.org/syntax/gitgraph.html

### 12. C4 Diagram (`C4Context`/`C4Container`/`C4Component`/`C4Dynamic`/`C4Deployment`)
**Purpose**: Software architecture at multiple zoom levels  
**Best for**: System context, container structure, component dependencies  
**Features**: System context, container, component, dynamic, deployment views  
**Complexity**: High  
**Notes**: Experimental; PlantUML-compatible syntax  
**Docs**: https://mermaid.js.org/syntax/c4.html

### 13. Mindmap (`mindmap`)
**Purpose**: Hierarchical idea organization, brainstorming  
**Best for**: Knowledge structure, topic breakdown, concept mapping  
**Features**: Indentation-based hierarchy, multiple node shapes  
**Complexity**: Low  
**Docs**: https://mermaid.js.org/syntax/mindmap.html

### 14. Timeline (`timeline`)
**Purpose**: Chronological events, historical data, roadmaps  
**Best for**: Product roadmaps, historical timelines, milestones  
**Features**: Sections, time periods, multiple events per period  
**Complexity**: Low  
**Docs**: https://mermaid.js.org/syntax/timeline.html

### 15. ZenUML (`zenuml`)
**Purpose**: Alternative sequence diagram syntax (code-like)  
**Best for**: Developers preferring code-style sequence diagrams  
**Features**: Sync/async messages, loops, alt/else, try/catch  
**Complexity**: Medium  
**Docs**: https://mermaid.js.org/syntax/zenuml.html

### 16. Sankey Diagram (`sankey-beta`)
**Purpose**: Flow quantities between nodes  
**Best for**: Energy flows, budget tracking, data pipelines, material flow  
**Features**: CSV-like syntax (source, target, value), link coloring  
**Complexity**: Low  
**Version**: v10.3.0+  
**Docs**: https://mermaid.js.org/syntax/sankey.html

### 17. XY Chart (`xychart-beta`)
**Purpose**: Bar and line charts on x/y axes  
**Best for**: Data visualization, time series  
**Features**: Categorical or numeric x-axis, horizontal/vertical orientation  
**Complexity**: Low  
**Docs**: https://mermaid.js.org/syntax/xyChart.html

### 18. Block Diagram (`block-beta`)
**Purpose**: General-purpose block layouts  
**Best for**: Layout visualization, column-based organization  
**Features**: Columns, spacing, nested blocks  
**Complexity**: Low  
**Docs**: https://mermaid.js.org/syntax/block.html

### 19. Packet Diagram (`packet-beta`)
**Purpose**: Network packet structure visualization  
**Best for**: Protocol documentation, network packet formats  
**Features**: Bit ranges, field descriptions, labels  
**Complexity**: Low  
**Version**: v11.0.0+  
**Docs**: https://mermaid.js.org/syntax/packet.html

### 20. Kanban (`kanban`)
**Purpose**: Task boards, workflow stages  
**Best for**: Workflow management, task tracking  
**Features**: Columns, tasks, metadata (assigned, ticket, priority)  
**Complexity**: Low  
**Docs**: https://mermaid.js.org/syntax/kanban.html

### 21. Architecture Diagram (`architecture-beta`)
**Purpose**: Cloud/CI-CD service relationships  
**Best for**: Microservices architecture, cloud infrastructure  
**Features**: Groups, services, edges, junctions, icon support  
**Complexity**: Medium  
**Version**: v11.1.0+  
**Docs**: https://mermaid.js.org/syntax/architecture.html

### 22. Radar Chart (`radar-beta`)
**Purpose**: Multi-dimensional comparison (spider/star chart)  
**Best for**: Performance comparison, skill assessment, capability matrix  
**Features**: Multiple axes, curves, graticule  
**Complexity**: Low  
**Version**: v11.6.0+  
**Docs**: https://mermaid.js.org/syntax/radar.html

### 23. Treemap (`treemap-beta`)
**Purpose**: Hierarchical data as nested rectangles  
**Best for**: Budget visualization, file sizes, organizational structures  
**Features**: Proportional sizing, value formatting, styling  
**Complexity**: Low  
**Docs**: https://mermaid.js.org/syntax/treemap.html

### 24. Examples (General Reference)
View working examples for all diagram types  
**Docs**: https://mermaid.js.org/syntax/examples.html

---

## Workflow

1. **Select chart type** from the catalog above based on your visualization goal
2. **Fetch detailed syntax** from the documentation URL if needed
3. **Apply critical syntax rules** when writing the diagram
4. **Test rendering** to verify correctness

---

## Additional Resources

- **Official Mermaid Site**: https://mermaid.js.org/
- **Live Editor**: https://mermaid.live/ (test diagrams online)
- **Examples Index**: https://mermaid.js.org/syntax/examples.html
