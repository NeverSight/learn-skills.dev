---
license: MIT
name: repo-audit
description: >
  Run a read-only audit of every catalog skill's checks against a
  repository and report which setup gaps exist. Runs a bundled Python
  script from the repository root, prints one row per catalog skill
  (check, status, evidence, the skill that fixes it), then proposes an
  ordered plan naming those skills. Never writes a file and never calls a
  mutating GitHub API endpoint, even with the optional --github flag,
  which adds read-only GET checks. Use when the user says "audit this
  repo", "what's missing in this repository", "repo health check",
  "which setup skills apply", or invokes /repo-audit. Do NOT use for
  applying any fix directly — route each finding to its catalog skill —
  or for code review of application logic.
---

# repo-audit

A read-only survey of a repository against every other catalog skill's setup checks. It answers one question: which catalog skills apply here, and in what order?

## What this skill is NOT for

- Applying a fix — a finding routes to the skill that owns it (`oss-hygiene`, `gh-bootstrap`, and so on); this skill never edits a file or calls a mutating API.
- Code review of application logic, tests, or business behavior — out of scope.
- Replacing a catalog skill's own protocol — the audit is a triage pass, not a substitute for reading that skill's `SKILL.md`.

## Protocol

### 1. Run the bundled script from the repository root

```bash
python3 skills/repo-audit/scripts/repo_audit.py
```

Add `--github` to also run read-only `gh api` GET calls (merge settings, rulesets, `delete_branch_on_merge`, the CODEOWNERS errors endpoint). `--github` is opt-in; the default run only reads the working tree and local git metadata (`git tag --list`, `git remote get-url origin`).

Use `--json` for machine consumption or `--markdown` to paste the table into a PR comment. The script always exits `0` unless it errors itself — a `missing` or `warn` row is not a script failure.

### 2. The script checks, read-only, one row per catalog skill

| Check | What it inspects | Route to |
| --- | --- | --- |
| prek | `prek.toml` or `.pre-commit-config.yaml` | `prek` |
| oss-hygiene | `LICENSE`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `.github/ISSUE_TEMPLATE`, `PULL_REQUEST_TEMPLATE`, `.github/dependabot.yml`, plus scorecard/codeql/dependency-review workflow presence | `oss-hygiene` |
| gh-bootstrap | `.github/release.yml`; with `--github` also merge settings and non-empty rulesets | `gh-bootstrap` |
| safe-settings | `.github/settings.yml` (informational) | `safe-settings` |
| config-review-bot | `.coderabbit.yaml` | `config-review-bot` |
| release | `git tag --list` and `CHANGELOG.md` | `release` |
| justfile | `justfile` | `justfile` |
| ci-optimize | workflows present with `concurrency:` (informational) | `ci-optimize` |
| build-optimize | skipped — needs measured wall-time data | `build-optimize` |
| github-copilot-repo-instructions | `.github/copilot-instructions.md` or `.github/instructions/*.instructions.md` | `github-copilot-repo-instructions` |
| codeowners | `CODEOWNERS` in root, `docs/`, or `.github/`; with `--github` also the codeowners/errors endpoint | `codeowners` |
| actions-pinning | count of `uses:` refs not pinned to a 40-hex commit SHA | `actions-pinning` |
| pr-title-lint | a workflow containing `action-semantic-pull-request` or `commitlint` | `pr-title-lint` |
| labels-as-code | `.github/labels.yml` or `.github/labeler.yml` | `labels-as-code` |
| repo-attributes | `.gitattributes`, `.editorconfig`, `.gitignore` | `repo-attributes` |
| branch-cleanup | with `--github`, `delete_branch_on_merge` | `branch-cleanup` |
| agents-md | `AGENTS.md` exists, under 32 KiB, under about 200 lines | `agents-md` |

Each row's status is `pass`, `warn`, `missing`, or `skipped`. `skipped` means the check needs data this script cannot gather statically (`build-optimize`) or needs `--github` and it was not passed (`branch-cleanup`), not that the repository failed the check.

### 3. Read the table and propose an ordered plan

After the script prints its table, read the `missing` and `warn` rows and propose an ordered plan that names the catalog skill for each gap. Order gaps by dependency where one exists (for example, `gh-bootstrap` locks the merge surface before `oss-hygiene` adds contributor-facing files; `actions-pinning` matters more once workflows exist). Do not apply any fix yourself — hand each gap to its named skill.

### 4. No writes, no mutating calls

This skill and its script never create, edit, or delete a file, and never call a `POST`, `PATCH`, `PUT`, or `DELETE` GitHub API endpoint. `--github` only adds `GET` calls. If a user asks the audit to "just fix it", decline and restate the routing plan from step 3 instead.

## References

- `references/checks.md` — one row per check, the file or endpoint it inspects, and a docs.github.com citation where an API is used.
