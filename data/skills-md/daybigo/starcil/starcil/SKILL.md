---
name: starcil
description: "Control Starcil, the terminal workspace for AI coding agents, from inside one of its panes (requires STARCIL_ENV=1). Use it to inspect neighboring panes and agents, split panes, run commands, read output and wait for state changes — and use it PROACTIVELY to work as a fleet: start peer agents (any installed CLI, same vendor or mixed) in sibling panes, hand them compiled briefs, run them in parallel, unblock them, collect their results by file and synthesize. Covers the command mechanics, the orchestration doctrine (roles, briefs, waits, debates, budget) and the platform gotchas."
---

# Starcil

Starcil organizes terminals into workspaces, tabs and panes, recognizes the coding agents
running inside panes, tracks their lifecycle (`idle · working · blocked · done · unknown`) and
exposes the whole session through the `starcil` CLI. An agent inside a pane can therefore
create layout, run commands, and start and steer other agents: **agents orchestrating agents**.

Part 1 is the command reference. Part 2 is how to work as a fleet. Read both before your first
orchestration; return to Part 1 for exact syntax.

## Guardrail

Before any control command, verify that you run inside a Starcil-managed pane:

```bash
test "${STARCIL_ENV:-}" = 1        # bash / zsh
```

```powershell
$env:STARCIL_ENV -eq "1"           # PowerShell
```

If the check fails, say that you are not running inside Starcil and stop. Never inspect or drive
someone else's Starcil session from outside it.

---

# Part 1 — Command mechanics

## Learn the current CLI

The installed binary is the authority for syntax, not this file. Start with `starcil --help`,
then print a command group by running it without a subcommand:

```bash
starcil agent
starcil pane
starcil workspace
starcil tab
starcil worktree
starcil session
```

Do not run bare `starcil` for discovery: it launches or attaches the TUI. Do not probe a
mutating command by omitting arguments (`starcil workspace create` is valid with defaults and
executes). Control commands return JSON: read identifiers and state from those responses instead
of predicting them. Server errors are JSON on stderr with exit status 1; syntax errors exit 2.

## Model

- **Workspace → tab → pane** organize terminal locations. IDs are opaque stable handles:
  `w1`, `w1:t1`, `w1:p1`. Closed IDs are never reused.
- A **pane** is a terminal whether or not an agent runs in it. Pane commands control raw
  terminals: shells, tests, servers, input, output.
- An **agent** is Starcil's recognition of a supported CLI occupying a pane. Agent commands
  add identity validation and lifecycle interpretation. They accept a unique live agent name
  or the pane ID hosting the agent. Names match `[a-z][a-z0-9_-]{0,31}`.
- **States.** `working`: a turn is running. `idle`: ready for input, and its tab has been seen
  in the UI. `done`: the same idle state after work finished while nobody was looking; focusing
  the pane (or `agent focus`) marks it seen, CLI reads do not. `blocked`: Starcil recognized an
  approval, trust, y/n, password or selection prompt — the agent needs a decision. `unknown`:
  an agent is present but cannot be classified; it does not prove completion.
- Lifecycle evidence, strongest first: dead process → installed hook reports
  (`starcil integration install claude|codex`) → screen rules from the agent manifest →
  screen-stability fallback. `starcil agent explain <target> --verbose` shows which one won.

## Caller context and IDs

Starcil injects the caller's location into every managed pane:

```bash
printf '%s\n' "$STARCIL_WORKSPACE_ID" "$STARCIL_TAB_ID" "$STARCIL_PANE_ID"   # bash
```

```powershell
$env:STARCIL_WORKSPACE_ID; $env:STARCIL_TAB_ID; $env:STARCIL_PANE_ID          # PowerShell
```

Prefer `--current` when a pane command should target the calling pane. Omitting a target may
resolve to the UI-focused pane, which can belong to the user or to another client. Discover
live state with:

