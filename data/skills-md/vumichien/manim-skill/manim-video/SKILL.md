---
name: manim-video
description: Generate Manim animations from ideas, research papers, or math topics. Use when user asks to "make a video about X", "animate X", "explain X with Manim", or invokes /manim-video. Orchestrates a 4-role pipeline (researcher + planner + implementer + main) to produce out/<run-id>/video.mp4 with chrome (header bar + captions) and cross-fade transitions, plus storyboard, scenes, narration script, and captions.srt.
license: Apache-2.0
metadata:
  author: vumichien
  version: "0.2.0"
  homepage: https://github.com/vumichien/2026-manim-skill
---

# manim-video

Turn ideas, papers, and math topics into rendered Manim animations with on-screen
chrome (header bar + scene title cards), bottom-of-frame captions, gtts voiceover
(default), and cross-fade transitions between scenes.

## When to use

Activate this skill whenever the user wants:
- A short explanatory video for a concept ("explain Fourier transforms", "animate Pythagoras")
- A research paper visualized ("turn this arXiv paper into a 5-min video")
- A math derivation animated step by step
- Any invocation of `/manim-video --idea | --paper | --math`

Do **not** activate for:
- Static images or single-frame plots — use matplotlib / `/ck:ai-multimodal` instead
- Slideshow presentations — use `manim-slides` or `/ck:remotion`
- Generic web animation — use `/ck:remotion` or shaders

## Inputs

| Flag | Required | Default | Notes |
|---|---|---|---|
| `--idea "<topic>"` | one of these three | — | Pure topic; pipeline invents scope. |
| `--paper <id\|url\|path>` | one of these three | — | arXiv id, PDF (local/URL), or HTML page. |
| `--math "<topic>"` | one of these three | — | Math specialization; prefers MathTex when LaTeX available. |
| `--voice gtts\|openai\|elevenlabs` | optional | `gtts` | **Default flipped from `null` to `gtts` in 0.2.0.** Keyless for gtts. |
| `--no-voice` | optional | off | Opt out; captions still render. Mutually exclusive with `--voice`. |
| `--no-chrome` | optional | off | Disable header + title cards. Captions still render. |
| `--transition-s <float>` | optional | 0.7 | Cross-fade duration; range 0.3–1.5. |
| `--quality low\|medium\|high\|4k` | optional | `high` | 1080p60 default. |
| `--storyboard-only` | optional | off | Stop after T1; skip rendering. |
| `--out <dir>` | optional | `out/<run-id>/` | Override output directory. |

Run-id format: `<YYMMDD-HHMM>-<slug>` (slug derived from topic, ≤40 chars).

## Pipeline

```
T0 main → spawn manim-researcher  (reads source.md if --paper)  → outline.md
       || spawn manim-planner skeleton                          → storyboard.draft.yaml
T1 main → spawn manim-planner final (reads outline + draft)     → storyboard.yaml (schema 0.2.0)
T2 main → spawn manim-implementer
            → emits scenes/_shared.py (chrome module, palette substituted)
            → emits scenes/scene_NN.py per scene (header + title card + caption track)
            → renders per-scene mp4 via scripts/render.py (retry budget = 5)
            → calls scripts/concat-xfade.py with meta.transition_s
            → calls scripts/emit-captions-srt.py to write captions.srt
T3 main → write summary.md (+ paths to captions.srt, _shared.py)
```

### Step-by-step

1. **Parse flags.** Validate exactly one of `--idea/--paper/--math`. Derive `run_id` and `out_dir`. Resolve voice:
   ```
   if --no-voice: voice = null
   elif --voice <p>: voice = <p>
   else: voice = "gtts"        # default since 0.2.0
   ```
   Resolve chrome:
   ```
   show_progress     = not --no-chrome
   show_title_card   = not --no-chrome   (per-scene; planner override possible)
   ```
   Validate `--transition-s` in [0.3, 1.5]; clamp on out-of-range.

2. **Ingest (only if `--paper`).** Run:
   ```bash
   python scripts/ingest-router.py "<source>" --out <out_dir>
   ```
   Produces `<out_dir>/source.md` + `<out_dir>/source.meta.json`. If exit non-zero: stop, write summary.md with error.

3. **T0 — spawn two agents in parallel.**

   Read `agents/manim-researcher.md` and `agents/manim-planner.md`. Spawn both via the `Task` tool **in a single message** so they run concurrently:

   - Task A: subagent_type=`general-purpose`, prompt = `<contents of agents/manim-researcher.md>` + run-specific args (run_id, out_dir, source/topic, source_md_path if --paper).

   - Task B: subagent_type=`general-purpose`, prompt = `<contents of agents/manim-planner.md>` + skeleton-mode args (mode: skeleton, run_id, out_dir, topic, voice, quality, no_chrome, transition_s).

