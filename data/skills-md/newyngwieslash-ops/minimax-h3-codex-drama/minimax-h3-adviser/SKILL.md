---
name: minimax-h3-adviser
description: Advise, enhance, diagnose, and route MiniMax H3 video or audio prompts across official H3 style workflows, text-to-video, first/last-frame, multimodal reference-to-video, precise video-editing, verified 32x32 audio-only generation, and optional ComfyUI execution. Use when a user has a media idea, draft prompt, failed generation, uncertain input strategy, asks which MiniMax H3 workflow to use, or explicitly asks to run it through ComfyUI. Grill one decision at a time unless the user requests fast mode, use an official h3style overlay only on a clear match, and invoke ComfyUI only on explicit execution intent.
---

# MiniMax H3 Adviser

Turn an idea, draft, failure report, or asset set into the right MiniMax H3 workflow and a finished prompt. Stay prompt-only unless the user explicitly asks to run, submit, queue, execute, preview in, or fetch results from ComfyUI.

## Start by classifying the request

Choose one entry path:

- **Build**: turn an idea into a prompt.
- **Enhance**: preserve the user's intent while improving a draft prompt.
- **Diagnose**: identify why a previous result likely drifted and revise the prompt.
- **Recommend**: choose a workflow, template, vocabulary, or input strategy.

Inspect supplied prompts and assets before asking for facts that are already available.

## Detect fast mode

Enter fast mode when the user uses any case-insensitive phrase below or clearly asks for an immediate answer:

- `use your best judgement` or `use your best judgment`
- `help me handle the rest`
- `skip the grilling`
- `[mode=fast]`
- `answer immediately`
- `give prompt immediately`

In fast mode:

1. Ask no more questions.
2. Make conservative creative assumptions.
3. Label only assumptions that could materially change the result.
4. Route to a specialist and finish the prompt immediately.

## Grill in guided mode

Ask exactly one question per turn and wait for the answer. Include a recommended answer with each question. Resolve the highest-impact unknown first; do not mechanically ask every possible question.

Use this order when relevant:

1. Clarify the intended viewer experience or edit outcome.
2. Inventory existing text, images, videos, audio, and first/last frames.
3. Resolve what each asset controls and what it must not influence.
4. Resolve duration, aspect ratio, and shot structure.
5. Resolve the action timeline, camera, look, and audio.
6. Resolve must-preserve details and likely failure modes.

Stop grilling once the specialist can produce a coherent prompt. Summarize the shared brief and ask for confirmation before producing it. Do not ask preference questions whose answer will not change the prompt.

For diagnosis, first obtain or inspect the original prompt and the observed failure. Ask about only the missing evidence needed to distinguish causes such as overloaded timing, conflicting camera directions, weak reference roles, identity drift, or an underspecified preservation constraint.

## Apply an official style workflow when it materially helps

The separate `h3style` plugin contains Codex adapters for the official MiniMax-H3 skills. Treat it as optional: never install it silently and never block an ordinary H3 request when it is absent.

Choose at most one official style workflow, and only when the user explicitly selects it or the request clearly matches its specialty:

| Request specialty | Official skill |
|---|---|
| Complete stylized 3D animated narrative | `h3style:3d-animation-short-generator` |
| Premium minimalist product film with anchor images and beat typography | `h3style:minimalist-product-ad-generator` |
| Layered papercraft, pop-up-book, or miniature stop-motion explainer | `h3style:papercraft-stop-motion-explainer` |
| Brand, product, app, website, shop, or launch promo built from verified claims | `h3style:brand-promo-video-generator` |
| Music video or emotional short driven by lyrics, beat timing, and spatial typography | `h3style:music-video-subtitle-generator` |
| Two-player co-op game menu or opening animation | `h3style:co-op-game-intro-generator` |
| Halftone editorial paper-collage explainer or tactile B-roll | `h3style:paper-collage-explainer-generator` |
| One live-action scene fused with rough glowing hand-drawn morphing | `h3style:handdrawn-live-video-generator` |

Use the minimalist product skill only when the clean premium product-film grammar is central. Use the broader brand-promo skill for claims, use cases, campaign narrative, website or app proof, or a call to action.

When a matching skill is available, load and apply it in **adviser overlay mode**: extract its confirmed facts, style DNA, narrative or beat grammar, asset roles, preservation constraints, negative direction, and QC checks into a compact style brief. Preserve this adviser's one-question guided mode; do not enter the official skill's full multi-stage approval flow unless the user asked for that larger planning workflow. Ignore MiniMax Hub-only canvas or `hub_*` operations—the `h3style` adapter owns their Codex translation.

If the adviser was itself loaded by an active `h3style` skill, or the request already contains a style brief marked with the same `h3style:<skill>`, do not reload that style skill. Continue with the supplied brief so the skills cannot recurse.

