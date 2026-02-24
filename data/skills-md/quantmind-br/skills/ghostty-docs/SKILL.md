---
name: ghostty-docs
description: |
  Ghostty - Fast, feature-rich, cross-platform terminal emulator with GPU acceleration and native UI.
  Use when configuring Ghostty terminal, customizing keybindings, theming, shell integration, or working with VT/ANSI escape sequences and control codes.
  Keywords: ghostty, terminal-emulator, gpu-acceleration, configuration, keybindings, themes, shell-integration, escape-sequences, vt-sequences, csi, osc, control-sequences, cursor, colors, cross-platform.
compatibility: Ghostty runs on macOS and Linux. Install via Homebrew (macOS), package managers (Linux), or build from source with Zig compiler.
metadata:
  source: https://ghostty.org/
  total_docs: 79
  generated: 2026-02-11
---

# Ghostty

> Ghostty is a fast, feature-rich, and cross-platform terminal emulator that uses platform-native UI and GPU acceleration. It differentiates itself by being fast, feature-rich, and native — without forcing you to choose between the three.

## Quick Start

```bash
# macOS (Homebrew)
brew install --cask ghostty

# Configuration file location
# macOS: ~/.config/ghostty/config  OR  ~/Library/Application Support/com.mitchellh.ghostty/config
# Linux: ~/.config/ghostty/config

# Example minimal config
cat > ~/.config/ghostty/config << 'EOF'
theme = Catppuccin Frappe
font-family = JetBrains Mono
font-size = 14
keybind = ctrl+shift+t=new_tab
keybind = ctrl+shift+n=new_window
EOF
```

## Installation

```bash
# macOS - Official DMG from https://ghostty.org/download or:
brew install --cask ghostty

# Arch Linux
pacman -S ghostty

# NixOS
environment.systemPackages = [ pkgs.ghostty ];

# Alpine Linux
apk add ghostty

# openSUSE
zypper install ghostty

# Snap
snap install ghostty --classic

# Void Linux
xbps-install ghostty

# Build from source (any platform)
# See docs/006-docs-install-build.md
```

## Documentation

Comprehensive documentation in `docs/`. Consult `docs/000-index.md` for detailed navigation.

### By Topic

| Topic | Files | Description |
|-------|-------|-------------|
| Introduction | 001-003 | Project overview and documentation index |
| Installation | 004-007 | Install methods: prebuilt, binaries, source, packaging |
| Features | 008-010 | Core features, themes, shell integration |
| Configuration | 011-015 | Config syntax, keybindings, full option reference |
| VT Sequences Overview | 016 | Terminal API introduction |
| VT Concepts | 017-020 | Screen, cursor, colors, sequences fundamentals |
| VT Control Characters | 021-025 | BEL, BS, CR, LF, TAB |
| VT ESC Sequences | 026-034 | Index, keypad modes, cursor save/restore, reset |
| VT CSI Sequences | 035-062 | Cursor movement, scrolling, editing, margins |
| VT OSC Sequences | 063-076 | Colors, titles, clipboard, notifications |
| VT Reference | 077-078 | Full sequence reference, external protocols |

### By Keyword

