---
name: picture
description: Generate images using Google Imagen. Use when user needs 'hero image', 'presentation visual', 'conceptual illustration', or 'generate an image'. Composes with itv-styling for brand-constrained outputs. (user)
allowed-tools:
  - Bash
  - Read
---

# Image Generation

Generate AI images using Google Imagen via the Gemini API.

## When to Use

- Presentation images (hero visuals, section dividers)
- Conceptual illustrations (visual metaphors, abstract concepts)
- Photo-realistic images (product mockups, scenarios)
- Visual explanations that benefit from AI generation

## When NOT to Use

- **Precise diagrams or charts** — use `diagramming` skill (editable SVG, exact data)
- **Screenshots** — use `screenshot` skill
- **Simple icons** — often faster to find stock or use emoji

**Overlap with diagramming:** There's fuzzy boundary. A "chart for a presentation" could go either way:
- Need precise data, editability → diagramming
- Need striking visual punch → image-generation
- Use judgement; ask if unclear.

## Workflow

### 1. Understand the Need

Clarify with user:
- **Purpose** — presentation, concept illustration, visual metaphor?
- **Style** — photorealistic, illustration, abstract?
- **Brand** — does it need ITV styling? (if so, read itv-styling skill)

### 2. Draft with Flash

Use the fast model for initial iterations:
```bash
~/.claude/skills/picture/imagen.sh "prompt" --model gemini-2.5-flash-image
```

### 3. Review and Refine

Open the image, assess, iterate:
```bash
# Edit mode: refine previous output
~/.claude/skills/picture/imagen.sh "make it warmer, add more contrast" --input ./images/previous.png
```

### 4. Final Render with Pro

For client-facing or final deliverables:
```bash
~/.claude/skills/picture/imagen.sh "prompt" --model gemini-3-pro-image-preview
```

## Command Reference

```bash
# Basic generation
imagen.sh "prompt" [--output ./images] [--model MODEL]

# Edit existing image
imagen.sh "refinement prompt" --input previous.png

# Models
--model gemini-2.5-flash-image     # Fast, cheap (default)
--model gemini-3-pro-image-preview # Higher quality
--model imagen-4.0-generate-preview-06-06  # Imagen 4
```

Output: Saves to `./images/` with timestamped filename, prints path.

## Prompting Framework

Based on Max Woolf's Nano Banana research.

### Structure

```
[Specific object description with exact requirements in CAPS]

Aspects that MUST be followed EXACTLY:
- [Compositional rule 1]
- [Compositional rule 2]

[Publication/camera details for style elevation]

Do not include [unwanted elements].
```

### Key Techniques

| Technique | Example |
|-----------|---------|
| Structured bullets | Requirements as dashed list, not prose |
| ALL CAPS constraints | "MUST", "EXACTLY" increases adherence |
| Hex colors | `#9F2B68` more precise than "magenta" |
| Composition rules | "rule of thirds", "negative space", "depth of field" |
| Style elevators | "Pulitzer Prize-winning cover photo for NYT" |
| Camera specs | "Canon EOS 90D DSLR camera" |
| Publication targets | "Vanity Fair cover profile" |
| Negative constraints | "Do not include text, watermarks, or line overlays" |

### Example Prompt

```
A professional headshot of a confident business executive.

Aspects that MUST be followed EXACTLY:
- Shot from shoulders up, rule of thirds composition
- Neutral background with soft gradient #E8E8E8 to #FFFFFF
- Natural 3PM diffuse lighting from left
- Sharp focus on eyes, slight bokeh on background

Pulitzer Prize-winning portrait, Canon EOS R5, 85mm f/1.4.

Do not include any text, logos, or watermarks.
```

## Composing with Brand Skills

### With itv-styling

When creating ITV-branded images:

1. Read `itv-styling` for color palette and principles
2. Bake brand constraints into prompt:

```
Corporate presentation image for ITV.

Aspects that MUST be followed EXACTLY:
- Dark background #0F2323 (ITV dark green)
- Accent elements in #E8E557 (ITV yellow) or #4ECDC4 (ITV teal)
- Clean, modern, professional aesthetic
- No busy patterns or off-brand colors

Professional corporate photography style.
```

### With diagramming

For hybrid needs (visual + precise data):
- Generate AI background/illustration with image-generation
- Overlay precise elements with diagramming
- Composite manually if needed

## Limitations

| Limitation | Workaround |
|------------|------------|
| Style transfer fails ("Studio Ghibli style") | Use structural descriptions instead |
| Text generation imperfect | Add text as overlay after generation |
| Exact positioning difficult | Iterate with refinement prompts |
| Rate limits | Use Flash for drafts, Pro only for finals |

## Output Location

Images save to `./images/` in the project directory:
- Created on first use
- Timestamped filenames for uniqueness
- Stays with project for easy reference

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Skip brand check | Inconsistent styling | Load itv-styling first when brand applies |
| Vague prompts | Poor results | Use specific, concrete descriptions |
| Wrong tool for data | Inaccurate charts | Use diagram skill for precise data |

## See Also

- `references/prompting.md` — Extended prompting reference
- `diagramming` skill — For precise diagrams and charts
- `itv-styling` skill — For brand-constrained outputs
