---
name: seedance-advanced
description: On-demand Seedance 2.0 power techniques (in-engine dialogue/lip-sync, native audio design, multi-shot-in-one-take, true in-engine multi-clip continuation, dense 2D storyboards, role-isolated reference-to-video, non-English on-image dialogue) that we deliberately keep OUT of the everyday ad-clip pipeline.
tags: [seedance, video-gen, lip-sync, in-engine-audio, multi-shot, continuation, r2v, advanced, exception-path]
---

# Seedance Advanced (the exception path)

## 1. When to use this skill

Our everyday ad-clip pipeline lives in `higgsfield-video-prompt`. That default sets
`generate_audio=false` and adds ElevenLabs voiceover plus music in post, so anything in THIS file
is the exception path, not the default. Reach for this skill only when a specific job actually
needs one of Seedance 2.0's in-engine powers:

- in-engine spoken **dialogue / lip-sync** (mouth moves and voices a real line in the render),
- native **in-render audio design** (footsteps, ambience, SFX, beat-sync generated in one pass),
- a **multi-shot clip generated as ONE take** (real editorial cuts inside a single generation),
- a **true multi-clip in-engine continuation** (one clip literally continues another, not ffmpeg stitching),
- **dense-storyboard / 2D anime** work (many panels or cel-style boards),
- **role-isolated reference-to-video** (image = identity, video = camera only, audio = tempo only),
- **non-English on-image dialogue / subtitles** planning.

If the job is a normal hero-to-cutdowns ad clip with VO added later, stay in the default pipeline.
Everything below drifts model behavior surface-to-surface, so re-verify on the live surface before
you promise a result (see the footer).

---

## 2. In-engine audio and lip-sync

Native audio is generated **together with the video in one pass**, so picture and sound are
committed at once and post-sync work drops sharply. It is NOT bulletproof: audio can still desync,
pick the wrong speaker, or mask the line, so keep the repair moves at the end of this section handy.
Key reasoning model before you prompt:

- **The model tends to infer sound from what it sees.** Gravel gets footsteps, a street gets
  traffic. "Generic default audio" is the resting state. You override it by NAMING the exact sound
  you want (a sound cue acts as audio direction).
- **A moving mouth tends to force a voice.** Speech and lip articulation are tightly coupled. Asking for a
  moving mouth with no line is unreliable, the model tends to voice something anyway. So either give
  it the line you want, or keep the mouth still. Do not expect free silent lip-sync.
- **Lip-sync is not always on by default.** On some surfaces (for example Jimeng / 即梦) voiced
  dialogue is a toggle that ships OFF. Confirm the surface enables it before blaming the prompt.
- **Language strength is uneven.** Field reports rank **Mandarin strongest** for lip-sync, English a
  close second, then Japanese / Korean / Russian weaker (often English-accented). Prompt wording
  cannot fix this, it is a training-data effect.

> **Running it, flip the audio flag (or you ship a MUTE lip-sync).** You are here ONLY after an advanced trigger fired (see the Step-0 routing gate in `higgsfield-video-prompt`); the DEFAULT pipeline keeps `--generate_audio false`. The pipeline skill's CLI hardcodes `false`, so do NOT copy that line here. For any in-engine audio / lip-sync job set it TRUE:
> `higgsfield generate create seedance_2_0 --prompt "..." --start-image <png> --generate_audio true --duration 8 --resolution 720p --mode std --aspect_ratio 16:9 --wait`
> Verify the exact flag name live with `higgsfield model get seedance_2_0` (native audio also defaults ON when the flag is omitted, but set it explicitly so intent is unambiguous).

### Reliable-sync word budgets (field-observed, ~15s clip, verify per surface)

Two budgets get confused. The **acoustic** budget is how many words fit at natural pace (English
roughly 35 to 40 in 15s). The **reliable-sync** budget, how much stays lip-synced and un-garbled,
is much lower and is the real limit. The safer unit across languages is "one short sentence, about
one breath" (roughly 1.5 to 2.5s, one idea).

| Language | Reliable-sync budget (~15s) | Per line | Note |
|---|---|---|---|
| English | ~16 to 20 words before the mix compresses | 5 to 10 words | close-second sync |
| Mandarin | count characters/syllables, not words | one short clause | strongest sync |
| Japanese | treat as weaker tier | one short line | mora-timed, word counts mislead |
| Korean | under-tested | one short line | do not assume parity |
| Russian | ~10 to 15 words max | under 10 words | weak, often English-accented |

