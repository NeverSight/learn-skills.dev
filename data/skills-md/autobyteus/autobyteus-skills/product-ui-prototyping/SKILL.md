---
name: product-ui-prototyping
description: "Design and validate product UI behavior as visual state prototypes before coding. Use when tasks ask how screens should change after user actions (click, tap, submit), when non-developers need to review web/iOS/Android UX flows, or when teams need interaction-state assets and acceptance checks for implementation."
---

# Product UI Prototyping

## Overview

Turn product ideas into testable UI behavior using generated and edited screen images. Produce state-by-state visuals, click-through transition logic, and per-platform viewers that teams can navigate end-to-end before implementation.

## Prototype Folder Convention (Project-Local)

- For each prototype effort, create/use one folder under the current project's `ui-prototypes/` directory:
  - `ui-prototypes/<prototype-name>/`
- Keep all prototype artifacts in that folder so each prototype remains self-contained.
- Use clear kebab-case for `<prototype-name>`.
- Keep image assets separated by platform:
  - `ui-prototypes/<prototype-name>/images/web/<flow>/...`
  - `ui-prototypes/<prototype-name>/images/ios/<flow>/...`
  - `ui-prototypes/<prototype-name>/images/android/<flow>/...`
- Keep flow maps separated by platform and flow:
  - `ui-prototypes/<prototype-name>/flow-maps/<platform>/<flow>.json`
- Keep a manifest that maps each image to its exact generation/edit prompt:
  - `ui-prototypes/<prototype-name>/image-prompt-manifest.md`
  - `ui-prototypes/<prototype-name>/prompts/<platform>/<flow>/<screen>-<state>.md`
- If the user specifies a different location, follow the user-specified path.

## Input Strategy (Flexible)

- If `ui-prototypes/<prototype-name>/experience-story.md` exists, use it as upstream source for screens, actions, and transitions.
- If it does not exist, proceed directly and define screens/transitions in this workflow.
- Do not block prototyping on any specific upstream file.

## Workflow

### Audible Notifications (Speak Tool, Required)

- Use the `Speak` tool for key stage-boundary status so the user does not need to watch the screen continuously.
- Hard rule: speak at both stage start and stage completion for each key stage below (no selective skipping).
- Required speak stages:
  - workflow kickoff (`prototype target acknowledged`, `next stage`),
  - transition model stage (`started`, then `ui-behavior-test-matrix.md` drafted/updated),
  - baseline screen stage for each platform+flow (`started`, then baseline set written),
  - interaction-state stage for each platform+flow (`started`, then state set written),
  - manifest synchronization stage (`started`, then `image-prompt-manifest.md` updated and consistent),
  - click-through bundle stage (`started`, then flow-map + viewer written),
  - viewer smoke test stage (`started`, then `Pass`/`Fail` result),
  - final handoff stage (`started`, then package-ready completion).
- Speak trigger policy:
  - do not skip required stage-boundary speak events,
  - for completion events, speak only after the milestone is durably completed (files written + relevant checks known),
  - do not speak for partial drafts or intermediate prompt iterations between required stage-boundary events,
  - batch close-together milestone updates into one short message.
- Keep each spoken message short (1-2 sentences), status-first, with one clear next step.
- If the `Speak` tool fails or is unavailable, continue workflow and provide the same update in text.
- Do not speak secrets, tokens, or full sensitive payloads.

### Tool Execution Discipline

- Execute image tool calls strictly one at a time.
- Do not run multiple generate/edit image calls in parallel for different screens/states.
- Wait for each call to finish, inspect the output, then issue the next call.
- For multi-screen/multi-state batches, process a deterministic queue sequentially.
- When calling image tools, always use absolute filesystem paths.
- Always pass an absolute `output_file_path` for generated/edited images.
- For edit calls, use absolute paths for source images.

### Prompt Lineage And Update Discipline

- For iterative updates, default to `edit image` anchored to the latest approved source image ("shell").
- Use `generate image` for first drafts, major structural resets, or when repeated edit attempts cannot recover accuracy.
- Before updating an image, read the current prompt from manifest `Prompt Path` and identify its `Parent Image` (if any).
- Create the next prompt by updating the current prompt (preserve unchanged constraints, modify only requested deltas, and explicitly call out unchanged regions).
- Save the updated prompt back to the same prompt path as latest source of truth.
- For edit operations, prompt files must document:
  - Human intent header: `UI Purpose`, `User Can Do`, `Transition Outcome`
  - Transition metadata: `Trigger`, `From State`, `To State`
  - I/O linkage: `Input Image`, intended `Output Image`
