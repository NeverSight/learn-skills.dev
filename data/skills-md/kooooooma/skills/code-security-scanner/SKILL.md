---
name: code-security-scanner
description: Scan code repositories for security threats including data exfiltration, backdoors, malicious code injection, dependency chain risks, and sensitive file access. Use this skill when users want to audit a codebase (especially TypeScript/JavaScript/Node.js projects) for security vulnerabilities, detect hidden malware, review npm dependencies for supply-chain attacks, check for credential leaks, or perform a pre-deployment security review. Triggers on requests like "scan for malicious code", "security audit", "check for backdoors", "review dependencies for vulnerabilities", "detect data exfiltration".
---

# Code Security Scanner

Scan code repositories for malicious behavior: data theft, backdoors, code injection, supply-chain attacks, and sensitive file access. Optimized for TypeScript/JavaScript/Node.js but applicable to general codebases.

## Security Auditor Mindset

Before scanning, think like an attacker:

- **Motivation**: What valuable data exists in this project? (API keys, user data, financial info, cloud credentials)
- **Attack Surface**: What are the entry points? (`npm install` lifecycle, runtime execution, build pipeline, CI/CD)
- **Stealth**: How would an attacker hide malicious code? (obfuscation, delayed execution via `setTimeout`, legitimate-looking variable names, deeply nested dependencies)
- **Exfil Path**: How would stolen data leave? (HTTP POST, DNS queries, WebSocket, embedded in error logs, encoded in image metadata)

> Ask yourself: "If I were a malicious actor with commit access or supply-chain control, where would I hide code and how would I avoid detection?"

### Severity Triage Principle

Not all findings are equal. Prioritize by **blast radius × stealth**:

| Priority | Blast Radius | Stealth Level | Example |
|----------|-------------|---------------|---------|
| P0 | Full credential theft | High (obfuscated) | Base64-encoded exfil URL + env var harvest |
| P1 | Single secret leaked | Medium | Hardcoded webhook URL with API key |
| P2 | Potential access | Low (visible) | `eval()` with user-controlled input |
| P3 | Informational | None | Unpinned dependency version |

## Core Workflow

### Step 1: Determine Scan Scope

Identify the project structure before scanning:

