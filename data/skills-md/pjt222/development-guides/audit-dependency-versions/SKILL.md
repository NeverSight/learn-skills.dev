---
name: audit-dependency-versions
description: >
  Audit project dependencies for version staleness, security vulnerabilities,
  and compatibility issues. Covers lock file analysis, upgrade path planning,
  and breaking change assessment. Use before a release to ensure dependencies
  are current and secure, during periodic maintenance reviews, after receiving
  a security advisory, when upgrading to a new language version, before
  submitting to CRAN or npm, or when inheriting a project to assess its
  dependency health.
license: MIT
allowed-tools: Read Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: versioning
  complexity: intermediate
  language: multi
  tags: versioning, dependencies, audit, security, upgrades
---

# Audit Dependency Versions

Audit project dependencies for version staleness, known security vulnerabilities, and compatibility issues. This skill inventories all dependencies from lock files, checks each against the latest available version, classifies staleness levels, identifies security concerns, and produces a prioritized upgrade report with recommended actions.

## When to Use

- Before a release to ensure dependencies are current and secure
- During periodic maintenance (monthly or quarterly dependency reviews)
- After receiving a security advisory affecting a project dependency
- When upgrading a project to a new language version (e.g., R 4.4 to 4.5)
- Before submitting a package to CRAN, npm, or crates.io
- When inheriting a project and assessing its dependency health

## Inputs

- **Required**: Project root directory containing dependency/lock files
- **Optional**: Ecosystem type if not auto-detectable (R, Node.js, Python, Rust)
- **Optional**: Security-only mode flag (skip staleness, focus on CVEs)
- **Optional**: Allowlist of dependencies to skip (known acceptable older versions)
- **Optional**: Target date for compatibility (e.g., "must work with R 4.4.x")

## Procedure

### Step 1: Inventory All Dependencies

Locate and parse dependency files to build a complete inventory.

**R packages:**
```bash
# Direct dependencies from DESCRIPTION
grep -A 100 "^Imports:" DESCRIPTION | grep -B 100 "^[A-Z]" | head -50
grep -A 100 "^Suggests:" DESCRIPTION | grep -B 100 "^[A-Z]" | head -50

# Pinned versions from renv.lock
cat renv.lock | grep -A 3 '"Package"'
```

**Node.js:**
```bash
# Direct dependencies
cat package.json | grep -A 100 '"dependencies"' | grep -B 100 "}"
cat package.json | grep -A 100 '"devDependencies"' | grep -B 100 "}"

# Pinned versions from lock file
cat package-lock.json | grep '"version"' | head -20
```

**Python:**
```bash
# From requirements or pyproject
cat requirements.txt
cat pyproject.toml | grep -A 50 "dependencies"

# Pinned versions
cat requirements.lock 2>/dev/null || pip freeze
```

**Rust:**
```bash
# From Cargo.toml
grep -A 50 "\[dependencies\]" Cargo.toml
# Pinned versions
cat Cargo.lock | grep -A 2 "name ="
```

Build an inventory table:

```markdown
| Package | Pinned Version | Type | Ecosystem |
|---|---|---|---|
| dplyr | 1.1.4 | Import | R |
| testthat | 3.2.1 | Suggests | R |
| express | 4.18.2 | dependency | Node.js |
| pytest | 8.0.0 | dev | Python |
```

**Expected:** Complete inventory of all direct and (optionally) transitive dependencies with pinned versions.

**On failure:** If lock files are missing, the project has reproducibility issues. Note this as a finding and inventory from the manifest file (DESCRIPTION, package.json) using declared version constraints instead of pinned versions.

### Step 2: Check Latest Available Versions

For each dependency, determine the latest available version.

**R:**
```r
# Check available versions
available.packages()[c("dplyr", "testthat"), "Version"]

# Or via CLI
Rscript -e 'cat(available.packages()["dplyr", "Version"])'
```

**Node.js:**
```bash
# Check outdated packages
npm outdated --json

# Or individual package
npm view express version
```

**Python:**
```bash
# Check outdated
pip list --outdated --format=json

# Or individual
pip index versions requests 2>/dev/null
```

