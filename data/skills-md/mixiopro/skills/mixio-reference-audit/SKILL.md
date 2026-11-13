---
name: mixio-reference-audit
description: "Audit an accepted shot plan against reference looks and views for visual readiness, plus Cast & World completeness, consistency, duplicates, and metadata quality before generation. Builds sheets: mixio-sheets; creates/edits entries: mixio-references. Unclear which step you need → mixio-pipeline."
version: 0.3.0
invoke: /mixio:reference-audit
---

# Mixio Reference Audit

Step 04 of `mixio-pipeline`, after the shot plan has been confirmed in chat and synced. It compares the accepted plan with existing references and images, then runs again after confirmed reference changes. The question it answers: **are the references this episode will generate against actually ready?** Missing items are production-readiness findings; they do not block local planning or automatically block generation when the user accepts the limitation and the selected schema/project policy permit the job.

A missing character image found here is one asset issue. The same gap found in Step 06 affects every shot that character appears in — re-generated blind, or blocked until someone notices.

## Prerequisites

- A project with references registered (`mixio-references`)
- The accepted, persisted shot plan (pipeline Step 03), including linked characters, locations, props, appearance state, and camera direction
- The source screenplay/script selected during pipeline setup, for source requirements and provenance
- The current Cast & World and available images; missing sheets and anchors may be reported before they are built

## What it checks

Seven categories, run in order. Each produces a finding list and a checkpoint with recommended fixes, likely impact, and accepted limitations. Findings inform the user's decision; only an actual project-policy or input-schema constraint prevents the dependent action.

### 1. Completeness — script demand vs reference supply

Read the accepted plan and persisted scene/shot relations, plus the episode's native `SCREENPLAY` and episode record. Use a non-empty screenplay `body`, including drafts; use episode `script` / `metadata.fullScript` only when no usable screenplay body exists, following `screenplay-grammar.md`. Extract scripted entity requirements from the source, then add inferred coverage and actual camera zones from the accepted plan. Cross-reference that combined demand against `studio_list_references({ projectId })`.

For the final pipeline audit, check `metadata.pipeline.reference_pack_inventory`. If it is absent, unconfirmed, or incomplete, report `REFERENCE_PACK_INVENTORY_MISSING` and explain what cannot be verified. Offer to build the inventory or continue with the user-accepted uncertainty; chat “proceed” is sufficient to continue when the model schema and project policy allow it. Never claim completeness without evidence. Do not let a single image or `Default` look pass by itself. Compare screenplay-evidenced age/costume combinations and location configurations, plus actual camera zones and coverage in the accepted plan, with the inventory and reference data. A default-only pack passes when the accepted plan requires no other look/configuration. CAPS extraction alone cannot establish that a costume combination, location configuration, or angle pack exists.

**Judge `MISSING_IMAGE` by `hasImage` — never by `thumbnailUrl`/`previewUrl`.** `list_references` returns `thumbnailUrl`/`previewUrl` alongside it, and it's easy to grab the wrong pair: those two are a card-preview column that nothing populates when a Look is attached, so a reference with real turnaround images routinely still shows both as `null`. Reading those as the presence signal produces a false `MISSING_IMAGE` on every reference in the project — a wrong blocking finding on the roster's healthiest data, not its worst. `hasImage` (see `mixio-references`) is the real signal.

| Finding | Meaning |
|---------|---------|
| `MISSING_REF` | Entity mentioned in script has no matching reference element at all |
| `MISSING_IMAGE` | Reference exists but `hasImage` is false |
| `MISSING_IMAGE_HIGH_USAGE` | Same, but the entity appears in ≥3 shots or ≥2 scenes — generation will be inconsistent without a visual anchor |
| `NO_PRIMARY_LOOK` | Reference has variant images but none marked `isPrimary` or `isDefault` — prompt assembly picks arbitrarily |
| `MISSING_REQUIRED_VARIANT` | A screenplay-required character age/clothing look or location configuration has no approved variant |
| `MISSING_REQUIRED_VIEW` | A required location configuration lacks a camera-view image mapped to a planned shot zone |
| `SCRIPT_REQUIREMENT_UNMAPPED` | A screenplay-evidenced character look, location configuration, or camera zone has no confirmed inventory row |
| `REFERENCE_PACK_INVENTORY_MISSING` | The pipeline inventory is absent, empty before demand reconciliation, or unconfirmed, so variant/view completeness cannot be established |
| `REFERENCE_PACK_NOT_CONFIRMED` | The user has not selected a required reference or variant pack in the current chat/record; a chat confirmation counts even if Studio still shows `draft` or `in_review` |
| `REJECTED_MEDIA_ACTIVE` | A candidate rejected by evaluation or human review remains in an active reference image store or is still shown as its card preview |

