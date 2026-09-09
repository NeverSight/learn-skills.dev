---
name: auto-cartoon-animation-director
description: Build or repair warm cinematic family animated ads with scene-by-scene storyboard, native lip-sync preservation, clean audio repair, Foley, captions, and QA. Use when the owner asks for Auto Cartoon, animated ad shots, cartoon lip sync, music/voice repair, subtitles, or cinematic family short workflow.
---

# Auto Cartoon Animation Director

This skill is the portable Claude/Codex version of the Auto Cartoon method refined during the Gold Cash family short on 2026-06-16 to 2026-06-17. Source project: `<HOME>/AI Advertising/campaigns/gold`.

The job is not just to render clips. The job is to direct acting, preserve the best native performances, and make audio, captions, and story logic line up.

## Where this sits

A video FORMAT specialist invoked by `vid-ad` (the brain that picks the format and hands off the concept). Read the brief from `ad-strategy`. Gate storyboard stills through `static-qa` and the final render through `vid-qa`; the human Stage-3 gate plus `legal-compliance-checker` / the `brand-safety-gate` agent give final sign-off. The QA steps in this skill are format-specific checks (cartoon lip-sync, audio repair, Foley, captions) layered ON TOP of those shared gates, not a replacement for them. `ai-ad-pipeline` orchestrates the whole flow.

## Production Order

1. Read the product brief and workflow first.
2. Write 3 story concepts before video generation.
3. Get the owner approval on the story.
4. Write the 55 to 65 second script and shot list.
5. Generate character reference board and style frame.
6. Generate storyboard stills scene by scene.
7. Only after still approval, generate short clips by shot.
8. QA raw clips before stitching.
9. Stitch approved clips only.
10. Rebuild music, Foley, captions, and subtitles in post.
11. Watch sound-on and sound-off.
12. Save a QA note with what passed and what still needs the owner/legal approval.

## UGC Boundary

For UGC or creator-style ads, do not apply the cartoon aesthetic. Borrow only the production discipline:

- Lock story first.
- Create a reference or character anchor.
- Generate static shots before motion.
- Review a contact sheet before spending video credits.
- Generate short clips by shot.
- Verify audio, captions, and lip sync before final assembly.

UGC success criteria are different from cartoon success criteria:

- The creator should feel calm, casual, and real, not overacted.
- Avoid prompt language that makes the creator angry, suspicious, or dramatic unless the owner explicitly requests it.
- Reject identity drift, extra people, unexpected gender changes, unclear storyline, and fake customer/testimonial framing.
- If the creator is synthetic, keep disclosure in the distribution plan.

## Live-Action Adaptation

For cinematic live-action AI microfilms with synthetic everyday people, borrow the Auto Cartoon discipline but remove cartoon instincts.

- Prioritize believable ordinary behavior over dramatic reveals. If the owner says "authentic" or "real," remove glow, beams, holograms, sci-fi scan effects, treasure lighting, corporate staging, and overacted reactions.
- Build character references, style frames, and storyboard stills first. Do not spend motion credits until the stills pass product-form and realism QA.
- Use the exact generation tool when the project already has a proven path. For Gold Cash on the owner's machine, Higgsfield is reachable at `<HOME>/.local/bin/higgsfield`; image-to-video inputs should use the CLI `--image` flag.
- Raw clip review pages must include the story context, intended dialogue, final voiceover line, Chinese subtitle, shot purpose, and pass or conditional verdict. A grid of videos without the script makes the story feel missing.
- Do not stitch clips before the owner approves raw clips. After approval, copy approved clips into `approved/` and stitch only from that folder.
- Natural transitions require active motion on both sides. If a 4-second generated clip has already stopped, a crossfade over the frozen tail still feels like a hard cut. Cut shorter, transition earlier while motion is alive, generate longer clips, or add B-roll. Do not solve this by padding dead frames.
- To make a natural 55 to 65 second film from short AI clips, plan enough actual motion: longer 6 to 8 second takes, bridge B-roll, reaction shots, product close-ups, or environmental inserts. A one-minute duration target cannot be met cleanly by freezing ten 4-second clips.
- Voice, music, and Foley are not optional review layers. If there is no music bed, say that plainly. If the voice is scratch TTS, label it as review voice and replace it before public release if needed.

## Required Shot Fields

Every shot should include:

- `acting`: body action, facial expression, eye direction, emotional change.
- `dialogue_delivery`: pace, emotion, breaths, sighs, laughs, pauses.
- `lip_sync`: `model_native`, `tracked_overlay`, `keyframed_overlay`, or `none`.
- `foley`: timed cues such as footsteps, scan beeps, paper rustle, coin click, room tone.
- `take_count`: default 3 for hero/dialogue shots.
- `reject_if`: frozen body, dead eyes, wrong speaker, drifting character, text garble, off-style redraw.

## Native Voice Rule

Gold Cash lesson: model-native cartoon voices can be better than external TTS because they match the generated facial acting and lip sync.

Do not replace a good native voice just because the mix has problems.

When native audio has good acting but bad baked-in music:

