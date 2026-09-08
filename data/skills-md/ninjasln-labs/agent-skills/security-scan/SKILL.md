---
name: security-scan
description: >-
  Security scan: scan code for security vulnerabilities including OWASP Top 10, secrets,
  and misconfigurations, with severity thresholds. Use when you need comprehensive
  security analysis of a codebase.
slug: security-scan
version: 1.0.0
displayName: security-scan
---

# Security Scan

Comprehensive security vulnerability detection for codebases.

## Quick Start

```
/security-scan                    # Full scan of current directory
/security-scan --scope src/       # Scan specific directory
/security-scan --quick            # Fast scan (critical issues only)
/security-scan --focus injection  # Focus on specific category
```

## What This Skill Does

Analyzes code for security vulnerabilities across multiple categories:

1. **OWASP Top 10** - Industry-standard web vulnerability categories
2. **Secrets Detection** - Hardcoded credentials, API keys, tokens
3. **Injection Flaws** - SQL, XSS, command injection patterns
4. **Cryptographic Issues** - Weak algorithms, insecure implementations
5. **Configuration Problems** - Insecure defaults, misconfigurations

## Scan Modes

### Full Scan (Default)
Comprehensive analysis of all security categories.

```
/security-scan
```

**Checks performed:**
- All OWASP Top 10 categories
- Secrets and credential detection
- Dependency vulnerabilities (if package files exist)
- Configuration file review

**Duration:** 2-5 minutes depending on codebase size

### Quick Scan
Fast check for critical and high-severity issues only.

```
/security-scan --quick
```

**Checks performed:**
- Critical injection patterns
- Exposed secrets
- Known dangerous functions

**Duration:** Under 1 minute

### Focused Scan
Target specific vulnerability category.

```
/security-scan --focus <category>
```

**Categories:**
- `injection` - SQL, XSS, command injection
- `secrets` - Credentials, API keys, tokens
- `crypto` - Cryptographic weaknesses
- `auth` - Authentication/authorization issues
- `config` - Configuration security

## Output Format

### Severity Levels

| Level | Icon | Meaning | Action Required |
|-------|------|---------|-----------------|
| CRITICAL | `[!]` | Exploitable vulnerability | Immediate fix |
| HIGH | `[H]` | Serious security risk | Fix before deploy |
| MEDIUM | `[M]` | Potential vulnerability | Plan to address |
| LOW | `[L]` | Minor issue or hardening | Consider fixing |
| INFO | `[i]` | Informational finding | Awareness only |

### Finding Format

```
[SEVERITY] CATEGORY: Brief description
  File: path/to/file.ext:line
  Pattern: What was detected
  Risk: Why this is dangerous
  Fix: How to remediate
```

### Summary Report

```
SECURITY SCAN RESULTS
=====================

Scope: src/
Files scanned: 127
Duration: 45 seconds

FINDINGS BY SEVERITY
  Critical: 2
  High: 5
  Medium: 12
  Low: 8

TOP ISSUES
1. [!] SQL Injection in src/api/users.ts:45
2. [!] Hardcoded AWS key in src/config.ts:12
3. [H] XSS vulnerability in src/components/Comment.tsx:89
...

Run `/security-scan --details` for full report.
```

## OWASP Top 10 Coverage

| # | Category | Detection Approach |
|---|----------|-------------------|
| A01 | Broken Access Control | Authorization pattern analysis |
| A02 | Cryptographic Failures | Weak crypto detection |
| A03 | Injection | Pattern matching + data flow |
| A04 | Insecure Design | Security control gaps |
| A05 | Security Misconfiguration | Config file analysis |
| A06 | Vulnerable Components | Dependency scanning |
| A07 | Auth Failures | Auth pattern review |
| A08 | Data Integrity Failures | Deserialization checks |
| A09 | Logging Failures | Audit log analysis |
| A10 | SSRF | Request pattern detection |

See `references/owasp/` for detailed detection rules per category.

## Detection Patterns

### Injection Detection

**SQL Injection:**
```
- String concatenation in queries
- Unsanitized user input in database calls
- Dynamic query construction
```

**Cross-Site Scripting (XSS):**
```
- innerHTML assignments with user data
- document.write() with dynamic content
- Unescaped template interpolation
```

**Command Injection:**
```
- exec(), system(), popen() with user input
- Shell command string construction
- Unsanitized subprocess arguments
```

