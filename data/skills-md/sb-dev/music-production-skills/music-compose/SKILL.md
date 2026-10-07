---
name: music-compose
description: Compose, develop, arrange, compare, select, and refine musical material before final production. Use for music briefs, references, melody, harmony, rhythm, groove, lyrics, hooks, motifs, song structure, arrangements, MIDI drafts, composition alternatives, and preservation of approved musical decisions.
---

# Music Compose

Develop the musical work before final production commitment.

## Scope

Own:

- brief interpretation for composition;
- reference analysis;
- composition;
- arrangement;
- structured and MIDI drafts;
- draft sets;
- whole-artifact and component-level selection;
- approved musical decisions;
- composition/arrangement lineage.

Do not own final audio production, mastering, provider infrastructure, or general-purpose audio editing.


## Execution prerequisites

Core composition and arrangement behaviour requires only an Agent Skills-compatible host.

MIDI helper scripts require Node.js 22+ plus the dependencies in this skill directory's `package.json`; run `npm install` in the installed `music-compose` directory before using those scripts.

If composition work escalates to Replicate-backed audio generation, require the official `find-models`, `compare-models`, and `run-models` peer skills plus `REPLICATE_API_TOKEN`. Do not build or invoke a custom Replicate client as a substitute.

## Optional customisation pack

This skill remains fully usable without a customisation pack.

When a selected peer music customisation pack is available, treat it as reusable production guidance with this precedence:

```text
1. explicit user/project instructions
2. approved and locked music artifacts / decisions
3. selected customisation pack
4. music-compose defaults
```

Apply only pack guidance relevant to composition and arrangement, such as format, use context, genre, form, groove, instrumentation, production-language constraints that affect arrangement, draft strategy, and selection criteria.

A pack may narrow the creative search space but must not silently choose or reopen high-impact musical decisions. Do not require a pack for normal composition work.

## Determine the unresolved decision

Before creating output, identify what is actually uncertain: melody, harmony, rhythm/groove, lyrics, hook, structure, arrangement, instrumentation, or energy progression.

Use the smallest representation capable of testing it.

## Draft

1. Generate alternatives only where meaningful creative uncertainty exists.
2. Make alternatives materially different.
3. Prefer structured text, Tonal, or MIDI before generated full audio when sufficient.
4. Record what each draft is testing.
5. Preserve parent and variant lineage.

Do not generate complete finished songs merely to compare local composition ideas.

## Selection and decision state

Support complete-candidate and component-level selection.

When a component is selected, record its source.

Keep workflow state and decision state separate:

```text
workflowState: draft | refine | final
decisionState: open | selected | approved | locked
```

Selection means continue developing the choice. Approval means downstream work may rely on it. Locking means downstream work may assume it will not change unless explicitly reopened.

## Refine

1. Start from the selected/approved composition or arrangement.
2. Identify each relevant decision state.
3. Change only open or explicitly reopened decisions.
4. Preserve approved and locked musical decisions.
5. Update lineage.

## Final

A composition or arrangement is final when it is stable enough to hand to production. Final-as-composition does not mean final mastered audio.

## Deterministic tools

Use Tonal for deterministic music-theory mechanics.

Use `@tonejs/midi` and the local scripts for MIDI mechanics.

Do not ask a generative model to perform deterministic file operations when a local tool can do them reliably.

## Audio sketches

Use Replicate only when audio materially improves evaluation of the current composition/arrangement decision.

When using Replicate:

1. determine hard capabilities;
2. use `find-models`;
3. use `compare-models`;
4. translate the musical requirement into the selected model's native inputs;
5. use `run-models`;
6. preserve execution provenance.

## Evaluation

For drafts, check whether the artifact answers the intended question and provides meaningful alternatives.

For refinement, verify the requested change and preservation of approved/locked decisions.

Before production handoff, make unresolved musical issues explicit.

## Do not

- create a static model catalogue;
- silently rewrite approved or locked melody, lyrics, harmony, rhythm, or structure;
- treat every music-theory concept as a separate top-level artifact;
- force audio generation when structured/MIDI representation is sufficient;
- perform final production work that belongs to `music-produce`.

## References

Read the relevant local reference only when needed:

- `references/composition.md`
- `references/arrangement.md`
- `references/drafting-and-selection.md`
- `references/reference-analysis.md`
- `references/midi.md`
