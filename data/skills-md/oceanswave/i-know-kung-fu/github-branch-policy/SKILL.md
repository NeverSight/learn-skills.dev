---
name: github-branch-policy
description: Audit GitHub repository branch governance and workflow hygiene. Use when asked to review rulesets, required status checks, update restrictions, bypass/update behavior, delete-on-merge settings, auto-merge workflow reliability, stale branches, ghost workflow registrations, or branch-policy drift.
---

# GitHub Branch Policy

## Overview

Run a repeatable audit for GitHub branch policy safety and Actions workflow hygiene. Validate ruleset enforcement, required checks, workflow registration integrity, and branch cleanup behavior that commonly break CI and auto-merge.

This skill explicitly checks for real-world failure modes where:
- auto-merge is enabled and checks are green, but PRs remain `BEHIND`/`BLOCKED`, and
- auto-merge enablement fails transiently (for example GitHub API 502), leaving PRs stranded.

## Use This Skill When

Apply this skill for requests like:
- "Audit branch protection/rulesets on this repo."
- "Check whether auto-merge and branch cleanup are configured correctly."
- "Find ghost workflows or stale branches causing Actions failures."
- "Why are we getting `Cannot update this protected ref`?"
- "Why is auto-merge enabled but nothing merges?"
- "Make sure branch policy matches solo-developer expectations."

## Prerequisites

- `gh` authenticated for the target repo (`repo` + `workflow` scopes).
- `jq` available.
- Target repository known as `OWNER/REPO`, or current directory is a checked-out repo with a GitHub remote.

## Quick Setup

```bash
OWNER_REPO="${OWNER_REPO:-$(gh repo view --json nameWithOwner -q .nameWithOwner)}"
OWNER="${OWNER_REPO%/*}"
REPO="${OWNER_REPO#*/}"
DEFAULT_BRANCH="$(gh repo view "$OWNER_REPO" --json defaultBranchRef -q .defaultBranchRef.name)"
echo "Auditing $OWNER_REPO (default: $DEFAULT_BRANCH)"
```

## Known Good Baseline (Solo-Maintainer Friendly)

- Repository has `allow_auto_merge: true`.
- Active default-branch ruleset includes `pull_request` and `required_status_checks`.
- Required status check contexts exactly match live check names.
- Default-branch ruleset has no bypass actors (`bypass_actors: []`).
- Required status check contexts are limited to merge-critical gates; non-critical provider checks (for example `Vercel Preview Comments`) may not be present and may unintentionally break auto-merge.
- `update` rule is optional:
  - If enabled, bypass actors must be intentionally configured.
  - If not needed for your workflow, remove it to prevent unnecessary `BLOCKED` states.
- Branch updater workflow is not `push`-only (has at least one fallback trigger such as `pull_request_target`, `schedule`, or `workflow_dispatch`).
- Branch updater verifies required CI checks are present on the latest PR head SHA after any update-branch operation.
- Auto-merge workflow tolerates transient API failures (retry/backoff).
- `delete_branch_on_merge: true` (or equivalent cleanup automation).

## Audit Checklist

### 1. Repository merge settings are compatible with policy

Verification:
```bash
gh api "repos/$OWNER/$REPO" \
  --jq '{allow_auto_merge,allow_squash_merge,allow_merge_commit,allow_rebase_merge,delete_branch_on_merge,default_branch}'
```

Pass criteria:
- `allow_auto_merge: true` when auto-merge is expected.
- Merge methods match branch rules (for example, squash-only policy means squash is enabled).
- `delete_branch_on_merge: true` unless intentionally disabled.

Remediation:
- Enable auto-merge at repo level.
- Align repo merge methods with ruleset `allowed_merge_methods`.
- Enable delete-on-merge, or document why not.

---

### 2. Active ruleset applies to default branch and enforces PR + required checks

Verification:
```bash
gh api "repos/$OWNER/$REPO/rulesets" \
  --jq '.[] | {id,name,enforcement,target,include:(.conditions.ref_name.include // []),rules:[.rules[].type]}'
gh api "repos/$OWNER/$REPO/rulesets" \
  --jq '.[] | select(.enforcement=="active") | .rules[] | select(.type=="pull_request" or .type=="required_status_checks" or .type=="update")'
```

Pass criteria:
- At least one active branch ruleset applies to `~DEFAULT_BRANCH` (or equivalent explicit default branch include).
- Ruleset includes `pull_request` and `required_status_checks`.
- `update` may be present or absent, but must be intentional.

Remediation:
- Enable or create a default-branch ruleset.
- Add missing `pull_request` and `required_status_checks` rules.
- Remove accidental `update` if it is not part of your branch update strategy.

