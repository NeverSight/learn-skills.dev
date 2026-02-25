---
name: omarchy
description: Manage and configure Omarchy Linux systems. Use when user asks about Omarchy, Hyprland, themes, keybindings, system config, or any omarchy-* commands.
---

# Omarchy Skill

Manage [Omarchy](https://omarchy.org/) Linux systems using natural language.

## ⛔ NEVER MODIFY CORE FILES

**DO NOT edit, write, or delete any files in `~/.local/share/omarchy/`**

This directory contains Omarchy's core system files. User configuration belongs in `~/.config/` instead.

If you need to change behavior controlled by a file in `~/.local/share/omarchy/`, find or create the corresponding override in `~/.config/`.

## Discovery

Omarchy provides ~145 commands following the pattern `omarchy-<category>-<action>`.

### Find Commands

```bash
# List all omarchy commands
compgen -c | grep -E '^omarchy-' | sort -u

# Find commands by category
compgen -c | grep -E '^omarchy-theme'
compgen -c | grep -E '^omarchy-restart'

# Read a command's source to understand it
cat $(which omarchy-theme-set)
```

### Command Categories

| Prefix | Purpose | Example |
|--------|---------|---------|
| `omarchy-refresh-*` | Reset config to Omarchy defaults (backs up first) | `omarchy-refresh-waybar` |
| `omarchy-restart-*` | Restart a service/app | `omarchy-restart-waybar` |
| `omarchy-toggle-*` | Toggle feature on/off | `omarchy-toggle-nightlight` |
| `omarchy-theme-*` | Theme management | `omarchy-theme-set <name>` |
| `omarchy-install-*` | Install optional software | `omarchy-install-docker-dbs` |
| `omarchy-launch-*` | Launch apps | `omarchy-launch-browser` |
| `omarchy-cmd-*` | System commands | `omarchy-cmd-screenshot` |
| `omarchy-pkg-*` | Package management | `omarchy-pkg-install <pkg>` |
| `omarchy-setup-*` | Initial setup tasks | `omarchy-setup-fingerprint` |
| `omarchy-update-*` | System updates | `omarchy-update` |

## Configuration Locations

### Hyprland (Window Manager)

```
~/.config/hypr/
├── hyprland.conf      # Main config (sources others)
├── bindings.conf      # Keybindings
├── monitors.conf      # Display configuration
├── input.conf         # Keyboard/mouse settings
├── looknfeel.conf     # Appearance (gaps, borders, animations)
├── envs.conf          # Environment variables
├── autostart.conf     # Startup applications
├── hypridle.conf      # Idle behavior (screen off, lock, suspend)
├── hyprlock.conf      # Lock screen appearance
└── hyprsunset.conf    # Night light / blue light filter
```

**Restart/Refresh:**
- `omarchy-refresh-hyprland` - Reset to defaults
- Hyprland auto-reloads on config save (no restart needed)
- `omarchy-restart-hypridle` / `omarchy-restart-hyprsunset` for those services

### Waybar (Status Bar)

```
~/.config/waybar/
├── config.jsonc       # Bar layout and modules (JSONC format)
└── style.css          # Styling
```

**Restart/Refresh:**
- `omarchy-restart-waybar` - Restart waybar
- `omarchy-refresh-waybar` - Reset to defaults
- `omarchy-toggle-waybar` - Show/hide

### Walker (App Launcher)

```
~/.config/walker/
└── config.toml        # Launcher configuration
```

**Restart/Refresh:**
- `omarchy-restart-walker`
- `omarchy-refresh-walker`

### Terminals

```
~/.config/alacritty/alacritty.toml
~/.config/kitty/kitty.conf
~/.config/ghostty/config
```

**Restart:**
- `omarchy-restart-terminal`

### Other Configs

| App | Location |
|-----|----------|
| btop | `~/.config/btop/btop.conf` |
| fastfetch | `~/.config/fastfetch/config.jsonc` |
| lazygit | `~/.config/lazygit/config.yml` |
| starship | `~/.config/starship.toml` |
| git | `~/.config/git/config` |

## Omarchy Data

```
~/.local/share/omarchy/
├── bin/               # All omarchy-* scripts
├── config/            # Default config templates
├── themes/            # Installed themes
└── version            # Current version info
```

## Safe Editing Pattern

When modifying any Omarchy config:

### 1. Read Current Config

```bash
cat ~/.config/<app>/config
```

### 2. Backup Before Changes

```bash
cp ~/.config/<app>/config ~/.config/<app>/config.bak.$(date +%s)
```

### 3. Make Changes

Use the Edit tool. Preserve existing structure and comments.

### 4. Apply Changes

```bash
# For most apps, use the restart command
omarchy-restart-<app>

# Or reset to defaults (creates backup automatically)
omarchy-refresh-<app>
```

### 5. Explain What You Did

After completing changes, include a **Learn More** section to help the user understand what happened:

```
> **Learn More**
>
> [Explain what file(s) were modified or commands were run]
> [Explain why these changes achieve the user's goal]
> [Explain key config options that were set and what they control]
```

**Example:**

> **Learn More**
>
> Modified `~/.config/hypr/looknfeel.conf` to change window gaps.
> The `gaps_in` setting controls space between adjacent windows (set to 5px).
> The `gaps_out` setting controls space between windows and screen edges (set to 10px).

## Common Tasks

### Themes

```bash
omarchy-theme-list              # Show available themes
omarchy-theme-current           # Show current theme
omarchy-theme-set <name>        # Apply theme
omarchy-theme-next              # Cycle to next theme
omarchy-theme-bg-next           # Cycle wallpaper
omarchy-theme-install <url>     # Install from git repo
```

### Keybindings

Edit `~/.config/hypr/bindings.conf`. Format:
```
bind = SUPER, Return, exec, xdg-terminal-exec
bind = SUPER, Q, killactive
bind = SUPER SHIFT, E, exit
```

View current bindings: `omarchy-menu-keybindings`

### Display/Monitors

Edit `~/.config/hypr/monitors.conf`. Format:
```
monitor = eDP-1, 1920x1080@60, 0x0, 1
monitor = HDMI-A-1, 2560x1440@144, 1920x0, 1
```

List monitors: `hyprctl monitors`

### Screenshots

- `omarchy-cmd-screenshot` - Interactive screenshot
- `omarchy-cmd-screenrecord` - Toggle screen recording

### System

```bash
omarchy-update                  # Full system update
omarchy-version                 # Show Omarchy version
omarchy-debug                   # Debug info for troubleshooting
omarchy-lock-screen             # Lock screen
omarchy-cmd-shutdown            # Shutdown
omarchy-cmd-reboot              # Reboot
```

## Fonts

```bash
omarchy-font-list               # Available fonts
omarchy-font-current            # Current font
omarchy-font-set <name>         # Change font
```

## Troubleshooting

```bash
# Check Omarchy state
omarchy-state

# Debug information
omarchy-debug

# Upload logs for support
omarchy-upload-log

# Reset specific config to defaults
omarchy-refresh-<app>

# Full reinstall (nuclear option)
omarchy-reinstall
```

## Omarchy Manual

**IMPORTANT:** For general "how do I" questions, ALWAYS fetch the relevant manual page BEFORE answering. The manual at `https://learn.omacom.io` contains Omarchy-specific guidance that may differ from generic Linux advice.

### When to Fetch the Manual

**Always fetch first** when users ask:
- "How do I..." / "What is..." / "Why does..." questions
- Questions about installing/running software (Windows, games, apps)
- Questions about concepts, workflows, or best practices
- Topics where Omarchy may have a specific approach

### Manual Index

**Match the user's question to topic(s) below and fetch the page(s) before responding:**

| Topic | Keywords | URL |
|-------|----------|-----|
| Welcome / Overview | what is omarchy, introduction, about | `/2/the-omarchy-manual/91/welcome-to-omarchy` |
| Getting Started | install, installation, setup, ISO, new user | `/2/the-omarchy-manual/50/getting-started` |
| Navigation | tiling, workspaces, move, resize, focus, window management | `/2/the-omarchy-manual/51/navigation` |
| Themes | theme, appearance, colors, look, style | `/2/the-omarchy-manual/52/themes` |
| Extra Themes | community themes, more themes, additional themes | `/2/the-omarchy-manual/90/extra-themes` |
| Making Themes | create theme, custom theme, theme development | `/2/the-omarchy-manual/92/making-your-own-theme` |
| Hotkeys | keybindings, shortcuts, keyboard, hotkey reference | `/2/the-omarchy-manual/53/hotkeys` |
| PDFs | pdf, forms, documents, xournal | `/2/the-omarchy-manual/54/filling-out-pdfs` |
| Applications | apps, software, included, default apps | `/2/the-omarchy-manual/55/the-applications` |
| Neovim | neovim, nvim, vim, editor | `/2/the-omarchy-manual/56/neovim` |
| Shell Tools | fzf, zoxide, ripgrep, rg, search | `/2/the-omarchy-manual/57/shell-tools` |
| Shell Functions | compress, format, convert, shell utilities | `/2/the-omarchy-manual/58/shell-functions` |
| TUIs | lazygit, lazydocker, btop, terminal ui | `/2/the-omarchy-manual/59/tuis` |
| GUIs | obsidian, pinta, localsend, graphical apps | `/2/the-omarchy-manual/60/guis` |
| Commercial GUIs | 1password, typora, paid apps | `/2/the-omarchy-manual/61/commercial-guis` |
| Development Tools | dev, programming, coding, ide | `/2/the-omarchy-manual/62/development-tools` |
| Web Apps | web app, pwa, browser apps | `/2/the-omarchy-manual/63/web-apps` |
| Configuration | config, customize, settings | `/2/the-omarchy-manual/64/configuration` |
| Dotfiles | dotfiles, .config, config files | `/2/the-omarchy-manual/65/dotfiles` |
| Other Packages | pacman, yay, aur, arch packages | `/2/the-omarchy-manual/66/other-packages` |
| FAQ | faq, questions, common issues | `/2/the-omarchy-manual/67/faq` |
| Updates | update, upgrade, system update | `/2/the-omarchy-manual/68/updates` |
| Gaming | games, steam, retroarch, gaming | `/2/the-omarchy-manual/71/gaming` |
| Troubleshooting | problem, issue, fix, broken, not working | `/2/the-omarchy-manual/88/troubleshooting` |
| Backgrounds | wallpaper, background, custom wallpaper | `/2/the-omarchy-manual/89/backgrounds` |
| Security | encryption, firewall, security, luks | `/2/the-omarchy-manual/93/security` |
| Fonts | font, typeface, typography | `/2/the-omarchy-manual/94/fonts` |
| Prompt | starship, prompt, terminal prompt | `/2/the-omarchy-manual/95/prompt` |
| Manual Installation | manual install, arch install, step by step | `/2/the-omarchy-manual/96/manual-installation` |
| Mac Support | mac, macbook, intel mac, apple | `/2/the-omarchy-manual/97/mac-support` |
| Windows VM | windows, run windows, install windows, vm, virtual machine, microsoft | `/2/the-omarchy-manual/100/windows-vm` |
| System Snapshots | snapshot, backup, restore, timeshift | `/2/the-omarchy-manual/101/system-snapshots` |
| Common Tweaks | tweak, customize, adjust, modify | `/2/the-omarchy-manual/102/common-tweaks` |
| Input Devices | keyboard, mouse, trackpad, touchpad, input | `/2/the-omarchy-manual/78/keyboard-mouse-trackpad` |
| Fingerprint / Fido2 | fingerprint, fido, yubikey, biometric | `/2/the-omarchy-manual/77/fingerprint-fido2-authentication` |
| Monitors | monitor, display, screen, resolution, scaling | `/2/the-omarchy-manual/86/monitors` |
| Running Omarchy | vm, virtualbox, vmware, platforms | `/2/the-omarchy-manual/79/omarchy-on` |

### Fetching Manual Pages

When a user asks a general question:

1. **Identify relevant topic(s)** from the index above
2. **Fetch the page** using WebFetch with the full URL:
   ```
   https://learn.omacom.io<path>
   ```
3. **Extract the answer** from the page content
4. **Summarize** the relevant information for the user

**Examples:**
- "How do I set up my fingerprint reader?" → Fetch `/2/the-omarchy-manual/77/fingerprint-fido2-authentication`
- "How do I install Windows on Omarchy?" → Fetch `/2/the-omarchy-manual/100/windows-vm`
- "How do I install Steam?" → Fetch `/2/the-omarchy-manual/71/gaming`

## Example Requests

- "Change my theme to catppuccin"
- "Add a keybinding for Super+E to open file manager"
- "Configure my external monitor"
- "Make the window gaps smaller"
- "Set up night light to turn on at sunset"
- "Show me what omarchy commands are available for bluetooth"
- "Increase waybar height"
- "Change my terminal font"
- "How do I install Steam?"
- "How do I install Windows on Omarchy?"
- "What keyboard shortcuts are available?"
- "How do I set up my fingerprint reader?"
