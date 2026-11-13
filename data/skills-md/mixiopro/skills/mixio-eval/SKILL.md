---
name: mixio-eval
description: "Run visual continuity and consistency evaluations on rendered media and catalog-supported reference images through the hosted Studio evaluator gateway."
version: 0.4.1
invoke: /mixio:eval
---

# Mixio Eval

Evaluate rendered media as a delivery review checkpoint, and evaluate reference-image candidates
during Step 04 only when the live catalog explicitly supports still-image
comparison. This skill uses the modern hosted Studio evaluator gateway. For
the director-led Continuity Checklist before rendering, use `mixio-continuity`.

Use the shared [director’s lens](../mixio-pipeline/references/directors-lens.md) for the evaluation question: does the result communicate the accepted shot’s purpose and connect to its neighbors? Apply only relevant craft checks—for example, cinematography for framing/light/movement, script supervision for state and screen direction, editing for transitions, and sound design when audio evidence is available. Use supported plan, shot-plan, shot, and expected-state context where available, and distinguish creative-direction mismatches from technical image defects.

## Boundary with `mixio-continuity`

Use `mixio-continuity` to write scene, shot, and transition checklist items and propose grounded corrections to the local plan before rendering. Use this skill
for post-rendered sequence evidence, or for a reference candidate only when a
listed profile and live contract accept still-image candidates plus the needed
approved-reference/expected-state evidence. When a request is ambiguous, route
it through `mixio-pipeline`; neither gate substitutes for the other.

## Scope and compatibility boundary

The canonical evaluation surface is:

| Hosted MCP name | Local stdio proxy | Mixio CLI command | Purpose |
| --- | --- | --- | --- |
| `evals_list_evaluation_catalog` | `studio_evals_list_evaluation_catalog` | `evals-list-evaluation-catalog` | Read the approved profile catalog for a confirmed project. |
| `evals_evaluate_media` | `studio_evals_evaluate_media` | `evals-evaluate-media` | Submit one background evaluation. |
| `evals_get_evaluation_result` | `studio_evals_get_evaluation_result` | `evals-get-evaluation-result` | Poll one existing evaluation run. |

`run_eval`, `run_evaluation`, and `get_evaluation_result` are deprecated
compatibility aliases only. Their stdio/CLI spellings are
`studio_run_eval`/`run-eval`, `studio_run_evaluation`/`run-evaluation`, and
`studio_get_evaluation_result`/`get-evaluation-result`. They exist for clients
that are pinned to an older hosted surface; they are not the pipeline contract.

The aliases accept the legacy `capability`, `videoUrl`, and `imageUrls` shape.
Legacy capability names are therefore an adapter concern, not canonical
profile or metric names. If a compatibility adapter is unavoidable, translate
the request once at that boundary, call one alias once, and poll the returned
run with the canonical result reader when the server permits it. Do not call an
alias and its replacement for the same run. If an alias cannot represent the
ordered keyframe, expected-state, or shot-plan context below, mark the strict
continuity gate unavailable rather than silently downgrading it.

## Prerequisites and scope

- Resolve and confirm the Studio `projectId` before evaluation. If it is not
  established, call `studio_list_projects`, show the numbered list in the same
  message as the question, and ask the user to choose. Never invent a project
  ID or create a project to avoid the choice.
- Evaluation submission is billable. Confirm the planned evaluation unless the
  session already authorizes it. Catalog and contract reads are non-billable;
  this skill's examples and checks must not submit a live evaluation.
- Local stdio clients use the `studio_` prefix. Direct hosted `/api/mcp`
  clients use the bare hosted names. The CLI exposes the same names in
  kebab-case.
- Upload local media through `mixio-workspace`, with the known project and
  organization scope, and pass permanent public URLs to the evaluator. Public
  `source-url` values must use HTTP(S) and must not target private or loopback
  hosts.

## Discover the live contract and catalog

Read the current contract before using an unfamiliar tool:

```text
studio_get_contract({ target: "tool", toolName: "evals_evaluate_media" })
studio_get_contract({ target: "tool", toolName: "evals_get_evaluation_result" })
studio_evals_list_evaluation_catalog({ projectId })
```

