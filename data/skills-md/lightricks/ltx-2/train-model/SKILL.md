---
name: train-model
description: End-to-end agent for training LTX models. Probes filesystem and GPU, picks the right conditioning mode from the user's intent, prepares the dataset (scenes, captions, references), preprocesses, autotunes, launches, and monitors training. Use when the user wants to train, fine-tune, LoRA, or otherwise produce a custom LTX model.
argument-hint: [optional source path or run name]
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, Edit, Write, Agent, AskUserQuestion, TodoWrite
---

# Train Model — Orchestrator

Take the user from "I want to train something" to a running, monitored training job — automating the mechanical glue (dataset layout, captioning, preprocessing, config patching, launch, monitoring) without making silent decisions on their behalf.

> **Source of truth for the trainer:** [`packages/ltx-trainer/docs/`](../../../packages/ltx-trainer/docs/). This skill orchestrates those scripts; it does not duplicate their reference content.

## Hard Invariants

These are non-negotiable. Re-read them before every action that touches the filesystem or starts a process.

1. **No file mutation outside the run workspace without explicit user approval.** The workspace is `./projects/<run-name>/`. Never overwrite, move, delete, or modify any user file or directory outside it without surfacing an explicit ask. Hours of dataset work must never be silently destroyed.
2. **No heavy work before plan approval.** Captioning, preprocessing, training, and autotune do **not** start until the user approves `plan.md` (Phase 4). Probing the filesystem and running `nvidia-smi` is fine; encoding videos or downloading models is not.
3. **No silent assumptions.** Every non-trivial default appears under "Assumptions" in `plan.md`.
4. **No code changes to the trainer package without explicit consent.** If the user's intent doesn't map to a supported configuration, follow the **Escape Hatch** section below — do not unilaterally edit `packages/ltx-trainer/`.
5. **No fabricated claims about training outcomes or data sufficiency.** Do not assert how well something *will* train, whether a dataset is "too small," how many samples/seconds of audio are "enough," which modality will "learn better," expected quality, or any similar prediction — you have no grounded basis for these, they're frequently wrong, and they mislead users. Stick to facts you can substantiate: what the trainer/docs actually say, observed numbers (loss, step time, VRAM), counts, and the user's own stated goals. If the user asks for a recommendation that depends on such judgment, you may share it **only** as an explicitly-flagged uncertainty ("I'm not sure — you'd have to try it"), never as authoritative fact. When in doubt, say less.

## Keep the User Informed

Most users don't know how this skill works under the hood — they don't know what "preprocessing," "a one-sample sanity check," or "autotune" mean or why they're happening. Narrate the run in plain language so it never feels like a black box:

- **Entering a phase:** one or two sentences on *what you're about to do and why* — in user terms, not jargon.
- **Leaving a phase:** one line on *what came out of it* (e.g. "captioned 9 clips," "found the fastest stable config: batch 1, ~3s/step").
- **Explain the non-obvious phases explicitly** — these are the ones that confuse people:
  - *Sanity check (Phase 6):* "Before the full run, I do a quick dry run on a single clip at your target resolution. It catches out-of-memory or config problems in a couple of minutes instead of failing hours into training."
  - *Autotune (Phase 6):* "Then I try a few configuration variants on that one clip to pick the fastest one that still fits your GPU — so the full run is as fast as it can be."
  - *Preprocess (Phase 7):* "I'm encoding your videos into the compressed latents the trainer reads. One-time step; the trained model never sees the raw videos directly."
- Keep it concise — a sentence or two per transition, not walls of text or raw logs. This is running commentary, not a replacement for the upfront plan (Phase 4) or the status reports (Phase 8).
- Long-running steps (preprocess, training): say roughly how long it'll take and that you'll report back, so silence doesn't read as "stuck."
- **Describe what you're doing — don't editorialize about how it'll turn out.** Narration covers *what's happening*; it must not drift into unfounded predictions about training quality or data sufficiency (e.g. "26s of audio is too little," "voice won't learn well"). Those are fabricated claims — see Hard Invariant #5. State facts and the user's choices; leave the "will it be good?" judgment to the user watching the results.

