---
name: write-commit-message
description: Use this skill when drafting, choosing, or revising a Git commit message from a concrete, coherent change and its resolved scope. Express the commit-specific what and why in the repository's established style. Do not use it to decide where project knowledge should live, edit repository artifacts, or perform Git operations.
---

# Write a Commit Message

Write a message that remains useful when read later without the surrounding
conversation.

## Contract

- **Input:** the exact logical change being committed and, when available, its
  diff, nearby commit history, and resolved decisions about what belongs in the
  message.
- **Output:** one commit message with a subject and an optional body. Return
  only the message unless the user asks for explanation or alternatives.
- **Boundary:** describe the actual commit, not the whole task or pull
  request. Do not decide where project knowledge belongs, edit artifacts, stage
  files, commit, push, or decide how to split changes.
- **Failure:** if the change or commit scope is missing, ambiguous, or mixes
  unrelated concerns, do not invent a message. Ask for a resolved scope before
  writing; keep information that belongs in a durable project artifact out of
  the message.

## Workflow

1. Establish the exact commit scope from the user's request and the available
   diff. For a working tree, the smallest useful evidence is `git status
   --short`, `git diff`, and `git diff --cached`. Do not mutate the repository.
2. Inspect recent commit messages when available, unless the caller limits the
   evidence. Match the repository's established choices for types, scopes,
   capitalization, punctuation, wrapping, issue references, and breaking-change
   notation. Do not impose a generic format over a stable local convention.
3. Distill the purpose of the change:
   - the subject says **what changed** or what resulting behavior/design exists;
   - the body, when needed, says **why it changed**, including constraints,
     compatibility impact, or a non-obvious trade-off.
4. Confirm that the supplied scope is one coherent commit. If it is not,
   do not write an umbrella message; wait for a resolved commit boundary before
   drafting.
5. Run the final check below, then return the message exactly as it should be
   used.

## Subject

When the repository uses Semantic or Conventional Commits, use:

```text
<type>(<scope>): <imperative subject>
```

The scope is optional. Choose the narrowest conventional type that describes
purpose, such as:

- `feat` — add or extend user-visible behavior;
- `fix` — correct incorrect behavior;
- `refactor` — change structure without intentionally changing behavior;
- `perf` — improve performance;
- `docs` or `test` — change documentation or tests without production behavior;
- `build` or `ci` — change packaging, dependencies, build, or automation;
- `chore` — maintenance that has no more meaningful type.

Use a scope only when it identifies a stable subsystem. Avoid vague scopes such
as `src` or `core`, and do not invent a scope to fill the parentheses.

Make the subject:

- specific enough to distinguish this change from nearby commits;
- imperative and concise;
- about the observable intent or resulting design, rather than edited files,
  function movements, or work performed;
- free of vague words such as “fix bug”, “cleanup”, or “improvements”.

If recent history uses plain imperative subjects instead of a Semantic prefix,
follow that local style. Consistency with the repository outranks a generic
format.

Prefer:

```text
fix: preserve clipboard contents during text insertion
```

over:

```text
fix: save and restore NSPasteboard contents
```

The first names the corrected behavior; the implementation remains in the diff.

## Body

Omit the body when the reason is obvious from the subject and diff. Otherwise,
write one or more concise paragraphs explaining information that the diff does
not make clear, such as:

- the problem with the previous behavior;
- why the chosen approach was necessary;
- constraints or compatibility consequences;
- intentionally preserved behavior or a non-obvious trade-off.

Do not turn the body into a list of files, functions, or mechanical edit steps.
Those details belong in the diff. Wrap lines according to the repository's
convention when one exists.

For a breaking change, use the repository's established notation (commonly
`!`) and explain the compatibility impact or migration requirement. Add issue
references or other trailers only when the repository or user calls for them;
do not fabricate them.

## Final check

Before returning the message, verify that:

- it describes only the resolved commit scope;
- the type, if used, matches the commit's purpose;
- the subject clearly states what changed and uses the local style;
- the body, if present, adds the reason or important consequence rather than
  narrating the diff;
- implementation details appear only when they explain a meaningful choice;
- breaking changes, issue references, and trailers are accurate;
- unrelated changes are not hidden behind a broad subject.

Return only the final commit message unless the user explicitly requests more.
