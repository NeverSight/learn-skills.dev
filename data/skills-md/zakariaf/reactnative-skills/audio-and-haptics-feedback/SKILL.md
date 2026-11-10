---
name: audio-and-haptics-feedback
description: Builds SFX and haptics behind ports. Use when adding or tuning sounds, SFX, music or haptics, or sound ignores the silent switch, stops the user's music or a pulse fails on Android. Not for settings (settings-and-preferences).
---

# Audio and haptics feedback

Every sound an Expo app plays as feedback is synthesised from a literal recipe and played through one
ambient `AudioContext` behind `AudioPort`; every pulse is a cue from a fixed table played through
`HapticsPort` on iOS and Android, gated by the user's preference and throttled. This skill builds the
ports, the cue tables, the banks, and the two checkers that prove them.

## Rules that must hold

1. **One engine each, behind ports.** Only `src/services/audio/audio-api-audio-adapter.ts` imports
   `react-native-audio-api` and only `src/services/haptics/expo-haptics-adapter.ts` imports
   `expo-haptics`; nothing imports `react-native-sound` or `react-native-haptic-feedback`, the feedback
   layer imports no media player, and `Vibration` never appears in the feedback layer or a view
   (elsewhere only with `// vibration-exempt: <reason>`). Tests use `createFakeAudio()`/`createFakeHaptics()`.
   Why: one file changes on a bump, two engines fight over the session, and tests run without native code.
2. **Pin react-native-audio-api exactly and override all five plugin defaults** (`iosBackgroundMode:
   false`, `androidPermissions: []`, `androidForegroundService: false`, `disableFFmpeg: true`,
   `disableStaticExternalLibs: true`) through `AUDIO_API_PLUGIN` in `app.config.ts`; a new version goes
   through "Before any bump" and is recorded in `contracts/audio-feedback.json`. Why: the library is
   pre-1.0, and the defaults add background audio, Android foreground-service permissions and
   build-time downloads.
3. **One AudioContext, created in the adapter after `setAudioSessionOptions({ iosCategory: 'ambient' })`,
   and no audio focus on Android** (`observeAudioInterruptions(true)` only under `Platform.OS === 'ios'`).
   Why: ambient respects the silent switch and mixes with the user's music; on Android that call requests
   `AUDIOFOCUS_GAIN`, which fades out and mutes the user's music.
