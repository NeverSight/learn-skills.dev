---
name: ro-engineer
description: "Build, debug, review, and design Roblox/Luau gameplay systems. Use for project integration, remotes, persistence, lifecycle, architecture, profiling, or gameplay loops."
---

# Ro-Engineer

Inspect existing project code before proposing systems: relevant scripts,
dependencies, call sites, remotes, persistence, and lifecycle conventions.
Reuse suitable interfaces and libraries. Keep unrelated systems intact; a
small fix does not need a new architecture or a game-design phase.

## Available evidence

- **Studio:** use available MCP capabilities to identify the right place,
  read scripts and callers, edit narrowly, run applicable tests/playtests,
  and inspect console results. Select the target if multiple places are open.
- **ROTEX:** retrieve relevant system/library documentation and interfaces
  before integrating them. Use validation if exposed; report what it checks.
- **Repository:** inspect/edit local project files and use configured tooling.
  Filesystem access does not imply access to the running place.
- **Offline:** use supplied code; state assumptions, placement (service/path
  and Script, LocalScript, or ModuleScript), integration points, and manual tests.

Capabilities can combine. Detect actual tool descriptions and permissions;
names and read/write/validation support vary between MCP implementations.
Installing this skill grants no Studio or ROTEX connection. Never invent
inspection, execution, or test results. Read [tool modes](references/tool-modes.md)
when choosing a target, connecting tools, or handling partial access.

## Load only needed detail

Start with relevant project files. Load references when their detail is needed;
the table is not a bundle to read in full. Templates are optional.

| Task | Start here |
|---|---|
| Small fix / simple module | Project code; [implementation](workflows/implement.md) if useful |
| Plan requested / substantial multi-system work | [planning](workflows/plan.md) |
| New system / significant architecture change | [system design](workflows/design-system.md), then [pattern selection](references/pattern-selection.md) |
| OOP / composition / ECS | Only the relevant [OOP](references/oop-patterns.md), [composition](references/composition.md), or [ECS](references/ecs.md) reference |
| Remotes / trust boundary | [client/server security](references/client-server-boundaries.md); [transport](references/networking-remotes.md) as needed |
| Replicated state | [state management](references/state-management.md) |
| Cleanup / respawn / streaming | [lifecycle](references/cleanup-lifecycle.md) |
| Performance problem | [performance audit](workflows/performance-audit.md); [pooling](references/object-pooling.md) if relevant |
| Review / validation | [review](workflows/code-review.md) / [testing](references/testing.md) |
| Luau API / typing issue | [Luau conventions](references/luau-modern.md) / [types](references/luau-types.md) |
| Known failure modes | [sharp edges](references/sharp-edges.md) |
| Player loop / reference-game analysis | [loop design](workflows/design-game-loop.md) |
| Retention / onboarding | [incentives](references/player-incentives.md); [retention audit](workflows/retention-audit.md) for a review |
| Economy / progression / events | [economy](references/progression-economy.md), [economy audit](workflows/economy-audit.md), or [events](references/live-ops-events.md) |

Keep game-design references out of unrelated engineering work. For significant
architecture choices, briefly explain fit, trade-offs, and relevant alternatives.
Consider existing architecture, scale, update rate, target devices, maintenance,
integration cost, and available tests. Counts alone do not justify ECS or pooling.

## Roblox safeguards

- Keep gameplay outcomes, economy, inventory, and grants authoritative on the
  server. Validate untrusted requests for type/shape, finite numbers, bounds,
  ownership, legal state, distance where relevant, and rate limits. Typed
  payloads do not replace runtime validation.
- Make purchase grants idempotent and durable through supported server receipt
  processing. Handle save failures, retries, concurrent requests, session
  ownership, and migrations without losing or duplicating progress.
- Assign resource ownership and lifetimes. End subscriptions, delayed work,
  and instance ownership when their owner ends; reset pooled state before
  reuse. Account for respawn, player departure, and client streaming.
- Prefer typed public interfaces and `--!strict` for new Luau where compatible;
  preserve project contracts. A ModuleScript returns exactly one non-nil value,
  which need not be a table. Use supported APIs and project conventions.
- Check current Roblox policy for paid randomness, trading restrictions, or
  purchase pressure. Preserve honest odds and player choice; avoid manipulative
  pressure, particularly on young players.

Scale planning and validation to risk. Continue authorized implementation;
ask only for material missing requirements or actions outside scope. A plan-only
request ends with the plan. Report changes, checks actually run, and unverified
behavior. Distinguish static review, types, runtime tests, security, and profiling.