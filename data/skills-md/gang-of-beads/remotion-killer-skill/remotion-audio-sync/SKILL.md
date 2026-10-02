---
name: remotion-audio-sync
description: Professional audio in Remotion — TTS narration orchestration, measuring audio to derive scene timings, music/beat sync and onset snapping, captions pipeline, ducking and mixing. Use whenever the video has narration, music, or captions.
---

# Audio, Narration & Sync

## Audio-first timing (the master pattern)

1. Generate TTS per scene offline (build script, never during render). Output one file per scene into `public/audio/`.
2. Measure durations at generation time with `ffprobe -v error -show_entries format=duration -of csv=p=0 file.mp3` and write them to a JSON manifest (no runtime probing).
3. Derive scene durations: `frames = Math.ceil((voDurationSec + bufferSec) * fps)` with buffer 0.3–0.8s tail padding.
4. Import the manifest in the composition and lay out `<Sequence from>` windows from it. Total duration = Σ scene frames.
5. For scripts that change length: pass the manifest as props and compute `durationInFrames` in `calculateMetadata` — one composition serves any script.

## Provider-agnostic by design

None of the steps below require a specific vendor. The skill defines an **interface contract**: any narration source (TTS API, local model, human recording) and any music source (music-gen model, stock track, self-composed) works as long as it can deliver:
- one audio file per scene (or per speaker), any format `ffprobe` can measure;
- optional word-level timings if you want captions without a transcription pass.

Pick whichever provider matches the user's account, region, budget, and quality bar. The tradeoffs below are guidance for choosing, not dependencies. Write a thin generation script per provider — everything downstream (timing, sync, mixing, QA) is provider-independent and never changes.

## TTS services (pick any, per user preference)

- ElevenLabs: best quality; multilingual models; some endpoints return word-level timestamps (skips the transcription pass for captions).
- Azure Speech: cheap, SSML control of pauses/rate/pitch — good for batch VO.
- OpenAI TTS: simple API, good quality, no word timings (pair with Whisper for captions).
- MiniMax Speech: multilingual T2A API, competitive quality.
- Multi-speaker: one voice per role, one file per scene per speaker; place speaker files inside the scene's `<Sequence>` so re-timing scenes never desyncs voices. Keep voices distinct in pitch AND pace; write SSML breaks between speaker turns.

## Music & beat sync

- Music source is provider-agnostic too: music-gen models (MiniMax Music, Suno, Udio, Lyria...), stock libraries, or your own composition. Only requirements: an offline audio file and (ideally) known/steady BPM. Generate or fetch offline (build script), export WAV for analysis.
- Beat/onset detection: run librosa (`librosa.onset.onset_detect` / beat tracking) or `aubio` offline; emit a JSON list of beat timestamps (ms).
- Convert to frames: `frame = Math.round(ms * fps / 1000)`. Snap cuts, transitions, and impact moments to the nearest beat frame.
- BPM math when the track has steady tempo: `framesPerBeat = fps * 60 / bpm` (30fps@120bpm = 15). Then beats are `frame % framesPerBeat === 0` — no detection needed for generated music where you control the BPM.
- Visual pulses: decay envelope per beat `pulse = Math.exp(-beatPhase * k)` (k ≈ 4–6) driving scale, glow (`boxShadow`/`textShadow` radius), or particle brightness.
- Real-time waveform-reactive visuals: `useAudioData()` + `visualizeAudio()` from `@remotion/media-utils` inside components (bars, circles) — frame-accurate and render-safe.
- Cutting on beats: place `<Sequence from>` values on beat frames; scene changes on downbeats feel intentional.
- Reverse snapping (visual-first): when visuals are already timed (e.g. a transition must land on a specific frame), find the nearest beat/onset from the beat JSON and either nudge the visual ±2–3 frames or generate the music at a BPM whose beat grid aligns (`bpm = 60 * fps / framesPerDesiredInterval`). Verify with sudden-volume-change detection against the scene-cut list (see remotion-video-qa).
- Generated-music prompt structure (MiniMax Music 3 and similar): describe genre, BPM, key, instruments, mood, arrangement arc (`intro → build → drop → outro`), and `instrumental only, no vocals` for BGM. BPM in the prompt makes the no-detection snap path usable; ask for a clean ending if the video must end in silence.
- Music level under narration: 0.10–0.15 volume (BGM), VO at 0.85–0.95. Manual ducking: interpolate BGM volume to ~0.05 during VO windows via `<Sequence>`-scoped `<Audio volume>`.

## Captions

- Pipeline: VO → word-level timed JSON → group into lines/pages → render as styled text.
- Transcription: OpenAI Whisper (`timestamp_granularities=["word"]`), Deepgram (word timings by default), or free/local `@remotion/install-whisper-cpp` (recommended OSS path for offline renders).
- Types from `@remotion/captions`: `Caption { text, startMs, endMs, timestampMs, confidence, pageBreakAfter? }`; helpers like `getTikTokStyledCaptions()` group words into caption pages.
- Karaoke highlight: current word gets color/scale pop; previous words full opacity; upcoming dimmed. Group to max 3–5 words per screen for social; full lines for corporate.
- Style captions as a component (position, background bar, stroke) — same tokens as the rest of the design; keep captions inside the safe area (bottom ~10% margin, higher on 9:16).

## Mixing & delivery

- Fades: `<Audio volume={interpolate(frame, [0, 15, end-15, end], [0, 1, 1, 0], {extrapolateLeft:"clamp"})}>` for music in/out.
- Target loudness -14 LUFS for online platforms; normalize the BGM and VO separately before muxing (ffmpeg `loudnorm`).
- Codec: AAC audio in h264 mp4 masters. WAV only for intermediate analysis.
- Gotchas: `getAudioDurationInSeconds` (browser context) needs `delayRender` if used during render and can fail on webm/opus — prefer ffprobe at generation time; audio paths via `staticFile` must match `public/` filenames exactly (404 fails the render mid-flight).
