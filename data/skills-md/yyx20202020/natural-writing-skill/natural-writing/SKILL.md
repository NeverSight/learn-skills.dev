---
name: natural-writing
description: Rewrite, draft, or review Chinese and English prose so it sounds natural, specific, and appropriate to its real audience while preserving facts and matching an author's voice. Use for 去AI味、人性化改写、润色、降低模板感、文风模仿、AI writing pattern diagnosis, final-pass editing, or the humanization stage of a long-form writing workflow. Supports diagnostic-only, light in-place editing, bounded cleanup, structural rewriting, and voice calibration.
---

# Natural Writing

Turn generic model prose into situated human expression. Preserve truth before improving style.

## Route the task

Determine four controls before editing:

1. `language`: Chinese, English, or mixed.
2. `task`: diagnose, rewrite, draft, or final-pass.
3. `intensity`: minimal, standard, or aggressive.
4. `scope`: in-place, bounded, or structural.

Infer them from the request. Use `standard + bounded` when the user gives no preference. Use `minimal + in-place` for legal, technical, academic, quoted, or approval-sensitive text. Read [references/routing.md](references/routing.md) when routing is ambiguous.

## Execute the workflow

### 1. Establish the writing situation

Identify the speaker, audience, purpose, channel, and desired reader action. Do not add personality that the situation does not support.

### 2. Protect content

Before rewriting, mark facts and exact strings that must survive: names, dates, numbers, versions, commands, code, URLs, paths, quotations, evidence, terminology, and responsibility attribution.

Read [references/protected-content.md](references/protected-content.md). For file-based work, run:

```powershell
python scripts/check_protected_spans.py extract --input original.txt --output protected.json
```

### 3. Diagnose patterns

Locate only patterns that materially harm the requested text. Do not turn a phrase list into a blind ban list.

- For Chinese or mixed Chinese-dominant text, read [references/chinese-writing.md](references/chinese-writing.md).
- For English or mixed English-dominant text, read [references/english-writing.md](references/english-writing.md).
- When the user asks only for analysis, load [prompts/diagnose.md](prompts/diagnose.md) and stop after the diagnostic report.

### 4. Calibrate voice when evidence exists

If the user supplies writing samples, read [references/voice-calibration.md](references/voice-calibration.md) and [prompts/calibrate-voice.md](prompts/calibrate-voice.md). Match observable habits, not the author's identity or private traits.

If no samples exist, preserve the draft's strongest genuine traits and use a neutral, context-appropriate voice.

### 5. Rewrite

Load [prompts/rewrite.md](prompts/rewrite.md). Apply the chosen language rules, intensity, and scope.

Prefer these transformations:

- Replace abstraction with actors, actions, objects, evidence, and consequences.
- Remove announcements that merely introduce the next sentence.
- Break repeated sentence frames and mechanical paragraph symmetry.
- Keep uncertainty where the evidence is uncertain.
- Preserve useful structure in reference, technical, and operational writing.
- Never invent anecdotes, emotions, quotations, sources, or firsthand experience.

For a full article pipeline rather than a final edit, read [references/long-form-workflow.md](references/long-form-workflow.md) and [prompts/long-form-final-pass.md](prompts/long-form-final-pass.md).

### 6. Verify

Read [references/quality-gates.md](references/quality-gates.md). Check meaning, facts, protected strings, scene fit, rhythm, and residual template language.

For file-based work, run:

```powershell
python scripts/check_protected_spans.py compare --before original.txt --after rewrite.txt
```

If a protected span is missing, restore it or explicitly explain why the user must decide. Never hide a factual change inside stylistic editing.

## Deliver

Default to the rewritten text only. Add a short change note when the user requests explanation, the edit is aggressive, or a factual/structural tradeoff needs approval.

For diagnostic-only tasks, return:

1. The highest-impact patterns.
2. Evidence from the text.
3. A recommended intensity and scope.
4. A short sample revision, unless the user forbids rewriting.

Do not claim that a rewrite is “undetectable” or guaranteed to pass an AI detector. Optimize for truthful, useful writing and human review.
