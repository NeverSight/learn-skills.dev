---
name: quickshell
description: >
  Build, debug, and extend QuickShell configs — QML-based desktop shell/widget framework for Linux Wayland compositors.
  USE FOR: writing shell.qml configs, bars, panels, popups, widgets, process runners, IPC, Hyprland/Wayland integration,
  notifications, system tray, media controls (MPRIS), audio (PipeWire), power (UPower), multi-monitor layouts, singletons,
  Scope modules, IpcHandler, PersistentProperties, Connections, inline components, typed QML functions.
  DO NOT USE FOR: generic QML/Qt app development unrelated to desktop shells, non-Linux platforms.
---

# QuickShell

QuickShell is a QML-based framework for building custom desktop shells — bars, panels, popups, widgets — on Linux Wayland compositors. Configs are pure QML files; no build system required.

## When to Use

- User wants to create or modify a QuickShell `shell.qml` config
- User needs help with services, Hyprland, Wayland, MPRIS, notifications, system tray, PipeWire, or UPower
- User wants to spawn processes, parse output, do IPC, or persist state across reloads
- User asks about any type from the `Quickshell.*` module namespace

## When Not to Use

- User is building a standalone Qt application (not a shell/bar/widget)
- User is on X11 only with no Wayland layer shell support
- User is asking about a different shell framework (AGS, Waybar, eww, etc.)

---

## Config Setup

| Item | Detail |
|------|--------|
| Entry point | `~/.config/quickshell/shell.qml` (or named subfolder: `~/.config/quickshell/<name>/shell.qml`) |
| Run default config | `quickshell` |
| Run named config | `quickshell -c <name>` |
| Run arbitrary file | `quickshell -p /path/to/shell.qml` |
| Reload running instance | `quickshell --reload` |
| LSP support | Create empty `.qmlls.ini` next to `shell.qml`; QuickShell auto-fills it |
| Set env vars in config | `//@ pragma Env VAR=value` at the top of `shell.qml` |
| Enable platform menus | `//@ pragma UseQApplication` at the top of `shell.qml` — **required** for `QsMenuAnchor.open()` (system tray context menus, right-click menus). Restart QuickShell after adding; `--reload` is not enough. |

---

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Goal or existing QML snippet | Yes | What the user wants to build or fix |
| Compositor | No | Hyprland, generic Wayland, etc. — determines which modules to import |
| Target monitor | No | Single vs. multi-monitor affects whether to use `Variants` |

---

## Core Concepts

### shell.qml entry point

```qml
//@ pragma Env QSG_RENDER_LOOP=threaded

import "modules"
import "services"
import Quickshell

ShellRoot {
    Background {}
    Bar {}
    Notifications {}
    Shortcuts {}
    BatteryMonitor {}
}
```

`ShellRoot` is the root element. Child elements are typically `Scope`-based modules or window types.

### PanelWindow — anchored bar/panel

```qml
import Quickshell
import QtQuick

PanelWindow {
    anchors { top: true; left: true; right: true }
    implicitHeight: 30

    Text {
        anchors.centerIn: parent
        text: "hello world"
        color: "white"
    }
}
```

### Multi-monitor with Variants

Spawn one instance per screen. Instances appear/disappear automatically as monitors connect/disconnect.

```qml
import Quickshell

Variants {
    model: Quickshell.screens

    PanelWindow {
        required property ShellScreen modelData
        screen: modelData

        anchors { top: true; left: true; right: true }
        implicitHeight: 30
    }
}
```

### Singleton — global shared service

Add `pragma Singleton` to a capitalized `.qml` file. Access it by filename from anywhere in the config.
The root element must be `Singleton {}`, not `QtObject` or `Item`.

```qml
// services/Audio.qml
pragma Singleton

import Quickshell
import Quickshell.Services.Pipewire

Singleton {
    id: root

    readonly property PwNode sink: Pipewire.defaultAudioSink
    readonly property bool muted: !!sink?.audio?.muted
    readonly property real volume: sink?.audio?.volume ?? 0

    function setVolume(newVolume: real): void {
        if (sink?.ready && sink?.audio)
            sink.audio.volume = Math.max(0, Math.min(1.0, newVolume));
    }
}
```

### Scope — non-singleton module

Use `Scope` (not `Singleton`) for modules that don't need global access, or that are instantiated per context (e.g., keyboard shortcuts, battery watchers). Scope participates in the reload graph but is not globally addressable.

