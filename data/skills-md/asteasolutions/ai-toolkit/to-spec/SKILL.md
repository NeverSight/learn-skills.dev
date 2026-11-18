---
name: to-spec
description: Synthesize the settled conversation into a thin Plan on the work-tree leaf doc — no interview. Use when intent is pinned and you need a durable plan before building; helm's Plan phase reaches for this when the goal fits in one change.
---

# to-spec

Turn settled conversation into a **thin Plan**. Do **not** interview — grilling already happened; capture what was decided.

Shapes match helm's work-tree artifacts (see `helm/references/artifacts.md` if present).

## Publish policy

1. **Always write local** under `.scratch/<goal-slug>/` — this is the program counter.
2. **Also mirror to GitHub** only when the user asks for GitHub, or already pointed at an issue URL/id. If `docs/agents/issue-tracker.md` exists, follow its GitHub conventions for that mirror.
3. Never skip the local write. Never ask which tracker after a local-only run.

## Process

1. **Orient if needed.** If the touched area isn't already understood, explore it. Prefer any domain vocabulary / decision docs the repo already has; discover them — don't invent a layout.

2. **Sketch test seams.** Prefer existing seams; pick the highest seam that still exercises the behaviour; minimise their number (ideal: one). **Check seams with the developer** before writing.

3. **Write a thin Plan** into the leaf doc:
   - Undecomposed goal: `.scratch/<goal-slug>/task.md`
   - If Intent already exists (helm Capture), fill or replace only the `## Plan` section.
   - If starting fresh, write Intent (short what+why) + Plan.

   Thin Plan contents only:
   - what / why
   - test seams (how it will be verified)
   - implementation decisions
   - behaviour-level `done` criteria

   No brittle file paths or code. Exception: a decision-encoding prototype (schema, type, state machine) may be inlined when the shape *is* the decision.

4. **Ask once about extras.** After the thin Plan is written, ask whether to also include any of: user stories, out of scope, further notes (or other sections the developer names). Default is no. Add only what they pick.

5. **GitHub mirror (opt-in).** If publishing to GitHub, create/update the issue from the same Plan body. Local remains source of truth for resume.

## Leaf shape

```markdown
# <feature title>

## Intent
<what + why>

## Plan
<what/why · test seams · implementation decisions · behaviour-level done criteria>
<!-- optional extras only if the developer asked for them -->
```
