---
name: ai-product-photo
description: "Specialized skill for AI product photography. Use when you need professional product shots, hero images, lifestyle photography, or e-commerce visuals. Triggers on: product shot, hero image, e-commerce photo. Outputs production-ready product photography."
---

# AI Product Photo

Generate professional product photography that sells. Not generic AI images — strategic visual assets that highlight product value, create desire, and convert viewers to buyers.

**Use this skill when:** You need product shots for e-commerce, hero banners, marketing campaigns, or catalogs.
**Route here from:** ai-creative-workflow when product imagery is needed.

---

## Why This Skill Exists

**The problem:** Most AI product photos fail because they:
1. Look obviously AI-generated (uncanny details, wrong reflections)
2. Don't follow commercial photography principles
3. Miss what makes products sell (features hidden, benefits unclear)
4. Ignore platform-specific requirements (Amazon vs Instagram vs hero banners)

**The solution:** A systematic approach that:
- Uses proven commercial photography techniques in prompts
- Optimizes for specific platforms and use cases
- Highlights product benefits, not just appearance
- Creates desire through strategic styling and context

---

## Model

**ALWAYS use Nano Banana Pro via Glif.**

| Model | Glif ID | Speed |
|-------|---------|-------|
| **Nano Banana Pro Text 2 Image** | `cmi7ne4p40000kz04yup2nxgh` | ~20sec |

**Do NOT use:** imagen-3, DALL-E, Flux, or direct Replicate API calls unless specifically requested.

**Why Glif:** Faster (~20sec vs ~3min), consistent quality, no async polling.

---

## Style Exploration (Before Execution)

**Critical principle:** Don't lock into one visual approach. Product photography has many valid styles — the right one depends on brand, platform, and competitive landscape.

### Why This Matters for Products

The same product photographed differently can feel:
- Premium luxury vs accessible value
- Innovative tech vs reliable traditional
- Lifestyle aspirational vs utility functional

**One style = hope. Multiple styles = strategic choice.**

### Generate 5 Different Approaches

For any new product photography project:

```
Style 1 - Clean E-commerce:
[Product] on pure white background, professional studio lighting,
sharp commercial photography, Amazon listing optimized,
clean minimal, product hero shot

Style 2 - Lifestyle Context:
[Product] in real-world [setting], natural lighting,
lifestyle product photography, human context,
aspirational but relatable

Style 3 - Dark Premium:
[Product] against dark gradient background, dramatic spotlight,
luxury product photography, premium positioning,
sophisticated mood, high-end commercial

Style 4 - Editorial Magazine:
[Product] editorial photography style, artistic composition,
magazine quality, creative angles, fashion-adjacent aesthetic

Style 5 - Warm Natural:
[Product] in warm natural setting, soft window light,
organic styling, [wood/linen/natural materials],
approachable premium feel
```

### Style Decision Framework

| Brand Positioning | Best Style Direction |
|-------------------|---------------------|
| Premium/Luxury | Dark Premium or Editorial Magazine |
| Accessible/Friendly | Lifestyle Context or Warm Natural |
| Tech/Innovation | Clean E-commerce or Dark Premium |
| Natural/Organic | Warm Natural or Lifestyle Context |
| Fashion/Beauty | Editorial Magazine or Dark Premium |
| Utility/Practical | Clean E-commerce or Lifestyle Context |

### Extract Principles from Winner

Once style is chosen, document:

```markdown
## Winning Style: [Name]

**Visual Principles:**
- Background: [specific approach]
- Lighting: [mood and direction]
- Color palette: [tones]
- Composition: [approach]
- Props/styling: [elements]

**Apply across:**
- Hero shot: [how]
- Secondary angles: [how]
- Lifestyle variants: [how]
- Detail shots: [how]
```

---

## Photography Shot Types

### Hero Shot (Primary)

The main product image. Highest stakes, most important.