```qml
// modules/BatteryMonitor.qml
import Quickshell
import Quickshell.Services.UPower
import QtQuick

Scope {
    Connections {
        target: UPower

        function onOnBatteryChanged(): void {
            if (UPower.onBattery)
                console.log("Charger unplugged")
        }
    }

    Timer {
        id: hibernateTimer
        interval: 5000
        onTriggered: Quickshell.execDetached(["systemctl", "hibernate"])
    }
}
```

### pragma ComponentBehavior: Bound

**Always add this pragma when a file uses `component` definitions or signal handlers inside nested components.** Without it, inner `component` blocks cannot reliably access outer `id` references or required properties.

```qml
pragma Singleton
pragma ComponentBehavior: Bound

import Quickshell
import QtQuick

Singleton {
    id: root

    component Notif: QtObject {
        required property string summary
        // Can safely reference `root` here because of ComponentBehavior: Bound
        function close(): void {
            root.list = root.list.filter(n => n !== this);
            destroy();
        }
    }
}
```

---

## Typed Functions and Properties

QuickShell uses QML 6 — always annotate function parameters and return types:

```qml
function setVolume(newVolume: real): void { ... }
function getStreamVolume(stream: PwNode): real { return stream?.audio?.volume ?? 0 }
function getStreamName(stream: PwNode): string { return stream?.name ?? "Unknown" }
function isDndEnabled(): bool { return props.dnd }
function cycleWorkspace(direction: string): void { ... }
```

Typed property declarations:

```qml
readonly property PwNode sink: Pipewire.defaultAudioSink
readonly property list<PwNode> sinks: nodes.sinks
property list<Notif> list: []
readonly property HyprlandMonitor focusedMonitor: Hyprland.focusedMonitor
```

---

## Null Safety

Use `?.` (optional chaining) and `??` (null coalescing) freely — they are idiomatic in QuickShell code:

```qml
readonly property bool muted: !!sink?.audio?.muted      // double-! coerces to bool
readonly property real volume: sink?.audio?.volume ?? 0
readonly property string layout: keyboard?.activeKeymap ?? "Unknown"
readonly property int activeWsId: focusedWorkspace?.id ?? 1
```

---

## Connections

`Connections` is the primary way to react to signals on external objects. Use the `function onXxx()` syntax (not the old `onXxx:` property syntax):

```qml
Connections {
    target: Hyprland

    function onRawEvent(event: HyprlandEvent): void {
        if (event.name === "configreloaded")
            root.reload();
        else if (["openwindow", "closewindow"].includes(event.name))
            Hyprland.refreshToplevels();
    }
}

Connections {
    target: UPower.displayDevice

    function onPercentageChanged(): void {
        const p = UPower.displayDevice.percentage * 100;
        if (p <= 10) console.warn("Battery critical:", p);
    }
}
```

Multiple `Connections` blocks in one file are fine and common.

---

## Readonly Properties with Complex Expressions

Use JS array methods directly in `readonly property` bindings:

```qml
// Partition Pipewire nodes into sinks, sources, and streams
readonly property var nodes: Pipewire.nodes.values.reduce((acc, node) => {
    if (!node.isStream) {
        if (node.isSink) acc.sinks.push(node);
        else if (node.audio) acc.sources.push(node);
    } else if (node.audio) {
        acc.streams.push(node);
    }
    return acc;
}, { sinks: [], sources: [], streams: [] })

readonly property list<PwNode> sinks: nodes.sinks

// Find active network access point
readonly property AccessPoint active: networks.find(n => n.active) ?? null

// Filter only open special workspaces
readonly property var openSpecials: workspaces.values
    .filter(w => w.name.startsWith("special:") && w.lastIpcObject.windows > 0)
```

---

## Inline Components

Define reusable local types inside a file using `component`. Requires `pragma ComponentBehavior: Bound`.

```qml
pragma Singleton
pragma ComponentBehavior: Bound

import Quickshell
import Quickshell.Services.Notifications
import QtQuick

Singleton {
    id: root

    property list<Notif> list: []
    readonly property list<Notif> popups: list.filter(n => n.popup)

    component Notif: QtObject {
        property bool popup
        property bool closed
        property string summary
        property string body
        property int urgency
        property var locks: new Set()

        function close(): void {
            closed = true;
            if (locks.size === 0) {
                root.list = root.list.filter(n => n !== this);
                destroy();
            }
        }
    }

    Component { id: notifComp; Notif {} }

    NotificationServer {
        onNotification: notif => {
            const obj = notifComp.createObject(root, {
                summary: notif.summary,
                body: notif.body,
                popup: true
            });
            root.list = [obj, ...root.list];
        }
    }
}
```