4. **T1 — final storyboard.** After T0 returns, spawn the planner in `mode: final` with `outline_path`, `draft_path`, and on retry, `validation_errors`. Then validate:
   ```bash
   python scripts/validate-storyboard.py <out_dir>/storyboard.yaml
   ```
   If exit non-zero: re-spawn the planner once with `validation_errors`. After two failures, escalate to summary.md.

5. **`--storyboard-only` short-circuit.** If flag set, jump to step 7.

6. **T2 — implementer.** Spawn:
   - subagent_type=`general-purpose`, prompt = `<contents of agents/manim-implementer.md>` + args:
     ```
     RUN ARGS:
       run_id: <run_id>
       out_dir: <out_dir>
       storyboard_path: <out_dir>/storyboard.yaml
       quality: <quality>
       voice: <gtts|openai|elevenlabs|null>
       no_chrome: <true|false>
       retry_budget: 5
     OUTPUT: scenes/_shared.py + scenes/scene_NN.py + manim_media/ + render.log + video.mp4 + captions.srt
     ```

   Implementer writes `<out_dir>/render.log` with per-scene render JSON (now including `chrome_emitted`, `voice_path`, `scene_duration_s` fields).

7. **T3 — summary.** Write `<out_dir>/summary.md` with:
   - Run id, command-line args, total duration
   - Paths: source.md, outline.md, storyboard.yaml, scenes/_shared.py, scenes/, video.mp4, captions.srt
   - Render outcomes (per scene: ok / error_class / render_time_s)
   - Voice path summary (gtts | fallback_caption_only | none); link error.md if voice fallback occurred
   - Next steps if errors occurred

## Outputs

```
out/<run-id>/
├── source.md                # only if --paper (frontmatter + extracted markdown)
├── source.meta.json         # only if --paper
├── outline.md               # researcher: tldr + key concepts + visual metaphors + narrative arc
├── storyboard.draft.yaml    # planner skeleton (schema 0.2.0)
├── storyboard.yaml          # planner final (validated, schema 0.2.0)
├── scenes/
│   ├── _shared.py           # chrome module emitted ONCE per run
│   └── scene_NN.py          # implementer-emitted Manim scenes
├── manim_media/             # raw Manim render artifacts
├── video.mp4                # final concatenated render with cross-fades
├── captions.srt             # SRT captions (cumulative offsets across all scenes)
├── render.log               # per-scene render JSON (with chrome_emitted, voice_path, scene_duration_s)
├── error.md                 # only if any scene failed or voice fallback triggered
└── summary.md
```

## Error handling

- **Ingest fails** → stop after step 2; summary.md notes the URL/PDF that failed.
- **Storyboard invalid twice** → escalate to user; do not start rendering.
- **Render fails after retry budget exhausted** → implementer keeps successful scenes; concat-xfade builds video from successful subset; summary.md flags incomplete render.
- **LaTeX missing + --math used** → main pre-checks `xelatex --version`. If absent: warn user, downgrade MathTex hints to Text in the storyboard via planner second-pass.
- **Voice fallback** → after second voice-related failure on any scene, all remaining scenes downgrade to voice-free. Logged in error.md; final video is captioned only.
- **xfade unavailable** → concat-xfade falls back to plain ffmpeg concat (hard cuts). Logged in summary.md.

## References

Lazy-load these only when needed:

- [`references/manim-api-cheatsheet.md`](references/manim-api-cheatsheet.md) — Mobject + animation reference + chrome helpers
- [`references/storyboard-schema.md`](references/storyboard-schema.md) — Storyboard YAML format (v0.2.0)
- [`references/voiceover-text-style.md`](references/voiceover-text-style.md) — Style guide for `voiceover_text` field
- [`references/shared-chrome-template.py`](references/shared-chrome-template.py) — Template the implementer copies into _shared.py
- [`references/flag-reference.md`](references/flag-reference.md) — Long-form flag semantics
- [`references/render-runner-contract.md`](references/render-runner-contract.md) — `scripts/render.py` JSON contract
- [`references/xfade-concat-contract.md`](references/xfade-concat-contract.md) — `scripts/concat-xfade.py` JSON contract
- [`references/voiceover-setup.md`](references/voiceover-setup.md) — TTS provider env vars + fallback policy
- [`../../docs/storyboard-migration-0.2.0.md`](../../docs/storyboard-migration-0.2.0.md) — 0.1.x → 0.2.0 migration guide

Agent prompts live in `agents/`:

- [`agents/manim-researcher.md`](../../agents/manim-researcher.md)
- [`agents/manim-planner.md`](../../agents/manim-planner.md)
- [`agents/manim-implementer.md`](../../agents/manim-implementer.md)

## Pre-flight

Before T0, verify the venv is ready:
```bash
python scripts/check-env.py
```
If exit non-zero: instruct user to run `pwsh scripts/install.ps1` (Windows) or `bash scripts/install.sh` (Linux/macOS), then retry.
