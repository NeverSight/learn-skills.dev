---
name: talking-head-b-roll
description: Add b-roll motion graphics to a talking-head video. Transcribes the recording with word timings, decides line by line when the speaker is shown, when a graphic is laid over them and when a full-frame graphic covers them, draws each graphic from what is actually said (numbers, comparisons, steps, key words) in JavaScript on a canvas, and renders the finished MP4 with the original sound, plus the b-roll alone with alpha for an editor. Use when someone has a recording of a person talking to camera (a talking head, a spoken explainer, a course lesson, an ad read, a podcast clip) and wants it more engaging to watch, wants b-roll, or wants motion graphics added to it.
---

# Talking-head b-roll

The user's recording is already good: the words and delivery are final. A talking head alone is dull to watch, so the film's job is to decide, for each stretch of speech, what the picture shows. The voice never stops; only the picture changes.

The recording is never cut, moved, cropped or scaled. Everything you make is a layer drawn above it: transparent where the speaker should show, opaque where a graphic covers them. `scripts/render.mjs` lays that layer over the recording and keeps its sound.

Make it in one go: don't ask questions the recording or a sensible default answers, and list what you chose when you deliver. Work in a folder that holds the recording and run the scripts from there; outputs land there. Below, `<skill>` is this skill's folder (the one holding this file).

## 1. Transcribe

```bash
node <skill>/scripts/transcribe.mjs talk.mp4            # → transcript.json, and prints every line with its start and end
```

It prints the video's size, frame rate and length (they go into the page) and the transcript split at sentence ends, with every word timed in `transcript.json`. Read the whole transcript before deciding anything. It uses local whisper.cpp when installed, otherwise `ELEVENLABS_API_KEY`; with neither, it prints how to set one up. Pauses come from the audio itself, so the gaps between sentences are where the speaker actually stops; times inside a sentence are within a few tenths of a second. A transcript can mishear a figure: if one doesn't add up with the rest of what is said, keep it off screen and say so when you deliver.

## 2. Plan: three treatments

**A. Speaker.** The video alone, nothing over it. Use where the person is the point: the opening line, a personal opinion or story, an emotional beat, the call to action, the closing line.

**B. Overlay.** The video stays visible; a transparent motion layer sits on top: a keyword or short phrase, a number counting up, an icon, an arrow, a logo, a short list building item by item. Use when a line has one concrete thing worth seeing while the speaker is still worth watching. Keep overlays toward the edges and the top or bottom third, where they will not sit on the speaker's face. One idea on screen at a time; it leaves when the line moves on.

**C. Cover.** An opaque full-frame motion scene hides the speaker while their voice carries on. Use when the line is better shown than said by a face: numbers and comparisons, a process or sequence of steps, how something works, a product or interface, anything with three or more parts. The motion should explain the line, not decorate it.

Split the transcript into lines at sentence or clause ends. Give each line A, B or C with a one-sentence reason, and say what B or C shows. Then check the rhythm:

- Open on A, so the viewer meets the person; close on A.
- No stretch of A longer than about 8 seconds; break it with B or C.
- A C stretch runs about 3–8 seconds; return to the speaker between C stretches so the film does not become a slideshow with a voice-over.
- Change treatment only at a line boundary, never mid-word. Time overlay entrances to the word they illustrate.
- Prefer fewer, clearer treatments over a change every line.

Full burned-in captions are not part of this: add them only when the user asks. A B overlay's text is a few key words, not the sentence being spoken.

Text on screen uses words the speaker actually says, or numbers and names from the transcript or the user's materials. Do not invent figures, claims or quotes.

## 3. Build the page

Copy `<skill>/templates/b-roll.html` next to the recording as `page.html` and set:

- `VIDEO`, `W` × `H` (the video's shape: 1920 × 1080, or 1080 × 1920 for vertical; a 4K file can keep a 1920 × 1080 page), `FPS`, `DURATION`, from what `transcribe.mjs` printed.
- `FACE`: where the speaker's head is (with hair, and a little room around it), as fractions of the frame. `node <skill>/scripts/render.mjs page.html face --stills 2s,20s --face` shows the recording with the box; adjust until it holds the head in every still.
- `SCENES`: one entry per B or C stretch, `{ from, to, kind: 'overlay' | 'cover', draw }`, times taken from the word timings in `transcript.json`. Everything not in a scene is A. Two scenes can meet (one's `to` is the next one's `from`); a sliver of the speaker between them reads as a flicker.
- One `draw(t, s)` per scene, written for what that line says. The template's two (a keyword card and a counting number) show the structure, not the look. `s.in` and `s.out` give the entrance and exit; `s.now` is the time in the video, to time a reveal to the word it shows.

Surfaces default to LIGHT. Go dark only when (a) the user or brand explicitly asks for it, or (b) the subject inherently lives on a dark surface (terminal/code, night sky, cinema). Neon-on-black is the cliché default of every AI video; picking it unprompted is a design failure.

Fonts: one Google Fonts `<link>` per family with the weights you use, and every face you draw with listed in `FONTS`, so nothing renders in a fallback font (rendering needs network access to load them).

## 4. Check it

```bash
node <skill>/scripts/render.mjs page.html --check                 # the plan against the transcript and the pixels
node <skill>/scripts/render.mjs page.html film.jpg --sheet 1      # the whole film, one frame a second, over the recording
node <skill>/scripts/render.mjs page.html shot --stills 12s,20s   # full frames, to read text and spacing
```

`--check` must pass: every cover hides the speaker completely once it is in, no overlay reaches into `FACE`, every scene starts and ends between words, nothing is drawn outside a scene, no text runs off the frame or onto other text. It warns when text sits within 3% of the frame's edge, where some players crop. It also prints the timeline with what is said in each stretch and warns about rhythm (a long stretch of only the speaker, a cover shorter than 3 s or longer than 8 s, covers back to back, not opening or closing on the speaker); a warning can stand when you have a reason, so say it.

It can't tell whether a graphic says what its line says, whether text is legible, or whether it runs off its card or across a line of a chart: look at the sheet for the flow and at stills of every scene for the text. Fix and look again until it holds up.

## 5. Render and deliver

```bash
node <skill>/scripts/render.mjs page.html film.mp4        # the finished film: the recording, the b-roll over it, the original sound
node <skill>/scripts/render.mjs page.html b-roll.mov      # the b-roll alone with alpha: ProRes 4444 for Premiere Pro, Resolve, Final Cut
node <skill>/scripts/render.mjs page.html b-roll.webm     # the same as VP9 with alpha: small, for browsers and OBS
```

Hand over `film.mp4`, the page (open it in a browser to play the film with sound and scrub through the scenes), and the plan as a short table: time, what is said, treatment, what is on screen. Give the alpha layer too when the user edits in Premiere Pro, DaVinci Resolve or Final Cut (the `.mov`; ProRes is large, about 5 MB a second at 1080p): it goes on the track above the recording, starting at 0. Say what you chose that they didn't ask for.

Needs: Node 18+, `npm i playwright-core` in the working folder or any folder above it (or in the skill's own folder or above), ffmpeg, Chrome (or `npx playwright install chromium`), and whisper.cpp or an ElevenLabs key for the transcript.
