---
name: comfyui-prompt-engineer
description: Craft model-specific prompts optimized for the target checkpoint and identity method. Handles FLUX, SDXL, SD1.5, and Wan video models with proper syntax, quality tags, and negative prompts. Use when generating or refining prompts for ComfyUI workflows.
user-invocable: true
metadata: {"openclaw":{"emoji":"✍️","os":["darwin","linux","win32"]}}
---

# ComfyUI Prompt Engineer

Generates optimized prompts tailored to specific models and identity methods. Different models respond differently to prompts.

## Model-Specific Prompt Rules

### FLUX.1 (dev/schnell/Kontext)

- **Style**: Natural language descriptions work best
- **CFG**: 3.5-4 (very low)
- **Quality tags**: Minimal - FLUX doesn't need "masterpiece, best quality"
- **Length**: Medium (50-100 words)
- **Structure**: `{subject description}, {setting}, {lighting}, {camera/style}`

**Good FLUX prompt:**
```
photorealistic portrait of a woman with auburn hair and green eyes, freckles across
her nose and cheeks, wearing a cream knit sweater, sitting in a cafe with warm ambient
lighting, shallow depth of field, shot on Sony A7IV, 85mm lens
```

**Bad FLUX prompt (too many quality tags):**
```
masterpiece, best quality, 8k uhd, highly detailed, photorealistic portrait...
```

### SDXL (RealVisXL, Juggernaut, etc.)

- **Style**: Quality tags at front help significantly
- **CFG**: 7-9
- **Quality tags**: Include `masterpiece, best quality, photorealistic`
- **Length**: Medium-long (50-150 words)
- **Structure**: `{quality tags}, {trigger word}, {subject}, {details}, {setting}, {style}`
- **Weighted syntax**: Supported `(important:1.3)` or `((very important))`

**Good SDXL prompt:**
```
masterpiece, best quality, sage_character, photorealistic portrait of a woman,
detailed skin texture with freckles, emerald green eyes, auburn copper hair,
natural lighting from window, indoor setting, shallow depth of field,
RAW photo quality, 8k uhd, film grain
```

### SD 1.5

- **Style**: Tag-based works best
- **CFG**: 7-8
- **Quality tags**: Essential
- **Length**: Shorter (30-80 words)
- **Structure**: `{quality}, {trigger}, {subject}, {details}, {style tags}`

### Wan 2.1/2.2 (Video)

- **Style**: Concise motion descriptions
- **CFG**: 5-7
- **Quality tags**: Minimal
- **Length**: Short (20-50 words)
- **Focus**: Describe the motion, not just the appearance
- **Structure**: `{subject}, {action/motion}, {setting}, {quality}`

**Good Wan prompt:**
```
young woman with auburn hair, talking naturally with gentle hand gestures,
seated at a modern desk, soft studio lighting, high quality
```

### AnimateDiff

- **Style**: Same as base model (SD1.5/SDXL) but add motion keywords
- **Motion keywords**: Include camera/subject motion description
- **Length**: Same as base model

## With Identity Methods

### InstantID Prompts

**Key adjustments:**
- DO NOT describe specific facial features (the model provides them)
- DO describe everything else: clothing, pose, setting, lighting
- Keep CFG at 4-5

```
photorealistic portrait, wearing black leather jacket, standing in an alley,
dramatic side lighting, urban setting, moody atmosphere, 8k quality
```

### PuLID Prompts

**Key adjustments:**
- Can include some facial descriptions (PuLID is more tolerant)
- Method "neutral" for realistic, "fidelity" for exact match
- CFG 5-7

```
sage_character, photorealistic portrait, green eyes visible, natural makeup,
professional headshot, neutral grey background, studio lighting
```

### IP-Adapter FaceID

**Key adjustments:**
- Describe the style you want, not the face
- weight_type "style transfer" for 3D→realistic
- Standard CFG for base model

```
photorealistic portrait, DSLR photo quality, natural skin texture,
warm indoor lighting, bokeh background, professional photography
```

### FLUX Kontext (Editing)

**Key adjustments:**
- Describe the EDIT, not the full image
- Be specific about what to change
- Mention what to preserve

```
Change the outfit to a formal black evening dress while keeping the face,
hair, and pose exactly the same. Add subtle jewelry.
```

### With Character LoRA

**Key adjustments:**
- ALWAYS include trigger word first
- Don't describe features the LoRA has learned
- Focus on what varies: pose, clothing, setting, lighting

```
sage_character, standing on a rooftop at sunset, wind blowing hair,
wearing casual summer dress, city skyline behind, golden hour lighting,
cinematic composition
```

## Negative Prompt Templates

### Universal Negative (SDXL/SD1.5)
```
(worst quality:1.4), (low quality:1.4), blurry, deformed, bad anatomy,
bad hands, extra fingers, missing fingers, extra limbs, fused fingers,
text, watermark, signature, jpeg artifacts, username, error
```

### Photorealism Negative
```
3d render, cartoon, anime, illustration, painting, drawing, cgi,
plastic skin, smooth skin, airbrushed, video game, doll, mannequin,
oversaturated, artificial lighting
```

### Video Negative (Wan/AnimateDiff)
```
static, frozen, jerky motion, low quality, blurry, distorted face,
bad anatomy, glitch, artifacts, flickering, jittery, unnatural movement
```

### FLUX Negative (keep minimal)
```
blurry, low quality, distorted, deformed, ugly, watermark, text
```

## Prompt Construction Workflow

1. **Get character profile** from `projects/{project}/characters/{name}/profile.yaml`
2. **Get target model** from inventory/user preference
3. **Apply model rules** from above
4. **Add identity method modifiers** if applicable
5. **Include trigger word** if LoRA is being used
6. **Draft positive + negative** pair
7. **Review against past successes** in character's `generation_history`
8. **Adjust CFG** recommendation based on method stack

## Reference

- `references/prompt-templates.md` - Full template library with examples
- `references/workflows.md` - CFG and sampler settings per workflow
- Character profiles in `projects/` for trigger words and feature descriptions
