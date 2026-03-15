---
name: pravidhi-commit-protocol
description: A complete, opinionated development workflow skill for agents. Triggers when the user asks to implement a feature, fix a bug, or refactor code in a Git repo. Enforces hygiene, security, quality, and atomic commits.
license: MIT
metadata:
  version: "1.0.0"
  tags: "git, workflow, quality, ci-cd, security, testing, linting, formatting"
---

# Pravidhi Commit Protocol Skill

> **Developed and maintained by [Pravidhi](https://pravidhi.net)**

## Overview

This skill drives a complete, repeatable, and quality-enforced coding workflow inside any Git repository. Every major stage can pause and ask the user for input. The goal is clean atomic commits, zero leaked secrets, minimal diff noise, and a passing CI pipeline before a single line is pushed.

**Formatting threshold (hardcoded default):** If more than **10 files** would be reformatted, stop and ask the user before applying formatting. Adjust per project if the user instructs you to.

---

## Quick Reference

| Stage | Key Actions |
|---|---|
| 1. Repo Hygiene | branch check, fetch, pull, porcelain status, .gitignore triage |
| 2. Dependency & Security | audit (npm/pip/cargo/etc.), known-vuln scan |
| 3. Pre-coding Quality | formatter dry-run, linter check-only |
| 4. CI/CD Pre-validation | detect & mirror local CI checks |
| 5. Refactor Safety Net | revert command, risks, rollback verification |
| 6. Implementation | scoped, convention-respecting code changes |
| 7. Post-coding Validation | format, lint, type-check, tests, coverage, build, hooks |
| 8. Secret Detection | scan staged files before commit |
| 9. CHANGELOG | detect & prompt update |
| 10. Commit & Push | atomic, high-quality commit message |
| 11. Pull Request | generate PR/MR via CLI or link |

---

## Stage 1 — Repository Hygiene

### 1.1 Branch Safety Check

```bash
git branch --show-current

```

**Rules:**

* If branch is `main`, `master`, `dev`, or `production`: **STOP.** Ask user: "You are on a protected branch. Should I create a new feature branch named `feature/<task-slug>`?"
* If branch is a feature branch: Proceed.

### 1.2 Sync with Remote

```bash
git fetch --all --prune
git pull --ff-only

```

If `--ff-only` fails, stop and ask the user whether to rebase or merge.

### 1.3 Check for Uncommitted Changes

```bash
git status --porcelain

```

* **Empty output** → repository is clean, continue.
* **Non-empty output** → inspect each entry:

| Prefix | Meaning | Action |
| --- | --- | --- |
| `M` | Modified tracked file | Ask: stash, commit, or abort? |
| `A` | Staged new file | Ask: keep staged or unstage? |
| `??` | Untracked file | Evaluate for .gitignore (see 1.4) |
| `D` | Deleted file | Ask: intentional or restore? |

Present a clean summary to the user and ask how to proceed before continuing.

### 1.4 .gitignore Triage

Scan untracked paths (`??` entries) and immediately add **known suspects** to `.gitignore` without asking:

```text
# Build artifacts
dist/         build/        out/           target/       .next/
__pycache__/ *.pyc         *.pyo          *.class       *.o

# Logs & temp
*.log         *.tmp         .DS_Store      Thumbs.db

# Generated files
coverage/     .nyc_output/ *.lcov        htmlcov/

# Secrets & environment (NEVER commit these)
.env          .env.* *.pem         *.key         *.p12
secrets/      credentials/ .aws/         .gcloud/

# IDE / editor
.idea/        .vscode/      *.swp         *.swo

```

For **ambiguous** untracked paths (not obviously an artifact), ask the user before adding.

Stage and commit `.gitignore` changes as a standalone commit:

```text
chore: update .gitignore — exclude build artifacts and env files

```

---

## Stage 2 — Dependency & Security Audit

Run the appropriate audit for the detected ecosystem(s). Multiple ecosystems may be present in a monorepo.

### Detection

```bash
# Detect ecosystems
ls package.json package-lock.json yarn.lock pnpm-lock.yaml   # Node
ls requirements.txt Pipfile pyproject.toml setup.py            # Python
ls Cargo.toml                                                  # Rust
ls go.sum                                                      # Go
ls Gemfile.lock                                                # Ruby
ls composer.lock                                               # PHP

```

### Audit Commands by Ecosystem

```bash
# Node
npm audit --audit-level=moderate          # or: yarn audit / pnpm audit
npx audit-ci --moderate                   # CI-friendly exit code

# Python
pip-audit                                  # pip install pip-audit
safety check --full-report                 # pip install safety

# Rust
cargo audit                                # cargo install cargo-audit

# Go
govulncheck ./...                          # go install golang.org/x/vuln/cmd/govulncheck

# Ruby
bundle audit check --update                # gem install bundler-audit

# PHP
composer audit

```

### Decision Logic

| Severity Found | Action |
| --- | --- |
| **Critical** | Stop immediately. Do not proceed. Show findings. Ask: patch deps now or abort? |
| **High** | Stop. Ask: patch now (separate commit) or accept risk and continue? |
| **Moderate** | Warn. Ask: patch now or track in a follow-up ticket? |
| **Low / Info** | Note in output, continue automatically. |

If the user chooses to patch:

1. Apply fixes (`npm audit fix`, `pip install --upgrade <pkg>`, etc.)
2. Run audit again to confirm clean
3. Commit as a standalone commit:
```text
chore(deps): fix [critical|high] security vulnerabilities — <brief description>

```



---

## Stage 3 — Pre-coding Quality Checks

### 3.1 Check Memory for User Preferences

Before running any tools, check if there is a stored preference from previous sessions:

* `skip_pre_coding_format: true` → skip formatter dry-run
* `skip_pre_coding_lint: true` → skip linter check-only pass
* `format_commit_threshold: <N>` → override the default threshold of 10

If no memory exists, proceed with defaults and store the user's decisions at the end of this stage (see Stage 6).

### 3.2 Formatter Dry-Run

Detect the formatter from config files:

```bash
# Prettier (JS/TS/CSS/HTML/JSON/YAML)
npx prettier --list-different "**/*.{js,ts,jsx,tsx,css,json,yaml,md}"

# Black (Python)
black --check --diff .

# Rustfmt
cargo fmt -- --check

# gofmt
gofmt -l ./...

# PHP CS Fixer
php-cs-fixer fix --dry-run --diff

# rubocop (Ruby)
rubocop --auto-correct-all --dry-run

```

Count the number of files that would be reformatted.

**If count > threshold (default: 10):**

> 🛑 **Formatting check found N files that would be reformatted.**
> Creating a dedicated formatting commit before implementing your task has these benefits:
> * **Clean diffs** — reviewers see only your feature changes, not whitespace noise
> * **Clearer Git history** — formatting is a separate, revertable concern
> * **Easier code review** — no mixing of stylistic and semantic changes
> * **Reduced merge conflicts** — formatting is settled before feature branching
> 
> 
> **Would you like to:**
> 1. Apply formatting now in a dedicated commit, then proceed with your task
> 2. Skip formatting for now and proceed directly with the task
> 3. Apply formatting only to files touched by the task (post-coding)
> 
> 

Store the user's choice for future sessions.

### 3.3 Linter Check-Only

Detect and run:

```bash
# ESLint
npx eslint . --format=compact 2>&1 | tail -1    # count violations

# Pylint / Flake8 / Ruff
ruff check . --statistics
flake8 . --statistics --count

# Clippy (Rust)
cargo clippy -- -D warnings 2>&1 | grep -c "^error"

# golint / staticcheck (Go)
staticcheck ./...

# rubocop (Ruby)
rubocop --format progress | tail -3

```

Classify output:

| Violation Count | Classification | Action |
| --- | --- | --- |
| 0–5 | Minor | Continue, note in output |
| 6–20 | Moderate | Stop, ask user (fix in dedicated commit or continue?) |
| 21+ | Extensive | Stop, strongly recommend dedicated lint fix commit |

If user chooses to fix lint:

1. Run auto-fix where safe: `npx eslint . --fix`, `ruff check . --fix`, `cargo clippy --fix`
2. Manually address remaining issues
3. Commit:
```text
chore(lint): resolve linting violations before feature work

```



---

## Stage 4 — CI/CD Pre-validation

### 4.1 Detect CI Configuration

```bash
ls .github/workflows/     # GitHub Actions
ls .gitlab-ci.yml         # GitLab CI
ls Jenkinsfile            # Jenkins
ls .circleci/config.yml   # CircleCI
ls .travis.yml            # Travis CI
ls azure-pipelines.yml    # Azure DevOps
ls bitbucket-pipelines.yml
ls .drone.yml

```

### 4.2 Extract and Mirror CI Steps Locally

Parse the CI config and identify steps that can be run locally. Common patterns to extract:

```bash
# From GitHub Actions: find "run:" steps
grep -A1 "run:" .github/workflows/*.yml

# Run them in the same order as CI

```

**Example mapping (GitHub Actions → local equivalents):**

```yaml
# CI step:            # Local equivalent:
npm ci               →   npm ci
npm run build        →   npm run build
npm test             →   npm test
npm run lint         →   npx eslint .
npm run type-check   →   npx tsc --noEmit

```

For each detected CI step, run it locally and capture exit codes. If any step fails:

> ⚠️ **CI pre-validation failure: `<step name>**`
> The following CI step failed locally: `<command>`
> Exit code: `<N>`
> Output: `<last 20 lines>`
> This will likely cause CI to fail after push.
> **Would you like to:**
> 1. Fix the issue now before implementing the task
> 2. Note it and proceed (I'll flag this again at post-coding validation)
> 3. Abort
> 
> 

### 4.3 Pre-commit / Pre-push Hook Detection

```bash
ls .git/hooks/pre-commit .git/hooks/pre-push
ls .husky/pre-commit .husky/pre-push            # Husky
ls .lefthook.yml lefthook.yml                   # Lefthook
ls .pre-commit-config.yaml                      # pre-commit framework

```

**If hooks exist, run them now as a pre-flight check:**

```bash
# Native hooks
bash .git/hooks/pre-commit
bash .git/hooks/pre-push

# Husky
npx husky run pre-commit

# pre-commit framework
pre-commit run --all-files

# Lefthook
lefthook run pre-commit

```

If hooks fail, stop and report. Hooks represent the project's own quality gate — do not bypass them.

---

## Stage 5 — Refactor Safety Net (Major Refactors Only)

**Trigger this stage if the task involves:**

* Renaming or moving multiple files/modules
* Changing a public API or interface
* Modifying database schemas or migrations
* Restructuring directory layout
* Changing build configuration or dependency graph

### 5.1 Document Before Touching Code

Before writing a single line, output and store:

```markdown
## Refactor Safety Net

**Task:** <description of refactor>
**Date:** <ISO timestamp>

### Revert Command
```bash
git stash         # if not yet committed
# OR
git revert <SHA>  # if committed
# OR
git reset --hard <SHA-before-changes>

```

### Known Risks

* <Risk 1: e.g., "API consumers outside this repo may break">
* <Risk 2: e.g., "Database migration is irreversible without a down migration">
* <Risk 3: e.g., "Cache keys will be invalidated — plan for cold cache on deploy">

### Rollback Verification Steps

1. Run: `<command to verify system is working post-rollback>`
2. Check: `<what to look for in logs or UI>`
3. Confirm: `<specific assertion that proves rollback succeeded>`

```

Present this to the user and ask for confirmation before proceeding.

### 5.2 Create a Pre-refactor Tag

```bash
git tag pre-refactor/<task-slug>-$(date +%Y%m%d)
git push origin pre-refactor/<task-slug>-$(date +%Y%m%d)

```

This gives a named rollback point that survives branch resets.

---

## Stage 6 — Implementation

### 6.1 Store User Preferences from Prior Stages

At this point, persist the following to memory for future workflow runs:

```text
skip_pre_coding_format: <true|false>
skip_pre_coding_lint: <true|false>
format_commit_threshold: <N>
audit_severity_threshold: <critical|high|moderate>

```

### 6.2 Define Scope

Before writing code, state clearly:

```text
Task:   <one-line description of what is being implemented>
Files:  <exhaustive list of files to modify>
Scope:  <what is explicitly OUT of scope for this change>

```

### 6.3 Implementation Rules

* Follow existing project architecture, patterns, and naming conventions
* Do not introduce formatting changes in files unrelated to the task
* Do not refactor code outside the defined scope
* Do not modify test fixtures, mocks, or test utilities unless the task requires it
* Preserve existing error handling patterns
* Keep new public APIs consistent with existing ones
* **Do not stage any changes yet** — post-coding validation comes first

---

## Stage 7 — Post-coding Validation

Run every applicable tool against **only the files that were changed**. Fix issues that are safe and mechanical (e.g., trailing whitespace, import ordering). For anything requiring judgment, stop and ask the user.

> **Context Guard:** When running linters, tests, or builds, **DO NOT** output the full log if it exceeds 50 lines. Use `| tail -n 50` or pipe to a temporary file and `grep` for "Error" or "Fail" to avoid crashing the agent context window.

### 7.1 Formatter (Write Mode)

```bash
# Only on changed files
git diff --name-only | xargs npx prettier --write
git diff --name-only | xargs black

```

### 7.2 Linter

```bash
git diff --name-only | xargs npx eslint --fix
git diff --name-only | xargs ruff check --fix

```

If unfixable violations remain after auto-fix, stop and report each one with file, line, and rule name. Ask: fix manually, suppress with justification, or abort?

### 7.3 Type Checker

```bash
npx tsc --noEmit                    # TypeScript
mypy <changed_files>                # Python
cargo check                         # Rust
go vet ./...                        # Go

```

Type errors are **blocking** — do not proceed past this step with type errors.

### 7.4 Tests & Coverage

#### Detect Testing Framework

```bash
# Node
ls jest.config.* vitest.config.* .mocharc.*
grep -E '"test":|"jest":|"vitest"' package.json

# Python
ls pytest.ini setup.cfg pyproject.toml | xargs grep -l '\[tool.pytest'
ls tests/ test_*.py *_test.py

# Rust
grep '\[dev-dependencies\]' Cargo.toml

# Go — built-in
ls *_test.go

# Ruby
ls spec/  test/

```

#### Run Tests

```bash
# Run full suite first (with context guard)
npm test 2>&1 | tail -n 50
pytest | tail -n 50
cargo test
go test ./...
bundle exec rspec

# If full suite passes, run coverage for changed files
npx jest --coverage --collectCoverageFrom='<changed_files>'
pytest --cov=<module> --cov-report=term-missing <changed_files>

```

#### Coverage Rules

| Scenario | Requirement |
| --- | --- |
| Project has established test suite (>0 tests exist) | Achieve complete coverage of changed files. If files are small (<200 LOC), target 100%. |
| Project has no tests | Write basic tests for every public function/method changed. Cover happy path + at least one error case per function. |
| Changed files are small (<100 LOC) | Target 100% coverage of those specific files. |

If coverage drops below the project's configured threshold (e.g., `coverageThreshold` in jest.config), stop and ask whether to write additional tests or document the coverage gap.

#### Test Failure Protocol

* First failure: Attempt to fix
* Second consecutive failure on same test: Stop, show full output, ask user how to proceed

### 7.5 Build

```bash
npm run build
cargo build --release
go build ./...
python -m build
mvn package -q

```

Build failures are **blocking**.

### 7.6 Pre-commit and Pre-push Hooks (Final Run)

Run all detected hooks one final time against the actual changed files:

```bash
pre-commit run --files $(git diff --name-only)
bash .git/hooks/pre-commit

```

If hooks fail here, the commit will fail anyway — fix issues before staging.

---

## Stage 8 — Secret Detection

**Always run before staging.** Never skip.

```bash
# gitleaks (recommended — install: brew install gitleaks / apt install gitleaks)
gitleaks detect --source . --no-git

# truffleHog
trufflehog filesystem .

# detect-secrets (Python)
detect-secrets scan --baseline .secrets.baseline

# git-secrets (AWS focused)
git secrets --scan

# Fallback: manual pattern grep if no tool is available
grep -rE \
  '(AKIA[0-9A-Z]{16}|sk-[a-zA-Z0-9]{32,}|ghp_[a-zA-Z0-9]{36}|-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY|password\s*=\s*["\x27][^"\x27]{4,}["\x27])' \
  $(git diff --name-only)

```

### Secret Found Protocol

> 🚨 **Potential secret detected in `<filename>` at line `<N>**`
> Pattern matched: `<redacted — show only type, not value>`
> **DO NOT COMMIT.** Options:
> 1. Replace with environment variable reference and add to `.env.example`
> 2. Move to a secrets manager (Vault, AWS Secrets Manager, etc.)
> 3. Mark as false positive and add to `.secrets.baseline`
> 
> 

Do not proceed to staging until all findings are resolved.

---

## Stage 9 — CHANGELOG Check

### 9.1 Detect CHANGELOG

```bash
ls CHANGELOG.md CHANGELOG.rst CHANGELOG.txt CHANGES.md HISTORY.md RELEASES.md 2>/dev/null

```

### 9.2 Evaluation Rules

| Condition | Action |
| --- | --- |
| CHANGELOG not found | Skip (note absence) |
| CHANGELOG found + task is a new feature | Stop, ask user to confirm CHANGELOG entry |
| CHANGELOG found + task is a bug fix | Stop, ask user to confirm CHANGELOG entry |
| CHANGELOG found + task is chore/refactor only | Ask but default to "skip" |

### 9.3 CHANGELOG Entry Format

Use the project's existing format. If none exists, default to **Keep a Changelog**:

```markdown
## [Unreleased]

### Added
- <feature description> — <brief rationale>

### Fixed
- <bug description> — fixes #<issue> if applicable

### Changed
- <what changed and why>

```

If user confirms an entry is needed, add it and stage `CHANGELOG.md` alongside the feature files in the same commit (not a separate commit — changelog belongs with the change).

---

## Stage 10 — Version Control & Commit

### 10.1 Inspect Final Diff

```bash
git status
git diff --stat

```

Classify every modified file:

| Category | Disposition |
| --- | --- |
| Intentional (task-related) | Stage |
| Tool-generated (formatter/linter on task files) | Stage |
| CHANGELOG.md (if updated) | Stage |
| Tool-generated on unrelated files | Do NOT stage — ask user |
| Accidentally modified | Do NOT stage — restore with `git checkout -- <file>` |
| New files not related to task | Do NOT stage — ask user |

### 10.2 Final Secret Scan on Staged Files Only

```bash
git stash       # stash unstaged
git diff --cached | gitleaks detect --no-git --pipe
git stash pop   # restore unstaged

```

### 10.3 Stage Files

```bash
git add <file1> <file2> ...    # Always stage explicitly, never `git add .`
git diff --cached --stat       # Confirm staged set looks correct

```

### 10.4 Commit Message

Follow Conventional Commits format. Craft a commit that answers:

* **What** changed (summary line, imperative mood, ≤72 chars)
* **Why** it was changed (body)
* **What problem** it solves (body)
* **Architectural/behavioral impact** if any (body or footer)
* **References** — issue/PR numbers, related commits

```text
<type>(<scope>): <short imperative summary>

<Paragraph explaining WHY the change was made and WHAT problem it solves.
Wrap at 72 characters. Use present tense. Be specific — avoid "fix bug".>

<Optional paragraph for architectural impact, migration steps, or
behavioral changes users/consumers should be aware of.>

Refs: #<issue>, #<pr>
Breaking-Change: <description if applicable>

```

**Type vocabulary:**

| Type | Use for |
| --- | --- |
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring without behavior change |
| `test` | Adding or fixing tests |
| `chore` | Build, deps, tooling, CI |
| `docs` | Documentation only |
| `perf` | Performance improvement |
| `style` | Formatting only (no logic change) |
| `revert` | Reverting a prior commit |

### 10.5 Push

```bash
git push origin <branch>

```

If the push is rejected (non-fast-forward), stop and ask the user before force-pushing. Never force-push to `main`, `master`, or `production` branches.

---

## Stage 11 — Pull Request (Optional)

If `gh` (GitHub) or `glab` (GitLab) CLI tools are installed and authenticated:

### GitHub

```bash
gh pr create \
  --title "<commit summary>" \
  --body "<commit body>" \
  --base main \
  --head <current-branch> \
  --draft  # Ask user: Draft or Ready?

```

### GitLab

```bash
glab mr create \
  --title "<commit summary>" \
  --description "<commit body>" \
  --source-branch <current-branch>

```

If no CLI tool is found, generate the **HTTPS link** for the user to click to create the PR manually (e.g., `https://github.com/org/repo/compare/main...feature-branch`).

---

## Error Recovery Playbook

| Symptom | Recovery |
| --- | --- |
| `git pull --ff-only` fails | `git fetch && git rebase origin/<branch>` — ask user if conflicts |
| Formatter changes too many files | Create dedicated format commit first |
| Lint violations > 20 | Create dedicated lint commit first |
| Audit finds critical CVE | Patch deps, re-audit, commit before feature work |
| CI step fails locally | Fix before implementation or document as known issue |
| Test fails after repeated fix attempts | Stop, show full trace, ask user |
| Secret detected in staged files | Unstage, rotate credential, fix, re-scan |
| Build fails | Stop — do not push broken builds |
| Hook fails | Fix — hooks represent the project's own enforcement |
| Push rejected | Fetch, rebase, resolve conflicts — never force-push protected branches |

---

## Commit Sequence Summary

A full workflow may produce multiple commits in this order:

```text
1. chore: update .gitignore                      (if needed)
2. chore(deps): fix security vulnerabilities     (if audit findings patched)
3. style: apply formatter to codebase            (if user approved pre-coding format)
4. chore(lint): resolve linting violations       (if user approved pre-coding lint)
5. feat/fix/refactor(<scope>): <main task>       (the actual work + changelog + tests)

```

