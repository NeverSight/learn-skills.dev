---
name: repo-scaffold
description: "Initialize GitHub repositories with standard files and configuration. Generates LICENSE, CONTRIBUTING.md, SECURITY.md, issue/PR templates, CI config, and .gitignore. Detects project type and adapts templates accordingly."
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

# Repo Scaffold

Initialize GitHub repositories with standard files and configuration. This skill generates LICENSE, CONTRIBUTING.md, SECURITY.md, CODEOWNERS, .gitignore, .editorconfig, YAML-based issue templates, PR template, CI config skeleton, and optional safety files. It detects project type from existing files and adapts all templates accordingly.

## Install

```bash
claude skill install repo-scaffold
```

## When to Use

This skill should be used when:
- Setting up a new GitHub repository from scratch
- Adding missing standard files to an existing repository
- Standardizing repository configuration across projects
- Preparing a private repo for open-source release

## Usage

```
/repo-scaffold [repo-path] [--license MIT|Apache-2.0|ISC] [--public] [--ci github-actions|none]
```

| Flag | Default | Description |
|------|---------|-------------|
| `repo-path` | `.` (cwd) | Path to the git repository root |
| `--license` | `MIT` | License type (MIT, Apache-2.0, ISC, GPL-3.0, BSD-2-Clause) |
| `--public` | off | Include `.public-repo`, `.pii-allowlist`, `.commit-msg-blocklist` |
| `--ci` | `github-actions` | CI provider skeleton (`github-actions` or `none`) |

## Procedure

### Step 1: Validate Repo Path

Confirm the target path is an initialized git repository (contains `.git/`). If not, halt and inform the user. Never run `git init` without explicit permission.

### Step 2: Scan Existing Files

Inventory the repo root and `.github/` directory for any files this skill would generate. Build a conflict list. **Never overwrite existing files.** If conflicts exist, present them and ask which to skip or replace.

### Step 3: Detect Project Type

Identify the primary language and tooling by checking for marker files:

| Marker File | Project Type |
|-------------|-------------|
| `package.json` | Node.js / JavaScript / TypeScript |
| `pyproject.toml`, `setup.py`, `requirements.txt` | Python |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| Multiple markers | Multi-language |
| None of the above | Generic |

If multiple markers are found, treat as multi-language and combine relevant patterns.

### Step 4: Generate Files

Generate each file with language-appropriate content. Refer to [REFERENCE.md](REFERENCE.md) for templates, patterns, and format specifications.

#### 4a. LICENSE

Prompt the user for license choice if `--license` was not provided. Default to MIT. Insert the current year and the repo owner's name (from `git config user.name` or ask). See REFERENCE.md license comparison table for guidance.

#### 4b. .gitignore

Generate language-appropriate ignore patterns based on the detected project type. Combine patterns for multi-language repos. Always include OS-level ignores (`.DS_Store`, `Thumbs.db`) and editor ignores (`.vscode/`, `.idea/`).

#### 4c. CONTRIBUTING.md

Generate a fork-branch-PR contribution guide. Include:
- Fork and clone instructions
- Branch naming conventions (`feat/`, `fix/`, `docs/`)
- Code style notes (link to linter config if detected)
- Commit message format
- PR checklist

#### 4d. SECURITY.md

Generate a security policy with:
- Supported versions table (populate from package version if detectable)
- Vulnerability reporting instructions (email-based, not public issues)
- Response timeline expectations

#### 4e. CODEOWNERS

Scan the top-level directory structure and generate a CODEOWNERS file. Map directories to the repo owner by default. Add comments explaining how to customize.

#### 4f. .editorconfig

Generate settings appropriate to the detected project type:
- Indent style and size
- End-of-line character
- Trim trailing whitespace
- Insert final newline
- Charset (utf-8)

#### 4g. .github/ISSUE_TEMPLATE/bug-report.yml

Generate a YAML form-based bug report template with fields: description, steps to reproduce, expected behavior, actual behavior, environment, and optional screenshots. See REFERENCE.md for YAML form spec.

#### 4h. .github/ISSUE_TEMPLATE/feature-request.yml

Generate a YAML form-based feature request template with fields: problem statement, proposed solution, alternatives considered, and additional context.

#### 4i. .github/pull_request_template.md

Generate a PR template with sections: summary of changes, type of change (checkboxes), testing performed, and checklist.

#### 4j. .github/workflows/ci.yml

Generate a CI skeleton for GitHub Actions (unless `--ci none`). Include:
- Trigger on push to main and pull requests
- Language-appropriate setup step
- Lint step (ESLint, ruff, clippy, golangci-lint)
- Test step (language-appropriate test runner)
- Placeholder comments for additional steps

#### 4k. Optional: Safety Files (when --public)

When `--public` is passed, also generate:
- `.public-repo` — Empty marker file indicating the repo is public
- `.pii-allowlist` — One regex per line; starts with a comment header explaining usage
- `.commit-msg-blocklist` — One term per line; starts with a comment header and common defaults

### Step 5: Present Plan

Before writing any files, present the full list of files to be created with a one-line description of each. Show which files were skipped due to conflicts. Ask the user to confirm before proceeding.

### Step 6: Write Files

Write all confirmed files. Report each file as it is written.

### Step 7: Summary

Print a summary table:
- Files created (with paths)
- Files skipped (with reason)
- Suggested next steps (e.g., review CODEOWNERS, customize CONTRIBUTING.md, add secrets to CI)

## Key Principles

1. **Never overwrite existing files.** Always scan first, flag conflicts, and ask.
2. **Always ask before writing.** Present the plan and get explicit confirmation.
3. **Language-appropriate defaults.** Detect the project type and tailor every template.
4. **Minimal but complete.** Generate the standard set every well-maintained repo needs, nothing more.
5. **Composable.** Each file stands alone. Re-run the skill later to add missing files without disrupting existing ones.

## References

- [REFERENCE.md](REFERENCE.md) — License comparison, .gitignore patterns, YAML template spec, CI skeletons, CODEOWNERS syntax, .editorconfig settings, SECURITY.md and CONTRIBUTING.md templates
- [EXAMPLES.md](EXAMPLES.md) — Worked examples for Node.js, Python, and public repo scaffolding
