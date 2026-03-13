---
name: security-scanner
description: >-
  Proactive security assessment with SAST, secrets detection, dependency
  scanning, and compliance checks. Use for pre-deployment audit. NOT for
  code review (honest-review) or pen testing.
argument-hint: "<mode> [path]"
model: opus
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0"
---

# Security Scanner

Proactive pre-deployment security assessment. SAST pattern matching, secrets detection,
dependency scanning, OWASP/CWE mapping, and compliance heuristics.

**Scope:** Pre-deployment security audit only. NOT for code review (use honest-review),
penetration testing, runtime security monitoring, or supply chain deep analysis.

## Canonical Vocabulary

| Term | Definition |
|------|------------|
| **finding** | A discrete security issue with severity, CWE mapping, confidence, and remediation |
| **severity** | CRITICAL / HIGH / MEDIUM / LOW / INFO classification per CVSS-aligned heuristics |
| **confidence** | Score 0.0-1.0 per finding; >=0.7 report, 0.3-0.7 flag as potential, <0.3 discard |
| **CWE** | Common Weakness Enumeration identifier mapping the finding to a known weakness class |
| **OWASP** | Open Web Application Security Project Top 10 category mapping |
| **SAST** | Static Application Security Testing — pattern-based source code analysis |
| **secret** | Hardcoded credential, API key, token, or private key detected in source |
| **lockfile** | Dependency manifest with pinned versions (package-lock.json, uv.lock, etc.) |
| **compliance** | Lightweight heuristic scoring against SOC2/GDPR/HIPAA controls |
| **triage** | Risk-stratify files by security relevance before deep scanning |
| **remediation** | Specific fix guidance with code examples when applicable |
| **SARIF** | Static Analysis Results Interchange Format for CI integration |
| **false positive** | Detection matching a pattern but not an actual vulnerability |

## Dispatch

| $ARGUMENTS | Mode | Action |
|------------|------|--------|
| Empty | `scan` | Full codebase security scan with triage/sampling |
| `scan [path]` | `scan` | Full security scan of path (default: cwd) |
| `check <file/dir>` | `check` | Targeted security check on specific files |
| `deps [path]` | `deps` | Dependency lockfile analysis |
| `secrets [path]` | `secrets` | Secrets-only regex scan |
| `compliance <standard>` | `compliance` | SOC2/GDPR/HIPAA heuristic checklist |
| `report` | `report` | Dashboard visualization of findings |
| Unrecognized input | — | Ask for clarification |

## Mode: scan

Full codebase security assessment with triage and sampling for large codebases.

### Step 1: Triage

1. Enumerate files: `find` or Glob to build file inventory
2. Risk-stratify files into HIGH/MEDIUM/LOW security relevance:
   - HIGH: auth, crypto, payments, user input handling, API endpoints, config with secrets
   - MEDIUM: data models, middleware, utilities touching external I/O
   - LOW: static assets, tests, documentation, pure computation
3. For 100+ files: sample — all HIGH, 50% MEDIUM, 10% LOW
4. Build dependency graph of HIGH-risk files

### Step 2: SAST Pattern Scan

Read HIGH and sampled MEDIUM/LOW files. Match against patterns from `references/owasp-patterns.md`:

- Injection flaws (SQL, command, path traversal, template, LDAP)
- Authentication/session weaknesses
- Sensitive data exposure (logging PII, plaintext storage)
- XXE, SSRF, deserialization
- Security misconfiguration
- XSS (reflected, stored, DOM)
- Insecure direct object references
- Missing access controls
- CSRF vulnerabilities
- Using components with known vulnerabilities

### Step 3: Secrets Scan

Run: `uv run python skills/security-scanner/scripts/secrets-detector.py <path>`
Parse JSON output. Cross-reference findings with `.gitignore` coverage.

### Step 4: Dependency Check

If lockfiles exist, run: `uv run python skills/security-scanner/scripts/dependency-checker.py <path>`
Parse JSON output. Flag outdated or unmaintained dependencies.

### Step 5: CWE/OWASP Mapping

Map each finding to CWE IDs and OWASP Top 10 categories using `references/cwe-patterns.md`.
Assign severity (CRITICAL/HIGH/MEDIUM/LOW/INFO) and confidence (0.0-1.0).

### Step 6: Remediation

For each finding with confidence >= 0.7, provide:
- CWE reference link
- Specific remediation guidance
- Code example when applicable

### Step 7: Report

Present findings grouped by severity. Include:
- Executive summary with finding counts by severity
- Detailed findings with CWE, OWASP, evidence, remediation
- Dependency health summary (if lockfiles scanned)
- Secrets summary (count by type, no values exposed)

## Mode: check

