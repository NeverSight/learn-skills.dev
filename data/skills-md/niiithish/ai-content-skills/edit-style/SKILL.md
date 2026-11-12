---
name: edit-style
description: The house editing style for every short-form ad edited in FilmCraft, whatever is on screen. A talking head with inserts, 150 Flow B-roll shots under a voiceover, a sung ad, a stills slideshow. It holds the principles clients approved across Aleo, Mysa and CloudAlign (a new picture only on a caption start or a cut, cuts on the first word, something new every 2–4 s, every still moving, dead air cut to a breath, captions on the words, music well under the voice, hooks 2–3 cloned from the user's hook 1), the user's working rules (never move their clips, back up, no exports unless asked), the checks before every hand-back, recipes for change requests, and a new-machine checklist. Use for any FilmCraft edit, fix, re-cut, caption pass or export, for a client's edit feedback (Loom, notes), or when starting the edit of a new video. Then load the sub-skill for the format, talking-head-edit (a speaker carries the script with full-screen inserts) or voiceover-edit (shots or stills under a voiceover or song), plus filmcraft and captions-filmcraft.
---

# Edit style

This is how the user and I edit every ad in FilmCraft. The principles below held across four clients and about 30 videos: talking heads (Aleo), voiceover and song ads over 3D, clay and photoreal B-roll (Mysa), and a stills slideshow (CloudAlign). They apply whether the timeline holds 15 clips or 150. The format sub-skills add only what differs.

| Load | When |
|---|---|
| `talking-head-edit` ([talking-head/SKILL.md](talking-head/SKILL.md)) | One speaker (Aleo video-5, DCT-2190) or a two-woman podcast (Calvin video-23) carries the script on V1 with full-screen pictures over her |
| `voiceover-edit` ([voiceover/SKILL.md](voiceover/SKILL.md)) | Shots, clips or stills under a voiceover or a song, one picture per line (Mysa video-7 to 18, CloudAlign) |
| [references/screen-inserts.md](references/screen-inserts.md) | Any search, AI-answer, typed-address, study or product-page screen: made by us as focus screens, full frame, key line at centre |
| [references/recipes.md](references/recipes.md) | Any change request on a saved edit: swap, remove, retime, caption fixes; FilmCraft traps |
| [references/new-machine.md](references/new-machine.md) | A new PC, or a missing tool or font |
| `assets/` | Shared overlays: iPhone 🤯, red CTA arrows, the click sound; `assets/screens/` screen-UI templates and approved examples |
| `scripts/setup/filmcraft-update` | Install or update FilmCraft |

Also load `filmcraft` (CLI, bridge, export) and `captions-filmcraft` (`fc_captions.py`, `fc_inserts.py`). `filmcraft-pacing` cuts dead air and adds motion. The client folder's `AGENTS.md` / `CLAUDE.md` (playbook, taste log) and the video's own file win over this skill. Newest feedback wins over older notes.

## The principles (every format)

1. **Copy the client's reference ad.** It is what he measures against. Copy its pacing (count pictures per second on it), its caption look and height, its hook structure and its severity. Where the brief is silent, the reference decides. Measure from its frames (`video-breakdown`, scene detection) rather than guessing.
2. **Something new on screen every 2–4 s.** That can be a new picture, a cut, or a zoom step. Never two quiet shots in a row. No picture repeats inside a hook.
3. **A picture changes only on a caption start or a V1 cut**, at the first frame of the words it shows. Never mid-caption, and never for under 8 frames: no 1–3 frame flashes. Cuts sit on the phrase's first word, not a few frames off it (`voiceover/scripts/roll_cuts.py`). Check with `fc_inserts.py check` (and `fc_captions.py plan` for cuts off the voice).
4. **Each picture holds until the next one.** No gap where something vanishes while the voice goes on.
5. **Everything moves.**
   - Every still gets a slow, centred push from its first frame to its last at one rate: 2 % of its scale a second. It never starts late, never stops early.
   - Every clip has motion in it. Flow clips start slowly, so start them from the 1 s mark (user 2026-11-09: "the main action is slow in the first 1 sec").
   - Talking shots get a slow push, plus hard zoom steps only on a cut or a caption start. Never a sideways drift.
   - **In a hook opening, no hard zoom steps** (video-23 user, 2026-11-10: "no hard cut zoom… slow zoom"): the talking pieces share one continuous slow zoom across their jump cuts. A dead-air jump cut there is better as the real pause played at 1.5x with a quick ×1.08 zoom across it (`talking-head/scripts/dct-28/fill_jumpcuts.py`).
   - **The hook-to-body cut gets a push-in blur**: FilmCraft's `zoom_blur` transition, 8 frames centred on the V1 cut (4 frames on a split's listener clip so the whole frame blurs).
