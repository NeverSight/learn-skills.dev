---
name: tella-auto-cut
description: Tighten a Tella video in one pass through the Tella MCP. Cuts recording mistakes (false starts, retakes, repeated phrases, abandoned sentences), filler words and silent pauses, then cleans up the gaps and broken seams those cuts leave behind. Use when asked to auto cut, auto edit, clean up, or tighten a recording.
---

# Auto cut a Tella video

Cut the mistakes, the fillers and the silences from every clip, then read the result back and fix what the cuts left behind: pauses that joined across a cut, doubled words and leftover fragments.

This skill needs the Tella MCP. If tools such as `get_timeline` are missing, follow the connection steps in the `tella` skill first.

## Scope

Auto cut is a direct action: cut, then report what you did. Don't ask for approval of the mistake list first; the user can restore or adjust afterwards. Ask only when you can't tell which video or clip is meant.

It cuts silent stretches even when something is happening on screen. Pace is the silence mode: `natural` (pauses over 800 ms) unless the user asks for `fast` (500 ms) or `faster` (300 ms). If the user only wants some of the steps ("just the silences"), do only those, but still run the final pass.

Don't change layouts, zooms, overlays or captions.

## Workflow

Work clip by clip; transcripts, word indices and cuts are all per clip. `get_timeline` lists the clips. Before cutting, call `get_clip` on each one and keep its `cuts`, so you can say how to restore it.

On a clip, run the steps one at a time: send a step's call only after the previous call on that clip has returned. Calls on the same clip that run together each return the clip as they saw it, so one call's result can be missing the other's cuts even though both landed.

1. **Mistakes.** Follow steps 1–3 and 5 of the `tella-remove-mistakes` skill, with its rules in [../tella-remove-mistakes/references/mistake-rules.md](../tella-remove-mistakes/references/mistake-rules.md): read the transcript, find the mistakes, and cut them with one `cut_clip_by_transcript` call per clip. Skip its review step (step 4). Its rule still holds: when unsure, leave it in.
2. **Fillers.** `remove_fillers` on each clip.
3. **Silences.** `remove_silences` on each clip with the chosen `mode`. If it answers that the audio analysis is still processing, wait a little and try again, at most a few times; if it still isn't ready, skip silences for that clip, do the final pass anyway and say so in the report.
4. **Final pass.** See below.
5. **Report** per clip: the mistakes cut (time, reason, words), that fillers and silences were removed, the gaps and seams the final pass fixed, and the clip's length before and after. Say how to restore (below).

Mistakes go first because they are the step that needs reading. Fillers and silences can follow in either order: word indices never shift, and `remove_silences` works from the original recording.

## Final pass

`remove_silences` finds pauses in the original recording and ignores the clip's cuts. When a mistake or filler is cut, the pause before it and the pause after it now play back to back. Each was shorter than the threshold, so neither was cut, but together they play as one long gap. The transcript after all cuts is the only place that shows what actually plays.

1. **Re-read the transcript** with `get_transcript` (in windows for long clips, as in the mistakes skill). Times are on the playback timeline, with every cut applied.
2. **Trim long gaps.** For each pair of neighbouring words, the gap is the next word's `startTimeMs` minus the previous word's `endTimeMs`. Where it is longer than the mode's threshold (800 / 500 / 300 ms), cut `{fromMs: previous.endTimeMs + 120, toMs: next.startTimeMs - 120}`, which leaves 120 ms of air next to each word. Treat the gap before the first word and after the last word the same way, keeping 120 ms next to the word. Send every range for a clip in one `cut_clip` call: ranges are resolved against the playback timeline as it was when the call started, so a second call would use shifted times.
3. **Fix broken seams.** Read across each cut and look for what the cuts left:
   - the same word on both sides of a cut ("the the"): cut one of them;
   - one or two stray words stranded between two cuts that no longer belong to either sentence: cut them;
   - leftover words of a mistake that a cut took too little of: cut them.

   Fix these with `cut_clip_by_transcript` on the word indices. Never split a word or pad a range with extra words.

   Cuts only remove words: a word that is already cut is absent from the transcript and no further cut brings it back. If a mistake cut took too much (the sentence lost a word it needs), restore the clip's saved cuts with `update_clip` (see Restoring), redo steps 1–3 with the corrected mistake range, and run the final pass again on the new transcript.
4. **Listen to the risky seams**: mistake and filler cuts, several cuts within a few seconds of each other, and a word that ends right at a cut (it can sound clipped). A cut at a clear pause needs only the transcript re-read and `get_audio_levels`. `get_clip_preview` only returns a URL: download its MP4 (it has the clip's audio), cut each risky seam's range to audio with ffmpeg (`ffmpeg -ss 2 -t 6 -i preview.mp4 -vn -ac 1 -ar 22050 -b:a 48k seam.mp3`), join them into one file and listen to it once with your audio tool (`describe_audio` in the Tella editor). If the listen and the transcript disagree, `get_audio_levels` for those few seconds settles whether the word is whole. If the word isn't needed, cut it whole; if it is, restore and redo as above with that cut one word smaller. Never adjust a cut by milliseconds.

Run the final pass once (twice for a clip you had to restore), then report anything you saw but left alone.

## Restoring

A single cut can't be undone cleanly: a mistake cut merges with the filler and silence cuts next to it. To restore a clip, call `update_clip` with the `cuts` you saved from `get_clip` before starting. `cuts` replaces the clip's whole cut list, and the person may be editing the video by hand while you work: keep any cut in the current `get_clip` that neither you made nor was in the saved list, and send `cuts: []` only when that is the result: the saved list was empty and the current clip has no cuts to keep, or they asked to remove every cut. To redo with different choices, restore and run again.

A cut call that returned the clip succeeded; don't send it again, even when a later result seems to lack its cuts. If a cut call fails or its outcome is unclear, re-read the transcript before retrying: words that were cut are absent from it. When `cut_clip_by_transcript` reports word indices not found, those words are already cut: drop those ranges and send the rest once. Never blindly repeat a cut.
