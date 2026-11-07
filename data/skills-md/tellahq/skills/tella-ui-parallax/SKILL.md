---
name: tella-ui-parallax
description: Turn a real product screenshot into a parallax shot in Tella Motion, through the Tella MCP, by cutting its pieces out with masks, stacking them as depth layers over the blurred, dimmed screen, and moving one camera through them so near layers travel further, with shadows, depth blur and an optional slight 3D turn. Nothing is redrawn, so it is quick and exactly the real UI. Use when asked for a parallax product shot, a 2.5D or 3D-feeling screenshot, to make a screenshot pop or pull a piece of the UI out, or for b-roll from a screenshot. To rebuild UI that animates its interaction, use tella-ui-redraw. Builds on tella-motion-design. Needs the Tella Motion tools, which are in beta and not available in every workspace.
---

# Parallax shots from a screenshot

Cut a few pieces out of the real screenshot, lift the one that matters towards the viewer, let the rest fall back into soft focus, and move one camera through the stack. Follow `tella-motion-design`; load it first.

This skill needs the Tella MCP. If tools such as `get_timeline` are missing, follow the connection steps in the `tella` skill first. If the Tella Motion tools are missing, offer a slow `add_zoom` on the screenshot instead.

## Source

A sharp, large capture (2× if possible): the user's screenshot, a recording frame (`get_clip_frame`), or the product page (`import_from_url`). A lifted piece is shown larger than captured; if the source is small, say it will look soft. Crop it in the sandbox to read each piece's box and corner radius in image pixels.

## Layers, far to near

| Layer | Holds | Depth factor |
| --- | --- | --- |
| Ground | a brand colour or soft gradient, larger than the canvas | 0.15 |
| Screen | the whole screenshot as a window, soft shadow; blurred 2–6 px and dimmed 15–30% once a piece lifts | 0.4 |
| Panel (optional) | a larger section the hero sits in | 0.7 |
| Hero | the one piece the words are about, sharp, 1.2–1.6× | 1 |
| Foreground (optional) | a cursor, badge or notification cut from the same image | 1.3 |

One hero per shot, at most three lifted pieces.

## Build

- `addMedia` the screenshot once. Each piece is a `duplicate` of the screen node with a rect mask (`setMasks`, the piece's box and `radius`, no feather), so it sits exactly on its place.
- The lift, on the word that names it (0.6–0.9 s, long ease out): the hero scales up and moves slightly toward the centre while its shadow grows softer and further, and the screen behind blurs and dims, which also hides the hole it leaves.
- The camera: key `cam.x`, `cam.y` (and `cam.zoom` for a push) with `setCurve`. Wrap each layer in its own group and bind the group's `x` and `y` to the camera times its depth factor (`bindProperty` with `multiply`); key the lift on the piece inside, so keys and bindings never sit on the same property. The drift is slow: a few percent of the frame over the shot.
- No 3D turn unless the user asks for one; then `perspective` 1500–2500 px and `rotateY` under 8° on the screen group during the move only, flat before text must be read.
- Ground and screen larger than the canvas by the camera's travel.

Place each shot as b-roll or an overlay as `tella-ui-redraw` does, and make later shots from the first (`duplicate_motion_document`).

## Check

`get_motion_frame` before the lift (pieces exactly on their places), at the lift (hero sharp at 100%, no hole or ghost), and at the ends of the move (no edge in view); then the frames around the shot in the video.
