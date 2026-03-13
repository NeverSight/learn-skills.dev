---
name: sca-security
description: "Software Composition Analysis skill for identifying vulnerable dependencies, license compliance, and supply chain security. This skill should be used when scanning dependencies for CVEs, analyzing SBOM (Software Bill of Materials), checking license compliance, auditing npm/pip/maven/cargo packages, or assessing supply chain risks. Triggers on requests to scan dependencies, check for vulnerable packages, generate SBOM, analyze license compliance, or audit software supply chain."
---

# Software Composition Analysis (SCA)

This skill enables comprehensive analysis of software dependencies for security vulnerabilities, license compliance, and supply chain risks using tools like Snyk, OWASP Dependency-Check, Trivy, Grype, and various ecosystem-specific scanners.

## When to Use This Skill

This skill should be invoked when:
- Scanning project dependencies for known vulnerabilities
- Generating and analyzing Software Bill of Materials (SBOM)
- Checking license compliance for open source components
- Auditing npm, pip, Maven, Cargo, Go modules
- Assessing supply chain security risks
- Integrating dependency scanning into CI/CD

### Trigger Phrases
- "scan dependencies for vulnerabilities"
- "check package security"
- "generate SBOM"
- "license compliance check"
- "audit npm packages"
- "supply chain security scan"

---

## Prerequisites

### Required Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| Trivy | Multi-ecosystem scanner | `brew install trivy` |
| Grype | Vulnerability scanner | `brew install grype` |
| Syft | SBOM generator | `brew install syft` |
| OWASP Dependency-Check | Java-focused scanner | Download from GitHub |
| Snyk CLI | Commercial scanner | `npm install -g snyk` |
| npm audit | Node.js native | Built into npm |
| pip-audit | Python packages | `pip install pip-audit` |
| cargo audit | Rust crates | `cargo install cargo-audit` |
| OSV-Scanner | Google OSV database | `go install github.com/google/osv-scanner/cmd/osv-scanner@latest` |

---

## Quick Start Workflow

```markdown
1. **Identify Package Ecosystem**
   - Node.js (package.json, package-lock.json, yarn.lock)
   - Python (requirements.txt, Pipfile.lock, poetry.lock)
   - Java (pom.xml, build.gradle)
   - .NET (packages.config, *.csproj)
   - Rust (Cargo.lock)
   - Go (go.mod, go.sum)
   - Ruby (Gemfile.lock)
   - PHP (composer.lock)

2. **Generate SBOM**
   - Use Syft for comprehensive SBOM
   - Export in CycloneDX or SPDX format

3. **Vulnerability Scan**
   - Run Trivy/Grype against SBOM or directory
   - Check ecosystem-specific tools

4. **License Analysis**
   - Extract license information
   - Check compliance with policy

5. **Remediation**
   - Upgrade vulnerable packages
   - Replace deprecated dependencies
   - Document accepted risks

6. **CI/CD Integration**
   - Add scanning to pipeline
   - Set failure thresholds
   - Generate reports
```

---

## SBOM Generation

### Syft SBOM Creation

```bash
# Scan directory
syft dir:/path/to/project

# Scan container image
syft nginx:latest

# Output formats
syft dir:. -o json > sbom.json
syft dir:. -o cyclonedx-json > sbom-cyclonedx.json
syft dir:. -o spdx-json > sbom-spdx.json
syft dir:. -o table

# Scan specific package files
syft file:package-lock.json
syft file:requirements.txt

# Include file metadata
syft dir:. -o json --file-metadata
```

### CycloneDX Native Tools

```bash
# Node.js
npx @cyclonedx/cyclonedx-npm --output-file sbom.json

# Python
pip install cyclonedx-bom
cyclonedx-py environment -o sbom.json

# Java/Maven
mvn org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom

# .NET
dotnet tool install --global CycloneDX
dotnet CycloneDX project.csproj -o sbom.json

# Go
go install github.com/CycloneDX/cyclonedx-gomod/cmd/cyclonedx-gomod@latest
cyclonedx-gomod mod -json > sbom.json
```

---

## Vulnerability Scanning

### Trivy Dependency Scanning

