---
name: seenry-video
description: "Direct and render short product films as code: launch videos, feature explainers, tool and agent demos, social cuts. Studies launch videos and recordings in Seenry for pacing, writes the story, shot list and voiceover, builds a seekable HTML film from real captures, renders it frame by frame, designs and mixes the sound, and checks format, loudness and every on-screen claim. Not for editing live-action footage."
license: Apache-2.0
metadata:
  author: Seenry
  version: "0.1.0"
---

# Direct the film, then render it

A good product film proves one thing. Everything in it, picture, words, music and cuts, serves that proof, and every fact it shows is true. The film is built as a web page whose every frame is a pure function of time, rendered by seeking frame by frame. That makes it exact, repeatable and editable like code: change a number, re-render, and the cut is identical except for that number.

Use this for 6–90 second films about a product: launches, feature reveals, "how it works" explainers, MCP and agent demos, social cuts. For interface motion inside a product use [seenry-motion](../seenry-motion/SKILL.md); for the page or product being shown use [seenry](../seenry/SKILL.md).

## The standard

- **One claim, proven on screen.** Write the sentence the viewer should repeat afterwards. If a scene does not move toward proving it, cut the scene.
- **Real over representational.** Real product UI, real captures, real numbers, real sound recordings or deliberately designed sound. Never a fake dashboard, invented metrics or stock "tech" visuals.
- **True, or labeled.** Every number, quote, tool call and product behavior on screen is either captured evidence or clearly an illustration. Record each in `claims.json` as you build. If the product does not do what the film shows, change the film, or build the feature first.
- **Cut on the music.** Pick the tempo first; scenes start on bar lines, hits land on beats, and the voice sits between them. 120 BPM gives a 2-second bar, which is easy to reason about.
- **Sound is designed, not decorated.** Music ducks under the voice, effects mark real events (a value landing, a page arriving), and the mix is mastered to −14 LUFS. Silence is a tool.
- **Readable at a glance.** On-screen text stays up long enough to read twice (about 0.3s per word plus 1s), is at least 28px at 1080p, and is never smaller than the thing it describes.

## The flow

1. **Brief (`brief.md`).** The claim, the proof, the audience, where it plays and at what size (16:9 1920×1080 for sites and X; 1:1 or 4:5 for feeds; 9:16 for stories), the length (social 8–15s, launch 30–60s, explainer up to 90s), voice or no voice, and what is fixed (brand, product state, legal lines).
2. **Study references.** Follow [research](references/research.md): find launch videos and recordings in Seenry, watch them at normal speed, pull frames at their cuts, and write `study.md` with what each proves about pacing, type, transitions and sound, and what you will not take.
3. **Story and shot list.** Follow [directing](references/directing.md): beats on a bar grid, a shot list with timings, the voiceover script timed to it, and three or four storyboard stills before any animation. Show the shot list and script to the user before building when the film is for publication.
4. **Material.** Pull real captures, measurements and recordings through Seenry MCP or the product itself, and get licensed or generated imagery through [seenry-assets](../seenry-assets/SKILL.md). Add a `claims.json` row for every fact as it enters the film.
5. **Build.** Copy [the film template](assets/film/index.html) and its [cue sheet](assets/film/cues.json), [sound spec](assets/film/sound.json) and [claims ledger](assets/film/claims.json) into the project. Replace the demo scenes with your shot list. Open the page to scrub and play; export stills (`render.mjs --stills`) to check composition at full size.
6. **Sound.** Follow [sound](references/sound.md): music edited to the cut, effects on real events, the voice recorded or generated, then `mix.py` with the cue sheet. ElevenLabs generation (`elevenlabs.py`) is optional and spends the user's credits; ask before running it.
7. **Render, check and review.** Follow [review](references/review.md): `render.mjs`, `mix.py`, `film_check.py` until it passes, then `film_critic.mjs`, a blind film critic that watches the cut as a sequence beside the reference films. Apply its fixes, keep what it says to keep, and run it again. Scores are blind and fixes are written against the full history, so rounds converge. Score a reference film the same way to know the ceiling; aim for that ceiling, and when two rounds do not move the score, change the concept rather than the layout. Report the score either way. Watch it once yourself at normal speed with sound before delivering.

## Tools

All scripts are in `scripts/` and take paths relative to the film folder.

- `node scripts/render.mjs --dir film/` renders `film.silent.mp4`. `--stills 2,9.5` exports frames, `--contact 12` a contact sheet. Needs ffmpeg and Playwright with Chromium (`npm i -D playwright && npx playwright install chromium`, or `--playwright <path>`).
- `python3 scripts/mix.py film/cues.json` edits the music on bar lines, places effects by their peaks, ducks under the voice, masters to the target loudness and muxes `film.mp4`. Needs numpy.
- `python3 scripts/elevenlabs.py film/sound.json voices|vo|sfx|music` generates voice, effects and score when `ELEVENLABS_API_KEY` is set. Optional.
- `node scripts/film_critic.mjs --dir film/ --refs study/a.mp4,study/b.mp4` has a fresh model judge the film from a beat-grid storyboard with the voice under each frame, a phone-feed board and full-size shot frames, alongside measured cuts, loudness, the script and the claims ledger. It scores claim, proof, story, pacing, picture, legibility, sound with picture and truth against the references (median of three runs), names what to keep, scores blind, and writes fixes against the full history of earlier rounds so it neither repeats nor reverses them. `--dry-run` writes the boards and prompt only; `--min 8` exits 1 below the bar.
- `python3 scripts/film_check.py film/cues.json` checks duration, codec and color range, loudness and true peak, voice lines running into each other, and that every non-dramatised claim has a source.

## Never ship these

- A number, quote, tool call or product behavior on screen that was not captured or is not labeled as an illustration.
- Fake product UI built to look real, invented customer logos or metrics, AI-generated "screenshots" of the product.
- Text that is on screen for less time than it takes to read twice, or smaller than 28px at 1080p.
- Stock "AI" visuals: glowing brains, particle networks, purple gradient blobs, floating holograms, a typing cursor as the only idea.
- Music that fights the voice, effects on every frame, a whoosh on every cut, a mix louder than −13 LUFS or peaking above −1 dBTP.
- Copying a reference film's shots, music or sequence. References teach pacing and craft; the film's idea comes from this product's claim.
- A slow logo intro. Show the claim or the product in the first two seconds.

## Deliver

The film (`film.mp4`), the silent render, the cue sheet, the brief, the study, the script and `claims.json`. Report the claim the film proves, what each reference contributed, what is captured versus illustrated, the measured loudness, the film critic's scores, and anything unverified.
