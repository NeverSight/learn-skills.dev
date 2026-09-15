---
name: clapper
description: Bootstrap Clapper and create, edit, preview, render, and improve React videos and original music-as-code scores and optional local voice narration. Handles CLI/runtime/project setup, sampled SFZ instruments, MIDI and stems, the studio Music/Code view, motion design, characters, foley, and adversarial visual/audio review. Use for Clapper films, original scores, animated demos, and recuts; not ordinary website UI or unrelated video editors.
---

# Clapper: brief → picture + sound → reviewed MP4

Make the next useful artifact yourself: a scene plan, a few proof frames, a playable draft, or a verified final. Keep updates short and numbered. Ask only for decisions that materially change the film; infer ordinary production choices from the request and existing project.

## 1. Bootstrap, then choose the shortest route

**When an eval author request supplies a ready runtime and workspace, read the
[author handoff contract](references/technical-evals.md#author-handoff-contract)
first and use that route.** Otherwise read [bootstrap.md](references/bootstrap.md)
first. Installing this skill is the user's only setup step; perform the remaining setup yourself. Detect the project, OS/architecture and installed tools. With Node/npm available, run the bundled `scripts/bootstrap.mjs` using the installed skill's absolute path. It installs a pinned CLI through npm's cache, prepares the managed runtime, creates/restores the project, runs doctor and captures a proof frame. Without Node/npm, follow the verified native-launcher route in that reference. Reuse a working install; never silently upgrade a pinned project. Use the source route only for an existing framework workspace or framework development.

For the rest of this skill, `clapper` means the exact command prefix resolved during bootstrap (possibly `npm exec --yes --package=@archastro/clapper@<resolved-version> -- clapper`, or an absolute native launcher path). It does not assume a global executable. Run commands with the project directory as `workdir`. Do not require pnpm, a source checkout, system FFmpeg, a browser install or a separate sampler for the standalone route.

1. Read project instructions, `clapper.json`, package scripts and Git status; preserve existing edits. Read API exports from the installed runtime or existing source checkout rather than assuming the last session's API. Bootstrap already verified the first frame; inspect that proof and continue instead of repeating setup.
2. Choose the mode:
   - **Benchmark / skill or runtime comparison:** read [technical-evals.md](references/technical-evals.md). Use the isolated evaluator and independent evidence; do not turn a regression test or self-review into a quality claim.
   - **Technical / scientific explainer:** read [explainers.md](references/explainers.md). Verify the intended primary source, build intuition, and explain the whole flow at each abstraction level before drilling down.
   - **New film:** use the bootstrapped basic/comic project; choose a visual direction from the brief and a relevant available example.
   - **Recut:** preserve the previous composition ID; reuse exported scene components and make the new scene plan explicit. Review changed scenes and both joins, plus regressions in the full export.
   - **Voice narration / dialogue:** read [narration.md](references/narration.md), then [audio.md](references/audio.md). Install the optional local engine, audition voices, define one central cast, and explicitly lock it before preparing scenes.
   - **Audio pass:** keep picture timing fixed unless authorized to retime; read [audio.md](references/audio.md).
   - **Original music / band / choreography:** read [music.md](references/music.md), then [audio.md](references/audio.md) for mix review. Music-only requests do not require creating a video.
   - **Preview/render only:** use the existing entry and composition; don't impose a redesign or full creative review.
   - **Polish/final production:** use [visuals.md](references/visuals.md), [audio.md](references/audio.md), and [review.md](references/review.md).
3. Resolve the entry and composition with `clapper compositions`; never silently render the CLI's first composition. Root `pnpm preview` / `pnpm render` target intern-promo, not whichever film the user mentioned.

| Intent | Read the closest concrete example |
| --- | --- |
| Basic scenes, data, score, portrait variant | `videos/_template/src/index.tsx`, `data.ts`, `theme.css` |
| Editorial type and counters | `videos/showcase/src/ledger/` |
| Playful springs and spatial movement | `videos/showcase/src/orbit/` |
| Terminal, graphs, camera and grain | `videos/showcase/src/nimbus/` |
| Character acting and continuous score | `videos/showcase/src/archdev/archdev2.tsx` |
| Boiling-ink comic and reusable rig | `videos/showcase/src/archdev3/`, `@archastro/clapper-core/rigs` |
| New opening/ending around approved scenes | `videos/showcase/src/archdev4/archdev4.tsx` |
| Sampled original score, beat-driven choreography, Music inspector | `videos/cat-ballet/src/score.ts`, `src/index.tsx`, `clapper.json` |

The table names repository examples, not files guaranteed to exist beside an installed skill. Prefer the installed runtime's templates and core/music exports; fetch only a relevant example from the matching official release tag if needed. Missing checkout examples must not block a new film. Use the existing primitive before inventing a replacement. Later local examples such as `archdev5` may contain useful new instruments; check exports and tests before relying on them. They are not automatically reviewed or shipped because their source exists.

## 2. Get to a working frame

Commands below use the resolved `clapper` prefix and the project root as `workdir`. Set the actual composition ID from bootstrap or `compositions`; don't rely on persistent `cd` state. These are production checks, not a second installation sequence.

```fish
set -l clapper_id spot # replace with the requested/configured ID
clapper --help
clapper compositions --json
clapper still -c "$clapper_id" --frame 0,30 --out out/stills/first-look
clapper preview --port 4321
```

Preview is a long-running server. Use its printed URL (the port may change). Open the user handoff in their main Google Chrome profile; automated browser checks use an isolated profile. Space plays, arrows step, `[` / `]` jump cuts, `s` shows safe areas, `c` shows copy boxes, `i` / `o` set a loop range. ScoreAudio plays the actual prepared WAV; synthesized cue previews are approximations. Judge the exported combined mix.

If a dependency or runtime check fails, return to the appropriate route in [bootstrap.md](references/bootstrap.md); don't improvise a second installation. For legacy workspace projects, pass their explicit entry and use the checkout-local CLI; preserve that workflow instead of converting it silently.

## 3. Author picture and sound together

For a full musical score, follow [music.md](references/music.md): compose with `@archastro/clapper-music`, select real SFZ presets, prepare through `clapper.json`, and place `ScoreAudio` in the film. The studio's Music tab exposes a clickable piano roll and exact source code. Use synthesized cues for foley or their intended timbre; use sampled instruments for a requested sampled score.

1. Write a compact beat plan: audience, promise, duration, format, style reference, one action per scene, on-screen copy, and the intended sound/quiet beat. For a requested spec, use an HTML task UI. Otherwise a short scene table is enough; don't delay a simple edit with a spec.
2. `defineScenes` owns durations and overlaps. Pass the plan to both `<Composition scenes={SCENES}>` and `<Scenes plan={SCENES}>`. Use `SCENES.start(name)` for global sound cues. Inside a scene, `useFrame()` is local. Numeric times are frames; `"0.4s"` is seconds. Recompute frame references after a retime.
3. Put factual copy/numbers in one `data.ts`, scoped brand tokens in `theme.css`, and long music beds in one root-level `Score`. Local action foley may stay in its scene. Check reused scenes for old beds/hits before adding a new score.
4. All important motion comes from `useFrame()`. Use seeded randomness, `useBoil`, or `noise1d`; no wall clocks, timers, or unseeded randomness. CSS animations may depend on worker history: use frame-based motion for anything that must survive arbitrary seeking.
5. Read [visuals.md](references/visuals.md) before authoring or polishing picture. Read [audio.md](references/audio.md) before scoring or changing the mix. These cover demonstrated traps, not a mandated house style.

### Voice narration is a separate script

Use `defineNarration` and `NarrationAudio` from the narration API, following
[narration.md](references/narration.md). The CLI downloads the optional model/runtime
only through `clapper voices install`; normal setup stays lightweight. Reuse one
central narrator ID across scenes and commit `clapper-voices.lock.json`. Never
silently relock, select a new voice per scene, or change speaking speed to squeeze
copy into a shot. Prepare takes, inspect actual durations, then adjust copy or scene
windows. Listen to returning narrator lines together and review the final muxed mix.

## 4. Iterate with the right artifact

```fish
# For a scene named intro; replace with a name from the scene map.
clapper still -c "$clapper_id" --scene intro --every 6 -o out/stills/intro
clapper render -c "$clapper_id" --scene intro --draft -o out/intro-draft.mp4
clapper review -c "$clapper_id" --draft -o out/review/round-1

# Final encode, then review that exact file without another encode.
clapper render -c "$clapper_id" --crf 20 -o out/final.mp4
clapper review -c "$clapper_id" --video out/final.mp4 -o out/review/final
```

`--scene` makes explicit still frame numbers scene-local. `--range a-b` is start-inclusive/end-exclusive; with `still --range`, explicit frame numbers are offsets from the range start too. Without either, `--frame` is absolute. Valid final frame is `durationInFrames - 1`.

JPEG q96 is the default intermediate and was much faster than PNG on grain. Choose PNG when lossless intermediates matter. CRF 17 suits flat art; 20–22 was useful for grain-heavy work. Measure the result instead of treating those as delivery requirements. Use short scene/range probes to diagnose slow renders.

**Concurrency:** the standalone packaging implementation gives each build a unique `.clapper/harness-*/build` directory; those versions can build concurrently with distinct output paths. Older Clapper versions rebuild/delete one `.clapper/harness-build` directory: serialize their harness commands or use isolated project snapshots. Check the installed version/source rather than assuming isolation. Do not edit source while reviewers are capturing frames.

## 5. Required adversarial review gate

**A successful render is not a finished film.** For a new finished film, showcase, substantial polish, or final original score, read and follow [review.md](references/review.md). Plan reviewer access before the final encode. This gate is required unless the user explicitly limits the task to a draft, preview, or diagnostic.

1. **Independent reviewers are required when available and permitted.** After author inspection, delegate read-only critique of the frozen export to separate visual and audio reviewers. For original music, require explicit composition/performance review too (the audio reviewer may cover both). Music-only work needs music/audio review, not an invented visual deliverable. Add a muted-feed/story reviewer for social-feed work.
2. **Review the actual artifact.** Supply the exact export path/hash, brief, scene map, kit and source snapshot. Visual review must include playback/motion evidence, not just a contact sheet. Audio review must address the final muxed soundtrack; stems, source and loudness numbers alone are insufficient. Reviewers must state what they actually saw/heard and what remains unverified.
3. **Collect verdicts and an issue ledger.** Each required reviewer returns SHIP / REVISE / BLOCKED, inspected frames/time ranges, evidence-backed issues, and verification of prior fixes. Missing reports, tools, playback or listening evidence do not count as approval. Self-review and `clapper review` output do not substitute for independent critique.
4. **Fix → regenerate → independently recheck.** Reproduce findings, record decisions, fix accepted blockers/major defects, and have reviewers verify the changed export. Any picture, sound, timing, props, format or encode change invalidates affected approvals. Keep the reports tied to the final artifact, not an earlier draft.
5. **Do not declare final/approved without the gate.** Every required domain must have sufficient evidence, an independent SHIP verdict, and no unresolved blocker/major defect. If independence or required media inspection is unavailable, deliver only a clearly labeled draft/partial result with **review incomplete**, naming the missing check. Ask for the specific capability or user acceptance of that limitation; never silently downgrade the requirement. Do not chase an arbitrary numeric score or add unrelated redesign.

Completion means:

1. The requested entry/ID/format renders; picture is inspected at opening, cuts, motion trouble spots, and final held frame; factual copy and CTA agree.
2. Sound was checked on the exported file. Report whether it was actually auditioned or only measured. No claim of listening based on a waveform.
3. Required independent reviews are complete, and accepted blockers/major defects are fixed and rechecked. Record remaining minor/taste notes and any user-accepted limitation. A score is supporting feedback, not a substitute for evidence or a promise of awards/virality.
4. The final MP4 and kit match the final source/props/format. Link the playable output and review reports, name the composition/duration, and report visual, audio and (when applicable) music verdicts separately. Never describe an unreviewed replacement as the approved file.

Keep commits, pushes, uploads and publishing within the user's requested scope. This skill does not authorize them.

For why these rules exist and which old advice was superseded, see [session-evidence.md](references/session-evidence.md).
