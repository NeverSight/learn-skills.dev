---
name: se-dev-server-code
description: Allows reading the decompiled C# code of the Space Engineers Dedicated Server
license: MIT
allowed-tools: Read, Bash(*Prepare.bat*), Bash(*Clean.bat*), Bash(*run_prepare.sh*), Bash(*test_search.bat*), Bash(*uv run search_code.py *), Bash(*uv run index_code.py *), Bash(*busybox* grep *), Bash(*busybox* find *), Bash(*busybox* cat *), Bash(*busybox* head *), Bash(*busybox* tail *), Bash(*busybox* ls*), Bash(*busybox* wc *), Bash(*busybox* sort *), Bash(*busybox* uniq *), Bash(*busybox* tree*)
---

# SE Dev Server Code Skill

Allows reading the decompiled C# code of the Space Engineers Dedicated Server. The "game logic" of the server is largely the same as the game (client) is running. The entry point (main executable), some aspects of logging and configuration differ. Also, some of the libraries are not used by the server, but they may still present to provide the necessary data structures and some backend functionality.

**⚠️ CRITICAL: Commands run in a UNIX shell (busybox), NOT Windows CMD. Use bash syntax!**

Examples:
- ✅ `test -f file.txt && echo exists`
- ✅ `ls -la | head -10`
- ❌ `if exist file.txt (echo exists)` - This will NOT work

**Actions:**

- **prepare**: Run the one-time preparation (Prepare.bat)
- **bash**: Run UNIX shell commands via busybox
- **search**: Run code searches using `search_code.py`
- **test**: Test this skill by running `test_search.bat`

## Routing Decision

Check these patterns **in order** - first match wins:

| Priority | Pattern | Example | Route |
|----------|---------|---------|-------|
| 1 | Empty or bare invocation | `se-dev-server-code` | Show this help |
| 2 | Prepare keywords | `se-dev-server-code prepare`, `se-dev-server-code setup`, `se-dev-server-code init` | prepare |
| 3 | Bash/shell keywords | `se-dev-server-code bash`, `se-dev-server-code grep`, `se-dev-server-code cat` | bash |
| 4 | Search keywords | `se-dev-server-code search`, `se-dev-server-code find class`, `se-dev-server-code lookup` | search |
| 5 | Test keywords | `se-dev-server-code test`, `se-dev-server-code verify`, `se-dev-server-code check` | test |

## Getting Started

**⚠️ CRITICAL: Before running ANY commands, read [CommandExecution.md](CommandExecution.md) to avoid common mistakes that cause command failures.**

If the `Prepare.DONE` file is missing in this folder, you MUST run the one-time preparation steps first. See the [prepare action](./actions/prepare.md).

## Essential Documentation

- **[CommandExecution.md](CommandExecution.md)** - ⚠️ **READ THIS FIRST** - How to run commands correctly on Windows

## Code Search Documentation

- **[QuickStart.md](QuickStart.md)** - More examples and quick reference
- **[CodeSearch.md](CodeSearch.md)** - Complete guide to searching classes, methods, fields, etc.
- **[HierarchySearch.md](HierarchySearch.md)** - Finding class/interface inheritance and implementations
- **[Advanced.md](Advanced.md)** - Power user techniques for complex searches
- **[Troubleshooting.md](Troubleshooting.md)** - What to do when searches return NO-MATCHES or too many results
- **[Implementation.md](Implementation.md)** - Technical details for skill contributors (optional)

## Quick Search Examples

```bash
# Find class declarations
uv run search_code.py class declaration MyCubeBlock

# Find method signatures
uv run search_code.py method signature UpdateBeforeSimulation

# Find class hierarchy
uv run search_code.py class children MyTerminalBlock

# Count results before viewing (useful for large result sets)
uv run search_code.py class usage MyEntity --count

# Limit number of results
uv run search_code.py class usage MyEntity --limit 10

# Paginate through results
uv run search_code.py class usage MyEntity --limit 10 --offset 0
uv run search_code.py class usage MyEntity --limit 10 --offset 20
```

Always check the server code when:
- You're unsure about the server's internal APIs and how to interface with them.
- The inner workings of the Space Engineers Dedicated Server is unclear.

## Custom Scripting

For building your own utility scripts to work with the indexes and decompiled code:

- **[ScriptingGuide.md](ScriptingGuide.md)** - How to write Python scripts, use BusyBox, handle Windows paths

## Server Content Data

The textual part of the server's `Content` is copied into the `Content` folder for free text search:
- Language translations, including the string IDs
- Block and other entity definitions
- Default blueprints and scenarios
- See [ContentTypes.md](ContentTypes.md) for the full list of content types

## Running the Dedicated Server

The server executable is `SpaceEngineersDedicated.exe` in the `DedicatedServer64` folder.

### Headless Mode (No UI)

```
SpaceEngineersDedicated.exe -console
```

This bypasses the Telerik WinForms configuration UI and runs the server directly.

### Configuration

The server is configured via XML files. The primary configuration file is `SpaceEngineers-Dedicated.cfg` located in the server's AppData directory (typically `%APPDATA%\SpaceEngineersDedicated\`).

Key configuration areas:
- **Server settings** (name, world, mods, max players)
- **World settings** (game mode, inventory size, welding speed)
- **Network settings** (port, public/private)

Configuration should be done by editing the XML files directly or with utility Python scripts. See below for planned utilities.

### Planned Utility Scripts (Not Yet Implemented)

- **config_editor.py** — Read and modify `SpaceEngineers-Dedicated.cfg` values from the command line (e.g. set server name, max players, world name)
- **world_manager.py** — List, backup, and manage saved worlds in the server data directory
- **mod_manager.py** — List and validate mods referenced in the configuration

### Server-Only Assemblies

| Assembly | Description |
|----------|-------------|
| `SpaceEngineersDedicated` | Server entry point (replaces `SpaceEngineers.exe`) |
| `VRage.Dedicated` | Dedicated server framework, lifecycle, and configuration |
| `VRage.RemoteClient.Core` | Remote client support (RCON-like functionality) |

## General Rules

- In the `Decompiled` folder search only inside the C# source files (*.cs) in general. If you work on transpiler or preloader patches, then also search in the IL code (*.il) files.
- In the `Content` folder search the files appropriate for the task. See [ContentTypes.md](ContentTypes.md) for the list of types.
- Do not search for decompiled server code outside the `Decompiled` folder which is at the same level as this skill file. The decompiled server source tree must be there if the preparation succeeded.
- Do not search for server content data outside the `Content` folder which is at the same level as this skill file. The copied server content must be there if the preparation succeeded.

## Action References

Follow the detailed instructions in:

- [prepare action](./actions/prepare.md) - One-time preparation
- [bash action](./actions/bash.md) - Running UNIX shell commands via busybox
- [search action](./actions/search.md) - Running code searches
- [test action](./actions/test.md) - Testing this skill

## Remarks

The original source of this skill: https://github.com/viktor-ferenczi/se-dev-skills
