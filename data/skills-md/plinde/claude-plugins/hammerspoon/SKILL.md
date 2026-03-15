---
name: hammerspoon
description: This skill should be used when automating macOS with Hammerspoon, configuring window management hotkeys, working with Spoons (plugins), writing Lua configuration in init.lua, or using the hs CLI for scripting and reloading.
---

# Hammerspoon macOS Automation

Hammerspoon bridges macOS and Lua scripting for powerful desktop automation.

## Directory Structure

```
~/.hammerspoon/
├── init.lua              # Main entry point (always loaded on startup)
├── Spoons/               # Plugin directory
│   └── *.spoon/          # Individual Spoon packages
│       └── init.lua      # Spoon entry point
└── .gitignore
```

## Configuration Basics

### init.lua - Entry Point

Hammerspoon always loads `~/.hammerspoon/init.lua` on startup:

```lua
-- Enable CLI support (required for hs command)
require("hs.ipc")

-- Load a Spoon
hs.loadSpoon("SpoonName")

-- Configure the Spoon
spoon.SpoonName:bindHotkeys({...})
```

### Loading Spoons

```lua
-- Load and auto-init (default)
hs.loadSpoon("MySpoon")

-- Load without global namespace
local mySpoon = hs.loadSpoon("MySpoon", false)
```

When loaded, Spoons are accessible via `spoon.SpoonName`.

## CLI Usage (hs command)

**Prerequisite:** Add `require("hs.ipc")` to init.lua, then reload manually once.

```bash
# Reload configuration
hs -c 'hs.reload()'

# Show alert on screen
hs -c 'hs.alert("Hello from CLI")'

# Run any Lua code
hs -c 'print(hs.host.locale.current())'

# Get focused window info
hs -c 'print(hs.window.focusedWindow():title())'
```

## Window Management with ShiftIt

ShiftIt is a popular Spoon for window tiling.

### Installation

```bash
# Download from https://github.com/peterklijn/hammerspoon-shiftit
# Extract to ~/.hammerspoon/Spoons/ShiftIt.spoon/
```

### Configuration

```lua
require("hs.ipc")
hs.loadSpoon("ShiftIt")

spoon.ShiftIt:bindHotkeys({
    -- Halves
    left = { { 'ctrl', 'cmd' }, 'left' },
    right = { { 'ctrl', 'cmd' }, 'right' },
    up = { { 'ctrl', 'cmd' }, 'up' },
    down = { { 'ctrl', 'cmd' }, 'down' },

    -- Quarters
    upleft = { { 'ctrl', 'cmd' }, '1' },
    upright = { { 'ctrl', 'cmd' }, '2' },
    botleft = { { 'ctrl', 'cmd' }, '3' },
    botright = { { 'ctrl', 'cmd' }, '4' },

    -- Other
    maximum = { { 'ctrl', 'cmd' }, 'm' },
    toggleFullScreen = { { 'ctrl', 'cmd' }, 'f' },
    center = { { 'ctrl', 'cmd' }, 'c' },
    nextScreen = { { 'ctrl', 'cmd' }, 'n' },
    previousScreen = { { 'ctrl', 'cmd' }, 'p' },
    resizeOut = { { 'ctrl', 'cmd' }, '=' },
    resizeIn = { { 'ctrl', 'cmd' }, '-' },
})
```

### Modifier Keys

| Key | Lua Name |
|-----|----------|
| Command | `'cmd'` |
| Control | `'ctrl'` |
| Option/Alt | `'alt'` |
| Shift | `'shift'` |

## Hotkey Binding (Without Spoons)

```lua
-- Simple hotkey
hs.hotkey.bind({'cmd', 'alt'}, 'R', function()
    hs.reload()
end)

-- Hotkey with message
hs.hotkey.bind({'cmd', 'shift'}, 'H', function()
    hs.alert.show('Hello!')
end)
```

## Common Modules

### hs.window - Window Management

