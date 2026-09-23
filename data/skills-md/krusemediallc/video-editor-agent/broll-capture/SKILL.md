---
name: broll-capture
description: >
  Capture website B-roll and screenshots for a video edit: full-page screenshots of
  real pages (for shot-cards and "proof" beats), smooth scripted-scroll screen
  recordings, and high-fidelity Screen Studio recordings of the user's real browser
  for sites that block automation. Use whenever an edit needs real screenshots,
  a screen recording of a website/app, "capture the site", or B-roll of a product.
  NOT for generating graphics (branded-ad-edit cards) or editing footage.
---

# B-roll & Screenshot Capture

Three lanes, in order of effort. Real captures read as proof; recreations read as
ads — always prefer capturing the actual site.

**Every capture, whatever the lane, ends the same way:** re-encode with dense
keyframes (`-g 30 -keyint_min 30`) so seeks don't freeze in the renderer, then
frame-extract and LOOK at every take before using it.

---

## Lane A — Full-page screenshots (shot-cards, docs, blog "proof" beats)

### A1. Playwright MCP (zero code — use it if the client has it connected)

If the Claude Code session has a Playwright (or browser) MCP available:
navigate to the URL, wait for load, take a full-page screenshot, save it into
`assets/shots/`. Good enough for most shot-cards. Take at the largest viewport
available and capture more height than you need — crop later.

### A2. Scripted (bundled): `scripts/capture-shots.mjs`

Puppeteer script — edit the `TARGETS` list (name, url, capture height) and run
`node scripts/capture-shots.mjs`. What it encodes:

- Real desktop UA + 1440×900 viewport at `deviceScaleFactor: 2` (crisp 2x shots).
- A **widget killer** injected twice (cookie/consent/chat/intercom/banner/dialog
  selectors hidden with `display:none !important`) — once after load, once after
  the scroll pass, because chat widgets re-mount.
- A **lazy-load scroll pass** (step to the bottom, settle, back to top) so images
  and deferred sections are actually painted before the shot.
- Clipped full-page screenshot (`clip` to the min of wanted height vs body height).

Review every PNG. Common junk that survives: keychain popups (from a
Chrome-for-Testing profile — use system Chrome + a fresh `userDataDir` +
`ignoreDefaultArgs:["--enable-automation"]`), region banners, half-loaded heroes.

---

## Lane B — Scripted scroll recordings (clean site B-roll, 3–6s clips)

The branded-ad-edit skill's `references/design.md` §3 carries the full recipe:
kiosk system-Chrome, scripted **eased** scrolling (never native jerky scroll),
recorded or screencast, cut into 3–6s clips. Key gotchas:

- Scroll the **smallest matching node** — a text anchor can match an ancestor div
  whose scrollTop never moves (the scroll silently no-ops).
- Sweep junk selectors on an interval during the take.
- Frame-extract-review EVERY take.

---

## Lane C — Screen Studio / real-browser recording (highest fidelity, or when automation is blocked)

Some sites (Cloudflare and friends) **block kiosk/fresh-profile Chrome outright**.
The proven fallback: record the user's REAL logged-in browser.

1. **Drive the real browser** — a browser-extension MCP (e.g. claude-in-chrome) or
   the user by hand — through scripted, eased scrolls of each target page.
2. **Sync markers:** flash the page pure white for ~0.3s before each take
   (`document.body.style.filter` or an injected overlay). Markers make take
   boundaries findable in one pass.
3. **Record the display** with Screen Studio (`screenstudio-cli` if installed —
   check `screenstudio --help`) or any screen recorder. Screen Studio's polish
   (smooth cursor, auto-zoom) is why it's worth using when available.
4. **Find the markers** afterwards: invert the video and run black-frame detection —
   `ffmpeg -i cap.mp4 -vf "negate,blackdetect=d=0.1:pix_th=0.10" -f null -` — each
   detected "black" run is a white flash; cut takes between markers.
5. **Crop off the chrome**: browser toolbar and the Dock/menu bar must go — e.g. a
   1920×1080 display capture cropping to `1920×816` at `y=176` keeps only the page.
   Compute your crop from a test frame, verify by eye.
6. Re-encode dense keyframes; clip into 3–6s beats.

### Traps learned the hard way

- **CDP on :9222 may not be the user's browser.** Screen Studio runs its own
  embedded Chromium that can occupy the debug port (UA `ScreenStudio/…`,
  `Target.createTarget` unsupported). If an automation script suddenly sees a
  logged-out web, check WHOSE browser it attached to.
- Inner-container scroll areas (docs sites) often defeat page-level scrolling —
  takes come out static. Target the container, or skip that page.
- Never enter credentials for the user; if a login wall appears, hand the browser
  to them and resume after.

---

## Where captures go

`assets/shots/*.png` for stills, `media/broll/*.mp4` for clips. In compositions,
stills usually display as a **sharp card floating over a blurred blow-up of
itself**, or inside a browser-chrome frame (see branded-ad-edit
`references/design.md`).

### More traps (profile captures, 2026-09)

- **A TypeScript runner can poison `page.evaluate`.** tsx/esbuild injects a `__name` helper
  into any function it serialises; inside the page that helper does not exist and the
  evaluate throws `__name is not defined`. Pass page scripts as **strings**, not functions.
- **Some platforms never render their grid for automation** (TikTok: "Something went wrong",
  survives Refresh clicks and long waits). The profile header still renders — take the still,
  and carry the scrolling beat with another platform's grid.
- **A screencast that "worked" can be static.** Instagram's grid lives in an inner scroll
  container; page-level `scrollTo` no-ops and every frame is identical. Frame-tile every take
  before using it — the tile is how this was caught.
- **Check the handle before blaming the tool.** Two 404s were a handle mismatch (the
  creator's handle differs by a dot between platforms), not blocking.
- **An authenticated dashboard capture can violate a client rule.** An Ads Manager screenshot
  shows real account IDs and campaign names; treat it as unusable unless cropped to chrome.
