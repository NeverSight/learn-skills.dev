---
name: create-pr-azdo
description: Create an Azure DevOps pull request using az devops tooling; include the repo’s linear-history merge preference and ask the Maintainer if merge options differ.
compatibility: Requires git, Azure CLI (az) with azure-devops extension, authentication, and network access.
---

# Create PR (Azure DevOps)

## Purpose
Create an Azure DevOps pull request in a consistent way, while still encoding the repository’s preference for a **linear history**.

This skill prefers using the repo wrapper script `scripts/pr-azdo.sh` to minimize Maintainer approval interruptions (single terminal invocation).

## Notes on Merge Policy
`CONTRIBUTING.md` specifies **Rebase and merge** as the required merge strategy for this repo.

Azure DevOps UI/merge options differ by project settings. When merging an Azure DevOps PR, choose the most “rebase/linear-history” option available (often called **Rebase and fast-forward**) when available; otherwise, ask the Maintainer what to use.

## Hard Rules
### Must
- Work on a non-`main` branch.
- Ensure the working tree is clean before creating a PR.
- Push the branch before creating the PR.
- Keep PR title and description conventional and review-friendly.
- Before creating the PR, post the **exact Title and Description** in chat.
- Use the standard description template (Problem / Change / Verification).

### Must Not
- Merge using a strategy that introduces merge commits unless the Maintainer explicitly requests it.

## Actions
### 0. Title + Description (Required)
Before running any PR creation command, provide in chat:

- **PR title** (exact)
- **PR description** (exact), using this template:

```markdown
## Problem
<why is this change needed?>

## Change
<what changed?>

## Verification
<how was it validated?>
```

### Recommended: One-Command Wrapper
```bash
scripts/pr-azdo.sh create --title "<type(scope): summary>" --description "<why + what + testing notes>"
```

Abandon a test PR (cleanup):
```bash
scripts/pr-azdo.sh abandon --id <pr-id>
```

### 1. Pre-flight Checks
```bash
git branch --show-current
scripts/git-status.sh --short
```

### 2. Push the Branch
```bash
git push -u origin HEAD
```

### 3. Create the PR
This is a minimal example; set `--organization`/`--project` appropriately for the target repo.

```bash
az repos pr create \
  --title "<type(scope): summary>" \
  --description "<why + what + testing notes>" \
  --source-branch "$(git branch --show-current)" \
  --target-branch main
```

### 4. Merging
- If you need to merge the PR, confirm the exact merge option with the Maintainer first.
- Prefer a rebase/linear-history option when available.
