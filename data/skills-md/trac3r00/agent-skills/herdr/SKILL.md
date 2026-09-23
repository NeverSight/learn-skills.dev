---
name: herdr
description: "Drive Herdr, a terminal workspace manager for AI coding agents, from any agent client (Claude Code, Codex, pi/senpi, Gemini, OpenCode, Kimi, Grok, Cursor, Hermes, and more). Covers the entire surface - workspaces, tabs, panes, agent lifecycle, worktrees, remote machines, integrations, config, and the 103-method socket API - so a client can build terminal layout, start and prompt sibling agents, read their output, wait on state changes, and coordinate parallel work. Use when the user mentions Herdr or when panes, tabs, sibling agents, or a persistent terminal session must be inspected or controlled."
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [herdr, terminal, multiplexer, panes, agents, orchestration, socket-api, cli]
---

# Herdr

Herdr is a terminal workspace manager built for coding agents. It organizes terminals
into **workspaces -> tabs -> panes**, recognizes the coding agent running inside a pane,
tracks that agent's lifecycle (`idle`, `working`, `blocked`, `done`, `unknown`), and
exposes the running session through the `herdr` CLI and a Unix-socket JSON API.

Two things follow from that, and this skill exists to exploit both:

1. **You can control terminals** - your own and the user's - without owning them.
2. **You can drive other agents** running in sibling panes exactly as a human would:
   start them, prompt them, read their output, wait for them to settle.

Reference set (read the one you need; every claim here is checkable against the binary):

| File | Contents |
|------|----------|
| `references/cli-reference.md` | Every command group, every subcommand, every flag, with examples |
| `references/api.md` | Socket API: envelope, 103 methods, event + subscription catalog, error codes, env injection |
| `references/config.md` | Every `config.toml` section and key, keybinding actions, themes, UI/toast/sound knobs |
| `references/integrations.md` | Supported agent kinds, per-client integration install/verify, what each integration writes |

## Environment gate (do this first)

```bash
test "${HERDR_ENV:-}" = 1 && echo "inside a Herdr pane: $HERDR_PANE_ID" || echo "not inside Herdr"
```

- **Gate passes** - you are running inside a Herdr-managed pane. You now have **caller
  context**: `HERDR_PANE_ID`, `HERDR_WORKSPACE_ID`, `HERDR_TAB_ID`, `HERDR_SOCKET_PATH`,
  `HERDR_BIN_PATH`. Prefer `--current` for pane commands and treat your own pane as home
  base. Your pane's own working directory is `$PWD`.
- **Gate fails** - the `herdr` CLI still works: it resolves the default session socket
  (`~/.config/herdr/herdr.sock`), so read-only discovery and explicit-ID control work
  from an ordinary shell or a non-Herdr agent session. What you lose is caller context:
  there is no `HERDR_PANE_ID`, `--current` does not apply, and the UI-focused pane may
  belong to the user or another client. In that mode **always** pass explicit
  `--pane`/`--workspace`/`--tab` IDs, or target a saved machine with
  `--machine <label>`, and never infer targets from sidebar order.

Never run bare `herdr` for discovery: it launches or attaches the interactive TUI. Use
`herdr --help`, `herdr <group> --help`, and `herdr <group> <sub> --help`. Likewise never
probe a mutating command by omitting arguments - `herdr workspace create` is valid with
defaults and will execute.

## Mental model

**Hierarchy and IDs.** Public IDs are opaque and stable:

| Object | Example | Notes |
|--------|---------|-------|
| Workspace | `w1`, `w19`, `w1J` | A directory-scoped space; sidebar "space" |
| Tab | `w1:t1` | Workspace-qualified |
| Pane | `w1:p1` | Workspace-qualified; hosts a terminal, and maybe an agent |

Closed tab/pane IDs are never reused. A pane moved to another workspace gets a **new**
workspace-qualified pane ID - read it from `.result.move_result.pane.pane_id` (the old
value is `.result.move_result.previous_pane_id`, kept alive only for the moved process's
inherited caller context).

Creation responses hand you the IDs to use next:

- `workspace create` -> `.result.workspace`, `.result.tab`, `.result.root_pane`
- `tab create` -> `.result.tab`, `.result.root_pane`
- `pane split` -> `.result.pane` (`.result.pane.pane_id`)

Parse IDs from JSON responses. Never derive them from examples, numbering, or sidebar order.

**Panes vs agents.** A pane is a terminal that exists whether or not an agent occupies it.
Use **pane** commands for ordinary processes (shells, tests, servers, log tails). Use
**agent** commands when Herdr must validate agent identity or interpret lifecycle state.