```bash
# Scan filesystem for vulnerabilities
trivy fs /path/to/project

# Scan specific file
trivy fs --scanners vuln package-lock.json

# Filter by severity
trivy fs --severity HIGH,CRITICAL .

# Output formats
trivy fs -f json -o results.json .
trivy fs -f sarif -o results.sarif .
trivy fs -f table .

# Ignore unfixed vulnerabilities
trivy fs --ignore-unfixed .

# Exit code on findings
trivy fs --exit-code 1 --severity CRITICAL .

# Scan SBOM
trivy sbom sbom.json
```

### Grype Scanning

```bash
# Scan directory
grype dir:/path/to/project

# Scan SBOM
grype sbom:./sbom.json

# Output formats
grype dir:. -o json > results.json
grype dir:. -o table
grype dir:. -o cyclonedx > results-sbom.xml

# Fail on severity
grype dir:. --fail-on high

# Only show fixed vulnerabilities
grype dir:. --only-fixed
```

### OSV-Scanner

```bash
# Scan directory
osv-scanner -r /path/to/project

# Scan specific lockfile
osv-scanner --lockfile package-lock.json

# Scan SBOM
osv-scanner --sbom sbom.json

# Output formats
osv-scanner -r . --format json > results.json
osv-scanner -r . --format table

# Experimental call analysis (Go)
osv-scanner -r --experimental-call-analysis .
```

### OWASP Dependency-Check

```bash
# Basic scan
dependency-check --project "MyProject" --scan /path/to/project

# Specific formats
dependency-check --project "MyProject" --scan . \
  --format HTML --format JSON --out reports/

# Fail on CVSS score
dependency-check --project "MyProject" --scan . \
  --failOnCVSS 7

# Update NVD database
dependency-check --updateonly

# Suppress false positives
dependency-check --project "MyProject" --scan . \
  --suppression suppressions.xml
```

---

## Ecosystem-Specific Scanning

### Node.js / npm

```bash
# npm audit
npm audit
npm audit --json > audit.json
npm audit fix
npm audit fix --force  # May introduce breaking changes

# Yarn
yarn audit
yarn audit --json > audit.json

# pnpm
pnpm audit
pnpm audit --json > audit.json

# Snyk
snyk test
snyk test --json > snyk.json
snyk monitor  # Continuous monitoring
```

### Python

```bash
# pip-audit
pip-audit
pip-audit -r requirements.txt
pip-audit -f json -o audit.json
pip-audit --fix  # Auto-upgrade packages

# Safety (PyUp.io)
pip install safety
safety check
safety check -r requirements.txt --json > safety.json

# Bandit for code + dependencies
bandit -r . -f json -o bandit.json

# Snyk
snyk test --file=requirements.txt
```

### Java / Maven

```bash
# OWASP Dependency-Check Maven Plugin
mvn org.owasp:dependency-check-maven:check

# SpotBugs with security plugin
mvn com.github.spotbugs:spotbugs-maven-plugin:check

# Snyk
snyk test --file=pom.xml
snyk test --all-projects  # Multi-module

# Gradle
./gradlew dependencyCheckAnalyze
```

### Go

```bash
# govulncheck (official)
go install golang.org/x/vuln/cmd/govulncheck@latest
govulncheck ./...

# Nancy (Sonatype)
go install github.com/sonatype-nexus-community/nancy@latest
go list -json -deps ./... | nancy sleuth

# Snyk
snyk test --file=go.mod
```

### Rust

```bash
# cargo-audit
cargo install cargo-audit
cargo audit
cargo audit --json > audit.json

# cargo-deny (licenses + advisories)
cargo install cargo-deny
cargo deny check

# Snyk
snyk test --file=Cargo.toml
```

### Ruby

```bash
# Bundler audit
gem install bundler-audit
bundle-audit check
bundle-audit check --update

# Snyk
snyk test --file=Gemfile.lock
```

### .NET

```bash
# dotnet list vulnerable packages
dotnet list package --vulnerable

# Snyk
snyk test --file=project.csproj

# OWASP Dependency-Check
dependency-check --project "DotNetProject" --scan . \
  --enableExperimental
```

### PHP

