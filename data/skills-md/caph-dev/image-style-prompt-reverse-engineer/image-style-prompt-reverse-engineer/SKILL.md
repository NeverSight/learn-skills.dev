---
name: image-style-prompt-reverse-engineer
description: Reverse-engineer the visual style of one or more reference images into a reusable AI image-generation prompt. Use when the user asks to analyze an image style, extract an aesthetic, preserve the look while changing the subject, or produce a general prompt stripped of specific characters, text, brands, or plot details.
---

# Image Style Prompt Reverse Engineer

## Overview

Use this skill to inspect a reference image and produce a polished, reusable image-generation prompt that captures the image's aesthetic DNA without copying its concrete subject matter.

## Workflow

1. Confirm that at least one reference image is available in the conversation or via a usable local path. If no image is available, ask the user to provide one.
2. Inspect the image visually and infer the style across the required dimensions below.
3. Strip away all source-specific content: named characters, recognizable identities, exact text, logos, brands, plot events, and other non-style details.
4. Preserve the aesthetic structure: composition, medium, color, lighting, texture, atmosphere, spatial treatment, rendering traits, and production feel.
5. Output only the final prompt text unless the user explicitly asks for analysis, explanation, variants, or a breakdown.

## Required Internal Analysis Dimensions

Cover these dimensions internally before writing the prompt:

- Visual style: genre, art direction, realism level, stylization, and overall image language.
- Image components: foreground, midground, background, subject-to-environment balance, props, and environmental layers.
- Composition: framing, symmetry/asymmetry, balance, focal hierarchy, cropping, scale, and visual flow.
- Shot or storyboard type: close-up, medium shot, wide shot, cinematic still, editorial frame, concept art frame, poster-like layout, panel-like scene, or other framing logic.
- Light and shadow: lighting source, contrast ratio, shadow softness, highlight behavior, rim light, bounce light, volumetric light, and practical light.
- Tone and color science: palette, saturation, contrast curve, temperature, filmic response, color grading, and hue relationships.
- Medium and material texture: paint, ink, 3D render, analog photo, digital illustration, grain, paper, brushwork, surface wear, lens artifacts, or material finish.
- Mood and atmosphere: emotional register, tension, softness, solitude, grandeur, mystery, nostalgia, warmth, coldness, or dreamlike quality.
- Rendering or capture parameters: camera/lens feel, depth of field, exposure, aperture, focal length, motion blur, render engine cues, resolution feel, and detail handling.
- Historical period and cultural context: retro, contemporary, futuristic, regional visual codes, fashion era, design lineage, or art-historical references.
- Spatial logic and perspective: depth layers, horizon line, vanishing points, lens compression, architectural logic, spatial distortion, or flat graphic space.
- Information density and negative space: ornament level, clutter, silence, readable empty areas, and density distribution.
- Dynamic state and instantaneity: whether the image feels posed, frozen mid-action, drifting, suspended, explosive, quiet, or documentary.
- Post-processing and digital traces: bloom, halation, chromatic aberration, film grain, sharpening, AI-render smoothness, glitch, scan, compression, or compositing marks.
- Symbolic features: recurring shapes, motifs, iconography, visual metaphors, silhouette language, and abstracted signs.

## Prompt Construction Rules

- Begin the final prompt with, or place near its core, the exact placeholder: `[Replace this with the main content you want to generate]`.
- Make the prompt general enough that replacing the placeholder creates a new image with the same style rather than a copy of the reference.
- Describe style traits as transferable instructions, not as references to the original image.
- Prefer concrete visual language over labels alone. For example, pair "cinematic" with lighting, framing, lens, contrast, and color behavior.
- Include enough production detail for image models to reproduce the look: composition, lighting, palette, material texture, atmosphere, perspective, and rendering/capture traits.
- Avoid source-specific nouns unless they describe generic style elements. Do not mention exact characters, original text, logos, brands, celebrity identities, or unique plot details.
- Do not include an analysis section, bullet list, title, markdown fencing, or explanation when the requested output is the prompt itself.
- Keep the final prompt as one fluent paragraph unless the user asks for multiple variants or a structured format.

## Output Pattern

Use this pattern as a guide, adapting the wording to the actual reference image:

`Start with the required subject placeholder, then continue as one polished Chinese prompt paragraph that compactly specifies the transferable visual style: image genre, subject-environment layering, composition and shot language, lighting behavior, color science, material texture, emotional atmosphere, spatial perspective, information density, sense of motion or frozen instant, post-processing traces, symbolic features, and any necessary rendering or capture parameters.`

## Quality Checklist

Before finalizing, verify that:

- The prompt is written in English unless the user requested otherwise.
- The placeholder appears exactly as `[Replace this with the main content you want to generate]`.
- The prompt is reusable with a different subject.
- The original image's specific identity, text, brands, and plot have been removed.
- The 15 style dimensions are represented either explicitly or through compact descriptive phrases.
- The answer contains only the final prompt text unless the user requested an analysis.
