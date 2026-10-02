---
name: implement-to-pr
description: Implement a GitHub issue or the work agreed in the conversation, check it, and open a pull request that is ready for review.
disable-model-invocation: true
---

# Implement to PR

1. Work out what to build. If you were given a GitHub issue, read it and its comments with `gh issue view <number> --comments`. Otherwise, build what we agreed on in this conversation. Don't add anything beyond that.
2. If you're on the main branch, create a new branch with a short name that describes the work. Leave unrelated local changes alone.
3. Build it the way the rest of the codebase does things, and follow the repository's instructions. Add or update tests where the change creates or alters behavior that users or callers rely on. When removing behavior, remove its tests rather than asserting its absence.
4. Run the repository's usual checks (formatting, linting, type checks, tests, and build) and read through the whole diff. The work is done when everything the issue or conversation asked for works and every check passes.
5. Commit, push, and open a pull request into the main branch. That branch is usually `main` or `master`, and `gh repo view --json defaultBranchRef` tells you which. Don't open it as a draft. Write the title and description as described below, save the description to a temporary file outside the repository, and pass it with `--body-file`.

If anything does not work as expected, don't hesitate to ask questions so we can get it working right. That includes an unclear request, a check that fails for a reason you can't find, and code that doesn't behave the way the issue assumes. Ask instead of guessing or working around the problem.

When you're done, share the PR link. Never force-push or merge.

## Pull request title and description

Write both from the committed diff, the issue, and the check results, not from conversation memory. The readers are engineers who review many pull requests. Use plain words, short paragraphs, the most important point first, and backticks for code identifiers. Keep the description proportional to the change.

Title: the outcome in plain words that a reviewer understands without opening the PR, such as "Retry failed webhook deliveries with backoff" rather than "Update webhook logic".

Description, in this order:

```markdown
## Summary

Two to four sentences: what problem this solves, why it matters, and how behavior changes. A reader who stops here should know what the PR does. End with `Closes #N` when the PR fully resolves that issue in the same repository; otherwise reference it without closing it.

## Changes

The changes grouped by concern, each with the behavior before and after. Explain decisions a reviewer might question and the alternatives you rejected.

## How to review

Where to start, which parts need careful reading, and which are mechanical, such as renames, moved code, or generated files. Name any specific question you want the reviewer's judgment on.

## Verification

The commands run and their results, manual checks, and screenshots for UI changes. Say what was not tested and why.

## Risks and non-goals

What could break, such as compatibility, migrations, performance, or security, and what this PR deliberately does not do.
```

Always include Summary and Verification. Include the other sections only when they have real content; a one-file fix usually needs only those two. Never write a section that says "None".

Leave out file-by-file change lists, restatements of the diff, unticked checkboxes, secrets, absolute local paths, and raw command output.
