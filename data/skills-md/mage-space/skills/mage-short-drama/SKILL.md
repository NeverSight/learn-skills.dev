---
name: mage-short-drama
description: |
  Scripted short dramas with Mage, from one 30-second scene to a vertical
  series, with characters who act and speak in their own voices. Writes the
  story, bible, script, and shot list; makes identity stills and places on
  Mango 3, voices on Seed Audio or Eleven Speech, and a storyboard on Mango 3
  Turbo; films each scene as one multi-shot Cherry 2 Pro clip (or Lemon);
  adds voice-over and music; delivers the clips with an edit list, or joined
  with ffmpeg. Use when: "short drama", "vertical drama", "mini drama",
  "drama series", "web series", "soap opera scene", "a scene with dialogue",
  "episode 1", "make my script into a video", "cliffhanger", "two characters
  arguing", "film this scene".
  Chain with mage-characters to reuse a cast. NOT for: one clip from a
  prompt (use mage-generate), a two-character preset scene
  (mage-scene-builder), creator-style product videos (mage-ugc-video),
  narrated explainers with no one on camera (mage-faceless-video), or making
  a face speak an existing audio clip (mage-lipsync).
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems. Cropping, tiling, and joining clips need a shell with ffmpeg; without one, the skill delivers the clips in order with an edit list.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Short Drama

A short drama works when the story reads at a glance, every character looks and sounds like themselves in every shot, every reaction has a trigger the viewer sees, and each line is spoken exactly as written. Generating video is the easy part; controlling it is the work. Decide the performance, the blocking, the shots and the continuity in writing before anything is generated, so each paid generation is one deliberate attempt, not a lottery.

## Before you start

1. **Mage tools:** `list_models`, `get_model`, `estimate_cost`, `generate`, `get_request`, `list_characters`, `create_character`, `list_references`, `create_reference`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **What the user brought.** Skip any stage whose output the user already has (a script, a cast, a storyboard). Check `list_characters` and `list_references` before making a cast; reuse saved characters and places by `@handle`.
3. **Models.** `list_models` shows what the account can run: Mango 3 and Mango 3 Turbo for stills, Cherry 2 Pro and Lemon for scenes, Seed Audio, Eleven Speech and Eleven Music for sound. Read `get_model` once per model before its first call.

## UX rules

1. Defaults, unless the user says otherwise: 9:16, 720p finals, photoreal live action, dialogue in the user's language, 30 seconds per scene or episode. Say what you assumed.
2. The user's own story, script and lines are the contract: keep their events and words exactly, and write only what they left open.
3. **Money is explicit.** Price every paid step with `estimate_cost`, show the logline, the lines and the total together, and wait for a yes. Video is the expensive step: a 30-second Cherry 2 Pro scene at 720p costs about as much as 75 Mango 3 stills or 380 Mango 3 Turbo keyframes. Ask again before anything the approved plan did not include.
4. Characters are original people. Never cast a real person's likeness without that person's consent, and never a public figure.
5. Be concise. Deliver links with short labels in story order, no JSON or request ids. Results expire after 30 days: say so once.

## Paths

| Request | Path |
|---|---|
| "A 30-second drama", one scene, a teaser | **Quick**: one place, two or three characters, one Cherry 2 Pro clip holding 4 to 6 shots |
| Episodes, a series, anything over 30 seconds | **Full**: story, bible and outline once; then per episode a script, shot list, storyboard, scenes and the cut |

## The stages

| # | Stage | What it settles | With |
|---|---|---|---|
| 1 | Story | Who wants what, what stands in the way, the turn, the ending hook | Writing |
| 2 | Bible | Each character's fixed look, costume, voice, want and knowledge; each place's landmarks and light | Writing |
| 3 | Outline (series) | Per episode: what happens, what is revealed, the hook it ends on | Writing |
| 4 | Script | Scenes as action, reactions and exact lines | Writing |
| 5 | Shot list | Blocking per scene; per shot the framing, start → action → end, the line, the sound | Writing |
| 6 | Cast and places | An identity still per character, saved with a voice; an empty still per place | Mango 3, Seed Audio or Eleven Speech, `create_character`, `create_reference` |
| 7 | Storyboard | A keyframe per shot: the draft the user approves | Mango 3 Turbo |
| 8 | Scenes | One clip per scene of up to 30 seconds, several shots inside | Cherry 2 Pro (or Lemon) |
| 9 | Voice-over, music | Narration; one music track per episode | Eleven Speech or Seed Audio; Eleven Music or Seed Audio |
| 10 | Cut | The clips, music and voice-over in order | An edit list, or ffmpeg |

Stages 1 to 5 are free: write them in the chat, a few lines each on the quick path. `references/templates.md` holds every stage's template and prompt, with one worked example; read it when you reach the stage.

## 1. Write it

