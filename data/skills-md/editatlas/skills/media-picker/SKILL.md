---
name: media-picker
description: Find and pick B-roll (stock clips for the lines of a voice-over), background music, photos and sound effects that fit the video, and check each before it goes into the edit. Use it before calling search_videos, search_music, search_photos or search_sfx, or downloading from Pexels or Pixabay, whenever a video needs B-roll, cutaway shots or music, and when someone says a pick does not fit. Writes what each slot needs, gathers 3-5 candidates per slot, measures each with measure.py (camera shake, cuts inside a clip, what a 9:16 crop keeps, repeats; for music the tempo, intro, energy, length), looks at every frame sheet, drops what does not show the line, and has the person hear two or three music options first. Triggers include "cần B-roll cho mấy câu này", "tìm cảnh trên Pexels", "tìm b-roll", "tìm nhạc nền", "chọn nhạc nền", "nhạc nền không hay", "cảnh bị rung", "find B-roll for these lines", "find background music". Not for checking a finished render (video-check) or placing sounds on frames (sound-design).
license: Apache-2.0. LICENSE.txt has the complete terms
compatibility: Requires Python 3.9+ with numpy and Pillow, and FFmpeg with ffprobe. Needs network access to download candidates, or the files downloaded by the person. Designed for Claude Code and other agents with a shell that can read images.
metadata:
  author: EditAtlas
  version: "0.2.0"
  status: beta
  library: sfx
  mcp-tools: search_music search_videos search_photos search_sfx get_sfx send_feedback
---

# Media picker: pick music, footage and sounds that fit this video

This is media-picker 0.2.0.

The person gets music, B-roll, photos and sounds chosen for their video and their words, not the first results of a
search, and an `ASSETS.md` that says what each pick is for, why the others were dropped, and who to credit.

Three things are true the whole way through:

- **A search result is a candidate, not a pick.** Stock searches return what matches the words, in their order.
  Users have been sent a cat on a bench for "stepping on a scale", a shaky handheld pan for a calm cutaway, and a
  Christmas song for a romantic Paris ad. Every pick is measured and looked at before it goes in.
- **You cannot hear.** `measure.py` gives tempo, intro, energy and loudness; it cannot tell you whether a song feels
  right, and a track's title is not its sound. Music goes into the edit after the person has listened to it, or
  with a plain line that nobody did.
- **The person's own taste wins.** If they have a sound they use ("nhạc như các clip trước"), a channel style or a
  brand colour, that is the brief. Ask for it before searching. When they say a pick does not fit, ask what they
  disliked and whether there is music from their earlier videos to match, in the same message as the new options.

## When the inputs are missing

You need to know what the video is and where each item goes. If there is a script, a transcript or an edit plan,
read it and write the brief yourself. If not, ask once, in one short message: what the video is for and where it
will be posted, the feeling they want, and whether they have music or footage they already use. Never invent
footage, and never present a stock clip as the person's own product, place or people.

## Workflow

1. **Write the brief.** One line per slot in `brief.md`, using the template in `references/fit-guide.md`: the
   section or line it covers, what must be on screen (or heard), the mood, the place and season, the frame (for
   example 1080x1920), the seconds it must fill, and what to avoid (a holiday, a brand, a look the person disliked).
   Music gets one slot per section whose mood changes: a calm opening and a tense middle are two slots.

2. **Gather three to five candidates per slot.** Search with English words for what is on screen, not for the
   meaning: "feet stepping on bathroom scale", not "weight loss motivation". Pexels and Pixabay return no
   description of a clip, so the words in a search say nothing about what a result shows. If the brief names a
   place or people stock rarely has (a Vietnamese office, a local dish), search the action without the place, and
   if nothing fits, say so and offer hands, objects, a different shot or the person's own footage. When a search
   gives nothing new, change the words; do not repeat it with one word added. For music, take
   `has_youtube_content_id` and `is_ai_generated` from the result into the brief.

3. **Measure.** Download a small copy of each candidate (for video, the smallest file in `video_files` that is at
   least 640 px wide; a larger one later for the edit) and run:

   ```
   python scripts/measure.py c1.mp4 c2.mp4 https://.../c3.mp4 photo.jpg track.mp3 --out work/assets --target 1080x1920 --slot 4
   ```

   It prints one line per item with its flags, writes `work/assets/summary.md`, `assets.json` and a sheet per item
   in `work/assets/sheets/`: six frames with the `--target` crop outlined for video, the photo with its crop, an
   energy strip for music. Run music separately with `--slot` set to the length of its section.
   `references/reading-the-numbers.md` says what each number means and where it is wrong.

