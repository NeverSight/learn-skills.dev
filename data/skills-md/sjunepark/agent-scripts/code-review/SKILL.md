---
name: code-review
description: "Review completed code changes, roadmap or specification implementation, architecture, technical choices, or overengineering."
---

# Code Review

## Workflow

1. Establish scope and edit policy.
   - If the user names files, a directory, a module or subsystem, a branch, a
     commit, a PR patch, or a diff, review that target.
   - When the user asks to review implementation against a roadmap,
     specification, issue, ADR, or migration plan, treat that document as the
     source of intent and resolve the implementation it governs. Do not reduce
     the target to the document alone.
   - For an initiative review, establish four scope axes: governing intent,
     claimed milestone or outcome, implementation range, and edit policy.
     Inspect along requirement, consumer, and risk edges as needed, while
     keeping findings bounded to those axes.
   - If no target is named and the repository has uncommitted changes, default
     to the current uncommitted change set.
   - If no target is named and no review target can be inferred, ask for the
     target.
   - Honor `review-only`, `do not edit`, and equivalent instructions.
   - Distinguish issues introduced by the reviewed change from pre-existing
     debt.
   - Continue once the target and edit policy are explicit.

2. Run the implementation gate for every review. Read
   [lenses/implementation-review.md](lenses/implementation-review.md).
   - Continue once material issues, obvious safe fixes, validation gaps, and
     remaining decision points have been checked.

3. Run the system lens for every review. Read
   [lenses/system.md](lenses/system.md).
   - Apply it proportionately to the target. Inspect the system choices and
     cross-cutting consequences the target changes or materially relies on;
     treat inapplicable dimensions as checked without manufacturing findings.
   - Follow the named intent and its consequences across affected areas without
     turning a bounded review into an unsolicited whole-repository audit.
   - Continue once every relevant stated outcome, constraint, material choice,
     and applicable cross-cutting consequence has a disposition, and every
     criticized choice has an evidenced alternative and tradeoff.

4. Run the design lens for every review. Read
   [lenses/design.md](lenses/design.md).
   - Apply it proportionately to the affected modules and consumers. A routine
     local edit still receives a bounded design check; it does not require a
     broader redesign or whole-codebase investigation.
   - Continue once the target's responsibilities, interfaces, dependencies,
     affected consumers, and relevant architecture decisions have been checked.

5. Run the diet lens for every review. Read
   [lenses/diet.md](lenses/diet.md).
   - Apply it proportionately. For a routine small edit with no complexity
     signal, make a brief check and conclude without a diet finding rather than
     searching for speculative simplifications.
   - Continue once unearned complexity candidates are either reported or
     explicitly kept as-is.

6. Report findings and validation concisely. Use the buckets below when they
   contain material information; for a clean review, state that no actionable
   findings remain and summarize validation.
   - `Delivery Coverage`: only for roadmap, specification, or initiative
     reviews; use the system lens's outcome classifications and evidence.
   - `Bucket I - Safe Fixes`: safe issues found, marked `applied` or `proposed`
     according to edit policy, with changed or affected files and validation
     evidence.
   - `Bucket II - Needs Decision`: real issues or simplifications that need
     user judgment, with the decision needed and the main tradeoff.
   - `Keep As-Is`: meaningful concerns inspected and intentionally rejected,
     when useful.
   - `Validation`: commands run and results, or skipped/blocked reason.
   - `Residual Risk`: only when validation, scope, or context leaves a material
     gap.

## Review Rules

- Prefer no finding over a weak finding.
- Record only discrete, actionable issues with affected paths, trigger
  scenarios, and likely maintainer action. When implementation is absent, cite
  the governing requirement, consumer, or system surface instead of inventing
  an affected path.
- Record each issue once under the lens that owns its remedy: implementation
  for concrete behavior, requirement fulfillment, and validation; system for
  initiative outcome coverage, non-goals, readiness, and durable technical
  decisions; design for system shape and contracts; and diet for
  simplification.
- Apply obvious safe Bucket I fixes by default. When the edit policy forbids
  edits, report them as `proposed`.
- Do not implement Bucket II without explicit user approval.
- Keep edits tightly scoped to the reviewed target.
- Do not stage, commit, or push unless explicitly asked.
