---
name: skill-dev-workflow
version: 0.4.0
description: "Orchestrate the 9-step skill development lifecycle for the CaldiaWorks Skills repository. Guides through ideation, issue creation, planning, branch creation, requirements definition, skill implementation, commit, pull request, and post-merge issue cleanup. Use when: skill development workflow, develop a skill end-to-end, skill-dev-workflow, /skill-dev-workflow, create and publish a skill."
---

# Skill Development Workflow

Orchestrate the full lifecycle of creating a skill for the CaldiaWorks marketplace. This skill is specific to the CaldiaWorks Skills repository.

## Mandatory Execution Rule

Each invoked skill defines its own internal steps. **Every internal step of every invoked skill must be executed in order without exception.** Do not skip, merge, or silently omit any step -- even if the step seems trivial or the answer seems obvious.

Only ask the user for input that cannot be derived from available context (issue titles, document content, git history, etc.). If a step produces output, present it. Violating this rule degrades quality and erodes user trust.

## Partial Workflow Entry

If the user already has artifacts from earlier steps, skip completed steps:

| Existing Artifact | Start From |
|-------------------|------------|
| Idea document | Step 2: Issue Creation |
| Issue number | Step 3: Planning |
| Plan document | Step 4: Branch Creation |
| USDM requirements document | Step 6: Skill Implementation |

Ask the user what artifacts they already have before starting.

## Workflow Steps

Execute these 9 steps in order. Proceed automatically from one step to the next.

### Step 1: Ideation

Invoke the `ideation` skill.

- Input: User's rough idea or problem description
- Output: Idea document at `.docs/ideas/YYYY-MM-DD-<topic>.md`
- Pass the idea document path to Step 5 (USDM)

### Step 2: Issue Creation (Parent Issue)

Invoke the `issue-create` skill in standalone mode.

- Input: Summary from the idea document
- Output: GitHub Issue number and URL
- Pass the issue number to Step 3 (Planning)

### Step 3: Planning

Invoke the `planning` skill.

- Input: The parent issue number from Step 2
- Output: Plan document at `.docs/plans/YYYY-MM-DD-<topic>.md`
- Pass the plan document and first work unit's issue numbers to Step 4

Update the plan document: set the first work unit's Status to `In Progress`.

### Step 4: Branch Creation

Invoke the `branch-create` skill.

- Input: Issue number and description from the plan's first work unit
- Output: Feature branch name

Update the plan document: set the work unit's Branch to the created branch name.

### Step 5: Requirements Definition (USDM)

Invoke the `usdm` skill.

- Input: The idea document from Step 1
- Output: USDM requirements document at `.docs/REQ-DOC-*.md`

After USDM completes, invoke the `issue-create` skill in USDM mode to create requirement sub-issues:
- Input: USDM document path + parent issue number from Step 2
- This creates all REQ issues as sub-issues with SPECs in the body

### Step 6: Skill Implementation

Invoke the `skill-creator` skill.

- Input: The USDM requirements document from Step 5
- Output: Complete skill directory under `skills/<skill-name>/`
- The skill must include `SKILL.md` with frontmatter

After `skill-creator` completes:
1. Add the skill path to both `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.
2. Bump the version in both manifest files to the same value.

### Step 7: Commit

Invoke the `commit` skill.

- Input: All changes from Steps 4-6
- Commits may be made multiple times during implementation for safety

### Step 8: Pull Request

Invoke the `pull-request` skill.

- Input: The feature branch with all commits
- Output: PR number and URL

After the PR is merged or the user confirms completion, update the plan document: set the work unit's Status to `Done`.

### Step 9: Issue Cleanup

After the PR is merged, close all remaining open sub-issues under the parent issue.

1. List open sub-issues of the parent issue: `gh sub-issue list <parent-issue-number>`
2. For each open sub-issue, recursively list and close its own sub-issues first (bottom-up).
3. Close each open sub-issue with a comment referencing the merged PR.

This is necessary because `Resolves #N` in commit messages only auto-closes the directly referenced issues. Sub-issues created from USDM requirements (sub-REQs) are not auto-closed and must be closed explicitly.

## Plan Progress Tracking

Throughout the workflow, keep the plan document up to date:

| Event | Update |
|-------|--------|
| Work unit begins | Status: `Pending` -> `In Progress` |
| Branch created | Branch: `TBD` -> branch name |
| PR merged or user confirms completion | Status: `In Progress` -> `Done` |

## Before Finishing

After the workflow completes (or when the user stops at any step), verify nothing is left behind:

- **Open issues?** Are there sub-issues under the parent issue that should be closed? Step 9 handles this after merge, but if the workflow is interrupted earlier, flag any open issues to the user.
- **Uncommitted changes?** Run `git status` to check for changes that were not included in the final commit.
- **Plan up to date?** Does the plan document reflect the actual state of all work units (Status and Branch columns)?

## Constraints

- This skill is specific to the CaldiaWorks Skills repository.
- Always follow the project's git workflow: feature branches, squash merge, no direct commits to main.
- Do not skip marketplace registration after skill creation.
