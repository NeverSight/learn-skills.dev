---
name: create-pull-request
description: Open a ready-for-review GitHub pull request for completed local changes, including any needed commit and push.
---

# Create Pull Request

Publish the completed change as one accurate GitHub pull request that is ready for review.

A request to open the PR authorizes creating a branch when needed, committing the in-scope changes, pushing without force, and creating the PR or updating a matching open one. Do these without pausing to confirm them. The request does not authorize merging, auto-merge, force-pushing, history rewrites, labels, reviewers, assignees, issue edits, or touching unrelated changes.

Stop and report only when:

- the change is empty, incomplete, or mixed with changes whose ownership is unclear
- a required check fails or cannot run
- publishing fails

## 1. Establish the change

- Read the repository instructions, the source issue if there is one, and a few recent commits to learn the repository's conventions.
- The head is the current branch unless the user names one. The base is the branch the user or repository instructions name, otherwise the repository's default branch. If the head is the base branch or HEAD is detached, create a branch named for the change.
- Review the full diff from the merge base with the base branch, plus staged, unstaged, and untracked changes. Stage only paths that belong to this change. Never stash, reset, clean, amend, or rebase to make publishing work.
- If an open PR from this head to this base exists, update it instead of creating another.

## 2. Verify

Run the checks the repository requires. If it names none, run the smallest checks that exercise the changed behavior, plus `git diff --check`. Reuse earlier results when the code they tested has not changed since. Never weaken tests or bypass failing paths to get a check to pass, and never report a check that did not run.

## 3. Commit and push

Commit the in-scope changes as one commit with a message in the repository's style. Push the head branch without force.

## 4. Write the title and body

Write both from the committed diff, the source issue, and the check results, not from conversation memory. The readers are engineers who review many pull requests. Use plain words, short paragraphs, the most important point first, and backticks for code identifiers. Keep the body proportional to the change.

Title: the outcome in plain words that a reviewer understands without opening the PR, such as "Retry failed webhook deliveries with backoff" rather than "Update webhook logic".

Body, in this order:

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

Write the body to a temporary file outside the repository and pass it with `--body-file`.

## 5. Publish and report

For a matching open PR, update it with `gh pr edit` if needed, and run `gh pr ready` if it is a draft. Otherwise run `gh pr create` with explicit `--repo`, `--base`, `--head` (`OWNER:BRANCH` for forks), `--title`, and `--body-file`. Never pass `--draft`. If creation fails or its output is unclear, check whether the PR exists before retrying.

Report the PR URL, the checks run with their results, and any CI checks still pending. Leave the PR open. Merge only if the user asks after receiving the URL.
