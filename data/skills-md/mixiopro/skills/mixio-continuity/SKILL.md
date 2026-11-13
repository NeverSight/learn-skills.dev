---
name: mixio-continuity
description: "Use when a shot plan needs a director-led continuity checklist for scene, shot, and cross-scene/shot continuity, generation risks, and missing coverage before Studio sync."
version: 0.3.0
invoke: /mixio:continuity
---

# Continuity Checklist

Create a written, director-led Continuity Checklist for the local shot plan before Studio sync. The deliverable identifies what each scene and shot must preserve, what can break in image/video generation, and what connecting or alternate coverage is missing for the audience to follow what happened, how it happened, where everyone is, and why the next image follows. Keep the checklist actionable and grounded in the screenplay and available Cast & World references. For the full pre-sync loop, see the [pipeline review cycle](../mixio-pipeline/references/pre-sync-review-cycle.md).

Use the shared [director’s lens](../mixio-pipeline/references/directors-lens.md) to judge continuity in service of audience understanding and dramatic flow, with coverage chosen for the scene’s dramatic purpose. Apply the script-supervisor lens to source, prop, wardrobe, eyeline, and position continuity; use the editor’s lens for coverage and cut logic, and bring in camera, art, costume, prop, sound, or action expertise only when the finding needs it.

The checklist is a written planning artifact, not a pass/fail score. Use it to guide shot-plan corrections, prompt/reference preparation, and post-render evaluation. It does not replace `/mixio:eval`, which checks whether generated media follows the approved plan; evaluation submissions are billable and require confirmation unless already authorized.

**Normal mode is read-and-correct locally.** Do not mutate Studio while drafting an unpresented correction. If the user asks to check persisted shots, present the proposed diff as a checkpoint; chat confirmation or prior authorization for that scope is sufficient to apply it. A Studio approval status is not required. Continue independent checklist work while a choice is open.

## Inputs and grounding

- The approved, director-developed production screenplay selected by `mixio-script-breakdown` (or the supplied breakdown when no screenplay/script is available).
- The current local shot table, including source/inference provenance and the connection to neighboring shots.
- Current Cast & World characters, locations, props, looks/configurations, existing shots, reference metadata and image URLs, plus available scene anchors when scoped and accessible.

Declare the evidence mode:

- **GROUNDED** — a relevant reference image or scene anchor is available. Compare only details it actually shows.
- **TEXT-ONLY** — no relevant image is available. Review source and stated direction; do not claim an anchor comparison or report “zero anchor mismatches.”

Missing sheets and anchors are readiness gaps. They do not block writing the checklist or local planning.

The checklist is written before Studio sync. If a later optional `/mixio:blocking` proxy review reveals a staging issue after sync, update the affected local plan and checklist items, present the revised exact diff, and return through the pipeline's Step 03 confirmation and readback before planning. Do not treat proxy review as permission to mutate synced shots directly.

## Checklist construction

Build the checklist in story order. For each concern, include its evidence, scope, why it matters to the audience, the likely image/video generation failure, and the missing shot or corrective direction. Do not turn unknowns into facts.

### 1. Story beats and scene coverage

Map every screenplay beat and required dialogue moment to one or more planned shots. List absent establishing/re-establishing, entrance/exit, action-cause, prop insert, reveal, reaction/listener, reverse-angle, transition, or other connective shots when the scene needs them. Mark added coverage as `INFERRED`. Flag missed source beats, redundant candidates, or an inference that changes story facts.

### 2. Character, performance, and prop state

For each relevant shot, track character presence/count, identity, position, facing, posture, wardrobe/look, emotion/performance, condition, voice, and consequential props. Record state at entry and exit. Check image-generation risks such as wrong or duplicated faces, extra/missing people, wrong look, pose or prop ownership; check video risks such as identity drift, sudden state changes, and inconsistent action. A change must have a visible cause, be named as an intentional off-screen event, or remain an `OPEN DECISION`.

Check prop ownership shot by shot. A pickup, put-down, handoff, reveal, disappearance, arrival, or exit needs a legible beat. Fix the shot where the state changes, then re-check dependent shots.

### 3. Scene geography, camera POV, and staging

Check the location configuration, room/table/street axis, entrances/exits, blocking, screen direction, eyelines, and camera POV within a scene and across scene transitions. Identify the controlling location/seat/overhead/map reference and which attributes it owns. Check frame visibility and subject counts for POV shots (including who must remain off-camera). Ask whether the subject moved or the camera moved before calling a facing change a continuity error. If no image grounds the layout, mark the assumption as inferred or as a readiness gap.

