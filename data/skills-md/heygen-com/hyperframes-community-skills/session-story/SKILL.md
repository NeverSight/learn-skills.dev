---
name: session-story
description: >
  An agent makes an animated film of an average session with its own user, beginning to end, told with that user's
  real messages: whatever their routine is (code, writing, data, design, video). The agent sits at a desk in a room
  decorated from what it knows about the user, and the monitor shows their kind of work. Requests glide in as paper
  planes and unfold. Corrections are a 3D cartoon mallet that bonks, then turns to show the words on its face. Praise is a butterfly
  towing the words on a ribbon. The agent types each reply onto a sheet, folds it and throws it back. The film opens
  with the agent asleep until the monitor boots: "Initiating session with <name>". The agent composes its own
  orchestral score, cued to every action. p5.brush watercolour, rendered in HyperFrames. Trigger on: "a video of our
  session", "animate a session with me", "session story", "show what working with me is like", "make a film about
  me and my agent".
---

# Session story

The agent reads its own history with its user, finds their routine, and turns one typical session into a 40 to 70 s
film, in the order it happened:
- **Story:** the user's verbatim words arriving as objects, and the agent's own replies going back. The window and
  the wall clock follow the session's real time.
- **Room:** decorated from what the agent knows about its user.
- **Score:** composed by the agent against the film's own timeline.

Write `story.json` and the engine does the choreography. Nothing on screen is invented: every line is a quote, and
the user approves every line before a frame is rendered.

## When to use / when not

- **Use** when a user asks their agent for a film of their work together, and the agent has real history with that
  user: local transcripts, or messages the user pastes in.
- **Do not use** for someone else's history, a team's shared logs, marketing with made-up quotes, or anything the
  user won't review. With no history at all, ask the user for a session's messages. Never invent quotes.

## Requirements and side effects (complete list)

- **Tools:** Node 22+, Python 3.9+ (standard library only), `ffmpeg` on PATH, and the HyperFrames CLI pinned to
  `npx --yes hyperframes@0.8.71` (downloaded from the npm registry on first use).
- **Setup (once, manually):** `sh scripts/setup.sh` runs `npm ci` from the committed lockfile: p5 2.3.3 (LGPL-2.1),
  p5.brush 2.2.3 (MIT), @fontsource/permanent-marker 5.3.0 (Apache-2.0). Read-only downloads from npm.
- **Score renderer:** on macOS, `swift` (Xcode Command Line Tools) plays the score through Apple's built-in General
  MIDI bank. Elsewhere, `fluidsynth` with a General MIDI soundfont you set as `SOUNDFONT`. Neither downloads anything.
- **Reads (local only, after the user says yes):** the agent's own transcripts, `~/.claude/projects/<project>/*.jsonl`
  (Claude Code) and `~/.codex/sessions` (Codex), for the current project unless the user allows `--all-projects`.
  Also the agent's memory and instruction files for the room. Nothing is uploaded.
- **Writes:** `session-story-candidates.json` (harvest) and everything inside the project folder you create. Both hold
  the user's words: never commit or share them.
- **Network at build time:** none. Pass `--describe false` to every `snapshot`, as shown below: with
  `GEMINI_API_KEY` set, `snapshot` otherwise sends frames (the user's words) to Gemini. Render locally: the page paints
  with WebGL.
- **No credentials, no paid calls.**

## Workflow

1. **Setup:** `sh scripts/setup.sh` (once).
2. **Ask first.** Tell the user you'll read your local history with them to find the session, and wait for a yes.
3. **Harvest:** `python3 scripts/harvest.py --project <their project folder> --out <scratch>/candidates.json` prints
   the routine and lists sessions, most typical first. `--session <id>` (with the same `--project`) prints one in
   order, with local times and your replies. Per [references/sources.md](references/sources.md).
4. **Scaffold:** `node scripts/new-project.mjs <dir>`. Everything you write from here lives in `<dir>`.
5. **Story:** take a typical session and write `<dir>/story.json` beat by beat, in the order it happened, with each
   beat's real time, per [references/story.md](references/story.md). The user's lines are verbatim spans; your replies
   are your own words from that session. Set `screen` to what their work looks like, and pick the ending their
   sessions have. `node scripts/schedule.mjs <dir>` checks it: run it after every edit.
6. **Room:** fill the slots from what you know about the user, per [references/room.md](references/room.md). Draw a
   custom prop in `<dir>/scenes/props-custom.js` when the library has nothing true to them. If you are not Claude,
   draw yourself: [references/cast.md](references/cast.md).
7. **Privacy gate:** show the user one table of every on-screen line (hook, nameplate, each quote, each reply, each
   prop and why), each with its source. Take their edits, get an explicit yes, then set `"approved": true`. Until
   then every frame carries a DRAFT stamp.
8. **Design pass:** run the `snapshot` command `schedule.mjs` prints. Look at every frame: quotes legible, props where
   they belong, nothing covering a message. Show the user the contact sheet.
9. **Score:** write `<dir>/score/score.py` with your own theme, key and palette, per
   [references/score.md](references/score.md). Then `sh <dir>/score/build.sh`. It fails on dead air.
10. **Render:** from `<dir>`: `npx --yes hyperframes@0.8.71 check`, then
    `npx --yes hyperframes@0.8.71 render --fps 24 --crf 12 -o renders/session-story.mp4`.
11. **Check the render:** its length must match `schedule.mjs`. Pull a frame at each key moment
    (`ffmpeg -ss <t> -i renders/session-story.mp4 -frames:v 1 renders/check-<t>.png`) and look at them. Then hand
    it to the user to watch with sound.

The example (`node scripts/new-project.mjs <dir> --example`, then `schedule.mjs <dir> --example`) is the reference
film: a real session between Claude and the skill's author, who makes videos. It shows the format, not the shape of
your film. `schedule.mjs` refuses it without `--example`, so it can't stand in for your user's story.

## Verify success

- `schedule.mjs` exits 0 and prints no warnings. `hyperframes check` passes. p5.brush logs WebGL `uniform`
  warnings, which are harmless.
- The design-pass frames show every quote legible, and match the beat table.
- `score/build.sh` ends with `ok: no dead air`, and the score's length matches the film's.
- The render is the length `schedule.mjs` printed, has an audio track, and its frames at the key moments match the
  design pass.
- Failure path to test: a story that opens on a reply, or has a quote over the limit, makes `schedule.mjs` exit 1
  and name the beat.

## What the engine owns

The motion is physical and already tuned: glide paths, the fold, the throw, the swing, the bonk and the wingbeats.
Change the story, the room, the cast and the score. Leave the choreography in `scenes/director.js` and
`scenes/compile.js` alone unless you are fixing a bug. The motion rules are in
[references/motion.md](references/motion.md).
