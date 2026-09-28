---
name: probe
description: Sketch the load-bearing architecture of a complex change as real code stubs - whatever decisions drive the rest of the work (schema, API surface, interfaces, data flow, module boundaries...) - without filling in implementation details. The user reviews and iterates on the skeleton interactively, then hands it to the "ship" skill to implement fully. Use when the user says "probe", "probe this", "sketch the architecture first", or wants to agree on the high-level shape of a complex change before full implementation.
---

# Probe

Sketch the skeleton of a complex change — the decisions that drive everything else — and stop there for review. No implementation details, no PRs, no review bots. Just: "here's the shape I'd build; do you agree?"

The point: in a complex change, a handful of decisions are load-bearing — the ones everything else gets built around. Get one of those wrong and every PR built on top inherits the mistake; undoing it means rewriting the stack. It's much cheaper to agree on the skeleton first, then let `ship` fill in the details.

For the really complex stuff, this is the middle stage of a three-skill pipeline: **`advisor` → `probe` → `ship`**. Advisor settles *what* to build and why (scope, approach, the product-level decisions); probe makes the agreed direction concrete as code (*where* things live, what shape they take); ship fills in the details and runs the review loop. Each stage is optional — plenty of changes skip straight to ship.

## What to probe

Probe shares its plumbing with `ship` — read that skill's SKILL.md and follow its "What's being shipped" section for interpreting the input (Linear ticket vs. plain-text ask, tool requirements) and its worktree setup. Same rules, same behavior.

The one entry flavor probe adds: the output of an `advisor` conversation — a spec, a shaped ticket, or just the decisions agreed in chat. Treat those as settled; don't relitigate them.

Probe is for changes complex enough to have real architectural decisions; if the ask turns out to be simple, say so and suggest going straight to `ship`.

## The skeleton

First figure out which decisions are load-bearing **for this particular change** — the ones that, if changed later, force a rewrite of everything built on top. What those are depends entirely on what's being built. For a web app it's things like the schema, the API surface, new pages, key types. For a CLI it might be the command/flag surface and the config format; for a library, the public API; for a pipeline, the stage boundaries and the shape of the data flowing between them; for infra, the resource topology. Persistent data shapes and public contracts are almost always on the list — they're the hardest to walk back. Where the logic lives (module boundaries) usually is too.

Then, in the worktree (per `ship`'s setup), write the **actual stubs** for those decisions, in real code, uncommitted: real signatures with typed params and returns, real schema/config changes, files in their real locations — bodies as `TODO` stubs, shells rendering placeholders. A new file with typed function signatures and empty bodies says more than a paragraph of prose.

Don't implement anything beyond what's needed to show the shape. No business logic, no edge cases, no tests. It doesn't need to pass CI — it needs to be reviewable. (Typechecking is nice if it's cheap; don't contort the stubs for it.)

Prefer code over prose, but decisions that don't show up well in stubs (e.g. "polling vs. webhooks", "denormalize or join") get a short bullet in the summary instead — with your recommendation.

## The review conversation

Present the skeleton: a compact summary of every load-bearing decision made — one line each with the *why* — pointing at the stub files. If a decision was a close call, say what the alternative was and why you picked this side.

Then iterate. The user pushes back, you adjust the stubs, re-present what changed. This back-and-forth is the whole product of the skill — don't rush it, and don't quietly expand scope while iterating.

## Handoff

When the user is happy, stop. Leave the stubs in the worktree, uncommitted, and remind them the next step is invoking `ship` — which will treat the skeleton as the agreed architecture and fill in the details from there. Don't start implementing, don't create branches or PRs, don't invoke `ship` yourself.
