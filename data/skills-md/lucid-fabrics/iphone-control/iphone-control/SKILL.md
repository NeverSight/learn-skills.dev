---
name: iphone-control
description: Control iPhone via iPhone Mirroring on macOS. Capture screenshots, tap, swipe, and type on iPhone screen rendered as a Mac window. Use when user wants to interact with their iPhone through the Mac.
---

# iPhone Mirroring Control

Control your iPhone through macOS iPhone Mirroring. The skill captures the mirroring window, analyzes it, and sends taps/swipes/typing back.

## Prerequisites

| Tool | Install | Purpose |
|------|---------|---------|
| `screencapture` | Built-in macOS | Window capture by window ID |
| `osascript` | Built-in macOS | JXA: window discovery, CGEvent taps/swipes, typing |
| `swiftc` | Xcode CLT | Auto-compiles the window/OCR helpers on first run |
| iPhone Mirroring | macOS 15+ (Sequoia) | Renders iPhone on Mac |

## Permissions Required

- **Accessibility**: Terminal/iTerm must have Accessibility access (System Settings > Privacy & Security > Accessibility)
- **Screen Recording**: Terminal/iTerm must have Screen Recording access (System Settings > Privacy & Security > Screen Recording)
- iPhone Mirroring must be open and phone connected

## Usage

All commands go through `iphone-control.sh`:

```bash
# Find the iPhone Mirroring window
./iphone-control.sh find

# Take a screenshot of the iPhone screen
./iphone-control.sh screenshot

# Tap at coordinates (relative to iPhone screen)
./iphone-control.sh tap 187 400

# Tap on-screen text by OCR - PREFER over raw coordinates when text is visible
./iphone-control.sh tap-text "Battery"
./iphone-control.sh tap-text "Bluetooth" --index 2

# Read the screen: the only inspection channel (no accessibility tree over mirroring)
./iphone-control.sh read                      # every string + tappable coordinates
./iphone-control.sh read --grep "wi-?fi"      # filter
./iphone-control.sh read --json               # machine-readable
./iphone-control.sh read --at 180 400         # what is at this point

# Wait for a condition instead of sleeping a guess - faster AND more reliable
./iphone-control.sh wait text "Settings"      # until it appears
./iphone-control.sh wait gone "Loading"       # until it disappears
./iphone-control.sh wait still                # until animation settles

# Long press (context menus, edit mode, selection) and double tap
./iphone-control.sh press 306 555 800
./iphone-control.sh double-tap 180 400

# Keys and clipboard
./iphone-control.sh key return
./iphone-control.sh key a --cmd               # select all
./iphone-control.sh paste                     # Universal Clipboard from the Mac
./iphone-control.sh clear-text

# Navigation
./iphone-control.sh back
./iphone-control.sh scroll-to "Battery" --tap

# Scroll lists/pages (dy>0 down, dy<0 up; optional position)
./iphone-control.sh scroll 300
./iphone-control.sh scroll -300 180 400

# Swipe - horizontal page changes and gestures ONLY (drags do NOT scroll lists; use scroll)
./iphone-control.sh swipe 300 400 60 400

# Move a home-screen icon, or drop it onto another icon to create/extend a folder
./iphone-control.sh drag-icon 138 463 54 463              # reorder (one slot at a time is exact)
./iphone-control.sh drag-icon 54 463 138 463 --hover 1200 # drop INTO icon -> folder

# Type text (optionally tap a field first)
./iphone-control.sh type "hello world"
./iphone-control.sh type "hello world" 187 400

# Batch: several actions in ONE session - much faster, one focus steal total
./iphone-control.sh batch "tap 54 598" "tap 138 598" "scroll 200" "sleep 0.5" "tap 90 300"
```

## Workflow for AI Agent

1. `find` - locate the mirroring window (do once per session)
2. `screenshot` - capture current state, analyze the image
3. Decide action based on what's visible
4. `tap-text` (preferred when target has visible text) / `tap` / `scroll` / `swipe` / `type`
5. `screenshot` - verify the result
6. Repeat 3-5