```lua
-- Get focused window
local win = hs.window.focusedWindow()

-- Move/resize
win:moveToUnit('[0,0,0.5,1]')  -- Left half
win:maximize()
win:centerOnScreen()

-- Get all windows
local allWindows = hs.window.allWindows()
```

### hs.application - App Control

```lua
-- Launch or focus app
hs.application.launchOrFocus('Safari')

-- Get running app
local app = hs.application.get('Finder')
app:activate()
```

### hs.alert - On-screen Messages

```lua
hs.alert.show('Message')
hs.alert.show('Message', nil, nil, 3)  -- 3 second duration
```

### hs.notify - System Notifications

```lua
hs.notify.new({title='Title', informativeText='Body'}):send()
```

### hs.caffeinate - Sleep/Wake

```lua
-- Prevent sleep
hs.caffeinate.set('displayIdle', true)

-- Watch for sleep/wake events
hs.caffeinate.watcher.new(function(event)
    if event == hs.caffeinate.watcher.systemWillSleep then
        print('Going to sleep')
    end
end):start()
```

## Spoons

### What is a Spoon?

Self-contained Lua plugin with standard structure:

```
MySpoon.spoon/
└── init.lua     # Required: exports a table with methods
```

### Official Spoon Repository

- Browse: https://www.hammerspoon.org/Spoons/
- Source: https://github.com/Hammerspoon/Spoons

### SpoonInstall - Package Manager

```lua
hs.loadSpoon("SpoonInstall")

-- Install from official repo
spoon.SpoonInstall:andUse("ReloadConfiguration", {
    start = true
})

-- Install from custom repo
spoon.SpoonInstall.repos.Custom = {
    url = "https://github.com/user/repo",
    desc = "Custom spoons",
    branch = "main",
}
spoon.SpoonInstall:andUse("CustomSpoon", { repo = "Custom" })
```

## Configuration Reloading

### Manual Reload

- Click menubar icon -> "Reload Config"
- Or bind a hotkey:

```lua
hs.hotkey.bind({'cmd', 'alt', 'ctrl'}, 'R', function()
    hs.reload()
end)
```

### Auto-reload on File Change

```lua
hs.loadSpoon("ReloadConfiguration")
spoon.ReloadConfiguration:start()
```

Or manually:

```lua
local configWatcher = hs.pathwatcher.new(os.getenv('HOME') .. '/.hammerspoon/', function(files)
    for _, file in pairs(files) do
        if file:sub(-4) == '.lua' then
            hs.reload()
            return
        end
    end
end):start()
```

### CLI Reload

```bash
hs -c 'hs.reload()'
```

Note: Requires `require("hs.ipc")` in init.lua.

## Troubleshooting

### IPC Not Working

```
error: can't access Hammerspoon message port
```

**Fix:** Add `require("hs.ipc")` to init.lua and reload manually via menubar.

### Spoon Not Loading

1. Check path: `~/.hammerspoon/Spoons/Name.spoon/init.lua`
2. Check Lua syntax in Spoon's init.lua
3. Check Hammerspoon console for errors (menubar -> Console)

### Hotkey Not Working

1. Check for conflicts with system shortcuts
2. Verify modifier key names are lowercase strings
3. Check console for binding errors

## Console and Debugging

```lua
-- Print to console
print('Debug message')

-- Inspect objects
hs.inspect(someTable)

-- Open console
hs.openConsole()
```

Access console: Menubar icon -> Console (or Cmd+Alt+C if bound)

## Best Practices

1. **Always use IPC** - Add `require("hs.ipc")` for CLI support
2. **Use Spoons** - Don't reinvent window management
3. **Version control** - Track `~/.hammerspoon/` with git
4. **Capture variables** - Objects not stored in variables get garbage collected
5. **Check console** - First place to look for errors

## References

- [Official Documentation](https://www.hammerspoon.org/docs/)
- [Getting Started Guide](https://www.hammerspoon.org/go/)
- [Spoons Repository](https://www.hammerspoon.org/Spoons/)
- [GitHub Repository](https://github.com/Hammerspoon/hammerspoon)