- For replacement updates, write the new image to the same image path unless the user explicitly asks for a new variant.
- Do not create version-sprawl prompt files (`v2`, `v3`, etc.) unless the user explicitly requests branching.
- Keep one canonical shell per screen/flow and derive state variants from that shell or its approved descendants.

### Transition Traceability Model

- Treat documentation as four linked layers:
  - Canonical behavior intent: `ui-behavior-test-matrix.md` (`transition_id`, trigger, from/to state, acceptance checks)
  - Navigation runtime: `flow-maps/<platform>/<flow>.json` transitions derived from the behavior matrix
  - Edit execution: prompt file for the target state (exact edit prompt + transition metadata)
  - Artifact lineage: `image-prompt-manifest.md` (input/output image paths and parent linkage)
- Use the same `transition_id` across all four layers for one transition.
- If reusing the same image path across iterations, keep latest output on disk and append an iteration log section in the prompt file (short delta summary + previous input image path).

### Artifact Lifecycle Discipline (Required)

- Keep only active artifacts that match the latest product vision and current valid use cases.
- When a use case/flow/screen/state becomes invalid, deprecated, or obsolete, delete its files from:
  - `images/`
  - `prompts/`
  - `flow-maps/`
  - `viewer/` (if the flow is removed)
- Do not keep deprecated artifacts "just in case" unless the user explicitly asks to archive them.
- If naming is stale or unclear, rename files/folders to reflect current product language and use-case intent.
- After any rename or deletion, update all references in the same change:
  - `image-prompt-manifest.md`
  - flow-map `screens[].image` paths
  - viewer map path configuration
- Prefer stable, descriptive kebab-case names that communicate platform, flow, screen, and state.

### Aspect Ratio Discipline

- Specify an explicit aspect ratio in every image generation prompt.
- Use only supported ratios: `1:1`, `4:3`, `3:4`, `3:2`, `2:3`, `5:4`, `4:5`, `16:9`, `9:16`, `21:9`.
- For each platform + flow, keep one fixed ratio across all screens/states to avoid distortion drift.
- For edits, keep the same ratio as the baseline source image.
- Do not normalize, stretch, or re-encode generated images unless the user explicitly asks.

### 1) Define Product Intent And Constraints

- Define target platform (`web`, `ios`, `android`) and viewport assumptions.
- Define target aspect ratio per platform/flow from the supported ratio list.
- Define user personas, primary jobs-to-be-done, and critical paths.
- Define design constraints: brand tone, accessibility needs, component style, and data density.
- Define fidelity level (`wireframe`, `mid`, `high`) before generating assets.
- Define the platform+flow bundles that must be navigable in local viewers.

### 2) Map Screens, Actions, And States

- Create a state transition table for each flow:
  - `transition_id` (stable key, e.g., `gateway_validate_to_success`)
  - `screen`
  - `trigger` (click/tap/submit/navigation/system event)
  - `from_state`
  - `to_state`
  - `expected_feedback` (visual + microcopy)
- Treat this table as canonical and keep all map/manifest transition IDs aligned to it.
- Cover at minimum: `default`, `focus`, `pressed`, `disabled`, `loading`, `success`, `error`, and `empty` where applicable.
- Prioritize one critical flow first, then expand to secondary flows.

### 3) Create One Canonical Product Base Spec And Shell Lock

- Build one reusable `product_base_spec` (platform, viewport, typography, spacing, tokens, accessibility intent).
- Reuse the same base spec in all generate/edit prompts to prevent style drift between screens.
- For each screen, create and lock a canonical shell image before state branching.
- If the initial generation is not accurate, iteratively edit the same shell until layout and visual identity are stable.

### 4) Generate Baseline Screens

- Generate net-new screen drafts with the image generation tool.
- If a draft is not accurate enough, refine it with iterative `edit image` passes until the canonical shell is locked.
- Run baseline work sequentially: one screen per tool call, then review result before the next.
- Include explicit ratio in each generation prompt and keep it constant for that platform + flow.
- Use absolute `output_file_path` in every generation/edit tool call.
- Save the exact prompt used for each baseline image to:
  - `ui-prototypes/<prototype-name>/prompts/<platform>/<flow>/<screen>-default.md`
- Use deterministic style instructions and the shared base spec to keep typography, spacing, iconography, and color consistent across screens.
- Save locked shell outputs in a stable structure:
  - `ui-prototypes/<prototype-name>/images/<platform>/<flow>/<screen>-default.png`
