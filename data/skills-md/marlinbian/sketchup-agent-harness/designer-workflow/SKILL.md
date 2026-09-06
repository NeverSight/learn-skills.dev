---
name: designer-workflow
description: Guide designers through project setup, planning, placement, validation, execution, versioning, and visual review workflows.
---

# Designer Workflow Skill

## Purpose

Guide the designer through the currently implemented SketchUp Agent Harness
workflow. Keep `design_model.json` as the source of truth and use SketchUp as
the executed view.

## Current Supported Flow

### 1. Confirm Project Workspace

The designer should work inside a design project directory, not the source
repository.

Expected files:

- `design_model.json`
- `design_rules.json`
- `assets.lock.json`
- `.mcp.json`
- `snapshots/`
- `snapshots/manifest.json`

Use `get_project_state` to read the current structured model, effective design
rules, asset-lock summary, visual feedback summary, and saved version summary. Use
its execution summary to see whether SketchUp entity IDs have been synced. Use
`list_project_components` to inspect placed component-like instances, and
`validate_design_project` before reporting that the project files are internally
consistent.

If these files are missing, tell the user to initialize the project with:

```bash
sketchup-agent init <project-path> --template bathroom
```

If the user asks whether setup is healthy, guide them to run:

```bash
sketchup-agent doctor <project-path> --sketchup-version 2024
```

If the user asks to inspect current files without opening an agent tool call,
guide them to run:

```bash
sketchup-agent state <project-path>
```

During source development, the equivalent command is:

```bash
cd mcp_server
uv run --extra dev sketchup-agent init <project-path> --template bathroom
```

### 2. Plan Before Executing

For the first vertical slice, prefer `plan_bathroom` before mutation. It returns:

- `design_model`
- `design_rules`
- `validation_report`
- `bridge_operations`

Use this when the user asks to create or review a small bathroom, especially if
SketchUp is not open yet. If the project already has `design_rules.json`, the
planner should use it instead of silently reverting to built-in defaults.

Use `get_design_rules`, `set_design_clearance`, `set_fixture_dimension`, or
`set_design_preference` when the designer changes a project preference before
planning.

### 3. Place Components Into Project Truth

Use `search_components` or `get_component_manifest` before placing reusable
objects. If the designer gives exact coordinates, call `add_component_instance`.
If the designer gives a supported relationship to a rectangular space, call
`add_component_instance_semantic`. If the designer gives a supported
relationship to another component instance, call `add_component_instance_relative`.

Supported semantic placement relations are:

- `centered_in_space`
- `against_wall` with `wall_side` as `north`, `south`, `east`, or `west`
- `above` a reference component
- `beside` a reference component with `side` as `north`, `south`, `east`, or
  `west`

After component placement, use `plan_project_execution` to confirm the updated
`design_model.json` can be converted into a bridge trace. Use
`execute_project_model` only when the designer wants SketchUp updated.

Use `validate_project_layout` after component placement or when the designer
asks to check the layout. Treat failures as blockers for SketchUp execution
unless the designer explicitly wants to keep a known conflict.

### 4. Import Existing Source Material

When the designer provides a DWG, DXF, PDF, floor-plan image, scanned plan, or
photo, use `import_floorplan_to_model` to generate editable working truth
directly in `design_model.json`.

Import is autonomous-first. Do not ask the designer to confirm every wall, door,
window, or low-level numeric candidate before generating the first model. If the
designer gives known dimensions, pass them as `width` and `depth` in
millimeters. If dimensions are not available, let the tool estimate scale and
report quality flags.

If the import creates source-specific knowledge that should guide later turns
in the same project, create or update a project/session dynamic runtime skill in
the active design project, such as
`.agents/skills/import-source-<import_id>/SKILL.md` and the corresponding
Claude skill location when supported. Use it for local symbol legends, known
designer corrections, project-specific naming, and import-source assumptions.
Follow the `project-runtime-memory` skill for dynamic skill scope, format, and
guardrails. Do not add those source-specific facts to shipped product runtime
skills. `design_model.json` remains the canonical editable truth.

After import, call `plan_project_execution` to verify that imported walls and
hosted openings produce `create_wall_with_openings` bridge operations. Use
`execute_project_model(clean_before_execute=True, clean_scope="all")` only when
the designer wants SketchUp updated. Normal import execution should not leave
raw source images, template entities, or stale imported geometry in the SketchUp
scene.

When the designer later says the imported model differs from the source, call
`review_model_against_import_source`, then choose the narrowest repair tool. Use
`normalize_imported_wall_alignment` when a near-straight exterior wall is offset
by a wall-thickness-sized step. Use `rescale_imported_model` when the correction
is a better overall width, depth, or scale factor. Use
`repair_imported_corner_notch` when the source has an exterior stepped corner or
corner notch missing from the generated model. Use
`review_imported_boundary_coverage` and `repair_imported_boundary_coverage` when
the imported footprint contains a room edge but the explicit wall list missed a
long wall segment or a short gap has source-backed wall-continuity evidence.
Use `review_imported_wall_space_consistency` and
`repair_imported_shell_overreach` when explicit imported walls enclose an extra
area that no imported room or balcony footprint claims. Use
`repair_imported_region` for other specific corrections.

