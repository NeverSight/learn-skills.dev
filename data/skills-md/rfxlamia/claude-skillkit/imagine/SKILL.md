---
name: imagine
description: Prepare detailed, professional prompts for Google Imagen 3/4 image generation. Supports character, environment, and object prompts using natural language with technical photography specifications. Extensible support for multiple art styles via reference files.
---

# Imagine: Imagen Prompt Architect

Generate detailed, professional prompts for Google Imagen 3/4 that leverage its natural language processing strengths and technical parameter understanding.

## Core Prompt Structure

Imagen uses a **Subject-Context-Style framework** powered by T5-XXL language models. Build prompts in three layers:

1. **Subject**: Primary focus (person, object, animal, scenery)
2. **Context**: Environment, placement, background, setting
3. **Style**: Aesthetic approach (photographic, artistic, specific technique)

### Photography Prompts Pattern

Start with explicit photography signals: `"A photo of [detailed subject description], [context/placement], [technical specifications]"`

**Technical specifications include:**
- Lens type: 24-85mm (portraits), 60-105mm macro (products), 10-24mm wide-angle (landscapes)
- Lighting: natural light, studio lighting, golden hour, dramatic lighting
- Quality modifiers: sharp focus, high detail, professional photography, 8K resolution
- Camera/equipment: shot on ARRI Alexa, 35mm film, DSLR

**Example**: `"A photo of an elderly woman with weathered hands holding a steaming cup of tea, soft sunlight highlighting her wrinkles and smile, 35mm lens, warm and intimate mood, natural outdoor setting, sharp focus, professional portrait photography"`

### Artistic/Stylized Prompts Pattern

For non-photographic styles, read the relevant artstyle reference file first, then layer:

**Foundation**: `"[Art style name] aesthetic, [medium/technique], [key visual characteristics]"`

**Character/Subject**: Specific features, proportions, design elements

**Environment**: Scene composition, spatial elements, atmospheric details  

**Atmosphere**: Mood, color palette, lighting approach

**Technical**: Rendering specifics, texture, quality markers

## Using Artstyle References

### Step 1: List Available Artstyles

**Before creating any artistic/stylized prompts, ALWAYS list available artstyle files:**

Use bash to check: `ls /mnt/skills/user/imagine/references/artstyle-*.md`

This returns all available artstyle reference files. Present the list to the user so they can choose, or intelligently select based on their request.

### Step 2: Read the Selected Artstyle Reference

**Once an artstyle is selected (either by user or inferred from request):**

1. Read the complete `references/artstyle-[name].md` file to understand the visual language
2. Apply the layered prompting strategy from the reference
3. Use the technical descriptors provided for style-specific characteristics
4. Follow the style-specific guidelines and vocabulary from the reference

### Artstyle File Naming Convention

All artstyle references follow the pattern: `artstyle-[name].md`

Examples:
- `artstyle-sciencesaru.md` - Science SARU animation style
- `artstyle-corporate-memphis.md` - Corporate Memphis/Alegria style
- `artstyle-crewdson-hyperrealism.md` - Gregory Crewdson cinematic hyperrealism
- `artstyle-iphone-social-media.md` - Modern iPhone social media aesthetic

### When No Artstyle is Specified

If the user doesn't specify an artstyle and their request seems to need one:
1. List available artstyles
2. Ask which style they prefer, or suggest the most appropriate based on context
3. Never assume a default artstyle

For pure photography requests without artistic styling, proceed without reading artstyle references.

## Best Practices from Imagen Architecture

### Natural Language Advantage
- Write detailed descriptive sentences, not keyword lists
- Imagen rewards verbose descriptions over brevity
- Use professional creative brief language
- Default enhancePrompt=true automatically optimizes your prose

### Iterative Refinement
Start simple, layer details progressively:
1. Base: `"A cat"`
2. Add specifics: `"A fluffy Persian cat with bright blue eyes"`
3. Add context: `"...sitting on a velvet cushion in a sunlit room"`
4. Add technical: `"A photo of a fluffy Persian cat with bright blue eyes, sitting on a velvet cushion in a sunlit room, 50mm lens, natural soft lighting, warm colors, professional pet photography"`

### Critical Constraints
- **Text-in-image**: Maximum 25 characters per phrase, 3 phrases total
- **Negative prompts**: Use plain descriptive terms ("wall, frame") not instructive language ("no walls, without frame")
- **Token limit**: 480 tokens for prompt text

### Technical Parameters
**Aspect ratios** (match use case):
- 1:1 - Square social media
- 3:4 - Portrait ads, vertical social
- 4:3 - Traditional photography, TV
- 16:9 - Widescreen landscape, modern displays
- 9:16 - Vertical video, tall subjects