```
Completeness — 12 references checked
  ✅ TONY         — 1 primary look, 3 images
  ✅ POPPY        — 1 primary look, 2 images
  ⚠️  CEREAL BOWL — MISSING_IMAGE (appears in 2 shots)
  ❌ HALLWAY DOORWAY — MISSING_REF (mentioned 4× in script)
```

### 2. Visual reference readiness — sheet integrity and coverage

Build the review set from every screenplay-required row in the confirmed
`metadata.pipeline.reference_pack_inventory`: exact reference, look/configuration,
view, and image. Include all candidate images attached to each required row;
do not audit or block unrelated, unused project looks. Compare a candidate with
its relevant approved baseline image when one exists (for a character, usually
the approved canonical identity sheet; for a location, the approved view or
configuration that shares its stable geometry). Also compare sibling views and
variants when their relationship is meaningful. Use the exact row's declared
reason for the look/configuration to distinguish intended changes from drift.
Do not treat drafts or in-review images as an approved baseline, and do not let
an image's approval status imply it passed this visual review.

Use only evidence that applies to the row: the screenplay and confirmed variant
reason; the locked project style in `settings.studio` (including
`visualStyle`, `toneAndMood`, `cinematographyDirection`, and
`defaultStylePrompt` when present); structured reference details; an approved
baseline; and an applicable scene anchor. Keep the following checks separate so
one strong similarity score cannot hide a specific contradiction:

- **Style and materials:** Match the requested medium and realism level,
  including photorealistic/hyperrealistic versus stylized treatment, detail,
  and surface/material rendering. Plastic or waxy skin is a defect when it
  conflicts with the requested realism or material treatment; for an explicit
  photorealistic/hyperrealistic character row, clear poreless smoothing,
  airbrushed skin, or plastic/waxy gloss is a blocking visual contradiction.
  Preserve that finish only when it is an intentional part of the locked style.
- **Lighting and palette:** Compare light direction, quality, temperature,
  contrast, exposure, and shadow behavior, plus palette and color relationships.
  Treat a change as intentional only when the screenplay or confirmed row says
  that the look changes time, weather, mood, or lighting. Check sibling views
  for continuity under the same declared conditions.
- **Identity and anatomy:** Across each required character look/view, check face,
  age, build, hair, skin, distinctive features, proportions, wardrobe, and
  accessories. Mark hidden or off-frame features unobservable. Flag deformation,
  extra or fused limbs/fingers, warped joints, hallucinated accessories, or
  unexplained silhouette changes; an aggregate score cannot waive these.
- **Scale:** Compare visible height or relative scale only with explicit source
  evidence such as screenplay facts, structured height details,
  `metadata.scalingLabel`, a `SCALING_SHEET`, or another confirmed measurement.
  Account for perspective and framing; never infer an exact height from an
  image alone or invent scale metadata to make a candidate pass.
- **Location continuity:** Compare each required configuration and view with its
  declared layout, depth axes, landmarks, entrances, and other persistent
  geometry. A reverse angle or declared day/night configuration may change
  framing, light, and palette; it must preserve the world geometry and every
  other invariant the row does not authorize changing.
- **Hallucinations and defects:** Check for unexplained people, props, text or
  logos, missing signature features, duplicate or merged features, impossible
  geometry, seams, severe blur, inconsistent materials, and other visible
  defects that would mislead downstream generation.

Record each finding against the exact reference/look/view/image and include the
visible evidence, governing source or invariant, confidence, severity, and safe
next action. A high-confidence contradiction of an explicit script fact,
locked style, approved baseline, declared cross-view invariant, or scale record
is **BLOCKING**. Subjective, weakly observable, or source-ambiguous impressions
are **ADVISORY** for human judgment. Never auto-edit a reference or change its
approval state from this audit.

