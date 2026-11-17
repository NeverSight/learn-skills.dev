---
name: product-demo
description: "Record a short, polished product demo video of the running app for social media, ScreenStudio-style — the real UI in a rounded window on a soft wallpaper, a drawn cursor that glides, hovers and clicks like a hand would (arrow over content, pointing hand over anything clickable, a ripple on click), captured frame by frame at 2x and encoded to a square (or any aspect) MP4 with a poster frame. Use when asked to record a demo, a walkthrough, a screen recording, a \"video of the modal/page/flow\", a clip for X/LinkedIn/Product Hunt, or anything \"like ScreenStudio\" of the product's own interface."
---

# Video demo

Every file this skill uses ships in its own folder, next to this SKILL.md, and paths here are relative to that folder. It needs nothing from other skills or other folders, so don't go looking for them. Unless the user names another place, save everything it makes in `out/product-demo/` under the current project.

Output: a **10–40 second MP4** (square 1080×1080 by default) of the real app being used, plus a poster PNG. Nothing is faked: the recorder drives the actual running app with a real mouse and keyboard; only the cursor, the window chrome and the wallpaper are drawn.

Example: `references/run-modal-frame.jpg`, a frame from a take of Paralect Agent in `references/run-modal.mjs` (open the Run modal, click each category on the left, hover the cards in it, 30s).

## How it works

`scripts/record.mjs` opens the app in an iframe inside a stage page served from the app's own origin (so sign-in and storage carry over), draws the cursor on top, and takes a screenshot per frame at 2x. A **take** — a small JS module you write for the video — scripts what the cursor does with a handful of verbs (`hover`, `clickOn`, `sweep`, `type`, `wheel`, `hold`). Frames are stitched with ffmpeg.

CSS transitions are slowed to the per-frame capture cost, so hover states and dialog open animations land on the right frames instead of flashing by. Cursor paths are eased with a slight bow and small, seeded random offsets, so it reads as a hand and re-renders identically.

## Rules

1. **Real product, real state.** Record the running app with real data where it looks good. Pick a project/account/page whose background is calm and doesn't leak anything private (task titles, emails, credentials). Never put credentials in the take file: read them from env (`DEMO_EMAIL`, `DEMO_PASSWORD`) or the project's screenshot notes.
2. **One idea per video.** Open one thing, show what's in it, end where you started. 10–40 seconds. Every hover dwells long enough to read (~350ms), every click settles (~200ms) before the next move.
3. **The cursor is the narrator.** It moves like a hand: eased, never in straight lines, aimed a little off-center. It hovers cards on their preview, rows on their left third, buttons on their label. Skip hovering things that don't respond to hover.
4. **Presentation tweaks only, never product changes.** Injected CSS may hide carets and scrollbars (done by default), pin a dialog's height so it doesn't jump between sections, or hide a dev-only banner. Don't restyle the product.
5. **Square by default** (1200×1200 canvas → 1080×1080). Landscape for a wide page (`--width 1600 --height 900`), portrait for a mobile flow (`--width 900 --height 1600`). The window fills the canvas minus `--pad` on every side.

## Steps

### 1. Find the app and the way in

- Which app, which port, what URL shows the thing to demo. Verify the port serves this app (`curl -s localhost:<port> | head`), other local servers answer on `localhost` too.
- How to sign in: an env var pair (`DEMO_EMAIL`, `DEMO_PASSWORD`). Sign in inside `prepare(page)` on the real origin; saved storage states go stale when the app rotates refresh tokens.
- What to show: the elements' selectors (roles and labels are most robust: `getByRole("button", { name: "Run" })`), the container that scrolls, and which items respond to hover. Buttons whose labels hide at narrow widths need an icon-based selector or a wider canvas.

### 2. Write the take

`out/product-demo/takes/<name>.mjs` in the project (create the folder):

```js
export const url = "http://localhost:3000/app/page";   // the page to record

export async function prepare(page) {                  // optional: sign in on the real origin
  await page.goto("http://localhost:3000/login");
  await page.getByPlaceholder("Email").fill(process.env.DEMO_EMAIL);
  await page.getByPlaceholder("Password").fill(process.env.DEMO_PASSWORD);
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL((u) => !u.pathname.startsWith("/login"));
}

export const css = ``;                                 // optional: presentation-only CSS for the app

export async function ready(t) {                       // optional: wait for the app; default 1.5s after network idle
  await t.frame.getByRole("button", { name: "Run" }).waitFor();
  await t.page.waitForTimeout(1200);
}

export async function still(t) {                       // optional: the state to check with --still
  await t.frame.getByRole("button", { name: "Run" }).click();
  await t.page.waitForTimeout(1000);
}

export default async function take(t) {
  await t.hold(500);                                            // settle on the resting state
  await t.clickOn(t.frame.getByRole("button", { name: "Run" }), { settle: 500 });
  await t.sweep(t.frame.locator("[role=option]"), {             // hover the visible cards in order
    within: t.frame.locator("[role=listbox]"), max: 4,
  });
  await t.clickOn(t.frame.getByRole("button", { name: "Content", exact: true }));
  t.poster();                                                   // this frame becomes the PNG
  await t.moveTo(t.width * 0.6, t.height * 0.5, { ms: 700 });   // drift off and hold to end
  await t.hold(900);
}
```

