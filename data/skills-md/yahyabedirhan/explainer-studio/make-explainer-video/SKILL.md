---
name: make-explainer-video
description: Make a narrated explainer video about a project, feature or idea in the local explainer studio. Use when the user asks for an explainer, walkthrough or animated video, or wants a studio video changed.
---

# Make an explainer video

Make a narrated explainer video about a **source project**, the project the user wants explained, with the explainer studio, [yahyabedirhan/explainer-studio](https://github.com/yahyabedirhan/explainer-studio). The source project is read-only: read what explains the subject, such as its code, docs and its own pull requests, and write nothing into it.

A video is a stack of **layers**. Each layer has options, and the video uses one option per layer. A **preset** is a named set of choices. Start from a preset, or choose each layer yourself.

## Parameters

- `<studio>`: a checkout of the studio, e.g. `~/Developer/<owner>/explainer-studio`, or any worktree of it.

## Layers

[references/layers.md](references/layers.md) says how layers combine.

| Layer | Options | Choose |
|---|---|---|
| Renderer | [`remotion`](references/renderer/remotion.md), [`fframes`](references/renderer/fframes.md) | one |
| Drawing | [`dom`](references/drawing/dom.md), [`canvas`](references/drawing/canvas.md) | one or both, scene by scene; `remotion` only |
| Look | [`dark-ui`](references/look/dark-ui.md), [`paper-blueprint`](references/look/paper-blueprint.md), [`paper-havooch`](references/look/paper-havooch.md), [`pixel-thermal`](references/look/pixel-thermal.md) | one |
| Effects | [`grain`](references/effects/grain.md), [`shaders`](references/effects/shaders.md) | none, one or both |
| Captions | [`on`, `off`](references/captions.md) | one |
| Voice | [`kokoro`](references/voice/kokoro.md) | one |
| Sound | [`synth`, `none`](references/sound.md) | one |
| Optional steps | [`reference-study`](references/steps/reference-study.md), [`process-page`](references/steps/process-page.md) | none, one or both |

## Presets

- [`studio`](presets/studio.md): products, interfaces, data and architecture, with real UI and bold type.
- [`sketchbook`](presets/sketchbook.md): a concept or process in under a minute, drawn on paper and blueprint.
- [`havooch`](presets/havooch.md): a video about Havooch, the sketchbook in Havooch's colours with Havuç the cat.

## Steps

1. **Open the studio.** Work in `<studio>`. Every checkout and worktree shares one videos root; [references/videos-root.md](references/videos-root.md) says where a video's files go.
   - **When there's no clone:** clone the studio to `<studio>`, run `npm install`, `npm run setup:voice` and `npm run setup:skills`, and render the README's smoke-test video once to confirm it works. It needs `ffmpeg` and `espeak-ng`.
   - **When `.claude/skills/remotion-best-practices/` or `fframes-video` is missing:** run `npm run setup:skills`.
2. **Learn the subject.** Read the source project until you can explain what the user asked about, end to end.
3. **Ask once.** Ask in a single round, and only what the request and the project leave open: what the viewer should take away, the length, the preset or the layer choices. When nothing is open, ask nothing. Then work to the MP4 with no more check-ins. The one exception is the `shaders` effect: the user picks each effect from a prototype sheet in step 7.
   - **When nobody can answer**, such as when you run as a sub-agent: decide, and write each decision into the brief.
4. **Scaffold.** `npm run new-video -- <project>-<topic>` creates `<root>/<slug>/` and prints its path. Pass `--fps <n>` when the preset or the brief sets one.
5. **Choose the layers.** Take the preset's choices, then apply the user's changes. Check each option's needs in its reference. Write the choices into the brief's Choices lines, and read the reference of every chosen option.
   - **When the look has no code for the chosen renderer or drawing:** follow "A look in a new renderer" in [references/layers.md](references/layers.md).
   - **With `reference-study`:** do it now, before the brief.
   - **With `process-page`:** from here on, end every step with a snapshot, as [references/steps/process-page.md](references/steps/process-page.md) says.
6. **Brief and script.** Fill `<root>/<slug>/brief.md`: the goal, the audience, the length, the look notes, one line of narration per scene, and every asset the scenes show. Kokoro speaks about 2.5 words a second, so budget the words against the length. Write for the ear: [references/pronunciation.md](references/pronunciation.md).
   - Done when each scene has its line, and every sentence names something that appears or moves on screen.
7. **Asset sheet.** Draw every character, prop, UI mock and diagram element on one still: `<root>/<slug>/Sheet.tsx` in Remotion, a frame of the project in FFrames (the renderer reference says how). Look at it, and fix what collides, reads badly or overflows.
   - **With `shaders`:** draw the candidate effects on the sheet, and let the user pick: [references/effects/shaders.md](references/effects/shaders.md).
   - Done when every asset in the brief is on the sheet and reads at a glance.
8. **Voice.** Put the narration in `voiceover.json`, one scene per line, and run `npm run voice -- <slug>`. Find each cue word in the scene's `words`.
   - Done when every scene has `durationSeconds` and `words`, and the total is within about 10 % of the length.
9. **Storyboard.** Build each scene at its end pose, with no motion yet, and render a still of its last frame. Fix overlaps, text outside its shape and empty halves of the frame.
   - Done when every end pose reads as the brief says.
10. **Animate.** Add the motion. Cue every reveal on the narration word it shows. Run the sound layer with the final length, then place the music and the sound effects, and add the effects the choices name.
   - Done when every reveal has a word cue, and `npx tsc -p "$(npm run --silent root)"` passes (in FFrames, `cargo build`).
11. **Check and render.** Look at stills at key frames, then render the MP4 to `<root>/<slug>/out/<slug>.mp4`, as the renderer reference says. Look at a contact sheet of the render (`npm run sheet -- <slug>`; add `--every 0.125` for a video under 15 seconds) and at stills two or three frames after the cues. For fast motion, render four stills a few frames apart. Look for:
   - a reveal off its word, or something appearing with no cue;
   - a stretch where the voice talks and nothing moves;
   - text outside its box, overlaps, a trail left after a flight;
   - a rotation fast enough to look frozen.
   - Done when a round of stills and the sheet finds none of these.
12. **Final checks.** Run `ffprobe` on the MP4.
   - Done when the frame count equals the summed scene frames, the size and fps match `config.ts`, and there is an audio stream.
   - **With `process-page`:** build the page now.
13. **Hand over.** Give the user the full path of the MP4 and of anything they asked for, the choices the video used, and `npm run dev` in the studio to preview or tweak it.

## Rules

- **Timing comes from the voice.** Scene lengths come only from `voiceover.json` after `npm run voice`; every reveal is cued on a spoken word. Type no scene length and no guessed cue frame.
- **One scene per file.**
- **Look before you finish.** A render command that succeeds proves nothing: look at the stills, the sheet and the `ffprobe` output.
- **Small edits for feedback.** Change the part the user named, and keep the rest.
- **Free and local.** No paid APIs and no keys. Draw art in code first. When code can't draw it, use a freely licensed file and note its source and licence beside it.
- **Videos stay private.** A video's files stay in the videos root. Commit only studio code, never a video's files.

## Where the official skills differ

Use the official skill of each tool for the tool itself: Remotion's skills (`.claude/skills/remotion-best-practices/` and the references it routes to) and FFrames' `fframes-video`. Where one of them disagrees with this skill, this skill wins. When you find a disagreement the table doesn't list, follow this skill and add a row to this table.

| Where the official skill says | Do this instead |
|---|---|
| Remotion `SKILL.md`, "Open the preview" and "Render the video": start Studio before building, and render only when the user asks | Finish with steps 11 and 12: stills you've looked at, then the MP4, checked with `ffprobe`. Start Studio (`npm run dev`) when the user asks to watch. |
| Remotion: render or take a still with `npx remotion render` or `npx remotion still` | `npm run render -- <slug>` and `npm run still -- <slug> <name>`, which write into `<root>/<slug>/out/`. |
| Remotion: write scene lengths as literal numbers | Lengths come from `voiceover.json` through `@studio/lib/timing`. |
| Remotion `remotion-markup/voiceover.md`: ElevenLabs, ask for an API key, size the composition with `calculateMetadata` | Kokoro through `npm run voice`, which needs no key. Lengths as above. |
| Remotion `remotion-markup/sfx.md`: `remotion.media` URLs, search the internet | Sound files are local, in the video's `assets/`: [references/sound.md](references/sound.md). |
| Remotion `remotion-markup/REFERENCE.md`: make components editable with `Interactive.withSchema` and `Interactive.Div` | Plain JSX components and `<div>`s. |
| Remotion `remotion-captions/`: transcribe with Whisper, show a copied caption element fed an inline array | Captions are the script: [references/captions.md](references/captions.md). |
| `fframes-video`: make a project folder of its own | The project is `<root>/<slug>/fframes/`, inside the video's folder. |
| `fframes-video`: time scenes in seconds or frames you choose | Timing comes from `voiceover.json` through `npm run fframes-sync`, which writes `src/timing.rs`. |
| `fframes-video`: voice and sound from other sources | Kokoro through `npm run voice`, and the sound layer's files. |
