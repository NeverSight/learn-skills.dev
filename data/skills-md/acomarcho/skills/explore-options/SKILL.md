---
name: explore-options
description: Generate diverse solution alternatives for a known problem instead of locking onto the first obvious fix. Use when the user asks to explore options, compare approaches, find alternatives, list several solutions, avoid tunnel vision, think from different angles, or evaluate obvious and radical ways to solve a root cause. Produces a scored comparison table of practical, moderate, and radical options.
---

# Explore Options

Use this skill after the problem, root cause, or likely failure mode is understood enough to compare possible solutions. The goal is to avoid tunnel vision: do not present one answer as the only reasonable path unless the evidence truly supports that.

## Workflow

1. Restate the problem: root cause, goal in plain terms, and constraints that matter (time, risk, compatibility, data, ownership, rollout, security, reversibility).
2. Pick the option count: use the user-requested count when given, otherwise 5 (or 8-10 for broad architecture/product/strategy questions).
3. Build a diverse option set (see Option Range). Avoid tiny variations of the same idea. Do not invent unrealistic options just to fill slots.
4. Score and compare each option, then recommend (see Output Format).

## Option Range

Aim for a spread like this unless the user asks otherwise:

- Minimal patch: smallest reasonable change; useful for urgent mitigation or low-risk issues.
- Targeted root-cause fix: addresses the actual source without broad redesign.
- Refactor within current architecture: improves shape while preserving the system boundary.
- Process or data fix: changes workflow, validation, migration, monitoring, or ownership instead of only code.
- Architectural change: changes boundaries, contracts, storage, queues, services, or ownership.
- Radical rethink: removes the problem by changing the product behavior, user flow, invariant, or assumption.

Not every problem needs every category.

## Scoring

Score each option 1-10 on three metrics. Higher is always better:

- **Root cause**: how directly it fixes the actual source of the problem (10 = true root-cause fix, 1 = whack-a-mole patch).
- **Simplicity**: how small and simple the change is (10 = tiny diff, 1 = huge rewrite).
- **Safety**: how low the risk is (10 = easily reversible, small blast radius; 1 = risky, hard to undo).

Score honestly; do not inflate scores to favor a preferred option.

## Output Format

Default to a table:

```text
Problem: ...

| # | Option (1-line idea) | Root cause | Simplicity | Safety | Notes |
|---|----------------------|------------|------------|--------|-------|
| 1 | Minimal patch: ...   | 3          | 9          | 8      | quick mitigation, recurs later |
| 2 | Root-cause fix: ...  | 9          | 7          | 7      | ...                            |

Recommendation
- Safest default: ...
- Best long-term option: ...
- Avoid or defer: ...
```

Keep the idea to one line per row; put extra tradeoffs, "choose this when", or "bad choice when" details in the Notes column or a short list under the table only when they change the decision.

## Evidence and Honesty

- Base options on the actual problem and context already gathered.
- If context is missing, say what assumptions the scores depend on.
- Label speculative options as speculative.
- If all reasonable options point to the same answer, still explain why the alternatives are weaker.
- Do not pretend to know cost, risk, or team constraints that were not provided.
