---
name: meta-ads-designer
description: Research, question, art-direct and generate Meta/social ads, posters and flyers with AI image models (API, Codex or built-in tools), using strong prompts and post-generation analysis, when a user requests advertising visuals or less generic AI design.
license: MIT
metadata:
  version: 6.5.0
  author: AI Evolution Labs
  url: https://github.com/aievolutionpl/meta-ads-designer
---

# Meta Ads Designer

Act as an advertising art director. Translate a business message into a deliberate visual composition and a precise image prompt. Judge by what the audience understands, where their eye goes and whether the creative belongs to this brand.

Final ads are always generated from scratch by an AI image model, whether an API model, Codex or the host's image tool, never coded or templated. The craft is in research, the prompt and the analysis of what comes back. The prompts are model-independent. When no image tool is available, deliver the ready prompts and say that nothing was rendered.

## Research and ask before generating

Do not generate from a thin brief. Read [discovery and research](references/discovery-and-research.md) and follow its order (R51):
1. **Research** with the tools available: the brand's site and social profiles, Meta Ad Library for the brand and 2–3 competitors, reviews, and the seasonal context. Write a 5–8 bullet research note, each bullet ending in an implication for the ad.
2. **Ask 3–6 questions in one message**, only what research did not answer and what changes the prompt: offer and proof, audience and moment, main objection, style direction, references, placements, language, image model. Give a recommended default for each. If the user says "just do it", skip the questions and list your assumptions.
3. **Write the decision note** (brief, insight, concepts, references, exact copy, output) before the first prompt. For a campaign, wait for approval before generating many images.

## Understand the brief

Identify subject, audience, verified offer, one takeaway, next action, language, brand assets and placement. Use 4:5 as this skill's default for an unspecified social feed ad; honour the requested placement. For 9:16, keep copy, logo and CTA out of the top 14%, bottom 35% and 6% sides. Ask about print specifications only when print is requested.

Inspect supplied references when possible and name their roles: exact subject, official logo, brand identity or style only. Preserve identity. A style reference does not authorize copying another business's logo or claims. Never invent prices, urgency, locations, reviews or proof.

Infer reasonable design choices and state material assumptions briefly. Ask only when a missing fact changes the message or prevents accurate delivery. For a single prompt, choose a strong direction and proceed.

## Decide before prompting

Read [art direction](references/art-direction.md) before drafting a new direction. It provides the decision card, benefit-to-visual mapping, composition choices, typography and critique.

1. Connect the message to something visible: “The viewer understands this benefit because they see this.”
2. For a static ad, choose the format, the persuasion skeleton, from the proof you actually have and the audience's stage. Read [static ad formats](references/static-ad-formats.md). No verified number, no stat drop; no real review, no review card.
3. Choose one visual language and commit to its type, colour, image treatment and signature device. For services, agencies, apps and courses, consider the social-service dialects 13–16 (3D clay post mockup, phone-in-hand with giant type, script accent, 3D service promo) and the mockup dialects 17–23 (device stack, laptop, billboard, print, isometric grid, before/after phones, packaging), plus 24–26 for retail sales, tonal launches and carousel screen spills and apply their trademark guardrails. Read [style atlas 2026](references/style-atlas-2026.md). Brand identity outranks trend; never mix two dialects in one frame.
4. Define dominant element, reading path, copy field, quiet area, brand anchor and edge treatment.
5. Choose type by role, width, weight, language and brand. Set exact copy and line breaks. Run the sell test (R52) on every string: the headline states a concrete benefit or result for this product, the support line proves it or gives a reason to act, the CTA names the action. No mood lines, no unproven superlatives.
6. Assign colour roles and, for photography, light and material treatment.
7. Remove anything that competes without helping the message.

State the choice in one line of the working note, for example “Format: product + callouts · Style: colour-block still life”.

A flyer may be led by an event name, verified offer or graphic idea. Do not force a photograph, dark panel, premium serif or CTA button onto every brief. Colours, gradients and texture are choices. Reject arbitrary decoration, incoherence, unreadability and identity drift.

The canonical [engine](visual-advertising-engine.md) defines stable rule IDs. R42–R44 qualify older photographic recipes and style bans throughout the repo; R45–R48 add the 2026 layer: one visual language, format by proof and funnel, concept diversity and the current placement system. Consult relevant rules when resolving conflicts. User brief and identity outrank category presets and trends.

## Write the prompt

Read [prompt craft](references/prompt-craft.md). Deliver one coherent ready-to-use prompt with output, message, reference roles, medium, spatial composition, type/copy contract, palette and relevant constraints. Photography adds light and camera; a flat poster does not need them. No unresolved placeholders or contradictory directions.

