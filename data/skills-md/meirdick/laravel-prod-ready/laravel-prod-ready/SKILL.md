---
name: laravel-prod-ready
description: >
  Run a comprehensive production readiness audit on a Laravel application. Use this skill
  whenever someone wants to know if their Laravel app is ready to ship, launch, or go live —
  even if they phrase it as "security check", "pre-launch review", "is this production-ready?",
  "audit my project", "code review before deploy", "go-live checklist", or similar. Also
  trigger when someone asks for help with security vulnerabilities, finding hardcoded secrets,
  checking their CI/CD setup, or evaluating the reliability/scalability of their Laravel backend.
  This skill systematically evaluates a Laravel project across 6 dimensions (Security,
  Scalability, Reliability, Hardening, Code Quality, Operational Readiness) and produces a
  scored report with actionable, Laravel-specific fixes — not just a list of problems, but a
  clear picture of what's production-grade and what needs work.
license: MIT
compatibility: Designed for Laravel applications (8.x through 12.x). Requires a PHP/Composer project.
compatible_agents:
  - Claude Code
  - Cursor
  - Windsurf
  - Amp
  - Goose
  - Gemini CLI
  - OpenCode
  - Roo Code
tags:
  - laravel
  - php
  - security
  - production
  - audit
  - deployment
  - code-review
  - devops
metadata:
  author: meirdick
  version: "1.0"
---

# Laravel Production Readiness Review

## Context

This skill performs a comprehensive, read-only production readiness audit of a Laravel
application. It evaluates the project across 6 dimensions and produces a scored, actionable
report.

**Scope:** Laravel 8.x through 12.x applications using Eloquent, Blade, Sanctum/Passport,
Queues, Horizon, Livewire, Inertia, and the broader Laravel ecosystem.

**Tools covered:** Composer, Artisan, Eloquent ORM, Laravel config system, Blade templates,
Laravel HTTP client, Queue workers, Horizon, Telescope, Pulse, Forge, Vapor, Envoyer.

**You must NEVER modify any project files. This is a read-only audit.**

---

## Rules

### Step 1: Identify the Laravel Project

Orient yourself in the Laravel codebase. Use Glob to discover the project structure:

```
Glob: **/composer.json, **/artisan, **/config/*.php, **/routes/*.php
Glob: **/app/Http/Kernel.php, **/bootstrap/app.php, **/config/app.php
Glob: **/database/migrations/*.php, **/app/Models/*.php
Glob: **/.env*, **/.gitignore, **/Dockerfile, **/docker-compose.*
Glob: **/.github/workflows/*.{yml,yaml}
```

Read `composer.json` to determine:
- **Laravel version** (laravel/framework constraint)
- **Key packages** (Sanctum, Passport, Horizon, Telescope, Pulse, Livewire, Inertia, etc.)
- **PHP version** constraint

| Indicator | What it tells you | Watch out for |
|---|---|---|
| `laravel/sanctum` | API token / SPA auth | Missing token expiration, no ability revocation |
| `laravel/passport` | OAuth2 provider | Token lifetime too long, unused grant types |
| `laravel/horizon` | Queue monitoring | Dashboard exposed without auth |
| `laravel/telescope` | Debug/dev tool | Enabled in production, no auth gate |
| `laravel/pulse` | Production monitoring | Dashboard auth not configured |
| `livewire/livewire` | Full-stack components | Unprotected component methods, missing authorization |
| `inertiajs/inertia-laravel` | SPA bridge | Over-sharing props, exposing server data to client |
| `spatie/laravel-permission` | Roles & permissions | Missing authorization checks on routes |
| No queue driver config | Sync queue | Heavy operations blocking HTTP requests |

Also check the Laravel version to know which patterns apply:
- **Laravel 11+**: Slim skeleton — no `Http/Kernel.php`, middleware in `bootstrap/app.php`, `/up` health route built-in
- **Laravel 10 and below**: Traditional structure — `Http/Kernel.php`, `Exceptions/Handler.php`

### Step 2: Run All Six Audits

Load and apply each reference checklist **one at a time**, in order. For each one, actually run
the Glob and Grep patterns to discover findings — don't guess or assume from the stack alone.

Read these files from `references/`:

1. `security-checklist.md` — secrets, injection, auth, CSRF, mass assignment, rate limiting
2. `scalability-checklist.md` — N+1 queries, eager loading, pagination, queues, caching
3. `reliability-checklist.md` — exception handling, logging, health checks, transactions
4. `hardening-checklist.md` — APP_DEBUG, session config, env validation, dependency pinning
5. `code-quality-checklist.md` — tests, debug helpers, type safety, structural anti-patterns
6. `operational-readiness.md` — CI/CD, deployment, .env.example, monitoring, rollbacks

