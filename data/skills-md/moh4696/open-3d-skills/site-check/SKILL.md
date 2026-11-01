---
name: site-check
description: Verifies a 3D or animated web page in real headless browsers before anyone else sees it. Shoots every view, light state and scroll position at desktop, tablet and phone widths in Chromium and WebKit (Safari), measures frame time, draw calls and triangles, catches page errors, failed requests, blank WebGL canvases, horizontal overflow and reduced-motion behaviour, and builds one contact sheet. Use after building or changing any three.js, WebGL, canvas, scroll-driven or animated page, before publishing or recording it, or when someone asks "does it work", "check it on mobile", "why is it slow" or "test it in Safari".
---

# Site check

An animated page can look perfect in the one browser tab it was built in and fail everywhere else: a blank canvas in Safari, a crop on phones, a seam in a scroll film, a 40 ms frame on a laptop. This skill looks at the page the way visitors will, in several real browsers at several sizes, and reports what broke with pictures.

## Tool

`scripts/check.py` drives headless Chromium (on the real GPU) and WebKit through Playwright.

```bash
python3 scripts/check.py http://127.0.0.1:8000/ --out shots \
  --widths 1440,768,390 --browser both \
  --query "view=front" "view=aerial&light=night" \
  --scroll-steps 6 --ready "window.__ready === true"
```

| Option | Meaning |
| --- | --- |
| `--query` | Query strings appended to the URL, each shot at every width. Give pages deep links (`?view=`, `?light=`, `?step=`) so every state is reachable |
| `--widths` | 1440 (laptop), 768 (tablet), 390 (phone, emulated with touch and DPR 2) |
| `--browser` | `chromium`, `webkit` (Safari's engine) or `both` |
| `--scroll-steps N` | Also shoots N evenly spaced scroll positions, for scroll-driven pages |
| `--ready` | JS expression that is true once the page has rendered for real |
| `--wait` | Seconds to let things settle before measuring |

Output: one PNG per shot, `report.json`, and `sheet.jpg` with every shot labelled; problem shots are labelled in red. The script exits 1 if any shot had a page error, a failed or 4xx/5xx request, a blank canvas or horizontal overflow. Each shot also gets a reduced-motion pass at the widest width.

Needs Python 3.9+, `pip install playwright pillow`, and `python3 -m playwright install chromium webkit`. Serve the page over HTTP (ES modules and video seeking need it) with `scripts/serve.py DIR --port 8000`; it answers Range requests, which `python3 -m http.server` does not.

## Reading the report

- **ms per frame** is measured over 60 real frames. Under 16.7 is 60 fps; headless on a laptop GPU should sit near 16.7 (vsync), so a higher number means real cost. Compare runs with each other. If the report says the renderer is SwiftShader or llvmpipe, the GPU was not used and frame times mean nothing.
- **calls / triangles** come from `window.__app.renderer` (three.js), counted for a whole frame including every post-processing pass. Expose the renderer there so the check can see it.
- **ready_s** is how long the page took to set its ready flag. Over 3 s on a fast machine means the loader is visible for too long on a phone.
- **blank canvas** means a visible canvas was one flat colour: a WebGL context that failed, a shader that did not compile in that browser, or a frame drawn before assets loaded.

## Then look

The numbers catch breakage; your eyes catch ugliness. Open `sheet.jpg` and check each shot for:

- The subject cropped or tiny on the phone shot. 3D scenes should widen their vertical field of view on portrait screens; layouts should restack.
- Text over busy imagery without contrast.
- UI covering the subject, or sitting under the phone's home indicator.
- Lighting states that crush to black or clip to white.
- WebKit shots that differ from Chromium: colour (Safari ignores some colour-space hints), missing transparency (VP9 alpha video does not play in Safari), fonts.

## Checks the script cannot do alone

Run these by hand or with `frame-capture` at a low frame rate (`--fps 8`), which is fast and exact:

- **Seams and loops.** Scrub every scroll film up and down fast; watch each join and the wrap of every loop. `scroll-film/scripts/prep.py seams` scores joins numerically.
- **Pins release.** At the end of every pinned section the page must scroll on without a jump.
- **Long sessions.** Leave the page running for a minute, switch light presets back and forth, resize the window a few times; frame time should not creep up (leaked geometries and textures show in `report.json` as rising counts).
- **Throttled first load.** With network throttling, the first paint should be the hero's poster or first frame, not a blank page.
- **Interaction.** Orbit, zoom, hover states, keyboard focus on every control, and touch on a phone.

## Environment traps

- An embedded browser preview that is hidden, or a background tab, throttles or freezes `requestAnimationFrame`. A page that "does not animate" there may be fine. Headless browsers do not have this problem.
- `python3 -m http.server` ignores Range requests, so videos cannot seek and scroll-scrubbed video freezes. Use a server that answers them.
- A missing Playwright browser build after an upgrade: the script falls back to any Chromium in the Playwright cache; `CHROME_PATH` overrides it.

## Report back

Lead with what is broken, ranked by how many visitors it hits: errors and blank canvases first, then phone layout, then Safari differences, then performance, then polish. Attach the contact sheet. Say what was not checked (no real phone, no Windows GPU, no slow network) rather than implying it was.
