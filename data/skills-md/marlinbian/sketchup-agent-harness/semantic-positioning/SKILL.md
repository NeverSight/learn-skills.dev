---
name: semantic-positioning
description: Resolve supported space-relative and component-relative placement language into project-backed coordinates.
---

# Semantic Positioning Skill

## Purpose

Convert designer language such as "against the north wall" or "above the
vanity" into millimeter coordinates before calling placement tools.

## Inputs

Use the best available source, in this order:

1. `design_model.json` from the active project.
2. Registry metadata from `search_components` or `get_component_manifest`.
3. Scene state from `get_scene_info`.
4. Explicit dimensions supplied by the user.

If none of these sources provide enough geometry, ask one clarification question
or use a clearly labeled placeholder.

## Project-Backed Relationships

| Relationship | Calculation Basis |
| --- | --- |
| `centered_in_space` | Center of rectangular `spaces.<space_id>.bounds` |
| `against_wall` | Rectangular space side, component dimensions, wall side |
| `above` | Reference component bounds and optional wall provenance |
| `beside` | Reference component bounds, side, and gap |

Use the MCP tool `add_component_instance_semantic` for these relationships when
a project path and rectangular space exist: `centered_in_space` and
`against_wall`. It writes `design_model.json`, refreshes `assets.lock.json`,
records `relative_to=<space_id>`, and stores the semantic placement provenance
under the instance source.

Use `add_component_instance_relative` for component-to-component relationships:
`above` and `beside`. If the reference component was placed against a wall, the
tool reuses that wall side to keep wall-mounted components such as mirrors on
the same wall plane.

Other relationships such as `in_front_of` or `aligned_with` are not yet generic
project-backed tools. Resolve them manually only when dimensions and anchors are
explicit, and report the assumption.

## Workflow

1. Identify the target object and reference object or space.
2. Read dimensions, anchors, and clearances.
3. Convert the relationship into absolute coordinates.
4. Check fit using project space bounds, `design_rules.json`, and registry data.
5. Call `add_component_instance_semantic` for supported space-relative
   placement, or `add_component_instance_relative` for supported
   component-relative placement.
6. Use `plan_project_execution` or `execute_project_model` if the designer wants
   SketchUp updated.
7. Report assumptions and validation warnings.

## Example

```python
search_components(
    query="vanity",
    category="fixture",
    project_path="<project-path>",
    limit=5
)
add_component_instance_semantic(
    project_path="<project-path>",
    component_id="vanity_wall_600",
    space_id="bathroom_001",
    relation="against_wall",
    wall_side="north"
)
```

```python
add_component_instance_relative(
    project_path="<project-path>",
    component_id="mirror_wall_500",
    reference_instance_id="vanity_001",
    relation="above",
    gap=150
)
```

For a Chinese user prompt such as "把洗手台靠北墙放", preserve the user's
intent, search with the natural term first, then use the same English tool
contract:

```python
search_components(query="洗手台", category="fixture", project_path="<project-path>")
add_component_instance_semantic(
    project_path="<project-path>",
    component_id="vanity_wall_600",
    space_id="bathroom_001",
    relation="against_wall",
    wall_side="north"
)
```

## Guardrails

- Do not rely on semantic words without checking actual dimensions.
- Do not pretend semantic placement is collision-free; the current tool checks
  space bounds, not every clearance or collision.
- Do not bypass `design_model.json` for project-backed placement.
- Prefer `plan_bathroom` for the supported bathroom slice.
