---
name: oas-program
description: Use when capturing OAS design intent — room requirements, area targets, adjacency rules, circulation rules, or global constraints — before any geometry has been resolved.
---

# OAS Program

## When to use

Use this skill when the user is describing *what they want* rather than *what exists*: target areas, must-be-near rules, circulation preferences, count of rooms, hard limits. Program is the brief; Layout is the answer. If a polygon or wall coordinate is being emitted, you're in `oas-layout` territory, not here.

## Key fields (the document is a flat JSON object, not typed classes)

- `oas_program`, `plan_id`, `title`, `description` — metadata; `plan_id` links program → layout
- `design_goal` — natural-language intent sentence (helps LLM context)
- `global_constraints` — `target_area_m2`, `max_area_m2`, `orientation_preference`, `climate`, `accessibility_level`, etc.
- `rooms[]` — each entry has `id`, `usage`, `desired_area_m2`, `must_have`, `should_have`, `adjacency`, `avoid`
- `adjacency` — uses prefixed keys: `must_touch`, `should_touch`, `avoid_touch`, `must_connect_via`
- `circulation` — `primary_entry` + free-form `rules[]`
- `rationale` — optional reasoning string per room

## Critical rules

1. **Intent only — no resolved geometry.** Program documents must not contain `boundary_polygon`, walls, or coordinates. Resolved geometry lives in OAS-Layout.
2. **`desired_area_m2` accepts `{ "min": X, "max": Y }` or an exact number.** Both are valid per the spec — don't reject a scalar.
3. **Constraint strength is encoded by the field prefix, not a flag.** `must_have`/`must_touch` are hard; `should_have`/`should_touch` are soft; `avoid_touch` is a hard negative. There's no separate `hard: true` field.
4. **Refer to rooms by program `id`, not Layout ids.** Layout ids don't exist yet — adjacency targets are program-level ids like `"corridor"` or `"living_kitchen"`.
5. **Circulation `rules[]` are natural-language strings.** Solvers parse them heuristically; keep them concise and declarative.

## Full schema

See [docs/program.md](../../../docs/program.md) for the complete reference, including constraint composition and adjacency weighting.

## Related skills

- `oas-layout` — the resolved geometry derived from a program
- `oas-core` — for the vocabulary of `usage` values shared with Layout