For each required location variant/configuration, compare `depthAxes`, stable
landmarks, and every attached orientation record. Require the camera looks
needed by that configuration's shot zones, including a reverse/opposite-axis
view where the shot plan crosses the line. Validate world-left/right separately
from camera-left/right and screen-left/right. Every location pack sent to
`image-location` must meet that profile's minimum view count and have explicit
`reference-coverage` aliases mapped to its exact variant and image labels.
Missing coverage or a misbound view is **BLOCKING**; unneeded
top/bottom/overhead/underslung/detail views are not failures.

Compare variants against the location inventory's declared invariants (such as
building silhouette, fixed entrances, window/door placement, and world axes).
Treat changes as intentional only when the screenplay or user-confirmed
inventory names them. High-confidence geometry, landmark, palette, or
orientation drift that contradicts an explicit invariant is **BLOCKING**;
subjective or source-ambiguous drift is **ADVISORY**. A rejected candidate must
never remain in `referenceVariants`, legacy `characterDetails.looks`, or flat
`attachments`, and must not remain in top-level `thumbnailUrl`/`previewUrl` as
the card image. Retain its feedback and evaluation receipt outside the active
media stores. Read the reference back to verify removal before clearing the
finding; if a rejected preview cannot be cleared through a documented
operation, do not reuse that reference pack for generation. Offer another clean reference or a compatible route that omits it; continue unrelated planning and generation. Report that the rejected asset could not be safely removed, and never claim the pack is clean.

If no vision-capable reviewer is available, use a compatible still-image
evaluation profile only after checking the live catalog and contract and
receiving confirmation for the billable submission. Do not assume a video or
storyboard profile accepts reference sheets. If neither visual path is
available, record `VISUAL_REVIEW_UNAVAILABLE` for each affected required row,
        leave its visual status unresolved, and keep the Step 04 readiness audit open. A metadata-only
check is not a visual pass. Report the unresolved row and its limitation; continue
when the user accepts it or with unaffected work. Record the choice and rationale
in the working audit record. Evaluator results are evidence for human review, not
an approval state.

| Finding | Meaning |
|---------|---------|
| `STYLE_MISMATCH` | Candidate conflicts with the locked style or script's treatment |
| `LIGHTING_MISMATCH` / `PALETTE_MISMATCH` | Lighting or color conflicts with the applicable confirmed evidence without an intended variant change |
| `SCALE_OR_PROPORTION_CONFLICT` | Visible scale or proportions contradict explicit source evidence |
| `IDENTITY_OR_VARIANT_DRIFT` | Identity or other stable character invariants drift, or the candidate fails its declared look purpose |
| `LOCATION_GEOMETRY_DRIFT` | Persistent layout, landmarks, depth, or world axes change across required views without explanation |
| `HALLUCINATION_OR_IMAGE_ARTIFACT` | Unwanted content or a visible generation defect undermines the reference |
| `VISUAL_REVIEW_UNAVAILABLE` | A required row has no completed vision or compatible image-evaluation review |

### 2.5 Scene-anchor cast and position coverage

Compare each scene anchor and its location position guide against the accepted shot plan, complete screenplay cast ledger, and all `appears_in` relations. If the saved `metadata.pipeline.reference_audit.anchor_cast_ledger` is missing or stale, reconstruct it from those sources before comparing images. Report a per-scene matrix with canonical character/reference, source shot IDs or screenplay entrance cue, opening presence, first entrance/special condition, guide color/position, and visual-review status. Include special/cameo appearances, story-relevant background roles, off-screen entrances, exits, and returns; reconcile aliases to canonical identities. The opening anchor depicts only characters present at scene open. Later entrants must be represented in the guide by a reserved position/entry route but must not appear early. Distinct characters need distinct faces unless the screenplay explicitly calls for an intentional duplicate identity/role. Visually compare faces against the character sheets and each other. If no vision-capable reviewer or compatible image-evaluation path is available, mark the visual check unresolved; do not claim a pass.