Past the reliable-sync budget (especially non-English), use the voice-reference path below or plan a post-dub.

### Voice-reference-as-lip-sync-compiler (the strong move for non-English)

On surfaces that accept a spoken-voice audio reference, attaching an **actual voice clip** makes the
model lip-sync to that audio instead of synthesizing its own speech. That is effectively a lip-sync
compiler and is the most reliable field-reported path for non-English dialogue: record or commission
the line, attach it, let the model only move the mouth. Use only your own recorded / licensed /
rights-cleared voice, treat any real or recognizable person's voice as authorization-sensitive.
Verify the surface actually exposes a voice audio reference before relying on it.

### Syntax you actually type

- **Dialogue:** short line in quotes, assigned to one speaker, stable framing (no head turns / big
  face movement / extreme camera moves while mouth accuracy matters). If the line matters more than
  the setting, drop music and SFX during the line.
- **Sound layers:** `Dialogue: A says "I found it." Sound: low room tone + distant rain. SFX: cup lands on table at 2s. Music: no music until after the line.`
- **Beat-sync (audio as clock):** `[Audio1] provides tempo only. On each downbeat: back wall light pulses once, dancer hits one pose, camera stays locked wide.` Tie each musical landmark to exactly ONE visible event (one event per beat, stacked events smear). Works only inside one generation, audio is not continuous across calls.
- **Inline audio tags (surface-specific, unverified):** some surfaces (e.g. Jimeng) accept bracketed
  cues appended to the line to steer timbre and insert SFX, e.g. `"..." [low warm voice][distant bell]`. Do not assume universal support.
- **Reference conflict repair:** if a video ref and audio ref both fight for timing, mute the video
  ref and state priority: `[Video1] controls camera/motion only; [Audio1] controls tempo`.

### Post handoff

Prompt audio shapes performance and visible timing, but final mixes are post's job. For paid /
delivery work, record separately: spoken language, subtitle/dub needs, M&E and stems, sync cues, and
the buyer loudness target. Deliverables that live in post: full mix, dialogue stem, music stem,
effects stem, M&E (music+effects minus dialogue, needed for localization), printmaster, dubbing
guide, loudness report. Repairs: desync -> shorter line + locked framing + less head motion; wrong
speaker -> tag the speaker and split turns; music masks the line -> cut music during dialogue.

---

## 3. Multi-shot in ONE generation

Seedance 2.0's headline power over 1.x: a single 10 to 15s call can hold 2 to 3 shots with genuine
editorial cuts.

- **The labels ARE the cut points.** Write `Shot 1:` / `Shot 2:` / `Shot 3:` in plain prose. A long
  UNLABELED prompt renders as one continuous take. Per shot: one primary action + one camera move +
  its sound, in the order subject/action -> camera -> sound.
- **The budget math.** Shots cost seconds. Plan ~4 to 6s per shot: two shots want ~10s, three want
  12 to 15s. Ask for four shots in 5s and the model compresses or skips beats. Multi-shot below ~10s
  starves the beats.
- **`duration: auto`** (surface-dependent) lets the model size the clip to the prompt's complexity.
  Verify the surface accepts it with `model get` first: the Higgsfield CLI in the pipeline skill takes
  an INTEGER `--duration` (e.g. `--duration 12`), so on that surface set the seconds explicitly.
- **Tier gotcha:** field reports say fast tiers do not reliably honor multi-shot on the first try, use the standard tier.
- **Want an unbroken take instead?** Say so explicitly: `single continuous take, no cuts`, otherwise
  a long action description may get chopped up.
- **Surface exception:** on Dreamina / Jimeng, Chinese practice structures longer prompts (over ~8s)
  with a bracketed timeline as the primary skeleton (`【时间轴】0-3s: ... / 3-6s: ...`, each segment
  carrying its own 画面/镜头/音效). Match the active surface, do not mix both skeletons in one prompt.

Worked shape (three-shot commercial, ~15s): `Shot 1: extreme close-up of condensation sliding down a glass bottle, ice clinking. Shot 2: the bottle rises from crushed ice, camera tilts up into a backlit halo. Shot 3: a hand grabs it against a sunset rooftop, city humming below.`

