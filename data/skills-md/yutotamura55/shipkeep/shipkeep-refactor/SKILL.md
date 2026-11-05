---
name: shipkeep-refactor
description: Use when restructuring code without changing what it does — after an inspection, when a part has become hard to change, or to find which parts are worth restructuring. Finds hotspots, pins current behavior with tests, measures complexity before and after, changes in small steps on a dedicated branch, and stops when the work would change behavior. Any language.
---

# Restructure code without changing its behavior

Refactoring here means changing the structure of code while keeping what it
does, as seen from outside, the same. This skill turns a vague wish ("make it
cleaner") into a goal that can be checked, protects current behavior with
tests, and changes the code in small, verified steps.

The skill changes the repository. Follow `references/change-principles.md`
throughout; the steps below add what refactoring needs on top.

## Steps

1. **Find candidates** when the user has not named the code to restructure:

   ```bash
   python3 <this skill's directory>/scripts/hotspots.py <repository> [--max-commits 500] [--limit 20]
   ```

   It prints JSON with the source files that changed most often in recent
   commits, multiplied by their size (`score`). With `--format result` it
   prints the same list in the common shipkeep result format
   (`references/result.schema.json`) for filing or keeping. Exit code 2 means the script
   could not run (wrong arguments, Git missing or failing, or no repository with
   commits); report its message and stop. For the top
   files, measure complexity and duplication as `references/measurement.md`
   describes, then read the code. Present a few candidates to the user with the
   reason for each, and let them choose.
2. **Agree on four things before changing any code**, and write them in the
   plan (and in an Issue if the user wants one):
   - **Goal**: which change or reading becomes easier. "Make it readable" cannot
     be checked. Example: "adding one status message needs a change in one
     function only."
   - **Scope and exclusions**: the files and functions to change, and what stays
     untouched. Changes of behavior, new features, and new dependencies or
     settings are out of scope; if one turns out to be needed, propose a
     separate task.
   - **Done when**: the conditions in step 7, made concrete for this work.
   - **Stop when**: a limit on time or on the number of changed files, plus the
     conditions in step 8.
3. **Pin current behavior.** Write down the inputs, outputs, state changes, and
   failure behavior of the code in scope, including order, public names and
   arguments, and error types. Read the existing tests. If they do not cover
   that behavior, add tests against the current code first and make sure they
   pass. Tests that record what the code does now, right or wrong, are called
   characterization tests. Passing tests alone do not prove equal behavior:
   prepare the same inputs, including boundary values (empty, maximum, date
   boundaries), to compare outputs before and after.
4. **Measure before changing.** Measure complexity and duplication of the code
   in scope as `references/measurement.md` describes, and record the tool,
   version, settings, and files.
5. **Apply deterministic transformations first.** Before changing code by
   hand, let tools make the changes that are the same every time, in this
   order, and commit them separately from your own changes: the formatter, the
   linter's fixes marked safe, the fix attached to a rule (ast-grep, Semgrep),
   then a language codemod. Measure again afterwards, so that step 7 compares
   your changes, not the tools'. `references/change-principles.md`, principle 7.
6. **Change in small steps.** Move one boundary at a time, and keep the build
   and tests passing after each step. Keep commits that change behavior (there
   should be none) apart from restructuring commits. When a test fails, first
   find out whether behavior changed before you touch the test.
7. **Check that you are done.** All of these must hold:
   1. The goal is met, shown in code. For the example goal, walk through adding
      one status message and show the change stays in one function.
   2. The tests from step 3 and all existing tests pass, and the outputs for the
      comparison inputs match the ones from before.
   3. Measured under the same conditions as step 4, no function in scope got
      worse. When splitting lowered a number, also check that the number of
      states, the number of files or functions a reader must jump between,
      duplication, and public names and arguments did not grow.
   4. Read as a newcomer: you can follow the code from input to result, see
      which state changes and who owns it, and trace the failure paths. Names
      and responsibilities feel natural, and each abstraction makes reading
      easier rather than harder. Numbers alone do not decide this.
   5. The diff was reviewed independently (`references/change-principles.md`),
      including the design questions below.
   6. Nothing outside the agreed scope is in the diff.
8. **Stop** when any of these happens: the goal needs a change of behavior, the
   agreed limit is exceeded, or there is no way to check that behavior stays
   the same. Keep the steps done so far only if the tests pass and the
   comparison inputs from step 3 still give the same outputs for them;
   otherwise undo the changes. Either way, report what you learned and what
   work remains.
9. **Report** each item of step 7 as done or not verified, with the numbers
   before and after.

## Design questions for the review

Do not apply design principles as rules while writing code. Ask these questions
in the review, and state each finding as a concrete change scenario and place
in the code ("changing X also requires changing Y in `file:line`"), not as a
principle's name:

- Does one function, class, or module change for more than one reason (for
  example, both when wording on a screen changes and when the storage format
  changes)?
- Does code that makes business decisions call the database, the OS, an
  external API, or the current time directly, so tests cannot replace them?
- Is there an interface with one implementation, or a thin wrapper with one
  caller, added for a future that has not arrived?
- Where inheritance or interfaces are used, does each implementation keep the
  callers' assumptions (input range, exceptions, side effects)? Does any
  interface force implementers to provide methods they do not use?
- Are the owner of each state and its invariants clear? Are names and structure
  consistent with the surrounding code?