| Finding | Meaning |
|---------|---------|
| `ANCHOR_CAST_OMISSION` | A character scripted as present at scene opening is absent from the anchor |
| `ANCHOR_EARLY_ENTRY` | A character whose entrance occurs later is already visible in the opening anchor |
| `ANCHOR_UNSCRIPTED_PERSON` | The anchor contains an unaccounted-for person |
| `POSITION_GUIDE_MISSING` | A multi-person location/scene has no color-coded translucent position guide, or the guide omits a character/entry zone |
| `FACE_COLLISION` | Two distinct characters appear to share a face without an intentional duplicate in the screenplay |

Persist the matrix and source evidence with `reference_audit` in the existing free-form `metadata.pipeline` record:

```json
{
  "sceneId": "scene-id",
  "sceneNumber": 2,
  "characters": [
    {
      "referenceId": "character-id",
      "name": "MAY",
      "sourceShotIds": ["shot-2-4"],
      "openingPresence": false,
      "firstEntrance": "shot-2-4",
      "entranceCondition": "enters through the side door",
      "guideColor": "violet",
      "guidePosition": "side-door entry zone",
      "visualReview": "reviewed"
    }
  ]
}
```

Treat these findings as high priority before shot generation. Present the exact cast/shot evidence and recommended correction; follow the normal user checkpoint for accepted limitations. Never silently add, remove, or duplicate a character.

### 3. Consistency — name/description vs image alignment

For each reference that has both structured details and at least one image, check for contradictions:

| Finding | Meaning |
|---------|---------|
| `GENDER_MISMATCH` | `characterDetails` implies one gender but attached image presents as another |
| `AGE_MISMATCH` | Description says "child" / "elderly" but image shows a different age bracket |
| `BUILD_MISMATCH` | `build` field contradicts what the image shows |
| `DESCRIPTION_CONFLICT` | `description` or `visualAnchor` text contradicts visible features in a required attached image |

This check is **advisory, not blocking** — it requires visual interpretation which may be wrong. Flag for human review rather than auto-fixing.

Implementation: inspect every required image with vision or a compatible,
confirmed evaluation. Compare against `characterDetails.build`, `.age`, `.hair`,
`.skin`, `.distinctiveFeatures`, the exact look purpose, and the approved
baseline. If no visual reviewer is available, record
`VISUAL_REVIEW_UNAVAILABLE`; do not report a metadata-only pass.

### 4. Duplicates — fuzzy matching across the roster

| Finding | Meaning |
|---------|---------|
| `LIKELY_DUPLICATE` | Two references of the same type with names within edit distance 2, or one name is a substring of another |
| `ALIAS_CANDIDATE` | Script uses a name that matches an existing reference's description/bio but not its canonical name — likely an alias |
| `VARIANT_CONFUSED_AS_REF` | A reference whose name looks like `CHARACTER (state)` — e.g. `TONY (gala)` — or a location alias for a configuration already modeled under one canonical place, when the screenplay does not require an independent LOCATION identity |

```
Duplicates — 12 references checked
  ⚠️  LIKELY_DUPLICATE: "TONY" (CHARACTER) ↔ "TONY RUSSO" (CHARACTER) — same entity?
  ⚠️  ALIAS_CANDIDATE: script mentions "Antonia" — matches TONY's bio but no alias recorded
  ⚠️  VARIANT_CONFUSED_AS_REF: "TONY (GALA)" is a separate CHARACTER — should be a variant of TONY
```

Resolution plan:
- Merge duplicates: identify the canonical name and the alias to preserve; hand the plan to `/mixio:pipeline` Phase 2 or `mixio-references`, which reads `settings.references` before any update.
- Convert variant-as-ref: identify the parent reference and its candidate look; hand the plan to `mixio-references` for a policy-safe migration. Do not delete a reference from this audit.

### 5. Metadata quality — structured detail completeness

For each reference type, check the fields that downstream steps depend on:

**Characters** — generation needs these for consistent prompts:
| Field | Severity |
|-------|----------|
| `visualAnchor` | HIGH — the one-line visual identity used in every prompt |
| `build` | MEDIUM |
| `hair` | MEDIUM |
| `skin` | MEDIUM |
| `distinctiveFeatures` | LOW |
| `wardrobeNotes` | LOW |

**Locations** — sheets and anchors need these:
| Field | Severity |
|-------|----------|
| `setting` | HIGH |
| `lighting` | HIGH — anchor generation without this guesses |
| `palette` | MEDIUM |
| `mood` | LOW |

