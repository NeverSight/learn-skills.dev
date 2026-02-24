---
name: text-to-image-prompt-optimizer
description: >
  Generate and optimize AI image generation prompts with primary support for Google Gemini (Nano Banana),
  plus Midjourney, Stable Diffusion, DALL-E, Leonardo.ai, and other text-to-image tools.
  Use when users request: (1) Generate a prompt/提示词 for an image, (2) Optimize or improve an existing prompt,
  (3) Create variations of a prompt, (4) Translate ideas into detailed prompts, (5) Ask for help with AI image generation,
  or (6) Mention keywords like 'prompt', '提示词', 'Gemini', 'Nano Banana', 'Midjourney', 'Stable Diffusion',
  'AI绘图', '文生图', 'text-to-image', or '/imagine'.
---

# AI Image Prompt Optimizer

Generate professional, optimized prompts for AI image generation tools with **primary support for Google Gemini (Nano Banana)**, plus Midjourney, Stable Diffusion, DALL-E, Leonardo.ai, and others.

## Core Workflow

When a user requests prompt generation or optimization:

1. **Understand the intent**
   - Identify the core subject and desired outcome
   - Ask clarifying questions ONLY if the request is extremely vague
   - Default to reasonable assumptions rather than over-questioning

2. **Generate comprehensive prompts**
   - **Primary format: Google Gemini (Nano Banana)** - Use conversational, natural language with photographic/cinematic terminology
   - Provide multiple variations (2-3) with different styles or approaches
   - Include both English (primary) and Chinese translations
   - For Gemini: Use clear, descriptive sentences rather than keyword lists
   - For other platforms: Structure using formula `[Subject] + [Environment] + [Style] + [Lighting] + [Composition] + [Quality]`

3. **Include platform-specific optimizations**
   - **Gemini (Nano Banana) - PRIMARY**: Clear conversational prompts with photographic/cinematic language, semantic positive descriptions
   - Midjourney (secondary): Add `--ar`, `--s`, `--q`, etc. as appropriate
   - Stable Diffusion (secondary): Suggest sampling steps, CFG scale, and negative prompts
   - Adapt to user's specified platform, but default to Gemini when not specified

4. **Explain and educate**
   - Break down each component of the prompt
   - Explain why specific keywords were chosen
   - Suggest modifications for different effects

5. **Provide actionable next steps**
   - Guide users on how to use the prompt
   - Suggest parameter tweaks for refinement
   - Offer to iterate based on results

## Output Format

Structure responses as follows (prioritize Gemini format):

```
## 🎨 Generated Prompts

### ⭐ Variation 1: Google Gemini (Nano Banana) - RECOMMENDED
**English (Conversational):**
[Natural language prompt with clear, descriptive sentences using photographic/cinematic terminology]

**中文版本:**
[Chinese translation in conversational style]

**适用平台:** Google Gemini (Nano Banana / Nano Banana Pro)
**推荐模型:** [Nano Banana for testing / Nano Banana Pro for professional output]

---

### Variation 2: [Alternative Style/Platform]
**English:**
[Platform-specific format - keywords for Midjourney, structured for SD, etc.]

**中文版本:**
[Chinese translation]

**适用平台:** [Midjourney / Stable Diffusion / DALL-E / Leonardo.ai]

---

### Variation 3: [Another Alternative]
[Optional third variation if helpful]

---

## 📝 Prompt Breakdown

- **Subject:** [Explanation]
- **Composition:** [How elements are arranged - important for Gemini]
- **Lighting:** [Photography/cinematography terms used]
- **Style:** [Visual aesthetic description]
- **Technical:** [Camera terms, angles, etc. for Gemini]

## ⚙️ Platform Guide

**🌟 Gemini (Primary):**
- Model choice: [When to use Nano Banana vs Pro]
- Editing tips: [How to iterate conversationally]
- Special features: [Character consistency, multi-image, etc.]

**Other Platforms (Secondary):**
[Brief notes on Midjourney/SD/etc. parameters if relevant]

## 💡 Optimization Tips

[Gemini-focused suggestions first, then others]

## 🎯 Next Steps

**For Gemini:**
1. [How to use in Gemini app/AI Studio]
2. [How to iterate with conversational edits]
3. [How to leverage character consistency / multi-image features]

**For Other Platforms:**
[Platform-specific usage notes if requested]
```

