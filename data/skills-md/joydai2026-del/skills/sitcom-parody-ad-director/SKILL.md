---
name: sitcom-parody-ad-director
description: Direct sitcom-inspired parody ads and mockumentary AI videos from product brief to transcript/style mining, archetype design, script beats, shot lists, reference boards, image-to-video generation, lip-sync/audio post, captions, and QA. Use when Codex is asked for Office-style, Friends-style, workplace comedy, sitcom parody, mockumentary, ensemble comedy, talking-head reaction, or comedy ad workflows for products.
---

# Sitcom Parody Ad Director

## Overview

Use this skill to make a product ad feel like a workplace sitcom, mockumentary, or ensemble comedy without copying dialogue, exact character likenesses, or voice performances. Favor repeatable comedy grammar: cold open, talking head, awkward meeting, reaction shot, practical prop demo, button joke.

A video FORMAT specialist invoked by `vid-ad`. Read the brief from `ad-strategy`; gate storyboard stills through `static-qa` and the final render through `vid-qa` (this skill's QA gate is format-specific comedy checks layered on top, not a replacement). `ai-ad-pipeline` orchestrates the campaign. For Gold Cash, the live `PRODUCT-BRIEF.md` wins over all memory.

For detailed genre patterns, read `references/sitcom-parody-patterns.md` when writing a script, shot list, or production plan.

## Workflow

1. **Lock the product argument**
   - Read the product brief, campaign config, and current claim constraints.
   - State the one useful product truth the comedy must reveal.
   - For Gold Cash, keep the product as light paper-cash-like notes with embedded precision-cut gold or silver, phone verification, and approved use rails. Reject bars, coins, glitter, fake bills, fake balances, fake merchant proof, and QR-square drift.

2. **Mine the reference, do not copy it**
   - Use transcripts and datasets to analyze structure, rhythm, character functions, scene types, line length, and reaction timing.
   - Do not paste show dialogue into the ad. Write new lines around the product.
   - Do not recreate exact living actors, celebrity voices, or named show characters unless rights and approvals are explicitly in the production file. Safer default: fictional archetypes inspired by function, not identity.

3. **Build archetypes**
   - Assign each character a product-objection role.
   - Good Gold Cash trio:
     - Overconfident manager: misunderstands cash, says confident wrong things.
     - Security obsessive: distrusts cold cash, loves verification once shown.
     - Grounded receptionist or operations person: asks the practical question and lands the useful truth.
   - Keep names fictional and reusable across brands.

4. **Write a short comedy spine**
   - Best first pilot: 30 to 45 seconds.
   - Structure: cold open problem, awkward office escalation, talking-head confession, product reveal, verification beat, button joke.
   - Keep the product reveal late enough to feel like an answer, early enough that the ad is still useful.
   - Make one joke from human suspicion, not from mocking the product.

5. **Create reference boards before motion**
   - Make character sheets, office set sheet, prop sheet, and product close-up sheet.
   - Create stills for each shot and a contact sheet.
   - Get approval before video generation.

6. **Generate shot by shot**
   - Use image-to-video from approved stills. Do not generate a whole episode in one prompt.
   - Keep each dialogue shot short: 3 to 6 seconds.
   - Use talking-head closeups for lip sync, office reaction shots for pacing, and product insert shots for clarity.
   - Add brand text, subtitles, labels, and legal copy in post, not in the video model prompt.

7. **Audio and captions**
   - Prefer one coherent voice performance per speaker or performance-capture/lip-sync pass.
   - If model-native dialogue is unreliable, mute raw audio and rebuild dialogue, foley, room tone, and music in post.
   - Subtitles must match the actual spoken audio. For the owner-facing Gold Cash review cuts, default to English plus Chinese unless asked otherwise.

8. **QA gate**
   - Open and watch raw clips before stitching.
   - Build a raw clip review page with script context, intended dialogue, Chinese subtitle, shot purpose, and verdict.
   - Approve only usable clips into `approved/`.
   - Final QA covers visual continuity, product truth, lip sync, subtitles, audio balance, safe zones, and disclosure state.

## Recommended Stack

- Transcript/style mining: Kaggle CSVs, `schrute` R package data, Python pandas, simple scene-beat analysis.
- Reference video inspection: `yt-dlp --skip-download --print` for metadata, `ffmpeg` for frame grids if a local reference clip is permitted.
- Character and set stills: image model or Higgsfield image tools, with fictional archetypes.
- Video: Higgsfield Seedance/Veo/Kling path for fast proof; Runway Act-Two for performance-driven talking heads; ComfyUI only when owning the pipeline matters more than speed.
- Lip sync fallback: MuseTalk or another reviewed lip-sync repo after repo-safety scan.
- Stitching: HyperFrames when captions, audio ducking, and end cards matter; ffmpeg for simple joins/contact sheets.

## Output Files

For each serious parody ad, save:

- reference-analysis note
- archetype bible
- full script and timing
- shot list
- still board and contact sheet
- raw clips, approved clips, rejected clips with reasons
- final render
- subtitle files
- QA note