---

### 3. Required check contexts match real check names

Verification:
```bash
gh api "repos/$OWNER/$REPO/rulesets" \
  --jq '.[] | .rules[] | select(.type=="required_status_checks") | .parameters.required_status_checks[].context'
gh pr list --state all --limit 20 --json number \
  --jq '.[0].number' | xargs -I{} gh pr view {} --json statusCheckRollup
```

Pass criteria:
- Required contexts exactly match real checks reported on PRs (case-sensitive), for example `ci`, `Vercel`, `Vercel Preview Comments`.

Remediation:
- Update required check contexts in the ruleset to match actual check names.

---

### 4. `update` rule and bypass actors are compatible with your auto-merge flow

Verification:
```bash
gh api "repos/$OWNER/$REPO/rulesets" \
  --jq '.[] | select(.enforcement=="active" and .target=="branch") |
    {id,name,has_update:([.rules[].type] | index("update") != null),
     bypass_actors:((.bypass_actors // []) | map({actor_type,actor_id,bypass_mode}))}'
```

Pass criteria:
- If `has_update` is `false`, this is acceptable when no branch-update automation is required.
- If `has_update` is `true`, bypass actors and modes are intentionally set so trusted maintainers/automation can still complete merges.

Remediation:
- For solo-maintainer repos, prefer removing unneeded `update` requirements.
- Remove bypass actors from the default-branch ruleset.
- If emergency bypass is temporarily required, keep scope minimal, time-box it, document owner approval, and remove it immediately after incident resolution.
- Re-test with a smoke PR after policy changes.

---

### 5. Solo-dev compatibility: CODEOWNERS review is not forced unless intentional

Verification:
```bash
gh api "repos/$OWNER/$REPO/rulesets" \
  --jq '.[] | {name, pull_request_rules:[.rules[] | select(.type=="pull_request") | .parameters.require_code_owner_review]}'
```

Pass criteria:
- For solo-maintainer repos, `require_code_owner_review` is `false` unless intentionally required.

Remediation:
- Set `require_code_owner_review: false` where solo-dev flow is desired.

---

### 6. Actions policy allows the workflow dependencies you actually use

Verification:
```bash
gh api "repos/$OWNER/$REPO/actions/permissions" \
  --jq '{enabled,allowed_actions,sha_pinning_required}'
gh api "repos/$OWNER/$REPO/actions/permissions/selected-actions" \
  --jq '{github_owned_allowed,verified_allowed,patterns_allowed}'
```

Pass criteria:
- If `allowed_actions: selected`, all actions used by workflows are explicitly allowed (or covered by allowed classes).
- If SHA pinning is required, actions are pinned.

Remediation:
- Add missing action patterns to selected-actions policy.
- Pin unpinned actions.
- Prefer minimal/no third-party actions for sensitive auto-merge workflows.

---

### 7. Auto-merge workflow registration is clean (no ghost duplicates)

Verification:
```bash
gh api "repos/$OWNER/$REPO/actions/workflows" \
  --jq '.workflows[] | [.id,.name,.path,.state] | @tsv' | sort
gh workflow list --all
```

Pass criteria:
- Exactly one active registration for the canonical auto-merge workflow path.
- Legacy/stale registrations are disabled or removed.

Remediation:
- Disable stale workflow IDs:
```bash
gh workflow disable <workflow_id>
```
- Keep a single canonical filename on default branch.

---

### 8. Auto-merge workflow trigger and runtime behavior are reliable

Verification:
```bash
AUTO_WF="Enable PR Auto-Merge"  # adjust if needed
gh workflow view "$AUTO_WF" --yaml | sed -n '1,260p'
gh run list --workflow "$AUTO_WF" --limit 20 \
  --json databaseId,event,status,conclusion,headBranch,createdAt,url
```

Deep check for suspicious runs:
```bash
RUN_ID="<id>"
gh run view "$RUN_ID" --json event,conclusion,jobs
# Log text is critical for transient API failures (502/503/etc.)
gh run view "$RUN_ID" --log-failed | sed -n '1,260p'
```

Pass criteria:
- Trigger is intentionally chosen (`pull_request_target` is often safer for base-branch-controlled orchestration; `pull_request` is valid when branch consistency is guaranteed).
- Recent PR-event runs execute real jobs.
- Workflow handles transient GitHub failures (retry/backoff or equivalent).
- No repeating failures with `push` event + zero jobs + missing logs (ghost workflow symptom).

