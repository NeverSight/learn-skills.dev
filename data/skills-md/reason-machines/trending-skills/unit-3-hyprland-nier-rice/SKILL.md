---
name: unit-3-hyprland-nier-rice
description: NieR:Automata themed Hyprland + Quickshell + Waybar rice for Arch Linux with QML widgets
triggers:
  - set up unit-3 rice
  - configure hyprland nier automata theme
  - install unit-3 dotfiles
  - customize quickshell widgets
  - add keybinds to unit-3 hyprland
  - unit-3 waybar configuration
  - nier automata linux desktop rice
  - unit-3 quickshell QML setup
---

# Unit-3 Hyprland NieR:Automata Rice

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Unit-3 is a fully themed Arch Linux desktop rice combining Hyprland (Wayland compositor), Quickshell (QML-based widget system), and Waybar into a cohesive NieR:Automata aesthetic. It includes custom QML widgets for an app menu, lockscreen, wallpaper picker, notifications, and media player.

---

## Installation

### Quick Install (Recommended)

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/samyns/Unit-3/main/install.sh)
```

### Manual Clone

```bash
git clone https://github.com/samyns/Unit-3.git
cd Unit-3
bash install.sh
```

The installer sets up:
- Hyprland config in `~/.config/hypr/`
- Quickshell widgets in `~/.config/quickshell/`
- Waybar config in `~/.config/waybar/`
- Kitty terminal config

---

## Directory Structure

```
Unit-3/
├── install.sh
├── .config/
│   ├── hypr/
│   │   ├── hyprland.conf       # Main Hyprland config
│   │   └── user.conf           # User overrides (never overwritten)
│   ├── quickshell/
│   │   └── *.qml               # Quickshell QML widget files
│   └── waybar/
│       ├── config              # Waybar modules config
│       └── style.css           # Waybar NieR-themed styles
```

---

## User Configuration (Never Overwritten)

All personal overrides go in `~/.config/hypr/user.conf`. This file is safe from updates.

```conf
# ~/.config/hypr/user.conf

# Monitor setup
monitor = DP-1, 2560x1440@144, 0x0, 1
monitor = HDMI-A-1, 1920x1080@60, 2560x0, 1

# Input layout
input {
    kb_layout = us
    kb_variant = 
    follow_mouse = 1
    sensitivity = 0
}

# Custom keybinds
bind = SUPER, B, exec, firefox
bind = SUPER, E, exec, nautilus
bind = SUPER, M, exec, spotify

# Environment variables
env = XCURSOR_SIZE, 24
env = GTK_THEME, NieR
```

---

## Keybinds Reference

| Key | Action |
|-----|--------|
| `SUPER` (tap) | Open app menu |
| `SUPER + L` | Lockscreen |
| `SUPER + T` | Terminal (kitty) |
| `SUPER + Return` | Toggle Quickshell player |
| `SUPER + P` | Wallpaper picker |
| `SUPER + Q` | Close window |
| `SUPER + F` | Fullscreen toggle |
| `ALT + Tab` | Cycle windows |
| `ALT + 1/2/3...` | Switch workspace |
| `Print` | Screenshot |
| `ALT + SHIFT + S` | Region screenshot |

---

## QML Widget Development

Quickshell widgets are written in QML. Unit-3 widgets follow a NieR aesthetic with dark backgrounds and angular UI elements.

### Basic Quickshell Widget Structure

```qml
// ~/.config/quickshell/MyWidget.qml
import Quickshell
import Quickshell.Io
import QtQuick
import QtQuick.Controls

ShellRoot {
    // Panels are screen-anchored overlays
    PanelWindow {
        id: myPanel
        anchors {
            top: true
            left: true
            right: true
        }
        height: 40
        color: "transparent"

        Rectangle {
            anchors.fill: parent
            color: "#1a1a1a"
            border.color: "#c8a951"  // NieR gold accent
            border.width: 1

            Text {
                anchors.centerIn: parent
                text: "Unit-3"
                color: "#e8d5a3"
                font.family: "monospace"
                font.pixelSize: 14
            }
        }
    }
}
```

### Notification Widget Pattern

```qml
// Notification popup following NieR style
import Quickshell
import Quickshell.Services.Notifications
import QtQuick

