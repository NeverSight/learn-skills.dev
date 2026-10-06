---
name: vox-motion-graphics
description: Autonomously direct and implement editorial motion-graphics films in Remotion from vague or complete briefs. Use for short-form and long-form explainers/documentaries, hierarchical story direction, visual invention, storyboards, asset vocabulary, narration-led timing, and independent editorial plus technical QA without requiring the user to be a designer.
---

# v0.10 — Visual Invention & Long-Form Direction

## Mission

Turn a topic, script, or rough brief into an authored, visually inventive film, from a vertical short to a 5–20 minute documentary/explainer. Own the directing decisions unless they change factual meaning, rights, brand identity, material cost, or another user-owned constraint.

Optimize for fewer expensive iterations: resolve the visual argument in a cheap browser storyboard, freeze it, then implement it faithfully in Remotion.

Default to autonomous direction. Choose composition, visual metaphor, choreography, camera, assets, transitions, captions, and sound without asking the user to supply motion-design expertise. Pause only for a real blocker or an approval gate the user explicitly wants to own.

## Operating principles

1. **Match the visual job to the beat.** When explaining a mechanism, show relationships, causes, constraints, transformations, and consequences rather than nouns. Identification, evidence inspection, chronology, atmosphere, and emotion are valid jobs too.
2. **Hierarchy before treatment.** The factual claim, focal point, and dominant change must read before texture, effects, labels, or ambient motion.
3. **One visual thesis per scene.** A scene may contain many events, but each state needs a clear focal point and the events must support one idea.
4. **Narrative change needs visual response.** When the narration introduces a new cause, stage, contrast, or consequence, change the visual structure or explicitly justify a hold.
5. **Technical success is not editorial success.** A valid render can still be confusing, static, generic, or badly paced. Run separate technical and editorial QA.
6. **Generated is not accepted.** Track asset origin, technical verification, editorial acceptance, rights, and factual representation separately.
7. **References teach grammar, not templates.** Reuse a useful mechanism only when it solves the new story; do not inherit exact layouts, assets, colors, timings, or surface style by default.
8. **The approval surface is not the production spec.** Storyboards optimize for visual judgment. Keep prompts, frame math, source notes, and implementation detail secondary or collapsed until design freeze.
9. **Direct the film, not just its modules.** Scene polish cannot establish sequence rhythm, chapter progression, callbacks, or a cumulative payoff. Judge these at their owning level; variation and repetition both need a purpose.

## Production graph

`brief/evidence -> hierarchical direction and vocabulary -> mechanism concepts and shot scores -> storyboard with caption/sound intent -> independent multi-level design review -> freeze -> final VO/alignment -> timing conformance -> bounded implementation handoff -> mastered draft -> technical and independent multi-level editorial review -> delivery`

Scratch narration drives provisional storyboard pacing. Final voice performance precedes frame-accurate choreography. Decide caption layout and sound intent with the visual design; source, synchronize, and mix the final audio during mastering. Render previews whenever needed for inspection; review the mastered output before publication.

## 1. Brief, evidence, and story

Infer reasonable audience, format, duration envelope, tone, and platform defaults. Ask only when missing information materially changes facts, rights, brand, cost, or scope.

For factual work:

- record claims as `verified`, `unverified`, `disputed`, or `inference`;
- keep rights and factual accuracy as separate axes;
- never make narration, labels, charts, or reconstructed visuals more specific than their supporting evidence;
- distinguish `literal`, `evidence`, `reconstruction`, `metaphor`, and `abstract` representations;
- never style invented or retypeset material so it can be mistaken for a recovered primary document. Use a real sourced artifact, or clearly label an editorial reconstruction/retypeset excerpt and keep invented mastheads, quotations, and article copy out of evidence scenes.
- choose the representation type before adding concrete staging. Unspecified geography, materials, device behavior, wear, or gestures are not verified facts. Use neutral or clearly illustrative staging when those details are unsupported; do not call an invented path or action historically known.