The contract currently exposes an open evaluator configuration surface for
`profile`, `metrics`, `skills`, `plan`, `shot-plan`, `keyframe-continuity`,
`shots`, `modifiers`, and `output-schema`. The live catalog owns the meaning and
availability of those values. Do not invent required metric identifiers, copy the old `capability`
enum into a modern request, or make a profile-specific metric mandatory unless
the catalog response says so.

## Canonical request contract

The modern evaluator request schema requires `project-id`, a non-empty ordered `inputs`
array, and a numeric `threshold` from `0` through `1`. This skill adds two
intentional strictness rules: always select an explicit catalog `profile`, and
always provide a non-empty `prompt`. Omitting either lets a server default hide
which quality gate was actually run.

The modern evaluator payload spells project scope `project-id`, as in the
example. A Studio MCP transport exposes the same scope as `projectId`; map it
at the transport adapter boundary and never send both spellings in one modern
request. For a local call, convert
`{ "project-id": wire["project-id"], ...wire }` to
`{ projectId: wire["project-id"], ...wireWithoutProjectId }` before calling
`studio_evals_evaluate_media`; the hosted/CLI adapter converts it back to the
wire spelling. Polling similarly maps `projectId`/`runId` at the tool boundary
to the wire request's `project-id`/`run-id`.

The canonical request uses `project-id`, an explicit catalog `profile`, ordered
`inputs`, a non-empty `prompt`, a threshold, and background execution. The
complete deterministic request is kept in the JSON example below.

Each input must have:

- a unique kebab-case `input-alias`;
- a live-contract `role` such as `candidate`, `reference`, `expected-state`,
  or `sequence`;
- a live-contract `type` such as `image`, `video`, `text`, `sequence`, or a
  canonical reference type; and
- exactly one source: `source-url`, `asset-id`, or `reference-id`.

Use `view` only when the source is a view the live contract accepts. The
pipeline treats `profile`, `prompt`, `threshold`, and `background: true` as
required, even where the wire schema leaves some of them optional. Keep
`execution-mode: "background"` and `stream: false` only when the current
contract or client requires the explicit forms; do not request streaming.

The complete deterministic request example is
[references/modern-evaluation-request.example.json](references/modern-evaluation-request.example.json).

## Reference-pack readiness

Use `image-character` for a character turnaround or wardrobe sheet. Treat face
identity, anatomy, hands/limbs, wardrobe/accessories, and generation artifacts
as required quality gates; a clean aggregate score must not hide a deformed
face, extra limb, fused hand, or unexplained costume change. For a multi-view
sheet, pass the views as ordered image inputs and include the
`reference-coverage` context. Evaluate each script-required age/clothing
variant as its own pack against the approved character default; retain the
variant name, input aliases, findings, repair feedback, and human decision with
the inventory row. Evaluator output is evidence for review, not approval.

Use `image-location` for a location reference pack. It requires at least two
image views, a `location-reference` anchor, and explicit coverage metadata. Use
an approved image from the same configuration as the anchor when available. If
no approved image exists for that configuration yet, use a representative
staged candidate as the evaluation-only anchor only when the live evaluation
contract accepts its URL as a `location-reference` input. Compare the candidate
views against their declared orientation records, landmarks, and world axes;
keep all candidates outside Cast & World until the user selects one in chat or
has already authorized that exact candidate. Never use an image from another
configuration just to fill the anchor role. If no valid anchor input is
available, report the evaluation limit and offer to continue with partial
evidence; do not claim the pack was fully evaluated.
This `location-reference` is the pack's evaluation anchor, distinct from the
per-scene KEYFRAME `anchorRef` generated later in Step 04.
Record each view's camera position, facing direction, visible landmarks, and
world-to-screen mapping. Add `shot-zones` when the shot plan needs a reverse,
overhead, underslung, top, bottom, or detail view. Do not generate every angle
by habit: required views come from the planned camera zones. If only one view is
script-required, add only the second view needed to satisfy the evaluator's
minimum for that pack. Evaluate every script-required location configuration
as a separate pack; map each input alias
to its exact variant and image label/orientation record. Compare views and
configurations for stable geometry, world axes, landmarks, and palette, and
record intentional spatial or environmental changes in the inventory.