---

## IpcHandler — CLI control

Expose functions to external tools via `qs ipc call <target> <function> [args...]`.
Return types matter: use `string`, `bool`, `real`, or `void`.

```qml
IpcHandler {
    target: "audio"

    function getVolume(): real { return Audio.volume }
    function setVolume(v: real): void { Audio.setVolume(v) }
    function toggleMute(): void {
        if (Audio.sink?.audio)
            Audio.sink.audio.muted = !Audio.sink.audio.muted;
    }
}

IpcHandler {
    target: "notifs"

    function isDndEnabled(): bool { return props.dnd }
    function toggleDnd(): void { props.dnd = !props.dnd }
    function clear(): void {
        for (const n of root.list.slice()) n.close();
    }
    function listActive(): string {
        return root.notClosed.map(n => n.summary).join("\n");
    }
}
```

Call from the terminal:

```bash
qs ipc call audio setVolume 0.5
qs ipc call notifs toggleDnd
qs ipc call notifs isDndEnabled
qs ipc call hypr listSpecialWorkspaces
```

---

## PersistentProperties

Survives config reload. Use `reloadableId` (not `reloadSource`) to key the storage.

```qml
PersistentProperties {
    id: props
    reloadableId: "notifs"

    property bool dnd
    property string lastWorkspace: ""
}
```

Access like any object: `props.dnd`, `props.lastWorkspace = "special:scratch"`.

---

## FileView — reading and writing files

```qml
FileView {
    path: `${Quickshell.configDir}/state/notifs.json`

    onLoaded: {
        const data = JSON.parse(text());
        for (const item of data)
            root.list.push(notifComp.createObject(root, item));
    }

    onLoadFailed: err => {
        if (err === FileViewError.FileNotFound)
            setText("[]");   // initialize empty file
    }
}
```

`setText()` writes back to the file. Use `JsonAdapter` for typed JSON access.

---

## Process — running commands

```qml
import Quickshell.Io

// One-shot: collect full output
Process {
    id: dateProc
    command: ["date", "+%H:%M"]   // always an array, never a plain string
    running: true

    stdout: StdioCollector {
        onStreamFinished: root.timeText = text.trim()
    }
}

// Streaming: line-by-line output
Process {
    command: ["nmcli", "monitor"]
    running: true

    stdout: SplitParser {
        onRead: line => root.handleNmcliLine(line)
    }
}
```

Periodic refresh:

```qml
Timer {
    interval: 60000; repeat: true; running: true
    onTriggered: dateProc.running = true
}
```

---

## LazyLoader — conditional/deferred components

```qml
LazyLoader {
    id: dialogLoader
    active: false   // set true to load, false to unload and destroy

    FloatingWindow {
        // only created when dialogLoader.active = true
    }
}
```

---

## Utility Functions

```qml
// Fire-and-forget (no stdout capture):
Quickshell.execDetached(["systemctl", "hibernate"])
Quickshell.execDetached(["notify-send", "Hello"])

// Read environment variable:
Quickshell.env("XKB_RULES_PATH") || "/usr/share/X11/xkb/rules/base.lst"

// Deferred execution (next event loop tick):
Qt.callLater(() => { root.initialize() })
Qt.callLater(() => { root.sync() }, 100)   // with ms delay
```

---

## Import Structure

Three tiers — always in this order:

```qml
// 1. Local project imports
import "modules"
import qs.services
import qs.config

// 2. Framework/plugin imports (if any)
import Caelestia.Services

// 3. Quickshell + Qt imports
import Quickshell
import Quickshell.Hyprland
import Quickshell.Io
import Quickshell.Services.Pipewire
import QtQuick
import QtQuick.Layouts
```

---

## Module Reference

### `Quickshell` (core)

