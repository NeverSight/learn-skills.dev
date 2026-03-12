---
name: engineering-senior-developer
description: "Lead complex software implementation, architecture decisions, and reliable delivery across any modern technology stack. Use when you need pragmatic architecture tradeoffs, technical plan creation from ambiguous requirements, code quality improvements, production-safe rollout strategies, observability setup, or senior engineering judgment on maintainability, testing, and operational reliability."
metadata:
  version: "1.0.0"
---

# Senior Development Guide

## Overview
This guide covers the workflow, standards, and patterns for delivering production-grade software across web, backend, mobile, and platform work. Use it when planning implementation, making architecture tradeoffs, improving code quality, or shipping safely.

## Delivery Workflow

### 1. Understand the problem
- Clarify goals, constraints, success metrics, deadlines, and non-goals. If any of these are missing, ask before writing code — never assume.
- Identify unknowns: if >2 unknowns exist, add a spike task (max 2 hours, concrete deliverable) before committing to an estimate.
- Propose a minimal viable technical approach first. If the approach requires >5 days of work, look for a simpler alternative or split into phases.
- Define acceptance criteria before implementation. Every criterion must be verifiable — "works correctly" is not a criterion; "returns 200 with JWT containing user_id claim" is.

### 2. Plan implementation
- Break work into small, testable milestones. Each milestone must be mergeable independently — if milestone B cannot ship without milestone A, they are one milestone.
- If a change touches >5 files, write a 1-paragraph plan before starting. If >15 files, write a design doc (see references/design-docs.md).
- Plan rollback: every database migration must be reversible. If a migration drops a column, first deploy code that stops reading it, then drop in the next release.
- For any new external dependency (API, service, database), define: timeout (default 5s), retry policy (3 attempts, exponential backoff), circuit breaker threshold (5 failures in 60s), and fallback behavior.

### 3. Implement and verify
- Functions >40 lines: split. Files >300 lines: split. If a function takes >4 parameters, introduce a config/options object.
- Test at the right level: pure logic = unit test. API endpoints = integration test. Critical user flows = E2E test (max 5 E2E tests per feature — they are slow and flaky).
- Every new API endpoint must have: input validation (Zod/Pydantic/class-validator), error response schema, rate limit, and at least one integration test.
- Every database query on a table with >10k rows must have an index. Run EXPLAIN ANALYZE and reject sequential scans on large tables.
- Never catch an error and swallow it silently. Log it with context (operation, input, correlation ID) or re-throw. Catch only errors you can handle.
- Backward compatibility: if changing a shared type or API response shape, grep all consumers. If >0 consumers depend on the old shape, use expand-migrate-contract (add new field, migrate consumers, remove old field).

### 4. Ship and stabilize
- Before merging: run the full test suite locally, verify no lint/type errors, check bundle size / binary size if applicable.
- Deploy with observability: every deploy must be visible in metrics within 5 minutes. If you cannot tell from a dashboard whether the deploy is healthy, add instrumentation before deploying.
- After deploy: monitor error rates and p95 latency for 30 minutes. If error rate increases >2x or p95 doubles, roll back immediately — do not debug in production first.
- Capture tech debt within 48 hours of discovering it. Each debt item must have: description, impact (latency/reliability/developer velocity), estimated effort, and owner. Unowned debt does not get fixed.

## Engineering Standards
- Every API endpoint must document: request/response schema, error codes with meanings, authentication requirement, and rate limit. If an endpoint lacks this, it is not ready for review.
- Every database migration must be tested with rollback on a copy of production data (or realistic seed data) before merging. Migrations that take >30s on production-size data must be run as background jobs, not blocking deploys.
- Every critical path (auth, payment, core CRUD) must have: latency histogram, error rate counter, and an alert that fires when p95 exceeds 2x the baseline or error rate exceeds 1%.
- Security is not a follow-up task. Auth checks, input validation, and CSRF protection are part of the initial implementation. If a PR adds an endpoint without auth, it is not ready for review.
- Performance budgets: API response p95 <200ms for reads, <500ms for writes. If a new feature exceeds these, optimize before merging — not after.

## Anti-Pattern Detection
When reviewing or writing code, flag and fix these immediately:
- **N+1 queries:** Loop that makes a database call per iteration. Fix with batch query, JOIN, or DataLoader.
- **Unbounded queries:** `SELECT *` or query without LIMIT on a user-facing endpoint. Always paginate, always select only needed columns.
- **Shared mutable state:** Global variable modified by multiple request handlers. Use request-scoped context or dependency injection.
- **Stringly-typed code:** Using raw strings for status, type, or role values. Use enums or union types.
- **God function:** Function that handles parsing, validation, business logic, database, and response formatting. Split into layers.
- **Missing error context:** `catch (e) { throw new Error("failed") }`. Always include the original error and operation context.
- **Premature abstraction:** Creating a generic framework for something used in one place. Wait until the pattern repeats 3 times.
- **Config in code:** Hardcoded URLs, API keys, feature flags, or environment-specific values. Move to environment variables or config service.