Keep these coordinate systems distinct: `world-left`/`world-right` are fixed
to the location; `camera-left`/`camera-right` may reverse; `character-left`/
`character-right` are anatomical; and `screen-left`/`screen-right` belong to
one shot. A reverse angle is not a defect by itself. A landmark crossing the
declared axis, or changing color/shape between adjacent views without an
intended change, is.

The coverage context is trusted evaluator input, not free-form prompt prose.
Missing required aliases, unbound views, or unsupported location geometry fail
the readiness gate rather than being filled in by model inference.
See [references/reference-readiness-request.example.json](references/reference-readiness-request.example.json)
for a complete location-pack request.

## Human-in-the-loop repair plan

Request the reusable `human-review` extension when a review may produce a
repair recommendation:

```json
{
  "mode": "extend",
  "namespace": "human-review",
  "schema": { "...": "inline the contents of the linked JSON schema here" }
}
```

Use the schema in
[references/human-review-repair-plan.schema.json](references/human-review-repair-plan.schema.json).
The request must embed that document as the `schema` object; the path above is a
repository reference, not a value sent to the evaluator.
It is deliberately manual-only. Every proposed action must cite source
finding IDs, evidence links, input aliases, and an optional frame/time range;
declare the narrowest repair scope (`segment`, `shot-boundary`, `shot`,
`sequence`, or `full-delivery`); state what references/keyframes must be
preserved; and define the evaluation to run after the repair. The evaluator
must never return an approval or an executable command.

Interpret the result as a review packet:

- `proposed` + `human-approval: required` means present the recommendation as a
  checkpoint; the user's chat decision is sufficient to proceed;
- `no-action` means retain the current render and record why;
- `time-range-ms`, `frame-range`, and `shot-ids` are localization hints, not
  an authorization to regenerate;
- if the evidence is insufficient, propose `sequence` or `full-delivery`
  review rather than inventing a precise segment.

For video repair, use the finding's time/frame range to identify the smallest
affected segment. When evaluation does not localize the fault, inspect a
timecoded still grid sampled from the video and use the visible evidence to
bound the segment. Keep unaffected approved footage and references. Recommend
full-shot or broader replacement only when the fault spans that scope, the
evidence cannot isolate it, or the selected generation route cannot produce a
smaller segment; state which case applies. Before any regeneration, show the
exact replacement prompt and inputs for each job and get the user's
confirmation. An evaluation result or repair plan never authorizes generation.

The generic core findings remain authoritative for verdict and evidence. The
repair plan is advisory and must be preserved alongside the evaluation receipt
and the human decision.

For reference candidates, keep the evaluation receipt, input aliases, findings,
human feedback, and chat selection/rejection decision linked to the corresponding
variant/view inventory rows in episode
`metadata.pipeline.reference_pack_inventory`. Attach only candidates the user
selects in chat; no separate Studio approval status is required. If a rejected
candidate was attached earlier, use `mixio-references` to remove it from every
active store and clear any matching `thumbnailUrl`/`previewUrl` through a
documented operation, then read the reference back; do not treat a rejection
note as cleanup. If removal cannot be verified, report that Studio may still
select that image and offer a compatible input/method that excludes it. Continue
when the user accepts the limitation and the job schema allows it; never claim
the rejected image was removed.

The example also requests an explicit `output-schema` wrapper for a structured
continuity extension: `review-verdict`, `worst-transition`,
`blocking-findings`, and per-transition `transitions` containing localized
`transition-findings`. The stable result already owns the reserved core
`verdict` field,
so an extension must use its own lower-kebab-case names and cannot redeclare
core properties. This asks the evaluator for a response shape; it does not
replace profile-owned semantics, and it never replaces client-side result
normalization and gate validation.
Use `{ mode, namespace, schema }` for an inline extension; the JSON Schema
document belongs under `schema`, not at the `output-schema` root.
Treat unsupported or omitted output-shape fields as contract uncertainty and
retain the raw `evaluation` payload.

## Ordered keyframe/video evidence

