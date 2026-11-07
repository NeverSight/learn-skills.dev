---
name: "4"
description: "Deeper execution timebox for substantial tasks requiring broader investigation, implementation, and regression testing. Use when the user invokes /4 and target completion within 18 minutes."
---

# /4 — Deep

Complete this substantial task end to end with focused investigation and strong verification.

## Timebox

Target completion in under 18 minutes. The larger timebox allows broader investigation, not lower urgency.

## Behavior

- Understand the relevant system before modifying it.
- Trace interactions across affected files and components when necessary.
- Find root causes rather than layering patches.
- Consider meaningful edge cases and failure states.
- Implement the complete requested behavior.
- Refactor locally when required for a clean solution.
- Run appropriate tests, builds, linting, or visual verification.
- Check for regressions in closely connected functionality.
- Remove temporary or debugging artifacts.
- Do not wander into unrelated improvements.

Parallelize independent investigation or verification when tools allow it. Prefer decisive execution over prolonged deliberation. Finish with the implementation in a clean, verified state.