**Props** — less critical but helps consistency:
| Field | Severity |
|-------|----------|
| `category` | LOW |
| `material` | LOW |
| `significance` | LOW |

```
Metadata quality — 12 references
  ❌ TONY (CHARACTER): missing visualAnchor, hair
  ⚠️  APARTMENT (LOCATION): missing lighting, palette
  ✅ POPPY (CHARACTER): all HIGH/MEDIUM fields present
```

### 6. Policy compliance

Read `projects.settings.references` from `studio_get_project` and verify:

| Finding | Meaning |
|---------|---------|
| `POLICY_VIOLATION_CREATE` | Reference was created under `createPolicy: link_only` — should have been linked, not created |
| `VARIANT_VOCAB_VIOLATION` | A variant name exists outside the `variantVocabulary` set |
| `ALIAS_MATCHING_DISABLED` | Aliases are recorded but `aliasMatching` is false — they won't participate in breakdown matching |

This category is informational when the project has no policy set (the defaults are permissive).

### 7. Look-binding integrity — required looks are selected and bindings resolve

A shot or scene can bind a CHARACTER reference's age/clothing variant via `lookRef` on its `appears_in`/`presence` relation (`mixio-script-breakdown`). Compare post-breakdown relations with the confirmed character appearance mappings in `reference_pack_inventory`: when a row maps a shot's age/clothing state to a non-default approved variant, the relation must carry that variant's exact id/name. A missing binding silently renders the default, so report it before generation. The approved default needs no explicit `lookRef`. Location configuration and camera-view readiness are checked against the accepted plan's Step 04 inventory separately.

Pull bindings from `studio_get_production_context`'s `lookBindings` (or `studio_query_relations`
per relation). Pass relation `metadata` as a native object, never a JSON-stringified string, and
cross-reference each character `lookRef` against the target reference's `referenceVariants[].id` / `.name`.

| Finding | Meaning |
|---------|---------|
| `REQUIRED_LOOK_UNBOUND` | A confirmed inventory mapping requires a non-default character variant for this shot, but its appearance relation has no matching `lookRef` |
| `STALE_LOOK_REF` | `lookRef` names a variant id/name that no longer exists on the reference — renamed or deleted since the binding was made |

```
Look-binding integrity — 4 bindings checked
  ✅ Shot 7  → TONY:formal
  ❌ Scene 2 → TONY'S APARTMENT:night — STALE_LOOK_REF, no variant named "night" (renamed to "evening")
```

Resolution: rebind to the current variant name/id, or restore the variant under its old name.

## Report format

```
REFERENCE AUDIT — Project "Brooklyn Stories" — Episode 3
═══════════════════════════════════════════════════════════

References checked:    12 (6 CHARACTER, 4 LOCATION, 2 PROP)
Script entities:       15

Completeness:          2 MISSING_REF, 1 MISSING_IMAGE_HIGH_USAGE
Variant/view packs:    1 MISSING_REQUIRED_VIEW, 1 REJECTED_MEDIA_ACTIVE
Visual readiness:      1 PALETTE_MISMATCH (advisory), 1 VISUAL_REVIEW_UNAVAILABLE
Visual coverage:       7 required rows, 6 reviewed, 1 unresolved
Consistency:           1 GENDER_MISMATCH (advisory)
Duplicates:            1 LIKELY_DUPLICATE, 1 ALIAS_CANDIDATE
Metadata quality:      2 HIGH-severity gaps
Policy:                0 violations
Look bindings:         1 STALE_LOOK_REF

High-priority findings (resolve or accept at the checkpoint):
  ⚠️ HALLWAY DOORWAY — MISSING_REF — appears in 4 script lines, 0 references
  ⚠️ THE HOUSE / interior-living-room — MISSING_REQUIRED_VIEW — sofa-to-dining view has no selected image
  ⚠️ TONY — REJECTED_MEDIA_ACTIVE — rejected teen-formal candidate remains in legacy attachments
  ⚠️ CEREAL BOWL — MISSING_IMAGE_HIGH_USAGE — 2 shots depend on this prop
  ⚠️ HALLWAY:night.reverse — VISUAL_REVIEW_UNAVAILABLE — required view has not been visually reviewed
  ⚠️ TONY — missing visualAnchor — every prompt mentioning TONY will lack identity anchor

ADVISORY findings (review recommended):
  ⚠️  TONY — GENDER_MISMATCH — characterDetails.build="athletic female" but primary image presents male
  ⚠️  "TONY" ↔ "TONY RUSSO" — LIKELY_DUPLICATE
  ⚠️  script mentions "Antonia" — ALIAS_CANDIDATE for TONY

CLEAN references: POPPY, BED, BEDSIDE TABLE, NAPOLI POSTER, TABLET, PHONE, PERSIAN RUG
```

