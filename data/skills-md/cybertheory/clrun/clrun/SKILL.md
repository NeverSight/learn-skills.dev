---
name: clrun
description: Run and control interactive CLI sessions for AI agents. Handles TUI prompts (select lists, checkboxes, confirms), persistent shell state, and long-running processes. Use when you need to execute terminal commands, respond to interactive prompts, navigate scaffolding wizards like create-vue or create-vite, or manage dev servers.
license: MIT
metadata:
  author: cybertheory
  version: "1.0.1"
compatibility: Requires Node.js >= 18. Works on macOS, Linux, and Windows.
---

# clrun — The Interactive CLI for AI Agents

No more `--yes` flags or command retries. `clrun` gives you full control over interactive terminal sessions with structured YAML responses.

## Install

```bash
npm install -g clrun
```

## Core Commands

| Action | Command |
|--------|---------|
| Run a command | `clrun <command>` |
| Send text + Enter | `clrun <id> "text"` |
| Send keystrokes | `clrun key <id> down enter` |
| Toggle checkbox | `clrun key <id> space` |
| Accept default | `clrun key <id> enter` |
| View output | `clrun tail <id>` |
| Check sessions | `clrun status` |
| Kill session | `clrun kill <id>` |
| Interrupt | `clrun key <id> ctrl-c` |

## Two Input Modes

**Text input** — sends text followed by Enter:
```bash
clrun <id> "my-project-name"    # Type and press Enter
clrun <id> ""                    # Just press Enter
```

**Keystroke input** — sends raw keys for TUI navigation:
```bash
clrun key <id> down down enter           # Select 3rd item in list
clrun key <id> space down space enter    # Toggle checkboxes 1 and 2
clrun key <id> enter                      # Accept default
```

Available keys: `up`, `down`, `left`, `right`, `enter`, `tab`, `escape`, `space`, `backspace`, `delete`, `home`, `end`, `pageup`, `pagedown`, `ctrl-c`, `ctrl-d`, `ctrl-z`, `ctrl-l`, `ctrl-a`, `ctrl-e`, `y`, `n`

## Identifying Prompt Types

When you `tail` a session, identify the prompt type to choose the right input:

| You see | Type | Action |
|---------|------|--------|
| `◆ Name: │ default` | Text input | `clrun <id> "value"` or `clrun key <id> enter` |
| `● Opt1 ○ Opt2 ○ Opt3` | Single-select | `clrun key <id> down... enter` |
| `◻ Opt1 ◻ Opt2 ◻ Opt3` | Multi-select | `clrun key <id> space down... enter` |
| `● Yes / ○ No` | Confirm | `clrun key <id> enter` or `right enter` |
| `(y/n)` | Simple confirm | `clrun <id> "y"` or `clrun <id> "n"` |
| `name: (default)` | Readline | `clrun <id> "value"` or `clrun <id> ""` |

## Select List Navigation

Count items from the top. First item is highlighted by default. To select item N, send N-1 `down` presses then `enter`.

```
◆  Select a framework:
│  ● Vanilla       ← 0 downs
│  ○ Vue           ← 1 down
│  ○ React         ← 2 downs
│  ○ Svelte        ← 3 downs
```

```bash
clrun key <id> down down enter   # Selects React
```

## Multi-Select Pattern

Plan a sequence of `space` (toggle) and `down` (skip) from top to bottom, ending with `enter`:

```bash
# Select items 1, 3, and 4 from a list of 5:
clrun key <id> space down down space down space enter
#              item1 skip  skip  item3 item4 confirm
```

## Reading Responses

All responses are structured YAML. Key fields:

- **`terminal_id`** — store this for all subsequent calls
- **`output`** — cleaned terminal output (ANSI stripped)
- **`status`** — `running`, `suspended`, `exited`, `killed`, `detached`
- **`hints`** — exact commands you can run next (copy-pasteable)
- **`warnings`** — detected issues with input or output

## Workflow Pattern

```
1. START    →  clrun <command>               → get terminal_id
2. OBSERVE  →  clrun tail <id>               → read output, identify prompt
3. INTERACT →  clrun <id> "text" / clrun key → respond to prompt
4. REPEAT   →  steps 2-3 until done
5. CLEANUP  →  clrun kill <id>               → if needed
```

## Shell Variable Quoting

Use single quotes to prevent your shell from expanding `$` variables:

```bash
clrun <id> 'echo $MY_VAR'          # Correct
clrun <id> "echo $MY_VAR"          # Wrong — expanded before clrun sees it
```

## Session Persistence

- Environment variables persist within a session
- Sessions auto-suspend after 5 min idle (env and cwd saved)
- Sending input to a suspended session auto-restores it
- No pre-check needed — just send input

See [references/tui-patterns.md](references/tui-patterns.md) for complete real-world examples.
