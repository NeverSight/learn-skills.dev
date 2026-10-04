---
name: ui-recording-timeline
description: Turn a screen recording of a UI (page load, navigation, redirect/auth flow, app startup) into an interactive paint timeline page. You get a full-window video, a timeline of each visual paint with timestamps and durations, and on-video flashes of what was painted (pink) versus what only moved (blue). Use when the user shares a screen recording (.mp4/.mov) and asks for a timeline of paints, frames, or visual changes, a filmstrip, load-performance breakdown, "what painted when", or how long each screen was shown.
---

# UI recording timeline

Produces a self-contained folder with `index.html` and the video. The video fills the window. Below it are a one-line caption and a thin timeline (phase colors, paint ticks, hover thumbnails, scrubbing). Change regions flash on the video at each paint, and a paint list drawer opens with `l`.

Everything needed is in this skill directory:

- `scripts/timeline.py`: one CLI with all the steps. Dependencies are declared inline, and `uv run` installs them.
- `assets/template.html`: the page. `build` injects the data into it.

Requirements: `ffmpeg`/`ffprobe` and `uv` on PATH. Chrome or Chromium is needed only for `preview`.

Below, `T` means `uv run <this skill dir>/scripts/timeline.py`. Define it as a shell function, not a variable: zsh doesn't word-split variables. Use the absolute path of the skill directory:

```bash
T(){ uv run "/abs/path/to/ui-recording-timeline/scripts/timeline.py" "$@"; }
```

 `WD` is the output folder. If the user's project has conventions for where research or collateral goes, follow them; otherwise put `WD` next to the video as `<video-stem>-timeline/`.

## Workflow

### 1. Extract and find candidate paints

```bash
T extract /path/to/recording.mp4 WD     # copies video, writes meta.json (frame timestamps; VFR is fine)
T candidates WD                         # table of frames that differ from the previous frame
```

Each row has the frame index, time, % changed, kind (`change` / `full` / `cursor?`), and the normalized bbox. Small cursor-like changes are hidden (use `--all` to show them).

### 2. Look at the frames, then decide what counts as a paint

Never label from the table alone. Look at the frames:

```bash
T sheet WD --frames 0,4,14,26,61 --name overview          # labelled contact sheets -> WD/sheets/*.jpg
T sheet WD --frames 18,19 --crop 0,0,0.25,0.15 --name zoom # zoom into a small change
```

Read the sheet images with the image viewer. Make sure to include the frame before each candidate, so you can see what changed.

Rules for choosing paints:
- **Is a paint:** a visible content or layout change. That covers skeletons appearing, real content replacing skeletons, navigation to a blank page, a new page's first paint, a label or button-state change, and browser chrome that signals load state (the reload icon replacing the stop X).
- **Is not a paint:** cursor movement, hover highlights, spinner rotation, caret blink, or a gradual shimmer on skeletons that are already there. Look at the bbox: tiny regions that wander across consecutive frames are the cursor.
- **Animations:** a multi-frame animation (a check-mark animating, a panel sliding in) is one paint at its final frame. Give it `"base": <frame before the animation started>` so the diff compares the whole animation.
- **Minor paints:** set `minor: true` on small in-place updates (a label, a button state, browser chrome). They get shorter ticks and muted text.
- **Phases:** group paints into phases by screen or URL (for example: app shell, SSO gate, IdP, blank redirect, signed-in app, idle). The address bar in the frames usually tells you. Phases must cover 0 to the recording's duration with no gaps.
- **Idle phases:** set `"idle": true` on stretches where nothing on screen changes. That always includes the tail after the last paint, and can include long waits on one unchanged screen. Idle phases are drawn hatched grey, not in a palette color: a saturated color would suggest activity, and dark grey makes the bar look like it ends early. Don't trim the idle tail; it's real time, and the video spans it.
- **Metrics:** the first two appear in the caption, so put the most important first (for example "main content" and "visually complete"). Others, like time on the IdP or total blank time, go in the drawer.
- **Caveat:** t=0 is the first frame of the recording, not navigation start. If the first frame already shows UI, say so in `notes`.

### 3. Write `WD/paints.json`