| Type | Purpose |
|------|---------|
| `ShellRoot` | Root config element; host for all `Scope`/window children |
| `Singleton` | Base type for global singleton services (`pragma Singleton` required) |
| `Scope` | Non-singleton module; participates in reload graph |
| `PanelWindow` | Panel attached to screen edges; reserves screen space |
| `FloatingWindow` | Standard OS window |
| `PopupWindow` | Temporary popup; position with `PopupAnchor` |
| `PopupAnchor` | Anchor spec used by `PopupWindow` / `QsMenuAnchor`; properties: `window`, `item`, `rect`, `edges` (see `Edges`), `gravity`, `adjustment` |
| `Edges` | Flag enum for anchor edges: `Edges.Top`, `Edges.Bottom`, `Edges.Left`, `Edges.Right`. Combinable with `\|` |
| `QsMenuAnchor` | Displays a `QsMenuHandle` (e.g. `SystemTrayItem.menu`) as a platform menu. Set `menu` + `anchor.item`/`anchor.edges`, then call `open()`. Requires `//@ pragma UseQApplication` |
| `QsMenuHandle` | Opaque handle returned by services (tray menus, etc.); cannot be shown directly — pass to a `QsMenuAnchor` |
| `Variants` | Spawns one component instance per model entry |
| `LazyLoader` | Load/unload a component on demand via `active` |
| `BoundComponent` | Component loader with initial properties |
| `PersistentProperties` | State that survives `--reload`; key with `reloadableId` |
| `SystemClock` | System time with configurable `precision` |
| `ElapsedTimer` | Measure time between events |
| `DesktopEntries` | Index of `.desktop` application entries |
| `ColorQuantizer` | Extract palette from an image |
| `ObjectModel` / `ObjectRepeater` | Model/repeater for non-`Item` objects |
| `ScriptModel` | QML model from a JS expression |

### `Quickshell.Io`

| Type | Purpose |
|------|---------|
| `Process` | Spawn child process; `command` must be a string array |
| `SplitParser` | Stream stdout split by delimiter; `onRead: line => ...` |
| `StdioCollector` | Buffer all stdout; `onStreamFinished` fires on exit |
| `FileView` | Read/write small files; `onLoaded`, `onLoadFailed`, `setText()` |
| `JsonAdapter` | Typed JSON access through `FileView` |
| `Socket` / `SocketServer` | Unix domain socket IPC |
| `IpcHandler` | Expose typed functions to `qs ipc call` |

### `Quickshell.Hyprland`

| Type | Purpose |
|------|---------|
| `Hyprland` | Main singleton; `toplevels`, `workspaces`, `monitors`, `activeToplevel`, `focusedWorkspace`, `focusedMonitor` |
| `HyprlandWindow` | Hyprland-specific window properties |
| `HyprlandWorkspace` | Workspace state; `id`, `name`, `lastIpcObject` |
| `HyprlandMonitor` | Monitor state; `lastIpcObject` |
| `HyprlandToplevel` | Top-level surface |
| `HyprlandFocusGrab` | Grab keyboard/mouse focus |
| `GlobalShortcut` | Register a global keybind |
| `HyprlandEvent` | Live IPC event; `name`, `data` |

Refresh methods: `Hyprland.refreshWorkspaces()`, `Hyprland.refreshMonitors()`, `Hyprland.refreshToplevels()`, `Hyprland.dispatch(request)`.

### `Quickshell.Wayland`

| Type | Purpose |
|------|---------|
| `WlrLayershell` | Wlroots layer-shell window |
| `WlrLayer` | `Background`, `Bottom`, `Top`, `Overlay` |
| `WlrKeyboardFocus` | Keyboard focus mode for layer surfaces |
| `ToplevelManager` | List all open windows via foreign-toplevel |
| `Toplevel` | A window from another application |
| `WlSessionLock` / `WlSessionLockSurface` | Lockscreen implementation |
| `ScreencopyView` | Capture and display a window or monitor |

### `Quickshell.Services.Mpris`

| Type | Purpose |
|------|---------|
| `Mpris` | Entry point; `Mpris.players` |
| `MprisPlayer` | `trackTitle`, `trackArtist`, `playbackState`, `play()`, `pause()`, `next()`, `previous()`, `position`, `length` |
| `MprisPlaybackState` | `Playing`, `Paused`, `Stopped` |
| `MprisLoopState` | `None`, `Track`, `Playlist` |

### `Quickshell.Services.Notifications`

| Type | Purpose |
|------|---------|
| `NotificationServer` | Daemon; `onNotification: notif => { }`, `keepOnReload`, `actionsSupported`, etc. |
| `Notification` | `summary`, `body`, `appName`, `appIcon`, `urgency`, `image`, `actions`, `dismiss()` |
| `NotificationAction` | `identifier`, `text`, `invoke()` |
| `NotificationUrgency` | `Low`, `Normal`, `Critical` |
| `NotificationCloseReason` | Why a notification closed |

