---
name: orchestrating
description: The orchestrator's discipline - delegate the work, trust delegates to build and verify it, and be the user's one contact. Use when coordinating tickets across agents, when asked to orchestrate, or when another skill says to.
---

# Orchestrating

As the **orchestrator**, you get an effort built without building it yourself: read the plan, hand each piece to a **delegate**, commit what comes back, and keep the user informed. Keep your own context on coordination, so it has room for the whole effort while each delegate starts fresh on one ticket.

## Parameters

- `<notification-method>`: how a notification reaches the user, e.g. a desktop notification command, or the harness's own tool.

## Effort lifecycle

This is how one **effort**, such as a feature, a new app, a refactor or a re-architecture, travels from an idea to a merged pull request. The thinking runs on `/grilling`, `/prototype`, `/to-spec`, `/to-tickets` and `/handover`. The building runs on the orchestrate skills, whose delegates use `/implement`, `/tdd` and `/code-review`. Run routine upkeep, such as data edits and small fixes, in the current checkout without any of this.

An effort passes through five phases in one worktree on one branch:

```text
START      decide the worktree once; everything after follows it
THINKING   decide what to build; leave a spec, tickets, and a handoff
HANDOVER   the session commits everything and starts a fresh orchestrator
BUILD      orchestrate the tickets through delegates; open the pull request
SETTLE     the user approves; the agent merges, follows up, and cleans up
```

The session host, the program where new agent sessions open, decides which of two paths an effort takes. When the host is `herdr`, take the host path: `/handover-to-herdr` automates every step between phases. Otherwise take the plain path, which runs anywhere: this session carries on, or the user pastes each starting prompt.

```text
                START                          HANDOVER                        BUILD
Host path       init-effort                    handover                        orchestrate-with-handoff
                worktree tool;                 → handover-to-herdr:            → orchestrate-effort
                  → handover-to-herdr:           new "Orchestrator" tab,
                  "Thinking" tab,                agent started, prompted
                  agent started, prompted

Plain path      init-effort                    handover                        orchestrate-with-handoff
                worktree tool,                 runs the prompt here,           → orchestrate-effort
                or git worktree;               or prints it; the user
                thinks here, or prints         pastes it into a new
                the starting prompt            session
```

### Start

`/init-effort` names the effort and creates its branch and worktree. The worktree is decided here, before any thinking, so the spec, tickets, and handoff are written on the effort's branch rather than on the default branch. The build later runs in the same worktree.

For a brand-new project it first creates the repository, and the project's first effort then starts like any other. It writes the idea into a handoff in the worktree and starts the thinking session on it.

### Thinking

```text
grilling     sharpen the idea, one round of questions at a time
  prototype  when a question needs a runnable answer; the user reviews it
to-spec      the thread becomes a spec
to-tickets   tracer-bullet tickets, each naming what blocks it
handover     hand over to an orchestrator
```

The starting prompt names these skills and the agent loads each one itself: the user types no slash command. Run it in one unbroken context window, so the spec and tickets build on the same reasoning. [folder-standard.md](folder-standard.md) says where the spec and tickets land.

### Handover

The session that hands over finishes its own work cleanly, through `/handover`. A handover can run from any session at any point, not only at the end of the thinking: a desktop-app session on the default branch can hand an effort to an orchestrator in the session host without leaving its own checkout. It gets the session ready, starts the new session on the handoff with a one-line prompt, and confirms it started. The session that handed over then stops, and stays open for reference.

### Build

`/orchestrate-with-handoff` picks up the handoff and runs `/orchestrate-effort`, which delegates the tickets to sub-agents in parallel, each building its ticket with `/implement` in its own worktree, integrates each ticket as its own commit, and opens the pull request with `/to-pr` after one branch review. In a project that opts in to QA, a ticket the user can try stays open and goes to them with try-this steps; the merge waits for it only when the spec says "QA: blocking".

### Settle