Build one editorial angle, a causal/logical spine, a viewer promise, and narrative beats. Scene boundaries follow visual ideas, not punctuation, fixed durations, or one-sentence-per-scene formulas.

Use **Film → Chapter → Sequence → Scene → Beat** to assign decisions at the right scale. Collapse chapter/sequence ownership for a short; use them in longer work for argument progression, evidence, rhythm, motifs, escalation, callbacks and payoffs. A scene need not carry the whole film. Plan visual vocabulary before resolving assets, then run a neighboring-scene sequence pass before implementation. Read [sequence-direction.md](references/sequence-direction.md).

If the user supplies reference videos, creators, or a target look, deconstruct them before concept generation and classify transferable grammar separately from benchmark-specific surface details. After analysis, translate named references into observable grammar; do not use creator names as a substitute for direction in production prompts unless the user explicitly wants those names retained as human shorthand. Read [reference-analysis.md](references/reference-analysis.md).

Read [story-director.md](references/story-director.md) for story construction and [research-and-representation.md](references/research-and-representation.md) for factual work.

## 2. Editorial translation and visual concepts

For explanatory, causal and process scenes, require **Visual State Delta**:

`before state -> visible operation -> after state -> viewer inference`

Ask what is visibly different about the relationship/world afterward. Another label arriving is not sufficient by itself. Preserve a stable reference and factual limit; do not force a delta onto identity, evidence inspection, chronology, atmosphere or emotional holds. Judge those by their assigned contribution.

Use `Anchor -> Action -> Consequence -> Launchpad` as a compact scene grammar, not a rigid timing template.

When narration describes causality, systems, economics, loops, growth/decline, transformation, or dependencies, prefer connected structures such as flows, handoffs, accumulation/depletion, networks, object systems, diagrams, or state changes. Use archival media when it supplies identity, evidence, emotion, or context—not as a substitute for explaining the mechanism.

For difficult or important explanatory beats, compare **2–3 low-cost concepts across different construction families** before expensive asset creation or coding. Each must explain the same inference through a different mechanism. Select autonomously for instant comprehension, story specificity, visual surprise, motion potential, factual honesty, asset feasibility, neighboring continuity and implementation cost. A palette swap is not a second mechanism; stop searching after selection.

Turn the chosen concept into a short shot score: **composition/viewpoint; object action; camera and information revealed; attention path; rhythm/payoff; sound or silence; exit/handoff**. Camera discovery is not a substitute for object change when the claim needs that change. A locked camera or direct cut may be the strongest choice. Use [motion-patterns.md](references/motion-patterns.md) for the working procedure.

For thesis/payoff scenes, prefer a visual demonstration that makes the conclusion inevitable before short text/VO names it. Typography, evidence or an emotional hold may carry the payoff when justified. Record the observable contribution, not just the closing slogan.

Read [scene-patterns.md](references/scene-patterns.md), [visual-language.md](references/visual-language.md), and [transitions.md](references/transitions.md).

## 3. HTML storyboard is the creative decision surface

Create a browser-viewable HTML/CSS/JS storyboard or motion preview before Remotion implementation.

Before authoring the storyboard:

- If the project has a root `DESIGN.md`, read it first. Its `Layout`, `Typography`, `Elevation & Depth`, `Shapes`, `Components`, and `Do's and Don'ts` sections are the project's visual source of truth.
- Always load [storyboard-layout.md](references/storyboard-layout.md) as the embedded canonical storyboard layout reference. Use its structure and constraints when building the storyboard, not just its general aesthetic.
- If a project `DESIGN.md` exists, apply its token values and named rules over the embedded reference; if it is absent, use the embedded reference unchanged.
- Treat the shell as layout grammar, not as a copy of another project's topic, assets, scene count, copy, or animation.
- Keep frame content, scene-specific visual systems, and motion studies inside the shell. Do not let them change the outer page anatomy without an explicit design decision.

