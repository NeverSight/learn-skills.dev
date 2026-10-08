---
name: clean-up-comments
description: >-
  Clean up the comments on the current diff: rewrite docstrings and kept comments
  in plain, concise words, delete inline comments that narrate the code, and add a
  role docstring to complex methods and modules, all within the repo's lint rules.
  Touches comments only, never code.
disable-model-invocation: true
---

# Cleanup comments

You own the comments on the lines this diff changes.

Edit comments and docstrings only. Never change code, names, imports, or formatting outside a comment. When a comment exists only because the code is hard to follow, delete it and flag the code in the report; the user decides whether to change it.

## 1. Scope

By default, cover the branch: everything that differs from its merge base with the default branch, whether committed, staged, unstaged, or untracked. Find the default branch with `git symbolic-ref --short refs/remotes/origin/HEAD`, else `origin/main`, else `origin/master`. Take `git diff $(git merge-base HEAD <default>)` plus untracked files from `git status --porcelain`.

Narrow it when the user asks:

- **Uncommitted:** `git diff HEAD` plus untracked files.
- **Staged:** `git diff --staged` only.
- **A path:** only that path.

Collect changed lines with `-U0`. Comments outside these lines are out of scope, even in the same file. Tell the user the scope in one line before going further, such as "Scope: branch `foo` vs `origin/main`, 12 files".

Done when you have the list of changed files and line ranges.

## 2. Read the repo's comment rules

Read the enabled linter, pre-commit, and CI config, not only the prose docs. Note which docstrings a lint rule requires (and its exemptions), the docstring format (or whatever the changed files already use when no rule says), and the line length.

Done when you can state, per language in the diff, which docstrings are required, their format, and the line length.

## 3. Sort and fix each comment on a changed line

- **Directives stay untouched:** `type: ignore`, `noqa`, `pylint: disable`, `pragma`, `eslint-disable`, `@ts-expect-error`, `@ts-ignore`, `prettier-ignore`, `//go:` lines, shebangs, encoding lines, license headers, and Rust `// SAFETY:` blocks. Flag in the report any directive that names a rule the repo's linter doesn't have.
- **Inline comments that explain why stay inline**, rewritten to one plain line: a workaround, a constraint from a library, vendor, or protocol, a non-obvious reason, a limitation that looks like a bug, or a TODO or note with a ticket reference. Keep ticket references as written without looking them up. Do not move these comments into the docstring.
- **Every other inline comment is deleted:** narration of what the next line does, edit history ("previously this used polling"), references to the prompt, the chat, or the agent, commented-out code, section banners, and TODOs that name no real unfinished work.
- **Docstrings are rewritten** to say what the thing does for its caller, plus the arguments, returns, and errors the repo's format calls for, matching the current signature. Delete a docstring that only restates the name and signature, unless step 2 found it required.

Every comment you rewrite or add follows these rules:

- **Plain words.** Expand abbreviations and project codenames, and pick the everyday word over the technical one. Domain terms the codebase already uses are fine.
- **Short.** One line when one line does it. Cut filler like "This function is responsible for".
- **True today.** Describe the code as it is now, not how it got here.

Done when every comment on a changed line has been kept, rewritten, or deleted under one of the four kinds above.

## 4. Add role docstrings

List every function, method, class, and module the diff adds or changes the body of, and decide each one. It needs a role docstring when any of these hold: it coordinates several steps, it has callers in other modules, or it hands its output to something non-obvious. An existing docstring you rewrote in step 3 counts once it states the role.

For each one that needs it, search the whole repo for its callers and for what consumes its output; the diff shows only the callers that changed. Write the role in general terms: what it does for its callers and what it passes on. Do not name specific callers or files, because those go stale when code moves. Mention timing or ordering ("must run after auth", "safe to call twice") only when getting it wrong would cause a bug.

If more than about eight methods need a role docstring, split them into groups by file and spawn one read-only subagent per group on a mid-tier model, in parallel, with the prompt in `references/caller-search-prompt.md`. Each returns callers and handoffs with `path:line`. Write every docstring yourself from what they return.

Done when every item on the list has a role docstring or a one-line reason it needs none, and both go in the report.

## 5. Check

Run the repo's linters from step 2 on the changed files only, check-only, such as `ruff check --no-fix <files>` or `npx eslint <files>` without `--fix`. Never run a `fmt` or `fix` command; some configs autofix by default and some lint wrappers run formatters. Fix failures your edits caused, and leave the rest. If no linter can run, check line length by hand. Do not run tests or builds.

Then read the final diff and revert anything that isn't a comment or docstring line, including rewrites the linter made.

Done when no lint failure comes from your edits and the diff touches nothing but comments.

## 6. Report

Reply: how many comments you rewrote, deleted, and added. Then list the step 4 decisions, any code flagged as hard to follow with `path:line` and one line each, and the lint result.