6. **A clip that goes from a start state to an end state plays whole.** Speed it up to fit its slot, so the end state is seen.
7. **Dead air is cut to a breath.**
   - The voice is sped up 1.1x (1.12x when the user asks).
   - Pauses of 0.35 s or more are cut to about 0.2 s, keeping about 0.04 s before the voice comes back.
   - Hook to body: about 0.37 s.
   - A word is never cut off: a shot of the speaker holds until the word ends.
8. **Captions say the script's words, on the words.**
   - Verbatim, with numbers as digits.
   - Each starts on its first word: at most 3 frames early, never late. Each ends when its last word ends, or stays up to the next caption.
   - Whole phrases, one short line, using the client's template (`captions-filmcraft`).
   - All at one height unless the picture under one is busy. A caption build resets positions, so rerun the position script after every build.
   - Captions and text are added only in the edit, never in generated media.
9. **Audio.**
   - The voice (or song) is the only sound from the media. Clip sound is off unless it is a talking clip.
   - Music sits 12–18 dB under the voice (measured with ebur128), with a 1–2 s fade out at the end.
   - Every voice source is at the same loudness (normalise to −16 LUFS before the edit).
10. **Splits, grids and cards are built in the edit**, from separate clips or stills: a 50/50 split with a seam, a top/bottom split, a word card, a CTA overlay. Never generate one split frame.
11. **Hooks 2–3 are clones of the user's finished hook 1.** Only the opening changes. The body, with every tweak of theirs, moves as one block, retimed to the new hook's voice. A song take that drifts gets every cut moved to the same sung word.
12. **Severity and literalness sell.** Every line is a picture a viewer gets in one glance. The problem is shown at its worst, and the product is always the real one with its real label.

## Working with the user (nithish)

- **The user edits in FilmCraft and has the final say.** You build an export-ready timeline. They tweak hook 1 by hand. From then on their saved file is the base.
- **Never move clips the user placed.** A swap keeps the same slot (start and length). No `fc_inserts.py snap`, no re-timing a saved edit. Diff clip positions against the backup after every change.
- **Write a project only while FilmCraft doesn't hold unsaved changes to it.** Scripts write the `.fcproj` headless. Ask the user to save (or close) first, then to reload afterwards. Never `file.save` from a stale MCP copy.
- **Back up every `.fcproj` before scripting it**, to `edit/backup-<date>-<what>/`.
- **No exports or preview exports unless asked.** Check by rendered frames: `filmcraft-cli --project P render --seconds S --out f.png`, stacked with ffmpeg, then looked at and sent with SendUserFile. Keep review sheets in the scratchpad, never in the project.
- **Ask before any paid generation.** Give the count and the price, then wait for a yes. If they ask for one take, make one.
- **Approve the still before making its clip.** Never crop or edit a still without asking. Video stays video: never swap a clip for a still.
- **Only touch what was named.** Do exactly the client's items. Say plainly when a choice was ours, not the client's.
- **Be quick.** The user measures it: on video-23 the captions took ~40 s and most of ~14 minutes was the agent waiting and adding extras. Start long steps (word timing, exports, renders) in the background at once, check their output files rather than polling processes, render check frames in parallel, and do only what was asked.
- **Short replies, with frames as proof.** "Stop" means stop every background task.
- **Log it.** Each decision goes in the video's `AGENTS.md`, dated, with who decided. Each action goes in `RUN-LOG.md`.
- **ffmpeg only makes source media** (speed-ups, voice muxes, scaled stills) and does analysis. FilmCraft renders and exports the edit. Encode with `h264_vaapi`.

## Checks before anything goes back

1. **`fc_inserts.py check edit/<hook>.fcproj`**: 0 changes under 8 frames, and no new mid-caption changes compared with before your edit. Look at every FLASH (the speaker showing under 18 frames between two pictures or at the end) and JUMP (a jump cut on her with no zoom change) it warns about, and fix it or say why it stays: on video-23 the user found these by eye ("weird cut… just after that b roll end").
2. **Positions**: every clip you didn't mean to touch is where it was. After a cut, everything after it moved by exactly the cut.
3. **V1 has no gaps.** Every jump cut sits under a picture or on a caption start.
4. **New voice media** passes `transcribe.py --engine parakeet` against the script, word for word. Listen for bleeps, doubled words and a second voice.
5. **Rendered frames** at every changed spot, plus the hook's first frame (title not over a face).

## Export (only when asked)

```bash
python3 ~/.claude/skills/filmcraft/scripts/fc.py export edit/hook-N.fcproj -o deliverables/<Brand>_<Concept>_HookN_9x16.mp4
```

- Run it in the background, one hook after another.
- Move old exports to `deliverables/pre-<what>/` first.
- Output: 1080×1920 H.264 + AAC, about 45 MB a minute.
- Afterwards check each file with `ffprobe` (duration and audio stream).
