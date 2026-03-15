---
name: code-audit
description: >
  Perform a comprehensive security and code quality audit on web-based projects (React, Next.js, NestJS).
  Uses the OWASP Top 10:2025 standard as the primary security framework. Generates a detailed Markdown
  report with findings categorized by severity (CRITICAL, HIGH, MEDIUM, LOW). Use this skill whenever
  the user asks to audit, review, scan, or analyze their codebase for vulnerabilities, security issues,
  code quality problems, bad patterns, or potential bugs. Also trigger when the user mentions "OWASP",
  "security review", "vulnerability scan", "code audit", "pentest review", "security assessment",
  "code health check", or asks "is my code secure?" or "find bugs in my project". Trigger even if
  the user just says "audit this" or "check my code" pointing at a web project. This skill supports
  React, Next.js, and NestJS projects, including monorepos containing multiple project types.
---

# Code Audit Skill — OWASP Top 10:2025

This skill performs a structured security and code quality audit against the OWASP Top 10:2025 standard.
It produces a severity-classified Markdown report with actionable remediation guidance.

## Supported Project Types

- **React** (CRA, Vite, custom setups)
- **Next.js** (App Router, Pages Router)
- **NestJS** (REST APIs, GraphQL APIs, microservices)
- **Monorepos** containing any combination of the above

## Workflow

Follow these steps in order. Do not skip steps. Read the relevant reference files before scanning.

### Step 1: Discover Project Structure

Run these commands to understand the project:

```bash
# Find the project root and understand structure
ls -la <project_root>
cat <project_root>/package.json
find <project_root> -name "tsconfig*.json" -maxdepth 2 | head -5
find <project_root> -name "next.config*" -maxdepth 2 | head -3
find <project_root> -name "nest-cli.json" -maxdepth 2 | head -3
```

Determine the project type(s):
- **Next.js**: Has `next` in dependencies and `next.config.*`
- **React (non-Next)**: Has `react` in dependencies, no `next`
- **NestJS**: Has `@nestjs/core` in dependencies, or `nest-cli.json`
- **Monorepo**: Has `workspaces` in package.json, or `lerna.json`, `nx.json`, `turbo.json`

### Step 2: Read the Relevant Reference Files

Based on the detected project type, read the corresponding reference files:

- **All projects**: Read `references/owasp-2025-checks.md` (the OWASP Top 10:2025 mapping)
- **React / Next.js**: Read `references/frontend-checks.md`
- **NestJS**: Read `references/nestjs-checks.md`

These files contain the specific patterns, anti-patterns, and code signatures to look for.

### Step 3: Collect Critical Files

Gather these files for analysis (adapt paths to the project structure):

**Configuration & Dependencies (always)**:
- `package.json` and `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml`
- `.env*` files (check if they exist, flag if committed)
- `tsconfig.json`
- `.eslintrc*`, `.prettierrc*`
- `Dockerfile`, `docker-compose.yml` if present
- CI/CD configs (`.github/workflows/`, `.gitlab-ci.yml`, etc.)

**Next.js specific**:
- `next.config.*` (rewrites, headers, CSP, image domains)
- `middleware.ts` / `middleware.js`
- `app/layout.tsx` or `pages/_app.tsx`
- API routes: `app/api/**/route.ts` or `pages/api/**`
- Server actions, server components with data fetching

**React specific**:
- Entry point (`src/index.tsx`, `src/main.tsx`)
- Router configuration
- Auth context/provider files
- API client/service layer

**NestJS specific**:
- `main.ts` (bootstrap, CORS, helmet, validation pipe)
- `app.module.ts`
- All `*.guard.ts`, `*.interceptor.ts`, `*.filter.ts`, `*.middleware.ts`
- All `*.controller.ts` and `*.service.ts`
- Auth module files
- Database entities/schemas and migration configs
- DTOs and validation pipes

### Step 4: Perform the Audit

Systematically analyze each OWASP Top 10:2025 category. For each category:

1. Search for the specific patterns described in the reference files
2. Check both presence of security controls AND absence of expected protections
3. Consider the architectural context (a missing guard matters more in a payment controller)
4. Record every finding with: file path, line range, description, severity, OWASP category, and fix

Use `grep -rn` and `find` commands to search for patterns efficiently:

