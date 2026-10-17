---
name: lemma-artifacts
description: >-
  Read this codebase and record what its AI agents are for in Lemma. Use when
  the user asks to tell Lemma about their agent, set up or improve Lemma
  artifacts or agent context, record what an agent does, describe their agent
  to Lemma, bring Lemma's understanding up to date with the code, or fix a
  rule Lemma still has that the codebase no longer enforces. After its
  closing report it offers to hand off to lemma-tracing when the agent it
  settled on is not instrumented, whether or not anything was written. Do not
  use for installing tracing or fixing trace delivery and shape — that is
  lemma-tracing and lemma-diagnostics.
metadata:
  version: 2.0.0
---

# Lemma Artifacts

You are recording, in Lemma, what the AI agents in this codebase are for.

Lemma detects failures in production agents by reading their traces. It reads
them better when it knows what the agent was supposed to do. That knowledge
normally accrues from traces over time, which means the earliest traces are
judged with no context at all. This skill front-loads it from the source the
customer already has: their own code.

Two things follow from where you are standing, and they govern everything below.

**The code tells you intent, not behaviour.** You are reading what the authors
meant to build. Only traces show what actually happens, so leave out anything
only a run could tell you: the shape of a trace, latencies, call counts.

**Nothing is written without the user saying yes to specifics.** You are about
to put words in their vendor's mouth about their own system. They get to read
those words first, every time.

## Core rules

1. **Read Lemma's current state before proposing anything.** Call
   `list_project_artifacts` first, always — including when you expect it to be
   empty. What is already recorded changes what is worth adding.
2. **Never call a write tool before the user has approved that specific
   content in this conversation.** `write_learn_agent_artifact_version`,
   `upload_project_artifact`, `update_project_artifact` and
   `delete_project_artifact` all wait for an explicit yes.
3. **Itemize the claims in the confirmation.** "Write 3 artifacts?" is not a
   confirmation. Name the agent, state the claims, and say which file each
   would land in. See [references/record.md](references/record.md).
4. **Never modify the user's code.** You are reading their repository to
   describe it. No edits, no new files, no reformatting — not even to a
   README, and not to "fix" something you noticed. Mention it and move on.
5. **Never touch the key.** You reach Lemma with `LEMMA_MCP_API_KEY`, which
   the user sets in the environment you run in. Reference it by name only.
   Never read, print, echo, or write its value into any file, tracked or not,
   and never ask the user to paste it into this conversation. A placeholder
   line such as `LEMMA_MCP_API_KEY=` in an env example is fine. If it is
   missing, see [When Lemma refuses the connection](#when-lemma-refuses-the-connection).
6. **Never call `regenerate_project_artifacts`.** That starts Lemma's own
   trace-driven learning run, which is a different thing costing real time and
   money, and it is not how this skill writes.
7. **Say what convinced you.** Every proposed claim cites the file that
   supports it. A claim you cannot point at is a claim you should drop.
8. Keep tool names exactly as written here so transport mappings stay valid.

## Two kinds of artifact, and they are not interchangeable

Lemma stores two things and the word "artifact" is used loosely for both. They
behave differently and picking wrong loses information.

| | Agent understanding | Project context files |
| --- | --- | --- |
| Holds | how the agent works: its task and its tools | facts no trace shows: rules, intended behaviour that looks like a failure, setup facts |
| Written by | Lemma's learning runs; you write the first version | the customer, and you |
| Rewritten by Lemma | on every learning run, from observed traces | never |
| Tools | `write_learn_agent_artifact_version` | `upload_project_artifact`, `update_project_artifact`, `delete_project_artifact` |
| Contract | [references/agent-artifact-contract.md](references/agent-artifact-contract.md) | [references/project-context-contract.md](references/project-context-contract.md) |

**The understanding you write is a first draft for Lemma's learning run, not
lasting context.** Once traces arrive, the run reads your version as its
previous draft and rewrites the whole document from what it observes. It may
keep little of yours. That is expected: write it in the same shape and register
the learning run uses, so the hand-off is clean, and do not try to make it
survive.

Which one a finding belongs in is decided by one test, set out with examples
in [references/project-context-contract.md](references/project-context-contract.md):
**could someone learn this from the agent's traces, including the system prompt
they carry?** If not, it goes in a project context file. If so, it goes in the
understanding.

Anything worth keeping that you put in the understanding instead will be gone
after the first learning run.

## Workflows

| Step | When | Reference |
| --- | --- | --- |
| Discover | Find the real agents, tell them from examples and dead code, settle their names | [references/discover.md](references/discover.md) |
| Record | Read current state, propose, confirm, write, report | [references/record.md](references/record.md) |
| Hand off | After the closing report, offer tracing when the settled target agent is not instrumented — written or declined | [references/tracing-handoff.md](references/tracing-handoff.md) |

Read all three before acting. Run them in that order.

## When Lemma refuses the connection

A `401` from any Lemma tool means the key behind `LEMMA_MCP_API_KEY` is
missing, expired, or revoked. It is a thing for the user to fix, never a thing
to work around.

Stop there. Write nothing, offer nothing, and tell the user to set
`LEMMA_MCP_API_KEY` in the environment this agent runs in, then run you again.
A key comes from the **Describe your agent** step in Lemma onboarding, or from
**Settings → API keys** in the dashboard.

Do not ask them to paste the key to you. Do not read it back out of a file or
the environment to check it. Do not retry the call until they say it is set.

## When this is not the right skill

- The user wants tracing installed, or traces are not arriving: hand off to
  `lemma-tracing`. Do not install the SDK yourself. The one time this skill
  raises tracing on its own is the offer after the closing report
  ([references/tracing-handoff.md](references/tracing-handoff.md)): the offer
  is a question, and the work is still `lemma-tracing`'s.
- Traces arrive but are thin or malformed: hand off to `lemma-diagnostics`.
- The user wants to triage detected issues: that is `lemma-mcp`.

This skill does not need traces to exist. Recording specification before the
first trace is the point of it, so an empty project is a normal starting state,
not a blocker.
