---
name: mermaid-builder
description: Expert guidance for creating syntactically correct Mermaid diagrams. Use when creating flowcharts, sequence diagrams, class diagrams, state diagrams, Gantt charts, ER diagrams, or data lineage visualizations.
allowed-tools: Read Write Edit MultiEdit Grep Glob Bash WebSearch WebFetch
---

# Mermaid Builder

## Core Philosophy

- **Correctness**: Follow Mermaid syntax rules strictly
- **Clarity**: Diagrams communicate complex ideas simply
- **Simplicity**: Avoid overloading with unnecessary detail
- **Modularity**: Break complex diagrams into subgraphs

## Critical: Label Quoting Rule

**RULE: Wrap labels in double quotes if they contain spaces, special characters, or punctuation.**

```mermaid
%% CORRECT - labels with spaces quoted
flowchart LR
    A["User Login"] --> B["Process Request"]
    C["Pay $100?"] --> D["Confirm (Yes/No)"]

%% WRONG - will fail to render
flowchart LR
    A[User Login] --> B[Process Request]
```

**Must quote:** Spaces, special chars (`$%&`), punctuation (`:,;`), operators (`()[]`)
**Optional:** Simple alphanumeric (`Login`, `Process`, `Node1`)

**When in doubt, use quotes. It never hurts.**

## Quick Reference

### Flowchart Shapes

| Syntax | Shape |
|--------|-------|
| `["Text"]` | Rectangle |
| `("Text")` | Rounded |
| `{"Text"}` | Diamond (decision) |
| `[("Text")]` | Cylinder (database) |
| `(("Text"))` | Circle |

### Arrow Types

| Syntax | Type |
|--------|------|
| `-->` | Solid arrow |
| `---` | Solid line |
| `-.->` | Dotted arrow |
| `==>` | Thick arrow |
| `-->|Label|` | Arrow with label |

### Diagram Types

| Type | Declaration | Use Case |
|------|-------------|----------|
| Flowchart | `flowchart TD` | Processes, workflows, decisions |
| Sequence | `sequenceDiagram` | Component interactions, API flows |
| Class | `classDiagram` | OOP structure, models |
| State | `stateDiagram-v2` | State transitions |
| Gantt | `gantt` | Timelines, scheduling |
| ER | `erDiagram` | Database schema |
| Pie | `pie` | Proportional data |

**Directions:** `TB`/`TD` (top-down), `BT` (bottom-up), `LR` (left-right), `RL` (right-left)

See [references/diagram-examples.md](references/diagram-examples.md) for complete examples of each diagram type.

## Minimal Examples

### Flowchart

```mermaid
flowchart TD
    Start["Start"] --> Check{Valid?}
    Check -->|Yes| Process["Process"]
    Check -->|No| Error["Error"]
    Process --> End["End"]
```

### Sequence

```mermaid
sequenceDiagram
    Client->>Server: Request
    Server-->>Client: Response
```

### ER Diagram

```mermaid
erDiagram
    USER ||--o{ ORDER : "places"
    USER { int id PK string email }
    ORDER { int id PK int user_id FK }
```

## Subgraphs for Organization

```mermaid
flowchart TD
    subgraph "Frontend"
        A["UI"]
    end
    subgraph "Backend"
        B["API"]
        C[("DB")]
    end
    A --> B --> C
```

## Styling

```mermaid
flowchart TD
    A["Success"] --> B["Error"]

    classDef successStyle fill:#C8E6C9,stroke:#388E3C
    classDef errorStyle fill:#FFCDD2,stroke:#D32F2F

    class A successStyle
    class B errorStyle
```

## Common Errors to Avoid

| Error | Wrong | Correct |
|-------|-------|---------|
| Unquoted spaces | `A[User Login]` | `A["User Login"]` |
| Invalid arrow | `A -> B` | `A --> B` |
| Unquoted special | `A[Cost: $100]` | `A["Cost: $100"]` |
| Missing bracket | `A["Node --> B` | `A["Node"] --> B` |

## Validation Checklist

- [ ] Labels with spaces are quoted
- [ ] Labels with special characters quoted
- [ ] Brackets properly matched
- [ ] Arrow syntax correct (`-->` not `->`)
- [ ] Node IDs unique and meaningful
- [ ] Comments explain complex sections
- [ ] Previewed without errors

## Data Lineage Patterns

See [references/data-lineage.md](references/data-lineage.md) for:
- ETL pipeline patterns
- Multi-layer data architecture
- Cross-system data flows
- Database schema lineage
- Streaming data lineage
- Column-level lineage

## Resources

- [Mermaid Docs](https://mermaid.js.org/)
- [Live Editor](https://mermaid.live/)
- [Syntax Reference](https://mermaid.js.org/intro/syntax-reference.html)

---

**Remember: The quoting rule is the #1 cause of Mermaid rendering failures. When in doubt, quote it.**
