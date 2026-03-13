---
name: weavgui
description: "Automate desktop GUI operations using the weavgui CLI: taking screenshots, moving the mouse, clicking, typing keystrokes, and reading/writing the system pasteboard. Use when asked to interact with the desktop graphically — clicking UI elements, reading on-screen content, filling forms, navigating applications, or any task requiring precise mouse control and visual feedback."
---

# Skill: weavgui Desktop Automation

## Installation

```bash
uv tool install weavgui
```

Verify:

```bash
weavgui --version
```

> **macOS requirement**: mouse and keystroke automation requires Accessibility permission.  
> Grant it at: `System Settings > Privacy & Security > Accessibility`

---

## Auto-Screenshot Behavior

Every action command automatically captures a screenshot to **`screenshot.png`** in the current working directory after a short delay. You never need to pass output paths or screenshot flags.

| Command | Auto-screenshot delay |
|---|---|
| `screenshot` | immediate |
| `mouse move`, `mouse moveto` | 500 ms |
| `mouse click`, `doubleclick`, `rightclick` | 2 s |
| `keystroke` | 1 s |

After each command, read `screenshot.png` as an image to observe the current state of the screen.

---

## Coordinate System

All mouse and screenshot commands share the same coordinate space:

- Origin `(0, 0)` is the **top-left** of the primary display
- `x` increases to the right, `y` increases downward
- Coordinates are **logical pixels** (on macOS Retina, screenshots are auto-downscaled to match)

---

## Core Commands

### Screenshot

```bash
weavgui screenshot
```

Always saves to `screenshot.png` in the current working directory. Always draws cursor markers:

- Red crosshair lines
- Red small box (100×100 px, radius 50)
- Green medium box (200×200 px, radius 100)
- Blue large box (600×600 px, radius 300)

The three concentric boxes are **positioning references** — use them to gauge how far to move the mouse next:

| Target location | Delta range |
|---|---|
| Inside red box | Fine: `±50 px` |
| Between red and green | Medium: `±50–100 px` |
| Between green and blue | Coarse: `±100–300 px` |
| Outside blue box | Large move — estimate from full screenshot |

The command also prints the current mouse coordinates and display bounds to stdout.

### Mouse Move

```bash
weavgui mouse move '(dx,dy)'
```

Moves the mouse by a **relative delta**. The argument uses `(dx,dy)` format — negative values work naturally. Fails if the target would leave the display bounds. Prints the start position, end position, and display bounds to stdout. Automatically saves a screenshot to `screenshot.png` after a 500 ms delay.

### Mouse Move To

```bash
weavgui mouse moveto '(x,y)'
```

Moves the mouse to an **absolute position**. Fails if the position is outside the display bounds. Automatically saves a screenshot to `screenshot.png` after a 500 ms delay.

### Mouse Click

```bash
weavgui mouse click         # left click
weavgui mouse doubleclick   # double left click
weavgui mouse rightclick    # right click
```

All clicks happen at the **current cursor position**. A screenshot is automatically saved to `screenshot.png` after a 2 s delay to allow the UI to settle.

### Keystroke

```bash
weavgui keystroke <keys>
```

Examples: `c`, `ctrl+c`, `command+c`, `shift+a`, `command+z`

A screenshot is automatically saved to `screenshot.png` after a 1 s delay.

### Pasteboard

```bash
weavgui pasteboard write <text...>   # write to clipboard
weavgui pasteboard read              # read from clipboard
```

---

## Critical Workflow: Precise Mouse Positioning

**Never guess a target coordinate and click immediately.**

`mouse move` accepts only relative deltas; `mouse moveto` accepts absolute coordinates but you still need to know the target pixel position. The correct approach is an **iterative positioning loop**:

```
screenshot → analyze image → move mouse → (auto-screenshot) → analyze image → move mouse → ... → click
```

### Step-by-step

1. **Take a screenshot** and read the image into context:

   ```bash
   weavgui screenshot
   ```

   Then read `screenshot.png` as an image attachment.

