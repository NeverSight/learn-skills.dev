---
name: fight
description: "You MUST use this to run substantial work in this repo's workflow. The goal is to be the single coordinator (chiefmate): own the sequence Brainstorm -> Roadmap -> Design -> Plan -> Development (loop) -> Deploy, the gates, subagent dispatch, and the loop state. You are not allowed to skip a gate or the loop. Skip it for a question, reading code, or a trivial fix. Trigger phrases: fight mode, /fight, run the workflow."
argument-hint: "Optionally: the task, or 'continue'."
---

# Fight Mode

Fight mode is the **spine** of the workflow: it owns the sequence, the gates, the rules, and the state, and it turns the agent into the project's one and only coordinator. It does **not** own how each phase is done — that lives in the phase skills it dispatches to.

You are the chiefmate: you run the ship, you don't do every job by hand. You delegate exploration, implementation slices, and review, and you own integration, final verification, and the response to the user.

## The Model

| Thing       | What it is                                             | Where it lives                       |
| ----------- | ------------------------------------------------------ | ------------------------------------ |
| **Spine**   | Phase order, gates, rules, state. This skill.          | `skills/fight/`                 |
| **Phase**   | A stage of the workflow, each with its own skill.      | `skills/<phase>/`                    |
| **State**   | Live cursor: which phase / feature is current.         | `specs/_state.md`                    |
| **Roadmap** | Features grouped into phases. The _order_.             | `specs/_roadmap.md`                  |
| **Ledger**  | Landed PRs, tagged by phase / feature / task.          | `specs/_status.md`                   |
| **Design**  | How it fits together (system + UI). The _shape_.       | `docs/architecture/`, `docs/design/` |
| **Tasks**   | Atomic work per feature, with its tests. The _slices_. | `specs/NNN-slug/tasks.md`            |

The roadmap and tasks track _what_ and _how far_; `specs/_state.md` tracks _where we are now_, and `specs/NNN-slug/status.md` holds one feature's `cycle` (the loop's memory). `specs/_status.md` is a plain ledger of what has landed.

## When to Use

- The user says "fight mode", invokes `/fight`, or asks to run the workflow.
- Any substantial change: a feature, a component, a behavior change.
- You're about to write code and no spec/roadmap/design/plan gate has been passed yet.

**Do NOT use** for a question, reading/explaining code, or a trivial unambiguous fix the user fully specified — just do it.

## Operating Rules

These come from `AGENTS.md`; fight mode enforces them, it doesn't restate their detail.

- **Business logic lives in the service layer.** Never in controller/interface.
- **Small commits, Conventional Commits** (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).
- **One feature = one branch (`feat/NNN-slug`) = one PR.** Diffs under ~300 lines.
- **Tests when behavior changes.** Write the test first when possible.
- **Type hints, no bare `except`, structured logging.** Concise comments.
- **Boundaries (never):** commit secrets or edit `.env`; edit existing migrations; add a dependency without asking; force-push; **push directly** to `main`/`master` (land via a reviewed MR instead); merge or deploy without approval.

## Subagent Policy

You are the coordinator. For each task in `tasks.md`, dispatch the loop's **\_implementer** subagent, then its **\_reviewer** subagent — one fresh session each, never the author's. Do not implement inline in the main session. The loop's rules, cycle cap, and dispatch contracts live in `development-loop`, which `fight` calls; they are not restated here.

- **Explore/`scout`** — codebase reconnaissance and questions.
- **Design subagents** — in the Design phase, `system-design` dispatches an **architect** (system design) and, when the spec has a UI, a **UI designer** (screens + static mocks) with crafted context. They run in parallel where independent; the coordinator reconciles them.
- **Implementer** — one task at a time, test-first, reporting fresh evidence (via `development-loop`).
- **Tester** — the test strategy for the current feature (via `test-strategy`), settled once in the Plan phase, before the loop; it can run in a fresh thread alongside planning so tests and tasks converge.
- **Reviewer** — review of a completed change, always in a **fresh session** (`AGENTS.md`).
- After dispatching a background task, keep handling the user's messages and other unblocked work; incorporate results as they arrive.
- You own integration, final verification, and the response to the user. Never relay a subagent's "success" as fact — check it.

