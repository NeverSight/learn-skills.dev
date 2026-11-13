---
name: mixio-script-breakdown
description: "Use to enrich a supplied or existing scene/shot breakdown with production detail, or create one from a screenplay/script when no breakdown exists."
version: 0.3.0
invoke: /mixio:script-breakdown
---

# Mixio Script Breakdown

Prepare a complete local shot plan before writing a breakdown to Studio. The selected screenplay should be the confirmed, director-developed production source; if the available material is only a high-level script or incomplete screenplay, route through Step 00.5 of `mixio-pipeline` before breakdown. When the user supplies a scene/shot breakdown or one already exists in Studio, use it as the baseline and enrich it; do not restart the scene-and-shot breakdown from the screenplay. Preserve its scene and shot order, authored beats, and user-stated direction. Add production detail and clearly labeled missing coverage without replacing the user's structure. When no usable breakdown exists, create the scene-and-shot structure from the confirmed screenplay. A supplied breakdown can serve as the source when no screenplay/script is available; state the evidence limit and do not invent missing source facts. Keep the confirmed screenplay unchanged during breakdown and label source facts separately from inferred direction.

Use the shared [director’s lens](../mixio-pipeline/references/directors-lens.md): the plan serves audience intent and sequence flow, while source facts, user-authored direction, inference, and open decisions remain distinct. Bring in relevant cinematography, production design, props, script-supervision, editing, sound, or action perspectives to answer craft-specific questions; record their recommendations in the plan rather than treating them as approved story facts.

The normal path is **local analysis → director-led Continuity Checklist → exact Studio diff checkpoint → sync and readback on chat confirmation or prior authorization**. Do not use the write-through `script_breakdown` job as the normal path. This skill does not generate images, video, or audio.

## Choose the breakdown mode and read the current production

1. Resolve the project and episode using `mixio-pipeline` scope rules. Never infer an ID.
2. Identify the baseline before planning: a user-supplied breakdown, an existing Studio scene/shot breakdown, or no usable breakdown. If more than one exists, preserve each source and flag conflicts rather than silently choosing which authored direction to discard.
3. Read the confirmed production screenplay when available. A non-empty native `SCREENPLAY` body takes precedence after screenplay development, even while its Studio status is draft; otherwise use episode `script` / `metadata.fullScript` as source material and develop a screenplay first for a full production run. Preserve the confirmed screenplay verbatim, including dialogue, `#mentions`, `~locks`, and standalone `[Key: Value]` paragraphs. See [screenplay grammar](../mixio-episode/references/screenplay-grammar.md). The screenplay grounds and checks an existing breakdown; it does not replace that breakdown as the planning baseline. If no screenplay/script exists but the user supplied a usable breakdown, use it as the source and state that limitation.
4. Read current scenes/shots, project references and policy, and available image assets. Use exact canonical names and confirmed element IDs. Existing sheets and anchors help ground the plan; missing ones are recorded as readiness gaps.
5. Keep all breakdown analysis and corrections in the local plan. Do not write screenplay, scene, shot, relation, or reference changes while drafting.

If a usable breakdown exists, retain its scene/shot numbering and sequence. Carry its authored content into the local review table, then add production detail for visual action, audience purpose, camera, character/prop state, geography, transitions, and readiness. Label every proposed addition as `INFERRED`; keep the original direction distinguishable from the enrichment. Do not renumber, condense, reorder, or replace authored rows just to fit a newly generated structure. If a requested enrichment requires restructuring, present that as a separate proposal and identify the affected rows.

If no usable scene/shot breakdown exists, segment the source into scenes and dramatic beats and create the initial structure. Preserve source order and line references; infer only the coverage needed to make the source legible and connected.

## Director’s decision sequence

Run these questions in story order. Each shot should solve an audience, action, state, space, or flow problem; a shot that solves none of them has not earned its place.

| Pass | Ask | Plan |
|---|---|---|
| Intent | What should the audience know, feel, or anticipate here? Whose point of view carries it? | The shot’s dramatic or informational purpose |
| Change | What shifts in the character’s goal, power, information, relationship, or emotion? What choice or visible action causes it? | The action, reveal, reaction, or reversal the audience must see |
| State | What is true at entry and exit for each character, prop, costume, injury, and environment? | A cause for each material state change, or an explicit off-screen event/open question |
| Geography | Where is everyone in the location? What establishes orientation, screen direction, eyelines, and the axis? | Blocking and spatial relations that make the cut readable |
| Coverage | What minimum images make the action and its cause legible? | Needed establishing, entrance, hand/prop, reveal, reaction, movement, or exit coverage |
| Flow | How does this image connect to the previous and next one? | A motivated cut, action match, eyeline, sound bridge, transition, or deliberate time/space change |
| Expression | What framing, camera movement, performance, sound, and duration serve the intent? | Specific choices; movement and shot size carry meaning rather than decorate the beat |
| Feasibility | Which references/assets exist? What remains unknown or costly? | Readiness gaps and decisions for later production planning; no asset generation |

