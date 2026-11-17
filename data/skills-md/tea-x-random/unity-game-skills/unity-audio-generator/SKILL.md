---
name: unity-audio-generator
description: "Generate, convert, clean, and import audio for Unity casual games using ElevenLabs, then import as AudioClips with mobile-correct settings. Use for sound effects, looping ambience/music beds, UI sounds (tap/win/coin/level-up), impact/collectible/power-up audio, announcer/voice/TTS lines, voice conversion, and audio cleanup/isolation. Owns the seamless-loop crossfade and target-LUFS normalization post-processes (loopify/normalize; seamless loops are NOT an ElevenLabs feature) and routes production clips through per-clip contracts + the approved-asset registry (unity-asset-pipeline) under the art-spec audio-direction block. Covers Unity AudioClip import: compression (Vorbis), load type by clip length, force-to-mono, loop flag, target LUFS, and mobile memory budgeting."
---

# Unity Audio Generator

Generate game audio with ElevenLabs, then import it as Unity AudioClips with settings tuned for mobile.

## API key & script

Key resolution: `--api-key`, then `ELEVENLABS_API_KEY`. Probe / built-in probe:
```bash
bash $UNITY_GAME_SKILLS_HOME/unity-game-director/scripts/probe_asset_credentials.sh   # ELEVENLABS_API_KEY=SET|MISSING
python3 $UNITY_GAME_SKILLS_HOME/unity-audio-generator/scripts/unity_audio_asset.py probe
```
Subcommands: `sfx` (effects/ambience from a prompt), `tts` (spoken line), `isolate` (clean/isolate speech), `voice-change` (convert a performance to a target voice), `loopify` (local seamless-loop crossfade), `normalize` (target-LUFS loudness). Write outputs under `Assets/<Game>/Audio/`.

```bash
# UI / gameplay SFX
python3 $UNITY_GAME_SKILLS_HOME/unity-audio-generator/scripts/unity_audio_asset.py sfx \
  --prompt "bright cheerful coin pickup blip, short, casual mobile game" \
  --out Assets/<Game>/Audio/SFX/sfx_coin_pickup.mp3

# Music/ambience bed intended to loop
python3 $UNITY_GAME_SKILLS_HOME/unity-audio-generator/scripts/unity_audio_asset.py sfx \
  --prompt "upbeat looping casual puzzle music, light marimba and claps" \
  --duration 20 --out Assets/<Game>/Audio/Music/music_gameplay_raw.mp3

# Announcer / voice line
python3 $UNITY_GAME_SKILLS_HOME/unity-audio-generator/scripts/unity_audio_asset.py tts \
  --text "Level complete!" --out Assets/<Game>/Audio/VO/vo_level_complete.mp3
```

## Audio direction: one sound world, keyed to the art-spec

Production audio follows the game's `art-spec.yaml` **audio-direction block** (`audio_direction:` — shared prompt prefix, instrument palette, mood tokens keyed to `style_id`, pinned TTS voice) the same way art follows the palette:

- **Every** production `sfx` prompt starts with the spec's shared prompt prefix/instrument-palette tokens VERBATIM — SFX identity rests entirely on these shared tokens (there is no voice/style pin for SFX).
- A pinned `voice_id` applies to **TTS only**: all VO uses the spec's one pinned voice via `--voice-id`.
- No art-spec / no audio_direction block yet = exploratory clips only; do not register production audio without one (write the block first via `unity-art-direction`).

## Loops and loudness (local post-processing, requires ffmpeg)

Seamless looping is a **local crossfade post-process, NOT an ElevenLabs feature** — the API's `--loop` flag and "seamless" prompt words do not guarantee a clean seam. For every clip whose contract sets `runtime.audio.loop: true`:

```bash
# tail-into-head crossfade; output length = input - crossfade, seam exact by construction
python3 $UNITY_GAME_SKILLS_HOME/unity-audio-generator/scripts/unity_audio_asset.py loopify \
  --input Assets/<Game>/Audio/Music/music_gameplay_raw.mp3 --out Assets/<Game>/Audio/Music/music_gameplay.wav --crossfade 0.5

# hit the contract's runtime.audio.target_lufs before approval
python3 $UNITY_GAME_SKILLS_HOME/unity-audio-generator/scripts/unity_audio_asset.py normalize \
  --input Assets/<Game>/Audio/Music/music_gameplay.wav --out Assets/<Game>/Audio/Music/music_gameplay_final.wav --target-lufs -16
```

Verify 2-3 loop wraps in Unity (`AudioSource.loop = true`) before flipping the loop flag.

## Production clips ship via contract + registry

Like art, a generated file is not a game asset. Production clips get a per-clip `asset-contract.yaml` (`source.generator: elevenlabs`, `runtime.type: audio`) whose `runtime.audio:` section records load type, Vorbis quality, force-to-mono, loop flag, and target LUFS; validate with `unity-asset-pipeline/scripts/validate_asset_manifest.py` and register in the approved-asset registry (audio entries use `clip:` instead of `prefab:`). The AudioImporter settings below are the enforcement of that section — import QA fails when they disagree. Exploratory jingles/one-off tests may skip the pipeline but never ship.

## What to generate for casual games

- **Core feedback SFX:** tap/select, success/win, fail, coin/collectible, combo/streak, level-up, button — short, punchy, distinct. These carry most of the "juice."
- **Music:** one or two short seamless loops (menu + gameplay); keep files small.
- **Ambience:** optional looping bed for theme.
- **Voice:** announcer stingers or tutorial VO via `tts`; clean recordings with `isolate`.

## Import into Unity (via unity-mcp-bridge)

After writing under `Assets/<Game>/Audio/`, `refresh_unity(scope="assets", wait_for_ready=true)`, then set `AudioImporter` settings with `execute_code` from the clip contract's `runtime.audio:` values (role guidance below when no contract exists yet):

```csharp
var p = "Assets/<Game>/Audio/SFX/coin.wav";
var ai = (UnityEditor.AudioImporter)UnityEditor.AssetImporter.GetAtPath(p);
var s = ai.defaultSampleSettings;
s.compressionFormat = UnityEditor.AudioCompressionFormat.Vorbis; // good size/quality on mobile
s.quality = 0.7f;
// Short SFX: decompress on load (cheap CPU, tiny). Music/ambience: streaming or compressed-in-memory.
s.loadType = UnityEngine.AudioClipLoadType.DecompressOnLoad;     // music -> .Streaming
ai.defaultSampleSettings = s;
ai.forceToMono = true;        // mono for SFX saves memory; keep music stereo (forceToMono=false)
ai.SaveAndReimport();
return "imported clip";
```

Guidance by role:
- **Short SFX (<1s):** Vorbis, `DecompressOnLoad`, force-to-mono.
- **Music / long loops:** `Streaming` (or `CompressedInMemory`), stereo, lower quality is fine.
- **VO:** `CompressedInMemory`, mono.

Then wire playback: an `AudioSource` per role (SFX one-shots via `PlayOneShot`, a looping music source), or a small `AudioManager` singleton. Keep concurrent voices low on mobile.

## Mobile rules

- Favor Vorbis; avoid uncompressed PCM for anything but tiny critical SFX.
- Force-to-mono for SFX/VO; reserve stereo for music.
- Cap total audio memory; stream music rather than loading it whole.
- Report prompts, output paths, contract paths, import settings per clip, and where each clip triggers.