**Safety/person controls**: Adjust personGeneration (allow_adult, allow_all, dont_allow) and safetySetting (block_low_and_above, block_medium_and_above, block_only_high, block_none) as needed

## Practical Use Case Patterns

### Character/Portrait
`"Portrait of [character description with age, features, clothing, emotion], [lens specification 24-85mm], [lighting type], [mood descriptors], [setting], [quality modifiers]"`

**For styled characters**: Read appropriate artstyle reference for character design specifics (proportions, features, design language)

### Environment/Landscape  
`"[Environment type], [weather/time/season], [lens specification 10-24mm wide-angle], [atmospheric conditions], [quality modifiers]"`

**For styled environments**: Read appropriate artstyle reference for environment treatment (composition, color theory, architectural approach)

### Product/Object
`"[Product] on [surface], [lens specification 60-105mm macro], [lighting type], [background type], [material/texture details], [quality modifiers]"`

### Cinematic/Stylized
`"[Animation/art style], [scene description], [color grading approach], [cinematography terms], [atmospheric effects]"`

**For cinematic styles**: Read appropriate artstyle reference for cinematic specifics (camera work, lighting philosophy, emotional coding)

## Workflow for Creating Prompts

1. **Determine type**: Photography, artistic style, or hybrid?
2. **If using art style**: 
   - List available artstyles: `ls /mnt/skills/user/imagine/references/artstyle-*.md`
   - Select appropriate style (by user choice or inference)
   - Read complete `references/artstyle-[name].md` file
3. **Build foundation**: Establish subject clearly and early
4. **Layer context**: Add environment, placement, spatial relationships
5. **Specify style**: Include aesthetic approach with technical vocabulary from reference (if using artstyle)
6. **Add technical specs**: Lens type, lighting, quality modifiers appropriate to subject
7. **Refine iteratively**: Start simple, add detail progressively until satisfied
8. **Validate constraints**: Check text-in-image limits, negative prompt format, token count

## Example Complete Prompts

### Photography Example
`"A photo of a plate of traditional Indonesian nasi goreng with fried egg on top, colorful vegetables visible, served on rustic ceramic plate on wooden table, 100mm macro lens, natural window lighting from side, warm atmosphere, steam rising from rice, glistening sauce, high detail, professional food photography, appetizing composition"`

### Artistic Style Example (Generic Template)
`"[Artstyle name] aesthetic, [medium/technique]. [Character description following style's design principles], [character-specific features from artstyle reference]. [Environment description following style's composition approach], [environmental specifics from artstyle reference]. [Atmospheric qualities from style guide], [color and lighting approach from reference]. [Technical rendering specs from style guide], [texture and quality markers from reference]"`

**Note**: The actual artistic prompt should be built by reading the specific artstyle reference file and applying its guidelines. See individual artstyle-*.md files for complete examples.

### Hybrid Example (Styled character, photographic background)
`"A photo of [character description in chosen art style], standing on actual [real environment], 35mm lens, golden hour natural lighting, real background with stylized character overlay, professional photography with [art style] integration, warm atmospheric lighting, high detail background with stylized character"`

## Tips for Quality Output

- **Be specific with materials and textures**: "glistening sauce," "rough ceramic," "polished wood" guide fine detail
- **Use cinematography vocabulary**: "shot on ARRI Alexa," "Summilux lens," "volumetric lighting" elevate professional quality  
- **Time of day matters**: Golden hour, overcast, midday sun, twilight each create distinct lighting and mood
- **Color grading terms**: "muted cold tones," "warm sepia," "desaturated," "high contrast" specify aesthetic precisely
- **Atmospheric effects**: "misty," "foggy," "heat haze," "rain-soaked" add environmental depth

## Extensibility

This skill is designed to grow with your needs:
- Add new `artstyle-[name].md` files to `references/` for different visual styles
- Follow consistent documentation structure from existing artstyle files
- Always list available artstyles at the start of artistic prompt workflows
- Each artstyle reference should provide:
  - Visual DNA and core characteristics
  - Technical prompting vocabulary
  - Layered prompting strategy
  - Complete example prompts
  - Style-specific guidelines for characters, environments, lighting, composition

## Adding New Artstyles

To add a new artstyle:
1. Create `references/artstyle-[name].md`
2. Document the style's visual characteristics comprehensively
3. Provide AI prompting vocabulary and technical descriptors
4. Include layered prompting strategy and complete examples
5. The skill will automatically detect and list it when checking available artstyles

No code changes needed - the skill dynamically discovers all artstyle-*.md files in the references directory.