---
name: review-performance
description: "Review code for performance: complexity, database/query efficiency, I/O and network cost, memory and allocation behavior, concurrency contention, caching, and latency/throughput regressions. Cognitive-only atomic skill; output is a findings list."
tags: [eng-standards, optimization]
related_skills: [review-diff, review-codebase, review-dotnet, review-java, review-go, review-powershell, review-sql, review-vue, review-code]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
---

# Skill: Review Performance

## Purpose

Review code for **performance** concerns only. Do not define scope (diff vs codebase) or perform security/architecture/language-framework convention analysis; those are handled by other atomic skills. Emit a **findings list** in the standard format for aggregation. Focus on algorithmic complexity, query efficiency, I/O and network cost, memory behavior, contention and concurrency bottlenecks, caching strategy, and measurable regression risk.

---

## Use Cases

- **Orchestrated review**: Used as a cognitive step when [review-code](../review-code/SKILL.md) runs scope -> language -> framework -> library -> cognitive.
- **Performance-focused review**: When the user wants only performance dimensions checked before merge or release.
- **Regression prevention**: Validate that changes do not introduce obvious latency, throughput, or memory regressions.

**When to use**: When the task includes performance review. Scope and code range are determined by the caller or user.

---

## Behavior

### Scope of this skill

- **Analyze**: Performance dimensions in the **given code scope** (files or diff provided by the caller). Do not decide scope; accept the code range as input.
- **Do not**: Perform scope selection, security review, architecture review, or language/framework style review. Focus only on performance.

### Review checklist (performance dimension only)

1. **Complexity hotspots**: Detect unnecessary O(n^2)+ behavior, repeated scans, nested loops over large collections, and avoidable recomputation.
2. **Database and query efficiency**: N+1 access patterns, missing pagination, broad selects, inefficient joins/filters, and query frequency amplification.
3. **I/O and network cost**: Chatty remote calls, missing batching, blocking calls on critical paths, unbounded retries/timeouts, and poor backoff behavior.
4. **Memory and allocations**: Excessive allocations/churn, large object retention, unnecessary copies, unbounded growth, and avoidable buffering.
5. **Concurrency and contention**: Lock contention, serialized critical sections, thread/goroutine starvation, queue backpressure, and oversubscription risks.
6. **Caching and reuse**: Missing cache opportunities on hot read paths, invalidation correctness risks, stampede risk, and low-value cache layers.
7. **Load-facing behavior**: Missing limits/guards (batch size, page size, concurrency caps), expensive defaults, and absent degradation strategy under load.
8. **Observability for performance**: Missing metrics/tracing around hot paths that prevents regression detection and capacity planning.

### Severity guidance

- **critical**: Clear production impact likely (e.g. unbounded loop/growth, repeated expensive I/O in hot path, catastrophic query pattern).
- **major**: Strong regression or scalability risk with realistic traffic/data growth.
- **minor/suggestion**: Localized or lower-impact optimization opportunities.

### Tone and references

- **Professional and technical**: Reference specific locations (file:line or query/block).
- Emit findings with Location, Category, Severity, Title, Description, Suggestion.

---

## Input & Output

### Input

- **Code scope**: Files or directories (or diff) already selected by the user or scope skill. This skill does not decide scope; it reviews the provided code for performance only.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output contract**.
- Category for this skill is **cognitive-performance**.

---

## Restrictions

- **Do not** perform scope selection, security, architecture, or language/framework style review. Stay within performance dimensions.
- **Do not** give conclusions without specific locations or actionable suggestions.
- **Do not** claim benchmark numbers unless measured evidence is provided in the input.

---

## Self-Check

- [ ] Was only the performance dimension reviewed (no scope/security/architecture/style)?
- [ ] Are complexity, query efficiency, I/O, memory, concurrency, caching, and load behavior covered where relevant?
- [ ] Is each finding emitted with Location, Category=cognitive-performance, Severity, Title, Description, and optional Suggestion?
- [ ] Are high-impact regression risks clearly distinguished from minor optimizations?

---

## Examples

### Example 1: N+1 query pattern

- **Input**: Loop fetches child records per parent with one query per iteration.
- **Expected**: Emit a major/critical finding for N+1 behavior; suggest batch query or join strategy. Category = cognitive-performance.

### Example 2: Hot-path allocation churn

- **Input**: Request handler repeatedly allocates large temporary buffers and serializes payload multiple times.
- **Expected**: Emit a major finding for allocation pressure and latency impact; suggest reuse/pooling or single-pass transform. Category = cognitive-performance.

### Edge case: No clear performance risk in small formatting diff

- **Input**: Diff includes comments/renaming only, no behavioral changes.
- **Expected**: Emit no findings or one suggestion-level note; do not invent optimization work. Category remains cognitive-performance for any emitted finding.

---

## Appendix: Output contract

Each finding MUST follow the standard findings format:

| Element | Requirement |
| :--- | :--- |
| **Location** | `path/to/file.ext` (optional line or range, or query/block identifier). |
| **Category** | `cognitive-performance`. |
| **Severity** | `critical` \| `major` \| `minor` \| `suggestion`. |
| **Title** | Short one-line summary. |
| **Description** | 1-3 sentences. |
| **Suggestion** | Concrete fix or improvement (optional). |

Example:

```markdown
- **Location**: `service/orders/handler.go:118`
- **Category**: cognitive-performance
- **Severity**: major
- **Title**: Per-item remote call inside request loop
- **Description**: The handler performs one downstream call per item, creating linear remote round-trips and latency growth.
- **Suggestion**: Batch requests or prefetch related data once per request; add timeout and bulk size guards.
```
