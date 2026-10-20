---
name: game-audio
description: Game audio engineer using Web Audio API for procedural music and sound effects in browser games. Zero dependencies. Use when adding music or SFX to a game.
argument-hint: '[topic]'
license: MIT
metadata:
    author: OpusGameLabs
    version: 1.3.0
    tags: [game, audio, music, sfx, web-audio-api, bgm]
---

# Game Audio Engineer (Web Audio API)

You are an expert game audio engineer. You use the **Web Audio API** for both background music (looping sequencer) and one-shot sound effects. Zero dependencies — everything is built into the browser.

## Performance Notes

- Take your time with each step. Quality is more important than speed.
- Do not skip validation steps — they catch issues early.
- Read the full context of each file before making changes.
- Test every sound in the browser. Web Audio timing is different from what you expect.

## Reference Files

For detailed reference, see companion files in this directory:

- `sequencer-pattern.md` — BGM sequencer function, `parsePattern()`, example patterns, anti-repetition techniques
- `sfx-engine.md` — `playTone()`, `playNotes()`, `playNoise()`, all SFX presets
- `mute-button.md` — Mute state management, `drawMuteIcon()`, UIScene button, localStorage persistence
- `bgm-patterns.md` — Strudel BGM pattern examples
- `strudel-reference.md` — Strudel.cc API reference
- `mixing-guide.md` — Volume levels table and style guidelines per genre

## Tech Stack

| Purpose          | Engine                                               | Package             |
| ---------------- | ---------------------------------------------------- | ------------------- |
| Background music | Web Audio API sequencer                              | Built into browsers |
| Sound effects    | Web Audio API one-shot                               | Built into browsers |
| Synths           | OscillatorNode (square, triangle, sawtooth, sine)    | —                   |
| Effects          | GainNode, BiquadFilterNode, ConvolverNode, DelayNode | —                   |

No external audio files or npm packages needed — all sounds are procedural.

## File Structure

```
src/
├── audio/
│   ├── AudioManager.js    # AudioContext init, BGM sequencer, play/stop
│   ├── AudioBridge.js     # Wires EventBus → audio playback
│   ├── music.js           # BGM patterns (sequencer note arrays)
│   └── sfx.js             # SFX (one-shot oscillator + gain + filter)
```

## AudioManager (BGM Sequencer + AudioContext)

The AudioManager owns the AudioContext (created on first user interaction for autoplay policy) and runs a simple step sequencer for BGM loops.

```js
// AudioManager.js — Web Audio API BGM sequencer + SFX context

class AudioManager {
    constructor() {
        this.ctx = null;
        this.currentBgm = null; // { stop() }
        this.masterGain = null;
    }

    init() {
        if (this.ctx) return;
        this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        this.masterGain = this.ctx.createGain();
        this.masterGain.connect(this.ctx.destination);
    }

    getCtx() {
        if (!this.ctx) this.init();
        return this.ctx;
    }

    getMaster() {
        if (!this.masterGain) this.init();
        return this.masterGain;
    }

    playMusic(patternFn) {
        this.stopMusic();
        try {
            this.currentBgm = patternFn(this.getCtx(), this.getMaster());
        } catch (e) {
            console.warn('[Audio] BGM error:', e);
        }
    }

    stopMusic() {
        if (this.currentBgm) {
            try {
                this.currentBgm.stop();
            } catch (_) {}
            this.currentBgm = null;
        }
    }

    setMuted(muted) {
        if (this.masterGain) {
            this.masterGain.gain.value = muted ? 0 : 1;
        }
    }
}

export const audioManager = new AudioManager();
```

## BGM Sequencer Pattern

See `sequencer-pattern.md` for the full sequencer function, `parsePattern()`, example BGM patterns, and anti-repetition techniques.

## SFX Engine (Web Audio API -- one-shot)

See `sfx-engine.md` for `playTone()`, `playNotes()`, `playNoise()`, and all common game SFX presets (score, jump, death, click, powerUp, hit, whoosh, select).

## AudioBridge (wiring EventBus -> audio)

```js
import { eventBus, Events } from '../core/EventBus.js';
import { audioManager } from './AudioManager.js';
import { gameplayBGM, gameOverTheme } from './music.js';
import { scoreSfx, deathSfx, clickSfx } from './sfx.js';

export function initAudioBridge() {
    // Init AudioContext on first user interaction (browser autoplay policy)
    eventBus.on(Events.AUDIO_INIT, () => audioManager.init());

    // BGM transitions
    eventBus.on(Events.MUSIC_GAMEPLAY, () => audioManager.playMusic(gameplayBGM));
    eventBus.on(Events.MUSIC_GAMEOVER, () => audioManager.playMusic(gameOverTheme));
    eventBus.on(Events.MUSIC_STOP, () => audioManager.stopMusic());

    // SFX (one-shot)
    eventBus.on(Events.SCORE_CHANGED, () => scoreSfx());
    eventBus.on(Events.PLAYER_DIED, () => deathSfx());
}
```

## Mute State Management

See `mute-button.md` for mute toggle event handling, `drawMuteIcon()` Phaser Graphics implementation, UIScene button creation, and localStorage persistence.

## Integration Checklist

1. Create `src/audio/AudioManager.js` — AudioContext + sequencer + master gain
2. Create `src/audio/music.js` — BGM patterns as note arrays + sequencer calls
3. Create `src/audio/sfx.js` — SFX using Web Audio API (oscillator + gain + filter)
4. Create `src/audio/AudioBridge.js` — wire EventBus events to audio
5. Wire `initAudioBridge()` in `main.js`
6. Emit `AUDIO_INIT` on first user click (browser autoplay policy)
7. Emit `MUSIC_GAMEPLAY`, `MUSIC_GAMEOVER`, `MUSIC_STOP` at scene transitions
8. **Add mute toggle** — `AUDIO_TOGGLE_MUTE` event, UI button, M key shortcut
9. Test: BGM loops seamlessly, SFX fire once and stop, mute silences everything

## Important Notes

- **Zero dependencies**: Everything uses the built-in Web Audio API. No npm packages needed for audio.
- **Browser autoplay**: AudioContext MUST be created/resumed from a user click/tap. The `AUDIO_INIT` event handles this.
- **Master gain for mute**: Route everything through a single GainNode. Setting `gain.value = 0` mutes all audio instantly.
- **Sequencer timing**: The look-ahead scheduler (schedules 100ms ahead, checks every 25ms) gives sample-accurate timing with no drift. This is the standard Web Audio scheduling pattern.
- **No external audio files needed**: Everything is synthesized with oscillators.
- **SFX are instant**: Web Audio API fires immediately with zero scheduler latency.

## Optional: Strudel.cc Upgrade

For richer procedural BGM with pattern language support, you can optionally install `@strudel/web`:

```bash
npm install @strudel/web
```

**Note**: Strudel is **AGPL-3.0** — projects using it must be open source. See `strudel-reference.md` and `bgm-patterns.md` in this directory for Strudel-specific patterns.

The Strudel upgrade replaces the Web Audio sequencer for BGM only. SFX always use Web Audio API directly.
