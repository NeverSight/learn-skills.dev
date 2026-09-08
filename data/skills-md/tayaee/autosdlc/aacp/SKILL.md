---
name: aacp
description: Archive an implemented issue, stage remaining tracked changes, commit code+archive together, and push (4 steps, no deploy). Use when the user says "/aacp", "aacp #"
---

# aacp — archive, add -u, commit, push (no deploy)

Merges a `/tdd2`-staged issue into `main` (archive, add, commit, push) without calling deploy.
Companion skill for deploying: `/aacpd` (5 steps, includes deploy to dev).

`aacp: 4단계 (deploy 없음); aacpd: 5단계 (deploy 포함)`

**Precondition**: code changes for the issue are already staged (`git add`, not yet committed).

## Usage

### Explicit issue number — no prompts

```bash
bash .claude/skills/aacp/aacp.sh <issue-number> <commit-summary...>
```

## What the script does

Run from anywhere inside the target repo.

0. Lightweight safety check: verifies inside a git repository (<0.1s). Quality verification belongs to preceding `tdd2` and `code-quality-gate` phases.
1. Stages `issues/issue-<#>.md`.
2. Archives it (`git mv` to `issues/archive/YYYY/MM/DD/`).
3. `git add -u` (stages remaining tracked changes).
4. Commits code + archiving as one commit.
5. Pushes to remote repository.
(Step 6 Deploy is omitted in aacp).
