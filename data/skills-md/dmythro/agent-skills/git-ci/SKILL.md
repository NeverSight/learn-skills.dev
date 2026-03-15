---
name: git-ci
description: CI/CD status queries for GitHub Actions (gh) and GitLab CI (glab). Check
  pipeline status, failing jobs, workflow runs, and merge readiness
---

# CI/CD Status Queries

**Query CI/CD pipelines and check merge readiness across GitHub Actions and GitLab CI.** All recipes use minimal field sets for token efficiency. Covers pipeline status, failing jobs, run logs, workflow management, and merge readiness assessment.

## When to Use

- **Checking CI status** -- "are checks passing?", "what's failing?", pipeline status
- **Watching CI runs** -- wait for completion, fail-fast on errors
- **Debugging failures** -- view logs for failing jobs, identify flaky tests
- **Assessing merge readiness** -- all checks green, reviews approved, no conflicts
- **Listing workflow runs** -- recent pipelines, specific workflow history
- **Configuring CI allowlists** -- auto-approval patterns for read-only CI commands

## Critical Rules

1. **Use `gh pr checks` (not `gh run`) for current-branch CI status.** The `pr checks` subcommand maps directly to the PR's required status checks.
2. **Use `glab ci status` for current-branch CI in GitLab.** It shows the pipeline for the current branch without needing a pipeline ID.
3. **Always use `--json` with `gh` to filter output fields.** Full JSON output wastes tokens.

---

## Provider Detection

```bash
git remote get-url origin
```

| Remote URL contains                | Provider | CLI    | CI system        |
|------------------------------------|----------|--------|------------------|
| `github.com`                       | GitHub   | `gh`   | GitHub Actions   |
| `gitlab.com` or self-hosted GitLab | GitLab   | `glab` | GitLab CI        |

If ambiguous or both present, ask the user.

---

## CI Status (Current Branch)

**GitHub:**
```bash
gh pr checks --json name,state,conclusion,bucket
```

**GitLab:**
```bash
glab ci status
```

## CI Status as JSON

**GitHub:**
```bash
gh pr checks --json name,state,conclusion,bucket
```

**GitLab:**
```bash
glab ci get
```

## Watch Until Complete

**GitHub:**
```bash
gh pr checks --watch --fail-fast
```

**GitLab:**
```bash
glab ci status --live
```

## Recent Pipeline/Workflow Runs

**GitHub:**
```bash
gh run list --json databaseId,displayTitle,status,conclusion,headBranch,event --limit 10
```

**GitLab:**
```bash
glab ci list
```

## Specific Run Details

**GitHub:**
```bash
gh run view {run_id} --json jobs,status,conclusion,displayTitle
```

**GitLab:**
```bash
glab ci view {pipeline_id}
```

## Run Logs

**GitHub:**
```bash
gh run view {run_id} --log-failed
```

**GitLab:**
```bash
glab ci trace {job_id}
```

---

## Merge Readiness (Current Branch)

**GitHub:**
```bash
gh pr view --json mergeable,reviewDecision,statusCheckRollup,isDraft,mergeStateStatus
```

Fields:
- `mergeable` -- `MERGEABLE`, `CONFLICTING`, or `UNKNOWN`
- `reviewDecision` -- `APPROVED`, `CHANGES_REQUESTED`, `REVIEW_REQUIRED`, or empty
- `isDraft` -- boolean
- `mergeStateStatus` -- `CLEAN`, `BLOCKED`, `BEHIND`, `DIRTY`, `UNSTABLE`

**GitLab:**
```bash
glab mr view -F json | jq '{merge_status:.merge_status,conflicts:.has_conflicts,blocking:.blocking_discussions_resolved,draft:.draft}'
```

---

## Variables and Secrets

**GitHub:**
```bash
gh variable list
gh secret list
```

**GitLab:**
```bash
glab variable list
```

---

## CI Queries Reference

> **Reference**: See `references/ci-queries.md` for advanced patterns: failing check extraction, required checks, workflow listing, cache management, rulesets.

---

## Allowlist

> **Reference**: See `references/allowlist.md` for tiered `Bash(command:*)` patterns covering all read-only CI operations -- safe to auto-approve in Claude Code `settings.json` or OpenCode config.
