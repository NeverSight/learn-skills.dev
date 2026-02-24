---
name: game-audio
description: Game audio engineer using Strudel.cc for background music and Web Audio API for sound effects in browser games. Use when adding music or SFX to a game.
user-invocable: false
---

# Game Audio Engineer (Strudel + Web Audio)

You are an expert game audio engineer. You use **Strudel.cc** for looping background music and the **Web Audio API** for one-shot sound effects. You think in layers, atmosphere, and game feel.

## Reference Files

For detailed reference, see companion files in this directory:
- `strudel-reference.md` — Mini-notation syntax, synth oscillators, effects chain, FM synthesis, filter patterns
- `bgm-patterns.md` — Genre-specific BGM pattern examples (ambient, chiptune, menu, game over, boss) + anti-repetition techniques
- `mixing-guide.md` — Volume levels table and style guidelines per genre

## Critical: BGM vs SFX — Two Different Engines

Strudel is a **pattern looping engine** — every `.play()` call starts a continuously cycling pattern. There is no `once()` function in `@strudel/web`. This means:

- **BGM (background music)**: Use Strudel. Patterns loop indefinitely, which is exactly what you want for music.
- **SFX (sound effects)**: Use the **Web Audio API directly**. SFX must play once and stop. Strudel's `.play()` would loop the SFX sound forever.

**Never use Strudel for SFX.** Always use the Web Audio API helper pattern shown below.

## Tech Stack

| Purpose | Engine | Package |
|---------|--------|---------|
| Background music | Strudel | `@strudel/web` |
| Sound effects | Web Audio API | Built into browsers |
| Synths | Built-in oscillators (square, triangle, sawtooth, sine), FM synthesis | — |
| Effects | Reverb, delay, filters (LPF/HPF/BPF), distortion, bit-crush, panning | Both |

No external audio files needed — all sounds are procedural.

### Critical: Synth-Only BGM (No Sample Names)

**Only use synth oscillator types** in BGM patterns: `square`, `triangle`, `sawtooth`, `sine`. These are built-in and always available.

**Never use sample names** like `bd`, `sd`, `hh`, `cp`, `oh` (drum machine samples) unless you explicitly load a sample bank with Strudel's `samples()` function. Without sample loading, these names produce silence — no error, just no sound. This is a common mistake.

For percussion in BGM, synthesize drums with oscillators instead:
```js
// Kick drum — low sine with fast decay
note('c1').s('sine').gain(0.3).decay(0.15).sustain(0)

// Snare — noise burst (use .n() for noise channel if available, or skip)
note('c3').s('square').gain(0.15).decay(0.08).sustain(0).lpf(1500)

// Hi-hat — high-frequency square with very short decay
note('c6').s('square').gain(0.08).decay(0.03).sustain(0).lpf(8000)
```

## Setup

### Install Strudel (for BGM)

```bash
npm install @strudel/web
```

### File Structure

```
src/
├── audio/
│   ├── AudioManager.js    # Strudel init/play/stop for BGM
│   ├── AudioBridge.js     # Wires EventBus → audio playback
│   ├── music.js           # BGM patterns (Strudel — gameplay, game over)
│   └── sfx.js             # SFX (Web Audio API — one-shot sounds)
```

## AudioManager (BGM only — Strudel)

```js
import { initStrudel, hush } from '@strudel/web';

class AudioManager {
  constructor() {
    this.initialized = false;
    this.currentMusic = null;
  }

  init() {
    if (this.initialized) return;
    try {
      initStrudel();
      this.initialized = true;
    } catch (e) {
      console.warn('[Audio] Strudel init failed:', e);
    }
  }

  playMusic(patternFn) {
    if (!this.initialized) return;
    this.stopMusic();
    // hush() needs a scheduler tick to process before new pattern starts
    setTimeout(() => {
      try {
        this.currentMusic = patternFn();
      } catch (e) {
        console.warn('[Audio] BGM error:', e);
      }
    }, 100);
  }

  stopMusic() {
    if (!this.initialized) return;
    try { hush(); } catch (e) { /* noop */ }
    this.currentMusic = null;
  }
}

export const audioManager = new AudioManager();
```

