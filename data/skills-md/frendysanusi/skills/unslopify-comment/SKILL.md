---
name: unslopify-comment
description: >
  Keeps code comments and docstrings few, short, and load-bearing. Use on any
  coding task that writes or edits comments, docstrings, JSDoc, or doc blocks.
  Also use when the user says "too many comments", "comments are too long",
  "clean up the comments", "unslopify comments", "remove the AI comments", or
  says the code reads like AI wrote it. Defaults to writing no comment, and
  allows one only when it says something the code cannot. Runs while writing
  and as a cleanup pass over existing files or a diff. Only touches comments
  and docstrings, never the code.
---

# Unslopify comment

Write a comment only where the code cannot speak for itself, and keep it short.
Most comments an agent writes repeat the line below them.

## The test

Ask whether the next engineer would be surprised by this. If not, write no
comment.

Value and length are separate questions. A real constraint is one line about the
constraint, not a paragraph. Comments survive a review they should not because
the content is genuinely useful and nobody checks the size.

## While writing

Write the code first, then add a comment only where the test passes.

At most one comment per logical block. When every line has one, the reader has
to check all of them to find the one that matters.

One line. Two only when the second carries a fact the first does not. At three
lines you are writing documentation, so move it to a doc, the commit message, or
the PR body.

Stay under the comment density of the code around you. A file with four comments
in three hundred lines has already told you its convention.

Write short and plain, in sentence case. Skip the reasoning chain, the issue
number, and the version that fixed it. Git records those better.

## What earns a comment

- A constraint from outside the code: an API's retry behaviour, a protocol rule,
  a platform bug you are working around.
- A decision with a discarded alternative: why this way, when the obvious way
  looks better.
- A trap: code that looks wrong but is correct, or looks safe but is not.
- A domain rule the code enforces without naming it, such as a rounding
  convention or a regulatory cutoff.
- Units and assumptions the types do not carry: cents not dollars, UTC not
  local, caller already holds the lock.
- Licensing and legal notices.

Two facts, so two lines:

```js
// Stripe retries webhook deliveries for up to three days.
// Ignore duplicates by event ID.
```

## What never earns one

- Restating the line: `// Initialize the counter` above `let count = 0`.
- Restating the declaration: `// User class` above `class User {}`.
- Workflow narration: `// Step 1: validate`, `// First...`, `// Next...`. Flow
  that is hard to follow is a structure problem, and a comment will not fix it.
- Section banners: `// ===== ROUTES =====`, box drawing, ALL CAPS labels.
- Empty labels: `// Main logic`, `// Helper function`, `// Note: this is
  important`. A category carries no fact.
- Vague TODOs: `// TODO: improve this`. Keep a TODO only when it names a task
  someone could pick up.
- End markers: `} // end if`, `# End of function`.
- Decorative emoji: rocket, checkmark, lock.
- Change narration: `// Replaced the old loop because it was O(n^2)`. Describe
  the code as it is. Change logs and migration guides are the exception.
- Commented-out code. Delete it; git has it.

## Docstrings

Docstrings are where the length problem lands, because the format invites a
field for every parameter whether the parameter needs one or not.

Write none when the name and signature already say it.
`calculateTotal(items: LineItem[]): Money` needs no block.

Write one when the contract is invisible in the signature: what happens on empty
input, whether the argument is mutated, what it raises, what it costs, whether
it is safe to call concurrently.

Never write a `@param` that restates the parameter name, a `@returns` that
restates the return type, or a summary that restates the function name.

When a linter demands full docs, the linter wins. Write the shortest form that
satisfies it, put the real content in the one field that carries a fact, and say
that is what you did.

## Cleanup pass

When pointed at files, a diff, or a PR:

1. Read each file in full. A comment's value often depends on code outside the
   hunk.
2. Give every comment one verdict: **keep** when it passes the test at its
   current length, **shorten** when the fact is real and the length is not, or
   **delete** when it adds nothing the code does not show. For a shorten, write
   the line it should become.
3. Apply the comment and docstring edits only.
4. Report the counts, and name anything you kept that looks like slop but is
   not, so the user can disagree.

Leave comments the user wrote alone. Flag them if they look stale or wrong and
let the user decide.

## Boundaries

Change comments and docstrings only. Leave executable code, identifiers,
imports, formatting, whitespace, and control flow untouched, even when the code
beside a deleted comment is obviously improvable. Say what you noticed instead.

A repo convention, a linter rule, or a documented house style outranks this
skill. Name the conflict instead of silently breaking either one.

"stop unslopify-comment" or "normal mode" reverts to ordinary commenting.
