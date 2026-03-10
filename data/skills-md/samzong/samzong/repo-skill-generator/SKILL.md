---
name: repo-skill-generator
description: Generate repo-local coding and review skills from a repository's git history and GitHub PR review activity. Use when asked to create, refresh, or update repository-specific coding/review skills, learn from PRs, analyze commit history, extract coding patterns, or generate coding guidelines for the current repo or a specific module.
---

# Repo Skill Generator

## Overview

Generate two repo-local skills from repository history:

- A `coding` skill derived from Git commits and diffs.
- A `review` skill derived from GitHub PR review activity.

Generated artifacts are installed into:

- `./.agents/skills/` as the canonical repo-local source.
- `./.claude/skills` as a symlink pointing to `./.agents/skills`.

All generated content is in English.

## Hard Gates

- IF the target `repo-root` is not a Git repository, THEN terminate. FIX: `cd` to a valid Git repository or pass `--repo-root` pointing to one.
- IF `gh` is missing when generating review data, THEN terminate. FIX: Install GitHub CLI (refer to https://cli.github.com/).
- IF `gh` is unauthenticated, THEN terminate. ACTION: Run `gh auth status` before generating review data. If not logged in, run `gh auth login`.
- IF the install target is unwritable, THEN terminate. FIX: Check directory permissions or use `--install-root` to specify a writable path.
- Do not modify skills outside generator-managed coding/review skill names.
- Do not generate a review skill if review evidence is insufficient. The generator enforces minimum thresholds for effective reviews, unique human reviewers, and substantive review excerpts.

## Default Workflow

### 1) Pre-flight checks

1.  Execute `gh auth status`.
2.  IF `gh` is not authenticated, THEN instruct the user to run `gh auth login`.

### 2) Generate skills

Execute the command that matches the use case:

```bash
# Current repo
python3 skills/repo-skill-generator/scripts/generate_repo_skills.py

# Different repo
python3 skills/repo-skill-generator/scripts/generate_repo_skills.py \
  --repo-root /path/to/repo

# Module-level coding skill only
python3 skills/repo-skill-generator/scripts/generate_repo_skills.py \
  --repo-root /path/to/repo \
  --module src/router

# Safe install root for testing
python3 skills/repo-skill-generator/scripts/generate_repo_skills.py \
  --repo-root /path/to/repo \
  --install-root /tmp/repo-skill-generator-smoke

# Solo-repo preset (sparse review activity)
python3 skills/repo-skill-generator/scripts/generate_repo_skills.py \
  --repo-root /path/to/repo \
  --review-evidence-preset solo

# Strict preset (heavier review history expected)
python3 skills/repo-skill-generator/scripts/generate_repo_skills.py \
  --repo-root /path/to/repo \
  --review-evidence-preset strict

# Override preset thresholds (advanced)
python3 skills/repo-skill-generator/scripts/generate_repo_skills.py \
  --repo-root /path/to/repo \
  --min-effective-reviews 12 \
  --min-unique-human-reviewers 3 \
  --min-substantive-excerpts 6
```

### 3) Verify output

After generation completes, confirm all three conditions:

1.  `generator-meta.json` exists in each generated skill directory.
2.  `.repo-skill-generator-manifest.json` exists at the skill root.
3.  `.claude/skills` symlink points to `.agents/skills/`.

IF any check fails, THEN review the script's stderr for the erroring step and re-run from step 2.

## What The Script Produces

For each generated skill:

- `SKILL.md`
- `profiles/*.json`
- `profiles/*-summary.md`
- `references/evidence.md`
- `references/anti-patterns.md` or `references/blocking-patterns.md`
- `references/examples.md`
- `generator-meta.json`

At the skill root:

- `.repo-skill-generator-manifest.json`

## Notes

- The generator collects Git and GitHub review evidence before producing skills.
- Review skill generation is gated by evidence sufficiency. Repositories with weak review evidence may produce only a coding skill.
- Review sufficiency presets:
  - `default`: `8` effective reviews, `2` unique human reviewers, `5` substantive excerpts.
  - `solo`: `3` effective reviews, `1` unique human reviewer, `2` substantive excerpts.
  - `strict`: `20` effective reviews, `3` unique human reviewers, `10` substantive excerpts.
- The script writes repo-local skill directories and installs the `.claude/skills` symlink.
- The analyzer is conservative when evidence is weak and indicates this through the generated evidence layer.

## References

- Output contract: [references/output-contract.md](references/output-contract.md)
- Profile fields: [references/profile-fields.md](references/profile-fields.md)