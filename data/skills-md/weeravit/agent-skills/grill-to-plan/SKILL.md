---
name: grill-to-plan
description: Orchestrator that chains grilling, ponytail, superpowers:writing-plans, and flutter-unit-test — asks the user which language to grill in, pressure-tests the plan against over-engineering, then writes the confirmed design to an English plan doc in-project, with tests written per flutter-unit-test.
disable-model-invocation: true
---

Grill the user about the design below, then write the plan.

## Design

$ARGUMENTS

## Steps

1. Run `codegraph sync` first, always, before anything else.
2. Get an overview of the codebase with `codegraph` before starting — never grep/read raw when a codegraph query answers it.
3. Ask the user which language to grill in before starting the session. Use that language for every step below until the plan is written.
4. Run the `grilling` skill on the design above, conducting the entire session in the chosen language. For each question:
   - Before asking, explore the relevant code with `codegraph` so the question and its recommendation are grounded in what the code actually does — never ask from assumption.
   - Present `ponytail`'s minimal/lazy answer as one of the choices alongside grilling's normal recommendation — always, not only when an over-engineering risk appears.
5. When the session feels complete, ask the user (in the chosen language) whether they want to grill further or add questions. Loop step 4 until they explicitly confirm they're done — never advance on an assumed yes.
6. Only after that confirmation, run `superpowers:writing-plans` to write the plan:
   - Language: English.
   - Save path: `docs/superpowers/plans/` in the project (not the harness scratch/plan path).
   - Include tests in the plan. Write every test step by following the `flutter-unit-test` skill — its rules, mocking, and Given-When-Then structure.
   - Do not run `dart format` on it.
   - Do not perform any translation work.
   - No comments in the plan's code at all. Make the code self-explanatory instead: intent-revealing names, small functions, explicit types — a human reads it without a comment.
