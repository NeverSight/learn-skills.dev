---
name: migrate-design-system
description: Use when an app has to move onto a design system that already exists, such as "migrate the app to our design system", "move every screen onto the new components", a rollout, or an adoption audit. When design-system-boss is installed and nobody has checked the system's specs, the boss triages first, since a migration copies a weak system's gaps everywhere. Not for making the system.
---

# Migrate to a design system

1. Pick the mode. Full mode runs only when the ask names the migration or the person accepted an offer (`build-design-system/references/run-record.md`, Terms). Anything else is audit mode.
2. Frame: write `frame.md` and `standing-orders.md` with every default applied (`references/run-folder.md`).
3. Inventory, mapping and parity, read-only (`references/inventory.md`). Audit mode ends here with `plan.md`, its found-not-fixed table and the offer.
4. Baselines before any edit (`references/verification.md`, Baselines).
5. The shared layer, one agent, alone (`references/inventory.md`, The shared layer).
6. The pilot end to end, then the codemod from its recipe (`references/worker-brief.md`).
7. Fan out in a rolling window, one surface per worker, each verified by another agent (`references/orchestration.md`, `references/verification.md`).
8. Land each verified surface as its own commit, then close with `close.md` and one found-not-fixed table (`references/run-folder.md`, close.md).

Never ship:

- An edit in audit mode, or full mode started on a vague ask such as "clean the app up".
- A surface landed without a verifier that did not write it.
- A token, component, prop or variant invented to fill a gap.
- A behavior change passed off as part of the migration.
- A legacy module kept alive after its last caller moved, unless a gate names an owner and a removal date.
- A red check, or a relaxed predicate, at handoff.

When this skill runs as a subagent under another coordinator, it spawns workers as foreground calls, several in one message so a wave still runs side by side, and never ends its turn with a background worker live, because the host orphans or kills that worker when the step agent hands back. The drain comes after the whole wave returns.

The system is settled. One coordinator splits the app into surfaces and runs worker agents one surface at a time, with behavior unchanged. Sibling skill paths start at `<skills>`. Surface, run branch, identical-value swap, decision, gate, clearance, footprint, the status words and `<skills>` mean what `build-design-system/references/run-record.md` (Terms) says. It never designs the system. A missing token or component is a request to the system's owner. It does not deploy unless the standing orders grant it. No editing worker starts before `frame.md` states a budget.

A writing run lands every surface, and every decided gate default, on the run branch (`ds/<yyyy-mm-dd>-migrate` unless one is named), so Next is a plain merge. Each visible change needs a gate or decision, before and after captures and a montage row (`references/verification.md`).

## When a coordinator calls it

A coordinator passes the mode, the system location, scope, pilot, budget or a run folder. Use what it gives, default the rest from Inputs, and park questions in `gates.md`. An unanswered gate takes its default as `default (unanswered)`, and the run never waits on one. A boss that takes this seat on a host without subagents records that as one decision row. The reply starts with the status line, then `Commit: <run branch head>`, then the final report, `plan.md` in audit mode, or the stop shape below. Audit mode can run beside the build (`references/inventory.md`, Audit mode and plan.md).

## Done

Done means the predicate in `frame.md` holds on the final integration commit, proved from the run folder.

- The inventory script's `--check` exits 0 there: zero legacy imports, zero raw values outside `allowlist.tsv`, zero palette uses when `frame.md` counts them, zero legacy files.
- Every row in `queue.tsv` is `done` with a `verified` or `self-verified` ledger row at that commit. A verdict at a surface's branch commit or a reopened row does not count.
- The rule that blocks new legacy usage fails CI on a planted violation, and exits 0 at every handoff with the remaining findings in its committed ignore list (`references/inventory.md`). A red check at handoff is a failed run.
- `baselines/MANIFEST.sha256` still matches, and the forbidden-path check passed on every landed diff.
- Every spawned agent has a terminal row in `agents.tsv`, and every `decisions.tsv` row points at evidence that resolves.
- Every fix that recurred became a check, or the report says why it could not.
- No gate reads `todo`: each is `done`, `default (unanswered)`, `gate` with its default listed, or `skipped (<reason>)`.

The first commit that changes a surface fixes the complaint quoted in `frame.md`, and every claim names its command. The final message is the handoff in run-record (Handoff report), with migrate's counts and Next from `close.md`, unanswered defaults first and the Found, not fixed table last. If it stops, return the rule that stopped it, the count verified so far, the run folder path, the first action on resume, and the smallest reply that unblocks it.

## Inputs