ShellRoot {
    NotificationServer {
        id: notifServer
    }

    Variants {
        model: notifServer.trackedNotifications

        PanelWindow {
            required property var modelData
            property var notification: modelData

            anchors {
                top: true
                right: true
            }
            margins.top: 10
            margins.right: 10

            width: 320
            height: 80
            color: "transparent"

            Rectangle {
                anchors.fill: parent
                color: "#101418"
                border.color: "#c8a951"
                border.width: 1
                radius: 2

                Column {
                    anchors {
                        left: parent.left
                        verticalCenter: parent.verticalCenter
                        leftMargin: 16
                    }
                    spacing: 4

                    Text {
                        text: notification.summary
                        color: "#c8a951"
                        font.pixelSize: 13
                        font.bold: true
                    }
                    Text {
                        text: notification.body
                        color: "#9a9a8a"
                        font.pixelSize: 11
                    }
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: notification.dismiss()
                }
            }

            // Auto-dismiss timer
            Timer {
                interval: 5000
                running: true
                onTriggered: notification.dismiss()
            }
        }
    }
}
```

### Media Player Widget Pattern

```qml
// ~/.config/quickshell/Player.qml
import Quickshell
import Quickshell.Services.Mpris
import QtQuick
import QtQuick.Controls

ShellRoot {
    FloatingWindow {
        id: playerWindow
        visible: false  // toggled by SUPER + Return

        width: 340
        height: 100
        color: "transparent"

        Rectangle {
            anchors.fill: parent
            color: "#0d1117"
            border.color: "#c8a951"
            border.width: 1

            Row {
                anchors {
                    left: parent.left
                    verticalCenter: parent.verticalCenter
                    leftMargin: 12
                }
                spacing: 12

                // Album art
                Rectangle {
                    width: 64
                    height: 64
                    color: "#1a1a1a"
                    border.color: "#c8a951"
                    border.width: 1

                    Image {
                        anchors.fill: parent
                        source: MprisController.currentPlayer?.trackArtUrl ?? ""
                        fillMode: Image.PreserveAspectCrop
                    }
                }

                Column {
                    anchors.verticalCenter: parent.verticalCenter
                    spacing: 4

                    Text {
                        text: MprisController.currentPlayer?.trackTitle ?? "No media"
                        color: "#e8d5a3"
                        font.pixelSize: 13
                        font.bold: true
                        elide: Text.ElideRight
                        width: 220
                    }
                    Text {
                        text: MprisController.currentPlayer?.trackArtist ?? ""
                        color: "#9a9a8a"
                        font.pixelSize: 11
                    }

                    // Playback controls
                    Row {
                        spacing: 8
                        Repeater {
                            model: ["⏮", "⏯", "⏭"]
                            Text {
                                text: modelData
                                color: "#c8a951"
                                font.pixelSize: 16
                                MouseArea {
                                    anchors.fill: parent
                                    onClicked: {
                                        if (index === 0) MprisController.currentPlayer?.previous()
                                        else if (index === 1) MprisController.currentPlayer?.playPause()
                                        else MprisController.currentPlayer?.next()
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
```

### Wallpaper Picker Widget

```qml
// ~/.config/quickshell/WallpaperPicker.qml
import Quickshell
import Quickshell.Io
import QtQuick
import QtQuick.Layouts

ShellRoot {
    property string wallpaperDir: "/home/" + Qt.application.name + "/Pictures/Wallpapers"

    FloatingWindow {
        id: pickerWindow
        width: 800
        height: 500

        Rectangle {
            anchors.fill: parent
            color: "#0d1117"
            border.color: "#c8a951"
            border.width: 1

            GridView {
                anchors {
                    fill: parent
                    margins: 16
                }
                cellWidth: 180
                cellHeight: 120

                model: FileView {
                    path: wallpaperDir
                    nameFilters: ["*.jpg", "*.png", "*.webp"]
                }

                delegate: Rectangle {
                    width: 172
                    height: 112
                    color: "#1a1a1a"
                    border.color: mouseArea.containsMouse ? "#c8a951" : "transparent"
                    border.width: 2

                    Image {
                        anchors.fill: parent
                        anchors.margins: 2
                        source: "file://" + model.filePath
                        fillMode: Image.PreserveAspectCrop
                    }

                    MouseArea {
                        id: mouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: {
                            // Set wallpaper via swww
                            Process.exec(["swww", "img", model.filePath,
                                          "--transition-type", "wipe",
                                          "--transition-angle", "30"])
                            pickerWindow.visible = false
                        }
                    }
                }
            }
        }
    }
}
```

---

## Waybar Configuration Pattern

```jsonc
// ~/.config/waybar/config (NieR modules example)
{
    "layer": "top",
    "position": "top",
    "height": 32,
    "modules-left": ["hyprland/workspaces", "hyprland/window"],
    "modules-center": ["clock"],
    "modules-right": ["pulseaudio", "network", "battery", "tray"],

    "hyprland/workspaces": {
        "format": "{id}",
        "on-click": "activate"
    },

    "clock": {
        "format": "{:%H:%M}",
        "format-alt": "{:%Y-%m-%d %H:%M:%S}",
        "tooltip-format": "<big>{:%Y %B}</big>\n<tt>{calendar}</tt>"
    },

    "network": {
        "format-wifi": "  {essid}",
        "format-ethernet": "  {ipaddr}",
        "format-disconnected": "  disconnected",
        "tooltip-format": "{ifname}: {ipaddr}"
    },

    "pulseaudio": {
        "format": " {volume}%",
        "format-muted": " muted",
        "on-click": "pavucontrol"
    }
}
```

```css
/* ~/.config/waybar/style.css — NieR color palette */
* {
    font-family: "monospace";
    font-size: 13px;
}

window#waybar {
    background: rgba(13, 17, 23, 0.92);
    border-bottom: 1px solid #c8a951;
    color: #e8d5a3;
}

#workspaces button {
    color: #9a9a8a;
    border-radius: 0;
    padding: 0 8px;
    border-bottom: 2px solid transparent;
}

#workspaces button.active {
    color: #c8a951;
    border-bottom: 2px solid #c8a951;
}

#clock {
    color: #c8a951;
    font-weight: bold;
    letter-spacing: 2px;
}

#network, #pulseaudio, #battery {
    color: #e8d5a3;
    padding: 0 12px;
}
```

---

## Hyprland Config Patterns

```conf
# ~/.config/hypr/hyprland.conf (snippet)

# NieR-style animations
animations {
    enabled = true
    bezier = nier, 0.05, 0.9, 0.1, 1.0
    animation = windows, 1, 4, nier, slide
    animation = fade, 1, 4, nier
    animation = workspaces, 1, 5, nier, slidevert
}

# Minimal decorations for NieR aesthetic
decoration {
    rounding = 0
    blur {
        enabled = true
        size = 4
        passes = 2
        noise = 0.02
        contrast = 1.0
        brightness = 0.9
    }
    drop_shadow = true
    shadow_color = rgba(200, 169, 81, 0.4)
    shadow_range = 8
}

# Window gaps
general {
    gaps_in = 4
    gaps_out = 8
    border_size = 1
    col.active_border = rgba(c8a951ff)
    col.inactive_border = rgba(2a2a2aff)
}
```

---

## Troubleshooting

### Quickshell widgets not appearing
```bash
# Check if quickshell is running
pgrep -a quickshell

# Restart quickshell
pkill quickshell && quickshell &

# Check logs for QML errors
quickshell 2>&1 | grep -i error
```

### Waybar not loading
```bash
# Validate config syntax
waybar --log-level debug

# Reload waybar
pkill waybar && waybar &

# Check config location
ls ~/.config/waybar/
```

### Hyprland keybinds not working
```bash
# Check active config
hyprctl activewindow
hyprctl getoption general:border_size

# Reload config live
hyprctl reload

# Verify user.conf is sourced
grep "user.conf" ~/.config/hypr/hyprland.conf
```

### Wallpaper not setting (swww)
```bash
# Initialize swww daemon first
swww-daemon &

# Then set wallpaper
swww img ~/Pictures/wall.jpg --transition-type wipe
```

### Wrong monitor layout
```conf
# ~/.config/hypr/user.conf
# List available monitors first:
# hyprctl monitors

monitor = DP-1, 2560x1440@144, 0x0, 1
monitor = HDMI-A-1, 1920x1080@60, 2560x0, 1
```

---

## NieR Color Palette Reference

| Name | Hex | Usage |
|------|-----|-------|
| Gold accent | `#c8a951` | Borders, active elements |
| Light text | `#e8d5a3` | Primary text |
| Dim text | `#9a9a8a` | Secondary text |
| Background | `#0d1117` | Main background |
| Surface | `#101418` | Widget backgrounds |
| Dark surface | `#1a1a1a` | Inset elements |

---

## Updating the Rice

```bash
cd ~/Unit-3   # or wherever you cloned it
git pull
bash install.sh   # re-runs installer; user.conf is preserved
```
