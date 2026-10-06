---
name: roblox-studio-mcp
description: Drive Roblox Studio from an AI agent via the built-in Studio MCP server - connecting Claude Code, Codex, Cursor, OpenCode, Gemini CLI; tools to explore the DataModel, read/edit scripts, run Luau in edit/server/client, playtest, read output, capture screenshots, simulate input, insert assets. Use when an agent should inspect, modify, or playtest an open Studio place, or to set up the connection.
---

# Working in Roblox Studio through MCP

Roblox Studio ships a **built-in MCP server** (stdio). With it, an agent can explore the open place,
edit scripts, run Luau in edit/server/client contexts, playtest, read the Output, capture the viewport,
and simulate player input. It is the fastest way to **verify** Roblox changes instead of guessing.

## Setup

1. Latest Studio → open **Assistant** → **…** → **Manage MCP Servers** → enable **Enable Studio as MCP server**.
2. Use **Quick connect** (Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, VS Code, Antigravity)
   or configure the client manually:

| OS | Command |
| --- | --- |
| macOS | `/Applications/RobloxStudio.app/Contents/MacOS/StudioMCP` |
| Windows | `cmd.exe /c %LOCALAPPDATA%\Roblox\mcp.bat` |

```bash
# Claude Code
claude mcp add Roblox_Studio -- /Applications/RobloxStudio.app/Contents/MacOS/StudioMCP
claude mcp add Roblox_Studio -- cmd.exe /c "%LOCALAPPDATA%\Roblox\mcp.bat"   # Windows
```

```json
{ "mcpServers": { "Roblox_Studio": { "command": "/Applications/RobloxStudio.app/Contents/MacOS/StudioMCP" } } }
```

Client-specific config (Codex `config.toml`, OpenCode `opencode.json`, Cursor/VS Code `mcp.json`):
[references/client-setup.md](references/client-setup.md). A green indicator in **Manage MCP Servers**
confirms the connection. Only connect clients you trust: they can read and modify your places.

## Tools

| Group | Tools |
| --- | --- |
| Session | `list_roblox_studios` (every call takes a `studio_id`), `get_studio_state` (play state, available DataModels) |
| Explore | `search_game_tree` (filter by path/class/keyword, depth), `inspect_instance` (properties, attributes, children), `script_search` (fuzzy by name), `script_grep` (text across scripts, ≤ 50 hits), `script_read` (dot path like `game.ServerScriptService.Main`, line ranges) |
| Edit | `multi_edit` (several edits to one script, creates it if missing; `datamodel_type = Edit`) |
| Run | `execute_luau` (`datamodel_type` = `Edit`, `Server`, or `Client`; returns the result or error) |
| Playtest | `start_stop_play`, `get_console_output`, `screen_capture` (optional camera position/look-at), `character_navigation`, `user_keyboard_input`, `user_mouse_input` |
| Assets | `search_asset` (Creator Store / inventory), `insert_asset`, `upload_image`, `store_image`, `generate_mesh`, `generate_material`, `generate_procedural_model` + `wait_job_finished` |
| Delegation | `subagent` (`explore` or `playtest` types for multi-step investigations) |
| Knowledge | `http_get` (Roblox docs, API reference, Cloud docs), `skill` (Roblox-authored skills: debugging, device simulation, docs search, profiling, scene analysis, unit tests) |

## The working loop

1. **Orient**: `list_roblox_studios` → pick `studio_id`; `get_studio_state`. Map the project with
   `search_game_tree` (depth-limited: services first), then `script_grep`/`script_search` for the feature.
2. **Read before writing**: `script_read` every script you'll touch and its requirers. Check for a
   Rojo/Script Sync setup (see below) before editing in Studio.
3. **Edit** with `multi_edit` (exact, minimal edits; keep existing style). Create instances/attributes/
   tags with `execute_luau` in `Edit` context — changes made this way are **real edits to the place**.
4. **Verify statically**: re-read the script; for pure modules, `execute_luau` a quick check
   (`require` the module in `Edit` and call functions).
5. **Playtest**: `start_stop_play` (start) → wait → `get_console_output` for errors → drive the scenario
   with `character_navigation` / input tools → `execute_luau` in `Server`/`Client` to assert state →
   `screen_capture` for visual checks → `start_stop_play` (stop). Always stop play when done.
6. **Report** what changed and what was verified (and what wasn't).

```luau
-- Example execute_luau (Server context during play): assert game state instead of eyeballing.
local Players = game:GetService("Players")
local results = {}
for _, player in Players:GetPlayers() do
	local leaderstats = player:FindFirstChild("leaderstats")
	local coins = leaderstats and leaderstats:FindFirstChild("Coins")
	table.insert(results, `{player.Name}: {if coins and coins:IsA("IntValue") then coins.Value else "missing"}`)
end
return table.concat(results, "\n")
```

## Rules of thumb

- `execute_luau` in `Edit` mutates the place: prefer read-only queries while exploring, and batch
  intentional changes into one clear script. Use `ChangeHistoryService` recording (`TryBeginRecording`/
  `FinishRecording`) so the user can undo your edit as one step.
- Changes made during play (Server/Client contexts) are discarded when play stops — edit in `Edit`.
- **Rojo projects**: the file system is the source of truth — edit files on disk, let Rojo sync, and use
  MCP to playtest/inspect. Editing synced scripts via `multi_edit` gets overwritten. **Script Sync**
  projects sync both ways, so either side works, but don't edit the same script in both at once.
- Keep `search_game_tree` queries narrow (path + depth); large places produce huge outputs.
- Multiple Studio windows: always pass the right `studio_id`; tell the user which place you touched.
- Inserted assets from the Creator Store can contain scripts: inspect them (`search_game_tree` +
  `script_read`) before keeping them; remove unexpected scripts (backdoors are common in free models).
- Don't claim success without evidence: cite console output, assertion results, or screenshots.

## Roblox-authored skills and conversions

Studio exposes Roblox-authored skills through the `skill` tool (e.g. `rbx-debug`, `rbx-perf-profiling`,
`rbx-scene-analysis`, `rbx-unit-test`, `rbx-docs-search`, `rbx-device-simulator-lua`). Roblox also
publishes an official **streaming conversion** skill (`/rbx-convert-to-streaming`, downloadable from the
"Techniques and conversion" streaming docs) that runs through this MCP server; back up the place first.

## Related skills

`roblox-testing` (test runners), `roblox-performance` (profiling), `roblox-tooling` (Rojo/Script Sync),
`roblox-architecture` (where things belong), `roblox-code-review`.
