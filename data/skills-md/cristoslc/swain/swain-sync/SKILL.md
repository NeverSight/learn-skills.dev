---
name: swain-sync
description: "Fetch upstream, rebase, stage all changes, run ADR compliance check on modified artifacts, generate a descriptive commit message from the diff, commit, and push to the current branch's upstream. Handles merge conflicts by preferring local changes for config/project files and upstream for scaffolding."
user-invocable: true
allowed-tools: Bash, Read, Edit
metadata:
  short-description: Fetch, stage, commit, and push
  version: 1.4.0
  author: cristos
  license: MIT
  source: swain
---
<!-- swain-model-hint: sonnet, effort: low -->

Run through the following steps in order without pausing for confirmation unless a decision point is explicitly marked as requiring one.

Delegate this to a sub-agent so the main conversation thread stays clean. Include the full text of these instructions in the agent prompt, since sub-agents cannot read skill files directly.

## Step 1 — Detect worktree context and fetch/rebase upstream

First, detect whether you are running in a git linked worktree:

```bash
GIT_COMMON=$(git rev-parse --git-common-dir)
GIT_DIR=$(git rev-parse --git-dir)
IN_WORKTREE=$( [ "$GIT_COMMON" != "$GIT_DIR" ] && echo "yes" || echo "no" )
REPO_ROOT=$(git rev-parse --show-toplevel)
```

`IN_WORKTREE=yes` means the current directory is inside a linked worktree (e.g., `.claude/worktrees/agent-abc123`). Use this flag in Steps 3, 6, and the session bookmark step.

Next, check whether the current branch has an upstream tracking branch:

```bash
git --no-pager rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null
```

If there is an upstream, fetch and rebase to incorporate upstream changes BEFORE staging or committing:

```bash
git fetch origin
```

If there are local changes (dirty working tree), stash them first:

```bash
BRANCH=$(git rev-parse --abbrev-ref HEAD)
git stash push -m "swain-sync: auto-stash [$BRANCH]"
git --no-pager rebase origin/$BRANCH
git stash pop
```

If the rebase has conflicts after stash pop, abort and report:

```bash
git rebase --abort  # if rebase itself conflicts
git stash pop       # recover stashed changes
```

Show the user the conflicting files and stop. Do not force-push or drop changes.

If there is no upstream (`@{u}` returns an error) **and** `IN_WORKTREE=yes`, the worktree branch has no remote tracking counterpart. Rebase onto `origin/main` so the commits apply cleanly as a fast-forward:

```bash
git fetch origin
git rebase origin/main
```

If `origin` cannot be fetched, skip fetch/rebase and proceed to Step 2.

If there is no upstream **and** `IN_WORKTREE=no` (main worktree, new branch), skip this step entirely.

## Step 2 — Survey the working tree

```bash
git --no-pager status
git --no-pager diff          # unstaged changes
git --no-pager diff --cached # already-staged changes
```

If the working tree is completely clean and there is nothing to push, report that and stop.

## Step 3 — Stage changes

Identify files that look like secrets (`.env`, `*.pem`, `*_rsa`, `credentials.*`, `secrets.*`). If any are present, warn the user and exclude them from staging.

**If there are 10 or fewer changed files** (excluding secrets), stage them individually:

```bash
git add file1 file2 ...
```

**If there are more than 10 changed files**, stage everything and then unstage secrets:

```bash
git add -A
git reset HEAD -- <secret-file-1> <secret-file-2> ...
```

## Step 3.5 — Gitignore check

Before committing, verify `.gitignore` hygiene. **This step is blocking** — if relevant patterns are missing, stop and require the user to fix `.gitignore` before proceeding.

### 1. Check existence

If no `.gitignore` file exists in the repo root:

> STOP: No `.gitignore` file found. Create one before committing — without it, secrets, build artifacts, and OS files can enter git history.
> Minimal starting point: `curl -sL https://www.toptal.com/developers/gitignore/api/macos,linux,node,python > .gitignore`

