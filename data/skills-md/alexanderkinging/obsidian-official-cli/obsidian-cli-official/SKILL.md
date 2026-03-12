---
name: obsidian-cli-official
description: |
  Official Obsidian CLI (v1.12+). Complete command-line interface for 
  Obsidian notes, tasks, search, tags, properties, links, and more.
homepage: https://help.obsidian.md/cli
metadata:
  openclaw:
    emoji: "💎"
    requires:
      bins: ["obsidian"]
    platform: ["macos", "windows", "linux"]
---

# Obsidian Official CLI

Official command-line interface for Obsidian (v1.12+). 115 commands.

## Prerequisites

- **Obsidian 1.12+** (free, public release since v1.12)
- **Obsidian must be running** (CLI connects via IPC)
- **Enable CLI**: Settings → General → Enable CLI

## Setup

Add Obsidian to PATH:

**macOS:**
```bash
export PATH="$PATH:/Applications/Obsidian.app/Contents/MacOS"
```

**Windows:**
```powershell
$env:PATH += ";$env:LOCALAPPDATA\Obsidian"
```

**Linux:**
- Snap: Already in PATH
- Flatpak: `alias obsidian='flatpak run md.obsidian.Obsidian'`
- AppImage: Move to `~/.local/bin` and `chmod +x`

**Test:** `obsidian version`

## Syntax

- **Parameters**: `name=value` or `name="value with spaces"`
- **Flags**: just the name, e.g. `open`, `overwrite`
- **Newlines**: use `\n` in content strings
- **Target vault**: `obsidian vault="My Vault" <command>` (must be first)
- **Target file**: `file=<name>` (wikilink-style) or `path=<folder/file.md>` (exact)
- **Copy output**: append `--copy` to any command

## Common Commands (with examples)

### Daily Notes
```bash
obsidian daily                                    # Open today
obsidian daily:append content="- [ ] Buy milk"    # Add to today
obsidian daily:prepend content="# Important"      # Add to top
obsidian daily:read                               # Read today's content
obsidian daily:path                               # Get daily note path
```

### Files
```bash
obsidian create name="Note" content="# Hello"     # Create note
obsidian create name="Note" template=Meeting       # Create from template
obsidian read file="Note"                          # Read note
obsidian append file="Note" content="More text"    # Append to note
obsidian prepend file="Note" content="Top text"    # Prepend to note
obsidian move file="Note" to="Archive/Note.md"     # Move note
obsidian rename file="Note" name="New Name"        # Rename note
obsidian delete file="Note"                        # Delete note
obsidian open file="Note"                          # Open note
```

### Search
```bash
obsidian search query="meeting notes"              # Search vault
obsidian search:context query="TODO"               # Search with context
obsidian search:open query="project"               # Open search view
```

### Tasks
```bash
obsidian tasks daily todo                          # Incomplete tasks in daily
obsidian tasks todo                                # All incomplete tasks
obsidian task daily line=3 toggle                  # Toggle task at line 3
```

### Tags & Properties
```bash
obsidian tags counts                               # List all tags
obsidian tags counts sort=count                    # Sort by frequency
obsidian property:set name="status" value="done" file="Note"
obsidian property:read name="status" file="Note"
obsidian property:remove name="status" file="Note"
obsidian properties file="Note"                    # List all properties
```

### Links
```bash
obsidian backlinks file="Note"                     # Incoming links
obsidian links file="Note"                         # Outgoing links
obsidian orphans                                   # No incoming links
obsidian deadends                                  # No outgoing links
obsidian unresolved                                # Broken links
```

### Developer
```bash
obsidian devtools                                  # Open dev tools
obsidian eval code="app.vault.getFiles().length"   # Run JavaScript
obsidian dev:screenshot path=screenshot.png         # Screenshot
obsidian plugin:reload id=my-plugin                # Reload plugin
```

## All Commands (115 total)

### General (4)
- `help` - Show help / help for specific command
- `version` - Show Obsidian version
- `reload` - Reload the app window
- `restart` - Restart the app

### Daily Notes (5)
- `daily` - Open daily note
- `daily:path` - Get daily note path
- `daily:read` - Read daily note contents
- `daily:append` - Append content to daily note
- `daily:prepend` - Prepend content to daily note

### Files & Folders (12)
- `file` - Show file info
- `files` - List files in vault
- `folder` - Show folder info
- `folders` - List folders in vault
- `open` - Open a file
- `create` - Create a new file
- `read` - Read file contents
- `append` - Append content to a file
- `prepend` - Prepend content to a file
- `move` - Move or rename a file
- `rename` - Rename a file
- `delete` - Delete a file

### Search (3)
- `search` - Search vault for text
- `search:context` - Search with matching line context
- `search:open` - Open search view

### Tasks (2)
- `tasks` - List tasks in the vault
- `task` - Show or update a task