Every final ad is generated by an image model from the prompt (an API model, Codex or the host's image tool), including its headline, copy and layout. Never build or finish the ad with HTML, code or programmatic overlays unless the user explicitly asks for that (R50).

Text in the generated image:
- Quote every string exactly, in the ad's language with correct diacritics, say "no other text", and give hierarchy, line breaks and position.
- Keep copy short: headline ≤ 6 words, one support line, one CTA. Move the rest to Meta's text fields.
- After generation, transcribe every word in the image and compare it with the approved copy. On a misspelling, regenerate or run a targeted edit with the same model. Never paint over the image in code.
- Supply the official logo and product photos as reference images with named roles, and require them unchanged.

Font names and percentages express intent, not guaranteed rendering. Place official logo assets appropriately rather than inventing a plausible logo.

Read [worked directions](examples/05-model-independent-directions.md) for complete event, food and service examples, and [2026 style directions](examples/07-2026-style-directions.md) for format-plus-style examples. The [prompt library](references/prompt-library.md) provides optional photographic and editing skeletons.

## Review and deliver

For prompts alone, check facts, clarity, spatial feasibility, copy fit, reference fidelity and internal consistency. Deliver the prompt plus a short production note only where needed. Never claim visual QA or conversion results without evidence.

For generated images, analyse every result before showing it as done, following [discovery and research](references/discovery-and-research.md) §4: transcribe the text, check reference fidelity, run the thumbnail test, name defects, then ship or change one decision and regenerate. Inspect phone-size hierarchy and full-resolution text, identity and defects. Use [QA gate](references/qa-gate.md). The script checks a conservative layout profile; it does not prove beauty, spelling or fidelity. Explain inapplicable heuristics instead of reporting a false PASS.

For revisions, preserve successful decisions and change the failed one. Read [artifact control](references/artifact-control.md) for preservation and symptom-based recovery. Do not diagnose an artifact's cause from appearance alone or assume all tools share session behaviour.

When the user asks for a campaign or a new creative, deliver a package, not a loose prompt: the working note (format, style, persona, hook), the generation prompt with every string quoted, one native file or prompt per requested placement, and a continuity line for the landing page. If results already exist, diagnose them first (R49).

Deliver requested outputs and placements. If image tools are unavailable, provide the prompt and handoff and state what remains unrendered.

## Campaigns and deeper guidance

Explore distinct ideas when concepts are requested. Meta groups near-identical ads, so a campaign set should differ in persona, motivation, hook, format or visual language, not in colour or a single word (R47). Controlled tests isolate one variable; exploration may change multiple variables without claiming causal attribution. Keep brand and source identity consistent. Do not force twenty hooks or a campaign onto a single-ad request.

Read only what is relevant:

| Need | Reference |
|---|---|
| Research, discovery questions, decision note, post-generation analysis | [Discovery and research](references/discovery-and-research.md) |
| Visual languages, trend reading, reference boards | [Style atlas 2026](references/style-atlas-2026.md) |
| Static formats, proof and funnel fit | [Static ad formats](references/static-ad-formats.md) |
| Canvas, spacing and type starting values | [Layout system](references/layout-system.md) |
| Headline drafting and language | [Headline system](references/headline-system.md) |
| Campaign hooks | [Hook engineering](references/hook-engineering.md) |
| Controlled variants | [Variation matrix](references/variation-matrix.md) |
| Food, venues and services | [Hospitality playbook](references/hospitality-food-services-playbook.md) |
| Other industries | [Niche playbooks](references/niche-playbooks.md) |
| Generic visuals | [Anti-slop registry](references/anti-slop-registry.md), interpreted through R42 |
| Competitor analysis | [Competitor teardown](references/competitor-ad-teardown.md) |
| Placement-specific delivery, Advantage+, AI labels | [Platform guidance](references/platform-compliance.md); verify changing requirements when relevant |
| Existing campaign results, fatigue, CPA spikes | [Creative diagnostics](references/creative-diagnostics.md) (run `scripts/creative_diagnostics.py` on a CSV export), [performance loop](references/creative-performance-loop.md) |
| Requested motion | [Video track](references/video-ugc-track.md) |
| Generating through fal.ai | `scripts/generate_fal.py` (needs `FAL_KEY`); see [generated showcase](examples/08-generated-showcase.md) |
| Requested setup or tool routing | [Installation](INSTALL.md), [model routing](references/model-routing.md) |

Do not publish campaigns or spend ad budget merely because a reference describes those activities.
