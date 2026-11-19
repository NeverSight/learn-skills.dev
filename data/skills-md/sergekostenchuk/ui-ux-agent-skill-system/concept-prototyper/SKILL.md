---
name: concept-prototyper
description: Turn semantic core, business constraints, and user feedback into a site concept and throwaway wireframe prototype before visual design. Use when a public site project needs a pre-design concept, content hierarchy, concept conflicts, or business-idea feedback before Stitch, Pencil, Figma, or code.
---

# Concept Prototyper

This skill creates the concept bridge between SEO/semantic structure and UI design. Its prototype is a feedback artifact, not production code.

## Operating Modes

- `concept`: create `docs/site-concept.md` from semantic core and business logic.
- `wireframe`: create a throwaway HTML/wireframe prototype for feedback.
- `feedback`: structure user feedback into `reports/business-concept-feedback.json`.
- `conflict`: produce `reports/concept-conflicts.md` and route unresolved conflicts to council.

## Required Workflow

1. Read [references/concept-prototype-contract.md](references/concept-prototype-contract.md).
2. Load semantic core, project brief, known business facts, and existing content if available.
3. Build a content hierarchy: primary journey, page map, required facts, trust signals, CTA logic.
4. If prototyping, create a clearly non-production wireframe artifact with sections marked by source reason.
5. Collect or structure feedback and merge it with semantic constraints.
6. If conflicts remain, route to `senior-ui-ux-orchestrator` council mode before design exploration.
7. If conflicts are clear, hand off to `tech-stack-selector`, then design exploration.

## Non-Negotiable

The prototype is disposable. Do not use it as the production implementation base unless the user separately approves a rebuild/refactor plan.

## Handoff Shape

```text
Concept path:
Prototype path:
Feedback path:
Conflicts path:
Decision: clear | council-required
Next skills:
```

## Validation

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/concept-prototyper
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/concept-prototyper
```
