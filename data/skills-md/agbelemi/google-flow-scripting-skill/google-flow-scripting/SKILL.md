---
name: google-flow-scripting
description: Plans, scripts, storyboards, validates, and audits multi-shot Google Flow, Veo, and Gemini Omni Flash video projects. Use for narrative shorts, animation, live action, documentaries, ads, music videos, continuity planning, reference-image planning, prompt writing, or pre-generation QA.
---

# Google Flow Scripting and Prompting

> **Ask for surface, model, mode, and segment length before writing scenes.** Google Flow and the Gemini API expose different capabilities. In Flow, Veo 3.1 commonly uses 4-, 6-, or 8-second clips, Veo Quality is more restricted, and Gemini Omni Flash supports 4-, 6-, 8-, or 10-second generations. Confirm the active interface because features change.
>
> **Storyboard every segment as stills and approve them before video generation.** Panels first, approval second, video third.
>
> **Hard storyboard rule:** "A storyboard-generation prompt must command image generation in its first sentence, declare the exact output count and layout, prohibit planning responses, and enumerate forbidden invented actions."

**Version:** 1.6.0

Use this Skill to turn a video brief into a production-ready, continuity-aware package for Google Flow or the Gemini API.

## Non-negotiable output rules

1. Every referenced character or location uses a canonical `@PascalCase` handle with no spaces or punctuation, for example `@Kwame`, `@CafeLadies`, and `@SidewalkCafe`.
2. Use the canonical handle every time the referenced asset is named inside a generated script, not only in the attachment list.
3. Do not use em dashes in generated scripts. Use a colon, comma, full stop, parentheses, or spaced hyphen.
4. A storyboard copy-paste prompt begins exactly with:

```text
GENERATE THE STORYBOARD IMAGE NOW.
```

5. A ten-second scene with four authored moments uses exactly four panels in a 2x2 grid. Use 3x3 only when nine distinct frames were explicitly authored.
6. Keep internal operator notes, the copy-paste generation prompt, and the approval checklist in separate sections.

## Operating principles

1. **Do not assume guaranteed implicit memory between independent generations.** Carry continuity through self-contained prompt details, references, saved frames, supported first/last-frame controls, extensions, edits, and state tracking.
2. **Treat platform limits as dated facts.** Read `reference/FLOW-FEATURES.md` before making a capability claim. When the current interface differs, trust the active interface and record the discrepancy.
3. **Plan assets before segment prompts.** Establish cast, recurring objects, locations, canonical handles, reference priority, and set anchors first.
4. **Build plates from approved images, not identity prose.** Text descriptions can recreate a different person.
5. **Storyboard before expensive video generation.** Check identity, geography, composition, state, and handoffs in stills.
6. **Make each generation prompt usable on its own.** Avoid backward references such as "the same person" or "as before" unless an attached reference or frame is named explicitly.
7. **Use project policies, not universal creative laws.** Exact one-second beats, no on-screen text, and generated audio are configurable.
8. **Treat Omni as a separate workflow.** It supports conversational editing and broader multimodal context, but it does not support every Veo control.

## Workflow

### 1. Establish the production profile

Resolve:

- surface: Google Flow or Gemini API
- model: Veo 3.1 variant, Gemini Omni Flash, or another named model
- mode: text to video, first frame, first and last frame, references to video, video edit, or extend
- segment length
- aspect ratio
- format and visual treatment
- runtime and delivery platform
- audio policy
- text policy
- rights-sensitive people, brands, locations, or claims

Do not write timed scenes until the first four items are known.

### 2. Read the relevant craft files

Use:

- `core/flow-orchestrator.md`
- `core/flow-story-architect.md`
- `core/flow-asset-manager.md`
- `core/flow-storyboard-director.md`
- the closest file under `formats/`
- `core/flow-continuity-auditor.md`

### 3. Build the production package

Produce, in order:

1. brief and assumptions
2. runtime arithmetic and segment map
3. cast, object, environment, and state inventory
4. canonical handle and reference plan
5. storyboard contact-sheet package
6. approved final panel and handoff plan
7. self-contained video prompts
8. mechanical validation results
9. human continuity audit and unresolved risks

### 4. Prompt text policy

Video, reference-sheet, and ordinary image prompts begin with one explicit text policy:

```text
NO TEXT IN THE IMAGE: do not render words, labels, captions, or watermarks.
```

or:

```text
INTENTIONAL TEXT IN THE IMAGE: state the exact words, surface, and placement; no other text.
```

Storyboard prompts begin with the image-generation command, then place the text policy near the top.

### 5. Audio policy

For generated-audio workflows, include an `AUDIO:` block with dialogue, effects, ambience, music, silence, and exclusions when useful.

```text
AUDIO: Intentional silence.
```

For visual-only previs or sound added in post, state that policy and validate with `--no-require-audio`.

### 6. Generate a storyboard package

Use the agent instructions in `core/flow-storyboard-director.md`, the canonical template in `prompts/storyboard-contact-sheet.md`, or the executable generator:

```bash
python scripts/generate_storyboard_prompt.py examples/storyboard-spec.json \
  --output storyboard-package.md
```

### 7. Validate

Example for Flow and Omni reference generation:

```bash
python scripts/validate.py storyboard-package.md \
  --segment-length 10 \
  --surface flow \
  --model omni-flash \
  --mode references-to-video \
  --beat-mode off \
  --no-require-audio
```

Example for a Veo video prompt:

```bash
python scripts/validate.py video-script.md \
  --segment-length 8 \
  --surface flow \
  --model veo-3.1-fast \
  --mode text-to-video \
  --beat-mode exact
```

The validator is a mechanical linter, not a semantic continuity model. After it passes, run the continuity audit.

## Installation and updates

Install with Python, Bash, or PowerShell:

```bash
python scripts/install.py --tool cursor
./scripts/install.sh --tool cursor
powershell -ExecutionPolicy Bypass -File scripts/install.ps1 --tool cursor
```

Check and apply future release updates:

```bash
python scripts/check_update.py
python scripts/update.py
```

Downloaded and installed copies never update silently. The updater verifies checksums and tests, detects local changes, and creates a backup before replacement. Git clones should use `git pull` instead. See `reference/UPDATE-GUIDE.md`.

## Safety and rights

Before using a real person, protected brand asset, sensitive claim, archival material, or documentary reconstruction, identify consent, licence, disclosure, and factual-verification requirements. Never present a generated reconstruction as authentic evidence.

## Supporting resources

- `reference/PLAYBOOK.md`: production methodology
- `reference/FLOW-FEATURES.md`: dated capability notes
- `reference/TEMPLATES.md`: prompt and deliverable templates
- `reference/FAILURE-MODES.md`: evidence-tagged failure table
- `reference/UPDATE-GUIDE.md`: safe updates and rollback
- `reference/RELEASE-PROCESS.md`: future release procedure
- `release-history/`: permanent notes for every version
