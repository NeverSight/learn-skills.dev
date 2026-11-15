---
name: game-cinematic-cutscene-design
description: Design, storyboard, implement, render, and review game cutscenes, intro videos, cinematics, trailers, and in-engine camera sequences. Use when Codex is asked about storyboards, animatics, shot lists, blocking, camera language, Sequencer, Unity Timeline, Cinemachine, Unreal cinematics, Blender storyboarding, intro movies, prerendered videos, gameplay-to-cutscene transitions, cinematic trailers, subtitles, timing, editing, or cinematic production notes.
license: MIT
---

# Game Cinematic Cutscene Design

## Core Workflow

1. Identify the cinematic type: intro video, in-engine cutscene, interactive cutscene, dialogue scene, boss reveal, level flythrough, transition, ending, trailer, or prerendered movie.
2. Define the job of the scene before planning shots: establish world, reveal character, teach stakes, reward progress, hide loading, transition locations, sell a mechanic, create spectacle, or deliver story payoff.
3. Create a compact beat sheet, then convert it into a shot list with duration, camera intent, subject, action, dialogue/audio, transition, and gameplay handoff.
4. Build an animatic or blockout before polishing. Validate pacing, screen direction, readable silhouettes, camera continuity, timing, and whether the player understands the next action.
5. Implement with clear ownership of cameras, actors, animation, control lockout, audio, subtitles, gameplay events, save/load state, and skip behavior.
6. Review in context: before and after gameplay, target platform, expected aspect ratios, subtitles on, different languages where relevant, and with player settings applied.

## Creative Priorities

- Purpose: every shot should reveal, clarify, escalate, contrast, or transition. Remove shots that only repeat information.
- Player agency: use passive viewing deliberately; preserve control when interactivity would make the moment stronger.
- Readability: stage characters, props, UI, and camera movement so the player understands who acts, what changes, and where attention belongs.
- Continuity: track screen direction, eyelines, geography, action matching, lighting continuity, and audio continuity.
- Pacing: vary shot length, camera motion, performance intensity, and silence; do not cut faster than the player can parse.
- Tone: match lens, camera movement, editing rhythm, music, sound, and performance to the game world rather than generic film language.
- Handoff: end with a clear playable state, objective, camera position, input return, and no unexpected player danger unless intentional.

## Implementation Priorities

- Lock and restore player control, camera control, input context, UI visibility, time scale, physics, AI, and player/camera position deliberately.
- Support skip, pause, replay, subtitle, language, accessibility, and platform capture requirements where the game needs them.
- Avoid hiding critical gameplay information only in an unrepeatable cutscene.
- Keep cinematic actors, spawnables/possessables, bindings, animation tracks, audio events, and gameplay triggers named clearly.
- Use event tracks or timeline callbacks sparingly and document gameplay side effects.
- Decide whether the output is real-time, prerendered video, image sequence, or hybrid. Account for storage, compression, loading, aspect ratio, localization, and patch size.

## Freshness Rule

Verify current engine and tool documentation before making version-sensitive recommendations about Unreal Sequencer/Movie Render Queue, Unity Timeline/Cinemachine, Blender rendering/video editing, codec/export settings, or platform video playback constraints.

## Engine Mapping

- Unreal: use Sequencer/Level Sequence for multi-track cinematics, Cine Camera Actors, camera cuts, event tracks, actor bindings/rebinding, Take Recorder, Movie Render Queue, and gameplay-triggered sequences.
- Unity: use Timeline for shot/animation/audio orchestration, Cinemachine virtual cameras for shots and blends, Playable Director for playback, signals for gameplay events, and controlled return to Cinemachine Brain/gameplay cameras.
- Blender: use storyboarding, 3D layout, animatics, camera blocking, video sequence editing, and rendered image/video output for previs or prerendered scenes.
- Custom engines: define a timeline format, shot/camera system, actor binding, event callbacks, input lockout, subtitle/audio sync, and save/load behavior before authoring content.

## Deliverable Shape

For cutscene or intro-video work, produce:

- Scene purpose and player-facing outcome
- Beat sheet
- Shot list with timing and camera intent
- Required assets, animations, audio, UI, subtitles, and VFX
- Implementation notes for engine timeline/sequencer
- Skip/replay/accessibility/localization behavior
- Gameplay entry and exit state
- Review checklist and risks

## References

- Read `references/cinematic-cutscene-checklist.md` when planning, implementing, or reviewing a cutscene, intro video, trailer, or in-engine cinematic sequence.
