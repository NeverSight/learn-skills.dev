---
name: no-comments
description: 'Use when writing, editing, or reviewing code in any language. The rule is one thing: never write a comment on a line you add or change. Covers what to write instead - intent-revealing names, extracted functions, structure that makes the trap impossible, a test that fails when the claim stops being true, and rationale recorded in the PR, the commit message, an ADR or the wiki. Also use when deciding how to make code clear enough to need no comment: naming, extraction, types that make an illegal state unrepresentable, guard clauses, and tests that carry the claim. Also use when a diff adds comments, docstrings, JSDoc, test narration such as Arrange/Act/Assert, section banners, TODO or FIXME markers, or commented-out code. Also use to decide whether something is a comment or a machine-read directive such as eslint-disable, @ts-expect-error, noqa, a shebang, or a license header.'
---

# No Comments

Code that explains itself, with nothing written beside it.

This changes what you **write**: every line you add or change carries no comment. It never changes what is already in the file.

## Scope and precedence

Three hard limits. They outrank everything else in this document.

1. **The prohibition covers lines you add or change.** New lines and changed lines, source and tests alike. It is not a licence to strip comments out of code you did not write.
2. **Machine-read directives are not comments.** A tool reads them, and deleting one changes what that tool does. `eslint-disable`, `@ts-expect-error`, `# noqa`, `//go:build`, a shebang, a license header a legal policy mandates: leave every one of them exactly as it is. The per-language list is in [references/pragmas.md](references/pragmas.md).
3. **Correctness outranks the rule.** Never contort the code, drop a guard, weaken a type, or leave a real hazard unrecorded to avoid writing a comment. Restructure first. When the only honest form is prose, the prose goes outside the source.

There is no "unless the code is non-obvious" clause. That clause was tried, and it was used to justify a comment every single time, because every comment feels non-obvious to the person writing it.

## The one rule

**Never write a comment on a line you add or change.**

Reaching for a comment is a signal, and the signal is that the code is not clear enough yet. What you do with that signal is the ladder below.

## What to do instead

Work the ladder in order, and stop at the first rung that makes the code clear. Order matters: a rename costs nothing and improves every call site, a new type costs a review, and prose outside the source costs a reader a trip. Most comments die on rung one or two.

1. **Rename.** The comment says what something is, what unit it is in, or what it returns. Those words belong in the identifier, where every call site gets them. Stop here if the name now answers the question.
2. **Extract.** The comment heads a block, or explains a condition. The block is a function and the comment is its name; the condition is a predicate and the comment is its name. Stop here if the caller reads like the step list.
3. **Model it in a type.** The comment states a rule — which values are legal, that something may be absent, that this string is an identifier of one particular kind, that one thing must be validated before another. A type states the rule once and enforces it everywhere. Stop here if the illegal case can no longer be written.
4. **Restructure so the trap is impossible.** The comment warns. Ask what makes the hazard reachable and take that away: a guard clause, a single call site, a dangerous operation made private behind a safe wrapper, a second step that takes what only the first can produce. Stop here if there is nothing left to warn about.
5. **Write a test that states the claim.** The comment asserts a behaviour — a retry count, a boundary, the guarantee a workaround buys. The test name carries the sentence, and CI checks it on every push. Stop here if the claim is now enforced.
6. **Write it down outside the source.** What is left is genuine prose: why this trade-off, what you rejected, a quirk in someone else's contract, work you are not doing now. It goes in the PR description, the commit message, an ADR, the wiki, or the tracker. Never in the source.

Two rules about the ladder itself. **Never skip to rung six** because the first five look like work — rationale in a pull request does not excuse a function nobody can read. And **never stop below rung six with the prose unwritten** — a restructure that silently discards a real reason is not a win.

The technique catalogue for every rung is in [references/readable-code.md](references/readable-code.md): naming, extraction, types, control flow, tests, failure messages, and module shape, each one keyed to the comment it removes, in language-agnostic notation. Read a section when a rung is not obvious, not on every edit.

## Absolutely never

- **Explanatory comments**, including "why" comments and rationale. Rationale belongs on rung six: the pull request, the commit message, or an ADR.
- **Doc blocks** — JSDoc, TSDoc, docstrings, Javadoc, Scaladoc, Go doc comments — on anything, public or private. A typed signature and a good name are the documentation.
- **Test narration** — `// Arrange`, `// Act`, `// Assert`, `// given`, `// when`, `// then`. Blank lines already separate the phases, and the test name already says what is asserted.
- **Section banners**, dividers, decorative separators. A file that needs internal signposting is a file that wants splitting.
- **`TODO`, `FIXME`, `XXX`, `NOTE`, `HACK`.** An unowned marker in source is work nobody scheduled. File it in the tracker.
- **Commented-out code.** Delete it. Git remembers.
- **Comments that restate the code.** Pure cost.

Two ways people smuggle prose past this rule. Both are forbidden.

- **Appending prose to a real pragma**, so the line rides in as a directive: `// eslint-disable-next-line no-await-in-loop -- we need serial writes because the vendor API locks the row`. The pragma stays; the sentence after it does not.
- **Hiding a paragraph in a string, a log line, or a test name**: `logger.debug("NOTE: the second call must come after the flush")`, or a test called `testThatWeMustNotReorderTheseTwoCallsBecauseTheVendorLocksTheRow`. A comment in a costume is still a comment.

## Not comments — leave these alone

These are machine-read directives, not prose:

