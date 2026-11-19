---
name: review-video
description: Review a Remotion video with AI vision. Starts with a cheap local check of rendered still frames, then has TwelveLabs watch the full render and score it against a JSON rubric (pacing, composition, text legibility, audio sync and more) with timestamped fixes, applies the fixes and re-reviews. The feedback loop that closes the production circle.
---

# Review Video — AI-Powered Video Feedback Loop

You are reviewing a Remotion video and providing professional feedback: first from a few rendered frames, then by having TwelveLabs "watch" the full render. This closes the production loop — preview, review, improve, repeat.

**Load the `remotion-production` skill** for the `video-analysis` rule. Rendering follows the official `remotion-render` skill.

**Rendering is allowed here.** Invoking `/review-video` is an explicit request to render for review, so you don't need to ask again.

## Workflow

### 1. Quick Frame Check (cheap, local)

Before uploading anything, render a handful of still frames and look at them yourself, as official `remotion-render` shows:

```bash
npx remotion render [CompositionId] out/review-frames --frames=0,45,90,150,240 --image-format=png
```

Pick frames that cover the hook, each scene's midpoint, the busiest moments (captions, overlays) and the last frame. Read the PNGs and check:
- Blank or empty frames, missing assets (a missing `staticFile()` shows as nothing or an error)
- Text readability, overflow and safe areas (official `remotion-create/video-layout.md`)
- Caption placement against the platform UI (the `captions-workflow` rule)

If these frames show obvious bugs, fix them first (see step 6) and repeat this step. That's much cheaper than a full render plus a TwelveLabs upload.

### 2. Render the Full Video

Look for an existing render:

```bash
ls -t out/ 2>/dev/null | grep -E '\.(mp4|webm|mov)$'
```

If there's none, or the code changed since it was made, render it now:
```bash
npx remotion render [CompositionId] out/video.mp4
```

### 3. Upload the Render to TwelveLabs

```
create-asset:
  file: [absolute path to the render, e.g. /path/to/project/out/video.mp4]
```

Keep the returned asset ID. No index is needed. If the analyse call says the asset isn't ready, wait a few seconds and retry.

### 4. Analyze — The Director's Review

Run **one** `sync-analyse-video` call that returns the whole review as JSON (renders over 1 hour: `async-analyse-video` with the same `prompt` and `jsonSchema`, then poll `get-analyse-task`):

```
sync-analyse-video:
  assetId: [asset ID]
  modelName: "pegasus1.5"
  temperature: 0.2
  prompt: "You are a video director reviewing a [duration]s [platform] video at [WxH]. Intent: [one-line brief]. Script: [narration, per scene]. Score each dimension 1-10 and list concrete fixes with timestamps in seconds. Check: framing and composition; whether on-screen text is readable and on screen long enough; transitions; blank, frozen or glitchy frames; pacing (scenes too long or too short); whether the voiceover matches what's on screen; SFX timing; music mood and level under the voice; whether the first 3 seconds hook; whether the CTA is clear."
  jsonSchema: [the rubric below]
```

Always pass `modelName: "pegasus1.5"`: the server's default model has been removed from the API.

**Rubric (`jsonSchema`):**
```json
{
  "type": "object",
  "properties": {
    "overall_score": { "type": "integer", "description": "1-10" },
    "scores": {
      "type": "object",
      "properties": {
        "hook": { "type": "integer", "description": "1-10, first 3 seconds" },
        "pacing": { "type": "integer", "description": "1-10" },
        "composition": { "type": "integer", "description": "1-10, framing and layout" },
        "text_legibility": { "type": "integer", "description": "1-10, size, contrast, time on screen" },
        "transitions": { "type": "integer", "description": "1-10" },
        "audio_sync": { "type": "integer", "description": "1-10, voiceover and SFX against visuals" },
        "audio_mix": { "type": "integer", "description": "1-10, voice clarity, music level" },
        "cta": { "type": "integer", "description": "1-10, clarity of the ending" }
      },
      "required": ["hook", "pacing", "composition", "text_legibility", "transitions", "audio_sync", "audio_mix", "cta"]
    },
    "working": { "type": "array", "items": { "type": "string" } },
    "fixes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "start": { "type": "number", "description": "seconds" },
          "end": { "type": "number", "description": "seconds" },
          "dimension": { "type": "string", "enum": ["hook", "pacing", "composition", "text_legibility", "transitions", "audio_sync", "audio_mix", "cta", "glitch"] },
          "severity": { "type": "string", "enum": ["critical", "major", "minor"] },
          "issue": { "type": "string" },
          "fix": { "type": "string" }
        },
        "required": ["start", "end", "dimension", "severity", "issue", "fix"]
      }
    },
    "priority_fix": { "type": "string" }
  },
  "required": ["overall_score", "scores", "working", "fixes", "priority_fix"]
}
```

