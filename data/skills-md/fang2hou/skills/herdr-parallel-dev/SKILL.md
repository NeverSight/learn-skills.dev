---
name: herdr-parallel-dev
description: >
  Runs parallel multi-agent development with Herdr: one worktree and agent per
  task in the project's herdr space, accept-or-send-back review,
  integration-branch or CI-gated PR landing, then cleanup. Use for multi-task
  fan-out when HERDR_ENV=1.
license: MIT
compatibility: Requires HERDR_ENV=1, herdr CLI, git, gh, jq, Bash, and standard POSIX utilities inside a Herdr-managed pane.
metadata:
  author: fang2hou
  version: "2.2"
  sources: "Incident-proven workflow (2026-08-17 multi-project worktree misadventure + 3-PR sequential merge); herdr CLI behavior verified 2026-08-18"
---

# Herdr Parallel Development

Run N independent repo tasks as N herdr agents, each in its own git worktree that herdr creates and owns; review each deliverable, land them in a verified order, and give the machine back exactly the state it started in.

## When to Use

- Several independent tasks on one repo ("make these 3 PRs", "do these in parallel").
- Fanning out multi-file changes that would collide in one working tree.
- Landing multiple finished agent branches as one integration branch or as PRs.
- Post-merge verification of cross-branch consistency and cleanup.

## When NOT to Use

