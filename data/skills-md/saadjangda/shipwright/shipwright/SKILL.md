---
name: shipwright
description: "The only skill you need to build and ship world-class software — from idea to production. Covers the COMPLETE lifecycle: architecture design, domain modeling, service boundaries, data architecture, implementation with TDD, distinctive frontend design (anti-AI-slop), exhaustive QA across all layers, security hardening, scalability and load balancing, reliability engineering, performance optimization, accessibility (WCAG 2.1 AA), CI/CD, observability, and operational excellence. Applies Airbnb/Stripe/Meta-level engineering standards. Use this skill whenever: building something new ('let's build X', 'I have an idea'), designing architecture ('how should I structure this'), taking software live ('make this production ready', 'QA this', 'launch checklist'), or doing targeted work ('harden security', 'polish the UI', 'optimize performance', 'review my code'). One skill to design, build, test, polish, and ship."
---

# Shipwright

> *One skill to design it, build it, test it, polish it, and ship it.*

Shipwright covers the **complete software lifecycle** — from a rough idea to a production system built to the standards of Airbnb, Stripe, Meta, and Linear.

| User Intent | Mode | What Happens |
|---|---|---|
| "Let's build X" / new project | **BUILD** | Design → Architecture → Plan → Implement → flows into SHIP |
| "QA this" / "make this production ready" | **SHIP** | 12-phase exhaustive audit across every layer |
| "Polish the UI" / "harden security" / specific | **TARGETED** | Jump directly to the relevant phase |

---

# ━━━ BUILD MODE ━━━

# B1 — THINK: Design Before Code

<HARD-GATE>
Do NOT write any code, scaffold any project, or take any implementation action until a design is presented and the user has approved it. Every project, regardless of perceived simplicity.
</HARD-GATE>

**Explore context** — check files, docs, commits, existing code. Ask clarifying questions one at a time.

**Start with failure modes, not features.** Write down every way the system could fail — technical and business. Work backward from catastrophe.

**Define constraints explicitly** — data residency, offline requirements, legacy integrations, compliance mandates. These are load-bearing walls that shape every decision downstream.

**Propose 2-3 approaches** with clear tradeoffs. Present the design section by section and get approval before proceeding. Save to `docs/plans/YYYY-MM-DD-<topic>-design.md`.

---

# B2 — ARCHITECT: Structure the System

Read `references/architecture.md` for the complete reference. Key decisions:

**Domain Model** — Establish ubiquitous language (every term has one meaning). Identify bounded contexts. Define aggregates (transactions never span aggregate boundaries). Consider event sourcing for audit-heavy or temporal domains. Consider CQRS to separate write (correctness) from read (speed).

**Data Access Patterns First** — Write down every query you'll need. Group them. Pick storage to match patterns, not familiarity. Consider polyglot persistence: PostgreSQL for transactions, Redis for speed, Elasticsearch for search, ClickHouse for analytics, vector DBs for embeddings.

**Consistency Requirements** — Can you tolerate stale reads for 200ms? 2 seconds? Never? This determines strong vs eventual consistency.

**Service Boundaries** — Start with a modular monolith. Rigorous internal module boundaries. Extract services only when forced (independent scaling, autonomous deployment, incompatible runtime).

**API Strategy** — REST for external APIs, gRPC for internal service-to-service, GraphQL for multi-client data needs. Consider BFF (Backend for Frontend) to give each client the API it needs.

---

# B3 — PLAN: Break It Down

Break the design into tasks (2-5 minutes each). Each task: exact file paths, what code should do, verification steps, dependencies.

**Principles:** TDD (RED → GREEN → REFACTOR, non-negotiable). YAGNI (build what the design calls for). Small commits (one task = one commit). Idempotency (every mutating operation accepts an idempotency key).

---

# B4 — IMPLEMENT: Build With Craft

Work through tasks sequentially. After each: run tests, review against plan, commit. If a task reveals a design problem, pause and surface it.

**Frontend: No AI Slop.** Read `references/frontend-design.md`. Bold aesthetic direction before CSS. Never generic AI aesthetics. Every interactive element needs ALL states.

**After implementation, flow into SHIP MODE.**

---

# ━━━ SHIP MODE ━━━

*12-phase production audit. Fix everything. Test everything.*

