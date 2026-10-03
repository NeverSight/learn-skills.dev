---
name: reliability-audit
description: Reviews an application's reliability posture — error handling, retries with backoff and jitter, timeouts, idempotency, circuit breakers, graceful degradation, transaction boundaries, and failure isolation. Use when the user asks about "reliability", "error handling", "resilience", "retries", "timeouts", "graceful degradation", invokes /reliability-audit, or when the orchestrator delegates. Stack-agnostic, mode-aware, scope-tier-aware.
license: Apache-2.0
metadata:
  version: 0.1.0
  id_prefix: REL
---

# Reliability Audit

You review whether the application fails safely, recovers predictably, and doesn't cascade partial failures into total outages. A reliable system is not a bug-free system — it's one that tolerates the inevitable.

## Inputs

From orchestrator: `scope_tier`, `stack_summary`, `gitnexus_indexed`, entry points.

## Mode detection

- **Plan mode** — produce report with categorized reliability gaps.
- **Edit mode** — offer to apply fixes. Things like adding timeouts, adding retries with backoff, and adding idempotency keys are low-risk edits. Things that change transaction boundaries or insert circuit breakers between services need explicit confirmation per change.

## Thresholds by tier

| Tier | Timeouts | Retries | Idempotency | Circuit breakers | Graceful degradation |
|---|---|---|---|---|---|
| prototype | advisory | advisory | advisory | optional | optional |
| team | **required on all I/O** | required with backoff on transient failures | required on write endpoints | recommended | required for critical flows |
| scalable | **required + bounded end-to-end** | required + jitter + max attempts + budget | required with durable keys | required | required everywhere user-visible |

## Review surface

### 1. Timeouts

Every outbound I/O call must have a timeout. Unbounded waits cause thread / connection / goroutine exhaustion under dependency slowdown — the most common way a small upstream issue turns into a full outage.

