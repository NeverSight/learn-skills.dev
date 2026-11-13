---
name: ad-variation
description: Create, remake, edit, or revise complete presenter-led ads and video variations through OpenArt MCP. Use for reference adaptations, product explainers, new openings, B-roll, captions, motion, sound and finished edits. Use OpenArt MCP for image, video, audio and other supported operations; choose supplementary tools only for operations it does not provide. Includes script review and preview/full-quality decisions without a fixed editing engine.
---

# OpenArt Ad Variation

Read [shared video experience](references/video-experience.md) first. This skill preserves the creative,
editorial and interaction guidance for complete ad productions without binding them to an editing engine.
Use OpenArt MCP for image, video and audio generation and every other needed operation it supports.
The agent selects supplementary tools only for operations OpenArt MCP does not provide. Read
[capability selection](guides/execution/capability-selection.md) before choosing an execution path.
It supplies strategies and production relationships, not hardcoded tool calls or a bundled engine.
The Seedance 2.5 preview/full-quality defaults are accessed through OpenArt MCP using its live capabilities.
For a video commission, use actual available capabilities to finish the video after approval; do not stop
at a strategy document unless that is what the user requested.

Before interpreting any brief, script or timecoded draft, read
[intent and script development](references/intent-and-script-development.md). Preserve the intended message,
required facts and exact keywords; actively improve expression, reasoning, actions and flexible beat timing
in this skill's style. Input detail is not an instruction to execute verbatim. Explicit exact-execution
constraints and an approved version requested unchanged remain locked.

When the Script Plan revises supplied creative input, END that response by briefly explaining what changed
and why, then ask whether to use the revised script or follow the original input exactly. Resolve that
version choice before generation under [generation approval](references/generation-approval.md);
a Draft/full-quality choice alone is not acceptance of the rewrite.

Before authoring, read [shared video experience](references/video-experience.md) and
[product understanding](references/product-understanding.md). Before a generation decision, read
[generation approval](references/generation-approval.md), including native question UI and wording examples.
Complete the full prompt and its matching readable Script Plan before showing either for approval; keep
all spoken and on-screen text in that same version. Default to Seedance 2.5 Draft preview; explicit
high-quality/full-quality delivery defaults directly to Seedance 2.5. Reuse clear approval or an explicit
approval waiver. These shared rules own the experience flow across every video and variant.
For presenter-led promotions, also read [opening hooks](references/opening-hooks.md): establish relevance
in the first 3–5 seconds and show the product from the first image without forcing a spoken brand pitch.

Read the entrypoint and these shared workflow guides, then follow the relevant references linked below.
Supporting Markdown is loaded on demand, not automatically in full. Read reference-analysis guides
for uploaded reference videos, product research for product URLs, direction before authoring, OpenArt
execution before fixing references, duration or request counts, and review before acceptance. Follow nested
links when that decision requires them.

For installation and the package overview, see [README](README.md).

Own the complete viewing experience requested by the user. Understand the material, make deliberate creative choices, and deliver the finished video. Match the user's language in conversation and the commissioned language in speech and graphics.

Treat each commission as a set of relationships: who addresses whom, what the viewer discovers, what supplies evidence, and how picture and sound guide attention. The presenter can lead continuously, share the frame, disappear during a demonstration, or participate in a conversation. No layout, caption treatment, presenter cutout, transition, or end card is mandatory.

Before authoring or revising prompts, read [creative preflight](guides/creative-direction/techniques/creative-preflight.md).
Product images and a short brief are a valid starting point; actively design progression and
performance within this skill's boundary. Audit the final prompt for unjustified restrictions before submission.

## Locate the work

Read the request and existing project notes before asking questions. Identify the intended change and separate supplied material by role: **footage to retain**, **person identity/performance reference**, **creative reference**, and **product evidence**. One asset may serve several explicit roles. Measure duration and inspect streams; a requested output length, a source duration, and a model's per-request limit are different facts.

Use [intake](guides/project-intent/intake.md) for missing inputs and presenter onboarding. Use [project memory](guides/project-intent/project-memory.md) to establish or resume the production. Carry forward settled choices, usable assets, approvals, and generation receipts. Ask only for information that changes the work; continue independent preparation while waiting.

## Understand before directing

For a supplied reference, read [reference reading](guides/project-intent/reference-reading.md). Inspect the entire piece, its speech, representative frames, and important transitions. Explain why the sequence works, then investigate details that may change that explanation. Keep observed evidence separate from inference.

