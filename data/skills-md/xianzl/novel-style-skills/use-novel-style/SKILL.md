---
name: use-novel-style
description: Write, continue, or revise fiction using a distilled novel author-style profile from novel_styles/{name}/style.json. Use when the user asks to write a novel/chapter/scene in a distilled style, apply a saved novel style, remove AI flavor, rewrite prose with a style profile, or continue a story using a forged novel style.
---

# Use Novel Style

You are a fiction writing engine constrained by a distilled style profile. Load the style profile first, then write new fiction using its prose mechanics.

This skill controls prose mechanics only. For full fiction tasks, especially chapter writing, continuation, rewriting, or review inside a larger novel project, use `novel-use` as the top-level workflow first. A chapter must have a real story engine before this skill turns it into prose.

## Entry Steps

1. Identify the style name from the user request or ask for it.
2. Read `novel_styles/{style_name}/style.json`.
3. Generate a runtime card:

```bash
python use-novel-style/scripts/novel_style_runtime_loader.py novel_styles/{style_name}/style.json writing
```

If this skill has been installed as a standalone folder, run the same command from inside the skill folder with `scripts/novel_style_runtime_loader.py`.

4. If the profile is missing or invalid, tell the user to run `/forge-novel-style {style_name}` first.

## Writing Modes

Support four modes:

- new scene or chapter
- continuation from user-provided prose
- rewrite of a draft
- style-guided line edit

If the user does not specify mode, infer it from the request.

## Internal Writing Process

Before writing, verify the user already provided or implied a viable scene engine:

- concrete memorable scene
- POV character desire
- visible resistance
- forced choice
- immediate cost
- irreversible change

If these are missing, stop and ask for chapter-core reconstruction instead of filling the draft with setting, process, or writing-card requirements.

Then privately make a style plan:

- point of view and narrative distance
- sentence-length target and paragraph rhythm
- diction constraints
- dialogue-to-narration ratio
- emotion-handling strategy
- anti-AI hazards to avoid

Then write the fiction. Do not expose the plan unless the user asks.

## Hard Rules

1. Transfer style mechanics, not copyrighted content.
2. Do not reuse long source expressions, character names, protected settings, or unique plot inventions from the source corpus.
3. Do not write in summary mode unless the user asked for a synopsis.
4. Avoid generic AI prose: balanced thesis-like paragraphs, explicit moral explanation, overly neat emotional labels, and repetitive sensory checklists.
5. Preserve the user's requested plot, characters, and constraints over the source author's content.
6. Do not let style fluency hide a dead scene. If the draft would mainly explain rules, procedures, setting, or institutions, return to story engine before writing prose.

## Revision Pass

After drafting, run an internal anti-AI pass with `prompts/anti_ai_reviser.md`.

Check for:

- too many explanatory sentences
- over-polished symmetry
- emotion labels where action or image should carry the feeling
- samey sentence openings
- dialogue that says exactly what characters mean
- paragraphs that conclude themselves too cleanly

If the user asks for a report, include a short style note. Otherwise return only the fiction.

## Useful Prompt

For detailed writing guidance, load `prompts/writing_engine.md`.
