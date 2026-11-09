---
name: record-demo
description: "Record a narrated, human-paced demo video of a web feature with agent-browser: a smooth pointer, typing a viewer can read, no dead air, clicks paced to land on the narration, and a camera directed shot by shot from a screenplay, as a sharp 2560x1440 60 fps MP4. Use when the user asks to demo a feature, record a walkthrough, make a demo or screen recording for a PR, docs or release notes, or show someone what changed in the UI."
---

# Record a demo

A demo shows a person what changed in under a minute. Dead air comes from you thinking between commands, so never record while exploring. Explore first, write a screenplay of beats, then let the bundled player run it with no model in the loop.

Needs `agent-browser` (0.38.1 or later), `ffmpeg` and Node 22 or later, on macOS, Linux or Windows. The scripts need no packages. The player drives agent-browser even when the project has its own browser driver: it needs Chrome's 3x screencast, the pointer's timing and the stepped scroll, which a test runner does not give. The player is `scripts/record.mjs` in this skill's folder. The narration comes from the `add-voiceover` skill, in the folder next to this one (`<skill-dir>/../add-voiceover`); without it, record a silent video. Install it with `npx skills add jamdotdev/skills --skill add-voiceover`.

## 1. Rehearse without recording

Open the page, run `agent-browser snapshot -i`, and run every action once. Pick CSS selectors that still match after earlier steps change the page; refs like `@e3` go stale.

If the app needs sign-in or seed data, set that up now, in the session the player uses, launched the way it launches it: `agent-browser --session demo --args "--force-device-scale-factor=3" open <url>`. The flag renders the page at 3x for a sharp take; a session started without it keeps its 1x screen. The player closes the session after each take, so for a sign-in that lasts across takes, put `AGENT_BROWSER_PROFILE=./demo-profile` (a folder of your own) in front of this command and of every `record.mjs` run. Don't export it: `polish.mjs` would then open its Chrome in that profile.

## 2. Write the screenplay, `beats.json`

At most six beats. A beat shows one thing: a `shot` for the camera, and in `do` the commands that show it, with the lines that say it as `["say", "..."]` actions. The voice leads, like a person recording: a line starts once the one before has finished, and the commands after it run while it plays, so a click lands on the words about it. A full example is `beats.example.json` in this skill's folder.

```json
[
  {"shot": "wide",
   "do": [["say", "This is TodoMVC. Let's add the first thing to do."],
          ["click", ".new-todo", "--human"], ["humantype", ".new-todo", "Buy oat milk"], ["press", "Enter"]]},
  {"shot": ".todoapp",
   "do": [["say", "Every item lands in the list the moment you press Enter."],
          ["humantype", ".new-todo", "Book flights to Lisbon"], ["press", "Enter"]]},
  {"do": [["say", "Done with one? Tick its checkbox."],
          ["click", ".todo-list li:nth-child(1) .toggle", "--human"]]}
]
```

Direct the camera before you write a command. A camera move is a cut the viewer has to follow, so each one needs a reason:

1. Open `wide`, so the viewer knows where they are.
2. Frame a region (`"shot": "<selector>"`) only to make readable what the line is about: the list that grows, the message that appears, the number that changed. The frame holds for the whole beat and must contain every control the beat clicks.
3. At most one move per beat. It starts with the beat's first line, so the voice and the camera arrive together. A beat without `shot` keeps the last one, and the camera stays still.
4. Stay framed across beats in the same area. Never zoom out and back in between them.
5. Go `wide` when the page changes under the viewer, and for the last beat.

The camera never follows clicks on its own. A frame that would zoom in less than 1.25x stays wide, and `polish.mjs` warns about a click outside its beat's frame.

- Write the lines with the rules in `add-voiceover`: short, spoken, one idea each, naming what the viewer should notice, not what the mouse does. Put a line just before the command it describes.
- `do` entries are agent-browser commands. `humantype <selector> <text>` types one key at a time; plain `type` and `fill` put the whole text in one frame.
- Use `click <sel> --human` so the pointer travels there like a hand and the press shows. A plain `click` happens with no pointer on screen.
- `["scrollto", "<sel>"]` scrolls smoothly until the element sits a fifth of the way down the screen, in the window or in whatever panel scrolls it. End a beat with it, and frame what it reveals in the next beat: a framed beat keeps its region as it was before the scroll, and the player warns when a framed beat does more than wait or talk after scrolling. Plain `scroll` jumps in one frame. Selectors are CSS, or XPath after `xpath=` to match by text: `xpath=//button[contains(., 'Save')]`.
- Add `["wait", "900"]` after a change the viewer needs a moment to read. Nothing should sit still and silent for more than 3 s; `record.mjs` warns when something does, so cut the wait or give it a line. The last beat's result holds 2 s on its own.
- Mark the beat that tells the whole story in one still with `"poster": true`, usually the payoff. Its last frame, after the result has landed and the pointer has stepped aside, becomes `poster.png`. Without a mark the last beat is used.
- `["cut", <agent-browser command>]` runs the command and cuts its time from the video, for a wait nobody needs to watch: `["cut", "wait", "--text", "Welcome"]` skips a loading screen. After `click <sel> --human`, the press shows and the cut follows straight away. `["cut", "open", "<url>"]` moves to another page, after the line playing has finished.
- A `humantype` text that starts with `$ ` is a shell command run at that moment. Its last output line is typed and the wait for it is cut, for a value only known mid-take, like an emailed sign-in code: `["humantype", "#code", "$ python3 fetch_code.py"]`. Never put the value itself in `beats.json`. A screenplay runs commands, so play only one you wrote or read; the player prints each command before it runs it.

