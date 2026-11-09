---
name: unity-game-dev
description: Use when the user wants to create, set up, or open a Unity project with AI, install the Unity-MCP plugin or its extensions, sign in to ai-game.dev, connect the editor, or wire your coding agent (Claude Code, Codex, Cursor, Gemini CLI) to Unity's MCP tools. Drives unity-mcp-cli end to end.
---

# Unity — AI Game Dev runbook

This skill teaches your AI coding assistant (Claude Code, Codex, Cursor or Gemini CLI) to drive **Unity** fully
automatically through the `unity-mcp-cli` npm package. The goal: take the user from nothing to a
running Unity Editor that is **connected to [ai-game.dev](https://ai-game.dev)** so the AI can
build the game for them.

Every command runs via `npx` so nothing needs to be installed globally:

```bash
npx -y unity-mcp-cli@latest <command> [args]     # <command> --help shows every flag
```

## Prerequisites (check first)

- **Node.js 20.19+ or 22.12+** — `node --version`.
- **Unity Hub + a Unity Editor** (e.g. Unity 6). `create-project` and `install-unity` locate Unity
  Hub and install it if it is missing. No editor yet? See step 0.
- **A free ai-game.dev account** — the `login` step signs this machine in.
- **Windows / macOS / Linux** with a real desktop session (the editor opens a window).

## The automatic end-to-end sequence

Run these **in order**. The one ordering rule: the editor must **start after a successful
`login`** (step 4).

### 0. Install a Unity Editor (only if none is installed)

```bash
npx -y unity-mcp-cli@latest install-unity                # latest stable release
npx -y unity-mcp-cli@latest install-unity 6000.3.1f1     # or an exact version
```

Installs the editor through Unity Hub. This is a large download — confirm with the user first.

### 1. Create the project (fresh start only)

Skip this step if the user already has a project — go straight to step 2 pointing at it.

```bash
npx -y unity-mcp-cli@latest create-project "C:/Games/MyGame"
npx -y unity-mcp-cli@latest create-project "C:/Games/MyGame" --unity 6000.3.1f1   # pin a version
```

- Scaffolds a new Unity project at the path with an editor installed in Unity Hub.
- Without `--unity` it uses the **highest installed** editor version.

**Verify:** the path now contains `Assets/`, `Packages/`, and `ProjectSettings/`.

### 2. Install the Unity-MCP plugin

```bash
npx -y unity-mcp-cli@latest install-plugin "C:/Games/MyGame"
```

Adds the Unity-MCP package to `Packages/manifest.json` (latest version unless
`--plugin-version` is given). **Verify:** `Packages/manifest.json` references
`com.ivanmurzak.unity.mcp`.

### 3. Sign in (interactive, once per machine)

```bash
npx -y unity-mcp-cli@latest login
```

- `login` takes **no project path**: it signs in **this machine** and stores the credential in the
  shared machine store `~/.ai-game-dev/credentials.json`, which every engine plugin, CLI, and the
  ai-game.dev desktop app read. If the machine is already signed in it prints
  *Already signed in* and exits — continue.
- Otherwise it starts a **device-code OAuth flow** and prints a **verification URL** and a
  **user code**. **Tell the user** to open the URL in a browser and enter the code.
- **Wait for the command to report success** before continuing.

### 4. (Re)start the editor (auto-connects)

```bash
npx -y unity-mcp-cli@latest close "C:/Games/MyGame"   # no-op when it isn't running; --force if it hangs
npx -y unity-mcp-cli@latest open  "C:/Games/MyGame"
```

The plugin reads the machine credential **once, when the editor starts**. An editor that was
already running when you signed in keeps running without it — so `close` it, then `open`. Run
`open` **only after a successful `login`.** New projects default to **Cloud** mode, so the plugin
connects to ai-game.dev on startup with no extra flag. Unity's first launch imports packages and
compiles; it can take minutes.

### 5. Confirm the connection

```bash
npx -y unity-mcp-cli@latest wait-for-ready "C:/Games/MyGame"
npx -y unity-mcp-cli@latest status         "C:/Games/MyGame"
```

`wait-for-ready` polls the project's MCP server (`/api/system-tools/ping`) until it answers;
default timeout 2 minutes (`--timeout <ms>`, e.g. `--timeout 600000` on a first launch). `status`
then reports whether Unity is running for this project and whether the MCP server is reachable.
**Do not tell the user setup succeeded until `wait-for-ready` passes and `status` shows Unity
running.**

### 6. Wire your AI assistant to the project's MCP tools

Register the project's MCP server with the assistant you are running as, so it can call the
engine's tools directly (create GameObjects, edit scenes, attach components, etc.):

```bash
# Pick the id of the agent you are running as (writes the file shown):
#   claude-code -> .mcp.json        codex  -> .codex/config.toml
#   cursor      -> .cursor/mcp.json gemini -> .gemini/settings.json
npx -y unity-mcp-cli@latest setup-mcp <agent-id> "C:/Games/MyGame"
```

The config is pinned to this project and, in Cloud mode, carries a project key (`--oauth` writes a
URL-only config instead; `--list` shows every agent id). The assistant loads it on its next session
start in the project folder.

### 7. Generate the project's skills (recommended)

```bash
npx -y unity-mcp-cli@latest setup-skills <agent-id> "C:/Games/MyGame"
```

The Unity plugin generates skills for the tools this project actually has (engine version,
installed extensions) and writes them where your agent reads skills: `.claude/skills`,
`.agents/skills`, `.cursor/skills` or `.gemini/skills` (needs the running editor). This runbook only gets the
project connected; those generated skills teach you the engine's tools in depth.

## Optional: extensions and `exec`

```bash
npx -y unity-mcp-cli@latest install-extension --list                   # what can be installed
npx -y unity-mcp-cli@latest install-extension Tilemap "C:/Games/MyGame" # adds the package + OpenUPM registry
npx -y unity-mcp-cli@latest exec --path "C:/Games/MyGame" "UnityEngine.Application.unityVersion"
```

- **Extensions** add tool sets (Animation, Cinemachine, InputSystem, ProBuilder, Tilemap, …).
  Install only what the game needs; Unity resolves the package on its next refresh.
- **`exec`** runs a C# snippet in the editor (the last expression is printed) — handy for a quick
  check or scripted edit. With no editor open it starts a **headless** one and keeps it warm
  (quits after 300 s idle); `close --owned-only "<path>"` stops only an editor the CLI started.

## One-shot summary

```bash
# 1. create (fresh only)  2. install  3. login  4. (re)start  5. verify  6. wire MCP  7. skills
npx -y unity-mcp-cli@latest create-project "C:/Games/MyGame"
npx -y unity-mcp-cli@latest install-plugin "C:/Games/MyGame"
npx -y unity-mcp-cli@latest login                                  # interactive: URL + code
npx -y unity-mcp-cli@latest close          "C:/Games/MyGame"
npx -y unity-mcp-cli@latest open           "C:/Games/MyGame"
npx -y unity-mcp-cli@latest wait-for-ready "C:/Games/MyGame"
npx -y unity-mcp-cli@latest status         "C:/Games/MyGame"
npx -y unity-mcp-cli@latest setup-mcp <agent-id> "C:/Games/MyGame"   # claude-code | codex | cursor | gemini
npx -y unity-mcp-cli@latest setup-skills <agent-id> "C:/Games/MyGame"
```

## Troubleshooting

- **`create-project` fails: no editors / version not found** — install one with
  `install-unity [version]`, or pass a `--unity` version that is installed in the Hub.
- **`login` never completes** — the user has not finished the browser step. Re-print the
  verification URL and code and wait. Ensure the ai-game.dev account is verified.
- **Wrong account / need to sign in again** — `login --force` (add `--yes` to confirm switching
  accounts), then `close` + `open` the editor.
- **Editor runs but doesn't connect** — it started before `login`. `close`, then `open` again.
- **`wait-for-ready` times out** — Unity may still be importing or compiling on first launch.
  Re-run with a longer `--timeout`, and check `status`.

## Golden rules

1. **`login` before the editor starts**; if it was already open, `close` then `open` it.
2. Never declare success until **`wait-for-ready`** passes.
3. `login` is **interactive** — relay the verification URL + code to the user and wait.
4. `login` is machine-wide — never pass it a project path (`--project` is a per-project override).

Learn more at **[ai-game.dev](https://ai-game.dev)**.