**Stop execution.** Do not commit.

### 2. Detect relevant patterns

Check which patterns are *relevant* to this repo, based on what actually exists on disk:

| Pattern | Relevant if |
|---------|-------------|
| `.env` | `.env.example` exists, OR any untracked/tracked `.env` or `.env.*` file is present (excluding `.env.example`), OR `dotenv` appears in `package.json` or `requirements.txt` |
| `node_modules/` | `package.json` exists in the repo root or any subdirectory |
| `__pycache__/` | any `*.py` file exists in the repo |
| `*.pyc` | same as `__pycache__/` |
| `.DS_Store` | repo is on macOS (`uname` returns `Darwin`) |

For each relevant pattern, check if `.gitignore` contains it (exact match or substring). Collect missing ones.

### 3. Decide whether to block

- If **no relevant patterns are missing**: this step is silent. Continue to Step 3.7.
- If **any relevant patterns are missing**: stop and report:

  > STOP: `.gitignore` is missing patterns relevant to this repo:
  >   - `.env` — `.env.example` found; without this, a local `.env` file could be committed
  >   - `node_modules/` — `package.json` found
  >
  > Add the missing patterns before committing:
  >   echo ".env" >> .gitignore
  >   echo "node_modules/" >> .gitignore
  >
  > To permanently suppress a specific pattern check (intentional omission), add a comment to `.gitignore`:
  >   # swain-sync: allow .env

  **Stop execution.** Do not commit until the user resolves this.

### 4. Skip logic

If `.gitignore` contains `# swain-sync: allow <pattern>` for a given pattern, treat that pattern as intentionally omitted and do not flag it.

## Step 3.7 — ADR compliance check

If modified files include any swain artifacts (`docs/spec/`, `docs/epic/`, `docs/vision/`, `docs/research/`, `docs/journey/`, `docs/persona/`, `docs/runbook/`, `docs/design/`), run an ADR compliance check against each modified artifact:

```bash
bash skills/swain-design/scripts/adr-check.sh <artifact-path>
```

For each artifact with findings (exit code 1 — DEAD_REF or STALE), collect the output and present a single consolidated warning after all checks complete:

> ADR compliance: N artifact(s) have findings that may need attention.
> <condensed findings summary>

This step is **advisory** — it warns but never blocks the commit. Continue to Step 4 regardless.

If the `adr-check.sh` script is not found or fails with exit code 2, skip silently — the check is only available in repos with swain-design installed.

## Step 4 — Generate a commit message

Read the staged diff (`git --no-pager diff --cached`) and write a commit message that:

- Opens with a **conventional-commit prefix** matching the dominant change type:
  - `feat` — new feature or capability
  - `fix` — bug fix
  - `docs` — documentation only
  - `chore` — tooling, deps, config with no behavior change
  - `refactor` — restructuring without behavior change
  - `test` — test additions or fixes
- Includes a concise imperative-mood subject line (≤ 72 chars).
- Adds a short body (2–5 lines) summarising *why*, not just *what*, when the diff is non-trivial.
- Appends a `Co-Authored-By` trailer identifying the model that generated the commit. Use the model name from your system prompt (e.g., `Claude Opus 4.6`, `Gemini 2.5 Pro`). If you can't determine the model name, use `AI Assistant` as a fallback.