See `references/patterns/` for language-specific patterns.

### Secrets Detection

**High-Confidence Patterns:**
```
AWS Access Key:     AKIA[0-9A-Z]{16}
AWS Secret Key:     [A-Za-z0-9/+=]{40}
GitHub Token:       gh[pousr]_[A-Za-z0-9]{36,}
Stripe Key:         sk_live_[A-Za-z0-9]{24,}
Private Key:        -----BEGIN (RSA |EC )?PRIVATE KEY-----
```

**Medium-Confidence Patterns:**
```
Generic API Key:    api[_-]?key.*[=:]\s*['"][a-zA-Z0-9]{16,}
Password in Code:   password\s*[=:]\s*['"][^'"]+['"]
Connection String:  (mysql|postgres|mongodb)://[^:]+:[^@]+@
```

### Cryptographic Weaknesses

**Weak Algorithms:**
```
- MD5 for password hashing
- SHA1 for security purposes
- DES/3DES encryption
- RC4 stream cipher
```

**Implementation Issues:**
```
- Hardcoded encryption keys
- Weak random number generation
- Missing salt in password hashing
- ECB mode encryption
```

## Integration with Other Skills

### With `/secrets-scan`
Focused deep-dive on credential detection:
```
/secrets-scan              # Dedicated secrets analysis
/secrets-scan --entropy    # High-entropy string detection
```

### With `/dependency-scan`
Package vulnerability analysis:
```
/dependency-scan           # Check all dependencies
/dependency-scan --fix     # Auto-fix where possible
```

### With `/config-scan`
Infrastructure and configuration review:
```
/config-scan               # All config files
/config-scan --docker      # Container security
/config-scan --iac         # Infrastructure as Code
```

## Scan Execution Protocol

### Phase 1: Discovery
```
1. Identify project type (languages, frameworks)
2. Locate relevant files (source, config, dependencies)
3. Determine applicable security rules
```

### Phase 2: Static Analysis
```
1. Pattern matching for known vulnerabilities
2. Data flow analysis for injection paths
3. Configuration review
```

### Phase 3: Secrets Scanning
```
1. High-confidence pattern matching
2. Entropy analysis for potential secrets
3. Git history check (optional)
```

### Phase 4: Dependency Analysis
```
1. Parse package manifests
2. Check against vulnerability databases
3. Identify outdated packages
```

### Phase 5: Reporting
```
1. Deduplicate findings
2. Assign severity scores
3. Generate actionable report
4. Provide remediation guidance
```

## Configuration

### Project-Level Config

Create `.security-scan.yaml` in project root:

```yaml
# Scan configuration
scan:
  exclude:
    - "node_modules/**"
    - "vendor/**"
    - "**/*.test.ts"
    - "**/__mocks__/**"

# Severity thresholds
thresholds:
  fail_on: critical    # critical, high, medium, low
  warn_on: medium

# Category toggles
categories:
  injection: true
  secrets: true
  crypto: true
  auth: true
  config: true
  dependencies: true

# Custom patterns
patterns:
  secrets:
    - name: "Internal API Key"
      pattern: "INTERNAL_[A-Z]{3}_KEY_[a-zA-Z0-9]{32}"
      severity: high
```

### Ignore Patterns

Create `.security-scan-ignore` for false positives:

```
# Ignore specific files
src/test/fixtures/mock-credentials.ts

# Ignore specific lines (use inline comment)
# security-scan-ignore: test fixture
const mockApiKey = "sk_test_fake123";
```

## Command Reference

| Command | Description |
|---------|-------------|
| `/security-scan` | Full security scan |
| `/security-scan --quick` | Critical issues only |
| `/security-scan --scope <path>` | Scan specific path |
| `/security-scan --focus <cat>` | Single category |
| `/security-scan --details` | Verbose output |
| `/security-scan --json` | JSON output |
| `/security-scan --fix` | Auto-fix where possible |

## Related Skills

- `/secrets-scan` - Deep secrets detection
- `/dependency-scan` - Package vulnerability analysis
- `/config-scan` - Configuration security review
- `/review-code` - General code review (includes security)

## References

- `references/owasp/` - OWASP Top 10 detection details
- `references/patterns/` - Language-specific vulnerability patterns
- `references/remediation/` - Fix guidance by vulnerability type
- `assets/severity-matrix.md` - Severity scoring criteria
