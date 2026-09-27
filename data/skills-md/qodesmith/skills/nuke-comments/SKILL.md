---
name: nuke-comments
description: Decide whether a comment earns its place, and strip the ones that do not. Use before writing or editing a comment in any code, when the user wants comments cut, or when they mention comment bloat or noisy agent comments.
---

# Nuke comments

A comment costs attention on every read, and goes stale the moment the code moves.
It earns that cost only by carrying what the code cannot.

## What a comment must earn

Four keepers, and nothing else:

- **Trap**: library or framework behaviour that bites the next editor.
  _"This Checkbox spreads external props over its own click handler, so an `onClick` here would replace the toggle rather than compose with it."_
- **Contract**: an invariant, a unit, or an order that the code does not show.
  _"`riskCells` stays row-major; the heatmap rebuilds its axes from that order."_
- **Directive**: text the tooling reads, for example `oxlint-disable`, `eslint-disable`, `use no memo`, `@ts-expect-error`, `@vitest-environment`, or `prettier-ignore`.
  These are machinery, not prose.
  Keep every one, and shorten a long trailing rationale to a clause.
  The legal comment (`/*!` or `@preserve`) marks a comment a human has exempted from a sweep, so keep it word for word.
  This one is enforced mechanically: esbuild keeps a legal comment in minified output, so `verify-comments-only.sh` reports a deleted one as `CODE CHANGED`.
- **Signpost**: a single terse JSDoc line on a shared util, a hook, or a project-level abstraction.
  Also a section marker that names a real structural division a reader must navigate, for example a Dockerfile build stage, or the grouped blocks of a config file.

The test, applied to every comment: **delete it, and ask whether a competent engineer could now plausibly break this code.**
If not, it was noise.
Default to deleting.

A keeper that runs past two lines is usually a trap with a story wrapped around it.
Keep the trap, and cut the story.

## Noise

These are noise by construction, whatever they say:

- Restating the line, the function name, or the type below it
- A per-field description on a type where the field name already says it
- A file-header essay, and a divider over a single logical unit or a section the code already labels
- A design-doc or issue reference, for example `#116`, "matches the design", or "see inventory section 9"
- Narration of mock and fixture data
- Arrange, act, and assert steps, or a comment that restates the `it(...)` description
- Commented-out code
- Rationale for a decision nobody would question

When a comment exists to explain _what_ the code does, the code is the problem.
Rename or restructure, and the comment dissolves.

## Writing code

Apply the test as you write.
The comment you never type is free, and the one you type gets deleted later by someone who pays to read it first.

## Sweeping a codebase

A sweep changes comments and whitespace **only**, so no code, logic, type, string, or JSX moves.

Asked to review rather than to sweep, for example a CI job or a pull request diff, edit nothing: classify each comment as a keeper or as noise, and report it.

1. **Establish green.**
   Run the typecheck, lint, format check, unused-code check, and tests of the project, and record the result.
   Every later check compares against this, so a failure that is already there must be known now.
2. **Find the density.**
   Rank the files by comment lines, to see where the weight sits.
   Exclude a generated file, for example `*.gen.*` or codegen output, because its generator rewrites it.
3. **Partition and fan out.**
   Split by directory into scopes that do not overlap, and dispatch one subagent per scope, in a single message, so they run at the same time.
   Give each subagent its exact file scope, the four keepers, the noise list, the comments-and-whitespace-only rule, and the instruction to run the typecheck and the lint but **not** the test suite, because parallel agents that share a tree trip over each other's runs.
   Name the worst offender in a scope, so its owner condenses it rather than deletes it blindly.
4. **Verify, do not trust.**
   A subagent reports its own diff, so confirm the claim yourself.
   Re-run the full baseline, then prove that the diff is comments only with the `verify-comments-only.sh` script beside this file:

   ```
   <this-skill-directory>/verify-comments-only.sh [base-ref]
   ```

   It minifies every changed file at the base ref and in the working tree and compares them.
   Identical output means the comments moved and the code did not.
   It reports two things it cannot judge, and both need your eyes: a type-only file, which erases to nothing, and a file that is not JS, for example HTML or Markdown.
   For those, diff the file and confirm that every `+` and `-` line is a comment or a blank line.

   Read the failures of the script, and not the exit code alone.
   A green run means something only when the tool really ran, because an esbuild call that errors prints nothing and compares empty output to empty output, which looks identical and proves nothing.

   Then audit the directives, which the minification cannot see, because it strips them as comments:

   ```
   git grep -c 'oxlint-disable\|eslint-disable\|@ts-expect-error\|vitest-environment\|use no memo\|@public\|@internal\|@beta\|@alias'
   ```

   Compare the counts against the base ref.
   A drop means a directive died, unless the lost hit was prose that only mentioned a directive inside a deleted essay, which is fine.
   Confirm which one it is before you move on.

   The last four belong to knip, when the project uses it: a JSDoc `@public` on an export that nothing else references is what keeps knip quiet about it, so a deleted comment turns a green unused-code check red.

5. **Report the numbers.**
   Total comment lines before and after, the files touched, and the checks that passed.
   Name a few comments you kept on purpose and why, so the judgement is reviewable rather than a wall of deletions.

Done means: the baseline is green, the minified output is identical, and the directive counts reconcile.