`inputs` is an evidence sequence, not an unordered attachment tray. Preserve
the production order in the array and make that order unambiguous in both
aliases and the prompt:

1. For every strict adjacent transition `shot-N → shot-N+1`, put the final
   keyframe for `shot-N` immediately before the first keyframe for `shot-N+1`,
   bind both through `role: "candidate"`, and describe their concrete
   `frame-index` or `time-ms` in the top-level `keyframe-continuity` context.
   Use `role: "sequence"` for the general `sequence-storyboard` lens.
2. Add the rendered candidate with `role: "candidate"` and `type: "video"`
   when judging a video. Keep its alias in the prompt, for example
   `@shot-02-video`.
3. If expected state is hosted as an evaluator-readable artifact, add one
   `role: "expected-state"`, `type: "text"` input using its public URL,
   `asset-id`, or `reference-id`. This is evidence/context, not a substitute
   for the ordered frames.
4. Use the optional `shots` array for stable shot IDs and descriptions, and
   the open `shot-plan` object for transition expectations. Keep shot IDs in
   the same order as the evidence and never rely on lexical alias sorting.
5. Mention every active input alias in the prompt as `@alias`. This binds the
   written review request to the evidence list without adding generation-only
   fields such as `slotTags` or `mentionMap` to the evaluator request.

The recommended `shot-plan` convention is skill-side context passed through
the live open object; it is not an invented required evaluator schema:

```json
{
  "sequence": ["shot-01", "shot-02"],
  "transitions": [
    {
      "id": "shot-01-to-shot-02",
      "from": "shot-01",
      "to": "shot-02",
      "expectedState": {
        "screenDirection": "Maya travels left-to-right; preserve the established axis",
        "spatialGeography": "door is background-left; table is foreground-right",
        "identity": "same Maya look and facial identity",
        "pose": "right hand remains raised toward the table",
        "wardrobe": "blue jacket and silver watch remain unchanged",
        "propState": "red cup remains in the right hand",
        "palette": "cool blue room with a warm red-cup accent",
        "lighting": "soft daylight from camera-left; exposure holds",
        "camera": "wide to right over-shoulder; preserve eyeline and geography",
        "temporalArtifacts": "no flicker, geometry warp, ghosting, or frame jump"
      },
      "intentionalChanges": [
        {
          "kind": "editorial-cut",
          "description": "wide shot cuts to an over-shoulder angle"
        }
      ]
    }
  ]
}
```

For cross-angle checks, describe the scene geography rather than only saying
“keep the subject consistent”: name the axis, screen direction, depth order,
landmarks, frame regions, eyeline, and any deliberate axis crossing. Record
identity, pose, wardrobe, and prop state separately from geography so a subject
can remain the same while a handoff or prop placement still fails.

Carry applicable items from the approved [Continuity Checklist](../mixio-continuity/references/checklist-template.md) into the live contract's supported prompt, `shot-plan`, `shots`, or plan context. Provide the actual reference and neighboring media evidence the selected profile needs. Report observed deviations against checklist items, including absent reactions/connective coverage and broken emotional or causal progression; a planning checkbox does not prove rendered compliance.

## What the strict continuity review covers

The `keyframe-continuity` prompt and `shot-plan` should make these dimensions explicit for every
adjacent transition and for any cross-angle comparison:

- screen direction and spatial geography, including relative subject/prop
  position and the 180-degree axis;
- identity, pose, wardrobe, prop state, relative scale, and visible proportions;
- requested visual style and surface/material treatment, including consistency
  with photorealistic/hyperrealistic or stylized intent;
- for photorealistic/hyperrealistic human imagery, natural skin surface detail
  at a scale the frame can resolve, with no poreless smoothing, airbrushing, or
  waxy/plastic gloss; in video, check that texture and complexion stay stable
  through motion and across cuts;
- palette and color relationships;
- lighting direction, quality, and exposure;
- unexpected content, missing signature features, and visible image defects;
- camera continuity, including framing, lens impression, movement, eyeline,
  and intentional angle changes; and
- temporal artifacts such as flicker, geometry/identity morphing, ghosting,
  frame jumps, or other unstable motion.

