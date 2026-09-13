---
name: setup-issue-tracker
description: >
  Use when a repository needs to choose or change where issues and feature
  intents live, or when docs/agents/issue-tracker.md is missing or stale.
---

# Setup Issue Tracker

Record the repository's issue and intent backend — and how later skills read
its issues and link finished work back to them — in
`docs/agents/issue-tracker.md`. Optionally connect that configuration to an
existing `AGENTS.md` without taking ownership of the rest of the file.

This skill configures local files only. It does not create remote repositories,
issues, or labels, and it does not create or replace `AGENTS.md` or
`CLAUDE.md`.

## Inspect first

1. Read an existing `docs/agents/issue-tracker.md` in full.
2. Read root-level `AGENTS.md` if present and check whether it already points to
   the tracker configuration or describes the intent-to-PR workflow.
3. Run `git remote -v`. Normalize ordinary GitHub HTTPS and SSH URLs to
   `owner/repo`, stripping a trailing `.git`. If fetch and push URLs disagree,
   multiple remotes are plausible, or the remote may be a fork, present the
   candidates rather than choosing one. Every inferred location is a proposal,
   not confirmation of the user's intended tracker.
4. Check `git status`, then summarize the current state before changing it.

## Confirm the backend

Ask where issues and intents should live:

| Backend | Configuration to confirm |
| --- | --- |
| GitHub | Confirm the `owner/repo` inferred from the remote. If remotes disagree or none identifies GitHub, ask rather than guessing. Offer `intent` as the label, but confirm it; this backend requires a label because `brainstorm-to-issue` consumes one. |
| Local markdown | Confirm `.scratch/<feature>/` or another user-specified location. |
| Other | Ask for the backend name, location, and enough freeform workflow notes for another agent to use it. |

Do not inspect, create, or update remote labels as part of configuration. A
later issue-creation workflow may do so with the required authorization.

## Confirm reading and linking

Later skills need two more things from this file: how to read issues, and how
finished work links back to one. Record both, so no skill applies GitHub's
syntax to a tracker that isn't GitHub.

| Backend | Proposal to confirm |
| --- | --- |
| GitHub | GitHub's own conventions: `#<number>` as the reference; `gh issue list` and `gh issue view` to read; `Closes #<number>` in a PR body to close the issue on merge, `Relates to #<number>` for partial work; `gh issue close` to close one by hand. Propose these as the defaults. |
| Local markdown | The intent file's path is its reference, and reading it means opening the file. Nothing closes on merge, so ask how a finished intent is marked — for example, a status line in the file — and therefore which files count as open. |
| Other | Ask for each line: the reference format, how to list and read issues (a CLI, an MCP server, a URL), what a PR writes to close or reference an issue, and how to close one by hand. For Jira, the reference is usually the issue key (such as `PROJ-123`) in the branch, commit, or PR title, and whether a merge closes the ticket depends on the team's Jira–GitHub integration — ask rather than assume. |

## Write the configuration

Create `docs/agents/` if needed, preserving every file already there. Write
`docs/agents/issue-tracker.md` with this shape:

```markdown
# Issue tracker

<!-- Read by: brainstorm-to-issue, superpowers-issue-bridge, fetch-issues, and any future spec/plan/triage skills -->

## Backend
<GitHub, Local markdown, or the named backend>

## Location
<confirmed owner/repo, local path, or tracker location>

## Labels
<confirmed labels, or None>

## Reading
- Issue reference: <e.g. `#<number>`, `PROJ-<number>`, or the intent file's path>
- List open issues: <command, tool, or rule for which files are open>
- Read one issue: <command, tool, or path>

## Linking
- Finishing PR: <what a PR writes to close the issue on merge, or None>
- Partial PR: <what a PR writes to reference the issue without closing it>
- Close by hand: <command or step, for when no PR carries the link>

## Notes
<user-provided details, or None>
```

For GitHub, record the intent label as `- <label> — applied to issues created
by brainstorm-to-issue`. For an existing configuration, show the proposed
differences and obtain confirmation before replacing real values. A
configuration written before the Reading and Linking sections existed is
missing values, not holding wrong ones: propose the two sections as an
addition and confirm them like any other change. Re-running with the same
values is a no-op.

## Connect an existing AGENTS.md

If root-level `AGENTS.md` does not exist, leave it absent. The tracker
configuration is still usable; recommend `setup-agent-md` if the
user wants shared repository instructions.

If `AGENTS.md` exists, read `assets/AGENTS-sections.md` and show the user the
exact missing entries or sections. Tracker selection does not implicitly
approve this optional edit: show its patch and obtain confirmation, which may
be combined with the backend confirmation in one question.

- Merge the tracker entry into an existing `Agent configuration` section when
  one exists; do not duplicate the heading.
- Preserve an existing `Workflow` section. If it lacks the intent-to-PR steps,
  show a surgical merge of the missing steps. If existing steps conflict with
  the supplied workflow, show the conflict and ask which text should remain.
- Do not reorder, rewrite, or reformat unrelated project instructions.

## Finish

Read back the tracker configuration and inspect the final diff. If
`AGENTS.md` changed, confirm that only the approved entry or sections changed.
Report the backend, location, labels, reading and linking conventions, and any
file deliberately left untouched. A completed tracker file remains valid when the optional
`AGENTS.md` integration is declined or deferred; report that state plainly.
Stop without creating an issue or invoking another skill.

## What NOT to do

- Don't guess the tracker, GitHub repository, local path, or label.
- Don't guess how a tracker that isn't GitHub reads, links, or closes issues —
  and don't record GitHub's `#<number>` and `Closes` syntax for one.
- Don't mutate GitHub or another remote service during local configuration.
- Don't overwrite a populated tracker configuration without showing the
  differences and receiving confirmation.
- Don't create `AGENTS.md` or `CLAUDE.md`; that belongs to
  `setup-agent-md`.
- Don't replace an existing `AGENTS.md` with a template or rewrite unrelated
  guidance.
- Don't create intent issues, specs, plans, or pull requests as part of setup.
