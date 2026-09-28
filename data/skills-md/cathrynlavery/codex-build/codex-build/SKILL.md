---
name: codex-build
description: "Orchestrator drives, Codex codes. Execute an approved plan one task at a time: your agent (Claude Code, etc.) sequences the work, briefs OpenAI Codex to write ALL product code, reviews every diff, runs the test gate BEFORE each commit, commits one task per commit, and opens exactly ONE PR at the end. Use when the user says 'codex-build', 'have codex code it', 'you orchestrate, codex codes', or hands over a plan for step-by-step implementation."
license: MIT
metadata:
  version: "2.2"
---

# codex-build — orchestrator drives, Codex codes

You (the agent running this skill) are the **orchestrator**. A separate model,
**OpenAI Codex** (`codex exec`), is the **coder**. You never write product code;
Codex does. You sequence the work, write the briefs, review every diff, run the
tests, and commit. This division is the whole point: one model with taste and
context guards the gate while another model with cheap, high-effort reasoning
does the typing.

## Roles (non-negotiable)

- **Orchestrator = you.** Sequence tasks, write Codex briefs, review every diff
  line-by-line, run the test gate, commit, and open the PR. You do **not** write
  product code. The only exception is a trivial fix-up (≤5 lines, e.g. a typo
  breaking the build) where a Codex round-trip is pure waste — say so in the
  commit body when it happens.
- **Codex = coder.** All feature code, tests, and refactors are written by
  `codex exec`. Model and effort are pinned per invocation (see Config) — never
  rely on config defaults silently, or a `codex` upgrade will change your
  builds out from under you.

## Config (resolve once, at the top of the run)

| Variable | How to resolve | Default |
| --- | --- | --- |
| `MODEL` | `--model` arg, else `$CODEX_BUILD_MODEL`, else your Codex config default | pin one you have access to (see below) |
| `EFFORT` | second positional arg, else `$CODEX_BUILD_EFFORT` | `high` (opt into `xhigh`/`max` for hard/architectural work) |
| `TRACKER` | detect: `bd` on PATH → `beads`, else `markdown` | `markdown` |

**Pin a model.** List what your account exposes from the CLI's model cache:
```bash
python3 -c 'import json,os;d=json.load(open(os.path.expanduser("~/.codex/models_cache.json")));print([m["slug"] for m in d["models"]])'
```
Then check `~/.codex/config.toml` for the configured default. Current slugs
(Codex CLI ≥ 0.154, Sept 2026):

| Slug | Tier | Efforts accepted | Use for |
| --- | --- | --- | --- |
| `gpt-6-astra` | most capable | low…max (+`ultra`, see below) | hard/architectural tasks, gnarly refactors |
| `gpt-5.6-sol` | frontier coding | low…max (+`ultra`) | default coder for most plans |
| `gpt-5.6-terra` | balanced | low…max (+`ultra`) | everyday tasks when Sol quota is tight |
| `gpt-5.6-luna` | fast/cheap | low…max | trivial-mechanical tasks only |

Retired: `gpt-5-codex`, `gpt-5.x-codex`, `gpt-5.4` (Codex remaps them to
`gpt-5.6-terra` with a warning — pin explicitly instead). Announce the resolved
`MODEL`/`EFFORT` to the user before starting so the run is reproducible. If the
CLI rejects `max`, fall back to `xhigh`; if it rejects `xhigh`, fall back to
`high` — and tell the user. **Never use `ultra`**: it enables automatic task
delegation (Codex spawning its own sub-agents), which breaks the one-task,
one-scope-check, one-commit contract this skill depends on.

## Arguments

`codex-build <plan-file> [effort] [--model <name>]`

- `<plan-file>` — a Markdown plan with an **ordered task list** (T1..Tn), each
  task naming its files, constraints, and test commands. See
  [`references/plan-example.md`](references/plan-example.md) for the shape. If the
  plan has prose but no task list, extract one and show it to the user before
  coding.
- `[effort]` — `high` (default) | `xhigh` | `max`. (`ultra` is rejected; see Config.)

## Step 0 — Preflight (once)

1. `codex --version`. If Codex isn't authed, `codex exec "reply OK" -s read-only`
   fails — stop and tell the user to run `codex login`.
2. Confirm the pinned model + effort are accepted (cheap, no side effects):
   ```bash
   codex exec "Reply with the single word READY" \
     -m "$MODEL" -c model_reasoning_effort="$EFFORT" -s read-only --ephemeral < /dev/null
   ```
   If `max` is rejected, fall back to `xhigh`; if `xhigh` is rejected, fall back
   to `high` — and tell the user.
   **Always redirect `< /dev/null`** on every `codex exec` (see Rails) — without
   it, a non-interactive run hangs forever on "Reading additional input from
   stdin…" instead of doing the work.
