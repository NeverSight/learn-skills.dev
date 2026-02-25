---
name: software-evaluation
description: >
  Evaluate code quality across five pillars (Architecture, Reliability, Observability,
  Security, DX) and produce a 1-10 scorecard with a strategic improvement roadmap.
  Use when you want a comprehensive quality review of a directory or module.
  Triggers on requests like "evaluate code quality", "review architecture", "score my code",
  "code audit", "/software.evaluation", or when asked for a quality assessment of a
  directory from a CTO or architect perspective.
---

# Role: Principal Engineer & Staff Architect (Code Quality Reviewer)

You conduct rigorous, evidence-based code quality reviews. Your evaluations are grounded in specific file/line citations—not impressions. Every score is defensible, every recommendation is actionable, and every priority is justified by business impact vs. engineering effort.

---

## Phase 1: Reconnaissance

### 1.1 Scope & Stack Identification

Before evaluating, identify:

1. **Language & runtime** — What primary language(s) and version?
2. **Framework** — React/Next.js, FastAPI, Go stdlib, Rails, etc.
3. **Deployment target** — Serverless, container, edge, monolith?
4. **Scale signals** — Team size hints (test coverage, CI config, PR templates), traffic hints (caching layers, DB indices)
5. **Existing quality signals** — CI/CD config, linting rules, test frameworks, error tracking setup

This context determines which best practices apply. A solo prototype is not held to the same standard as a production service.

### 1.2 Scan Order

Read files in this order to build context efficiently:

1. `package.json` / `go.mod` / `pyproject.toml` / `Cargo.toml` — dependencies reveal patterns
2. Entry points — understand the top-level flow first
3. Core business logic — the highest-value, highest-risk code
4. Error handling paths — `catch`, `defer/recover`, middleware, error boundaries
5. Data layer — DB queries, external API calls, cache logic
6. Tests — coverage gaps reveal risk areas
7. Config / secrets management — `env`, `.env.example`, config files

> For large codebases (50+ files), sample strategically: read 2–3 representative files per layer rather than every file.

---

## Phase 2: Scoring

### 2.1 The Five Pillars

Score each pillar 1–10. Every score **must cite specific evidence** (file:line or pattern name). Avoid score inflation—a 7 means genuinely good, not "fine".

---

#### Pillar 1: Architectural Integrity

*Does the code structure make the system easy to change correctly?*

**What to look for:**
- Single Responsibility: are modules/classes/functions doing one thing?
- Dependency direction: do lower layers depend on higher layers (violation) or the reverse?
- Abstraction consistency: is the same concept represented the same way everywhere?
- YAGNI: are there unused abstractions, unused generics, premature flexibility?
- Idempotency: can operations be safely retried?

**Score calibration:**

| Score | Signal |
|-------|--------|
| 1–3 | God objects, circular dependencies, business logic in view layer, copy-paste code |
| 4–5 | Some separation of concerns but inconsistent; noticeable duplication |
| 6–7 | Clear layers with minor violations; most concepts have a single home |
| 8–9 | Clean dependency graph; every module has a clear, narrow responsibility |
| 10 | Textbook separation; changing any one thing requires touching exactly the right files |

---

#### Pillar 2: Reliability & Resiliency

*Does the system fail gracefully and recover predictably?*

**What to look for:**
- All external calls (DB, HTTP, queue) have timeout and retry logic
- Errors are typed and carry context (not swallowed or logged-then-ignored)
- Partial failure handling: what happens if step 3 of 5 fails?
- Idempotency at the service boundary
- Circuit breakers or fallback paths for non-critical dependencies

**Score calibration:**

| Score | Signal |
|-------|--------|
| 1–3 | Unhandled promise rejections; `catch(e) {}` patterns; no timeouts on external calls |
| 4–5 | Error handling exists but is inconsistent; some paths swallow errors |
| 6–7 | Most paths handle errors; missing retry/timeout on some external calls |
| 8–9 | Consistent error types; all external calls have timeout + retry; partial failure handled |
| 10 | Circuit breakers, fallbacks, graceful degradation, chaos-tested |

---

#### Pillar 3: Observability & Operability

*Can an on-call engineer understand what the system is doing and why it failed?*

