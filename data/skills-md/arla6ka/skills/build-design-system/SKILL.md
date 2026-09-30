---
name: build-design-system
description: Use when an ask names one phase of design system work, such as "extract tokens from the app" or "add states and specs to our Button", or for an empty repo, such as "start a design system from scratch". A whole-app ask on a shipped app ("we need a design system") goes to design-system-boss when it is installed. Moving an app onto an existing system is migrate-design-system.
---

# Build a design system

1. Frame the run: mode and foundation, the base reference, the pilot, the Frame questions with defaults applied, the run branch and `.design-system/run.md` (`references/modes.md`, `references/run-record.md`, `references/coordinator-path.md` Start).
2. Size it: the small-app path, or fan-out inside the machine budget read from memory pressure (`references/coordinator-path.md`, Small app and Machine budget).
3. Inventory with scripts, and capture every surface before any edit (`references/inventory.md`, `references/browser.md`).
4. Tokens named by purpose: identical-value swaps, merges inside tolerance as decisions, a gate defaulting to the merge past it (`references/token-architecture.md`).
5. Components: the most-used family end to end, then the rest fanned out (`references/component-contract.md`, `references/rule-method.md`, `references/worker-brief.md`).
6. Checks that fail on seeded violations, a ratchet and two CI tiers (`references/checks.md`).
7. The pilot flow on the system, compared with its baseline and reviewed (`references/browser.md`).
8. The safe moves outside the pilot, and migration only with clearance (`references/coordinator-path.md`, Clearance).
9. Docs, generated twins and the AGENTS.md index (`references/system-structure.md`).
10. The handoff: close numbers, unanswered defaults first, the found-not-fixed list (`references/run-record.md`, Handoff report).

Never ship:

