---
name: mixio-pipeline
description: "Use when coordinating a full Mixio episode or deciding which production skill comes next, including optional Three.js blocking previsualization for selected synced shots."
version: 0.5.0
invoke: /mixio:pipeline
---

# Mixio Pipeline

The pipeline moves from a raw story/script to a locally developed, AI-ready director’s screenplay, then to a shot plan with a director-led Continuity Checklist and chat-confirmed Studio sync. **Use the director’s lens throughout production and consult relevant craft perspectives:** cinematography, production design, costume, props, script supervision, editing, sound, action, and technical feasibility. The director integrates them around audience intent and a connected sequence. The raw episode `script` remains the story source; the screenplay is a developed production document and may add clearly identified connective direction and coverage. See the shared [director’s lens](references/directors-lens.md).

Read the [native screenplay grammar](../mixio-episode/references/screenplay-grammar.md) when interpreting a screenplay and the [shot grammar](references/shot-grammar.md) when mapping direction to Studio fields.

## Prerequisites

- MCP server configured: `@mixio-pro/mcp`.
- Resolved project and episode. If scope is unknown, list options and ask in the same message; never infer IDs. Follow `mixio-project` and `mixio-episode` for setup.
- An existing screenplay/script, a user-supplied scene/shot breakdown, or another source text for this episode.

For full multi-step runs, use the current host’s native task or plan surface when available; use persistent goal features only when the user asks for work to continue across turns. Follow [agent-native tracking](references/agent-native-tracking.md). Native progress never substitutes for a needed user choice or billable-generation authorization.

### Human checkpoints

Checkpoints keep the user involved without requiring a separate Studio approval state. Present the screenplay, proposed breakdown diff, reference candidates, or production plan at the relevant point. A clear “proceed” in chat authorizes the scope just presented, and an earlier instruction authorizing that same scope remains valid; do not ask again or wait for a Studio status change. Continue independent preparation while a choice is open. Pause only the action that depends on a missing choice or authorization. If the user says to proceed with an advisory continuity or readiness issue, record the accepted risk and continue when the live model schema and project reference policy allow it. Unknown scope, ambiguous element identity, server access/policy rejection, and schema-invalid inputs remain technical constraints, not approval rituals.

## Sequence

| Step | Work | Result |
|---|---|---|
| 00 | Project and episode setup + read-only source snapshot | Confirmed scope; current script, screenplay, project references, existing shots, settings, and available images inspected |
| 00.5 | Director-led screenplay development | Complete local screenplay draft with scene/shot intent, technical direction, reference cues, continuity, and provenance; present changes as a checkpoint, then draft-upsert on chat confirmation or prior authorization |
| 01 | `/mixio:script-breakdown` | Structured local scene/shot plan derived from the confirmed screenplay, or an accepted existing breakdown enriched against it |
| 02 | `/mixio:continuity` — Continuity Checklist | Director-led scene, shot, and cross-scene checklist of continuity concerns, generation risks, and missing coverage; local corrections stay in the draft |
| 03 | Review and Studio sync | Exact scene/shot diff shown as a checkpoint; on chat confirmation or prior authorization, existing primitives write it and readback verifies it |
| 04 | Reference readiness | Audit references and assign stable voice IDs to speaking characters; build missing sheets/anchors as separately confirmed |
| 04.5 | `/mixio:blocking` (optional) | Approved shot-scoped Three.js proxy takes/renders for selected staging-heavy shots; render only when environment policy permits |
| 05 | `/mixio:shot-planning` | Method/model, dialogue audio needs, video audio-reference compatibility, batches, and production-plan review |
| 06 | `/mixio:generate`, then `/mixio:eval` | Dialogue audio generated first, then confirmed/authorized keyframe/video batches; evaluation findings offered as a delivery checkpoint |

## Step 00 — Set up and read

Resolve scope before expensive reads. If the project or episode does not exist, show available projects/episodes and get confirmation before creating it. Read the current project settings, references, existing episode scenes/shots, and available image assets.

Read the raw episode `script` / `metadata.fullScript`, current native `SCREENPLAY`, any supplied or persisted breakdown, references, settings, and images. Treat the raw script as story source material. A non-empty screenplay is the current production draft, even when it is only a copy of the script; assess whether it is sufficiently developed for the requested production. A high-level script or underdeveloped screenplay requires Step 00.5. Preserve the raw script; never silently treat it as a finished screenplay. If neither source text nor a usable supplied breakdown exists, request source material.

Read any existing delivery, visual-style, and reference-policy settings as constraints. Capture the user’s intended tone and format when stated; do not invent a style to fill an unset field. Missing settings, sheets, and anchors can be listed as readiness gaps; they do not block a local plan. Do not choose per-shot generation methods, select generation models, or submit image/video jobs before the accepted breakdown.

