---
name: fountain-clip-producer
description: Render a clip post into a finished, platform-ready video with framing, captions, and overlays.
---

## Overview

This skill turns the clip that a post carries into a video file.
It does not choose the moment or the span.
The caller chooses both before this skill runs.
Module **media** cuts the landscape master.
Every module after it works from that one file.
The other modules crop the picture and put the captions and the layers on it.
The skill delivers nothing until one report passes.

## Input

- The `SocialPostMediaSource` of a `SocialPost`, which names the file and the span.
  The file can have no video.
  Most files of a podcast catalogue have no video.
  Empty `ids` and a YouTube video id both name sources that Fountain does not hold as episodes.
- Or an external source for a raw local video, which carries the media path and span for this session.
  Its post carries no `source`, because a raw local path is not a valid `media` URL.
- The word timings of that span, which this skill makes from the clip's own audio.
  Module **shots** also needs the speaker of each word.
  No input supplies it.
- A delivery tier, which the words of the request imply.
- Or a queue run.
  Module **queue** reads the drafts that wait for media, and derives the inputs above from them.

Optional:

- A target shape, which is vertical, square, or landscape.
- The name of a caption preset, or the text of an overlay.

## Output

- The finished work: a landscape master, and one export for each shape that the request asks for.
  The master is finished work, and not one of the workings.
  The user keeps it and cuts from it again.
- A `SocialPostUpload` on `content.uploads` of the post, unless the user asked you not to attach it.
- Workings: a clip manifest, a crop plan, a caption plan, an overlay plan, a QA report, and a removal
  report when module **trims** cut the clip.

## Housekeeping

You MUST read HOUSEKEEPING.md if you haven't already.

## Requirements

- Fountain API.
- Python 3.11 or later.
- OpenCV 4.8 or later, importable from that same Python, for the face detection of module **framing**.
  Its model, and the fonts that the presets name, ship in `assets`, so no machine installs either.
- ffmpeg and ffprobe, built with libass, drawtext, fontconfig and whisper.
  Without them, the skill cannot burn a caption or time a word.
  A stock build often has none of them.
  On macOS, the Homebrew `ffmpeg-full` formula has them.
- A whisper.cpp model file.
  The whisper filter takes the path of this file, and does nothing without it.
  This skill looks first for `ggml-base.en.bin` in `~/.cache/whisper`.
  That file is 141 MB, so the skill does not ship it.
  The machine installs it one time.
- ImageMagick, to measure the width of caption text.
- yt-dlp, for a source that ffmpeg cannot seek directly.
  Keep it current, because YouTube changes what a client must send.
  A build a few weeks old gets a 403 error on every download, while the captions still download.
- A web search tool, and a way to read a page, for the reference sources of module **brand**.
- Skill **fountain-onboarding**, which installs a tool that module **preflight** finds missing.

## Process

1. Read the delivery tier from the request.
   Do the least work that the tier asks for.
2. Run module **preflight** to check the machine before the first render.
   One report serves every clip of a run, because the machine does not change between clips.
3. Run module **media** to cut the landscape master from `media`, between `ts_start` and `ts_end`.
   Cut all the clips of the run together, then transcribe them all together.
   No clip waits for another one.
   Then transcribe the master with whisper to get the word timings of the clip.
   Rebase the timings so that the first word starts at zero.
   Use the binary and the model that module **preflight** names, with `max_len=1`.
   Put `model=` last in the filter string, or the filter loses the option after it.
   Write the output as SRT, and give it to `scripts/align-word-timings.py`.
   Give the script the `transcript` of the source as the reference, and the clip's start in that SRT as
   the offset.
   The script keeps the words of the transcript and the timings of whisper.
   So a name or a number that whisper misheard is spelled correctly.
   The script writes the words JSON that module **captions** reads.
   Before you caption, read the words that the script lists as unheard.
   A number in digits, or a word that differs from the audio, is where a caption goes wrong.
   The words that the script lists as past the end are not in this clip, so check the offset and the duration.
   When the script matches less than 80% of the transcript, the transcript does not describe this clip.
   Then check the span and the offset before you caption.
   These timings are measured from the audio of the cut, so they are the only timings that describe this
   file.
4. Run module **trims** to survey the pauses and the filler, and report what it found.
   Cut only when the user asks, because a cut moves every time stamp after it.
5. Run module **framing** to crop the master to each shape that the request asks for.
   Run module **shots** with it when one shot holds two people and the crop must follow who speaks.
   Skip both for a source with no video.
   Such a source has no picture to crop and no face to follow.
