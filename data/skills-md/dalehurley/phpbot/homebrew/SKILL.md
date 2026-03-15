---
name: homebrew
description: "Install, manage, and search for software packages on macOS using Homebrew. Use this skill when the user asks to install software, apps, CLI tools, developer utilities, programming languages, databases, or any package on a Mac. Supports formulae (CLI tools) and casks (GUI apps). Can also search, update, upgrade, uninstall, and diagnose Homebrew issues."
tags:
  [
    macos,
    homebrew,
    brew,
    package-manager,
    install,
    software,
    cask,
    auto-generated,
  ]
version: 0.1.0
---

# Skill: homebrew

## When to Use

Use this skill when the user asks to:

- Install software, a tool, an app, or a package on macOS
- Install a programming language, database, or dev tool (e.g. node, python, redis, postgres, go, rust)
- Install a GUI/desktop application via `brew install --cask` (e.g. Chrome, Slack, Docker, VS Code)
- Search for available packages or check if something is installable via Homebrew
- List installed packages or check what's currently on the system
- Update Homebrew or upgrade installed packages
- Uninstall / remove a package
- Diagnose or fix Homebrew issues (`brew doctor`)
- Tap a new Homebrew repository
- Check info or version of an installed package

## Prerequisites

- **macOS only** — Homebrew is a macOS package manager (also works on Linux but this skill targets Mac)
- Homebrew must be installed. If not, install it first:
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```

## Available Tool

The `brew` tool is registered as a core tool. Use it directly:

| Action         | Tool Input                                                  | Description                          |
| -------------- | ----------------------------------------------------------- | ------------------------------------ |
| `install`      | `{"action": "install", "packages": ["node", "redis"]}`      | Install one or more formulae         |
| `install_cask` | `{"action": "install_cask", "packages": ["google-chrome"]}` | Install GUI apps via cask            |
| `uninstall`    | `{"action": "uninstall", "packages": ["node"]}`             | Remove installed packages            |
| `search`       | `{"action": "search", "query": "python"}`                   | Search for available packages        |
| `info`         | `{"action": "info", "packages": ["node"]}`                  | Get detailed info about a package    |
| `list`         | `{"action": "list"}`                                        | List all installed formulae          |
| `list_casks`   | `{"action": "list_casks"}`                                  | List all installed cask apps         |
| `update`       | `{"action": "update"}`                                      | Update Homebrew itself               |
| `upgrade`      | `{"action": "upgrade"}`                                     | Upgrade all outdated packages        |
| `upgrade`      | `{"action": "upgrade", "packages": ["node"]}`               | Upgrade specific packages            |
| `doctor`       | `{"action": "doctor"}`                                      | Diagnose Homebrew issues             |
| `tap`          | `{"action": "tap", "tap_name": "homebrew/cask-fonts"}`      | Add a third-party repo               |
| `outdated`     | `{"action": "outdated"}`                                    | Show packages with updates available |

## Procedure

1. **Check Homebrew is available**: The `brew` tool will automatically verify Homebrew is installed before running any action. If not found, it will return instructions to install it.
2. **Determine what to install**: Extract the package name(s) from the user's request. If unclear, use `ask_user` to clarify.
3. **Choose formulae vs cask**: CLI tools use `install`, GUI apps (Chrome, Slack, Docker Desktop, etc.) use `install_cask`.
4. **Execute**: Call the `brew` tool with the appropriate action and parameters.
5. **Report results**: Confirm what was installed/updated/removed with version info where available.

## Common Package Examples

### CLI Tools & Languages (formulae)

| Request              | Package Name                    |
| -------------------- | ------------------------------- |
| "install node"       | `node`                          |
| "install Python"     | `python@3.12` or `python`       |
| "install PHP"        | `php`                           |
| "install Go"         | `go`                            |
| "install Rust"       | `rust`                          |
| "install Redis"      | `redis`                         |
| "install PostgreSQL" | `postgresql@16` or `postgresql` |
| "install MySQL"      | `mysql`                         |
| "install Git"        | `git`                           |
| "install FFmpeg"     | `ffmpeg`                        |
| "install wget"       | `wget`                          |
| "install jq"         | `jq`                            |
| "install ripgrep"    | `ripgrep`                       |
| "install Docker CLI" | `docker`                        |

### GUI Apps (casks)

| Request                  | Cask Name            |
| ------------------------ | -------------------- |
| "install Chrome"         | `google-chrome`      |
| "install VS Code"        | `visual-studio-code` |
| "install Slack"          | `slack`              |
| "install Docker Desktop" | `docker` (cask)      |
| "install Spotify"        | `spotify`            |
| "install Figma"          | `figma`              |
| "install iTerm"          | `iterm2`             |
| "install Rectangle"      | `rectangle`          |
| "install 1Password"      | `1password`          |
| "install Cursor"         | `cursor`             |

## Example

Example requests that trigger this skill:

```
install node and redis on my mac
I need ffmpeg installed
install google chrome
what packages do I have installed?
search for a markdown editor
update all my brew packages
is postgres installed?
install docker desktop
```
