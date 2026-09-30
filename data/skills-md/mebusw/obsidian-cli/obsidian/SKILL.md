---
name: obsidian
description: |
  Official Obsidian CLI (v1.12+). Complete command-line interface for 
  Obsidian notes, tasks, search, tags, properties, links, and more.
homepage: https://obsidian.md/help/cli
metadata:
  author: JackyShen
  openclaw:
    emoji: "🪨"
    requires:
      bins: ["obsidian"]
    platform: ["macos", "windows", "linux"]
---

# Obsidian CLI

Official command-line interface for Obsidian (v1.12+)

> The CLI binary file is `obsidian-cli` inside the app, but it registers and is invoked as `obsidian`. The Setup section below covers both ways.

## Prerequisites

- **Obsidian 1.12+** (1.12.7+ recommended)
- **Obsidian app must be running** when using CLI commands
- **Enable CLI**: Settings → General → Command line interface → Toggle ON

## Setup

When you toggle the CLI on in Settings → General, Obsidian registers the CLI for your platform. **Restart your terminal** after enabling.

### macOS

Registration creates a symlink at `/usr/local/bin/obsidian` → `/Applications/Obsidian.app/Contents/MacOS/obsidian-cli`. Requires admin privileges.

Verify the symlink:
```bash
ls -l /usr/local/bin/obsidian
```

If missing, create it manually:
```bash
sudo ln -sf /Applications/Obsidian.app/Contents/MacOS/obsidian-cli /usr/local/bin/obsidian
```

> ⚠️ **Pitfall: The CLI binary changes between Obsidian versions.** After updating Obsidian, the existing symlink may break or point to a stale binary. Two ways to fix:
> 1. **Re-create the symlink manually** (fastest):
> ```bash
> sudo ln -sf /Applications/Obsidian.app/Contents/MacOS/obsidian-cli /usr/local/bin/obsidian
> ```
> 2. Toggle CLI off → on in Settings → General to let Obsidian re-register.
>
> A simple post-update alias to put in `~/.zshrc`:
> ```bash
> alias obsidian-refresh='sudo ln -sf /Applications/Obsidian.app/Contents/MacOS/obsidian-cli /usr/local/bin/obsidian'
> ```

Alternative without a symlink — add the MacOS dir to PATH and call the binary directly:
```bash
export PATH="$PATH:/Applications/Obsidian.app/Contents/MacOS"
obsidian-cli version    # works without /usr/local/bin symlink
```

Cleanup: older versions added `# Added by Obsidian` lines to `~/.zprofile`. Safe to delete after re-registering with the current version.

### Linux

Binary copied to `~/.local/bin/obsidian`. Make sure `~/.local/bin` is in your PATH:
```bash
export PATH="$PATH:$HOME/.local/bin"
```

Verify:
```bash
ls -l ~/.local/bin/obsidian
```

If missing, copy it manually:
```bash
cp /path/to/Obsidian/obsidian-cli ~/.local/bin/obsidian
chmod 755 ~/.local/bin/obsidian
```

### Windows

Registration creates `Obsidian.com` (a terminal redirector for stdin/stdout) in the install folder and adds it to your PATH. **Restart your terminal** for PATH changes to take effect.

Verify:
```powershell
Test-Path "$env:LOCALAPPDATA\Obsidian\Obsidian.com"
```

### Test
```bash
obsidian version
```

## Syntax

- **Top-level option**: `vault=<name>` must come first (e.g. `obsidian vault="My Vault" daily`)
- **Parameters**: `name=value` or `name="value with spaces"`
- **Flags**: bare name, e.g. `overwrite`, `newtab`, `inline`, `permanent`, `case`
- **Newlines / tabs**: use `\n` and `\t` inside content strings
- **Target file**:
  - `file=<name>` — wikilink-style (resolves by basename, no `.md`)
  - `path=<folder/note.md>` — exact path
- **Default to active file**: most commands default to the active file when `file`/`path` is omitted
- **Output formats**: many list commands accept `format=text|json|tsv|csv|md|paths` (default varies; check `obsidian-cli help <cmd>`)

## Common Commands (with examples)

### Daily Notes
```bash
obsidian daily                                    # Open today's daily note
obsidian daily:append content="- [ ] Buy milk"    # Add to today's note
obsidian daily:prepend content="# Important"      # Add to top of today's note
obsidian daily:read                               # Print today's content
obsidian daily:path                               # Print today's file path
```

### Files
```bash
obsidian create name="Note" content="# Hello"     # Create a note
obsidian create name="Note" template=Meeting       # Create from a template
obsidian read file="Note"                          # Read note contents
obsidian append file="Note" content="More text"    # Append to note
obsidian prepend file="Note" content="Top text"    # Prepend to note
obsidian move file="Note" to="Archive/Note.md"     # Move note
obsidian rename file="Note" name="New Name"        # Rename note
obsidian delete file="Note" permanent              # Delete (skip trash)
obsidian open file="Note" newtab                   # Open note in new tab
```

### Search
```bash
obsidian search query="meeting notes"              # List matching files
obsidian search:context query="TODO"               # Show matching lines
obsidian search:open query="project"               # Open search view
```

### Tasks
```bash
obsidian tasks daily todo                          # Incomplete tasks in daily note
obsidian tasks todo                                # All incomplete tasks
obsidian task daily line=3 toggle                  # Toggle task at line 3
obsidian task ref="Note.md:5" done                 # Mark a specific task done
```

