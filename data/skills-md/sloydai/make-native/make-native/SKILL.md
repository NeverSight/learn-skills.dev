---
name: make-native
description: Rewrites a bolted-on feature so it reads as if it was always part of the original design. Use when a diff, branch, or commit adds a feature through special cases, flags, aliases, parallel components, or preservation tests instead of reshaping the existing code.
---

A light-touch feature layers exceptions onto code that never planned for it. Your job is to redo it so the feature is native.

## Process

1. **Read the feature diff:** `git diff <base>...HEAD`, where `<base>` is the PR's target branch (for example `gh pr view --json baseRefName -q .baseRefName`), or the commit given. List every piece the feature added, including new branches, flags, constants, files, and tests.
2. **Learn the original design, then out-learn it.** For each touched area, go one or two levels deeper than the call site. Read the types, callers, and history (`git log -p`) until you can say why the code is shaped this way. You know more than the original author did. If you have access to runtime data (logs, error tracking, analytics, database records), check which paths and cases actually occur. Read it only; never commit it.
3. **Redesign as if the feature were in the original spec.** Ask: "If the author had known about this feature on day one, what would this code look like?" Then write that version. Take the chance to simplify: generalize the type or union, rename, restructure, merge duplicates, and delete what the new shape makes unnecessary.
4. **Apply Pareto.** Make the common 80% of cases perfect and simple first. Then handle the remaining 20% as well as you can, never at the expense of the 80%. If an edge case would complicate the main path, handle it separately or fail clearly instead.
5. **Rewrite the tests to the new design.** Delete tests that only prove old behavior survived the workaround. Update the remaining tests to the new behavior. Existing tests are expected to change.
6. **Check.** Nobody reading the final code should be able to tell which part was added last. `git grep` the removed symbols and confirm they have no leftovers. Run the project's build, linter, and tests.

## Smells to eliminate

- Aliases that re-derive an existing value, such as `const noun = isVideo ? 'video' : 'image'` when `getContentType()` already returns the noun.
- `if (newKind)` branches scattered through code that already dispatches on kind.
- A new file or component that mirrors an existing one for one variant.
- New `options` tokens, flags, or booleans that duplicate what a type already encodes.
- Duplicated validation or download paths beside the shared ones.
- Tests whose only purpose is "nothing else changed."
- A second system for a concern that already has one, such as a new cost tracker, counter, logger, retry helper, or config reader beside the existing one. Fold it into the existing system, extend that system where it falls short, and delete the duplicate.

## Rules

- Features only. Bug fixes should stay minimal. Don't run this on a bug-fix commit.
- Don't invent new abstraction layers. Reshape the existing ones.
- Keep genuinely different behavior. A `<video>` element versus an `<img>` is real. A duplicated state machine is not.
- Commit separately from the feature commits, following the repo's commit convention. With Conventional Commits, use `refactor` when behavior is unchanged and `feat` when the reshape changes behavior.