### Editorial coverage and continuity principles

- A material change must happen visibly, be identified as an intentional off-screen event, or remain an `OPEN DECISION`. Never let a new prop, location, injury, costume, or position appear without a cause.
- Plan the transition between shots, not just each shot alone. Track what enters and exits frame, who holds each prop, where people move, and what the next image needs to inherit.
- Establish geography when the audience needs orientation. Do not add a generic wide shot to every scene; a direct start or purposeful disorientation may serve better.
- Keep screenplay facts and authored direction distinct. The screenplay-development review labels additions; a useful extra breakdown shot may also be `INFERRED`. A choice that changes story facts or character intent is an `OPEN DECISION` with options for the user.
- Do not add dialogue or rewrite screenplay action to make the plan easier. Put proposed visual direction in the shot plan.
- Treat a stated runtime as the intended duration after post-production. Plan generated video equal to at least 1.2× the final runtime so the editor can select, trim, align, and pace the sequence. Add extra shots or clearly identified alternates when they provide useful coverage or choices; give each a purpose and approximate duration. Do not force generated shot durations to sum exactly to the target runtime or shorten action just to make them fit. Mark proposed surplus coverage `INFERRED`, and carry it into the production plan; this direction is not billable-generation approval.

## Produce the local shot table

For an existing breakdown, keep its scenes and shots as the baseline rows and enrich them in the local review table. For a new breakdown, segment the source into scenes and dramatic beats. In both modes, preserve original order and line references. Add visual coverage where it is missing, plus editorial surplus where it gives the editor meaningful choices. Label provenance at the shot level and split it when a row mixes source and inference—for example, `SCRIPTED beat; INFERRED framing and camera move`. Use this table in the user-visible review and add the [output ledger](../mixio-pipeline/references/editorial-coverage.md) for the main takes, alternate angles/emotions, reactions, inserts, and bridges:

| Scene / shot | Source beat | Audience purpose / POV | Action, framing, and camera | Character, prop, and space state | Connection from / to | Provenance and rationale | Readiness gaps |
|---|---|---|---|---|---|---|---|
| Local shot number | Exact source cue or line range | What the audience learns or feels | Concrete action plus shot size, angle/move, sound, and approximate duration | Relevant entry → exit state and blocking | How the shot starts from the last and hands off to the next | `SCRIPTED`, `INFERRED`, or `OPEN DECISION`; explain inference | Missing image, sheet, anchor, or unresolved production input |

Example of a proposed bridge: `INFERRED — the next scripted beat shows the character drawing a sword, but no acquisition is established. Add a brief insert/medium beat showing the sword enter the character’s possession. The source does not say whether it was carried in, found, or received; list those options as an OPEN DECISION if that choice affects the story.`

Use the existing canonical field map in [canonical-schema.md](references/canonical-schema.md) when preparing the approved sync payload. Each synced shot needs real values for `shot_type`, `camera_movement`, `subject`, `action`, `context`, `style_ambiance`, and `duration`; never put `TBD`, `unknown`, or an unresolved story choice into a required field. Keep original dialogue and screenplay lines verbatim. Provenance labels remain in the review plan; do not invent a Studio schema to store them.

