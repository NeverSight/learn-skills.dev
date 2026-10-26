---
name: code-refine
description: Refines code through the three lenses in `code-refinements` with verified, behavior-preserving edits. Use when the user asks to refine a scope of code, such as a module, a directory, or the changes on a branch.
disable-model-invocation: true
argument-hint: <scope, e.g. "the planner module" or "the changes on this branch">
---

# Code Refine

The scope is whatever the user asks to refine; without one, use the current staged and unstaged diff, including untracked source files. If there is no code to refine, say so and stop. A scope that names changes — pending changes, a branch, a pull request — is refined as the diff it names; everything else is an area.

Load the `code-refinements` skill and hold every change to its rules and its three lenses: constraints, simplicity, and parametricity. If it is not installed, install it with:

```sh
npx skills add https://github.com/alexandru/skills --skill code-refinements
```

## Workflow

1. **Establish scope, contracts, and verification.** Read the project's agent instructions, conventions, and relevant specifications. Identify the behavior and APIs to preserve, the scope's hot paths, and the required verification. Where a specification leaves behavior undefined, investigate existing contracts and callers; report unresolved ambiguity rather than inventing a requirement.
2. **Identify and apply justified refinements.** Review through the three lenses and trace callers to check behavior claims. Each change must name the complexity it removes and preserve the contracts below. Verify edits with the relevant tests; add characterization tests where observable behavior is uncovered. Report existing bugs that require behavior changes for approval; when a fix is authorized, demonstrate it with a failing test before fixing it.
3. **Repeat until no worthwhile improvement remains.** Reassess the changed code and its core model for further justified refinements within scope. Look beyond local cleanups: a different representation can eliminate invalid states, a pass, or an entire module.
4. **Review, verify, and report.** Review the aggregate diff for regressions and interactions between changes. Fix or revert regressions, run the project's required verification across supported configurations, and rerun after fixes. Check performance when hot paths change. Report the complexity removed, authorized bug fixes and their tests, verification results and limitations, and decisions left to the user.

## Invariants

- Refinement is refactoring: end-user behavior MUST NOT change without explicit user authorization, including changes to fix existing bugs. Internal structure, data types, call order and intermediate representations are free to change only while preserving observable behavior. Features stay, and hot paths must not get slower.
- Input the code accepted before stays accepted: a value that parsed, a request that succeeded, data already stored. A stricter input rule is a behavior change and requires authorization.
- The public API is behavior — the signatures users compile against, and their doc comments, which state the contract — unless the user or project's instructions explicitly permit API changes. A change updates a doc sentence it makes false.
- Tests keep running everywhere they ran before: never narrowed to the configuration CI happens to run, never deleted while their case is uncovered.
- For a diff scope, refine only what the diff added or changed; reach the surrounding code only when the diff's changes force it.
