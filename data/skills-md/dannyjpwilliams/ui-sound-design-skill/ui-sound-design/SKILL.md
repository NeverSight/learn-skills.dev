---
name: ui-sound-design
description: "Programmatic UI sound design using Web Audio API and Tone.js. Use when creating click sounds, notification chimes, toggle feedback, hover sounds, success/error audio, whoosh effects, or building a sound library for UI interactions. Provides an iterative describe-generate-listen-refine workflow with audio engineering knowledge translated into plain English."
license: MIT
metadata:
  author: dannyjpwilliams
  version: "1.0"
---

```
    ▁▂▄▆█▆▄▂▁

█  █ ██ ▄██▀ ██▀▄
█  █ ██  ▀▄  ██ █
▀██▀ ██ ▀██▄ ██▄▀
```

Describe what your UI should sound like.
Preview it, tweak it, and download it from the browser.

# UI Sound Design

Translate plain-English sound descriptions into working Web Audio API code. No audio engineering background needed — describe what you want to hear, and this skill provides the synthesis knowledge to make it real.

## Workflow

Every sound follows this loop: **Describe → Generate → Listen → Refine** (with optional **Review** for auditing existing code)

### 1. Describe

The user describes the sound in plain language. Ask clarifying questions using this framework:

**Four questions before generating any sound:**

1. **What triggers it?** (click, hover, toggle, notification, transition, success, error)
2. **What's the emotional tone?** (satisfying, subtle, urgent, playful, professional, minimal)
3. **How prominent should it be?** (barely perceptible, noticeable, attention-grabbing)
4. **Any reference points?** (iOS keyboard, Slack notification, macOS trash, game UI, "like a bubble popping")

If the user gives a vague request like "make a click sound", use sensible defaults from the recipes and generate immediately — don't over-ask.

### 2. Generate

1. Match the description to a **sound category** (see quick reference below)
2. Load the recipe from `references/sound-recipes.md`
3. Apply the **vocabulary bridge** to translate adjectives into parameter changes
4. For novel sounds not covered by recipes, compose from building blocks in `references/web-audio-api.md`
5. Output format: **HTML preview** by default (adapt `assets/sound-preview.html`), or ES module / React hook / class if requested

### 3. Listen

Provide the HTML preview file so the user can open it in a browser and hear the sound immediately. Each sound includes a download button that exports a .wav file for use in production code or handoff to developers. Include labeled buttons for each sound variation. The preview must:
- Handle AudioContext suspension (user gesture to start)
- Use the singleton AudioContext pattern
- Include visual feedback on play (the template handles this)

### 4. Refine

When the user gives feedback, translate it using the vocabulary bridge and adjust parameters. Common refinement patterns:
- "I like it but..." → tweak 1-2 parameters
- "Completely wrong" → try a different recipe/approach
- "Too much/little" → scale the relevant parameter up/down
- "More like X" → identify what makes X distinctive and match those characteristics

### 5. Review (optional)

Enter review mode when the user says "review", "audit", or "check my sound code", or pastes existing Web Audio code for evaluation.

**Steps:**
1. Load rules from `references/audio-rules.md`
2. Scan the code against each rule, starting with Critical priority
3. Report findings using the format in `audio-rules.md` — one line per violation with `file:line — [rule-id] description`
4. Provide a summary table (pass/fail counts by priority)
5. Suggest concrete fixes for each failing rule

**When to stay in generate mode:** If the user's request is ambiguous (e.g., "here's my click sound" without asking for review), default to the generative workflow. Only enter review mode when the intent to audit is clear.

## Vocabulary Bridge

This is the core translation layer. When the user uses subjective language, map it to synthesis parameters:

| User Says | Parameter Change | Example |
|-----------|-----------------|---------|
| "Brighter" | Raise frequency or filter cutoff | Filter cutoff 1500 → 3000 Hz |
| "Warmer" | Lower filter cutoff, use sine/triangle wave | Switch sawtooth → sine, cutoff 3000 → 1200 |
| "Darker" | Lower frequency, reduce high harmonics | Add lowpass filter at 800 Hz |
| "Snappier" | Shorter attack and decay | Decay 0.15 → 0.05s |
| "Softer" | Lower volume, longer attack, gentle envelope | Volume 0.3 → 0.15, attack 0 → 0.01s |
| "Louder" / "More prominent" | Raise volume (max 0.8) | Volume 0.2 → 0.4 |
| "Fuller" / "Richer" | Layer oscillators, add detune | Add second osc detuned +7 cents |
| "Thinner" | Remove layers, use sine wave, raise highpass | Single sine, highpass at 500 Hz |
| "More metallic" | FM synthesis, inharmonic ratios | Mod ratio 1.4, increase mod depth |
| "More organic" / "Natural" | Use noise components, subtle randomness | Mix in filtered noise burst |
| "Shorter" / "Crisper" | Reduce total duration | Duration 0.15 → 0.06s |
| "Longer" / "More sustained" | Increase duration and sustain | Duration 0.1 → 0.3s, add sustain phase |
| "More playful" | Higher pitch, bounce/overshoot | Frequency +200 Hz, add pitch overshoot |
| "More professional" | Subtle, clean, minimal | Lower volume, sine wave, short duration |
| "Retro" / "8-bit" | Square wave, quantized pitch | Switch to square, use note frequencies |
| "Bubbly" | Rapid pitch drop, sine wave | startFreq 2000, quick exponential drop |

