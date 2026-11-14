---
name: repo-health
description: "One-command GitHub repository health audit. Checks for missing standard files, GitHub configuration, branch protection, documentation quality, and code hygiene. Produces a scored health report with prioritized fix recommendations."
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: devops
  domain: github
  updated: 2026-03-19
  tested: 2026-03-19
  tested_with: "Claude Code v2.1"
---

# Repo Health

One-command health audit for GitHub repositories. Produces a scored report with prioritized fix recommendations.

## Install

```bash
claude skill add --from https://github.com/thatrebeccarae/claude-marketing/skills/repo-health
```

## When to Use

- Setting up a new repo and want to make sure nothing is missing
- Periodic health checks on active repositories
- Before open-sourcing a private repo (what needs to be added?)
- Onboarding onto an unfamiliar repo to assess its state
- Pre-release hygiene sweep

## How to Use

```
/repo-health [repo-path]        # Full audit with scored report
/repo-health [repo-path] --fix  # Audit + generate missing files
```

Default `repo-path` is the current working directory if omitted.

---

## Procedure

Execute each step in order. Do not skip steps.

### Step 1: Validate Repo Path

1. If `repo-path` is provided, resolve to absolute path. If omitted, use current working directory.
2. Confirm the path exists and is a directory.
3. Confirm it contains a `.git` directory (is a git repo).

If validation fails:
```
Error: {repo-path} is not a git repository.
Provide a path to a git repo or run from within one.
```
STOP.

### Step 2: Detect Public/Private

Determine repo visibility:
1. Check for `.public-repo` marker file at repo root -> public
2. Check if "public" appears in the remote URL -> public
3. Run `gh repo view --json isPrivate -q '.isPrivate'` if `gh` is available -> use result
4. If none of the above resolve it -> ask the user

Store as `repo_visibility` (public or private). Public repos are held to a stricter standard in scoring.

### Step 3: File Presence Checks

Check for each standard file. Track result as PRESENT or MISSING.

| File | Required (Public) | Required (Private) |
|------|-------------------|--------------------|
| `LICENSE` | Yes | No |
| `README.md` | Yes | Yes |
| `.gitignore` | Yes | Yes |
| `SECURITY.md` | Yes | No |
| `CONTRIBUTING.md` | Yes | No |
| `CODEOWNERS` | Recommended | No |
| `.editorconfig` | Recommended | Recommended |
| `.github/pull_request_template.md` or `.github/PULL_REQUEST_TEMPLATE.md` | Recommended | No |
| `.github/ISSUE_TEMPLATE/` directory (or `.github/ISSUE_TEMPLATE.md`) | Recommended | No |
| `CHANGELOG.md` | Recommended | No |
| `CODE_OF_CONDUCT.md` | Recommended (public) | No |

### Step 4: GitHub Configuration Checks

Use `gh` CLI to query repo metadata. If `gh` is not available, skip this category and note it in the report.

```bash
gh repo view --json description,repositoryTopics,hasWikiEnabled,defaultBranchRef,homepageUrl
```

Check each item. Track as PASS or FAIL.

| Check | Criteria |
|-------|----------|
| Description set | `description` is non-empty |
| Topics set | `repositoryTopics` has at least 3 topics |
| Homepage URL | `homepageUrl` is set (if project has a site) |
| Default branch name | `defaultBranchRef.name` is `main` (not `master`) |
| Branch protection | `gh api repos/{owner}/{repo}/branches/main/protection` returns 200 (public repos only) |
| Social preview | `gh api repos/{owner}/{repo}` and check for custom Open Graph image (informational only) |

### Step 5: Documentation Quality

**README checks:**
1. README.md exists (from Step 3)
2. README length: < 50 lines = WARN (too short), > 500 lines = INFO (consider splitting)
3. Has a project description in the first 5 lines (H1 or bold text)
4. Has install/setup instructions (scan for "install", "getting started", "setup", "usage")
5. Has a license reference (scan for "license", "LICENSE")
6. If the `/github-readme` skill is available, note that a deeper README audit can be run via `/github:readme audit`

**CHANGELOG checks:**
1. CHANGELOG.md exists (from Step 3)
2. If present: follows Keep a Changelog format (scan for `## [` version headers)
3. Most recent entry is within the last 90 days (WARN if stale)

### Step 6: Code Hygiene

**Stale branches:**
```bash
git branch -r --merged main | grep -v main | grep -v HEAD
git for-each-ref --sort=committerdate --format='%(refname:short) %(committerdate:relative)' refs/remotes/
```
- Flag branches with no commits in > 90 days as stale
- Count total stale branches

**Tracked secrets/env files:**
```bash
git ls-files | grep -E '\.env$|\.env\.|credentials|secrets'
```
- Any `.env`, `.env.*`, `credentials.*`, or `secrets.*` files tracked in git = FAIL

**Large binary files:**
```bash
git ls-files | while read f; do
  size=$(wc -c < "$f" 2>/dev/null)
  [ "$size" -gt 5242880 ] && echo "$f ($size bytes)"
done
```
- Files > 5MB tracked in git without Git LFS = WARN
- Check for `.gitattributes` with LFS patterns if large binaries exist