### Tags & Properties
```bash
obsidian tags counts                               # List tags with counts
obsidian tags counts sort=count                    # Sort by frequency
obsidian tag name="#status" verbose                # Files containing a tag
obsidian property:set name="status" value="done" file="Note"
obsidian property:read name="status" file="Note"
obsidian property:remove name="status" file="Note"
obsidian properties file="Note"                    # List all properties
```

### Links
```bash
obsidian backlinks file="Note"                     # Incoming links
obsidian links file="Note"                         # Outgoing links
obsidian orphans                                   # Files with no incoming links
obsidian deadends                                  # Files with no outgoing links
obsidian unresolved                                # Broken links
```

### Developer
```bash
obsidian devtools                                  # Toggle Electron dev tools
obsidian eval code="app.vault.getFiles().length"   # Run JavaScript in app context
obsidian dev:screenshot path=screenshot.png        # Take a screenshot
obsidian dev:console limit=20 level=error          # Show captured console messages
obsidian dev:errors                                # Show captured errors
obsidian dev:dom selector=".workspace"             # Query DOM
obsidian dev:css selector=".mod-header"            # Inspect CSS source
obsidian dev:cdp method="Page.reload"              # Run a CDP command
obsidian plugin:reload id=my-plugin                # Reload a plugin
```

## All Commands (95 total)

> Verified against `obsidian-cli help` output. Plugin-specific commands (Sync, Publish, etc.) only appear when those plugins are enabled — run `obsidian-cli help` again after enabling a plugin to see its commands.

### General (4)
- `help` - Show help / help for a specific command
- `version` - Show Obsidian version
- `reload` - Reload the vault
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
- `command` - Execute an Obsidian command by ID
- `hotkeys` - List hotkeys
- `hotkey` - Get hotkey for a command

### Tabs & Workspace (3)
- `tabs` - List open tabs
- `tab:open` - Open a new tab
- `workspace` - Show workspace tree

### File History & Diff (6)
- `diff` - List or diff local/sync versions
- `history` - List file history versions
- `history:list` - List files with history
- `history:read` - Read a file history version
- `history:restore` - Restore a file history version
- `history:open` - Open file recovery

### Recents (1)
- `recents` - List recently opened files

### Word Count (1)
- `wordcount` - Count words and characters

### Random Notes (2)
- `random` - Open a random note
- `random:read` - Read a random note

### Vault (2)
- `vault` - Show vault info
- `vaults` - List known vaults

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
- `plugins:restrict` - Toggle or check restricted mode
- `plugin` - Get plugin info
- `plugin:enable` - Enable a plugin
- `plugin:disable` - Disable a plugin
- `plugin:install` - Install a community plugin
- `plugin:uninstall` - Uninstall a community plugin
- `plugin:reload` - Reload a plugin

### Developer (10)
- `devtools` - Toggle Electron dev tools
- `eval` - Execute JavaScript and return result
- `dev:screenshot` - Take a screenshot
- `dev:console` - Show captured console messages
- `dev:errors` - Show captured errors
- `dev:css` - Inspect CSS with source locations
- `dev:dom` - Query DOM elements
- `dev:cdp` - Run a Chrome DevTools Protocol command
- `dev:debug` - Attach/detach Chrome DevTools Protocol debugger
- `dev:mobile` - Toggle mobile emulation

## Troubleshooting

**"Cannot connect to Obsidian"**
- Ensure Obsidian is running
- Enable CLI in Settings → General → Command line interface

**"Command not found: obsidian"**
- Follow Setup above for your platform
- Verify the symlink:
  - macOS: `ls -l /usr/local/bin/obsidian`
  - Linux: `ls -l ~/.local/bin/obsidian`

**Commands broke right after an Obsidian update**
- The CLI binary changes between releases — re-create the symlink:
  ```bash
  sudo ln -sf /Applications/Obsidian.app/Contents/MacOS/obsidian-cli /usr/local/bin/obsidian
  ```
  Or toggle CLI off → on in Settings → General to let Obsidian re-register.

**"File not found"**
- `file=Name` resolves like wikilinks (no path, no `.md`)
- `path=folder/file.md` for exact paths

## 中文说明

### 前置条件
- Obsidian 1.12+（1.12.7+ 推荐）
- Obsidian 必须运行中
- 启用 CLI：设置 → 通用 → 命令行界面

### 平台配置

**macOS**：CLI 注册会在 `/usr/local/bin/obsidian` 创建一个软链接指向 `/Applications/Obsidian.app/Contents/MacOS/obsidian-cli`。

> ⚠️ **坑点：升级 Obsidian 后软链接会失效。** 二进制文件每次版本更新都会变。最快的修复：
>
> ```bash
> sudo ln -sf /Applications/Obsidian.app/Contents/MacOS/obsidian-cli /usr/local/bin/obsidian
> ```
>
> 或者到 Settings → General 把 CLI 关掉再打开让 Obsidian 重新注册。

**Windows**：注册会把 `Obsidian.com`（终端重定向器）放到安装目录并加入 PATH，需要**重启终端**才生效。

**Linux**：二进制复制到 `~/.local/bin/obsidian`，确保该目录在 PATH 中。

### 常用命令
```bash
obsidian daily                    # 打开今日日记
obsidian create name="笔记"        # 创建笔记
obsidian search query="关键词"     # 搜索，只显示文件名
obsidian search:context query="关键词"     # 搜索，显示文件名以及内容所在的行
obsidian tasks daily todo         # 列出未完成任务
obsidian tags counts              # 列出标签
```