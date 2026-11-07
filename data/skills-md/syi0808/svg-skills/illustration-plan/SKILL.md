---
name: illustration-plan
description: Plan the visual direction and semantic parts of an illustration before production. Use for mood and style exploration, art-direction questions, composition planning, or preparing a scene.json for vector or raster artwork; not SVG authoring, image generation, or faithful image-to-SVG conversion by itself.
---

# Illustration Plan

Turn the brief into a useful visual direction and semantic scene plan. Stop at
planning: do not generate images, author SVG paths, or start production unless the
user requested it. This skill works independently of the production skills.

## Establish what is already decided

Read the brief and any supplied plan or reference. Inspect actual reference
images when available; distinguish inspiration from an image that must be copied
faithfully. For faithful conversion, extract the source's direction rather than
inventing a new one. Preserve existing IDs, approved decisions, and source files.

Record the subject, intended use and display size, aspect ratio, background,
required text or branding, and features that must remain unchanged. Do not turn
a local edit into a new art-direction exercise. Update only affected decisions
when continuing an existing plan.

## Resolve visual direction

Separate mood, rendering language, and material rather than treating style names
as mutually exclusive presets. A calm illustration can also be softly three-
dimensional and glass-like. Read [art-direction.md](references/art-direction.md)
when the brief needs style exploration or feasibility decisions.

Ask only about missing choices that materially change the result. Use plain
language or a few distinct directions when the user does not know design terms;
do not require a questionnaire. Infer low-impact defaults from context and make
important assumptions visible. If the user asks only for options, return those
options and stop rather than silently selecting one and producing artwork.

For SVG output, balance appearance with editability and the intended renderer.
Do not promise photographic fidelity or unsupported effects. The current bundled
SVG tools support gradients and opacity but not SVG filters, including blur.
Explain a consequential approximation or renderer requirement before adopting it.

## Write the semantic plan

When a direction is chosen or production needs a handoff, write `scene.json`
using [scene-model.md](references/scene-model.md). Keep simple plans short.
Use version 2 with `phase: "plan"`, a concise `art_direction.description`, a
canvas, and meaningful element IDs and roles. Record only useful assumptions,
palette hints, and spatial or preservation constraints.

Do not precompute path commands or control points. Leave actual SVG `tag` and
`parent` fields unset: the author adds these and changes the phase to `bound`
after constructing and inspecting the SVG. Planned relationships belong in
plain-language constraints. A plan is not a geometry compiler or executable prompt.

Existing version 1 scenes remain supported bound maps; do not migrate them just
to make a local edit. When deliberately adopting v2 art direction for an existing
SVG, retain its mapping as `bound` and have the production workflow verify it.
Do not demote a bound map to a plan or discard implementation details accidentally.

## Validate and hand off

Resolve `SKILL_DIR` to this skill's directory. Python 3.10+ is sufficient:

```bash
python3 "$SKILL_DIR/scripts/validate_scene.py" scene.json
```

This checks the scene contract without needing an SVG or renderer. It does not
judge design quality or verify actual SVG mappings. Report unresolved assumptions
and summarize the selected direction in the user's language. Return the plan path
when one was written; do not automatically call a production skill. When another
workflow requested planning, hand back the plan and let that workflow continue.
