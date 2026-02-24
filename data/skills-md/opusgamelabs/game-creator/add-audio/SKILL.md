---
name: add-audio
description: Add music and sound effects to a game using Strudel.cc — background music, gameplay themes, and SFX
argument-hint: "[path-to-game]"
disable-model-invocation: true
---

# Add Audio

Add procedural music and sound effects to an existing game. BGM uses Strudel.cc for looping patterns. SFX use the Web Audio API directly for true one-shot playback. No audio files needed — everything is synthesized in the browser.

## Instructions

Analyze the game at `$ARGUMENTS` (or the current directory if no path given).

First, load the game-audio skill to get the full Strudel patterns and integration guide.

### Step 1: Audit

- Read `package.json` to identify the engine and check if `@strudel/web` is installed
- Read `src/core/EventBus.js` to see what game events exist (flap, score, death, etc.)
- Read all scene files to understand the game flow (gameplay, game over)
- Identify what music and SFX would fit the game's genre and mood

### Step 2: Plan

Present a table of planned audio:

| Event / Scene | Audio Type | Style | Description |
|---------------|-----------|-------|-------------|
| GameScene | BGM | Chiptune | Upbeat square wave melody + bass + drums |
| GameOverScene | BGM | Somber | Slow descending melody |
| Player action | SFX | Retro | Quick pitch sweep |
| Score | SFX | Retro | Two-tone ding |
| Death | SFX | Retro | Descending crushed notes |

Explain in plain English: "Background music will automatically loop during each scene. Sound effects will play when you do things like jump, score, or die. The first time you click/tap, the audio system will activate (browsers require a user interaction before playing sound)."

### Step 3: Implement

1. Install `@strudel/web` if not already present
2. Create `src/audio/AudioManager.js` — manages Strudel init, BGM play/stop (uses `hush()` + 100ms delay before new `.play()`)
3. Create `src/audio/AudioBridge.js` — wires EventBus events to AudioManager for BGM, calls SFX functions directly
4. Create `src/audio/music.js` with BGM for each scene (Strudel `stack()` + `.play()` — these loop continuously)
5. Create `src/audio/sfx.js` with SFX for each event (**Web Audio API** — OscillatorNode + GainNode + BiquadFilterNode for true one-shot playback)
6. Add audio events to `EventBus.js` (`AUDIO_INIT`, `MUSIC_GAMEPLAY`, `MUSIC_GAMEOVER`, `MUSIC_STOP`)
7. Wire `initAudioBridge()` in `main.js`
8. Emit `AUDIO_INIT` on first user interaction (game starts immediately, no menu)
9. Emit music events at scene transitions and SFX events at game actions

**Critical**: Strudel's `.play()` starts a continuously looping pattern — correct for BGM, wrong for SFX. SFX **must** use the Web Audio API directly (see game-audio skill). Import `stack`, `note`, `s`, `hush` from `@strudel/web` for BGM only.

### Step 4: Verify

- Run `npm run build` to confirm no errors
- List all files created/modified
- Remind the user: "Click/tap once to activate audio, then you'll hear the music"
- Note the AGPL-3.0 license requirement for `@strudel/web`

## Next Step

Tell the user:

> Your game now has music and sound effects! Next, run `/game-creator:qa-game` to add automated tests that verify your game boots correctly, scenes transition properly, scoring works, and visuals haven't broken.
>
> **Pipeline progress:** ~~/make-game~~ → ~~/design-game~~ → ~~/add-audio~~ → `/qa-game` → `/review-game`