Walk through the entire codebase, find every issue, fix it, harden every surface. Ask no more than 2-3 clarifying questions before starting.

---

# PHASE 1 — CODE HEALTH

- Remove: dead code, unused imports, orphaned components, TODO/FIXME, debugging statements, Lorem Ipsum.
- Consistent naming across files, components, functions, DB columns, API routes.
- Dependencies: all used, pinned, no critical vulnerabilities. Lockfiles committed.
- No hardcoded secrets. `git log` searched for previously committed secrets. `.gitignore` complete.
- TypeScript strict mode (or equivalent). Runtime validation at every API boundary (Zod/Pydantic/Joi).
- Build completes with zero warnings.

---

# PHASE 2 — BACKEND ARCHITECTURE & SCALABILITY

## API Design
- Consistent conventions: URL structure, HTTP methods, status codes, response shapes, error format. Versioning in place.

## Error Handling
- Centralized error middleware. No unhandled rejections. Timeouts + retry with backoff on all async ops.
- Helpful errors with reference IDs — never stack traces to users.
- Circuit breakers on external dependencies (closed → open → half-open). One slow service must never cascade.

## Database
- Normalized schema (or justified denormalization). Migrations clean from scratch.
- Indexes on queried/filtered/sorted/joined fields. Composite indexes where warranted.
- FK constraints, unique constraints, cascade deletes. N+1 queries eliminated.
- Connection pooling configured. Slow query logging (>100ms investigated). Pagination on ALL list endpoints.

## Scalability
- **Stateless app** — no in-memory sessions. Any instance handles any request.
- **Read replicas** for read-heavy workloads. **Caching** — Redis for hot data, HTTP headers for statics, query cache for aggregations. Invalidation tested.
- **Background jobs** — async processing via job queue. Retry logic, dead letter queue, idempotent jobs, queryable status.
- **Rate limiting** — per-user and per-IP, graduated. **Health checks** — `/health` and `/ready` endpoints with DB check.
- **Large datasets** — tested with 100K+ rows. UI virtualizes — never 10K+ DOM nodes.

## Data Integrity
- Transactions for multi-step ops. Failure = complete rollback. Never silent data loss.
- Concurrent access: optimistic locking (version/ETag) or pessimistic locking.
- Idempotency keys for request deduplication. Outbox pattern if event-driven.

---

# PHASE 3 — TESTING

## Unit Tests
- Business logic: happy path, edge cases, boundary values, errors. Isolated. Descriptive names. ≥80% on business logic.
- Consider property-based testing for functions with wide input ranges.

## Integration Tests
- Every endpoint through HTTP layer with real test database.
- Auth flows end-to-end. Error scenarios. Pagination with 0, 1, many results.
- Contract testing (Pact or equivalent) if multi-service: consumers define expectations, providers verify.

## End-to-End Tests
- Critical journeys in Playwright/Cypress. Run in CI on every PR. Flaky tests fixed, never ignored.

## Edge Case & Stress
- Extreme inputs: empty, 10K+ chars, `<script>`, SQL injection, unicode, emoji, RTL, zero-width, null, MAX_INT.
- Rapid interactions: double-click, concurrent calls. Large datasets (100K+). External service failure simulation.

## Visual Regression (If Applicable)
- Screenshot tests. Both themes. Key breakpoints.

---

# PHASE 4 — SECURITY

Read `references/security-hardening.md` for deep-dive with test payloads.

- **Auth:** bcrypt ≥12 / Argon2id. Reset tokens single-use, 128-bit, 15-30 min. JWT RS256/ES256, refresh rotation + family detection. Cookies HttpOnly/Secure/SameSite. Lockout after 5 fails.
- **Authorization:** Every endpoint audited. IDOR tested. Privilege escalation tested. Centralized middleware. No PII/hashes/traces in responses.
- **Injection:** SQL (parameterized, least-privilege DB user), XSS (escaped + CSP nonces), CSRF, command injection, path traversal, SSRF, XXE, ReDoS — all tested.
- **Secrets:** Not in code, env vars, or config files. Secrets manager or encrypted vault. Short-lived credentials where possible.
- **Supply chain:** Dependencies scanned against CVE databases. Container images signed if applicable.
- **Data protection:** HTTPS-only + HSTS. TLS 1.2+. Encryption at rest. No PII in logs/caches. Data classification drives access controls.
- **Headers:** CSP, HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy. Stack headers removed. CORS specific origins.
- **Infrastructure:** Rate limits on sensitive endpoints. Request size limits. Debug OFF. Admin routes locked. No `.env`/`.git` accessible. File uploads validated by magic bytes.
- **Audit logging:** Auth events, failures, rate limit hits, admin actions logged. Append-only. Zero sensitive data.

