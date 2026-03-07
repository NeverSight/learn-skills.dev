---
name: adr-graph-easy-architect
description: ASCII architecture diagrams for ADRs via graph-easy. TRIGGERS - ADR diagram, architecture diagram, ASCII diagram.
allowed-tools: Bash, Read, Write, Edit
---

# ADR Graph-Easy Architect

Create comprehensive ASCII architecture diagrams for Architecture Decision Records (ADRs) using graph-easy. Pure text output with automatic layout - no image rendering required.

## When to Use This Skill

- Writing new ADR that involves architectural changes
- ADR describes migration, integration, or system changes
- User asks for visual representation of a decision
- Existing ADR diagram needs review or update

## Preflight Check

Ensure graph-easy is installed and functional before rendering diagrams.

Full setup instructions: [Preflight Setup](./references/preflight-setup.md)

**Quick verify:**

```bash
echo "[Test] -> [OK]" | graph-easy --as=boxart &>/dev/null && echo "✓ graph-easy ready"
```

---

## DSL Quick Reference

Full syntax with examples, node styling, edge styles, and emoji rules: [DSL Syntax Reference](./references/dsl-syntax.md)

### Essential Syntax

```
[Node]                          # Node
[A] -> [B]                      # Edge
[A] -- label --> [B]            # Labeled edge
[A] <-> [B]                     # Bidirectional
( Group: [Node A] [Node B] )    # Group/container
[id] { label: "Display"; }     # Custom label
```

### Flow Direction (MANDATORY)

```
graph { flow: south; }   # Top-to-bottom (architecture, decisions)
graph { flow: east; }    # Left-to-right (pipelines, sequences)
```

### Graph Label (MANDATORY: EVERY diagram MUST have emoji + title)

**WARNING**: This is the most commonly forgotten requirement. Diagrams without labels are invalid.

**Correct:**

```
graph { label: "🔄 Database Migration"; flow: south; }
[Old DB] -> [New DB]
```

**Anti-Pattern (INVALID):**

```
graph { flow: south; }
[Old DB] -> [New DB]
```

Missing `label:` with emoji. The preflight validator will **BLOCK** any ADR containing diagrams without `graph { label: "emoji ..."; }`.

### Emoji Selection (for graph labels ONLY - never inside nodes)

| Diagram Type       | Emoji | Diagram Type     | Emoji |
| ------------------ | ----- | ---------------- | ----- |
| Migration/Change   | 🔄    | Architecture     | 🏗️    |
| Deployment/Release | 🚀    | Network/API      | 🌐    |
| Data Flow          | 📊    | Storage/Database | 💾    |
| Security/Auth      | 🔐    | Monitoring       | 📡    |
| Error/Failure      | ⚠️    | Hook/Event       | 🪝    |
| Decision/Branch    | 🔀    | Before/After     | ⏮️/⏭️ |

### Node & Edge Styling Summary

| Style           | Syntax                | Use For               |
| --------------- | --------------------- | --------------------- |
| Rounded corners | `{ shape: rounded; }` | Start/end nodes       |
| Double border   | `{ border: double; }` | Critical/emphasis     |
| Bold border     | `{ border: bold; }`   | Important nodes       |
| Dotted border   | `{ border: dotted; }` | Optional/skippable    |
| Solid arrow     | `->`                  | Main/happy path       |
| Dotted arrow    | `..>`                 | Conditional/alternate |
| Bold arrow      | `==>`                 | Emphasized/critical   |
| Labeled edge    | `-- label -->`        | Annotated connections |

### Character Safety

- Graphical emojis INSIDE nodes: **NEVER** (breaks box alignment)
- Unicode symbols inside nodes (checkmark, cross, warning): **OK** (single-width)
- ASCII markers inside nodes ([x] [+] [!]): **ALWAYS safe**
- Graphical emojis in `graph { label: }`: **OK**

Full symbol reference: [Monospace-Safe Symbols](./references/monospace-symbols.md)

---

## Common Diagram Patterns

### Migration (Before -> After)

```
graph { flow: south; }
[Before] -- migrate --> [After]
```

### Multi-Component System

```
graph { flow: south; }
[A] -> [B] -> [C]
[B] -> [D]
```

### Pipeline (Left-to-Right)

```
graph { flow: east; }
[Input] -> [Process] -> [Output]
```

### Decision with Options

```
graph { flow: south; }
[Decision] -> [Option A]
[Decision] -> [Option B]
```

### Grouped Components

```
( Group:
  [Component 1]
  [Component 2]
)
[External] -> [Component 1]
```

### Bidirectional Flow

```
[Client] <-> [Server]
[Server] -> [Database]
```

More patterns by ADR type: [Diagram Examples](./references/diagram-examples.md)

---

## Rendering

### Command (MANDATORY: Always use boxart)

```bash
graph-easy --as=boxart << 'EOF'
graph { flow: south; }
[A] -> [B] -> [C]
EOF
```

**Never use** `--as=ascii` - it produces ugly `+--+` boxes instead of clean `┌──┐` lines.