- Speak completion after baseline screen set is physically written for the target platform+flow.

### 5) Create Interaction States From Baselines

- For iterative state updates, default to `edit image` from the locked shell (or latest approved state predecessor).
- Use `generate image` for state creation only when a state requires intentional structural divergence.
- Preserve layout and visual identity continuity by carrying forward unchanged constraints and fixed shell elements in the updated prompt.
- Run state updates sequentially: one tool call per update, then review result before the next.
- Preserve the source image ratio for every edit call.
- Use absolute paths for edit inputs and `output_file_path`.
- For each edit call, record tool-call inputs/outputs in the manifest row:
  - `Input Image` (required)
  - `Output Image` (same as `Image Path` unless branching)
- Ensure every edited state maps to one transition tuple:
  - (`transition_id`, `trigger`, `from_state`, `to_state`)
- Save the exact prompt used for each edited image to:
  - `ui-prototypes/<prototype-name>/prompts/<platform>/<flow>/<screen>-<state>.md`
- Edit only state-relevant deltas:
  - Hover/focus rings
  - Pressed depth
  - Disabled contrast
  - Loading affordance
  - Validation/success/error messages
- Save outputs as:
  - `ui-prototypes/<prototype-name>/images/<platform>/<flow>/<screen>-<state>.png`
- Speak completion after interaction-state set is physically written for the target platform+flow.

### 6) Maintain Image/Prompt Manifest (Required)

- Maintain `ui-prototypes/<prototype-name>/image-prompt-manifest.md` in real time.
- Treat this manifest as the latest source of truth (current artifact set only).
- Add one row per image artifact (`default` and each edited state).
- For each row, record at minimum:
  - `Transition ID`
  - `Use Case`
  - `Platform`
  - `Flow`
  - `Screen`
  - `State`
  - `Trigger`
  - `From State`
  - `To State`
  - `Situation/Purpose`
  - `Image Path`
  - `Input Image` (for edits)
  - `Prompt Path`
  - `Source` (`Generate`/`Edit`)
  - `Parent Image` (for edited states)
- Ensure every image in `images/` has exactly one matching manifest row.
- Ensure every `Edit` row has a non-empty `Input Image` and transition tuple (`Trigger`, `From State`, `To State`).
- For replacement updates, update the existing manifest row instead of creating a new row.
- Remove stale/legacy rows when images or prompts are replaced or deleted.
- Keep only active image/prompt pairs for the current prototype revision.
- When artifacts are deleted or renamed, update/remove rows immediately so manifest and filesystem stay 1:1.
- Speak completion after manifest synchronization is physically written and consistent with current artifacts.

### 7) Connect Screens For Click-Through Simulation

- Create one flow map per platform+flow:
  - `ui-prototypes/<prototype-name>/flow-maps/<platform>/<flow>.json`
- Derive map transitions from `ui-behavior-test-matrix.md`; do not maintain an independent transition definition.
- Include per-link definitions:
  - `transition_id`
  - `screen`
  - `trigger`
  - `hotspot` (`x`, `y`, `width`, `height`)
  - `target_screen`
  - `transition` (`instant`, `fade`, `slide`)
- Keep hotspot naming deterministic so non-developers can review and iterate quickly.

### 8) Assemble Behavior Test Matrix

- Produce `ui-prototypes/<prototype-name>/ui-behavior-test-matrix.md` with one row per transition.
- Treat this file as the canonical transition source of truth.
- Include:
  - `transition_id`
  - `flow`
  - `screen`
  - `trigger`
  - `from_state`
  - `to_state`
  - `expected next state image`
  - `acceptance check`
  - `open question / risk`
- Mark blocking issues where any trigger has ambiguous or missing feedback.
- Speak completion after `ui-behavior-test-matrix.md` is physically written/updated.

### 9) Deliver Review Package For Non-Developers

- Produce a concise review packet:
  - Optional: `ui-prototypes/<prototype-name>/ui-prototype-spec.md` summary if the team requests a narrative overview
  - `ui-prototypes/<prototype-name>/image-prompt-manifest.md` for prompt/image traceability
  - `ui-prototypes/<prototype-name>/flow-maps/<platform>/<flow>.json` for click-through linkage
  - `ui-prototypes/<prototype-name>/viewer/<platform>/<flow>/` local click-through viewer files
  - Image gallery links grouped by flow and platform
  - Explicit unresolved decisions for product/design sign-off
- Keep wording product-facing and avoid implementation jargon when possible.

### 10) Publish Local Click-Through Viewer