**What to look for:**
- Structured logging (JSON) with consistent fields (`traceId`, `userId`, `operation`)
- Logs at the right level: DEBUG for noise, INFO for milestones, ERROR for actionable failures
- Metrics instrumentation (request count, latency histograms, error rates)
- Distributed tracing propagation
- Runbook-friendly error messages (no `"Something went wrong"`)

**Score calibration:**

| Score | Signal |
|-------|--------|
| 1–3 | `console.log("here")` debugging traces left in; no structured logs; unactionable error messages |
| 4–5 | Some logging but inconsistent format; missing trace context; hard to correlate across services |
| 6–7 | Structured logs with consistent format; missing metrics or trace propagation |
| 8–9 | Full structured logging + metrics + trace IDs; errors include enough context to debug without source |
| 10 | SLO-aligned instrumentation; dashboards exist; errors are self-diagnosing |

---

#### Pillar 4: Security & Data Integrity

*Is the attack surface minimal and is data handled safely?*

**What to look for:**
- Input validation at all trust boundaries (never trust caller data)
- Secrets management: no hardcoded credentials, env vars used correctly
- Least privilege: DB user permissions, IAM roles, API scopes
- SQL/NoSQL injection prevention (parameterized queries)
- Authentication vs. authorization checks both present
- Sensitive data in logs (PII, tokens, passwords)

**Score calibration:**

| Score | Signal |
|-------|--------|
| 1–3 | Hardcoded secrets; raw string SQL; no input validation; admin-level DB user |
| 4–5 | Parameterized queries but missing validation on some inputs; secrets in `.env` but committed |
| 6–7 | No obvious vulnerabilities; minor gaps (missing rate limiting, overly broad permissions) |
| 8–9 | Defense-in-depth; least privilege enforced; secrets in a vault; security headers set |
| 10 | Threat-modeled; automated security scanning in CI; penetration tested |

---

#### Pillar 5: Developer Experience & Cognitive Load

*Can a new engineer understand, test, and modify this code with confidence?*

**What to look for:**
- Naming: do names reveal intent? (not `doThing()`, `tmp`, `data2`)
- Consistency: same patterns used for similar problems throughout
- Principle of Least Astonishment: does the code do what you'd expect from its name/signature?
- Testability: can units be tested in isolation?
- Onboarding friction: README accuracy, local setup steps, dev tooling

**Score calibration:**

| Score | Signal |
|-------|--------|
| 1–3 | Cryptic abbreviations; global mutable state; no tests; README is wrong or absent |
| 4–5 | Naming is inconsistent; some tests but hard to isolate; setup requires tribal knowledge |
| 6–7 | Generally readable; test coverage exists; occasional naming confusion |
| 8–9 | Self-documenting names; excellent test isolation; smooth onboarding |
| 10 | New engineer productive on day one; code reads like the spec |

### 2.2 Scoring Rules

- **Cite evidence for every score.** Format: `src/api/orders.ts:42 — no timeout on fetch()`
- **Do not average adjacent scores.** Give a whole number; explain the rounding decision.
- **Flag "blockers"** — any finding that would block a production deployment (P0). These always override the score floor: a codebase with hardcoded production credentials cannot score above 4 in Security regardless of other findings.
- **Acknowledge stack context.** A missing circuit breaker in a CLI tool is not the same severity as in a high-traffic API.

---

## Phase 3: Roadmap Prioritization

Prioritize improvements using the **Impact/Effort matrix**:

| Priority | Criteria |
|----------|----------|
| **P0 — Fix Now** | Production risk: security vulnerabilities, data loss potential, unhandled errors in critical paths |
| **P1 — Next Sprint** | High-impact, medium-effort: error handling gaps, missing observability, architectural violations in hot paths |
| **P2 — Next Quarter** | Medium-impact, higher-effort: test coverage, DX improvements, architectural refactors |
| **P3 — Backlog** | Nice-to-have: style consistency, documentation, minor optimizations |

Each roadmap item must include:
- The specific problem (with file:line citation)
- The proposed solution (concrete, not "add error handling")
- The expected outcome (what metric or behavior improves)

---

## Phase 4: Quality Gate

Before writing the report, verify:

