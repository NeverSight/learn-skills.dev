---
name: paper2video
description: Turn an arXiv paper into a narrated, fact-checked explainer video (1080p MP4) with animated 2D/3D scenes, subtitles and a verification report. Run with /paper2video <arxiv link or id> [overrides].
argument-hint: <arxiv link or id> [overrides]
disable-model-invocation: true
license: MIT
compatibility: Claude Code with a local shell. Needs Node 18+, Python 3.10-3.13, ~1 GB disk (voice model + headless Chromium). Tools install on first run.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/p2v *)
---

# paper2video

Paper in, explainer video out. The user picks the paper; everything after that is this workflow, with
**strict cross-checking instead of script approval**. The skill never publishes anything.

Paper to process: **$ARGUMENTS**

Every step runs through one command: `${CLAUDE_SKILL_DIR}/p2v <subcommand>` (works from any directory).
Always type that full path exactly as written here, not a shell variable or `cd` + `./p2v`: the pre-approved
permission matches this exact command, so other spellings stop for a permission prompt.
1. Run `${CLAUDE_SKILL_DIR}/p2v doctor`. It prints the folders (skill, tools, jobs, videos). If it ends with `-> run: ... setup`,
   tell the user "first run: installing tools (~1 GB, a few minutes)" and run `${CLAUDE_SKILL_DIR}/p2v setup` once,
   with the Bash tool's maximum timeout (600000 ms). If it is cut off, run it again: finished parts are skipped.
2. Write job files in the **jobs** folder that doctor printed (`<jobs>/<id>/`), never in the skill folder.
   Installed copies keep jobs and videos in `~/paper2video/`; a development clone keeps them in the repo.

## Input
Only the arXiv link or id is required (`https://arxiv.org/pdf/2610.35607`, `.../abs/...v2`, `2610.35607`).
Anything after it is an override (e.g. `3 min`, `voice am_michael`). Do not ask for more instructions.
Run the whole pipeline below with these defaults:

| Default | Value | User can override with |
|---|---|---|
| Length | 4-5 min, 10-14 scenes | "3 min" |
| Language / voice | **English**, Kokoro `af_heart` | `ko` / `Korean` / `한국어` → Korean (Supertonic 3 voice `F1`); another voice id (Kokoro `am_michael`..., Supertonic `F1`-`F5`, `M1`-`M5`) |
| Verification | step 9 always runs in a **fresh-context subagent**, all 5 layers; equations and derivations (not machine-checkable) are checked by the verifier against paper.txt with the evidence written in VERIFY.md | n/a (never skipped) |
| Fix loop | fix and re-verify up to 3 rounds, then stop with BLOCKED and the open items | n/a |
| Templates | if the skill folder is a git clone you can edit, move any new scene that would work for other papers into `engine/templates.js`; otherwise (plugin install) keep it in the job's `scenes.js` and list it as a template candidate in the report | n/a |
| Publishing | never upload or post anywhere; the MP4 is the end product | n/a |
| Git | do not commit; leave changes for review | "commit it" |

Only stop to ask the user when blocked (license forbids the planned visuals, the PDF has no text layer,
verification BLOCKED after 3 rounds, or a toolchain step fails twice).

## Korean (or another language)
When the overrides ask for Korean:
- `script.json`: `"lang": "ko"`; write subtitles and every on-screen string in natural Korean (plain 해요체 for narration).
  Keep widely used technical terms in English the first time, with a Korean gloss ("BEV(위에서 내려다본 지도)").
- TTS text (2nd element of each sentence): spell out units and abbreviations the way they should be read
  ("142센티미터", "엠에이피", "에이치백"); digits and dates are read correctly by the engine.
- `tts.py` picks Supertonic 3 automatically for non-English `lang` (first run downloads the model).
- `claims.json` quotes stay verbatim English from the paper; claim `text` may be Korean.
- Rendering needs a Korean font (macOS has Apple SD Gothic Neo; on Linux install Noto Sans CJK).

## Final report (always, at the end)
Per step: done / failed + output path · VERIFY.md verdict and open items · video path in the videos folder + length ·
new templates added · wall-clock time · anything the user should look at first.
Setup (`${CLAUDE_SKILL_DIR}/p2v setup`) installs Node packages, ffmpeg, Playwright Chromium, a Python 3.10-3.13 venv and the Kokoro voice model
into the tools folder, which survives updates. If the default `python3` is 3.14+, it picks 3.13/3.12, or set `PYTHON=/path/to/python3.12`.

## Pipeline