| Input | Required | If missing |
|---|---|---|
| The target system: token source, components, docs, and a version or commit | Yes | Find it per `references/inventory.md` (Finding the target system) and pin the commit in `frame.md` |
| The app repo, able to build and run | Yes | Stop if it cannot build, except in audit mode. If it cannot run, offer audit mode only, since nothing can be verified. |
| Mode | No | Audit, unless the ask names the migration |
| Scope | No | Everything the inventory finds, listed in `frame.md` for the person to trim |
| Pilot surface | No | The one the person complained about, else the one with the most system components and a failure state |
| Budget | No | The session, stated in `frame.md` |
| Widths and themes | No | The app's narrowest and widest widths, default 390 and 1280, and every theme it ships |
| Parity mode, `exact` or `mapped` | No | `mapped` when system values differ from legacy ones (`references/verification.md`) |
| Parallel agents with worktree isolation | No | `references/platforms.md` |
| A visual test harness | No | `capture.mjs`, run in the CI environment |

Project instructions (AGENTS.md, CLAUDE.md) seed the standing orders. With 8 surfaces or fewer, the small-app line in `build-design-system/references/coordinator-path.md` (Small app), one worker runs the phases in sequence, still with the inventory, baselines, ledger and predicate, because a window costs more than it saves.

## Procedure

Read `references/orchestration.md` and `references/run-folder.md` before Frame. Inventory is read-only and starts while Frame is written. Each step exits when the run-folder file its reference names proves it.

1. **Frame.** Exit when every field is filled or has a stated default, before any spawn.
2. **Inventory.** One agent builds or reuses the inventory script and the lint rule that blocks new legacy usage, and mappers run `token-mapping` per surface. Ambiguous rows become gates. Exit when `inventory/counts.txt` has the counts, every finding has a surface, and the rule fails on a planted violation. Audit mode adds no rule.
3. **Parity.** One read-only agent gives every legacy call site a verdict in `parity.tsv`. A blocking gap stops the whole fan-out until it closes. Audit mode writes `plan.md` here and stops.
4. **Baselines.** Exit when every surface has a baseline or a stated `not captured` reason, and the manifest is written.
5. **Shared layer.** Exit when the layer has landed, the runtime checks pass, and every baseline still matches or its diffs are explained.
6. **Pilot.** Worker, verifier, ledger row, landing. Fix what it exposed in the template. Exit when the pilot is `verified` and landed.
7. **Build the codemod.** Run it on the pilot's starting commit and diff the result against the hand migration. Exit when that diff is recorded and a second run is a no-op.
8. **Fan out.** A rolling window under the cap in `frame.md`, one surface per worker, each with its own branch and worktree (or the fallback in `references/platforms.md`). Stop spawning at about 70% of the budget.
9. **Verify each surface.** A verifier that did not write the code checks the visual diff, rendered checklist, accessibility snapshot, behavior and its delta, and runs `ui-review`. Exit per surface when the ledger has a verdict for its current commit.
10. **Integrate continuously.** Land each verified surface as its own commit with its captures, then run the integration checks. A red integration build stops landing until it is green.
11. **Delete legacy.** When a legacy module has zero callers, one unit deletes it, its adapter and its allowlist rows in one change, and the lint rule bans the path.
12. **Close.** A last drain, recapture every surface at the final integration commit, write `close.md`, audit `decisions.tsv`, turn each recurring fix into a check, and clear scratch files.

## Boundaries

The coordinator never writes product code when it can spawn subagents. On a host without subagents it runs the phases itself, in sequence, and self-verifies per `references/verification.md`.

Decide and log, without asking: the surface split and order, window size under the cap, retries and splits (`build-design-system/references/coordinator-path.md`, Dev server and retries), which verifier runs, clean landings, brief or codemod fixes the evidence supports, identical-value swaps on any surface, decided gate defaults, and adds-only accessibility changes (`build-design-system/references/traps.md`, Adds-only accessibility changes).

Park in `gates.md` with a default and keep working. Mapped pixel changes, color moves, component swaps and codemods on non-pilot surfaces are gates whose defaults land on the run branch with captures. These gates default to leaving the code as it is: a token or component the system lacks; a visual diff nobody can explain, or a change that removes, renames or restructures semantics; a `blocking` `ui-review` finding already in the baseline (the surface still verifies); a behavior change of any size; a standing order the code contradicts; a dead end that survived one replan; deleting data or an export used outside the repo.

Never let two workers edit the same file, or any worker touch the shared layer after its phase. Never count `checks-only`, `blocked` or a self-report as verified, or let a decision row stand in for a verifier.