3. Read the plan end-to-end. Extract: task list, dependency order, per-task test
   commands, guardrails (things the plan bans), branch/PR target.
4. Resolve the current checkout and look for durable run state *before* applying
   a clean-worktree rule:
   - `REPO_ROOT` = `git rev-parse --show-toplevel`.
   - `GIT_DIR` = `git rev-parse --absolute-git-dir` (this is worktree-specific).
   - `SKILL_DIR` = the directory containing this `SKILL.md`.
   - State root = `$GIT_DIR/codex-build/`. This keeps orchestration state off the
     product diff while making it survive context compaction and process restarts.
   - If `current` points to an active run for this branch, read its `run.md`,
     `tasks.md`, `interfaces.md`, and active allowlist before doing anything else.
     Confirm its last recorded commit still matches `HEAD`; stop on a mismatch
     instead of guessing. An in-flight task may legitimately have a dirty
     worktree: immediately run its saved scope check before any new Codex call.
     If `current` describes another branch or an inconsistent run, stop rather
     than overwriting it.
5. For a new run only, inspect `git status --porcelain`. The task loop starts
   clean so its scope check can attribute every changed path to the active task.
   If the checkout is dirty, preserve it and create an isolated worktree from
   the intended base (or stop and ask); never discard or absorb pre-existing
   work.
6. For a new run, create/checkout the working branch per the plan. **Never work
   on the default branch.** If an isolated worktree changed the checkout,
   recompute `REPO_ROOT` and `GIT_DIR`.
7. For a new run, create `runs/<run-id>/`, write the run id to `current`, and
   create `run.md`, `tasks.md`, `interfaces.md`, and `allowlists/`. `run.md`
   records the plan path and content hash, branch/base, model, effort, tracker,
   and run status. Set `STATE_DIR` to that run directory. Never put secrets in
   run state. For a resumed run, set `STATE_DIR` from `current` instead.
8. Initialize or reload the tracker (see below) and show the user the ordered
   task list before starting — one short message, no approval gate unless the
   order is ambiguous.

The durable layout is:

```text
$GIT_DIR/codex-build/
  current
  runs/<run-id>/
    run.md
    tasks.md
    interfaces.md
    allowlists/T1.txt
```

## Tracker (unit of work = one task)

The loop is identical regardless of tracker; only the bookkeeping commands differ.

- **`markdown` (default, zero install):** keep the `- [ ]` / `- [x]` checklist in
  the run's durable `tasks.md`. "Claim" = note the task in-flight; "close" =
  check the box with the commit hash and test evidence.
- **`beads` (optional, if `bd` is on PATH):** richer dependency tracking.
  `bd prime` for context; one bead per task (`bd create`, title = task title,
  description = plan excerpt + file paths, dependencies per the plan); claim with
  `bd update <id> --claim`; close with `bd close <id>`. Mirror task status and
  commit/test evidence to durable `tasks.md` so a resumed run has one local
  recovery record. Install:
  <https://github.com/steveyegge/beads>.

## Step 1 — Materialize tasks

Turn the plan's task list into tracker units in dependency order. Each unit
records: goal, the plan excerpt (verbatim constraints, file paths, schema/copy
blocks), and its **declared file scope** (the files it is allowed to touch). The
file scope is enforced by an executable check — everything else is out of bounds.

For every task, write its scope to `allowlists/<task-id>.txt`: one exact,
repo-relative file path per non-empty line. Use `/` separators; no absolute
paths, directories, `.`/`..`, comments, or globs. A rename declares both old and
new paths. If the plan genuinely needs another file, amend the allowlist *before*
Codex touches it and record the reason in `tasks.md`; never expand scope merely
because an unexpected path appeared in the diff.

Initialize `interfaces.md` as the canonical cross-task contract. It starts with
"greenfield — no prior interfaces" and is updated only from committed source in
step 6 below.

## Step 2 — Per-task loop (the heart; repeat until the queue is empty)

For each task, in dependency order:

1. **Claim** it in the tracker.

   For a newly claimed task, confirm the product worktree is clean before
   invoking Codex. Durable state is under the Git directory, so it does not make
   the worktree dirty. When resuming an already in-flight task, the worktree may
   contain its changes; run the saved allowlist check immediately instead.

