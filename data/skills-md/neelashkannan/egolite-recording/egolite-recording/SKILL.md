---
name: egolite-recording
description: Record an Ego-lite browser test or automation as a background WebM video with a visible synthetic pointer, action labels, and click ripples. Use when the user asks to record, film, replay, or preserve an Ego-lite browser run; do not use for ordinary unrecorded browsing.
---

# Ego-lite Recording

Use the bundled recorder at `scripts/ego-record.mjs`. It creates an isolated Ego task space, opens the target page, starts native CDP screencasting, runs the supplied test code, finalizes the recording, and closes the task space in a separate cleanup run.

## First-time setup

If the recorder reports a missing Ego runtime, run the bundled `scripts/setup.sh` using its actual path inside this installed skill. The setup requires:

- macOS with [Ego lite](https://lite.ego.app/) installed and first-run onboarding completed
- `ego-browser` available on `PATH`
- Node.js 22 or newer, Git, npm, and FFmpeg

The setup script downloads the open-source Ego browser runtime from `citrolabs/ego-lite`, builds it in `~/.local/share/egolite-recording/ego-lite`, and verifies the required executables. Do not claim setup succeeded unless the script exits successfully.

## Record a run

Use an explicit target URL and absolute output path:

```bash
EGO_RECORD_URL="https://example.com" \
EGO_RECORD_PATH="/absolute/path/test.webm" \
node /absolute/path/to/egolite-recording/scripts/ego-record.mjs <<'EOF'
await page.waitForLoadState('load')
const heading = await page.locator('h1').textContent()
if (heading !== 'Example Domain') throw new Error(`unexpected heading: ${heading}`)
EOF
```

The supplied code runs after navigation to `EGO_RECORD_URL`. Use the Playwright-style `page` facade, including `page.locator(...)`, `page.getByText(...)`, `page.goto(...)`, keyboard and mouse helpers, waits, and assertions implemented by throwing errors.

Keep all actions for one video inside the same heredoc. Prefer locator `.click()`, `.fill()`, `.hover()`, and related methods so the recording shows the pointer, label, and click ripple. Avoid `page.evaluate(() => element.click())`, because DOM-triggered clicks have no pointer coordinates and bypass the visual effects.

The recorder captures the webpage viewport only, without browser chrome or audio. It prints `EGO_RECORDING_PATH=...` and file size after finalization; report that exact path to the user.

## Options

- `EGO_RECORD_TASK_NAME`: isolated Ego task-space name; defaults to a unique timestamped name.
- `EGO_RECORD_WIDTH` and `EGO_RECORD_HEIGHT`: even video dimensions; default `1280x720`.
- `EGO_RECORD_QUALITY`: JPEG source-frame quality from 0 to 100; default `90`.
- `EGO_RECORD_PATH`: destination ending in `.webm`; defaults to `.agent-artifacts/ego-recordings/<timestamp>.webm` under the current directory.
- `EGO_RECORD_POINTER`: set to `0`, `false`, `off`, or `no` to disable pointer effects; enabled by default.
- `EGO_RECORD_CLI`: override the built Ego runtime entrypoint.
- `EGO_RECORD_RUNTIME_DIR`: override the setup/runtime directory.
- `EGO_BROWSER_FFMPEG_PATH`: override the FFmpeg executable.

If the test fails, report the recording path only when the wrapper confirms a non-empty file was finalized. Never claim a passed test merely because a video exists.
