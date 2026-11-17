---
name: network-diagrams
description: Draw network topologies as code — Mermaid, PlantUML, Graphviz — L1/L2/L3, BGP, failover sequence, C4-style. Use when the user wants a diagram in markdown, an RFC embed, or a Lucid precursor. For Lucidchart itself, use lucid-diagrams.
origin: snm-pack
---

# Network diagrams (as code)

Prefer **text that diffs**. Stakeholder polish happens later in Lucid.

## When to use

- Topology, VRF, BGP, packet walk, cutover sequence
- RFC / Notion / Git embed
- "Show me the as-is vs to-be"

## Pick a language

| Need | Tool |
|------|------|
| Flow / sequence / simple L3 | Mermaid `flowchart` / `sequenceDiagram` |
| State of failover | Mermaid `stateDiagram-v2` |
| Host-heavy L2/L3 | PlantUML `nwdiag` or Graphviz |
| Control-plane | Mermaid flowchart, left-to-right |
| C4 of a network program | Mermaid C4 or PlantUML C4 |

Patterns: [reference/mermaid-patterns.md](reference/mermaid-patterns.md).

## Rules

1. Node IDs = hostnames (`mai_c_core_01`), labels can be pretty.
2. Show **failure domain** boundaries as subgraphs.
3. Annotate circuits: `carrier · ID · Mb`.
4. Mark NEW / REMOVE on cutover diagrams.
5. No credentials, no serials unless asked, no PHI.
6. One idea per diagram. Split L2 from BGP.
7. Always ship a 4-line legend under the fence.

## Packet walk (required for path bugs)

Emit a sequence diagram: client → access → dist → fw → dest, with
VLAN/VRF and the **decision** at each hop (route, policy, NAT). If a
hop is unknown, draw it as `UNKNOWN` — do not guess a platform.

## Output

Fenced diagram + legend + "promote to Lucid if this is going to CAB".

## Reference Files
- [reference/mermaid-patterns.md](reference/mermaid-patterns.md)