Script:

- Characters are already doing something before they speak.
- Every reaction has a trigger: "she stops stirring at the word Tuesday", never "she reacts".
- Give behavior only the meaning the story has earned: a hand that stops is not a confession.
- Short lines, at most two per shot. English speech runs about 2.5 words a second, plus a beat for the reaction: 30 seconds holds three to five lines, 25 to 45 words.
- Hooks: the first two seconds open on the conflict or a question; a reveal, reversal or callback at least every third shot; the episode ends on a turn.

Shot list:

- Block each scene once: where everyone is against fixed things (the counter, the door), which way they face, who holds what, where the light comes from. The camera stays on one side of each conversation, so eyelines and screen sides hold across cuts.
- Vertical drama is faces: medium close-ups, close-ups and extreme close-ups, shot/reverse-shot for dialogue, a wide only to set the place. Never two shots in a row at the same framing; one camera move per shot at most.
- Show the reaction the script names, often on the listener while the speaker's line runs on.
- Every shot has a start state, an action and an end state; an object handed over says who holds it at the end. 3 to 6 seconds a shot, adding up to the clip's length.
- At most three speaking characters per Cherry scene: it carries three voices per clip.

Run the self-check in `references/templates.md` before pricing. Its last step reads script → shot list → prompt: every trigger, reaction and line must survive word for word. "He listens" where the script says "his hand stops at her name" is a lost performance: restore it.

## 2. One plan, one price

List every paid step with its model and settings, price each with `estimate_cost`, and show the total with the logline and the lines, so the user approves the story and the price together:

- **Cast:** an identity still per character, Mango 3 (`mango`, `mango-v3`), 2:3.
- **Places:** a still per place, Mango 3, 9:16.
- **Voices** (full path, or a voice the user asked for): a 10-second clip per speaking character, Seed Audio (`seed_audio`) or Eleven Speech (`eleven_speech`).
- **Storyboard:** a keyframe per shot, Mango 3 Turbo (`mango-v3-turbo`), 9:16.
- **Scenes:** one per scene, Cherry 2 Pro (`cherry`, `cherry-2-pro`), `aspect_ratio` 9:16, `resolution` 720p, `duration` the scene's length.
- Voice-over and music only when the user asked for them.

A series: plan the episodes the user asked for, with the cast and places once; with no number given, plan the first episode and offer the next.

## 3. Cast, voices and places

