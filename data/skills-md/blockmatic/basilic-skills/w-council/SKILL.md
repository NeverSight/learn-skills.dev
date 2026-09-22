---
name: w-council
description: Explore a codebase with parallel agents, then hand off findings.
disable-model-invocation: true
---

Gather architecture and keywords for the requested area, then spawn a small set of varied explorers. This playbook inspects. It does not commit, push, or open a PR. Implementation continues only when the user already asked for it.

1. Inspect the area yourself first: owning packages, README/scripts, and current behavior. Record keywords and the architecture sketch the agents will use. Skip spawn when one targeted read answers the question.
2. Spawn explorers only as needed. Default to 2–3 with distinct angles, including one out-of-the-box probe. Each brief is self-contained: roots, keywords, sketch, read-only, file:line evidence, no fixes, no further spawn. Split larger investigations into separate bounded runs.
3. Reconcile reports against the tree. Prefer file evidence over agent summaries. If the working tree changed underfoot, re-verify before using a finding.
4. Investigate-only: stop after reconcile. Plan: emit [plan output](../w-plan/references/plan-output.md) in this turn. Follow [build](../w-build/SKILL.md) only if they already asked to implement — do not publish.