## Technology Selection Decision Rules

### Language Selection
- **Go**: Choose when the service is I/O-bound with high concurrency (>10k concurrent connections), needs single-binary deployment, or is infrastructure tooling (CLI, proxy, sidecar). Avoid for rapid prototyping or heavy ORM usage.
- **Node.js (TypeScript)**: Choose when the team is full-stack JS, the service is a BFF (Backend for Frontend), real-time features dominate (WebSocket, SSE), or the ecosystem has a mature library for the domain. Avoid for CPU-bound processing (image/video, ML inference).
- **Python**: Choose when the domain is data/ML, the team is Python-native, or rapid iteration matters more than runtime performance. Avoid for latency-sensitive services (<10ms p95 target) unless using FastAPI with uvloop.
- **Java/Kotlin**: Choose when the organization has JVM expertise, needs mature enterprise libraries (Spring, Hibernate), or requires strong typing with high throughput. Avoid for small services where JVM startup time (2-5s) exceeds acceptable cold start.
- **Rust**: Choose only when the service has hard latency requirements (<1ms p99), processes untrusted input at scale, or is a performance-critical library. The 2-3x development time multiplier must be justified by a specific, measured need.

### Database Selection (Quick Reference)
- **PostgreSQL** (default): Use for any relational data <10TB. Supports JSON, full-text search, and geospatial — eliminate the need for a second database when possible.
- **Redis**: Use for caching (TTL <24h), session storage, rate limiting, or real-time leaderboards. Never as primary data store — data loss on restart is expected.
- **MongoDB**: Use only when schema genuinely varies per document (CMS, event stores with polymorphic payloads). If you can define a schema upfront, use PostgreSQL.
- **SQLite**: Use for CLI tools, mobile apps, embedded systems, or local-first apps. If >1 process writes concurrently, use PostgreSQL.

### API Style Selection
- **REST**: Default choice. Use for CRUD-dominant APIs, public APIs, or when caching matters (HTTP caching works natively).
- **GraphQL**: Use only when the client needs flexible field selection across >5 entity types AND the frontend team controls the schema. If <3 entity types, REST is simpler. Never use GraphQL for server-to-server communication.
- **gRPC**: Use for internal service-to-service communication when latency <5ms matters, streaming is required, or strong contract enforcement across >3 languages is needed. Never expose gRPC directly to browsers without a gateway.
- **tRPC**: Use when frontend and backend share a TypeScript monorepo. Gives end-to-end type safety with zero schema duplication. Not suitable for multi-language backends.

## Estimation Decision Rules

### Task Estimation by Type
- **CRUD endpoint** (route + validation + DB query + tests): 2-4 hours. If it needs pagination, filtering, and sorting: add 2 hours.
- **CRUD endpoint with auth + rate limiting + caching**: 1 day.
- **Third-party API integration** (OAuth, webhook, SDK): 1-2 days. Always double the estimate if the third-party documentation is poor — verify by reading it before estimating.
- **Database migration** (add column, add index): 1-2 hours if table <1M rows. If >1M rows, add 4 hours for online migration tooling and testing.
- **Database migration** (schema redesign, data backfill): 2-3 days including dual-write period and verification.
- **New service from scratch** (repo + CI/CD + health checks + first endpoint + monitoring): 3-5 days.
- **Authentication system** (signup + login + password reset + session management): 3-5 days with a proven library (NextAuth, Passport, Django auth). 2-3 weeks if building custom — strongly discourage.
- **File upload/download** (presigned URLs + validation + storage): 1-2 days.
- **Real-time feature** (WebSocket/SSE + connection management + reconnection): 2-3 days.
- **Search** (full-text across >3 fields with filtering): 1 day with PostgreSQL tsvector, 2-3 days with Elasticsearch.

### Estimation Multipliers
- First time using a library/framework: 2x the estimate.
- Legacy codebase with no tests: 1.5x (you must write tests to verify your change).
- Multi-timezone or i18n requirement: 1.3x.
- Compliance requirement (audit logging, encryption, access controls): 1.5x.
- If the estimate exceeds 5 days, break into sub-tasks and estimate each. If any sub-task exceeds 3 days, it is too large — break further.

## Refactoring Decision Rules

