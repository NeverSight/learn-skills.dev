---
name: sync-fork
description: Sync a forked repository with its upstream. Fetches both remotes, shows divergence, resets shared branches to upstream, re-merges local-only branches, cleans up branches already merged upstream, and pushes. Use when upstream has accepted PRs or moved ahead and you need to bring your fork in line.
---

# Sync Fork

Sync a forked repository with its upstream remote. The fork's shared branches (e.g., `main`) are maintained as the equivalent of upstream plus local patches re-merged on top — a "patched upstream" model. Each sync resets to upstream, rebases fork-only branches, and re-merges them.

If upstream hasn't advanced (i.e., `upstream/main` is already an ancestor of `fork/main`), the sync is a no-op.

## Usage

`/sync-fork [<fork-remote> <upstream-remote>]`

- With **no arguments** — auto-detect if exactly two remotes exist. If more than two, ask the user to specify.
- With **one argument** — the provided name is ambiguous. Look up its URL with `git remote get-url <name>` and ask the user: *"`<name>` points to `<url>` — is this your fork, or the repo you forked from?"* Then ask for the other remote name.
- With **two arguments** — first is the fork remote, second is the upstream remote.

When auto-detecting with exactly two remotes, use heuristics to guess which is the fork and which is upstream (e.g., a remote named `origin` is more likely the fork; a remote whose URL org differs from the other is more likely upstream). Present your guess and ask the user to confirm.

**⚠️ Credential safety:** Remote URLs may contain embedded credentials (e.g., `https://user:token@github.com/...`). Before displaying any URL to the user, redact the userinfo portion: replace `user:token@` with `***@`. Never output raw credentials from `git remote -v` or `git remote get-url`.

## Diagram legend

Used in reference files adjacent to this skill:

```
───       flow (left-to-right = time)
├── X     branch X forks here
└── X     branch X forks here (last branch at this point)
──┘       merge point (branch merges into line above)
●         notable state on the line
```

## Helper script

This skill includes `scripts/sync_fork.py` — a deterministic Python helper for branch analysis. It handles classification, divergence checking, and dependency graph building so these operations produce consistent results. Requires Python 3.9+ (stdlib only).

Locate the script relative to this skill file. Invoke it as:
```bash
python3 <skill-dir>/scripts/sync_fork.py <subcommand> [options]
```

Subcommands: `classify`, `divergence`, `graph`, `plan`, `state`. Run with `--help` for full usage. Default output is compact key-value (LLM-friendly). Add `--json` for structured output.

## Instructions for Claude

You are syncing a fork with its upstream. Follow the phases below in order.

This skill uses **incremental discovery** — the main flow below covers the common case. When you encounter a specific situation (a topology, an edge case), you will be directed to read the relevant reference file at that point. **Do not read all reference files upfront.** Read them only when triggered.

Reference files live in two directories adjacent to this skill:
- `examples/` — branch topology diagrams and rebase strategies
- `edge-cases/` — handling for unusual situations

### Phase 0: Pre-flight

1. **Check for interrupted previous run.** Look for branches matching `sync-fork/*`. If found, a previous sync was interrupted. Show the user what backup branches exist and ask: restore from backups, or clean up (`git for-each-ref --format='%(refname:short)' 'refs/heads/sync-fork/' | xargs git branch -D`) and start fresh?

2. **Check for state file.** Run `python3 <script> state read`. If a state file exists, a previous sync was interrupted mid-phase. Show the user which phase was reached and ask: resume from that phase, or delete the state file (`python3 <script> state delete`) and start fresh?

3. **Save current branch.** Record `git symbolic-ref --short HEAD` (or the detached commit) so we can restore it at the end.

4. **Guard dirty working tree.** Run `git status --porcelain`. If there are uncommitted changes, stash them:
   ```bash
   git stash push -m "sync-fork: uncommitted changes"
   ```
   This will be popped at the end. Stash is branch-independent, so it survives the checkout/reset operations that follow.