- For each platform+flow image set, copy the viewer template into:
  - `ui-prototypes/<prototype-name>/viewer/<platform>/<flow>/`
- Configure each viewer instance to load its matching map file:
  - `../../../flow-maps/<platform>/<flow>.json`
- In viewer code, always resolve map/image URLs from an absolute base URL:
  - build map URL with `new URL(mapPath, window.location.href)`
  - resolve each `screens[].image` against the resolved map URL
- Serve the workspace root locally and open:
  - `http://localhost:4173/ui-prototypes/<prototype-name>/viewer/<platform>/<flow>/index.html`
- Use per-platform/per-flow viewers for product/design review so each image set can be reviewed directly.
- Speak completion after flow-map + viewer files are physically written for the target platform+flow.

### 11) Viewer Smoke Test (Required)

- Run syntax check on viewer JavaScript before handoff.
- Serve the project locally and verify at least:
  - viewer page loads,
  - flow-map JSON loads,
  - one referenced image loads,
  - start screen renders with no URL-resolution errors.
- If any check fails, fix viewer path resolution before delivery.
- Speak the viewer smoke-test result (`Pass`/`Fail`) after checks complete.

## Prompt Patterns And Checklists

- Read and reuse `references/prompt-patterns.md` for:
  - UX criteria coverage and product base spec
  - Production screen generation and state edit templates
  - Shell-lock and iterative edit prompt patterns
  - Image/prompt manifest template and logging checklist
  - Flow-step and cross-platform adaptation templates
  - Click-through flow map template, viewer compatibility rules, and acceptance checklist

## Default Outputs

- `ui-prototypes/<prototype-name>/ui-behavior-test-matrix.md`
- `ui-prototypes/<prototype-name>/image-prompt-manifest.md`
- `ui-prototypes/<prototype-name>/prompts/<platform>/<flow>/*.md`
- `ui-prototypes/<prototype-name>/flow-maps/<platform>/<flow>.json`
- `ui-prototypes/<prototype-name>/viewer/<platform>/<flow>/index.html`
- `ui-prototypes/<prototype-name>/viewer/<platform>/<flow>/viewer.css`
- `ui-prototypes/<prototype-name>/viewer/<platform>/<flow>/viewer.js`
- `ui-prototypes/<prototype-name>/images/web/<flow>/*.png`
- `ui-prototypes/<prototype-name>/images/ios/<flow>/*.png`
- `ui-prototypes/<prototype-name>/images/android/<flow>/*.png`

## Quality Gate

- Ensure every critical trigger produces clear, visible feedback within one state transition.
- Ensure states are visually consistent across platforms and flows.
- Ensure aspect ratio is explicitly defined and consistent for each platform + flow.
- Ensure no generated image is normalized/stretched in a way that distorts UI geometry.
- Ensure every image has a corresponding prompt record in `image-prompt-manifest.md`.
- Ensure manifest contains only latest active artifacts (no stale legacy entries).
- Ensure each iterative update prompt is derived from the current prompt referenced by manifest `Prompt Path`.
- Ensure each state image preserves shell continuity (layout/frame/spacing/component geometry) unless a deliberate structural change is documented.
- Ensure each edited image has traceable lineage: `Parent Image` + `Input Image` + (`Trigger`, `From State`, `To State`).
- Ensure each manifest `Transition ID` exists in `ui-behavior-test-matrix.md`.
- Ensure each flow-map transition corresponds to a matrix `transition_id` and matching trigger semantics.
- Ensure no obsolete/deprecated artifacts remain for removed or invalidated use cases.
- Ensure file/folder names reflect latest product vision and are consistent across images, prompts, maps, and viewers.
- Ensure error and empty states include recovery guidance.
- Ensure accessibility cues (focus visibility, contrast intent, readable hierarchy) are represented in mockups.
- Ensure each click-through trigger in each flow map points to a valid target screen.
- Ensure viewer navigation works for each clickable hotspot and start screen in each platform+flow viewer.
- Ensure viewer smoke tests pass for each platform+flow bundle.

## Handoff

- Hand off approved behavior specs and state assets to implementation.
- If engineering planning is requested next, invoke `$software-engineering-workflow-skill` with `ui-prototypes/<prototype-name>/ui-behavior-test-matrix.md`, relevant `ui-prototypes/<prototype-name>/flow-maps/<platform>/<flow>.json` files, `ui-prototypes/<prototype-name>/image-prompt-manifest.md`, and viewer behavior notes as inputs.
- Speak final handoff completion after all required handoff artifacts are written.
