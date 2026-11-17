---
name: using-craft
description: Use when starting any conversation, before responding to any request that involves designing, reviewing or changing a UI, a screen, a page, a flow, a component or a style guide.
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to do one specific task, ignore this skill and do the task.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If there is even a small chance that a design skill applies to what you are about to do, invoke it **before you respond**, including before clarifying questions, before reading files and before drawing anything.

A design skill that applies is not optional. Small edits are the only exception (see below).
</EXTREMELY-IMPORTANT>

## How

1. Check the routing table below. The one thing to look at first is whether `DESIGN.md` exists at the project root; it decides between `craft-setup` and `craft`. Don't guess it.
2. Invoke the skill with your Skill tool, and announce: "Using <skill> to <purpose>."
3. Follow it exactly, including its stops for the person's approval. A stop means ending your turn with the question, which is always possible, even in a headless or one-shot session. Never decide a stop for the person.

## Routing table

| The situation | Skill |
|---|---|
| Any request to design, create, mock up or redesign a page, screen, flow or element | `craft` |
| A design task in a project with **no `DESIGN.md`** at its root | `craft-setup` first (it offers to import a design system already in code), then `craft` |
| "Set up the design", "define our style / brand / guidelines" | `craft-setup` |
| "Options", "alternatives", "other directions", "I don't like it", "rethink this" | `craft-explore` |
| "Review", "refine", "polish", "make it better", "feels off", or you are about to show your own design | `craft-critique` |
| Tokens, the style guide, a new or changed component, "make consistent", "audit" | `craft-system` |
| "Import / bring our design system, tokens or components into <tool>"; "apply / push / sync the guide's changes to the code" | `craft-sync` |
| "What states are missing?", "is this ready for dev?" | `craft-states` |

A reusable piece for the system ("we need a date picker component") goes to `craft-system`; something on a specific page goes to `craft`. These are craft's skills (prefixed `craft:` in the Claude Code plugin); prefer them over same-named skills from elsewhere.

## Priority

1. `craft-setup` before `craft` when there is no `DESIGN.md`. Reviews, options for an existing screen, audits and state questions don't need a brief: they work from what's already there.
2. `craft` before its sub-skills: it calls `craft-states`, `craft-explore`, `craft-system`, `craft-sync` and `craft-critique` at the right moment, so don't start them yourself in the middle of a `craft` run.
3. `craft-critique` is the last step before you show anything you made.

## Small edits: no process

A change the person described exactly (one value, one label, one element's size, one colour, a typo) is made directly. No skill, no states list, no options.

- If the thing is shared (a button style used on many screens), change it **once where it is defined**, and say which screens it affects. Don't open a full design pass for it.
- If you're unsure whether it's small, it isn't. Use the table.

## Red flags

| Thought | Reality |
|---|---|
| "It's just a quick mockup, I'll skip the process" | A quick mockup is still a design. The states list takes a minute. Use `craft`. |
| "There's no `DESIGN.md`, but the request is clear enough" | Without a brief, every screen invents its own style. `craft-setup` first; the person can say "skip". |
| "I'll draw it now and review it later" | Showing unreviewed work trains the person to do your review. `craft-critique` runs before you show. |
| "I know which states it needs" | You know the happy path. `craft-states` lists the rest. |
| "Let me read the files first, then decide on a skill" | Skills tell you what to read. Decide first. |
| "This is a small change" (to a new page) | A new page is never a small change. |
| "The session can't wait for answers, so I'll decide and list my calls" | End your turn with the question. Deciding for them is the one thing the stops exist to prevent. |

## Other agents

Where this skill isn't loaded automatically, put the routing table above in your `AGENTS.md` (or the equivalent) so the agent sees it at the start of every session.
