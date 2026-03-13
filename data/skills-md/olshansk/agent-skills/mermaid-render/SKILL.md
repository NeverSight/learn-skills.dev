---
name: mermaid-render
description: >
  Render and display Mermaid diagrams inline in iTerm2 or Ghostty.
  Use when creating, editing, or iterating on mermaid diagrams.
  Triggers on mermaid diagram work — flowcharts, sequence, state, class, ER, and XY charts.
allowed-tools: Read Write Edit Bash
---

# Mermaid Diagram Renderer <!-- omit in toc -->

Render mermaid diagrams to PNG and display them inline. Supports iTerm2 (imgcat) and Ghostty (kitten icat). Built for fast visual iteration.

<!-- TODO: Once Claude Code supports inline image passthrough, update the workflow
     to display directly instead of printing the view command.
     Tracking: https://github.com/anthropics/claude-code/issues/29254 -->

- [Workflow](#workflow)
- [Prerequisites](#prerequisites)
- [Rendering](#rendering)
- [Iteration Rules](#iteration-rules)
- [Mermaid Syntax Cheatsheet](#mermaid-syntax-cheatsheet)

## Workflow

Every time you generate or modify mermaid code, immediately render and display it. Never ask "want me to render?" — just do it.

**Write the mermaid code:**

```bash
cat > /tmp/mermaid-diagram.mmd << 'MERMAID'
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[End]
MERMAID
```

**Render:**

```bash
"${CLAUDE_SKILL_DIR}/scripts/render.sh" /tmp/mermaid-diagram.mmd
```

The script outputs `Rendered: <path>` and `View: <command>`. **Always print the `View:` command for the user** so they can copy-paste it to see the diagram inline. Claude Code's Bash tool captures stdout, so inline images won't display automatically.

If the user provides a specific file path, use that instead of `/tmp/mermaid-diagram.mmd`.

## Prerequisites

On first use, check that `mmdc` is available:

```bash
which mmdc || echo "MISSING: Run 'npm install -g @mermaid-js/mermaid-cli'"
```

The display command (`imgcat` or `kitten icat`) is detected automatically based on `$TERM_PROGRAM`. No manual setup needed — the script falls back to `open` if neither is available.

## Rendering

The `render.sh` script handles rendering with sensible defaults. It supports these flags:

- `--theme <name>` — mermaid theme: `default`, `dark`, `forest`, `neutral` (default: `default`)
- `--width <px>` — output width in pixels (default: `1200`)
- `--bg <color>` — background color (default: `transparent`)
- `--css <path>` — custom CSS file for styling
- `--output <path>` — custom output path (default: replaces `.mmd` with `.png`)

**Examples:**

```bash
"${CLAUDE_SKILL_DIR}/scripts/render.sh" /tmp/mermaid-diagram.mmd --theme dark
```

```bash
"${CLAUDE_SKILL_DIR}/scripts/render.sh" /tmp/mermaid-diagram.mmd --width 2400
```

```bash
"${CLAUDE_SKILL_DIR}/scripts/render.sh" /tmp/mermaid-diagram.mmd --output ~/Desktop/diagram.png
```

## Iteration Rules

- After each user edit request, update the `.mmd` file and re-render immediately
- Show the `View:` command after every change — the user should never have to ask
- Keep the `.mmd` file path consistent within a session so edits accumulate
- If `mmdc` reports a syntax error, show the error message and fix the mermaid code before retrying
- Use the cheatsheet below for syntax reference when iterating

## Mermaid Syntax Cheatsheet

### Graph Directions

`graph TD` (top-down), `graph LR` (left-right), `graph BT` (bottom-top), `graph RL` (right-left)

### Node Shapes

```text
A[Rectangle]    B(Rounded)    C{Diamond}
D((Circle))     E[[Subroutine]]   F[(Database)]
G>Asymmetric]   H{{Hexagon}}  I[/Parallelogram/]
```

### Link Styles

```text
A --> B           Solid arrow
A --- B           Solid line (no arrow)
A -.-> B          Dotted arrow
A ==> B           Thick arrow
A -->|label| B    Arrow with label
A -- text --> B   Arrow with text (alternate)
```

### Subgraphs

```text
subgraph Title
    A --> B
end
```

### Styling

```text
style A fill:#f9f,stroke:#333,stroke-width:2px
classDef highlight fill:#ff0,stroke:#333
class A,B highlight
```

### Themes

Set via `--theme` flag: `default`, `dark`, `forest`, `neutral`

Or in the diagram: `%%{init: {'theme': 'dark'}}%%`

### Sequence Diagram

```text
sequenceDiagram
    participant A as Alice
    participant B as Bob
    A->>B: Hello
    B-->>A: Hi back
    A->>+B: Request
    B-->>-A: Response
    Note over A,B: Handshake complete
```

### State Diagram

```text
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing: start
    Processing --> Done: finish
    Done --> [*]
```

### Entity Relationship

```text
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
```

### Class Diagram

```text
classDiagram
    class Animal {
        +String name
        +makeSound()
    }
    Animal <|-- Dog
    Animal <|-- Cat
```