## Step 00.5 — Develop the director’s screenplay

When the source is a high-level script, outline, or underdeveloped screenplay, use `/mixio:screenwriting` (scene-writing plus the relevant quality gate) to create a complete AI-readable screenplay locally before shot breakdown. Preserve the story’s stated events, dialogue, character intent, and canon while developing them into playable scenes and explicit visual beats. Use full, concrete screenplay action rather than a terse restatement of the source. Include scene headings and transitions; entrances, exits, establishing geography, staging, action and cause; reaction and connective beats; character, prop, wardrobe, location, and look continuity; and motivated framing, camera angle/movement, lens, lighting, sound, and pacing where known. Add reasonable connective coverage even when it is absent from the raw script, so scenes form a coherent sequence rather than isolated clips.

Keep a source-to-screenplay change list that distinguishes source facts and dialogue from `INFERRED` director additions. Do not invent consequential story facts, character motives, or dialogue to conceal gaps; present those as `OPEN DECISION`s with options. Use exact existing `#` mentions from `mentionableLooks`; describe unregistered looks/views in prose and record them as readiness needs. Keep shot-specific direction in readable screenplay action and supported standalone annotations; only the 11 keys listed in the native screenplay grammar are parsed into breakdown overrides. Capture duration, detailed per-shot fields, cut timing, and other data without a native screenplay key in the companion local director’s plan, then carry them into the structured breakdown.

Present the complete screenplay draft, source-to-screenplay changes, unresolved decisions, and reference gaps as a checkpoint. If the user says “proceed,” or has already authorized this screenplay work, upsert the presented body as a Studio draft and read it back. Use the read-back draft as the production baseline even while Studio reports `draft`; do not require a separate Studio approval action/status. If the user has not authorized the screenplay write, ask once and continue other independent preparation. Keep consequential story choices visible; if the user elects to proceed without resolving one, preserve it as `OPEN DECISION` and continue unaffected work. A screenplay edit after shot sync invalidates the breakdown and downstream direction that depends on it, so revise only those affected artifacts.

## Step 01 — Use or create the local director’s plan

First check whether the user supplied a scene/shot breakdown in the prompt or attachments, or the episode already has a usable scene/shot breakdown in Studio. Follow `mixio-script-breakdown` in one of two modes:

- **Breakdown supplied or already present:** Treat its scene order, shot order, authored beats, and stated direction as the baseline. Enrich it with production detail: audience intent, visible action, framing/camera, character and prop state, geography, shot handoffs, source links, and readiness gaps. Preserve its structure and wording where they carry the user's direction. Add clearly labeled inferred detail, missing connective coverage, and useful editorial surplus through extra shots or alternates; show unresolved story-changing choices as `OPEN DECISION`. Do not run a fresh screenplay-to-scenes-and-shots pass over it.
- **No usable breakdown exists:** Build the scene-and-shot structure from the approved, developed screenplay, preserving its order and facts, and add clearly labeled inferred coverage where needed.

If an existing breakdown appears incomplete, conflicting, or unsuitable for the requested work, identify the specific gap and propose a targeted repair or rebuild for review. Do not silently replace or discard existing scenes, shots, or user-authored direction. In either mode, keep the work local and do not mutate Studio scenes, shots, relations, references, or screenplay during this step.

Plan for editorial surplus: the stated episode/runtime target is the intended post-production duration, not a limit that all generated shot durations must sum to. Preserve enough coverage for the editor to select, trim, align, and pace the final cut. Add suitable alternate shots and extra coverage when they help editorial choices or protect transitions, and show their purpose and approximate duration in the plan. The planned generated video must reach at least 1.2× the intended final runtime (20% extra): at least 72 seconds for a 1-minute final or 108 minutes for a 90-minute final; do not force the breakdown to fit the runtime by deleting useful coverage or shortening shots below what the action needs. Flag material additions as `INFERRED` and include them in the later batch plan. Use the [editorial coverage ledger](references/editorial-coverage.md) to count each distinct candidate clip once, including alternate angles, emotional takes, reactions/listeners, inserts, and bridges; exclude still keyframes. This surplus direction does not itself approve billable generation.

## Step 02 — Create the director’s Continuity Checklist

Use `/mixio:continuity` to write the checklist artifact before Studio sync. Organize it by scene, shot, and cross-scene/shot handoff. Ground each item in the screenplay, shot plan, Cast & World records, selected look/configuration, and available references. Cover character/prop state, geography and camera POV, screen direction/eyelines, framing, light/time, dialogue/voice, and image/video generation risks. List missing establishing, entrance/exit, action-cause, insert, reaction/listener, reverse-angle, transition, or other coverage with its dramatic/editorial purpose.

