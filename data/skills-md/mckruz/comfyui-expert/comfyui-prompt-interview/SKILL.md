---
name: comfyui-prompt-interview
description: Conducts a guided conversational interview with the user about the image or scene they want to create, asking pertinent questions to fully understand their vision, then synthesizes a perfect model-appropriate prompt with recommended settings. Use when the user says "I want to create...", "help me make an image of...", "I have an idea for...", or asks for help crafting a prompt.
user-invocable: true
metadata: {"openclaw":{"emoji":"🎬","os":["darwin","linux","win32"]}}
---

# ComfyUI Prompt Interview

Conduct a guided conversation to draw out the user's complete creative vision, then synthesize a perfect, model-appropriate prompt with all recommended settings.

## When to Invoke This Skill

- User describes an image or scene idea but hasn't given enough detail for a quality prompt
- User says "help me think through what I want to create"
- User has a vague concept that needs refinement
- User wants a structured prompt but isn't sure what to specify

## The Interview Philosophy

**Ask, don't interrogate.** This is a conversation, not a form. Ask one or two questions at a time. Listen to what the user gives you and follow up on what's missing. Tailor your questions to what they've already shared — don't ask about character details if they're generating a landscape.

**Fewer questions = better.** Aim for 4-7 exchanges maximum. Ask the most impactful questions first. Stop asking when you have enough to generate an excellent prompt.

**Don't ask for what you can infer.** If the user says "cinematic portrait of a warrior woman," you don't need to ask if it's a person or whether to include a subject.

---

## Interview Flow

### Step 1: Open with the Big Picture

If the user hasn't told you what they want to create, start here:

> "What do you want to create? Give me whatever you have — even a rough idea, a mood, or a reference you're inspired by."

If they gave you a starting concept, skip this and go straight to what's missing.

---

### Step 2: Branch by Creation Type

Based on their answer, determine what kind of generation this is:

| Type | Key Questions to Ask |
|------|---------------------|
| **Portrait / Character** | Identity method? Existing character? Expression, clothing, setting, lighting |
| **Scene / Environment** | Location, time of day, mood, weather, foreground/background elements |
| **Product / Object** | Angle, background, lighting style, commercial vs. artistic |
| **Abstract / Concept** | Dominant colors, shapes, emotional tone, what to avoid |
| **Video** | Motion type, camera movement, duration needed, audio? |

---

### Step 3: Ask the High-Impact Questions

Ask only what's missing. Use natural conversational language, not a bullet list.

#### For character/portrait content — ask in order of impact:

1. **Identity** (if not specified): "Is this a specific character you have reference images for, or are we designing someone new?"
2. **Expression & mood**: "What's the emotion or energy — fierce, serene, playful, haunted?"
3. **Setting**: "Where are they, and when? (Time of day, location, interior/exterior)"
4. **Lighting**: "Any specific lighting in mind? (Golden hour, dramatic side light, soft studio, neon, candlelight)"
5. **Clothing & details**: "What are they wearing, and any other key visual details?"
6. **Camera/composition**: "How are we framing this — close-up portrait, three-quarter body, wide establishing shot?"
7. **Style**: "Photorealistic, cinematic film, editorial fashion, painterly, or something else?"

#### For scene/environment content — ask in order of impact:

1. **Setting**: "Describe the place — what does it look like, and when is it?"
2. **Mood/atmosphere**: "What feeling should hit the viewer instantly?"
3. **Lighting**: "What's the light source and quality?"
4. **Key elements**: "Any specific objects, structures, or details that must be in the shot?"
5. **Style**: "Photorealistic, stylized, concept art, painterly?"

#### For video content — additional questions:

1. **Motion**: "What's moving — the subject, the camera, or both?"
2. **Duration**: "How long? (Short: 3-5s vs. long: 15-60s changes model choice)"
3. **Audio**: "Do you need sound/music, or silent?"

---

### Step 4: Technical Questions (ask only if not obvious)

These can usually be inferred from context, but ask if unclear:

- **Aspect ratio**: "Standard 1:1 portrait, 16:9 cinematic, 9:16 vertical/social?"
- **Model preference**: "Any preference on the generation engine, or should I recommend the best one for this?"
- **Existing character setup**: "Do you have a LoRA trained for this character, or reference images?"
- **What to avoid**: "Anything specific you want to make sure stays OUT of the image?"

---

### Step 5: Confirm and Synthesize

Before generating the prompt, briefly reflect back the vision:

> "Got it. Here's how I'm reading this: [1-2 sentence summary of the concept]. Let me build that prompt."

