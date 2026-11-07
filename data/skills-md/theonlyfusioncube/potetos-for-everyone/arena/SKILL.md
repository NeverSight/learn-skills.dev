---
name: arena
description: Spawn parallel candidate implementations for the same task, cross-judge, and graft the best parts into the winning base. Use when exploring competing designs or critical artifacts.
---
# Arena

Fan out N parallel attempts at the same task, score them against concrete criteria, pick a base, and graft the best ideas from the others.

1. Frame: Define the artifact contract, 3-6 concrete rubric criteria, and isolated candidate output paths.
2. Fan out: Run parallel candidate attempts on isolated workers (via `delegate` when supported, or labeled sequential passes). Require a concrete artifact and short rationale from each.
3. Cross-judge: Score each candidate against the rubric criteria, compare trade-offs, and recommend the strongest base.
4. Pick a base: Select the implementation that is cleanest, easiest to maintain, and safest under domain invariants.
5. Graft: Port the best independent ideas or edge-case handling from losing candidates into the base by hand.
6. Verify: Validate the synthesized result against the full test and verification suite.