```bash
# Examples of useful searches
grep -rn "dangerouslySetInnerHTML" <project_root>/src/ --include="*.tsx" --include="*.jsx"
grep -rn "eval(" <project_root>/src/ --include="*.ts" --include="*.js"
grep -rn "@Public()" <project_root>/src/ --include="*.ts"
grep -rn "createQueryBuilder" <project_root>/src/ --include="*.ts"
grep -rn "innerHTML" <project_root>/src/ --include="*.ts" --include="*.tsx"
grep -rn "CORS" <project_root>/src/ --include="*.ts"
grep -rn "helmet" <project_root>/src/ --include="*.ts"
grep -rn "class-validator" <project_root>/package.json
grep -rn "rate" <project_root>/src/ --include="*.ts" -i
grep -rn "\.env" <project_root>/.gitignore
find <project_root> -name "*.env" -not -path "*/node_modules/*"
find <project_root> -name "*.pem" -o -name "*.key" -not -path "*/node_modules/*"
```

Beyond pattern matching, READ the actual source files for logic-level issues that grep cannot catch:
- Authorization logic flaws (checking wrong user ID, missing ownership validation)
- Business logic bypasses
- Race conditions in state management
- Insecure data flow between components
- Missing error boundaries and exception handling
- Improper secret management

### Step 5: Classify Severity

Each finding gets one severity level:

**CRITICAL** — Exploitable now with high impact:
- SQL/NoSQL injection with user input reaching queries unsanitized
- Authentication bypass, missing auth on sensitive endpoints
- Hardcoded secrets, API keys, or credentials in source code
- Remote code execution vectors (`eval()`, `Function()` with user input)
- Exposed admin routes without authentication
- SSRF vulnerabilities

**HIGH** — Exploitable with moderate effort or significant impact:
- XSS vulnerabilities (stored or reflected)
- Missing CSRF protection on state-changing operations
- Broken access control (IDOR, privilege escalation paths)
- Insecure direct object references
- Missing rate limiting on auth endpoints
- Sensitive data in logs or error responses
- Insecure deserialization

**MEDIUM** — Requires specific conditions to exploit or moderate impact:
- Missing security headers (CSP, HSTS, X-Frame-Options)
- Weak password policies or session management
- Verbose error messages leaking stack traces
- Missing input validation on non-critical endpoints
- Outdated dependencies with known CVEs (non-critical)
- Missing CORS restrictions (overly permissive)
- Insecure cookie configuration

**LOW** — Best practice violations, defense-in-depth gaps:
- Missing `rel="noopener noreferrer"` on external links
- Console.log statements in production code
- Missing TypeScript strict mode
- No Content Security Policy (informational)
- Missing Subresource Integrity (SRI) for CDN scripts
- Code quality issues that could lead to future vulnerabilities

### Step 6: Generate the Report

Use the template in `scripts/report-template.md` as the base structure. The report must include:

1. **Executive Summary** — Project type, overall risk score, total findings by severity
2. **OWASP Top 10:2025 Scorecard** — Pass/Fail/Partial for each of the 10 categories
3. **Detailed Findings** — Grouped by severity, then by OWASP category within each severity
4. **Remediation Roadmap** — Prioritized action items
5. **Appendix** — Files analyzed, tools/patterns used, audit metadata

Each finding in the detailed section must contain:
- Unique ID (e.g., `AUDIT-001`)
- Title
- Severity badge
- OWASP Category mapping
- Affected file(s) and line(s)
- Description of the vulnerability
- Code snippet showing the issue (keep it short, 5-10 lines max)
- Recommended fix with code example
- References (CWE ID if applicable)

### Step 7: Save the Report

- If the user specified an output path, save there
- Otherwise, save to `<project_root>/AUDIT-REPORT.md`
- Always inform the user where the report was saved
- Copy the report to `/mnt/user-data/outputs/AUDIT-REPORT.md` so the user can download it

## Important Principles

- **Do not guess.** If you cannot read a file, say so and note it as a gap in the audit.
- **Context matters.** A missing guard on a health-check endpoint is LOW. The same missing guard on a payment endpoint is CRITICAL.
- **Check for absence.** Missing security controls (no helmet, no validation pipe, no rate limiter) are findings, not just bad code.
- **Be specific.** "Possible XSS" is useless. "User input from `req.query.search` rendered via `dangerouslySetInnerHTML` in `SearchResults.tsx:42`" is actionable.
- **Include fixes.** Every finding must have a concrete remediation with a code example.
- **Stay current.** The OWASP Top 10:2025 is the standard. Do not use the 2021 categories.
- **Respect scope.** Only audit what is in the codebase. Do not speculate about infrastructure unless config files reveal it.