## Key Principles

### Conciseness
- Generate prompts directly without excessive preamble
- Avoid phrases like "I'll help you create a prompt for..."
- Jump straight to the prompts unless clarification is absolutely needed

### Quality Over Verbosity
- Use specific, impactful keywords rather than generic descriptions
- Prefer "cinematic lighting, dramatic shadows, golden hour" over "nice lighting"
- Reference established artistic styles when appropriate

### Platform Awareness
- **Default to Google Gemini (Nano Banana) format if platform is unspecified** - conversational, natural language style
- Always provide Gemini version first as the primary recommendation
- Include alternative platform formats (Midjourney, SD, etc.) as secondary variations
- Automatically include appropriate parameters for each target platform
- Highlight Gemini's unique features (character consistency, conversational editing) when relevant

### Educational Value
- Explain WHY certain keywords work
- Help users learn to craft their own prompts over time
- Reference the prompt library for deeper learning

## Common Patterns

### For Beginners
- Use simpler, more direct prompts
- Explain each component thoroughly
- Provide templates they can modify

### For Experienced Users
- Focus on advanced techniques (weights, negative prompts, multi-concept fusion)
- Suggest artist references and style mixing
- Provide minimal explanation unless requested

## Reference Materials

For comprehensive prompt templates and keyword libraries, refer to:
- **[references/prompt-library.md](references/prompt-library.md)** - Complete template library organized by category
- **[references/keywords-reference.md](references/keywords-reference.md)** - Quick keyword lookup by type
- **[references/platform-specific.md](references/platform-specific.md)** - Platform-specific parameters and techniques

Load these references when:
- User requests specific categories (portraits, landscapes, etc.)
- User asks for keyword suggestions
- User needs platform-specific guidance
- Complex or specialized prompts are needed

## Advanced Techniques

### 🌟 Gemini (Nano Banana) Techniques - PRIMARY

#### Character Consistency
```
First prompt: "Generate a character: [detailed description]"
Follow-up: "Show the same character [in new scenario/pose/style]"
# Gemini will maintain character likeness across images
```

#### Conversational Editing
```
Initial: "Create [image description]"
Edits:
- "Make the background darker"
- "Add [element] to the scene"
- "Change [attribute] to [new value]"
# Each edit builds on the previous image
```

#### Photographic Control
```
Use technical terms:
- "85mm portrait lens at f/1.8" (lens + aperture)
- "wide-angle shot from low angle" (lens + perspective)
- "shallow depth of field with bokeh" (focus effect)
- "golden hour lighting from left" (lighting direction)
```

#### Semantic Positive Descriptions
```
Instead of: "no cars, no people"
Use: "an empty, peaceful street with no signs of activity"

Instead of: "not blurry"
Use: "sharp focus, crystal clear, professional quality"
```

---

### Other Platform Techniques (Secondary)

#### Weight Control (Midjourney)
```
(red flower)::2 (blue flower)::1
# Red flower weighted 2x more than blue
```

#### Negative Prompts (Stable Diffusion)
```
Negative prompt: ugly, blurry, low quality, distorted,
bad anatomy, watermark, text
```

#### Style Mixing (Multiple Platforms)
```
in the style of [Artist A] combined with [Artist B]
```

#### Multi-Concept Fusion (Multiple Platforms)
```
a fusion of [concept 1] and [concept 2]
```

## Quick Templates

### 🌟 Gemini (Nano Banana) Templates - PRIMARY