```bash
starcil workspace list
starcil tab list --workspace "$STARCIL_WORKSPACE_ID"
starcil pane list --workspace "$STARCIL_WORKSPACE_ID"
starcil agent list
```

Creation responses carry the IDs to use next: `workspace create` → `.result.workspace`,
`.result.tab`, `.result.root_pane`; `tab create` → `.result.tab`, `.result.root_pane`;
`pane split` → `.result.pane.pane_id`.

## Create layout

Default to a sibling pane in the current tab with the caller's working directory. Do not create
a workspace, tab, worktree or different cwd unless the task or the user asks for that topology.
Inspect the caller's geometry, then split a wide pane to the right and a tall pane down; avoid
repeated same-direction splits that leave unusable slivers. Keep the user's focus where it is:

```bash
starcil pane layout --current
starcil pane split --current --direction right --cwd "$PWD" --no-focus
```

Read the new pane from `.result.pane.pane_id`. `pane move --new-tab` / `--new-workspace`
relocate a pane later; `pane close <id>` closes only panes you created.

## Run an ordinary command and read its output

```bash
starcil pane run <pane> "cargo test"
starcil pane wait-output <pane> --match "test result" --timeout 120000
starcil pane read <pane> --source recent-unwrapped --lines 120
```

- `pane run` sends the command text and Enter atomically. `pane send-text` does NOT imply
  Enter; `pane send-keys <pane> enter` adds it.
- `pane wait-output` checks the selected snapshot immediately (existing output can match),
  then polls. `--match` is a literal substring, `--regex` a Rust regex. Without `--timeout`
  it waits forever: always pass one.
- Read sources: `visible` (rendered viewport), `recent` (recent output with soft wraps),
  `recent-unwrapped` (soft wraps joined — prefer it for logs and transcripts). `agent read`
  adds `detection`, the plain-text bottom buffer used to classify agents. Add `--format ansi`
  only when colors are evidence.
- **Alternate-screen limit.** Most agent CLIs draw on the terminal's alternate screen, where
  rows that scroll away never enter scrollback. If a larger `--lines` does not reveal more of a
  finished answer, stop increasing it: ask the agent to write its full answer to a file and
  reply with the path, then read the file. Better: design tasks so results travel by file from
  the start (Part 2).

## Start a peer agent

```bash
starcil pane split --current --direction right --cwd "$PWD" --no-focus
starcil agent start reviewer --kind codex --pane <returned-pane-id> --timeout 60000
```

- Kinds: `starcil agent` prints the accepted list (claude, codex, gemini, opencode, copilot,
  kimi, amp, cursor, … 21 kinds). The kind must be installed on the machine; check before
  starting (`command -v claude` / `Get-Command claude`). A CLI that is not a kind can still be
  driven through `pane run` + `pane wait-output`, without lifecycle states.
- The target pane must be an available shell at its prompt: no editor, server or agent
  running. Starting never creates or moves layout.
- `agent start` types `<program> [args]` + Enter into that shell, assigns the name, then waits
  up to `--timeout` (default 30 s) for the agent to come up: its UI positively recognized (a
  screen rule or a hook report; for kinds without screen rules, a settled screen) with a process
  running under the shell. The response carries `.result.startup.outcome`: `reached` (with
  `.state`: `idle`, or `blocked` on a startup gate), `exited` (the shell is back at its prompt:
  the program is not installed or crashed — read the pane for the error) or `timeout`. None of
  them is an error and the command was already typed — **never retry a start**; read the pane
  and decide. Native arguments go after `--`.
- **Startup gates.** On `blocked`, read before unblocking:
  `starcil agent read <name> --source visible` → identify the gate → answer with logical keys,
  e.g. `starcil agent send-keys <name> enter` (or `down` then `enter`). Common gates: directory
  trust (approve only directories you created or own), update prompts (skip mid-task, update
  deliberately later), login (hand it to the user — never type credentials).
