---
name: workflow-progress-screenshots
description: Show the user real screenshots of the work as it progresses, without being asked. Capture the start, the key moment and the result of every visual change, send them as files with captions as soon as each is ready, and look at every image before sending it. Use on any task with a visible result (UI, pages, games, 3D, charts, motion), when the user says "show me", "screenshots", "keep giving me screenshots" or "where are the screenshots?", and before any report that claims a visual change works.
---

# Workflow: progress screenshots

The user judges visual work by looking at it, and asks for screenshots in almost every thread:
- "keep giving me screenshots"
- "send screenshots every pass"
- "can you give me screenshots of those?"
- "I still don't see the screenshots. Where are they?"

Describing a change is not showing it. **A screenshot mentioned but not sent doesn't count.**

## Rules

1. **Send, don't describe.** Use the host's file-sending tool (`SendUserFile`, or an inline image in the report) so the picture is in front of the user. A path in a sentence is not enough.
2. **Unasked, and as you go.** Send a picture after each meaningful pass, so the user can redirect early:
   - the first working version;
   - each big fix;
   - each round of a scoring loop.

   Don't hold them all for the final report. Don't flood them either: one small batch per pass, not every save.
3. **Start, key moment, result.** For any change with a before and after, capture all three with the same framing: the state before, the interaction (hovering, aiming, mid-animation, the panel opening), and the outcome. For fixes, show the bug, then the fix.
4. **Real renders only.** Capture the actual page, game or app, not a mockup or an idea of it. Set up the state with a review fixture, a URL flag or a debug hook, rather than describing it.
5. **Look at every image before sending.** Things that mean recapture:
   - stray toasts or hover pins;
   - half-loaded art or missing fonts;
   - the wrong scene, or stale numbers.

   If the picture doesn't show what the caption claims, it isn't evidence.
6. **Caption what it proves.** One line per picture: what changed and what it verifies. For example, "Before: the hint reads 'out of range'. After: '90% hit · 5 damage'."
7. **Label honestly.** Say "headless browser capture" or "browser viewport". A 390×844 viewport is a phone-sized browser check, not a device test. Scripted or staged moments are named as staged.
8. **Same framing for comparisons.** Use the same viewport, camera and state for before and after. Put them side by side with `compare.py`.

## How to capture

- **The in-app browser pane** is fine while it's visible. A hidden pane stalls `requestAnimationFrame` and returns stale or black frames, so use headless capture then.
- **Headless:** `scripts/capture.mjs <url> <out.png>`, with `WIDTH`/`HEIGHT`, `MOBILE=1`, `WAIT_FOR="<ready expression>"`, `SETTLE=<ms>`, and JS steps to click, open or scroll. It prints page errors, so a broken page gets caught instead of photographed.
  - 1600×900 for desktop, `MOBILE=1` for a 390×844 phone viewport.
  - `SETTLE=3000`–`5000` for WebGL or 3D scenes; they render slowly headless, and an early shot misses models, fonts and icons.
  - Run captures one at a time. Parallel headless Chrome on a busy machine gives protocol errors and missed frames.
- **Side by side:** `scripts/compare.py out.jpg before.png "Before" after.png "After"`, or three panels for start, key moment and result.
- **Motion:** a still misses what moves. Take a short burst of frames through the effect, and slow the page clock if the app exposes one. Or send a strip of frames.
- If the project names a specific capture tool (for example "use the Codex browser"), use it.
- Keep capture scripts and output in a gitignored folder inside the project (such as `qa/captures/`), not a scratchpad the app wipes on restart.

## In the final report

- The screenshots go inline, each with its caption, after the summary of what changed.
- Say which were headless captures, and which viewport a phone check used.
- If something couldn't be captured, say so and why. Don't substitute a description.
