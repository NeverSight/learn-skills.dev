---
name: w-perf
description: Measure bottlenecks with repository tools, then recommend or apply evidenced optimizations.
disable-model-invocation: true
---

Find performance issues with a measured baseline. Do not invent SLOs or impact percentages. Report-only unless the user asked to implement.

1. Read testing docs for budgets if present. Capture a baseline with the repo profiler, traces, tests, or `gh` job timing — not estimates.
2. Locate the owning hot path (query, render, allocation) with that evidence.
3. Recommend the smallest change. Implement only when authorized. Re-measure after a change.
4. If a new budget is required, document it in existing testing docs instead of inventing an SLO here.
5. Docs: `/w-docs` if behavior or commands changed.
