---
name: production-engineering
description: How to make software PRODUCTION-READY. Use for SLOs, error budgets, health checks, observability (logs/metrics/traces), alerts, feature flags, rollback, backups, disaster recovery, chaos engineering, cost monitoring, incident response.
when_to_use: |
  - SLOs, error budgets, health checks
  - observability, alerts, feature flags, rollback
  - backups, disaster recovery, chaos engineering, cost monitoring, incident response
license: MIT
metadata:
  version: "0.11"
  category: system-design
compatibility: OpenCode, Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, Windsurf, Cline
---

# Production Engineering & Reliability

Production is a different environment. Software that works locally is not production-ready.
**Design software that keeps operating correctly during failure, spikes, partial outages, and
unexpected behavior.**

## Golden principle

Assume production is hostile — everything will eventually fail, restart, timeout, slow, return
invalid data, or disappear. Design for recovery.

## Reliability hierarchy & production-first thinking

```
Correctness → Reliability → Availability → Performance → Scalability → Optimization
```

Never optimize broken software. Before any feature, answer: how is it monitored / deployed /
rolled back / tested / failed / recovered / debugged / upgraded? If any is unanswerable, it is
incomplete.

## SLOs, error budgets, health

- **SLOs:** availability, latency, error rate, RTO, RPO, capacity, cost = measurable targets.
- **Availability targets:** internal 95% · dashboard 99% · SaaS 99.9% · critical finance 99.99% ·
  infra 99.999% (higher always costs more).
- **Error budget:** failures expected — define allowed downtime/failures/latency. Never chase 100%;
  balance innovation vs stability.
- **Health checks:** readiness (accept traffic?), liveness (restart?), startup (init done?),
  dependency health (DB/Redis/search/queue/storage/APIs/LLMs/payments). Never report healthy with
  dead deps.

## Failure handling

- **Timeouts:** connection/read/write/overall on every external call. Never wait forever.
- **Retries:** only temporary failures; never retry validation/auth/authZ/business errors; exponential
  backoff. **Fail fast:** crash early, recover automatically.
- **Graceful degradation:** critical vs optional separated (recommendations down → products still
  load; analytics down → orders still complete).
- **Bulkhead / circuit breaker:** isolate workloads (AI must not impact payments); stop calling a
  failing dependency, return fallback. **Backpressure:** slow producers / queue / reject excess.
- **Rate limiting:** protect users, services, infra, 3rd-party APIs, LLMs, storage.

## Capacity, observability, ops

- **Capacity:** estimate CPU/RAM/storage/bandwidth/connections/DB/embedding/cache/queue growth;
  measure continuously.
- **Logging:** answer what/when/where/why/who + correlation ID; structured JSON; levels
  TRACE→FATAL (never log everything as ERROR).
- **Metrics:** request count, latency, CPU/mem/disk/net, queue length, retries, cache hit, DB
  queries, AI cost, model latency. **Tracing:** trace/span/correlation ID across frontend→backend→
  workers→queues→AI→payments. **Alerts:** only when human action needed (avoid fatigue).
- **Dashboards:** availability, latency, errors, traffic, infra, business KPIs, cost.
- **Feature flags:** deploy → observe → enable → measure → rollback (deploy ≠ release).
- **Rollback:** strategy, time, owner, trigger documented. **DR:** region/DB/cloud failure, accidental
  deletion, secret leak, compromised creds. **Backups:** automated, PITR, restore-tested, cross-region.
- **Chaos engineering:** simulate server/DB/queue/network/API/region failure. **Cost monitoring:**
  cloud, AI, DB, storage, bandwidth, embeddings, queues, logs, tracing — cost is an engineering metric.
- **Incident response & postmortem:** timeline, impact, root cause, detection, recovery, lessons,
  actions; fix systems, never blame individuals.

## Production checklist

- [ ] Health checks · Metrics · Logs · Tracing · Dashboards · Alerts · Feature flags
- [ ] Rollback · Backup · Restore · Capacity · Rate limits · Timeouts · Retries
- [ ] Circuit breakers · Monitoring · Incident runbook · Documentation

## Architecture decision tree

```
Shipping a feature
  ↓
Monitored / deployed / rollback defined? → NO → incomplete, fix first
External call? → timeouts + retry (temp only) + circuit breaker
Non-critical dependency down? → graceful degradation (keep critical path)
Traffic surge? → rate limit + backpressure + bulkhead isolation
Every service healthy & observable? → YES → ship behind feature flag
```

## Anti-patterns

- ❌ "Works on my machine" as a proxy for production readiness
- ❌ No health checks / reporting healthy with dead dependencies
- ❌ Waiting forever (no timeouts) or retrying permanent errors
- ❌ Chasing 100% uptime instead of using error budgets
- ❌ Alert storms that train engineers to ignore pages
- ❌ Untested backups · coupling deploy to release · treating cost as someone else's problem

## Architecture prompts

- How is this monitored, deployed, rolled back, and recovered?
- What happens when each dependency fails?
- Is there a timeout, retry, and circuit breaker on every external call?
- Can this degrade gracefully without losing the critical path?
- Is cost (cloud + AI) being measured as an engineering metric?