## Sound Categories — Quick Reference

| Category | Duration | Recipe | Trigger | Key Character |
|----------|----------|--------|---------|---------------|
| Click | 10–80ms | `references/sound-recipes.md#click` | Button press, tap | Noise burst, bandpass filtered |
| Toggle | 80–200ms | `references/sound-recipes.md#toggle` | Switch on/off | Rising/falling pitch sweep |
| Hover | 30–80ms | `references/sound-recipes.md#hover` | Mouse enter | Gentle, nearly subliminal |
| Success | 200–500ms | `references/sound-recipes.md#success` | Task complete, save | Ascending major third |
| Error | 150–400ms | `references/sound-recipes.md#error` | Validation fail, rejected | Descending, buzzy |
| Warning | 150–350ms | `references/sound-recipes.md#warning` | Caution state | Double pulse, mid-range |
| Notification | 200–800ms | `references/sound-recipes.md#notification` | New message, alert | Bell-like FM synthesis |
| Whoosh | 100–400ms | `references/sound-recipes.md#whoosh` | Page transition, slide | Filtered noise sweep |
| Pop | 30–80ms | `references/sound-recipes.md#pop` | Add item, bubble, appear | Sine with pitch drop |
| Custom | varies | `references/web-audio-api.md` | Anything else | Compose from building blocks |

## Critical Implementation Rules

### AudioContext user-gesture requirement
Browsers block audio until a user interaction (click, tap, keydown). Always initialize or resume the AudioContext inside an event handler. The singleton pattern in `references/web-audio-api.md` handles this.

### Never ramp gain to zero
`exponentialRampToValueAtTime(0, ...)` throws an error. Always ramp to `0.001` — it's inaudible but mathematically valid. This applies to every sound. No exceptions.

### Node cleanup
- OscillatorNodes auto-disconnect after `stop()` — no manual cleanup needed
- BufferSourceNodes are one-shot — create a new one each play
- For long-lived filter/gain nodes, call `disconnect()` when done
- Never create a new AudioContext per sound — use the singleton

### Volume safety
- Default volume: `0.3` (gain value)
- Maximum volume: `0.8` — never exceed this
- Hover sounds: `0.03–0.08` (barely perceptible)
- UI sounds should complement, not dominate — err on the side of quiet

### Scheduling precision
Capture `const now = ctx.currentTime` once at the start of each sound function. Derive all scheduling times from `now`. Never read `currentTime` multiple times.

### Use exponential ramps by default
`exponentialRampToValueAtTime` sounds natural for both volume and frequency. `linearRampToValueAtTime` sounds mechanical. Only use linear for sub-50ms transitions.

## Output Formats

### HTML Preview (default)
Adapt `assets/sound-preview.html`. Self-contained, no dependencies, opens in any browser. Best for the iterative listen-refine loop. Includes WAV download — click the download button on any sound to get a .wav file. Sound functions must use `(ctx, dest)` parameters with fallback defaults for download support, and each sound needs a matching entry in the `durations` map.

### ES Module
```javascript
// ui-sounds.js
export function playClick(options) { /* ... */ }
export function playSuccess(options) { /* ... */ }
```

### React Hook
```javascript
// useUISound.js
export function useUISound() {
  const ctxRef = useRef(null);
  const getCtx = useCallback(() => { /* singleton */ }, []);
  return { playClick, playSuccess, /* ... */ };
}
```

### Sound Library Class
Use the `UISoundLibrary` class from `references/sound-recipes.md`. Bundles all sounds with enable/disable and master volume control.

## Resources

### references/
- **`web-audio-api.md`** — Core Web Audio API building blocks: oscillators, envelopes, filters, noise, FM synthesis, factory patterns, common mistakes. Load when building custom sounds or understanding low-level mechanics.
- **`sound-recipes.md`** — Complete working implementations for all 9 sound categories plus a bundled `UISoundLibrary` class. Each recipe includes parameters, code, tuning guide, and variations. **Start here for most requests.**
- **`audio-rules.md`** — Formal validation rules with IDs, priorities, and pass/fail examples. Load when reviewing existing code or when you need to verify generated output against best practices.
- **`tone-js.md`** — Tone.js abstractions for faster prototyping. Simplified synth types, recipe equivalents, effects, and a conversion guide to vanilla Web Audio. Load when the user prefers Tone.js or wants rapid iteration.

### assets/
- **`sound-preview.html`** — Self-contained HTML template with all 10 default sounds, visual feedback, and AudioContext handling. Adapt this for every preview output.