Keep the review shell stable: masthead and hierarchical navigation, grouped film/sequence overviews, repeated scene inspection pairs, meaningful keyframes, and concise director notes. Canvases use the target aspect ratio, not mandatory 9:16. The exact shell rules live in [storyboard-layout.md](references/storyboard-layout.md); do not duplicate them in production instructions. Those tokens are not a mandated film palette or genre.

Show enough states to judge the mechanism and payoff, plus a short motion study where camera, timing, or transitions cannot be judged from stills. Keep production detail expandable.

Use this decision surface to resolve:
- composition and focal hierarchy;
- asset choice and representation;
- scene structure and meaningful states;
- camera/object relationships;
- motion and transition intent;
- rough pacing and readable holds;
- continuity across scenes.

Preview meaningful visuals, realistic captions and required disclosures at actual consumption size: phone-sized portrait for vertical shorts; desktop and mobile YouTube-scale landscape for long-form. Inspect clean and captioned states together and record the viewing dimensions/evidence. Simplify or recompose unreadable information rather than packing in smaller type. Choose a coherent scene-aware layout, not a universal empty caption band.

Do not reduce the storyboard to a single video switcher or wireframe cards. Keep the approval surface rich, tactile, and structured, but do not let production telemetry or animation controls crowd out the stable page hierarchy.

Critique and refine the storyboard before implementation. The HTML preview is the creative source of truth; structured files index or validate it, not replace it. Freeze only after independent Scene, Sequence, Chapter (where relevant) and Whole-Film critique resolves editorial blockers. Keep the approved snapshot distinct from as-built notes and bind evidence to that revision. Use `storyboard-plan.json` when a machine-readable handoff is useful.

If the user asked to approve the storyboard, an independent critic may mark it ready but must not substitute for that human gate. Otherwise, independent design review may freeze it autonomously.

After freeze, Remotion may refine timing, easing, compositing, and technical execution. A change to the scene thesis, focal hierarchy, defining relationship, asset identity, or transition logic returns to the storyboard.

Read [storyboard.md](references/storyboard.md).

## 4. Assets and visual language

Route assets deliberately:

`reuse -> programmatic -> source real/licensed -> reconstruction -> generate`

Prefer real or licensed material when identity/evidence matters; programmatic graphics for systems, charts, routes, interfaces, and neutral reconstructions; generated media for original illustrative material or clearly identified reconstructions.

Preserve subject identity without automatically repeating composition. Plan useful viewpoints, details, interiors, environments, archival/evidence material, process components, maps/diagrams, associated objects and human context according to the film's needs—not as a shopping checklist. Bind vocabulary roles to the existing asset ledger; do not create a second provenance system.

Track orthogonal asset fields:

- `origin`: how it was obtained;
- `technicalStatus`: candidate, available, or verified;
- `editorialStatus`: pending, accepted, or rejected;
- `rightsStatus`: unresolved, needs review, verified, or self-created;
- `representationType`: literal, evidence, reconstruction, metaphor, or abstract.

An asset enters implementation only when its editorial status is accepted and it meets the actual shot requirements. Inspect the deepest crop and promised full-object payoff, not just nominal dimensions. Evidence needs supported claims and source provenance; rights are a separate delivery gate. If the asset cannot support the shot, choose a feasible shot or an honest representation rather than fabricating evidence.

Read [asset-selection.md](references/asset-selection.md). For style, typography, hierarchy, treatments, and text restraint, read [visual-language.md](references/visual-language.md).

## 5. Narration, timing, motion, and transitions

Final narration performance is the authoritative clock. Before that performance exists, storyboard timing is provisional: use semantic anchors and approximate scene-local seconds, and avoid presenting exact global frame ranges as authoritative. After final VO/alignment, align words or phrases and reconcile:

- narration end;
- scene start/end;
- caption start/end and sentence boundaries;
- transition windows;
- SFX attacks/settles;
- declared final hold;
- total composition duration.

