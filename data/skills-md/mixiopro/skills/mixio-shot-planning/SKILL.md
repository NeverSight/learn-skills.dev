---
name: mixio-shot-planning
description: "Classify each shot into 6 structural archetypes (incl. MULTI_CUT for 10–15s multi-cut shots), match to model capabilities, validate duration and action density, verify prompt @ mentions and URL-valued mentionMap bindings, and group shots into generation batches — the model-aware layer between continuity and video generation. Submitting the actual generation job is mixio-generate. Unclear which step you need → mixio-pipeline."
version: 0.4.0
invoke: /mixio:shot-planning
---

# Mixio Shot Planning

Step 05 of `mixio-pipeline`. Runs after the director-led Continuity Checklist (Step 02), confirmed breakdown sync (Step 03), and reference-readiness review (Step 04), before video generation (Step 06). Answers: **how should each shot be generated, by which model, using what structural archetype, and is the shot's content feasible for that method?**

Fixed-ceiling batching assumed one model and one method. Shot planning acknowledges the live catalog, classifies each shot into a deterministic archetype, audits execution feasibility (action density, speaking rate, duration), and prepares the production plan. Ask before video generation unless the user has already authorized it.

## Prerequisites

- A persisted breakdown (Step 03), director-led Continuity Checklist (Step 02), and reference-readiness result (Step 04). Findings are surfaced at checkpoints; only schema, scope, or project-policy constraints prevent a dependent action.
- Resolved project and episode scope (from numbered Studio lists); use persisted scene/shot IDs only — never infer a label
- Use `duration`, `camera_movement`, `action`, and `audio` when present. If required data is missing, report the affected shot and continue planning the rest; only that job waits for the missing value if its schema requires it.
- The confirmed breakdown identifies the intended post-production runtime; planned generated-video duration must reach at least 1.2× that target, with every alternate and extra clip labeled by purpose and approximate duration
- `studio_list_use_cases({ outputType: "all" })` + `studio_get_use_case_input_schema({ useCaseId, modelId })` reachable (live catalog)
- Project/episode settings read during setup and any missing production defaults confirmed and locked (`settings.generation`, `settings.studio`)

## The three decisions per shot

For every shot, determine:

1. **Method / Archetype** — how it will be generated (the structural input shape)
2. **Model** — which engine produces it (the execution engine matched to shot characteristics)
3. **Feasibility** — whether the shot's duration, action density, dialogue, and reference bindings fit model constraints

Apply these decisions to every candidate in the approved [output ledger](../mixio-pipeline/references/editorial-coverage.md), including alternate takes attached to their owning confirmed shot. Refresh the applicable Continuity Checklist constraints for the selected route. Then group compatible work into batches and prepare the production plan for user review.

---

## 1. Structural Shot Typology (The 6 Archetype Families)

Every shot falls into exactly one generation archetype family: `GRID`, `MULTI_CUT`, `SEQUENCE`,
`MASTER_ANCHOR_MULTI_SHOT`, `SINGLE`/`DUAL_FRAME`, or `T2V`. `SINGLE` and `DUAL_FRAME` are
the two input shapes in one standard i2v family; persist the concrete code on the shot.
Classify by inspecting `camera_movement`, `action`, `duration`, markers, scene anchors,
`cuts[]`, and project settings.

| Archetype | Code | Target Video Use Case / Shape | When to use |
|-----------|------|--------------------------------|-------------|
| **Grid / Montage** | `GRID` | `production-generate-shot-keyframe-grid` (multi-panel) | Turnaround sheets, montages, multi-angle grids, comic/storyboard panels |
| **Multi-Cut** | `MULTI_CUT` | one `multi-shot-video` job from persisted `cuts[]` | 10–15s shots in a `multi_cut` band with authored per-cut specs (see `references/model-matching.md#multi-cut-routing`) |
| **Sequence** | `SEQUENCE` | keyframe planning as needed, then standard video passes through `cinematic-video` | Long or complex shots: multiple distinct beats, multi-marker choreographies, extended camera moves |
| **Master Anchor Multi-Shot** | `MASTER_ANCHOR_MULTI_SHOT` | scene anchor + derived keyframe/reference → `cinematic-video` | Coverage (CU, MCU, OTS) spatially grounded by the wide scene anchor |
| **Single-frame i2v** | `SINGLE` | 1 keyframe image → `cinematic-video` | Static/simple shots: holds, reactions, gentle camera moves (static, pan, tilt), single continuous action |
| **Start+End i2v** | `DUAL_FRAME` | start + end frames → `cinematic-video` | Complex transitions: significant blocking change, subject enters/exits, major camera framing change |
| **Text-to-video** | `T2V` | prompt-only `cinematic-video` model | Abstract, establishing shots with no prior frame, mood pieces |