```
[Product name] hero shot, professional product photography,
[lighting setup], [background], product as focal point,
commercial advertising quality, ultra-detailed, sharp focus,
space for text on [left/right] if needed
```

**What makes hero shots work:**
- Product clearly visible from best angle
- Lighting that creates depth and dimension
- Background that doesn't compete
- Composition that draws eye to product
- Space for marketing copy if needed

---

### Detail/Feature Shot

Highlights specific product features.

```
Close-up detail shot of [specific feature] on [product],
macro product photography, [feature] clearly visible,
shallow depth of field on [feature], professional lighting,
technical detail showcase
```

---

### Lifestyle/Context Shot

Product in use or realistic setting.

```
[Product] in [specific setting], lifestyle product photography,
[person using/product on surface/in environment],
natural lighting, authentic scene, editorial quality,
aspirational but believable context
```

---

### Group/Collection Shot

Multiple products or variants together.

```
Product collection shot, [multiple products] arranged together,
professional studio photography, cohesive styling,
group composition, clear hierarchy with [hero product] prominent,
commercial catalog quality
```

---

### Flat Lay

Top-down arrangement, popular for social media.

```
Flat lay photography, [product] arranged with [complementary items],
top-down view, [surface material], organized aesthetic,
styled composition, editorial product photography
```

---

### Scale/Size Reference

Shows product size with familiar objects.

```
[Product] with scale reference, shown next to [familiar object],
size comparison photography, clear proportion,
professional lighting, clean background
```

---

## Product Category Deep Dives

### Electronics & Tech

**Challenges:** Reflective surfaces, screens, small details
**Opportunities:** Premium tech aesthetic, innovation positioning

```
[Electronic product] professional tech photography,
controlled reflections on metallic/glass surfaces,
screen displaying [content or off], subtle rim lighting on edges,
dark gradient background, premium technology aesthetic,
clean minimal composition, commercial advertising quality
```

**Lighting for tech:**
```
+ subtle rim lighting on edges for dimension
+ controlled reflections (not eliminated, controlled)
+ gradient lighting on screens
+ separation light from background
```

**Common tech products:**
- Headphones: Show both ear cups, cable management, premium materials
- Phones/tablets: Screen content matters, show thinness
- Laptops: Screen angle, keyboard visible, premium materials
- Speakers: Show driver details, premium finishes
- Wearables: Show on wrist/body for scale

---

### Fashion & Apparel

**Challenges:** Fabric texture, accurate colors, shape/drape
**Opportunities:** Lifestyle aspiration, styling context

```
[Apparel item] fashion product photography,
visible fabric texture, accurate [color] reproduction,
natural draping/structure, [styled flat/on model/on hanger],
professional fashion lighting, editorial quality
```

**Key considerations:**
- **Flat lay:** Good for details, pattern visibility
- **On mannequin/form:** Shows structure without model
- **On model:** Highest aspiration, shows fit and movement
- **Hanging:** Simple, shows drape naturally

**Fabric-specific additions:**
- Silk/satin: `+ subtle sheen, controlled highlights, luxurious drape`
- Denim: `+ visible texture and weave, authentic blue tones`
- Leather: `+ rich material quality, subtle surface texture`
- Knitwear: `+ visible knit pattern, cozy texture, soft lighting`

---

### Food & Beverage

**Challenges:** Appetite appeal, freshness, color accuracy
**Opportunities:** Sensory triggers, desire creation

```
[Food/beverage product] professional food photography,
appetizing presentation, [steam/condensation/freshness cues],
natural daylight aesthetic, [surface/props],
editorial food styling, commercial quality
```

**Food photography essentials:**
- **Steam:** Shows freshness, warmth (for hot items)
- **Condensation:** Shows coldness, refreshment (for beverages)
- **Garnish:** Fresh herbs, citrus, adds life
- **Imperfection:** Slight drips, crumbs = authenticity

