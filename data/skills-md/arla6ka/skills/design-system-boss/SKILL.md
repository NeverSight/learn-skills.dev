---
name: design-system-boss
description: Use for vague whole-app design system asks on an app that already ships UI, like "our UI is a mess, fix it", "we need a design system", "we hardcode colors everywhere", "make the buttons consistent for an upstream PR", "document our whole design system" or "check the app before I ship". Triages the app, then runs the design.how skills in order. One named screen goes to ui-review, one component to component-docs, an empty repo to build-design-system.
---

# Design system boss

1. Resume from `.design-system/boss/state.md` if it exists (`references/state.md`, Resuming). Else run `scripts/triage.sh` (`references/triage.md`).
2. Pick the state, the intent and the foundation from the signals (`references/triage.md`). With `small_app yes`, take the fast path (`references/routes.md`, Small app).
3. Pick the route from the table below. It ends check-first unless the ask names the migration (`references/routes.md`, the rules at the top).
4. Pick the run branch, set the phase caps, probe the host, write the state file (`references/coordinator-path.md`, steps 6 to 9).
5. Send the Frame with every default applied. An unanswered question keeps its default as `default (unanswered)`, and the run goes on (`references/triage.md`, The one question).
6. Run the route's steps through subagents, one writing step at a time (`references/delegation.md`). Decided defaults land before any docs are written.
7. Check each return on its files and record a verdict (`references/delegation.md`, Checking a return).
8. Close: triage again, the clean-clone check, captures, then `close.md` and one found-not-fixed table (`references/state.md`).
9. Send the Report section as the final message, unanswered defaults first and the migration offered with its size.

Never ship:

- Product code written by the boss on a host that can spawn subagents.
- A migration past the safe moves without clearance, or a "fix it" read as clearance.
- A docs or spec commit made before the decided defaults landed.
- A new visual direction nobody chose through the design-source question.
- A number in the report that no row in `close.md` holds.
- A handback with a worker still running.
- A run that waited or stopped on a question it had a default for.

When the boss runs as a subagent, it spawns workers as foreground calls, several in one message to run them side by side, and never ends its turn with a background worker live. A worker left running keeps writing into a repo nobody checks.

The five siblings do the work: `build-design-system`, `migrate-design-system`, `token-mapping`, `ui-review` and `component-docs`, each called through its "When a coordinator calls it" section. Sibling paths start at `<skills>`. Terms such as surface, gate, clearance and the status words mean what `build-design-system/references/run-record.md` (Terms) says, and its standing orders bind the boss too. Read `references/coordinator-path.md` first. It lists each step and the file to open.

## Output

Done means the route's last step has returned, every step has a status and verdict in `.design-system/boss/state.md`, and the report is written from files. Checkable:

- `triage/signals.tsv` and `triage/after/signals.tsv` came from `scripts/triage.sh`, and the route is the routing table's, or a decision row says why it differs.
- Every step has a verdict naming the file that proves it. Every number in the report is a row in `close.md` with its unit and source.
- Every gate from every sibling record is in the state file's Gates table (`references/state.md`, The state file), and every unanswered one reads `default (unanswered)`.
- On a writing route, the check exits 0 on a clean clone of the run branch, or the repo's own lint, typecheck and build do on a minimal footprint. Every changed surface has captures and a montage row, every identical-value swap has its proof, and every pilot trap is fixed with numbers or gated with its measurement. `git status` before and after is saved, `.design-system/tmp/` is gone, and every untracked path is committed or named in a decision row.
- The report ends with one Found, not fixed table, ranked, at most 30 rows.

Your final chat message is the state file's Report section, verbatim (`references/state.md`, The handoff report). If a stop condition below holds, return the condition, what finished, the state file path, and the smallest reply that unblocks it, such as "Say which app: apps/web or apps/admin."

## Inputs

| Input | If missing |
|---|---|
| The ask | Required. "Our UI is a mess" is enough |
| The repo | Stop without one. Read-only access allows only Audit and Review |
| Target app, in a monorepo | The one question, default the app with the most routes. Triage every app meanwhile |
| Intent | From the ask's words, per `references/triage.md` |
| Budget | The Frame's `Go, <budget>` reply, else the host's session, else 2 hours, split per `references/routes.md` (Budget) |
| The sibling skills | In `<skills>`. A missing one stops only its steps, and the report names it |
| Subagents, a browser, a shell | Probe per `references/delegation.md` |
| AGENTS.md or CLAUDE.md, the person's words, saved memory | They win over every skill default, branch and push policy included. "Work on my current branch" makes it the run branch. Pass them into every brief |

## Clear the migration

Clearance comes from an ask that names the migration or a reply to the handoff's offer (`build-design-system/references/run-record.md`, Terms). A fallback intent and a complaint such as "fix it" never count. With clearance, migrate edits only after its audit `plan.md` is re-pinned and reconciled with the build's `registry.json`, and migrate's rolling window runs inside the machine budget on disjoint paths. Without it, the route ends check-first. An ask mid-run follows `references/routes.md` (the rules at the top).

## Routing table

State, **weak** and intent come from `references/triage.md`. `references/routes.md` has each route's steps. Copy them word for word, and keep a dropped step listed as `skipped (<reason>)`.

| State | Intent | Route |
|---|---|---|
| empty | any | Seed |
| none, or drifting and not weak | build | Build |
| drifting, weak | build | Harden, stated in the Frame |
| any, with a PR or upstream in the ask | named families | Named families, minimal footprint. Wins over every row below |
| drifting or settled, weak | full, harden, adopt | Harden, then Full from step 5. A values intent runs Values first. Wins over later rows |
| none, drifting or settled, not weak | harden | Harden. With no `harden_dirs`, Build |
| none or drifting, not weak | full | Full |
| settled or documented, not weak | full, adopt | Adopt |
| drifting, not weak | values | Values |
| settled | docs | Document |
| any | component | Component |
| any | review | Review |
| any | audit | Audit |

When the ask mentions a PR or upstream, or the repo looks like someone else's, the route runs as `<route>, minimal footprint` (Footprint in run-record Terms). When the ask and the state disagree, the state wins and the Frame says so. "Migrate us" on state `none` is Build.

## Boundaries

May decide the route, run branch, phase split, which read-only steps run side by side, one retry of a failed step, defaults for any sibling input the ask left out, and skipping a step whose output is current, citing its record.

Ask, with the default applied, and go on:

- A dirty checkout or someone else's branch on a writing route. Default: the run branch in its own worktree from HEAD, so the checkout stays as found. Never stash.
- Read-only access on a route that writes. Default: Audit.

Stop only when there is no repo, or a sibling returns its stop shape and the next step needs its output.

Never loosen a sibling's predicate or edit a sibling skill. "Make it modern" with no design source becomes a gate with the default "keep the current look" (`references/triage.md`, Standing questions).
