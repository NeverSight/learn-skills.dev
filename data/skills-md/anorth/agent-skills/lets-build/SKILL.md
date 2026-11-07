---
name: lets-build
description: >-
  Build from a written ticket or task, collaborating with the user: design it with them first if it isn't ready,
  then build it with the user in the loop. Use when the user says let's build, build together,
  or asks to build from a ticket or task description.
disable-model-invocation: false
---

# Let's Build

Build one ticket together. The agent does the work; the user stays in the loop for design and decisions.
A ticket that isn't ready yet gets designed first.

## When to use

Use when the user says let's build or build together, or asks to build a ticket or task with them.

If the user wants the ticket built independently, with the agent making its own decisions, use `/build-ticket`.
If they want to design without building yet, use `/lets-design`.

## Workflow

### 1. Load the ticket

Identify the written ticket or task. The user may give an id, URL, file path, or pasted text.
If it is unclear which item: ask. Do not guess.

Read the ticket in full. If it doesn't satisfy `/ready-ticket`, load and follow `/lets-design` first,
then write the agreed design into tickets with `/to-tickets`.
If that makes more than one ticket, stop there, and suggest which ticket is ready to pick up.

### 2. Build

Build with the `/build-ticket` skill, with the user in the loop.

## Guidelines

The user is the authority on what the system should do: their answers override the ticket.
When they do, keep the ticket's original brief and append a note saying what changed and why.
