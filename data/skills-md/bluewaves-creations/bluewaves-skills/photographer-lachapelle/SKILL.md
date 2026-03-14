---
name: photographer-lachapelle
description: Generate images in David LaChapelle's surreal pop art style. Use when users ask for LaChapelle style, pop surrealism, hyper-saturated colors, theatrical staging, baroque maximalism, kitsch aesthetic.
allowed-tools: Bash, Read, Write
license: MIT
compatibility: Requires credentials.json or FAL_KEY environment variable (fal.ai API key). Claude.ai users provide credentials via credentials.json.
---

# David LaChapelle Style Photography

Generate images in the iconic style of David LaChapelle - surreal, hyper-saturated pop art photography with theatrical staging and cultural commentary.

See `references/fal-api.md` for setup, Python patterns, and error handling.

## Style Characteristics

David LaChapelle's photography is defined by:
- **Kitsch pop surrealism** - hyper-real dreamlike compositions
- **Fluorescent saturated colors** - electric, overwhelming color palettes
- **Elaborate theatrical staging** - baroque abundance of elements
- **Cultural commentary** - themes of consumerism, fame, divine vs profane
- **Over-the-top maximalism** - visually opulent excess

## API Endpoint

`fal-ai/gemini-3-pro-image-preview`

## Prompt Construction

### Core Style Elements

Always include these elements for authentic LaChapelle style:

```
in the style of David LaChapelle, pop surrealism,
hyper-saturated fluorescent colors, elaborate theatrical set design,
baroque maximalism, surreal dreamlike composition,
kitsch aesthetic, provocative staging, fantasy scenario
```

### Mood Keywords

| Category | Keywords |
|----------|----------|
| Surreal | `dreamlike`, `fantastical`, `hyper-real`, `bizarre`, `otherworldly` |
| Color | `fluorescent`, `neon`, `hyper-saturated`, `electric`, `rainbow` |
| Style | `baroque`, `maximalist`, `kitsch`, `pop art`, `theatrical` |
| Theme | `provocative`, `satirical`, `religious`, `consumerist`, `celebrity` |

## CLI Script

```bash
python3 scripts/fal_generate.py \
    --endpoint image \
    --prompt "woman as modern Madonna surrounded by fast food and luxury items, in the style of David LaChapelle, pop surrealism, hyper-saturated fluorescent colors, baroque maximalism, kitsch aesthetic" \
    --aspect-ratio 3:4 \
    --output lachapelle-scene.png
```

## Examples

### 1. Pop Culture Satire
```
celebrity figure drowning in brand logos and dollar bills,
in the style of David LaChapelle, pop surrealism,
hyper-saturated neon colors, elaborate theatrical staging,
baroque excess of consumer goods, surreal composition,
kitsch aesthetic, satirical commentary on fame and money,
fluorescent pink and gold palette
```

### 2. Religious Pop Art
```
modern day saint figure with angel wings and halo,
surrounded by fast food and smartphones,
in the style of David LaChapelle, pop surrealism,
hyper-saturated fluorescent colors, baroque religious staging,
surreal dreamlike divine imagery, kitsch aesthetic,
provocative sacred meets profane, elaborate theatrical set
```

### 3. Underwater Fantasy
```
models in elaborate costumes floating underwater,
surrounded by tropical fish and treasure,
in the style of David LaChapelle, pop surrealism,
hyper-saturated aquamarine and coral colors,
elaborate theatrical underwater staging,
surreal dreamlike mermaid fantasy, baroque abundance,
kitsch aesthetic, fantastical scenario
```

### 4. Apocalyptic Beauty
```
fashion model amid burning paradise,
flowers and flames, beauty and destruction,
in the style of David LaChapelle, pop surrealism,
hyper-saturated fiery oranges and lush greens,
elaborate theatrical apocalyptic staging,
surreal dreamlike garden of eden burning,
baroque maximalism, provocative environmental commentary
```

### 5. Celebrity Excess
```
figure reclining on mountain of luxury goods,
designer bags, jewelry, champagne bottles,
in the style of David LaChapelle, pop surrealism,
hyper-saturated gold and pink fluorescent colors,
elaborate theatrical staging of opulence,
surreal dreamlike excess, baroque maximalism,
kitsch satirical take on wealth and celebrity
```

## Tips for Best Results

1. **Maximize color** - Use "fluorescent", "neon", "hyper-saturated", "electric colors"
2. **Go theatrical** - Add "elaborate staging", "baroque set design", "maximalist"
3. **Embrace surrealism** - Include "dreamlike", "fantastical", "bizarre", "otherworldly"
4. **Layer elements** - LaChapelle compositions are busy; describe multiple elements
5. **Add commentary** - Reference themes like "consumer culture", "celebrity worship", "sacred vs profane"
6. **Think kitsch** - Use "pop art", "kitsch aesthetic", "over-the-top"
7. **Web search grounding** - `enable_web_search: True` lets Gemini look up LaChapelle's actual style for authentic results

## Reference

David LaChapelle (born 1963) is an American photographer and director known for his surreal, hyper-saturated images blending pop culture, religious iconography, and social commentary. His work has appeared in magazines including Interview, Rolling Stone, and Vogue.

**Key Influences**: Pop Art, Baroque painting, religious iconography
**Signature**: Fluorescent colors, theatrical staging, cultural satire
