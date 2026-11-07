---
name: frame-capture
description: Records any web page (three.js, WebGL, canvas, GSAP, CSS animation, scroll-driven video) to a perfectly smooth 60 fps MP4 by running the page on a virtual clock, one exact frame at a time, and puts two recordings against each other as a labelled stacked or side-by-side comparison. Use when someone wants a video of a site, a demo clip for X or YouTube, a scroll-through, a showcase reel of a 3D scene, or a "model A vs model B" comparison video. Also use when a screen recording of an animated page stutters or drops frames.
---

# Frame capture

Screen recorders capture whatever the GPU managed to draw in real time, so a heavy scene stutters and a scroll-through looks hand-held. This skill records differently. Before the page's own scripts run, its clock is replaced: `performance.now`, `Date.now` and `requestAnimationFrame` read a virtual time, CSS animations and transitions are pinned to it, and every `<video>` is paused and seeked to it. Each output frame advances the clock by exactly 1/60 s, runs one frame, and takes a screenshot. A frame can take two seconds to render and the video still plays at a perfect 60 fps.

## Tools

| Script | What it does |
| --- | --- |
| `scripts/record.py` | Records a URL to MP4 with scroll keys, pointer motion and a ready condition |
| `scripts/compare.py` | Stacks two clips (or sets them side by side) with labels and rounded panels |
| `scripts/serve.py` | Static server that answers HTTP Range requests, so videos can seek |

Needs Python 3.9+, `pip install playwright pillow`, `python3 -m playwright install chromium webkit`, and ffmpeg on PATH.

## Run

1. **Serve the page with `scripts/serve.py`**, never `python3 -m http.server`. The built-in server ignores Range requests. The browser then cannot seek any video it serves (`video.seekable` is empty) and every recorded video holds its first frame. `record.py` warns when it sees this.

   ```bash
   python3 scripts/serve.py path/to/site --port 8000
   ```

2. **Make a fast timing pass first.** Ten frames a second shows the choreography in seconds instead of minutes:

   ```bash
   python3 scripts/record.py http://127.0.0.1:8000/ /tmp/check.mp4 --seconds 20 --fps 8 \
     --scroll "0:0 2.5:0 9:40% 12:40% 19:100%" --pointer drift
   ```

   Watch it, adjust the keys, repeat. Only then render the full clip.

3. **Render the final.** `--size` is the CSS viewport and `--dpr` multiplies it. `--size 1920x1080 --dpr 1` makes 1080p; `--size 1280x720 --dpr 1.5` makes the same 1920x1080 with a larger layout. Output is H.264, CRF 16, yuv420p, BT.709 tags, faststart, no audio.

   ```bash
   python3 scripts/record.py http://127.0.0.1:8000/ out.mp4 --seconds 20 --fps 60 \
     --scroll "0:0 2.5:0 9:40% 12:40% 19:100%" --pointer drift --ready "window.__ready === true"
   ```

4. **Look at the result** before handing it over. Pull frames at the moments that matter (`ffmpeg -ss 9 -i out.mp4 -frames:v 1 f.png`) and check them: first frame, every scroll stop, the last frame.

### Choreography

- `--scroll` keys are `seconds:position`. Positions are pixels (`1200`), a share of the scroll range (`40%`) or viewport heights (`2.5vh`). Segments ease (half linear, half smootherstep, so a long move never sprints in the middle). Add `~` after the time for a linear segment: `9~:60%`.
- Hold on anything the viewer needs to read: give a pinned section or a counter its own key pair with the same position.
- `--pointer drift` circles the real mouse slowly round the centre, so hover states, parallax and cursor-following rigs come alive. `--pointer 0.7,0.3` parks it.
- For choreography the page knows best (camera flights, a tour), let the page drive itself: define `window.__recordFrame = (t) => { ... }` behind a `?record=1` flag. It is called with the virtual time in seconds before each frame. `window.__recording` is true while recording.
- Smooth-scroll libraries fight a recorder that sets the scroll position. `--kill-lenis` stops Lenis from loading. For others, switch them off under `?record=1`.

## Make the page recordable

- **Time comes from `performance.now()` or the rAF timestamp, never from `setTimeout` or `setInterval`.** Timers keep real time while the clock is virtual, so a `setTimeout(next, 3000)` fires after three real seconds, which might be frame 20 or frame 400. Schedule on the page clock instead:

  ```js
  const pending = [];
  const later = (secs, fn) => pending.push({ at: performance.now() / 1000 + secs, fn });
  // in the frame loop:
  const now = performance.now() / 1000;
  for (let i = pending.length - 1; i >= 0; i--) if (now >= pending[i].at) pending.splice(i, 1)[0].fn();
  ```

- Expose a ready flag (`window.__ready = true` after the first rendered frame, textures decoded, fonts loaded) and pass it as `--ready`. Recording before assets land bakes a loading flash into frame 0.
- In record mode, hide UI that would not be in a film: hints, cursors, loaders, cookie bars.
- If WebGL frames come out black or stale, create the renderer with `preserveDrawingBuffer: true` when recording.

## Browsers

- **Chromium (default)** runs WebGL on the real GPU headless. On macOS the script adds `--use-angle=metal`, which renders at full speed; without it Chromium falls back to SwiftShader, which is correct but many times slower.
- **WebKit** (`--browser webkit`) shows how Safari renders: different font smoothing, colour handling and video decoding. Its screenshots occasionally stall at 1080p (about 1 in 100); the script retries, and because the clock is paused between steps the retry returns the identical frame.
- If Playwright's own Chromium is missing (a version mismatch after an upgrade), the script finds the newest Chromium in the Playwright cache. `CHROME_PATH` overrides it.
- Never record in a visible browser tab you are not looking at, and never in a hidden embedded preview pane. Background tabs throttle or freeze `requestAnimationFrame`. Headless does not.

## Comparisons

```bash
python3 scripts/compare.py a.mp4 b.mp4 versus.mp4 --labels "Model A" "Model B"            # stacked, for phones
python3 scripts/compare.py a.mp4 b.mp4 versus.mp4 --labels "Before" "After" --layout side   # side by side
```

A fair comparison holds everything equal except the thing being compared:

- Same viewport, same duration, same choreography (`--scroll` keys reused verbatim).
- Crop each source to its content first. Strip watermarks, webcam overlays and UI chrome the other clip does not have.
- Silent output. Two soundtracks fight, and audio steals attention from the picture.
- The shorter clip holds its last frame, so both finish together.
- Name each side honestly in its label. Put the one the audience knows on top.

## Delivery

- Social platforms re-encode everything. 1920x1080 or 1080x1920 at 60 fps, H.264, CRF 14 to 18 survives that best. Higher resolutions are often downscaled anyway.
- Keep the master. Make cut-downs (a 6 s loop, a vertical crop) from it with ffmpeg rather than re-recording.
- Add sound afterwards, timed to the frame numbers the recording printed. Never record audio through the virtual clock.