### Classification rules

Here `BLOCKING` means the current shot/job shape is invalid or incompatible with the live
contract. It is not a workflow-wide stop: continue other shots and offer a schema-valid
alternative or a focused question for the affected job. A quality/readiness concern may be
accepted by the user; a malformed request cannot be submitted unchanged.

Select the model and read its live duration schema before applying these rules. The resulting
`model_max_per_pass` is an input to classification, not a value that can be read before model
matching.

```
mode = episode metadata.pipeline.shot_contract.mode
in_band = shot.duration is inside the episode's locked band
has_cuts = cuts[] exists

if has_cuts AND (mode != "multi_cut" OR NOT in_band):
    → BLOCKING: cuts[] is only valid for a multi_cut shot inside its locked band;
      resolve the episode contract or re-author/remove cuts[] with approval before routing

if shot is a multi-panel layout, montage sequence, or storyboard grid:
    if has_cuts:
        → BLOCKING: GRID cannot consume MULTI_CUT cuts[]; resolve the conflicting shot contract
    else:
        → GRID

if mode == "multi_cut":
    if NOT in_band:
        → BLOCKING: shot duration is outside the locked multi_cut band; do not route it as another archetype
    if cuts[] is missing or empty:
        → BLOCKING: author and persist non-empty cuts[] before classifying or generating
    if cuts[] fails the canonical invariant:
        → BLOCKING: fix cuts[] before classifying or generating
    → MULTI_CUT (one native multi-shot-video job; validate the route in
      references/model-matching.md#multi-cut-routing and the cuts[] invariant in
      pipeline shot-grammar.md)

if shot has no preceding shot/anchor in the scene and is an abstract or atmospheric establishing shot:
    → T2V

if shot is coverage (CU, MCU, OTS) framed within an established wide scene anchor:
    → MASTER_ANCHOR_MULTI_SHOT (uses scene anchor as spatial reference)

if shot has ≥3 markers [M1] [M2] [M3] OR distinct multi-beat action choreographies:
    → SEQUENCE

if shot.duration > model_max_per_pass:
    → SEQUENCE (split into multi-segment passes)

if camera_movement in (dolly_in, dolly_out, tracking, crane, arc, handheld):
    if duration ≤ 5s and action has ≤1 beat:
        → SINGLE (model handles short continuous move)
    elif duration ≤ 10s:
        → DUAL_FRAME
    else:
        → SEQUENCE

if camera_movement in (static, pan_left, pan_right, tilt_up, tilt_down, rack_focus):
    if action contains ≤1 marker and ≤1 distinct subject movement:
        → SINGLE
    else:
        → DUAL_FRAME

if camera_movement is not in the listed vocabularies OR no prior rule matched:
    → DUAL_FRAME (conservative total-classification fallback; record CLASSIFICATION_FALLBACK)
```

### Project-level defaults