**Fanning out.** To run several tasks at once instead of in sequence, use the `dispatching-parallel-agents` skill: it's the safe way to dispatch independent tasks (one worktree + branch each) and merge them without collisions. Only independent tasks fan out; the rest stay sequential.

## Workflow Spine

```
Brainstorm -> Roadmap -> Design -> Plan (incl. test-strategy) -> Development (loop) -> Deploy
```

| Phase       | Skill                            | Done when                                                                                                                  |
| ----------- | -------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Brainstorm  | `brainstorming`                  | An approved document exists: `docs/product/PRD.md` (project) or a spec revision in `specs/NNN-slug/` (feature)             |
| Roadmap     | `roadmap`                        | `specs/_roadmap.md` + `specs/_state.md` are agreed, with `status.md` folders for the current phase's features              |
| Design      | `system-design` (+ `ui-design`)  | The agreed design is written: `docs/architecture/architecture.md` (+ `docs/design/` when there's a UI), diagrams drawn     |
| Plan        | `planning` (+ `test-strategy`)   | `specs/NNN-slug/tasks.md` is agreed, every task traced to acceptance criteria, and the feature's `## Test strategy` is set |
| Development | `development-loop`               | Every task built test-first, verified green, and reviewed clean; the final whole-branch review is clean                    |
| Land        | `finishing-a-development-branch` | The MR/PR is raised for the human — or merged on explicit approval — and the worktree cleaned up                           |
| Deploy      | `deploy`                         | Human approved the deploy                                                                                                  |

**The Development phase is the loop `implement -> verify -> review`, run per unit — usually one task, or a batch of small same-shape tasks.** Its single source of truth is `development-loop` — the cycle cap, the transitions, the subagent contracts, and the final whole-branch review live there, not here. Inside the loop, `implement` builds the unit test-first following the feature's strategy (settled once in Plan by `test-strategy`), `verify` holds the fresh-evidence gate, and `review` judges the diff in a fresh session. `test-strategy` itself is **not** a loop step — it runs once per feature, inside Plan.

**Gates (hard):**

- No build without an approved spec — a feature spec revision in `specs/NNN-slug/`, or a PRD for project mode (via `brainstorming`).
- No implementation until the design is agreed — that means `docs/architecture/architecture.md` reflects the agreed system design, and `docs/design/` the agreed UI when the spec has one.
- No code before an approved task list — `specs/NNN-slug/tasks.md` (via `planning`).
- A finished branch gets an **MR/PR raised for the human**; **merging requires explicit human approval** (`finishing-a-development-branch`) — exactly like a deploy. Never merge on your own.
- Deploy requires explicit human approval. Never deploy on your own.

**Before a release/milestone deploy**, run `e2e-testing` to prove the assembled product works end to end — green e2e is a precondition for `deploy`, alongside the project's declared test command (`AGENTS.md`). It's not a per-feature step, so it doesn't run on every session; it gates a release.

Dispatching, sequencing, and "what's next" are your calls — do them and say so. Questions are for the choices where a wrong guess changes what gets built.

## Checkpoint / Run Scope

The default is **stop at every phase boundary**: verify the phase Targets, report, and wait for the human before starting the next phase. Widen only when the user asks.

- **Default:** one phase at a time. At the boundary, walk the phase's exit criteria and targets in `specs/_roadmap.md` → report what's true → wait.
- **Widen (opt-in):** "run to the end of P1", "chạy liền P1→P2", "run until blocked". The user names the stop condition.
- **Always stop** on: a red gate, a Critical review finding, the loop cap, a merge, or a deploy.

Think in **stop conditions**, not "how many phases to run" — the default is to stop, not to keep going.

## Reporting to the Human

The human should never have to ask "where are we?". Every checkpoint report uses the same short shape, so it's scannable and comparable run to run:

```markdown
**Where:** <feature/spec> — <stage> (phase <Pn> · cycle <n>/3)
**Done:** <what is now true, with evidence — command + result>
**Next:** <the next step, or the gate awaiting approval>
**Needs you:** <one decision / approval, or "nothing — say go">
```

Rules: lead with what changed, not the process; state evidence as it is (a red result reported is fine); one "Needs you" line — the single thing that unblocks the next step, or explicitly none.

## Paved Fast-Path (small, already-approved changes)

The full pipeline is for work that deserves it. When a change is genuinely small and the human has **already** approved what to do, use the fast-path instead of running every phase ceremony — but the gates that _matter_ still hold.

Qualifies when ALL are true:

- The change is trivial or fully specified (a typo, a one-line fix, a config value, a rename) — no design decisions.
- The human has stated the intended outcome (so the spec gate is satisfied by their instruction).
- It touches one concern, stays under ~300 lines, and needs no new dependency, schema, or interface.

On the fast-path: skip Roadmap, Design, and Plan; still **write the test first** when behavior changes (`development-loop` → `implement`); still hold the **`verify`** gate (fresh evidence) before any "done" claim; still get a **fresh-session `review`** for anything but a truly trivial edit; still raise the branch through `finishing-a-development-branch`. Record the fast-path choice and why in the feature's `specs/NNN-slug/status.md` notes.

If any qualifier fails — ambiguity, a design decision, more than one concern — it is **not** small: run the full pipeline. When unsure, take the full path.

## State

There is **no `.agents/STATUS.md`.** Position lives in `specs/`, one file per concern:

| File                       | Holds                                                  | Written by                                                               |
| -------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------ |
| `specs/_state.md`          | Current phase + feature (the cursor).                  | `roadmap`                                                                |
| `specs/_roadmap.md`        | Phases, features, exit criteria, phase log.            | `roadmap`                                                                |
| `specs/_status.md`         | The landed-PR ledger (one row per landing).            | `roadmap` (create), `finishing-a-development-branch` / `deploy` (append) |
| `specs/NNN-slug/status.md` | One feature's `status` / **`cycle`** / `next` / notes. | `roadmap` (create); `system-design`, `planning`, `development-loop`      |

**Cycle lives only in `specs/NNN-slug/status.md`** — losing it loses the loop's memory. Keep every one of these **short**: state and ledger are _pointers_, not reports. Evidence and findings go in the feature's `status.md` notes, `review.md`, or the phase log — never in `_status.md`.

## Verification Bar

Never claim work is done, fixed, or passing without fresh evidence. Before any completion claim, run the command and read its output — that's the loop's `verify` step (`development-loop`). State results as they are; a red result reported is fine, a red result hidden is a false report.

## Red Flags

| Thought                                               | Reality                                                                              |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------ |
| "Let me just start coding, the spec is obvious"       | No code without an approved spec revision. Gate one.                                 |
| "The design can wait, this is small"                  | No implementation until the design is agreed. Gate two.                              |
| "I'll do everything inline, dispatching is slow"      | You'll burn the context you need to coordinate. Dispatch.                            |
| "It passed review, so it's done"                      | Review judges intent; the loop's `verify` proves it's green. Both, or it's not done. |
| "Cycle 4 is fine, we're close"                        | The cap is 3. STOP and ask the human.                                                |
| "I'll run through all the phases now"                 | Default is to stop at each phase boundary. Widen only if asked.                      |
| "It's still red, let me tweak and re-run"             | Find the root cause before the retry — a new approach, not another guess.            |
| "Cycle 3, same fix, maybe it sticks this time"        | Each cycle changes the approach. Same approach again → STOP and ask.                 |
| "The review is taking forever, let it finish"         | The review is bounded. Stop it, ask for the report — a growing review is broken.     |
| "The subagent said it worked"                         | Check the diff and re-run. Agent reports are claims, not evidence.                   |
| "I'll skip the state files, they're just bookkeeping" | The cycle count lives in `status.md`. Keep `_state.md` and `status.md` current.      |

## Completion Check

Fight mode is running correctly when ALL are true:

- [ ] `specs/_state.md` reflects the current phase/feature, and the feature's `specs/NNN-slug/status.md` is current (status / cycle / next).
- [ ] The current phase's gate is satisfied before moving on (spec → roadmap → design → plan → code).
- [ ] Work is dispatched to the right phase skill; the coordinator owns integration and the final report.
- [ ] The Development phase ran via `development-loop`; its rules (cycle cap 3, per unit; fresh-session review; the final whole-branch review) were honored, not restated here.
- [ ] Checkpoint reports used the standard shape (Where / Done / Next / Needs you); any fast-path use was justified and recorded.
- [ ] The run stopped at the agreed checkpoint (default: phase boundary).
- [ ] No "done/fixed/passing" claim without fresh verification evidence.