### Validation Workflow

```bash
# 1. Write DSL to heredoc
# 2. Render with boxart
# 3. Review output
# 4. Iterate if needed
# 5. Copy final ASCII to ADR
```

---

## Embedding in ADR

Every rendered diagram MUST include a collapsible `<details>` block with graph-easy source. Full format guide and GFM syntax rules: [ADR Embedding Guide](./references/adr-embedding.md)

**Required format:**

````markdown
```
┌───────┐     ┌──────┐
│ Build │ --> │ Test │
└───────┘     └──────┘
```

<details>
<summary>graph-easy source</summary>

```
graph { label: "🚀 Pipeline"; flow: east; }
[Build] -> [Test]
```

</details>
````

**The `<details>` block is MANDATORY** - never embed a diagram without its source.

---

## Mandatory Checklist (Before Rendering)

### Graph-Level (MUST have)

- [ ] **`graph { label: "🚀 Title"; }`** - semantic emoji + title (MOST FORGOTTEN - check first!)
- [ ] `graph { flow: south; }` or `graph { flow: east; }` - explicit direction
- [ ] Command uses `--as=boxart` - NEVER `--as=ascii`

### Embedding (MUST have - non-negotiable)

- [ ] **`<details>` block with source** - EVERY diagram MUST have collapsible source code block
- [ ] Format: rendered diagram in ` ``` ` block, followed by `<details><summary>graph-easy source</summary>` with source
- [ ] Never commit a diagram without its reproducible source

### Node Styling (Visual hierarchy)

- [ ] Start/end nodes: `{ shape: rounded; }` - entry/exit points
- [ ] Critical/important nodes: `{ border: double; }` or `{ border: bold; }`
- [ ] Optional/skippable nodes: `{ border: dotted; }`
- [ ] Long labels use `\n` for multiline - max ~15 chars per line

### Edge Styling (Semantic meaning)

- [ ] Main/happy path: `->` solid arrow
- [ ] Conditional/alternate: `..>` dotted arrow
- [ ] Emphasized/critical: `==>` bold arrow
- [ ] Edge labels are SHORT (1-3 words): `-- YES -->`, `-- error -->`

### Character Safety (Alignment)

- [ ] NO graphical emojis inside nodes (break alignment)
- [ ] Unicode symbols OK inside nodes (single-width)
- [ ] ASCII markers ALWAYS safe ([x] [+] [!] [OK])
- [ ] Graphical emojis ONLY in `graph { label: "..."; }` title

### Structure (Organization)

- [ ] Groups `( Name: ... )` used for logical clustering when 4+ related nodes
- [ ] Node IDs short, labels descriptive: `[db] { label: "PostgreSQL"; }`
- [ ] No more than 7-10 nodes per diagram (split if larger)

## Success Criteria

### Correctness

1. **Parses without error** - graph-easy accepts the DSL
2. **Renders cleanly** - no misaligned boxes or broken lines
3. **Matches content** - all key elements from description represented
4. **Source preserved (MANDATORY)** - EVERY diagram has `<details>` block with source

### Aesthetics

1. **Uses boxart** - clean Unicode lines, not ASCII `+--+`
2. **Visual hierarchy** - start/end rounded, important bold/double, optional dotted
3. **Consistent styling** - same border style = same semantic meaning throughout
4. **Readable labels** - multiline with `\n`, no truncation
5. **Clear flow** - direction matches natural reading (top-down or left-right)

### Comprehensiveness

1. **Semantic emoji in title** - emoji chosen to match diagram purpose
2. **Legend if needed** - multiline title with `\n` for complex diagrams
3. **Edge semantics** - solid=normal, dotted=conditional, bold=critical
4. **Logical grouping** - related nodes in `( Group: ... )` containers

## Troubleshooting

| Issue               | Cause                    | Solution                                                                         |
| ------------------- | ------------------------ | -------------------------------------------------------------------------------- |
| `command not found` | graph-easy not installed | Run [preflight check](./references/preflight-setup.md)                           |
| Misaligned boxes    | Used `--as=ascii`        | Always use `--as=boxart`                                                         |
| Box border broken   | Graphical emoji in node  | Remove emojis from nodes, use [ASCII markers](./references/monospace-symbols.md) |
| Nodes overlap       | Too complex              | Split into multiple diagrams (max 7-10 nodes)                                    |
| Edge labels cut off | Label too long           | Shorten to 1-3 words                                                             |
| No title showing    | Wrong syntax             | Use `graph { label: "Title"; flow: south; }`                                     |
| Weird layout        | No flow direction        | Add `graph { flow: south; }` or `flow: east`                                     |
| Parse error         | Special chars in node    | Escape or simplify node names                                                    |

## Resources

- [Graph::Easy on CPAN](https://metacpan.org/dist/Graph-Easy)
- [Graph::Easy Manual](http://bloodgate.com/perl/graph/manual/)
- [Graph::Easy GitHub](https://github.com/ironcamel/Graph-Easy)