## 3. Record

Voice the lines first, so each beat waits for its real narration, then record, then lay the voice under the video:

```bash
node <add-voiceover-dir>/scripts/voiceover.mjs beats.json ./voice
node <skill-dir>/scripts/record.mjs beats.json <url> ./demo-out --voice voice/lines.json
node <skill-dir>/scripts/polish.mjs demo-out
node <add-voiceover-dir>/scripts/voiceover.mjs demo-out/narration.json ./voice --video demo-out/polished.mp4
```

`polish.mjs` writes `polished.mp4` and `poster.png`. It gives the raw take the finish of a screen-recording editor: the camera runs the screenplay's shots over the whole composed shot, window and wallpaper included, easing between them in 0.7 to 1 s (a deeper zoom takes longer), and draws the pointer crisp at any zoom, blurred along its path while it moves, with a small squash and a fading ring on each press. The page sits as a rounded card with a shadow on the wallpaper in `assets/wallpaper.png` (`--background <image>` picks another; `--background none` fills the frame with the page edge to edge, for docs or side-by-side comparisons). `--frame safari` or `--frame chrome` puts the page in that browser's window, its address bar (and Chrome's tab title) following the page as it changes; use it when where you are in the app is part of the story. It renders at 2560x1440 and 60 fps, so text stays sharp even zoomed in. It lays out each frame in a headless Chrome (agent-browser session `polish`), about six seconds per second of video, so run it in the background or with a timeout of several minutes; a run cut short leaves nothing behind. It keeps the take's frames as JPEGs in `polish-frames/` while it runs, up to a gigabyte for a minute, removed when it finishes. Timing does not change, so the narration still lines up. The last command reuses the lines the first one voiced and writes `voice/voiced.mp4`. Pick the voice as `add-voiceover` says before the first command, and keep it for both voice commands: the first command voices the final cut, and a different voice changes each line's length, which moves the clicks off their words. To rehearse cheaply, run them all with Kokoro, then again with the real voice. For a silent video, skip both voice commands and drop `--voice`; lines are then timed at reading pace and the voice can be added later.

The page loads before recording starts, the viewport is 1280x720, and the player takes the frames straight from Chrome's screencast at 3x (agent-browser's own recorder captures at 1x), so the take is a true 3840x2160. The page moves at an even 30 fps, except a `scrollto`, which is filmed a step at a time at a true 60 fps however busy the machine is; the camera and pointer move at 60. The take has no pointer; `polish.mjs` draws it, so always run it. The pointer moves like a hand: each path bends its own way and eases in and out in one movement to a point inside the target, right of centre and a little low, where it presses off the label so the viewer can still read what was clicked; and once the beat is done with it, it drifts sideways off the content. It takes the shape the page asks for: a pointing hand over links and anything styled `cursor: pointer`, an I-beam over text fields, the arrow elsewhere, morphing as it crosses the target's edge. A field that already has focus is typed into without another click. The player writes `video.mp4`, `narration.json` with the second each line started, and `timeline.json` with each beat's shot and framed region, and the pointer's moves and presses.

If a command fails, the player stops and prints the agent-browser output. Fix the selector in `beats.json` and run it again.

## 4. Check before you share

Read what `polish.mjs` printed: the number of camera moves should match the shot changes you wrote, with no out-of-frame warning. Then extract one frame per beat, a second and a half after its `said` in `timeline.json`, and look at each:

```bash
ffmpeg -v error -ss <said + 1.5> -i voice/voiced.mp4 -frames:v 1 beat.png
```

Look at `poster.png` too: covered from the narration, it should still say what changed. If it doesn't, move `"poster": true` to another beat in `demo-out/timeline.json` (polish reads that file, not `beats.json`) and run `polish.mjs` again.

Then get a fresh look. If you can start a subagent, give it only the beat frames, `poster.png` and a one-line brief of what the demo shows, never your plan or your reasons. Ask it for a ranked list: wrong state or missing result first, then framing (the frame cuts off what the line names, the pointer covers it), then pace (a pause too long, a click too fast to follow), then polish. Each finding names the frame file that shows it and the fix in one line, or it says "nothing" and lists the frames it looked at. Without a subagent, do the same pass yourself, a frame at a time.

Re-record when a frame shows the wrong state, or when a shot needs another selector: the player measures each shot while it records. Run `polish.mjs` again when only its options change, like `--frame` or `--background`. Never edit the video to hide a failed step. Then run the checks in `add-voiceover`.

## Share

Attach the MP4 to the pull request (GitHub takes videos up to 10 MB on free plans) or the ticket. Where a video won't play inline, as in a Slack preview or a README, use `poster.png` as the still that links to it.

**With Jam:** when `command -v jam` (`where jam` on Windows) finds the CLI, ask the user once whether to upload the video; it becomes one link to comment on, with a synced transcript of the narration and frames the next agent can read. Upload only on a yes, with `jam create jam '{"kind": "video", "url": "<url>", "videoPath": "voice/voiced.mp4", "posterImagePath": "demo-out/poster.png", "screenDimensions": {"width": 2560, "height": 1440}}'`. Exit code 3 means signed out: run `jam auth login`, then retry.