1. Preserve the native performance first.
2. Try voice isolation before replacement.
3. Use cloned or generated voice only for product close-ups, phone screens, off-screen narration, or shots with no visible speaking mouth.
4. If a visible character says a new line, use a native rerender or alternate raw take where that character actually says the line.
5. Captions matching audio is not enough. Audio, subtitles, and visible mouth movement must all match.

## Lip Sync QA

Fail the shot if:

- The caption matches the audio but the visible mouth does not.
- The wrong speaker moves their mouth.
- A cloned line plays over a close-up face that is not saying the line.
- A profile icon substitutes for a real cartoon person when the owner asked for a character.

Fix options:

- Use an alternate native take.
- Rerender only the bad shot.
- Hide the speaking face with a cutaway only if it fits the story.
- Split the scene into question, action, and reaction beats.

## Captions And Labels

Subtitles must be generated from the current audio, not from an older script.

Rules:

- Bottom subtitles are only for spoken dialogue or narration.
- If nobody is visibly speaking, use small action labels, not dialogue captions.
- Keep labels sparse. One bottom subtitle plus, at most, one short top signal such as `Verified / 验证通过`.
- Split long captions into shorter timed beats.
- Captions should be smaller if they block faces, product, hands, or key actions.
- Use deterministic post overlays. Do not use model-rendered final text.

Caption QA:

- Sound-on: spoken words match subtitles.
- Sound-off: action labels explain silent product beats.
- Mobile safe zone: captions are not hidden by playback controls.
- Spot-check exact repaired timecodes.

## Product Demo Story Rule

For business/product ads, do not let cute storytelling hide the practical product lesson.

Every everyday-use animated ad should show:

- The pain: why the old way is hard.
- The product form: what the user actually holds or sees.
- Verification: how trust is checked.
- Use: what action the everyday person can take.
- Send/redeem/activation if those are part of the product.
- A final wrap-up that names the product and reinforces the core line.

If a story beat was approved, protect it through edits. Do not accidentally cut it because a later clip had better motion.

## Captions, Labels, And Subtitles

Gold Cash lesson: subtitles must be generated from the current audio transcript, not from an older approved script or prompt after audio or shot repairs.

Rules:

1. Run speech-to-text or otherwise verify the current audio before final subtitles.
2. Bottom subtitles are for spoken dialogue or narration only.
3. Product explanations that are not spoken become small action labels or signal labels, not dialogue captions.
4. If nobody is visibly speaking, avoid a dialogue-style subtitle unless it is clearly voiceover narration.
5. Do not put two competing text systems on screen. Use one bottom subtitle plus, at most, one short top signal such as `Verified / 验证通过`.
6. Split long captions into short timed beats. Smaller complete captions are better than large clipped captions.
7. Build captions as deterministic post overlays. Do not rely on model-rendered text.
8. For the owner-facing Gold Cash or bilingual campaign review exports, subtitles default to English plus Chinese unless the owner explicitly asks for English-only.
9. Subscription asks, CTAs, product labels, and verification labels are not subtitles unless they are actually spoken. Put them in an end card or separate overlay layer.

Caption QA:

- Watch with sound on: words heard should match bottom subtitles.
- Watch with sound off: action labels should explain silent product beats without pretending someone spoke.
- Check mobile safe zone: subtitles should not sit so low that playback controls cover them.
- Spot-check frames at every repaired timecode.
- Keep rejected caption renders marked in QA and preserve a clean no-subtitle base render for rebuilding.

## Patch Strategy

When the owner likes most of a cut, repair surgically.

1. Preserve what works.
2. Check existing raw takes before generating a new clip.
3. Patch the smallest segment that fixes the issue.
4. Rebuild from a muted/no-subtitle visual base if captions or audio drifted.
5. Keep separate files for no-subtitle render, captioned render, review segment, contact sheet, and QA note.

Common repairs:

- Wrong spoken line: alternate native take or rerender.
- Bad baked-in music: isolate native voice, rebuild music/Foley.
- Robotic unseen speaker: remove the voice, use action label plus Foley.
- Missing story beat: restore it with native lip sync, cutaway, or new shot.
- Profile icons where real people are needed: reject or replace.

## Music And Foley

Use one coherent background music bed across the cut unless a deliberate transition is needed. Do not stack random baked-in clip music with new music.

Required Foley categories:

- Body: footsteps, fabric, gestures.
- Props: paper note, package rustle, metal click.
- Tech: scan beep, verify chime, phone tap.
- Room: kitchen, supermarket, gas station ambience.
- Finish: soft end shimmer.

## QA Artifacts

Save:

- Raw clip QA.
- Contact sheet.
- Problem-frame screenshots.
- Short review segment for patched timecodes.
- No-subtitle render.
- Captioned render.
- QA note with pass/fail and still-needed the owner/legal approval.

Gold Cash reference QA files:

- `<HOME>/AI Advertising/campaigns/gold/qa/2026-06-17-bread-question-v6-quality-repair-qa.md`
- `<HOME>/AI Advertising/campaigns/gold/qa/2026-06-17-bread-question-v5-shot10-native-lipsync-qa.md`
- `<HOME>/AI Advertising/campaigns/gold/qa/2026-06-17-bread-question-v4-story-caption-repair-qa.md`
