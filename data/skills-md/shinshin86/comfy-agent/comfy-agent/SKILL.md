---
name: comfy-agent
description: >-
  Generate images, video, or music/audio with ComfyUI via the comfy-agent CLI.
  Use when the user asks to create/generate an image, video clip, animation,
  song, BGM, or sound effect, or asks to set up / reconnect a ComfyUI
  environment (local or Google Colab). Covers picking the right Colab kit,
  presenting a setup blueprint, running generations, and recovering from
  MISSING_MODEL_ON_SERVER / SERVER_UNREACHABLE errors.
---

# comfy-agent skill

Full policy: [docs/agent-playbook.md](../../../docs/agent-playbook.md) —
read it before non-trivial work. The short version:

## State machine (always start here)

```
comfy-agent doctor --json
├─ connection ok, preset check ok → generate (import/run)
├─ SERVER_UNREACHABLE + trycloudflare URL
│    → tell the human: "Colab session expired. Open the notebook, Run All,
│       then paste the printed `comfy-agent connect <url>` line."
│       Local presets/outputs are intact — never re-import or redo setup.
├─ SERVER_UNREACHABLE + local URL → start/install local ComfyUI yourself
└─ nothing configured → ask ONCE: Local (light models, persistent)
     or Colab (heavy models, ephemeral). Record the answer.
```

When the human pastes a `comfy-agent connect https://…` line, run it, then
resume the interrupted task immediately.

## Blueprint before generating

For a new creative goal (e.g. "make a music video", "10-second anime clip"):

1. Decompose into capabilities (image / video / audio stages).
2. `comfy-agent colab suggest "<requirement>" --json` per capability
   (works from `npm i -g comfy-agent` since 0.0.3; note `download_gb`, `setup_minutes`,
   `composable`, `status`, `gpu`).
3. `comfy-agent doctor --json` (+ `--preset <name>` when a preset exists).
4. Present: pipeline stages, chosen kit + alternatives, GPU/cost implication,
   the human's actions (count them: "Run All + paste 1 line, ~N min"),
   your actions, license cautions.
5. Get approval before big downloads or paid-GPU choices. While Colab boots,
   prepare prompts/parameters — don't idle.

Model-specific prompting: for MiniMax H3 runs (`minimax_h3_t2v` /
`minimax_h3_i2v`), use the `minimax-h3-prompting` skill before composing
`--104_prompt`.

## Error handling (decision table digest)

- Time-only problems → fix yourself (install, start server, retry ≤3 with
  adjusted params). Money/rights/physical-action problems → hand the human
  ONE concrete action or an explicit choice.
- `MISSING_MODEL_ON_SERVER` → `details.missing_models[].value` names the
  file; find the kit whose `assets` provide it via
  `comfy-agent colab catalog --json`. Local server: download it yourself
  (confirm if > a few GB). Colab: give the human that kit's `01_setup.py`
  cell (additive only if the added kit is `composable: true`).
- Exit codes: 0 ok / 2 your invocation or local environment is wrong /
  3 server-side or artifact state.

## Verify before reporting

Run `comfy-agent verify <run-dir> --json` (no API key; add
`--expect-kind`/`--expect-count`/`--min-duration` for hard assertions, exit 3
on failure). It writes `verify/sheet.png` and per-video frames when `ffmpeg`
exists; animated WEBP gets frame count/duration only. Then view the
sheet/frames (or `analyze` a frame) and report deviations honestly; `verify`
alone is not "inspected" — never claim success for an output you have not
looked at.

## Creative memory

- Before generating a known character, call `comfy-agent brief <name> --preset <preset> --json` once.
- Reuse `appearance` verbatim; follow `applicable`/`next_action`, avoid `avoid`, and start from `top_jobs`.
- Run with `--character <name>` and keep its reported `prompt_input`/`prompt_final` transparent.
- After `verify`, add only human-selected work to the gallery, then approve only on human confirmation.
- Tag failures `reject --reason`; store kit-specific learning with `character note --kit`.
- Ask the human to place missing LoRAs in `models/loras/`; export only when requested.

## H3 intent routing

For H3 generation, read [H3 environment selection](../../../docs/h3-environment-selection.md).
Ordinary H3 remains the default. Choose SNS LoRA, image/audio Guide or Motion
Context only when the user's creative intent calls for it; installation alone
never enables a feature. Explain the chosen profile before setup. Use the
existing FastH3 kit only for compatible T2V speed requests; VDN is explicit-only.
New extension and VDN kits are Starter until canonical Colab E2E verification.
Motion chains use runtime-local temporary latents, request no Drive access,
and advance one inspected clip at a time
using the local chain helper. Do not silently replace missing references or a
failed continuation with ordinary T2V.
