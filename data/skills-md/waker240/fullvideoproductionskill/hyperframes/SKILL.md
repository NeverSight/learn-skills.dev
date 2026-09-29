---
name: hyperframes
description: Plan, author, review, and render HTML videos with HyperFrames. Use for narrated films, explainers, animation, or a video workflow needing versioned review, audio, captions, and final audit.
compatibility: Requires sibling skills from this pack, a local filesystem and shell, Node.js 22.20.0+, and FFmpeg/ffprobe for media work. Generation providers and desktop tools are optional, separately configured capabilities.
---

<!-- Public portability adaptation, 2026-09-26. -->

# HyperFrames video workflow

HyperFrames renders video from HTML. Use this entry point for a narrated film, explainer, animation or review package. The user's chosen framework, provider, visual style and delivery stage take precedence. Install the sibling skills together and read [runtime setup](references/install-portability.md). This pack does not install an AI model, hosted service, music catalog or desktop tool.

## Production principles

1. Complete the authorized stage. A requested storyboard, A/B review or audio audition is a real deliverable. Existing authorization to finish does not require invented approval stops. Current instructions and versioned choices supersede stale notes.
2. Direct before scaling. Study the script, define each beat's visual change, and prove moving benchmarks. The [capability palette](references/capability-palette.md) is a menu, not a quota. Admit 3D, dense editing or a persistent world only when it serves the argument.
3. Preserve review evidence. Record candidate/version, choice, comment and repair. Agent QA never creates user approval. Keep approved shots and protected windows intact. See [review-driven production](references/review-driven-production.md).
4. Direct sound with picture. Plan voice, captions, BGM or intentional silence, and action-linked SFX. Audition alternatives alone and under narration. Discovery, validation, shortlisting and actual final use are different states.
5. Keep media portable. Save prompts and non-secret provenance; freeze selected media into the project. Keep source audio and required lossless masters. No render depends on a private output folder, live catalog, credentials or runtime network access.
6. Keep time deterministic. Use seeded randomness, seekable timelines and framework-owned media. Test cold seeks and the encoded result. Follow the [core contract](../hyperframes-core/SKILL.md).
7. Audit meaning and mechanics. Inspect the full film, every adjacent seam, type/captions, sound and protected windows. Repair findings and recheck neighbors. Numerical audio checks cannot establish listening quality.
8. Capture learning locally. Save a short project `RETROSPECTIVE.md`; generalize proven fixes in a separate [maintenance task](references/self-improvement.md).

## Script or topic to film

Resolve material unknowns using the brief and session context: script handling, delivery format, voice/provider, length and review stage. Preserve supplied wording unless editing is authorized. For a bare topic, produce the script first; honor requested review before dependent production. Do not assume a platform, house style, personal voice or account.

Read the user's completion checklist if supplied; otherwise adapt the [bundled checklist](references/completion-checklist.md). A short title card does not inherit a publishing package's requirements.

Follow [pipeline.md](references/pipeline.md). For A/B review or repeated visual corrections, also read [review-driven-production.md](references/review-driven-production.md). The runnable [review workbench](templates/review-workbench/USAGE.md) provides versioned choices, notes and audio/visual candidates. [Review publishing](references/review-publishing.md) covers optional sharing when requested.

| Phase | Work and evidence |
| --- | --- |
| 1 | Scaffold; record runtime/configuration and audio route. Bundled synthesis helpers implement Fish. Supplied narration or a selected provider can enter through the imported-audio contract. |
| 2 | Study script; make `DESIGN.md`, narration/visual plan, scene contract and sound palette. Record reasoned `PASS`/`USE` for Spatial Canvas and fast passages; neither is a quota. |
| 3 | Generate/import voice, concatenate/master, obtain word timing and align authoritative text. Lock the clock before exact shot timings. |
| 4 | Generate/source assets with prompts/provenance. Audition music/SFX and freeze selected files. |
| 5 | Build scenes with locked timing/ownership; protect approved concepts and windows. |
| 6 | Assemble picture, chosen BGM/SFX, directed mix and intentional scene handoffs. |
| 7 | Validate, snapshot and watch the complete assembly at final frame rate; check captions, sound, camera returns and fast-passage release. |
| 7.5 | Run readiness gates appropriate to the requested deliverable. A review package is not a finished film. |
| 8 | For a full film, log audit → repair → recheck evidence in `DIRECTION.md`; run `scripts/gate.cjs`. The supplied gate expects at least two logged loops. |
| 9 | Render, decode and inspect the encoded master; reconcile retained files/checklist, deliver rebuild instructions and a project retrospective. |

Small edits enter at their relevant phase. Timing changes require the pipeline's Cascade.

## Routes

| Task | Skill or reference |
| --- | --- |
| Composition, tracks, media ownership and sub-compositions | [hyperframes-core](../hyperframes-core/SKILL.md) |
| Motion, transitions, cameras and runtime adapters | [hyperframes-animation](../hyperframes-animation/SKILL.md) |
| Direction, storyboards, typography and asset prompts | [hyperframes-creative](../hyperframes-creative/SKILL.md) |
| Narration, timing, mixing and sound review | [hyperframes-media](../hyperframes-media/SKILL.md) |
| Reviewed local media discovery/resolution/freezing | [media-use](../media-use/SKILL.md) |
| Registry blocks/components | [hyperframes-registry](../hyperframes-registry/SKILL.md) |
| Short synthetic-graphics explainer | [faceless-explainer](../faceless-explainer/SKILL.md) |
| Short motion graphic or overlay | [motion-graphics](../motion-graphics/SKILL.md) |
| Music drives the timeline | [music-to-video](../music-to-video/SKILL.md) |
| General custom composition | [general-video](../general-video/SKILL.md) |
| Port existing Remotion source | [remotion-to-hyperframes](../remotion-to-hyperframes/SKILL.md) |
| Approved studies to narration-locked final assembly | [review-to-final-assembly](../hyperframes-core/references/review-to-final-assembly.md) |
| Still generation / generated footage / paper theatre | [asset generation](../hyperframes-creative/references/asset-generation.md), [generated media](../hyperframes-creative/references/generated-media-composition.md), [paper theatre](../hyperframes-creative/references/paper-theatre.md) |
| Persistent world / bounded fast passage | [Spatial Canvas](../hyperframes-creative/references/spatial-canvas.md), [fast editing](../hyperframes-creative/references/fast-paced-editing.md) |
| Cover candidates | [thumbnail generation](references/thumbnail-generation.md) |

Browser tools, generators, sharing and delegation are host capabilities or separate installations. Use current schemas and permissions. If absent, use supplied media or execute work serially; name a missing capability precisely without claiming it is included.

## Maintenance

Keep the bundle version fixed during production. Set `HYPERFRAMES_SKIP_SKILLS=1` before CLI initialization that may install upstream skills. Use the project's tested CLI version. Review upgrades separately and preserve local changes/notices. Project output and [skill maintenance](references/self-improvement.md) are separate.