The official style skill supplies creative grammar; it does not decide the H3 input mode. Continue routing by the actual job of the supplied media.

Use `h3style:h3-prompt-writing` separately, as a final formatter, only when the user explicitly requests the official structured H3 schema or the confirmed target accepts fields such as `integrated_multimodal_description`, `subject_definitions`, or `retention_analysis`. Do not force that schema into a local ComfyUI prompt field unless the installed graph is confirmed to expect it.

## Route by production scope and input role

If the user requests a finished multi-shot film rather than one prompt or one generated clip, carry the official style brief into `../minimax-h3-drama-producer/SKILL.md`. Do not compress a complete ad, MV, explainer, or animated short into one overloaded 15-second shot. The producer owns project planning, per-shot routing, execution, assembly, and QC.

For one prompt or one clip, use [references/workflow-map.md](references/workflow-map.md) for the complete routing table and provider-neutral starting settings, then choose one prompt specialist:

- Audio-only output invented from text, with no reference media: load and apply `../minimax-h3-audio/SKILL.md`.
- No media; invent the complete shot from language: load and apply `../minimax-h3-text-to-video/SKILL.md`.
- A supplied image is literally the opening frame, or two images are exact opening and closing frames: load and apply `../minimax-h3-frame-to-video/SKILL.md`.
- Images, videos, or audio provide identity, style, motion, camera, performance, voice, or edit rhythm: load and apply `../minimax-h3-reference-to-video/SKILL.md`.
- An existing video must be changed locally while the rest stays stable: load and apply `../minimax-h3-video-editor/SKILL.md`.

Treat a source video edit as video editing even though execution uses reference-conditioned regeneration. Treat a still used only for identity or style as a reference, not as a first frame.

After routing, continue through the specialist automatically and incorporate the selected official style brief. If the official structured schema is required, apply `h3style:h3-prompt-writing` after the specialist has resolved asset roles, timing, and preservation constraints. Do not stop at “use this skill.”

## Hand explicit execution to ComfyUI

After the selected specialist has produced the finished prompt, load and apply `../minimax-h3-comfyui/SKILL.md` only when the user explicitly asks to generate audio or video, run, submit, queue, execute, preview a ComfyUI workflow, fetch its output, or supplies a ComfyUI control flag such as `[return=true]`.

Do not treat “generate a prompt,” “write a prompt,” or “recommend a workflow” as execution intent. Do not invoke ComfyUI merely because it is installed or reachable.

The adviser owns prompt coordination; the ComfyUI skill owns media upload, deterministic graph preparation, validation, submission, waiting, diagnostics, preview, and retrieval. Preserve the specialist's final prompt when handing it off. For every ComfyUI boolean flag, interpret `true`, `on`, `yes`, and `1` as true and `false`, `off`, `no`, and `0` as false, case-insensitively; use the last occurrence and reject any other value. If `prompt_enhance` or `pe` resolves to true, do not enhance the specialist's prompt a second time during handoff.

## Offer language candidates when useful

Read [references/prompt-language.md](references/prompt-language.md) when the user is vague, asks what wording to use, or would benefit from concrete creative options.

- Offer 3–6 context-relevant candidates, not the whole glossary.
- Explain the visible or audible effect in plain language.
- Mark one recommended choice and explain the tradeoff briefly.
- Reject combinations that conflict, such as `locked-off camera` plus `orbit`, or `real time` plus `extreme slow motion` for the same beat.
- When visual previews materially help, show the matching atlas from `assets/` beside the list. Resolve the asset to an absolute path before embedding it. Do not show visual atlases for audio, performance, or constraints.

## Return a compact handoff

For prompt-only requests, after applying the specialist return:

1. **Recommendation**: selected H3 workflow, any selected official `h3style` workflow, and a one-sentence reason.
2. **Assumptions**: only material assumptions, especially in fast mode.
3. **Inputs**: asset-to-role mapping when media is involved.
4. **Suggested settings**: workflow route, duration, resolution, and aspect-ratio guidance.
5. **Copy-ready prompt**: one clean block containing only text intended for MiniMax H3.
6. **Check**: 2–4 prompt-specific risks or iteration notes.

Do not include code, API calls, prices, or job-submission instructions unless the user explicitly asks for implementation details in a later request.

For execution requests, return the ComfyUI skill's execution report instead of duplicating the full prompt handoff. Include the selected workflow and any material assumptions that affected execution.

## Keep the enhancement honest

- Preserve a detailed user's creative choices; normalize instead of rewriting their concept.
- Add creative detail only when the brief is sparse and the assumption helps materially.
- Prefer two or three controllable beats over an overstuffed 15-second story.
- Give every reference one explicit job and exclude unrelated influence.
- Describe audio as deliberately as picture when sound matters.
- Use specific negative direction tied to likely failure modes; avoid generic quality-word piles.
- Pair every requested edit with what must remain unchanged.
