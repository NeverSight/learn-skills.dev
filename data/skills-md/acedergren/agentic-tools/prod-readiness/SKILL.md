---
name: prod-readiness
description: "Use when assessing release readiness or running a pre-launch review. Spawns 5 specialist agents in parallel (security, testing, performance, observability, code quality) and synthesizes a prioritized report with ship/don't-ship recommendation. Keywords: production readiness, release review, pre-launch, security audit, test coverage, ship checklist."
---

# Prod-Readiness

Spawns 5 specialist review agents in parallel, each writing findings to a dedicated report file. Synthesizes into a prioritized production readiness report with executive summary, blockers, and remediation plan.

## Do NOT load when

- user wants only one narrow review (use the relevant specialist skill instead)
- codebase is mid-implementation with a knowingly broken baseline
- task is to fix issues rather than assess readiness

## NEVER

- **Never run on a dirty working tree** — uncommitted changes mean agent findings don't map to a stable commit; findings become unreproducible and the report loses traceability
- **Never run on a failing baseline** — a red test suite makes it impossible to distinguish pre-existing failures from review findings; always confirm baseline is green first
- **Never synthesize before all 5 agents finish writing** — partial synthesis produces a report that omits entire dimensions; a CRITICAL finding from a slow agent gets buried in LOW backlog
- **Never let agents write to the same file** — each agent has its own `REVIEW_*.md`; shared files produce interleaved, unparseable output
- **Never commit REVIEW_*.md files from a previous run without clearing them** — stale findings from a prior session mixed with new ones produce a misleading severity distribution
- **Never rate an issue CRITICAL without a file:line reference** — untraceable CRITICALs create review fatigue and get deprioritized the same as vague LOWs

## Pre-flight (always run before spawning agents)

```bash
git status --short          # must be clean
git log --oneline -5        # confirm recent work is committed
npx vitest run --reporter=dot 2>&1 | tail -5  # must be green
```

If tests are failing: warn the user, do not proceed until baseline is green.

## Agent specializations

**Team name**: `prod-review-<YYYYMMDD>`

Spawn all 5 in parallel via `TeamCreate` + `Task`.

| Agent | Report file | Domain |
|---|---|---|
| security-auditor | REVIEW_SECURITY.md | OWASP Top 10, RBAC gaps, input validation, secrets, auth flows, webhook security |
| test-coverage-analyst | REVIEW_TESTING.md | Uncovered critical paths, always-passing tests, missing error path tests, flaky patterns |
| performance-infra | REVIEW_PERFORMANCE.md | N+1 queries, unbounded queries, missing indexes, memory leaks, graceful shutdown, rate limiting |
| observability-analyst | REVIEW_OBSERVABILITY.md | Unhandled rejections, PII in logs, error response consistency, structured logging, health endpoint |
| code-quality | REVIEW_QUALITY.md | Dead code, circular deps, TODO/FIXME density, package boundary violations, type safety gaps |

### security-auditor prompt

```
Review this codebase for security vulnerabilities. Write ALL findings to REVIEW_SECURITY.md.

Check:
1. OWASP Top 10: injection, broken auth, IDOR, XSS, CSRF, misconfiguration
2. RBAC gaps: endpoints not protected by resolveOrgId() or permission checks
3. Input validation: user input reaching SQL without bind parameters
4. Secrets: hardcoded credentials, missing env var validation at startup
5. Dependency vulnerabilities: npm audit --json | jq '.vulnerabilities | length'
6. Auth flows: session fixation, token validation, logout behavior
7. Webhook security: HMAC validation, SSRF protection in isValidWebhookUrl()

Format findings as: [CRITICAL|HIGH|MEDIUM|LOW] Description — File:Line — Suggested fix
```

### test-coverage-analyst prompt

