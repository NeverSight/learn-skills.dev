---
name: swain-stage
description: "Tmux workspace manager — creates layout presets (review, browse, focus), opens editor/browser/shell panes, runs an animated MOTD status panel, and lets the agent directly manage panes during work. Only activates in tmux sessions."
user-invocable: true
license: MIT
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  short-description: Tmux workspace and pane management
  version: 1.0.0
  author: cristos
  source: swain
---

# Stage

Tmux workspace manager for swain. Creates pane layouts, manages an animated MOTD status panel, and gives the agent direct control over the visual workspace.

**Prerequisite:** Must be running inside a tmux session (`$TMUX` must be set). If not in tmux, inform the user and exit gracefully.

## Script location

All scripts live in this skill's `scripts/` directory:
- `swain-stage.sh` — main tmux layout and pane manager
- `swain-motd.py` — MOTD status panel (Textual TUI, runs via `uv run`)
- `swain-motd.sh` — legacy bash MOTD (kept as fallback if uv/Textual unavailable)

Resolve the script directory from this skill's install path.

## Commands

### Layout presets

Apply a named layout. Available presets are in `references/layouts/`:

| Layout | Description |
|--------|-------------|
| **focus** | Agent pane + MOTD top-right + file browser bottom-right |
| **review** | Agent + editor (changed files) + MOTD |
| **browse** | Agent + file browser + MOTD |

```bash
bash scripts/swain-stage.sh layout review
bash scripts/swain-stage.sh layout browse
bash scripts/swain-stage.sh layout focus
```

The default layout is configured in `swain.settings.json` under `stage.defaultLayout` (default: `focus`).

Users can override layout definitions in `swain.settings.json` under `stage.layouts.<name>`.

### Open individual panes

Open a specific pane type without applying a full layout:

```bash
bash scripts/swain-stage.sh pane editor file1.py file2.py   # editor with specific files
bash scripts/swain-stage.sh pane browser                      # file browser at repo root
bash scripts/swain-stage.sh pane browser /some/path           # file browser at specific path
bash scripts/swain-stage.sh pane motd                         # MOTD status panel
bash scripts/swain-stage.sh pane shell                        # plain shell
```

### MOTD management

The MOTD pane shows a dynamic status panel with:
- Project name, branch, and dirty state
- Animated spinner when the agent is working (braille, dots, or bar style)
- Current agent context (what it's doing)
- Active epic with progress ratio (from swain-status cache)
- Active bd task
- Ready (actionable) artifact count
- Last commit info
- Assigned GitHub issue count
- Count of touched files

The MOTD is a Textual TUI app (`swain-motd.py`) launched via `uv run`. It reads project data from `status-cache.json` (written by swain-status) when available, falling back to direct git/bd queries when the cache is absent or stale (>5 min). Agent state (spinner, context) is always read from `stage-status.json` for real-time responsiveness. Textual handles Unicode width correctly, provides proper box drawing with rounded corners, and supports color theming.

Control the MOTD:

```bash
bash scripts/swain-stage.sh motd start                        # start MOTD in a new pane
bash scripts/swain-stage.sh motd stop                         # kill the MOTD pane
bash scripts/swain-stage.sh motd update "reviewing auth module"  # update context
bash scripts/swain-stage.sh motd update "idle"                # mark as idle
bash scripts/swain-stage.sh motd update "done"                # mark as done/idle
```

### Close panes

```bash
bash scripts/swain-stage.sh close right     # close the right pane
bash scripts/swain-stage.sh close bottom    # close the bottom pane
bash scripts/swain-stage.sh close all       # reset to single pane
```

### Status

```bash
bash scripts/swain-stage.sh status          # show current layout info
```

### Reset

```bash
bash scripts/swain-stage.sh reset           # kill all panes except current
```

## Agent-triggered pane operations

The agent should use swain-stage directly during work. Recommended patterns:

### After making changes — open review

When you've finished modifying files, open them for the user to review:

```bash
bash scripts/swain-stage.sh motd update "changes ready for review"
bash scripts/swain-stage.sh pane editor file1.py file2.py
```

### During research — open file browser

When exploring the codebase:

```bash
bash scripts/swain-stage.sh pane browser src/components/
```

### Update context as you work

Keep the MOTD informed of what you're doing:

```bash
bash scripts/swain-stage.sh motd update "analyzing test failures"
bash scripts/swain-stage.sh motd update "writing migration script"
bash scripts/swain-stage.sh motd update "done"
```

### Clean up when done

```bash
bash scripts/swain-stage.sh close right
bash scripts/swain-stage.sh motd update "idle"
```

## Settings

Read from `swain.settings.json` (project) and `~/.config/swain/settings.json` (user override). User settings take precedence.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `editor` | string | `auto` | Editor command. `auto` detects: micro > helix > nano > vim |
| `fileBrowser` | string | `auto` | File browser command. `auto` detects: yazi > nnn > ranger > mc |
| `stage.defaultLayout` | string | `focus` | Layout applied by default |
| `stage.motd.refreshInterval` | number | `5` | MOTD refresh interval in seconds (idle) |
| `stage.motd.spinnerStyle` | string | `braille` | Spinner animation: `braille`, `dots`, or `bar` |
| `stage.layouts` | object | `{}` | User-defined layout overrides (same schema as preset files) |

## Error handling

- If not in tmux: report clearly and exit. Do not attempt tmux commands.
- If editor/file browser is not installed: warn the user and suggest alternatives or `swain.settings.json` override.
- If jq is not available: warn that settings cannot be read, use hardcoded defaults.
- Pane operations are best-effort — if a pane can't be created or found, warn but don't fail the session.
