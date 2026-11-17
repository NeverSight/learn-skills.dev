---
name: continuous-agent-loop
description: Patterns for continuous autonomous agent loops with quality gates, evals, and recovery controls.
origin: ECC
---

# Continuous Agent Loop

This is the v1.8+ canonical loop skill name. It supersedes `autonomous-loops` while keeping compatibility for one release.

## Loop Selection Flow

```text
Start
  |
  +-- Need strict CI/PR control? -- yes --> continuous-pr
  |
  +-- Need RFC decomposition? -- yes --> rfc-dag
  |
  +-- Need exploratory parallel generation? -- yes --> infinite
  |
  +-- default --> sequential
```

## Loop Pattern Spectrum

| Pattern | Complexity | Best For |
|---------|-----------|----------|
| Sequential Pipeline (`claude -p`) | Low | Daily dev steps, scripted workflows |
| NanoClaw REPL (`nanoclaw-repl`) | Low | Interactive persistent sessions |
| Infinite Agentic Loop | Medium | Parallel spec-driven generation |
| Continuous Claude PR Loop | Medium | Multi-day iterative projects with CI gates |
| De-Sloppify Pass (add-on) | Add-on | Quality cleanup after any Implementer step |
| RFC-Driven DAG (`ralphinho-rfc-pipeline`) | High | Large features, multi-unit parallel work |

Full recipes for each pattern — Sequential Pipeline variations, the Infinite
Agentic Loop two-prompt system, the Continuous Claude PR loop, the De-Sloppify
Pass, plus anti-patterns and a decision matrix — live in
[reference/loop-patterns.md](reference/loop-patterns.md).

## Reference Files

- [reference/loop-patterns.md](reference/loop-patterns.md) — detailed loop recipes, decision matrix, anti-patterns, and credits (migrated from the retired `autonomous-loops` skill, 2026-06-12).

## Combined Pattern

Recommended production stack:
1. RFC decomposition (`ralphinho-rfc-pipeline`)
2. quality gates (`plankton-code-quality` + `/quality-gate`)
3. eval loop (`eval-harness`)
4. session persistence (`nanoclaw-repl`)

## Failure Modes

- loop churn without measurable progress
- repeated retries with same root cause
- merge queue stalls
- cost drift from unbounded escalation

## Recovery

- freeze loop
- run `/harness-audit`
- reduce scope to failing unit
- replay with explicit acceptance criteria