### `Quickshell.Services.SystemTray`

| Type | Purpose |
|------|---------|
| `SystemTray` | Entry point; `SystemTray.items` |
| `SystemTrayItem` | `icon`, `tooltip`, `title`, `status`, `category`, `hasMenu`, `onlyMenu`, `menu` (→ `QsMenuHandle`), `activate()`, `secondaryActivate()`, `scroll(delta, horizontal)` |
| `Status` | `Active`, `Passive`, `NeedsAttention` |

**Opening a tray item's context menu.** `SystemTrayItem.menu` is a `QsMenuHandle` — calling `.open()` on it directly does nothing. You must display it via a `QsMenuAnchor` (from `Quickshell`). Also requires `//@ pragma UseQApplication` in `shell.qml`.

```qml
pragma ComponentBehavior: Bound
import Quickshell
import Quickshell.Widgets
import Quickshell.Services.SystemTray
import QtQuick

Row {
    QsMenuAnchor { id: menuAnchor }

    Repeater {
        model: SystemTray.items
        delegate: Rectangle {
            id: item
            required property SystemTrayItem modelData
            width: 28; height: 24

            IconImage { anchors.centerIn: parent; source: item.modelData.icon; implicitSize: 16 }

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                acceptedButtons: Qt.LeftButton | Qt.MiddleButton | Qt.RightButton
                onClicked: mouse => {
                    if (mouse.button === Qt.LeftButton) {
                        if (item.modelData.onlyMenu && item.modelData.hasMenu) {
                            menuAnchor.menu = item.modelData.menu
                            menuAnchor.anchor.item = item
                            menuAnchor.anchor.edges = Edges.Bottom
                            menuAnchor.open()
                        } else {
                            item.modelData.activate()
                        }
                    } else if (mouse.button === Qt.MiddleButton) {
                        item.modelData.secondaryActivate()
                    } else if (mouse.button === Qt.RightButton && item.modelData.hasMenu) {
                        menuAnchor.menu = item.modelData.menu
                        menuAnchor.anchor.item = item
                        menuAnchor.anchor.edges = Edges.Bottom
                        menuAnchor.open()
                    }
                }
            }
        }
    }
}
```

Key pieces:
- One shared `QsMenuAnchor` per widget — reassign `menu` and `anchor` on each click.
- `anchor` is a `PopupAnchor`: set `anchor.item` (the clicked delegate) and `anchor.edges` (from the `Edges` enum: `Edges.Top`, `Edges.Bottom`, `Edges.Left`, `Edges.Right`, combinable with `|`).
- Right-click convention opens the menu; left-click usually calls `activate()`. Check `onlyMenu` for icons that have no activate action (e.g. some indicator applets).
- Without `//@ pragma UseQApplication` you get: `Cannot call QsMenuAnchor.open() as quickshell was not started in QApplication mode.`

### `Quickshell.Services.Pipewire`

| Type | Purpose |
|------|---------|
| `Pipewire` | Entry point; `nodes`, `links`, `defaultAudioSink`, `defaultAudioSource`, `preferredDefaultAudioSink` |
| `PwNode` | Audio node; `audio` (→ `PwNodeAudio`), `isSink`, `isStream`, `ready`, `name`, `description`, `applicationName` |
| `PwNodeAudio` | `volume`, `muted`, channels |
| `PwLink` / `PwLinkGroup` | Connection between nodes |
| `PwObjectTracker` | Keep objects alive: `objects: [...sinks, ...sources]` |
| `PwNodeLinkTracker` | Track links to/from a node |

### `Quickshell.Services.UPower`

| Type | Purpose |
|------|---------|
| `UPower` | Singleton; `onBattery`, `displayDevice` |
| `UPower.displayDevice` | `percentage` (0–1), `state`, `timeToEmpty`, `timeToFull` |

### `Quickshell.Widgets`

| Type | Purpose |
|------|---------|
| `IconImage` | Renders XDG theme icons by name |
| `ClippingRectangle` | Rectangle that clips children inside its border radius |
| `WrapperRectangle` / `WrapperItem` | Manages size/position of a single visual child |
| `WrapperMouseArea` | MouseArea wrapping a single visual child |

---

## Workflow

### Step 1: Pick the right root type