## Phase 0 — Set Up

Create the workspace and todos.

1. Pick a workspace root in this order (use first writable):
   - `$LTX_TRAININGS_DIR`
   - `/data/ltx-trainings/`
   - `/workspace/ltx-trainings/`
   - `./projects/` (repo-relative — preferred default in this repo)
2. Derive a tentative `<run-name>` from the user's words; finalise after Phase 1 once the mode is known. Format: `<mode>-<dataset-name>-<YYYYMMDD-HHMM>`.
3. Create `<workspace>/<run-name>/` and seed empty subdirs: `dataset/`, `outputs/`, `overfit/`.
4. Create a todo list covering Phases 1–9 so the user can see progress.

## Phase 1 — Intent

Ask one question, framed in user terms (not jargon):

> What do you want the model to learn? Examples: "generate videos from text," "make a LoRA of a specific style," "extend a video forward in time," "add sound effects to a silent video," "fill in masked regions of a video."

Map the answer to one or more conditioning modes via `references/mode-selector.md`. If the requested capability has no mapping, go to **Escape Hatch**.

### Plain concept/style LoRA → ask how it'll be used, default to I2V

A "train a LoRA on X" request (a character/style/concept LoRA, no specific conditioning task) maps to either T2V or I2V. These aren't locked to inference: LoRA weights are pipeline-agnostic (the same checkpoint loads in both T2V and I2V inference), and the `i2v_lora` config applies first-frame conditioning with **`probability: 0.5`** — so it learns **both** conditioned (I2V) and unconditioned (T2V) generation in one run, and the first frame is taken automatically from each training clip (no extra data prep). I2V is therefore a versatile superset.

Ask how they intend to use the result:

> Will you generate videos from **text alone** (T2V), from a **starting image** (I2V), or **both / not sure**?

- **Both / not sure (default):** use `i2v_lora` (probabilistic first-frame) — works for both at inference.
- **I2V:** `i2v_lora`.
- **Text only:** `t2v_lora`.

(This only applies to plain concept/style LoRAs. A specific task — extension, inpainting, foley, IC-LoRA, etc. — maps directly to its mode via `mode-selector.md`; no usage question needed.)

### Confirm the mode before proceeding

Once the mode is determined, **state it plainly and confirm it** before doing any probing or work — a wrong inference is cheap to fix here and expensive later:

> "Got it — I'll train an **I2V LoRA** (usable for both image-to-video and text-to-video at inference). Sound right?"

The mode also appears in the plan (Phase 4), but confirm it here so the rest of the flow isn't built on a wrong guess.

## Phase 2 — Probe

No questions in this phase. Inspect what's already there. Use `references/onboarding.md` as the source of truth for the prerequisite checklist and what to do when something is missing.

### Filesystem probe
- If the user pointed at a path, classify: directory of raw videos, single long video, directory with a metadata file (CSV/JSON/JSONL), existing `.precomputed/`, partial outputs from a prior run.
- For metadata files, identify columns: `video`/`media_path`, `caption`, `audio`, `reference_video`, `video_mask`, etc. (see `packages/ltx-trainer/docs/dataset-preparation.md`).
- **Clip lengths (small datasets only):** for datasets up to a few hundred clips, `ffprobe` each clip's frame count and note the **minimum**. Clips shorter than the target frame bucket are silently skipped by `process_dataset.py`, so the shortest clip caps the achievable frame count — feed this into the Phase 3 resolution/frame-count choice (pick a bucket the clips support, or plan multi-bucket). Skip this per-clip probe for large datasets (too slow); rely instead on the post-preprocess reconciliation in Phase 7, which flags any dropped clips regardless of dataset size.
- Check for an existing `<workspace>/<run-name>/` and whether `outputs/checkpoints/` contains a prior checkpoint (`lora_weights_step_*.safetensors` or `model_weights_step_*.safetensors`, plus a matching `training_state_step_*.pt` when resume state is enabled). This is a **resume candidate** — but note the trainer does *not* auto-resume from the output dir; resuming requires explicitly setting `model.load_checkpoint` in `config.yaml` to that checkpoint path. See `phases/launch-and-monitor.md` for the resume flow.
- Check disk space at the workspace root. Preprocessed latents, checkpoints, and validation samples add up across a run; surface the available space alongside a rough sense of what one run consumes (one preprocessed bucket scales with sample count and resolution; each checkpoint is several GB), and warn the user if free space looks tight given their dataset size.