- After the first `idle`, read the visible screen once and confirm it is the CLI, model and
  working directory you expected. Configuration only applies to new instances.

## Prompt, wait, read

```bash
starcil agent prompt reviewer "Review the current diff. Report only actionable findings." --wait --timeout 300000
starcil agent read reviewer --source recent-unwrapped --lines 120
```

- `agent prompt` pastes the text honoring the pane's bracketed-paste mode, then sends Enter as
  a separate write. `--wait` returns at the first settled state (`idle`, `done` or `blocked`);
  `--until STATE` (repeatable) replaces that set. Always pass `--timeout`.
- **Stall rule.** A prompt sent to a non-working agent must change its state within 5 s or
  the call returns the error `agent_prompt_stalled` (the prompt was probably not consumed).
  Read the pane, then decide — do not blindly resend.
- **Multiline prompts.** Some CLIs treat a pasted multiline block as a draft (`[Pasted
  Content …]`) and stay idle. After any multiline `agent prompt`, read the pane; if the draft
  is sitting there, `starcil agent send-keys <name> enter`. Symptom of forgetting: the agent
  looks idle and never started.
- `agent wait <target> [--until STATE]... --timeout MS` waits without sending input. It is a
  plain wait: an agent already in a target state returns immediately and it never stalls. Use
  `--until blocked` for "tell me when it asks something".
- On `blocked`, inspect `agent get` and `agent read` before sending anything. Logical keys
  are validated before any byte is written: `enter`, `esc`, `ctrl+c`, `down`, `y`, …

## Custom lifecycle and metadata

External hooks can publish state through the public pane commands
(`pane report-agent`, `pane report-agent-session`, `pane report-metadata`,
`pane release-agent`) with a namespaced `--source`. See `starcil pane` for syntax. Report
`blocked` only for a real user gate.

---

# Part 2 — Working as a fleet

## When to orchestrate

Delegate proactively — the user does not need to mention Starcil — when the task has
independent slices, would take you more than a few minutes of pure execution, benefits from a
second model's review or perspective, or is a long campaign (test sweeps, migrations, research
across many files). Do not delegate small edits, anything whose answer you already know, or
work that depends on every step of its own output.

You are the **coordinator**: a player-coach. Take the architecturally hardest slice yourself,
compile every brief, judge every review, synthesize every debate. Peers are **full agent
instances** with their own context, visible to the user in their own panes and steerable by
them — that is why a peer in a pane beats an internal subagent when the human wants to watch,
interrupt or redirect the work.

## Budget: the smallest fleet that fits

Peers consume the user's quota or money. Size the fleet by independent slices, not by
enthusiasm:

- 0 peers for a task you can finish in minutes. 1 peer for a review or one independent slice.
  N peers only for N independent slices that are ready to start now.
- Reuse before you spawn: `starcil agent list` — an `idle`/`done` peer of the right kind can take
  the next brief.
- One vendor is enough. Same-kind peers (Claude coordinating Claude, Codex coordinating Codex)
  are full instances with separate context; mixed vendors add a second perspective, not a
  requirement.
- If a free or local CLI is installed, give it the mechanical bulk (fixtures, renames,
  formatting, running suites) and keep the stronger paid agent for judgment.
- Close the panes you created when their work is harvested, unless the user wants to keep them.

## Briefs: the compiled contract

Never forward the user's raw request. Peers execute explicit specs brilliantly and fill gaps
poorly, so compile:

```markdown
You are <name>, a peer agent in this fleet — a full <kind> instance, not a subagent.
I am <your name>, a <your kind> agent coordinating on behalf of <user>, the human owner.
# TASK: <one sentence>
## Context — exact files and what each one does (do not explore beyond this)
## Constraints — non-negotiables (style, security, scope, what must not change)
## Acceptance criteria — verifiable, with the command that proves each one
## Deliverable — write your full report to <dir>/.fleet/result-<id>.md
## Do NOT — the gaps you must not fill with assumptions
When everything is done and verified on disk, print exactly: FLEET_DONE
```