Declare editorial cuts and state changes in `intentionalChanges` with the
affected transition and the exact change (for example, a wardrobe change,
prop pickup, time-of-day change, or deliberate axis crossing). A declared
change is exempt only for the named dimension; undeclared drift across the
same transition remains a failure. A hard cut does not excuse within-shot
flicker, temporal artifacts, or an unexplained state change.

For a requested realistic human finish, a clear plastic/waxy or poreless
beauty-filter appearance is a high-priority visual defect, even when identity or
composition scores are otherwise strong. Localize the finding to the affected
face, frame range, or transition and recommend a correction/re-render. If the
user elects to proceed, record the accepted deviation without changing the
evaluation result. Apply this only when supported by the
locked style and visible evidence; retain deliberately stylized or glossy skin
when that treatment is intentional.

A `MULTI_CUT` render is one video containing deliberate in-shot cuts: declare
**every** cut boundary from the shot's `cuts[]` as its own `editorial-cut`
entry with the cut's timestamp range and planned change (for example,
`"Cut 2 at 00:04.5: wide cuts to insert CU of hands"`). Undeclared cut
boundaries are evaluated as transitions and fail like any other break.

## Profile routing

Use one explicit profile per request, selected from the live catalog. If a
production needs more than one quality lens, submit separate approved runs and
retain each receipt; do not put an invented profile list or metric enum into a
single request.

| Profile | Use as the primary lens for | Not a substitute for |
| --- | --- | --- |
| `image-character` | Character turnarounds and candidate sheets, including deformation, face, hands, wardrobe, and identity checks. | A rendered video-character or final delivery review. |
| `image-location` | Location packs with world-axis, landmark, orientation, lighting, palette, and artifact checks. | The shot-level keyframe continuity gate. |
| `keyframe-continuity` | Strict ordered keyframe evidence and adjacent-transition gating with expected state. | A general storyboard review or final delivery QC. |
| `sequence-storyboard` | General storyboard/keyframe visual review and sequence context. | The strict adjacent-transition gate or final delivery QC. |
| `video-multi-shot` | A rendered multi-shot candidate, cuts, and cross-angle geography — the primary lens for `MULTI_CUT` renders (10–15s multi-cut shots). | Character-only review. |
| `video-character` | Identity, pose, wardrobe, and character-state continuity. | Full temporal/delivery review. |
| `video-general` | General visual artifacts and broad palette, lighting, camera, motion, style/material, or scale review only when the catalog exposes that coverage. | A transition-specific gate when no ordered evidence is supplied. |
| `delivery-qc` | Final candidate delivery/readiness review after continuity checks. | The strict adjacent-keyframe continuity check. |

These are catalog profile identifiers, not a new capability enum. The catalog
may provide profile-specific skills or metrics; pass those only when the live
catalog contract returns them. A high aggregate or average result never
overrides a localized blocking transition finding.

Before submission, derive the required review dimensions from the locked project
style and each shot's expected state. Check that the selected profile returns
evidence for those dimensions. If it does not, use another compatible catalog
profile as a separate, confirmed run or route the uncovered dimensions to human
review; report the missing evidence and keep the evaluator result accurate. The user may accept the documented limitation and continue; do not represent uncovered dimensions as evaluated.

### Reference-image comparison for Step 04

The reference audit may use this evaluator for a required look/view candidate
only if the current catalog and tool contract explicitly support `image`
candidate inputs and an image `reference` or compatible expected-state input.
Do not infer that `sequence-storyboard`, `video-general`, or a video-only
profile accepts standalone sheets. If no suitable profile exists, use available
vision or human visual review and leave the row unresolved when neither is
available.

When a relevant human-approved canonical identity/world reference exists,
compare each required candidate look/view with it and the script's declared
variant purpose. Use the approved `workflow.status` and exact inventory/look
binding to pick a baseline; don't compare unrelated images or treat an
in-review candidate as the authority. When no approved baseline exists, use
only confirmed screenplay, inventory, locked-style, or structured expected-state
evidence; never treat the candidate itself or another unapproved candidate as
its own baseline. The prompt and expected-state evidence should name the
relevant invariants and intentional differences and request separate findings
for:

