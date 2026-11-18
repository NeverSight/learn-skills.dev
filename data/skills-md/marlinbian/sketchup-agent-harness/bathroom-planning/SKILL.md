---
name: bathroom-planning
description: Plan and execute the supported bathroom vertical slice with structured project truth, validation, and bridge operations.
---

# Bathroom Planning Skill

## Purpose

Plan and optionally execute the first supported bathroom vertical slice.

## Tool Selection

Use `plan_bathroom` when:

- SketchUp is not running.
- The user asks to preview, validate, or create a bathroom plan.
- You need a structured `design_model`, `design_rules`, validation report, and
  bridge operation trace.
- The project has `design_rules.json` preferences that should influence the
  plan.

Use `execute_bathroom_plan` when:

- The user explicitly wants the plan sent to SketchUp.
- The SketchUp Ruby bridge is running.
- The local socket `/tmp/su_bridge.sock` is expected to be available.

If the user asks to execute and the bridge is not available, call
`launch_sketchup_bridge` first. Execute only when it returns `socket_ready:
true`. If launch fails, report the structured blockers and keep the generated
plan/project files available.

## Default Slice

The default supported slice is:

- room size: 2000 mm x 1800 mm
- ceiling height: 2400 mm
- one 700 mm bathroom door
- one floor-mounted toilet
- one 600 mm vanity or sink
- one wall mirror
- one basic ceiling light
- clearance validation

## Result Handling

After a tool call, report:

- validation status
- failed checks and required distances
- where project files were written, if any
- execution status and bridge errors, if any
- whether SketchUp entity IDs were synced back to `design_model.json`

Keep the response grounded in returned JSON. Do not invent additional geometry
that is not present in `design_model` or `bridge_operations`.

When `project_path` is provided, project-local `design_rules.json` overrides the
built-in seed rules. Report failed checks from `validation_report`; do not
silently relax them.

When `execute_bathroom_plan` succeeds with `project_path`, use
`execution_sync` to report which generated space walls, component instances,
and lighting instances received live SketchUp `entity_id` values in
`design_model.json`.

## Prompt Examples

English:

```text
Plan a 2m x 1.8m bathroom with a toilet, sink, door, mirror, basic light, and
clearance check.
```

Chinese:

```text
规划一个 2 米 x 1.8 米的卫生间，包含马桶、洗手台、门、镜子和基础照明，并检查通行距离。
```

## Guardrails

- Current clearances are ergonomic seed rules, not legal code compliance.
- Do not claim that generated placeholder boxes are final production models.
- If execution fails because SketchUp is unavailable, keep the plan and explain
  that the bridge must be started before execution.