Remediation:
- Move to a stable default-branch workflow file.
- Use `pull_request_target` when orchestration must run from trusted base branch context.
- Add retry/backoff around `gh pr merge --auto ...` to avoid one-off 5xx failures stranding PRs.
- Disable stale workflow registrations.

---

### 9. Branch updater trigger coverage and run recency are reliable

Verification:
```bash
UPDATE_WF="Auto Update PR Branches"
gh workflow view "$UPDATE_WF" --yaml | sed -n '1,320p'
gh run list --workflow "$UPDATE_WF" --limit 30 \
  --json databaseId,event,status,conclusion,headBranch,headSha,createdAt,url
```

Correlate recent default-branch commits with updater runs:
```bash
git fetch origin "$DEFAULT_BRANCH"
git log --oneline -n 15 "origin/$DEFAULT_BRANCH"
# Check whether updater has runs for recent headSha values
```

Pass criteria:
- Updater is not `push`-only in environments where merges are performed by automation/apps.
- At least one fallback trigger exists (`pull_request_target`, `schedule`, or `workflow_dispatch`).
- Updater runs continue to appear after recent merges to default branch.

Remediation:
- Add fallback triggers to updater workflow (`pull_request_target`, `schedule`, `workflow_dispatch`).
- Add `concurrency` guard to avoid overlapping updater runs.
- Keep updater green when one PR cannot update, so other PRs still progress.

---

### 10. PR-level auto-merge state is actually mergeable (not just enabled)

Verification:
```bash
gh pr list --state open --limit 30 \
  --json number,title,isDraft,mergeStateStatus,autoMergeRequest \
  --jq '.[] | {number,title,isDraft,mergeStateStatus,autoMergeEnabled:(.autoMergeRequest != null)}'
```

Deep check:
```bash
PR_NUMBER="<pr_number>"
gh pr view "$PR_NUMBER" \
  --json autoMergeRequest,mergeStateStatus,isDraft,reviewDecision,statusCheckRollup
```

Pass criteria:
- PRs intended to auto-merge show `autoMergeEnabled: true`.
- Once checks and reviews are satisfied, `mergeStateStatus` is no longer `BLOCKED`/`BEHIND` for long periods.

Remediation:
- If PRs stay `BLOCKED` with green checks, verify ruleset gates first:
  - required status checks exact name match
  - `update` rule/bypass compatibility
  - review requirements
- If PRs stay `BEHIND`, verify branch updater trigger coverage and run recency.
- Adjust ruleset/workflows, then re-test with a throwaway PR.

---

### 10a. Required checks are attached to the latest PR head SHA

This catches the incident pattern where a branch updater creates a new PR head commit, but `ci` only exists on the previous SHA, leaving auto-merge `BLOCKED`.

Verification:
```bash
PR_NUMBER="<pr_number>"
gh pr view "$PR_NUMBER" \
  --json headRefName,headRefOid,mergeStateStatus,statusCheckRollup

HEAD_SHA="$(gh pr view "$PR_NUMBER" --json headRefOid -q .headRefOid)"
gh api "repos/$OWNER/$REPO/commits/$HEAD_SHA/check-runs" \
  --jq '[.check_runs[] | {name,status,conclusion}]'
```

Pass criteria:
- Every required status check context appears on the PR's current `headRefOid`.
- If updater automation changed the head SHA, required checks (especially `ci`) are present or queued on that new SHA.

Remediation:
- Immediate unstick:
```bash
HEAD_REF="$(gh pr view "$PR_NUMBER" --json headRefName -q .headRefName)"
gh workflow run CI --ref "$HEAD_REF"
```
- Permanent fix:
  - Re-resolve `headRefName` + `headRefOid` after updater actions.
  - Verify required checks on that exact SHA.
  - Dispatch CI when required checks are missing.
  - Keep non-critical checks out of required-status contexts.

---

### 11. `Cannot update this protected ref` diagnostics for branch-update workflows

Verification:
```bash
gh workflow list --all
gh run list --workflow "Auto Update PR Branches" --limit 20 \
  --json databaseId,status,conclusion,event,headBranch,createdAt,url
```

Pass criteria:
- Workflow updates eligible PR branches successfully.
- Protected or fork branches are skipped/handled without failing the entire run.

Remediation:
- In update-branch loops, continue on protected/fork failures.
- Skip PR heads that are protected or not writable.
- Treat this as per-PR conditional failure, not a global workflow failure.

---

### 12. Branch cleanup strategy is in place

Verification:
```bash
gh api "repos/$OWNER/$REPO" --jq '{delete_branch_on_merge}'
gh api "repos/$OWNER/$REPO/actions/workflows" \
  --jq '.workflows[] | {name,path,state}'
```

