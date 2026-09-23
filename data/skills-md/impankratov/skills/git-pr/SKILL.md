---
name: git-pr
description: >
  Create merge requests and pull requests per project conventions. Use when the
  user asks to create an MR, PR, merge request, or pull request, or says "commit
  and MR" for the MR step. Load before pushing or creating any PR/MR.
---

# git-pr

Create a pull request following project conventions.

## Execution

### Step 1 — Read project guidelines (HARD GATE)

You MUST find and read the project's PR/MR documentation **in full** before proceeding. If none exists, use sensible defaults.

- Never pass a `limit` (or equivalent partial read) on any PR/MR doc file.
- Search the repo for all related docs (`*mr*`, `*pr*`, `*pull*`, `*merge*`, `*backport*`) and read each match that applies to the operation.
- If the project has an MR doc, read the primary one end-to-end (including settings, labels, and CLI-creation sections if present).
- If the operation is a backport and a backport doc exists, read it end-to-end before cherry-pick or the MR/PR creation step.

**Proof of work (required in your first PR/MR reply):** one line listing the doc files read and sections used, e.g. "Read MR-workflow.md: settings, labels, CLI example; backport procedure: step 5". Name only the files you actually read.

**Completion**: PR format, required sections, and mandatory CLI flags or labels — only those the project's guidelines require — identified.

### Step 2 — Determine PR information

Check for issue reference in the branch name or user input. If found, use it to populate PR title and body.

Otherwise, infer PR information from the changes themselves. Only ask the user if you cannot determine it.

**Completion**: PR title, description, and metadata ready.

### Step 3 — Create PR

Push the branch and create the PR using the project's standard tooling.

- Provide a human-readable description relevant to PR content
- Do not list commits or include useless filler
- Only add labels if required by project guidelines

**Completion**: PR created.

### Step 4 — Verify and report

1. Confirm target branch, settings, and assignee are correct
2. Capture the PR URL from CLI output — use that URL only, never one you constructed
3. Output the URL as a bare line with no markdown wrapping

**Completion**: URL reported.