```json
{
  "title": "vercel.com/vercel-labs with an SSO redirect",
  "notes": "Recording starts mid-navigation: the dashboard shell is already on screen at t=0.",
  "metrics": [
    {"value": "6.50 s", "label": "main content"},
    {"value": "8.37 s", "label": "visually complete"},
    {"value": "2.53 s", "label": "on Okta"}
  ],
  "phases": [
    {"start": 0.0,   "end": 0.802,  "name": "Dashboard (unauthenticated)"},
    {"start": 0.802, "end": 2.002,  "name": "Vercel SSO gate"},
    {"start": 2.002, "end": 8.468,  "name": "Okta and back"},
    {"start": 8.468, "end": 10.935, "name": "Idle", "idle": true}
  ],
  "paints": [
    {"frame": 0,  "label": "Dashboard shell: sidebar nav and header skeleton (recording start)"},
    {"frame": 4,  "label": "Projects and usage skeleton cards"},
    {"frame": 19, "label": "Team switcher changes to \"Select Team\"", "minor": true},
    {"frame": 87, "label": "Okta Verify check badge (animates 2.668 to 3.068 s)", "minor": true, "base": 74}
  ]
}
```

- `frame` is the decoded frame index from `candidates`. The time comes from the frame's real timestamp, so don't hand-compute it. Phase boundaries are in seconds: use the `t` of the paint that starts each phase, and the duration from `extract` for the last one.
- Labels are short and concrete. Say what appeared, changed or disappeared, and quote on-screen text.
- Optional per phase: `"color": "#hex"`. By default colors come from a palette.

### 4. Compute and check the change regions

```bash
T regions WD     # move-aware diff for every paint -> regions.json
T check WD       # boxes drawn on every paint frame -> WD/sheets/check-*.jpg
```

Look at every check sheet. Pink means painted, blue means moved, and thin grey shows where the content moved from. How the diff works (details in `compute_regions`):
- Changed layout shapes are snapped to whole elements: words, icons, inputs, cards. Faint shimmer ends are included.
- A shape found nearby in the previous frame, whose old spot was vacated, counts as moved. For example, when a sidebar item is inserted, the rows below it slide down. Same-offset moves are grouped.
- Ambiguous repeated shapes (identical chevrons, rows) count as moved when they line up with an offset already found in the same frame.
- The cursor is learned, not guessed from size. Cursor sprites (arrow, hand, text cursor) come from the `candidates` frames where only something small moved on its own. Only boxes containing a known sprite, in either frame, are dropped. Small real paints like a logo, an icon or a toolbar button are kept. So run `candidates` before `regions`.
- Everything else is painted. That includes flat fills like a new backdrop.

If a box looks wrong:
- First check the paint choice. A wrong `base` or a hover state inside the paint frame is the usual cause.
- Only then consider tuning the constants at the top of `compute_regions`. They're tuned at 1710 px wide and scaled automatically: `EDGE`/`CHG` thresholds, `SEARCH` distance, the cursor size, and the grow tolerance.

### 5. Build, preview, and open

```bash
T build WD                    # paint thumbnails + WD/index.html
T preview WD --t 6.502        # headless screenshot with boxes frozen -> WD/preview.png
open WD/index.html
```

Read `preview.png` to verify the layout and that the overlay lines up with the video. Re-run `build` after any change to `paints.json` or `regions.json`. Run `regions` again only when the paint frames or bases change.

## Page reference

- Keys: `←`/`→` step between paints, `space` plays, `d` toggles the change flashes, `l` opens the paint list drawer, `f` goes fullscreen. Clicking the video plays or pauses. Clicking or dragging the timeline scrubs, and hovering shows a thumbnail.
- URL options: `#t=6.502` deep-links to a time, and `?hold` freezes the boxes, which helps with screenshots.
- "Shown" is the time until the next paint.
- The folder is portable: `index.html`, `recording.*`, `paints/`. `meta.json`, `paints.json`, `regions.json` and `sheets/` are inputs and debug output, safe to keep.

## Reporting back

Summarize the phases, the key metrics, and anything notable (blank screens, layout shifts that the diff shows as moves, long waits). Give the path to `index.html`. Mention the t=0 caveat, and that times are accurate to ±1 frame.
