---
name: explain-pr
description: >-
  Explain a PR's patches so the user understands them: the motivation and core
  idea, a before/after sample of what callers or users see, a flow diagram of
  that sample's path through the code with file:line citations, the facts a
  reader could miss, and where the PR description and the diff disagree. Use
  when the user says "explain-pr", or asks to explain, walk through, or help
  them understand a PR, a diff, or what a branch changes, including PRs written
  by an agent. Defaults to the PR for the current branch. This skill explains;
  it is not a review — it gives no verdict, changes no code, and posts nothing
  to the PR.
---

# Explain PR

Build the user's mental model of a change. A review hunts for defects; this
skill answers what the change does, why, and how to read it. Give no verdict
or priorities. If the user wants findings, point them to `review-all`.

## Establish the target

Resolve the PR the user names (number, URL, or `owner/repo#n`), else the PR
for the current branch, else the local `base...HEAD` diff against the
repository's default branch. Record the merge-base and head SHAs. Read the
before version at the merge base, not the base branch tip, so later changes
on the base branch are not attributed to the PR. Every citation refers to
the head; if the head moves while you work, recheck against the new head.

Read without touching the user's working tree: use `gh pr view`,
`gh pr diff`, and `git show <sha>:<path>` after
`git fetch origin pull/<n>/head`. For a PR in another repository, fetch into
a local clone of it if one exists, since reading many files through `gh api`
is slow; otherwise read files through `gh api` at those SHAs. Explaining a PR
must not cost the user their checkout state.

Explain the net diff. Use commit boundaries only as a hint for grouping.

## Gather context

A diff shows changed lines, not what the code did before or what depends on
it. Read:

- the PR title, description, linked issues, and commit messages;
- the merge-base version of each file with a meaningful change;
- the callers and callees of the changed code, enough to say what the change
  affects.

Treat the PR description as a claim to check, not as fact: descriptions go
stale, and agent-written ones can overstate. Base every behavioral statement
on code you read and cite `file:line`. Mark anything inferred rather than
confirmed.

## Write the explanation

Write in the language of the PR description, so the explanation reads
naturally to the PR's audience, and quote identifiers and spoken phrases
exactly.

Keep it short. Say each thing once, and skip what the PR description already
explains well; the explanation adds what the description lacks. Omit any
section with nothing to add. Use this order:

1. **Summary** — why the PR exists and its core idea, in three sentences at
   most.
2. **Before and after** — one realistic sample of what callers or users see,
   before and after.
3. **Flow** — a diagram of the path the sample takes through the code,
   marking where before and after differ, with `file:line` on each step.
   Followed top to bottom, it is also the order to read the diff in, so list
   the changes off the path (docs, tests, mechanical edits such as renames,
   formatting, or generated files) on one line beneath it.
4. **Worth knowing** — only facts a careful reader could miss: changed
   defaults, removed behavior, compatibility or rollout effects, new failure
   modes. State them as facts, not findings.
5. **Description vs diff** — where the description and the code disagree; if
   they agree, say so in one line.

End by offering to go deeper on any step.

For a large PR, give only the summary and the flow first, and let the user
choose which steps to open.

## Show the change

A concrete sample and a picture of its path make a change click faster than
prose.

**Sample.** When the change alters something a caller or user handles — a
request or response, a config file, CLI output, an error — show one
realistic sample before and after; a `diff` block is often the most compact
form. Prefer real output: when it is cheap and has no side effects, such as
validating against a model, run the sample against the code at the merge base
and at the head from a scratch location, and say the output is real.

**Flow diagram.** Where Markdown is rendered, such as a PR or issue on
GitHub, draw a Mermaid `flowchart` in a `mermaid` block. In a terminal, where
Mermaid shows only as source, draw the same diagram in ASCII inside a code
block. Keep it to the steps the change touches, each node a few words plus its
`file:line`. Label the edges where before and after differ instead of drawing
two diagrams, and mark where the data is rejected, dropped, or not read yet
with dashed lines or borders, not fill colors, which are hard to read in dark
mode. Quote every Mermaid label and keep to basic `flowchart` syntax, since
GitHub Enterprise may bundle an older Mermaid. When the change stays inside
one function, skip the diagram and show that function's before and after
instead. If the user asks for a richer visual and the environment can render
pages, render it there.

**Screenshots.** For a UI change, link the screenshots from the PR
description. Describe the visible difference only if you actually viewed the
images; PR attachments often cannot be fetched from a CLI, so otherwise say
they were not viewed. If a UI change has no screenshots, note it under
**Description vs diff** and offer to capture them: run the app at the
merge-base and head SHAs in separate temporary worktrees with the browser or
app-running facility available in the current environment, then remove the
worktrees. Capture only after the user agrees, since it builds and runs the
PR's code.