Targeted security check on specific files or directories.

1. Read the specified file(s)
2. Apply full SAST pattern matching (no triage/sampling — scan everything)
3. Run secrets detection on the path
4. Map findings to CWE/OWASP
5. Present findings with remediation

## Mode: deps

Dependency lockfile analysis.

1. Detect lockfiles: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `requirements.txt`, `uv.lock`, `Cargo.lock`, `go.sum`, `Gemfile.lock`, `composer.lock`
2. Run: `uv run python skills/security-scanner/scripts/dependency-checker.py <path>`
3. Parse output: dependency names, versions, ecosystem
4. Flag: outdated packages, packages with known CVE patterns, unusual version pinning
5. Present dependency health report

## Mode: secrets

Secrets-only scan using regex patterns.

1. Run: `uv run python skills/security-scanner/scripts/secrets-detector.py <path>`
2. Parse JSON findings
3. Cross-reference with `.gitignore` — flag secrets in tracked files as CRITICAL
4. Check git history for previously committed secrets: `git log --diff-filter=D -p -- <file>`
5. Present findings grouped by secret type, never exposing actual values

## Mode: compliance

Lightweight compliance heuristic scoring.

1. Validate `<standard>` is one of: `soc2`, `gdpr`, `hipaa`
2. Run: `uv run python skills/security-scanner/scripts/compliance-scorer.py <path> --standard <standard>`
3. Read reference checklist from `references/compliance-checklists.md`
4. Score each control as PASS/FAIL/PARTIAL with evidence
5. Present compliance scorecard with overall percentage and failing controls

## Mode: report

Generate visual security dashboard.

1. Collect all findings from the current session (or re-run scan if none exist)
2. Format findings as JSON matching the dashboard schema
3. Convert to SARIF if requested: `uv run python skills/security-scanner/scripts/sarif-formatter.py`
4. Inject JSON into `templates/dashboard.html`
5. Copy to a temporary file, open in browser

## Scaling Strategy

| Scope | Strategy |
|-------|----------|
| 1-10 files | Direct scan, no triage |
| 11-100 files | Triage + prioritized scan |
| 100-500 files | Triage + sampling (all HIGH, 50% MEDIUM, 10% LOW) |
| 500+ files | Triage + sampling + parallel subagents by risk tier |

## Reference Files

Load ONE reference at a time. Do not preload all references into context.

| File | Content | Read When |
|------|---------|-----------|
| references/owasp-patterns.md | OWASP Top 10 with code patterns and detection heuristics | During SAST scan (Step 2) |
| references/cwe-patterns.md | Top 50 CWEs with detection patterns and remediation | During CWE mapping (Step 5) |
| references/secrets-guide.md | Secret patterns, false positive hints, triage guidance | During secrets scan |
| references/dependency-audit.md | Dependency audit protocol and CVE lookup workflow | During deps mode |
| references/compliance-checklists.md | SOC2/GDPR/HIPAA control checklists with scoring | During compliance mode |
| references/triage-protocol.md | Risk stratification methodology for security files | During triage (Step 1) |
| references/scope-boundary.md | Boundary with honest-review, pen testing, runtime monitoring | When scope is unclear |

| Script | When to Run |
|--------|-------------|
| scripts/secrets-detector.py | Secrets scan — regex-based detection |
| scripts/dependency-checker.py | Dependency analysis — lockfile parsing |
| scripts/sarif-formatter.py | SARIF conversion — CI integration output |
| scripts/compliance-scorer.py | Compliance scoring — heuristic checklist |

| Template | When to Render |
|----------|----------------|
| templates/dashboard.html | After scan — inject findings JSON into data tag |

## Critical Rules

1. Never expose actual secret values in output — show type, file, line only
2. Every finding must map to at least one CWE ID
3. Confidence < 0.3 = discard; 0.3-0.7 = flag as potential; >= 0.7 = report
4. Run secrets-detector.py before reporting — regex patterns catch what LLM scanning misses
5. Do not report phantom vulnerabilities requiring impossible conditions
6. For 100+ files, always triage before scanning — never brute-force the full codebase
7. Dependency findings require version evidence — never flag without checking the actual version
8. Compliance mode is heuristic only — state this explicitly in output, never claim certification
9. Present findings before suggesting fixes — always use an approval gate
10. Cross-reference with .gitignore — secrets in untracked files are INFO, in tracked files are CRITICAL
11. Load ONE reference file at a time — do not preload all references into context
12. This skill is for pre-deployment audit only — redirect to honest-review for code review, refuse pen testing requests
13. SARIF output must conform to SARIF v2.1 schema — validate with sarif-formatter.py
14. Never modify source files — this skill is read-only analysis