### When to Refactor
- **Cyclomatic complexity >15** (measure with `scripts/review_checklist.py` or ESLint `complexity` rule): Extract branches into named functions. Each function should have complexity <10.
- **Function called from >5 call sites with different flag combinations**: Replace boolean flags with strategy pattern or separate functions. `processOrder(order, true, false, true)` is unreadable — split into `processStandardOrder()`, `processExpressOrder()`.
- **Identical code block appears 3+ times**: Extract to a shared function. At 2 occurrences, tolerate duplication — premature abstraction is worse than duplication.
- **Module has >10 imports from other modules**: High coupling. Introduce a facade or reorganize module boundaries so each module imports from at most 5 others.
- **Test requires >20 lines of setup**: The code under test has too many dependencies. Inject dependencies and provide test doubles. If you cannot test a function without starting a database, the function does too much.
- **Changing one feature requires modifying >5 files across >2 directories**: Shotgun surgery. Consolidate related logic into a single module or introduce a feature module pattern.

### When NOT to Refactor
- Code is stable, untouched for >6 months, and has no pending feature work. Leave it alone.
- You are refactoring to match a style preference, not to fix a measurable problem (complexity, coupling, test difficulty). Stop.
- The refactor would require >3 days and there is no feature work that benefits from it. Defer and document as tech debt.

## Code Review Decision Rules

### By Pattern Detected
- **New database query without EXPLAIN ANALYZE output**: Request it. No query merges without execution plan on production-like data volume.
- **New endpoint without error response test**: Block. Every endpoint must be tested with: valid input (200), missing auth (401), forbidden (403), and invalid input (400).
- **Catch block that logs and continues**: Verify the function can actually recover. If it cannot, re-throw. Catching + logging + continuing hides bugs until they cascade.
- **Function with >3 levels of nesting**: Request extraction of inner blocks into named functions. Deep nesting signals logic that should be inverted (early returns) or decomposed.
- **Magic numbers/strings**: Request named constants. `if (retries > 3)` → `if (retries > MAX_RETRIES)`. Exception: 0, 1, and common HTTP status codes (200, 404, 500).
- **TODO/FIXME without issue link**: Block. Every TODO must reference a ticket. Untracked TODOs never get fixed and rot.
- **Test that asserts only `toBeTruthy()` or `not.toThrow()`**: Weak assertion. Request specific value assertions. A test that passes when the output is wrong is worse than no test.
- **New dependency added**: Check: bundle size impact (run `bundlesize` or equivalent), last commit date, download count, license compatibility, and whether a stdlib solution exists. Block if the dependency adds >50KB to the bundle for a feature that could be built in <2 hours.

## Architecture Guidance
- If the team is <5 engineers, use a monolith. If 5-15, use a modular monolith with clear domain modules. If >15 with independent release cycles, consider service extraction.
- Keep boundaries explicit between domain logic, data access, and transport layers. If domain logic imports HTTP request types or database client types, the boundary is violated.
- When adding a new dependency (library, service, or tool): check last commit date (reject if >12 months inactive), weekly downloads (reject if <1k for JS, <500 for Python), and open security advisories.
- Use feature flags for changes that affect >1000 users or involve new infrastructure. Roll out to 1% → 10% → 50% → 100% with 24-hour soak at each stage.
- Record architecture decisions (ADRs) for: new external dependencies, database schema changes, API contract changes, infrastructure changes, and technology choices. An ADR that takes >10 minutes to write is too long.

## Self-Verification Protocol
After completing any implementation, run this checklist before considering the task done:
- Run the full test suite. Zero failures. If a test you did not touch fails, verify it also fails on main — if it does not, your change broke it.
- For every new API endpoint, make a real HTTP request (curl or integration test) and verify the response matches the documented schema field-by-field.
- For every database migration, run forward AND rollback on a fresh database and on production-like seed data. Both directions must succeed.
- After refactoring, diff test outputs before/after. If any behavior changed unintentionally, the refactor introduced a bug — revert and redo.
- Run `scripts/review_checklist.py` on every modified file. Fix all findings before requesting review.
- Check that no `console.log`, `print()`, `debugger`, or `TODO` statements remain in production code paths.
- Verify that every new dependency passes the health check: last commit <12 months, downloads >1k/week (JS) or >500/week (Python), zero open critical CVEs.
- If the change affects a user-facing flow, manually walk through it end-to-end in the browser/app. Automation catches regressions — manual testing catches UX issues.