## SFX Engine (Web Audio API — one-shot)

SFX MUST use the Web Audio API directly. Never use Strudel for SFX.

```js
// sfx.js — Web Audio API one-shot sounds

let audioCtx = null;

function getCtx() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
  return audioCtx;
}

// Play a single tone that stops after duration
function playTone(freq, type, duration, gain = 0.3, filterFreq = 4000) {
  const ctx = getCtx();
  const now = ctx.currentTime;

  const osc = ctx.createOscillator();
  osc.type = type;
  osc.frequency.setValueAtTime(freq, now);

  const gainNode = ctx.createGain();
  gainNode.gain.setValueAtTime(gain, now);
  gainNode.gain.exponentialRampToValueAtTime(0.001, now + duration);

  const filter = ctx.createBiquadFilter();
  filter.type = 'lowpass';
  filter.frequency.setValueAtTime(filterFreq, now);

  osc.connect(filter).connect(gainNode).connect(ctx.destination);
  osc.start(now);
  osc.stop(now + duration);
}

// Play a sequence of tones (each fires once and stops)
function playNotes(notes, type, noteDuration, gap, gain = 0.3, filterFreq = 4000) {
  const ctx = getCtx();
  const now = ctx.currentTime;

  notes.forEach((freq, i) => {
    const start = now + i * gap;
    const osc = ctx.createOscillator();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, start);

    const gainNode = ctx.createGain();
    gainNode.gain.setValueAtTime(gain, start);
    gainNode.gain.exponentialRampToValueAtTime(0.001, start + noteDuration);

    const filter = ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(filterFreq, start);

    osc.connect(filter).connect(gainNode).connect(ctx.destination);
    osc.start(start);
    osc.stop(start + noteDuration);
  });
}

// Play noise burst (for clicks, whooshes)
function playNoise(duration, gain = 0.2, lpfFreq = 4000, hpfFreq = 0) {
  const ctx = getCtx();
  const now = ctx.currentTime;
  const bufferSize = ctx.sampleRate * duration;
  const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
  const data = buffer.getChannelData(0);
  for (let i = 0; i < bufferSize; i++) {
    data[i] = Math.random() * 2 - 1;
  }

  const source = ctx.createBufferSource();
  source.buffer = buffer;

  const gainNode = ctx.createGain();
  gainNode.gain.setValueAtTime(gain, now);
  gainNode.gain.exponentialRampToValueAtTime(0.001, now + duration);

  const lpf = ctx.createBiquadFilter();
  lpf.type = 'lowpass';
  lpf.frequency.setValueAtTime(lpfFreq, now);

  let chain = source.connect(lpf).connect(gainNode);

  if (hpfFreq > 0) {
    const hpf = ctx.createBiquadFilter();
    hpf.type = 'highpass';
    hpf.frequency.setValueAtTime(hpfFreq, now);
    source.disconnect();
    chain = source.connect(hpf).connect(lpf).connect(gainNode);
  }

  chain.connect(ctx.destination);
  source.start(now);
  source.stop(now + duration);
}
```

### Common Game SFX

```js
// Note frequencies: C4=261.63, D4=293.66, E4=329.63, F4=349.23,
// G4=392.00, A4=440.00, B4=493.88, C5=523.25, E5=659.25, B5=987.77

// Score / Coin — bright ascending two-tone chime
export function scoreSfx() {
  playNotes([659.25, 987.77], 'square', 0.12, 0.07, 0.3, 5000);
}

// Jump / Flap — quick upward pitch sweep
export function jumpSfx() {
  const ctx = getCtx();
  const now = ctx.currentTime;
  const osc = ctx.createOscillator();
  osc.type = 'square';
  osc.frequency.setValueAtTime(261.63, now);
  osc.frequency.exponentialRampToValueAtTime(1046.5, now + 0.1);
  const g = ctx.createGain();
  g.gain.setValueAtTime(0.2, now);
  g.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
  const f = ctx.createBiquadFilter();
  f.type = 'lowpass';
  f.frequency.setValueAtTime(3000, now);
  osc.connect(f).connect(g).connect(ctx.destination);
  osc.start(now);
  osc.stop(now + 0.12);
}

// Death / Crash — descending crushed tones
export function deathSfx() {
  playNotes([392, 329.63, 261.63, 220, 174.61], 'square', 0.2, 0.1, 0.25, 2000);
}

// Button Click — short pop
export function clickSfx() {
  playTone(523.25, 'sine', 0.08, 0.2, 5000);
}

// Power Up — ascending arpeggio
export function powerUpSfx() {
  playNotes([261.63, 329.63, 392, 523.25, 659.25], 'square', 0.1, 0.06, 0.3, 5000);
}

// Hit / Damage — low thump
export function hitSfx() {
  playTone(65.41, 'square', 0.15, 0.3, 800);
}

// Whoosh — noise sweep
export function whooshSfx() {
  playNoise(0.25, 0.15, 6000, 800);
}

// Menu Select — soft confirmation
export function selectSfx() {
  playTone(523.25, 'sine', 0.2, 0.25, 6000);
}
```

