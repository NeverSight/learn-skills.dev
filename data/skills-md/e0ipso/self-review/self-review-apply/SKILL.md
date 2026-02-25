---
name: self-review-apply
description: Parse self-review XML feedback and execute the review comments as organized tasks
metadata:
  disable-model-invocation: "true"
  argument-hint: "[review.xml path]"
---

# Apply Self-Review Feedback

Read structured review feedback from a self-review XML file and execute the changes.

## XML Reference

Non-obvious semantics (keep in sync with `assets/self-review-v1.xsd`):

- **Line number pairing:** A comment has exactly one pair — `new-line-start`/`new-line-end` (for
  added/context lines) OR `old-line-start`/`old-line-end` (for deleted lines). Never both. If
  neither pair is present, it's a file-level comment.
- **`viewed` attribute:** `true` = reviewer looked at this file. `false` = reviewer did not mark it
  as viewed. Distinguishes "reviewed, no comments" from "not yet reviewed."
- **`path` on renames:** For renamed files (`change-type="renamed"`), `path` is the **new** path.
- **`change-type` values:** `added`, `modified`, `deleted`, `renamed`.

## 1. Read the Review XML

Read the XML file from `$ARGUMENTS` or default to `./review.xml`. Stop if the file does not exist.

## 2. Validate the XML

Use the Bash tool to run `xmllint --schema assets/self-review-v1.xsd <review-xml-path> --noout`
(where `assets/` is relative to this skill's directory). If validation fails, stop and report the
xmllint errors to the user. If `xmllint` is not installed, warn the user and continue without
validation.

## 3. Load Context

Check the `<review>` root element attributes to determine the review mode and load context:

- **Git mode** (`git-diff-args` and `repository` attributes present): Use the Bash tool to run
  `git diff <git-diff-args>` from the `repository` path. This gives you the same diff the reviewer
  saw. If the diff is too large, limit to files that have comments.
- **Directory mode** (`source-path` attribute present): Read each file listed in the review from the
  `source-path` directory (file `path` attributes are relative to it). Skip deleted files. If a file
  is too large, read only the line ranges referenced by comments (with surrounding context).

This context is essential — without it you're working blind.

## 4. Execute the Feedback

Skip files with zero comments. For files with comments, create one **TaskCreate** task per file,
then spawn subagents to work on independent files concurrently. For small reviews (3 or fewer
files **with comments**), apply changes directly without subagents.

For each file:

1. **Load attachments for this file.** For each comment with `<attachment>` elements, read the
   referenced image file using the Read tool to include it as visual context. The `path` attribute
   contains a relative path from the XML file to the image. If the image file does not exist, note
   this and proceed with text-based feedback only.

2. **Apply suggestions bottom-to-top.** Sort suggestions by line number descending so that
   insertions and deletions don't invalidate line numbers of subsequent suggestions. For each
   `<suggestion>`, find `original-code` in the file and replace it with `proposed-code`. Use line
   numbers as hints but match on text to handle drift.

3. **Address all other comments.** Read the referenced lines, understand the `<body>`, and implement
   the change. Use your judgment. Every comment category is actionable — including `question`, which
   often implies a change is needed. If a question is purely informational (no code change needed),
   answer it in the summary instead.

4. **Complete all changes for one file before moving to the next.**

## 5. Summary

After all feedback has been applied, output a clearly delimited summary section.

### Changes Applied

List each change that was made, grouped by logical unit of work (e.g., "refactored validation logic",
"updated API error handling") rather than by file. Keep entries concise (one line per change).

### Questions & Answers

For every `question` category comment in the review:

- Quote the question.
- Provide your answer.
- State explicitly whether the question resulted in a code change (`Changed` or `No change`).
