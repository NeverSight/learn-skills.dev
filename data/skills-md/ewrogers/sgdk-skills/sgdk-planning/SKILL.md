---
name: sgdk-planning
description: Turn a Mega Drive game idea or feature into playable milestones and a hardware-aware SGDK plan. Use for scope, resource budgets, feasibility probes and growth paths before implementation.
---

# SGDK planning

Help the developer choose the next playable proof, understand its hardware
risks, and leave room for the game to grow. Produce a useful plan for an
ordinary SGDK project, not a new engine or a generic game-design document.

## Find the smallest useful proof

Read the request and existing project decisions first. Ask only about choices
that materially change the initial proof, such as the core mechanic, target
region, simultaneous players or a required cartridge. Record reversible
assumptions and proceed instead of making the developer answer a fixed survey.

Describe what the player will see and do in the first milestone, including how
to tell whether it works. Keep the intended game recognizable while reducing
content. A scrolling game needs an early scrolling proof; a busy shooter needs
an early crowded-screen proof. An empty screen reaching 60 Hz proves neither.

Use [the planning workflow](references/planning-workflow.md) for examples of
scoping milestones, exposing assumptions and choosing feasibility checks.

## Budget the busiest useful moment

Read [hardware budgets](references/hardware-budgets.md) for the relevant
constraints. Keep hardware ceilings, SDK reservations and project targets
separate. Account for these independently:

- Main RAM, including SDK state, game state, buffers, heap and stack.
- VRAM residency, including patterns and all VDP tables.
- Shared palettes, hardware sprite pieces and worst-case scanline overlap.
- ROM content, final padding and any deliberate mapper requirement.
- Peak transfers/decompression and CPU work per update.

Label figures **measured**, **estimated** or **unknown** and state their basis.
Do not invent a CPU percentage, a universal safe entity count or a fixed amount
of free SGDK memory. Choose project headroom based on the proposed workload;
spare RAM cannot fix a scanline or palette overflow.

For a useful static calculation, optionally create a worksheet and use the
bundled [budget checker](scripts/budget_check.py). Its
[format and limits](references/budget-format.md) explain what it can check.
It does not measure timing or prove that a game is feasible.

```sh
python3 /path/to/sgdk-planning/scripts/budget_check.py budget.json
```

## Verify risky assumptions

Planning does not require Docker to be running. Use sourced hardware facts and
mark untested SDK or workload assumptions honestly. Before committing to an
unfamiliar API or resource behavior, inspect the project's installed SGDK headers,
implementation, resource manual and matching sample. Use the Docker image and
verification guidance in [hardware budgets](references/hardware-budgets.md#verify-the-selected-sdk).
Do not silently upgrade an existing project or guess an API from another SDK.

Put the highest-risk assumption in a small feasibility probe. Match its display
mode, update rate, asset sizes and peak workload to the planned game. Build
optimized release code for performance checks. A successful build proves
compiler/resource compatibility; visuals, controls, audio and timing still
need emulator or hardware checks. Report only validation that actually ran.

## Leave a plan someone can use

Adapt [the game-plan template](assets/game-plan.md) to the request. Remove
irrelevant sections and keep the summary readable without hardware expertise.
Include the first playable milestone, the next growth step, relevant budgets,
unresolved risks and a concrete way to settle each risk.

If a budget does not fit, offer choices that preserve the game: share graphics,
change the busiest formation, stream a map, alter an upload strategy or reduce
optional effects. Explain the tradeoff before proposing a lower update rate or
a different cartridge. Do not silently remove required behavior, claim that
banking solves RAM, or turn a planning request into an implementation rewrite.