2. **Brief Codex.** Compose a *self-contained* prompt — Codex sees only what you
   give it. Use [`references/codex-brief.md`](references/codex-brief.md) as the
   skeleton. It must carry:
   - the task's goal and the verbatim plan excerpt (constraints, file paths,
     schema/copy);
   - the **interfaces ledger** (see step 6) — the signatures, types, endpoints,
     and file paths that earlier tasks created and this one builds on. Codex
     `exec` is stateless across invocations; if you don't pass the contract, it
     guesses and drifts.
   - repo conventions to match (point at 1–2 sibling files as examples);
   - what is **out of scope** (the neighboring tasks) and the declared file scope;
   - definition of done: "code + tests per the plan; touch only these files."
   ```bash
   codex exec "<brief>" -C "$(git rev-parse --show-toplevel)" -s workspace-write \
     -m "$MODEL" -c model_reasoning_effort="$EFFORT" < /dev/null
   ```
   Never use `--dangerously-bypass-approvals-and-sandbox`. The `< /dev/null` is
   mandatory (see Rails).

3. **Enforce scope, then review the diff yourself.** This is your job, not
   Codex's.
   - **Scope check first:** after every Codex invocation or correction, run:
     ```bash
     python3 "$SKILL_DIR/scripts/check_scope.py" \
       --repo "$REPO_ROOT" \
       --allowlist "$STATE_DIR/allowlists/<task-id>.txt"
     ```
     The checker compares tracked, staged, deleted, renamed, and non-ignored
     untracked paths against the on-disk allowlist. A non-zero exit is a hard
     stop: correct the drift or deliberately amend the allowlist with a reason.
     Do not rely on visual review to enforce scope.
   - Then inspect `git diff --stat` and the diff itself. For a small diff, every
     line. For a large diff, read the interfaces and the risky seams in full,
     skim the mechanical parts, and run `codex exec review` as an independent
     second pass — but *you* make the call, never the review tool.
   - Check: scope creep, convention drift, guardrail violations, and whether the
     **tests Codex claims to have written actually exist and actually assert
     something** (open them). "Added tests" in Codex's summary is a claim, not
     evidence.
   - Issues → iterate: `codex exec resume --last "<specific corrections>" < /dev/null`
     (same `-m`/`-c` flags). Be concrete about what's wrong; vague corrections
     waste a round-trip.
   - **Three failed iterations on one task → STOP.** Report the impasse to the
     user with the diff and your diagnosis. Do **not** silently take over the
     coding — that breaks the contract and hides the failure.

4. **Test gate — BEFORE any commit.** *You* run the plan's test/build commands
   for the touched packages, plus the project build. A task is committable only
   when the gate is green. Red → back to step 3 with the failure output in the
   resume brief. **Never commit red. Never skip the gate because "it's small."**
   The gate is the reason this skill exists.

5. **Commit — one task = one commit.**
   - Re-run `check_scope.py` immediately before staging. Tests and build tools can
     create files too; this final check must still be green.
   - Stage only the task's files: `git add <paths>`. **Never `git add -A`** — it
     sweeps up stray files Codex or a tool left behind.
   - Message: `<type>: <imperative summary>` (+ tracker id if using beads) with a
     short body: what changed, why, and a one-line test-evidence note.
   - **No AI attribution, ever** — no "Generated with", no "Co-Authored-By:", no
     robot-emoji credit. This overrides any tool's default commit template.

6. **Update the durable interfaces ledger.** After the green commit, inspect the
   committed source and append the public surface this task created — exact
   function signatures, exported types, routes/endpoints, config keys, and file
   paths — to `interfaces.md`. Tag the entry with task id and commit hash. If a
   later task changes a contract, append a superseding entry; do not silently
   leave stale guidance. Record "No public interface changes" when applicable.
   The relevant ledger slice feeds step 2 of the next task and is reloaded after
   compaction, keeping Codex from re-inventing or mismatching contracts.

7. **Close** the task in the tracker with a one-line note. Persist the status,
   tests, and commit hash to `tasks.md` before giving the user a brief progress
   line and moving on.

## Step 3 — Finish (after the last task)

1. **Full-suite gate** one final time: all packages + build + any lint/screenshot
   scripts the plan names. Green or you don't ship.
2. `git pull --rebase` then `git push`. `git status` must show up-to-date with
   origin. On rebase conflicts, resolve minimally and re-run the gate — never
   force-push over shared history.