4. **Look at every sheet, as a stranger would.** Open each sheet with the Read tool. Write first what it shows, in
   one sentence, without your plan: "a woman's feet on a grey tiled floor, a pink scale, steady". Then judge it
   against its slot and give it one of three marks: fits, maybe, or out, with the reason. A clip is out when:

   - it does not show what the line says, or shows something else first (a cat, a lizard, a mat instead of a scale).
     A line that names two things ("salad with chicken") needs both on screen; if no candidate has both, say which
     part is missing and offer a second search or two short shots, instead of calling a half match a fit;
   - it breaks the brief: wrong season, place, culture or brand, a holiday the brief did not ask for;
   - it is shaky (`shake` 0.6 or more) where the cut is slow, cropped or slowed down; 0.25 to 0.6 only for short
     cuts. A big number on a shot where a liquid or a crowd fills the frame may be the subject moving, not the
     camera: look at the sheet;
   - the subject leaves the blue crop box, it must be scaled up more than 1.5x, or a cut inside it cannot be avoided;
   - it shows a watermark, a logo, readable text in another language, or a face looking into the lens the brief did
     not ask for;
   - it repeats a shot already picked (`measure.py` lists these under "Across the picks").

   Music is out when its title, tags or measured shape break the brief (a "Jingle Bells" track for a romantic
   Paris ad, a beatless drone under a calm explanation, a 20 s build under an opening that must hit at once), when
   it is shorter than its section and has no clean loop, or when it has a YouTube Content ID claim and the video
   goes to YouTube and the person has not accepted that.

5. **Let the person choose the music.** Before editing, show two or three music options per slot, each with one
   line on why it fits and its file or link, and ask which one. Do the same for any shot that carries the message
   (the product, the main person): show its sheet. If the person said to decide yourself, pick, and say what you
   picked, why, and that nobody has listened to it yet. Describe a track only by what was measured and by the
   words its source gives (title, genre, tags), quoted as theirs: "the source calls it 'French Paris Romantic
   Music'; about 86 BPM, full level from 2 s". Never your own word for how it feels or what it suits ("romantic
   piano", "hợp với làm đẹp", "sounds sad"): you have not heard it.

6. **Prepare what you picked.** Cut each clip to its `steadiest` stretch, or the stretch you chose on the sheet.
   If a slightly shaky clip is the only one that shows the line, keep the cut short, do not speed it up or crop it
   tighter, or stabilise it (`vidstabdetect` then `vidstabtransform` in FFmpeg) and measure it again. Bring a
   clip whose brightness or colour stands apart close to the others before it goes in. Start music where its
   energy matches the section, not always at 0 s.

## Deliver

**First, a version check.** If the EditAtlas MCP is connected, call `get_skill` without a name. If it lists media-picker above 0.2.0, the first line of your reply says a newer version exists and how to update it (in Claude Code: `/plugin`, then Marketplaces, editatlas-skills, Update marketplace; elsewhere `get_skill` with name media-picker gives the step). Without the MCP, skip it.

Write `ASSETS.md` next to the edit, in the person's language, with the template in `references/fit-guide.md`: for
each slot the pick, why it fits, its measured numbers, the in and out times, and the candidates dropped with one
reason each; the credits (author and `credit_url` for every Pexels, Pixabay or library item); Content ID and AI
flags; and what nobody checked: listening to the music under the voice, faces and brands in the footage on a
phone screen, and anything you could not find. Tell the person, in plain words, which picks they chose and which
you chose for them.

The reply itself, not only the file, lists each pick with its author and `credit_url` link, and each dropped
candidate with its id and one reason ("Pexels 7654321: a cat on a bench, not a scale"). People read the reply;
many never open `ASSETS.md`.

**Last, ask once how it went.** If the EditAtlas MCP is connected, after the edit is delivered ask the person, in
one short message in their language, about each item from EditAtlas or its searches that went into the video, by
name: each music track, each stock clip or photo, each sound and this skill. Send each answer with `send_feedback`
about `this_item`, with the issue they named (for a pick they disliked, `not_the_look` or `wrong_match`). Send only
what they said, and nothing if they do not answer. Ask once per edit: if you or another skill already asked, skip
it.

## References

- `references/fit-guide.md`: the brief and `ASSETS.md` templates, what to look for in each kind of item, starting
  points for music by video type, and stock search habits. Read it at step 1.
- `references/reading-the-numbers.md`: every number `measure.py` prints, its thresholds, what it was measured on
  and where it is wrong. Read it when a flag looks wrong.