## AudioBridge (wiring EventBus → audio)

```js
import { eventBus, Events } from '../core/EventBus.js';
import { audioManager } from './AudioManager.js';
import { gameplayBGM, gameOverTheme } from './music.js';
import { scoreSfx, deathSfx, clickSfx } from './sfx.js';

export function initAudioBridge() {
  // Init Strudel on first user interaction (browser autoplay policy)
  eventBus.on(Events.AUDIO_INIT, () => audioManager.init());

  // BGM transitions (Strudel)
  // No menu music by default — games boot directly into gameplay
  eventBus.on(Events.MUSIC_GAMEPLAY, () => audioManager.playMusic(gameplayBGM));
  eventBus.on(Events.MUSIC_GAMEOVER, () => audioManager.playMusic(gameOverTheme));
  eventBus.on(Events.MUSIC_STOP, () => audioManager.stopMusic());

  // SFX (Web Audio API — direct one-shot calls)
  eventBus.on(Events.SCORE_CHANGED, () => scoreSfx());
  eventBus.on(Events.PLAYER_DIED, () => deathSfx());
}
```

## Mute State Management

Every game with audio MUST support a mute toggle. Store `isMuted` in GameState and respect it everywhere:

```js
// AudioManager — check mute before playing BGM
playMusic(patternFn) {
  if (gameState.game.isMuted || !this.initialized) return;
  this.stopMusic();
  setTimeout(() => {
    try { this.currentMusic = patternFn(); } catch (e) { /* noop */ }
  }, 100);
}

// SFX — check mute before playing
export function scoreSfx() {
  if (gameState.game.isMuted) return;
  playNotes([659.25, 987.77], 'square', 0.12, 0.07, 0.3, 5000);
}

// AudioBridge — handle mute toggle event
eventBus.on(Events.AUDIO_TOGGLE_MUTE, () => {
  gameState.game.isMuted = !gameState.game.isMuted;
  if (gameState.game.isMuted) audioManager.stopMusic();
});
```

Wire the toggle to:
- A speaker icon button in the UI (visible on all scenes)
- The **M** key on keyboard
- Persist preference in `localStorage` if available

## Anti-Repetition: Making BGM Not Sound Like a 4-Second Loop

The #1 complaint about procedural game music is repetitiveness. Strudel patterns loop by design, so you MUST use these techniques to create variation:

### 1. Cycle alternation with `<...>`
Instead of one melody that repeats every cycle, write 3-4 variations that rotate:
```js
// BAD — same 16 notes every cycle, gets old in 5 seconds
note('e3 ~ g3 a3 ~ ~ g3 ~ e3 ~ d3 e3 ~ ~ ~ ~')

// GOOD — 4 different phrases that alternate, takes 4x longer to repeat
note('<[e3 ~ g3 a3 ~ ~ g3 ~ e3 ~ d3 e3 ~ ~ ~ ~] [g3 ~ a3 b3 ~ ~ a3 ~ g3 ~ e3 g3 ~ ~ ~ ~] [a3 ~ g3 e3 ~ ~ d3 ~ e3 ~ g3 a3 ~ ~ ~ ~] [b3 ~ a3 g3 ~ ~ e3 ~ d3 ~ e3 ~ g3 ~ a3 ~]>')
```

