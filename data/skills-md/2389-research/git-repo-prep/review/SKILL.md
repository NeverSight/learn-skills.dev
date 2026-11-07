---
name: review
description: Audits a codebase for openness across secrets, license, documentation, gitignore, CI/CD, and metadata, with severity-classified findings. Use when checking a repo for secrets, missing docs, or gaps before making it public — or at any point after preparation to validate state.
---

# Review Repo for Openness

Announce: "I'm using git-repo-prep:review to audit this repo for openness."

## Setup

Create a TodoWrite checklist for all audit categories:

1. Secrets scan
2. Personal info scan
3. License check
4. Documentation check
5. Gitignore check
6. CI/CD check
7. Metadata check
8. Present findings and summary

Mark each task in_progress before starting, completed immediately after.

## Scope

This is an **openness audit**, not a code quality review. Stay focused on what matters for making the repo public. Do NOT comment on error handling, architecture, performance, code style, test coverage quality, or design patterns.

## Ecosystem Detection

Detect the ecosystem to tailor checks:

| File | Ecosystem |
|------|-----------|
| `package.json` | Node.js |
| `pyproject.toml` / `setup.py` / `setup.cfg` | Python |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `*.csproj` / `*.sln` | .NET |
| `Gemfile` | Ruby |
| `pom.xml` / `build.gradle` | Java/Kotlin |

## Audit Categories

Scan every category below. Classify each finding as **Critical**, **Recommended**, or **Nice-to-have** using the severity definitions in this table exactly. Do not invent your own categories, and do not upgrade or downgrade severity — use the column where the issue appears.

| Category | Critical | Recommended | Nice-to-have |
|----------|----------|-------------|--------------|
| Secrets | API keys, passwords, tokens, .env committed | .env in gitignore | git history scan |
| Personal info | Real names/emails in source code | Author field review | Username cleanup |
| License | No LICENSE file | Mismatch between LICENSE file and package metadata; no license section in README | License headers in source files |
| Documentation | No README or empty README | Missing install/usage sections | CONTRIBUTING.md, SECURITY.md, CLAUDE.md |
| Gitignore | Sensitive files tracked/committed | Missing common patterns for ecosystem | IDE/OS files |
| CI/CD | — | No CI pipeline; no tests at all (CI cannot function) | No dependabot, no hooks, no coverage |
| Metadata | — | No repo URL in package metadata | Missing engine/version, keywords, description |

## Scanning Process

Work through each category in order.

### 1. Secrets

- Grep source files for patterns: `sk_live`, `sk_test`, `ghp_`, `AKIA`, `password\s*=`, `secret\s*=`, `token\s*=`, `api_key`, `-----BEGIN.*PRIVATE KEY`, connection strings with embedded credentials.
- Check for `.env` files in the repo (any level).
- Check `.gitignore` for `.env` and `.env.*` exclusion patterns.
- Look for `.pem`, `.key`, or credential files.

### 2. Personal Info

- Check author fields in package metadata (`package.json` author, `pyproject.toml` authors, `Cargo.toml` authors).
- Grep for email patterns (`\b\S+@\S+\.\S+\b`) in source files (not node_modules, not vendor, not lock files).
- Look for hardcoded usernames in config or source (`DEFAULT_USER`, `AUTHOR`, usernames in URLs or paths).

### 3. License

This is the most commonly missed area. Check all three locations and compare:

1. **LICENSE file** — Does it exist? What license does it contain?
2. **Package metadata** — What does the `license` field say in package.json / pyproject.toml / Cargo.toml?
3. **README** — Is there a license section? Does it name the same license?

Flag any mismatch between these three. Flag if any location is missing.

### 4. Documentation

- **README**: Does it exist? Is it non-empty? Does it have: project description, installation/getting started, usage, license section?
- **CONTRIBUTING.md**: Present or missing?
- **SECURITY.md**: Present or missing?

### 5. Gitignore

- Does `.gitignore` exist?
- Compare against ecosystem best practices:
  - Node.js: `node_modules/`, `.env`, `dist/`, `coverage/`
  - Python: `__pycache__/`, `*.pyc`, `.env`, `*.egg-info/`, `dist/`, `.venv/`
  - Rust: `target/`, `.env`
  - Go: `vendor/` (if not vendoring), `.env`
  - General: `.env`, `.env.*`, `*.log`, `.DS_Store`, `*.pem`, `*.key`
- Check if any sensitive files are already tracked by git (`git ls-files` for `.env`, credentials, keys).

### 6. CI/CD

- Look for `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`, etc.
- Check for Dependabot config (`.github/dependabot.yml`) or Renovate (`renovate.json`).

### 7. Metadata

Check ecosystem-specific metadata completeness:

- **Node.js**: `repository`, `engines`, `keywords`, `description` in `package.json`
- **Python**: `[project.urls]`, `classifiers`, `requires-python`, `keywords`, `description` in `pyproject.toml`
- **Rust**: `repository`, `keywords`, `categories`, `description` in `Cargo.toml`
- **Go**: module path matches repo URL, package doc comment

## Presenting Findings

Present findings conversationally — do NOT write a report file.

Group by severity, starting with the most urgent:

1. **Critical** — issues that must be fixed before going public
2. **Recommended** — issues that should be addressed for a quality release
3. **Nice-to-have** — improvements for polish

For each finding:
- Describe the issue concisely.
- Explain why it matters for openness (one sentence).
- Offer to fix it right now.

## Summary

End with a tally: "**X critical, Y recommended, Z nice-to-have** findings."

If critical findings exist, recommend addressing them before release. If none, say the repo looks ready and suggest tackling recommended items for polish.