### Hardware probe
- `nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader` → GPU model, count, VRAM. Stop the run if no CUDA GPU.
- W&B login state — use wandb's **own** credential resolution (source-agnostic: covers env var, netrc, and the wandb settings file), not a hand-rolled netrc grep and **not** `wandb status` (which misleadingly reports `api_key: null` even when logged in):

  ```bash
  uv run python -c "import wandb; print(bool(wandb.Api().api_key))"   # True => logged in
  ```

  `True` → W&B is available, enable it. `False` → genuinely not logged in. If the check errors or is ambiguous, **ask the user** rather than silently disabling — a wrong "W&B off" assumption can incorrectly disable expected tracking.
- Apply `references/hardware-profiles.md` to derive defaults (32GB / 40–60GB / 80GB+ VRAM tier).

### Prerequisite probe (first-run sanity)
- `uv` installed (`command -v uv`).
- Workspace synced (lockfile present + `ltx-trainer` import works).
- LTX `.safetensors` checkpoint and matching Gemma text encoder dir present in `/models/`, `~/models/`, or `$LTX_MODELS_DIR`.
- For LTX 2.5, `text_encoder_path` must point to the LTX-specific fine-tuned Gemma 4 root, not Google's vanilla Gemma 4 model.
- Captioner availability: Gemini auth (`GEMINI_API_KEY`/`GOOGLE_API_KEY` or gcloud/Vertex) OR a ≥40 GiB GPU to host the Qwen3-Omni-30B vLLM server (FP8; bf16 needs ≥66 GiB). On typical consumer GPUs (24/32 GB), Gemini is effectively the only local-free option — see `references/onboarding.md`.

For any missing prerequisite, **do not silently fail in a later phase**. Present the finding in chat with the specific next step from `references/onboarding.md`. The skill may offer to auto-install / auto-download missing pieces — but only ever after asking the user explicitly, one item at a time (model downloads are tens of GB each). Never auto-modify shell rc files or system config without consent.

When everything (or what the user agreed to set up) is in place, fold the resolved paths into the plan's Assumptions section.

### Pre-existing artifacts in the run dir

If the run dir (or a user-supplied path) already contains artifacts from a prior session, classify each into one of three buckets — only the third prompts the user:

1. **Deterministically verifiable → verify, then reuse silently (or stop).** `.precomputed/` latents: load a sample, check tensor shapes + modality coverage against the target (Phase 7). Match → reuse, no question. Mismatch/incomplete → stop and ask (reuse-at-old-spec / re-preprocess to a new dir / abort).
2. **Cheap, fully-derived intermediates → regenerate silently.** `overfit/`, eval renders, sanity/temp configs, one-sample metadata. Delete and redo; don't ask.
3. **Expensive AND not deterministically verifiable → ask.** Captions (`dataset.json`) and trained checkpoints/outputs. We can't programmatically decide whether existing captions or a half-finished run are what the user wants now, so surface what was found (counts, and how/when produced if knowable) and ask: reuse vs regenerate (for checkpoints: resume vs fresh).

