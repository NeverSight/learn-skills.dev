---
name: minimax-h3-prompting
description: >-
  Write or refine prompts for MiniMax H3 video generation via comfy-agent
  (minimax_h3_t2v / minimax_h3_i2v / minimax_h3_r2v presets). Use whenever
  composing the --104_prompt for an H3 run, when a user asks for a video clip
  on an H3 environment, or when an H3 output missed the intent (wrong audio, ignored
  camera move, style drift, rushed pacing) and the prompt needs iteration.
---

<!-- Generated into .agents/skills by `npm run sync-skills` for repo-level
     discovery. Edit only this .claude source; do not edit the mirror. -->

# minimax-h3-prompting

**Read [docs/minimax-h3-prompting.md](../../../docs/minimax-h3-prompting.md)
before composing any H3 prompt — it is the single source of truth.**

Non-negotiables it enforces:

- H3 renders picture **and stereo audio** in one pass: always direct
  ambience and music explicitly, or the model invents them.
- Render the final block in the official three-field format
  (`integrated_multimodal_description` / `overall_soundscape` /
  `non_diegetic_music`), with the `<Picture 1>` alignment sentence for I2V or
  explicit `<Picture 1>` / `<Audio 1>` role assignment for R2V.
- Fit beats to the frame budget (`--104_length`: 124 ≈ 5 s → one beat;
  243 ≈ 10 s; 362 ≈ 15 s → timecoded shot list).
- Iterate with a fixed `--15_noise_seed`; verify frames (`ffmpeg`) AND
  audio (`ffprobe`) before reporting results.
