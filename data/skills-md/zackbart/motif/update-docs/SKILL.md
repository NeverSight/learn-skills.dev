---
name: update-docs
description: >
  Scans project documentation for staleness and inaccuracies, then updates it
  to reflect the current codebase. Uses a read-only scanner subagent to assess
  docs and a writer subagent to apply approved changes. Optionally scoped to
  a specific area via arguments.
argument-hint: "[focus area, e.g. 'README', 'api docs', 'installation instructions']"
allowed-tools: "Agent, Read, Grep, Glob, Bash, AskUserQuestion"
---

# Documentation Updater

Update this project's documentation to accurately reflect the current state of the
code. Delegates discovery to a scanner subagent and updates to a writer subagent,
with user approval in between.

## Argument Parsing

Parse $ARGUMENTS for an optional focus area:

- If $ARGUMENTS is empty, scan all documentation in the project.
- If $ARGUMENTS contains a focus area (e.g. "README", "api docs", "CLAUDE.md",
  "installation steps", "architecture"), scope the scan to that area. Pass the
  focus to the scanner subagent so it narrows its search.

Store the focus (or lack thereof) for use in the briefings below.

---

## Step 1 — Scan

Spawn the `docs-scanner` subagent. Pass it a briefing containing:

1. **Project root**: run `ls` at the project root and include the output
2. **Focus area**: what the user wants scoped (or "all documentation" if no args)
3. **Key context**: language/framework if obvious from the root listing

The scanner will return a structured report of what documentation exists, what's
outdated, and what's missing. Display the full report to the user.

---

## Step 2 — User approval

Present the scanner's findings and ask the user what to act on:

> **Documentation scan complete.** [Summary of findings]
>
> Which updates should I apply?
> - **all** — apply everything the scanner found
> - **pick** — let me choose specific items
> - **none** — stop here, I just wanted the audit

Wait for the user's response. If they pick specific items, confirm the list before
proceeding.

---

## Step 3 — Update

For each approved update, spawn the `docs-writer` subagent. Pass it a briefing
containing:

1. **The file to update**: full path
2. **What needs to change**: the specific finding from the scanner
3. **Current file contents**: read the file and include it so the writer has the
   full context (not just the stale section)
4. **Codebase truth**: any relevant source files the writer needs to reference for
   accuracy — include paths so it can read them

If there are multiple independent files to update, you may spawn multiple writer
subagents in parallel.

Each writer returns the changes it made. Collect all results.

---

## Step 4 — Summary

After all writers complete, present a file-by-file summary:

- File path
- What was changed (brief)
- What was left alone

If any writer encountered something it couldn't resolve (ambiguous source of truth,
conflicting information), flag it for the user.
