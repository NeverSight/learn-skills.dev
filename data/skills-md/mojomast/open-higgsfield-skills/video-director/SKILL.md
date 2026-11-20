---
name: video-director
description: Top-level orchestrator that turns a one-line video idea into a finished short (story short, product spot, music-video snippet) on ComfyUI (local, Google Colab or Comfy Cloud) using only open-weights models. It does brief intake with defaults, a preflight and budget check that picks a draft, standard or max tier, then story bible and timed shot plan, stills first with a QA judge loop, image-to-video, continuity checks, voiceover, music and SFX, assembly with captions and exports, and a self-critique report. It keeps one resumable JSON manifest of every prompt, seed, model and cost. Use it when the user asks to "make a video", a short film, an ad or a music video, end to end.
---

# video-director

This skill directs the other skills in this collection. It never renders anything itself. Each step calls a sibling skill that the **routing table** picks (`references/routing.md`) and records the result in **one manifest** (`references/manifest.schema.json`). If a run is interrupted, re-running it resumes from the manifest.

The pipeline has 9 stages:

```
intake → preflight+tier → bible → shot plan ─(gate)→ STILLS ⟲ still-qa → VIDEO ⟲ → continuity ⟲ → audio → assembly → critique
```

Hard rules:
1. **Stills come first.** No video job runs for a shot until its still is `approved`.
2. **Caps are hard.** When a retry or regen cap is reached, keep the best attempt and log it. When the `max_renders` or GPU-minute ceiling is reached, log `cap_hit` and stop rendering. Never keep rendering quietly.
3. **Open weights only.** Every route uses downloadable weights. Read the license caveats in `references/quality-playbook.md`. The LTX-2 weights are under the **Lightricks LTX-2 Community License, which is not OSI-approved**. If `brief.commercial_use` is true, say so to the user before the spend gate.
4. **Do not spend credit without approval.** On Google Colab or Comfy Cloud, `gates.spend` defaults to `human`. Show the estimate (GPU-minutes and renders) and wait for the user to say yes.

## Files
| path | what |
|---|---|
| `references/routing.md` | decision table: need → skill, workflow, inputs, fallback and tiers. Adding a skill takes one row |
| `references/manifest.schema.json` | schema of the production manifest (JSON Schema 2020-12 subset) |
| `references/quality-playbook.md` | per-model prompting and graph rules (Klein, LTX, Qwen edit, audio), budget rules and license caveats |
| `references/examples/*.manifest.json` + `.md` | worked examples: a 30 s story short (standard), a 15 s product spot (max) and a 20 s music-video snippet (draft) |
| `scripts/direct.py` | optional stdlib-only driver: `routes`, `validate`, `tier`, `run [--dry-run] [--target google-colab]`, `approve`, `package --target google-colab` |
| `../google-colab-runner/` | Google Colab packaging and orchestration (`references/google-colab.md` is the runbook) |

## 1. Intake: fill smart defaults and ask at most 3 questions
Write `brief` into a new manifest. Fill the defaults below and record each one in `brief.defaults_used`, so the user can see what you assumed.

| field | default | ask only if |
|---|---|---|
| kind | inferred: story, product, music-video, explainer | it is ambiguous |
| length_s | story 30, product 15, music-video 20 | none |
| aspect | 16:9 (product and music-video: 9:16) | there is a platform hint |
| fps | 24 | none |
| style | derived from the idea, plus "35mm film still" | none |
| audio | story: narration+music+sfx. product: VO+music. music-video: user track + lip-sync | music-video with no track: **ask for the track** |
| captions | sidecar SRT (vertical deliverables: burned) | none |
| deliverables | master + 9:16 | none |
| commercial_use | false | it is a brand or product: **ask**, because of the license caveats |
| target / budget | ask: local URL, Google Colab tunnel or Comfy Cloud; GPU-minutes or credits | **always**, if unknown |

## Where to run: local, Google Colab or Comfy Cloud
Decide this at intake (`target`), before preflight. Step by step:
1. **Ask what the user has.** A local GPU and its VRAM, a Google Colab plan, or Comfy Cloud credits. Never assume a paid option.
2. **Local** (`target.kind = local`) when a GPU with 16 GB+ is available: no per-minute cost, no session limits. Run `direct.py run m.json --url http://127.0.0.1:8188`.
3. **Google Colab** (`target.kind = google_colab`) when there is no suitable local GPU and the user has Google Colab compute units:
   1. `python skills/google-colab-runner/scripts/colab.py estimate m.json --gpu L4` (also T4 and A100). Show session minutes and compute units, and say that the rates are unverified.
   2. Get a compute-unit cap into `target.budget.max_credits`, and the user's yes: `direct.py approve m.json spend`.
   3. Choose the mode:
      - **package** (the user runs everything in Google Colab; no tunnel): `direct.py package --target google-colab m.json`. Hand over the `.ipynb` (and the assets zip). Afterwards, `colab.py ingest m.json <outputs.zip>`, judge, then `direct.py run` locally for continuity onward.
      - **orchestrate** (you drive it; full judge loop): the user runs the same notebook with `MODE = orchestrate` and pastes the tunnel URL. Then `direct.py run m.json --target google-colab --url <URL>`.
   4. On exit 5 (session dropped), ask for a restart and the new URL, then re-run the same command. It resumes from the manifest and re-uploads finished assets.
   5. At the end or at the cap, offer `colab.py teardown --url <URL>`, and remind the user that a connected runtime keeps billing.