Pass criteria:
- `delete_branch_on_merge: true`, or equivalent cleanup workflow exists and is active.

Remediation:
- Enable delete-on-merge.
- Add/repair cleanup workflow if additional cleanup behavior is required.

---

### 13. No stale branches from merged/closed PRs

Verification:
```bash
gh api "repos/$OWNER/$REPO/branches" --paginate --jq '.[].name' | sort -u > /tmp/live-branches.txt
gh pr list --state merged --limit 500 --json headRefName --jq '.[].headRefName' | sort -u > /tmp/merged-pr-branches.txt
gh pr list --state closed --limit 500 --json headRefName,mergedAt \
  --jq '.[] | select(.mergedAt==null) | .headRefName' | sort -u > /tmp/closed-pr-branches.txt
cat /tmp/merged-pr-branches.txt /tmp/closed-pr-branches.txt | sort -u > /tmp/candidate-stale-branches.txt
comm -12 /tmp/live-branches.txt /tmp/candidate-stale-branches.txt
```

Pass criteria:
- Intersection output is empty, excluding intentional long-lived branches.

Remediation:
- Delete confirmed stale branches:
```bash
git push origin --delete "<branch>"
```

---

### 14. Rulesets are primary policy and legacy protection is not conflicting

Verification:
```bash
gh api "repos/$OWNER/$REPO/rulesets" --jq 'length'
gh api "repos/$OWNER/$REPO/branches/$DEFAULT_BRANCH/protection" 2>/dev/null | jq '.'
```

Pass criteria:
- Rulesets are the primary mechanism.
- Legacy branch protection is absent or intentionally non-overlapping.
- If branch protection endpoint returns 404 while rulesets exist, that is expected.

Remediation:
- Consolidate policy into rulesets.
- Remove redundant legacy branch protection after parity validation.

## Optional Smoke Test (Recommended for Auto-Merge Incidents)

1. Create a temporary PR from a throwaway branch.
2. Enable auto-merge on the PR.
3. Confirm auto-merge is enabled:
```bash
gh pr view <pr_number> --json autoMergeRequest,mergeStateStatus
```
4. Confirm auto-merge workflow ran and executed jobs:
```bash
gh run list --workflow "Enable PR Auto-Merge" --limit 5
```
5. Confirm branch updater can clear `BEHIND` without manual intervention.
6. Confirm PR actually merges after checks pass (not just auto-merge enabled).
7. Close/delete throwaway branch if still open.

## Fast Unstick Playbook (Operational)

Use this only for incident response, then fix root cause in workflow/ruleset config.

```bash
# Re-enable auto-merge if missing
gh pr merge <pr_number> --auto --squash --repo "$OWNER_REPO"

# Force update a behind branch
gh api --method PUT "repos/$OWNER/$REPO/pulls/<pr_number>/update-branch" -f update_method=merge

# Ensure required CI exists on current head
HEAD_REF="$(gh pr view <pr_number> --json headRefName -q .headRefName)"
gh workflow run CI --ref "$HEAD_REF"

# Re-check status
gh pr view <pr_number> --repo "$OWNER_REPO" \
  --json headRefOid,mergeStateStatus,autoMergeRequest,statusCheckRollup
```

## Tooling Notes (CLI Gotchas)

- `gh api` does not support `--repo`; use full endpoint paths like `repos/$OWNER/$REPO/...`.
- In zsh, quote `gh api` endpoints that include `?` query strings:
  - `gh api 'repos/$OWNER/$REPO/actions/workflows/<id>/runs?per_page=20'`

## Report Format

```markdown
## Branch Policy Audit Report
- Repository: OWNER/REPO
- Default branch: <branch>
- Timestamp (UTC): <iso8601>
- Overall status: PASS | NEEDS_ACTION | BLOCKED

### Findings
1. [SEV-<1-3>] <check name> - <pass/fail summary>
   Evidence: <key command output summary>
   Remediation: <next action>

### Actions Taken
1. <action performed or "none">

### Follow-up
1. <required human decision or "none">
```

## Guardrails

- Do not delete branches until confirmed stale and unprotected.
- Do not disable workflows blindly; verify canonical registration first.
- Default policy is no bypass actors on default-branch rulesets unless there is a documented, time-boxed incident exception.
- Treat `push + 0 jobs + no logs` on workflow runs as likely ghost/stale registration evidence.
- Do not treat `autoMergeRequest != null` as success by itself. Verify `mergeStateStatus` and actual merge outcome.
- Prefer deterministic `gh api` evidence over assumptions.
- If permissions are insufficient, report missing scope/permission and continue with remaining checks.
