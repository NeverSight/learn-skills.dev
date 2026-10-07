---
name: make-video
description: READ THIS FIRST for any request to make, edit, or publish a video in this repo — "make a video", "new video", "edit this clip", "create a reel/short", "faceless video", "turn this post/idea into a video", or any ambiguous video ask. This is the entry-point router — it asks what you're making (talking-head short 9:16 · long-form 16:9 · faceless motion reel · reel script only), scaffolds projects/<name>/, then runs the right pipeline end-to-end and ships to projects/<name>/outputs/. Route through this instead of picking video-edit / motion-design-edit / reel-script directly.
argument-hint: "<what you're making, or a source clip / VO / idea>"
user-invocable: true
metadata: { "tags": "read-first, router, intent-routing, video" }
---

# /make-video — one entry point for every video

You are the dispatcher for this video pipeline. Never guess a
workflow: **confirm the intent, then commit to exactly one route below.**

## 1. Intake (always first)

Ask (via AskUserQuestion, one round, skipping anything the user already said):

1. **What are we making?**
   - `talking-head short` — 9:16 reel from a camera clip
   - `long-form` — 16:9 YouTube video from a camera clip
   - `faceless motion reel` — paper-style motion graphics over a voiceover, no camera
   - `reel script only` — just write the script
2. **Project name** — then scaffold if missing:
   `mkdir -p projects/<name>/{raw,refs,working,outputs/previews}`
3. **Source** — clip path, VO path, or the idea/post text. Copy source media
   into `projects/<name>/raw/` before doing anything else.
4. **Brand setup, once per install (routes A/B only):** if repo-root
   `BRAND.md` doesn't exist yet, run the brand-setup flow in SETUP.md before
   your first render — it asks primary/secondary/accent colors, background
   preference, and fonts, then edits the token files
   (`$SKILL/remotion/src/templates/hfBrand.ts`,
   `$F5/remotion/src/motion/tokens.ts`) and writes `BRAND.md` so you never
   ask again. If `BRAND.md` already exists, skip straight to rendering — the
   token files already reflect the user's brand.
5. **If route C (faceless motion reel) with a VO in hand** — also ask
   **visual style**: `paper brand` (cream/ink/orange-punch, the original
   reference-reel look — default) vs `visual os` (the same brand-setup
   preset as routes A/B, or its own configured brand if `BRAND.md` differs
   for this project). Write the answer to `projects/<name>/.pr_style`
   (one word: `paper` or `visual-os`) — `series_pipeline.sh` reads it
   automatically on every render from then on, no need to ask again.

Shorthand used below (run from the repo root):

```
SKILL=.claude/skills/video-edit                   # 9:16 finisher (hf_* graphics)
F5=.claude/skills/video-edit-longform              # 16:9 finisher (viz graphics)
MSKILL=.claude/skills/motion-design-edit          # faceless pr_* graphics
PY="$(pwd)/.venv/bin/python"                      # repo-root shared venv (WhisperX local fallback)
OUT="$(pwd)/projects/<name>/outputs"              # ALWAYS absolute
```

## 2. Transcription (all routes)

Default — **the cloud transcription bridge**, which needs ONE of
`ASSEMBLYAI_API_KEY` or `OPENAI_API_KEY` in the repo `.env` (AssemblyAI is
tried first if both are set; pass `--provider openai` to force the other):

```bash
.venv/bin/python .claude/skills/make-video/scripts/transcribe_assemblyai_bridge.py <media>
```

Prints the workdir (`~/.cache/video-edit/<stem>_<sha1[:12]>/`) and writes
`words.json` + `.polished` there. Fallback for sensitive clips: local WhisperX
(`$PY "$SKILL/scripts/transcribe.py" <media>`).

**Mandatory:** read the transcript back against what was actually said and
hand-patch wrong words in `words.json` (keep `start`/`end`), then make sure
`.polished` exists. ASR mishears predictably (past examples: "instructions"→
"injections", "the floor"→"to Claude").

## 3. Routes

### A. Talking-head short (9:16) → `video-edit` (hf_* graphics)

Follow **EXECUTION.md §§0–5** exactly. Summary:
1. Phone portrait clip stored landscape+rotation flag? Bake it first
   (EXECUTION §0 ffmpeg command) → use the `.portrait.mp4` from there on.
2. `video-edit` is a **finisher**, not a cutter — it expects pre-cut footage.
   Raw/uncut multi-take recordings need filler-word and silence removal done
   first (by hand, or with your own cutting tool) before this route.
3. Transcribe (§2 above) → author `<workdir>/broll_plan.json` with `hf_*` kinds
   (EXECUTION §2 table). **Vary the templates** — rotate `hf_stat`, `hf_title`,
   `hf_chart`, `hf_listicle`, `hf_lower_third`, `hf_before_after`…; reserve the
   mascot `hf_callout` for a beat or two, never the through-line.
4. `$PY "$SKILL/scripts/lint_plan.py" <workdir>/broll_plan.json` — must pass.
5. Preview: `OUT_DIR="$OUT" CAPTION_EMPHASIS="…" bash "$SKILL/scripts/render.sh" <clip>`
   → iterate on the plan until the user likes it.
