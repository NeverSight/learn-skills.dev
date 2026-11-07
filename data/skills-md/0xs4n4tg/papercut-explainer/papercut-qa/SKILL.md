---
name: papercut-qa
description: Check a papercut reel's stills against the style DNA and the storyboard. Renders contact sheets at a few timestamps, runs the full checklist, then writes the delivery summary. Use for "QA the reel", "check my scenes look like paper", "is this ready to post".
---

# Papercut QA

Compare stills for style, not content, against the Style DNA and the storyboard. Run it per scene while building and once on the whole reel before the final render.

## Preflight

- Install: **Standard** or Full. Stills need a scaffolded project with Remotion, and the contact sheets need Python with numpy and Pillow (`$PAPERCUT_PY`). Missing pieces: `./install.sh --doctor`, then `papercut-setup`.
- Library: `$PAPERCUT_LIB`, else the `PAPERCUT_LIB=` line in `~/.config/papercut-explainer/config.env`, else ask once.
- Read first: Style DNA in `../papercut-explainer/references/style-guide.md` section 2, and the backdrop sheet `library/papercut/public/bg/backdrops/_sheet.jpg`. Each image costs about 0.7-1.5k tokens, so open only what the step needs.
- For density, `../papercut-explainer/references/frame-breakdown.md` ("Pacing stats" at the end): scenes average 2.8 s, 2-4 discrete visual events per scene, one every 0.4-0.8 s on a stressed word, a new caption page about every 0.6 s. Copy the density, not the content.

## 1. Render stills

From the project's `papercut/` folder:

```
$PAPERCUT_LIB/tools/qa.sh NAME FROM-TO NTH [SCALE=0.3] [COLS=9]
```

- Use 4-6 timestamps per check. For a scene, NTH is about its length in frames divided by 4. Leave `FROM-TO` out for the whole reel and raise NTH.
- The output is `out/qa/NAME_0.jpg` (and `_1`, `_2` for longer ranges), at most 45 frames per sheet. Read the sheet; keep sheets small.
- One QA command per scene, and never two renders at once. Keep fixes to two rounds per scene.
- Check against the storyboard: the scene's frame 0, its key events on their words, nothing clipped, nothing covering the banner or caption bands.

## 2. Checklist

- [ ] Every object reads as paper: grain, rough edge, drop shadow, stacked-piece shading, no outlines or gradients.
- [ ] The world camera moves smoothly. Only the banner and labels boil (stepped, subtle).
- [ ] The banner is fixed in position and taped, 3-7 words, one fact each, never repeats the VO. The banners alone read as a fact sheet.
- [ ] Every set illustrates a concrete word in its VO line, numbers are physical props, and there is one callback set before the CTA.
- [ ] Every number and UI label traces to the facts list. The script has at least one honest limitation and a feature stack of exactly three.
- [ ] Captions: one tag per word, tilted, popping on onset, pages of 1-3, in the 68-80% band, never on a face.
- [ ] Saturation only on characters, captions and signals.
- [ ] A visual event on every stressed word, with ambient motion always running.
- [ ] Cuts on banner changes (sets 1.5-3 s in tours and news, up to 5 s in a metaphor beat), bottom 20% clear.
- [ ] **The HOOK block (SAY / WRITE / SHOW / ALIGN) is on screen exactly as written:** frame 0 shows the SHOW moment mid-action with the WRITE title on it, and the first VO line is SAY.
- [ ] Every scene has a camera move, at most one page turn or tear, a tape pull or whip into the CTA, and every transition has its SFX.
- [ ] Humour pass visible on screen: one format throughout, a costume prop per idea, one struggling beat, the frame-0 prop returns changed in the CTA set, and every gag reads in under 1 s and never covers the banner, the captions or the key number.
- [ ] Vocabulary in the VO and banners matches the audience level in `SERIES.md`.
- [ ] Voiceover, captions and events are in sync (scrub the Studio at every cut).

For a failed item, fix the scene file (or the kit in the library, never `src/lib/` in the project) and re-run the one scene. Rebuild a scene with `papercut-build`.

## 3. Deliver

Open the Studio preview, list the scenes with timings, and say what is placeholder: voice, music, SFX, assets. If the voice is a placeholder, say how to re-voice it (`papercut-voice`). After posting, the numbers go to `papercut-strategy` for the autopsy.

## Principles pass

Scrub one scene at 5 fps and check against `../papercut-explainer/references/motion-principles.md`: anticipation before each big move (2), everything eased (6), something trailing after impacts (5), one focal prop (3), one exaggerated beat (10), stacked shading and a consistent shadow (11).

## Hand-off

Fixes go back to `papercut-build` (scene or sound) or `papercut-voice` (sync). A clean pass ends the reel: render with `$PAPERCUT_LIB/tools/render.sh` when the user asks.