- requested visual treatment, including photorealistic/hyperrealistic versus
  stylized rendering, skin and material texture, and visible synthetic defects;
- identity, signature features, wardrobe/state and cross-view consistency;
- explicit height/relative-scale constraints and anatomy/proportions;
- persistent location layout, landmarks and depth relationships;
- lighting direction/quality/exposure and palette/color relationships; and
- hallucinated people, objects, text/logos, omissions, warping or other image
  defects.

Judge each dimension only against evidence actually supplied: script, locked
project style, structured reference details, approved baseline images, relevant
scene anchors, or explicit scale records. A variant may change palette or
lighting when its declared purpose calls for it; preserve the non-varying
identity/world invariants. Record dimensions the profile does not support as
unreviewed instead of implying that its aggregate score covered them. Evaluation
does not select or mutate a reference; preserve its raw result with the audit.
The user's chat decision controls whether a candidate is selected and attached;
do not require a separate Studio approval status.

## Submit and poll

Submit the canonical request once:

```text
const { ["project-id"]: projectId, ...wireWithoutProjectId } = wire;
studio_evals_evaluate_media({ projectId, ...wireWithoutProjectId });
```

Keep the returned opaque `runId`, then poll with:

```text
studio_evals_get_evaluation_result({ projectId, runId })
```

Poll until the outer `terminal` is `true`. The normalized lifecycle statuses
are `queued`, `in_progress`, `completed`, `failed`, and `cancelled`. A
successful tool call (`ok: true`) only means that submission or result lookup
succeeded; it does not mean the quality review is complete. Pending results may have
`threshold: null`; a terminal result must report the applied threshold. Do not
resubmit while a run is pending or after an uncertain receipt—reconcile the
existing run first.

## Result interpretation and checkpoint

The result envelope is stable, but the nested `evaluation` object is
provider/profile-owned. Retain the raw `evaluation` object and normalize only
the fields the selected profile actually returns. For the pipeline decision,
each finding should be localized to a transition or shot and retain:

```text
transitionId · dimension · classification · blocking
```

This is a pipeline-side interpretation record, not an additional submission
schema. Use `classification: intended_change` for a declared cut/state change,
`accidental_drift` for an unexplained continuity break, `technical_artifact`
for temporal/render instability, and `unlocalized` when the evaluator does not
identify the affected shot or transition.

Use these checks to recommend whether to repair or accept the output. They describe a strong review result, not a delivery gate. A severe finding does not silently change the evaluator verdict, and it does not create a separate Studio approval state; present the evidence and let the user choose whether to accept a documented deviation or request a repair:

1. the run is terminal and completed;
2. the provider/profile decision is acceptable at the requested threshold;
3. every required visual dimension is covered by profile output or resolved by
   a recorded human review;
4. every required adjacent transition has localized evidence;
5. the worst transition is acceptable; and
6. no finding is blocking, accidental drift, technical artifact, or an
   unexplained/unlocalized failure.

The worst transition and any evaluator-classified blocking finding take precedence over
the aggregate score. They do not prevent the user from accepting a documented deviation.
If the user says to proceed, record that decision without changing the evaluator's verdict.
A
single severe position contradiction, identity/wardrobe/prop jump,
palette/color or lighting/exposure jump, camera-geography break, or temporal
artifact remains a serious finding even when the overall average is high.
Declared intentional changes are not accidental failures, but they must still
be present in the shot plan and must not mask failures in other dimensions.

Retain the request JSON, ordered aliases and source IDs/URLs, prompt, selected
profile, threshold, `runId`, and terminal response with the production review
record. Redact credentials and avoid copying private media into public skill
examples.

## Tips / Pitfalls

- Keep `keyframe-continuity` for strict ordered-transition checks; `sequence-storyboard` is a general storyboard lens.
- Treat `project-id` versus a Studio tool's `projectId` as an explicit transport adapter boundary; do not mix them in one payload.
- Put custom JSON Schema under the `output-schema.schema` wrapper with a lower-kebab `namespace` and an allowed `mode`.
- A submitted run is not a completed review: poll the same `runId`, inspect localized findings, and preserve the raw evaluator response.
