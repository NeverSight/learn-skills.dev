---
name: capability-map
description: Decompose one requirement that bundles several independently testable capabilities into a small module table with stable ids, one-way dependencies, and a build order, approved before any spec or design is written. Use when a request names distinct capabilities with their own consumers or data (identity, billing, notifications, reporting), when acceptance criteria cluster into groups that could ship and be verified separately, or when the user asks how to architect or split a system. Do not use for a single capability; go straight to its design. Do not use to chart open decisions or split a spec into tickets; that is effort-charting.
---

# Capability Map

Most requests describe one capability and need no map. The exception is a
request that bundles several: a monolithic spec then forces every downstream
task to reason over the whole contract, and module boundaries get decided
implicitly, mid-implementation, by whoever touched the code first. A ten-line map
reviewed up front is the cheap alternative.

## Detect

Decompose when at least one holds:

- the requirement names capabilities with their own consumers or their own data;
- the acceptance criteria cluster into groups that could ship and be verified
  separately;
- one capability could be cut or replaced without rewriting the others'
  requirements.

If none holds, say so and skip the map.

## Propose the map

Small and reviewable: a module table plus a build order, not a project plan.

```markdown
# Capability Map: <initiative>

| Module id | Responsibility | Depends on |
| --- | --- | --- |
| identity | accounts, sessions, SSO | — |
| billing | plans, invoices, payments | identity |
| notifications | email and webhook fan-out | identity |
| reporting | usage dashboards | billing, notifications |

Build order: identity → billing, notifications → reporting
```

- **Stable ids.** Kebab-case, chosen once, never renamed mid-initiative; specs,
  tickets, and reviews select work by id instead of guessing which document is
  current.
- **One-way dependencies, no cycles.** If two modules each need the other, they
  are one module; merge them rather than adding an indirection to break the loop.
- **Interfaces live at the boundary.** The map records that `billing` depends on
  `identity`; the contract between them belongs to the provider's design, not to
  the map.
- **Build order is topological.** Every module appears after everything it
  depends on; independent modules on the same line can be built in parallel.

Every `Depends on` id names a module in the table.

## Gate, then recurse

The user reviews module boundaries, dependency direction, and build order before
any module is specified; getting the map wrong is expensive and reviewing ten
lines is not. Once approved, save the map at the project root and design each
module in build order, one spec per id named by that id, scoped to that module's
objective, boundaries, and success criteria. The map, not filename guessing, is
the index of what exists. When a later design shows the map was wrong, change
the map first and say what moved.
