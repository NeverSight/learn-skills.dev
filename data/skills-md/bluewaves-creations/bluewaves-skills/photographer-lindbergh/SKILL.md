---
name: photographer-lindbergh
description: Generate images in Peter Lindbergh's iconic black and white style. Use when users ask for Lindbergh style, raw authentic beauty, emotional B&W portraits, supermodel aesthetic, or unretouched natural photography.
allowed-tools: Bash, Read, Write
license: MIT
compatibility: Requires credentials.json or FAL_KEY environment variable (fal.ai API key). Claude.ai users provide credentials via credentials.json.
---

# Peter Lindbergh Style Photography

Generate images in the iconic style of Peter Lindbergh - raw, authentic black and white photography that celebrates natural beauty and emotional depth.

See `references/fal-api.md` for setup, Python patterns, and error handling.

## Style Characteristics

Peter Lindbergh revolutionized fashion photography by:
- **Raw authentic beauty** - minimal retouching, natural imperfections celebrated
- **High-contrast black and white** - deep blacks, rich mid-tones, heavy film grain
- **Natural/subtractive lighting** - soft, directional light that sculpts faces
- **Emotional depth** - focus on personality and inner character over glamour
- **Timeless elegance** - avoids trends, captures enduring beauty

## API Endpoint

`fal-ai/gemini-3-pro-image-preview`

## Prompt Construction

### Core Style Elements

Always include these elements for authentic Lindbergh style:

```
in the style of Peter Lindbergh, black and white photography,
natural light, minimal makeup, raw authentic beauty, high contrast,
film grain texture, intimate portrait, emotional depth, unretouched skin
```

### Mood Keywords

| Category | Keywords |
|----------|----------|
| Emotion | `introspective`, `soulful`, `intimate`, `vulnerable` |
| Aesthetic | `raw`, `unretouched`, `authentic`, `natural` |
| Technical | `high contrast`, `film grain`, `black and white` |
| Style | `cinematic`, `timeless`, `verite`, `documentary` |

## CLI Script

```bash
python3 scripts/fal_generate.py \
    --endpoint image \
    --prompt "woman with freckles, in the style of Peter Lindbergh, black and white, natural light, raw authentic beauty, high contrast, film grain, intimate portrait" \
    --aspect-ratio 3:4 \
    --output lindbergh-portrait.png
```

## Examples

### 1. Classic Supermodel Portrait
```
woman with strong bone structure, direct gaze at camera,
in the style of Peter Lindbergh, black and white photography,
natural daylight, minimal makeup, raw authentic beauty,
high contrast with rich shadows, film grain texture,
intimate close-up portrait, soulful and introspective
```

### 2. Emotional Editorial
```
model in simple white shirt, wind in hair, beach setting,
in the style of Peter Lindbergh, black and white photography,
overcast natural light, unretouched skin texture,
documentary fashion photography, emotional vulnerability,
cinematic composition, timeless elegance
```

### 3. Group Dynamic
```
three models in casual poses, genuine interaction,
in the style of Peter Lindbergh, black and white photography,
studio with natural light, authentic connection between subjects,
raw beauty without heavy makeup, film grain aesthetic,
candid moment captured, verite fashion photography
```

### 4. Character Study
```
older man with weathered face, life experience in eyes,
in the style of Peter Lindbergh, black and white photography,
window light, every wrinkle celebrated, raw authentic portrait,
high contrast dramatic shadows, soulful depth,
humanistic photography, unretouched character study
```

## Tips for Best Results

1. **Embrace imperfection** - Include terms like "unretouched", "natural skin texture", "authentic"
2. **Specify lighting** - Use "natural light", "window light", "overcast", "subtractive lighting"
3. **Focus on emotion** - Add "soulful", "introspective", "vulnerable", "genuine expression"
4. **Keep it simple** - Lindbergh's style avoids elaborate styling; use "minimal makeup", "simple clothing"
5. **Add grain** - Always include "film grain texture" or "analog film aesthetic"
6. **Use portrait ratios** - 2:3, 3:4, or 4:5 work best for the classic Lindbergh look
7. **Web search grounding** - `enable_web_search: True` lets Gemini look up Lindbergh's actual style for authentic results

## Reference

Peter Lindbergh (1944-2019) was a German fashion photographer known for launching the supermodel era with his 1990 British Vogue cover featuring Naomi Campbell, Linda Evangelista, Tatjana Patitz, Christy Turlington, and Cindy Crawford. His work emphasized natural beauty and rejected heavy retouching.

**Key Influences**: Henri Cartier-Bresson, German Expressionist cinema
**Signature**: Black and white, natural light, emotional authenticity