**Lighting for food:**
```
soft overhead natural daylight feel,
backlit for steam visibility,
side lighting for texture,
warm tones for appetite appeal
```

---

### Beauty & Cosmetics

**Challenges:** Color accuracy, texture rendering, premium feel
**Opportunities:** Aspirational beauty, sensory luxury

```
[Beauty product] professional cosmetic photography,
clean premium aesthetic, [product details visible],
soft diffused beauty lighting, [color] accurate rendering,
luxury cosmetic branding, commercial advertising quality
```

**Product-specific approaches:**
- **Lipstick/makeup:** Show color accurately, often swatched
- **Skincare:** Clean, clinical or spa-like depending on brand
- **Perfume:** Aspirational, often abstract/artistic
- **Haircare:** Often lifestyle with results implied

**Textures to showcase:**
```
+ visible product texture (cream, gel, powder, liquid)
+ packaging material quality
+ applicator/closure details
```

---

### Jewelry & Watches

**Challenges:** Reflections, sparkle, small scale
**Opportunities:** Ultimate luxury positioning

```
[Jewelry/watch] luxury product photography,
controlled reflections with intentional sparkle,
[metal type] surface quality, premium black/gradient background,
rim lighting on metal edges, macro detail visible,
high-end commercial jewelry photography
```

**Jewelry lighting formula:**
```
+ main light for overall exposure
+ rim/edge light for metal definition
+ small accent light for sparkle on stones
+ gradient background for depth
```

**Watch-specific:**
- Show time as 10:10 (traditional, balanced look)
- Highlight dial details, hands, indices
- Show case thickness and finishing
- Crown and pushers visible

---

### Home & Furniture

**Challenges:** Scale, context, room integration
**Opportunities:** Lifestyle aspiration, room transformation

```
[Furniture/home item] interior product photography,
shown in [styled room setting], professional interior photography,
natural window lighting, lifestyle context,
aspirational home aesthetic, editorial interiors quality
```

**Key considerations:**
- Show scale with familiar objects
- Style with complementary decor (not competing)
- Realistic room settings > white void
- Lifestyle aspiration = desire creation

---

## Lighting Mastery

Lighting is the difference between amateur and professional product photography.

### Studio Lighting Setups

**Three-Point (Classic):**
```
three-point lighting setup:
- key light from upper left (main illumination)
- fill light from right (soften shadows)
- rim light from behind (edge separation)
```

**Single Source (Dramatic):**
```
single dramatic spotlight from [direction],
deep shadows, high contrast, gradient falloff,
premium moody aesthetic
```

**Soft Diffused (Beauty):**
```
soft diffused overhead lighting,
large soft box, minimal shadows,
even illumination, beauty product aesthetic
```

**Rim/Edge (Definition):**
```
strong rim lighting from behind,
edge definition on product silhouette,
glowing outline effect, dark background
```

### Natural Lighting Setups

**Window Light (Lifestyle):**
```
natural window lighting from [side],
soft diffused daylight, organic shadows,
lifestyle photography aesthetic
```

**Golden Hour (Warm):**
```
golden hour lighting quality,
warm directional light, long soft shadows,
aspirational warmth
```

**Overcast (Even):**
```
soft overcast natural light,
even illumination, no harsh shadows,
diffused daylight aesthetic
```

### Lighting Direction Guide

| Direction | Effect | Best For |
|-----------|--------|----------|
| Front | Flat, even, safe | E-commerce basics |
| 45° side | Depth, dimension | Most products |
| Side (90°) | Dramatic texture | Textured items |
| Back | Silhouette, glow | Drama, beverages |
| Top (overhead) | Food, flat lay | Food, accessories |
| Under | Dramatic, unusual | Creative/artistic |

---

## Background & Staging

### Studio Backgrounds