| Situation | Root type |
|-----------|-----------|
| Global service accessed by name everywhere | `Singleton {}` with `pragma Singleton` |
| Module that reacts to events but isn't global | `Scope {}` |
| Panel/bar attached to screen edge | `PanelWindow {}` |
| Standard window | `FloatingWindow {}` |
| Multi-monitor instance of anything | `Variants { model: Quickshell.screens }` |

### Step 2: Map goal to modules

| Goal | Module(s) |
|------|-----------|
| Bar / panel | `Quickshell` (`PanelWindow`) |
| Run shell commands | `Quickshell.Io` (`Process`, `StdioCollector`) |
| Workspaces (Hyprland) | `Quickshell.Hyprland` |
| Media controls | `Quickshell.Services.Mpris` |
| Notification popup | `Quickshell.Services.Notifications` |
| System tray | `Quickshell.Services.SystemTray` |
| Volume / audio | `Quickshell.Services.Pipewire` |
| Battery | `Quickshell.Services.UPower` |
| Lockscreen | `Quickshell.Wayland` (`WlSessionLock`) |
| Window list | `Quickshell.Wayland` (`ToplevelManager`) |
| CLI control | `Quickshell.Io` (`IpcHandler`) |
| Persist state across reload | `Quickshell` (`PersistentProperties`) |

### Step 3: Write the QML

- Add `pragma ComponentBehavior: Bound` whenever the file uses `component` definitions
- Annotate all function parameters and return types
- Use `?.` and `??` for nullable Quickshell model objects
- Use `Connections { target: X; function onY() {} }` for all signal reactions
- Extract shared state to `pragma Singleton` files (capitalized names, `Singleton {}` root)
- Use `PersistentProperties` with `reloadableId` for state that must survive `--reload`
- Add `PwObjectTracker { objects: [...] }` when holding Pipewire node references

### Step 4: Reload and test

```bash
quickshell --reload
quickshell -p shell.qml
```

### Step 5: Debug

- QML errors print to stderr — always run from a terminal
- `console.log(...)` / `console.warn(...)` for runtime values
- `qs ipc call <target> <fn>` to exercise IpcHandler functions live

---

## Validation

- [ ] `pragma ComponentBehavior: Bound` present in files that define `component` types
- [ ] All function parameters and return types annotated
- [ ] `?.` / `??` used on all nullable Quickshell model properties
- [ ] Multi-monitor widgets wrapped in `Variants { model: Quickshell.screens }`
- [ ] `Singleton {}` used as root in singleton files (not `QtObject` or `Item`)
- [ ] `PersistentProperties` uses `reloadableId` (not `reloadSource`)
- [ ] `Process.command` is a string array
- [ ] `PwObjectTracker` present when retaining Pipewire node references
- [ ] `quickshell --reload` shows no parse errors

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| `component Foo` can't access outer `id` | Add `pragma ComponentBehavior: Bound` |
| `reloadSource` not found on `PersistentProperties` | Use `reloadableId` |
| Singleton root is `QtObject {}` | Must use `Singleton {}` as root element |
| `command` is a plain string | Must be an array: `["bash", "-c", "..."]` |
| Widget only appears on one monitor | Wrap in `Variants { model: Quickshell.screens }` with `screen: modelData` |
| Pipewire nodes go null/disappear | Add `PwObjectTracker { objects: [...nodes] }` |
| `StdioCollector.text` is empty | Read text in `onStreamFinished`, not right after setting `running: true` |
| No LSP / autocomplete in editor | Create empty `.qmlls.ini` next to `shell.qml` |
| State lost on `--reload` | Use `PersistentProperties` with `reloadableId` |
| Binding loop warnings | Break cycles with explicit `onXxxChanged` handlers instead of two-way bindings |
| `HoverHandler.containsMouse` silently never fires | `HoverHandler` exposes `hovered` (and `onHoveredChanged`). `containsMouse` belongs to `MouseArea` — both compile, only one works per type |
| `QsMenuAnchor.open()` fails with "not started in QApplication mode" | Add `//@ pragma UseQApplication` at top of `shell.qml` and **restart** QuickShell (not `--reload`) |
| Tray item `.menu.open()` does nothing | `SystemTrayItem.menu` is a `QsMenuHandle`, not a widget. Display it via a `QsMenuAnchor` with `menu`, `anchor.item`, `anchor.edges` (then `open()`) |

---

## More Info

- Type reference: https://quickshell.org/docs/v0.2.1/types/
- Usage guide: https://quickshell.org/docs/v0.2.1/guide/
- Examples: https://github.com/outfoxxed/quickshell-examples
