---
name: music-sfx
description: Generate music beds, songs and sound effects with open-weights ACE-Step 1.5, Stable Audio Open / Stable Audio 3 and MiniMax Music 3 in ComfyUI, using model-specific prompt rules. Use for score, stingers, ambience and foley.
---

# music-sfx

Run every graph with the bundled client: `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`. Upload input files first with `python scripts/comfy_client.py upload <file>`. Before the first run on a server, check it with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses for this skill are in `references/requirements.md`. Use open-weights models only, and never swap in a hosted or closed model.

| Need | Workflow | Set |
|---|---|---|
| Music, or a song with lyrics | `music_ace_step15.api.json` | `4.tags` (genre, instruments, BPM, mood), `4.lyrics` (or `[instrumental]`), `6.seconds`, `4.seed` |
| Alternate music model | `music_minimax_music3.api.json` | `13.caption`, `13.lyrics` |
| SFX / ambience | `sfx_stable_audio_open.api.json` | `3.text`, `5.seconds` (up to about 47 s) |
| SFX, newer model | `sfx_stable_audio_3.api.json` | `6.text`, `11.seconds` |

## Prompt rules
Condensed from Fuobe's audio rules; the full copy is in `references/fuobe-audio-prompt-rules.md`.
- **Music models** take a style description, not a scene: genre, tempo or BPM, key instruments, mood, structure. Lyrics go in the lyrics field only, never in the tags.
- **SFX models** take one sound per prompt in concrete physical words (material, action, space, distance): "heavy wooden door slams in a stone hall, short reverb". Don't send music words to an SFX model.
- Set the duration to the cut length plus about 1 s for tails. A bed under narration should be sparse, with no vocals.
- Ignore the closed or hosted model rows in the reference file; this skill is open weights only.
- **Weight licenses:** check Stable Audio Open's license (believed to be the Stability AI Community License) before any commercial use. The MiniMax Music 3 license is unverified.