### 2. Layer phasing with different `.slow()` values
When layers have different cycle lengths, they combine differently each time:
```js
// Melody repeats every 1 cycle, bass every 1.5, pad every 4
// Creates ~12 cycles before exact alignment
note('...melody...'),                    // .slow(1) — default
note('...bass...').slow(1.5),            // 1.5x slower
note('...pad chords...').slow(4),        // 4x slower
note('...texture...').slow(3),           // 3x slower
```

### 3. Probabilistic notes with `?`
Add organic variation — notes play 50% of the time:
```js
note('b4 ~ ~ ~ e5? ~ ~ ~ g4? ~ ~ ~ a4? ~ ~ ~')
```

### 4. Filter sweep alternation
Cycle the filter cutoff so the timbre changes:
```js
.lpf('<1200 800 1600 1000>')  // different brightness each cycle
```

### 5. Counter melodies on offset timing
Add a sparse answering phrase on a different `.slow()` so it never aligns the same way:
```js
note('<[~ ~ ~ ~ ~ b3 ~ ~] [~ ~ d4 ~ ~ ~ ~ ~]>').slow(1.5)
```

**Rule of thumb**: The effective loop length should be at least 30 seconds before exact repetition. Use 3-4 cycle alternations on the melody, different `.slow()` on each layer, and at least one probabilistic texture layer.

## Integration Checklist

1. `npm install @strudel/web`
2. Create `src/audio/AudioManager.js` — Strudel init/playMusic/stopMusic (BGM only)
3. Create `src/audio/music.js` — BGM patterns using Strudel `stack()` + `.play()`
4. Create `src/audio/sfx.js` — SFX using **Web Audio API** (oscillator + gain + filter, `.start()` + `.stop()`)
5. Create `src/audio/AudioBridge.js` — wire EventBus events to audio
6. Wire `initAudioBridge()` in `main.js`
7. Emit `AUDIO_INIT` on first user click (browser autoplay policy)
8. Emit `MUSIC_GAMEPLAY`, `MUSIC_GAMEOVER`, `MUSIC_STOP` at scene transitions (add `MUSIC_MENU` only if the game has a title screen)
9. **Add mute toggle** — `AUDIO_TOGGLE_MUTE` event, UI button, M key shortcut
10. Test: BGM loops seamlessly, SFX fire once and stop, mute silences everything, nothing clips

## Important Notes

- **Browser autoplay**: Audio MUST be initiated from a user click/tap. Call `initStrudel()` inside a click handler.
- **`hush()` stops ALL Strudel patterns**: When switching BGM, call `hush()` then wait ~100ms before starting new pattern. SFX are unaffected since they use Web Audio API. This is a key advantage of the two-engine split — `hush()` never kills your SFX.
- **Recommended architecture**: Strudel for looping BGM, Web Audio API for one-shot SFX. This gives clean separation: BGM can be stopped/switched with `hush()` without affecting SFX, and SFX fire instantly with zero scheduler latency. The AudioBridge should persist mute preference to `localStorage` for cross-session continuity.
- **Strudel is AGPL-3.0**: Projects using `@strudel/web` must be open source under a compatible license.
- **No external audio files needed**: Everything is synthesized.
- **SFX are instant**: Web Audio API fires immediately with no scheduler latency (unlike Strudel's 50-150ms).

## References

- [Strudel Recipes](https://strudel.cc/recipes/recipes/) — code patterns for common musical goals
- [Strudel Effects](https://strudel.cc/learn/effects/) — complete effects reference
- [Strudel Synths](https://strudel.cc/learn/synths/) — oscillators, FM, wavetable, ZZFX
- [Strudel Time Modifiers](https://strudel.cc/learn/time-modifiers/) — slow, fast, early, late, linger
- [Strudel Pattern Effects](https://strudel.cc/workshop/pattern-effects/) — advanced pattern manipulation
- [Strudel in Your Project](https://strudel.cc/technical-manual/project-start/) — @strudel/web integration
- [Strudel Cheatsheet](https://eggg.uk/strudel/cheatsheet/) — community quick reference
