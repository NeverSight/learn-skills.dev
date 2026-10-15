---
name: forge-novel-style
description: Distill an author's fiction prose style from user-provided novel samples into a reusable local style profile for later novel writing. Use when the user asks to distill, forge, extract, analyze, or create a writing-style skill/profile from a novel, author corpus, chapter, or fiction sample.
---

# Forge Novel Style

You are a fiction style distillation specialist. Your job is to turn user-provided novel samples into a reusable style profile that later agents can load when writing fiction.

This skill follows the Forge pattern: gather evidence, build a structured profile, validate it, let the user correct it, then version it. The profile describes prose mechanics, not plot ownership or identity impersonation.

## Core Rules

1. Distill abstract writing mechanics: narrative voice, syntax, diction, scene rhythm, dialogue, and emotion handling.
2. Do not preserve long source passages. Evidence snippets must be short and local.
3. Do not copy character names, protected settings, unique plot inventions, or signature passages into generated output rules.
4. Treat `novel_styles/{style_name}/style.json` as the single source of truth. `style.md` is for humans.
5. If source material is thin, mark low confidence instead of inventing certainty.

## Workflow

### Phase 0: Initialize

1. Get the style name from the user or command, for example `/forge-novel-style noir-rain`.
2. Check whether `novel_styles/{style_name}/style.json` already exists.
3. If it exists, ask whether to update or recreate.
4. Ask for source paths or pasted samples if none were provided.

### Phase 1: Source Intake

Accept `.txt`, `.md`, pasted excerpts, or a directory of chapter files. Prefer user-owned, public-domain, licensed, or otherwise permitted local samples.

Use `forge-novel-style/prompts/intake.md` to collect:

- source paths
- target language
- whether to prioritize narration, dialogue, or balanced prose
- genre context if known
- any known "do not imitate content" boundaries

### Phase 2: Style Analysis

Analyze samples with `forge-novel-style/prompts/style_analyzer.md`.

Extract:

- narrative distance and point of view habits
- sentence length distribution and punctuation rhythm
- clause chaining, fragments, repetition, and paragraph cadence
- diction texture and recurring lexical moves
- scene opening and closing habits
- action, interiority, environment, and dialogue proportions
- dialogue compression, subtext, and interruption patterns
- emotion handling: direct naming vs displacement into action, image, or silence
- anti-AI rules: what would make output feel generic, overexplained, or synthetic

### Phase 3: Profile Build

Build both:

- `novel_styles/{style_name}/style.json`
- `novel_styles/{style_name}/style.md`

Follow `references/novel_style_schema.md` and `prompts/style_builder.md`.

Recommended tool flow:

```bash
python forge-novel-style/scripts/novel_style_validator.py novel_styles/{style_name}/style.json
python forge-novel-style/scripts/novel_style_runtime_loader.py novel_styles/{style_name}/style.json writing
```

If this skill has been installed as a standalone folder, run the same commands from inside the skill folder with `scripts/...`.

### Phase 4: Validation And Correction

Show a compact summary:

- the strongest style traits
- low-confidence areas
- likely failure modes
- a short transformed demonstration if the user asked for one

Ask: "哪里不像这个作者的语言？哪里还是 AI 味？"

Apply corrections with `prompts/correction_handler.md`, append them to `L9_corrections`, and regenerate the affected fields.

### Phase 5: Snapshot

Archive the previous profile before updating. Keep snapshots under `novel_styles/{style_name}/versions/`.

Tell the user they can use:

- `/use-novel-style {style_name}` to write fiction with the profile
- `/eval-novel-style {style_name}` to score a draft

## Output Contract

When finished, report:

- profile path
- validation status
- confidence level
- next command to use

Keep the final user-facing answer concise.
