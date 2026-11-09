---
name: unreal-game-dev
description: Use when the user wants to create, set up, or open an Unreal Engine project with AI, install the Unreal-MCP plugin or its extensions, sign in to ai-game.dev, connect the editor, or wire your coding agent (Claude Code, Codex, Cursor, Gemini CLI) to Unreal's MCP tools. Drives unreal-mcp-cli end to end.
---

# Unreal Engine — AI Game Dev runbook

This skill teaches your AI coding assistant (Claude Code, Codex, Cursor or Gemini CLI) to drive **Unreal
Engine** fully automatically through the `unreal-mcp-cli` npm package. The goal: take the user
from nothing to a running Unreal Editor that is **connected to [ai-game.dev](https://ai-game.dev)**
so the AI can build the game for them.

Every command runs via `npx` so nothing needs to be installed globally:

```bash
npx -y unreal-mcp-cli@latest <command> [args]     # <command> --help shows every flag
```

> **Path syntax differs by command:** `create-project`, `install-plugin`, `close`, `open`, and
> `install-extension` take the project path as a positional argument; `wait-for-ready`, `status`,
> `setup-mcp`, `setup-skills`, and `exec` take it as **`-p <path>`**.

## Prerequisites (check first)

- **Node.js 20.19+ or 22.12+** — `node --version`.
- **Unreal Engine installed** (e.g. UE 5.7 via the Epic Games Launcher). The CLI drives an installed
  engine; it cannot install one unattended (see step 0).
- **A C++ toolchain** (Visual Studio on Windows, Xcode on macOS) — the scaffold is a C++ project and
  `open` compiles its modules before launching.
- **A free ai-game.dev account** — the `login` step signs this machine in.
- **Windows / macOS / Linux** with a real desktop session (the editor opens a window).

> **Naming rule:** an Unreal **project/module name cannot contain hyphens** (`-`). The folder
> path may contain hyphens, but pass a hyphen-free `--name` (e.g. `MyGame`, not `My-Game`).

## The automatic end-to-end sequence

Run these **in order**. The one ordering rule: the editor must **start after a successful
`login`** (step 4).

### 0. Check the installed engines

```bash
npx -y unreal-mcp-cli@latest install-engine          # list installed engines
npx -y unreal-mcp-cli@latest install-engine 5.7      # is 5.7 installed? if not, links to the Epic launcher
```

There is no unattended engine installer: a missing version is installed by the user through the
Epic Games Launcher (a multi-GB download — confirm first).

### 1. Create the project (fresh start only)

Skip this step if the user already has a project — go straight to step 2 pointing at it.

```bash
npx -y unreal-mcp-cli@latest create-project "C:/Games/MyGame" --name MyGame --engine 5.7
```

- Scaffolds a minimal Unreal C++ project at the path (`--force` allows a non-empty folder).
- `--name` sets the project/module name (**no hyphens**; defaults to the folder name).
- `--engine` sets the engine version baked into the `.uproject` (an installed version, e.g. `5.7`).

**Verify:** the path now contains `MyGame.uproject`.

### 2. Install the Unreal-MCP plugin

```bash
npx -y unreal-mcp-cli@latest install-plugin "C:/Games/MyGame"
```

Downloads the UnrealMCP plugin release matching the CLI version into the project. **Verify:** a
`Plugins/UnrealMCP` folder now exists, and `status -p "<path>"` shows `plugin: installed`.

### 3. Sign in (interactive, once per machine)

```bash
npx -y unreal-mcp-cli@latest login
```

- Run it **without `-p`**: it signs in **this machine** and stores the credential in the shared
  machine store `~/.ai-game-dev/credentials.json`, which every engine plugin, CLI, and the
  ai-game.dev desktop app read. (`-p <path>` would write a per-project credential into the
  project's `.env` instead.)
- Unreal's `login` always starts a new sign-in. If `~/.ai-game-dev/credentials.json` already exists
  (this machine signed in through any engine CLI, editor, or the desktop app), skip this step.
- It starts a **device-code OAuth flow** and prints a **verification URL** and a **user code**.
  **Tell the user** to open the URL in a browser and enter the code.
- **Wait for the command to report success** ("Logged in.") before continuing.

### 4. (Re)start the editor in Cloud mode

```bash
npx -y unreal-mcp-cli@latest close "C:/Games/MyGame"   # terminates it; ask the user to save first
npx -y unreal-mcp-cli@latest open  "C:/Games/MyGame" --connection-mode Cloud
```

The plugin reads the machine credential **once, when the editor starts**. An editor that was
already running when you signed in keeps running without it — so `close` it (it reports when none
is running), then `open`. Run `open` **only after a successful `login`.** `open` compiles the
project's native modules when needed (`--no-build` skips it) and auto-dismisses known startup
dialogs; the first launch can take many minutes.

### 5. Confirm the connection

```bash
npx -y unreal-mcp-cli@latest wait-for-ready -p "C:/Games/MyGame" --timeout 600000
npx -y unreal-mcp-cli@latest status         -p "C:/Games/MyGame"
```

`wait-for-ready` polls the project's MCP server (`/api/system-tools/ping`) until it answers
(default timeout 2 minutes; the example allows 10 for a first compile). `status` then shows the
project, plugin, connection URL, whether a token is present, and `reachable: yes`. **Do not tell
the user setup succeeded until `wait-for-ready` passes.**

### 6. Wire your AI assistant to the project's MCP tools

Register the project's MCP server with the assistant you are running as, so it can call the
engine's tools directly (spawn actors, edit the level, run Blueprints, etc.):

```bash
# Pick the id of the agent you are running as (writes the file shown):
#   claude-code -> .mcp.json        codex  -> .codex/config.toml
#   cursor      -> .cursor/mcp.json gemini -> .gemini/settings.json
npx -y unreal-mcp-cli@latest setup-mcp <agent-id> -p "C:/Games/MyGame"
```

The config is pinned to this project and, in Cloud mode, carries a project key (`--oauth` writes a
URL-only config instead; `--dry-run` prints it; `--list` shows every agent id). The assistant loads
it on its next session start in the project folder.

### 7. Generate the project's skills (Claude Code only, optional)

```bash
npx -y unreal-mcp-cli@latest setup-skills -p "C:/Games/MyGame"
```

Writes a Claude Code skill (`.claude/skills/unreal-mcp/SKILL.md`) that drives this project's MCP
server. Other agents have no skills target yet; the MCP tools from step 6 are enough.

## Optional: extensions and `exec`

```bash
npx -y unreal-mcp-cli@latest install-extension com.ivanmurzak.unreal-ai-niagara "C:/Games/MyGame"
npx -y unreal-mcp-cli@latest exec -p "C:/Games/MyGame" "unreal.SystemLibrary.get_engine_version()"
```

- **Extensions** add tool sets (Niagara, EnhancedInput, PCG, GAS, Landscape, ControlRig); the id is
  the extension id, name (e.g. `"Niagara Tools"`), or plugin name. The CLI places the plugin under
  `Plugins/`, enables it in the `.uproject`, and it compiles on the next `open` (or now with
  `--build`). Install only what the game needs.
- **`exec`** runs a **Python** snippet in the editor (the last expression is printed) — handy for a
  quick check or scripted edit. With no editor open it starts a **headless** one and keeps it warm
  (saves and quits after 300 s idle); `close --owned-only "<path>"` stops only an editor the CLI
  started.

## One-shot summary

```bash
# 1. create (fresh only)  2. install  3. login  4. (re)start  5. verify  6. wire MCP
npx -y unreal-mcp-cli@latest create-project "C:/Games/MyGame" --name MyGame --engine 5.7
npx -y unreal-mcp-cli@latest install-plugin "C:/Games/MyGame"
npx -y unreal-mcp-cli@latest login                                   # interactive: URL + code
npx -y unreal-mcp-cli@latest close          "C:/Games/MyGame"
npx -y unreal-mcp-cli@latest open           "C:/Games/MyGame" --connection-mode Cloud
npx -y unreal-mcp-cli@latest wait-for-ready -p "C:/Games/MyGame" --timeout 600000
npx -y unreal-mcp-cli@latest setup-mcp <agent-id> -p "C:/Games/MyGame"   # claude-code | codex | cursor | gemini
```

## Troubleshooting

- **Project name rejected / build fails on module name** — the name contains a hyphen. Use a
  hyphen-free `--name`. The folder path may have hyphens; the module name may not.
- **Engine not found on `open`** — the `.uproject` engine version isn't installed. Check with
  `install-engine`; for a source build pass `--engine-root <dir>` to `open`.
- **Build fails on `open`** — install the C++ toolchain (Visual Studio / Xcode) and retry.
- **`login` never completes** — the user has not finished the browser step. Re-print the
  verification URL and code and wait. Ensure the ai-game.dev account is verified.
- **Different account already signed in** — `login` aborts unchanged; re-run with `--yes` to switch
  this machine to the new account, then `close` + `open`.
- **Editor runs but doesn't connect** — it started before `login`, or the project `.env` overrides
  the connection (`UNREAL_MCP_*` values). `close`, then `open --connection-mode Cloud`.
- **`wait-for-ready` times out** — the editor may still be compiling on first launch. Re-run with a
  longer `--timeout`, and check `status`.
- **`npx` cannot find the CLI** — confirm Node 20.19+ / 22.12+ and internet access.

## Golden rules

1. **`login` before the editor starts**; if it was already open, `close` then `open` it.
2. Never declare success until **`wait-for-ready`** passes.
3. Unreal **module/project names have no hyphens**.
4. `login` is **interactive** and machine-wide — relay the URL + code, and don't pass `-p`.

Learn more at **[ai-game.dev](https://ai-game.dev)**.
