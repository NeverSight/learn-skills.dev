---
name: code-comments
description: House rules for writing, reviewing, and pruning code comments, doc comments, docstrings, and TODO/FIXME notes in any codebase — what earns a comment, what is noise, where an issue reference belongs, and the drift test every kept comment must pass. Use whenever you are about to write or edit a comment, add developer documentation to a new type/function/property, decide whether documentation belongs on new code, audit the comments in a diff before committing or opening a review, or are asked to "add documentation", "document this", "comment this", "explain this code inline", "clean up comments", or "remove unnecessary comments".
license: Internal
metadata:
  version: "1.0"
  category: quality
---

# Code Comments

The rule: **comments earn their place only when they explain something the code cannot.** This skill covers what clears that bar, what doesn't, and the traps that produce most of the comment churn in review.

The default is no comment. Prefer a clearer name or a smaller function over a comment explaining an unclear one. When you do write one, keep it short and match the terseness of the surrounding code.

## What earns a comment

Information the code genuinely cannot carry:

- **A constraint the language or tooling can't enforce.** Ordering, threading or concurrency requirements, synchronous operations, or an invariant that holds across call sites.
- **A gotcha or edge case** a future editor would otherwise re-break. Non-obvious units or domain quirks count.
- **A workaround for platform, dependency, or external-service behavior** — name the version or the bug, so someone can test whether it's still needed.
- **Why this approach, when an obvious alternative was rejected** — specific enough to stop someone redoing it. "We tried X and it broke Y because Z."
- **A warning that a plausible-looking cleanup would break something.**
- **Historical context on a narrow piece of code**: why a legacy path still exists, migration state, the issue behind a quirk (see placement rules below).

A one-line comment that stops the next person re-breaking an invariant is worth keeping even if it looks trivial. Occasionally a comment genuinely has to be long to capture what it must — that is the exception, not the convention.

## What doesn't

- **Restates the code.** The code is the better version of that sentence.
- **Narrates structure**, or walks through the following lines step by step.
- **Template or scaffolding documentation** — anything copied from a skill or pattern doc, and comments that only re-spell the signature (`The view model.`, `Flat list of every identifier.`). Those are filler and should be stripped in review.
- **Describes the change rather than the code.** "Routed through X rather than a bare Y", "was previously Z", "added for search v2". Version history and the change description already say this, and it's wrong by the next release.
- **Justifies your edit**, even worded as a timeless invariant. If a comment only makes sense to someone reading the diff, delete it and put the context in the change description.
- **Reproduces the investigation.** Measurements, event traces, or what CI artifacts show are evidence for a decision already taken. They constrain nothing a future editor could get wrong.
- **Duplicates documentation that lives elsewhere.** Point at the stable source in a clause, or say nothing.
- **Commented-out code**, and comments that repeat what the enclosing test's name already says.
- **`TODO`/`FIXME` with no issue or owner.** Add the issue reference, owner, or removal condition, or delete it.

Out of scope for these rules: license headers, generated-file banners, navigation markers, linter and formatter directives, and build-configuration directives.

## Trap 1: don't calibrate on the file you're in

**Long doc blocks already in a file are likely debt, not precedent.** Writing a long block and reasoning "it's shorter than the one above it" is how the debt grows.

This is the single most common failure mode when reviewing your own work, because AI agents reproduce whatever style surrounds them. If you brief a review tool to "judge against the file's conventions", you will get the file's conventions back.

Judge every comment on its own merits.

## Trap 2: issue references are about placement, not permission

An issue reference is not banned. It's a question of what the comment is attached to.

- **Appropriate** on something narrow and weird: a workaround for one call site's quirk, an edge case, a line that looks wrong until you know the circumstance. There the issue *is* the missing context.
- **Not appropriate** on the documentation of a shared or public API the rest of the codebase will adopt. It makes the adopter think the API exists only to address that issue rather than being general-purpose, so they may assume it doesn't apply to their case or hesitate to use it. A shared API's documentation states the general contract. Which bug prompted it belongs in version history.

## The drift test

Apply this to every comment you're about to keep:

> Would this become false if someone renamed a symbol, changed a constant or layout value, added an enum case, reordered the code, ran in a different environment, or the upstream bug got fixed?

If yes, it must either name the thing it depends on — so the next editor sees the coupling — or it should go. A comment that quietly goes wrong in six months is worse than no comment.

Brittle anchors to avoid: line numbers, "the method below", counts ("all three cases"), a literal value duplicated from the code, a symbol name a rename would orphan. Measurements taken in one environment are a clear offender — literal coordinates, distances, durations, and percentages can all be falsified silently by a routine change.

## Where the cut material belongs

Nothing here says the information is worthless — only that the comment is the wrong home:

| Material | Home |
|---|---|
| What we found, what we tried, what the evidence was | Commit message / change description |
| Investigation writeup, measurements, artifacts | The issue or investigation record |
| "This branch is covered" | A test name |
| A value the comment repeats | A named constant |
| An invariant the comment asserts | An assertion, precondition, or test |
| How to set up or operate tooling (local environments, CI, scripts) | Team docs or a skill file |

## Examples

Revise — the comment states *what*; the *why* is the only part worth keeping:

```text
// Before
/// Sends the request and retries it if necessary.
sendRequest(request) { ... }

// After
/// The upstream service treats immediate retries as duplicates, so retries must remain delayed.
sendRequest(request) { ... }
```

Remove — every sentence is either the signature re-spelled or the change described:

```text
// Before
/// Coordinates background tasks.
/// Now routed through `TaskQueue` instead of starting workers directly.
TaskCoordinator { ... }

// After
TaskCoordinator { ... }
```

## Self-check before committing

Run this over every comment your diff added, and every pre-existing comment whose adjacent code you changed (the code moved out from under it, so it is the highest-value drift candidate):

1. Does it carry something the code cannot? If not → remove.
2. Does it describe the change, the investigation, or your reasoning for the edit? → remove; move the content to the commit, review, or issue.
3. Does it pass the drift test? If not → name the dependency, or remove.
4. Is an issue reference sitting on a shared or public API's documentation? → move it to the narrow call site, or drop it.
5. Could it be a better name, a smaller function, a constant, an assertion, a precondition, or a test name instead? → say which, and that the comment goes away with it. Propose the refactor; don't perform it as part of a comment cleanup.
6. Is it longer than a clause or two? → compress.

For a full audit of an uncommitted diff, use the `code-review-changes` skill — it applies these rules to every comment in the diff and reports Keep / Revise / Remove verdicts.
