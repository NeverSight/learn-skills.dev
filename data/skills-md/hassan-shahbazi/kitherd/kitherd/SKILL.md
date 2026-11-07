---
name: kitherd
description: Orchestrate multi-agent workflows using a headless Herdr server and Kitty terminal as the GUI window manager. Use whenever spawning, monitoring, coordinating, or viewing AI worker agents in Kitty splits and tabs.
compatibility: Requires herdr (running in headless server mode), kitty (with remote control enabled), and python3.
---

# Headless Herdr with Kitty

This skill guides an AI coordinator (master) agent on how to manage worker agents using **Herdr** as the headless background process manager and **Kitty** as the native GUI window manager.

In this architecture:
- **Headless Herdr Server (`default` session):** Runs as a background daemon (systemd service on Linux, launchd agent on macOS). It manages panes, terminal emulators, agent processes, and persistent lifecycles with no interactive TUI.
- **Kitty Terminal:** Serves as the visual interface. Rather than running a multiplexer UI, worker agents are viewed as native Kitty splits and tabs via `kitty @ launch ... herdr agent attach <name>`. Closing a Kitty split only detaches the view; the worker agent continues running in the background.
- **Interactive Switcher (`herdr_panel.py`):** The user can open an interactive fzf panel listing all agents with real-time status to attach or terminate them with a defined keybinding.

---

## Core Orchestration Rules

1. **Target the Default Session:**
   Always use plain `herdr` commands without `--session <name>`. Named sessions belong to interactive TUI workflows; do not create headless workers in them unless explicitly instructed.

2. **Strict Master-Worker Hierarchy:**
   The master agent is the single coordinator that spawns, prompts, monitors, and stops worker agents. Workers must **never** spawn or control other agents; recursive or peer agent spawning obscures the decision tree and breaks coordination.

3. **Herdr Environment Guards:**
   The standard Herdr skill's `HERDR_ENV=1` guard applies to interactive TUI panes, not the headless default session. You can safely run `herdr` CLI commands from any shell. Because the master runs outside a managed Herdr pane, `--current` and `$HERDR_PANE_ID` are unavailable; **always target explicit pane IDs or unique agent names**.

4. **Directory Isolation via Workspaces:**
   Every project directory must have its own dedicated Herdr workspace. Multiple workers for the same project share that workspace. Never mix workers from different repositories or projects in the same workspace to prevent context contamination during concurrent runs.

5. **Mandatory Absolute `--cwd`:**
   `--cwd` is **mandatory** on every `workspace create`, `tab create`, and `pane split`. It must be an **absolute path** (use `"$PWD"` for the current project root). Herdr CLI does not automatically inherit the caller's working directory; omitting `--cwd` causes the new pane to inherit whichever workspace was previously focused or fall back to `$HOME`. Confirm the `cwd` field in JSON responses before starting an agent.

6. **Kitty Remote Launch Parity (`--match`, `--next-to`, `--copy-env` and `--cwd`):**
   When opening a window or tab in Kitty via `kitty @ launch`, **always pass `--match`, `--next-to`, `--copy-env` and `--cwd="$PWD"`**:
   ```bash
   kitty @ launch --match "window_id:$KITTY_WINDOW_ID" --next-to "id:$KITTY_WINDOW_ID" --type=window --location=vsplit --copy-env --cwd="$PWD" herdr agent attach <worker-name>
   ```
   - `--match "window_id:$KITTY_WINDOW_ID"` and `--next-to "id:$KITTY_WINDOW_ID"`: Without them, Kitty opens the split in whichever tab is active, which is wrong once the user switches tabs. Kitty sets `KITTY_WINDOW_ID` in the master's own window, so `--match` targets the master's tab and `--next-to` splits beside the master. With `--type=tab`, `--next-to` keeps the new tab in the master's OS window. If `KITTY_WINDOW_ID` is empty, the master is not running inside Kitty; ask the user before launching.
   - `--copy-env`: Kitty's GUI process is spawned by systemd, launchd, or the desktop manager with a minimal environment. `--copy-env` propagates your active shell environment (PATH, API keys, virtualenvs, direnv).
   - `--cwd="$PWD"`: Sets the working directory of the Kitty window container. Without this, new splits (`alt+enter`), tabs, or helper terminals created inside that Kitty window default to `$HOME`. Note: `herdr agent attach` is a client proxy, not a shell, so Kitty's `--cwd=last_reported` cannot detect the agent's directory automatically.