4. **Every sound is a literal `SoundRecipe` that passes `recipeProblems`** (finite, peak 0.05-0.9, first
   sample < 0.05, last < 0.01, later layers fade in over at least 1 ms, 10-1500 ms, music up to 30 s);
   the app's synth renders byte-identically to the checker's port. No streaming and no URL audio in the
   feedback layer; every recorded audio file in the repo is listed with its licence and source in the
   contract (`bundledSounds` for feedback, `otherAudio` for a notification sound or a feature's media).
   Why: no clicks, no clipping, no licences to chase, previews that are exactly what the device plays.
5. **Banks and ids:** kebab-case nouns for what happened; `ui.` is reserved for `UI_SOUNDS`; each feature
   or game bank lives in `<owner>/sounds/<owner>-sounds.ts` as `<OWNER>_SOUNDS`, is tested, and is
   composed once in the root layout with `composeSoundBank` (which throws on a clash). Every cue names an
   id of its owner's bank and every sfx id is cued. Why: a typo is silence in production, a clash
   silently replaces another sound.
6. **Keep the voice policy:** three category gains (`sfx` and `ui` follow sound effects, `music`
   follows music), `volume²`, 50 ms ramps, at most 8 overlapping voices, the same sound at most once per
   30 ms (or its `minIntervalMs`, at most 1000), voices as intervals on the audio clock, released by
   `cancelPending`. Why: even loudness, no clicks, no pile-ups, no sound lost after a fast action.
7. **Music is off by default, never `activelyReclaimSession`, and every music control is hidden when
   `hasMusic(bank)` is false.** Why: the library cannot tell whether the user's own audio plays, so the
   app never plays over it unasked.
8. **Feedback fires from events on JS:** a feature's cue table played by its model (`playCue`), a canvas
   track cue scheduled on the audio clock, a UI moment (`playUiFeedback`), or drained sim events; never
   from a view's own handler, a sim, a `'worklet'` module or per frame, and each event in one place
   only; views (`src/ui`, a feature's screen or components) never call `audio.play`, `playCue` or
   `playUiFeedback`. Why: sync with the animation, and the UI thread never touches a port.
9. **Mount `useAudioLifecycle` once, in the root layout;** the context runs only while the app is active
   and nothing full-screen plays; iOS interruptions suspend it and resume it only if the lifecycle
   still wants it running (with a direction gate, mount it and load the bank behind the gate); `await audio.dispose()`
   before every JS reload, or await an injected `beforeReload` hook that the caller wires to
   `() => services.audio.dispose()`, or say why with `// audio-dispose-exempt: <reason>`. Why: no sound
   in the background or over a video, and the native engine closes before the bundle reloads.
10. **Haptics follow the cue table on both platforms** (iOS feedback generators; Android
    `performAndroidHapticsAsync` constants, an API 30 table and a legacy one), only while the user's
    preference is on, at least 40 ms apart, each call ending in `.catch(() => undefined)` inside the
    adapter; `isSupported` is false on iPad. Views use only `selection` (switches, pickers). Why: bursts
    feel like a buzz, a newer Android constant rejects on older phones, and buttons should not buzz.
11. **The app-wide moments go through `UI_FEEDBACK`** (by default `toggle`, `success`, `error`; the
    table is the app's), each moment it keeps played from a model; buttons are silent by default, and an
    app that adds a `tap` moment renders `<PressFeedbackProvider playsSound onPress={...}>` that plays
    it (the canonical press surface then sets `android_disableSound` itself; no synced file is edited).
    Why: one forgotten handler is a silent switch, and Android would play its own click on top of the tap.
12. **Add no microphone purpose string up front;** only if an App Store upload reports ITMS-90683, set
    `iosMicrophonePermission` (localised, with a comment naming ITMS-90683). Why: feedback never records,
    and an unused purpose string invites review questions.
13. **A green gate proves a sound is clean, not right.** Render the WAV previews, list the listening and
    the feel on a real iPhone and Android phone for a human, and never block on the answer; test builds
    prove requests with the recording decorators. Why: an agent cannot hear and simulators have no
    haptic engine.

## Workflow

1. **Pick the job.** A new feedback layer: steps 2-6. Sounds for a feature or game: steps 7-9. Tuning a
   sound: steps 8-9. Bumping the library: step 10. Always finish with step 11.
2. **Read** [references/audio-engine.md](references/audio-engine.md) (library, plugin, port, adapter,
   session and focus, lifecycle, music, wiring, testing) and [references/haptics.md](references/haptics.md)
   (cue table on both platforms, throttle, devices).
3. **Copy the templates** at the paths their first line names (tests included): `templates/src/services/audio/`
   (with `synth/`), `templates/src/services/haptics/`, `templates/src/services/feedback/`,
   `templates/src/services/test-hooks/recording-feedback.ts` (test builds only),
   `templates/src/config/audio-plugin.ts`, `templates/__mocks__/react-native-audio-api.ts`,
   `templates/contracts/audio-feedback.json` (+ schema). `src/hooks/use-is-app-active.ts`,
   `src/ui/press-feedback-context.tsx` and `src/core/rng/sfc32.ts` belong to other skills; copy them
   only if the app lacks them. A haptics-only app copies `haptics/` alone; the checker then notes that
   the audio rules do not apply.
4. **Install:** `npx expo install expo-haptics` and `npm install --save-exact react-native-audio-api@0.13.6`
   (dependency-management records both in its policy). Add `AUDIO_API_PLUGIN` to `app.config.ts`
   plugins; check that `.gitignore` ignores `reports/`.
5. **Wire the composition root** (the lines are in audio-engine.md, "Wiring"): `audio` and `haptics` in
   `Services`, `createDeviceServices` and `createTestServices`; the haptics preference read at call
   time (settings-and-preferences owns it). In the root layout, `services.audio.load(composeSoundBank(...))`
   in the startup initializer and `useAudioLifecycle(...)` once; imitate
   [examples/root-layout-wiring.tsx](examples/root-layout-wiring.tsx). Make every reload path dispose first.
6. **Wire the moments** ([references/feedback-moments.md](references/feedback-moments.md)):
   `playUiFeedback(services, 'toggle')` in switch handlers (the canonical one: the settings model's
   `onToggled`), `'success'`/`'error'` where a requested action ends. Tap sounds only if the app wants
   them (the opt-in there).
7. **Plan the sounds.** Read [references/sound-design.md](references/sound-design.md). Write the event →
   sound → haptic table: most events get nothing, three to six sounds per feature, the most repeated the
   quietest, loud and long only for rare moments.
8. **Write the bank and the cue table test-first.** Copy `templates/src/features/__FEATURE__/` (bank,
   cue table, their tests), replace `__FEATURE__`, `__FEATURE_PASCAL__`, `__FEATURE_SOUNDS__` and
   `__FEATURE_FEEDBACK__`, write one literal recipe per sound, play each row from the model with
   `playCue` (or put it on the canvas track), add the bank to `composeSoundBank`, run
   `npx prettier --write src/features/<feature>` on the copied files, and run
   `npx jest src/features/<feature> --ci --selectProjects unit` until green (paths before the flag).
9. **Render and hand over the listening:** `node ${CLAUDE_SKILL_DIR}/scripts/check-sound-banks.mjs . --wav-dir reports/sfx`,
   fix every `FAIL`, then list the listening as in [examples/listening-checklist.md](examples/listening-checklist.md).
   Carry on; when a human answers, tune one number at a time and re-render.
10. **Bumping react-native-audio-api:** follow "Before any bump" in audio-engine.md (release notes,
    plugin defaults, mock, focus code, adapter tests, a smoke test on a named iOS simulator and Android
    emulator, a listening check), then set `audioApiVersion` in `contracts/audio-feedback.json` with the pin.
11. **Run the checks** until both print `RESULT: PASS`: `node ${CLAUDE_SKILL_DIR}/scripts/check-sound-banks.mjs .`
    then `node ${CLAUDE_SKILL_DIR}/scripts/check-audio-haptics.mjs .`. Each `FAIL` names the file, the
    rule and the fix. Then `npx jest src/services src/features/<feature> --ci --selectProjects unit android`.

## Definition of done

- [ ] The audio, haptics and feedback services, the config plugin and the root mock exist as in
      `templates/`, and their tests pass in the unit and android Jest projects.
- [ ] `react-native-audio-api` is pinned to the contract's `audioApiVersion` (default 0.13.6),
      `expo-haptics` has the SDK's `~` range, `AUDIO_API_PLUGIN` is in `app.config.ts`, and there is no
      microphone purpose string without ITMS-90683.
- [ ] Every feature or game with sounds has a tested literal bank composed in the root layout, and a
      cue table (or track cues) that names only its ids.
- [ ] Music is off by default and its controls are hidden without music; the haptics row is hidden when
      `isSupported` is false (settings-and-preferences builds the rows).
- [ ] `useAudioLifecycle` is mounted once; every reload disposes the engine or carries an exemption reason.
- [ ] Every `UI_FEEDBACK` moment is played from a model; tap sounds only as the documented opt-in.
- [ ] The WAV previews are rendered and the listening on an iPhone and an Android phone is listed for a
      human (not blocking).
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-sound-banks.mjs .` prints `RESULT: PASS`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-audio-haptics.mjs .` prints `RESULT: PASS` (a haptics-only
      app prints the note `audio rules not applicable: ...`; an app with no feedback layer prints `NOT APPLICABLE`)

## Anti-patterns

- **An `AudioContext` in a screen or hook.** Two contexts fight over the session and double the memory;
  the adapter owns the only one.
- **`AudioManager.observeAudioInterruptions(true)` on every platform.** On Android it takes audio focus
  and silences the user's podcast at the first tap sound.
- **`audio.play(...)` in a view's `onPress` or a `useEffect` for an animated event.** The sound drifts from
  the animation and the event plays twice; play the cue table row from the model, or the track cue
  (the checker's `view-feedback` rule).
- **Wiring a settings switch to `usePressFeedback()`.** Without the tap opt-in it is a no-op, so the
  switch is silent; with it, the switch plays `tap`. The model's `onToggled` plays `toggle`.
- **A cue on every particle track, or a pulse per completed item.** One visible event, one cue; the
  voice limit and the throttle would drop the rest at random.
- **Pulsing on every button press.** Buttons are silent to the hand; only switches and pickers use `selection`.
- **`impactAsync` on Android.** It drives the Vibrator directly; `performAndroidHapticsAsync` follows the
  system's touch-feedback setting.
- **Shipping a downloaded sound "just this once".** It brings a licence, a file the checker rejects and
  possibly a network path; synthesize a recipe, or list a bundled file in the contract.
- **Turning music on by default to make the app feel livelier.** It plays over the user's music; ask the
  developer, and build the silence-hint check first.
- **Tuning by reading numbers, or blocking a change on the listening.** The gate proves clean, not right;
  render the previews, list them for a human, and carry on.
- **Raising `MAX_VOICES`, lowering the 40 ms throttle or widening the gate to pass a check.** Fix the
  recipe or the cue; the limits exist because the failures are audible.
- **Importing `expo-haptics` or `react-native-audio-api` in a test.** `jest.mock` + `jest.requireMock`
  in the adapter test; fakes everywhere else.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/audio-engine.md](references/audio-engine.md) | Versions, the plugin on iOS and Android, ITMS-90683, the one iOS session next to media, port, adapter (session, focus), voice policy, banks, lifecycle and the reload seam, music, wiring, testing, recorded audio (notification, media, bundled), licence rows, bump list, multi-package | Workflow steps 2-5 and 10 |
| [references/haptics.md](references/haptics.md) | Haptics port, the cue table for iOS and Android (with the legacy table), rules of use, throttle, devices and failure modes, tests | Workflow step 2, and when choosing a cue |
| [references/sound-design.md](references/sound-design.md) | Recipe model, quality gate, design starting points, ids and banks, cue tables and track cues, real-time games, WAV previews, the human check, the Tasks example | Workflow steps 7-9 |
| [references/feedback-moments.md](references/feedback-moments.md) | UI_FEEDBACK and the settings model's toggle, the tap opt-in (`playsSound`, `android_disableSound`), feature cue tables, settings and hidden rows, recording decorators, where the checkers are heuristic | Workflow step 6; when a checker misses or flags a shape |
| `templates/src/services/audio/` | Port, adapter (+ unit and android tests: no audio focus on Android), voice policy (+ test), fake (+ test), lifecycle hook (+ test), `composeSoundBank`/`hasMusic` (+ test), `synth/` (synth, gate, `UI_SOUNDS`, tests) | Step 3 (copy) |
| `templates/src/services/haptics/` | Port, `shouldPulse` (+ test), expo-haptics adapter with the iOS table and the three Android tables (+ unit and android tests), fake (+ test) | Step 3 (copy) |
| `templates/src/services/feedback/` | `playCue`, `UI_FEEDBACK`/`playUiFeedback`, each with its test | Steps 3 and 6 |
| `templates/src/services/test-hooks/` | `recording-feedback.ts`: the test-build recording decorators (a test-only folder, reached only through the test-only entry), with its test | Step 6 |
| `templates/src/features/__FEATURE__/` | A feature's bank (+ gate test) and cue table (+ test), filled for the Tasks app's `tasks` feature | Step 8 |
| [templates/src/config/audio-plugin.ts](templates/src/config/audio-plugin.ts) | `AUDIO_API_PLUGIN` with every default overridden (+ test) | Step 4 |
| `templates/src/config/audio-plugin.test.ts` | Pins the five overrides | Step 4 |
| `templates/contracts/` | `audio-feedback.json` (verified version, bundled sounds) and its JSON schema | Step 3; on a bump or a bundled sound |
| [templates/__mocks__/react-native-audio-api.ts](templates/__mocks__/react-native-audio-api.ts) | Root Jest mock completing the library mock's AudioManager (synced; this skill owns the canonical copy) | Step 3 |
| `templates/src/hooks/` | `use-is-app-active.ts` (+ test): the foreground check (synced from react-components-and-hooks; do not edit here) | Step 3, only if missing |
| `templates/src/ui/` | `press-feedback-context.tsx` (+ test): the press-feedback seam (synced from design-system-structure; do not edit here) | Step 6, tap opt-in only |
| `templates/src/core/rng/` | `sfc32.ts` (+ test): the seeded PRNG the synth's noise uses (synced from seeded-determinism-and-golden-vectors; do not edit here) | Step 3, only if missing |
| [examples/root-layout-wiring.tsx](examples/root-layout-wiring.tsx) | Root layout shape: compose the bank, mount the lifecycle once, dispose before a reload, the crash exemption | Step 5 |
| [examples/bundled-sound-loading.ts](examples/bundled-sound-loading.ts) | Shape of the opt-in recorded-sound decoding inside the adapter | Only when shipping a recorded sound |
| [examples/listening-checklist.md](examples/listening-checklist.md) | The human listening and feel follow-up for a change report | Step 9 |
| `scripts/check-audio-haptics.mjs` | Engines, pins, plugin, mic string, context and focus, file audio, voice and haptic policies (iOS and Android), call sites and views, UI moments, tap opt-in, lifecycle, dispose-before-reload (and the seam), root mock | Steps 3 and 11 |
| `scripts/check-sound-banks.mjs` | Renders every sound with the byte-exact synth port, gate, ids, categories, cues against banks, bank tests and wiring, synth drift; `--wav-dir` writes previews, `--owner` narrows | Steps 9 and 11 |
| `scripts/selftest.mjs` | Proves both checkers pass the templates and catch every planted bug | After changing a checker or a template |
| `scripts/lib/synth.mjs` | Synth, sfc32, gate and WAV port with a pinned golden hash | When changing the synth |
| `scripts/lib/ts-literal.mjs` | Reads TypeScript literal data without a compiler (synced; do not edit here) | Never by hand |
| `scripts/lib/app-modules.mjs` | Loads the app's pure TypeScript for the synth-drift rule (synced; do not edit here) | Never by hand |
| `scripts/check-lib.mjs` | Shared script helper (synced; do not edit here) | Never by hand |
| `assets/shared.json` | The shared files this skill copies in | When adding a shared file |
| `assets/template-placeholders.json` | Placeholder values verify-templates and the self-test fill in | When adding a placeholder |
| `tests/` | `bases/app/` (stand-ins for the app's root layout, models, a game) and `fixtures/` (overlay cases for both checkers) | When adding a rule |

## Related skills

- `settings-and-preferences` - the sound, music and haptics rows, their defaults, the settings-to-audio glue.
- `skia-canvas-rendering` - timeline track cues and the cue scheduler that calls these ports.
- `design-system-structure` - the press surface and the press-feedback context.
- `architecture-and-boundaries` - ports, adapters and the composition root.
- `dependency-management` - installing and pinning, the policy file.
- `error-handling-typed-results` - the one licensed best-effort swallow.
- `react-components-and-hooks` - `useIsAppActive`.
- `realtime-game-loop` - drained sim events that become sounds and haptics.
- `e2e-maestro`, `debug-menu-and-test-hooks` - asserting recorded feedback in test builds.
- `ios-release-testflight` - upload warnings such as ITMS-90683.
