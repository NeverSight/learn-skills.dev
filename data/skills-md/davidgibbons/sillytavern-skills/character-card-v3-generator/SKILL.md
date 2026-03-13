---
name: character-card-v3-generator
description: Generate, refine, and validate Character Card V3 cards and lorebooks. Use when creating new characters from a concept, converting or upgrading existing cards to CCv3, improving weak character behavior consistency, or building lorebook entries that steer scenario outcomes while staying token-efficient.
---

# Character Card V3 Generator

## Overview

Generate Character Card V3 JSON outputs that are spec-compliant and high quality for roleplay. Build cards and lorebooks with clear behavior anchors, practical activation logic, and predictable in-chat performance.

## Workflow

1. Clarify the brief.
- Capture genre, tone, hard boundaries, relationship to `{{user}}`, chat style (short/long), and desired behavior constraints.
- Ask whether output should be minimal, standard, or advanced template.
- If the user does not choose, default to `standard`.

2. Build the CCv3 skeleton.
- For new cards, start from `assets/templates/` and fill mandatory fields first.
- For conversions/upgrades, load the existing card first and do a minimal-diff transform to CCv3 (preserve existing intent/content unless it conflicts with CCv3 structure).
- Apply normalization patterns from `references/popular-card-patterns.md` (field rebalance, trigger cleanup, and lore entry splitting) when card structure is uneven.
- Keep schema-critical fields valid before adding style details.
- Use `references/spec-v3-field-map.md` for required field behavior.

3. Write high-signal character content.
- Apply `references/character-writing-guidelines.md`.
- Prioritize stable identity, behavioral constraints, and concrete examples over verbose prose.
- Design `system_prompt` and `post_history_instructions` as primary control surfaces using `references/spec-v3-field-map.md`.
- Keep persistent contract rules in `system_prompt`; keep final-turn steering/enforcement in `post_history_instructions`.

4. Design lorebook strategy.
- Use `references/lorebook-guidelines.md` to choose entry keys, activation depth, token budget, and insertion ordering.
- Keep one concept per entry and prefer iterative additions from observed failures.

5. Add card-scoped regex scripts when needed (SillyTavern-specific).
- Use `references/regex-scoped-scripts.md` for `data.extensions.regex_scripts` structure and examples.
- Use only for deterministic text transforms that should be tied to this character card.
- Keep regex scripts minimal and test them on sample dialogue before shipping.

6. Validate output.
- Run `scripts/validate_card.py <path-to-card.json>` for structural checks.
- Manually spot-check lore triggers against likely user phrasing.
- Run a quality pass with `references/reviewing-cards.md`.

7. Return deliverables.
- Return final CCv3 JSON.
- Include a short note with major design choices and tradeoffs as a separate section outside the JSON block.

## Output Rules

- Always output valid JSON, never pseudo-JSON.
- When also providing commentary, keep it outside the JSON artifact (for example: JSON in one fenced block, rationale in a separate prose section).
- Keep `spec` as `"chara_card_v3"` and `spec_version` as `"3.0"` unless explicitly requested otherwise.
- Use `extensions` for non-standard app data; avoid adding random top-level fields.
- Keep lorebook entries concise and actionable.
- Distinguish strict spec constraints from model-behavior heuristics.
- When using hidden-state patterns (such as XML comments), include leak-risk caveats and recommend chat-level testing.

## Resources

- `references/spec-v3-field-map.md`
  - Required/optional CCv3 fields and key constraints.
- `references/image-and-asset-formats.md`
  - PNG/APNG/JSON/CHARX handling and practical image asset compatibility rules.
- `references/character-writing-guidelines.md`
  - Practical character-writing quality rubric.
- `references/lorebook-guidelines.md`
  - Lorebook entry design, trigger quality, and token strategy.
- `references/multi-character-and-scenarios.md`
  - Patterns for ensemble casts, occasional NPCs, and structured world-event logic.
- `references/popular-card-patterns.md`
  - Generalized quality patterns and normalization strategies derived from high-usage cards.
- `references/source-notes.md`
  - One-time harvested heuristics from linked community discussions.
- `references/reviewing-cards.md`
  - Quality-review checklist and scoring rubric for release readiness.
- `references/regex-scoped-scripts.md`
  - SillyTavern card-scoped regex schema, examples, and safety practices.
- `references/format-options.md`
  - Comparison of Prose, Attributes, AliChat, JED/JED+, Plaintext, and W++ with use-case guidance.
- `examples/format-comparison.md`
  - Same character concept shown in each major format for quick side-by-side learning.
- `examples/command-orchestration-pattern.md`
  - Generic template for command-triggered lorebook actions with weighted outcomes and ephemeral cleanup.
- `examples/secret-reveal-pattern.md`
  - Public/secret split with delayed reveals, belief-vs-fact layering, and cadence control.
- `assets/templates/minimal-card-v3.json`
  - Lean starter for quick generation.
- `assets/templates/standard-card-v3.json`
  - Balanced starter with lorebook included.
- `assets/templates/advanced-card-v3.json`
  - Extended starter using multilingual notes and assets.
- `scripts/validate_card.py`
  - Lightweight structure validator for card JSON.

## Notes

- Community tactics can vary by frontend and model family. Apply heuristics, then adapt after test chats.
- Some linked Reddit threads may be inaccessible from restricted environments; if inaccessible, keep guidance conservative and prefer spec-backed behavior.