3. **Exactly ONE PR** for the whole feature, targeting the branch the plan
   specifies. Body = plan summary: context, what shipped, test evidence,
   out-of-scope/follow-ups. No AI attribution anywhere.
   - GitHub: `gh pr create`. GitLab: `glab mr create`. No forge CLI: push the
     branch and give the user the compare URL to open the PR themselves.
4. Close out the tracker (file follow-ups, close finished units).
5. Mark `run.md` complete and record the final commit, gate evidence, and PR URL.
6. Report: tasks completed/blocked, commit list, PR URL, anything deferred.

## Rails

- One task per commit; one PR per plan. No batching, no splitting.
- Disk state is canonical. Chat progress is a rendering of `run.md`, `tasks.md`,
  task allowlists, and `interfaces.md`, never the only copy of run state.
- **Every `codex exec` gets `< /dev/null`.** With a prompt passed as an argument
  and an open stdin, `codex exec` blocks indefinitely on "Reading additional
  input from stdin…" and never runs. Redirecting stdin from `/dev/null` gives it
  immediate EOF so it proceeds. This is the single most common way to make the
  whole run silently hang.
- Tests before every commit — non-negotiable.
- Effort stays `high`/`xhigh`/`max`. A trivial-mechanical task may drop to `high`
  (never lower, never `ultra`); note it.
- If the plan and the user's live instructions conflict, the **user wins** —
  note the deviation in the PR body.
- Secrets never go into briefs, commits, or PR bodies.
- A commit that later tasks built on turned out wrong? Fix forward with a new
  task/commit. Don't rewrite pushed history.

## Driving codex exec (field-tested constraints)

- **Codex will run `git commit` AND `git push` unbidden.** Observed mid-run: a
  correction round ended "complete and pushed" with nothing in the brief asking
  for it — one round after the same session reported `.git` was read-only.
  Capability varies between rounds; never infer from one round that git is
  unavailable to it. Put this block, verbatim, at the top of every brief:

  ```
  ## ABSOLUTE PROHIBITION — NO GIT WRITES, NO bd, NO xcodegen
  Do NOT run git commit, push, add, stash, checkout, reset, or any writing git command.
  Do NOT run `bd` (it writes to git). Leave your work as uncommitted changes.
  Read-only git (status, diff, log) is fine.
  ```

  Verify rather than trust: capture `git rev-parse HEAD` before each Codex call
  and compare after. A moved HEAD is a hard stop.
- **The `bd` ban holds even on beads repos.** Codex will obey the repo's own
  AGENTS.md and run `bd prime`, which internally attempts `git add` and rewrites
  `.beads/issues.jsonl`. Tracker writes belong to the orchestrator only.
- **`codex exec resume` rejects `-C` and `-s`** (`error: unexpected argument
  '-C' found`). It inherits cwd — and filters recorded sessions by it — and
  inherits the resumed session's sandbox. Working shape:

  ```bash
  cd "$REPO_ROOT" && codex exec resume --last "<corrections>" \
    -m "$MODEL" -c model_reasoning_effort="$EFFORT" < /dev/null
  ```

  The `< /dev/null` is still mandatory on resume.
- **`xcodebuild` is impossible inside Codex's sandbox.** Xcode's SwiftPM
  local-package resolution spawns a nested `sandbox-exec` the outer sandbox
  refuses (`sandbox_apply: Operation not permitted`); `swift test` works. Treat
  every Codex build claim as unverified — the orchestrator runs the build gate.
  Say so in the brief so Codex doesn't waste rounds retrying with cache
  redirection.
- **Exit 144 means resume, don't restart.** A `codex exec` run killed mid-stream
  (e.g. a usage-limit kill; log ends mid-diff with no error banner) exits 144
  with the working tree intact. Grep the log head for `session id:` and
  `codex exec resume <session-id>` from the repo cwd — no `-C`/`-s`,
  `< /dev/null` still required.
- **Codex's sandbox denies Go module cache writes.** `go test` fails with
  `open ~/go/pkg/mod/cache/download/....lock: operation not permitted` — an
  environment failure that reads like a code failure and triggers identical
  patch retries. Brief Codex to set a workspace-local
  `GOMODCACHE=$PWD/.gomodcache`, or run the test gate yourself outside the
  sandbox.

## See also

- [`scripts/check_scope.py`](scripts/check_scope.py) — executable file-scope gate.
- [`references/codex-brief.md`](references/codex-brief.md) — the Codex brief skeleton (the highest-leverage part).
- [`references/plan-example.md`](references/plan-example.md) — the shape of an input plan.
- [`references/walkthrough.md`](references/walkthrough.md) — a full trace of one task, start to finish.