Save the JSON (e.g. `out/review-1.json`) so the next pass can be compared with this one, then clean up:

```
delete-asset:
  assetId: [asset ID]
```

Every review uploads a new asset, and assets count against the account's storage.

To look closer at one stretch (say a fix at 12-18 s), run `sync-analyse-video` again with `startTime`/`endTime` around it (the window must be at least 4 s) before deleting the asset.

### 5. Present the Review

Format the JSON as a professional director's review. Convert each fix's timestamps to frames (`Math.round(seconds * fps)`) and name the scene it falls in, so the fix points at code:

```
🎬 Video Review: [filename]
Duration: [X]s | Resolution: [WxH]

📊 Overall Score: [overall_score]/10
   Hook [x] · Pacing [x] · Composition [x] · Text [x] · Transitions [x] · Audio sync [x] · Mix [x] · CTA [x]

✅ What's Working:
  - [working[0]]
  - [working[1]]

⚠️ Improvements Needed (by severity):
  1. [CRITICAL] [start]-[end]s (frames [a]-[b], [scene]) [issue] → [fix]
  2. [MAJOR] ...
  3. [MINOR] ...

🎯 Priority Fix:
  [priority_fix]

🔄 Next Steps:
  - [ ] [actionable task 1]
  - [ ] [actionable task 2]
  - [ ] [actionable task 3]
  Then run /review-video again.
```

Cross-check the AI review against your own frame check from step 1; if they disagree on something visible, trust the frames and say so.

### 6. Implement Fixes

Ask the user if they want to apply the suggested fixes. If yes:
1. **Preserve user changes.** Re-read the files before editing. If the user changed the code or edited things in Studio since the last turn, keep their edits and apply the fixes on top; ask if a fix would undo one of them.
2. Make the code changes, critical and major first
3. Check them in Studio (`npx remotion studio`, or `--no-open` with an in-app browser; open the URL it prints). Studio stays open while you iterate.
4. Re-render (step 2) and re-review (steps 1-5) to verify the improvements, comparing the new scores with the saved JSON

### 7. Iteration Loop

Keep iterating until the user is satisfied or the review shows no major issues.

The loop: **Frame check → Render → Upload → Analyse with the rubric → Delete asset → Fix (in Studio) → Re-render → repeat** until quality is right.

## Review Checklist

For each review, check these items:

**Visuals:**
- [ ] No blank/empty frames
- [ ] Text is readable at target resolution
- [ ] Colors are consistent throughout
- [ ] Animations are smooth (no stuttering)
- [ ] Images/footage are high quality (not pixelated)

**Audio:**
- [ ] Voiceover is clear and audible
- [ ] Music volume doesn't overpower voice
- [ ] Sound effects are timed correctly
- [ ] No audio clipping or distortion
- [ ] Fade in/out at start and end

**Structure:**
- [ ] Strong opening hook (first 2-3 seconds)
- [ ] Clear narrative flow
- [ ] Appropriate pacing for platform/audience
- [ ] Clean ending with CTA (if applicable)
- [ ] Total duration matches target

**Technical:**
- [ ] Correct aspect ratio (16:9 or 9:16)
- [ ] Correct FPS (30 or 60)
- [ ] File size reasonable for target platform
- [ ] No rendering artifacts