`t` gives you:

| Verb | What it does |
|---|---|
| `t.frame` / `t.app` / `t.page` | The app as a Playwright `FrameLocator` / `Frame`, and the stage page. Locators come from `t.frame`. |
| `t.hold(ms)` | Stay still. |
| `t.moveTo(x, y, { ms, bow })` | Glide to a canvas point (duration from distance unless `ms`). |
| `t.hover(target, { fx, fy, dwell, ms })` | Glide to a point inside a locator or box (`fx`/`fy` are fractions, default center) and dwell (360ms). |
| `t.clickOn(target, { fx, fy, dwell, settle })` | Hover briefly, press with a ripple, wait `settle` (180ms). |
| `t.click()` | Press where the cursor is. |
| `t.sweep(items, { within, max, dwell, fx, fy })` | Hover each item fully visible inside `within`, in DOM order. |
| `t.type(text, { perChar })` | Type with a human cadence into whatever is focused. |
| `t.wheel(dy, { ms })` | Scroll with the wheel at the cursor. |
| `t.visibleBoxes(items, { within, max })` / `t.box(locator)` / `t.aim(box, fx, fy)` | Geometry, when you need to plan a path yourself. |
| `t.poster()` | Mark the current frame as the poster PNG (default: the middle frame). |
| `t.width`, `t.height`, `t.pad`, `t.fps`, `t.position`, `t.random()` | Canvas facts and seeded randomness. |

Pacing that reads well: 500ms before the first move; the first click ~1.5s in; 350–420ms hover dwell on cards, ~280ms on list rows; 150–200ms settle after a click; end with a 700ms drift away and a 900ms hold so a loop doesn't snap.

### 3. Check the framing

```bash
node <this skill folder>/scripts/record.mjs --take out/product-demo/takes/<name>.mjs --out out/product-demo/<name> --still
```

Look at `<out>.png`: the window filled with the app, the thing to demo readable, the cursor shape right (hand over clickable things). Adjust `--width/--height/--pad`, the URL, the `css`, or the selectors before spending minutes on a take.

### 4. Record

```bash
DEMO_EMAIL=… DEMO_PASSWORD=… node <this skill folder>/scripts/record.mjs \
  --take out/product-demo/takes/<name>.mjs --out out/product-demo/<name>
```

A 30s take at 2x takes ~8–10 minutes (each frame is a full 2x screenshot). Run it in the background and keep working. Options: `--width 1200 --height 1200`, `--pad 40` (0 = no window chrome), `--wallpaper warm|cool|dark|plain`, `--fps 30`, `--out-width 1080`, `--seed 1`, `--keep-frames`.

Needs ffmpeg. Playwright installs into this skill's `scripts/` folder on the first run, with its Chromium if none is found.

### 5. Review

```bash
ffmpeg -y -loglevel error -i out/product-demo/<name>.mp4 \
  -vf "select='not(mod(n\,40))',scale=300:-1,tile=8x3" -frames:v 1 sheet.png
```

Look at the sheet and at a few full frames around a click (`-vf "select='eq(n\,45)'"`):

- The first frame is a calm resting state; the last frame ends where the video started or on a coherent state.
- Every hovered item shows its hover state; the cursor is a hand over it and an arrow between items.
- Clicks show the ripple and the state change on the very next frames; nothing is mid-transition for more than 2–3 frames.
- No caret blinking, no scrollbars, no private data in the background.
- Nothing jumps between steps (a dialog changing height, a layout shift from a late load). Pin it with `css`, or wait for it in `ready`.

## Output

Tell the user:

- the files: `out/product-demo/<name>.mp4` (size, duration) and `out/product-demo/<name>.png`
- what the take shows, step by step, in a few lines
- the take file and the exact command to re-render (with the env vars named, not their values)
- anything presentation-only that was injected (pinned heights, hidden banners)