6. Run module **brand** to load the look of the show, for a clean final or a publish final.
7. Send the user to the clip styling page when the request names no caption style and module
   **brand** holds none.
   The choice that the page records comes back as a brand kit.
   Do not stop the run to wait for an answer.
   Produce the clip with the default style, and tell the user which style that was.
8. Run module **captions** on every portrait export, and on another shape when the request asks for it.
   Run module **fonts** with it.
9. Run module **overlays** when the request asks for a layer, and always for a source with no video.
   For a source with no video, the overlay is not polish.
   There, an audiogram package is the whole picture.
   Without one, the clip is captions on an empty frame.
   Load the artwork of the show from `info.image`, and give it to the package.
   Every audiogram package needs the artwork.
10. Run module **qa** as the blocking gate.
    Deliver nothing until it reports a pass.
11. Use the render, and never the transcript, to confirm two things.
    The quote that the copy uses is in the clip.
    The person that the copy credits is the person who says the quote.
    The caller wrote the quote and the credit without seeing the clip.
    The transcript holds sentences and names no speaker.
    Find the speaker from the camera, and from a cutaway that shows a closed mouth.
    Repair what is wrong with the Social API, and tell the user what you changed.
    Move `ts_start` or `ts_end` when the clip opens or closes inside a word, or when the quote is outside
    the span.
    Then write the new words into `transcript`, so that the two agree.
    Correct the label, the title, the text and the context when the credit is wrong.
    A moved edge makes the render out of date, so go back to step 3 with the new span.
    The words, the captions and the gate all describe the old cut.
    Only the gate can say that the new cut is finished.
    Move an edge only to repair a fault that you can prove, or to make a change that the user asked for.
    Never move an edge to improve the clip, because choosing the moment is the caller's job.
12. Attach the video with the Uploads API and the Social API, unless the user asked you not to.
13. Present each finished clip on the clip card of skill **fountain-clip-finder**, with one added
    line saying the render result and where the video is attached.

## Additional notes

A run with more than one clip does the same work on each clip.
Move all the clips through one stage, then move them all through the next stage.
Most of the time of a render goes between the actions, and not inside them.
A render of one clip spends a third of its time in the tools.

There are three delivery tiers, and each tier adds to the one before it.
The request implies which tier to use.
The user names the work that they want, and not the tier, so read the tier from their words:

- A rough cut is the landscape master alone, with no crop, no captions and no gate.
  Read it from words about checking a span rather than making a clip.
- A clean final is publishable.
  Its portrait export has captions, because people watch it with the sound off.
  Read it from "produce this clip", when the request names neither captions nor packaging.
  A clean final of a source with no video also has its audiogram package.
  The reason is the same as for the captions on a portrait export.
  Without the package, there is nothing to watch.
- A publish final adds the overlays and the packaging, and the request names one of them.

Ask the user when the words fit none of the three tiers.
You MUST NOT raise the tier on your own, because polish is requested work.
Captions on a portrait export do not raise the tier.
Make a square or a landscape export only when the request asks for it.

The word timings come from the clip, and never from the episode transcript.
That transcript holds sentences and no words.
It is the caller's evidence for the span, and not this skill's evidence for a caption.
The text of the words follows a different rule.
Whisper mishears a name or a number that the transcript has right.
So the words come from the transcript, and the timings come from whisper.
Never write your own alignment code in the run, because code written during a run fails in a new way each time.

Always cut from the tallest rendition.
A 9:16 crop keeps the whole height and about a third of the width.
Thus that height is the real resolution of the clip, and module **qa** fails a big upscale.
When the tallest rendition cannot reach the target, deliver the size that it can hold, and tell the user.
E.g., deliver 720x1280 from a 720p master.
A true smaller resolution passes the gate, and an upscale does not.

When a span seems wrong but you cannot prove it wrong, report it and do not repair it.
A letterbox is also requested work.

To change a clip that this skill already made, first read the manifest and the QA report.
Reuse what is still correct, and write each new output under a new name.
Change only the output of the module that changes.
A caption change MUST NOT force a new crop.

A post does not have to be approved before this skill runs, and rendering one approves nothing.
Never put an API key, a token, or a cookie into a command, a manifest, or a report.

These steps make one clip, and the clips of one run are independent of each other.
Module **queue** therefore shares the clips of a long queue between at most three workers.
Each worker has its own output folder.
A run is finished when the last clip is finished.
Three workers do not finish three times faster, because ffmpeg already uses every core of the machine.
A short queue uses one worker, because each new worker reads the skill again before it renders anything.

The purpose of this skill is a good clip, and not a full set of completed steps.
Readability, framing, and sync matter more than procedure.
