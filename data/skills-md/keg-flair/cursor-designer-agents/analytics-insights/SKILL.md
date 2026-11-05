---
name: analytics-insights
description: Turns funnels/events into ranked UX hypotheses with mechanisms, fastest follow-up analyses/tests, and instrumentation gaps. Use when the user shares a funnel/dashboard drop-off and wants “why is this happening?” plus what to measure next.
---

# Analytics → UX Insights

See shared conventions in `docs/HOUSE_STYLE.md` (confidence, fallbacks, evidence labels).

## Defaults

- **What we know vs don’t**: restate inputs and definitions; flag ambiguity.
- **Ranked hypotheses**: each includes mechanism, expected signal, confidence, and fastest test.
- **Instrumentation-aware**: call out gaps that block confident conclusions.

## Constraints

- **Do not invent** metric definitions, time windows, segments, or causal claims.
- **Ask at most 3 clarifying questions**; if unanswered, proceed with low-confidence hypotheses and a tight “next analyses” list.

## Clarifying questions (ask max 3)

1. Time window + segment(s) + unit of counting (users vs sessions)?
2. Exact event definitions (especially “start” vs “complete”) and any known tracking quirks?
3. What decision do we need to make (copy/layout, error handling, performance, onboarding, pricing, etc.)?

## Inputs to request (only if missing)

- Funnel steps with counts + step-to-step conversion (if available)
- Time window + segment + denominator definitions
- Any relevant context (recent releases, traffic source changes, known bugs)

## Fallback behavior (when definitions are missing)

If the user gives “big drop after signup” with no definitions, still output:
- A **minimum data request** (time window, segment, steps, counting unit)
- 3–5 **low-confidence hypotheses** with the fastest analysis to confirm/deny each
- A focused **instrumentation gap list** (what would make the answer knowable)

## Output template

```markdown
#### 1) What we know (from provided data)
- **Time window**:
- **Segment**:
- **Funnel / steps**:
- **Biggest leak**:
- **Notes on definitions**:

#### 2) Top hypotheses (ranked)
##### 1)
- **Hypothesis**:
- **Mechanism**:
- **Where in the flow**:
- **Expected signal**:
- **Confidence**:
- **Fastest test**:
- **Risks / trade-offs**:

#### 3) Instrumentation gaps (blockers to confidence)
- …

#### 4) Next analyses (cheap, decisive)
- …

#### Test plan / validation
- Primary metric + guardrails
```