Then immediately generate the full output below.

---

## Output Format

Deliver all four components, clearly separated:

---

### 🎯 Positive Prompt

[Craft the positive prompt applying model-specific rules from `skills/comfyui-prompt-engineer/SKILL.md`]

Key rules:
- **FLUX / Kontext**: Natural language, 50-100 words, no quality tags, describe the scene not the face if using identity method
- **SDXL**: Quality tags first, trigger word second, 50-150 words, weighted syntax supported
- **SD 1.5**: Short and tag-based, 30-80 words
- **Wan / Video**: Concise, motion-focused, 20-50 words
- If a LoRA trigger word applies, put it first
- If using InstantID/InfiniteYou: don't describe facial features, let the identity method handle them

---

### 🚫 Negative Prompt

[Select the appropriate negative template and customize it]

Standard templates:
- **Photorealism**: `(worst quality:1.4), (low quality:1.4), blurry, deformed, bad anatomy, bad hands, extra fingers, missing fingers, text, watermark, 3d render, cartoon, anime, plastic skin, airbrushed, oversaturated`
- **FLUX (minimal)**: `blurry, low quality, distorted, deformed, ugly, watermark, text`
- **Video**: `static, frozen, jerky motion, low quality, blurry, distorted face, bad anatomy, glitch, artifacts, flickering`

---

### ⚙️ Recommended Settings

| Parameter | Value | Reason |
|-----------|-------|--------|
| Model | [Specific checkpoint] | [Why this model] |
| Sampler | [e.g., DPM++ 2M Karras] | |
| Steps | [e.g., 25] | |
| CFG Scale | [e.g., 4.5] | |
| Resolution | [e.g., 1016×1016] | [Avoid 1024 watermark artifacts if InstantID] |
| Identity method | [e.g., InfiniteYou SIM] | [If applicable] |
| LoRA | [Trigger word + weight] | [If applicable] |

---

### 🔧 Pipeline Recommendation

[1-3 sentences describing the recommended workflow pattern and why]

Example: "Use Pattern 2 from the character-gen skill: Load your LoRA, add InfiniteYou SIM for identity lock, route through FaceDetailer at 0.35 denoise, then upscale with 4x-UltraSharp. This gives you maximum identity fidelity while keeping the cinematic mood you described."

---

## Decision Rules for Model Selection

Apply these when recommending a model/pipeline:

| User's Goal | Recommend |
|-------------|-----------|
| "Photorealistic, single character, reference images available" | InfiniteYou or FLUX Kontext |
| "Multiple characters, consistent identity" | PuLID Flux II |
| "Fast iteration, character editing" | FLUX Kontext dev/pro |
| "Highest quality portrait, trained LoRA exists" | FLUX.1-dev + LoRA |
| "Wide scene / environment" | FLUX.1-dev or RealVisXL |
| "Stylized / artistic" | RealVisXL + style LoRA or SDXL |
| "Video, short clip" | Wan 2.2 1.3B (consumer) or LTX-2 (4K) |
| "Video, infinite length" | Wan 2.2 I2V A14B + SVI 2.0 Pro |
| "Talking head" | FramePack + LatentSync 1.6 |

---

## Example Interview

**User**: "I want to create a dramatic image of a woman warrior standing in ruins at dawn."

**VideoAgent**:
> "Love the concept. A few things that'll lock in the look:
> 1. Is this a specific character you want to preserve (reference images, LoRA) or someone new?
> 2. What's her energy — defiant and triumphant, exhausted but unbroken, something else?
> 3. Any specifics on how she looks — hair, armor style, anything iconic about her?"

**User**: "New character. Defiant and triumphant. Dark braided hair, ornate bronze armor, early morning light just cresting the horizon behind her."

**VideoAgent**:
> "Got it — framing this as a heroic aftermath shot: she's won, the sun rises behind her, rubble around her feet. One more thing: close portrait, three-quarter body, or full figure with the ruins environment?"

**User**: "Full figure, show the ruins and the dawn sky."

**VideoAgent**:
> "Perfect. Building that now."

[Delivers complete prompt output]

---

## Integration with Other Skills

After delivering the prompt, offer next steps:

- **Generate the workflow**: "Want me to build the full ComfyUI workflow for this? I'll check your inventory and configure every node."
- **Refine the prompt**: "I can adjust the style, swap the identity method, or rework the negative if anything doesn't feel right."
- **Save as character profile**: "If this becomes a recurring character, I can create a character profile so we always have her settings ready."
