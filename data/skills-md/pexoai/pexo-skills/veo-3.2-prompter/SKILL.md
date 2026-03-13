---
name: veo-3.2-prompter
description: >
  Expert prompt engineering for Google Veo 3.2 (Artemis engine). Use when the user wants to generate a video with Veo 3.2, needs help crafting cinematic prompts, or mentions Veo, Google video generation, or Artemis engine.
version: 0.1.0
author: wells
tags: [video, generation, prompt, veo, google, artemis, cinematic]
---

# Veo 3.2 Prompt Designer Skill

This skill transforms a user's scattered multimodal assets (images, videos, audio) and creative intent into a structured, executable prompt for the Google Veo 3.2 video generation model (Artemis engine). It acts as an expert prompt engineer, ensuring the highest quality output from the underlying model.

## When to Use

- When the user provides assets (images, videos, audio) for video generation with Veo 3.2.
- When the user's request is complex and requires careful prompt construction for the Veo model.
- When using any Google Veo 3.x model for video generation.

## Core Function

This skill analyzes all user inputs and generates a single, optimized JSON object containing the final prompt and recommended parameters. The internal workflow (Recognition, Mapping, Construction) is handled automatically and should not be exposed to the user.

### Internal Workflow

1. **Phase 1: Recognition** — Analyze uploaded assets and user intent. Use the `atomic_element_mapping.md` to classify each asset into its atomic element role(s).
2. **Phase 2: Mapping** — For each atomic element, determine the optimal reference method (reference image, text prompt, or hybrid). Use the mapping table to decide.
3. **Phase 3: Construction** — Assemble the final prompt using the 5-Part Framework (Shot → Subject → Environment → Camera → Style) and attach reference images via the Gemini API's `RawReferenceImage` system.

## Usage Example

**User Request:** "Make a cinematic shot of this perfume bottle rotating on a dark surface, like a luxury commercial."
*User uploads `perfume.png`*

**Agent using `veo-3.2-prompter`:**
*The agent internally processes the request and assets, then outputs the final JSON to the next skill in the chain.*

**Final Output (for internal use):**
```json
{
  "final_prompt": "Hero shot, a frosted glass perfume bottle with gold cap rotating slowly on a reflective dark surface, three-point studio lighting with soft key and rim light creating subtle caustics, smooth 180-degree arc, hyper-realistic luxury commercial style with shallow depth of field. Crystalline chime, soft ambient pad.",
  "reference_images": [
    {
      "file": "perfume.png",
      "reference_type": "SUBJECT"
    }
  ],
  "recommended_parameters": {
    "model": "veo-3.2-generate",
    "duration_seconds": 8,
    "aspect_ratio": "16:9",
    "resolution": "1080p",
    "generate_audio": true
  }
}
```

## Veo 3.2 Key Differentiators

| Feature | Capability |
|---|---|
| Engine | Artemis — world-model physics simulation (not pixel prediction) |
| Max duration | ~30s native continuous generation |
| Audio | Native dialogue + synchronized SFX |
| Reference images | Up to 3 (`STYLE`, `SUBJECT`, `SUBJECT_FACE`) |
| Video extension | Chain clips via previous video input |
| First/last frame | Specify start and/or end keyframes |
| Resolutions | 720p, 1080p, 4K (with upscaling) |
| Aspect ratios | 16:9, 9:16 |

## Knowledge Base

This skill relies on an internal knowledge base to make informed decisions. The agent MUST consult these files during execution.

- **`references/atomic_element_mapping.md`**: **Core Knowledge**. Contains the "Asset Type → Atomic Element" and "Atomic Element → Optimal Reference Method" mapping tables, adapted for Veo 3.2's reference image system.
- **`references/veo_syntax_guide.md`**: Veo 3.2 Gemini API syntax reference, covering `RawReferenceImage`, `GenerateVideosConfig`, video extension, and first/last frame specification.
