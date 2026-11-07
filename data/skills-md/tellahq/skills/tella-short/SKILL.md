---
name: tella-short
description: "Turn a Tella video into a vertical Short, Reel or TikTok through the Tella MCP: pick its strongest 15 to 60 seconds, make a trimmed 9:16 copy, tighten it, add captions, and lay it out at Shorts pace with a hook, B-roll that moves and the speaker on screen. Shows a scene-by-scene plan first, then builds it and checks every cut. Use when asked to make a Short, Reel, TikTok, clip, teaser or vertical version of a video."
---

# Make a Short from a Tella video

A Short is watched on a phone, often muted, by someone one swipe away from leaving. It needs a hook in the first seconds, a new shot every second or two, captions that carry the words, and an ending that pays off the hook. Pick the part of the video that can do that, copy it into a new 9:16 video, and edit the copy at that pace. Never edit the original.

This skill needs the Tella MCP. If tools such as `get_timeline` are missing, follow the connection steps in the `tella` skill first.

## Scope

Show a plan and wait for a go before the first write: the choice of segment is the user's call, and generated B-roll costs AI Credits. After the go, build the whole Short without asking again; the user can ask for changes.

If the user gives a time range, a chapter, a length, a platform or a style, those win over everything below. Without a length, aim for 30 to 45 seconds; never go past 60 unless the user asks.

## Workflow

1. **Read the video.** `get_video`, `get_timeline`, and `get_transcript` for each clip (in windows for long clips). `get_filmstrip` over the whole video shows what is on screen and where screen recordings, demos and results are.
2. **Pick the segment.** Find one self-contained idea that opens on a line that works as a hook, builds, and ends on a payoff or takeaway. A long tutorial usually holds several; pick the strongest and mention one or two runners-up. The segment can be one stretch, or a few stretches of the same thought when the middle wanders. Start and end on whole sentences.
3. **Plan the Short** with the rules below, and show it in chat:
   - the segment: its time range, first and last words, and the expected length after tightening;
   - the hook line and the question it raises;
   - one line per shot: the words it starts on, the layout, what is on screen, and the words spoken;
   - the B-roll sources, with links, and anything you propose to generate.

   Write each shot against its words, not its times: the times move once the copy is tightened.
4. **Make the copy.** `duplicate_video` with `startTime` and `endTime` (seconds on the video timeline, or `chapterIndex` for a chapter) and a name such as "<title> (Short)". For a segment made of several stretches, duplicate the span that covers them and cut the parts in between with `cut_clip_by_transcript`. Do every later step on the copy.
5. **Tighten it.** Run the `tella-auto-cut` skill on the copy with the `fast` silence mode, so mistakes, fillers and pauses go and the seams get checked. Then cut whatever the plan drops with `cut_clip_by_transcript`. Re-read the transcript after the last cut: every later time comes from it.
6. **Make it vertical.** `update_video` with `dimensions: {width: 1080, height: 1920}`. This remaps every layout, so run `list_layouts` and `get_filmstrip` on each clip before laying it out.
7. **Captions.** Turn them on with `update_video` (`captionsEnabled: true`, `subtitlesEnabled: true`, `captionGrouping: "chunked"`, `captionLinesPerBlock` 1 or 2). If the user has a saved subtitle preset in `list_subtitle_presets`, apply it with `apply_subtitle_preset`. Place them with `captionPosition` (see Captions below). Fix misspelled names and terms in the transcript with `update_transcript_words`, since captions show its text.
8. **Lay it out** shot by shot from the plan, using the rules below and the layout mechanics of the `tella-auto-layouts` skill (which tools, keeping the camera style, transitions). Add the B-roll with `add_layout` and `media`.
9. **Add text** where the plan calls for it, following `tella-motion-design`: the hook as type with `tella-kinetic-type`, a number the speaker says with `tella-data-callouts`. Keep it sparse: captions already carry the words.
10. **Check it** (see Check below) and fix what fails.
11. **Report** a link to the copy, its length, the segment it came from, one line per shot, and what the user should listen to, since you can only read the audio.

## Shorts rules

### The hook