Conform important events, not just scene lengths: orientation window, narration trigger, action completion, readable payoff, and transition. Reading time begins when essential content is readable, not when its entrance starts. Permit anticipation and J/L cuts when they preserve meaning and caption readability; an offset alone is not a defect. Do not truncate speech or evidence, or leave an unexplained inactive tail. If the available time cannot support the shot, simplify or reconform it rather than speeding every action up.

Motion must serve the assigned visual job; for explanation, prove the state delta rather than merely revealing labels. Stillness, silence, testimony, evidence holds and dramatic pauses are valid, including across multiple spoken facts. Direct fast/quiet and dense/sparse passages at sequence/chapter scale; quality is not an event every two seconds.

Choose repeated-object entrance semantics explicitly:

- `synchronized` when uniformity or one shared event matters;
- `staggered` when sequence, scale, or accumulation matters;
- `sequential` when one state causally enables the next.

Read [motion-patterns.md](references/motion-patterns.md), [transitions.md](references/transitions.md), and [audio.md](references/audio.md).

## 6. Remotion implementation

The implementation agent is primarily an implementer of the frozen visual decision, not a second director.

For agent handoffs, use bounded **SequencePacket / ScenePacket** contracts from [implementation-packets.md](references/implementation-packets.md): frozen identity, relevant direction/style, local claims/assets, aligned timing, neighboring boundaries and required proof. The scene implementer should not reread the entire creative skill. Packets index authoritative artifacts; they do not authorize redesign or introduce a model router.

- Derive render-visible motion from frames and video configuration.
- Use current official Remotion patterns and installed-package APIs.
- Do not use timed CSS transitions/keyframes for render-visible motion.
- Preserve the storyboard's defining objects, relationships, state order, hierarchy, and transition logic.
- Keep scene-local time local and use final alignment for offsets.
- Use deterministic seeded variation; never uncontrolled render-visible randomness.
- Keep text sharp and outside destructive image-treatment filters.
- Verify visible bounds, crops, identity anchors, and settled data labels in actual renders.
- Prove defining relationships, not just object/state presence: inspect actual boundary clips, visible before/after states, full-object reveals, and readable payoffs against the frozen revision.
- Account for planned sound cues as implemented, deliberately replaced, or intentionally omitted; audition the mastered result.

Expose a small typed tune surface only for decisions likely to need safe repair. Property controls, parameter manifests, and patches are conditional tools—not requirements for every scene. Studio-specific layer structures are optional unless the project needs manual editability.

Read [remotion-implementation.md](references/remotion-implementation.md).

## 7. Critique and QA

Render representative evidence around semantic moments: anchor, pre-action, defining change, payoff/settle, and handoff. Use short motion previews when timing or camera behavior matters. Build contact sheets with `tools/make_contact_sheet.py` when useful. Metadata cannot prove that a relationship is visible or a sound is audible.

The independent critic first observes the visual sequence without the director's explanation, recording focal subjects, changes, stable references, and inferred relationships. Then compare that observation with the intended visual job and review the complete captioned/audio master. Do not demand that images alone encode every name or factual qualification.

Review independently at **Scene → Sequence → Chapter (when present) → Whole Film** before freeze and again on the mastered draft. Sequence critique tests neighboring rhythm/repetition; whole-film critique tests progression, escalation, callbacks, style continuity, emotional rhythm, payoff and cumulative comprehension. A collection of approved scenes does not imply an approved film. One independent pass may cover several scopes; scopes are not mandatory separate model calls.

### Editorial QA

Evaluate actual storyboard/renders for:

- a legible assigned visual contribution and factual honesty;
- clear focal hierarchy;
- meaningful relationship changes where explanation requires them, or a successful exempt visual job;
- process/causal legibility;
- useful visual events rather than label-only explanation; no rejection of purposeful stillness;
- composition, crop, and readable text;
- pacing, holds, and transition intent;
- continuity, intentional construction repetition/contrast, and sequence/chapter rhythm;
- asset suitability and style cohesion;
- sound supporting semantic events without implying unsourced historical authenticity;
- status consistency: script/voice/timing claims do not contradict each other across the approval surface;
- evidence density: visible labels and specifications advance the scene thesis instead of turning the frame into a production/research dashboard.

