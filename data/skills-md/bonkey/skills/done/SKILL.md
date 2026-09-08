---
name: done
description: "Check if a PR already exists; if it does, update the PR. If no PR exists, merge current branch locally into main and push to main remote. If main is protected, create a PR instead."
---

# Done

Ship the current branch — by updating an existing PR, merging locally to main, or creating a PR when main is protected.

The deterministic plumbing (PR check → protected check → fast-forward merge → push) lives in `scripts/ship.sh` so the common local-merge path runs in one shot instead of many model round-trips. **Deciding what to ship is judgment, so the script never stages or commits** — you commit deliberately, it requires a clean committed tree, then it merges and pushes. The script auto-completes only the well-understood happy path; for anything unusual it prints a `HANDOFF` (with full state already gathered) and you take over.

## Workflow

### 0. Pre-flight — verify repo requirements

Find and read whichever convention/instruction files apply to this repo and harness (e.g. `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `.cursor/rules/*`, `.github/copilot-instructions.md`, `.clinerules`, etc. — follow any `@`-includes). Verify the branch satisfies the rules; fix or surface gaps before continuing. If a repo mandates a check before shipping (e.g. `just ci`), run it now.

### 1. Review and commit

Look at `git status` / the diff and confirm the working tree contains **only the change you intend to ship** — watch for unrelated edits or stray/untracked files. Stage deliberately (`git add -A` only once you've confirmed the tree is clean of anything that shouldn't ship; otherwise stage specific paths), then commit with a crafted message. Leave the working tree clean.

### 2. Run the ship script

From inside the branch's worktree:

```bash
skills/done/scripts/ship.sh
```

The script prints a `=== SHIP: STATE ===` block, then one of:

- **`=== SHIP: DONE ===`** — the local-merge happy path completed (fast-forwarded the default branch to your commit(s), pushed to origin, worktree preserved). Go to **Step 3**.
- **`=== SHIP: HANDOFF ===`** — the script stopped on purpose; read `suggested_path:` and the `reason:` lines and continue below. The STATE block is complete, so don't re-gather it.
- **`=== SHIP: ERROR ===`** — a step failed; read `step:`/`detail:`, investigate, and resolve manually.

`suggested_path` routing:

| `suggested_path` | What it means | Do this |
|---|---|---|
| `update-pr`   | An open PR already exists | **Step 2a** |
| `create-pr`   | Default branch is protected | **Step 2b** |
| `commit`      | Uncommitted changes in the tree | Review them (Step 1) — exclude anything unrelated — commit, then re-run Step 2 |
| `resolve`     | A merge/rebase/conflict is in progress | Resolve it, then re-run Step 2 |
| `manual`      | Detached HEAD, on default branch, behind origin, or diverged | Reconcile the stated condition, then re-run Step 2 |
| `nothing`     | Nothing to ship | Confirm with the user; likely already shipped |

### 2a. Update existing PR

Push the current branch to its remote so the PR updates:

```bash
wt step push
```

Then post a comment on the PR summarizing the changes.

### 2b. Create PR (main is protected)

Push the current branch and open a PR:

```bash
wt step push
gh pr create --fill
```

### 3. Update related ticket

If a related ticket is known (Jira, Linear, GitHub issue, etc. — from branch name, commit messages, PR body, or conversation context), update its status to reflect the ship:

- **PR updated** → move ticket to "In Review" (or equivalent) if not already there
- **Merged to main** (via local merge or PR merge) → move ticket to "Done" / "Closed" / "Shipped"

If no ticket is obviously linked, skip this step — don't guess.

### 4. Confirm

Report what happened, drawing the facts from the script's output (or the PR path you took):

- **Merged locally** (`SHIP: DONE`): print the `old → new` commit on the default branch and the changes summary
- **PR updated**: print the PR URL
- **PR created**: print the PR URL
- **Ticket updated**: print the ticket ID and new status (if applicable)

## Reference

- `scripts/ship.sh` — the deterministic local-merge path; reads as the source of truth for the decision tree.
- For `wt` command details, see `references/worktrunk.md`.
