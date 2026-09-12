---
name: superpowers-issue-bridge
description: >
  Use whenever Superpowers' brainstorming or writing-plans is about to run —
  including when it is unknown whether an intent issue exists — and when work
  that started from an intent issue is being merged or opened as a pull
  request.
---

# Superpowers Issue Bridge

## Where this fits

Superpowers' `brainstorming` is the conversation. For work with no intent
issue yet, it can end two ways, and the user picks:

- **Build now** — brainstorming continues as usual: its design, then a plan,
  code, and a pull request. No issue is involved.
- **Track first** — `brainstorm-to-issue` files an intent issue, and the
  session ends there. The issue is built later, by the user or by an agent
  working from it.

This bridge owns the moments around that choice: offering it, seeding
brainstorming from an issue that already exists, tracing the spec and plan
back to the issue, and linking the finished work to it.

## Before Step 1 — Read the tracker config

Read `docs/agents/issue-tracker.md`. Its Backend, Location, Reading, and
Linking sections say where issues live, how to read one, and what a pull
request writes to close or reference one.

- **GitHub, without Reading or Linking sections** (a config written before
  they existed): use GitHub's conventions — `#<number>`, `gh issue view`,
  `Closes #<number>`, `Relates to #<number>`, `gh issue close`.
- **Any other backend without them:** ask the user how to read and link its
  issues.
- **No config file:** ask where the issue lives rather than assuming this
  checkout's GitHub repository.

The examples below use GitHub's syntax; substitute the tracker's own.

## Step 1 — Find the intent issue

- The user references one ("implement #42", "build PROJ-123").
- The current branch name contains an issue reference (e.g.
  `feat/42-claims-status`). Confirm it with the user — a number in a branch
  name isn't always an issue.
- Otherwise, ask whether one exists. Don't assume there isn't one because it
  wasn't mentioned, and don't guess a reference.

An issue exists → Step 3. None exists → Step 2.

## Step 2 — No issue yet: offer build now or track first

Let brainstorming run its opening as usual: explore the project, classify the
work, and ask its clarifying questions about the problem. Once the problem is
understood — before brainstorming proposes approaches (architectural path) or
presents its short design (bounded path) — ask, as its own question:

> "Do you want to build this now, or track it as an intent issue first?"

- **Build now** — brainstorming continues unchanged. With no issue, Steps 3–5
  don't apply.
- **Track first** — invoke `brainstorm-to-issue` on the conversation so far.
  Every decision the user has explicitly made goes into the issue's
  Constraints section. Once the issue exists, the session ends: no spec, no
  `writing-plans`, no code. The user's choice replaces brainstorming's usual
  next step.

Skip the question when its answer is already known:

- The user already said which: "just fix it" or "build it now" means build
  now; "file this" or "track it first" means track first.
- Brainstorming classified the work as a spike. A spike ends in an answer,
  not tracked work; the user can file what it found afterwards.

## Step 3 — Seed brainstorming from the issue

Read the issue with the tracker's Reading method — on GitHub,
`gh issue view <number> --repo <owner/repo> --json title,body,url`.

Pass its Problem / Proposed outcome / Affected users and systems /
Constraints / Open questions into brainstorming as already answered:

- Don't re-ask what the issue states.
- Treat Constraints as settled: they hold decisions the user already made.
  Reopen one only when the user does.
- Ask what the issue doesn't cover. On the architectural path, that means
  alternatives, out-of-scope boundaries, and edge cases; on the bounded path,
  only the questions its short design needs.
- Carry the Open questions forward as questions still needing an answer,
  unless the conversation resolves them.

## Step 4 — Trace the spec and plan back to the issue

This step applies to brainstorming's architectural path, the only one that
writes files. When the spec is written (by default under
`docs/superpowers/specs/`), add this line directly under its title:

```markdown
Intent-Issue: #<number> — <url>
```

When `writing-plans` writes the plan (by default under
`docs/superpowers/plans/`), carry the same line forward unchanged, directly
after the plan header's `**Spec:**` line. For a local-markdown intent, the
file path replaces `#<number> — <url>`.

The spike and bounded paths write no spec or plan. Don't create one to hold
this line — the link in Step 5 is the trace.

## Step 5 — Link the finished work back

`finishing-a-development-branch` is where work lands —
`subagent-driven-development` and `executing-plans` both end there. Once the
user has picked one of its options, ask once: **does this work fully resolve
the intent issue, or is it partial?** Then apply the tracker's Linking
section:

| Option picked | Fully resolves | Partial |
| --- | --- | --- |
| Push and create a PR | Finishing reference in the PR body (`Closes #<number>`). | Partial reference in the PR body (`Relates to #<number>`). |
| Merge locally | No PR carries a reference, so nothing closes on its own. Tell the user, and offer to close the issue by hand once the merge is pushed (`gh issue close <number> --comment "Resolved in <sha>"`). | Once the merge is pushed, offer a comment on the issue naming the merge commit (`gh issue comment <number> --body "Progress in <sha>"`). |
| Keep as-is | Nothing to link yet. | Nothing to link yet. |

Closing or commenting by hand changes the tracker: do it only on the user's
yes.

In an unattended run — a dispatcher working through issues with no one to
ask — decide from the implementer's report instead: any work left undone
means partial. State the choice and its reason in the PR body.

Don't default to closing. An intent issue is often bigger than one PR, and
closing it early breaks the audit trail this setup exists to protect.

## What NOT to do

- Don't merge this bridge's logic into Superpowers' own skill files — keep
  it as a separate skill so Superpowers updates don't clobber it.
- Don't re-interview the user on what the intent issue already answers, and
  don't reopen its Constraints on your own.
- Don't write a spec, run `writing-plans`, or start code after the user chose
  to track first.
- Don't create a spec or plan file just to hold the `Intent-Issue:` line.
- Don't assume "fully resolves" or "partial" — ask once per PR or merge.
- Don't invent an issue reference. If one can't be found or confirmed,
  proceed without one rather than guessing.
- Don't use GitHub's `#<number>` or `Closes` syntax for a tracker that isn't
  GitHub.
- Don't close or comment on an issue without the user's yes.