- A color, font, shadow, gradient or motion value the app does not have, unless the person chose a design source and confirmed the sample (`references/modes.md`).
- A commit on the starting branch, a push, a publish or a deploy.
- An edited baseline, fixture or check. Fix the code instead.
- A change outside the pilot that is neither a safe move nor a cleared surface.
- An accessibility or contrast result read from source instead of rendered output.
- A count no script produced, or a check never seen failing.
- One of the person's bans anywhere but a `Don't:` line.

It calls `token-mapping`, `component-docs` and `ui-review` instead of restating them. The base reference for the foundation (`references/base-*.md`) wins over the general references.

## When a coordinator calls it

A coordinator may hand over the target, pilot, budget, run branch or run record path, and the rest defaults from Inputs. Write gates to the run record instead of asking, and return the handoff report or the stop shape. Start the reply with the status line, then `Commit: <run branch head>`. Under design-system-boss, the boss's rules and caps govern. As a subagent, run workers as foreground calls and never return while one runs.

## Done

The run ends check-first (`references/modes.md`). The phase 1 predicate holds, with every number measured in phase 8: "N canonical components cover M inventoried families, every token has a role, the checks fail on seeded violations and exit 0 on a clean clone, and the pilot matches its baseline except for the listed intended changes." Report a failing part as failing. Never loosen it.

- Every token states its role, and every safe move is made and proven (`references/run-record.md`, Terms).
- Every canonical component the pilot uses has a registry entry and a spec that passes `node scripts/check-spec.mjs docs/system`, with 0 plain entries skipped among registry components.
- The full check exits 0 on a clean clone, every rule was seen failing its bad fixture this session, and every route answers 200 on the production build.
- Every difference in the pilot's captures, and every commit outside the pilot, traces to a decision or gate.
- The handoff report follows `references/run-record.md`, with every count from `.design-system/close.md`.

The rest of Done, per mode and footprint, is in `references/coordinator-path.md` (Close). If it stops, return the condition, finished artifacts, the run record path and the smallest reply that unblocks it.

## Inputs

Fill each row from the repo or its default, and never ask for paths.

| Input | If missing |
|---|---|
| The repo, with write access | Stop. A system built from screenshots has no code to enforce it |
| A way to run the app | Try the `dev` or `start` script. If nothing starts, run phases 3, 4, 5 and 7 from code, skip the pilot and report "code-complete, not runtime-verified" |
| Target app, in a monorepo | The Frame's one target question (`references/run-record.md`, Questions). Meanwhile run phase 2's read-only scripts on every candidate |
| Pilot flow | The screen the complaint names, else the flow that uses the most families and has a form with an error state, ties going to a `high` tier flow, else a pattern page (`references/modes.md`) |
| Budget | The Frame's "Go, <budget>" reply, else the host's session, else `references/coordinator-path.md` (Phase caps) |
| Themes | The ones the app ships, and no new ones |
| Mode and foundation | From the router's triage, else `references/modes.md` |
| Existing tokens, library, design spec or brand | Start from it per the base reference and `references/modes.md` (What decides a question) |
| The person's words and saved memory, AGENTS.md, CLAUDE.md | They win over this file, branch and push policy included |

It needs a shell, git and Node.

## Procedure

Other files cite these phase numbers, not the list at the top. Each phase ends with its artifact path and a decision row, and stops at its cap (`references/coordinator-path.md`, Phase caps). After any shared UI or token edit, `capture.mjs --status` must show every route loading (`references/browser.md`).

1. **Frame.** Read the agent instructions, manifest, style entry points, theme providers and route tree. Write the complaint in the person's words and the first visible change that answers it, the predicate with blanks for counts, and the standing orders. Viewports are the narrowest and widest widths the app supports, default 390 and 1280 px. Set up the footprint and run `node scripts/check-system.mjs --init`, then settle Lock before fan-out. Start phase 2 without waiting.
2. **Inventory.** Run the scripts, then list every surface with its states and tier and capture them with one `capture.mjs --kind before` command. Record the animation lists and measure the pilot's traps. Group families, mark duplicates, run the rendered-style pass in `references/traps.md`, and delete what nothing uses in its own commit (`references/inventory.md`, Delete plan). Unless a coordinator did, start `migrate-design-system` in audit mode, read-only, right after the token commit.
3. **Foundations.** Cluster raw values by category and role into semantic tokens with surface and foreground pairs. Merges inside `token-mapping`'s tolerances are decisions. Past tolerance, open one gate per cluster whose default is the merge, naming the largest shift and the screens it touches, and apply every default in the token files now. Write the generator if the setup has one. Run `token-mapping` on the full inventory until every raw value maps to a role, a merge or a listed exception. Make every identical-value swap on every route, and give a route that changed to the migration map. Write the AGENTS.md block, name the motion presets and icon sizes, and start the live showcase when the person reviews in a browser (`references/system-structure.md`).
4. **Components.** Pick each canonical implementation by the contract. When the ask names states, every component gets its missing states. Build the most-used family first, end to end in one commit: component, tests, showcase page and spec with its rules. Show its page before fan-out. Write its old-to-new map and a codemod that matches a hand-moved pilot screen, or record why there is none. Fan out the families the pilot and the strays touch, and reject any diff outside a brief's scope. Deprecate replaced wrappers, never a stock foundation component. Close per `references/coordinator-path.md` (Components close).
5. **Checks.** Follow `references/checks.md`. The check exits 0 before phase 6. Prove the shipped rules with `node scripts/check-system.mjs --self-test --fixtures <skills>/build-design-system/fixtures/check-system`.
6. **Pilot, then safe moves.** Move the pilot with the codemod, reading every hunk. Capture after with the baseline's viewports, themes and data. An untraced difference is a defect, and a rendered change with no capture reports `checks-only`. Walk the flow by keyboard, trigger its error and loading states, and measure every trap before and after. Run `ui-review` on the after captures. Fix as decisions what existing tokens and components can fix, and broken behavior. The rest are gates. Then land the safe moves one surface per commit (`references/coordinator-path.md`, Surfaces on the run branch).
7. **Docs.** Run `component-docs` for any canonical component still without a spec. Write the foundation pages, the shared state patterns (`references/system-structure.md`) and the writing page (`references/writing-method.md`). Run `node scripts/gen-docs.mjs`, with `--name` on the first run, and add `copy-check.mjs` to the check once `docs/system/writing.md` exists. Then Review, decide, fix (`references/coordinator-path.md`), and regenerate.
8. **Handoff.** Rerun the inventory scripts, grade each component and fill the predicate. On a full footprint, write the project skills. Run the fresh-agent trial and close per `references/coordinator-path.md` (Close).

## Boundaries

Stop and ask only for these:

- No repo access.
- A deletion that touches something another package or a public API exports.
- A step git cannot undo, such as publishing a package or changing a shared remote.

Gate with a default and keep working, even when nobody answers:

- A brand color, typeface or logo value the code states two ways.
- A name that carries a product word, such as "Plan" or "Workspace".
- A merge past tolerance, or a removed variant that changes a shipped screen.
- A conflict between code and a spec or old docs that no project rule settles.
- A change to a link's color or underline, listing every surface it touches. Links in main content keep a resting cue.
- The footprint, when the repo looks like someone else's or the ask mentions a PR or upstream. Default minimal (`references/coordinator-path.md`).