```
Analyze test coverage quality. Write ALL findings to REVIEW_TESTING.md.

Check:
1. Run: npx vitest run --reporter=json 2>/dev/null | jq '.testResults[].testFilePath' | wc -l
2. Critical paths with ZERO test coverage (routes, services, repositories)
3. Tests that always pass (vi.fn() calls with no assertions)
4. Missing error path tests (most routes only test happy path)
5. Flaky test patterns (time-dependent, missing afterEach cleanup)
6. Mock coverage: branches of mocked functions not tested

Format: [CRITICAL|HIGH|MEDIUM|LOW] Area — Current coverage — Risk — Suggested tests
```

### performance-infra prompt

```
Review performance and infrastructure readiness. Write ALL findings to REVIEW_PERFORMANCE.md.

Check:
1. N+1 queries (loops with SQL inside), missing indexes for frequent queries
2. Unbounded queries: SELECT without LIMIT
3. Memory: unclosed connections, event listeners without removeListener
4. Docker: resource limits in docker-compose.yml, health check configuration
5. Graceful shutdown: SIGTERM handling, connection drain
6. Rate limiting: all public endpoints covered
7. Caching: query results that could be cached

Format: [CRITICAL|HIGH|MEDIUM|LOW] Issue — File:Line — Impact — Fix
```

### observability-analyst prompt

```
Review error handling and observability completeness. Write ALL findings to REVIEW_OBSERVABILITY.md.

Check:
1. Unhandled rejections: async functions without try/catch in route handlers
2. Error boundaries: frontend error handling for route errors
3. PII in logs: user emails, tokens, or sensitive data in log statements
4. Error response consistency: all errors use the project's error hierarchy
5. Structured logging: all log calls use structured objects, not string concatenation
6. Error aggregation coverage: errors reaching the global handler vs. swallowed in try/catch
7. Health endpoint: does /health check critical dependencies (DB connection)?

Format: [CRITICAL|HIGH|MEDIUM|LOW] Issue — File:Line — Risk — Fix
```

### code-quality prompt

```
Review code quality and architecture health. Write ALL findings to REVIEW_QUALITY.md.

Check:
1. Dead code: exported functions never imported
2. Circular dependencies: run pnpm run check:circular if available
3. TODO/FIXME/HACK density: grep -rn "TODO\|FIXME\|HACK" apps/ packages/ --include="*.ts"
4. Package boundary violations: cross-app imports
5. Inconsistent patterns: code not following established conventions
6. Type safety gaps: any casts, @ts-ignore, non-null assertions (!) in production code

Format: [CRITICAL|HIGH|MEDIUM|LOW] Issue — File:Line — Debt impact — Suggested refactor
```

## Monitor agents

```bash
ls -la REVIEW_*.md   # confirm files being written
wc -l REVIEW_*.md    # track progress
```

If no file update from an agent in 2 minutes, send a check-in message.

## Synthesize

Run after all 5 `REVIEW_*.md` exist. Use `node scripts/summarize-review-reports.js` or manually synthesize into `PRODUCTION_READINESS_REPORT.md`:

```markdown
# Production Readiness Report — <date>

## Executive Summary
<1 paragraph: ship / don't ship with top 3 reasons>

## Quality Gate Results
- Tests: <pass/fail count>
- TypeScript: <clean / N errors>
- Lint: <clean / N warnings>

## Critical Blockers (fix before deploy)
## High Priority (fix within first sprint post-launch)
## Medium Priority (fix within first month)
## Low Priority / Tech Debt (backlog)
```

Each item: `**[CATEGORY] Title**` with File:Line, Risk, Effort (S/M/L), Fix.

## Final quality gate

```bash
npx vitest run --reporter=dot 2>&1 | tail -10
cd apps/api && npx tsc --noEmit 2>&1 | tail -5
npm audit --audit-level=high 2>&1 | tail -10
```

Append results to report.

## Commit and shutdown

```bash
git add REVIEW_*.md PRODUCTION_READINESS_REPORT.md
git commit -m "docs(review): production readiness report $(date +%Y-%m-%d)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

Shut down all agents, clean up team.

## Arguments

- (empty) — full review
- `--quick` — skip performance and code-quality agents, focus on security and test coverage
- `--security-only` — spawn only security-auditor
- `--no-commit` — generate reports but don't commit