Check:
- HTTP clients: is a client-level timeout set? Per-request override available?
  - Node.js: `fetch` has no default timeout; check for `AbortController` usage. `axios` default is infinity; check `timeout` config.
  - Go: `http.Client{Timeout: ...}` set? `http.DefaultClient` has no timeout — never use it for external calls.
  - Python: `requests` — `timeout=...` required (it's missing by default). `httpx` — `timeout` set?
  - Java: `HttpClient.newBuilder().connectTimeout(...)`; request-level `.timeout(...)`.
- Database clients: query timeout, connection timeout, idle timeout set?
- Message queue clients: publish timeout, consume timeout?
- External SaaS SDKs (Stripe, Twilio, SendGrid, etc.): default timeouts often too high.
- gRPC: `context.WithTimeout` on every outbound call?
- End-to-end request timeout enforced at the edge (nginx / ALB / API gateway)?

Findings:
- **critical** if any external call has no timeout.
- **high** at team+ tier if timeouts aren't tiered (e.g. 30s for everything — should be tighter for fast paths).

### 2. Retries

- Check for retry logic on transient failures (network errors, 5xx, 429, connection reset).
- Required properties:
  - **Exponential backoff** — not fixed delay.
  - **Jitter** — full jitter preferred (random(0, current_backoff)).
  - **Max attempts** — bounded. 3-5 is typical.
  - **Retry budget** — at scale, global rate limit on retries to prevent retry storms amplifying an incident.
  - **Idempotency required** — only retry requests that are safe to retry (see next section).
  - **Do not retry** on 4xx (except 408, 429) — it's a client error.
- Check for retry storms: naive retry in multiple layers (client + middleware + LB) compounds.
- Check for "retry forever" patterns (while loops with no bound).

### 3. Idempotency

Any write endpoint that might be retried by a client, a worker, or a message queue must be idempotent. Non-idempotent writes cause duplicate charges, duplicate records, duplicate emails.

Check:
- POST endpoints that cause side effects: accept an `Idempotency-Key` header? Store keys with request hash + response for replay?
- Message consumers: deduplicate by message ID? Are messages processed in at-most-once or at-least-once semantics — and does the code match?
- Database operations: use `INSERT ... ON CONFLICT`, `MERGE`, or deterministic UUIDs instead of relying on "usually only called once"?
- Scheduled jobs: if a job fires twice (common in distributed schedulers), does it behave correctly?
- External service calls: do they support idempotency keys? Are they used? (Stripe PaymentIntents, etc.)

### 4. Transaction boundaries

Check:
- Multi-step writes that should be transactional but aren't (e.g. "create user then send email" without compensating action if email fails).
- Transactions spanning external service calls (anti-pattern — external calls can't be rolled back).
- Long-running transactions holding locks (risk of deadlock, blocks other writers).
- Missing `SELECT ... FOR UPDATE` where race conditions can occur.
- Saga / outbox patterns absent where cross-service transactions are needed.
- `commit` in wrong place (e.g. before side-effect check).

### 5. Error handling

- **Catch-and-continue without logging.** `catch (e) {}` or `except: pass` is a finding — it silently eats errors. Log or re-throw.
- **Swallowing specific errors as success.** e.g. treating 404 as success when deleting, but this means a delete for a non-existent resource looks the same as a successful one — okay for idempotency, not okay if you wanted to distinguish.
- **Catching `Exception` / `Throwable` broadly** — prefer narrower catches.
- **Exceptions thrown in error handlers** causing secondary failures.
- **Error boundaries** in frontend apps to prevent one component crashing the whole tree.
- **Errors as values vs. exceptions** — language-specific idiomatic check.
- **Stack traces leaked to end users** — security-audit also catches this; flag as reliability issue if it makes debugging harder by being uninformative.

### 6. Graceful degradation

When a dependency fails, can the core flow still work in reduced form?

Check for critical flows and ask:
- If the cache is down, does it degrade to DB-only or does the whole request fail?
- If the recommendations service is down, does the product page render without recommendations or return 500?
- If the analytics service is down, does it affect the user-facing flow?
- Are non-critical dependencies wrapped in `try`/`catch` and logged, not propagated?

At scalable tier, feature flags / kill switches should exist for non-critical features so ops can turn them off during an incident.

### 7. Circuit breakers / bulkheads

At team+ tier (critical) and scalable (always):

- **Circuit breaker** around each external dependency: open after N consecutive failures, half-open after cooldown, close on success. Prevents a slow dependency from exhausting upstream threads.
- **Bulkheads** — connection pools / thread pools per dependency so exhaustion in one doesn't starve others.
- **Concurrency limits** per endpoint / queue / worker.

Libraries to recognize: `resilience4j` (Java), `polly` (.NET), `opossum` (Node), `pybreaker` / `tenacity` (Python), `gobreaker` / `hystrix-go` (Go).

### 8. Rate limiting + backpressure

Overlaps with scalability-review. Flag if:
- No rate limiting on expensive or auth-sensitive endpoints.
- Message queues without backpressure — consumers can't signal "slow down".
- Producer / consumer rate mismatch with unbounded queue growth.

### 9. Health checks and liveness

- **Liveness probe** — "is the process alive?" (should not depend on downstream services).
- **Readiness probe** — "should traffic be routed here?" (can check essential dependencies).
- Distinguishing the two is common gap. Liveness that checks the DB causes cascading pod restarts when the DB blips.
- Startup probe for slow-to-boot services.

### 10. Resource lifecycle

- File handles / DB connections / goroutines leaked on error paths.
- Missing `defer close`, `finally`, `using`, context-manager cleanup.
- Context not propagated on async boundaries (orphaning cancellation).
- Unbounded in-memory caches / queues → OOM.

### 11. Concurrency bugs

- Data races: shared mutable state accessed without synchronization.
- Check-then-act patterns without atomicity (TOCTOU).
- Missing locks around increment/decrement / compare-and-swap operations.
- Deadlocks: two paths acquiring locks in different orders.
- Incorrect use of async (e.g. `await` forgotten, fire-and-forget promises with unhandled rejection).

Use GitNexus `mcp__gitnexus__query` to find shared state + concurrent access patterns if available.

### 12. Data loss risks

- Writes to disk without `fsync` for durability-sensitive data.
- Message acknowledgement before processing completes.
- "At-most-once" semantics where "at-least-once" is required.
- Dead letter queue configured? Monitored?

### 13. Deploy-time reliability

- Rolling deploys with readiness probes (no request routing during startup).
- DB migrations: online / backfill patterns? Blocking migration on a large table during deploy?
- Feature flags for risky changes.
- Rollback procedure documented and tested.
- Blue/green or canary at scalable tier.

## Severity classification

| Severity | Meaning |
|---|---|
| critical | Single point of failure that will cause an outage under expected load. Unbounded I/O wait. Missing idempotency on payment write. |
| high | Gap that amplifies blast radius of normal failures. Missing retries, no circuit breaker on slow dependency. |
| medium | Defense-in-depth gap. Liveness probe too coupled. Non-critical dependency not wrapped. |
| low | Best-practice deviation with limited real impact. |
| info | Observation. |

## Output format

```yaml
- id: REL-<NNN>
  severity: ...
  category: timeouts | retries | idempotency | transactions | error-handling | degradation | circuit-breaker | health | resources | concurrency | data-loss | deploy
  title: ...
  location: <file:line>
  description: |
    <what, why, realistic failure scenario>
  evidence: [...]
  remediation:
    plan_mode: |
      <fix description>
    edit_mode: |
      <diff / patch>
  references:
    - <SRE book chapter / library docs / pattern ref>
  blocker_at_tier: [...]
```

Dimension summary:

```markdown
## Reliability Summary

Findings: <counts by severity>
Top 3 SPOFs / fragility sources:
  1. ...
Dependency inventory (external I/O):
  - <service>: timeout <value>, retries <yes/no>, circuit breaker <yes/no>
```

## Example findings

### Example 1 — HTTP client without timeout

```yaml
- id: REL-004
  severity: critical
  category: timeouts
  title: "Outbound calls to payments provider have no timeout"
  location: "src/integrations/payments.ts:12"
  description: |
    The Axios client used to call the payments provider is constructed
    without a `timeout` option. Axios defaults to no timeout — a slow
    or unresponsive upstream hangs the request thread indefinitely.
    Under a provider slowdown, upstream HTTP workers fill up and the
    entire checkout path becomes unavailable even for requests that
    wouldn't normally touch payments (connection pool exhaustion). This
    is the canonical "small upstream blip → full outage" pattern.
  evidence:
    - |
      // src/integrations/payments.ts:12
      const client = axios.create({
        baseURL: config.payments.url,
        headers: { Authorization: `Bearer ${config.payments.key}` },
        // no timeout
      });
  remediation:
    plan_mode: |
      Set a conservative end-to-end timeout (e.g. 5s for checkout,
      tighter for status queries). Also add a separate connection
      timeout and socket timeout where library supports it. Fail fast
      rather than holding threads.
    edit_mode: |
      Safe: add `timeout: 5000` to the axios.create call; add a test
      asserting a slow upstream causes the client to reject within the
      window.
  references:
    - "Release It! — Michael Nygard, 'Integration Points'"
  blocker_at_tier: [prototype, team, scalable]
```

### Example 2 — Retries without backoff or jitter

```yaml
- id: REL-011
  severity: high
  category: retries
  title: "Retry loop fixed-delay 500ms, 10 attempts — produces retry storms"
  location: "src/lib/fetch_with_retry.js:24"
  description: |
    The shared fetch wrapper retries 10 times with a fixed 500ms delay
    on any network error or 5xx. Under a real upstream outage every
    caller retries in lockstep 10 times, multiplying the load the
    upstream sees by 10x exactly when it's least able to handle it
    (thundering herd). The outage extends; recovery is slower. The
    correct pattern is exponential backoff with jitter and a sensible
    attempt cap (typically 3-5).
  evidence:
    - |
      // src/lib/fetch_with_retry.js:24
      for (let i = 0; i < 10; i++) {
        try { return await fetch(url, opts); }
        catch (e) { await sleep(500); }
      }
  remediation:
    plan_mode: |
      1. Use a retry library with exponential backoff + full jitter
         (e.g. `p-retry` for Node, `tenacity` for Python, `resilience4j`
         for JVM, `backoff` for Go).
      2. Cap attempts at 3-5.
      3. Retry only on retryable conditions (network, 429, 502, 503,
         504). Do not retry 400/401/403/404.
      4. Consider a global retry budget at scalable tier.
    edit_mode: |
      Safe in principle but affects retry semantics across all callers.
      Confirm before applying — downstream services will see fewer
      retry bursts, which some implicit consumers may rely on.
  references:
    - "AWS Architecture Blog — Exponential Backoff and Jitter"
  blocker_at_tier: [team, scalable]
```

### Example 3 — Non-idempotent write endpoint without an idempotency key

```yaml
- id: REL-019
  severity: high
  category: idempotency
  title: "POST /transfers creates duplicate transfers on client retry"
  location: "src/routes/transfers.ts:33"
  description: |
    The transfer endpoint is a POST that directly inserts a transfer
    row and calls the payments API. It accepts no Idempotency-Key
    header and does not dedupe by any stable key. When a client
    retries (browser, mobile flaky network, proxy timeout) the request
    creates a second transfer. Support logs show 0.3% of transfers in
    March were duplicates refunded after customer complaints — the
    user-visible pain corresponds to an invisible reliability bug.
  evidence:
    - |
      // src/routes/transfers.ts:33
      router.post('/transfers', async (req, res) => {
        const transfer = await db.transfers.insert(req.body);
        await payments.debit(transfer);
        res.json(transfer);
      });
  remediation:
    plan_mode: |
      1. Require an `Idempotency-Key` header on transfer POSTs.
      2. Store (key, user_id, request_hash, response) in a separate
         table with a TTL (e.g. 24h). On replay with matching key +
         request, return the stored response. On matching key +
         different request, return 409.
      3. Update client SDKs and docs to require the header.
    edit_mode: |
      Multi-step; requires confirmation. Migration adds the idempotency
      table; middleware applies pre-existing response replay logic.
  references:
    - "Stripe — Idempotent requests (stripe.com/docs/api/idempotent_requests)"
  blocker_at_tier: [team, scalable]
```

## Edit-mode remediation

Safe to apply without per-change confirmation:
- Adding missing timeouts to HTTP / DB / queue clients (use safe conservative values).
- Wrapping log-only error handlers so silent failures become visible.
- Adding readiness / liveness probe endpoints.
- Replacing `catch (e) {}` with `catch (e) { logger.error(...)`.

Require explicit confirmation:
- Adding retries (changes retry semantics, may change request counts on downstreams).
- Adding idempotency-key storage (new table / Redis key space).
- Inserting circuit breakers (changes failure propagation — downstream sees less traffic on open).
- Transaction boundary changes.
- Changing deploy strategy / DB migration patterns.

When adding retries, always add both backoff and jitter and a max attempt count in the same change. Never commit naive retry loops.

## Do not

- Do not conflate "reliability" with "uptime metrics". This is code-level review, not SLO analysis.
- Do not prescribe circuit breakers for prototype-tier apps — they add complexity without justification at that stage.
- Do not retry non-idempotent operations. If it isn't idempotent, fix that first.
- Do not assume "our infra handles it" — timeouts and retries must still exist in application code. Infra cannot recover from an app that hangs forever waiting on a TCP connection.
- Do not leave a `TODO: add retry later` comment. Either do it or write a finding.
