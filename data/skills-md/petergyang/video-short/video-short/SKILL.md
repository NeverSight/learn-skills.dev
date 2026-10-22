---
name: video-short
description: "Turn a raw talking-head recording into a finished 1080x1920 Short, Reel, or TikTok with B-roll, motion graphics, captions, and music. Shows the plan in chat, then iterates on drafts the user comments on frame by frame. Use when someone wants to edit a raw recording into a vertical video or add captions, B-roll, or motion graphics to one."
---

# Video Short

Input: a raw talking-head recording. Output: `renders/<project>-vN.mp4` at 1080x1920 and 30 fps, a 720p copy in `renders/share/` small enough to send, and the `edit.md` that produced it.

You make every editorial call; the scripts measure, render, and serve the review page. Commands, the `edit.md` format, graphics, and style keys live in [reference.md](reference.md).

On first use, run `setup.sh`. If it lists missing tools, tell the user Video Short needs them and offer to install them with the commands it prints. A Gemini API key with billing enabled is optional, for generated images, video, and music. Ask the user to save it in `~/.config/video-short/.env` rather than paste it into chat.

## 1. Cut

Make one folder per Short, named with a short slug, where the user asks, else `projects_dir` from the style file, else the current folder. Leave the recording untouched and point `Source:` at it.

Run `transcribe.py` and read every line of `work/transcript_raw.md`. The transcript keeps ums, stutters, and restarts, so retakes show in the text. When the recording is longer than the Short, such as a full tutorial, first pick its strongest 30 to 60 seconds: cuts can be one or a few ranges from anywhere in the file. Write `## Cuts` in `edit.md`:

- Keep the last complete take of any repeated line. Drop false starts, stray fillers, and dead air.
- Cut between words, never inside one; use the word times in the `.json` for a restart mid-sentence.
- Start about 0.1s before the first word and end about 0.1s after the last. Leave a natural breath after commas and list items. Never speed up the voice.

Run `cut.py --look` and read the gridded stills, taken from the kept footage, for `Framing: x, y`, the face center. A landscape recording crops to vertical around that point. Add `--grade` to compare a subtle ffmpeg grade side by side, or use `Grade: none` when the footage already looks good.

Run `cut.py`, then read `work/transcript_clean.md`. Fix any clipped word or surviving retake and run it again. All scene times use this cut timeline.

## 2. Plan

Research what the Short needs, then write `## Scenes` in `edit.md`, one row per shot, with start and end on spoken words. When the user shares a reel they like, study it first with contact sheets and cut strips for its pacing, layouts, and transitions; borrow how it moves, never its words or assets.

- **Hook in the first 3 seconds.** Ask whether a viewer would now watch to the end. Open on the hook line with the speaker or the strongest visual, and make it clear with the sound off, since most phone viewers start muted. Plant one question there that the Short answers before it ends. Close on the speaker, and when it fits, bring back the hook's visual so the Short comes full circle.
- **Layouts:** `a-roll` (full-screen speaker), `punch` (tighter speaker for emphasis), `split` (visual on top, speaker below), `b-roll` (visual full screen).
- **Keep the speaker present** for at least half the Short, and end each full-screen B-roll shot within about 3.5 seconds, because viewers connect with a face.
- **Visuals show what the words don't:** the product doing the thing, the result, the proof. Captions already carry the words. Show the real product or UI, captured from the actual screen, and mock it up only when the real one isn't available. Never invent numbers or results.
- **Everything off-camera moves.** Real footage first. Otherwise a list card that adds a row per spoken item, a `number:` that counts up to a stat the speaker says, or a `graphic:` you write for anything else, such as a flow or a before and after. Never use a still image as B-roll; an image is only the first frame of a generated video clip, or a `page:` capture that scrolls. Skip dim UI panels and waveforms, which lose viewers. When a graphic leads into a clip, end it on the clip's first frame so the cut disappears.
- **Readable and clean.** A graphic fills its panel, with text a viewer can read on a phone at a glance. Never put a card or overlay over the speaker's face. Never show another captioned video full screen under this Short's captions.
- **Pace:** Change the shot every few seconds, since a phone viewer swipes away from a static frame. Good starting points, which the script can override: the first cut within about a second, on the first strong word, and most shots around 1 to 2 seconds, with a longer hold when a demo or a key line needs time to land. When the speaker names several things in a row, give each its own clip or card row on its spoken word. Use each clip once.

Find B-roll in this order: the user's own footage, including the screen-share parts of a longer recording, then official demos and the media in posts or launch pages about the topic. Use each clip's useful seconds with `@start-end`, and `hold` its last frame instead of letting a short clip loop. Keep every line of on-screen text whole: capture web pages with `capture.py`, which reflows them to phone width, and show them as `page:` drifting down one complete section. When product UI is too small to read, `zoom` into one complete card or field rather than cropping text at the edges. Use footage the user has the right to use. Show a brand's logo only from its official file, never redrawn or generated; without one, write the name.

When the user has a Gemini key and a shot has no good footage, propose generating it: a Nano Banana image, a Gemini Omni Flash video clip, or a Lyria music bed. Generate only what the user approves, because each call costs money.

Add `## Caption fixes` for misspelled names, and `## Emphasis` for the rare term that earns a box in the caption, such as a product name or the main number, so captions stay quiet. For music, use the user's track, a Lyria bed they approve, or none. Lyria sometimes returns slow solo piano, so share a generated bed for a listen and regenerate it if it lacks the groove the user asked for. When the user names a song or artist, describe its genre, tempo, and instruments in the Lyria prompt instead of the name. When the speaker mentions the music, raise it there with `Music lift`. Leave sound effects off unless the user asks.

Show the plan in chat and wait for a go:

- One line per scene: time, layout, what's on screen, and the words spoken.
- The B-roll sources you found, with links.
- What you propose to generate, if anything, and the music.

## 3. Draft and review

Run `render.py --draft`, then `qa.py` on it, and fix anything in its frames that fails the step 4 checks, so the user's review goes to taste, not mistakes. Then run `review.py` in the background. The review page plays the draft on a timeline split into scenes. The user pauses on any frame, presses C to comment, and clicks Send. The script exits and prints each note with its time, scene, spoken words, and a still of the frame the user paused on.

Look at each note's frame, then apply every note to `edit.md`, render the next draft, and run `review.py --no-open`; the open page reloads itself. Repeat until the user clicks Looks good.

## 4. Final

Run `render.py`, then `qa.py`, and fix any failed check. Look at `opening.jpg`, `contact.jpg`, and `cuts/*.jpg` in `work/qa/`:

- Captions never cover the mouth or chin.
- Every cut lands on the right word, with no blank, frozen, or stretched frames.
- Text and clip details are readable at phone size.

You can't hear the mix, so ask the user to listen for music level and clipped words. Run [eval.md](eval.md), then share the video path, duration, and loudness.

## Style

Fonts and colors come from a style file: `--style`, then `style.json` in the project, then `~/.config/video-short/style.json`, then the bundled default. When the user gives a note about the look, offer to save it to their style file so every Short gets it.