Apply only grounded corrections to the local plan and revise the affected checklist items. Keep story-changing ambiguity as an `OPEN DECISION`. Missing images or sheets are readiness findings, not continuity errors. Text-only review may assess intended geography and action, but must not claim an image/anchor comparison was performed when no image is available. The written checklist accompanies the exact Step 03 Studio diff. Use the [checklist template](../mixio-continuity/references/checklist-template.md), and carry its relevant constraints into generation prompts, reference bindings, and supported evaluation context.

## Step 03 — Show the diff, then sync on confirmation

Present the complete reviewed table and a separate Studio diff. For every proposed operation include:

- `ADD`, `UPDATE`, or `NO CHANGE`;
- the confirmed scene/shot element ID for an update, or `NEW` for an addition;
- the exact fields and before/after values;
- source beat and `SCRIPTED` / `INFERRED` / `OPEN DECISION` provenance;
- affected character, location, prop, and appearance relations;
- unresolved match questions and asset-readiness gaps.

Match an update only when the current Studio element ID and the intended scene/shot are confirmed. Before using an upsert key, verify that it resolves to that same element. Flag ambiguous matches and unmatched existing shots; do not silently overwrite, renumber, or delete them. Present the exact diff as a checkpoint; chat confirmation or prior authorization covering that diff is enough to write. A material later edit requires an updated diff and renewed confirmation for the changed portion.

After confirmation, use the existing primitives documented in `mixio-episode` and `mixio-script-breakdown`. Apply the project’s `settings.references` policy to any required reference registration. Read the persisted scenes, shots, and relations back; compare them with the confirmed diff and report any missing, altered, or partial writes by element ID. Never claim a write succeeded from the mutation response alone.

## Step 04 — Check readiness

Run `/mixio:reference-audit` against the confirmed plan and current Cast & World. Follow the full cast-ledger, positioning, and anchor-guide procedure in `mixio-sheets`; the audit reconstructs the per-scene matrix from the accepted shot plan, screenplay, and `appears_in` relations if it is missing, then records source shot/cue evidence and visual-review status in `metadata.pipeline.reference_audit.anchor_cast_ledger`. This check includes later/special appearances and entrance conditions, while keeping the opening image limited to the scene-opening cast. Distinct characters need distinct faces unless an intentional duplicate is scripted. Report missing references, images, details, and scene anchors with their likely effects and options. Continue on the user's accepted limitation when the model schema and project policy allow; technical input requirements still apply to each job.

Use `/mixio:sheets` only for assets that need building or enrichment. Confirm image generation in chat unless already authorized, then re-run the reference audit and refresh affected Continuity Checklist items after reference, look, view, or anchor changes. If accepted shot direction changes, show the revised Step 03 diff; proceed on confirmation or existing authorization before planning production. Report readiness gaps and their effect. If the user accepts a gap, carry it forward and continue where the model schema and project policy allow; do not turn advisory gaps into a pipeline-wide stop. Use `references/preflight-settings.md` after the breakdown to confirm and read back any missing delivery/anchor settings or generation defaults needed for production.

## Step 04.5 — Spatial Blocking (optional)

Use `/mixio:blocking` after Step 03 has persisted the confirmed shots and Step 04 has checked reference readiness. The Three.js tools require an authorized shot ID, so this cannot run against the local-only Step 01 plan. Select only shots whose performer routes, eyelines, prop interactions, entrances/exits, axis, or camera geography benefit from spatial review; simple holds, inserts, or clear staging can skip it. Present the selected shots and intended proxy scope as a checkpoint; a clear “proceed” authorizes the non-billable take and render for that scope. A render-policy rejection is a hard tool constraint.

Review the proxy as staging evidence, never as final performance or appearance. If it confirms the accepted direction, carry the reviewed take/render IDs into Step 05. If it reveals a needed direction change, update the local plan and Step 02 Continuity Checklist, show the revised exact diff, return to Step 03 for confirmation and readback, then refresh affected Step 04 readiness and proxies. Do not mutate synced shots directly from the proxy review.

## Step 05 — Plan production

Run `/mixio:shot-planning` against the confirmed, persisted shots. Choose each shot’s generation method and model from the live use-case contract while preserving its accepted purpose, action, camera direction, and handoff. Include the extra coverage and alternates in the batches. For dialogue, count planned TTS jobs, verify each speaking character has a stable `voiceProfile.voiceId`, and check whether the selected video route accepts audio references. Report planned generated-material duration separately from intended post-production runtime; planned generated video must reach at least 1.2× the final-edit target. Recalculate the output ledger using selected models’ supported durations and include every alternate clip in job counts. If a technical limit requires changing direction, present the available options; preserve user direction and proceed with the compatible option they choose. Verify reference readiness and mandatory prompt `@` mentions/maps, then present the production plan as a checkpoint. Continue on “proceed” or prior authorization for this scope. Confirm billable video generation only when it is not already authorized.

