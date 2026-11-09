---
name: godot-game-dev
description: Use when the user wants to create, set up, or open a Godot project with AI, install the Godot-MCP addon or its extensions, sign in to ai-game.dev, connect the editor, or wire your coding agent (Claude Code, Codex, Cursor, Gemini CLI) to Godot's MCP tools. Drives godot-cli end to end.
---

# Godot — AI Game Dev runbook

This skill teaches your AI coding assistant (Claude Code, Codex, Cursor or Gemini CLI) to drive **Godot** fully
automatically through the `godot-cli` npm package. The goal: take the user from nothing to a
running Godot Editor that is **connected to [ai-game.dev](https://ai-game.dev)** so the AI can
build the game for them.

Every command runs via `npx` so nothing needs to be installed globally:

```bash
npx -y godot-cli@latest <command> [args]     # <command> --help shows every flag
```

## Prerequisites (check first)

- **Node.js 20.19+ or 22.12+** — `node --version`.
- **Godot 4.x, .NET build** — the Godot-MCP addon is C#, so use the **.NET (Mono)** editor, not the
  standard build. The CLI finds it via `GODOT_BIN`, `PATH`, or common install folders; otherwise
  pass `--editor-path <exe>` to `open` / `exec`.
- **.NET SDK** — the C# project is built with `dotnet` (`dotnet --version`).
- **A free ai-game.dev account** — the `login` step signs this machine in.
- **Windows / macOS / Linux** with a real desktop session (the editor opens a window).

## The automatic end-to-end sequence

Run these **in order**. The one ordering rule: the editor must **start after a successful
`login`** (step 4).

### 1. Create the project (fresh start only)

Skip this step if the user already has a project — go straight to step 2 pointing at it.

```bash
npx -y godot-cli@latest create-project "C:/Games/MyGame" --dotnet --name MyGame
```

- Scaffolds a minimal Godot 4.x project (`project.godot`, `icon.svg`) at the path; refuses to
  overwrite an existing Godot/Unity/Unreal project.
- `--dotnet` also scaffolds the **C# `.csproj`** — required for the addon.
- `--name` sets the project name (defaults to the folder name).

**Verify:** the path now contains `project.godot` and a `.csproj`. An existing GDScript-only
project needs a C# project (`.csproj`) before step 2.

### 2. Install the Godot-MCP addon

```bash
npx -y godot-cli@latest install-plugin "C:/Games/MyGame"
```

Downloads the `godot_mcp` addon matching the CLI version into `addons/godot_mcp/`, adds its NuGet
references to the `.csproj`, and enables it in `project.godot`. **Verify:** `addons/godot_mcp/`
exists and `project.godot` lists the plugin under `[editor_plugins]`. Optional:
`npx -y godot-cli@latest build "C:/Games/MyGame"` compiles the C# assembly now (`open` does it
anyway).

### 3. Sign in (interactive, once per machine)

```bash
npx -y godot-cli@latest login
```

- Run it **without a project path**: it signs in **this machine** and stores the credential in
  the shared machine store `~/.ai-game-dev/credentials.json`, which every engine plugin, CLI, and
  the ai-game.dev desktop app read. (A path or `--project` would create a per-project credential
  instead.) If the machine is already signed in it says so and exits — continue.
- Otherwise it starts a **device-code OAuth flow** and prints a **verification URL** and a
  **user code**. **Tell the user** to open the URL in a browser and enter the code.
- **Wait for the command to report success** before continuing.

### 4. (Re)start the editor in Cloud mode

```bash
npx -y godot-cli@latest close "C:/Games/MyGame"   # no-op when it isn't running; --force if it hangs
npx -y godot-cli@latest open  "C:/Games/MyGame" --mode Cloud
```

The addon reads the machine credential **once, when the editor starts**. An editor that was
already running when you signed in keeps running without it — so `close` it, then `open`. Run
`open` **only after a successful `login`.** `open` first builds the C# assembly (`--no-build`
skips it), then launches the editor. `--mode Cloud` selects the ai-game.dev connection and passes
the signed-in credential to the editor; do not use `--url` for the cloud (it sets a custom host).

### 5. Confirm the connection

```bash
npx -y godot-cli@latest wait-for-ready "C:/Games/MyGame"
npx -y godot-cli@latest status         "C:/Games/MyGame"
```

`wait-for-ready` polls the project's MCP server (`/api/system-tools/ping`) until it answers;
default timeout 2 minutes (`--timeout <ms>`). `status` then reports whether a Godot editor is
running for this project and whether the MCP server is reachable. **Do not tell the user setup
succeeded until `wait-for-ready` passes and `status` shows the editor running.**

