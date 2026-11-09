---
name: roblox-agent-studio
description: "Connect an AI coding agent (Claude Code, Codex, Cursor, Copilot) to a running Roblox Studio through its built-in MCP server and use it safely: Roblox's official plugin first, one manual entry otherwise, never two; prove the connection with list_roblox_studios; run the playtest-and-verify loop (start_stop_play, execute_luau, get_console_output); reach Roblox's Studio skills through the skill tool; work around known bugs (disconnects, the execute_luau sandbox, stale reads before multi_edit). Use whenever the user asks to 'connect Claude to Roblox Studio', 'set up the Roblox MCP', 'let the agent see my place', 'playtest it for me', 'why can't Claude insert scripts', reports the Studio MCP disconnecting or not listing Studio, asks which Roblox MCP server to use, or says 'refresh roblox-agent-studio'. Code on disk is roblox-agent-project; checks without Studio are roblox-agent-checks."
---

# Roblox Studio over MCP

Outcome: the agent is connected to the right Studio window, proven by a `list_roblox_studios` result in the trace, and every change it makes in Studio is checked by a read-back or a playtest log, not by its own say-so.

## Step 0: freshness (every use, one read)

Read `evergreen.json` next to this file. If `contradiction` is set or today is on or after `next_due`, tell the user in one line, do the task with the current content, then refresh (`evergreen-refresh`) in the same session. If `tests.failing` is non-empty, say so in one line and run `evergreen-tune` after the task. Never block the task on a refresh unless the task depends on the stale claim.

## Step 1: is Studio the right tool for this job?

Pick the lowest rung that covers the job and say which one in one line:

1. Files only (roblox-agent-project, roblox-agent-checks): scripts, modules, tests and CI. Most coding work. Studio MCP is not needed while code lives on disk.
2. Studio MCP, read mostly: inspect the DataModel (`search_game_tree`, `inspect_instance`), read console output, take screenshots, run a playtest. This is what experienced users settle on.
3. Studio MCP, edits: instances, properties, UI, terrain and places that are not on disk. Each edit is followed by a read-back.

## Step 2: connect (only after the user says yes)

Studio must be open on Windows or macOS with a place loaded. There is no Linux Studio. The server is inside Studio. It runs over stdio and listens on local port 13469.

1. Open a place first: the setting is not reachable from the start page. In Studio: Assistant, then `...`, then Manage MCP Servers (newer builds: Settings, then MCP Servers), then turn on "Enable Studio as MCP server". In the 2026 layout (menus File, Edit, View, Plugins, Test, Window, Help), Assistant is not under View; it is a button at the top right of the window, next to Collaborate (L-002). The setting belongs to the Roblox account and has switched itself off after Studio updates, so check it again after any update.
2. Prefer Roblox's official plugin, `Roblox/roblox-studio-agent-plugin` (MIT, first published 2026-10-07; Claude Code, Codex, Cowork). It registers the server for both operating systems (the entry for the other OS always shows as failed, which is expected) and adds a `roblox-get-started` skill. Claude Code: run `/plugin`, search for "Roblox Studio" and install it; `/mcp` then lists `plugin:roblox-studio:macos` and `plugin:roblox-studio:windows`. Codex: `codex plugin marketplace add Roblox/roblox-studio-agent-plugin`, then `/plugins`. The user installs it; the agent never does. If `/plugin` does not find it (the repository has no Claude marketplace file of its own), fall back to step 3.
3. Without the plugin, add one entry by hand at local scope:
   - Windows: `claude mcp add --scope local Roblox_Studio -- cmd.exe /c "cd /d %LOCALAPPDATA%\Roblox && .\mcp.bat"` (the batch file must run from its own folder).
   - macOS: `claude mcp add --scope local Roblox_Studio -- /Applications/RobloxStudio.app/Contents/MacOS/StudioMCP` (or the same under `~/Applications`).
   - Other clients: Studio's Quick Connect writes the entry for Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, VS Code and Antigravity.
4. Never register a second Studio server next to the plugin's: the tools appear twice and calls go to whichever loads first. Check `claude mcp list` before adding anything.
5. Verify: call `list_roblox_studios`. Its result (`{"studios":[{"id":...,"name":...}]}`, one entry per open Studio; pass that `id` as `studio_id` to the other tools) is the evidence. A client started before the entry was added does not load its tools until it restarts. A local-scope entry belongs to the exact path it was added from, drive-letter case included: a session opened as `d:` does not see an entry added under `D:` (L-004). An empty list means Studio is closed, no place is open, or the setting is off. A config entry alone proves nothing.

## Step 3: working rules

