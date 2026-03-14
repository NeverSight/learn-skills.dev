---
name: photographer-vonunwerth
description: Generate images in Ellen von Unwerth's playful vintage style. Use when users ask for von Unwerth style, playful sensuality, vintage film noir, whimsical feminine photography, retro glamour, narrative storytelling.
allowed-tools: Bash, Read, Write
license: MIT
compatibility: Requires credentials.json or FAL_KEY environment variable (fal.ai API key). Claude.ai users provide credentials via credentials.json.
---

# Ellen von Unwerth Style Photography

Generate images in the iconic style of Ellen von Unwerth - playful, vintage-inspired photography celebrating feminine empowerment and whimsical sensuality.

See `references/fal-api.md` for setup, Python patterns, and error handling.

## Style Characteristics

Ellen von Unwerth's photography is defined by:
- **Playful sensuality** - whimsical, flirtatious energy
- **Vintage cinematic** - film noir influences, classic Hollywood glamour
- **Narrative storytelling** - each image tells a story with characters
- **Empowered femininity** - women as subjects, not objects
- **High-energy dynamism** - movement, spontaneity, joy

## API Endpoint

`fal-ai/gemini-3-pro-image-preview`

## Prompt Construction

### Core Style Elements

Always include these elements for authentic von Unwerth style:

```
in the style of Ellen von Unwerth, playful fashion photography,
vintage cinematic aesthetic, film noir lighting, narrative scene,
whimsical and flirtatious mood, feminine empowerment,
retro glamour, storytelling composition, dramatic light and shadow
```

### Mood Keywords

| Category | Keywords |
|----------|----------|
| Energy | `playful`, `flirtatious`, `whimsical`, `mischievous`, `joyful` |
| Style | `vintage`, `retro`, `film noir`, `Hollywood`, `cinematic` |
| Femininity | `empowering`, `sensual`, `feminine`, `provocative`, `confident` |
| Narrative | `storytelling`, `character`, `scene`, `dramatic`, `theatrical` |

## CLI Script

```bash
python3 scripts/fal_generate.py \
    --endpoint image \
    --prompt "woman in vintage lingerie looking mischievously over shoulder, in the style of Ellen von Unwerth, playful fashion photography, vintage cinematic aesthetic, film noir lighting, whimsical flirtatious mood, feminine empowerment" \
    --aspect-ratio 2:3 \
    --output vonunwerth-portrait.png
```

## Examples

### 1. Boudoir Playfulness
```
woman in vintage lingerie on rumpled bed sheets,
playful expression, caught mid-laugh,
in the style of Ellen von Unwerth, playful fashion photography,
vintage cinematic aesthetic, soft film noir lighting,
whimsical flirtatious mood, sensual yet fun,
feminine empowerment, retro boudoir glamour,
intimate storytelling moment
```

### 2. Retro Adventure
```
woman on vintage motorcycle, leather jacket,
wind-blown hair, adventurous spirit,
in the style of Ellen von Unwerth, playful fashion photography,
vintage cinematic warm tones, dynamic action,
whimsical rebellious mood, feminine power,
retro 1960s glamour, road trip narrative,
empowering energy, mischievous smile
```

### 3. Hollywood Noir
```
woman in satin dress at vanity mirror, applying lipstick,
dramatic shadows, mysterious mood,
in the style of Ellen von Unwerth, playful fashion photography,
vintage film noir black and white, dramatic lighting,
whimsical old Hollywood aesthetic, femme fatale character,
retro 1940s glamour, cinematic storytelling,
sensual and powerful
```

### 4. Best Friends Narrative
```
two women in cocktail dresses, champagne glasses,
whispering and giggling, party scene,
in the style of Ellen von Unwerth, playful fashion photography,
vintage cinematic aesthetic, warm ambient lighting,
whimsical friendship narrative, joyful energy,
retro glamour, feminine celebration,
storytelling composition, flirtatious mood
```

### 5. Pin-Up Revival
```
woman in vintage swimsuit, beach cabana,
playful pin-up pose, confident smile,
in the style of Ellen von Unwerth, playful fashion photography,
vintage 1950s color aesthetic, sunny lighting,
whimsical summer mood, empowered femininity,
retro beach glamour, playful narrative,
flirtatious energy, mischievous charm
```

## Tips for Best Results

1. **Keep it playful** - Use "whimsical", "flirtatious", "mischievous", "joyful"
2. **Add narrative** - Describe a scene or story, not just a pose
3. **Vintage references** - Include "film noir", "1950s", "Hollywood", "retro"
4. **Feminine energy** - Use "empowered", "confident", "sensual", "playful"
5. **Lighting drama** - Specify "film noir lighting", "dramatic shadows", "vintage aesthetic"
6. **Movement and life** - Add "dynamic", "caught moment", "spontaneous", "wind-blown"
7. **Web search grounding** - `enable_web_search: True` lets Gemini look up von Unwerth's actual style for authentic results

## Reference

Ellen von Unwerth (born 1954) is a German photographer and director known for her playful, feminine images that empower women through sensuality and storytelling. A former model herself, she brings an insider's perspective to fashion photography.

**Key Influences**: Classic Hollywood, Film Noir, 1950s pin-up
**Signature**: Playful sensuality, vintage aesthetics, narrative storytelling, feminine empowerment
