---
name: security-audit
description: "Multi-layer security audit — dependency scanning, filesystem analysis, optional SAST, and AI pentester reasoning. Use when the user says 'scan security', 'audit my code', 'check vulnerabilities', 'security report', or 'pentest this'."
---

# Security Audit

## Critical Rules

- **Never install tools automatically** — detect what is available, suggest install commands if missing, never run `curl | sh`.
- **Protect outputs** — `.security/` must be in `.gitignore` before any scan runs. Reports may contain secrets and vulnerability details.
- **Ask before fixing** — present findings and fix plan, apply only what the user explicitly approves, one fix at a time.
- **Target the analysis** — do not read the entire codebase. Focus Layer 4 on high-risk surfaces (auth, input boundaries, API config).
- **Timeout everything** — 120s per dependency audit command, 300s for Trivy, 600s for SAST. Kill and note if exceeded.

## Modes

| Mode | Layers | Output |
|------|--------|--------|
| `quick` | 1 + 2 | Inline summary only, no files |
| `full` (default) | 1 + 2 + 3 + 4 | Report + fix plan in `.security/` |
| `ci` | 1 + 2 + 3 + 4 | Report + exit code 1 if new critical/high |

If the user does not specify a mode, use `full`.

---

## Phase 0 — Setup

```bash
mkdir -p .security
```

**Gitignore guard:**

```bash
grep -qxF '.security/' .gitignore 2>/dev/null || echo '.security/' >> .gitignore
```

**Tool inventory** — check availability before running any layer:

```bash
command -v trivy >/dev/null && echo "trivy:ok" || echo "trivy:missing"
command -v semgrep >/dev/null && echo "semgrep:ok" || echo "semgrep:missing"
command -v snyk >/dev/null && echo "snyk:ok" || echo "snyk:missing"
```

If a tool is missing, note it in the report and suggest install via package manager only:

| Tool | macOS | Linux (Debian/Ubuntu) |
|------|-------|-----------------------|
| Trivy | `brew install trivy` | `sudo apt install trivy` |
| Semgrep | `brew install semgrep` | `pip install semgrep` |
| Snyk | `brew install snyk` | `npm install -g snyk` |

**Baseline** — if `.security/baseline.json` exists, load it. Known findings will be labeled "(baseline)" in the report and excluded from CI failure checks.

---

## Layer 1 — Dependency Audit

Detect the package manager from lockfiles. Run the matching command with a 120s timeout:

| Ecosystem | Detection file | Command |
|-----------|---------------|---------|
| Node (npm) | `package-lock.json` | `timeout 120 npm audit --json > .security/deps-audit.json` |
| Node (pnpm) | `pnpm-lock.yaml` | `timeout 120 pnpm audit --json > .security/deps-audit.json` |
| Node (yarn) | `yarn.lock` | `timeout 120 yarn npm audit --json > .security/deps-audit.json` |
| Python | `requirements.txt` / `pyproject.toml` | `timeout 120 pip-audit --format json -o .security/deps-audit.json` |
| Go | `go.sum` | `timeout 120 govulncheck -json ./... > .security/deps-audit.json 2>&1` |
| Rust | `Cargo.lock` | `timeout 120 cargo audit --json > .security/deps-audit.json` |
| Ruby | `Gemfile.lock` | `timeout 120 bundle audit check --format json > .security/deps-audit.json` |
| PHP | `composer.lock` | `timeout 120 local-php-security-checker --format json > .security/deps-audit.json` |
| Java (Maven) | `pom.xml` | Check for `dependency-check-maven` plugin first. If absent, skip with note. |

**Monorepo:** if multiple lockfiles exist, run each and merge into a single JSON array.

No package manager detected? Skip and note in report.

---

## Layer 2 — Filesystem Scan (Trivy)

Check `trivy --version` first. The `--scanners` flag requires >= 0.37 — fall back to `--security-checks vuln,secret,config` for older versions.

```bash
timeout 300 trivy fs \
  --scanners vuln,secret,misconfig \
  --skip-dirs .git,dist,build,.next,.turbo,vendor,target,node_modules,.security \
  --format json \
  -o .security/trivy-report.json \
  .
```

Trivy detects hardcoded secrets, infrastructure misconfigurations (Dockerfile, k8s, Terraform, Helm), and vulnerable dependencies (cross-validates Layer 1).

If Trivy is not installed, skip and note in report.

**Layer 1 and Layer 2 are independent — run them in parallel.**

---

### Quick mode stops here

If mode is `quick`:
1. Parse `deps-audit.json` and `trivy-report.json`
2. Output an inline summary grouped by severity (Critical / High / Medium)
3. Show new vs baseline counts if baseline exists
4. Stop — do not proceed to Layer 3 or 4

---

## Layer 3 — SAST (optional)

Run whichever tool was found in Phase 0. If none are installed, skip and note in report.

### Option A — Semgrep (preferred open-source)

```bash
timeout 600 semgrep scan \
  --config p/default \
  --json \
  -o .security/semgrep-report.json \
  --exclude .security \
  --exclude node_modules \
  --exclude vendor \
  --max-target-bytes 1000000 \
  .
```

Use `p/default` — not `auto`. The `auto` config fetches rules from a remote registry at runtime, introducing supply chain risk on the scanner itself.

### Option B — Snyk

```bash
timeout 300 snyk test --json > .security/snyk-sca.json
timeout 600 snyk code test --json > .security/snyk-sast.json
```