Read `projects.settings` through `studio_get_project` before selecting a fallback model or generation shape; see [`references/execution-audit.md#project-level-defaults`](references/execution-audit.md#project-level-defaults) for setting paths and effects.

---

## 2. Model matching

For `production-generate-shot-keyframe-sequence`, `keyframe_count` is one of `4`/`6`/`8`/`10`/`12` frames. Check the live input schema before selecting a count; if a locked shot already has authored beats, prefer one `production-generate-shot-keyframes` job per beat with `keyframe_count: 1`.

Match each shot to the best available model based on what it needs. This is a recommendation, not a hard constraint — the user may override. Read the real per-model contract with `studio_get_use_case_input_schema({ useCaseId, modelId })` — that is the only authoritative source. Do **not** call `studio_list_generation_models` for this: it returns `{ id, label }` and nothing else (see `mixio-generate`).
Full capability profiles, task-to-use-case routing, strength-area matching guidance, and the conflicting-needs pattern: `references/model-matching.md`. `MULTI_CUT` shots follow the route table in [`references/model-matching.md#multi-cut-routing`](references/model-matching.md#multi-cut-routing), starting with H3 Ref2Vid on the normal `multi-shot-video` use case. The video-use-case routing reference explains how Step 06 passes the full shot context and explicit inputs: [`mixio-generate/references/video-use-case-routing.md`](../mixio-generate/references/video-use-case-routing.md).

---

## 3. Execution audit & feasibility validation

For each shot × method × model, use the live schema for model-specific duration and input
constraints. Studio's action and dialogue pacing checks are universal heuristics, not per-model
ceilings, so they are advisory.

### Duration feasibility

A duration contract is its exact allowed values (`enum`/`const`, including `anyOf`) or bounds.
Normalize numeric strings for comparison, but preserve the schema's declared wire type when
submitting. Treat `auto` as an inexact value; do not use it for a shot with a locked duration.

For `MULTI_CUT` shots, derive the contract from the **`multi-shot-video` use case** on the routed
model (H3 Ref2Vid `auto,5–15`). Require non-empty authored `cuts[]` and validate the canonical
[`cuts[]` invariant](../mixio-script-breakdown/references/canonical-schema.md), including its
duration sum; report missing cuts, `CUTS_SUM_MISMATCH`, and `CUT_COUNT_EXCEEDED` as BLOCKING.

```
duration_schema = schema?.properties?.parameters?.properties?.duration
duration_contract = derive_numeric_duration_contract(duration_schema)
if duration_contract is unreadable:
    FINDING: DURATION_SCHEMA_UNAVAILABLE — selected model exposes no readable duration contract
    → Do not submit a job for this unresolved route. Continue planning other shots and offer another model/use case or defer only this shot until its live contract is available.

if duration_contract.allowed_values exists AND shot.duration not in numeric_allowed_values:
    FINDING: DURATION_NOT_SUPPORTED — Shot 9 (6s) is not one of [4s, 8s]
    → BLOCKING: Use an allowed duration, split the shot, or select another model

if duration_contract.bounds exist AND shot.duration is outside [minimum, maximum]:
    FINDING: DURATION_OUT_OF_RANGE — Shot 9 (18s) > model max (8s)
    → BLOCKING: Split into segments or reassign to model with a compatible range

For MULTI_CUT, the route's duration is the whole video output. The authored `cuts[].duration`
values define the planned cut timing and prompt timestamps; they are not model duration controls.
If an enum cannot express the exact shot duration, mark that route incompatible and re-author the
shot duration plus cuts sum under approval before generation.

if shot.duration < 2.0 and method in (SINGLE, DUAL_FRAME):
    FINDING: DURATION_TOO_SHORT — most video models produce minimum 3-4s
    → ADVISORY: Merge with adjacent shot or extend duration
```

### Action density audit

Count distinct action clauses in the `action` field:

```
action_count = count_distinct_action_beats(shot.action)
action_density = action_count / shot.duration  # actions per second

if action_density > 1.5:  # Studio planner's universal pacing heuristic, not a model limit
    FINDING: ACTION_DENSITY_HIGH — 5 actions in 3s exceeds physical motion pacing
    → ADVISORY: Extend duration, reduce action complexity, or upgrade to SEQUENCE

if action_density > 0.8 and method == SINGLE:
    FINDING: ACTION_TOO_COMPLEX_FOR_SINGLE — multiple movements in a single keyframe pass
    → ADVISORY: Upgrade method to DUAL_FRAME or SEQUENCE
```

### Dialogue speaking rate audit

For shots with `audio.dialogue`:

```
word_count = len(shot.audio.dialogue.split())
speaking_rate = word_count / shot.duration  # words per second

if speaking_rate > 4.0:  # Studio planner's universal pacing heuristic, not a model limit
    FINDING: DIALOGUE_TOO_FAST — 22 words in 4s (5.5 wps) is rushed and unintelligible
    → ADVISORY: Extend shot duration or trim dialogue lines

if speaking_rate > 0 and shot.duration < 2.5:
    FINDING: DIALOGUE_IN_SHORT_SHOT — spoken dialogue requires minimum 2.5s screen time
    → ADVISORY: Extend duration to allow natural speech cadence and lip sync
```

Before video generation, plan dialogue audio from the confirmed transcript. Each speaking
character should have a stable Gemini TTS `voiceProfile.voiceId`; flag missing IDs for assignment
in Cast & World. Prefer `gemini-3-8-flash-lite-tts` and include the required TTS jobs in the batch
plan. Check the selected video model/use-case schema for audio-reference support; attach
the rendered dialogue URL only when an audio slot such as `audio_urls` is declared.

### Reference readiness (cross-check with Step 04)

```
for each character_link / location_link / prop_link:
    if reference has no attached image AND model requires image reference:
        FINDING: REF_IMAGE_MISSING — model needs reference image for consistency
        → The current job payload is not submittable. Offer a compatible image, a route that accepts available inputs, or a change in direction; continue planning other jobs meanwhile.

for each shot's selected character variant and location configuration/view:
    resolve each selection to the image selected in chat and recorded in referenceVariants
    if no selected inventory row or image matches:
        FINDING: REFERENCE_VARIANT_VIEW_NOT_READY — selection is absent, ambiguous, or unapproved
        → Report the uncertainty and offer an available reference, alternate route, or user-accepted continuation if schema permits.
    for each location image:
        verify its label maps to the confirmed orientation record and shot camera zone
        if missing or inconsistent:
            FINDING: LOCATION_VIEW_UNMAPPED — image does not prove the planned camera view
            → Report the visual coverage gap; offer to map/build the view or proceed with an accepted limitation if schema permits.

for each character appearance with a confirmed non-default variant mapping:
    require appearanceState.lookRef to match that selected variant id/name
    if missing or stale:
        FINDING: REQUIRED_LOOK_UNBOUND — wardrobe/age state maps to an approved look but the shot will fall back to the default
        → Report that the requested look would fall back to default; offer to correct the binding or continue with an accepted fallback.
```

The inventory is entity-specific: a CHARACTER's approved sheet is its default,
with only screenplay-required age/clothing variants; a LOCATION variant names
the required spatial/environmental configuration and its labeled images are
camera views. Do not resolve a location camera angle through a character-style
`lookRef`. Record the chosen location `variantId`/`variantName` and exact view
label/URL in the persisted plan so Step 06 passes the correct approved image.

This is the final post-breakdown reconciliation: compare each shot's mapped
character appearance and actual camera zone/linked location with
`metadata.pipeline.reference_pack_inventory`.
If the shot needs a new view, report `REFERENCE_VARIANT_VIEW_NOT_READY`, add a
proposed row to the inventory, and show the visual consequence and options.
Continue planning other shots. If the user confirms a render round, render and
evaluate that candidate; otherwise proceed with the accepted limitation when
the model schema and project policy allow it. Re-run affected checks after a
reference or shot change; do not restart unaffected pipeline work.

When these checks pass, emit the resolved rows as the episode's Reference Pull List
([references/reference-pull-list.md](references/reference-pull-list.md)) — it is the
handoff artifact Step 06 reads to attach the exact approved images.

### Look-binding readiness

```
for each character_link with a bound lookRef:
    resolve against reference's referenceVariants
    if unresolved:
        FINDING: LOOK_REF_UNRESOLVED — binding stale, will silently render default look
        → Report `STALE_LOOK_REF`; re-bind if the named look is required, or offer a default/alternate look and record the user's choice.
```

Pull character bindings once via `studio_get_production_context`'s `lookBindings` rather than per-shot queries. Carry each approved character `variantId`/`variantName` into the persisted plan. For locations, record the confirmed configuration `variantId`/`variantName` and exact labeled view URL; a generic `lookRef` check does not prove camera-view readiness (see `mixio-generate/references/reference-media.md`).

### Prompt mention & mention map validation (Universal Invariant across all models & methods)

For every media-bearing job, validate the public MCP binding contract before batching. The caller
supplies `mentionMap` as `{ "@tag": "exact URL from input.media" }`; the adapter derives Studio’s
internal `slotTags` and display labels. Do not ask MCP callers to provide those internal fields.
Run this check before batching. These are public MCP contract errors, so correct the affected job payload before submitting it; continue planning and preparing other valid jobs:

```
for each shot with media references:
    assets = flatten_media_slots(input.media)  # retain slot/index for diagnostics
    effective_prompt = prompt if prompt is present else materialized_prompt(sequence_notes, shot_spec)
    urls = all media URLs in this job
    if any URL is duplicated:
        FINDING: MENTION_URL_DUPLICATE — one URL cannot identify two references
        → BLOCKING: use distinct URLs for each reference
    for each [tag, url] in mentionMap:
        if url does not exactly match one URL in input.media:
            FINDING: MENTION_URL_MISMATCH — map URL is absent from this job’s media
            → BLOCKING: correct the URL or media slot
        if effective_prompt contains tag zero times:
            FINDING: PROMPT_MENTION_MISSING — mapped tag is absent from the prompt
            → BLOCKING: embed the exact @tag where that asset acts
    if a prompt @tag has no mentionMap entry, or a media reference identified in the prompt has no binding:
        FINDING: MENTION_MAP_MISSING — prompt and media bindings are incomplete
        → BLOCKING: add the exact URL binding or remove the unused mention
    if any mentionMap entry is unused:
        FINDING: MENTION_MAP_ORPHANED — map contains an unused binding
        → BLOCKING: remove orphan entries
```

For a sequence use case that intentionally leaves the caller `prompt` unset, validate the effective
materialized prompt (`sequence_notes` plus the shot-spec prompt); an omitted caller field is not a
grounding bypass. Descriptive prose may supplement a tag, never replace it. Record each validated
mention and URL in the [Prompt & Mention Sheet](../mixio-generate/references/prompt-mention-sheet.md).
Any `PROMPT_MENTION_MISSING`, `MENTION_MAP_MISSING`, `MENTION_URL_MISMATCH`,
`MENTION_URL_DUPLICATE`, or `MENTION_MAP_ORPHANED` finding makes that job invalid
under the public MCP contract. Correct the map/prompt or omit the unused reference;
do not submit that invalid job. This does not stop unrelated valid jobs or require a
separate Studio approval status.

### Natural skin prompt readiness

When the locked visual style or user direction is photorealistic/hyperrealistic, inspect every shot where character skin is visible and ensure its effective prompt carries concrete natural-skin and anti-smoothing direction. Match detail to framing: fine pores, subtle tonal variation, peach fuzz, and faint expression lines belong in close views where they can resolve; use natural complexion and surface variation at wider scales. Specify soft, physically plausible light and natural contrast when skin appearance matters. Do not rely on `ultra-realistic`/`8K` slogans, and do not add unsupported scars, freckles, or numeric reference weights. Bind the selected character image when available and permitted; URL-valued `mentionMap` bindings and prompt `@` mentions remain mandatory. Missing skin direction is a high-priority prompt-quality finding for a realistic character close-up. Recommend a correction and record any accepted deviation; this is not a schema gate.

### Continuity handoff feasibility

```
if shot is first in a new batch AND previous batch exists:
    if method not in (SINGLE, DUAL_FRAME, MASTER_ANCHOR_MULTI_SHOT):
        FINDING: CONTINUITY_BREAK_RISK — T2V/GRID cannot take previous frame as input
        → ADVISORY: Upgrade to SINGLE/DUAL_FRAME or accept cut discontinuity
```

---

## Feasibility report

Report archetype/model distribution and every finding with remediation, separating invalid-current-job
payloads from high-priority quality concerns and advisories. Use the [worked format](references/execution-audit.md#feasibility-report); the report
must include any `PROMPT_MENTION_MISSING`, `MENTION_MAP_MISSING`, `MENTION_URL_MISMATCH`,
`MENTION_URL_DUPLICATE`, or `MENTION_MAP_ORPHANED` finding with its asset, tag, and remediation. Correct affected invalid jobs before submission; continue all other work.

---

## Grouping into generation batches

After archetype/model assignment and feasibility resolution, group shots into **batches** per model-specific constraints:

### Batch rules (per model)

**Confirm per-shot limits from `studio_get_use_case_input_schema({ useCaseId, modelId })`**;
historical [batch profiles](references/execution-audit.md#batch-profiles) are lookup material,
not a live contract. The planner's configurable batch limits and the `MULTI_CUT` consequence
are in the [batch-planning reference](references/batch-planning.md).

### Batch formation algorithm

1. Group consecutive shots only when they share the **same model, generation use case, and input contract**. `GRID`, `MULTI_CUT`, `SEQUENCE`, `SINGLE`, `DUAL_FRAME`, and `T2V` are separate input contracts unless the live schema explicitly supports batching them together.
2. Within each compatible group, start a batch with the first shot and keep adding consecutive shots as long as the running duration and count remain under the model's ceilings.
3. The moment either limit is exceeded, close the batch and open a new one beginning with that shot.
4. A shot whose duration exceeds model max becomes a multi-segment batch (`SEQUENCE` forced).
5. Prefer closing batches at scripted cuts over arbitrary duration boundaries.
6. Never reorder shots. Batches are strictly contiguous ranges.

---

## Production summary

Report model assignments, archetype distribution, job counts, execution risks, and high-risk
cross-model boundaries. Report the intended final-edit runtime separately from the total planned
generated-material duration. Count every additional shot and alternate output in the latter, even
when it is an editorial substitute for another shot; make clear which outputs are alternates and
which extend coverage. The planned generated-video duration must be at least 1.2× the intended final-edit runtime, so the editor can select, trim, align, and pace the cut. For a 90-minute final, plan at least 108 minutes of generated clips; for a 1-minute final, plan at least 72 seconds. Count every alternate angle, emotional take, reaction/listener shot, insert, transition, and other candidate clip. Do not count still keyframes as video seconds or present generated duration as final cut runtime. Plan more when the screenplay or edit needs it. Use the [editorial coverage ledger](../mixio-pipeline/references/editorial-coverage.md) to avoid double-counting internal cuts or reused clips. Include all surplus outputs in job counts and batches. Follow `mixio-generate` and the user's stated generation authorization; do not make price estimates a planning gate.

---

## Persisting the plan

Persist each shot's model, `generation_use_case`, and input contract with `studio_revise_shot_specs`,
then write the completed Step 05 plan to `episode.metadata.pipeline`. The plan is a review
checkpoint, not an approval state. A chat “proceed” or prior authorization for the presented
scope is sufficient to continue; no `awaiting_approval` state or approval digest is required.
See the [field shape and writes](references/execution-audit.md#plan-persistence).

---

## Production plan checkpoint

Present the production plan, coverage totals, model choices, and known execution risks. Continue
on a clear chat confirmation or prior authorization for this scope. Do not require an additional
Studio status change or ask again for an already confirmed plan. If the user asks to proceed with
a documented advisory risk, record it and carry it into the generation prompt/evaluation when the
schema allows. A schema-invalid request, unresolved scope, or project-policy restriction remains
a technical constraint.

Persist `step_05: "complete"` when planning is complete, with the plan details for recovery. If
the plan changes materially after the checkpoint, show the changed portion and continue on the
user's confirmation or prior authorization for that revised scope. Step 06 handles any separate
billable-generation authorization under `mixio-generate`.

Announce the close with the production plan, for example:
`Step 05 — Shot Planning complete. 13 planned outputs (including 2 alternates) / 7 planning batches / 72.0s planned generated material for a 60.0s intended final edit. Please review the plan to proceed to Step 06.`

---

## Workflow

```
1. read confirmed breakdown (Step 03) + reference readiness findings from Step 04 + project settings + live model catalog
2. match each shot to the best model based on characteristics; read its live input schema and duration ceiling
3. classify each shot into one of 6 archetype families (GRID / MULTI_CUT / SEQUENCE / MASTER_ANCHOR_MULTI_SHOT / SINGLE or DUAL_FRAME / T2V), using the selected model ceiling
4. run execution audit (duration limits, action density, speaking rate, dialogue/voice readiness, audio-reference support, references, prompt @ mentions + URL-valued mentionMap)
5. prepare schema-valid job payloads (split/reassign unsupported durations, assign missing voice IDs when dialogue TTS is requested, plan TTS before video, embed @ mentions, bind URLs in mentionMap, remove orphan bindings); keep high-priority quality findings visible as accepted risks when the user chooses to proceed
6. group into contiguous batches per model-specific ceilings
7. emit PRODUCTION SUMMARY with archetype distribution, model assignments, job counts, and execution risks
8. studio_revise_shot_specs → persist plan in shot metadata; persist the complete plan and `step_05: "complete"` in episode metadata.pipeline
9. CHECKPOINT — present plan and risks; proceed on chat confirmation/prior authorization, then enter Step 06 under the user's generation authorization
```

## Notes
- **Always query the live catalog.** Model capabilities change. Use `studio_get_use_case_input_schema` for the authoritative duration contract and parameter support.
- Archetype classification is a recommendation. The user may override any assignment — record overrides in shot metadata.
- Cross-model batch boundaries are where `mixio-eval` should focus its post-generation checks.
- Duration adjustments during execution audit cascade batch boundaries. Re-batch after any duration change.
- Multi-keyframe sequence planning: for pre-locked shots from Step 03, prefer `production-generate-shot-keyframes` with `keyframe_count: 1` per beat rather than sequence planner regeneration.
