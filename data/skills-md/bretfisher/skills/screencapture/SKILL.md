---
name: screencapture
description: Captures the user's macOS screen, a window, or a region with the built-in `screencapture` CLI, then reads the image so the agent can see what the user sees. Use it when the user asks to check how a native macOS app looks (SwiftUI, AppKit, Electron, Qt, Tk, Java Swing), verify a window rendered correctly after a build or code change, diagnose a visual bug they describe in a desktop app, confirm a menu, dialog, or layout state, or asks "can you see this?" about anything outside a browser, even if they don't say "screenshot". Web pages and web apps belong to a browser automation tool.
---

# screencapture

macOS ships `screencapture`, a fast CLI for grabbing the screen. Use it to _see_ what the user sees when working on native GUI software. Web apps belong in a browser-automation tool; this skill is for everything else (SwiftUI/AppKit, Electron, Java/Swing, Qt, Tk, games, system UI, Finder, Xcode, etc.).

## Core workflow

1. **Capture** to the scratch directory with a unique filename. Pick the directory in this order: the session scratch directory when the host names one in its instructions (Claude Code calls it the scratchpad directory), else `$TMPDIR`, else `/tmp`. A session directory is isolated from other sessions and from the user's project, so files there cannot collide or clutter shared space. Set `OUT` to that path and use it in every command below.
2. **Read** the image with the Read tool — Agent is multimodal and will see the PNG inline.
3. **Delete** the file immediately after reading. The user wants temp space kept clean; never leave screenshots lying around.

Filename convention: `$OUT/screencap-$(date +%s).png`. The timestamp prevents collisions if you capture multiple times in one task.

## Picking the right mode

| Goal                                                             | Command                                                                                   |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Whole main display, no UI sound                                  | `screencapture -x -m $OUT/screencap-<ts>.png`                                             |
| All displays                                                     | `screencapture -x $OUT/screencap-<ts>.png` (one file per screen — macOS appends suffixes) |
| User picks a window or region interactively                      | `screencapture -x -i $OUT/screencap-<ts>.png`                                             |
| Specific rectangle (x,y,width,height in points, origin top-left) | `screencapture -x -R 100,100,800,600 $OUT/screencap-<ts>.png`                             |
| Specific window by id                                            | `screencapture -x -l <windowid> $OUT/screencap-<ts>.png`                                  |
| Capture after delay (e.g. to let a menu open)                    | `screencapture -x -T 3 $OUT/screencap-<ts>.png`                                           |

Always pass `-x` so the shutter sound doesn't startle the user.

`-i` is interactive: it blocks until the user clicks/drags. Only use it when you genuinely need the user to point at something — for autonomous "show me the app's main window" checks, prefer full-screen (`-m`) or a known rect (`-R`).

To find a window id for `-l`, you can run `osascript -e 'tell app "System Events" to get id of windows of process "<AppName>"'` or use `CGWindowListCopyWindowInfo` via a small helper; this is rarely worth it — full-screen capture is usually fine.

## Full flag reference

```text
usage: screencapture [-icMPmwsWxSCUtoa] [files]
  -c         force screen capture to go to the clipboard
  -b         capture Touch Bar — non-interactive modes only
  -C         capture the cursor as well as the screen. only in non-interactive modes
  -d         display errors to the user graphically
  -i         capture screen interactively, by selection or window
               control key — causes screenshot to go to clipboard
               space key   — toggle between mouse selection and window selection modes
               escape key  — cancels interactive screenshot
  -m         only capture the main monitor, undefined if -i is set
  -D<display> screen capture or record from the display specified. -D 1 is main display, -D 2 secondary, etc.
  -o         in window capture mode, do not capture the shadow of the window
  -p         screen capture will use the default settings for capture. The files argument will be ignored
  -M         screen capture output will go to a new Mail message
  -P         screen capture output will open in Preview or QuickTime Player if video
  -B<bundleid> screen capture output will open in app with bundleid
  -s         only allow mouse selection mode
  -S         in window capture mode, capture the screen not the window
  -J<style>  sets the starting of interactive capture
               selection       - captures screen in selection mode
               window          - captures screen in window mode
               video           - records screen in selection mode
  -t<format> image format to create, default is png (other options include pdf, jpg, tiff and other formats)
  -T<seconds> take the picture after a delay of <seconds>, default is 5
  -w         only allow window selection mode
  -W         start interaction in window selection mode
  -x         do not play sounds
  -a         do not include windows attached to selected windows
  -r         do not add dpi meta data to image
  -l<windowid> capture this windowsid
  -R<x,y,w,h> capture screen rect
  -v         capture video recording of the screen
  -V<seconds> limits video capture to specified seconds
  -g         captures audio during a video recording using default input.
  -G<id>     captures audio during a video recording using audio id specified.
  -k         show clicks in video recording mode
  -U         Show interactive toolbar in interactive mode
  -u         present UI after screencapture is complete. files passed to command line will be ignored
  -H         capture content in HDR
  files      where to save the screen capture, 1 file per screen
```

## Cleanup is mandatory

The user keeps temp space tidy. After every `Read` of the screenshot, immediately `rm` it in the same logical step. Don't batch — capture, read, delete, one screenshot at a time. If you need a sequence of screenshots, still delete each one as soon as you've consumed it.

Example flow:

```bash
OUT="${SCRATCH_DIR:-${TMPDIR:-/tmp}}"   # SCRATCH_DIR = the session scratch path from the host's instructions, if any
screencapture -x -m "$OUT/screencap-1715300000.png"
# → Read tool on $OUT/screencap-1715300000.png
rm "$OUT/screencap-1715300000.png"
```

If a capture fails (e.g. no Screen Recording TCC permission), `screencapture` writes a black or empty image rather than erroring loudly. If the Read shows a black/empty frame, tell the user to grant Screen Recording permission in System Settings → Privacy & Security → Screen Recording for the terminal app running Agent, then retry.

## When NOT to use this skill

- Web pages, web apps, anything in a browser → use the browser automation skill.
- The user asks for a screen _recording_ (video) → `screencapture -v` works but is rarely what's wanted; ask first.
- You just want to know what app is focused → `osascript -e 'tell app "System Events" to name of first process whose frontmost is true'` is faster and doesn't need TCC.