---

# PHASE 5 — FRONTEND DESIGN & UI CRAFT

Read `references/frontend-design.md` for complete guidelines.

## Design Direction
- Intentional aesthetic. NEVER generic AI aesthetics. Distinctive typography. Cohesive palette via CSS variables/design tokens.

## Light Mode
- Off-white base (never all `#FFFFFF`). Pure white cards. Near-black text (never `#000000`). Soft shadows. Subtle borders.

## Dark Mode
- Never `#000000` base. 4-5 surface levels with color tint. Off-white text (never `#FFFFFF`). Reduced accent saturation. Subtle glow sparingly. Styled scrollbars.

## Component States
- Every element: resting, hover, focus, active, disabled, loading, error, empty. No exceptions. Both themes.

## Animations
- Purposeful: page transitions (150-300ms), button feedback, skeleton loaders, modal transitions. `prefers-reduced-motion` respected.

## Visual Assets
- One icon library, consistent style. Custom 404/500 pages. Helpful empty states. Logo variants. Favicons.

## Design System
- Tokens defined once, consumed everywhere. Components encode accessibility by default. Storybook or equivalent for living docs.

---

# PHASE 6 — MOBILE RESPONSIVENESS

Read `references/mobile-responsive.md` for full checklist.

- Breakpoints: 320px → 1920px, continuous resize smooth. No overflow/overlap.
- Touch: ≥44px targets, 8px gaps. No hover-only interactions. Keyboard types match input.
- Typography ≥16px body. Images responsive, lazy-loaded, srcset. Tables: scroll/card/collapsible.
- Viewport meta set. Safe area insets. `100dvh`. No CLS. Fast first paint on 3G.

---

# PHASE 7 — ACCESSIBILITY (WCAG 2.1 AA)

- **Semantic HTML:** `<nav>`, `<main>`, `<button>`, `<a>`. One `<h1>`. Sequential headings. No `<div onClick>`.
- **Keyboard:** Full Tab nav. Visible focus both themes. Focus trapped in modals. Skip-to-content link.
- **Screen readers:** Meaningful alt. Labels on inputs. `aria-live` for dynamic content. Correct ARIA roles/states.
- **Contrast:** Text 4.5:1 (3:1 large). UI components 3:1. Never color-alone for information.

---

# PHASE 8 — PERFORMANCE

- **Bundle:** Code-split by route. Tree-shaking. Replace oversized dependencies.
- **Assets:** Images compressed, WebP/AVIF, lazy-loaded, srcset. Fonts subsetted, `font-display: swap`.
- **Core Web Vitals:** LCP < 2.5s, INP < 200ms, CLS < 0.1. Track via RUM in production.
- **Runtime:** No memory leaks. Lists virtualized at 100+ items. Expensive ops memoized. Stale-while-revalidate caching.
- **Server:** p50 < 100ms, p95 < 500ms, p99 < 1s. Queries < 50ms simple, < 200ms complex. Gzip/brotli.
- **Rendering:** Correct strategy per page: SSR for SEO, SSG for static, CSR for interactive authenticated.

---

# PHASE 9 — CI/CD & DEPLOYMENT

- **CI:** Lint + type-check + unit tests (< 2 min) + integration (< 10 min, parallel) + security scan on every PR. Build with zero warnings. Branch protection.
- **CD:** Automated deploy main → staging → production. Canary: 5% → monitor → proceed or auto-rollback. Rollback in < 5 min.
- **Environments:** Staging mirrors production. Same OS/runtime/DB version. Sanitized PII.
- **Docker (if applicable):** Pinned base images, multi-stage builds, no secrets in layers.
- **Post-deploy:** Smoke tests. Dashboards (errors, latency p50/p95/p99, DB, resources). Alerting on spikes.

