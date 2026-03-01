---
name: security-scan
description: |
  Whole-codebase vulnerability analysis leveraging 1M context window.
  Loads entire project source, runs deep security analysis in a single pass.
  Opus 4.6 found 500 zero-day vulnerabilities in pre-release testing — this skill weaponizes that capability.
argument-hint: "[optional: specific focus area, e.g. 'auth' or 'api routes']"
effort: max
---

# /security-scan

Deep security analysis of an entire codebase in a single pass.

## Philosophy

Traditional security scanning is file-by-file. It misses cross-file vulnerabilities: data flows from user input through multiple modules to a dangerous sink. With Opus 4.6's 1M token context, we load the entire project and trace attack surfaces end-to-end.

**This is NOT a replacement for dedicated SAST/DAST tools.** It's a complementary analysis that catches what those tools miss: logic flaws, auth bypasses, business logic vulnerabilities, and cross-module data flow issues.

## Process

### 1. Load Full Codebase

```bash
# Estimate token count
find . -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.rb" | \
  grep -v node_modules | grep -v .next | grep -v dist | grep -v build | \
  xargs wc -l 2>/dev/null | tail -1
```

If under ~200K lines: load everything into context via full file reads.
If over: focus on the attack surface (auth, API routes, data access, user input handlers).

### 2. Map Attack Surface

Read ALL of these file categories:
- **Entry points**: API routes, webhooks, form handlers, CLI commands
- **Auth/authz**: Middleware, guards, session management, JWT handling
- **Data access**: Database queries, ORM models, raw SQL
- **User input**: Form validation, request parsing, file uploads
- **External integrations**: API clients, webhook handlers, OAuth flows
- **Secrets management**: env var usage, config files, .env patterns
- **Infrastructure**: Dockerfile, CI/CD workflows, deployment configs

### 3. Vulnerability Analysis

Spawn `security-sentinel` agent with the full diff/codebase context. Analyze for:

**OWASP Top 10:**
- A01: Broken Access Control — missing auth checks, IDOR, privilege escalation
- A02: Cryptographic Failures — weak hashing, plaintext secrets, insecure transport
- A03: Injection — SQL, NoSQL, OS command, LDAP, XSS
- A04: Insecure Design — business logic flaws, missing rate limiting
- A05: Security Misconfiguration — default creds, verbose errors, open CORS
- A06: Vulnerable Components — outdated deps with known CVEs
- A07: Auth Failures — weak passwords, missing MFA, session issues
- A08: Software/Data Integrity — unsigned updates, insecure deserialization
- A09: Logging Failures — missing audit trails, sensitive data in logs
- A10: SSRF — unvalidated URLs, internal network access

**Cross-Module Analysis (unique to 1M context):**
- Trace user input from entry point through all transformations to sink
- Identify auth bypass paths across middleware chains
- Find data exposure through API response serialization
- Detect race conditions in concurrent operations
- Map trust boundary violations across service calls

### 4. Dependency Audit

```bash
# npm/pnpm
pnpm audit 2>/dev/null || npm audit 2>/dev/null

# Python
pip-audit 2>/dev/null || safety check 2>/dev/null

# Go
govulncheck ./... 2>/dev/null

# Rust
cargo audit 2>/dev/null
```

### 5. Secrets Scan

```bash
# Check for hardcoded secrets
grep -rn "sk_live\|sk_test\|AKIA\|password\s*=\s*['\"]" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" . | grep -v node_modules | grep -v ".env.example"

# Check .env files not in .gitignore
git ls-files --cached | grep -i "\.env$" | head -5
```

## Output Format

```markdown
## Security Scan: [project-name]

**Scope:** [X files, Y lines analyzed]
**Effort:** max
**Date:** [timestamp]

---

### Critical (Immediate Fix Required)
- [ ] `file:line` — [Vulnerability type] — [Description] — [Exploit path]

### High (Fix Before Deploy)
- [ ] `file:line` — [Vulnerability type] — [Description]

### Medium (Fix in Sprint)
- [ ] `file:line` — [Vulnerability type] — [Description]

### Low (Track and Fix)
- [ ] `file:line` — [Vulnerability type] — [Description]

### Dependency Vulnerabilities
| Package | Version | CVE | Severity | Fix Version |
|---------|---------|-----|----------|-------------|

### Cross-Module Findings
- [Data flow from X through Y to Z creates injection risk]
- [Auth middleware skipped on route A when accessed via B]

### Positive Observations
- [Good security patterns found]
- [Well-implemented auth flows]
```

## When to Use

- Before any production deployment
- After adding new API routes or auth logic
- When integrating new external services
- During quarterly security reviews
- After dependency updates

## Related

- `/check-quality` — Includes lightweight security scan
- `/review-branch` — security-sentinel is mandatory reviewer
- `/billing-security` — Payment-specific security patterns
