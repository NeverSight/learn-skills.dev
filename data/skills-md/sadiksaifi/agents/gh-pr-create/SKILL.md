---
name: gh-pr-create
description: >-
  Use when opening a pull request, submitting code for review, or when the user
  says "create PR," "open PR," or "/gh-pr-create." Generates conventional-commit
  title and structured body from branch commits.
---

Generate and submit a GitHub pull request from the current feature branch.

**Iron laws:** (1) No PR without user preview. (2) No raw commit dumps — always synthesize.

## The Process

### Step 1: Validate & Push

Gather state and fail fast:

```bash
BASE=$(gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name')
HEAD=$(git branch --show-current)
COMMITS=$(git log "$BASE".."$HEAD" --oneline)
```

**Stop if:** `$HEAD` equals `$BASE`, or `$COMMITS` is empty, or `gh pr view --json url 2>&1` shows an existing PR.

**Dirty working tree:** If `git status --porcelain` is non-empty, warn: "You have uncommitted changes that won't be included in this PR."

**Push** if upstream is not set or local is ahead: `git push -u origin "$HEAD"`

### Step 2: Gather Context & Generate Content

```bash
git log "$BASE".."$HEAD" --pretty=format:'%h %s' --reverse
git diff --stat "$BASE".."$HEAD"
```

**Detect PR template:** Check `gh repo view --json pullRequestTemplates` first. If none, use [references/pr-template.md](references/pr-template.md).

**Generate title** — conventional-commit format: `type(scope): subject`

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`, `perf`. Imperative, lowercase, no period, under 50 chars. Single commit: reuse if already conventional. Multiple: synthesize dominant type.

**Fill the body:**
- **Single commit:** Use the commit's full message to fill the template.
- **Multiple commits:** Synthesize a summary. Group changes by logical area.
- **Low-quality commits** (e.g., "fix", "wip"): Ask the user what changed and why.

**Linked issues:** Scan commit messages for `Closes #X`, `Fixes #X`, or `Resolves #X`. If found, include them. If none found, ask briefly: "Any issues to link?"

**Irrelevant template sections:** Write "N/A" — don't delete them.

### Step 3: Preview

Show the preview:

```
═══ PR PREVIEW ═══════════════════════
Title: type(scope): subject
Base: main ← Head: feature-branch
Body:
──────────────────────────────────────
[full body content]
──────────────────────────────────────
Closes: #123, #456 (or "None")
══════════════════════════════════════
```

Ask: **"Create this PR? (yes / edit / cancel)"**

<HARD-GATE>USER APPROVAL — preview must be approved before creation</HARD-GATE>

### Step 4: Create

```bash
gh pr create --base "$BASE" --title "$TITLE" --body "$BODY"
```

Print PR URL. If issues linked, note they'll auto-close on merge.