For each finding, note the **file path and line number**. Vague findings ("somewhere in the
codebase there might be...") are not useful. Be specific.

**Severity classification:**
- **CRITICAL** — Actively dangerous; fix before deploying (e.g. hardcoded secret, `APP_DEBUG=true` in production, SQL injection via `DB::raw()` with user input)
- **WARNING** — Meaningful risk or debt that should be addressed soon (e.g. missing rate limiting, no eager loading, no queue worker)
- **SUGGESTION** — Would improve quality or resilience but isn't a blocker (e.g. missing Telescope auth gate, no monitoring)

### Credential Redaction (Mandatory)

When reporting findings that contain secrets, API keys, passwords, or tokens, ALWAYS redact
the actual value. Show only the first 4 characters followed by `••••••••`. Never output full
credential values in the report. Example: `sk_live_••••••••`, `AKIA••••••••`, `ghp_••••••••`.

### Step 3: Score Each Dimension

Score each dimension 0–10 using the rubric in `references/report-template.md`.

Quick reference:

| Score | Meaning |
|---|---|
| 9–10 | Production-grade |
| 7–8 | Good — minor gaps only |
| 5–6 | Acceptable — some risks |
| 3–4 | Concerning — significant gaps |
| 0–2 | Critical — not safe for production |

**Overall rating:**
- **READY** — All dimensions 7+
- **ALMOST** — Most dimensions 6+, none below 4
- **NOT READY** — Any dimension below 4

### Step 4: Write the Report

Read `references/report-template.md` and produce the final report using that exact structure.

- **Be specific, not generic.** Don't say "consider adding rate limiting." Say: "No rate limiting on `POST /login` — the `throttle` middleware is missing from `routes/web.php:14`. Add `throttle:5,1` to the login route or configure `RateLimiter::for('login', ...)` in `AppServiceProvider`."
- **Acknowledge what's working.** Real Laravel projects always have some things done well. Find them and say so.
- **Order findings by impact.** The most dangerous issues should appear first.
- **Explain the "why" in plain language.** A brief, honest explanation of the real-world risk helps developers prioritize correctly.
- **Give concrete, Laravel-specific fixes.** Provide the actual Laravel code, Artisan command, or config change — not generic pseudocode.
- **Reference CWE/OWASP when relevant.** Include the CWE ID (e.g. CWE-798) so developers can look up the full context.

### Tool Usage

- **Glob** — File discovery (configs, migrations, models, controllers, routes, tests)
- **Grep** — Pattern matching (secrets, anti-patterns, missing configurations)
- **Read** — Inspect specific files for context and line-level findings
- **Never use Edit, Write, or Bash** — this is a read-only audit

### Tone

This audit is most useful when it's direct without being alarmist. A missing rate limiter is a
warning, not a catastrophe. An exposed `APP_KEY` or database password in source code is a
catastrophe. Calibrate your language accordingly.

When the project is in genuinely good shape, say so. When something is serious, be clear about
why it's serious. Developers trust audits that treat them as intelligent professionals who can
handle honest feedback.

---

## Examples

### Example finding (CRITICAL)

```
### 1. Hardcoded Stripe Key in Config — Security
**Severity:** CRITICAL
**Reference:** CWE-798
**File:** `config/services.php:18`
**Finding:** Stripe secret key is hardcoded instead of using `env()`:
  `'secret' => 'sk_live_••••••••'`
**Why it matters:** This key is committed to git history and visible to anyone with repo access.
  It grants full access to your Stripe account — charges, refunds, customer data.
**Fix:**
  // config/services.php
  'stripe' => [
      'secret' => env('STRIPE_SECRET'),
  ],
  // .env
  STRIPE_SECRET=<value from secrets manager>
```

### Example finding (WARNING)

```
### 4. N+1 Query in OrderController — Scalability
**Severity:** WARNING
**File:** `app/Http/Controllers/OrderController.php:34`
**Finding:** `Order::all()` without eager loading, then accessing `$order->customer` in the
  Blade view. With 100 orders, this makes 101 database queries.
**Fix:**
  // Before
  $orders = Order::all();
  // After
  $orders = Order::with('customer')->paginate(25);
```

### Example "What You Did Well"

```
## What You Did Well
- Sanctum is properly configured with token expiration and ability scoping
- All models define explicit `$fillable` arrays — no mass assignment risk
- Migrations are well-structured with proper indexes on foreign keys
- Form Requests are used consistently across all controllers
- Queue jobs implement `ShouldQueue` with retry and backoff configuration
```

---

## Anti-patterns

- **Not a penetration test.** This is a static code review, not an intrusive security assessment. It does not test running applications or exploit vulnerabilities.
- **Not a compliance certification.** This does not certify SOC 2, PCI-DSS, HIPAA, or GDPR compliance. It can identify common gaps, but formal compliance requires a qualified auditor.
- **Not a replacement for automated scanning tools.** For dependency vulnerability scanning, use `composer audit`. For secret scanning, use `gitleaks` or `trufflehog`. This skill complements those tools with architectural and configuration review.
- **Don't guess findings.** Every finding must reference a specific file and line number discovered via Glob/Grep/Read. Never report an issue based on assumptions about the stack.
- **Don't modify files.** This is strictly read-only. Never use Edit, Write, or Bash tools during the audit.

---

## References

- `references/security-checklist.md` — 16 security checks with CWE references and Laravel-specific Grep patterns
- `references/scalability-checklist.md` — Eloquent N+1, pagination, queues, caching, session drivers
- `references/reliability-checklist.md` — Exception handling, logging channels, health checks, transactions
- `references/hardening-checklist.md` — APP_DEBUG, Telescope/Debugbar exposure, cookie security, trusted proxies
- `references/code-quality-checklist.md` — Pest/PHPUnit, debug helpers, Larastan, structural anti-patterns
- `references/operational-readiness.md` — CI/CD, Forge/Vapor/Envoyer, monitoring, rollbacks
- `references/report-template.md` — Report structure, scoring rubric, tone guidelines