## Finding priority and user checkpoints

| Priority | Recommended response |
|----------|--------------|
| HIGH_PRIORITY | Recommend resolving before generation. If the user accepts the documented risk in chat, record the decision and continue when the selected schema and project policy allow it. |
| ADVISORY | Surface and record; continue. |

**High-priority criteria:**
- Any `MISSING_REF` for an entity appearing in ≥2 shots
- Any `MISSING_IMAGE_HIGH_USAGE`
- Any `ANCHOR_CAST_OMISSION`, `ANCHOR_EARLY_ENTRY`, `ANCHOR_UNSCRIPTED_PERSON`, `POSITION_GUIDE_MISSING`, or `FACE_COLLISION` before shot generation
- Any HIGH-severity metadata gap on a character appearing in ≥1 scene — a missing `visualAnchor` means every prompt mentioning that character lacks its identity anchor, no matter how few scenes it appears in
- Any HIGH-severity metadata gap on a location appearing in ≥1 scene — `setting` and `lighting` are required to render the scene's anchor frame without guessing
- Any `GENDER_MISMATCH` confirmed by both text and vision (not advisory-only)
- Any `STALE_LOOK_REF` — it renders the wrong look silently, with nothing in the UI to catch it before delivery
- Any `MISSING_REQUIRED_VARIANT`, `MISSING_REQUIRED_VIEW`, or `REJECTED_MEDIA_ACTIVE` for a script-required reference pack
- Any `REFERENCE_PACK_NOT_CONFIRMED` for media a planned shot will use
- Any unexplained cross-view or cross-variant location geometry/landmark drift
- Any high-confidence contradiction of the locked visual style, lighting/palette invariants, or explicit scale evidence
- Any confirmed character-sheet deformation, hallucinated anatomy, identity drift, or unexplained wardrobe/accessory/color break
- Any missing or misbound location view required by a declared shot camera zone
- Any required visual row without reviewed evidence or a recorded user override

These findings guide the checkpoint; they are not a second approval system. If the user says “proceed anyway,” record the accepted risk in the working production record and continue when technically and policy compatible. Do not write a guessed audit status or mutate unrelated Studio metadata just to record consent.

### Enrichment readiness review (after Step 03, before Step 05)

Check whether the **reference enrichment** phase (`mixio-sheets`) populated the load-bearing fields used by the accepted shots. The local breakdown does not write reference details; keep missing sheets and anchors visible as readiness findings after the confirmed shot sync. HIGH-severity fields are recommended for every character/location that appears in any scene:

**Characters — `characterDetails` (via `studio_update_reference`):**
| Field | Required |
|-------|----------|
| `build` | yes |
| `hair` | yes |
| `skin` | yes |
| `visualAnchor` | **yes** — the identity anchor, non-negotiable |

**Locations — `locationDetails` (via `studio_update_reference`):**
| Field | Required |
|-------|----------|
| `setting` | **yes** |
| `lighting` | **yes** |
| `spatialLayout` | yes |
| `depthAxes` | yes |

These are fields prompt materializers in Steps 05/06 use for visual continuity. If any are missing, report the likely effect and recommend the fix in Step 04 (`mixio-sheets`). If the user accepts the risk, continue when the selected model input schema and project policy allow it; do not describe an advisory finding as a system or Studio block.

## Findings and remediation

This audit does not mutate references or image assets. Its only write is the audit result in episode `metadata.pipeline.reference_audit` described below. Report each finding with its evidence, severity, affected shot/reference, and proposed next action. Route reference creation or enrichment to `/mixio:references`, and sheets/anchors to `/mixio:sheets`. Before any reference write, read `studio_get_project({ projectId })` and follow `settings.references.createPolicy`, `variantPolicy`, and the type-specific `variantVocabulary`. Do not mutate references, attach media, upload files, or submit image-generation jobs from this audit.