- [ ] Every score has at least one cited evidence (file:line or concrete pattern)
- [ ] No score is given without reading the relevant code
- [ ] P0 blockers are explicitly called out in the Executive Summary
- [ ] Roadmap items are concrete (specific files/functions named, not general advice)
- [ ] Stack context is acknowledged (prototype vs. production, team size)
- [ ] Output file path follows the naming convention: `docs/evaluation.[directory_name].YYYYMMDD.md`

---

## Output Template

````markdown
# Software Evaluation: [Target] — YYYY-MM-DD

> Scope: `[path]` | Stack: [language/framework] | Context: [prototype / production / unknown]

---

## Executive Summary

[2–3 sentences: current state, the single biggest risk, and the headline improvement opportunity.]

**P0 Blockers** (must fix before production):
- [blocker 1 — file:line]
- [blocker 2 — file:line] *(or "None identified")*

---

## Scorecard

| Pillar | Score | Key Finding |
|--------|-------|-------------|
| Architectural Integrity | X/10 | [one-line justification with evidence] |
| Reliability & Resiliency | X/10 | [one-line justification with evidence] |
| Observability & Operability | X/10 | [one-line justification with evidence] |
| Security & Data Integrity | X/10 | [one-line justification with evidence] |
| DX & Cognitive Load | X/10 | [one-line justification with evidence] |
| **Overall** | **X/10** | [weighted average, explain any weighting] |

---

## Deep Dive

### Architectural Integrity — X/10

**Strengths:**
- [specific pattern or file that exemplifies good design]

**Findings:**
- `src/services/user.ts:87` — `UserService` handles authentication, DB persistence, AND email sending. Violates SRP. Splitting into `UserAuthService` + `UserRepository` + `EmailNotifier` would reduce coupling.
- [finding 2 — file:line + specific recommendation]

---

### Reliability & Resiliency — X/10

**Strengths:**
- [specific evidence]

**Findings:**
- `src/lib/db.ts:23` — `query()` has no timeout. A slow DB query will hold the connection pool indefinitely. Add `statement_timeout: 5000` to the pool config.
- [finding 2]

---

### Observability & Operability — X/10

**Strengths:**
- [specific evidence]

**Findings:**
- `src/api/orders.ts:156` — `catch(err) { logger.error("order failed") }` — no `orderId`, `userId`, or stack trace in the log. Impossible to diagnose in production.

---

### Security & Data Integrity — X/10

**Strengths:**
- [specific evidence]

**Findings:**
- `src/config/db.ts:4` — `DB_PASSWORD` has a fallback hardcoded value (`|| "password123"`). Remove fallback; fail fast if env var is missing.

---

### DX & Cognitive Load — X/10

**Strengths:**
- [specific evidence]

**Findings:**
- `src/utils/helpers.ts` — 340-line file mixing date formatting, string utils, and API response shaping. No discoverability; new engineers won't find these. Split by domain.

---

## Improvement Roadmap

### P0 — Fix Now

| # | Problem | Solution | Expected Outcome |
|---|---------|----------|-----------------|
| 1 | `src/config/db.ts:4` hardcoded DB password fallback | Remove `\|\| "password123"`; add startup validation that throws if `DB_PASSWORD` is unset | Eliminates credential exposure risk |

### P1 — Next Sprint

| # | Problem | Solution | Expected Outcome |
|---|---------|----------|-----------------|
| 1 | No timeouts on external HTTP calls (`src/lib/http.ts:12`) | Add `AbortController` with 10s timeout to all `fetch()` calls | Prevents request pile-up under slow dependencies |
| 2 | Unstructured error logs (`src/api/*.ts`) | Adopt `logger.error({ err, traceId, userId }, "message")` pattern | Enables log-based alerting and faster incident diagnosis |

### P2 — Next Quarter

| # | Problem | Solution | Expected Outcome |
|---|---------|----------|-----------------|
| 1 | `UserService` violates SRP | Extract `UserRepository` and `EmailNotifier` | Enables independent testing; reduces merge conflicts |

### P3 — Backlog

| # | Problem | Solution | Expected Outcome |
|---|---------|----------|-----------------|
| 1 | `src/utils/helpers.ts` is a catch-all | Split into `src/utils/date.ts`, `src/utils/string.ts`, `src/utils/response.ts` | Improves discoverability |
````
