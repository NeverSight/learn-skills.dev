---
name: image-generation
description: Generate high-quality images via MCP (Gemini models or compatible services) using structured prompts, ratios, and validation for marketing, UI, or presentations.
metadata:
  tags: image-generation, gemini, mcp, design, creative, ai-art
  platforms: Claude, ChatGPT, Gemini, Codex
---


# Image Generation via MCP

AI image generation skill via MCP. Use Gemini models or compatible services to generate high-quality images for marketing, UI, and presentations.

## When to use this skill

- **Marketing assets**: Hero images, banners, social media content
- **UI/UX design**: Placeholder images, icons, illustrations
- **Presentations**: Slide backgrounds, product visualizations
- **Brand consistency**: Generate images based on a style guide

---

## Instructions

### Step 1: Configure MCP Environment

```bash
# Check MCP server configuration
claude mcp list

# Check Gemini CLI availability
# gemini-cli must be installed
```

**Required setup**:
- Model name (gemini-2.5-flash, gemini-3-pro, etc.)
- API key reference (stored as an environment variable)
- Output directory

### Step 2: Define the Prompt

Write a structured prompt:

```markdown
**Subject**: [main subject]
**Style**: [style - minimal, illustration, photoreal, 3D, etc.]
**Lighting**: [lighting - natural, studio, golden hour, etc.]
**Mood**: [mood - calm, dynamic, professional, etc.]
**Composition**: [composition - centered, rule of thirds, etc.]
**Aspect Ratio**: [ratio - 16:9, 1:1, 9:16]
**Brand Colors**: [brand color constraints]
```

### Step 3: Choose the Model

| Model | Use case | Notes |
|-----|------|------|
| `gemini-3-pro-image` | High quality | Complex compositions, detail |
| `gemini-2.5-flash-image` | Fast iteration | Prototyping, testing |
| `gemini-2.5-pro-image` | Balanced | Quality/speed balance |

### Step 4: Generate and Review

```bash
# Generate 2-4 variants
ask-gemini "Create a serene mountain landscape at sunset,
  wide 16:9, minimal style, soft gradients in brand blue #2563EB"

# Iterate by changing a single variable
ask-gemini "Same prompt but with warm orange tones"
```

**Review checklist**:
- [ ] Brand fit
- [ ] Composition clarity
- [ ] Ratio correctness
- [ ] Text readability (if text is included)

### Step 5: Deliverables

Final deliverables:
- Final image files
- Prompt metadata record
- Model, ratio, usage notes

```json
{
  "prompt": "serene mountain landscape at sunset...",
  "model": "gemini-3-pro-image",
  "aspect_ratio": "16:9",
  "style": "minimal",
  "brand_colors": ["#2563EB"],
  "output_file": "hero-image-v1.png",
  "timestamp": "2026-01-21T10:30:00Z"
}
```

---

## Examples

### Example 1: Hero Image

**Prompt**:
```
Create a serene mountain landscape at sunset,
wide 16:9, minimal style, soft gradients in brand blue #2563EB.
Focus on clean lines and modern aesthetic.
```

**Expected output**:
- 16:9 hero image
- Prompt parameters saved
- 2-3 variants for selection

### Example 2: Product Thumbnail

**Prompt**:
```
Generate a 1:1 thumbnail of a futuristic dashboard UI
with clean interface, soft lighting, and professional feel.
Include subtle glow effects and dark theme.
```

**Expected output**:
- 1:1 square image
- Low visual noise
- App store ready

### Example 3: Social Media Banner

**Prompt**:
```
Create a LinkedIn banner (1584x396) for a SaaS startup.
Modern gradient background with abstract geometric shapes.
Colors: #6366F1 to #8B5CF6.
Leave space for text overlay on the left side.
```

**Expected output**:
- LinkedIn-optimized dimensions
- Safe zone for text
- Brand-aligned colors

---

## Best practices

1. **Specify ratio early**: Prevent unintended crops
2. **Use style anchors**: Maintain consistent aesthetics
3. **Iterate with constraints**: Change only one variable at a time
4. **Track prompts**: Ensure reproducibility
5. **Batch similar requests**: Create a consistent style set

---

## Common pitfalls

- **Vague prompts**: Specify concrete style and composition
- **Ignoring size constraints**: Check target channel dimension requirements
- **Overly complex scenes**: Simplify for clarity

---

## Troubleshooting

### Issue: Outputs are inconsistent
**Cause**: Missing stable style constraints
**Solution**: Add style references and a fixed palette

### Issue: Wrong aspect ratio
**Cause**: Ratio not specified or an unsupported ratio
**Solution**: Provide an exact ratio and regenerate

### Issue: Brand mismatch
**Cause**: Color codes not specified
**Solution**: Specify brand colors via HEX codes

---

## Output format

```markdown
## Image Generation Report

### Request
- **Prompt**: [full prompt]
- **Model**: [model used]
- **Ratio**: [aspect ratio]

### Output Files
1. `filename-v1.png` - [description]
2. `filename-v2.png` - [variant description]

### Metadata
- Generated: [timestamp]
- Iterations: [count]
- Selected: [final choice]

### Usage Notes
[Any notes for implementation]
```

---

## Multi-Agent Workflow

### Validation & Retrospectives

- **Round 1 (Orchestrator)**: Prompt completeness, ratio correctness
- **Round 2 (Analyst)**: Style consistency, brand alignment
- **Round 3 (Executor)**: Validate output filenames, delivery checklist

### Agent Roles

| Agent | Role |
|-------|------|
| Claude | Prompt structuring, quality verification |
| Gemini | Run image generation |
| Codex | File management, batch processing |

---

## Metadata

### Version
- **Current Version**: 1.0.0
- **Last Updated**: 2026-01-21
- **Compatible Platforms**: Claude, ChatGPT, Gemini, Codex

### Related Skills
- [frontend-design](../../frontend/design-system/SKILL.md)
- [presentation-builder](../../documentation/presentation-builder/SKILL.md)
- [video-production](../video-production/SKILL.md)

### Tags
`#image-generation` `#gemini` `#mcp` `#design` `#creative` `#ai-art`
