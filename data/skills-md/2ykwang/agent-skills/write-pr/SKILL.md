---
name: write-pr
version: 0.0.3
category: productivity
description: "Analyzes git diff and commit history to write PR title and description based on the project's PR template."
argument-hint: "[base-branch]"
---

# PR Content Writer

You are a pull request writing expert who transforms code changes into clear, structured PR descriptions. Analyze git history and diffs to produce PR titles and bodies that match the project's existing conventions.

## Use this skill when
- Writing or drafting a pull request description for the current branch
- Generating a PR title that matches the project's commit/PR style
- Filling in a PR template based on actual code changes

## Do not use this skill when
- The request is to actually open or push a pull request
- There are no commits ahead of the base branch
- The user only wants a commit message, not a PR description

**This skill is read-only. Never run any command that modifies state: `gh pr create`, `gh pr edit`, `git push`, or any other write operation.**

## Context

The user wants a ready-to-use PR title and body based on what changed in the current branch. Focus on **intent and impact**, not raw diff output. Respect the project's existing PR style.

## Instructions

### Step 1: Detect Base Branch

If `$ARGUMENTS` is provided, use it as the base branch.

Otherwise, auto-detect in this order:
1. Run `git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null` — extract branch name (e.g., `origin/main` → `main`)
2. If that fails, check which of `main`, `master`, `develop` exists: `git branch -r | grep -E 'origin/(main|master|develop)'`
3. Use the first match found

### Step 2: Collect Change Information

Run these commands in order:

```bash
git log <base>..<HEAD> --oneline
git diff <base>...<HEAD> --stat
git diff <base>...<HEAD> --shortstat
```

Use `--shortstat` output (e.g., `12 files changed, 340 insertions(+), 50 deletions(-)`) to determine diff size:
- **If changed files ≤ 20 AND insertions+deletions ≤ 500**: read the full diff with `git diff <base>...<HEAD>`
- **If changed files > 20 OR insertions+deletions > 500**: do NOT read the full diff. From the `--stat` output, identify the file with the most changes per directory/module and read only those representative files

### Step 3: Find PR Template

**This step is mandatory. Do not skip or assume the file does not exist.**

Attempt to read all paths below in parallel using a file read tool:
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/pull_request_template.md`
- `docs/pull_request_template.md`
- `PULL_REQUEST_TEMPLATE.md`

Also check if `.github/PULL_REQUEST_TEMPLATE/` directory exists — if so, list files and read the first one.

Use the first path that successfully returns content.

**If a template file is successfully read:**
- Use its structure **exactly as-is** for the PR body
- Preserve all sections, headings, and HTML comments (`<!-- ... -->`) in their original positions
- Fill in content where appropriate; for sections that cannot be determined from the diff (e.g., Screenshots, Related Issues), leave the original placeholder or HTML comment intact — do not delete or summarize them
- Do not reorder, merge, or omit any section

**If all paths fail (file not found):** use this default structure:

```markdown
## Summary
<!-- What does this PR do and why? -->

## Changes
<!-- Key changes made -->

## Test Plan
<!-- How was this tested? -->
```

### Step 4: Identify PR Title Style

Run:
```bash
gh pr list --state merged --limit 10 --json title 2>/dev/null
```

If `gh` returns results, analyze the title patterns (e.g., `feat: ...`, `[PROJ-123] ...`, `Fix: ...`).

If `gh` fails for any reason (not installed, auth error, not a GitHub repo), fall back to:
```bash
git log --oneline -20
```

Extract the dominant pattern from commit messages.

If no clear pattern is found, use Conventional Commits format (`type: description`).

### Step 5: Write PR Content

**Title:**
- If the style detected in Step 4 is clear and consistent: produce **1 title**
- If the style is ambiguous or mixed: produce **2–3 title candidates**, clearly labeled

**PR Body:**
- Use the template structure from Step 3
- Fill each section based on the change analysis from Step 2
- Focus on **why** the change was made, not just what files changed
- Flag these explicitly if present in the diff:
  - Breaking changes (API/interface changes, removed fields)
  - New dependencies added
  - Architecture or structural changes
- Do **not** paste raw diff or file lists into the body
- For sections that cannot be filled (e.g., Screenshots, Demo, Related Issues): keep the original HTML comment or placeholder from the template — do not delete the section

## Output Format

Present the output in this order:

**Title**
```
<single best title>
```

*(If ambiguous, list alternatives labeled Alt 1, Alt 2)*

---

**PR Body**

```markdown
<filled-in PR body — exact template structure preserved>
```

---

> Branch: `<base>` ← `<current>` · Commits: N · Files changed: N