### 5. Execute Only When the User Wants SketchUp Updated

Use `execute_bathroom_plan` when the user wants the model updated in SketchUp and
the Ruby bridge is running.

If the bridge is not running, use `launch_sketchup_bridge` before execution
rather than only telling the designer to open SketchUp. A successful launch
returns `socket_ready: true`. If it returns `socket_ready: false`, report the
`possible_blockers` field and keep the structured plan/project truth unchanged.

For an existing project that already has `design_model.json`, prefer
`plan_project_execution` before whole-project synchronization. It derives the
bridge trace from current project truth. If it returns skipped instances, report
them and fix the missing space bounds, component references, or registry entries
before executing.

Use `execute_project_model` when the designer wants the current project truth
sent to SketchUp. On success, use `execution_sync` to report which generated
space walls, component instances, and lighting instances received SketchUp
`entity_id` values.

Use `clean_before_execute=True` when the intended result is a clean replay of
current project truth, especially after import, re-import, repair, or rescale.
Use `clean_scope="all"` for import clean replay when raw source images or
SketchUp template entities may be present.
Do not use clean replay when the designer is intentionally preserving unrelated
manual SketchUp geometry on managed layers.

Before calling it, confirm the bridge is available at `/tmp/su_bridge.sock`.
If execution fails because SketchUp is not running, retry the startup path once
with `launch_sketchup_bridge`; then report any environment blockers and keep the
structured plan available.

### 6. Report Structured Results

After planning or execution, summarize:

- whether `validation_report.valid` is true
- failed clearance checks, if any
- files written, if `project_path` was provided
- execution status, if `execute_bathroom_plan` was used
- skipped instances, if `plan_project_execution` refused to convert part of the
  project truth
- layout validation failures, if `validate_project_layout` or
  `validate_design_project` found containment, overlap, or front-clearance
  issues
- execution sync details, if `execute_project_model` was used
- import summary details, if `import_floorplan_to_model`,
  `rescale_imported_model`, `repair_imported_shell_overreach`, or
  `repair_imported_region` was used

Do not replace structured output with only prose. The design model remains the
canonical state.

### 7. Save Reviewable Versions

Use `save_project_version` when the designer asks to save a milestone, compare
alternatives later, or preserve a rollback point. Use `list_project_versions`
when the designer asks what versions exist. Use `compare_project_versions` when
the designer asks how two drafts differ or whether the current project changed
from a saved milestone. Use `restore_project_version` only after the designer
explicitly asks to restore a version, because it overwrites current project
truth files.

### 8. Capture Visual Review Artifacts

Use `capture_project_snapshot` when the user asks for a screenshot or visual
review and a project path is available. Snapshot provenance is recorded in
`snapshots/manifest.json`.

Before asking a rendering or image generation tool to produce a derived visual,
use `prepare_render_brief` to produce a prompt from `design_model.json`,
effective project context, and the source snapshot. The brief must preserve the
structured layout and should be passed through to `record_render_artifact` after
the renderer returns an output path or URL.

When a generated or external rendered image is produced from a snapshot, call
`record_render_artifact` with the output path or URL, renderer tool/model,
prompt, and source snapshot information. Rendered images remain advisory
artifacts; they do not replace `design_model.json`.

If the user wants to act on a screenshot or rendered image, call
`record_visual_feedback` first with proposed structured actions. Only mutate
`design_model.json`, components, rules, materials, or styles after the visual
feedback has been converted into explicit actions.

Use `get_project_state` or `list_visual_feedback` before applying pending visual
actions. After an accepted action has been applied through structured tools, call
`update_visual_feedback_action_status` with `status="applied"` so the manifest
does not become a stale suggestion log.

Use `apply_visual_feedback_action` only for supported structured actions:
component, lighting, material, style, rule, and note. Do not use it to apply
geometry changes from pixels; use dedicated geometry tools instead.

## Supported User Prompts

English examples:

```text
Plan a 2m x 1.8m bathroom with a toilet, sink, door, mirror, basic light, and
clearance check.
```

```text
Execute the bathroom plan in SketchUp.
```

```text
Sync the current design_model.json to SketchUp.
```

```text
Put the vanity against the north wall of bathroom_001.
```

```text
Put the mirror above vanity_001 with a 150 mm gap.
```

```text
Import this PDF floor plan and generate an editable model.
```

Chinese examples:

```text
帮我规划一个 2 米 x 1.8 米的卫生间，包含马桶、洗手台、门、镜子和基础照明，并检查通行距离。
```

```text
把这个卫生间方案同步到 SketchUp。
```

```text
把当前 design_model.json 同步到 SketchUp。
```

```text
把洗手台靠 bathroom_001 的北墙放。
```

```text
把镜子放在 vanity_001 上方，留 150 mm 间距。
```

```text
导入这张户型图，生成可编辑模型。
```

## Guardrails

- Do not promise full-home automatic design yet.
- Do not claim jurisdictional code compliance. Current rules are ergonomic seed
  defaults.
- Do not use image rendering as source of truth.
- Treat snapshots as advisory artifacts.
- Do not directly apply visual pixels as geometry; convert accepted visual
  feedback into structured actions first.
- Do not write maintainer workflow instructions into designer project files.