5. **Identify remotes.** Run `git remote -v` and resolve which remote is the fork and which is upstream using the rules in the Usage section above. Confirm with the user if there was any ambiguity.

### Phase 1: Assess Divergence

1. Fetch both remotes.

2. **No-op check.** For each shared branch, check `git merge-base --is-ancestor <upstream>/<branch> <fork>/<branch>`. If upstream is already an ancestor of fork for ALL shared branches, the sync is a no-op — upstream hasn't advanced. Tell the user and stop.

3. **Classify branches.** Run the helper script:
   ```bash
   python3 <script> --fork <fork> --upstream <upstream> classify
   ```
   This identifies shared branches, fork-only branches (merged, promoted, partially promoted, active), and reports them in a compact format.

   - ⚠️ If `fork-only-partial` entries appear → **read `edge-cases/partial-promotion.md`**.
   - ⚠️ If `fork-only-promoted` entries appear → **read `examples/promoted-branch.md`** for the full handling strategy.

4. **Check divergence.** Run the helper script:
   ```bash
   python3 <script> --fork <fork> --upstream <upstream> divergence
   ```
   This shows per-branch commit counts and flags.

   - ⚠️ If any branch shows `rewrite=true` AND `fork_merges_only=false` → **STOP and read `edge-cases/history-rewrite.md`** before proceeding. (When `fork_merges_only=true`, the fork-only commits are just merge commits from previous syncs — this is normal, not a history rewrite.)
   - ⚠️ If any branch shows `reverts>0` → **STOP and read `edge-cases/upstream-reverts.md`** before proceeding.

5. **Dry-run plan.** Run:
   ```bash
   python3 <script> --fork <fork> --upstream <upstream> plan
   ```
   Present the full plan to the user. Wait for confirmation before proceeding.

### Phase 2: Create All Backups and Reset Shared Branches

Create all backups upfront (both pre-reset and pre-rebase) before any destructive operations. This consolidates recovery points into a single step.

#### 2a. Create all backup branches

```bash
# Pre-reset backups for shared branches
for branch in <shared_branches>; do
  git branch sync-fork/pre-reset/$branch <fork>/$branch
done

# Pre-rebase backups for fork-only active branches
for branch in <fork_only_active>; do
  git branch sync-fork/pre-rebase/$branch <fork>/$branch
done
```

These backups serve triple duty:
- Recovery points if anything goes wrong
- Old-ref storage for `--onto` rebases (the `sync-fork/pre-rebase/<parent>` tip IS the old ref)
- Correct ancestry refs for the dependency graph (shared branches are about to be reset)

#### 2b. Reset shared branches

For each shared branch (in order: default branch first, then others):

1. Check out the branch locally. (If no local tracking branch exists, `git checkout` will auto-create one.)
2. `git reset --hard <upstream>/<branch>` to align with upstream.
3. `git push <fork> <branch> --force-with-lease` to update the fork.

#### 2c. Save state

Write state after resets complete so an interrupted run can resume from Phase 3:
```bash
python3 <script> state write --data '<JSON with phase, remotes, classification, backups>'
```

### Phase 3: Rebase Fork-Only Branches

#### 3a. Build the dependency graph

Run the helper script to build the dependency graph. It uses the `sync-fork/pre-reset/*` backup refs for shared branch ancestry checks (since shared branches now point to upstream):

```bash
python3 <script> --fork <fork> --upstream <upstream> graph \
  --branches <comma-separated-fork-only-active> \
  --shared <comma-separated-shared> \
  --backup-prefix sync-fork/pre-reset
```

The output provides: parent map, topological order, orphaned branches, and merge targets.

- ⚠️ If `orphaned` is not `(none)` → **read `edge-cases/orphaned-branches.md`**.

#### 3b. MANDATORY: Read the matching topology reference

**You MUST read the applicable example file before continuing.** Match the dependency graph you just built to the correct topology and read that file now:

