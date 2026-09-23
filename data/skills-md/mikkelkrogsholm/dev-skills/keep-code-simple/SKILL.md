---
name: keep-code-simple
description: Prevent overengineering before and during software planning, implementation, fixes, reviews, and refactors. Use before planning coding work and whenever an agent might add speculative abstractions, excessive indirection, unnecessary files or dependencies, broad cleanup, premature extensibility, several competing approaches, or ceremony beyond the current requirement. Apply KISS, YAGNI, pragmatic DRY, selective SOLID, a dependency ladder, explicit non-goals, and a diff-scoped simplification gate to produce the smallest clear, correct, verifiable change.
---

# Keep Code Simple

Read and apply this skill before planning. Build the smallest clear solution that satisfies the current requirement and can be verified now. Treat additional structure as a cost that must earn its place.

If the work involves delegation, a goal loop, a board, a DAG, or runtime limits, also load `keep-agent-workflows-simple` before planning when available.

## Write the task contract first

Define these items before proposing architecture or edits:

- **Outcome:** one observable result.
- **Non-goals:** tempting adjacent work that must remain unchanged.
- **Write scope:** the smallest files or subsystem likely to change.
- **Acceptance:** commands, tests, artifacts, or observations that prove success.
- **Stop condition:** finish when acceptance passes; stop and ask when a required change escapes scope or needs an unresolved product, architecture, security, dependency, production, or irreversible decision.

Keep the contract short. Inspect first when the repository must determine the exact scope. Do not use a long-running goal or implementation loop to discover what the task should be.

## Set the priority order

1. Preserve correctness, safety, compatibility, and explicit constraints.
2. Make the smallest change that solves the demonstrated problem.
3. Keep control flow and data flow easy to trace locally.
4. Reuse an existing pattern when it already fits.
5. Add a new abstraction only when current evidence justifies it.

Do not use simplicity to omit required validation, error handling, security, migrations, accessibility, or tests.

## Follow the implementation ladder

Choose in this order:

1. Remove work that is not required now.
2. Reuse the repository's existing implementation or convention.
3. Use the language, framework, or platform's native facility.
4. Use an already-installed dependency.
5. Add the smallest direct code needed.
6. Add a new dependency or abstraction only with a concrete present-day justification.

Prefer one straightforward approach. Compare alternatives only when the choice is materially ambiguous, unfamiliar, expensive to reverse, or high risk; bound the comparison and select one before implementation.

## Apply the principles pragmatically

### KISS and YAGNI

- Prefer direct functions, explicit data, static dependencies, conventional framework patterns, and boring technology.
- Keep the happy path visible and handle real edge cases without designing for imagined ones.
- Do not add extension points, flags, plugin systems, generic engines, shims, future-facing APIs, or speculative infrastructure without a current consumer.
- Keep unrelated cleanup and hypothetical improvements out of the diff.

### DRY

- Treat DRY as one authoritative source for knowledge, not a ban on similar-looking code.
- Tolerate small local duplication when it preserves independence and clarity.
- Extract only when duplication represents the same rule and already creates drift or maintenance cost.
- Reject helpers whose flags, callbacks, generics, or branches are harder to understand than the repeated code.

### SOLID

- Favor SRP: give a unit one coherent reason to change.
- Require real substitutability before introducing LSP-oriented hierarchies.
- Split interfaces only for actual consumers.
- Apply dependency inversion at real external or volatile boundaries, not between every module.
- Do not use OCP to predict future variants. Modify simple code until real variation appears.

## Enforce abstraction and dependency budgets

Prefer zero new abstractions and dependencies. Add an interface, base class, factory, wrapper, service, manager, registry, event bus, dependency-injection layer, generic type, configuration option, file, or package only when at least one condition is true:

- the current requirement explicitly needs it;
- multiple current consumers need the same boundary;
- it isolates a real external or volatile dependency;
- it removes more complexity than it introduces; or
- an established repository or framework convention requires it.

State the present-day pressure when adding one. Do not justify it with “might,” “later,” “future-proof,” or “for extensibility” alone.

## Optimize for agent readability

- Prefer cohesive vertical slices over new horizontal layers.
- Use domain-specific names that are easy to locate with search.
- Prefer explicit imports, direct calls, composition, and typed boundaries over magic dispatch, deep inheritance, barrel indirection, or hidden global state.
- Keep tests close to behavior when repository conventions allow it.
- Make time, randomness, network, environment, and other side effects deterministic or injectable where tests require it.
- Follow the repository's framework conventions when they conflict with generic preferences.

## Execute and simplify

1. Inspect the nearest relevant code, tests, and conventions.
2. Confirm the task contract and choose the smallest edit surface.
3. Implement one direct path.
4. Add or update the narrowest meaningful verification.
5. Run the named acceptance checks.
6. Review only the resulting diff against outcome, non-goals, and write scope.
7. Remove unused flexibility, speculative branches, redundant comments, accidental dependencies, unrelated edits, and one-use abstractions that add no boundary value.
8. Re-run verification after simplification.

Do not turn the simplification pass into a broad refactor or a new multi-agent workflow. Preserve tests, security controls, useful assertions, accessibility, and necessary error handling.

## Stop overengineering loops

Stop and simplify when:

- more files or concepts were added than the behavior needs;
- a simple operation requires several navigation hops;
- the design serves only hypothetical consumers or variants;
- a new abstraction has one implementation and no boundary value;
- the task expands into adjacent systems without necessity;
- verification fails repeatedly without a changed hypothesis, input, environment, or tool; or
- explaining the architecture takes longer than explaining the behavior.

## Report the result

Lead with completed behavior and verification. Mention the key simplification decision and any justified new dependency or abstraction. Do not advertise hypothetical extensibility or optional future phases unless asked.

For provenance and dated evidence behind these evergreen rules, read [references/research-basis.md](references/research-basis.md) only when reviewing or evolving this skill.
