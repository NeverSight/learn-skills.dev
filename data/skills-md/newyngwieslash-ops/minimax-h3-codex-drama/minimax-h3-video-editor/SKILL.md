---
name: minimax-h3-video-editor
description: Create, enhance, or diagnose precise MiniMax H3 prompts for editing an existing video while preserving everything outside requested changes. Use for subject or object replacement, removal, wardrobe changes, background replacement, relighting, localized VFX, text or signage changes, dialogue or voice replacement, performance adjustment, and multi-element edits that need explicit change-and-preserve pairs and copy-ready prompts.
---

# MiniMax H3 Video Editor

Describe localized changes to a source video while locking every unaffected property. Stay prompt-only and never submit a generation job.

## Confirm this workflow

Use this skill when at least one existing video is the source to modify. Route execution through reference-conditioned video generation; label the source as `Video 1` unless the user's existing ordering differs. Additional images, videos, or audio may supply replacement identity, design, environment, motion, or voice.

Recommend 5–15 seconds, `768P` for iteration or `2K` for a final pass when supported, and a fixed or `adaptive` aspect ratio. Preserve the source duration or aspect when that is important to the edit, and let the executor validate the installed workflow.

## Write change-and-preserve pairs

Create a short edit ledger before the prompt. For each operation, pair:

- **Change**: exact target, location or time, operation, and replacement source.
- **Preserve**: surrounding subjects, action, timing, framing, lighting, shadows, reflections, geometry, audio, text, or effects that must remain stable.

Examples of precise operations include replace, remove, add, relight, recolor, rewrite, retime, and overlay. Avoid broad restyling language unless broad restyling is the requested edit.

## Build the prompt

1. Identify the source video and all replacement references by modality and order.
2. State the requested edits in temporal or spatial order.
3. Bind each replacement to a source asset where applicable.
4. Explain integration: matching perspective, motion, occlusion, lighting, shadows, reflections, lip sync, or performance.
5. State the global invariant: everything not explicitly listed remains unchanged.
6. Add targeted failure constraints such as no source-camera drift, no identity change, no extra objects, no altered timing, or no compositing seams.

For dialogue replacement, provide the exact new line and identify the voice reference. Ask for subtle mouth, breath, expression, and gesture adaptation without changing unrelated performance. For relighting or background replacement, require subject light, shadow, reflection, and atmospheric integration.

## Enhance or diagnose

When enhancing, preserve the user's edit list and source ordering. Turn ambiguous nouns such as “that sign” into a spatial or temporal identifier when evidence permits.

When diagnosing, test for:

- edits with no preservation partner;
- unclear target instances when the object appears multiple times;
- a replacement asset with no role assignment;
- lighting, shadow, reflection, or occlusion mismatches;
- dialogue changes without lip-sync and performance adaptation;
- too many unrelated edits in one pass;
- global style directions that regenerate the entire shot.

Recommend splitting into passes only when edits compete or accurate targeting becomes implausible.

## Use the template and examples

Read [references/template-and-examples.md](references/template-and-examples.md) for the canonical fill-in template and two representative examples. Adapt their edit precision, not their subject matter.

## Return

Provide:

- an edit ledger and asset mapping;
- suggested duration, aspect ratio, resolution, and workflow route;
- material assumptions, if any;
- one copy-ready prompt;
- 2–4 preservation checks.

Do not return an API payload or submit a job.