Charts, recurring assets, side profiles, locked cameras and direct cuts are valid tools. Require a reason when repetition weakens progression, not uniqueness for every neighbor. Do not demand morphs or constant motion.

Route failures to their cause: wrong relationship -> redesign; correct relationship but weak staging -> composition/choreography repair; accepted plan missing from output -> implementation repair; subjective preference without functional harm -> taste, not blocker.

### Technical QA

Verify:

- render/build/type/lint success as applicable;
- deterministic frame-driven motion;
- timing bounds and declared final hold;
- captions and critical content inside named platform-safe presets;
- asset existence, dimensions, alpha needs, provenance, and lifecycle coherence;
- scene/state IDs preserved from the frozen storyboard;
- representative frames and audio files exist.

Both gates must pass. A technical pass cannot override an editorial revision, and editorial approval cannot waive factual, rights, or rendering failures.

The generating/implementation pass must not self-award `publish_candidate`. Use an independent critic when available. If independent review is unavailable, report `needs_review` rather than claiming production readiness.

Read [critique.md](references/critique.md) and [anti-patterns.md](references/anti-patterns.md). For compact before/correction patterns, read [positive editorial decisions](examples/positive/editorial-decisions.md) and [editorial failures](examples/negative/editorial-failures.md). Use `tools/validate_project.py` for deterministic cross-artifact checks; before promoting a publish candidate, run its publication gate with artifact-bound review evidence as described in [orchestration.md](references/orchestration.md). Hashes prove artifact identity, not creative quality or reviewer honesty.

## Artifacts: one source of truth per decision

Do not emit JSON merely because a schema exists. Structured artifacts support handoffs, validation, or resumability—not a second creative workspace. Publication needs a small machine-checkable evidence contract; exploratory previews do not need release paperwork.

Typical minimum:

- script/research notes in the project's natural format;
- `storyboard.html` or equivalent browser preview as the creative source of truth;
- final render/preview evidence.

Add structured artifacts only when they solve a concrete need:

- `claim-set.json` for evidence-heavy factual work;
- `storyboard-plan.json` to index frozen states across agents or resume runs;
- `direction` in story/storyboard handoffs for hierarchy, sequence rhythm and vocabulary, using [direction-plan.schema.json](schemas/direction-plan.schema.json);
- bounded implementation packets when separate implementers/resumed contexts consume them, using [implementation-packet.schema.json](schemas/implementation-packet.schema.json);
- `asset-manifest.json` when external/generated assets need provenance or acceptance tracking;
- `frame-scene-spec.json` after final VO when timing/alignment needs a machine contract;
- editorial/technical QA reports when another agent or automation consumes verdicts;
- `reference-analysis.json` when references materially drive decisions;
- tune manifests/patches when bounded parameter repair is actually used;
- publication review receipts binding the frozen board and mastered output to the reviewed artifacts, with verdicts, blockers, and evidence references.

If structured metadata disagrees with an approved HTML storyboard, do not silently trust either copy. Treat it as drift, inspect the approved preview/review evidence, and reconcile the metadata before implementation.

Legacy projects may continue as drafts. For v0.10 publication, reconcile the direction index with the frozen preview, resolve new scene contracts and obtain actual scoped/viewing-size reviews before updating the existing receipt. See [orchestration.md](references/orchestration.md); a draft pass is never release approval.

## Stop conditions

Continue until:

- the frozen storyboard has no unresolved editorial blocker;
- accepted assets and final narration are available;
- implementation matches the frozen defining relationships;
- technical QA passes;
- independent editorial QA and the publication gate approve the mastered artifact, or the output stays explicitly draft/`needs_review` when prerequisites are missing;
- factual and rights blockers are resolved;
- the requested render/preview exists.

Do not keep adding effects after the thesis, hierarchy, timing, and transitions are resolved.