**Rust:**
```bash
# Check outdated
cargo outdated

# Or individual
cargo search serde --limit 1
```

Update the inventory with latest versions:

```markdown
| Package | Pinned | Latest | Gap |
|---|---|---|---|
| dplyr | 1.1.4 | 1.1.6 | patch |
| ggplot2 | 3.4.0 | 3.5.1 | minor |
| Rcpp | 1.0.10 | 1.0.14 | patch |
| shiny | 1.7.4 | 1.9.1 | minor |
```

**Expected:** Latest version identified for each dependency with the gap magnitude (patch/minor/major).

**On failure:** If a package registry is unreachable, note the dependency as "unable to check" and proceed with the rest. Do not block the entire audit on one unreachable registry.

### Step 3: Classify Staleness

Assign a staleness level to each dependency:

| Level | Definition | Action |
|---|---|---|
| **Current** | At latest version or within latest patch | No action needed |
| **Patch behind** | Same major.minor, older patch | Low priority upgrade, usually safe |
| **Minor behind** | Same major, older minor | Medium priority, review changelog for new features |
| **Major behind** | Older major version | High priority, likely breaking changes in upgrade |
| **EOL / Archived** | Package no longer maintained | Critical: find replacement or fork |

Produce a staleness summary:

```markdown
### Staleness Summary

- **Current**: 12 packages (48%)
- **Patch behind**: 8 packages (32%)
- **Minor behind**: 3 packages (12%)
- **Major behind**: 1 package (4%)
- **EOL/Archived**: 1 package (4%)

**Overall health**: AMBER (major-behind and EOL packages present)
```

Color coding:
- **GREEN**: All packages current or patch-behind
- **AMBER**: Any minor-behind or one major-behind
- **RED**: Multiple major-behind or any EOL packages

**Expected:** Every dependency classified by staleness with an overall health rating.

**On failure:** If version comparison logic is ambiguous (non-SemVer versions, date-based versions), classify conservatively as "minor behind" and note the non-standard versioning.

### Step 4: Check for Security Vulnerabilities

Run ecosystem-specific security audit tools:

**R:**
```r
# No built-in audit tool; check manually
# Cross-reference with https://www.r-project.org/security.html
# Check GitHub advisories for each package
```

**Node.js:**
```bash
# Built-in audit
npm audit --json

# Severity levels: info, low, moderate, high, critical
npm audit --audit-level=moderate
```

**Python:**
```bash
# Using pip-audit
pip-audit --format=json

# Or safety
safety check --json
```

**Rust:**
```bash
# Using cargo-audit
cargo audit --json
```

Document findings:

```markdown
### Security Findings

| Package | Version | CVE | Severity | Fixed In | Description |
|---|---|---|---|---|---|
| express | 4.18.2 | CVE-2024-XXXX | High | 4.19.0 | Path traversal in static file serving |
| lodash | 4.17.20 | CVE-2021-23337 | Critical | 4.17.21 | Command injection via template |

**Security status**: RED (1 critical, 1 high)
```

**Expected:** Security vulnerabilities identified with CVE, severity, affected version, and fix version.

**On failure:** If no audit tool is available for the ecosystem, search GitHub Security Advisories manually for each dependency. Note that the audit is best-effort without tooling.

### Step 5: Plan Upgrade Path

Prioritize upgrades based on risk and impact:

```markdown
### Upgrade Plan

#### Priority 1: Security Fixes (do immediately)
| Package | Current | Target | Risk | Notes |
|---|---|---|---|---|
| lodash | 4.17.20 | 4.17.21 | Low (patch) | Fixes CVE-2021-23337 |
| express | 4.18.2 | 4.19.0 | Low (minor) | Fixes CVE-2024-XXXX |

#### Priority 2: EOL Replacements (plan within 1 month)
| Package | Current | Replacement | Migration Effort |
|---|---|---|---|
| request | 2.88.2 | node-fetch 3.x | Medium (API change) |

#### Priority 3: Major Version Upgrades (plan for next release cycle)
| Package | Current | Target | Breaking Changes |
|---|---|---|---|
| webpack | 4.46.0 | 5.90.0 | Config format, plugin API |

#### Priority 4: Minor/Patch Updates (batch in maintenance window)
| Package | Current | Target | Notes |
|---|---|---|---|
| dplyr | 1.1.4 | 1.1.6 | Patch fixes only |
| ggplot2 | 3.4.0 | 3.5.1 | New geom functions added |
```

