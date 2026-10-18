---
name: tldr-highlight
description: |
  About the TL;DR mod that comes with this skill: on a long reply it highlights in yellow
  the few paragraphs worth reading, shows the reply in one sentence as a notification, and
  puts a TL;DR on/off button above the prompt. Use when the user asks what the yellow
  highlight or the TL;DR button is, how to turn it off, why it did not show up, what it
  costs, or how to remove it. Triggers: "TL;DR mod", "yellow highlight", "turn off TL;DR",
  "why is my reply yellow", "המוד של TL;DR", "הסימון הצהוב", "לכבות את TL;DR".
  NOT for summarizing or shortening a text the user gives you.
---

# TL;DR mod

This folder holds a Claude Code mod (the `.claude-plugin` and `hooks` folders). Claude Code
loads it by itself in every new conversation. This skill only answers questions about it.
Answer in the language of the user's messages.

## What it does

- After a reply of about 150 words or more, a small model (Haiku) reads it and picks at most
  three paragraphs: the direct answer, anything waiting on the user, and anything that failed
  or was not checked. Those paragraphs get a yellow background. Past the first one, no more
  than a third of the reply is highlighted, and never code or a lone heading.
- The same call writes the whole reply as one sentence, in the language the user writes in.
  It shows as a notification for 15 seconds.
- Only the drawing changes. The conversation, and what Claude reads, stay as written.
- The highlight shows in the desktop app (the Code tab). A terminal keeps its own drawing, and
  shows only the button and the notification.

## The button

Above the prompt: `↩ No TL;DR` turns it off, `TL;DR` turns it back on (and reads the reply on
screen right away). The choice is kept for the next conversations. When other mods from this
collection, or Smart PreCompact, are installed, the button sits in the same row as theirs.

## What it costs

One short Haiku call per long reply, from the user's own Claude plan, the same way the
conversation itself is billed. Short replies are never sent. Turning it off stops all calls.

## Turning it off for good, or removing it

- Off without removing: `claude plugin disable tldr@skills-dir`
- Remove: `npx skills remove tldr-highlight -g`, or delete the folder
  `~/.claude/skills/tldr-highlight`
- Never keep a backup copy of this folder inside `~/.claude/skills`: Claude Code would load the
  mod twice.

## When it does not show up

- No button above the prompt in a new conversation: this Claude Code version does not run mods
  yet. Updating Claude Code fixes it.
- A button but no yellow: the reply was short, it is a terminal, or the mod is off.
- The engine's own notes about the mod are in the debug log (`claude --debug`), on lines that
  start with `tldr:`.
