---
name: ds-principles
description: "Compact engineering principles for design, debugging, verification, and delegation, each with a trigger. Use when choosing structure or types, sizing a diff, debugging, writing tests, or when the user types /ds-principles."
---

# Engineering principles

If a trigger matches, apply the rule. Name principles that changed a decision.

## Design

1. **Subtract, then add little.** Remove dead code and stale checks first, then make the shortest diff that works. No abstraction with one user. Apply when sizing a diff or tempted to add a layer.
2. **Data shape first.** Choose the core types and structures before logic. Apply before writing new logic.
3. **Model the domain.** Put states in one structure, such as a typed union, state machine, or lookup table, not scattered conditionals. Apply when code branches a lot or repeats a shape across files.
4. **Redesign for the new need.** Fit a new requirement as if it existed from day one. Apply when an addition strains the design.
5. **Low reader load.** Inline one-caller wrappers and shrink mutable scope. Apply when code is hard to trace.
6. **Guards at boundaries.** Validate where input enters: CLI, config, network, files, external APIs. Trust types inside and keep core logic pure. Apply when adding validation or error handling.
7. **Idempotent steps.** Rerunning a step, even after a crash, reaches the same state. Apply to commands, setup, and retries.
8. **No shared writers.** Give each concurrent actor its own file, branch, or key before using locks. Apply when parallel work touches shared state.
9. **Migrate, then delete.** Move every caller and delete the old API in one change. No shims. Apply when replacing an API or rewriting in phases.
10. **Compare options.** For an unprecedented design, sketch two or three. Prefer fewer, polished features. Apply to novel architecture, UX, or scope choices.

## Debugging and verification

11. **Fix root causes.** Fix where state first went wrong. A guard fixes only legitimate states. Apply when debugging.
12. **Attack the premise.** After two failed fixes that share an assumption, write it down and test it directly. Apply before a third attempt.
13. **Prove it works.** Run the real thing and read the actual output, not a proxy. Apply before claiming done.
14. **Verifiable units.** Split work into steps that each end in a passing check. Apply to sweeps, migrations, and stacked commits.
15. **Test behavior.** Assert what callers can observe, so tests survive refactors. Apply when writing or keeping a test.
16. **Explain the number.** Find what limits a measurement and confirm it measured the right work. Apply to benchmarks and eval scores.
17. **Build the tool.** Script bulk or repeated work so it can be rerun. Apply to large edit sets or checks.

## Process

18. **Guard the context.** Keep summaries, not dumps. Send bulk reading to subagents. Apply when outputs or files are large.
19. **Do not block on the human.** On reversible work, proceed and show the result. Apply when tempted to ask "should I?".
20. **Encode repeated lessons.** A correction given twice becomes a lint, test, or script. Apply when a mistake recurs.
21. **Comments explain why.** Keep a comment only for a reason the code cannot show, such as an external constraint or a public API contract. Delete narration and dead code. Fix code whose surprise needs a comment. Apply when writing or reviewing code.

## Types

- Make illegal states unrepresentable. Use discriminated unions, not optional-field bags.
- Parse external data once at the boundary into a named type. Trust it inside.
- Use `unknown` for untrusted input. Never `any`. No `as` casts before validation.
- Derive types from a schema, not hand-written guards.
- Add a `never` check in default branches so new variants fail the build.
- Brand primitives that must not mix, such as user IDs and order IDs.