- **Identity still** per character on Mango 3: one person, head to knees, a slight three-quarter turn with the face near-frontal and large, both hands empty and visible, plain backdrop, even light, neutral closed mouth. No props, text or labels: a video model copies text it finds in a reference. Check each still against the bible before saving it.
- **Voices.** Inside one clip, Cherry keeps each voice by itself, so a single-scene drama needs no clips. Across clips, voices drift: give every recurring speaker a 10-second clip (one speaker, dry room, no music). Make it on Seed Audio with the character's identity still as `image` and a line in character (the model designs a voice that fits the face), or from a described voice; or on Eleven Speech in the preset `voice` that fits.
- **Save the character** with `create_character`: the face, and the voice clip as `voice` (characters can't be edited later, so make the voice first). The face saves best as a tight, front-facing crop: when you can run commands, crop it from the still and upload it with `create_upload`; otherwise save the identity still itself, whose face is already large. When the costume must hold, also save the full still as an `outfit` reference with `create_reference`.
- **Places:** an empty still of each location at 9:16, landmarks and light named, no people; save it as a `location` reference.
- Start the stills together; a voice made from a still waits for it.

## 4. Storyboard: the draft

- One keyframe per shot on Mango 3 Turbo at 9:16, with the `@handles` and the place: the shot's framing at its key moment. Show them in shot order beside the identity stills and redo only a panel that drifted.
- When you can run commands, tile them in shot order into one image with no numbers or captions and upload it (`references/templates.md` has the ffmpeg line); the scene then takes it as `@image1`. Without a shell, leave the grid out: the scene prompt's shot paragraphs carry the order.
- Ask: film it, or what to change. It is the last cheap moment.
- For hard blocking (a fight, a chain of handoffs, three speakers), a Cherry Mini (`cherry-mini`) motion draft at 480p in 15-second halves, only when the user approves it.

## 5. Scenes on Cherry 2 Pro

- One clip per scene of up to 30 seconds, holding all its shots: shots in one clip share faces, voices and room sound across their cuts. Split a longer scene at a cut, never inside a line. `duration` is the shortest allowed length (4, 5, 8, 10, 15, 20, 25, 30) that holds the scene.
- Inputs: the storyboard grid (if any) as `image`; each character and place by `@handle`; `use_character_voices` on (the default). Each `@handle` brings its image and voice.
- The prompt follows the scene template in `references/templates.md`: a global block (the storyboard's role, a cast line naming each `@handle` once beside the character's NAME, the place, blocking, camera side, light, dialogue and sound rules, an Avoid line), then one paragraph per shot: framing and camera, the action with hands and eyes, the speaker, delivery and exact line, and "End with" the end state. `references/scene-prompts.md` has Cherry's markup.
- No timestamps in a Cherry prompt: the shot order and the lines pace it; the seconds stay in your shot list.
- Write for the edit: no music in the clip (the music goes on once, under the whole cut), the sound each action makes, listeners' mouths closed, and "no subtitles, captions or on-screen text" (vertical clips draw stray subtitles more often).
- Start every scene of an episode together, each with a new `idempotency_key`, and wait on each with `get_request`. A scene that continues another without a break opens with "Continuing from the previous scene:" (positions, hands, props, light). When you can run commands, also pass the earlier clip's last frame as one more reference, for positions and light only; that scene then waits for the earlier one.

### Lemon instead

| Need | Lemon (`lemon`) |
|---|---|
| Four or five speakers in one scene | Reference mode: up to five voices and ten images |
| A lower price | About half of Cherry 2 Pro at the same length and resolution |
| An exact first and last frame (an insert, a transition, a payoff pose) | Frame mode (`first_image`, `last_image`): no `@handles`, references or voices, so describe the people and put any words in voice-over |

On Lemon, give each shot a time range and tile the clip with them (`Shot 1 [0-4s]`), 2 to 5 seconds each (`references/scene-prompts.md`). It is below Cherry 2 Pro in quality: say so when you choose it.

## 6. Voice-over and music

- On-screen lines: Cherry speaks them in sync, in the characters' voices. Narration, inner monologue, a voice on the phone: Eleven Speech (one preset voice for the narrator all series long; audio tags such as `[whispers]`) or Seed Audio with the narrator's voice saved as an `audio` reference; in the clip, that character's mouth stays closed.
- A narrated drama (the user asks for narration or a recap style) tells the story in voice-over over silent acting: faces hold steadier without lip sync, and a retake need not match lips, while spoken scenes play more naturally. Use voice-over too for a line whose talking face keeps drifting.
- Music, when asked: one instrumental track for the episode, made at or above its length (Eleven Music with `instrumental: true`, or Seed Audio at 30, 60 or 120 seconds), cut and faded to the picture. Never a track per shot. Use whichever `list_models` shows.

## 7. The cut

- **With a shell:** download the clips and audio, join the scenes in order, lay the music under them about 10 dB below the dialogue with a fade-out, and place each voice-over at its start time (`references/templates.md` has the ffmpeg commands). Upload nothing back unless the user asks; deliver the file.
- **Without one:** deliver the scene clips in order with an edit list: each clip's label and length, where the music starts and ends and how loud it sits, and each voice-over's start time. Any editor (CapCut, Premiere, DaVinci Resolve) assembles it in minutes.
- Captions only when the user asks, from the script so every word matches, clear of faces. A single clip with nothing added is delivered as generated.

## 8. Check and fix

- Look at each scene beside the identity stills if you can view media; otherwise ask the user to watch for faces, costumes, props, every scripted line and every scripted reaction.
- Fix the stage the flaw comes from: a beat that does not read is the script; a missing reaction is the shot list; a reaction the prompt dropped is the prompt; a drifting face or costume is the clip (regenerate that scene once, the drifting detail named first); a jump or a level is the cut.
- Look only (a jacket's colour, a stray object): a Cherry 2 Pro edit of that clip (in `videos`, called `video 1`) keeps the acting and timing; send `keep_original_audio: true` so the dialogue survives. A change to action, timing or a line: regenerate the scene.
- A note on one shot redoes only that scene and the cut. Quote any retake before running it.

## A series

- The bible and outline are the series' memory: present the bible with the first episode (or write it to a file when you have a filesystem) so a later session can continue. After each episode, update what each character knows; open the next episode on the last one's hook.
- Characters and places stay in the user's Mage library across sessions.
- A redesigned character is saved as a new character and used from then on: never mix old and new looks in one episode.

## Deliver

```text
Episode 1, "The Key" (30 s, 9:16, Cherry 2 Pro 720p, 10,400 Gems in all):
1. Scene 1, the diner (30 s): https://…
Cast saved: @nora, @eli · Place: @diner
```

Offer once: the next episode, or a cover image (`mage-youtube-thumbnail`).

## References

- `references/templates.md`: bible, outline, script and shot-list templates, the self-check, every prompt (identity still, place, keyframe, voice clip, Cherry and Lemon scenes, voice-over, music), the storyboard tile, and the cut, with one worked example.
- `references/scene-prompts.md`: Cherry 2 Pro and Lemon prompt markup for drama: how Mage numbers images and voices, dialogue, silence, consistency, and what to avoid.