Prefer `tap-text` over pixel coordinates whenever the target shows text: OCR-derived
centers do not drift. If it fails it prints every string it saw on screen - use that
to decide whether to `scroll` and retry. Chain known sequences with `batch`.

Never `sleep` a guessed duration after an action. Use `wait still` (animation
settled), `wait text` (target appeared) or `wait gone` (spinner cleared). Guessed
sleeps are both slower on fast transitions and flaky on slow ones.

## Speed

`helpers/input` is a compiled engine that does window resolution, the input
session and event posting in a single process. `helpers/input batch` reads one
action per line from stdin and runs them all in ONE session, which is the fastest
way to execute a known sequence:

```bash
printf 'tap 54 598\ntap 138 598\nkey 36 0\n' | ./helpers/input batch
```

The engine also runs as a **resident daemon** (`helpers/input serve`, auto-started
on first use by `helpers/input send <verb...>`): it keeps the Vision OCR model
warm, captures natively via ScreenCaptureKit, and holds one input session open
across commands, closing it (restoring the user's focus and cursor) after 1.5s
idle. `read.sh`, `wait.sh`, `screenshot.sh` and `tap-text.sh` use it automatically
and fall back to their process pipelines if it is unavailable. Set
`ICTL_NO_DAEMON=1` to disable. The daemon exits on its own after 5 minutes idle;
`helpers/input send quit` stops it now.

| Path | Cost |
|------|------|
| One action, focus stolen and returned | ~0.5s (macOS app activation dominates) |
| One action, mirroring already frontmost | ~0.15s |
| Each extra action inside a batch | ~0.03s |
| Screenshot via daemon | ~0.1s (was ~0.27s) |
| `read` / `tap-text` OCR via daemon (warm) | ~0.2-0.4s (was ~1-1.3s) |
| `wait text` present-immediately via daemon | ~0.25s (was ~3.8s) |

## Platform constraints worth knowing

- Mirroring is a **live video stream**: two captures of a frozen screen are never
  byte-identical, so frame comparison needs a tolerance (`wait still` handles it).
- Mirroring forwards **virtual keycodes** and ignores unicode payloads, so typing
  must map characters to real keys on the active layout.
- Only **line-unit** scroll wheel events scroll iOS lists; drag gestures do not.
- Icon drag needs **hardware-like dynamics** (~125Hz, subpixel, jitter) or
  SpringBoard never lifts the icon.
- The **Escape key does not dismiss** iOS context menus; tap outside instead.
- **Control Center and Notification Center are not reachable.** The pull-down
  gesture must start at content y=0-8, which is inside the mirroring window's
  own drag handle - a drag there moves the WINDOW, not the phone. Apple's own
  View menu has no shortcut for either, for the same reason. Do not retry this
  with different gesture timing; it is not a tuning problem.
- **Pinch/zoom and rotate cannot be synthesized.** They require genuine
  Multi-Touch trackpad `NSEvent` gesture reports (magnification/rotation), a
  channel this tool has no way to fake - `CGEventCreateMagnificationGestureEvent`
  and friends do not exist on this macOS (checked via `nm` and `dlsym`). The
  feature is real for trackpad users, just not scriptable. Use `double-tap` for
  zoom-toggle coverage instead.

## Coordinate System

- Origin (0,0) is the **top-left** of the iPhone Mirroring content area
- Coordinates are relative to the iPhone screen, NOT the Mac screen
- The scripts handle conversion to absolute Mac screen coordinates
- Typical iPhone screen in mirroring: ~375x812 points (varies by model)
- Screenshots are normalized to point dimensions: 1 image pixel = 1 tap coordinate
- Multi-display safe: the window can be on any display, including ones with
  negative global coordinates (left of / above primary) or a different Retina scale

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "iPhone Mirroring window not found" | Open iPhone Mirroring app on Mac |
| Tap lands in wrong spot | Run `find` again - window may have moved |
| No screen recording permission | System Settings > Privacy & Security > Screen Recording > add Terminal |
| No accessibility permission | System Settings > Privacy & Security > Accessibility > add Terminal |
