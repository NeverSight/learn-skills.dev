---
name: architecture-review
description: Mandatory PRE-MERGE architecture review. Use before approving or merging any code — run the review dimensions and merge scorecard to challenge design, catch coupling/security/scalability/cost issues, and verify production readiness.
when_to_use: |
  - about to approve or merge code
  - challenging a design before implementation
  - running the merge scorecard / architecture review dimensions
license: MIT
metadata:
  version: "0.11"
  category: system-design
compatibility: OpenCode, Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, Windsurf, Cline
---

# Architecture Review Engine

The mandatory review that runs before, during, and after implementation. Writing code is easy;
removing bad architecture is expensive. Every implementation must survive this review. A Principal
Engineer asks *"Should this exist?"* — not just *"Can I build it?"*

## Primary rule & thinking loop

**Never approve your own first idea.** Generate Option A → B → C, compare, choose. Never stop at
the first working solution.

```
Understand → Question → Challenge → Simplify → Validate → Implement → Review → Improve
```

Repeat until complexity cannot be reduced.

## Review dimensions (run before merge)

- **Requirements:** clearly defined? measurable? assumptions documented? scope reducible /
  postponeable / already solved / actually needed?
- **Domain:** which capability & domain owns it? duplicated? ownership ambiguous? vocabulary improved?
- **Architecture:** tighter coupling? hidden/circular deps? global/shared mutable state? god objects?
  Should get *simpler*.
- **Data:** single owner? duplicated ownership? normalize/denormalize? transactions? history? audits?
  indexes? growth (data survives code).
- **API:** business capability (not DB structure)? async/event? immediate? pagination/filter/version/
  idempotency?
- **Security:** authN, authZ, tenant isolation, rate limit, input/output validation, prompt & SQL
  injection, secrets, encryption, audit logs, least privilege — every answer explicit.
- **AI:** needs AI at all? deterministic alternative? retrieval first? tool used? memory stored?
  context reduced? prompts cached? outputs verified? *Best AI call is often no AI call.*
- **Performance:** expected latency/throughput? largest payload? slowest op? async/stream/batch/cache?
- **Scalability:** what breaks first (DB/mem/bandwidth/CPU/queue/storage/network/AI)? scale & fail
  independently?
- **Cost:** infra, per-request AI, storage/embedding growth, bandwidth, logging/tracing — does
  doubling users double cost? Can cost be bounded?
- **Operations:** deployed/monitored/rolled back/upgraded/debugged/restored? Another engineer can fix
  tonight?
- **Testability:** unit/integration/contract/load/security/chaos? deps mockable? (hard-to-test = poor
  design).
- **Maintainability:** new engineer/AI understand it? naming communicates intent? modules shrinkable?
- **Change blast radius:** if this changes, how many modules/services/DBs/APIs/teams change? (high =
  poor boundaries).
- **Failure:** DB/Redis/queue/search/LLM/payment/cloud fails → degrade gracefully?
- **Observability:** logs/metrics/traces/events/alerts/dashboards? failures diagnosable remotely?
- **Dependency:** exists already? maintained? security history? migration & exit strategy? (every dep
  is a long-term responsibility).
- **Refactor:** module shrink? responsibilities separate? interfaces simplify? duplication reduce?
  Prefer deleting code over adding abstractions.
- **Simplicity:** explainable in five minutes? If not, too complex.

## Staff & principal questions

- **Staff:** Would Stripe build this way? Linear ship it? Shopify approve? Vercel simplify? Netflix
  isolate? Survive 10× traffic? Think from principles, not imitation.
- **Principal:** If I leave tomorrow, will it survive? Can another engineer/AI own & continue it?
  Reduces future complexity? Makes sense in two years? Architecture is measured in years, not PRs.

## Merge scorecard

Score 0–10: Architecture · Security · Performance · Reliability · Maintainability · Scalability ·
Cost · Observability · Documentation · Testing. **Only merge when every critical category meets the
team's quality bar.**

## Final review

Before marking complete: can anything be deleted / simplified? responsibilities clearer? another
engineer/AI understand it faster? operational burden / cost / risk / coupling decrease? If yes, keep
improving.

## Architecture decision tree

```
About to implement / merge
  ↓
Generate ≥3 options (A/B/C) → choose best, never first idea
  ↓
Run review dimensions (requirements → domain → architecture → data → API → security
  → AI → perf → scale → cost → ops → test → maintain → change → failure → observability
  → dependency → refactor → simplicity)
  ↓
Any critical category below the bar? → YES → challenge & simplify, then re-review
  ↓ NO → merge
```

## Anti-patterns

- ❌ Approving your own first idea without alternatives
- ❌ Skipping the review engine for "simple" changes
- ❌ Treating the merge scorecard as a formality
- ❌ Implementing vague, unmeasured requirements
- ❌ Adding a dependency without an exit strategy
- ❌ Shipping without observability because "it works locally"

## Architecture prompts

- Should this exist at all, or can it be postponed / already solved?
- Would this survive 10× traffic and two years of new engineers?
- What is the change blast radius if this breaks?
- Is the best AI call actually no AI call?
- Does every critical review category clear the quality bar?