Failure -> fix: renders as one take -> clearer labels / fewer shots / standard tier. A shot skipped
-> fewer shots, raise duration or `auto`, one action per shot. Cut lands mid-action -> end each
shot's sentence on the completed beat, let the next shot open the new one.

---

## 4. Multi-clip in-engine continuation (the sequence state machine)

This is a true in-engine continuation: one clip literally opens from another clip's accepted footage
or its accepted final frame. It is NOT ffmpeg stitching. Plan globally, generate locally, observe the
real result, update canon, continue from actual accepted footage.

### The five continuation modes

Pick one per continuation and name it:

| Mode | Use when |
|---|---|
| `seamless_continuation` | The next generation continues the SAME shot, geography, and open motion from accepted footage. Legal only INSIDE one scene. |
| `intentional_next_shot` | An editorial cut is right. Preserves story continuity, does NOT promise exact frame continuity. This is the default at a scene boundary. |
| `bridge_between_known_states` | A known start state must reach a known end state. |
| `repair_tail` | The final seconds of the parent clip failed, fix only that tail. |
| `reanchor_after_drift` | Extension depth or visible drift has made the chain unstable, re-open from canonical references. |

### The rules that keep it from drifting

- **Never promise seamless across a scene boundary.** A scene = one location + time envelope. At a
  scene boundary the next clip opens from **canonical references** (not prior output), and
  `extension_depth` resets to 0. `extension_depth` counts consecutive output-sourced generations
  since the last canonical re-anchor. Keep chains short: re-anchor every 2 to 3 output-sourced
  generations (verify any hard ceiling on the live surface). Schedule re-anchors
  in the plan, do not wait for visible drift.
- **Don't replay a completed beat.** If Clip 01 already exited the terminal, Clip 02 must not show
  the terminal exit again.
- **Don't leak a future (reserved) beat.** If vehicle departure is reserved for Clip 03, Clip 02
  must stop before departure. Every continuation prompt excludes both completed beats and reserved beats.
- **Reset identity at scene boundaries** from the canonical reference registry (character identity,
  wardrobe, product geometry, persistent props, location).
- **Accepted footage overrides plan.** Record observed start/end state on accept. Rejected footage
  never becomes canon and can never be a continuation parent. If a clip unexpectedly completes a
  future beat, mark that beat done and drop it from later prompts.
- **Preserve reference tags byte-for-byte.** `@Image1`, `[Video 1]`, etc. must not be renamed,
  re-cased, translated, or renumbered.
- **Observe, don't interrogate.** The moment a final frame or accepted clip is attached, YOU read
  pose / screen position / wardrobe / props / lighting / framing off it. Ask the user at most about
  what a still cannot show: open motion at the cut, camera phase, audio phase. (To grab the final
  frame as the next clip's image anchor, use ffmpeg: `ffmpeg -sseof -0.2 -i <take>.mp4 -frames:v 1 -q:v 2 last.png`.
  The source repo ships its own `scripts/extract_last_frame.py`, which we do NOT have locally, so use the ffmpeg line.)

### Lightweight state discipline (skip their full JSON schema unless you need it)

For a real multi-clip project, keep a machine truth (`project-state.json`) and regenerate a readable
capsule from it, never hand-maintain the same fact twice. A completed scene compresses to ONE line
(scene id + one-line outcome + accepted final frame). Keep full detail only for the current scene
plus the immediately previous accepted clip. Capsule stays under ~40 lines. The capsule fields worth
carrying across a session: PROJECT ID, STORY GOAL, FINAL OUTCOME, SURFACE, REFERENCE TAGS, CANONICAL
REFERENCES, ACCEPTED CLIPS, SCENE MAP, CURRENT SCENE, CURRENT ACTUAL STATE, OPEN MOTION, COMPLETED
BEATS, NEXT CLIP JOB / INTENT, CONTINUITY LOCKS, ALLOWED CHANGES, RESERVED FUTURE BEATS, EXTENSION
DEPTH, UNRESOLVED UNCERTAINTIES. Audio note: clips carry ambience + sync SFX + on-camera dialogue
only, the unifying score is added in post because audio is not continuous across generations.

---