| Topology detected | Read this file |
|---|---|
| All branches root directly on a shared branch, no dependencies between them | `examples/independent-branches.md` |
| One branch depends on another (B based on A) | `examples/linear-chain.md` |
| Multiple branches depend on the same parent (B and C both based on A) | `examples/fan-out.md` |
| Three or more branches in a chain (A → B → C) | `examples/deep-chain.md` |
| Branches root on different shared branches | `examples/multi-target.md` |
| Mixed (combination of above) | Read ALL applicable files |

If the graph has any dependencies between fork-only branches, you **must** understand the `--onto` rebase strategy from the relevant file before proceeding. Getting this wrong causes duplicate commits and false conflicts.

#### 3c. Rebase in topological order

For each fork-only branch (parents first, children last — use the `order` from the graph output):

1. **Check for merge commits:** `git log --merges sync-fork/pre-rebase/<parent>..<branch>`
   - ⚠️ If merge commits found → **read `edge-cases/merge-commits-in-branches.md`** before rebasing this branch.

2. **Rebase:**
   - **If parent is a shared branch:** `git rebase --empty=drop <shared-branch> <branch>`
   - **If parent is another fork-only branch:** `git rebase --empty=drop --onto <parent> sync-fork/pre-rebase/<parent> <branch>`
   - `--empty=drop` automatically discards commits already in upstream. If Git < 2.26, omit the flag and use `git rebase --skip` when prompted.
   - If rebase conflicts occur, resolve them. Show the user what you resolved and why.

3. **Check for empty result.** If ALL commits were dropped (branch now points to same commit as its parent), warn the user: *"Branch `<branch>` appears fully absorbed by upstream. Consider deleting it."*

4. `git push <fork> <branch> --force-with-lease` to update the fork.

5. **Update state** after each successful rebase (add to `completed_rebases` list).

### Phase 4: Re-merge into Shared Branches

The fork's shared branches are maintained as "upstream + local patches." This phase replays merge commits on top, so fork/main = upstream/main + fork-only work.

For each shared branch that has fork-only branches targeting it (use the `target` map from the graph output):

1. Check out the shared branch locally.
2. Merge each rebased fork-only branch with `--no-ff` in **topological order** (parents before children). Use the message format:
   ```bash
   git merge --no-ff <branch> -m "sync-fork: merge <branch> into <shared-branch>"
   ```
   - These merges should be clean since branches were just rebased. If a conflict occurs, resolve it and show the user what you resolved.
   - After merging a parent (e.g., A), merging its child (e.g., B) only brings in B's unique commits.
3. `git push <fork> <branch> --force-with-lease` to update the fork.

### Phase 5: Clean Up

1. Delete remote branches (`git push <fork> --delete <branch>`) that are fully merged into upstream.
2. Delete all backup branches: `git for-each-ref --format='%(refname:short)' 'refs/heads/sync-fork/' | xargs git branch -D`
3. Delete state file: `python3 <script> state delete`
4. Restore the original branch saved in Phase 0: `git checkout <saved-branch>`.
5. If changes were stashed in Phase 0, restore them: `git stash pop`.
6. List any local tracking branches that can be pruned.
7. Show the user a final summary of what was synced, rebased, merged, deleted, and what branches remain.

### Rules

- **Always confirm** the plan with the user before resetting or force-pushing.
- **Use `--force-with-lease`**, never `--force`, when pushing reset branches.
- **Preserve local-only work** — the point is to keep branches that upstream hasn't accepted while aligning with upstream's current state.
- **Don't delete branches that have unmerged work** — only clean up branches whose content is already in upstream (even if commit SHAs differ due to squash-merging).
- **Don't touch branches unrelated to the fork sync** — leave feature branches that aren't targeting a shared branch alone.
- **Backup branches use the `sync-fork/` prefix** — these are temporary and cleaned up at the end. If a sync is interrupted, they survive for recovery. Clean up manually with `git for-each-ref --format='%(refname:short)' 'refs/heads/sync-fork/' | xargs git branch -D`.