When the accepted episode contract uses the 10–15s `multi_cut` band, plan its per-cut action and handoffs in `cuts[]` and follow the invariant in [canonical-schema.md](references/canonical-schema.md#cuts--multi-cut-passthrough). The managed `script_breakdown` job cannot emit `cuts[]`; prepare that approved sync with the composed primitives.

## Check the local draft

Before presenting the diff, confirm:

- Every beat and required dialogue moment in the available source (screenplay/script or supplied breakdown) is represented; added coverage is clearly labeled as inference.
- Every character and consequential prop has a legible entry/exit state. Pick-ups, put-downs, handoffs, arrivals, departures, and changes of possession have a cause.
- Location, screen direction, blocking, and eyelines remain understandable across cuts, or a deliberate change is identified.
- Each shot has a purpose and each transition has a visual, action, sound, or time/space relationship to its neighbors.
- Inferred direction does not silently settle a story-changing question.
- If a user-supplied or existing breakdown was the baseline, its authored scenes, shots, order, and direction remain recognizable in the enriched table; every proposed structural change is called out separately.
- Planned generated video reaches at least 1.2× the intended post-production runtime. The [output ledger](../mixio-pipeline/references/editorial-coverage.md) identifies each candidate clip, purpose, owning shot, alternate relationship, approximate duration, and checklist items; still keyframes are excluded.
- Existing images ground only the details they actually show. Missing sheets/anchors are listed as readiness gaps; do not claim visual validation without an image.

Use `/mixio:continuity` to create the director-led Continuity Checklist. Resolve grounded coverage gaps locally and include the checklist with the proposed Studio diff.

## Prepare the exact Studio diff

Read the current Studio graph again before comparison. Show a separate change table with one row per operation:

| Operation | Confirmed target ID | Exact change | Related elements | Match confidence / question |
|---|---|---|---|---|
| `ADD`, `UPDATE`, or `NO CHANGE` | Existing scene/shot ID or `NEW` | Exact fields and before → after values | Character, location, prop, and appearance links | Why the match is clear, or what needs resolving |

Match by confirmed element ID and the current scene/shot content. Studio upserts also use scene and shot numbers, so verify each upsert key resolves to the intended ID before calling it. Flag ambiguous matches and unmatched existing shots. Never silently overwrite, renumber, or delete an existing shot. Leave uncertain changes out of the write set and ask a focused question.

Show the finished shot table and complete diff as a checkpoint. A clear chat “proceed” or prior authorization for this scope is sufficient to write; do not require a separate Studio approval status or ask again for an already authorized diff. If the user changes the plan, rerun affected checks and show only the revised portion before writing.

## Sync after confirmation

On chat confirmation or prior authorization for the presented diff, use the existing tools:

1. Apply the confirmed scene/shot additions or updates with `studio_upsert_scene_packages` or targeted `studio_revise_shot_specs` as appropriate.
2. Resolve only confirmed Cast & World IDs. Register a missing reference only when it is included in the confirmed diff and `settings.references.createPolicy` permits it; for `propose`, chat confirmation of the exact proposal is sufficient. `link_only` remains a Studio policy boundary and permits linking existing references only.
3. Add/update typed relations with `studio_link_graph` and appearance state for the confirmed shot content.
4. Read persisted scenes, shots, references, and relations back. Compare fields and IDs against the confirmed diff; report exact successes and any partial or mismatched result.

### Reference policy and appearance bindings

Read `settings.references` before syncing any missing reference. Under `createPolicy: propose`, show the exact entity proposal as a checkpoint; if the user says proceed, write it and verify readback. Under `createPolicy: link_only`, offer matching existing references; the configured policy does not permit creating a missing entity, so continue only with a selected existing reference or a chat-confirmed plan that does not depend on that entity. Never bypass the configured policy.

Before authoring appearances, read `metadata.pipeline.reference_pack_inventory`. When a confirmed CHARACTER row maps the screenplay to a non-default variant, write that exact variant ID/name to `metadata.lookRef` on the character-to-shot `appears_in` relation (the relation’s per-appearance metadata, exposed as `appearanceState.lookRef` by the composed path), alongside the descriptive wardrobe state. Do not write `lookRef` to shot metadata or to a character reference globally. Never choose a variant by fuzzy text similarity. If an inventory mapping is ambiguous, keep it as an `OPEN DECISION` and ask a focused question; continue unaffected work. After chat confirmation, use the composed path so it can write the explicit `lookRef`; read back the persisted relation and check type, endpoints, and exact variant ID/name. Also confirm `get_production_context.lookBindings` resolves the expected variant when available. Report `REQUIRED_LOOK_UNBOUND` when the binding is missing or mismatched; let the user choose a compatible fallback if available.

The complete existing write/readback contract is in [persistence-and-audit.md](references/persistence-and-audit.md). That reference documents the existing primitives; it does not add a separate Studio approval-state requirement.

## Workflow

```text
read source + current graph/assets
  → reason through intent, change, state, geography, coverage, flow, expression, feasibility
  → build and locally audit the shot table
  → show the exact ID-matched Studio diff as a checkpoint
  → chat confirmation or prior authorization for that scope
  → sync with existing primitives and verify by readback
```