- The first words are the hook: the most surprising claim, the result, or the question the Short answers. Move a stronger line to the front by starting the segment there; don't open on a greeting, a name or "so, today".
- The first 3 seconds must make sense with the sound off: the speaker's face, the strongest visual, or the hook as large type, plus captions.
- The hook raises one question, and the Short answers it before it ends. Cut a segment that never pays off.
- End on the speaker with the takeaway. Where it fits, bring back the opening visual so the Short comes full circle. Don't end on "thanks for watching" or a long outro.

### Pace

- The first shot change comes within about a second, on the first strong word.
- Most shots last 1 to 2 seconds. Hold longer only while a demo plays out or a key line lands, and never hold one framing of the speaker past about 4 seconds: change to a punch-in, a B-roll shot or a split.
- When the speaker names several things in a row, give each its own shot, card row or list item, on its spoken word.
- Use each B-roll clip once.

The "few changes per minute" guidance in `tella-auto-layouts` is for long videos. It does not apply to a Short.

### The speaker and the visuals

- Keep the speaker on screen for at least half the Short: people stay for a face. End each full-screen B-roll shot within about 3.5 seconds.
- Shots, in the order to reach for them: the speaker full frame; a punch-in for emphasis (`fullscreen` with `style: stretch` on a camera clip, `camera-only` with `punchIn: true` on a screen-and-camera clip); a split with the visual on top and the speaker below; B-roll full frame while the speaker keeps talking. The `add_layout` schema lists which kinds each clip's `layoutSceneType` accepts.
- A visual shows what the words don't: the product doing the thing, the result, the proof. Find it in this order: the recording itself (`media: {type: "recording", startTimeMs}` plays the clip's own screen recording from that moment); the user's library (`list_library`); the product's official pages and demos (`import_from_url`, with `scroll: true` for a page); and only then, if the user approved it, `generate_video`. Only use media the user has the right to use.
- Everything off the speaker moves. Never leave a still image or a static page as B-roll: record a page scrolling, use a video, or give an image a slow `add_zoom` (`manualZoom`) across its shot.
- Text on screen must be readable on a phone at a glance. When UI is too small, zoom into one whole card or field rather than cropping text at the edges.
- Never put a graphic, card or B-roll bubble over the speaker's face. Never show a video that has its own captions under this Short's captions.
- Never invent a number, result or quote. Every number on screen is one the speaker says or the source shows. Show a logo only from the brand's official file; without one, write the name.

### Captions

On a phone, the bottom fifth of the frame sits under the app's buttons, the account name and the description, and the top tenth under the status bar. Keep captions between them: above the bottom 20% of the frame, clear of the speaker's mouth and chin, and clear of text in a split's top panel. Short blocks of a few words read best. Look at a frame of each kind of shot to check.

## Check

Look at the copy as the viewer will, then answer each of these yes or no, and fix any no:

1. **The opening.** `get_filmstrip` with `timesMs` every 250 ms over the first 3 seconds, then `get_video_preview` of them. Does the hook land, and does it read with the sound off?
2. **Every shot change.** `get_filmstrip` with the frames just before, at and just after each layout change. Does each land on its word, with no blank, frozen, stretched or wrongly framed frame?
3. **The whole Short.** `get_filmstrip` across the whole copy. Is the speaker on screen for at least half of it, with no full-screen B-roll over about 3.5 seconds and no speaker shot held past about 4?
4. Do the captions stay clear of the mouth, the chin, the app's bottom area and the text in a split's top panel?
5. Is all text and UI on screen readable at phone size, with nothing cut off at a frame edge?
6. Does every off-camera shot move?
7. Is every number on screen one the speaker said or the source shows, and every logo from an official file?
8. Is the face clear of every graphic, and is there no captioned video under the captions?
9. Does the Short answer the question its hook raises, and end on the speaker?
10. Was every generated asset one the user approved?

After a fix, check that range again. If a write's outcome is unclear, read the state back before retrying, and never add the same layout or overlay twice.

## Looks worth keeping

When the user gives a note about the look (a caption style, a font, a layout), offer to save it so the next Short starts from it: `save_subtitle_preset` for captions, `save_text_preset` for a text style, `save_layout` for a layout as a Favorite.
