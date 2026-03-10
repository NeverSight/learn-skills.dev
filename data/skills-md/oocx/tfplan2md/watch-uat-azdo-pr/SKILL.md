---
name: watch-uat-azdo-pr
description: Watch an Azure DevOps UAT PR for maintainer feedback or approval by polling threads and reviewer votes until approved/passed.
compatibility: Requires Azure CLI (az) with azure-devops extension, authentication, jq, and network access.
---

# Watch UAT PR (Azure DevOps)

## Purpose
UAT polling is historically brittle. This skill standardizes the watch loop so the agent can reliably wait for Maintainer feedback/approval using a single stable command.

This skill uses the repo wrapper script `scripts/uat-watch-azdo.sh`, which repeatedly calls `scripts/uat-azdo.sh poll` until:
- PR status becomes `completed`, or
- an approval vote is detected, or
- approval keywords are detected in non-agent comments, or
- a timeout is reached.

## Hard Rules
### Must
- Use `scripts/uat-watch-azdo.sh` (single stable command).
- Prefer reviewer votes / PR completion as the strongest approval signal.

### Must Not
- Spam threads or post follow-ups while waiting.
- Run many ad-hoc `az`/`az devops invoke` calls; prefer the wrapper.

## Actions

### 1. Watch the PR
```bash
scripts/uat-watch-azdo.sh <pr-id>
```

### 2. Optional: Tune polling interval / timeout
```bash
scripts/uat-watch-azdo.sh <pr-id> --interval-seconds 60 --timeout-seconds 3600
```

## Output
- Exit code `0`: approval detected / PR completed (treat as pass)
- Exit code `1`: timed out (treat as incomplete; ask Maintainer)
