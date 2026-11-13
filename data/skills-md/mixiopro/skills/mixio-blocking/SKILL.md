---
name: mixio-blocking
description: "Previsualize actor, prop, and camera blocking as a simple Three.js scene tied to a confirmed Studio shot. Use when spatial staging or movement needs a visual review before video generation; for shot breakdown use mixio-script-breakdown, and for text continuity checks use mixio-continuity."
version: 0.1.0
invoke: /mixio:blocking
---

# Mixio Blocking

Build a reviewable spatial blocking proxy for selected shots. Blocking defines where performers and important props are, how they move and relate, what they look toward, and how the camera sees that action. The Three.js render is a staging reference for review; it is not final animation, a photorealistic look reference, or a replacement for the generated shot.

Use this skill after the breakdown has been confirmed and synced to Studio and reference readiness is complete, because its tools require a persisted shot. Read the screenplay, shot specs, scene anchor, location details, and character/prop references that affect the selected shot. Preserve authored direction. Label any inferred position, route, eyeline, or camera placement, and surface choices that change screen direction, geography, or dramatic emphasis for review.

## Scope and tool contract

Resolve and restate the confirmed project, episode, scene, and shot before reading or writing shot-scoped data. Numbered shot labels repeat across scenes and episodes; use confirmed element IDs, never a guessed ID.

The Mixio CLI exposes `create-threejs-scene-take` and `render-threejs-scene` (the hosted MCP names are `create_threejs_scene_take` and `render_threejs_scene`; the local bridge may prefix them with `studio_`). Call `studio_describe_tools` for the active transport's tool details before use. The CLI contract describes:

- `create-threejs-scene-take`: saves an immutable, non-billable code take for one shot; it does not render. Pass the confirmed `projectId`, `episodeId`, `sceneId`, and `shotId`, plus `input.source`, `input.parameters`, and `input.settings`. A first take may include `name`; a revision may include `parentTakeId` or the existing `sceneProgramId`.
- `input.source`: a JavaScript module exporting a default `createScene` function. The CLI contract's example receives `{ THREE, scene }` and adds Three.js objects to `scene`. Do not assume additional runtime helpers or imports; inspect the live tool description/contract for the deployed environment.
- The current tool contract does not specify a timeline/update callback or animation semantics. Do not claim that a multi-beat blocking path was rendered or validated unless the live runtime contract documents how time drives the scene. If it does not, use static key poses or separate take revisions to show staging states, and mark continuous movement as unverified.
- `input.parameters`: up to 100 declared numeric controls with `id`, `label`, `min`, `max`, `step`, and `defaultValue`.
- `input.settings`: required `width`, `height`, `fps`, and `durationSeconds`; the current schema allows 64–3840 pixels per dimension, 1–60 fps, and durations above 0 through 30 seconds.
- `render-threejs-scene`: submits a capped, non-billable render only when the environment render policy is enabled. It requires the confirmed project/episode/scene/shot, `sceneProgramId`, `takeId`, and a stable `idempotencyKey`; optional `parameterOverrides` must use declared parameters. Poll the returned Studio job with `get_job_status`.

Tool contracts can change. Use `mixio get-contract --target tool --tool-name create_threejs_scene_take` and the corresponding render tool on the CLI, or the active transport's schema discovery, when exact current fields or limits are needed. Do not submit a guessed payload.

## Choose the blocking approach first

Decide per shot which approach the proxy serves before building it. A creator video on video-model blockouts (Seedance and MiniMax examples) describes two workable approaches and one to avoid. This is one creator's guidance, not a Mixio-verified result, so confirm it with a trial on a representative shot.

- **Static composition (default).** Simple shapes fix the scene, composition, positions, and camera. The prompt and reference images carry the action, which leaves the model free to interpret movement. Do not model an action the prompt can state; for example, do not animate someone riding a bike or even include the bike, and describe it in the prompt instead. Include a prop only when geography, a handoff, or an eyeline depends on it.
- **Detailed motion.** Fully animated figures with precise movement and timing, plus camera movement, give the model a much stronger motion reference for reproducing specific actions and camera moves. Use this only when the shot needs that control and the live runtime documents how time drives the scene. This skill cannot currently confirm that (see the scope section), so treat it as unavailable until it is documented.
- **Avoid the middle.** A blockout with some movement that is still stiff or limited may carry that stiffness into the generated shot instead of natural motion. If detailed motion is not available, show staging as static key poses rather than a rough walk cycle or a simple slide along a path.

Record the chosen approach and the reason in the handoff.

## Build a blocking proxy

