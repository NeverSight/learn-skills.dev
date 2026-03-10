---
name: desktop-control
description: "Control the mouse, keyboard, and read screen content via accessibility. Use this skill when the user asks to click somewhere on screen, type text into an app, move the mouse, press keyboard shortcuts, read what's on screen, get the accessibility tree of the current window, automate desktop interactions, or control the computer."
tags:
  [
    desktop,
    mouse,
    keyboard,
    accessibility,
    screen,
    automation,
    pyautogui,
    osascript,
    computer-use,
  ]
version: 0.1.0
---

# Skill: desktop-control

## When to Use

Use this skill when the user asks to:

- Click somewhere on the screen
- Move the mouse to a position
- Type text into an application
- Press keyboard shortcuts or hotkeys
- Read what's on the current screen (accessibility tree)
- Get information about the frontmost window
- Automate desktop interactions
- Control the computer (mouse, keyboard, screen)
- Scroll up/down in an application
- Drag and drop elements

**IMPORTANT**: This skill requires Accessibility permissions for the terminal/IDE. On macOS, go to System Settings > Privacy & Security > Accessibility and enable the running application.

## Bundled Scripts

| Script                | Type   | Description                                      |
| --------------------- | ------ | ------------------------------------------------ |
| `scripts/mouse.py`    | Python | Mouse movement, clicking, dragging, scrolling    |
| `scripts/keyboard.py` | Python | Text typing, key presses, hotkeys                |
| `scripts/screen.py`   | Python | Screen info, capture, accessibility tree reading |

All scripts auto-install `pyautogui` if needed.

---

## Mouse Control

### Input Parameters

| Parameter | Required   | Description                                                    | Example |
| --------- | ---------- | -------------------------------------------------------------- | ------- |
| `action`  | Yes        | `move`, `click`, `doubleclick`, `rightclick`, `drag`, `scroll` | click   |
| `x`       | For most   | X coordinate (pixels from left)                                | 500     |
| `y`       | For most   | Y coordinate (pixels from top)                                 | 300     |
| `button`  | No         | Mouse button: `left` (default), `right`, `middle`              | left    |
| `to_x`    | For drag   | Destination X coordinate                                       | 700     |
| `to_y`    | For drag   | Destination Y coordinate                                       | 400     |
| `amount`  | For scroll | Scroll amount (positive=up, negative=down)                     | -3      |

### Script Usage

```bash
# Move mouse
python3 skills/desktop-control/scripts/mouse.py move --x 500 --y 300

# Click at position
python3 skills/desktop-control/scripts/mouse.py click --x 500 --y 300

# Double click
python3 skills/desktop-control/scripts/mouse.py doubleclick --x 500 --y 300

# Right click
python3 skills/desktop-control/scripts/mouse.py rightclick --x 500 --y 300

# Drag from one position to another
python3 skills/desktop-control/scripts/mouse.py drag --x 100 --y 100 --to-x 500 --to-y 500

# Scroll down 3 clicks
python3 skills/desktop-control/scripts/mouse.py scroll --amount -3

# Scroll up 5 clicks at specific position
python3 skills/desktop-control/scripts/mouse.py scroll --x 500 --y 300 --amount 5

# Get current mouse position
python3 skills/desktop-control/scripts/mouse.py position
```

---

## Keyboard Control

### Input Parameters

| Parameter  | Required   | Description                                         | Example     |
| ---------- | ---------- | --------------------------------------------------- | ----------- |
| `action`   | Yes        | `type`, `press`, `hotkey`                           | type        |
| `text`     | For type   | Text to type                                        | Hello World |
| `key`      | For press  | Key name to press                                   | enter       |
| `keys`     | For hotkey | Key combination, plus-separated                     | command+c   |
| `interval` | No         | Delay between keystrokes in seconds (default: 0.02) | 0.05        |

### Script Usage

```bash
# Type text
python3 skills/desktop-control/scripts/keyboard.py type --text "Hello World"

# Type slowly
python3 skills/desktop-control/scripts/keyboard.py type --text "Hello" --interval 0.1

# Press a single key
python3 skills/desktop-control/scripts/keyboard.py press --key enter
python3 skills/desktop-control/scripts/keyboard.py press --key tab
python3 skills/desktop-control/scripts/keyboard.py press --key escape

# Keyboard shortcuts (hotkeys)
python3 skills/desktop-control/scripts/keyboard.py hotkey --keys "command+c"
python3 skills/desktop-control/scripts/keyboard.py hotkey --keys "command+shift+s"
python3 skills/desktop-control/scripts/keyboard.py hotkey --keys "alt+tab"
python3 skills/desktop-control/scripts/keyboard.py hotkey --keys "command+space"
```

### Common Key Names

`enter`, `return`, `tab`, `space`, `backspace`, `delete`, `escape`, `up`, `down`, `left`, `right`, `home`, `end`, `pageup`, `pagedown`, `f1`-`f12`, `command`, `ctrl`, `alt`, `shift`, `capslock`

---

## Screen Reading

### Input Parameters

| Parameter                   | Required           | Description                  | Example         |
| --------------------------- | ------------------ | ---------------------------- | --------------- |
| `action`                    | Yes                | `info`, `capture`, `read-ui` | read-ui         |
| `output`                    | For capture        | Screenshot output path       | /tmp/screen.png |
| `x`, `y`, `width`, `height` | For capture region | Region to capture            |                 |

### Script Usage

```bash
# Get screen size and mouse position
python3 skills/desktop-control/scripts/screen.py info

# Take a screenshot
python3 skills/desktop-control/scripts/screen.py capture --output /tmp/screen.png

# Capture a specific region
python3 skills/desktop-control/scripts/screen.py capture --x 0 --y 0 --width 800 --height 600 --output /tmp/region.png

# Read the accessibility tree of the frontmost application (MOST USEFUL)
python3 skills/desktop-control/scripts/screen.py read-ui

# Read accessibility tree with depth limit
python3 skills/desktop-control/scripts/screen.py read-ui --depth 3
```

The `read-ui` command uses AppleScript to read the accessibility tree of the frontmost application, returning window titles, buttons, text fields, menus, and other UI elements. This is the primary way to understand what's on screen before interacting.

---

## Typical Workflow

1. **Read the screen** to understand what's visible:
   ```bash
   python3 skills/desktop-control/scripts/screen.py read-ui
   ```
2. **Identify targets** from the accessibility tree output
3. **Interact** using mouse/keyboard:
   ```bash
   python3 skills/desktop-control/scripts/mouse.py click --x 500 --y 300
   python3 skills/desktop-control/scripts/keyboard.py type --text "search query"
   python3 skills/desktop-control/scripts/keyboard.py press --key enter
   ```
4. **Verify** by reading the screen again

## Example

```
click on the search bar
type "hello" into the text field
press command+s to save
what's on the screen right now
read the UI elements of the current window
move the mouse to the center of the screen
scroll down in this window
```