Principle: only ask when reuse-vs-regenerate is a genuine judgment call with cost either way. Never silently delete user-supplied data (hard invariant #1).

## Phase 3 — Ask (minimum viable set)

Ask only what cannot be inferred. Use `AskUserQuestion` with multiple-choice when possible. Typical questions:

- **Target resolution / frame count** — propose a default per mode (e.g., `960x544x49` from the T2V LoRA config); offer overrides.
- **Training steps** — if dataset size doesn't pin it, propose a default (e.g., 2000 for small LoRA datasets).
- **LoRA trigger word / concept name** — only for style/concept LoRAs. Ask **only** for the word itself (or whether they want one). **Never** ask or mention *how* it's injected — it's always the `--lora-trigger` flag (passed to `process_dataset.py`, which forwards it to `process_captions.py` where the prepend happens); this is a fixed implementation detail. Presenting caption-injection as an option creates unnecessary confusion.
- **Captioner backend** — only if more than one path is viable (e.g. a ≥40 GiB GPU can host the Qwen3-Omni-30B server *and* Gemini auth is available). On typical consumer GPUs, default to `gemini_flash` and surface that Gemini auth is required rather than asking.
- **Model paths** — only if not found in the probe.

Never ask anything answerable by `ls`, `nvidia-smi`, or the W&B credential check above.

## Phase 4 — Plan

Write the plan to `<workspace>/<run-name>/plan.md` using `references/plan-template.md`. Present it to the user in chat (don't just dump the file path). Wait for explicit approval before proceeding.

If the user requests changes, edit the plan and re-present. Do not start Phase 5 until approval.

## Phase 5 — Prepare Dataset

If captioned metadata already exists with all required columns for the chosen mode, skip this phase. Otherwise follow `phases/prepare-dataset.md` — re-read it before acting.

**Captioning gate:** caption a 3-sample spot-check first, show the captions in full, and **STOP for explicit user approval** before captioning the full set. The user must approve or give tuning instructions — never auto-proceed to the full pass. (Details in `phases/prepare-dataset.md`.)

**Conditioning-inputs gate:** modes that need a reference (V2V/A2A/AV2AV IC-LoRA) or a mask (video/audio inpainting) require a per-sample input that encodes the user's specific idea. **Ask the user to provide it** — never invent the method (no defaulting to Canny/depth/generic masks). Only help generate it if the user explicitly asks, following *their* approach. Don't enter preprocessing for these modes without the input present. (Details in `phases/prepare-dataset.md` Step 4.)

## Phase 6 — Sanity Check + Autotune (always run)

**Tell the user what this phase is before starting it** — it's the most opaque to someone who doesn't know the design (see "Keep the User Informed"). In plain terms: a quick single-clip dry run at the target resolution to catch OOM/config errors cheaply, followed by trying a few config variants to pick the fastest stable one.

Run **at the full target resolution** on **one sample** before the full preprocess. Purpose:
1. Catch OOM / config errors before paying the full preprocessing cost.
2. Empirically pick the fastest stable config via a small sweep.

Steps:
1. Pick one sample from the dataset metadata. Preprocess just that sample to `<workspace>/<run-name>/overfit/.precomputed/` (see `phases/preprocess-dataset.md` — use it in "one-sample" mode).
2. Generate a temp config matching the planned full-run config but with `data.preprocessed_data_root: overfit/.precomputed`, `optimization.steps: 50`, `validation.interval: 50`, `checkpoints.interval: null`.
3. Run the **baseline trial**: the conservative config from the matched VRAM tier (32GB tier = `t2v_lora_low_vram.yaml` defaults; 80GB+ tier = `t2v_lora.yaml` defaults — see `references/hardware-profiles.md`).
4. **Success criteria** (all required):
   - No OOM, no NaN loss, no crash.
   - All 50 training steps complete.
   - Validation sample at step 50 generates successfully (validation pass is a real OOM risk — do not skip).
   - **For audio runs:** the one-sample `audio_latents/` is non-empty (the trainer log should report audio enabled). A joint/audio run that silently produced no audio latents is a failure even if steps complete — see the audio gate in `phases/preprocess-dataset.md`.
   - **Loss is NOT a success criterion.** Loss can be non-monotonic even when training is healthy.
5. **Autotune sweep** — incremental, capped at 5 trials total. Each trial = current best + one change. Stop on OOM (revert), no step-time improvement, or 5 trials:
   - Trial 2: `quantization: null` (disable transformer quantization) if VRAM headroom allows.
   - Trial 3: `optimizer_type: adamw` (disable 8-bit optimizer) if headroom allows.
   - Trial 4: `batch_size` up (1 → 2 → 4). Adjust `gradient_accumulation_steps` proportionally to keep effective batch constant. **Note:** batch size can't be meaningfully tested on the one-sample set — defer it (test on the full set later, or just keep `batch_size: 1`, which is preferable for small concept-LoRA datasets anyway).
   - **Do not sweep:** resolution (user decision), `acceleration.load_text_encoder_in_8bit` (one-time, no step-time impact), `enable_gradient_checkpointing` (the trainer's example configs ship with it on; on the 80GB+ tier you *may* try it off, but for the 22B model it usually OOMs even with tens of GB of apparent headroom — don't expect a win; never turn it off on the 32GB tier).
6. Collect per trial: step time and peak VRAM. **Prefer the trainer's own end-of-run stats** (it prints total time / step time and peak GPU memory) — no external timing tool is needed (`/usr/bin/time` is often not installed). Append results to `<workspace>/<run-name>/autotune.log`.
7. Winning trial's deltas are patched into the main `config.yaml`. Summarise the sweep to the user (one line per trial + winner).

If the baseline trial fails, consult `references/troubleshooting.md`, propose a fix, re-run. Never push forward to the full preprocess after a failed sanity check.

## Phase 7 — Full Preprocess

Follow `phases/preprocess-dataset.md`. Re-read it before acting.

**If `.precomputed/` already exists at the target path** (user-supplied or prior run), the phase verifies shapes and modality coverage before reuse. On mismatch it stops and asks — never silently overwrites.

## Phase 8 — Launch & Monitor

Follow `phases/launch-and-monitor.md`. Re-read it before acting. Surface the W&B URL (if enabled) and produce periodic status reports. At completion, the phase writes `<workspace>/<run-name>/outputs/run-summary.md`.

## Phase 9 — Post-Train Validate

After training finishes, follow `phases/post-train-validate.md`. Re-read it before acting. The phase renders the final LoRA against in-distribution, out-of-distribution, and held-out prompts; surfaces the MP4 paths to the user and exits.

**Important constraint:** the post-train validate phase does not solicit a verdict and does not coach on causes for "soft" failures. Soft training quality has no reliable if/then rule book — the user inspects the renders and decides for themselves whether to ship, iterate, or change course. The orchestrator's job ends after Phase 9; iteration is a new invocation with a new run-name.

## Monitor-Only Entry

If invoked against an existing `<workspace>/<run-name>/` that already has a training process running or completed, **skip to Phase 8 in monitor-only mode** instead of restarting anything: report current step, recent loss, ETA, checkpoint list, W&B URL, and the resume command. Distinguish "live process" vs "stopped run with checkpoints" and offer the appropriate next action.

## Escape Hatch: Unsupported Modes

If Phase 1 intent doesn't map to any combination of supported `flexible`-strategy conditions:

1. Stop. Do not edit `packages/ltx-trainer/` on your own.
2. Explain what's missing in concrete terms: "you want X. The trainer supports A, B, C via conditions D, E, F. X requires a new condition / strategy."
3. Identify the code change needed (typically a new `Condition` subclass in `ltx_trainer/training_strategies/flexible.py` plus schema wiring in `config.py`).
4. Ask the user explicitly: "Proceed with the code change, do it yourself, or abort?"
5. Only on explicit consent, drop out of this skill's orchestrator and edit code as a normal agent task. After the change lands and is tested, return here.

## Ask-vs-Assume Cheat Sheet

| Decision | How |
|----------|-----|
| Precision, quantization, optimizer, grad checkpointing | Assume from matched VRAM tier. List in plan's "Assumptions". |
| Checkpoint/validation interval, seed, W&B project name, output dir | Assume sensible defaults. List in "Assumptions". |
| Target resolution / frame count | Ask if not given; propose mode-appropriate default. |
| Step count | Ask if dataset size doesn't pin it. |
| LoRA trigger word / concept name | Ask for the word only (style/concept LoRAs). Never ask *how* it's injected — always `--lora-trigger`. |
| Captioner backend | Ask only if multiple backends are viable. |
| Anything answerable by `ls`, `nvidia-smi`, or the W&B credential check | Never ask. Probe. |

## The Two `load_text_encoder_in_8bit` Flags

Same name, different layers — do not conflate:

| Flag | Layer | Effect |
|------|-------|--------|
| `process_dataset.py --load-text-encoder-in-8bit` | Preprocessing CLI | Memory during caption-embedding precompute (Phase 7). One-time per dataset. |
| `acceleration.load_text_encoder_in_8bit` (trainer YAML) | Trainer config | Memory during validation-sample prompt-embedding caching at training start (Phase 8). One-time per run. |

Both are one-time costs and neither affects per-step training speed. Default per the trainer's shipped configs: **ON** on the 32GB tier (matches `t2v_lora_low_vram.yaml`), **OFF** on the 80GB+ tier (matches `t2v_lora.yaml`). No measured guidance for the 40–60GB tier beyond starting from the 32GB tier and autotuning.

## Workspace Layout

```
<workspace>/<run-name>/
  plan.md                  # the approved plan
  config.yaml              # generated training config (NOT in packages/ltx-trainer/configs/)
  autotune.log             # per-trial sweep results
  dataset/
    dataset.json           # captions + media paths (training split)
    holdout.jsonl          # held-out split (if reserved)
    videos/                # source media copies (NO derived files here)
    .precomputed/          # latents/ audio_latents/ conditions/ (+ references/masks per mode)
  outputs/
    checkpoints/           # training checkpoints + states
    samples/               # in-training validation samples (step_*)
    eval/                  # Phase 9: in-distribution/ out-of-distribution/ held-out/ + prompts.json
    run-summary.md         # written at completion
  logs/                    # all run logs
  overfit/                 # Phase 6 scratch (one-sample preprocess + sanity/autotune runs)
```

`<run-name>` default: `<mode>-<dataset-name>-<YYYYMMDD-HHMM>`. Surface in the plan; user may rename.

### Workspace hygiene (keep it clean)

- **Don't create undocumented directories** (e.g. an ad-hoc `scratch/`). Intermediates belong under `overfit/` (sanity/autotune scratch) or a `/tmp` tempdir — not loose in the run dir or the repo root.
- **Never write derived files into `dataset/videos/`** (the source media dir). Latents go under `.precomputed/`; one-sample/eval metadata goes under `overfit/`, not `dataset/`.
- **One canonical manifest per artifact** — don't leave duplicate `*_prompts.json` / metadata copies.
- **Clean up phase byproducts:** the Phase 9 eval must delete its validate-only trainer cruft (see `phases/post-train-validate.md`); `overfit/` is scratch and may be removed after a successful run. The final tree should look like the layout above — no stray `.pt`/`.wav` files, no `eval/checkpoints/`, no duplicate manifests.

## References

- `references/mode-selector.md` — user intent → conditioning mode mapping, LoRA rank guidance (read in Phase 1).
- `references/onboarding.md` — first-run prerequisite checklist, model download paths, captioner graceful degradation (read in Phase 2).
- `references/hardware-profiles.md` — GPU VRAM → tier + config defaults (read in Phase 2).
- `references/config-patching.md` — safe YAML edits + schema constraints (read whenever editing `config.yaml`).
- `references/troubleshooting.md` — OOM, NaN, validation failures, resume (read on any failure).
- `references/plan-template.md` — exact plan.md format (read in Phase 4).

## Phase Procedures

These are procedure documents the orchestrator reads when entering each phase. They are not standalone skills — they're never invoked by Claude's skill-discovery system. The orchestrator opens them via the `Read` tool and follows the instructions inline.

- `phases/prepare-dataset.md` — Phase 5: scenes, captioner iteration, IC-LoRA references, metadata, holdout split.
- `phases/preprocess-dataset.md` — Phases 6 (one-sample) & 7 (full): `process_dataset.py` orchestration, existing-data verification.
- `phases/launch-and-monitor.md` — Phase 8: launch command, accelerate, W&B, status reports, run-summary writing.
- `phases/post-train-validate.md` — Phase 9: render the final LoRA against three prompt categories; surface paths only.