```bash
# Composer audit
composer audit

# Local PHP Security Checker
symfony security:check

# Snyk
snyk test --file=composer.lock
```

---

## License Compliance

### License Detection

```bash
# Syft with license info
syft dir:. -o json | jq '.artifacts[].licenses'

# licensee (GitHub)
gem install licensee
licensee detect .

# license-checker (npm)
npx license-checker --json > licenses.json
npx license-checker --onlyAllow 'MIT;Apache-2.0;BSD-3-Clause'

# pip-licenses (Python)
pip install pip-licenses
pip-licenses --format=json > licenses.json
pip-licenses --fail-on "GPL"
```

### License Categories

```markdown
## Permissive (Generally Safe)
- MIT
- Apache 2.0
- BSD-2-Clause / BSD-3-Clause
- ISC
- Unlicense

## Copyleft (Requires Review)
- GPL v2 / v3
- LGPL v2.1 / v3
- AGPL v3
- MPL 2.0

## Restrictive / Commercial
- Proprietary
- Commercial
- Source-available

## Unknown / Custom
- Requires manual review
- May need legal consultation
```

### License Policy Enforcement

```yaml
# .licensepolicy.yaml
allowed:
  - MIT
  - Apache-2.0
  - BSD-2-Clause
  - BSD-3-Clause
  - ISC

denied:
  - GPL-2.0
  - GPL-3.0
  - AGPL-3.0

exceptions:
  - package: some-gpl-package
    license: GPL-2.0
    reason: "Used only at build time, not distributed"
```

---

## Supply Chain Security

### Dependency Confusion Prevention

```markdown
## Checks
- [ ] Private registry configured
- [ ] Scoped packages used (@company/package)
- [ ] Registry priority enforced
- [ ] Lock files committed
- [ ] Integrity hashes verified

## npm Configuration
// .npmrc
registry=https://registry.npmjs.org/
@company:registry=https://npm.company.com/

## pip Configuration
// pip.conf
[global]
index-url = https://pypi.company.com/simple/
extra-index-url = https://pypi.org/simple/
```

### Typosquatting Detection

```bash
# Check for similar package names
# Manual: Compare with official package names

# Automated tools
# - Snyk monitors for typosquatting
# - Socket.dev detects suspicious packages
# - npm diff to compare packages
```

### Lockfile Integrity

```bash
# npm
npm ci  # Clean install from lockfile
npm install --package-lock-only  # Update lockfile only

# pip
pip-compile requirements.in  # Generate locked requirements
pip install --require-hashes -r requirements.txt

# Go
go mod verify

# Cargo
cargo check --locked
```

### Provenance & Signing

```bash
# npm provenance
npm publish --provenance  # Sign with OIDC

# Sigstore / cosign
cosign sign package.tar.gz
cosign verify package.tar.gz

# Go module checksums
# Automatically verified via sum.golang.org

# Python (PEP 458)
# Experimental TUF support
```

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Dependency Scan

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '0 0 * * *'  # Daily

jobs:
  trivy-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'HIGH,CRITICAL'
          exit-code: '1'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  npm-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm audit --audit-level=high

  snyk-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high
```

### GitLab CI

```yaml
stages:
  - security

dependency-scan:
  stage: security
  image: aquasec/trivy:latest
  script:
    - trivy fs --exit-code 1 --severity HIGH,CRITICAL .
  artifacts:
    reports:
      container_scanning: trivy-results.json
  allow_failure: false

npm-audit:
  stage: security
  image: node:20
  script:
    - npm ci
    - npm audit --audit-level=high
  only:
    changes:
      - package*.json
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: npm-audit
        name: npm audit
        entry: bash -c 'npm audit --audit-level=high'
        language: system
        files: package-lock.json

      - id: pip-audit
        name: pip-audit
        entry: pip-audit
        language: python
        files: requirements.txt
```

---

## Vulnerability Database Sources

### Primary Sources

| Database | URL | Coverage |
|----------|-----|----------|
| NVD | nvd.nist.gov | CVEs (all) |
| GitHub Advisory | github.com/advisories | Multi-ecosystem |
| OSV | osv.dev | Multi-ecosystem |
| Snyk Vuln DB | snyk.io | Commercial |
| PyPI Advisory | pypi.org | Python |
| npm Registry | npmjs.com | Node.js |
| RustSec | rustsec.org | Rust |
| Go Vuln DB | vuln.go.dev | Go |

### Updating Databases

```bash
# Trivy
trivy image --download-db-only