4. **Comfy Cloud** (`target.kind = comfy_cloud`) when the user already pays for it and every route's nodes exist there: `COMFY_API_KEY` from the user's environment, `direct.py run m.json --url <their Comfy Cloud API URL>`. The spend gate is human as on Google Colab.
5. Whatever the target, run preflight first; it reads `/object_info` from that server and decides the tier.

## 2. Preflight and tier
Run **comfyui-preflight** against every workflow the plan will use. It reads `/object_info` and the model lists only, and executes nothing. Store `target.preflight` (ready per route, missing nodes and weights). Then pick the tier. `direct.py tier` does this for you.

| tier | min VRAM | still | video base → final | caps (still/variants/video/continuity) | pass mean/min | extras |
|---|---|---|---|---|---|---|
| draft | 16 GB | `still.flux2_4b` 1024×576 | 512×288 → 1024×576 | 1 / 1 / 0 / 0 | 3.0 / 2 | none |
| standard | 24 GB | `still.klein` 1280×704 | 640×352 → 1280×704 | 2 / 1 / 1 / 1 | 3.5 / 3 | LUT grade |
| max | 40 GB | `still.klein_base` | 768×448 → 1536×896 | 3 / 2 / 2 / 2 | 4.0 / 3 | SeedVR2 upscale, flf transitions |

Choose the highest tier whose VRAM fits, whose required routes are ready, and whose estimate (`renders × rate`) fits `budget.max_gpu_minutes`. Otherwise step down a tier. A route that is not ready uses its `fallback` column, or the shot is re-planned. The default rates are **unverified placeholders**.

## 3. Preproduction
1. **story-bible**: logline, cast with a *full visual descriptor* (pasted verbatim into every prompt), locations, palette, LUT and voice. Gate `bible`.
2. **shot-planning**: timed beats into shots with `start_s` (a running total), `duration_s`, type, framing, camera, cast, narration, SFX, `chain_from` and `transition_in`. Durations must sum to `length_s`. Write the still prompt (end-state, long) and the video prompt (motion only) per the playbook. Gate `plan`. For human gates, show the shot table and wait. `direct.py approve <manifest> plan` records the approval.

## 4. Routing
For every shot, set `still.route` and `video.route` from `routing.md`. Extra passes go in `shot.extra[]` (for example `vfx.onetake`, `fix.tryon` or `video.lipsync_wan`).

| shot need | route |
|---|---|
| default still | the tier's still route |
| product or character identity from a reference image | still + `fix.edit` with ref |
| camera moves / static | `video.i2v` (strength1 1.0 if static) |
| land on an exact end frame | `video.i2v_se` |
| speaking or singing on camera | `video.lipsync` / `video.lipsync_wan` |
| remove object / swap character | `vfx.remove` / `vfx.swap` (fallback `vfx.swap_ltx`) |
| stylise footage / one-take effect | `vfx.restyle` / `vfx.onetake` |
| join two shots smoothly | `transition.flf` (max) otherwise `transition.cut` |
| motion or blocking must match a clip or previs | `control.pose` / `control.canny` (+ `job.params.video`), after `plan.previs_passes` |
| an exact, named camera move | `camera.fun` (`params.MOVES`, for example `"arc-left-45"`; valid names are the keys of `MOVES` in camera-control/assets/motionfield_nodes/core/camera_trajectory.py), or `camera.ati` for drawn paths |
| audio drives the whole performance | `video.s2v` (`params.audio`), or `video.talk_music` for a singer on a full mix |
| copy an effect from a reference clip | `vfx.recipe_read` then `vfx.recipe_apply` |
| motion from a reference clip onto a still | `vfx.motion_ref` |
| placed-light relight of a keyframe | `fix.relight_lights` (fallback `fix.relight`) |
| a recurring identity needs a LoRA | `plan.lora`. The dataset gate is human and always runs before training |
| several GPUs or servers | `plan.dispatch` (`multi-gpu-dispatch/scripts/dispatch.py`) |

Unknown needs go to the closest row. If nothing fits, tell the user, and never call an unlisted closed API.

## 5. Stills and the judge loop
For each shot: render the still → judge it with **still-qa** (scores from the bible and prompt). A still passes when `mean ≥ pass_mean` and `min ≥ pass_min`. On a fail, choose the fix from the issue tags:
- identity: `fix.edit` with the cast reference, or swap the reference to the best previous pass
- composition or framing: re-prompt (rewrite the offending clause, keep the rest)
- artifacts: seed+1

