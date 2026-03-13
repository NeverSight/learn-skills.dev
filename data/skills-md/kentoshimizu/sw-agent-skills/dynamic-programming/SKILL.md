---
name: dynamic-programming
description: "Design dynamic programming solutions by defining state, transitions, base cases, and optimization strategy (memoization/tabulation). Use when optimal substructure and overlapping subproblems make brute-force or greedy approaches insufficient; do not use for persistence schema or deployment topology decisions."
---

# Dynamic Programming

## Overview
Use this skill to design correct and efficient DP solutions with explicit state modeling and complexity reasoning.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Inputs To Gather
- Problem objective and correctness constraints.
- State variables needed to represent subproblems.
- Transition rules and dependency ordering.
- Input size limits and memory constraints.

## Deliverables
- DP formulation (state, transition, base cases).
- Complexity analysis (time/space) and optimization options.
- Chosen implementation strategy (top-down/bottom-up).
- Edge-case and correctness verification plan.

## Quick Example
- Problem: minimum cost path.
- State: `dp[i][j]` = min cost to reach cell `(i,j)`.
- Transition: `dp[i][j] = cost[i][j] + min(dp[i-1][j], dp[i][j-1])`.
- Base: first row/column initialization.

## Quality Standard
- State definition is complete and non-redundant.
- Transition uses only valid predecessor states.
- Base cases cover minimal subproblems correctly.
- Complexity fits constraints or includes optimization plan.

## Workflow
1. Define subproblem state and objective function.
2. Derive transitions and base cases.
3. Choose memoization or tabulation strategy.
4. Optimize memory if full table is unnecessary.
5. Validate against edge cases and known examples.

## Failure Conditions
- Stop when state does not capture required decision context.
- Stop when transition introduces cyclic/invalid dependencies.
- Escalate when complexity exceeds target constraints without viable optimization.