| Keyword | File |
|---------|------|
| configuration | `011-docs-config.md` |
| config-syntax | `011-docs-config.md` |
| config-reference | `015-docs-config-reference.md` |
| font-family | `015-docs-config-reference.md` |
| font-size | `015-docs-config-reference.md` |
| font-features | `015-docs-config-reference.md` |
| theme | `009-docs-features-theme.md` |
| color-schemes | `009-docs-features-theme.md`, `017-docs-vt-concepts-colors.md` |
| light-dark-mode | `009-docs-features-theme.md` |
| keybindings | `012-docs-config-keybind.md` |
| keybind-actions | `014-docs-config-keybind-reference.md` |
| key-sequences | `013-docs-config-keybind-sequence.md` |
| shell-integration | `010-docs-features-shell-integration.md` |
| bash | `010-docs-features-shell-integration.md` |
| zsh | `010-docs-features-shell-integration.md` |
| fish | `010-docs-features-shell-integration.md` |
| installation | `005-docs-install-binary.md` |
| homebrew | `005-docs-install-binary.md` |
| build-from-source | `006-docs-install-build.md` |
| prerelease | `004-docs-install-pre.md` |
| gpu-acceleration | `002-docs-about.md`, `008-docs-features.md` |
| cross-platform | `002-docs-about.md`, `008-docs-features.md` |
| native-ui | `002-docs-about.md` |
| libghostty | `002-docs-about.md` |
| zig | `002-docs-about.md` |
| terminal-features | `008-docs-features.md` |
| cursor-movement | `035-062` (CSI sequences) |
| cursor-style | `057-docs-vt-csi-decscusr.md` |
| cursor-positioning | `041-docs-vt-csi-cup.md` |
| scrolling | `055-docs-vt-csi-sd.md`, `056-docs-vt-csi-su.md` |
| scroll-region | `059-docs-vt-csi-decstbm.md` |
| scroll-margins | `058-docs-vt-csi-decslrm.md` |
| clipboard | `069-docs-vt-osc-52.md` |
| window-title | `065-docs-vt-osc-0.md`, `066-docs-vt-osc-2.md` |
| dynamic-colors | `070-docs-vt-osc-1x.md`, `073-docs-vt-osc-11x.md` |
| color-palette | `071-docs-vt-osc-4.md`, `074-docs-vt-osc-104.md` |
| desktop-notification | `076-docs-vt-osc-9.md` |
| escape-sequences | `018-docs-vt-concepts-sequences.md` |
| control-sequences | `016-docs-vt.md`, `018-docs-vt-concepts-sequences.md` |
| terminal-colors | `017-docs-vt-concepts-colors.md` |
| terminal-cursor | `019-docs-vt-concepts-cursor.md` |
| screen-buffer | `020-docs-vt-concepts-screen.md` |
| erase-display | `048-docs-vt-csi-ed.md` |
| erase-line | `049-docs-vt-csi-el.md` |
| mouse-reporting | `034-docs-vt-csi-xtshiftescape.md` |
| vt-reference | `078-docs-vt-reference.md` |
| external-protocols | `077-docs-vt-external.md` |
| background-opacity | `015-docs-config-reference.md` |
| splits | `015-docs-config-reference.md` |
| tabs | `008-docs-features.md` |
| quick-terminal | `008-docs-features.md` |
| kitty-graphics | `008-docs-features.md` |
| packaging | `007-docs-install-package.md` |
| sponsor | `079-docs-sponsor.md` |
| conemu | `068-docs-vt-osc-conemu.md` |
| working-directory | `067-docs-vt-osc-7.md` |
| pointer-shape | `063-docs-vt-osc-22.md` |

### Learning Path

1. **Foundation** - Read `001-003` for project intro, then `004-007` for installation
2. **Core Configuration** - Learn features (`008-010`: theming, shell integration), then master config (`011-015`)
3. **Terminal API Fundamentals** - VT intro (`016`), concepts (`017-020`: screen, cursor, colors, sequences)
4. **Control Sequences** - Control chars (`021-025`), ESC (`026-034`), CSI (`035-062`), OSC (`063-076`)
5. **Reference** - Complete VT reference (`077-078`)

## Common Tasks

### Install Ghostty
-> `docs/005-docs-install-binary.md` (macOS, Linux packages, Homebrew, Nix)

### Configure Ghostty
-> `docs/011-docs-config.md` (config file location, syntax, reloading)

### Set a Theme
-> `docs/009-docs-features-theme.md` (built-in themes, light/dark mode, custom themes)

### Customize Keybindings
-> `docs/012-docs-config-keybind.md` (trigger syntax, modifiers, actions)

### Set Up Shell Integration
-> `docs/010-docs-features-shell-integration.md` (bash/zsh/fish/elvish, prompt navigation, working directory)

### Customize Fonts
-> `docs/015-docs-config-reference.md` (font-family, font-size, font-features, ligatures)

### Configure Background Opacity / Blur
-> `docs/015-docs-config-reference.md` (background-opacity, background-blur)

### Use VT Escape Sequences
-> `docs/018-docs-vt-concepts-sequences.md` (sequence types, syntax, CSI/OSC/ESC formats)

### Look Up All Config Options
-> `docs/015-docs-config-reference.md` (comprehensive option reference)

### Look Up All Keybind Actions
-> `docs/014-docs-config-keybind-reference.md` (complete action reference)