### Tags (2)
- `tags` - List tags in the vault
- `tag` - Get tag info

### Properties (4)
- `properties` - List properties in the vault
- `property:set` - Set a property on a file
- `property:remove` - Remove a property from a file
- `property:read` - Read a property value

### Aliases (1)
- `aliases` - List aliases in the vault

### Links (5)
- `backlinks` - List backlinks to a file
- `links` - List outgoing links from a file
- `unresolved` - List unresolved links
- `orphans` - Files with no incoming links
- `deadends` - Files with no outgoing links

### Outline (1)
- `outline` - Show headings for a file

### Bookmarks (2)
- `bookmarks` - List bookmarks
- `bookmark` - Add a bookmark

### Bases / Database (4)
- `bases` - List all base files
- `base:views` - List views in a base
- `base:create` - Create a new item in a base
- `base:query` - Query a base and return results

### Templates (3)
- `templates` - List templates
- `template:read` - Read template content
- `template:insert` - Insert template into active file

### Commands & Hotkeys (4)
- `commands` - List available command IDs
- `command` - Execute an Obsidian command
- `hotkeys` - List hotkeys
- `hotkey` - Get hotkey for a command

### Tabs & Workspaces (7)
- `tabs` - List open tabs
- `tab:open` - Open a new tab
- `workspace` - Show workspace tree
- `workspaces` - List saved workspaces
- `workspace:load` - Load a saved workspace
- `workspace:save` - Save current layout
- `workspace:delete` - Delete a saved workspace

### File History & Diff (6)
- `diff` - List or diff local/sync versions
- `history` - List file history versions
- `history:list` - List files with history
- `history:read` - Read a file history version
- `history:restore` - Restore a file history version
- `history:open` - Open file recovery

### Sync (7)
- `sync` - Pause or resume sync (on/off)
- `sync:status` - Show sync status
- `sync:history` - List sync version history
- `sync:read` - Read a sync version
- `sync:restore` - Restore a sync version
- `sync:open` - Open sync history
- `sync:deleted` - List deleted files in sync

### Publish (6)
- `publish:site` - Show publish site info
- `publish:list` - List published files
- `publish:status` - Show publish status
- `publish:add` - Publish files
- `publish:remove` - Unpublish files
- `publish:open` - Open published site

### Themes & Snippets (9)
- `themes` - List installed themes
- `theme` - Show active theme or get info
- `theme:set` - Set active theme
- `theme:install` - Install a community theme
- `theme:uninstall` - Uninstall a theme
- `snippets` - List installed CSS snippets
- `snippets:enabled` - List enabled CSS snippets
- `snippet:enable` - Enable a CSS snippet
- `snippet:disable` - Disable a CSS snippet

### Plugins (9)
- `plugins` - List installed plugins
- `plugins:enabled` - List enabled plugins
- `plugins:restrict` - Toggle restricted mode
- `plugin` - Get plugin info
- `plugin:enable` - Enable a plugin
- `plugin:disable` - Disable a plugin
- `plugin:install` - Install a community plugin
- `plugin:uninstall` - Uninstall a community plugin
- `plugin:reload` - Reload a plugin

### Vault (3)
- `vault` - Show vault info
- `vaults` - List known vaults
- `vault:open` - Open a vault (TUI only)

### Random Notes (2)
- `random` - Open a random note
- `random:read` - Read a random note

### Unique Notes (1)
- `unique` - Create unique note

### Web Viewer (1)
- `web` - Open URL in web viewer

### Word Count (1)
- `wordcount` - Count words and characters

### Recently Opened (1)
- `recents` - List recently opened files

### Developer (10)
- `devtools` - Toggle Electron dev tools
- `eval` - Execute JavaScript
- `dev:screenshot` - Take a screenshot
- `dev:console` - Show captured console messages
- `dev:errors` - Show captured errors
- `dev:css` - Inspect CSS with source locations
- `dev:dom` - Query DOM elements
- `dev:cdp` - Run Chrome DevTools Protocol command
- `dev:debug` - Attach/detach CDP debugger
- `dev:mobile` - Toggle mobile emulation

## Troubleshooting

**"Cannot connect to Obsidian"**
- Ensure Obsidian is running
- Enable CLI in Settings → General → Enable CLI

**"Command not found: obsidian"**
- Add Obsidian to PATH (see Setup above)

**"File not found"**
- `file=Name` resolves like wikilinks (no path, no .md)
- `path=folder/file.md` for exact paths

## 中文说明

### 前置条件
- Obsidian 1.12+（免费公开版本）
- Obsidian 必须运行中
- 启用 CLI：设置 → 通用 → 启用 CLI

### 常用命令
```bash
obsidian daily                    # 打开今日日记
obsidian create name="笔记"       # 创建笔记
obsidian search query="关键词"    # 搜索
obsidian tasks daily todo         # 列出未完成任务
obsidian tags counts              # 列出标签
```
