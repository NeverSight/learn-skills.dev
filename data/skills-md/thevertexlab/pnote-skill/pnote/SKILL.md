---
name: pnote
description: pnote - The PromptNote CLI for managing prompts, notes, and snippets
allowed-tools: Bash(pnote *)
user-invocable: true
argument-hint: <command> [options]
---

# pnote - The PromptNote CLI

Manage your prompts and notes from the terminal. Requires `npm install -g pnote` and authentication via `pnote auth token <your-pat>`.

## Available Commands

!`pnote --help`

## Quick Reference

**List & Search:**
- `pnote notes` - list all notes
- `pnote notes --tag "AI/art"` - filter by tag
- `pnote search "query"` - search notes and snippets

**Read & Copy:**
- `pnote notes get <id>` - get note with snippet
- `pnote snippet copy <id>` - copy to clipboard

**Create & Manage:**
- `pnote notes create "Title"` - create note
- `pnote snippet add <id>` - add snippet from stdin
- `pnote tags rename "old" "new"` - rename tag

**PIN Protection:**
For protected notes, set `PNOTE_PIN` env var or use `-p <pin>` flag.

## Execute

Run the user's command:

```bash
pnote $ARGUMENTS
```