### 6. Wire your AI assistant to the project's MCP tools

Register the project's MCP server with the assistant you are running as, so it can call the
engine's tools directly (create nodes, edit scenes, wire signals, etc.):

```bash
# Pick the id of the agent you are running as (writes the file shown):
#   claude-code -> .mcp.json        codex  -> .codex/config.toml
#   cursor      -> .cursor/mcp.json gemini -> .gemini/settings.json
npx -y godot-cli@latest setup-mcp <agent-id> "C:/Games/MyGame"
```

The config is pinned to this project and, in Cloud mode, carries a project key (`--oauth` writes a
URL-only config instead; `--list` shows every agent id). The assistant loads it on its next session
start in the project folder.

### 7. Generate the project's skills (recommended)

```bash
npx -y godot-cli@latest setup-skills <agent-id> "C:/Games/MyGame"
```

The Godot plugin generates skills for the tools this project actually has (engine version,
installed extensions) and writes them where your agent reads skills: `.claude/skills`,
`.agents/skills`, `.cursor/skills` or `.gemini/skills` (no editor needed). This runbook only gets the
project connected; those generated skills teach you the engine's tools in depth.

## Optional: extensions and `exec`

```bash
npx -y godot-cli@latest install-extension "Tilemap Tools" "C:/Games/MyGame"
npx -y godot-cli@latest exec --path "C:/Games/MyGame" "Godot.Engine.GetVersionInfo()"
```

- **Extensions** add tool sets (Particles, Tilemap, Navigation, Animation, CSG, GridMap, …); the id
  is the extension name or its package id (e.g. `com.IvanMurzak.Godot.MCP.Tilemap`). The CLI adds
  the `<PackageReference>` to the `.csproj` and rebuilds. Install only what the game needs.
- **`exec`** runs a C# snippet in the editor (the last expression is printed) — handy for a quick
  check or scripted edit. With no editor open it starts a **headless** one and keeps it warm
  (quits after 300 s idle); `close --owned-only "<path>"` stops only an editor the CLI started.

## One-shot summary

```bash
# 1. create (fresh only)  2. install  3. login  4. (re)start  5. verify  6. wire MCP  7. skills
npx -y godot-cli@latest create-project "C:/Games/MyGame" --dotnet --name MyGame
npx -y godot-cli@latest install-plugin "C:/Games/MyGame"
npx -y godot-cli@latest login                                  # interactive: URL + code
npx -y godot-cli@latest close          "C:/Games/MyGame"
npx -y godot-cli@latest open           "C:/Games/MyGame" --mode Cloud
npx -y godot-cli@latest wait-for-ready "C:/Games/MyGame"
npx -y godot-cli@latest status         "C:/Games/MyGame"
npx -y godot-cli@latest setup-mcp <agent-id> "C:/Games/MyGame"   # claude-code | codex | cursor | gemini
npx -y godot-cli@latest setup-skills <agent-id> "C:/Games/MyGame"
```

## Troubleshooting

- **`install-plugin` warns there is no `.csproj`** — the project is GDScript-only. Create it with
  `create-project --dotnet` (new project) or add a Godot.NET.Sdk C# project, then re-run.
- **Build errors / addon won't load** — you're on the standard (non-.NET) Godot build or missing
  the .NET SDK. Use the **.NET** editor and install the .NET SDK, then `build` and `open` again.
- **Editor not found** — set `GODOT_BIN` or pass `--editor-path <exe>` to `open`.
- **`login` never completes** — the user has not finished the browser step. Re-print the
  verification URL and code and wait. Ensure the ai-game.dev account is verified.
- **Wrong account / need to sign in again** — `login --force` (add `--yes` to confirm switching
  accounts), then `close` + `open --mode Cloud`.
- **Editor connects locally / not to Cloud** — it started before `login`, or was opened with `--url`.
  `close`, then `open --mode Cloud`.
- **`wait-for-ready` times out** — Godot may still be restoring NuGet packages / building C# on
  first launch. Re-run with a longer `--timeout`, and check `status`.

## Golden rules

1. **`login` before the editor starts**; if it was already open, `close` then `open` it.
2. Never declare success until **`wait-for-ready`** passes.
3. Use the **.NET** Godot build and a **C# project**; the build needs the **.NET SDK**.
4. Select the cloud connection with **`--mode Cloud`** — not `--url`.

Learn more at **[ai-game.dev](https://ai-game.dev)**.
