---
name: dep-audit
description: "Cross-repository dependency audit. Scans package manifests for outdated packages, security advisories, version conflicts, and license issues. Produces a prioritized update plan. Supports Node.js, Python, Rust, and Go projects."
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: devops
  domain: dependencies
  updated: 2026-03-19
  tested: 2026-03-19
  tested_with: "Claude Code v2.1"
---

# Dependency Audit

Cross-repository dependency audit. Scans package manifests (package.json, pyproject.toml, Cargo.toml, go.mod) for outdated packages, security advisories, version conflicts between repos, and license compatibility issues. Produces a prioritized update plan.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/dep-audit ~/.claude/skills/
```

## When to Use

- **Monthly hygiene**: Run on a cadence to catch dependency drift before it compounds
- **Before releases**: Verify no known vulnerabilities ship to production
- **Security incidents**: When a CVE drops, quickly assess exposure across all repos
- **Onboarding new repos**: Baseline the dependency health of a repo you're inheriting or adopting

## Usage

- `/dep-audit [repo-path]` — audit a single repository
- `/dep-audit [repo-path1] [repo-path2] ...` — cross-repo audit (enables version conflict detection)

## Procedure

### 1. Detect Package Managers

Scan the target repo(s) for manifest files:

| Manager | Manifest | Lock File |
|---------|----------|-----------|
| npm | `package.json` | `package-lock.json` |
| yarn | `package.json` | `yarn.lock` |
| pnpm | `package.json` | `pnpm-lock.yaml` |
| pip | `requirements.txt`, `setup.py`, `setup.cfg` | `requirements.txt` (pinned) |
| poetry | `pyproject.toml` (has `[tool.poetry]`) | `poetry.lock` |
| uv | `pyproject.toml` (has `[tool.uv]`) | `uv.lock` |
| cargo | `Cargo.toml` | `Cargo.lock` |
| go mod | `go.mod` | `go.sum` |

```bash
# Detect which manifests exist
ls package.json pyproject.toml Cargo.toml go.mod requirements.txt 2>/dev/null
# Detect lock files
ls package-lock.json yarn.lock pnpm-lock.yaml poetry.lock uv.lock Cargo.lock go.sum 2>/dev/null
```

If multiple ecosystems are present (e.g., a monorepo with Node.js frontend and Go backend), audit each independently and merge results.

### 2. Parse Manifests and Lock Files

Read the manifest to identify declared dependencies (direct) and the lock file for resolved versions (transitive). Distinguish between:
- **Production dependencies** (`dependencies`, `[dependencies]`, main requires)
- **Development dependencies** (`devDependencies`, `[dev-dependencies]`, extras)

### 3. Check for Outdated Packages

Query the registry for latest versions and categorize the delta:

```bash
# Node.js
npm outdated --json

# Python (pip)
pip list --outdated --format=json

# Python (poetry)
poetry show --outdated

# Rust
cargo outdated --format json  # requires cargo-outdated

# Go
go list -m -u all
```

Categorize each outdated package:
- **Patch update** (e.g., 2.3.1 -> 2.3.4): Safe, usually bug fixes
- **Minor update** (e.g., 2.3.1 -> 2.5.0): New features, should be backward-compatible
- **Major update** (e.g., 2.3.1 -> 3.0.0): Breaking changes likely, needs migration review

### 4. Check for Security Advisories

Run ecosystem-native audit tools:

```bash
# Node.js
npm audit --json

# Python
pip-audit --format=json  # or: safety check

# Rust
cargo audit --json  # requires cargo-audit

# Go
govulncheck ./...
```

Parse severity from results:
- **Critical**: Remote code execution, authentication bypass, data exfiltration
- **High**: Privilege escalation, significant data exposure
- **Medium**: DoS potential, limited data exposure
- **Low**: Information disclosure, minor issues

### 5. Cross-Repo Analysis (Multiple Repos)

When auditing two or more repos, compare dependency versions:

- **Version conflicts**: Same package at different versions across repos (e.g., `axios@0.27.2` in repo A, `axios@1.6.2` in repo B)
- **Shared dependencies**: Packages used by multiple repos that could be aligned to a single version
- **Divergent major versions**: Flag these as highest priority — they indicate repos drifting apart

Present a conflict table showing package, version per repo, and recommended target version.

### 6. License Scan

Check dependency licenses against compatibility rules:

```bash
# Node.js
npx license-checker --json

# Python
pip-licenses --format=json

# Rust
cargo license --json  # requires cargo-license

# Go
go-licenses report ./...  # requires go-licenses
```

Flag issues:
- **Copyleft in permissive projects**: GPL/AGPL dependencies in MIT/Apache-licensed projects
- **Unknown or missing licenses**: Dependencies with no license metadata
- **Non-OSI-approved licenses**: Custom or restrictive licenses
- **License conflicts**: Incompatible license combinations (e.g., GPLv2-only with Apache-2.0)

### 7. Generate Update Plan

Prioritize all findings into a single ordered list:

1. **Critical security advisories** — fix immediately
2. **High security advisories** — fix this sprint
3. **License violations** — assess and remediate
4. **Major outdated (with known issues)** — plan migration
5. **Cross-repo version conflicts** — align versions
6. **Minor outdated** — batch update
7. **Patch outdated** — batch update

Group related updates together:
- All `@types/*` packages in one PR
- All packages from the same org (e.g., `@babel/*`)
- Peer dependency chains that must move together

Note breaking change risks for any major update. Link to migration guides where available.

### 8. Report

Produce a severity-coded summary table:

| Priority | Package | Current | Latest | Type | Severity | Repos Affected | Action |
|----------|---------|---------|--------|------|----------|---------------|--------|
| 1 | lodash | 4.17.19 | 4.17.21 | patch | CRITICAL (CVE-2021-23337) | repo-a, repo-b | Update immediately |
| 2 | express | 4.17.1 | 4.21.2 | minor | HIGH (CVE-2024-29041) | repo-a | Update this sprint |
| 3 | webpack | 4.46.0 | 5.94.0 | major | MEDIUM (outdated) | repo-a | Plan migration |
| ... | | | | | | | |

Follow with:
- Total dependency count (direct / transitive) per repo
- Security summary: X critical, Y high, Z medium, W low
- Outdated summary: X major, Y minor, Z patch
- License summary: X flagged, Y clean
- Cross-repo conflicts: X packages with version divergence

## Key Principles

1. **Never auto-update.** This skill audits and recommends. The human decides what to update and when. Automated updates can introduce breaking changes, especially for major versions.
2. **Security first.** Critical and high-severity vulnerabilities always top the priority list, regardless of how old other dependencies are.
3. **Group related updates.** Updating `react` without updating `react-dom` creates version mismatches. Always identify peer dependency chains.
4. **Context matters.** A major version bump on a dev-only dependency (e.g., `eslint`) is lower risk than a patch on a production runtime dependency with a CVE.
5. **Lock files are truth.** Always read the lock file for actual resolved versions, not just the range specifier in the manifest.
6. **Don't chase latest for its own sake.** If a dependency is working, stable, and has no advisories, "outdated" is not the same as "broken."

## How to Use This Skill

Ask:
- "Audit the dependencies in ~/Repos/my-app"
- "Compare dependency versions across these three repos"
- "Are there any security vulnerabilities in this project?"
- "Check for license issues before we open-source this repo"
- "Build me an update plan for everything that's behind"

For command reference, license compatibility details, and false positive handling, see [REFERENCE.md](REFERENCE.md).
For worked examples, see [EXAMPLES.md](EXAMPLES.md).