1. **Extract the staging facts.** Record the playable area and persistent landmarks, entrances/exits, performer start/end positions, facing, posture, eyelines, prop handoffs, and camera position/framing. Choose and state one world-axis convention for the scene (for example, Y-up, X lateral, Z depth), then keep it stable across takes. Track the axis of action and screen direction; flag reversals rather than silently correcting them.
2. **Separate authored facts from inference.** Use `SCRIPTED`, `INFERRED`, and `OPEN DECISION`. Ask for a decision when alternatives alter a reveal, power relationship, eyeline, screen direction, or intended camera coverage.
3. **Represent only what staging needs, with primitive shapes and a fixed color legend.** Build every object from basic Three.js primitives (box, cylinder, sphere, cone) with flat, unlit-looking solid colors. No models, textures, or costume detail.
   - **Performers:** a peg figure: one cylinder body with a sphere head, plus a small cone on the front edge to show facing. Keep the same size unless height matters to the shot. Give each performer a different saturated color, never reused for another performer, prop, or set piece in the same scene.
   - **Hand props that matter:** a small box or sphere in its own color, distinct from every performer.
   - **Set and landmarks:** plain boxes in neutral grays and browns (floor, walls, furniture, doors), with simple cut-outs only where a window or doorway affects sightlines or entrances. They must never compete with performers and props for color. Show the floor plane and the landmarks the staging depends on. Give the floor a grid or checker pattern, and add a few tall landmarks, so camera movement and distance are readable.
   - **Camera:** a white or black cone pointing along the view direction.
   - **Paths and markers:** thin lines or small flat markers in the owning performer's color.
   - **Legend:** use this default palette unless the project already defines one, and keep it identical across takes and revisions: red `0xe53935`, blue `0x1e88e5`, yellow `0xfdd835`, green `0x43a047`, orange `0xfb8c00`, purple `0x8e24aa`. Do not rely on text labels; the runtime contract only guarantees `THREE` and `scene`, so identity must come from shape and color alone. When several performers are close in hue, keep their shapes or sizes different too, so the proxy stays readable without color.
   - **Prompt-ready naming:** record the legend as a table (color + shape → Cast & World element and its `SCRIPTED`/`INFERRED` status) in the handoff, for example "red peg figure = Maya", "blue peg figure = Dev", "yellow box = the briefcase". Prompts can then say "the red figure" and be traced back to a character. Cast & World names and mentions stay the identity authority: the legend only describes the proxy and never replaces a reference image or a bound `@tag`.
4. **Keep the camera legible.** Show the camera/frustum or a clear view marker when the runtime supports it. Check that the proxy view communicates foreground/background order, entrances, eyelines, key prop interactions, and intended screen direction. Never invent a camera move that conflicts with the shot spec.
5. **Create and render a take.** Write a concise scene module and only the numeric parameters needed for review. Match dimensions and duration to the shot's approved settings where the live tool allows them. Save the take with full confirmed scope, then render it with its returned program/take IDs and a stable idempotency key. A disabled render policy is a reported limitation, not a reason to bypass the tool.
6. **Review and revise.** Inspect the rendered proxy and compare it against the screenplay, shot spec, and anchor. Report concrete issues such as a crossed axis, blocked eyeline, unreachable prop, obscured entrance, or camera path through geometry. Create a child take for revisions so provenance remains intact. Do not overwrite the approved screenplay or silently change shot direction.
7. **Hand off to planning.** Record the reviewed take/render IDs, the color/shape legend, staging facts, open decisions, and findings. A render does not approve itself. Get human confirmation before treating it as accepted staging evidence. If it changes the accepted shot direction, update the local Continuity Checklist and plan, show the revised Studio diff, and sync the confirmed change before planning production.

## Using the proxy as a generation reference (check before relying on it)

A reference video of colored peg figures on a gray set, with the camera path shown, may be able to steer position, movement, and camera in a later generation. This section describes how to prepare for that use. It does not promise that Studio supports it.

- **Support is unverified.** Before saying a render can be attached, read the live use-case schema (`studio_get_use_case_input_schema`) for an image or video reference slot that accepts it. If there is none, keep the proxy as a review artifact and describe the staging in words.
- **Time-driven motion is unverified.** The tool contract documents no timeline or update callback (see above). A motion or camera-path reference needs a documented way for time to drive the scene. Without it, use static key poses or separate take revisions and mark movement as unverified.
- **Bind identity in the prompt.** The proxy's colors mark position only. State the mapping from the handoff legend ("the red figure is @maya") and say that proxy colors, shapes, and the gray set are not to appear in the result. Character looks still come from bound Cast & World references.
- **Keep one idea per color.** Reuse the same color for the same performer in every take, and do not change a color between a reference render and its prompt.
- **Read the camera path.** Check that the proxy camera's start, end, and travel match the shot spec before treating the render as a camera reference. A fast or inverted move needs an orientation cue: for example, a two-tone body or a distinct head color, so up and down remain readable.
- **Treat model response as untested.** The creator video reports that simple shapes leave the model freedom while stiff partial motion can be preserved, but it shows paired examples and not a controlled comparison. Run one low-cost trial on a representative shot, and ask for confirmation before billable generation, before generalizing to the episode.

## Pipeline relationship

In the full episode workflow, this is optional Step 04.5, after Step 03 Studio sync and Step 04 reference readiness, before Step 05 shot planning. The tools require a confirmed persisted shot, so do not call them on the local-only breakdown. Use this step only for selected shots where staging benefits from spatial review; simple holds, inserts, and shots with unambiguous staging can skip it. The Step 02 Continuity Checklist remains the source of pre-sync concerns; revisit its affected items if proxy review changes direction.

If proxy review finds that the accepted shot direction should change, update the local plan and Continuity Checklist, present the revised exact Studio diff, and return to Step 03 for confirmation and sync. Rebuild affected proxies and refresh reference readiness as needed before Step 05. Any breakdown or blocking change after shot planning invalidates the dependent plan. Track take/render IDs, review state, and unresolved decisions in the host's task/plan surface or working handoff; do not invent an episode metadata key for this optional step.

## Limits

- The Three.js proxy communicates spatial and temporal staging, not final character identity, performance nuance, lighting, wardrobe, or rendered-image quality. Its colors are proxy markers; do not let them leak into the generated shot's look. If a render is attached to a generation job as a staging reference, check the live use-case schema for an accepted media slot and bind it through `input.media` and `mentionMap` as `mixio-generate` describes, and say in the prompt that colors and shapes mark position only.
- It does not replace the Continuity Checklist in `mixio-continuity`, the anchor/reference work in `mixio-sheets`, shot planning, generated-video evaluation, or human approval.
- This tool surface delivers a shot-scoped proxy, not an assembled film or timeline.