Agent targets accept either a unique live agent name or the pane ID hosting that agent -
never a terminal ID or a bare kind label (`claude`, `codex`). Names must match
`[a-z][a-z0-9_-]{0,31}` and be unique among live agents. A name follows the current pane
occupant and is cleared when that agent exits, is released, or is replaced.

**Lifecycle states.** `idle` and `done` both mean "ready for input"; the server's seen
state distinguishes them (explicit focus marks seen, reads do not), and each TUI client
tracks its own Done badge - so a badge can disagree with the CLI. `blocked` means Herdr
recognized an approval or question dialog. `unknown` means an agent is present but could
not be classified: it is **not** proof of completion.

**Caller context is injected into every managed pane**, which is what makes coordination
possible:

```bash
printf '%s\n' "$HERDR_WORKSPACE_ID" "$HERDR_TAB_ID" "$HERDR_PANE_ID"
```

An omitted `pane split` target means your own pane when `HERDR_PANE_ID` exists, otherwise
the UI-focused pane. Other commands may default to the UI-focused pane - which can belong
to someone else. Be explicit (`--current` or an ID) for anything that writes.

## Complete feature map

Every Herdr capability, by group. Flags and examples for each are in
`references/cli-reference.md`; `references/api.md` maps each to its socket method.

**Top level** - `--help`, `--version/-V`, `--skill` (print the vendor's agent skill),
`--default-config` (print default `config.toml`), `--session <name>` (use/create a named
persistent session), `--machine <label-or-id>` (run an API command on a saved SSH
machine), `--remote <ssh-target>` (attach through SSH; `--remote-keybindings
<local|server>`), `--handoff` (live handoff for update/remote attach), `update`,
`completion <shell>`, `status`, `server`, `api`, `config`, `channel`, `workspace`,
`worktree`, `tab`, `notification`, `agent`, `pane`, `session`, `machine`, `integration`.

| Group | Subcommands (the full set) |
|-------|----------------------------|
| `workspace` | `list`, `create`, `get`, `focus`, `rename`, `report-metadata`, `close` |
| `tab` | `list`, `create`, `get`, `focus`, `rename`, `close` |
| `pane` | `list`, `current`, `get`, `layout`, `process-info`, `neighbor`, `edges`, `focus`, `resize`, `zoom`, `read`, `rename`, `input`, `split`, `swap`, `move`, `close`, `send-text`, `send-keys`, `wait-output`, `run`, `report-agent`, `report-agent-session`, `release-agent`, `report-metadata` |
| `agent` | `list`, `get`, `read`, `send-keys`, `prompt`, `rename`, `focus`, `wait`, `attach`, `start`, `explain` |
| `worktree` | `list`, `create`, `open`, `remove` |
| `session` | `list`, `attach`, `stop`, `delete` |
| `machine` | `list`, `add`, `rename`, `remove`, `enable`, `disable` |
| `integration` | `install`, `uninstall`, `status` |
| `notification` | `show` |
| `config` | `check`, `reset-keys` |
| `channel` | `show`, `set <stable\|preview>` |
| `server` | `stop`, `reload-config`, `agent-manifests`, `update-agent-manifests`, `reload-agent-manifests` (bare `herdr server` runs headless) |
| `api` | `snapshot`, `schema [--json] [--output PATH]` |
| `status` | `[--json]`, `server`, `client` |

Beyond the CLI, protocol 22 exposes **103 socket methods** - including plugin management
(`plugin.*`), event streaming (`events.subscribe`, `events.wait`), layout capture and
restore (`layout.export`, `layout.apply`, `layout.set_split_ratio`), pane scroll/selection/
graphics/link activation (`pane.scroll`, `pane.selection.read`, `pane.graphics.*`,
`pane.link.activate`), agent view projection (`agent.view.set/clear`), popup control
(`popup.close`), and client shell/title control. See `references/api.md`.

## Standard recipes

All recipes assume the gate passed. Read IDs from the JSON you just got; do not predict them.

### Run a command in a sibling pane (keep the user's focus)

```bash
herdr pane layout --pane "$HERDR_PANE_ID"          # wide -> right, narrow/tall -> down
herdr pane split --current --direction right --cwd "$PWD" --no-focus
# -> read .result.pane.pane_id as $NEW
herdr pane run "$NEW" "pytest -q"
herdr pane wait-output "$NEW" --match "passed" --timeout 120000
herdr pane read "$NEW" --source recent-unwrapped --lines 120
```

`pane run` atomically sends text **and** Enter. `pane wait-output` searches the selected
snapshot immediately (so existing output can match) and then polls; `--match` is a literal
substring, `--regex` a Rust regex; omitting `--timeout` waits forever. Use `--no-focus`
unless the user asked to switch context. Avoid repeated same-direction splits that produce
unusably narrow columns or short rows.

### Start another agent and give it work

```bash
herdr agent start reviewer --kind codex --pane "$NEW"      # pane must be at a shell prompt
herdr agent prompt reviewer "Review the staged diff; report only actionable findings." \
  --wait --timeout 120000
herdr agent read reviewer --source recent-unwrapped --lines 120
herdr agent get reviewer
```

`agent start` never creates layout: the pane must exist, be at its interactive shell
prompt (shell in foreground, no running command/editor/agent), and the command returns
only after Herdr detects the expected agent and considers it ready (default timeout
30 s, max 300 s). Pass native agent flags after `--`.

`agent prompt` respects live bracketed-paste mode and writes text plus encoded Enter as one
ordered submission. `--wait` matches the first settled `idle`, `done`, or `blocked` state;
do not restate those with `--until`. If the agent is already at an approval/question dialog
the call is rejected with `agent_blocked` **before** sending input - inspect the UI and ask
the user before answering it. Submission from a non-working state must produce observed
`working`/`blocked` activity within 5 s or the call returns `agent_prompt_stalled`;
the caller timeout yields `timeout`. A timeout or stall does **not** prove the prompt was
never delivered - inspect with `agent get`/`agent read` before retrying.

Interactive UI control uses logical keys: `herdr agent send-keys reviewer esc` /
`ctrl+c`. Herdr validates all keys before writing any bytes. Use
`herdr agent wait <target> --until blocked --timeout 120000` when you specifically want to
catch an agent asking for input.

### Read terminal output well

Choose the source that matches the question:

- `visible` - the currently rendered viewport
- `recent` - recent rendered output, soft wraps included (default)
- `recent-unwrapped` - soft wraps joined; prefer for logs and transcripts
- `detection` - the plain-text bottom-buffer snapshot Herdr uses for agent detection

`--lines N` asks the server for more rows from screen plus host scrollback;
`--format ansi` (or `--ansi`) when styling is evidence; `--raw` keeps escape sequences.
Alternate-screen rows do not enter ordinary scrollback, though for supported idle agents
Herdr can collect application-owned history and restore the viewport.

If a large read still misses the answer, ask that agent to write its report to a Markdown
file in a temp dir and reply with the path, then read the file. Use that only as a fallback.

### Git worktree workspace

```bash
herdr worktree list --cwd "$PWD"
herdr worktree create --workspace "$HERDR_WORKSPACE_ID" --branch feat/x --base main --no-focus
herdr worktree open --path ~/src/repo/.worktrees/x
herdr worktree remove --workspace <ws> [--force]
```

`--trust-repository` grants per-request Git trust - use it only after the user has verified
the repository, never as a retry for a failed command. `worktree` actions require the
workspace to live inside a Git work tree (`not_git_worktree` otherwise).

### Remote machines

```bash
herdr machine list --json
herdr --machine <label-or-id> agent list
herdr --machine <label-or-id> pane list
herdr --machine <label-or-id> agent prompt <remote-agent> "status?" --wait --timeout 120000
```

The selector is an **enabled saved profile ID or a unique case-sensitive label** - not an
arbitrary SSH hostname. Do not combine `--machine` with `--session` or `--remote`. IDs are
per-server: two machines can both own `w1:p1`. Forwarding requires the remote server to
already run with an API-compatible version; it never installs, starts, or restarts one, and
never falls back to the local session. Local config, session management, installs, and
interactive attach are not forwarded. A connection failure does not prove a mutation did
not happen - inspect remote state before retrying. Add/remove/enable/disable profiles only
when the user asks; `machine add` uses the remote default session unless `--remote-session`
is given, and its setup prompt defaults to **No** when an incompatible server must be stopped.

### Named sessions (isolation)

```bash
herdr session list --json
herdr --session scratch pane list            # use or create a named session
herdr session stop scratch                   # then:
herdr session delete scratch                 # only stopped sessions delete
```

Use a named session for experiments that need an isolated server. Never run
`herdr server stop` from an active session unless the user explicitly wants the server and
its pane processes stopped; never kill the main Herdr process.

### Notify, inspect, diagnose

```bash
herdr notification show "Build finished" --body "12 tests green" --sound done
herdr api snapshot                      # whole live session in one JSON document
herdr status --json                     # client/server versions, protocol, compatibility
herdr agent explain <target> -v         # why Herdr classified an agent that way
herdr server agent-manifests --json     # active detection manifest versions
herdr config check                      # validate config.toml
```

Keep `notification show` for genuine user-facing milestones, not progress chatter.

## Socket API in one screen

Every CLI verb is a thin wrapper over one method. The wire format is a JSON object per
line over the session socket:

```json
{"id":"cli:pane:get","method":"pane.get","params":{"pane_id":"w1:p1"}}
{"id":"cli:pane:get","result":{"type":"pane_info","pane":{"pane_id":"w1:p1","agent_status":"idle"}}}
{"id":"cli:pane:get","error":{"code":"pane_not_found","message":"pane w99:p9 not found"}}
```

`herdr api schema --json` prints the bundled JSON schema (protocol 22, `schema_version` 1,
schemas: `request`, `success_response`, `error_response`, `event`, `subscription_event`);
`herdr api snapshot` returns the live `{agents, panes, tabs, workspaces, layouts,
focused_*}` document. 26 event types and 27 subscription types are catalogued in
`references/api.md`.

Exit codes: `0` success, `1` server/API error (JSON on stderr), `2` CLI syntax error.

## Configuration

Path: `~/.config/herdr/config.toml` (`HERDR_CONFIG_PATH` overrides). Sections: `theme`,
`terminal`, `update`, `keys`, `server`, `worktrees`, `ui` (sidebar, toasts, sound),
`session`, `remote`, `experimental`, `advanced`. `herdr config check` validates;
`herdr config reset-keys` backs up and clears custom keybindings; `herdr server
reload-config` applies changes to the running server; `herdr --default-config` prints the
annotated default. Full key-by-key reference: `references/config.md`.

## Client integrations

`herdr integration install <target>` wires agent-state reporting into a client so Herdr can
detect that agent, track lifecycle, and (when supported) resume its conversation after a
server restart. 18 targets: `pi`, `omp`, `claude`, `codex`, `copilot`, `devin`, `droid`,
`kimi`, `opencode`, `kilo`, `hermes`, `qodercli`, `qwen`, `cursor`, `mastracode`,
`antigravity-cli`, `grok`, `letta` (experimental).

```bash
herdr integration status                 # path + version per target, "current"/"outdated"
herdr integration status --outdated-only
herdr integration install codex          # reinstall/upgrade; overwrites managed files
```

Installed integrations are version-stamped and marked managed - add custom hooks beside
them, never inside them. Per-client paths, kinds, and verification steps:
`references/integrations.md`. Agents Herdr can *start* are a separate, larger list (24
kinds) - `gemini`, `agy`, `cline`, `kiro`, `amp`, `maki`, and `muse` have no matching
state-reporting target, so their lifecycle falls back to screen detection.

## Safety and etiquette

- Use `--no-focus` for background work unless the user asked to switch context.
- Target with `--current`, an explicit pane ID, or a unique agent name - never another
  client's focused pane.
- Do not close workspaces, tabs, panes, or sessions you did not create unless asked.
  `workspace.close` carries `close_group`, which also closes linked worktree workspaces;
  never add it merely to bypass `workspace_group_close_required`.
- Client and server versions can differ after an update. Check `herdr status` before
  relying on newer server features; a missing method is not permission to stop or upgrade
  the server.
- Read-only discovery is always safe; creation, focus changes, and closes are user-visible
  side effects and should be deliberate.
- Local configuration, session lifecycle, installation, and interactive attach are
  local-only operations - they are never forwarded to a remote machine.

## Verified environment

Facts above were measured against the installed binary on 2026-09-22:
`herdr 0.9.1`, client/server protocol **22**, endpoint protocol generation 1, capabilities
`live_handoff`, `detached_server_daemon`, `surface_interest`, `health_check`
(macOS arm64). Socket `~/.config/herdr/herdr.sock`; logs `herdr-server.log`,
`herdr-client.log`; state `~/.local/state/herdr/` (`agent-detection/`, `client-shell/`).
Error shapes observed live: `pane_not_found`, `agent_not_found`, `not_git_worktree`;
`agent_blocked`, `agent_prompt_stalled`, `agent_not_ready`, `timeout` are documented
lifecycle outcomes. Re-verify with `herdr --version` and `herdr status --json`, and re-run
`herdr api schema --json` after an update - the CLI binary, not this document, is the
authority on syntax.
