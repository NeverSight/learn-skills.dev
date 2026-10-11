---
name: roblox-dev-skill
description: >
  Core scripting and engine skill for Roblox game development.
  Covers full-lifecycle development: architecture, Luau scripting, debugging, security,
  performance, data persistence, networking, and the Roblox Studio environment.
  MUST use this skill whenever the user mentions: 'Roblox', 'Luau', 'Roblox Studio',
  'ServerScriptService', 'ReplicatedStorage', 'DataStoreService', 'RemoteEvent',
  or when working with Roblox Studio MCP tools like execute_luau, search_game_tree.
  Note: For UI/UX design, refer to roblox-design-skill and roblox-design-intelligence.
  For Audio, VFX, or Monetization, refer to their respective skills in the suite.
---

# Roblox Game Development Skill

Expert development companion for building Roblox experiences with Luau. Grounded in
official Roblox documentation (https://create.roblox.com/docs), the Luau language spec
(https://luau.org), and the Roblox Lua Style Guide (https://roblox.github.io/lua-style-guide/).

> **Engine**: Roblox Studio **0.741.19.7411056** with **Luau 0.740** (released 2026-09-25) —
> dump downloaded, re-split, and diffed against 0.740 on **2026-10-01**. 931 classes / 641 enums /
> 260 services / 48 deprecated.
>
> Roblox ships roughly weekly, so this line is stale by design — never quote it as today's version.
> Re-derive it instead:
>
> ```bash
> curl -s "https://clientsettings.roblox.com/v2/client-version/MacStudio"   # or WindowsStudio64
> curl -s "https://api.github.com/repos/luau-lang/luau/releases?per_page=1" | grep tag_name
> ```
>
> The `WindowsStudio` (no `64`) endpoint returns a long-stale value — measured 2026-09-06 it still
> answered `0.578.0.5780566`. Use `WindowsStudio64` or `MacStudio`.
>
> When in doubt about an API, look it up (see **API & Documentation Lookup** below) rather than
> recalling it. If it is still unclear, ask the user before proceeding.

---

## MCP Detection

On every invocation, detect available Roblox Studio MCP tools before proceeding:

### Official Roblox MCP (Roblox_Studio server)

**This skill is a knowledge base, not an MCP server.** It ships no tools and no execution
surface. The tools below belong to **Roblox's own MCP server, built into Studio** — this skill
only tells you how to use them well. Official reference:
https://create.roblox.com/docs/studio/mcp

The docs page lists **26 tools**; the build observed 2026-09-25 exposed **28** (plus
`generate_texture` and `segment_mesh`, undocumented). Detect what your host actually exposes
rather than trusting this table.

| Tool | Purpose |
|------|---------|
| `execute_luau` | Run Luau in Studio at plugin privilege — **returns the result or the error** |
| `multi_edit` | Apply several exact-match edits to **ONE** script (creates it if missing); `Edit` datamodel only |
| `script_read` | Read script source, whole or by line range; output is `LINE→CONTENT` |
| `script_search` / `script_grep` | Find scripts by name (fuzzy, ≤10) or by content (≤50 matches) |
| `search_game_tree` | Explore the DataModel as flat JSON, filterable by path/type/keyword |
| `inspect_instance` | Properties, attributes, and child summary for one instance |
| `subagent` | Launch a Roblox-side subagent for autonomous multi-step work (types vary by build) |
| `get_studio_state` | Play state **and which datamodel types are available** |
| `start_stop_play` | Start/stop playtesting |
| `get_console_output` | Read Output/console logs |
| `screen_capture` | Capture the viewport, optionally from a custom camera |
| `character_navigation` | Move the character to a position or instance path |
| `user_mouse_input` / `user_keyboard_input` | Simulate ordered mouse/keyboard actions |
| `search_asset` / `insert_asset` | Search Creator Store + Inventory; insert by asset ID |
| `store_image` | **Local** png/jpg ≤5 MB → `IMAGEID_` URI for other tools |
| `upload_image` | Batch upload from **HTTP(S) URLs** → imagePath→assetId map |
| `generate_mesh` / `generate_procedural_model` | Generate 3D content |
| `generate_material` / `generate_texture` | Generate materials and textures |
| `segment_mesh` | Segment a mesh into parts |
| `wait_job_finished` | Await a background `jobId` (from a tool's own `async: true`) |
| `http_get` | Fetch Roblox docs **from an allowlist**; URL must end `.md` or be `llms.txt` |
| `skill` | Roblox's first-party `rbx-*` references (debug, perf, scene analysis, …) |
| `list_roblox_studios` | Enumerate connected Studio instances (name + place ID) |

> **Every call takes a `studio_id`.** There is no "set active studio" tool — call
> `list_roblox_studios` first and pass the id you want on each subsequent call. Several Studio
> instances are commonly open at once, so picking the wrong id silently targets the wrong place.
>
> **`datamodel_type` is asymmetric.** `execute_luau` accepts `Edit` / `Client` / `Server`;
> **`multi_edit` accepts `Edit` only**, so you cannot edit scripts mid-playtest — stop the
> playtest first. `Client` and `Server` exist only during a playtest; check `get_studio_state`.
>
> **`multi_edit` is one script per call**, taking `file_path` plus
> `edits[{old_string, new_string, replace_all}]`. Replacements are sequential, exact-match, and
> atomic within the call. `script_read` first or the call simply fails.
>
> **`script_grep`'s line numbers are unreliable** — measured 2026-09-06, it reported a match at
> line 171 that `script_read` showed was 15 lines further down. Use it to find *which* script
> contains a string, then `script_read` for the real location.
>
> **There is no `run_as_job` tool.** Earlier versions of this file listed one; it does not exist
> in the docs or in any observed build. Async is a per-tool argument returning a `jobId`.

If MCP tools are available, prefer using them for:
- Reading existing scripts before writing new ones (`script_read`, `script_search`)
- Validating changes by running code (`execute_luau`)
- Inspecting game tree to understand project structure (`search_game_tree`)
- Testing changes with playtest (`start_stop_play`, `get_console_output`)
- Roblox's own domain skills (`skill`) for debugging, MicroProfiler, and scene analysis —
  they are first-party and versioned with Studio

**Before the first mutation of any session**, read `references/agent-safety.md`. Roblox's own
warning: *"MCP clients can read and modify content in your open Roblox places."* There is no
dry-run and no reliable undo. Confirm which place you are targeting before you write to it.

If MCP tools are NOT available, provide copy-paste-ready Luau scripts with clear
placement instructions (which service container to put them in).

---

## Routing Table

Match user intent to the appropriate reference file. Read the file BEFORE generating code.

| User Intent | Reference File |
|---|---|
| **How do I actually sequence this?** End-to-end worked patterns: build a server-authoritative feature, debug via MCP, migrate a deprecation, verify an API, refuse an unsafe request | `references/worked-examples.md` |
| Luau syntax, types, naming conventions, style | `references/luau-fundamentals.md` |
| Project layout, architecture, patterns | `references/project-structure.md` |
| Save/load player data, DataStore, ProfileStore | `references/datastore-persistence.md` |
| Client-server communication, RemoteEvents, input | `references/networking.md` |
| Security, anti-exploit, server authority, bans | `references/security-hardening.md` |
| Agent→Studio safety, destructive MCP ops, prompt injection from place content | `references/agent-safety.md` |
| Performance, memory, optimization, Parallel Luau | `references/performance-optimization.md` |
| Using Roblox Studio MCP tools effectively | `references/mcp-integration.md` |
| UI, GUI, ScreenGui, menus, HUD, StyleQuery | `references/ui-systems.md` |
| Migrating legacy code, deprecated APIs | `references/legacy-migration.md` |
| Monetization, game passes, donations, transfers | `references/monetization.md` |
| File formats, import/export, asset management | `references/file-formats-and-assets.md` |
| Plugins, `Script.Source` limits, HttpService/engine limits | `references/studio-plugins-and-limits.md` |

**Start with `worked-examples.md` when the task is a *doing* task** (build, debug, migrate, look up)
rather than a *knowing* task. It gives the call sequence and the verification step, and each example
carries a **Not this** list so a near-miss request routes to the right place instead of the nearest
familiar pattern. Where an example and a reference file disagree, the reference file wins.

If the intent spans multiple domains, read all relevant files.
If a reference file doesn't cover a topic sufficiently, use the Official
Documentation Lookup workflow below.

---

## API & Documentation Lookup

### Priority 1: Local API Reference (`~/RobloxDocs/`)

**Always check local files first** — they are pre-split, far cheaper to read than the full dump, and
require no network. If `~/RobloxDocs/RobloxAPI/` exists, use it.

**How much cheaper, re-measured 2026-10-01 on 0.741.19.7411056** (an earlier "845× smaller" figure
was not reproducible from any measurement, so here are the real numbers and the command that
produced them): the full dump is **8,356,896 bytes**; the 931 split class files run **101 B min,
2,054 B median, 4,782 B mean, 104,956 B max**. So a typical class lookup reads about **0.02%** of
the dump, and even the largest class reads under **1.3%** of it. Re-measure with:

```bash
# Portable (macOS, Linux, Windows). Do not use `stat -f %z`: on Linux `stat -f` reports the
# *filesystem*, not the file, and prints a wrong number without any error. It also reads the
# 75-byte latest.json symlink instead of the dump unless you remember -L.
python3 -c "import os,glob,statistics as s; d=os.path.expanduser('~/RobloxDocs/RobloxAPI'); \
z=sorted(os.path.getsize(f) for f in glob.glob(d+'/classes/*.json')); \
print('dump', os.path.getsize(os.path.realpath(d+'/dumps/latest.json')), 'B | n', len(z), \
'min', z[0], 'median', int(s.median(z)), 'mean', int(s.mean(z)), 'max', z[-1])"
```

```bash
# Look up a specific class (~2 KB median vs the 8.4 MB full dump — see measurement above)
cat ~/RobloxDocs/RobloxAPI/classes/<ClassName>.json

# Query a specific property/method (jq if installed; the python3 form works everywhere)
jq '.Members[] | select(.Name == "<MemberName>")' ~/RobloxDocs/RobloxAPI/classes/<ClassName>.json
python3 -c "import json,os; print([m for m in json.load(open(os.path.expanduser('~/RobloxDocs/RobloxAPI/classes/<ClassName>.json')))['Members'] if m['Name']=='<MemberName>'])"

# Find all services
cat ~/RobloxDocs/RobloxAPI/service-index.json

# Check what's deprecated
cat ~/RobloxDocs/RobloxAPI/deprecated-index.json

# Search across classes by filename
ls ~/RobloxDocs/RobloxAPI/classes/ | grep -i <keyword>

# Search for a property across all classes
grep -l '"<PropertyName>"' ~/RobloxDocs/RobloxAPI/classes/*.json
```

**Obsolescence check:** Before using local data, verify freshness:
```bash
# Check when local data was last updated
cat ~/RobloxDocs/RobloxAPI/.current-version
# → {"version":"0.741.19.7411056","platform":"MacStudio","platformVersion":"0.741.19.7411056",
#    "winHash":"version-76e1a02649ad4f35","updatedAt":"2026-10-01T03:41:12Z","checkedAt":"2026-10-01T03:41:12Z"}
```

> **Read whichever timestamp is present: `updatedAt` OR `checkedAt`.** `updatedAt` is when a dump
> was last downloaded; `checkedAt` is when the version was last checked. The current monitor
> (skill 2.12.0+) always writes both, but the older zsh script wrote **only `updatedAt`** after a
> download — so an install that has not refreshed its tools may lack `checkedAt` entirely. Earlier
> versions of this file told the agent to read `checkedAt`, which silently found nothing there.

If that timestamp is older than 7 days, or a class/member is not found locally, **proceed with the
live web fallback below and tell the user the local dump looks stale.** Offer to refresh it:

```bash
# Only after the user agrees — this downloads and re-splits the API dump
~/RobloxDocs/scripts/roblox-api-monitor.sh                      # macOS, Linux, WSL, Git Bash
python "%USERPROFILE%\RobloxDocs\scripts\roblox-api-monitor.py"    # Windows without bash
```

If `~/RobloxDocs` does not exist at all, the user never set it up. Say so and point them at the
installer's `--docs-only` option (`-DocsOnly` in PowerShell) rather than creating it yourself.

> **Do not background this and do not run it unasked.** Earlier versions of this file told the
> agent to fire `roblox-api-monitor.sh &` automatically, which contradicted both the
> Knowledge Freshness Check below ("NEVER auto-update without user approval") and the README.
> There is no scheduler and no background job in this skill; a human triggers the refresh.
> Staleness never blocks the answer — fall through to the web sources and say so.

### Priority 2: Live Web Sources (Fallback)

Use these when local data doesn't cover a topic, is obsolete, or you need prose docs:

| Resource | URL | Use For |
|----------|-----|--------|
| **LLM docs index** | `https://create.roblox.com/docs/llms.txt` | Browse all available doc pages by topic |
| **Full docs (single file)** | `https://create.roblox.com/docs/llms-full.txt` | Comprehensive single-file reference |
| **Per-page markdown** | `https://create.roblox.com/docs/en-us/{path}.md` | Read specific doc pages in clean markdown |
| **Engine API index** | `https://create.roblox.com/docs/reference/engine/llms.txt` | Luau API classes, methods, events |
| **Open Cloud API index** | `https://create.roblox.com/docs/cloud/llms.txt` | **Primary discovery** for all Cloud REST API: features, domains, guides, auth |
| **OpenAPI spec (raw)** | `https://create.roblox.com/docs/cloud/openapi.json` | Machine-readable OpenAPI spec for MCP/code-gen tools |
| **Deprecated API check** | `https://robloxapi.github.io/ref/class/<Name>.html` | Check individual class/member status (deprecated items marked visually) |

> **If you are fetching these through Studio's `http_get` tool, note its allowlist:** only
> `create.roblox.com/docs` (incl. `/reference/engine`, `/cloud`, `/performance-optimization`) and
> `github.com/Roblox/libmp`, and **the URL must end in `.md` or be `llms.txt`**. So
> `llms-full.txt`, `openapi.json`, and `robloxapi.github.io` are **rejected** by `http_get` — use
> the host's own fetch tool or `curl` for those. `http_get`'s `query` argument returns only
> matching sections, which is much cheaper than pulling a whole page into context.

### Lookup Workflow
1. Check if a **reference file** covers the topic (Routing Table above)
2. Check **`~/RobloxDocs/RobloxAPI/classes/<Name>.json`** for Engine API details
3. If not found locally, fetch the per-page markdown URL with whatever web-fetch tool the host
   provides (`WebFetch` in Claude Code, `curl` in a shell — the URL is the portable part)
   - Example: `https://create.roblox.com/docs/en-us/studio/importer.md`
4. If unsure which page to read, browse `llms.txt` for the right URL
5. For **Open Cloud / REST API** topics, read `https://create.roblox.com/docs/cloud/llms.txt`
   - Search Features section first, then Domains
   - Prefer Open Cloud endpoints (API key / OAuth) over legacy cookie-auth endpoints
6. **Fallback**: Context7. Its MCP tools are `resolve-library-id` then `get-library-docs` (there is
   no `query-docs` tool — an earlier version of this file named one that does not exist). Where the
   MCP server is not connected, the CLI does the same job:
   `npx ctx7@latest library "Roblox"` then `npx ctx7@latest docs <libraryId> "<question>"`
7. If still unclear, ask the user before proceeding

> **Important**: Engine APIs (Luau via `game:GetService()`) and Open Cloud APIs
> (HTTP REST via `x-api-key`) are **completely separate systems**. Using the
> wrong index will produce non-functional code.

> **Checking deprecated APIs**: Use these approaches (in priority order):
> 1. `cat ~/RobloxDocs/RobloxAPI/deprecated-index.json` — instant local lookup
> 2. `cat ~/RobloxDocs/RobloxAPI/deprecated/<ClassName>.json` — full deprecated class detail
> 3. Check `robloxapi.github.io/ref/class/<Name>.html` — deprecated members marked visually
> 4. Use Context7 (`resolve-library-id` → `get-library-docs`, or the `ctx7` CLI) to query specific APIs

---

## Core Coding Standards

These rules apply to ALL generated Roblox/Luau code. They are non-negotiable.

### 1. Type Safety
- Use `--!strict` at the top of every new script
- Annotate function parameters and return types
- Define custom types with `type` keyword for complex data structures

### 2. Naming Conventions (Official Roblox Style)
- **PascalCase**: Classes, ModuleScripts, Constructors, Services — `CombatService`, `PlayerData`
- **camelCase**: Variables, functions, parameters — `playerHealth`, `calculateDamage()`
- **UPPER_SNAKE_CASE**: Constants — `MAX_HEALTH`, `DEFAULT_SPEED`
- Spell out words fully — avoid abbreviations
- Don't fully capitalize acronyms: `JsonTable` not `JSONTable`

### 3. Modern API Usage
- Use `task.spawn()`, `task.delay()`, `task.wait()` — NOT legacy `spawn()`, `delay()`, `wait()`
- Use `task.cancel()` to clean up deferred tasks
- Always disconnect event connections in cleanup: `connection:Disconnect()`
- Wrap fallible operations in `pcall()` or `xpcall()`

### 4. Architecture Rules
- **Server authority**: All game state mutations happen on the server
- **ModuleScripts** for shared logic — avoid monolithic scripts
- **Service/Controller pattern**: Services (server), Controllers (client)
- Scripts go in the correct container:
  - Server logic → `ServerScriptService`
  - Client logic → `StarterPlayerScripts` or `StarterCharacterScripts`
  - Shared modules → `ReplicatedStorage`
  - Server-only data → `ServerStorage`
  - UI → `StarterGui`

### 5. Error Handling
```lua
local success, result = pcall(function()
    return DataStoreService:GetDataStore("PlayerData"):GetAsync(key)
end)
if not success then
    warn("[DataService] Failed to load data:", result)
    -- Handle gracefully: use defaults, retry, etc.
end
```

### 6. Security (Always Apply)
- NEVER trust client-sent data — validate types, ranges, and permissions on server
- Keep sensitive logic in `ServerScriptService` (not visible to clients)
- Validate RemoteEvent arguments: check `typeof()`, ranges, and player state
- Rate-limit RemoteEvent calls from clients
- Never expose admin commands or server keys to ReplicatedStorage

---

## Script Template

When creating new scripts, use this template as a starting point:

```lua
--!strict
-- [ScriptName]
-- [Brief description of what this script does]
-- Container: [ServerScriptService/StarterPlayerScripts/ReplicatedStorage]

----- Services -----
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

----- Dependencies -----
-- local SomeModule = require(ReplicatedStorage.Modules.SomeModule)

----- Constants -----
local MAX_VALUE = 100

----- Types -----
type PlayerData = {
    coins: number,
    level: number,
    inventory: { string },
}

----- Variables -----
local activeConnections: { [Player]: { RBXScriptConnection } } = {}

----- Private Functions -----
local function cleanup(player: Player)
    local connections = activeConnections[player]
    if connections then
        for _, conn in connections do
            conn:Disconnect()
        end
        activeConnections[player] = nil
    end
end

----- Public / Event Handlers -----
local function onPlayerAdded(player: Player)
    activeConnections[player] = {}
    -- Setup logic here
end

----- Initialization -----
Players.PlayerAdded:Connect(onPlayerAdded)
Players.PlayerRemoving:Connect(cleanup)

-- Handle players already in game (Studio hot-reload)
for _, player in Players:GetPlayers() do
    task.spawn(onPlayerAdded, player)
end
```

---

## Response Guidelines

1. **Ask before building**: If the request is vague, ask clarifying questions about genre, scale, and target audience
2. **Read before writing**: If MCP is available, read existing scripts and game tree before modifying
3. **Small slices**: Generate 50-100 lines at a time for complex systems — easier to debug
4. **Explain the why**: Comment non-obvious code and explain architectural decisions
5. **Test path**: Suggest how to test the code (playtest steps, console checks)
6. **Migration-aware**: When touching existing code, check for legacy patterns and suggest migration if appropriate — but never force it. Incremental migration is acceptable.

---

## Common Workflows

### New Feature
1. Read existing project structure (MCP: `search_game_tree`)
2. Identify where the feature fits in the architecture
3. Create ModuleScript(s) in the appropriate container
4. Wire up server/client communication if needed
5. Test via playtest (MCP: `start_stop_play` + `get_console_output`)

### Debug Issue
1. Read the relevant script (MCP: `script_read`)
2. Check console output (MCP: `get_console_output`)
3. Identify the root cause — look for:
   - Missing `pcall` around DataStore/HTTP calls
   - Client-server boundary issues
   - Connection leaks (missing Disconnect)
   - Race conditions (script execution order)
4. Apply minimal fix
5. Verify fix via playtest

### Code Review
1. Read scripts in the project (MCP: `script_grep`)
2. Check against Core Coding Standards above
3. Flag security issues (client trust, exposed data)
4. Flag performance issues (expensive loops, part count)
5. Suggest improvements with before/after examples

---

## Knowledge Freshness Check

Nothing about this is automatic — there is no scheduler, hook, or background job behind it. It is an
instruction to *you*, the agent reading this file: **when this skill is invoked**, read
`metadata.json` in this skill directory and compare `last_updated` to the current date.

### Logic:
```
IF (current_date - last_updated) > update_interval_days (default: 7):
    TELL the user:
    "⏰ Roblox Dev Skill knowledge was last updated on {last_updated}, {days} days ago.
     Want me to run a knowledge update before we rely on it?"
    ...then WAIT. Do not update anything unless they say yes.
ELSE:
    Proceed normally — knowledge is fresh.
```

### Decision Rules:
- **NEVER auto-update** without user approval — always ask first
- **Source of truth**: https://create.roblox.com/docs, https://devforum.roblox.com
- **Decision maker**: Always the user (never the AI alone)
- **Update process**: Deep research → fact-check → QnA with user → apply → audit
- **After update**: Update `metadata.json` with new timestamp, version, and changes

---

## Manual Knowledge Update

The user can trigger a full knowledge update at any time by asking for one in plain language —
"update roblox skill knowledge", "refresh roblox dev skill", "roblox-update".

> **`/roblox-update` is NOT a registered slash command.** Earlier versions of this file presented it
> as one; it has never been installed in `~/.claude/commands/` or shipped by a plugin, so typing it
> resolves to nothing. It is a phrase this skill listens for, and that is all it has ever been.

### Update Protocol:
1. **Research** — Search for latest Roblox changes since `last_updated` timestamp
   - DevForum release notes, API changelog, deprecation notices
   - Use web search for "Roblox developer updates {year}" and "Roblox API changes {month} {year}"
   - Visit https://devforum.roblox.com/c/updates/release-notes/58
2. **Compare** — Cross-check findings against existing reference files
3. **Report** — Present findings to user with clear "what changed" summary
4. **Discuss** — QnA with user on any decisions (add/remove/modify content)
5. **Apply** — Update reference files (keep what's correct, update what changed)
6. **Audit** — Full fact-check (same pattern as initial audit: file integrity + content verification)
7. **Stamp** — Update `metadata.json` with new timestamp and changelog entry

> [!IMPORTANT]
> All updates must be research-based. No improvisation. When in doubt, ask the user.
> Fallback: consult official docs via context7 MCP or direct web search.

---

## Export / Publish

This skill is designed to be export-ready for GitHub publishing. See `README.md`
in the skill root directory for the complete structure and usage guide.

Users install it with the one-line installers in the repository (`install.sh`, `install.ps1`,
`install.cmd`), which link it into each agent's skills folder. When copying it by hand, the folder
**must be named `roblox-dev-skill`** — the Agent Skills spec requires the folder name to match the
`name` field above, and stricter agents skip a skill whose folder does not.