| # | Step | Command / output |
|---|---|---|
| 1 | Fetch paper + license | `${CLAUDE_SKILL_DIR}/p2v fetch <arxiv id or link>` → `<jobs>/<id>/paper/{meta.json,paper.pdf,paper.txt}` and job skeleton |
| 2 | Read + outline | Read `paper.txt` fully. Fill `<jobs>/<id>/BRIEF.md` (license block first, outline that follows the paper's own logic, shot list) |
| 3 | Script | `<jobs>/<id>/script.json`: scenes → sentences `[subtitle, tts_text]` |
| 4 | Claims | `<jobs>/<id>/claims.json`: every factual statement and every on-screen number, with source; `used_in` lists every sentence (`<scene id>.<index>`) that says or shows it |
| 5 | Mechanical check (script) | `${CLAUDE_SKILL_DIR}/p2v check <id>` → must be **FAIL 0, WARN 0** for subtitles, narration and claims (scene numbers are checked again in step 8) |
| 6 | Scenes | `<jobs>/<id>/scenes.js` (templates + custom), replacing the starter scene. See `references/scene-authoring.md` |
| 7 | Narration + timing | `${CLAUDE_SKILL_DIR}/p2v tts <id>` → `build/narration.wav`, `build/timing.json` |
| 8 | Preview QA + check | `${CLAUDE_SKILL_DIR}/p2v preview <id>` → `build/preview_*.jpg` and `build/onscreen.json` (every string drawn). Look at every sheet (overflow, overlap, blank, legibility, camera inside geometry), then `${CLAUDE_SKILL_DIR}/p2v check <id>` again: FAIL 0, WARN 0 now includes numbers drawn by scenes |
| 9 | Independent verification | Fresh-context verifier subagent per `references/verification.md`, all 5 layers, with the preview sheets → `<jobs>/<id>/VERIFY.md`. Fix and loop (re-run 5-8 for what changed) until it passes. Only a PASS goes to render |
| 10 | Render | `${CLAUDE_SKILL_DIR}/p2v render <id>` → `<videos>/<id>_<Short-Title>[_ko].mp4` (shortcut to `build/<id>.mp4`) + `build/contact.jpg` (no Playwright: `render <id> --manual`, open the URL in any browser) |
| 11 | Final checks | `${CLAUDE_SKILL_DIR}/p2v check <id>` once more (the render records every frame's text, so it sees more than the preview). Must be FAIL 0, WARN 0. Watch `contact.jpg` |
| 12 | Report | Final report (below). If `local/*.md` exists in the skill folder, follow those personal add-on steps after this one |

Re-runs: steps 7, 8, 10, 11 are idempotent. Change `script.json` → re-run 5, 7, 8, then re-verify the changed claims (9) and render.

## Hard rules
- **License first.** `meta.json.figure_reuse` decides whether paper figures may appear. Default: draw everything yourself; never paste paper figures or dataset camera images unless the license allows it (`references/licensing.md`). No company logos.
- **Spoken numbers count too.** Narration numbers are checked as digits and as English number words. Product or model names read aloud
  (H100 as "H one hundred", SD3.5) need an `allow_numbers` entry with the reason. Leave `tts` in script.json empty unless the user
  asked for a specific voice: the engine follows `lang` (Kokoro for `en`, Supertonic for others).
- **No unsourced numbers.** Every number in subtitles or on-screen strings must be covered by `claims.json`. Rounded numbers must state the exact source value in the claim `text` (e.g. "141.72 → shown as 142").
- **Keep the paper's conditions.** "Best" needs its qualifiers ("among compared methods", "after benchmark-specific fine-tuning", ablation setting, hardware).
- **Label approximations and opinions on screen**, not only in the claims file (`derived` / `opinion` kinds need `on_screen_label`).
- **Show where before how.** Open each mechanism with a location/context cue (what part of the system, where on the car) before the mechanism itself.
- **Narration:** Kokoro (Apache-2.0) is the default and is cleared for public use. Do not swap in voices whose terms for public or commercial use are unchecked.
- **Plain language.** Expand jargon on first use; one concrete number beats three abstract sentences.

## Files
- `engine/` timeline player (`main.js`), 3D/2D primitives (`core.js`), reusable templates (`templates.js`)
- `scripts/` fetch, tts, check_claims, serve/render (frames → MP4 via ffmpeg)
- `p2v` single entry point (setup, doctor, fetch, check, tts, preview, render, collect, smoke, run); `scripts/p2v_paths.py` decides the folders
- `templates/job/` skeleton copied into new jobs
- `jobs/2610.30340/` complete worked example (copied into the jobs folder on first use) (Foundation4D, 14 scenes, 66 claims, 4.6 min)
- `jobs/_smoke/` and `jobs/_smoke_ko/` short template-only jobs for testing the toolchain (English / Korean)
- `references/` verification, scene authoring, licensing
- `local/` (optional, git-ignored) your own add-on steps, e.g. a publishing checklist

## Smoke test (after setup)
```bash
${CLAUDE_SKILL_DIR}/p2v smoke        # English; stops at the first failing step; render refuses stale narration
${CLAUDE_SKILL_DIR}/p2v smoke --ko   # also tests Korean narration (downloads the Supertonic model on first run)
```
