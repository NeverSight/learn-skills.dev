---
name: orchestrate-multi-repo-sdks
description: >-
  Use when each language SDK lives in a separate repository. Covers cross-repo
  workflow dispatch, PR status reporting, PR reconciliation on merge/close.
  Triggers on "multi-repo SDK", "separate SDK repositories", "cross-repo workflows",
  "SDK PR synchronization", "spec repo triggers SDK repos".
license: Apache-2.0
---

# Orchestrate Multi-Repo SDKs

Manage SDK generation when each language SDK lives in its own repository (e.g., `myapi-typescript`, `myapi-python`, `myapi-go`).

## When to Use

- SDKs for different languages in separate repositories
- Need PR-triggered cross-repo SDK generation
- Want automated PR reconciliation (merge/close SDK PRs when spec PR closes)
- Different teams maintain different language SDKs
- User says: "multi-repo SDK", "cross-repo workflows", "SDK PR sync"

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  API Spec Repository                     │
├─────────────────────────────────────────────────────────┤
│  PR opened    │  PR merged/closed    │  Main push       │
│      ↓        │        ↓             │      ↓           │
│  kick-off     │  reconcile-prs       │  sync            │
└───────────────┴──────────────────────┴──────────────────┘
        │                │                    │
        ▼                ▼                    ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ typescript   │  │ python-sdk   │  │ go-sdk       │
│ SDK PR       │  │ SDK PR       │  │ SDK PR       │
└──────────────┘  └──────────────┘  └──────────────┘
```

## Workflow 1: Kick Off Generation (PR Trigger)

Triggers SDK generation in each language repo when spec PR opens:

```yaml
# .github/workflows/kick-off-generation.yaml
name: Kick Off SDK Generation
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  trigger_sdk_repos:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        include:
          - repo: myapi-typescript
          - repo: myapi-python
          - repo: myapi-go
    steps:
      - name: Trigger SDK generation
        env:
          GH_TOKEN: ${{ secrets.SDK_REPOS_PAT }}
        run: |
          gh workflow run sdk_generation.yaml \
            --repo "your-org/${{ matrix.repo }}" \
            --field feature_branch="${{ github.head_ref }}"
```

## Workflow 2: Reconcile PRs (On Merge/Close)

Auto-merge or close SDK PRs when spec PR closes:

```yaml
# .github/workflows/reconcile-prs.yaml
name: Reconcile SDK PRs
on:
  pull_request:
    types: [closed]

jobs:
  manage_sdk_prs:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        repo: [myapi-typescript, myapi-python, myapi-go]
    steps:
      - name: Manage SDK PR
        env:
          GH_TOKEN: ${{ secrets.SDK_REPOS_PAT }}
        run: |
          branch="${{ github.event.pull_request.head.ref }}"
          was_merged="${{ github.event.pull_request.merged }}"

          pr_number=$(gh pr list --repo "your-org/${{ matrix.repo }}" \
            --head "$branch" --json number --jq '.[0].number')

          if [[ -n "$pr_number" ]]; then
            if [[ "$was_merged" == "true" ]]; then
              gh pr merge "$pr_number" --repo "your-org/${{ matrix.repo }}" \
                --squash --delete-branch
            else
              gh pr close "$pr_number" --repo "your-org/${{ matrix.repo }}"
            fi
          fi
```

## SDK Repository Workflow

Each SDK repo needs a dispatchable workflow:

```yaml
# .github/workflows/sdk_generation.yaml (in each SDK repo)
name: SDK Generation
on:
  workflow_dispatch:
    inputs:
      feature_branch:
        description: 'Feature branch from spec repo'
        required: false

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Create branch
        if: inputs.feature_branch != ''
        run: git checkout -b "${{ inputs.feature_branch }}"

      - name: Generate SDK
        run: speakeasy run -y
        env:
          SPEAKEASY_API_KEY: ${{ secrets.SPEAKEASY_API_KEY }}

      - name: Create PR
        if: inputs.feature_branch != ''
        run: |
          git add -A && git commit -m "chore: regenerate SDK" || exit 0
          git push -u origin "${{ inputs.feature_branch }}"
          gh pr create --title "SDK update" --body "Auto-generated" || true
```

## Required Secrets

| Secret | Where | Purpose |
|--------|-------|---------|
| `SPEAKEASY_API_KEY` | All repos | Speakeasy CLI auth |
| `SDK_REPOS_PAT` | Spec repo | PAT with `repo` scope for SDK repos |

## PR Status Reporting

Report SDK generation status back to spec PR:

```yaml
- name: Update PR comment
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    marker="<!-- sdk-${{ matrix.repo }}-status -->"
    comment="$marker
    ### ${{ matrix.repo }} SDK
    | Status | PR |
    |--------|-----|
    | ✅ Success | [View PR](url) |"

    gh api "repos/${{ github.repository }}/issues/${{ github.event.pull_request.number }}/comments" \
      -f body="$comment"
```

## Multi-Repo vs Monorepo

| Aspect | Multi-Repo | Monorepo |
|--------|-----------|----------|
| Isolation | Independent versioning | Shared versioning |
| CI Complexity | Higher | Lower |
| Best For | Different teams/cadences | Unified releases |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| PAT permissions | Ensure `repo` + `actions` scope |
| Branch not found | SDK repo must have workflow on `main` |
| PR not created | Check if branch already has PR |

## Related Skills

- `start-new-sdk-project` - SDK repo setup
- `orchestrate-multi-target-sdks` - Single repo, multiple targets