---

# PHASE 10 — OBSERVABILITY

## Four Pillars
- **Metrics:** Rate, Errors, Duration (RED) per service. p99 matters more than average. Prometheus/Grafana or equivalent.
- **Logs:** Structured JSON with timestamp, severity, service, trace ID, request ID. Never PII/tokens.
- **Traces:** OpenTelemetry. Visual waterfall for bottleneck identification.
- **Profiling:** CPU/memory from production for latency spike investigation (if infra supports it).

## Reliability
- SLIs defined (quantitative health measures). SLOs set (targets). Error budgets tracked.
- Health endpoints: `/health` (alive), `/ready` (dependencies healthy).
- Incident runbooks written for: deploy failure, migration rollback, outage, security incident. Stored alongside code.

---

# PHASE 11 — WORLD-CLASS STANDARDS

- **i18n:** No hardcoded strings. Locale-aware date/number/currency formatting. UI handles 40% longer text. RTL-ready CSS.
- **SEO & GEO (if public-facing):** Read `references/seo-geo.md` for full checklist. Technical: SSR/SSG for crawlable pages, unique `<title>` + `<meta description>` per page, canonical URLs, XML sitemap, robots.txt, structured data (JSON-LD), clean URLs, internal linking, Core Web Vitals passing. Content: semantic HTML hierarchy, descriptive headings, image alt text, FAQ schema where relevant. Social: OG + Twitter Card tags with `og:image` (1200×630). GEO (Generative Engine Optimization): structured content that AI systems can cite, authoritative sourcing, FAQ/how-to schema, clear entity definitions, comprehensive topic coverage.
- **Analytics:** Funnel events (acquisition → revenue). No PII. Cookie consent. Web Vitals monitored.
- **Feature flags:** System in place. Experiments behind flags. Dead flags cleaned up.
- **Resilience:** Error boundaries (top-level + per-feature). Third-party failures isolated. Fetch timeouts + retry + fallback.
- **Chaos:** Slow 3G / offline tested. Concurrent sessions. Session expiry saves form state. Timezones/DST. Unicode edge cases.
- **Legal:** Privacy policy, ToS, cookie consent. Data deletion tested end-to-end. Dependency licenses audited.

---

# PHASE 12 — DOCUMENTATION

- **README:** Setup instructions, env vars, architecture overview, deployment. `git clone` → running in < 15 minutes. Setup scripted.
- **ADRs:** Key architecture decisions documented: context, decision, alternatives considered, tradeoffs. In the repo, versioned with code.
- **API docs:** Accurate, auto-generated from code (OpenAPI). Never hand-maintained separately.
- **Runbooks:** Deploy, rollback, migration issues, incident response. Stored in repo.
- **Architecture diagrams:** In code (Mermaid/Structurizr), updated with changes.
- **Tech debt:** Identified issues logged with location, impact, and estimated fix effort.

---

# Execution Rules

1. **Fix as you go.** Don't list problems — fix them immediately.
2. **Test after every fix.** Verify it works. Verify nothing else broke.
3. **Be surgical.** Stability, security, and polish over rewrites.
4. **Be paranoid on security.** Restrictive > permissive when in doubt.
5. **Never ship unfinished UI.** Every component, every state, every screen.
6. **Never ship AI slop.** Every design choice intentional.
7. **Prefer boring technology.** Novel only when boring genuinely can't solve the problem.
8. **Log everything.** Final report: issues found/fixed by phase, security controls, design changes, test coverage, performance metrics, CI/CD status, items needing manual action, post-launch recommendations.

---

# Reference Files

Consult `references/` for deep-dive checklists. Load on-demand:

- `references/architecture.md` — Domain modeling, service boundaries, data architecture, polyglot persistence, CQRS/event sourcing, infrastructure patterns, AI-native architecture
- `references/frontend-design.md` — Typography, color, motion, light/dark mode, spatial composition, component states, anti-patterns
- `references/security-hardening.md` — Security deep-dive with test payloads and configurations
- `references/mobile-responsive.md` — Mobile responsiveness & cross-device QA
- `references/production-readiness.md` — Granular sub-steps for every phase
- `references/seo-geo.md` — Technical SEO, content SEO, structured data, and Generative Engine Optimization
