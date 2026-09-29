---
name: avoid-feature-creep
description: Keeps a change scoped to what was asked. Flags extra features, refactors, and 'while we are here' edits, and moves them to a suggestions list instead of the diff. Use when a request is small and the agent is about to expand it, when a PRD grows beyond its problem statement, or when the user says 'just do what I asked'.
---

# Avoid feature creep

The request sets the scope. Everything the diff contains should trace back to a sentence in the ask. Anything else is a suggestion, not a change.

## The core rule

Build what was asked. Not what would be nice, not what a senior engineer would also do, not what the codebase "should" have. If a line of the diff cannot be justified by the request, it does not belong in the diff.

This applies to product scope and to code scope. A PRD that grows past its problem statement has the same disease as a bug fix that ships with a refactor.

## Signals that creep is starting

Stop when you notice any of these:

- "While we're here" or "might as well" appears in your reasoning
- Adding a config option, flag, or parameter for a case nobody asked about
- Refactoring code adjacent to the change because it looked untidy
- Adding a second feature to make the first one feel complete
- Adding error handling for edge cases the user has never hit
- Adding tests, types, or docs for code outside the change
- Generalizing a one off into a reusable abstraction
- Copying a competitor feature without a stated user need
- A PRD section titled "Future" or "Nice to have" that keeps getting longer
- The change touches a file the request never implied

Each of these might be a good idea. None of them are in scope unless the user says so.

## What to do instead

1. Finish the ask. Ship the smallest change that fully answers the request.
2. Collect the extras as you go. Do not act on them.
3. Put them in one place at the end:
   - In a chat or PR summary, under a `Suggestions` heading, one line each
   - In a PRD, under `Out of scope` with a one line reason
   - In a repo with a `prds/` folder, append to the relevant PRD's `Out of scope` section
4. Let the user pick. "The agent thought so" is not approval.

Suggestions are cheap to write and free to ignore. Unrequested code costs review time, adds bugs, and blurs what the change was for.

## Stakeholders, including agents

Every feature request has a source: a PM, an exec, a user, a developer scratching an itch, or an AI coding agent. Treat them all the same way. Log the request, weigh it against the current scope, and defer it unless it solves the problem the work was started for.

AI agents are stakeholders now. They have opinions and they push. Common agent driven creep:

- "Let me also add error handling for edge cases you haven't hit yet"
- "This would be cleaner with a refactor"
- "You should probably add tests for this"
- "I added types for these additional scenarios"

If you are the agent, catch yourself doing this and move it to the suggestions list. If you are working with an agent, state the scope at the start of the session and treat its extras like any other stakeholder ask.

Before adding anything, ask:

- Does this solve the problem the request named?
- What is the smallest version that works?
- What happens if we never build it?

If the first answer is no, it goes in suggestions.

## Before and after

Request: "Add a `deletedAt` field to tasks and hide deleted tasks from the list query."

Before, the creeping version:

- Added `deletedAt` to the schema
- Added a `by_user_and_deleted` index
- Rewrote `list` to use the index
- Added `softDelete`, `restore`, and `purgeDeleted` mutations
- Added a cron to purge after 30 days
- Renamed `list` to `listActive` and updated three call sites
- Added a `showDeleted` argument "for the admin view later"

After, the scoped version:

- Added `deletedAt: v.optional(v.number())` to the schema
- Added the index and pointed `list` at it so deleted rows never load

Summary sent with the change:

```
Done: deletedAt field and list query now skips deleted tasks.

Suggestions
- A softDelete mutation to set deletedAt (nothing sets it yet)
- A restore mutation
- A cron to purge rows older than 30 days
- An admin flag on list to include deleted rows
```

Two lines of diff answered the request. Four lines of suggestions preserved every idea. The user decides what happens next.

## PRDs

A PRD earns each section by pointing back to its problem statement. When a PRD grows:

- Reread the problem statement. Cut anything that does not serve it.
- Move cut items to `Out of scope` with one reason each.
- If the cut items form a coherent feature, that is a second PRD, not a bigger first one.

## Checklist

- [ ] Every changed file is implied by the request
- [ ] No new config options, flags, or parameters the request did not ask for
- [ ] No refactors of adjacent code
- [ ] No second feature added to round out the first
- [ ] No tests, types, or docs added for code outside the change
- [ ] Extras are listed under `Suggestions` in the summary or `Out of scope` in the PRD
- [ ] The summary says what was done in one line before the suggestions
- [ ] If the user said "just do what I asked", the diff contains only that
