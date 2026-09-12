---
name: loop-converge
description: Author and optionally direct-launch a two-node loop-graph run whose North Star is code convergence — delete unused code, merge duplicates, reuse, slim. Use when the user invokes /loop-converge, or asks to loop on dead code, duplication, unused exports, DRY cleanup, or merging twin implementations. Starts the owner interview (scope / authority / launch) immediately; supervisor is required. Not for adding features or a one-shot tidy. Do not execute or resume existing runtime node files from this authoring skill.
---

# loop-converge — a loop-graph preset for slimming code

A thin authoring entry. It binds a code-convergence pack, starts the owner
interview, then follows [`loop-graph`](../loop-graph/SKILL.md) to compile a
normal two-node run (executor + supervisor). It is not a third runtime node
and it does not ship a second template set.

## Fit check

- Use this when unused or duplicate code will take many verified rounds to
  remove, merge, or reuse, and an independent audit should keep the bar from
  sliding into a rewrite.
- If the request is a one-shot tidy that fits a normal host task, say so and
  send the task directly. Do not wrap it in a graph.

## On invoke

1. Inspect the workspace and the current host the same way loop-graph does.
   Never ask which client this is when context already identifies it.
2. Read and bind [`preset.md`](preset.md). That pack **is** the North Star,
   the supervisor requirement, the method guards, the knob overrides, the
   recommended shape, and the detector hints. Do not redesign them.
3. Start the owner interview immediately. With this pack bound, ask at most
   the three questions the pack names — **scope**, **authority**, **launch
   mode** — each as a recommended A/B (or A/B/C) choice. Do not ask for a
   North Star. Do not offer to omit the supervisor.
4. Read and follow [`../loop-graph/SKILL.md`](../loop-graph/SKILL.md) from
   **When called from a preset skill** through generate and deliver. Compile
   only from loop-graph's [`templates/`](../loop-graph/templates/). This skill
   never executes the generated nodes.