For each major upgrade, note known breaking changes by checking the dependency's changelog.

**Expected:** Prioritized upgrade plan with security fixes first, then EOL replacements, major upgrades, and minor/patch batches.

**On failure:** If a dependency has no clear upgrade path (abandoned with no fork), document the risk and recommend: (1) vendoring the current version, (2) finding an alternative package, or (3) accepting the risk with monitoring.

### Step 6: Document Compatibility Risks

For each planned upgrade, assess compatibility:

```markdown
### Compatibility Assessment

#### express 4.18.2 -> 4.19.0
- **API changes**: None (patch-level fix)
- **Node.js requirement**: Same (>=14)
- **Test impact**: Run full test suite; expect zero failures
- **Confidence**: HIGH

#### webpack 4.46.0 -> 5.90.0
- **API changes**: Config file format changed, several plugins removed
- **Node.js requirement**: >=10.13 (unchanged)
- **Test impact**: Build configuration must be rewritten; all tests need re-run
- **Confidence**: LOW (requires dedicated migration effort)
- **Migration guide**: https://webpack.js.org/migrate/5/
```

Write the complete audit report to `DEPENDENCY-AUDIT.md` or `DEPENDENCY-AUDIT-2026-02-17.md`.

**Expected:** Compatibility risks documented for each significant upgrade. Complete audit report written.

**On failure:** If compatibility cannot be assessed without testing, recommend a branch-based upgrade approach: create a branch, apply the upgrade, run tests, and evaluate results before merging.

## Validation

- [ ] All direct dependencies inventoried from lock/manifest files
- [ ] Latest available version checked for each dependency
- [ ] Staleness level assigned (current / patch / minor / major / EOL)
- [ ] Overall health rating calculated (GREEN / AMBER / RED)
- [ ] Security audit run with ecosystem-appropriate tooling
- [ ] All CVEs documented with severity, affected version, and fix version
- [ ] Upgrade plan prioritized: security > EOL > major > minor/patch
- [ ] Compatibility risks assessed for each major upgrade
- [ ] Audit report written to DEPENDENCY-AUDIT.md
- [ ] No dependencies left as "unable to check" without documented reason

## Common Pitfalls

- **Ignoring transitive dependencies**: A project may have 10 direct dependencies but 200 transitive ones. Security vulnerabilities often hide in transitive dependencies. Use `npm ls` or `renv::dependencies()` to see the full tree.
- **Upgrading everything at once**: Batch-upgrading all dependencies in one commit makes it impossible to identify which upgrade caused a regression. Upgrade in logical groups (security first, then majors individually, then minors/patches as a batch).
- **Confusing "outdated" with "insecure"**: A package one major version behind with no CVEs is lower risk than a current package with a critical vulnerability. Always prioritize security over freshness.
- **Not reading changelogs**: Blindly upgrading a major version without reading the changelog. Breaking changes in the dependency become breaking changes in your project.
- **Audit fatigue**: Running audits but not acting on findings. Set a policy: security findings must be addressed within 1 sprint, EOL within 1 quarter.
- **Missing lock files**: Projects without lock files have non-reproducible builds. If the audit reveals missing lock files, that is itself a critical finding to address before versioned upgrades.

## Related Skills

- `apply-semantic-versioning` -- Version bumps may be triggered by dependency upgrades
- `manage-renv-dependencies` -- R-specific dependency management with renv
- `security-audit-codebase` -- Broader security audit that includes dependency vulnerabilities
- `manage-changelog` -- Document dependency upgrades in the changelog
- `plan-release-cycle` -- Schedule dependency upgrades within the release timeline