The user reviews and approves the pull request: that is their only step. The agent then merges it and settles the effort with `/settle-effort`, whether it is the orchestrator that delivered or any session told the pull request merged or to merge it. Workspaces and agent sessions stay open for the user to close.

### Why two sessions

The thinking session fills its context with debate, dead ends, and prototype output. The builder needs none of it: the spec, tickets, and handoff carry the conclusions. Starting fresh leaves the orchestrator's context free for the long run, and each ticket's delegate starts even fresher, from one ticket file.

## The discipline

- **Delegate.** Hand every ticket to a delegate, even a small one. A delegate is a sub-agent unless the skill that started the orchestration says otherwise.
- **Point, don't restate.** Give a delegate the paths to the ticket and the spec, not a paraphrase of them, because the documents are the source of truth.
- **Trust the delegate.** A delegate builds, tests and reviews its own ticket, to the review depth its brief sets. Read its report against the ticket's acceptance criteria, and send back only what the report shows is missing or failing.
- **Keep reviews in the delegate.** Tell delegates to run their reviews synchronously in their own context, because a sub-agent a delegate starts reports to you instead of back to the delegate.
- **Be the one contact.** Delegates send their questions to you, so the user deals with one agent.
- **Keep moving.** While one ticket waits on the user, run another that isn't blocked.
- **Leave nothing running.** When a delegate reports, stop anything it left running, such as dev servers, preview and browser tabs or background tasks, unless its report names it with a reason. Sweep your own the same way before telling the user a run is finished.
- **Commit alone.** Run each commit and each push as its own call, never chained with cleanup: a permission check that refuses one part refuses the whole chain, and the refusal then looks like a refused commit. Move what a delegate leaves behind into `.scratch/`, and put every record where `folder-standard.md` says.

## Talking to the user

The thinking session gathered the inputs only the user has, such as credentials, IDs, accounts, external setup or a call only they can make, and the handoff records them. A secret stays out of the chat and out of committed files: the user puts it where the work reads it, such as an environment variable, a keychain or the tool's own login, and the handoff says where.

- **Decide the rest yourself.** An open question the spec, tickets and handoff don't settle is yours: look up the facts, weigh the options, pick one, and pass the decision to the delegates it touches so no one asks again. Keep a running list of the decisions you made alone, each with its reason, for the pull request's last section, where the user reviews them.
- **Interrupt only for a critical blocker,** when every remaining ticket waits on a call or an input only the user has. Send the blocked notification, then ask one question in this shape, and wait:

```text
<The question, in one sentence.>

<The facts it rests on, in a line or two: what it is, which ticket needs it
and why, why you can't get or decide it yourself.>

|                | A: <option> (my pick) | B: <option> |
|----------------|-----------------------|-------------|
| <what differs> | ...                   | ...         |

Reply "A" to go with my pick, or name another.
```

- **Record the answer** where later delegates and a successor orchestrator read it: the ticket, or the handoff.
- **Give every decision with its facts, its options and your pick,** in the chat or the pull request, so the user can weigh it without opening a file.
- **Show, from real data.** Draw a visual report with `/show-me`, and draw options with it when a picture makes them easier to weigh, such as the ticket tree or the result as a diff.
- **Name an issue, ticket or pull request by its title,** never by its number alone: `#12 Add login`, not `#12`.

## Notifications

The user steps away during a long run, and a notification is how they know to come back. Send one with `<notification-method>` at exactly two moments:

- **Done:** the pull request is delivered, with every ticket committed and pushed, the final review fixed and the description written.
- **Blocked:** nothing can continue without the user, and you are about to ask your one question.

Keep routine progress, such as a ticket landing or a delegate reporting, in the chat. Write each notification as one line under 200 characters, leading with what the user acts on:

```text
PR ready for review: Effort workflow, 19 tickets, 2 decisions to check
blocked: "Sign in with the provider" needs your OAuth app client ID
```

## References

- [folder-standard.md](folder-standard.md): where each record of an effort goes in a project, and how to remove what's no longer needed.
