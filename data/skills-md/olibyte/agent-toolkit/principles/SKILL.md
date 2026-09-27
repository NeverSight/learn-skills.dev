---
name: principles
description: Apply named engineering principles such as laziness, prove-it-works, and model-the-domain. Use when choosing a design, sequencing work, reviewing a diff, or the user names a principle.
license: MIT
---

Codex `$principles`. Claude Code, Cursor, and Antigravity `/principles`.

# Principles

Read the matching file under `references/` in full before you apply a principle. Cite only files you read this session.

## Index

- **Attack the Premise** (`principle-attack-the-premise`). Apply when two or more fixes that share one premise have failed the same gate. Take a census of which actors hold the imbalance before the next fix, then question the premise instead of writing another fix that assumes it.
- **Boundary Discipline** (`principle-boundary-discipline`). Apply when wiring validation, error handling, or framework adapters. Concentrate guards at system boundaries (CLI, config, network, external APIs); trust internal types and keep business logic in pure functions.
- **Build the Lever** (`principle-build-the-lever`). Apply to any non-trivial work, not just bulk work: edits, migrations, analyses, checks. Build the tool that does it or proves it (codemod, script, generator, or a skill your subagents follow) instead of working by hand. The tool is the artifact a reviewer can rerun.
- **Encode Lessons in Structure** (`principle-encode-lessons-in-structure`). Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction. Encode the rule as a lint, metadata flag, runtime check, or script instead of more text.
- **Exhaust the Design Space** (`principle-exhaust-the-design-space`). Apply when facing a novel UI interaction or architectural decision with no precedent in the codebase. Build 2-3 competing prototypes and compare side by side before committing.
- **Experience First** (`principle-experience-first`). Apply when product, UX, or feature-scope tradeoffs come up. Choose user delight over implementation convenience; ship fewer polished features over more rough ones.
- **Fix Root Causes** (`principle-fix-root-causes`). Apply when debugging. Trace each symptom to its root cause and fix it there; reproduce first, ask why until you reach it, resist nil-check guards that silence crashes.
- **Foundational Thinking** (`principle-foundational-thinking`). Apply before writing logic: choosing core types and data structures, sequencing scaffold-vs-feature work, asking what concurrent actors share. Get the data structures right so downstream code becomes obvious.
- **Guard the Context Window** (`principle-guard-the-context-window`). Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents; keep summaries in the main thread, not raw payloads.
- **Laziness Protocol** (`principle-laziness-protocol`). Apply when refactoring, evaluating diff size, tempted to add abstractions, layers, or signal threading, or reaching for a new helper or dependency. Bias toward deletion, reuse, and the smallest change that solves the problem.
- **Make Operations Idempotent** (`principle-make-operations-idempotent`). Apply when designing commands, lifecycle steps, or processing loops that run amid crashes, restarts, and retries. Converge to the same end state regardless of partial prior runs.
- **Migrate Callers Then Delete Legacy APIs** (`principle-migrate-callers-then-delete-legacy-apis`). Apply when introducing a new internal API while old callers still exist. Migrate callers and delete the old API in the same wave instead of preserving compatibility layers.
- **Minimize Reader Load** (`principle-minimize-reader-load`). Apply when reviewing or shaping code that's hard to trace. Count layers between question and answer, and hidden state in the reader's head; collapse one-caller wrappers and shrink mutable scope.
- **Model the Domain** (`principle-model-the-domain`). Apply when writing stateful logic, or when code branches a lot or repeats a shape assumption across files. Encode the domain in a structure instead of scattered conditionals.
- **Never Block on the Human** (`principle-never-block-on-the-human`). Apply when tempted to ask 'should I do X?' on reversible work. Proceed, present the result, let the human course-correct after the fact; reserve confirmation for irreversible actions.
- **Outcome-Oriented Execution** (`principle-outcome-oriented-execution`). Apply during planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture; don't preserve smooth intermediate states with throwaway compatibility code.
- **Prove It Works** (`principle-prove-it-works`). Apply after completing a task, before declaring done. Verify against the real artifact (run the feature, read the actual value, inspect the diff), not a proxy, self-report, or 'it compiles.'
- **Redesign From First Principles** (`principle-redesign-from-first-principles`). Apply when integrating a new requirement into an existing design. Redesign as if the requirement had been a foundational assumption from day one, instead of bolting it on.
- **Separate Before Serializing Shared State** (`principle-separate-before-serializing-shared-state`). Apply when concurrent actors might write to the same file, branch, key, or state object. Eliminate the sharing first; serialize structurally only when one shared writer is a real invariant.
- **Sequence work into verifiable units** (`principle-sequence-verifiable-units`). Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs. Break work into small units that each end in a verifiable state, check each before the next, and order delivery so the sequence proves itself to a reviewer.
- **Subtract Before You Add** (`principle-subtract-before-you-add`). Apply when sequencing an addition, refactor, or rewrite. Remove dead code, redundant validators, and stub references first, then build on the simpler base.
- **Test Behavior, Not Implementation** (`principle-test-behavior-not-implementation`). Apply when you write, change, or keep a test. Call the code the way its users do and assert the result they observe against a literal expected value. If the test would still pass when every imported function returns undefined, rewrite the assertion or delete the test.
- **Type System Discipline** (`principle-type-system-discipline`). Apply when designing types, reviewing a function signature, or writing code in any statically-typed language. Make illegal states unrepresentable, brand semantic primitives, parse external data at boundaries, refuse to lie to the compiler, exhaust variants, derive from authoritative schemas.
