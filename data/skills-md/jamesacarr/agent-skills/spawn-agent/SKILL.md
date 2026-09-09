---
name: spawn-agent
description: Starts a named agent session (Claude Code, Codex, pi, or any Herdr-supported kind) in a new Herdr tab in the current workspace, optionally on a specific model. Use when the user asks to spawn an agent, open a new tab running Claude, Codex, or pi, or hand a side task to a fresh session (e.g. "/spawn-agent ABC-123", "spin up a codex agent for the docs"). Do NOT use to implement a ticket (use implement-ticket). Requires HERDR_ENV=1.
compatibility: Requires running inside Herdr (HERDR_ENV=1) with the herdr and jq CLIs available
---

# spawn-agent

## Essential Principles

- The script does the Herdr work; you resolve the inputs. `scripts/spawn-agent.sh` creates the tab, starts the agent in it, retries busy panes, suffixes colliding handles, closes the tab if the agent never starts, and sends at most one prompt.
- The parameters come from the user's words or a calling skill's explicit values, never from what a value resembles. An inferred value looks helpful and produces a session nobody asked for.
- The new session inherits only cwd. Its context is empty, so a task the user stated can only reach it as a prompt. When they stated none, an empty session waiting for their input is the intended result, not a gap to fill.

## Parameters

| Param | Flag | Required | Default |
|-------|------|----------|---------|
| `name` | `--name` | yes | - |
| `kind` | `--kind` | yes | the harness running this skill: Claude Code → `claude`, Codex → `codex`, pi → `pi` |
| `model` | `--model` | no | omitted, so the session starts on that agent's default |
| `task` | `--task` | no | none |
| `focus` | `--focus` / `--no-focus` | no | derived from `task` by the script |

`name` is free text (spaces and capitals are fine). It becomes the tab label, the session display name, and, slugified, the Herdr handle. Use it exactly as given. If it's missing and can't be inferred from the request, ask rather than inventing one.

`kind` needs no detection command: you know which harness is executing this skill. Pass an unfamiliar kind through untouched - Herdr validates it against its own list.

`model` is passed verbatim to the agent's model flag - never guess a value the user didn't give, and never translate a model between agents (`sonnet` means something to `claude` and nothing to `codex`). For reference: `claude` takes an alias (`opus`, `sonnet`, `fable`, `haiku`) or a full ID (`claude-opus-5`); `pi` takes a pattern or ID (`provider/id`, fuzzy like `*sonnet*`, optional `:<thinking>` suffix); `codex` takes a model ID. For any other kind the script rejects `--model` because it can't know that CLI's flag; check `<cli> --help` and pass the flag after `--`.

`task` is set when the user stated a task in words ("spawn an agent to review the auth MR") or a calling skill supplies one. Leave it unset otherwise. `name` never implies a task: a name that looks like a ticket ID (`ABC-123`) is a label the user chose, not a request to look the ticket up, rename the session after its summary, or start work on it.

`focus` follows `task` unless a flag is passed: a task set means the user delegated and stays put (no focus); no task means the empty session waits for their input, so land them there (focus). Pass a flag only for an explicit choice: "open a tab" or "take me there" is `--focus`, and a calling skill's `focus` always wins.

## Process

### Step 1: Run the Script

Run it by its absolute path under this skill's directory, with your cwd in the repo the new session should work in - the script passes its cwd, not its own location, to the tab:

```bash
<skill-dir>/scripts/spawn-agent.sh --name "<name>" --kind <kind> [--model <model>] [--task "<task>"] [--focus|--no-focus]
```

On success it prints one JSON object: `handle`, `tab_id`, `pane_id`, `label`, `kind`, `model`, `status`, `task_sent`. Diagnostics, including the pane's own output on failure, go to stderr.

### Step 2: Act on the Exit Code

| Exit | State | Do |
|------|-------|----|
| 0 | Session ready; task sent if given | Report |
| 1 | Herdr failed; the tab is already closed | Relay the stderr - it includes the shell's own error - and stop. Don't re-run unchanged |
| 2 | Usage or preflight failure; nothing created | Not inside Herdr → say so and stop. Otherwise fix the invocation |
| 3 | Session up but blocked at a startup dialog (folder trust, MCP consent); task not sent | Read the pane and ask the user before answering it - those are consent decisions. Don't re-run; the tab exists |
| 4 | Session up; prompt failed | Read the pane and report. Don't re-run |

### Step 3: Report Back

Give the user the tab label, the handle, the kind (when it isn't the default), the model if one was requested, and how to drive it:

```bash
herdr agent prompt <handle> "<text>"
```

Leave off `--wait`: it blocks the caller until the agent finishes its turn, which undoes the delegation. The user can read the pane or ask you to check on it later.

## Anti-Patterns

- **Reading a task into a ticket-shaped name.** `/spawn-agent ABC-123` creates a session named `ABC-123` and stops. Looking the ticket up, drafting a brief, or inventing an implement prompt imports another skill's behaviour the user didn't ask for. When they want the ticket worked they say so, and implement-ticket calls this skill with the task spelled out - a supplied task is fine, an inferred one is not.
- **Improving the name.** A user-supplied `name` is used as given, IDs and capitals included. Substituting a "more descriptive" label breaks the handle other skills derive from the ticket ID (merge-ticket looks the agent up by it).
- **Prompting to fill the silence.** With `task` unset, an idle session is the successful outcome. Don't send a greeting, a summary of cwd, or a guessed task.
- **Running the herdr commands by hand.** Bypassing the script drops every quirk it encodes, and the failures come back as confusing timeouts and orphan tabs. If the script can't do what's needed, that's a change to the script.

## Success Criteria

- The script ran once. Exactly one tab exists in the current workspace, labelled `name`, cwd matching the invoking session, focused only when `focus` resolved to yes.
- `herdr agent list` shows the handle with the resolved kind; for `claude` and `pi` the terminal title reads `name`.
- The session runs the requested model, or that agent's default when `model` was omitted.
- With `task` set, the session received it once; with `task` unset, it received no prompt.