## 5. The retake protocol (full version)

The everyday 5-verdict summary lives in the main pipeline. This is the full economy of what to do
when a take comes back partially good (which is most of real production). Cost figures are volatile,
verify live before budgeting. For the owner's real Higgsfield credit prices see `higgsfield-video-prompt`;
the dollar-per-second framing below is the source's fal-surface economy, not our Higgsfield credits.

**Triage every take, five verdicts:**

| Verdict | When | Next move |
|---|---|---|
| **Keep** | The primary spend (what the shot is FOR) is delivered, nothing fatal. | Lock, log, move on. Perfection in secondary detail is post's job. |
| **Fix in post** | The flaw is in post's domain: color, on-screen text, sound mix, a trim, a few unstable end frames. | Never burn a take on what an editor fixes in minutes. |
| **Edit, don't regenerate** | Composition + timing are right, exactly ONE layer is wrong, surface supports edit. | Keep the take as source, change only the failing layer. |
| **Re-roll** | Prompt is right, the sample was unlucky. | Same prompt, new seed (the new seed IS the one variable, consistent with the everyday one-variable rule). Two or three re-rolls max, then the prompt is the problem by definition. |
| **Rewrite** | The SAME flaw appears in two or more takes. | Systematic, not luck. Diagnose by mechanism, change the prompt. |

**The one-variable rule:** change ONE thing per retake (one prompt clause, OR the seed, OR the mode,
OR one reference), never several. Same seed + one prompt change is the closest thing to a controlled
experiment. Change two things at once and the result is unreadable either way.

**Attempt budget (set BEFORE take one):** a take count (default five standard-tier, or ten fast-tier
drafts) and a written "good enough". At half the budget with no progress on the same flaw, stop
iterating and change strategy (different mode, decompose into more shots, or the honest exit below).

**Cost awareness:** draft cheap, lock expensive. Explore composition on the fast tier / short
durations / lower res, spend standard tier + full length only on the locked design. Ten four-second
drafts answer more questions than one failed fifteen-second take.

**The shot log** (one line per take, story state made auditable):
`Take N · changed: [the one variable] · seed: [same/new] · verdict: [keep/post/edit/re-roll/rewrite] · evidence: [one sentence]`.
Two log lines with the same flaw = a rewrite by rule, no third attempt on luck.

**When the answer is "don't generate":** dense on-screen text belongs to post, a real product's
exact behavior may belong to a camera, archival reality belongs to licensing, and a shot that failed
its budget twice after decomposition belongs to a different idea. "Film this one for real" is a
deliverable, not a failure.

---

## 6. Dense-storyboard / 2D mode

Use when a request has many panels, storyboard beats, or animation boards.

- **Classifier:** choose `dense_multishot` only when the user explicitly wants cuts inside one
  generation AND the surface supports it. Choose `phased_single_take` when the action should stay
  continuous. Never combine "single continuous take" with hard shot labels.
- **Dense multishot rules:** use shot labels, one action + one endpoint per shot, keep continuity
  locks visible across shot boundaries, do not overload a short generation with many locations /
  large actions / character changes.
- **Continuous take rules:** use Beginning / Then / Finally, no shot labels, no hard cuts, describe
  phases of one camera path + one geography + one physical action chain.
- **2D / anime / cel:** use animation-layout vocabulary (layers, parallax, holds, smear frames,
  impact frames, cel shadow, line boil, background pan, compositing). Avoid photographic sensor /
  lens / bokeh / ISO / shallow-focus language unless the user explicitly wants a hybrid look.
- **Endpoint discipline:** every dense beat must end in a completed visual state, or the next clip
  cannot inherit it safely.

## 7. R2V role isolation (reference-to-video)

When you feed multiple references, bind each one to a single role and explicitly state the
non-transfer boundary, or identity leaks from the wrong source. Pattern: image = identity, video =
camera only, audio = tempo only. Worked compiled prompt:

`[Image1] controls the original character identity and wardrobe. [Video1] controls camera rhythm only; ignore its performer, room, logo, and costume. [Audio1] controls tempo only; do not copy voice or song identity. The character walks toward the doorway in three steady steps as the camera matches the reference rhythm and stops when her hand reaches the handle.`

