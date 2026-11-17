---
name: fix-failed-build
description: Fix a specified OneDev build failure in the current checkout.
---

# Fix a failed OneDev build

Use configured `tod` and the build reference from the prompt. Ask for the
reference if it is missing. Keep the current checkout. Verify that
`git symbolic-ref --short HEAD` identifies a branch and that
`tod project current` identifies the build's project.

## Diagnose the failure

Read `tod build get <build>` and `tod build get-log <build>`. Check the
project and `commitHash` in the build detail against the checkout. Use the
failing commit as evidence and verify that the fix applies to the current
branch before editing.

If the log says a required dependency failed, get that build's detail.

- Cancelled dependency. Report it as the blocker and stop.
- Failure on the same commit. Diagnose that build instead, following
  further required dependency failures as needed.
- Failure on a different commit. Report the dependency as the cause of
  the current failure and stop.

For these failure lines, take the exact report name inside the brackets.
Preserve spaces and casing, and quote the name as one argument. Read the
report before deciding on a fix.

- `[<report>]: found problems with severity <severity> or higher` →
  `tod build get-code-problems <build> "<report>" <severity>`.
- `[<report>]: <count> not passed test cases` →
  `tod build get-unit-test-report <build> "<report>"`. To download a referenced
  artifact, add `--artifact <artifact-path> > <output-file>`.

Use `tod build get-changes-since-success <build>` if the previous successful
build helps explain the failure. Inspect `.onedev-buildspec.yml` for job
configuration problems and run `tod build get-spec-schema` before changing it.

## Leave the fix in the checkout

Make and verify the fix locally. Use `git status --short` to confirm what
changed. Leave edits unstaged and uncommitted, with any push or OneDev
comment outside this workflow.

If no edit is appropriate, explain why. Stop on an unmet precondition or
an unrecoverable error and report the failing command and error when applicable.