**Pure White (#FFFFFF):**
```
on pure white background, seamless backdrop,
no shadows (or: soft drop shadow),
e-commerce clean aesthetic
```
*Best for: Amazon, Shopify, catalog, transparent backgrounds*

**Light Gray Gradient:**
```
on light gray gradient background,
subtle depth, soft shadow beneath product,
professional studio aesthetic
```
*Best for: Website heroes, professional presentations*

**Dark Gradient:**
```
against dark charcoal gradient background,
dramatic studio lighting, premium aesthetic,
product highlighted against dark
```
*Best for: Premium/luxury positioning, tech products*

**Colored Backdrop:**
```
against [color] background,
complementary or brand-aligned color,
bold product presentation
```
*Best for: Brand campaigns, social media*

### Surface Staging

**Marble:**
```
on white marble surface, elegant staging,
luxury product photography, subtle veining
```

**Wood:**
```
on [oak/walnut/rustic] wood surface,
warm organic aesthetic, natural grain visible
```

**Concrete:**
```
on concrete surface, industrial aesthetic,
modern minimal, textured background
```

**Fabric/Linen:**
```
on [white/neutral] linen fabric,
soft organic texture, lifestyle aesthetic
```

### Props & Styling

**Rule:** Props enhance, never compete.

**Good props:**
- Complementary materials (leaves for natural products)
- Lifestyle context items (coffee cup near morning product)
- Scale references (hand, familiar objects)
- Brand-aligned accessories

**Bad props:**
- Competing products
- Distracting colors
- Unrelated items
- Too many elements

---

## Composition Principles

### Rule of Thirds

```
product positioned at rule of thirds intersection,
not centered, dynamic composition,
visual interest through placement
```

### Centered (Hero)

```
product centered in frame,
symmetrical composition, hero positioning,
commanding central presence
```

### Negative Space (Text Room)

```
product positioned [left/right/lower],
negative space on [opposite side] for text overlay,
marketing composition, headline room
```

### Angle Guide

| Angle | Effect | Best For |
|-------|--------|----------|
| Eye level | Relatable, natural | Most products |
| Slightly above | Overview, context | Collections, scenes |
| Slightly below | Powerful, imposing | Premium, hero |
| 45° | Classic product shot | E-commerce |
| Top-down | Flat lay, pattern | Food, accessories |
| Macro/close | Detail, texture | Features, quality |

---

## Platform-Specific Optimization

### Amazon / E-commerce

```
Requirements:
- Main image: Pure white background
- 85%+ frame fill
- No text, graphics, or watermarks
- 1000×1000 minimum (1500×1500 preferred)
- RGB color

Prompt addition:
+ Amazon product listing optimized, pure white background,
product fills 85% of frame, no props or text,
e-commerce compliant, commercial product photography
```

### Shopify / DTC Website

```
More creative freedom than Amazon.
- Hero images can have context
- Lifestyle images encouraged
- Brand aesthetic consistent

Prompt addition:
+ e-commerce hero shot, [brand aesthetic] style,
website product page optimized, commercial quality
```

### Instagram / Social

```
- 1:1 or 4:5 aspect ratio
- Scroll-stopping visuals
- Lifestyle context often better
- Bold colors perform

Prompt addition:
+ Instagram product photography, [1:1/4:5] composition,
scroll-stopping visual, social media optimized,
lifestyle context, bold engaging aesthetic
```

### Hero Banner (Website)

```
- 16:9 or wider aspect ratio
- Space for text overlay
- Product as hero element
- Brand-aligned styling

Prompt addition:
+ hero banner product shot, 16:9 landscape composition,
product as hero element, space for headline on [side],
website banner optimized, marketing asset
```

### Pinterest

```
- 2:3 vertical (1000×1500)
- Aspirational lifestyle
- Text overlays work here
- Save-worthy aesthetic

Prompt addition:
+ Pinterest product pin, vertical 2:3 composition,
aspirational lifestyle photography, save-worthy visual,
space for text overlay, editorial product aesthetic
```

---

## Execution Workflow

### Step 1: Gather Requirements

```
□ What product? (specific details, materials, features)
□ What use case? (Amazon, hero banner, social, etc.)
□ What style? (or need style exploration?)
□ What aspect ratio?
□ Text space needed?
□ Brand colors/aesthetic?
```

### Step 2: Style Exploration (if new product/brand)

Generate 5 different visual approaches, pick winner, extract principles.

### Step 3: Construct Prompt

Use the formula:
```
[Product specific description] + [Shot type] + [Lighting] +
[Background/staging] + [Composition] + [Quality boosters] +
[Platform optimization]
```

### Step 4: Generate

```
Glif: Nano Banana Pro Text 2 Image
ID: cmi7ne4p40000kz04yup2nxgh
Inputs: ["[constructed prompt]"]
```

### Step 5: Review & Iterate

**Check against requirements:**
- Product accurately represented?
- Correct lighting mood?
- Background works?
- Composition effective?
- Platform requirements met?

**Common iteration adjustments:**
```
Too dark → add "bright, well-lit, high key"
Too cluttered → add "minimal, clean, simple"
Wrong angle → specify angle explicitly
Reflections wrong → add "controlled reflections"
Not premium enough → add "luxury, premium, high-end"
```

### Step 6: Approve or Variant

- If approved → Deliver final
- If close → Iterate with adjustments
- If fundamentally wrong → New prompt approach

---

## Quality Checklist

### Technical Quality
- [ ] Resolution sufficient for intended use
- [ ] No obvious AI artifacts (weird reflections, melted details)
- [ ] Sharp focus on product
- [ ] Appropriate for platform requirements

### Product Accuracy
- [ ] Product features clearly visible
- [ ] Colors accurate to actual product
- [ ] Scale/proportions correct
- [ ] Key selling points highlighted

### Commercial Quality
- [ ] Looks professionally photographed
- [ ] Lighting creates depth and dimension
- [ ] Background supports (not competes with) product
- [ ] Composition is intentional

### Platform Fit
- [ ] Correct aspect ratio
- [ ] Meets platform requirements (Amazon white, etc.)
- [ ] Style matches platform expectations
- [ ] Text space if needed

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Looks obviously AI | Generic prompt | Add specific commercial photography terms |
| Wrong reflections | Not controlled | Add "controlled reflections, professional lighting" |
| Flat lighting | No direction | Specify lighting direction and type |
| Product unclear | Too much context | Simplify, focus on product |
| Wrong scale | No reference | Add scale context or familiar objects |
| Colors off | Model interpretation | Be very specific about colors |
| Too perfect | Hyperreal rendering | Add subtle imperfection cues if needed |
| Wrong background | Default used | Explicitly specify background |
| Not commercial | Missing quality terms | Add "commercial, advertising, professional" |
| Competing elements | Props too prominent | Simplify staging, props should be subtle |

---

## Output Format

```markdown
## Product Photo Generated

**Product:** [name]
**Shot Type:** [hero/detail/lifestyle/etc.]
**Style:** [visual approach]
**Aspect Ratio:** [ratio]

**Image URL:** [URL]

**Prompt Used:**
> [full prompt for reference]

**Quality Check:**
- [ ] Product accurate
- [ ] Lighting effective
- [ ] Background appropriate
- [ ] Platform requirements met

**Feedback?**
- Product representation accurate?
- Lighting/mood right?
- Background works?
- Ready to approve or iterate?

**Options:**
- [ ] Approve this shot
- [ ] Iterate (specify changes)
- [ ] Generate different angle
- [ ] Try different style approach
```

---

## Integration with Pipeline

```
PRODUCT PHOTO PIPELINE

┌─────────────────────────────────────────┐
│  Request arrives                        │
│  → Direct or from ai-creative-workflow  │
│  → Clarify product and requirements     │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│  Style Exploration (if needed)          │
│  → Generate 5 different approaches      │
│  → User selects winner                  │
│  → Extract principles for consistency   │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│  ai-product-photo (THIS SKILL)          │
│  → Construct platform-optimized prompt  │
│  → Generate with Nano Banana Pro/Glif   │
│  → Review against quality checklist     │
│  → Iterate as needed                    │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌──────────────────┐   ┌──────────────────┐
│  Static Delivery │   │  Route to Video  │
│  → Final product │   │  → ai-product-   │
│    images        │   │    video         │
└──────────────────┘   └──────────────────┘
```

---

## Handoff Protocols

### Receiving from ai-creative-workflow
```yaml
Receive:
  product: "[what product]"
  category: "[electronics/fashion/food/etc.]"
  shot_type: "[hero/detail/lifestyle/etc.]"
  platform: "[Amazon/Instagram/hero banner/etc.]"
  style: "[if established]"
  brand_colors: "[if specified]"
  text_space: true/false
```

### Returning to Workflow
```yaml
Return:
  status: "complete" | "needs_iteration" | "needs_different_approach"
  deliverables:
    - url: "[image URL]"
      shot_type: "[type]"
      aspect_ratio: "[ratio]"
      prompt_used: "[prompt]"
  additional_shots_available: true/false
```

### Routing to Video
```yaml
Route to ai-product-video:
  image_url: "[approved product image URL]"
  product: "[product name]"
  animation_type: "[reveal/360/floating/etc.]"
  platform: "[destination platform]"
```

---

## Pro Tips from Commercial Photography

### What Actually Sells

1. **Show the benefit, not just the product** — Headphones in use > headphones floating
2. **Lighting creates desire** — Dramatic lighting = premium perception
3. **Context triggers imagination** — "I could use that here"
4. **Details signal quality** — Close-ups show craftsmanship
5. **Consistency builds brand** — Same style across all product shots

### Common Amateur Mistakes

1. **Flat front lighting** — Use directional light for depth
2. **Random backgrounds** — Match background to positioning
3. **Product too small** — Fill the frame (especially e-commerce)
4. **Competing props** — Props enhance, never distract
5. **Inconsistent style** — Build a system, not one-offs

### The 80/20 of Product Photography

80% of results come from:
1. Specific product description in prompt
2. Appropriate lighting direction/type
3. Background that supports positioning
4. Platform-correct composition

Get these four right and you'll outperform most AI product photos.

---

## Example Prompts (Complete)

### Tech Hero Shot
```
Premium wireless over-ear headphones hero shot,
silver and black colorway, soft padding visible,
floating against dark charcoal gradient background,
dramatic single spotlight from upper left,
subtle rim lighting on edges, metallic surface reflections controlled,
negative space on right for headline,
commercial technology advertising photography,
ultra-detailed, professional quality, 16:9 composition
```

### Skincare E-commerce
```
Luxury skincare serum bottle product photography,
glass bottle with dropper, golden serum visible,
on pure white background, Amazon listing optimized,
soft diffused studio lighting, product fills 85% of frame,
clean minimal composition, accurate color rendering,
commercial beauty product photography, 1:1 square
```

### Food Lifestyle
```
Artisan coffee bag product in lifestyle setting,
kraft paper bag with window showing beans,
on rustic wooden kitchen counter, morning light through window,
fresh coffee beans scattered, ceramic mug nearby,
lifestyle food photography, warm inviting tones,
editorial quality, aspirational home aesthetic
```

### Jewelry Macro
```
Diamond engagement ring luxury photography,
platinum band, brilliant cut center stone,
extreme detail macro shot, sparkle on facets,
black gradient background, controlled reflections,
rim lighting on metal edges, jeweler quality detail,
high-end commercial jewelry photography
```

### Fashion Flat Lay
```
Premium leather wallet flat lay photography,
brown full-grain leather, visible stitching detail,
on white marble surface, minimalist styling,
styled with brass key holder and pen,
top-down composition, editorial menswear aesthetic,
soft even lighting, luxury accessories photography
```