1. Locate `package.json`, `tsconfig.json`, `.npmrc`, lockfiles (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`)
2. Identify entry points: `main`, `scripts`, `bin` fields in `package.json`
3. List all `preinstall`/`postinstall`/`prepare` lifecycle scripts
4. Note any `.env`, `.env.*`, or config files containing potential secrets
5. Check if monorepo — scan all `packages/*/package.json` if `workspaces` field exists

**For non-npm projects** (Deno, Bun, or plain scripts): Skip dependency analysis and focus on code pattern scanning (Phases 1-3, 5).

### Step 2: Load Detection Rules

Load the reference file(s) matching the scan type:

| User Request | MUST Load | Do NOT Load |
|-------------|-----------|-------------|
| "full security audit" | ALL 5 references | (none) |
| "check for credential leaks / data exfiltration" | `references/data-exfiltration.md` | dependency-risks, filesystem-risks |
| "check for backdoors" | `references/backdoor-detection.md` | dependency-risks, filesystem-risks |
| "scan for malicious code / eval" | `references/malicious-code-patterns.md` | dependency-risks, filesystem-risks |
| "audit npm dependencies" | `references/dependency-risks.md` | data-exfiltration, backdoor-detection |
| "check for sensitive file access" | `references/filesystem-risks.md` | data-exfiltration, backdoor-detection |

> **IMPORTANT**: For targeted scans, load ONLY the relevant reference. Do NOT load all 5 references for a focused request — this wastes context and dilutes attention.

### Step 3: Execute Scan

Scan in severity order — **Critical (🔴) first, then Medium (🟡)**:

#### 🔴 Phase 1: Data Exfiltration Detection

**MANDATORY**: Read `references/data-exfiltration.md` for grep patterns.

Search for patterns that send sensitive data to external servers.

**Key signals:**
- HTTP requests containing `process.env`, API keys, or tokens in the body/headers
- Hardcoded URLs receiving environment variable data
- Base64-encoded destination URLs
- DNS-based exfiltration patterns

#### 🔴 Phase 2: Backdoor Detection

**MANDATORY**: Read `references/backdoor-detection.md` for grep patterns.

Search for hidden network listeners and remote access.

**Key signals:**
- `net.createServer` / `http.createServer` on unusual ports
- `child_process` spawning shells with network arguments
- Hidden Express/Koa/Fastify routes not documented in API specs
- WebSocket connections to hardcoded external hosts

#### 🔴 Phase 3: Malicious Code Injection

**MANDATORY**: Read `references/malicious-code-patterns.md` for grep patterns.

Search for dynamic code execution and obfuscation.

**Key signals:**
- `eval()`, `new Function()`, `vm.runInNewContext()`
- Strings assembled character-by-character then executed
- `Buffer.from(..., 'base64')` followed by `eval` or `exec`
- `postinstall` / `preinstall` scripts running network requests or shell commands

#### 🟡 Phase 4: Dependency Chain Risks

**MANDATORY**: Read `references/dependency-risks.md` for analysis patterns.

Analyze dependencies for supply-chain attack indicators.

**Key signals:**
- Typosquatting package names (e.g., `lodahs` instead of `lodash`)
- Packages with `postinstall` hooks that download/execute remote code
- Unpinned versions (`*`, `latest`) or very recent publications

**Fallbacks for different package managers:**

| Tool | Primary Command | Fallback |
|------|----------------|----------|
| npm | `npm audit --json` | Parse `package-lock.json` manually |
| yarn | `yarn audit --json` | Parse `yarn.lock` manually |
| pnpm | `pnpm audit --json` | Parse `pnpm-lock.yaml` manually |
| None | — | Read `package.json` dependencies and grep `node_modules/*/package.json` for `postinstall` |

#### 🟡 Phase 5: Sensitive File Access

**MANDATORY**: Read `references/filesystem-risks.md` for grep patterns.

Search for code reading sensitive local files.

**Key signals:**
- Reading `~/.ssh/`, `~/.aws/`, `~/.gnupg/`
- Accessing browser profile directories or cookie stores
- Reading `.env` files outside the project root
- OS keychain or credential manager access

### Step 4: Generate Security Report

Produce a structured report:

```markdown
# Security Scan Report — [Project Name]

## Summary
- **Scan Date**: [date]
- **Files Scanned**: [count]
- **Critical Findings**: [count]
- **Medium Findings**: [count]

## 🔴 Critical Findings
### [Finding Title]
- **Category**: [Data Exfiltration | Backdoor | Malicious Code]
- **File**: `path/to/file.ts:line`
- **Code**: [offending code snippet]
- **Risk**: [what could happen]
- **Recommendation**: [how to fix]

## 🟡 Medium Findings
### [Finding Title]
- **Category**: [Dependency Risk | Filesystem Risk]
- **File**: `path/to/file.ts:line`
- **Risk**: [description]
- **Recommendation**: [action]

## ✅ Passed Checks
[List categories that passed with no findings]
```

## Anti-Patterns (Common False Positives)

> NEVER flag these without checking context first. Doing so floods the report with noise and erodes trust.

1. **Legitimate `eval()`** — Template engines (EJS, Handlebars), REPL tools, and test frameworks may use `eval`. Flag ONLY when it processes external/user input or fetched data.
2. **Build scripts with `child_process`** — Common in build tools (webpack plugins, gulp tasks). Only flag when combined with network operations or env var exfiltration.
3. **HTTP requests in test files** — Mock servers and test utilities commonly use `net.createServer`. Deprioritize `**/*.test.*`, `**/*.spec.*`, and `__tests__/` directories.
4. **Env var access in config loaders** — Libraries like `dotenv`, `convict`, `config` legitimately read `.env` files. Flag only when env values are sent to non-project endpoints.
5. **Minified/bundled vendor files** — `dist/`, `vendor/`, `*.min.js`, `*.bundle.js` contain obfuscated code by design. Skip UNLESS recently modified (check `git log` timestamp) or the project doesn't use a bundler.
6. **Crypto libraries** — Legitimate use of `crypto`, `bcrypt`, `argon2`, `jose`, Base64 encoding for JWT. Flag ONLY when combined with network calls to non-standard endpoints.
7. **Code generators and AST tools** — Babel plugins, TypeScript compiler extensions, ESLint custom rules, and Prettier plugins legitimately use `eval`-like constructs and dynamic `require()`. Check the package purpose.
8. **CI/CD and dev tooling `postinstall`** — `husky`, `patch-package`, `electron-builder`, `node-gyp` use legitimate `postinstall` hooks. Prioritize scanning `dependencies` over `devDependencies`. Flag devDependencies only if they download from suspicious URLs.
9. **Monorepo workspace scripts** — Tools like Turborepo, Lerna, and Nx run `child_process.exec` across workspace packages. This is expected infrastructure, not a backdoor.
10. **SSH libraries in deployment tools** — Packages like `node-ssh`, `ssh2` are legitimate in deployment/provisioning tools. Flag only in libraries/packages that shouldn't need remote access.

### The Context Rule

> Before escalating any finding to 🔴 Critical, verify: **"Does this code run in production, AND does it touch sensitive data, AND does it communicate externally?"** All three must be true for a genuine critical finding.