- Single sequential task: use a plain herdr agent in a sibling pane; no worktree is needed.
- Remote branch management or repo settings (out of scope).
- Cleaning up branches or worktrees left by earlier sessions: use git-branch-cleanup. Step 9 here cleans only this run's objects.
- Base herdr CLI reference: read the `herdr` skill first (install: `npx skills add ogulcancelik/herdr -g`; docs: https://herdr.dev/docs/cli-reference/). This skill adds only the multi-worktree orchestration layer.

## Inputs

| Input        | Required | Format                             | Example                               |
| ------------ | -------- | ---------------------------------- | ------------------------------------- |
| Project path | Yes      | absolute path                      | `/Users/me/Developer/projects/my-app` |
| Task list    | Yes      | 1–8 self-contained tasks           | each becomes one worktree + one agent |
| Landing mode | Yes      | `integration` / `pr`               | see Step 7                            |
| Base branch  | No       | branch, default `origin/<default>` | a work branch in `integration` mode   |

Cap concurrency at 8 worktrees: queue anything beyond that and dispatch each queued task as an earlier agent settles; monitoring quality degrades faster than extra parallelism pays off.

## Forge boundaries

The `gh` commands in this skill are **GitHub-forge-specific**: they are the verified baseline for GitHub-hosted repositories, not a requirement of the worktree, branch, validation, or cleanup rules. Load [Forge Adaptation](references/forge-adaptation.md) before Step 1 when the repository is not GitHub-hosted, `gh` is unavailable, or forge behavior differs. Use only a verified client or API that achieves the same review, merge, CI, and recovery outcomes; do not invent substitute commands.

## Tool response contract

Herdr JSON responses used here expose the fields needed to rebuild the run table: workspace creation returns `.result.workspace.workspace_id`, worktree creation returns `.result.root_pane.pane_id` and `.result.worktree.path`, and listing returns `.result.worktrees[]`. Verify fields before dispatching; never infer IDs from pane order or memory.

## Hard Rules

1. **Never let herdr guess the repo.** Every `worktree create` binds the repo explicitly with `--workspace <project-space-id>` (preferred: the project's own herdr space) or `--cwd <absolute-project-path>`. With neither, herdr can resolve its focused/recent project and create worktrees in a different repo. A workspace ID is trustworthy only when returned by `herdr worktree list --cwd "$PROJECT"` or from a space opened for `$PROJECT`, never from sidebar order or memory.
2. **Let herdr own the layout.** Use no `--path` (herdr places checkouts under `~/.herdr/worktrees/<repo>/<branch-slug>`), no `--label` (the branch is the sidebar handle), and `--no-focus` while dispatching. Switch with `herdr worktree open --cwd "$PROJECT" --branch <b> --focus` or `herdr workspace focus <id>`.
3. **Verify every worktree before dispatching** with `<this-skill-dir>/scripts/verify-worktrees.sh "$PROJECT" <created-paths...>` (omit paths to auto-discover). A wrong origin URL means remove it, fix the binding, and recreate; never improvise on the wrong repo.
4. **Every agent prompt starts with a GUARD block:** the agent runs `git remote get-url origin` and confirms one known path exists, then stops and reports if either check fails. Agents are the second defense; one once caught a mismatch the dispatcher missed.
5. **One worktree = one branch = one agent.** Never share a worktree.
6. **Agents start blank.** Every prompt is self-contained: guard, ground truth (files/line pointers), task, verification steps, commit rules, repo conventions from AGENTS.md, and “decide and document; do not ask.”
7. **Nothing lands on a red gate.** Never merge while target CI is red or advance to the next branch on a red run. A green Deploy does not substitute for CI; only the CI workflow proves the project's checks passed.
8. **Retire before removing.** Stop the agent (`send-keys ctrl+c`, then `ctrl+d`; confirm it left `herdr agent list`) before `herdr worktree remove`, which kills its pane.
9. **Cleanup deletes only this run's objects**, and only after merge proof (content on target or PR shows merged). Squash-merged local branches need `git branch -D`; anything not tied to a task of this run, including an already-open space, stays.

## Run Table

State lives in this session, not on disk, so two runs never collide. Keep one row per task:

| task | branch | worktree workspace | pane | worktree path | agent | status | deliverable |
| ---- | ------ | ------------------ | ---- | ------------- | ----- | ------ | ----------- |

The fixed field order is `task`, `branch`, `worktree_workspace`, `pane`, `worktree_path`, `agent`, `status`, `deliverable`; keep it in the human table and downstream exports. Also record the project's space as **already open** (leave it) or **opened by this run** (close it in Step 9).

After interruption, rebuild the table from `herdr worktree list --cwd "$PROJECT"`, `herdr agent list`, and `gh pr list` (**GitHub-forge-specific; use a verified review-list equivalent elsewhere**). Never recreate a worktree whose branch exists; adopt it and continue from observed state.

## Workflow

### Step 1: Scan the repo, then fix the landing mode

```bash
git -C "$PROJECT" remote get-url origin                            # expected repo
DEFAULT=$(git -C "$PROJECT" symbolic-ref --short refs/remotes/origin/HEAD)   # never hardcode
DEFAULT=${DEFAULT#origin/} && echo "default branch: $DEFAULT"
gh repo view --json squashMergeAllowed,deleteBranchOnMerge --jq '{squash: .squashMergeAllowed, deleteOnMerge: .deleteBranchOnMerge}' # GitHub-forge-specific
ls .github/workflows/                                              # GitHub Actions baseline; use verified CI discovery elsewhere
grep -n "merge" AGENTS.md CONTRIBUTING.md 2>/dev/null | head       # repo merge conventions
```

Record default branch, merge method (squash unless the repo says otherwise), head auto-delete behavior, and workflow names that must be green. Choose with the user's request as the deciding input:

- **`integration`**: every task branches off one work branch not yet on default; children merge back and ship as one PR.
- **`pr`**: every task ships its own PR to default.

Bind the mode's base once and carry it in the run table:

```bash
MODE=pr                                   # or: MODE=integration
WORK_BRANCH=""                            # integration mode: the work branch name
if [ "$MODE" = integration ]; then BASE="$WORK_BRANCH"; else BASE="origin/$DEFAULT"; fi
git -C "$PROJECT" rev-parse --verify "$BASE"   # fail here, not at create time
```

### Step 2: Plan branches

For each task choose a `type/slug` branch, an agent name `<slug>-pr` matching `[a-z][a-z0-9_-]{0,31}`, and a blast radius: docs/style is low-risk shared text; isolated infra deploys alone and lands first for attribution; feature has the widest runtime/contract/docs surface. Compute the conflict surface (files touched by ≥2 tasks, predicted then confirmed with `git diff --name-only`); these are rebase/propagation hotspots and set Step 7 order.

Worked example: a bundler swap was isolated infra (slot 1), a docs guideline realign was docs/style (slot 2), and an interactive-controls runtime/worker/contracts/migration feature was widest (slot 3). Landing 1→2→3 made the feature rebase onto the final doc baseline; Step 8 checked conformity.

### Step 3: Create worktrees inside the project's herdr space

Worktrees belong to the project's space, nested under it exactly as the TUI's New Worktree action (`prefix+shift+g`) creates them. Resolve that space once, then create each worktree against it:

```bash
SPACE=$(herdr worktree list --cwd "$PROJECT" | jq -r '.result.worktrees[] | select(.is_linked_worktree == false) | .open_workspace_id // empty' | head -1)
SPACE_OPENED_BY_RUN=no
if [ -z "$SPACE" ]; then
  SPACE=$(herdr workspace create --cwd "$PROJECT" --no-focus | jq -r '.result.workspace.workspace_id')
  SPACE_OPENED_BY_RUN=yes
fi
herdr worktree create --workspace "$SPACE" --branch feat/rolldown-bundler --base "$BASE" --no-focus
# record .result.workspace.workspace_id, .result.root_pane.pane_id, .result.worktree.path
```

One create per task. Each yields its own workspace labelled with the branch and nested under `$SPACE`; do not expect the pane in the caller's workspace. `$BASE` is `origin/$DEFAULT` in `pr` mode and the work branch in `integration` mode. Then gate dispatch:

```bash
SKILL_DIR=<directory containing this SKILL.md>
"$SKILL_DIR/scripts/verify-worktrees.sh" "$PROJECT" <created-paths...>
```

Exit 0 dispatches; any FAIL row means stop and fix first.

### Step 4: Dispatch agents

```bash
sleep 3                                                   # new pane needs a settled shell
herdr agent start rolldown-pr --kind omp --pane <pane-id> # returns when ready
herdr agent prompt rolldown-pr '<full self-contained brief>'
sleep 6 && herdr agent get rolldown-pr                    # must report agent_status "working"
```

`agent_pane_busy` means wait and retry; never dispatch into a non-shell pane. Pick the agent kind from the installed list (`herdr agent` prints it); `omp` is common. The brief's gate command comes from AGENTS.md/README (for example `mise run check`), never an assumption.

Prompt template (all parts mandatory):

```
<ONE-LINE TASK>. You are in a dedicated worktree on branch <branch> (base <base>) of the <repo-name> repo.

GUARD: run `git remote get-url origin` — it must be <expected-url> and <one known path> must exist. Otherwise STOP and report; never improvise on a different repo.

GROUND TRUTH (verify yourself): <files, symbols, current behavior, pointers>
TASK: <numbered steps including verification and the repo's gate command>
DELIVER: Conventional Commits (English), push the branch, and report its tip. In `pr` mode, open a review request through the configured forge (GitHub: `gh pr create --base <default>`); in `integration` mode, do not open one. Never merge.
RULES: <package manager>, stay in your worktree, no unrelated refactors, decide and document; do not ask.
```

The 6-second check matters: a prompt that failed to land leaves the agent `idle`; resend or read the pane before assuming work started.

### Step 5: Monitor

```bash
herdr agent wait <name> --timeout 300000   # returns on first settled state
herdr agent get <name>                     # idle | working | blocked | done
herdr agent read <name> --source visible --lines 12   # TUI agents: viewport only
```

Loop `wait` in ~5-minute cycles. Full-screen agents use the alternate screen, so `recent-unwrapped` is not useful; read `visible`. On `blocked` (approval/question UI), read the pane and resolve via `agent prompt` or `send-keys`. An agent in the wrong repo gets `send-keys <name> ctrl+c` immediately; verify the foreign worktree is clean before touching it.

**Stall escalation:** `working` across two cycles (~10 min) with zero worktree changes (`git status --porcelain` before/after), or over ~60 min total, means read the pane and steer with a specific prompt. Still unresponsive → `ctrl+c` and take over in that worktree.

### Step 6: Accept or send back

For each settled agent, verify the deliverable yourself, never its summary:

```bash
git -C <worktree> log --oneline "$BASE"..HEAD     # real commits exist
git -C <worktree> status --porcelain              # nothing stranded uncommitted
git -C <worktree> diff "$BASE"...HEAD --stat      # scope matches task
gh pr list --head <branch>                        # GitHub-forge-specific; pr mode only
```

Run the repo gate in the worktree, then decide: **Accept** marks the row accepted and leaves the agent alive/idle for Steps 7–8; **Send back** with the specific defect, expected behavior, verification, failing command, and output (never a vague request), then return to Step 5; two failed round trips on one defect means take over and record why; **Drop** removes an unsalvageable task from the landing plan and records the reason. Do not land until every row is accepted or explicitly dropped.

### Step 7: Land

#### Phase A: Plan (Gate 7A)

Order accepted branches by dependency edges first, then risk: isolated infra first for attribution; docs/style second as the baseline; widest-surface feature last so it rebases onto the final baseline. Write ordered branches, target base, landing mode, and rationale in the run and landing tables. The user decides ambiguous mode/order.

**Gate 7A:** every row is accepted or explicitly dropped, every branch is tied to this run, and mode/base/order are recorded before any merge.

#### Phase B: Validate (Gate 7B)

```bash
for b in <ordered branches>; do
  git -C "$PROJECT" log --oneline "$BASE..$b" --stat
  git -C "$PROJECT" diff --name-only "$BASE...$b"
done
```

Confirm touched files match tasks, no dropped task is included, the repository gate is green, and required review checks are green. In GitHub mode, `gh pr list --head <branch>` and run-status queries are the forge-specific baseline; use a verified equivalent elsewhere (load [Forge Adaptation](references/forge-adaptation.md) before this phase when the forge is not GitHub).

**Gate 7B:** stop on unexpected scope/review state, required checks, or mergeability; record evidence before proceeding.

#### Phase C: Execute (Gate 7C)

**Mode `integration`** (children collapse into the work branch, which ships as one review request):

```bash
git -C "$PROJECT" checkout <work-branch> && git -C "$PROJECT" pull --ff-only
for b in <ordered branches>; do
  git -C "$PROJECT" merge --squash "$b" && git -C "$PROJECT" commit   # or --no-ff, per repo convention
  <repo gate command>                                                 # green before next branch
  git -C <next-worktree> fetch origin --prune
  git -C <next-worktree> rebase <work-branch>
  git -C <next-worktree> push --force-with-lease
done
git -C "$PROJECT" push
gh pr create --base <default> --head <work-branch>  # GitHub-forge-specific
```

**Mode `pr`** (one review request per task, strictly sequential and CI-gated; GitHub-forge-specific baseline syntax):

```bash
gh pr merge <N> --squash                          # 1. merge, per repo convention
gh run list --branch <default> --limit 2 --json databaseId,name
gh run watch <ci-run-id> --exit-status            # 2. green required (Hard Rule 7)
git -C <next-worktree> fetch origin --prune       # 3. rebase the next branch
git -C <next-worktree> rebase origin/<default>
git -C <next-worktree> push --force-with-lease
# 4. required checks COMPLETED/SUCCESS and mergeability CLEAN, then repeat
```

Another forge's equivalent must merge exactly one accepted review request, identify and await its required CI checks, and rebase the next branch only after green checks. Never advance on a red or ambiguous result.

**Gate 7C:** after each merge, observe proof that expected content is on the target and required CI is green; record merge/run identifiers before advancing. Load [Conflict Resolution](references/conflict-resolution.md) when a Step 7 rebase reports conflicts. Load [CI Failure Triage](references/ci-triage.md) when a landing gate is red or a run needs classification.

### Step 8: Post-merge consistency audit

Once everything is on the target branch and green: (1) **sync**: for squash merges, compare each squash commit with its branch tip's touched files; (2) **coherence**: check that the ADR index, architecture map, README/DEVELOPMENT commands, `mise.toml`/`package.json`, and shared concepts agree (`git log --oneline` plus targeted `git show <squash> -- <shared-files>`); (3) **style propagation**: if an early branch changed global style and a later branch touched the same files, verify conformance. Rebase merges content, not intent; re-prompt the later agent with “realign <files> to the structure from commit <A-squash>, keep B's facts, zero code changes,” then land the follow-up.

### Step 9: Retire agents, then remove worktrees

Only after merge proof (PR shows merged or content is on target), retire first because `worktree remove` kills the pane and agent:

```bash
herdr agent send-keys <name> ctrl+c
sleep 1
if herdr agent get <name> >/dev/null 2>&1; then herdr agent send-keys <name> ctrl+d; sleep 2; fi
herdr agent list | jq -r '.result.agents[].name'   # <name> must be absent before removal
herdr worktree remove --workspace <worktree-workspace-id>
test ! -e <worktree-path> && echo "gone: <worktree-path>"
herdr worktree list --cwd "$PROJECT" | jq -c '.result.worktrees[] | {branch, path}'
git -C "$PROJECT" fetch --prune
git -C "$PROJECT" branch -vv
git -C "$PROJECT" branch -D <branch...>                   # squash-merged only
if [ "$SPACE_OPENED_BY_RUN" = yes ]; then herdr workspace close "$SPACE"; fi
```

On success, removal deletes the checkout, prunes registration, and closes its workspace but never deletes the branch. On failure it changes nothing; a row still listed by `herdr worktree list` means removal failed. Fix it; never close that workspace by ID or orphan the checkout. A dirty worktree is not an obstacle to force past: `dirty_worktree_requires_force` means inspect/report `git status --porcelain` and `git diff`, keep it, and use `--force` only when worthless or committed elsewhere.

**Force/recovery protocol:** before any `--force`, `branch -D`, or `push --force-with-lease`, record branch tip, remote tip, worktree path, and `git status --porcelain`. If a local branch was deleted by mistake, restore it at the saved (or verified reflog) tip and prove `git rev-parse <branch>` equals it. If a force-push was mistaken, restore the saved remote tip only after checking target and lease, then fetch and prove `git ls-remote origin refs/heads/<branch>` equals it. If a worktree was removed by mistake, its committed branch still exists: recreate with explicit `--cwd "$PROJECT"` or trusted `--workspace`, rerun `verify-worktrees.sh`, and prove the recovered path is listed, on the expected branch, and at the saved tip. Uncommitted files deleted by forced removal have no git undo; recover only from a separately saved patch/backup, otherwise report loss and stop. These path/tip/list/clean-status checks are the observable recovery proof.

Before each `branch -D`, confirm PR merged or content provably on target; `[gone]` upstream alone is only a hint. Leave the empty `~/.herdr/worktrees/<repo>/` directory for herdr to reuse.

## Verification

The run is done only when observed:

- [ ] Every task row is accepted or dropped with a reason.
- [ ] `verify-worktrees.sh "$PROJECT" <paths>` exited 0 before any agent started.
- [ ] Every accepted branch's content is on target (`git -C "$PROJECT" log --oneline <base>..<target>`) or its PR reads merged.
- [ ] Target CI is green on its latest run; Step 8 found no unresolved sync, coherence, or style drift.
- [ ] `herdr agent list` contains none of this run's names; `herdr worktree list --cwd "$PROJECT"` contains none of its paths.
- [ ] `git -C "$PROJECT" branch -vv` has no leftover run branch without a recorded reason.
- [ ] `herdr workspace list` shows the project's space exactly as found (closed again only if this run opened it).

The bundled `scripts/verify-worktrees.sh` emits data only on stdout and diagnostics/results only on stderr. Default stdout is TSV with fields `status`, `worktree`, `branch`, `url`, `dirty`, `ahead`; `--format json` emits one object with `status`, `count`, `results`, and `expected_url`. Exit codes are documented and stable: 0 all pass, 1 at least one FAIL row, 2 usage/environment error.

## Failure Handling

| Failure                         | Signal                                      | Action                                                                                                                                |
| ------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Worktree on wrong repo          | verifier FAIL row or agent GUARD report     | Remove it, fix binding, recreate; never edit in place.                                                                                |
| `agent_pane_busy`               | `agent start` error                         | Wait for shell prompt and retry; never dispatch into a busy pane.                                                                     |
| Prompt did not land             | `agent get` still `idle` after ~6s          | Re-send; read pane before assuming work started.                                                                                      |
| Agent `blocked`                 | approval/question UI                        | Read pane; answer via `agent prompt` or `send-keys`.                                                                                  |
| Agent stalled                   | no worktree change across two ~5-min cycles | Steer specifically, then `ctrl+c` and take over.                                                                                      |
| Deliverable rejected twice      | same defect after two send-backs            | Take over and record it.                                                                                                              |
| Rebase conflict, semantic       | conflicting files span a feature            | Hand to that branch's agent with both intents; never drop one side.                                                                   |
| CI red (infra)                  | setup/download/network (HTTP 429)           | GitHub: `gh run rerun <id> --failed`; otherwise use a verified equivalent; re-watch.                                                  |
| CI red (regression)             | failure inside project checks               | Stop landing, fix branch, rerun gates.                                                                                                |
| `dirty_worktree_requires_force` | `worktree remove` exits 1                   | Inspect/report uncommitted work; keep it; force only once worthless.                                                                  |
| Interrupted run                 | table lost                                  | Rebuild from worktree/agent lists and GitHub `gh pr list` (or verified review-list equivalent); unmatched objects are someone else's. |

Stop and ask the user when landing mode is ambiguous, a merge needs force-pushing a shared branch, uncommitted agent work has value you cannot judge, or cleanup would touch an object this run did not create.

## Gotchas

- **`worktree create` without `--workspace` or `--cwd` targets the wrong project.** Plausible paths expose the mistake only through `remote get-url origin` (Hard Rule 1).
- Each create spawns a workspace and opens the project's space if closed; IDs come from JSON, never layout assumptions.
- `--label` overwrites the branch handle in the sidebar (Hard Rule 2); `--no-focus` documents the API's false default.
- A fresh pane rejects `agent start` with `agent_pane_busy` until its shell is interactive.
- `agent prompt` without `--wait` can return a stale snapshot; confirm `working` with `agent get`.
- An `idle`/`done` agent still holds its pane/name until it exits.
- Squash-merged branches are not ancestors: `-d` refuses them, so `-D` is correct only after merge proof.
- `deleteBranchOnMerge: true` makes remote heads vanish; local `[gone]` is expected.
- Resolve rebase conflicts in the rebasing branch's worktree, never the main checkout, because the main checkout may hold the integration branch or the user's work.

## Output Contract

On completion, return:

1. Run table in fixed order `task → branch → worktree workspace → pane → worktree path → agent → status → deliverable` (PR URL or branch tip), including dropped tasks and reasons.
2. Review log: first-time accepts, send-backs with defects and round trips, and manual takeovers.
3. Landing log: mode, order and rationale, each gate outcome, and flakes rerun.
4. Audit results: sync, coherence, and style-propagation findings with fixes.
5. Cleanup report: agents stopped, worktrees removed, branches deleted with proof basis, space closed/left open and why, preserved objects, and final `git branch -vv`, `herdr worktree list --cwd "$PROJECT"`, and `herdr workspace list`.

Stable run-table fields for downstream consumers:

```text
task | branch | worktree_workspace | pane | worktree_path | agent | status | deliverable
```