Write briefs and result files in English unless the project's convention differs; speak to the
user in their language. One directory, one writer: partition by directory, or give each peer
its own git worktree (`starcil worktree` — print the group for syntax) when several must edit
the same repository.

## Dispatch without blocking

- Fire every `agent prompt` WITHOUT `--wait`, then keep working your own slice. Foreground
  waiting serializes the fleet and wastes the point.
- Doorbell: run `starcil agent wait <name> --timeout <ms>` as a background task (in Claude Code,
  Bash with `run_in_background`). Waits without `--timeout` block forever.
- Harvest cheaply between your own chunks: `starcil agent list` (states) then read only what
  changed.
- **Blocked peers are silent.** Every harvest checks for `blocked`, reads what is being asked
  (`starcil agent read <name> --source recent-unwrapped`) and only then answers with
  `send-keys`. Read before approving; approve only actions you would take yourself.
- Results travel by **file**, never by scraping panes: each peer writes
  `.fleet/result-<id>.md` and prints `FLEET_DONE`.
- **Sentinel echo trap.** `pane wait-output --match FLEET_DONE` fires on the brief's own text
  ("print exactly: FLEET_DONE") sitting in the transcript. Wait on the result file instead
  (`until [ -s .fleet/result-<id>.md ]; do sleep 20; done`), or make the sentinel unguessable
  and only wait for it after the brief has scrolled away.
- After every multiline brief: read the pane; dispatch a stuck paste with `send-keys enter`.

## Debate protocol (design questions)

- Anti-anchoring: for an open question, ask the peer for ITS plan before showing yours;
  otherwise you get your own plan decorated with praise.
- Then a critique exchange: each side attacks the other's proposal ("weakest assumption,
  missing risk, better alternative"). **Maximum two rounds** — further rounds converge by
  politeness, not depth.
- Circuit breaker: on agreement or at the round limit, write `.fleet/consensus-<topic>.md`.
  Both sides stop prompting each other once that file exists.
- Synthesize against the ORIGINAL goal (long agent conversations drift). The user decides.

## Safety rails

- `--no-focus` for every background spawn; never steal the user's focus.
- Never close workspaces, tabs, panes or sessions you did not create unless the user asks.
- Never run `starcil server stop` or `starcil session stop` from a live session unless the user
  explicitly intends to stop every process in it. Use a named session
  (`starcil --session <name> …`) for experiments that need an isolated server.
- Never type credentials, tokens or payment details into a peer's gate. Hand those to the user.
- Reports are honest: a failing acceptance criterion is FAIL, a skipped check is SKIP with its
  reason. Verify a peer's claim on disk before repeating it to the user.

---

# Platform notes

- **PowerShell vs. bash.** Every example above works in both; adapt quoting (`"$PWD"` → `"$PWD"`
  works in PowerShell too, `$STARCIL_PANE_ID` → `$env:STARCIL_PANE_ID`). Prefer the shell the
  pane already runs (Starcil defaults to PowerShell on Windows, the user's `$SHELL` elsewhere).
- **Git Bash on Windows mangles slash commands.** `starcil agent prompt rev "/status"` arrives
  as `C:/Program Files/Git/status`. Prefix `MSYS_NO_PATHCONV=1` or send it from PowerShell.
- **Windows startup.** `agent start` types the launch command into the pane's shell, so it works
  the same as on Unix; there is no launcher to work around.
- **Shell prompt symbols.** Some prompt themes print `❯` or `›`, the glyphs Claude Code and
  Codex use for their input box; the detector may read a bare shell as `idle` for a moment.
  Confirm with a screen read before the first prompt.
- **Nested Starcil.** Starting `starcil` inside a Starcil pane is refused by default; drive the
  outer session with the CLI instead.