**Dependency freshness (if applicable):**
- If `package.json` exists: check for `package-lock.json` presence
- If `requirements.txt` exists: check if pinned (versions specified)
- Do NOT run install commands or modify anything

### Step 7: Score and Report

#### Scoring Categories

| Category | Weight | What It Covers |
|----------|--------|----------------|
| Standard Files | 30% | LICENSE, SECURITY.md, CONTRIBUTING.md, CODEOWNERS, .gitignore, .editorconfig, templates |
| GitHub Config | 15% | Description, topics, branch protection, default branch |
| Documentation | 25% | README quality, CHANGELOG presence and freshness |
| Code Hygiene | 20% | Stale branches, tracked secrets, large binaries |
| Community | 10% | CODE_OF_CONDUCT, issue templates, PR templates, CONTRIBUTING.md |

#### Per-Category Scoring

Each category scores 0-100 based on checks passed within it. See REFERENCE.md for the full rubric.

#### Letter Grade

| Score | Grade |
|-------|-------|
| 90-100 | A |
| 80-89 | B |
| 70-79 | C |
| 60-69 | D |
| 0-59 | F |

#### Report Format

```
=== Repo Health Report: {repo-name} ===
Visibility: {public | private}
Overall Score: {score}/100 (Grade: {letter})

--- Standard Files (30%) --- Score: {n}/100
  [PASS] .gitignore
  [PASS] LICENSE (MIT)
  [MISS] SECURITY.md
  [MISS] CONTRIBUTING.md
  [PASS] CODEOWNERS
  ...

--- GitHub Config (15%) --- Score: {n}/100
  [PASS] Description: "One-command repo health audit..."
  [FAIL] Topics: none set
  [PASS] Default branch: main
  [FAIL] Branch protection: not enabled
  ...

--- Documentation (25%) --- Score: {n}/100
  [PASS] README.md (142 lines)
  [WARN] No install/setup instructions found in README
  [MISS] CHANGELOG.md
  ...

--- Code Hygiene (20%) --- Score: {n}/100
  [PASS] No tracked .env files
  [WARN] 3 stale branches (>90 days)
  [PASS] No large binary files tracked
  ...

--- Community (10%) --- Score: {n}/100
  [MISS] CODE_OF_CONDUCT.md
  [MISS] Issue templates
  [PASS] PR template
  ...

=== Prioritized Fixes ===
1. [HIGH] Add SECURITY.md — required for public repos. See template in REFERENCE.md.
2. [HIGH] Enable branch protection on main — prevents force pushes and requires reviews.
3. [HIGH] Add repository topics — improves discoverability. Suggest: {topic1}, {topic2}, {topic3}.
4. [MED]  Add CONTRIBUTING.md — guides external contributors.
5. [MED]  Add CHANGELOG.md — tracks releases for users.
6. [LOW]  Clean up 3 stale branches.
7. [LOW]  Add CODE_OF_CONDUCT.md — signals welcoming community.
```

Priority levels:
- **HIGH**: Security, legal (LICENSE/SECURITY.md), or protection issues
- **MED**: Documentation and community gaps that affect usability
- **LOW**: Cleanup and nice-to-haves

### Step 8: Fix Mode (--fix)

If `--fix` flag was passed:

1. Present the list of MISS and FAIL items that can be auto-generated
2. Ask the user to confirm which files to create (show numbered list, accept comma-separated selection or "all")
3. For each confirmed file, generate it using sensible defaults:
   - `SECURITY.md`: Standard vulnerability reporting template
   - `CONTRIBUTING.md`: Fork/branch/PR workflow with code style notes
   - `CODE_OF_CONDUCT.md`: Contributor Covenant v2.1
   - `.editorconfig`: Sensible defaults for the detected tech stack
   - `CODEOWNERS`: Prompt user for owner patterns
   - Issue/PR templates: YAML form-based templates (see REFERENCE.md)
4. Do NOT overwrite existing files
5. Run infra/PII scrub on all generated content before writing

---

## Key Principles

- **Read-only by default.** The audit never modifies files unless `--fix` is explicitly passed.
- **Public repos are held to a higher standard.** Private repos skip community and some config checks.
- **Prioritize actionable output.** Every finding includes a specific fix recommendation.
- **No false urgency.** Recommended items are scored lower than required items. The report distinguishes between must-fix and nice-to-have.
- **Respect existing work.** Fix mode never overwrites. It only creates missing files.
- **Infra/PII awareness.** All generated files pass through the standard PII scrub before writing.

## Anti-Patterns -- Do NOT

- Modify any files during a standard audit (no `--fix` flag)
- Run install commands (`npm install`, `pip install`, etc.)
- Push changes or create commits -- the user decides when to commit
- Fabricate repository metadata -- use what `gh` and `git` report
- Rate repos you do not have local access to -- this is a local audit tool
- Skip the PII scrub when generating files in fix mode
