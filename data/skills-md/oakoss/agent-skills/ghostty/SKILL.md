---
name: ghostty
description: 'Controls the Ghostty terminal emulator via CLI actions and configuration. Use when managing Ghostty windows, fonts, themes, keybinds, config validation, or debugging terminal configuration. Use for ghostty CLI, terminal config, theme selection, font management.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: 'https://ghostty.org/docs'
user-invocable: false
---

# Ghostty Skill

## Overview

Ghostty is a fast, feature-rich, cross-platform terminal emulator that uses platform-native UI and GPU acceleration. It provides a CLI with `+action` commands for querying configuration, listing themes/fonts, validating config, and opening new windows via IPC. Window, tab, and split management are handled through keybind actions configured in the config file, not through CLI commands.

**When to use:** Configuring Ghostty themes, fonts, and keybinds; validating config files; querying available actions and themes; opening new windows from scripts; debugging terminal rendering issues.

**When NOT to use:** Managing other terminal emulators; tasks unrelated to terminal configuration.

## Quick Reference

| Task             | Command / Config                    | Key Points                                        |
| ---------------- | ----------------------------------- | ------------------------------------------------- |
| List CLI actions | `ghostty +list-actions`             | Shows keybind actions, not CLI actions            |
| List themes      | `ghostty +list-themes`              | Interactive TUI preview; `--color=dark` to filter |
| List fonts       | `ghostty +list-fonts`               | Uses Ghostty's font discovery                     |
| List keybinds    | `ghostty +list-keybinds`            | Add `--default` for defaults only                 |
| List colors      | `ghostty +list-colors`              | Named RGB colors available in config              |
| Show config      | `ghostty +show-config`              | Add `--default --docs` for all options            |
| Validate config  | `ghostty +validate-config`          | Check config file for errors                      |
| Edit config      | `ghostty +edit-config`              | Opens config in `$VISUAL` or `$EDITOR`            |
| New window (IPC) | `ghostty +new-window`               | Linux/GTK only via D-Bus; use `-e` for command    |
| Run command      | `ghostty -e htop`                   | Arguments after `-e` are the command              |
| Set working dir  | `ghostty --working-directory=/path` | Changes directory before running command          |
| Custom config    | `ghostty --config-file=/path`       | Load additional config file                       |
| Check version    | `ghostty --version`                 | Display version info                              |
| SSH terminfo     | `ghostty +ssh-cache`                | Manage SSH terminfo cache for remote hosts        |
| Show font face   | `ghostty +show-face <codepoint>`    | Which font renders a specific Unicode codepoint   |
| Crash reports    | `ghostty +crash-report`             | Inspect and manage crash reports                  |

## Common Mistakes

| Mistake                                                         | Correct Pattern                                                                                       |
| --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Running `ghostty +new-tab` or `+new-split` as CLI commands      | These are keybind actions, not CLI actions; configure them in the config file with `keybind = ...`    |
| Running `ghostty` without full path when not symlinked on macOS | Use `/Applications/Ghostty.app/Contents/MacOS/ghostty` or create a symlink                            |
| Using `+new-window` on macOS expecting it to work               | `+new-window` uses D-Bus IPC and only works on Linux/GTK                                              |
| Editing config without reloading                                | Use the `reload_config` keybind action (default: `ctrl+shift+comma` on Linux)                         |
| Using `--config-file` with a relative path                      | Use absolute paths for `--config-file` to avoid resolution issues                                     |
| Passing unknown actions without checking available list         | Run `ghostty +help` to see CLI actions or `+list-actions` for keybind actions                         |
| Confusing CLI actions with keybind actions                      | CLI actions use `+action` syntax; keybind actions are configured via `keybind = key=action` in config |

## Delegation

- **Discover available actions and themes**: Use `Explore` agent to run `ghostty +list-actions` and `ghostty +list-themes`
- **Automate terminal layouts**: Use `Task` agent to script window creation and config changes
- **Plan configuration changes**: Use `Plan` agent to design keybind and theme configurations before applying

## References

- [CLI actions, flags, and IPC commands](references/cli-actions.md)
- [Configuration file, themes, fonts, keybinds, and debugging](references/configuration.md)
