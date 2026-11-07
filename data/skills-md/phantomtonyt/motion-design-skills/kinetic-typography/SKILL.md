---
name: kinetic-typography
description: Kinetic typography videos where big words are the visuals - slamming, stretching, stacking, splitting and swapping in time with a voiceover or music beat - rendered to MP4 at 9:16 or 16:9. Use for text-only explainers, hooks and title sequences, quotes, lyric or poem videos, announcements and word-by-word captions as the main design. Not for subtitles over other footage (use the platform's caption tools) or long reading-heavy slides (use data-story-charts or system-diagram-animation).
license: MIT
compatibility: HyperFrames (Node 22+, FFmpeg) with GSAP. Fonts from Google Fonts.
---

# Kinetic Typography

Make videos where the words themselves are the picture. A phrase lands, fills the frame, gets punched and is replaced by the next one, in rhythm. It should feel bold, fast and musical, like a poster that moves.

## Options

| Option | Default | Notes |
|---|---|---|
| format | vertical 1080×1920 | or landscape 1920×1080, square 1080×1080 |
| duration | 10–20 s | match the voiceover or the song section |
| tone | punchy | `calm` (slides and fades of 0.4 s, fewer flips), `punchy` (default), `chaotic` (all caps, slams, shakes, a flip on every other phrase) |
| rhythm | fixed tempo | or voiceover word times, or music beats |

## Brief (answer before planning)

1. What is the one sentence the viewer should remember?
2. Split the script into phrases of 1–4 words; mark one hero word per phrase.
3. Where does the energy peak (the phrase that gets the colour flip)?
4. What is the ending lockup (title, call to action, handle)?

## Reads sheet (write it with the beat list)

For every beat, write the one thing the viewer must understand ("the robot can't fly", "the cache missed") and how long it stays readable. One read at a time. Text floors: a label stays at least 0.8 s, a sentence about 0.3 s per word once fully on screen. If the text won't fit the time, cut words rather than speed up.

## Motion discipline

- Motion is causal: every move has a reason on screen (a click, a fall, a packet arriving), and the next move follows from it.
- Pick one main direction of travel for the whole video and keep it. Use the other directions for meaning: up for success or conclusion, a zoom out for "here's the whole picture".
- A scene's exit sets up the next entry: same axis, same direction, similar speed. Carry one object across the change instead of crossfading.
- No idle filler motion (floating, breathing, wobbling) on diagrams, charts or text. If nothing should move, hold still; one deliberate camera drift is enough.
- Easing: smooth ease-out for entries (`power2.out` to `power4.out`), quicker ease-in for exits (about 75% of the entry time). Entries at most 0.8 s. Total stagger for a group at most 0.5 s. Overshoot (`back.out`) only for small pops; no elastic or bounce.
- One thing moves at a time when it matters; the eye can follow only one.
- Add a 0.3–0.75 s beat of stillness right before the payoff.

## Style rules (always)

These make it this style; keep them whatever the colours or words.

1. Type fills 50–80% of the frame width, because small text reads as captions, not as the visual.
2. One idea on screen at a time: 1–4 words, at most 3 lines. Everything else has left.
3. Every word arrives with a move (slam, slide, stretch, mask reveal, flip). Nothing simply fades in.
4. Changes land on a rhythm: a new word or move every 0.25–0.7 s, and keywords on the beat or the stressed syllable.
5. Contrast is extreme: near-black on off-white or the reverse, plus one accent colour for the key word only.
6. Each phrase gets one hero word: biggest, accent-coloured, or moving differently from the rest.

## Defaults (change freely)

Fonts, colours, words, timing and background. If the user gives brand fonts or colours, theirs win. Precedence: user's brand or spec, then the explicit request, then these defaults.

- Background `#111111`, text `#f4f1ea`, accent `#ff4d2e`. Flip to light-on-dark or dark-on-light per phrase for energy.
- Display font: a heavy condensed face (Anton, Bebas Neue or Archivo Black), all caps for hero words. Support font: a heavy sans (Inter 800) for small connecting words.
- Size: hero words 180–320 px in 9:16; small words 60–90 px.

## Setup (once)

```bash
node -v                      # needs 22+
ffmpeg -version
npx hyperframes init my-video --non-interactive --resolution portrait && cd my-video   # landscape for 16:9
```

Inside an existing empty folder use `npx hyperframes init . --non-interactive --resolution portrait`, then replace the generated `index.html` with the template below.

## Decide before building

State these back to the user in one line before writing code.

1. **Aspect:** 9:16 (1080×1920) or 16:9 (1920×1080). Default is 9:16.
2. **Words and timing:** split the script into phrases of 1–4 words. With a voiceover, take times from its word timestamps (`npx hyperframes transcribe voice.wav`). Without one, give each phrase 0.6–1.4 s, and give hero words longer.
3. **Rhythm source:** voice (land on stressed syllables), music (land on beats; `npx hyperframes beats music.mp3`), or a fixed tempo (e.g. 120 BPM = a beat every 0.5 s).
4. **Hero word per phrase** and which move it gets.

| Need | HyperFrames + GSAP (default) | Remotion |
|---|:-:|:-:|
| Word and letter moves, masks, stretches | yes | yes |
| Timing from voice or beat data | yes (labels) | yes (frames) |
| Runs with only Node and FFmpeg | yes | yes |
| Licence | free | free up to 3 people, paid above |

## Move vocabulary

| Move | How (GSAP) | Use for |
|---|---|---|
| Slam | `from {scale: 2.6, opacity: 0}`, `expo.out`, 0.22 s, plus a 6 px screen shake for 0.1 s | hero words |
| Slide stack | lines `from {yPercent: 110}` inside `overflow:hidden` masks, stagger 0.06 s, `power4.out` 0.35 s | lists, two-line phrases |
| Stretch | `scaleY: 1.6 → 1`, `transformOrigin: bottom`, `back.out(3)` 0.3 s | emphasis, verbs |
| Letter cascade | letters `from {y: -120, rotation: -20, opacity: 0}`, stagger 0.025 s, `back.out(2)` | names, titles |
| Flip swap | old word `rotationX: 90` out (0.12 s), new word `rotationX: -90 → 0` in (0.18 s) | X becomes Y |
| Split | word halves slide apart `x: ±140` to reveal a smaller word between | contrasts |
| Exit | `yPercent: -110` or `scale: 0.7, opacity: 0`, 0.15 s, `power2.in` | every phrase leaving |

Exits are fast (0.12–0.18 s) and entrances are snappier than you think (0.18–0.35 s). Hold each phrase at least 0.35 s after it lands, so it can be read.

## Make it eye-catching

- **Fill the frame.** Size words to the frame width, not to a font size. Condensed fonts at 250+ px are the look.
- **Colour flips:** the background swaps between dark and light (or to the accent) on 2–3 key phrases, as a hard cut on the beat.
- **Texture and depth:** a subtle grain overlay, a soft shadow or offset duplicate behind hero words (accent colour, offset 10–14 px), and an occasional giant faded word in the background.
- **Camera energy:** a slow 2–4% scale drift on the whole stage, a punch-in (scale 1.06 for 0.1 s) on hero hits, and a 6–10 px shake on slams.
- **Shapes with words:** underline bars that draw in, circles that pop behind a word, arrows. Accent colour, flat.
- **End on a lockup:** the title or call to action, fully composed, held 1–1.5 s, matching the opening frame so it loops.
- **Quality gate:** if any snapshot shows small centred text on a plain background, it isn't done.

## Build: template

```html
<!doctype html><html><head><meta charset="UTF-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@800&display=swap">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#111}
#root{width:100%;height:100%;position:relative;overflow:hidden}
#stage{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.phrase{position:absolute;left:60px;right:120px;top:270px;bottom:670px;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:0}
.line{overflow:hidden;line-height:.92;padding:0 8px}
.w{display:inline-block;font-family:Anton,sans-serif;text-transform:uppercase;color:#f4f1ea;white-space:nowrap}
.hero{color:#ff4d2e}
.flip .w{color:#fff}.flip .hero{color:#111}
.small{font-family:Inter,system-ui,sans-serif;font-weight:800;text-transform:none}
#bg{position:absolute;inset:0;background:#111}
</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="8" data-width="1080" data-height="1920">
<div id="bg"></div><div id="stage"></div></div>
<script>
// [time, lines, moveName, heroWordIndex, flipBackground?]  -- edit this list; times in seconds
const PHRASES = [
  [0.2, ["WORDS"], "slam", 0],
  [1.0, ["can", "MOVE"], "stack", 1],
  [2.0, ["LIKE", "MUSIC"], "stretch", 1, true],
  [3.2, ["one", "idea"], "stack", 1],
  [4.2, ["AT A", "TIME"], "slam", 1],
  [5.4, ["KINETIC", "TYPE"], "cascade", 1],
];
const END = 8, W = 1080 - 180;
// measure text only after the web fonts load, then build and register the timeline
document.fonts.ready.then(() => {
const tl = gsap.timeline({ paused: true });
const stage = document.getElementById("stage");
PHRASES.forEach(([t, lines, move, hero, flip], i) => {
  const p = document.createElement("div"); p.className = "phrase" + (flip ? " flip" : ""); stage.appendChild(p);
  const words = lines.map((txt, k) => {
    const line = document.createElement("div"); line.className = "line";
    const w = document.createElement("span"); w.className = "w" + (k === hero ? " hero" : "") + (txt === txt.toLowerCase() && k !== hero ? " small" : "");
    w.textContent = txt; line.appendChild(w); p.appendChild(line);
    w.style.fontSize = "100px"; const fit = Math.min(420, (100 * W) / w.getBoundingClientRect().width); // fill the width
    w.style.fontSize = (w.classList.contains("small") ? Math.min(fit, 110) : fit) + "px";
    return w;
  });
  gsap.set(p, { autoAlpha: 0 });
  tl.set(p, { autoAlpha: 1 }, t);
  if (move === "slam") tl.from(words, { scale: 2.6, opacity: 0, duration: 0.22, ease: "expo.out", stagger: 0.08 }, t)
                         .fromTo("#stage", { x: -10 }, { x: 10, duration: 0.04, yoyo: true, repeat: 3, ease: "none" }, t + 0.18).set("#stage", { x: 0 }, t + 0.34);
  if (move === "stack") tl.from(words, { yPercent: 110, duration: 0.35, ease: "power4.out", stagger: 0.07 }, t);
  if (move === "stretch") tl.from(words, { scaleY: 1.7, opacity: 0, transformOrigin: "50% 100%", duration: 0.3, ease: "back.out(3)", stagger: 0.08 }, t);
  if (move === "cascade") words.forEach((w, k) => {
    const letters = Array.from(w.textContent); w.textContent = "";
    letters.forEach((c) => { const l = document.createElement("span"); l.style.display = "inline-block"; l.textContent = c; w.appendChild(l); });
    tl.from(w.children, { y: -140, rotation: -20, opacity: 0, duration: 0.4, ease: "back.out(2)", stagger: 0.03 }, t + k * 0.15); });
  const next = PHRASES[i + 1] ? PHRASES[i + 1][0] : null;
  if (flip) tl.set("#bg", { background: "#ff4d2e" }, t).set("#bg", { background: "#111" }, next || END);   // colour flip on a key phrase
  if (next) tl.to(words, { yPercent: -110, opacity: 0, duration: 0.15, ease: "power2.in", stagger: 0.03 }, next - 0.17)
               .set(p, { autoAlpha: 0 }, next);
});
tl.fromTo("#root", { scale: 1 }, { scale: 1.04, duration: END, ease: "none" }, 0);         // slow drift
tl.set({}, {}, END);
window.__timelines["main"] = tl;
});
</script></body></html>
```

Edit `PHRASES` to change the words and times. Add moves by adding an `if (move === ...)` branch from the move vocabulary. With a voiceover, put the `<audio>` element in the root and take phrase times from its transcript.

## Parameters to expose to the user

`aspect` · `phrases` (time, lines, move, hero) · `fontDisplay` · `fontSupport` · `colors` (bg, text, accent) · `tempo or audio` · `flipPhrases` (where the background flips) · `endLockup`.

## Avoid

- Fade-ins and slow drifts as the main motion. It reads as a slideshow.
- More than 4 words or 3 lines on screen at once.
- Several accent colours. One accent, used only on hero words.
- Thin or light font weights, or script fonts for hero words.
- Text in the bottom 670 px or top 270 px of a 9:16 frame (platform UI covers them).
- Random or per-render variation. Every value must come from the timeline.

## Failure modes

| Looks like | Cause | Fix |
|---|---|---|
| A slideshow | fades, long holds, same move every time | vary moves from the vocabulary; entrances under 0.35 s; exits 0.15 s |
| Captions, not design | words too small, centred in empty space | size words to the frame width; condensed font; 250+ px |
| Messy, unreadable | too many words or moves at once | one phrase on screen; one hero word; hold 0.35 s after landing |
| Off-beat | phrase times guessed | use transcript or beat times; land hits 2–3 frames early |
| Words clipped by masks | line-height too tight for the font | `line-height` 0.92–1.0 with padding on `.line`; check snapshots |
| Wrong font in render | font not loaded | Google Fonts `<link>` in the head; check a snapshot shows the condensed face |

## Validate before the final render

```bash
npx hyperframes check
npx hyperframes snapshot --at <one time per phrase 0.3 s after it lands, plus one mid-exit>
npx hyperframes render -o renders/<name>.mp4
ffprobe -v error -show_entries stream=width,height,r_frame_rate:format=duration -of csv=p=0 renders/<name>.mp4
```

Look at every snapshot and `snapshots/contact-sheet.jpg`, and confirm:
- [ ] every phrase fills 50–80% of the width and is readable at phone size
- [ ] one hero word per phrase, in the accent colour or with a different move
- [ ] no two phrases overlap on any frame
- [ ] all text inside the safe area for the aspect
- [ ] the ending lockup is held at least 1 s and matches the opening
- [ ] size and duration match the request

## Self-critique before the final render

Score the snapshot sheet 1–10 on: hook (first second), readability at phone width, motion quality, composition, accuracy, and the "muted test" (can a viewer summarise it in one sentence with no sound?). Fix only what scores 7 or below, re-snapshot, and repeat until everything is 8 or above. If you can, have a separate read-only pass do the scoring, so you aren't grading your own work.

| Don't | Instead |
|---|---|
| Crossfade between two busy layouts | exit the old content, then bring in the new, or carry one object across |
| Make several things move at once | stagger, one focus per moment |
| Fill pauses with floating or wobble | hold still, or let the character act |
| Add particles, rainbow gradients or 3D flips for "energy" | add a stronger event: a reveal, a hit, a camera move |
| Rush text to fit the time | cut words |

## Deliver

- Poster: the strongest settled frame, baked in as frame 0 so thumbnails show it: `ffmpeg -ss <t> -i renders/<name>.mp4 -frames:v 1 poster.jpg`, then `ffmpeg -i renders/<name>.mp4 -i poster.jpg -filter_complex "[0:v][1:v]overlay=enable='eq(n,0)'" -c:a copy renders/<name>-final.mp4`.
- A 1–2 sentence caption, ready to post, that names the idea rather than the technique.
- Tell the user the phrase list with times, and which phrases to change for a revision.

## Study these

- @8co28, JIZURA, a lyric-text video generator with beat-tapped word timing: https://x.com/8co28/status/2102572322016370781
- @deedydas, an essay turned into on-screen typography: https://x.com/deedydas/status/2104151743907160546
- @stephanlivera, a type-heavy motion showreel from a one-line prompt: https://x.com/stephanlivera/status/2103315922098470926
- @deedydas, a launch video built on punchy headline slams: https://x.com/deedydas/status/2102787937482252537
- Ideas adapted (not copied) from the HyperFrames motion doctrine and faceless-explainer skills, JohnHeibel/ClaudeAnimationBase's animation guide, howseen-ai/claude-motion-design's critique loop, and latent-spaces/brag.