- Pass `studio_id` on every call. One client can drive several Studios, and since 2026-08 every tool needs the id.
- Read before you edit. `script_read` and `script_grep` have returned stale source on large scripts. Re-read the exact lines right before a `multi_edit`, keep each edit small, and avoid anchors on aligned whitespace (padded `=` signs make `multi_edit` fail repeatedly).
- Since about 2026-10-27 (Studio 0.744 and 0.745) some Windows installs fail to connect: `list_roblox_studios` is empty and the Studio log shows `401 Unauthorized` on `ws://localhost:13469/studio` because the StudioMCP helper now enforces an auth token that Studio does not send (DevForum 4960526, CREATORBUG-30469, staff investigating, no fix yet). Try staff's steps first: close Studio, end every `StudioMCP.exe`, delete old folders under `%LOCALAPPDATA%\Roblox\Versions`, restart Studio and the client. A forum workaround sets the flag `FFlagStudioMCPProxyTokenEnforce` to false; that lets any local program drive Studio, so do not apply it yourself, and if the user chooses it, tell them to remove it once Roblox ships the fix.
- `execute_luau` has twice run in a capability-restricted sandbox, switched on server-side by Roblox and rolled back by staff each time (2026-09-14 to 09-18, and about 2026-10-01 to 10-02). While it is on: no `require` of unsandboxed ModuleScripts, `_G` nil, and creating or reparenting scripts fails with an error like "lacking capability LoadUnownedAsset ... and 3 more". It was off on 0.742.0.7421053 in the Edit, Server and Client data models (T-20261011-2). So try the direct call first. If it fails with a Capabilities error, say it is Studio's sandbox coming back, not a refusal; write the script through `multi_edit` or into a synced file, and tell the user to restart Studio and check the DevForum for a staff rollback. Never suggest overriding Studio feature flags to get around it: that switches off a safety check.
- `execute_luau` returns only the first return value. Return one string built with `string.format` or `table.concat` (L-005).
- Edit-mode tools fail while a playtest runs. Stop the playtest (`start_stop_play`) and confirm with `get_studio_state` before editing.
- There is no batch undo for agent edits. Before a multi-script change, have the user commit or save a copy of the place, or keep the change in synced files where Git can undo it.
- Search tools cap their results (`script_search` top 10, `script_grep` top 50). For a project-wide refactor, work on synced files with ripgrep instead.
- Inserting from the Creator Store (`search_asset`, `insert_asset`) can bring in backdoors. Inspect inserted scripts for `require(<number>)`, `loadstring`, `getfenv` and HTTP loaders before keeping them.
- `http_get` reaches Roblox docs domains only. Roblox's own skills come through the `skill` tool: rbx-debug, rbx-perf-profiling, rbx-scene-analysis, rbx-unit-test, rbx-docs-search, rbx-device-simulator-lua and rbx-create-skill. Use them for those jobs rather than improvising.

## Step 4: the playtest-and-verify loop

1. `get_studio_state`: confirm Edit mode and the right place.
2. `start_stop_play` to start. Then `execute_luau` with `datamodel_type` Server or Client to check state (a value, an instance, an attribute) and return it.
3. `get_console_output` for errors and your own prints. `screen_capture` when the change is visual. `character_navigation` or `user_keyboard_input` to drive the player.
4. `start_stop_play` to stop. Report the returned values and log lines as the evidence.
5. The `subagent` tool (`playtest` type, beta) can run a longer test. It has reported false passes, so check its claims against console output.
6. Gameplay: the break-it pass and the human checklist are in [game-design.md](../roblox-agent-workflow/references/game-design.md) section 7.

## Step 5: when the connection breaks

First check that Studio has a place open (the start page gives 0 tools and an empty `list_roblox_studios`, L-001), then toggle the setting off and on and restart the client. For anything past that, read [references/troubleshooting-and-servers.md](references/troubleshooting-and-servers.md) and work through its list in order.

## Step 6: other servers

The built-in server is the default. A third-party server only for a job it cannot do, and only after the user agrees (the options are in the reference above). Never recommend an unlicensed, newly starred "Roblox MCP" repo with github.io download links (a malware lure), and never an "executor" server.

## Output

The rung chosen, the connection evidence (`list_roblox_studios` output with the `id` used as `studio_id`), and for every edit the read-back or playtest output that shows it worked.

## While working: capture learnings

If the user corrects you, the same error happens twice, a workaround is found, or an environment fact is discovered, write it to `LEARNINGS.md` now (format in MAINTENANCE.md; check existing entries first: add, update, retire, or nothing). If a learning proves a claim above wrong, fix it here, log it in `CHANGELOG.md`, and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `fast`, schedule in `evergreen.json`). Files: `evergreen.json` (state), [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md) (every change, with reasons), [LEARNINGS.md](LEARNINGS.md) (lessons), [TESTS.md](TESTS.md) and `evals/evals.json` (the cases that prove it and the runs). Protocol: MAINTENANCE.md (pointer to the installed evergreen plugin). Refresh with `evergreen-refresh`; test with `evergreen-test`; fix a failure with `evergreen-tune`. Sibling skills in this suite: roblox-agent-checks, roblox-agent-cloud, roblox-agent-project, roblox-agent-studio, roblox-agent-workflow.
