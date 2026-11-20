---
name: voiceover
description: Narration and voice-over with open-weights Chatterbox Multilingual TTS (23 languages, optional voice reference) in ComfyUI, following one-voice narration rules. Use for film narration, explainer VO and character lines.
---

# voiceover

Run every graph with the bundled client: `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`. Upload input files first with `python scripts/comfy_client.py upload <file>`. Before the first run on a server, check it with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses for this skill are in `references/requirements.md`. Use open-weights models only, and never swap in a hosted or closed model.

## Graph
`voice_chatterbox_multilingual.api.json`: set `1.text` and `1.language` (for example `English (en)`), and `1.seed`. Node `2` LoadAudio is the voice reference. Upload a clean 5-15 s clip and set `2.audio`. With no reference, delete node `2` and the `audio_prompt` link in node `1` (the rosesfield README in `references/` describes this). If you need the 40 s trim, it is in node `4`.

## Voice conversion
`voice_change_chatterbox.api.json` (Chatterbox VC) re-voices recorded speech: set `3.audio` to the source speech, `2.audio` to the target voice and `1.seed`. Only use a target voice with the speaker's consent.

## Narration rules
Condensed from Fuobe's narration skill; the full copy is in `references/fuobe-narration-rules.md`.
- Use one consistent narrator voice, reference clip and seed for the whole film. Log them in the story bible.
- Deliver speech only. Music and SFX go to `music-sfx` and are mixed later in `film-assembly`.
- Write for the ear: short sentences, numbers spelled the way they are spoken, no markup. Render one line per shot so lines can be re-timed.
- About 2.5 words per second. If a line runs longer than its shot, cut words; don't speed up the audio.
- Only clone a voice with the speaker's consent.
