---
name: scenario-video-ads
description: "Use when producing a video ad with Scenario from a product shot or brand assets: a mobile 9:16 or landscape 16:9 commercial, a TikTok, Reels, Shorts, YouTube, or CTV spot, or campaign creative needing a creative brief, storyboard, cinematic camera work, brand-faithful product footage, music and voiceover, captions, ad variants, budget planning, or platform delivery specs. Keywords: video ad, commercial, product video, advert, hook, CTA, end card, campaign, ad creative."
license: MIT
---

# Scenario Video Ads

## Overview

This skill is the director layer: it turns one product shot and a brief into a finished ad, delegating mechanics to the sibling skills it names per stage. Connection and the core loop: see the `scenario` skill in this repo. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap. The full sibling map and install commands: [references/dependencies.md](references/dependencies.md).

Two rules bind every stage, because they carry the ad's credibility. The product is never generated: every product shot starts from the uploaded photo, as a first frame or composited into an approved still. Text is never generated: logos, taglines, prices, and legal lines are overlaid in assembly on text-free plates.

Ask the brief once, then run without stopping. The one approval that matters sits between the priced storyboard and generation: video is the expensive stage, so the user signs off on the budget table first. The concept page and the stills are cheaper checkpoints: show them when someone can answer. In a run where nobody can, continue: the brief's spend ceiling stands in for the sign-off, so generate video only while the priced board fits it, and the fidelity gate stands in for still approval.

## Quick reference

| Stage            | What happens                                                                                                     | Detail                                                             |
| ---------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| 1. Brief         | One objective, audience, proposition, creativity and length dials, platforms, mandatories, spend ceiling         | [references/brief.md](references/brief.md)                         |
| 2. Concept       | One page, anchored to a named famous-ad pattern, shown to the user                                               | [references/storyboard.md](references/storyboard.md)               |
| 3. Storyboard    | Beats and panels per the objective's rulebook, priced shot by shot with `dry_run`, approved                      | storyboard.md, brief.md                                            |
| 4. Stills        | Composed natively per delivery ratio, product composited from the real photo, approved before animating          | `scenario-image`, `scenario-consistency`                           |
| 5. Animate       | Image-to-video per approved still, one camera move, `generateAudio: false` where the schema has it, `wait=false` | `scenario-video`, `scenario-seedance`                              |
| 6. Fidelity gate | Extract frames from every product or character clip, spot-the-difference against the approved reference          | storyboard.md, `scenario-asset-analysis`                           |
| 7. Audio         | Music generated on the cut's beat grid, voiceover to a word budget, sonic logo                                   | `scenario-audio`, [references/delivery.md](references/delivery.md) |
| 8. Assemble      | Timeline, text cards from `scenario-text-overlay` as image layers, captions in safe zones                        | `scenario-video-assembly`, delivery.md                             |
| 9. Pre-flight    | Policy, flashes, sound-off pass, loudness, spend report                                                          | delivery.md                                                        |

## Worked example: a perfume ad, 9:16, 20 seconds

1. Brief once: awareness, twist creativity, 20s for Reels and TikTok, ceiling in CU. Upload the product shot, then build the fidelity checklist from it with `asset_analyze`, instructing it to inventory label text, cap geometry, and glass tint: every later check reuses it (`asset_describe` returns a style line, not this inventory).
2. Concept names its anchor: open inside the gala-and-gown cliche, break it on beat three. Show the page to the user.
3. Storyboard 7 panels at 2 to 4 seconds each, hero shot designed first, 3 hook variants, 2 inserts as cut cover. `dry_run` every planned run, multiply by retry floors, present the budget table.
4. Stills at 9:16: composite the real bottle into styled plates with an image-edit model, baseline-plus-delta prompts. Each still is approved before animating, by the user or by the fidelity checklist when nobody can answer: image money is cheap, video money is not.
5. Animate each approved still: `model_schema_get` first, prompt movement first ("slow push-in over 4 seconds, the bottle rests fixed in place"), `generateAudio: false` when the schema lists it.
6. Gate every clip: frame-extract, then one `asset_analyze` call against the checklist. Label drift fails the clip; regenerate from the same still, never from the drifted output.
7. Music at a stated BPM so cuts land on bars; compose the timeline, `scenario-text-overlay` renders the tagline card into the safe zone; caption the master.
8. Pre-flight per delivery.md, then report spend from `usage` against the approved board.

## Common mistakes

- Reaching for local ffmpeg or a desktop editor for the cut: assembly is `model_run` on Scenario tool models (see `scenario-video-assembly`).
- Letting the video model render a label, logo, tagline, or price: generated type drifts frame to frame; composite text in post.
- One long clip at the schema's maximum duration: generate 3 to 5 second product shots and 5 to 10 second coverage, then cut to rhythm in assembly.
- Judging fidelity by watching a clip once: drift hides between glances; run the frame-extract gate.
- Leaving the schema's audio toggle (`generateAudio`, where offered) at its default: the soundtrack is built in assembly, so clips with baked-in audio fight the bed.
- Cropping a 16:9 master to 9:16: each ratio is its own composition, decided at the storyboard.
- Two objectives in one brief: brand and performance in the same asset serves neither; make two cuts from one board instead.
- Shipping without the pre-flight: a sensual perfume cut or a wrong-length CTV file dies in ad review, not in generation.