# Grype
grype db update

# OWASP Dependency-Check
dependency-check --updateonly

# OSV-Scanner
# Auto-updates from osv.dev API
```

---

## Remediation Strategies

### Upgrade Path Analysis

```bash
# npm
npm outdated
npm update
npm install package@latest

# pip
pip list --outdated
pip install --upgrade package

# Maven
mvn versions:display-dependency-updates

# Cargo
cargo update
cargo outdated
```

### Vulnerability Suppression

```xml
<!-- dependency-check suppression.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<suppressions xmlns="https://jeremylong.github.io/DependencyCheck/dependency-suppression.1.3.xsd">
  <suppress>
    <notes>False positive - not using vulnerable feature</notes>
    <packageUrl regex="true">^pkg:npm/example-package@.*$</packageUrl>
    <cve>CVE-2021-XXXXX</cve>
  </suppress>
</suppressions>
```

```yaml
# .trivyignore
CVE-2021-XXXXX
CVE-2022-YYYYY

# Snyk .snyk file
version: v1.5.0
ignore:
  SNYK-JS-EXAMPLE-123456:
    - '*':
        reason: 'Not exploitable in our usage'
        expires: 2024-12-31
```

### Remediation Checklist

```markdown
### For Each Vulnerability
- [ ] Verify vulnerability applies to usage
- [ ] Check if patch/upgrade available
- [ ] Test upgrade compatibility
- [ ] Document if accepting risk
- [ ] Set review date for unresolved

### Priority Matrix
| Severity | Exploitable | Fix Available | Action |
|----------|-------------|---------------|--------|
| Critical | Yes | Yes | Immediate fix |
| Critical | Yes | No | Mitigate/Monitor |
| High | Yes | Yes | Fix within 7 days |
| High | No | Yes | Fix within 30 days |
| Medium | - | Yes | Fix within 90 days |
| Low | - | - | Document/Monitor |
```

---

## Reporting Template

```markdown
# Software Composition Analysis Report

## Executive Summary
- Project: [Name]
- Scan date: YYYY-MM-DD
- Total dependencies: X
- Direct dependencies: Y
- Transitive dependencies: Z
- Vulnerabilities: Critical (X) | High (Y) | Medium (Z) | Low (W)

## Vulnerability Summary

### Critical Vulnerabilities
| Package | Version | CVE | CVSS | Fix Version |
|---------|---------|-----|------|-------------|
| lodash | 4.17.20 | CVE-2021-23337 | 9.1 | 4.17.21 |

### High Vulnerabilities
| Package | Version | CVE | CVSS | Fix Version |
|---------|---------|-----|------|-------------|
| axios | 0.21.1 | CVE-2021-3749 | 7.5 | 0.21.2 |

## License Compliance

### License Distribution
| License | Count | Compliance |
|---------|-------|------------|
| MIT | 150 | Approved |
| Apache-2.0 | 45 | Approved |
| GPL-3.0 | 2 | Review Required |

### Flagged Packages
| Package | License | Action |
|---------|---------|--------|
| gpl-package | GPL-3.0 | Requires review |

## SBOM
Full SBOM attached in CycloneDX format.

## Recommendations
1. [P1] Upgrade lodash to 4.17.21
2. [P1] Upgrade axios to 0.21.2
3. [P2] Review GPL-licensed dependencies
4. [P3] Enable automated scanning in CI
```

---

## Bundled Resources

### scripts/
- `scan_all.sh` - Multi-ecosystem dependency scan
- `sbom_generate.py` - SBOM generation automation
- `license_check.py` - License compliance checking

### references/
- `vulnerability_databases.md` - Database source documentation
- `license_guide.md` - License compatibility matrix
- `remediation_guide.md` - Upgrade strategies

### checklists/
- `sca_audit.md` - SCA audit checklist
- `supply_chain.md` - Supply chain security checklist
- `license_compliance.md` - License compliance checklist
