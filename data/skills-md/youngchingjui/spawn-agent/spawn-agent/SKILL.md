---
name: spawn-agent
description: "Spawn an independent agent in a separate terminal pane for parallel work. Detects your terminal environment and guides you to the right spawn command."
disable-model-invocation: true
metadata:
  author: youngchingjui
  version: "3.0.0"
---

# Spawn Agent

Spawn an independent, full-fledged agent in a separate terminal pane.

## Why spawn externally?

Some agents (Claude Code, Codex, etc.) have built-in sub-agent capabilities that run within the same thread. Those sub-agents are useful for quick, autonomous tasks — but they have limitations:

- You **can't see what the sub-agent is doing** in real time
- You **can't interact with it** — it runs autonomously and returns results
- It's designed for **simpler, contained tasks** that don't need human guidance

This skill enables a different workflow: **spawn a fully independent agent in its own terminal pane.** The spawned agent:

- Runs in its own visible pane/window — you can **watch it work**
- Is **fully interactive** — the user can guide it, answer questions, course-correct
- Handles **complex, independent tasks** that benefit from human oversight
- Works **in parallel** — the originating agent continues its own work

As an agent, you write better prompts for other agents than humans typically do. When you identify a task that should be delegated, craft a detailed prompt and spawn it off.

## How to spawn

### 1. Determine the spawn method

Before spawning, you need to know two things: **which terminal environment** you're in, and the **user's preferences** (split direction, agent command). Resolve these in order:

1. **Check saved config.** Read `~/.claude/spawn-agent.json` — it may already have the terminal type and user preferences from a previous run.

2. **Look for context clues.** Environment variables can tell you directly:

   - `$TMUX` is set → you're in tmux
   - `$TERM_PROGRAM` = `vscode` → you're in VS Code's integrated terminal
   - `$TERM_PROGRAM` = `iTerm.app` → you're in iTerm2
   - On macOS with none of the above → likely Terminal.app
   - On Linux → check for gnome-terminal, xterm, etc.

3. **Run the helper script.** If you're still unsure, run the detection script — it checks these same environment variables and saves the result:

   ```bash
   bash "${CLAUDE_SKILL_DIR}/scripts/detect-terminal.sh"
   ```

   This writes to `~/.claude/spawn-agent.json` (preserving any existing user preferences).

4. **Ask the user.** If the environment is ambiguous or you want to confirm their preference, just ask. This is especially useful the first time — the user may want a specific split direction or agent command.

### Config file

The config file `~/.claude/spawn-agent.json` stores both detected environment and user preferences:

```json
{
  "terminal": "tmux",
  "split": "vertical",
  "agent_command": "claude"
}
```

| Key             | Description                                                                | Default       |
| --------------- | -------------------------------------------------------------------------- | ------------- |
| `terminal`      | Terminal environment (`tmux`, `iterm2`, `terminal-app`, `vscode`, `linux`) | auto-detected |
| `split`         | Preferred split direction: `vertical` or `horizontal`                      | `vertical`    |
| `agent_command` | Command to launch the agent (e.g. `claude`, `codex`)                       | `claude`      |

If preferences aren't set, use sensible defaults (vertical split, `claude` as the agent command).

### 2. Spawn the agent

Based on the terminal environment, run the matching command directly. Replace `AGENT_CMD` with the configured agent command, and `PROMPT` with your crafted prompt.

#### tmux

```bash
tmux split-window -h -c "$(pwd)" "AGENT_CMD 'PROMPT'"
```

- `-h` = vertical split (side-by-side). Use `-v` for horizontal (top-bottom).
- `-c "$(pwd)"` = start in the current directory. Use `-c "/other/path"` for a different directory.

#### iTerm2

```bash
osascript -e '
tell application "iTerm2"
  tell current session of current window
    set newSession to (split vertically with default profile)
  end tell
  tell newSession
    write text "cd /path/to/project && AGENT_CMD '\''PROMPT'\''"
  end tell
end tell'
```

Change `split vertically` to `split horizontally` for a top-bottom split.

#### Terminal.app (macOS fallback)

```bash
osascript -e '
tell application "Terminal"
  activate
  do script "cd /path/to/project && AGENT_CMD '\''PROMPT'\''"
end tell'
```

Opens a new window. Terminal.app doesn't support split panes, and opening a new tab requires Accessibility permissions that agents typically don't have.

#### VS Code integrated terminal

```bash
# Open a new terminal in the VS Code terminal panel
code -r --command workbench.action.terminal.new
# Then type the command into it — VS Code terminals don't support direct command injection,
# so print instructions for the user to paste, or use the VS Code CLI if available.
```

#### Linux terminals

```bash
# gnome-terminal
gnome-terminal --working-directory="$(pwd)" -- bash -lc "AGENT_CMD 'PROMPT'; exec \$SHELL"

# xterm
xterm -e bash -lc "cd '$(pwd)' && AGENT_CMD 'PROMPT'; exec \$SHELL" &
```

## Best practices

- **Interactive mode only.** The spawned agent must run interactively so the user can guide it. Never pass flags that suppress interactivity (e.g. `--print`, `-p`).
- **Write a detailed prompt.** Include all context the spawned agent needs: what to do, which files matter, expected outcome, and constraints.
- **Use `$ARGUMENTS`** as the prompt text when the user invokes this skill directly.