Stop at `still_retries`. At draft tier, keep the best-scoring attempt and log its issues. At standard and max tiers, set the shot to `awaiting_approval` (exit 3) and show the user the best attempt. Record every attempt (prompt, seed, scores, file) in `shot.still.attempts[]`.

## 6. Video and continuity
- Render the video from the approved still (or from the last frame of the `chain_from` shot). Use LTX frames `8n+1`, base sizes in multiples of 32, and strength1 1.0 for static shots and 0.7 otherwise. Stage 2 is always 1.0.
- Measure every render with **shot-qc** (`qa.shot`: freeze, black, cuts, flicker, soft frames, clipping). Static cameras are exempt from the freeze check. A freeze or black flag fails the attempt. **When the measurements and the VLM disagree, the numbers win.**
- Judge 3 frames (first, mid, last) with still-qa, and retry up to `video_retries` with a new seed.
- Wan-family graphs (VACE, Fun Camera, S2V) use their sidecar `fps` (16) and 4n+1 frames instead of the LTX 8n+1 at 24 fps. `direct.py` handles this from `workflows/<file>.defaults.json`.
- **continuity-check** looks at every join (last frame of A vs first frame of B): identity, wardrobe, light direction and screen direction. On a fail, regenerate B, or insert a `transition.flf` at max tier, up to `continuity_regens`.

## 7. Audio
- VO: **voiceover** (Chatterbox), one line per shot, timed to `start_s`.
- Music: **music-sfx** ACE-Step (`audio.music`) set to the cut length plus 2 s, or the user's track.
- SFX: Stable Audio (`audio.sfx`) per `shot.sfx`.
- Lip-sync shots use the vocal stem for that shot's window.

## 8. Assembly
Run **film-assembly** `assemble.py`: concat or xfade, the LUT grade (standard and above), and a ducked music mix. Run **subtitles-captions** `make_srt.py` to build captions from the manifest narration (or from Whisper ASR on the mix), as a sidecar or burned in. Then exports: `post.reframe` for 9:16 and 1:1, `post.interp` for 60 fps, and `post.upscale` at max tier. Gate `final`.

## 9. Critique and report
Judge the mid-frame of the final cut, then write `REPORT.md`, which covers:
- what was asked vs delivered
- each shot's final score and the issues that were kept
- the caps that were hit
- renders and GPU-minutes (estimate vs actual)
- the models and licenses used (with the LTX and commercial caveats)
- 3 concrete things to improve on a re-run

The manifest itself is the full record of prompts, seeds, models and costs.

## Driving it
- **With the script:**
  - `python3 scripts/direct.py validate m.json`
  - `python3 scripts/direct.py run m.json --dry-run` (prints every call; no network and no subprocess)
  - `python3 scripts/direct.py run m.json --url $COMFY_URL`
  - `python3 scripts/direct.py package --target google-colab m.json` (Google Colab bundle)
  - `python3 scripts/direct.py run m.json --target google-colab --url $TUNNEL_URL` (drive a Google Colab ComfyUI)
  - It exits with 3 at a human gate. Run `approve`, then re-run.
- **Without it:** follow sections 1–9 by hand. Call each sibling skill's documented command, and update the manifest after **every** job (set the status to `done` with the outputs), so any agent can pick it up again.

## Adopted from agentY's director design
agentY (szprivate/agentY, MIT) runs 34 skills behind one orchestrator prompt. These rules were adopted here, rewritten in our own words:
1. **Measurements beat descriptions.** shot-qc numbers override VLM claims about motion, freezes and black frames.
2. **Say the plan, then act.** A numbered plan is shown, and you wait only at the gates that the user or the manifest set to human. You do not wait at every step.
3. **Never end on a menu.** Pick a route, say in one line why, and continue. Ask only for what only the user can supply (a file, a credential, consent to spend or train).
4. **Hard constraints.** A model or template the user names is never silently substituted. If its route is not ready, stop and ask rather than take the fallback. `direct.py` follows fallbacks automatically, so for a pinned route, set that row's `fallback` to `-` in your working copy of `routing.md`.
5. **Approve once.** An approved gate is never put up for approval again for the same work.
6. **One fix per QA note.** A retry changes only what the judge flagged and keeps the rest.
7. **The dataset gate is human** (lora-training). Nothing trains on an unapproved or changed dataset.

Not adopted:
- agentY's hosted and partner API routes (fal, Kling, Seedance, DashScope), because this collection is open weights only
- its canvas and viewer tools, which are specific to its UI

## Adding a skill
Add one row to `references/routing.md` in the documented 9-column format, and give the skill a `requirements.md`. `direct.py routes` checks that the skill folder and workflow exist.