Use [adaptation](guides/project-intent/adaptation.md) to state what stays and what changes. A strict identity replacement preserves the requested source relationships; a new-product adaptation rebuilds the argument around the new product. Do not replace either with a generic short teaser. A reference is neither automatically a model input nor permission to reuse every asset in it.

Develop a brief and a treatment proportional to the task. The brief records the commission; the treatment explains the proposed viewing experience. For missing copy or uncertain claims, use [message and script](guides/project-intent/message-and-script.md). For time, use [speech and events](guides/composition/speech-and-events.md): accepted performances establish spoken timing, and authored graphic sequences establish their own reading rhythm.

## Read the craft that owns the next decision

Load the relevant pages when the decision arises, including when revising inherited prompts or code. These are sources of judgment, not a sequence of mandatory effects.
Before deciding audio direction, read [Sound](guides/creative-direction/techniques/sound.md). Normally plan fitting
background music for the completed ad; use a reasoned unscored exception for formats such as interviews or podcasts.
Assign music to either the retained/generated audio or the final mix so it is neither omitted nor doubled.

| Current question | Read |
| --- | --- |
| How should this kind of presentation work? | [Presentation forms](guides/creative-direction/presentation-forms/index.md) |
| How should the person look, speak, and react? | [Performance](guides/creative-direction/techniques/performance.md) |
| What should an image model receive? | [Image direction](guides/creative-direction/techniques/image-direction.md) |
| What should a video model receive? | [Video direction](guides/creative-direction/techniques/video-direction.md) |
| How do generated passages remain coherent? | [Continuity](guides/creative-direction/techniques/continuity.md) |
| What should cover or support the speech? | [Supporting pictures](guides/creative-direction/techniques/supporting-pictures.md) |
| How should a real product be demonstrated? | [Product interface](guides/creative-direction/techniques/product-interface.md) |
| How should words appear and move? | [Captions](guides/creative-direction/techniques/captions.md), [motion and graphics](guides/creative-direction/techniques/motion-and-graphics.md) |
| How should the video sound? | [Sound](guides/creative-direction/techniques/sound.md) |
| How should imperfect recorded footage become an edit? | [Recorded-footage editing](guides/composition/recorded-footage.md) |

## Make the material and composition

Resolve OpenArt MCP capabilities for the approved commission first. Use supplementary media analysis,
editing or rendering tools only for operations it does not provide. Use
[capability selection](guides/execution/capability-selection.md) to distinguish what needs
new media from what can be retained or edited. Do not delegate creative planning to an execution tool.
Honor a request to disable automatic prompt rewriting when supported; report missing control honestly.

Prepare only dependencies needed for this production. Installing a knowledge skill does not install an
engine, connect an account or supply credits. Use the OpenArt tools that
[OpenArt execution](references/openart-execution.md) maps for supported operations, reading their live forms;
no supplementary editor commands or runtimes are prescribed here.

For generated or supplied files, use [material handoff](guides/composition/material-handoff.md). Choose the simplest sufficient method for the approved edit; changing a hook, correcting captions or joining shots does not require building a production framework.

While generation runs, develop composition work that does not depend on its result. Once media arrives, inspect it, accept or correct it, then resolve timing and framing against the actual files. Reuse accepted material explicitly. Before building, inspect the execution plan for accidental regeneration. [Execution and recovery](guides/composition/build-and-recovery.md) owns durable execution, receipts, and result reuse.

## Refine and deliver

Review the whole export and targeted passages using [review and delivery](guides/composition/review-and-delivery.md). Technical validity is one check; speech completeness, identity fidelity, reference relationships, readable product evidence, expressive timing, and sound require separate review. Never report a silent contact sheet as playback verification.

A revision starts from the requested change and its dependencies. Preserve unrelated choices and material, then recompute affected timing, crops, graphics, and sound. See [adaptation](guides/project-intent/adaptation.md), rather than inventing a separate workflow for every possible request.

Deliver the final video and requested variants with usable links and a concise account of changes and unresolved issues. Editable projects, component packages, material manifests and rebuild instructions are not required deliverables. Keep only the working records needed for the edit and generation recovery. Keep the user informed with discoveries, meaningful choices, and the current next step while work runs. A plan, a generated clip, and a successful renderer exit are intermediate results when the commission is a complete video.

## Working examples

[Read the examples](examples/README.md) for contrasting creative decisions and a generation brief. Examples demonstrate relationships and technical seams; they do not prescribe a house style. Product-specific layouts, scripts, people, and production assets belong to their own projects.