`MISSING_IMAGE_HIGH_USAGE` has no free synthetic fix. Report a permitted existing user-supplied asset when available; otherwise ask whether to upload, generate, or proceed with the limitation. Chat “proceed” or prior authorization is enough for the selected action; do not require a separate Studio approval status. Missing reference readiness is a finding, not a planning blocker. Continue into generation when the user accepts the risk and the selected model schema/project policy permit it. Any shot or binding change goes into an updated diff checkpoint; write on chat confirmation or prior authorization and re-run affected audit checks.

The remediation plan identifies the required action:

```
Fix: HALLWAY DOORWAY — MISSING_REF
→ studio_register_reference_entities({ projectId, references: [
    { type: "LOCATION", name: "HALLWAY DOORWAY", metadata: { description: "..." } }
  ]})
  Then: upload or generate a reference image via /mixio:sheets

Fix: TONY — missing visualAnchor
→ studio_update_reference({ projectId, referenceId: "<tony-id>",
    characterDetails: { visualAnchor: "Athletic Italian-American woman, late 20s, loose dark curls, warm olive skin" }
  })

Fix: TONY ↔ TONY RUSSO — LIKELY_DUPLICATE
→ studio_update_element({ projectId, elementId: "<tony-id>", updates: { metadata: {
    aliases: ["Tony Russo", "Antonia"]
  }}})
  Then: archive or delete the duplicate reference

Fix: STALE_LOOK_REF — TONY'S APARTMENT:night
→ studio_update_reference({ projectId, referenceId: "<apartment-id>", referenceVariants: [
    ...existingVariants,
    { name: "night", kind: "look", images: [{ url: nightUrl, isPrimary: true }] }
  ]})
```

After a user-confirmed fix is applied through the appropriate skill, **re-run the audit** to update affected findings and record which visual rows have evidence, are accepted with a known limitation, or remain unresolved.

## Persisting the result

```
studio_update_episode({ projectId, episodeId, updates: { metadata: { pipeline: {
  step_04: "complete",
  reference_audit: {
    checked: 12,
    blocking: 0,
    advisory: 1,
    clean: 11,
    visual_coverage: { required: 7, reviewed: 7, unresolved: 0 },
    visual_findings: [
      { code: "PALETTE_MISMATCH", reference: "HALLWAY", look: "night", view: "reverse",
        image: "hallway-night-reverse", evidence: "possible warm cast on a dark wall; practical lighting may explain it",
        source: "sibling night view; no explicit palette constraint", confidence: "low", severity: "advisory",
        next_action: "human review: confirm whether the reflection is intentional" }
    ],
    acknowledged_advisories: ["GENDER_MISMATCH:TONY"],
    user_overrides: [],
    timestamp: "2026-..."
  },
}}}}})
```

## Workflow

```
1. read the accepted plan and persisted scenes/shots/relations → planned demand, state, and camera zones
2. read the source screenplay/script and current Cast & World → scripted demand and available references
3. read `metadata.pipeline.reference_pack_inventory` and project reference policy
4. run all 7 check categories and inspect every required look/view image → findings + visual coverage
5. emit the REFERENCE AUDIT report with proposed remediation; do not write references or submit image jobs
6. route user-confirmed fixes to `/mixio:references` or `/mixio:sheets`, then re-run affected audit checks
7. present the completed Step 04 audit result and accepted risks → continue to Step 05 Shot Planning
```

## Notes

- Run once after the confirmed breakdown is synced to identify gaps, then again after confirmed sheet/reference changes. Step 04 informs Step 05 and generation; a finding alone is not a hard gate.
- This audit never bypasses reference policy, mutates assets, or starts image generation. Run it as a readiness checkpoint after local planning.
- Re-run after any reference change in a later step. It's free (reads only) and a stale audit means a stale contract.
- The duplicate check uses normalized names (lowercased, stripped of punctuation, collapsed whitespace). `aliasMatching` in project settings controls whether recorded aliases participate in *breakdown* matching — the audit checks aliases regardless, because it's looking for data quality, not runtime behavior.
- On a project with 50+ references, emit the clean list as a count rather than naming each one. The high-priority and advisory findings are what the user needs to review.