6. Final (only after explicit sign-off): same command plus `QUALITY=final SCORE=0`.

### B. Long-form (16:9) → video-edit-longform (viz graphics)

Same loop as route A but against `$F5`: transcribe → author the beat plan with
its `viz`/native kinds (`$F5` knowledge + `template_library.md`) → lint →
preview `bash "$F5/scripts/render.sh"` with absolute `OUT_DIR` → sign-off →
final. Notes:
- Colors/fonts come from `$F5/remotion/src/motion/tokens.ts` — run the brand
  setup in SETUP.md before your first render so this matches your own brand,
  not the shipped example preset.
- The bespoke one-off compositions from the original bundle (channel-specific
  intros/outros) were removed when this skill was cleaned up for reuse — only
  the generic `EditedVideo` engine and reusable `templates/`/`motion/` library
  remain. Don't try to reintroduce channel-specific one-offs here.

### C. Faceless motion reel → `reel-script` + `motion-design-edit` (pr_* graphics)

**No VO yet** (user brought an idea, notes, or a Facebook/LinkedIn post):
1. Run `/reel-script` on it → beat-tagged script (HOOK / CREDIBILITY / REFRAME /
   TIP 1-3 / CTA, each tagged `pr_card`/`pr_punch`/`pr_proof`).
2. Save it to `projects/<name>/working/script.md`, hand it to the user, and
   **stop**. They record the VO and drop it in `projects/<name>/raw/`.

**With a VO** in `raw/` — follow **EXECUTION.md "Faceless motion-graphics
workflow"** exactly. Summary:
1. Build the black 1080×1920 base with the VO muxed in, at the VO's **exact
   ffprobe duration** (never `-shortest`) → `projects/<name>/working/base.mp4`.
2. Transcribe base.mp4 (§2 above) + verify/patch the transcript.
   **Check for `raw/captions.txt`** — if present, parse it
   (`scripts/parse_captions.py`) and use its lines verbatim as on-screen
   text; it's authoritative for wording, not a paraphrase source. Without
   it, compress the transcript into on-screen text yourself as before.
3. **Read `MOTION-STYLE.md` (repo root) first**, then author `<workdir>/broll_plan.json`: group ideas into evolving multi-layer scenes (split on nearly
   every sentence), `speech_anchor` on every beat, 5-part arc per
   `$MSKILL/knowledge/paper_style.md`. `projects/motion-reel/working/broll_plan.json`
   is the reference plan.
4. `python3 "$MSKILL/scripts/lint_plan.py" <workdir>/broll_plan.json projects/<name>/working/base.mp4`
5. Preview + final, both scored (music + SFX) by default:
   `bash "$MSKILL/scripts/series_pipeline.sh" <name> preview` /
   `bash "$MSKILL/scripts/series_pipeline.sh" <name> final` (only after
   explicit sign-off). This reads `.pr_style` automatically and writes to
   `projects/<name>/outputs/previews/` and `outputs/` respectively — no
   per-project script needed. See EXECUTION.md's "Recurring series"
   subsection for the full pattern.
6. **If this project will run more than one episode**, scaffold a
   project-local `STYLE.md` creative contract (palette table, component
   rules, beat arc, timing rules) — mirror
   `projects/claude-code-edit/STYLE.md`'s structure — so every future
   episode reuses the same locked look instead of re-deriving it.

### D. Reel script only → `reel-script`

Run `/reel-script` on the idea/post; save the beat-tagged script to
`projects/<name>/working/script.md`. Offer route C as the follow-up once
they've recorded the VO.

## 4. Hard rules (every route)

- **Brand:** routes A/B always render in whatever brand `BRAND.md` records —
  run the brand-setup flow (SETUP.md) once per install before the first
  render if `BRAND.md` doesn't exist yet (see §1 step 4). Ships with an
  example "Visual OS" preset (navy ink, electric-blue accent, Claude-orange
  punch, light bg; Georgia titles · Inter body · JetBrains Mono peripheral
  chrome only) until you customize it. Whatever palette you land on, keep it
  disciplined: one clear accent color, one distinct punch/execution color,
  and don't let peripheral-chrome fonts bleed into headline/body roles.
  Route C (`pr_*`) supports **two selectable styles** — Paper Brand
  (default, its own cream/ink/orange palette, independent of the brand-setup
  flow) or the configured Visual-OS-style brand, chosen per project via
  `.pr_style` (see §1 step 5 above). Token files are the source of truth:
  `$SKILL/remotion/src/templates/hfBrand.ts`,
  `$F5/remotion/src/motion/tokens.ts`, `$MSKILL/remotion/src/templates/paperBrand.ts`.
- **Never auto-run the final render.** Preview → user says "ship it" → final.
- **Absolute `OUT_DIR` always** — render.sh cd's into its remotion dir; a
  relative path strands the output inside the skill.
- `pr_proof` without `image_path` renders a blank card — source a real
  screenshot/photo or explicitly flag the placeholder before calling it done.
- Finals belong in `projects/<name>/outputs/`, previews in `outputs/previews/`,
  intermediates in the `~/.cache/video-edit/` workdir — never in `raw/`.
- After shipping or pausing, append the session to **WORKLOG.md** (state,
  decisions, what's next).
