---
name: markdown-rendering
description: "Open Markdown reliably in cmux panes and recover from blank rendered surfaces."
category: productivity
risk: safe
source: community
source_repo: davidondrej/skills
source_type: community
date_added: "2026-07-07"
author: davidondrej
tags: [markdown, cmux, rendering]
tools: [claude, codex]
license: "MIT"
license_source: "https://github.com/davidondrej/skills/blob/main/LICENSE"
---

# Markdown Rendering in cmux

## When to Use

- Use when opening Markdown in cmux shows a blank pane or wrong layout.
- Use when you need to display a Markdown file in a stable cmux right pane.

## The Problem

`cmux markdown open` defaults to **spawning a brand-new pane** every time, even with `--direction right`. The common "fix" — moving the new markdown surface into the existing right pane with `move-surface` — **bugs out: the moved viewer renders BLANK.** The surface keeps `type=markdown` and looks healthy, but shows nothing.

So you get stuck: either a stray extra pane, or a blank viewer after moving it.

## The Rule

The contributor observed two workarounds for a particular cmux version. Verify the installed command/version; the blank-render issue may have changed. Prefer reopening an owned viewer without altering unrelated panes.

### Option A — Open it right on the first try

If there is no usable right pane yet, just let cmux create one and leave it where it lands:

```bash
cmux markdown open /abs/path/file.md --direction right --focus false
```

Do NOT then move it. If it spawned where you want it, you're done.

### Option B — Close existing right pane(s), then open fresh

If there are other right panes in the way (and they're unused or irrelevant), **close them first**, then open the markdown fresh as a new right pane:

```bash
# 1. find panes in THIS workspace
cmux list-panes --workspace "$CMUX_WORKSPACE_ID"

# 2. close the unused/irrelevant right pane(s) by closing their surfaces
cmux list-pane-surfaces --pane pane:NN
cmux close-surface --surface surface:XX     # repeat per surface in that pane

# 3. THEN open the markdown fresh — it creates its own clean right pane
cmux markdown open /abs/path/file.md --direction right --focus false
```

## Hard Rules

- **Never `move-surface` a markdown viewer.** It renders blank afterward. This is the core bug this skill exists for.
- Open it correctly the first time (Option A), OR close the conflicting right pane(s) and open a fresh right pane from scratch (Option B).
- Close only surfaces created for this task or explicitly authorized for closure; apparent irrelevance does not prove they contain no unsaved work.
- Always anchor to `$CMUX_WORKSPACE_ID`; never assume the visually focused workspace.
- Pass `--focus false` so you don't steal the user's focus.
- Use any supported readback/rendered inspection available on the actual host. If it cannot inspect the viewer, report that limit instead of claiming success.

## Limitations

- Adapted from `davidondrej/skills`; verify local paths, tools, credentials, and agent features before acting.
- For commands, remote access, scheduling, browser automation, or file-changing workflows, get explicit user approval and confirm the target environment first.