- **Linter and compiler pragmas**: `eslint-disable*`, `@ts-expect-error`, `@ts-ignore`, `prettier-ignore`, `# noqa`, `# type: ignore`, `//nolint`, `//go:build`, `#[allow(...)]`, `@SuppressWarnings`, `// scalafix:ok`, `# rubocop:disable`.
- **Shebangs**: `#!/usr/bin/env bash`.
- **Codegen markers**: `Code generated by ... DO NOT EDIT.`, `@generated`.
- **License and copyright headers** a toolchain or a legal policy mandates.
- **Annotations a framework parses** out of comment syntax.

Two questions decide it:

1. Does a tool read this line?
2. Would deleting it change behaviour — a build, a lint result, coverage, a generated file?

Yes to both means it is a directive: leave it, and never add one to carry prose. Anything else is a comment. When you cannot answer both questions, leave the line alone; a stray comment costs a review note, and a deleted pragma costs a broken build.

The full per-language list is in [references/pragmas.md](references/pragmas.md). Read it when you are unsure about a specific token, not on every edit.

## Pre-existing comments

Leave them alone. Editing a file does not make its comments yours to clean up.

Three reasons: it inflates the diff, it buries the real change from reviewers, and it discards context you did not write and cannot fully judge.

Two consequences worth being explicit about:

- **A comment your change made wrong is deleted, not rewritten.** That is the one case where you touch someone else's comment, and the fix is to remove the stale line — never to write a fresh comment in its place.
- **A file whose existing comments follow a convention you are told not to write** gets nothing added and nothing removed. Test narration everywhere in the file is not permission to narrate your test, and it is not an invitation to strip theirs.

A comment sweep is its own change, with its own PR, and only when someone asks for it.

## By situation

The nine cases that come up most. The move behind each one is in [references/readable-code.md](references/readable-code.md).

| Situation | No | Yes |
|---|---|---|
| A non-obvious algorithm | A paragraph above the loop | A named function per step, and a test per boundary |
| A magic number | `900 // 15 minutes in seconds` | `sessionIdleTimeoutSeconds = 15 * 60` |
| A workaround for an upstream bug | `// works around vendor bug #221` | A named wrapper, the vendor issue linked in the PR, a test that fails when they fix it |
| An ordering dependency between two calls | `// call flush() first` | One function that does both, or a type the second call needs from the first |
| A public API surface | A doc block on every export | Precise types, honest names, an example in the README |
| A test's arrange, act, assert | `// Arrange` and friends | Blank lines between the phases, and the assertion in the test name |
| A dense regex | The pattern explained in prose above it | A named constant per part, composed, with a table-driven test |
| Work you want to leave behind | A marker in the source | An issue in the tracker, linked from the PR |
| A quirk in someone else's payload | The quirk explained at the parse site | A named constant or branch, and the quirk written up in the wiki |

## Do not overcorrect

| Overcorrection | Looks like | Fix |
|---|---|---|
| Stripping someone else's comments | A three-line change with forty deleted comment lines | Touch only what your change made wrong. |
| Deleting a pragma to satisfy the rule | `@ts-expect-error` removed, the build now red | Pragmas are directives. Leave them. |
| Forty-character identifiers | `orderThatHasBeenValidatedAndPersisted` | Name the concept, not the history. `persistedOrder`. |
| One extracted function per statement | Six one-line helpers called once each | Extract a block that has a name, not every line that has one. |
| Smuggling it into a log line or a string | `logger.debug("must run before flush")` | That is a comment. Restructure so the ordering cannot be got wrong. |
| Recording the rationale nowhere at all | A silent restructure, no PR text, no commit body | The comment moves out of the source. It does not vanish. |

The point was never fewer words. It was words in the place that keeps them true.

## Final pass before you commit

Read your diff once and ask:

1. Did I add any `//`, `#`, `/* */`, `"""`, or `<!-- -->` on a line I touched?
2. Is every comment still in this diff one that was already there?
3. Did I delete or reword a comment I did not write?
4. Is any comment I removed one my change actually made false?
5. If I wanted to explain something, where did that explanation go — PR, commit, ADR, wiki, tracker?
6. Does any name in this diff still need a comment to be understood?
7. Did I leave every pragma, shebang, and mandated header intact?
8. Is there a marker or a block of commented-out code left behind?
9. Did I put prose in a string constant, a log line, or a test name instead?
10. Would a reader need anything outside this code to follow it?

Fix what you find, then commit. Never show this pass to the user.

## Red flags

These thoughts mean you are about to write a comment.

| Thought | Reality |
|---|---|
| "This one is genuinely non-obvious." | Every comment's author thought that. Work the ladder from rung one. |
| "The next reader will not know why." | Correct, and the PR and the commit message are where they will look. |
| "It's a public API, so it needs a doc block." | Types and names are the contract. A doc block duplicates them, then drifts. |
| "It's only a TODO." | An unowned marker is work nobody scheduled. The tracker owns it. |
| "The test needs Arrange, Act, Assert to be readable." | Blank lines separate the phases. The name states the claim. |
| "I'll add the comment now and clean it up later." | Nobody comes back. It ships, then it rots. |
| "The file is already full of comments, so mine matches the style." | Their comments stay, and you still add none. Consistency is not a licence. |
| "A comment is cheaper than a refactor." | It is cheaper today and wrong by next quarter. The refactor is the cheap one. |
| "Nobody will read the PR description." | A reviewer reads it now and a git archaeologist reads it later. A stale comment misleads both. |
| "I need the comment to explain the workaround." | Name the workaround, link the upstream issue in the PR, and write the test that fails when it is fixed. |
| "I got to rung four and the code is clear, so the reason can go unwritten." | Rung six is not optional. A discarded reason is a reason someone re-derives wrong. |