Example shape:
```
feat(terraform): add Cloudflare DNS module for hub provisioning

Operators can now point DNS at Cloudflare without migrating their zone.
Module is activated by dns_provider=cloudflare and requires only
CLOUDFLARE_API_TOKEN — no other provider credentials are validated.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

## Step 4.5 — Pre-commit hook check

Check if pre-commit hooks are configured:

```bash
test -f .pre-commit-config.yaml && command -v pre-commit >/dev/null 2>&1 && echo "hooks-configured" || echo "no-hooks"
```

If `no-hooks`, emit a one-time warning (do not repeat if the same session already warned):
> WARN: No pre-commit hooks configured. Run `/swain-init` to set up security scanning.

Continue to Step 5 regardless — hooks are recommended but not required.

## Step 5 — Commit

```bash
git --no-pager commit -m "$(cat <<'EOF'
<generated message here>
EOF
)"
```

Use a heredoc so multi-line messages survive the shell without escaping issues.

**IMPORTANT:** Never use `--no-verify`. If pre-commit hooks are installed, they MUST run. There is no bypass.

If the commit fails because a pre-commit hook rejected it:

1. Parse the output to identify which hook(s) failed and what was found
2. Present findings clearly:
   > Pre-commit hook failed:
   >   gitleaks: 2 findings (describe what was flagged)
   >
   > Fix the findings and run `/swain-sync` again.
   > Suppress false positives: add to `.gitleaksignore`
3. **Stop execution** — do not push. Do not retry automatically.

## Step 6 — Push

**If `IN_WORKTREE=yes`:** push the worktree's commits directly to `main` rather than creating a remote worktree branch:

```bash
git push origin HEAD:main
```

If this push is rejected with a non-fast-forward error:
- Check whether the rejection message mentions branch protection rules or required reviews.
  - If **branch protection is the cause**, open a PR instead:
    ```bash
    BRANCH=$(git rev-parse --abbrev-ref HEAD)
    SUBJECT=$(git log -1 --pretty=format:'%s')
    BODY=$(git log -1 --pretty=format:'%b')
    gh pr create --base main --head "$BRANCH" --title "$SUBJECT" --body "$BODY"
    ```
    Report the PR URL. Do not retry the push. Proceed to worktree pruning below.
  - If **diverged history is the cause** (not branch protection), report the conflict and stop. Do not force-push.

After a successful push or PR creation, remove the worktree:
```bash
WORKTREE_PATH=$(git worktree list --porcelain | grep -B2 "HEAD" | awk '/worktree/{print $2}' | grep -v "$(git rev-parse --git-common-dir | sed 's|/.git$||')")
git -C "$(git rev-parse --show-toplevel 2>/dev/null || git rev-parse --git-common-dir | sed 's|/.git||')" worktree remove --force "$WORKTREE_PATH" 2>/dev/null || true
git -C "$(git rev-parse --git-common-dir | sed 's|/.git||')" worktree prune 2>/dev/null || true
```

**If `IN_WORKTREE=no`** (main worktree, normal case):

```bash
git push          # or: git push -u origin HEAD (if no upstream)
```

If push fails due to divergent history (shouldn't happen after Step 1 rebase, but as a safety net):

```bash
git --no-pager pull --rebase
git push
```

## Step 7 — Verify

Run `git --no-pager status` and `git --no-pager log --oneline -3` to verify the push landed and show the user the final state. Do not prompt for confirmation — just report the result.

## Index rebuild (SPEC-047)

Before committing (after staging, before Step 5), check whether any artifact index files (`list-*.md`) are stale. If `skills/swain-design/scripts/rebuild-index.sh` exists, run it for each artifact type that had changes staged:

```bash
REBUILD_SCRIPT="$REPO_ROOT/skills/swain-design/scripts/rebuild-index.sh"
if [[ -x "$REBUILD_SCRIPT" ]]; then
    # Detect which types had staged changes
    for type in spec epic spike adr persona runbook design vision journey; do
        if git diff --cached --name-only | grep -q "^docs/$type/"; then
            bash "$REBUILD_SCRIPT" "$type"
            git add "docs/$type/list-${type}.md" 2>/dev/null || true
        fi
    done
fi
```

This ensures the index is current when the session's commits land.

## Session bookmark

After a successful push, update the bookmark. Use `$REPO_ROOT` (set in Step 1) as the search root so this works from both main and linked worktrees:

```bash
bash "$(find "$REPO_ROOT" -path '*/swain-session/scripts/swain-bookmark.sh' -print -quit 2>/dev/null)" "Pushed {n} commits to {branch}"
```