## Failure Recovery
- **Build fails after your change**: Read the full error — not just the last line. If it is a type error, fix it. If it is a test failure in code you did not touch, run `git stash && npm test` to verify it fails on main too. If it does, pre-existing; if not, your change broke it.
- **Test passes locally, fails in CI**: Check environment differences — Node/Python version, missing env vars, timezone, OS case sensitivity, or Docker vs host filesystem. Never `skip` a CI test — fix the root cause.
- **Approach not working after 2 hours**: Stop. Write: (1) what you tried, (2) why it failed, (3) what assumption was wrong. Identify the simplest alternative. If none exists, escalate with a concrete blocker description.
- **Performance regression after deploy**: Roll back first, investigate second. Reproduce locally with profiling (see references/performance-profiling.md). Never debug performance in production while users are affected.
- **Merge conflict on large PR**: If >5 files conflict, do not resolve blindly. Re-read both sides of every conflict. If the other branch changed the same function, test both behaviors after resolution.
- **Dependency upgrade breaks things**: Pin the working version, file an issue with exact error, move on. Do not spend >1 hour on a third-party regression.
- **Flaky test blocking merge**: Run it 5 times locally. If it fails inconsistently, it has a race condition or timing dependency. Fix the test (add proper waits, mock time, remove shared state) — never retry-until-pass.

## Existing Codebase Orientation
When dropped into an unfamiliar codebase, complete this sequence before writing any code:
1. **Read README and config files** (5 min) — Identify language, framework, build/test/deploy commands, and entry points.
2. **Run the app locally** (10 min) — If it fails, fixing the dev setup is task zero. Nothing else matters until the app runs.
3. **Run the test suite** (5 min) — Note: total tests, duration, failures. Failing tests on main are a red flag to document.
4. **Trace the critical path** (15 min) — Pick the core user action. Trace from HTTP handler → business logic → database → response. Note file and function at each step.
5. **Map architecture layers** (10 min) — Entry points (routes/controllers), business logic, data access, external services. Note where boundaries are clean vs tangled.
6. **Check dependency health** (5 min) — `npm outdated` / `pip list --outdated`. Flag anything >2 major versions behind.
7. **Read last 20 commits** (5 min) — Understand active work areas and commit conventions.
8. **Identify test gaps** (5 min) — What types exist (unit/integration/E2E)? Where are the blind spots?

Only after this orientation should you plan your change. This 1-hour investment prevents breaking things you did not know existed.

## Scripts

- `scripts/review_checklist.py` -- Analyze a source file for common code review concerns: TODO/FIXME count, long functions, bare excepts, hardcoded secrets, leftover debug statements. Run with `--help` for options.

## References

- [Code Examples](references/code-examples.md) — TypeScript API handler, Python retry wrapper, migration-safe SQL, and CI quality gate.
- [Design Docs & ADRs](references/design-docs.md) — Design document template (filled-in payment processing example), Architecture Decision Record example, and lightweight RFC template.
- [Production Patterns](references/production-patterns.md) — Feature flags with percentage rollout, graceful shutdown, expand-migrate-contract database migrations, structured logging with correlation IDs, circuit breaker, and retry with exponential backoff. All TypeScript.
- [Code Review & Incident Response](references/code-review.md) — Code review checklist, incident response runbook, post-mortem template, and on-call handoff template.
- [Performance Profiling](references/performance-profiling.md) — Node.js profiling with clinic.js and Chrome DevTools, EXPLAIN ANALYZE workflow, pg_stat_statements top queries, N+1 detection, memory leak investigation (3-snapshot heap diff), CPU profiling with worker threads, and a full worked example from "endpoint is slow" to root cause fix.
- [Debugging Strategies](references/debugging-strategies.md) — Git bisect with automated test scripts, structured log correlation across services, HTTP traffic capture and replay, seed-based reproducible test data, race condition debugging with timestamp analysis and lock contention queries, production debug endpoints, verbose logging feature flags, canary deployments, and common bug pattern signatures.
- [Architecture Decisions](references/architecture-decisions.md) — Concrete decision matrices with scoring and thresholds for monolith vs microservices, database selection (PostgreSQL vs MySQL vs MongoDB vs DynamoDB vs Redis), queue selection (SQS vs RabbitMQ vs Kafka), caching strategy with hit rate thresholds and stampede prevention, API style (REST vs GraphQL vs gRPC), and auth strategy (sessions vs JWT vs OAuth2) with security checklists.
- [Team Patterns](references/team-patterns.md) — PR review turnaround SLA by PR size, review comment categories (must-fix/suggestion/learning/praise), tech debt register with severity scoring, on-call runbook template with triage decision tree, story point calibration with reference stories, velocity tracking formulas, brown bag and decision log templates, mentoring framework with pairing progression, and dependency upgrade strategy with Renovate config.