7. **Prefer Splits Over Tabs:**
   Always default to Kitty vertical splits (`--location=vsplit`) when attaching new worker agents so the user can observe progress side-by-side. Use horizontal splits (`--location=hsplit`) or tabs (`--type=tab --tab-title <worker-name>`) only if requested or if screen space is constrained.

---

## Step-by-Step Workflow

### Step 1: Ensure Project Workspace Exists

Check active workspaces:
```bash
herdr workspace list
```

If no workspace corresponds to your project directory (`"$PWD"`), create one:
```bash
herdr workspace create --cwd "$PWD" --label "<project-name>" --no-focus
```
Parse the `workspace_id` (e.g. `w1`) from `.result.workspace.workspace_id`.

### Step 2: Create a Dedicated Tab/Pane for the Worker

Create a new tab in the project's workspace:
```bash
herdr tab create --workspace <workspace-id> --cwd "$PWD" --label "<worker-name>" --no-focus
```

Extract the `pane_id` from `.result.root_pane.pane_id` in the JSON response (e.g. `w1:p2`). Verify that `.result.root_pane.cwd` matches your project path.

### Step 3: Start the Agent in the Pane

Start the worker agent in the newly created pane:
```bash
herdr agent start <worker-name> --kind <kind> --pane <pane-id> -- <agent-args...>
```

- Supported `--kind` values include: `claude`, `codex`, `copilot`, `opencode`, `agy`, `pi`, `gemini`, `cursor`, `amp`, `cline`, `omp`, `devin`, etc.
- Pass flags specific to the agent after `--` (e.g. `--dangerously-skip-permissions` or `--model ...`).
- `herdr agent start` blocks until Herdr detects that the interactive agent has booted and reached an idle, ready prompt.

### Step 4: Open a Visual View in Kitty

Attach a Kitty split to view the agent:
```bash
kitty @ launch --match "window_id:$KITTY_WINDOW_ID" --next-to "id:$KITTY_WINDOW_ID" --type=window --location=vsplit --copy-env --cwd="$PWD" herdr agent attach <worker-name>
```

For a horizontal split, use `--location=hsplit`. For a new tab, use `--type=tab --tab-title <worker-name>`.

### Step 5: Coordinate, Prompt, and Monitor

Submit instructions to the worker:
```bash
herdr agent prompt <worker-name> "<instruction-text>" --wait
```

- `--wait`: Waits until the agent returns to an idle, done, or blocked state.
- Inspect overall fleet status at any time:
  ```bash
  herdr agent list
  ```

### Step 6: Handling Blocked Agents and Approvals

When `herdr agent list` reports an agent status as `blocked`:
1. Inspect the terminal screen to understand what the agent is asking:
   ```bash
   herdr agent read <worker-name> --source visible
   ```
2. **Caution with Claude Code:** Claude Code's inline autosuggestions (ghost text in the input box) can occasionally cause Herdr's detector to report `blocked` when the agent is actually idle. Always confirm with `herdr agent read` before attempting to answer a prompt.
3. Send necessary confirmation or keys:
   ```bash
   herdr agent send-keys <worker-name> y
   herdr agent send-keys <worker-name> enter
   ```

### Step 7: Teardown and Cleanup

When a worker completes its assigned task and is no longer needed:
1. Close its Herdr pane on the server:
   ```bash
   herdr pane close <pane-id>
   ```
2. The associated Kitty split or window will terminate automatically once the attached process exits.

---

## Quick Reference CLI Commands

| Action | Command |
| :--- | :--- |
| **List Workspaces** | `herdr workspace list` |
| **Create Workspace** | `herdr workspace create --cwd "$PWD" --label <name> --no-focus` |
| **Create Tab / Pane** | `herdr tab create --workspace <ws> --cwd "$PWD" --label <name> --no-focus` |
| **Start Agent** | `herdr agent start <name> --kind <kind> --pane <pane-id> -- <args>` |
| **Attach View in Kitty** | `kitty @ launch --match "window_id:$KITTY_WINDOW_ID" --next-to "id:$KITTY_WINDOW_ID" --type=window --location=vsplit --copy-env --cwd="$PWD" herdr agent attach <name>` |
| **Prompt Agent** | `herdr agent prompt <name> "<prompt>" --wait` |
| **Check Fleet Status** | `herdr agent list` |
| **Read Agent Output** | `herdr agent read <name> --source visible` (or `--source recent-unwrapped`) |
| **Send Keys to Agent** | `herdr agent send-keys <name> <key>` |
| **Close Pane** | `herdr pane close <pane-id>` |
