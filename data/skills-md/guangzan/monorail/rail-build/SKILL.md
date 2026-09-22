---
name: rail-build
description: Implement docs/monorail tasks serially in one session — drive rail-tdd at agreed seams, then commit.
disable-model-invocation: true
---

# Rail Build

Implement tasks from `docs/monorail/<feature>/tasks/`. **One session, serial run**: after a task goes green, continue to the next frontier task in the **same** session — no fresh session, no check-ins or questions between tasks. Defaults: run to queue-clear, **one commit per task** on the current branch. The skill never asks about run length or commit policy — the user states any deviation (review pause, no-commit, narrower run) in their command and the agent honors it.

Confirm with the shell before concluding it is missing (`ls docs/monorail/work-tracker.md`, or read the path directly) — search tools skip gitignored paths, so an empty Glob/Grep result is **not** evidence of absence. If it is missing on disk, tell the user to run `/rail-setup` and stop.

## Process

1. Load the task file and its parent `spec.md`. If `spec.md` is missing, stop and suggest `/rail-spec`. Confirm blockers are done (blocker tasks show `Status: done`). If the task shows `Status: claimed` but its `## Comments` has no matching `Run <date>: start` line (a stale claim from a crashed run), recover it: revert to `Status: open` with a `## Comments` note before working — a stale `claimed` silently blocks the frontier.
2. If the task is too large for one context window, stop and suggest `/rail-slice` re-split or `/rail-align` — do not hard-code a giant task.
3. Claim: set `Status: claimed` on the task file before coding.
4. **Explore on demand** — read what the task needs (paths, types, call chains, nearby tests, `docs/monorail/CONTEXT.md` / ADRs), at the depth the task warrants; a small task needs no ceremony, often one or two file reads. Use the read-only sweep under **Exploration** only when the territory is genuinely unfamiliar or wide — never let it delay red-phase TDD. Before writing any test, open the file(s) the task's `Seams:` line points at. If the code contradicts the spec's `## Testing Decisions` (a seam is missing, wrong, or overlaps unlisted code), **do not re-derive seams and do not keep coding** — stop per §4 and report; otherwise proceed on the spec's seams.
5. Drive `/rail-tdd` at the task's `Seams:` line (set at slice time from the spec's code-anchored `## Testing Decisions`).
6. Run typecheck / relevant tests regularly; full suite once at the end.
7. Set task `Status: done` when the task's behaviour is covered (TDD complete at the task's `Seams:`) and typecheck / relevant tests are green — and append the done-gate block under `## Comments` (see §3.2). Do **not** run `/rail-review` as part of build — review is opt-in (see `/rail-review`).
8. Commit **once per task** on the current branch (default policy — the task's single commit carries its claim and status changes); skip committing only when the user opted out for this run.
9. **Continue or stop.** Another frontier task exists and the user's go-ahead covers it → continue serially (see **Serial run**). Otherwise stop and report where you left off. When the run ends with no open/unblocked tasks remaining, cross-check that every numbered `## User Stories` entry in `spec.md` is covered by a `done` task (or explicitly out of scope) — report any uncovered story instead of claiming the queue is clear — then say the feature's implementation queue is clear (human decides merge/ship; a new feature starts at `/rail-align`).

**Frontier (implementation):** `Status: open`, every listed blocker is `Status: done`, not claimed; lowest `NN` wins (see `docs/monorail/work-tracker.md`). Read task files by path, and list `tasks/` with the shell (`ls docs/monorail/<feature>/tasks/`) — search tools skip gitignored paths, so an empty Glob/Grep result is **not** evidence the queue is empty.

Never run two tasks in the same working tree **concurrently** — serial runs are strictly sequential. For actual parallelism use worktrees (**Parallel builds** below).

## Serial run (one session, task after task)

The default is **one prolonged session**: green tasks keep coming — one working tree, one commit per task, no new sessions. A serial run is throughput, not parallelism; parallel execution still requires worktrees (next section).

A serial run is the default once build starts — **ask nothing**: no up-front question about run length or commit policy, no check-ins mid-run. Run to queue-clear and one commit per task are the defaults; the user can narrow or override them anytime ("just this task", "stop after task k", "don't commit", "pause between tasks") — honor that statement, never prompt for it.

Fit check (before the run):

- Same feature (same `spec.md`, one seam decision) so the run shares context
- Each task fits one fresh context window (rail-slice already guarantees this) — a **heavy** slice that needs its own context budget should be its own session, not folded into a serial run
- No two tasks edit the same files — check paths up front; if files overlap, order the later task **after** the one that owns the file, or drop it from the run

### 1. Pre-flight (once, per run)

- **File map:** list per-task files; order the run by file ownership and `Blocked by` edges, not by `NN`.
- **Contradiction scan:** acceptance criteria that conflict, two tasks owning the same public symbol, seams that overlap. A contradiction is a spec/task defect — do not ask and do not guess; stop per §4 and report.
- **Seams:** each task's `Seams:` line was set at slice time from the spec's `## Testing Decisions` (code-anchored and confirmed at spec time). No seam questions mid-run — a contradiction with the code stops the run per §4.
- **Review pause:** only if the user asked for it in their command — insert a review stop after each task's commit (the commit is the hand-off point) and wait for a go-ahead before the next task. Never offer it.

### 2. Claim and record

- Claim each task (`Status: claimed`) before coding. In a serial run the claim rides in that task's single commit — no separate claim commits. Parallel builds commit claim edits before forking worktrees (see below).
- Under each task's `## Comments`, append `Run <date>: start — <base commit>`; when the task is done, append a **done-gate block**:

  ```
  done — <commits>
  - seams used: <from the task's `Seams:`>
  - typecheck: green
  - relevant tests: green (which)
  - acceptance criteria: met (or itemised open gaps)
  ```

  These lines are the resume map after `/rail-pass` or a crash, and they make `Status: done` audit-able — a `done` with no done-gate block is not credible. A `claimed` task with no matching `Run … start` line is a stale claim; recover it to `open` (Process §1).

### 3. Run (sequential, no check-ins)

For each task in order:

1. **Keep the orchestrator head clean — inline by default.** Implement the task **in the main session** unless a hand-off trigger fires: (a) the task's territory is genuinely unfamiliar or wide (exploration would cost more than a spawn), or (b) the orchestrator's context has degraded (compaction keeps firing, reasoning quality drops, harness warns — the §4 context stop). When a trigger fires, hand the task to a **fresh implementer sub-agent** (sequential — wait for it to return before the next); its brief must be self-contained: absolute paths to the task file and `spec.md`, `What to build`, `Acceptance criteria`, the task's `Seams:` line (and `Touchpoints:` if present) pasted in full, and "TDD at these seams — red before green; do not touch other tasks' files; read-only on the tracker". If the harness cannot spawn sub-agents, implement the task yourself — **sequentially**. Never dispatch two implementers on the same tree. A handed-off task stays with its implementer until green (red → back to it, step 4); the next task defaults back to inline.
2. When the implementer returns (or you finish inline): run typecheck / relevant tests yourself and check the acceptance criteria against the code.
3. Green → set `Status: done`, append the done-gate block, **commit that task**, continue. **Never pause between tasks** to ask "continue?" — the run is the go-ahead; the only stop between tasks is a review pause the user requested in their command.
4. Red or criteria not met → send the failing evidence back to the same implementer — the inline session or the sub-agent whose context holds the task (it is intact); if it cannot resolve, stop per §4. Never mark `done` on red.

### 4. Stop conditions (reactive, task-level)

- Hard bug / unclear failure on task *k* → commit tasks *1..k-1*, leave task *k* `claimed` with a `## Comments` note (or revert to `open`), stop, suggest `/rail-debug`. Completed work stays committed — never roll back.
- Context degraded (compaction keeps firing, reasoning quality drops, harness warns) → stop the run; hand the next task to a fresh implementer sub-agent or write `/rail-pass`. The `## Comments` run lines resume the run.
- Spec/task wrong → stop the run; same rule as a single task (`/rail-align`, leave `claimed`/`open`, never `done`).
- User narrowed or ended the run → stop at that point and report where you left off (what's `done`, what's next).
- Harness poor fit for long sessions → fall back to one-task-per-fresh-session mode. That is the escape hatch, not the default.

`done` still means green at the task's `Seams:`, per task — a partially implemented task is not `done`. Run the full suite once at the end of the run.

A serial run does not replace **Parallel builds** below (true concurrency still needs one worktree per task — one serial run per worktree).

## Parallel builds (worktree-mandatory)

The default is one serial run in the current worktree. To run **more than one** `/rail-build` at once, isolation is a **git worktree**, not "more sessions".

**Hard rule:** never two build writers on the same working tree — whether two Cursor sessions, two sub-agents, or any mix. Same-cwd concurrent builds are forbidden; stop and set up worktrees instead.

### Setup (primary worktree only, serially)

1. Pick N frontier tasks (`Status: open`, blockers `done`).
2. Claim each (`Status: claimed`) on the **primary** worktree.
3. Commit those claim edits on the integration branch so Status is durable before fork (follow the user's commit rules).
4. For each claimed task, add a dedicated worktree + branch from that commit, e.g.:
   - branch: `rail/build/<feature>-<NN>`
   - path: repo-sibling or `.worktrees/<feature>-<NN>` (create `.worktrees/` if needed; do not commit build artifacts from it)
   - `git worktree add <path> -b rail/build/<feature>-<NN> <integration-ref>`
5. Start **one** `/rail-build` per worktree (cwd = that worktree). The task is already claimed — verify `claimed`, do not claim a different task.

### During / after

- Each build writes only inside its own worktree. Do not edit other worktrees' files.
- Mark `Status: done` and commit on that task's branch when the solo done gate passes.
- **Integrate serially** into the integration branch (merge or rebase **one branch at a time**). Resolve conflicts on the integration branch. Do not parallel-merge.
- Remove worktrees after their branches are integrated.

Parallel builds do **not** mean dispatching implementation sub-agents on one tree — a **serial run** dispatches them strictly sequentially; parallel means separate worktrees (usually separate sessions). Keep the same-tree implementation ban.

## Exploration (optional, on demand)

Exploring the code in the main session is the default for a task whose territory is already familiar. When the territory is genuinely unfamiliar or wide, a **read-only sweep** is worth its latency: parent agent stays the orchestrator; sub-agents must not edit files, claim tasks, or start implementation. Send a **single message** with up to three Agent/Task tool calls (explore / general-purpose). If the harness cannot spawn parallel sub-agents, run the scopes sequentially or answer the questions yourself.

| Sub-agent | Scope | Return |
| --------- | ----- | ------ |
| **Code map** | Paths, types, and call chains named or implied by the task / `What to build` | Relevant files + how they connect (under ~300 words) |
| **Test / seam precedents** | Existing tests and public boundaries near those paths | Candidate seams and nearby test patterns to reuse (under ~300 words) |
| **Domain docs** | `docs/monorail/CONTEXT.md` (if present), ADRs under `docs/monorail/adr/` that touch this area, plus any repo coding-standards docs | Binding terms, constraints, and standards that apply (under ~200 words) |

Skip a scope whose inputs clearly do not exist (e.g. no `CONTEXT.md` and no ADRs — skip Domain docs and note that).

Each sweep prompt must include: absolute paths to the task file and `spec.md`, the task's `What to build` (or equivalent) and `Seams:` line pasted in full, and "read-only — do not modify the repo".

After the sweep returns: synthesize, then **compare against the spec's `## Testing Decisions`**. Matching seams → proceed. Divergence (a spec seam is missing, wrong, or overlaps unlisted code) → **stop** per §4 and report — never re-derive the seams yourself and never ask. Then continue at step 5.

**Do not** dispatch implementation or fix sub-agents in parallel on the same working tree during build — the same-tree ban is absolute. For multi-task throughput, use **Parallel builds** (worktrees) above.

## Escape hatches (mid-build)

- Hard bug / unclear failure → suggest `/rail-debug` (fresh session only if the run's context is already heavy)
- Context full / near degraded → `/rail-pass`; do not push on — the `## Comments` run lines resume the run
- Spec/task wrong or incomplete (missing requirement, bad slice) → **stop**; do not keep coding. Suggest `/rail-align` (update `align.md` or map); when alignment is durable again the **planning chain** resumes (`/rail-spec`, which stops for your go/no-go before `/rail-slice`). Leave the task `Status: claimed` or revert to `open` with a `## Comments` note; do not mark `done`
