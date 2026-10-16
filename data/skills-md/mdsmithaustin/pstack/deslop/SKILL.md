---
name: deslop
description: "Remove AI slop from the code a branch changed, before a commit and without changing behavior: narrating comments, guards on states the types or the boundary already rule out, dead compatibility paths, unrelated edits, one-caller wrappers and speculative abstractions, casts that silence the type checker, and nesting an early return flattens. Use for /deslop, deslop it, clean the diff, strip the slop, or before any commit. Code only. The unslop skill cleans prose and the no-comments skill reviews comments."
---

# Deslop

Clean AI slop out of the code a branch changed, and leave behavior unchanged. Use it before every commit, and on `/deslop`, "deslop it", "clean the diff", or "strip the slop". It cleans code only. The **unslop** skill owns prose, and the **no-comments** skill owns the comment review.

## Scope

Use the caller's files or diff. Otherwise diff against the branch this one builds on, including the working tree and untracked files (`git status --short`): the pull request's base when one is open (`gh pr view <branch> -R <host>/<owner>/<repo> --json baseRefName`, with `<host>/<owner>/<repo>` from origin's fetch URL), else the branch it was cut from (`git branch -vv` or `git reflog show <branch>`), else `main`. On a stacked branch, `main` would pull the parent's commits into the diff. Edit only inside the hunks the branch added or changed. Read whatever the rules need to judge them: callers, types, existing helpers, and the rest of the file. Slop you notice elsewhere goes in the report and stays untouched.

## Process

1. Read the diff hunk by hunk and name the task each hunk serves. A hunk that serves none is rule 17.
2. Apply the rules below in order. Make the smallest edit. Delete before you rewrite.
3. Stop at a cut that needs a new shape, such as a type, a helper, or a state model. Flag it for the [Refactoring playbook](../poteto-mode/playbooks/refactoring.md). Deslop never adds abstraction to remove slop.
4. Prove behavior unchanged on the real artifact. Run the tests the diff touches and the type check. A test that must change to pass means behavior changed. Revert that cut.
5. Hand what remains to the neighbors. A comment that rules 1 to 3 do not settle needs the comment review before you report. Use the **no-comments** skill on those comments. If its review changes code, run step 4 again. Then use the **unslop** skill on names, messages, and kept comments.
6. Report in the format below.

## Rules

Rule numbers are stable ids that other skills cite. A removed rule leaves a gap. Each rule names the target, its tell, and the fix.

### Comments

1. **Narrating comments.** The comment restates the line below it or names a phase (`// increment count`, `// Phase 1: add cards`). Delete it.
2. **Commented-out code and removal markers.** Code behind comment markers, or a `// removed` note. Delete it.
3. **Keep list.** License headers. Non-obvious behavior forced by an external dependency, platform, vendor, or protocol you cannot reshape. `prettier-ignore`. Doc comments that define a public API contract. Issue or RFC links that explain a constraint code cannot express. A kept comment is still prose, so step 5 sends it to the **unslop** skill.

### Guards

4. **Guard on an impossible state.** A null check on a value the types or the boundary never leave null, `instanceof` on an already narrowed type, a length check on a tuple, a default for an argument every caller passes. Delete it. Trust the type.
5. **Defensive wrapping on a trusted path.** A `try/catch` or a fallback around an internal call that cannot fail the way the handler expects, or a handler that swallows the error. Remove the wrapper, or let it throw. A silent fallback that hides an unclear invariant is rule 4, and the report names the invariant.
6. **Repeated validation.** A check that re-parses or re-validates data the boundary already parsed. Delete the inner copy.

A guard at a system boundary (user input, network, file, environment, external API) stays. A guard a test demands stays, and the test is the proof.

### Dead paths

7. **Compatibility shims.** An old path kept beside the new one, an alias or re-export kept "for callers" with no caller, a deprecation notice for code this branch replaced. Delete a shim with no caller. When every caller sits inside the branch's hunks, migrate them and delete the shim in the same change. A shim with a caller outside those hunks stays, and the report names it, because migrating that caller would edit outside Scope.
8. **Unused parameters, exports, and flags.** A parameter nothing passes, an export nothing imports, an option with one value, a flag with one reachable branch, a branch marked temporary. Delete it.
9. **Debug residue.** Debug logs and prints, tagged or not, throwaway prototypes, variant switchers. Delete them.

A symbol on the package's public surface (an entry-point export, a documented API) stays even with no caller in the repository, because its callers live outside it. Delete it only when the task removes it from the public API. Otherwise list it under "Did not touch".

### Types

10. **Checker silencers.** A cast to `any` or `unknown`, an `as` assertion, or a suppression comment whose only job is to make the type checker pass. Fix the type or delete the cast.

### Shape

11. **One-caller wrappers.** A function, helper, or adapter with one caller that passes its arguments through. Inline it.
12. **Speculative generality.** An abstraction, parameter, hook, or seam with one implementation and no second use in the task. Inline it back until a real need shows.
13. **Re-implemented helpers.** Code that does what a helper in the codebase already does. Call the existing one.
14. **Nesting an early return flattens.** A guard clause whose body is the rest of the function. Return early and dedent.
15. **Copy-paste with variation.** The same shape twice inside the diff with small differences. Extract only when the codebase already names the shared shape. Otherwise three similar lines stay.
16. **Structure the diff cannot fix.** A new conditional bolted onto an unrelated flow, a one-off boolean or nullable mode, repeated conditionals on one shape. Flag it for the Refactoring playbook under **principle-model-the-domain**. Do not fix it here.

### Scope

17. **Unrelated edits.** Formatting churn, renames, import reorders, or syntax modernizing in code the task did not need to touch. Revert the hunks git can restore: those committed on the branch, and those you wrote this session. An uncommitted hunk you did not write stays, and the report names it, because reverting it would destroy work no commit holds. `git diff <base>...HEAD` shows the committed hunks and `git diff HEAD` the uncommitted ones. Revert hunk by hunk, never by restoring a whole file, so an uncommitted hunk in the same file survives. To revert a committed hunk, edit its lines back by hand, or reverse only that hunk taken from `git diff <base>...HEAD -- <file>`. Reversing that whole diff also undoes the file's task work, and `git diff <base> -- <file>` also carries the file's uncommitted hunks.
18. **A behavior change inside cleanup.** A hunk that changes what the code does under a cleanup label. Split it out and name it in the report.
19. **Style against the file.** A pattern the surrounding file does not use. Match the file.

## Report

One to three sentences, then:

- Counts by rule id, and the files touched.
- Hunks reverted under rule 17, and the uncommitted unrelated hunks left in place.
- Flags handed to the Refactoring playbook (step 3, rule 16).
- The comments step 5 gave the **no-comments** skill, and what it did with each.
- A "Did not touch" list of slop outside the scope.
- The test and type-check commands with their results.

`CREDITS.md` names the sources this skill drew on and the sentences it carried over.
