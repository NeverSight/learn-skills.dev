---
name: tella-changelog-video
description: Turn release notes, a changelog or a list of shipped changes into a short product update video in Tella through the Tella MCP, picking the changes users will notice, one beat per change shown in the real product, in the brand's look, and quick to repeat every release. Use when asked for a changelog video, a release or update video, a "what's new" video, or a video from release notes or merged pull requests.
---

# Changelog video

One beat per change a user would notice, the same shape every release.

This skill needs the Tella MCP. If tools such as `get_timeline` are missing, follow the connection steps in the `tella` skill first.

## Plan

1. Read the notes the user gives (pasted text, a file, a link). Keep what users will notice, fold small fixes into one line, drop internal work: three to six beats. Say what you left out.
2. One line per beat, in the notes' words: what you can now do, and where. Never claim more than the notes say.
3. A visual per beat: the user's recording of it, a screenshot as a parallax shot (`tella-ui-parallax`), or redrawn UI doing it (`tella-ui-redraw`). Ask for the screens you don't have.
4. Show the plan as `tella-plan-video` does and wait for a go.

## Build

- Open on the release name or date and the biggest change, not on a logo.
- Each beat: a short title (`tella-kinetic-type`), then its visual, 4 to 8 s, with one transition kind throughout (`tella-transitions`).
- End on where to try it, exactly as given. Music under it (`set_background_music`), quiet under a voice.

## Next time

Make the first one the template. Then `duplicate_video` it and swap each beat's text, screen and date; offer to save the title style (`save_text_preset`) and layouts (`save_layout`).