### 4. Shot-to-shot flow, image/video continuity, and rhythm

For each cut and cross-scene handoff, state the connection: continuing action, eyeline, match, reveal, contrast, sound bridge, transition, or intentional time/space jump. Check screen direction, axis, eyeline, camera side/height, lens/framing, lighting/time, screen or document content, action state, performance, sound/dialogue/voice, and duration as relevant. For video, state start/end pose or prop state, action cause, movement path, and what must stay stable through frames. For `MULTI_CUT` shots, cover every authored cut and verify cut durations sum to the shot duration within the canonical tolerance. Add coverage only when the screenplay and audience need it.

### 5. Cast & World and reference authority

For each checklist item, identify the controlling character/prop/location record, selected look/configuration/view, anchor, or exact media reference. State what each reference controls and what it does not prove; do not let a room image override character identity or an unapproved alternate look override the selected one. Record missing references, images, structured details, voice IDs, or anchors as readiness gaps, separate from continuity findings. Do not create references, upload media, generate assets, or change bindings while creating the checklist.

### 6. Editorial coverage and generated-material reserve

Treat the stated runtime as the intended post-production duration. The minimum planned generated video duration is 1.2× that target: a 90-minute final needs at least 108 minutes of generated clips; a 1-minute final needs at least 72 seconds. Count every planned alternate angle, emotional take, reaction/listener clip, insert, transition, and other candidate video output because each creates an editorial option. Do not count still keyframes as video seconds. Give every extra a purpose and relationship to the shot it can replace or extend. Report final target and total planned generated-video duration separately; plan more than 1.2× when the script or editorial needs warrant it. Flag a shortfall as `COVERAGE`, explain the trade-off at the Step 03 checkpoint, and continue on the user's direction rather than treating it as a pipeline-wide stop.

## Checklist artifact and local corrections

Use the [checklist template](references/checklist-template.md) for concrete item rows, reference authority, prompt/coverage actions, and evidence/status. Keep planned constraints distinct from observed rendered compliance. Write the deliverable in this order:

1. Evidence mode, episode/scene/shot scope, and the reference sources reviewed.
2. The continuity rules that govern this sequence (cast, looks, props, geography, POV, time/light, sound/dialogue).
3. A scene-level checklist for invariants, entrances/exits, location geography, and scene handoffs.
4. A shot-level checklist with the expected start/end state, camera/frame constraints, reference owner, and applicable image/video generation risks.
5. A cross-shot/cross-scene checklist for axis, eyelines, action/prop state, performance, sound, and transitions.
6. A coverage-gap list naming missing shots/clips (including reactions, listening shots, inserts, reverses, entrances/exits, and bridges) with dramatic/editorial purpose.
7. The 1.2× generated-video-duration calculation, alternates/coverage counted, `OPEN DECISION`s, and reference-readiness gaps.
8. Local correction log and the rechecked checklist, with applicable item IDs carried into prompt preparation and supported evaluation context.

Use the [editorial coverage ledger](../mixio-pipeline/references/editorial-coverage.md) for duration counting and per-output purpose. Refresh affected checklist items after screenplay, coverage, blocking, look/reference, or generation-route changes. Rebuild the checklist from current source and confirmed Studio state after context loss; a previous planning check is not proof of rendered compliance.

Use these categories: `COVERAGE`, `CAUSE`, `PROP`, `PRESENCE`, `BLOCKING`, `FACING`, `POSTURE`, `WARDROBE`, `AXIS`, `FLOW`, `CAMERA`, `AUDIO`, `ANCHOR`, `SOURCE`, and `READINESS`.

Apply grounded local corrections, then update the affected checklist items and shot rows. Keep unresolved concerns visible rather than reducing the checklist to a clean/failed verdict. Never silently “fix” an open story decision: present alternatives. If the user says proceed without choosing, keep the decision open and continue with unaffected work. A readiness gap may remain visible in the plan; explain its likely effect and let the user decide whether to proceed. Continue when the user accepts the risk and the live schema/project policy allow it.

## If checking persisted shots

Read current records first and identify each by confirmed Studio element ID. Return the proposed before/after changes and any relation updates as a checkpoint. On the user's chat confirmation—or existing authorization covering that diff—write through the appropriate existing primitive and read the records back. Do not require a separate Studio approval state. If the user asks for an audit only, report the diff without writing.

## Workflow

```text
read source + local shot plan + available images
  → build scene, shot, cross-scene, reference, and coverage checklists
  → name evidence + generation risks + missing coverage → apply grounded local corrections
  → update checklist and generated-material reserve → return checklist with the Studio diff for review
```