2. **Analyze the screenshot**: Identify the target UI element. Read the cursor marker position from the stdout output (printed automatically). Use the three reference boxes to gauge your delta:
   - Target inside the **red box** (radius 50) → fine delta, within `±50 px`
   - Target inside the **green box** (radius 100) → medium delta, within `±100 px`
   - Target inside the **blue box** (radius 300) → coarse delta, within `±300 px`
   - Target outside the **blue box** → large move, estimate from the full screenshot

3. **Move the mouse**:

   ```bash
   weavgui mouse move '(dx,dy)'
   ```

   A screenshot is saved to `screenshot.png` automatically after 500 ms. Read it immediately.

4. **Verify position**: Check that the crosshair (red lines) is now centered on the target. If not, repeat from step 2 with a corrected delta.

5. **Click only when the cursor is confirmed on-target**:

   ```bash
   weavgui mouse click
   ```

   A screenshot is saved automatically after 2 s. Read it to confirm the action took effect.

### Why this loop matters

- Even with `mouse moveto`, you need the exact target pixel coordinate — which requires a screenshot to determine.
- Screen content, window positions, and scroll state can all shift between steps.
- Even a single iteration of screenshot → analyze → move can land the cursor accurately.
- For high-precision targets (small buttons, text fields), two or three iterations are typical.

### Example: clicking a button labeled "Submit"

```bash
# Step 1: initial screenshot
weavgui screenshot
# → read screenshot.png, observe crosshair at (500, 400), Submit button at approx (720, 610)
# → estimate dx=220, dy=210

# Step 2: move toward target (auto-screenshots after 500 ms)
weavgui mouse move '(220,210)'
# → read screenshot.png, crosshair now at (720, 608) — close enough

# Step 3: click (auto-screenshots after 2 s)
weavgui mouse click
# → read screenshot.png to confirm the click took effect
```

---

## Delegate to a Subagent

The iterative positioning loop loads multiple screenshots into context, which can consume significant tokens. **When possible, launch a subagent (Task tool) to perform the entire positioning-and-click sequence**, keeping the main conversation context clean.

### How to delegate

Use the Task tool with a prompt that describes:

1. The target element (e.g. "the Submit button in the bottom-right of the dialog")
2. The action to perform once positioned (e.g. `mouse click`, `mouse doubleclick`)
3. Any follow-up actions (e.g. type text, press a key)

Example prompt for the Task tool:

```
Use the weavgui CLI to click the "Submit" button visible on screen.

Workflow:
1. Run `weavgui screenshot`, then read screenshot.png as an image.
2. Identify the "Submit" button. Read the crosshair position from stdout.
3. Estimate (dx, dy) from the crosshair to the button center, run `weavgui mouse move '(dx,dy)'`.
4. Read screenshot.png (auto-captured after 500 ms), verify the crosshair is on the button. Adjust if needed.
5. Run `weavgui mouse click`.
6. Read screenshot.png (auto-captured after 2 s) to confirm the click took effect.

Return a summary of what happened and the final mouse position.
```

### Benefits

- **Saves main context**: screenshots stay inside the subagent and are discarded when it finishes.
- **Isolation**: if the loop takes many iterations, the main conversation is unaffected.
- **Composability**: you can launch multiple subagents in sequence (e.g. one to click a field, another to type text) without accumulating images.

### When NOT to delegate

- If you only need a single screenshot for analysis (no mouse interaction), just run the command directly.
- If the task is a single click where you are already confident about the position.

---

## Text Input Workflow

To type text into a focused field:

1. Click the target field (using the positioning loop above)
2. Optionally select all existing text: `weavgui keystroke command+a`
3. Write new text to the pasteboard: `weavgui pasteboard write <your text>`
4. Paste: `weavgui keystroke command+v`

```bash
weavgui mouse click
weavgui keystroke command+a
weavgui pasteboard write Hello World
weavgui keystroke command+v
```

---

## Tips

- Every action command auto-captures `screenshot.png` — always read it after each command to observe the result.
- Always prefer the **iterative screenshot loop** over single-shot coordinate estimation.
- After any keyboard shortcut that changes screen state (e.g. `command+z`, `return`), the auto-screenshot is taken automatically after 1 s — read `screenshot.png` before proceeding.
- The stdout output of every command includes the current mouse position — use this as a precise anchor for the next delta calculation.