The load-bearing sentences are `controls camera rhythm only` (prevents video identity transfer) and
`ignore its performer, room, logo, and costume` (states the boundary out loud). Keep them.

---

## 8. Non-English on-image dialogue / subtitles

The source repo carries multilingual vocab tables (`references/vocab/zh.md`, `references/vocab/en.md`,
plus per-language dialogue notes) for role binding and precise wording. A couple of examples of the
approach: Chinese role bind `@图1 锁定主体身份` (Image 1 locks subject identity) / `@视频1 仅参考运镜`
(Video 1 provides camera movement only); English precision swaps like `slow push-in` instead of
"cinematic zoom" and `warm practical light from the left` instead of "moody lighting" (concrete
production English reads better to both the model and the moderation filter).

**House rule for CJK on-image text:** do NOT trust in-render Chinese text (Seedance garbles on-screen
CJK). Generate a **clean textless plate** and composite Chinese on-image text deterministically in
code with PIL, the same way we do for banknote and ad stills. In general, subtitles / captions /
forced narratives / market copy are authored in POST from the approved script, not generated as
moving text. When shooting subtitle-friendly footage: keep dialogue short + speaker-assigned, use a
stable medium or medium close-up for spoken lines, leave negative space for captions, preserve clean
plates for markets where copy changes. Localization is not literal translation, ask what actually
must localize (dialogue, product claim, holiday, gesture, sign, food, wardrobe, legal text, music).

---

## Attribution

Distilled 2026-07-04 from the open-source repo **`Emily2040/seedance-2.0`** (`main`), which is
licensed **MIT** (Copyright (c) 2026 Iamemily2050 / @iamemily2050). Techniques are re-expressed here
in our own words, not copied, and no repo code is installed. Seedance model behavior drifts between
surfaces and versions, so treat every number, budget, and toggle above as a hypothesis to re-verify
on the live surface at use time (per global rule 3.16, live source is ground truth).

## Production lessons (G-赌局 The Bet, 2026-07-05, first full in-engine-audio film)

- **Render ≥4-5s, edit 1-2s, ALWAYS by trim.** In-engine-audio clips can never be speed-ramped (kills lip-sync, pitch-shifts SFX). Fast pacing = aggressive trims of 5s renders down to 1-2s beats.
- **Dialogue lands LATE in a 5s render** (observed on all 4 lip-sync clips: lines at ~3.5-5.0s). Trim from the head, keep the tail; prompt the actor to finish early and hold, so the trim tail is a settled beat. Locate lines without ears via silencedetect spans + mouth-open frames (vid-qa observations); after the owner listens, widen any clipped line (err WIDE on hook lines).
- **"Stillness" wording renders a FREEZE-FRAME.** A frozen-crowd beat prompted with "everyone holds still / nothing else moves" produced a literal static frame twice. Rewrite so CAMERA MOTION + light motion are the grammatical subjects ("the camera dollies forward continuously... the flame dances, throwing moving shadows... patrons breathe and blink"). Detection: changed-pixel ratio between sampled frames (>12 gray-levels, sampled grid), frozen ≈0.1-0.2%, alive ≈48%; dark scenes make plain mean-diff useless.
- **The sudden-silence arc can live at the CUT.** If "the room noise dies mid-clip" doesn't render inside one clip, a loud clip (-28dB) cut into a quiet clip (-42dB) produces the perceived骤静 anyway; reinforce in the mix.
- **Byte-identical duplicate trap (bit us):** when re-rolling with a versioned prompt tag, derive the list-match tag FROM THE PROMPT ITSELF (e.g. `P[name].split(']')[0]+']'`), never rebuild it from the clip name, "[BET-R1]" substring-matched the OLD job and silently re-downloaded the old mp4, making a fixed clip look broken twice. ALWAYS shasum a re-roll against the previous file before judging it.
- **Reaction beats = one action per clip.** A multi-person tableau animated in one clip smears details (the owner rule): break crowd reactions into per-person ~1s close-ups + optional wide exhale.
- **Post mix that worked:** jazz bed (ElevenLabs /v1/music simple endpoint, INSTRUMENTAL forced, silent tail trimmed) with a volume envelope, low under act 1, ZERO from ignition through reveal, gentle return after; deterministic verify: per-section volumedetect (got -17dB / -28dB / -16dB) + silencedetect 0 dead-air.