---

## Layer 4 — AI Pentester Reasoning

**This is the most important layer. Do not skip it.**

### Step 1 — Parse scanner outputs

Read all JSON files in `.security/`:
- Summarize critical and high findings in plain language
- Group by type: secrets, vulnerable deps, misconfigs, SAST issues
- Deduplicate: same CVE in Layer 1 and Layer 2 counts once
- Filter noise: skip informational and low-confidence findings
- Note skipped layers and reasons

### Step 2 — Targeted codebase analysis

Do not attempt to read the full codebase. Use glob/grep to locate high-risk files, then read only those. Analyze in this priority order:

**1. Authentication & session management**
Search: `**/auth/**`, `**/login.*`, `**/session.*`, `**/middleware/auth*`, JWT/session config files.
Look for: missing token expiry, weak hashing, session fixation, broken logout, missing CSRF protection.

**2. Authorization & access control**
Search: `**/middleware/**`, `**/guard*`, `**/policy*`, `**/permission*`, route definitions with role checks.
Look for: missing authz on endpoints, IDOR, privilege escalation, mass assignment via unfiltered request bodies.

**3. Data input boundaries**
Search: route handlers, API controllers, form processors, GraphQL resolvers.
Look for: unvalidated input reaching DB queries (SQLi), shell commands (command injection), HTML output (XSS), file paths (path traversal), URLs (SSRF).

**4. API surface configuration**
Search: CORS config, rate limiting setup, CSP/security headers, cookie config.
Look for: `Access-Control-Allow-Origin: *`, missing rate limits, insecure cookie flags, missing security headers.

**5. Secrets & environment**
Search: `.env*` files, config files, hardcoded strings matching key patterns.
Look for: committed `.env` files, secrets in source code, keys in client-side bundles, insecure defaults.

**6. Infrastructure as code**
Search: `Dockerfile*`, `docker-compose*`, `**/k8s/**`, `**/*.tf`, CI config files.
Look for: running as root, exposed ports, privileged containers, overly permissive IAM, secrets in CI env.

### Step 3 — Generate report

Save to `.security/report-YYYY-MM-DD.md`:

```markdown
# Security Audit Report — YYYY-MM-DD

## Summary

- **Mode:** quick | full | ci
- **Scope:** <project name>
- **Layers executed:** <list>
- **Layers skipped:** <list with reasons>
- **Tools:** <name + version for each>

| Severity | New | Baseline | Total |
|----------|-----|----------|-------|
| Critical | X   | Y        | X+Y   |
| High     | X   | Y        | X+Y   |
| Medium   | X   | Y        | X+Y   |
| Low      | X   | Y        | X+Y   |

## Critical & High Findings

### [C-01] <Title>

- **Severity:** Critical
- **Source:** Layer N — <tool> | AI analysis
- **File(s):** `path/to/file.ts:42`
- **Description:** <What is wrong and why it matters>
- **Evidence:** <Code snippet or scanner output>
- **Impact:** <What an attacker could do>
- **Recommendation:** <How to fix>

## Medium & Low Findings

<!-- Same structure, condensed -->

## Skipped Layers

| Layer | Reason |
|-------|--------|
```

---

## Fix Plan

Save to `.security/fix-plan-YYYY-MM-DD.md`.

For each finding:

| Field | Value |
|-------|-------|
| **ID** | Finding ID from report (C-01, H-02, etc.) |
| **What** | Clear description |
| **File(s)** | Exact paths |
| **Severity** | Critical / High / Medium / Low |
| **Difficulty** | Easy (config/dep update) / Medium (code change) / Hard (architecture) |
| **Effort** | < 5 min / 5–30 min / > 30 min |
| **Fix** | Exact command, code snippet, or config change |

Sort: Critical > High > Medium > Low, then quick wins first (effort ascending).

**Present the plan to the user. Only apply fixes the user explicitly approves.**
- One fix at a time — show the diff before applying.
- After each fix, re-run only the relevant scanner to verify.
- Do not batch fixes.

---

## Baseline Management

After the report, ask the user:

> "Do you want to mark any findings as accepted risk? They will be excluded from future CI failures."

If yes, save to `.security/baseline.json`:

```json
{
  "version": 1,
  "updated": "YYYY-MM-DD",
  "acknowledged": [
    {
      "hash": "<sha256 of type+file+line>",
      "id": "M-03",
      "reason": "Accepted risk — internal API only",
      "date": "YYYY-MM-DD"
    }
  ]
}
```

Future runs diff against the baseline and label known findings as "(baseline)".

---

## CI Mode

When mode is `ci`:
- Run all layers, generate report files
- **Exit 1** if any Critical or High finding is new (not in baseline)
- **Exit 0** if all findings are Medium/Low or already baselined
- Print one-line summary to stdout: `SECURITY AUDIT: 2 critical, 1 high, 5 medium (1 new critical) — FAIL`

---

## Output Structure

```
.security/
├── deps-audit.json            # Layer 1
├── trivy-report.json          # Layer 2
├── semgrep-report.json        # Layer 3 (if Semgrep)
├── snyk-sca.json              # Layer 3 (if Snyk)
├── snyk-sast.json             # Layer 3 (if Snyk)
├── baseline.json              # Acknowledged findings
├── report-YYYY-MM-DD.md       # Final report
└── fix-plan-YYYY-MM-DD.md     # Fix plan
```
