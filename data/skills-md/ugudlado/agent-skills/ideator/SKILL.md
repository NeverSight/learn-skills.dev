---
name: ideator
description: "Generate, refresh, and prioritize product or engineering ideas using current evidence. Use for brainstorming, backlog triage, or choosing what to build next."
---

# Ideator

Use the supplied vision, constraints, repository evidence, existing ideas,
completed work, and optional external research. Sources may be inline or
caller-selected files and services.

## Method

- Check whether each candidate already exists, is partly complete, is stale,
  or is superseded before ranking it.
- Generate new ideas only after checking for duplication.
- Rank by user value, strategic fit, dependency order, risk reduction, effort,
  and evidence—not a stored priority label alone.
- Distinguish facts from research signals and assumptions.
- Do not create tickets or persist backlog changes unless requested.

## Result

Return `ideas` containing ranked recommendations, rationale, freshness status,
dependencies, evidence, and rejected stale or duplicate candidates.