Before batching, compare each shot’s camera zone, location configuration, and selected labeled view against `reference_pack_inventory`. If a view is absent or unconfirmed, report the gap and its likely effect. Ask whether to build the missing view or proceed with the documented limitation; if the user says proceed, continue when the selected model accepts the available inputs and project policy allows it. After any newly generated reference image, use the user’s chat decision to attach it; no separate Studio approval state is required. Refresh affected Checklist items and the reference audit when references change. If shot direction or relations change, show the revised diff and proceed on confirmation or prior authorization for the change. Group consecutive shots only when their model, generation use case, and input contract all match.

## Step 06 — Generate and evaluate

Run `/mixio:generate` for the confirmed production plan. Before video, use speaking characters’ stable Gemini TTS voice IDs and generate their dialogue audio with `gemini-3-8-flash-lite-tts`; use that audio as a video reference when the selected model schema accepts audio inputs. Then generate keyframes and video. Apply each shot’s relevant Continuity Checklist items to its effective prompt, media references, start/end state, and intended transition; revisit affected items after a reference or generation-route change. Preserve the confirmed transcript and voice assignment. **Before every video job, including each job in a batch, show the exact effective prompt and exact inputs for that job and wait for the user to confirm them.** Include model/use case, target shot/segment, media assets and slot bindings, `mentionMap`, parameters, and prompt-enhancement mode. A prior authorization covers generation only when it explicitly covers those same prompts and inputs; general batch or cost authorization is insufficient. Recheck schema-valid media slots, URL-valued `mentionMap` bindings, and prompt `@` mentions immediately before each confirmed job. The MCP adapter derives Studio’s internal `slotTags` and labels. Use the deepest confirmed context (`projectId`, `episodeId`, `sceneId`, `shotId`). Upload final outputs through `mixio-workspace`.

When evaluation is included in the requested delivery, run `/mixio:eval` for each rendered batch through `evals_evaluate_media` and poll with `evals_get_evaluation_result`. Reference-image evaluation may use `image-character` or `image-location` only when the live catalog and contract support the candidate and its evidence; it does not replace shot evaluation. Use `keyframe-continuity` for strict ordered keyframes and adjacent-transition checks, `sequence-storyboard` only as a general storyboard lens, `video-multi-shot` for cross-angle geography, and `delivery-qc` for final delivery review. Request `human-review` when a repair plan is useful. Bind ordered inputs and expected state to the shot plan, including any accepted Step 04.5 blocking direction. Report the worst transition and findings clearly; if the user accepts a documented deviation or chooses to proceed without evaluation, record that decision and the evidence limitation. An aggregate score cannot hide a severe break. If the current catalog exposes only a deprecated compatibility alias, follow the adapter boundary in `mixio-eval` and do not claim a strict transition check when that alias cannot carry its context.

Evaluation submissions are billable; a clear evaluation request or existing authorization for the current batch is enough. Present the receipt, localized findings, and any `human-review` repair plan as a decision checkpoint. Use evaluation time/frame ranges to identify the smallest faulty segment. If evaluation does not localize it, inspect a timecoded still grid from the video. Regenerate only the affected segment by default, preserving unaffected approved footage. If the model cannot generate that segment independently, present the smallest supported replacement scope and explain the limit. A repair recommendation or “retry” decision does not confirm a new video prompt or input set: show the exact replacement prompt and inputs and wait for confirmation before submitting. If the user says to retry and has confirmed that exact job, proceed without another approval step.

## Resume and re-entry

The screenplay change map, shot plan/output ledger, and Continuity Checklist are review artifacts in the current agent context; they have no new Studio schema. If context is lost, reread the raw script, current Studio screenplay and graph, then rebuild the plan and checklist from source evidence and recorded chat decisions. Treat a confirmed Studio draft as the current screenplay baseline even if its Studio status is still `draft`; do not require a separate approval status. If a confirmed screenplay edit changes synced direction, update only the affected breakdown, checklist, and batches.

## Working sequence

```text
setup + read → develop/review screenplay when needed → chat confirmation or prior authorization + draft upsert/readback
             → use/enrich supplied or existing plan, or create one if absent → director-led Continuity Checklist
             → show exact breakdown diff → chat confirmation or prior authorization → sync + readback
             → reference readiness → method/model + generation authorization → generation + evaluation
```