#### Conversational Formula (Recommended)
```
Create/Generate [subject description] [action/state].
The scene should show [environment details] with [composition description].
Use [lighting description] to create [mood/atmosphere].
The style should be [visual style] with [quality description].
```

#### Portrait (Gemini)
```
Generate a professional portrait of [age/gender], [appearance details],
wearing [clothing]. The subject should have [expression/mood].
Use [lens/angle] perspective with [lighting description].
The background should be [background details]. The style should be
[photographic/artistic style] with [quality expectations].
```

#### Landscape (Gemini)
```
Create a [location/scene type] during [time/season]. The scene should
feature [key elements] with [weather/atmosphere]. Use [angle/perspective]
to capture [compositional focus]. The lighting should be [lighting type]
creating [mood]. Style: [photographic/artistic approach].
```

#### Product (Gemini)
```
Generate a product photograph of [product] made of [material].
Position it on/against [background/surface] with [arrangement details].
Use [lighting setup] from [direction] creating [shadow/highlight effect].
Shot with [camera/lens details] at [angle]. The aesthetic should be
[style] suitable for [purpose].
```

#### Character Design (Gemini)
```
Create a character: [description of person/creature] with [physical features].
They should be wearing [clothing/armor/accessories] and have [expression/pose].
The setting is [environment]. Use [art style] with [detail level].
```

---

### Other Platform Templates (Secondary)

#### Basic Keyword Formula (Midjourney/SD)
```
[subject], [environment], [style], [lighting], [composition], [quality]
```

#### Portrait (Keyword Style)
```
[age/gender], [appearance], [clothing], [expression], [background],
[style], portrait photography, [quality]
```

#### Landscape (Keyword Style)
```
[location], [time/season], [weather], [color mood],
landscape photography, [angle], [quality]
```

#### Product (Keyword Style)
```
[product], [material], [background], product photography,
[lighting], [angle], commercial, [quality]
```

#### Concept Art (Keyword Style)
```
[subject], [details], [genre] art, [atmosphere],
concept art, highly detailed, trending on ArtStation, [quality]
```

## Common Keywords by Category

**Quality:**
- 4k, 8k, ultra hd, high resolution
- highly detailed, sharp focus
- masterpiece, professional
- photorealistic, hyperrealistic

**Lighting:**
- natural lighting, golden hour, soft lighting
- dramatic lighting, volumetric lighting
- studio lighting, rim lighting

**Composition:**
- close-up, wide angle, bird's eye view
- shallow depth of field, bokeh
- rule of thirds, centered

**Style:**
- cinematic, artistic, minimalist
- cyberpunk, fantasy art, anime style
- photorealistic, oil painting, watercolor

**Mood:**
- peaceful, dramatic, mysterious
- cozy, epic, ethereal
- vibrant, melancholic

## Handling User Requests

### "Generate a prompt for [simple idea]"
Expand the idea with reasonable assumptions, provide 2-3 variations, explain choices.

### "Optimize this prompt: [existing prompt]"
Analyze the existing prompt, identify weaknesses, provide improved version with explanation.

### "I want [specific style]"
Use style-specific keywords and artist references, provide examples.

### "Make it better/more detailed"
Add quality keywords, refine composition, enhance specificity.

### "Create variations"
Generate 3-4 variations with different styles, moods, or compositions.

## Tips for Effective Prompts

1. **Be specific** - "a golden retriever puppy" beats "a dog"
2. **Use artist/style references** - "in the style of Studio Ghibli"
3. **Quality keywords matter** - Always include quality descriptors
4. **Order matters** - Earlier keywords have more influence
5. **Test and iterate** - Encourage users to share results for refinement

## When to Consult References

- **Specific categories**: Read prompt-library.md sections for portraits, landscapes, etc.
- **Keyword suggestions**: Reference keywords-reference.md for comprehensive lists
- **Platform details**: Check platform-specific.md for advanced parameters
- **Complex requests**: Load relevant references to provide thorough guidance
