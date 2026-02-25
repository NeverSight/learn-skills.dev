---
name: ai-product-video
description: "Specialized skill for AI product video generation. Use when you need product reveals, animated product shots, hero video banners, or e-commerce video content. Triggers on: product video, product reveal, animate product, hero video. Outputs professional product videos."
---

# AI Product Video

Transform static product images into cinematic video content. This skill handles product reveals, animated hero shots, 360 showcases, and e-commerce video — all the video types that make products feel premium and desirable.

**Use this skill when:** You have a product image to animate or need product-focused video content.
**Route here from:** ai-product-photo after image approval, or ai-creative-workflow for direct video needs.

---

## Why This Skill Exists

**The problem:** Video content converts dramatically better than static images, but:
1. Traditional product video requires expensive shoots
2. Most AI video prompts produce generic, floaty results
3. Different platforms need different video styles
4. Wrong motion can cheapen even premium products

**The solution:** A systematic approach that:
- Uses proven commercial motion styles
- Matches motion to product category and positioning
- Leverages multi-model generation for quality selection
- Anchors animation to approved static images (I2V workflow)

---

## Video Model Roster

**Strategy:** Generate with multiple models, present outputs for selection. Different models excel at different things.

| Model | Owner | Speed | Best For |
|-------|-------|-------|----------|
| **Sora 2** | openai | ~80s | General quality, text comprehension |
| **Veo 3.1** | google | ~130s | Audio generation, cinematic quality |
| **Kling v2.5 Turbo Pro** | kwaivgi | ~155s | People, natural motion, longer coherence |

### Model Strengths & Weaknesses

**Sora 2:**
- Excellent prompt comprehension
- Good motion coherence
- Sometimes over-stylizes
- No native audio

**Veo 3.1:**
- Can generate matching audio
- Cinematic quality
- Slower generation
- Sometimes "interprets" prompts loosely

**Kling v2.5:**
- Best for human subjects
- Natural motion quality
- Longer video coherence
- Sometimes adds unwanted elements

### When to Use Which

```
GENERAL PRODUCT → Sora 2 (reliable, fast)
NEEDS AUDIO → Veo 3.1 (native audio)
HAS PEOPLE → Kling v2.5 (best human motion)
UNCERTAIN → Run all 3, pick winner
```

---

## I2V vs T2V: Why Image-First Wins

### Image-to-Video (I2V) — RECOMMENDED

```
ai-product-photo → [approve image] → ai-product-video (I2V)
```

**Why I2V is superior for products:**
- Frame 1 is exactly what you approved
- Product appearance locked in
- Motion anchored to known composition
- Easy iteration without changing product
- If video fails, you still have the approved image

### Text-to-Video (T2V)

Only use when:
- No source image available
- Need completely new composition
- Exploring motion concepts before committing to image

T2V requires extremely detailed prompts and often needs multiple attempts.

---

## Motion Style Exploration

**Don't lock into one motion style.** Generate multiple approaches, pick the winner.

### Why Motion Style Matters

The same product animated differently can feel:
- Premium vs cheap
- Innovative vs traditional
- Exciting vs calming
- Professional vs amateur

**One style = hope. Multiple styles = informed choice.**

### 5 Motion Style Directions

For any product, consider these distinct approaches:

```
Style 1 - Slow Reveal (Premium):
Slow cinematic push-in, dramatic lighting shifts,
atmospheric particles, elegant pacing, luxury feel

Style 2 - Orbit Showcase (360):
Camera smoothly orbits product, reveals all angles,
professional product demo, informational

Style 3 - Floating Premium (Tech):
Product floats weightlessly, gentle hover motion,
dreamlike quality, premium tech aesthetic

Style 4 - Dynamic Energy (Bold):
Fast camera moves, dramatic angles, high energy,
sports/action commercial aesthetic

Style 5 - Contextual/Lifestyle:
Product in use or setting, natural motion,
lifestyle commercial, relatable context
```

### Style Decision Framework

| Product Positioning | Best Motion Style |
|---------------------|-------------------|
| Luxury/Premium | Slow Reveal or Floating Premium |
| Tech/Innovation | Floating Premium or Dynamic Energy |
| Practical/Everyday | Orbit Showcase or Contextual |
| Fashion/Lifestyle | Contextual or Slow Reveal |
| Sports/Action | Dynamic Energy |
| Food/Beverage | Slow Reveal or Contextual |

---

## Motion Style Deep Dives

### Slow Reveal (Premium)

The go-to for luxury and premium products. Builds anticipation, creates desire.

```
Slow cinematic push-in toward [product], smooth elegant motion,
dramatic spotlight illumination with subtle light shifts,
atmospheric dust particles drifting through light beam,
premium commercial reveal, luxurious pacing, 5 seconds
```

**Key elements:**
- **Speed:** Slow, deliberate (builds anticipation)
- **Camera:** Push-in (draws viewer to product)
- **Lighting:** Dramatic shifts (creates dimension)
- **Atmosphere:** Particles/bokeh (premium feel)

**Variations:**
```
+ gradual brightness increase (dawn reveal)
+ side lighting sweep (sculptural reveal)
+ spot to fill (dramatic to detailed)
+ emerging from darkness (mystery reveal)
```

---

### Orbit Showcase (360)

Shows product from multiple angles. Informational but can be premium.

```
Camera smoothly orbits around [product], elegant 180-degree arc,
lighting shifts to reveal different surfaces and angles,
product remains perfectly centered, professional product showcase,
commercial demo quality, smooth continuous motion, 5 seconds
```

**Key elements:**
- **Speed:** Moderate, steady (professional)
- **Camera:** Orbiting (reveals all angles)
- **Lighting:** Shifts with camera (reveals features)
- **Product:** Centered, stable (not rotating itself)

**Variations:**
```
+ low angle orbit (powerful, imposing)
+ high angle orbit (overview, accessible)
+ half orbit with return (A-B-A motion)
+ orbit with zoom (combining movements)
```

---

### Floating Premium (Tech)

Weightless, dreamlike quality. Perfect for tech products.

```
[Product] floating weightlessly in space, gentle hovering motion
with subtle micro-movements, soft rotating drift,
premium tech aesthetic, clean minimal environment,
dreamlike quality, smooth ethereal motion, 5 seconds
```

**Key elements:**
- **Speed:** Very slow (dreamlike)
- **Motion:** Floating, hovering (defies gravity)
- **Environment:** Clean, minimal (focus on product)
- **Quality:** Ethereal, otherworldly (premium tech)

**Variations:**
```
+ subtle particle field (space tech)
+ gentle light ripples (premium feel)
+ minimal rotation (revealing sides)
+ breathing motion (organic tech)
```

---

### Dynamic Energy (Bold)

High energy for products that need excitement. Sports, gaming, lifestyle.

```
Dynamic reveal of [product], fast camera sweep with dramatic angles,
high energy motion with impact moment, bold lighting changes,
sports commercial aesthetic, exciting and engaging,
powerful reveal with kinetic energy, 5 seconds
```

**Key elements:**
- **Speed:** Fast, punchy (exciting)
- **Camera:** Dramatic angles, sweeps (energy)
- **Lighting:** Bold changes (dramatic)
- **Feel:** Impact, power (commanding)

**Variations:**
```
+ whip pan reveal (extreme speed)
+ crash zoom (sudden attention)
+ rotating explosion (dynamic start)
+ stop-motion style beats (rhythmic energy)
```

---

### Contextual/Lifestyle

Product in realistic use or setting. Relatable, aspirational.

```
[Product] in [setting], natural environmental motion,
[person interacting/environmental movement/ambient motion],
lifestyle commercial quality, authentic feel,
relatable context, aspirational but believable, 5 seconds
```

**Key elements:**
- **Speed:** Natural pace (realistic)
- **Motion:** Environmental (wind, hands, ambient)
- **Setting:** Realistic context (relatable)
- **Feel:** Authentic (not over-produced)

**Variations:**
```
+ morning light shift (time passing)
+ hand reach/grab (product use)
+ environmental wind (outdoor context)
+ steam/condensation (food/beverage)
```

---

## Camera Motion Vocabulary

Master these terms for precise motion control.

### Camera Movements

| Movement | Description | Best For |
|----------|-------------|----------|
| **Push-in** | Camera moves toward subject | Reveals, focus, intimacy |
| **Pull-out** | Camera moves away from subject | Context reveal, endings |
| **Orbit** | Camera circles subject | 360 showcase, features |
| **Dolly** | Smooth lateral movement | Panning reveals, scanning |
| **Crane** | Vertical movement | Grand reveals, overhead |
| **Tracking** | Following movement | Motion, lifestyle |

### Motion Speeds

| Speed | Description | Creates |
|-------|-------------|---------|
| **Slow** | Deliberate, elegant | Premium, luxury, contemplation |
| **Moderate** | Natural pace | Professional, informational |
| **Fast** | Quick, dynamic | Energy, excitement, urgency |
| **Variable** | Speed changes | Drama, emphasis, rhythm |

### Subject Movements

| Movement | Description | Best For |
|----------|-------------|----------|
| **Float** | Gentle hovering | Tech, premium, dreamlike |
| **Rotate** | Spinning on axis | Feature reveal, 360 |
| **Shimmer** | Light play across surface | Luxury, jewelry, metallic |
| **Settle** | Coming to rest | Endings, product placement |
| **Rise** | Ascending motion | Reveals, emergence |

### Atmospheric Elements

| Element | Description | Creates |
|---------|-------------|---------|
| **Particles** | Floating dust/light | Premium, cinematic |
| **Bokeh** | Background blur animation | Focus, depth |
| **Light shift** | Changing illumination | Drama, dimension |
| **Reflections** | Moving light on surfaces | Luxury, quality |
| **Shadows** | Shadow movement | Time, drama |

---

## Product Category Deep Dives

### Electronics & Tech

**Motion characteristics:**
- Controlled reflections moving across surfaces
- Subtle LED/screen glow animation
- Premium tech aesthetic
- Clean, precise motion

```
[Tech product] with controlled reflections moving across
metallic surfaces, subtle indicator lights glowing,
premium technology commercial motion, clean precise aesthetic,
professional tech showcase, sophisticated reveal
```

**Best styles:** Floating Premium, Slow Reveal
**Avoid:** Chaotic motion, uncontrolled reflections

---

### Fashion & Apparel

**Motion characteristics:**
- Natural fabric movement
- Subtle wind/flow effects
- Fashion editorial quality
- Elegant, aspirational

```
[Apparel item] with natural fabric movement, subtle wind effect
creating gentle flow, fashion commercial motion quality,
elegant and aspirational, editorial photography in motion
```

**Best styles:** Slow Reveal, Contextual
**Avoid:** Stiff fabric, unnatural movement

---

### Food & Beverage

**Motion characteristics:**
- Rising steam (hot items)
- Condensation (cold items)
- Fresh ingredient motion
- Appetizing reveal

```
[Food/beverage product] with [steam rising/condensation forming],
fresh appetizing motion, food commercial aesthetic,
delicious reveal, mouth-watering presentation,
warm inviting tones in motion
```

**Best styles:** Slow Reveal, Contextual
**Key elements:** Steam, pour, drip, fresh

---

### Beauty & Cosmetics

**Motion characteristics:**
- Smooth texture reveals
- Shimmer and sparkle
- Luxury beauty aesthetic
- Elegant product motion

```
[Beauty product] with smooth cream/liquid texture in motion,
subtle shimmer and light play, luxury beauty commercial aesthetic,
elegant product reveal, premium cosmetic presentation,
sophisticated and aspirational
```

**Best styles:** Slow Reveal, Floating Premium
**Avoid:** Fast motion, harsh lighting

---

### Jewelry & Watches

**Motion characteristics:**
- Sparkling reflections
- Light dancing across facets
- Luxury slow motion
- Elegant rotation

```
[Jewelry/watch] with sparkling reflections, light dancing
across precious surfaces and facets, luxury jewelry commercial,
elegant slow rotation revealing brilliance,
premium positioning, sophisticated motion
```

**Best styles:** Slow Reveal, Orbit Showcase
**Key:** Controlled sparkle, not chaotic reflections

---

### Furniture & Home

**Motion characteristics:**
- Environmental context motion
- Natural light shifts
- Lifestyle integration
- Scale demonstration

```
[Furniture/home product] in styled room setting,
natural light shifting through window, environmental motion,
lifestyle interior commercial, aspirational home aesthetic,
showing product in context, inviting atmosphere
```

**Best styles:** Contextual, Slow Reveal
**Key:** Show scale, show in use

---

## Sound Design Considerations

### When to Use Audio

**Veo 3.1** can generate matching audio. Consider:

| Content Type | Audio Recommendation |
|--------------|---------------------|
| Premium reveal | Subtle ambient + bass swell |
| Tech product | Electronic tones, clean |
| Lifestyle | Environmental sounds |
| Food | Sizzle, pour, crunch |
| Fashion | Music-driven |

### Audio Prompt Additions (Veo 3.1)

```
With accompanying audio:
+ subtle cinematic bass swell on reveal
+ ambient room tone with product sounds
+ gentle electronic undertone
+ natural environmental audio
```

### When to Skip Audio

- Will add music in post
- Platform auto-mutes
- Need flexibility for voiceover
- Clean audio for other edit

---

## Platform Specifications

### Hero Banners (Website)

```
Ratio: 16:9
Duration: 5-8 seconds
Loop: Clean loop or freeze-end
Motion: Premium reveal or floating
Quality: High bitrate, clean compression
```

### Instagram Feed

```
Ratio: 1:1 (square) or 4:5 (portrait)
Duration: 5-15 seconds
Loop: Seamless loops perform best
Motion: Scroll-stopping first frame
Quality: Mobile-optimized
```

### Instagram Stories/Reels

```
Ratio: 9:16 (vertical)
Duration: 5-15 seconds
Loop: Optional
Motion: Vertical-optimized composition
Quality: Mobile-first
Safe Zone: Avoid top/bottom UI areas
```

### TikTok

```
Ratio: 9:16 (vertical)
Duration: 5-15 seconds
Style: More dynamic, native aesthetic
Motion: Not over-produced
Quality: Mobile-optimized
```

### Product Pages

```
Ratio: 16:9 or 1:1
Duration: 5-15 seconds
Loop: Clean loops
Motion: Informational (orbit, features)
Quality: Fast loading
```

---

## Execution Workflow

### Step 1: Source Image

**Option A:** Use approved image from ai-product-photo
```
Source: [approved product image URL]
Ratio: [must match desired video ratio]
```

**Option B:** Generate image first
Route to ai-product-photo → approve → return here

### Step 2: Motion Style Selection

Choose approach or generate multiple for comparison:

```
□ Slow Reveal (Premium)
□ Orbit Showcase (360)
□ Floating Premium (Tech)
□ Dynamic Energy (Bold)
□ Contextual/Lifestyle
□ Explore multiple (generate 2-3 approaches)
```

### Step 3: Construct Motion Prompt

Formula:
```
[Motion style template] + [Product-specific additions] +
[Category modifications] + [Duration] + [Quality terms]
```

### Step 4: Multi-Model Generation

Run same prompt through selected models:

**Sora 2:**
```json
{
  "model_owner": "openai",
  "model_name": "sora-2",
  "input": {
    "prompt": "[motion prompt]",
    "first_frame_image": "[source image URL]",
    "aspect_ratio": "[16:9/9:16/1:1]",
    "duration": "5s"
  }
}
```

**Veo 3.1:**
```json
{
  "model_owner": "google",
  "model_name": "veo-3.1",
  "input": {
    "prompt": "[motion prompt]",
    "image": "[source image URL]",
    "aspect_ratio": "[16:9/9:16/1:1]",
    "generate_audio": true
  }
}
```

**Kling v2.5:**
```json
{
  "model_owner": "kwaivgi",
  "model_name": "kling-v2.5-turbo-pro",
  "input": {
    "prompt": "[motion prompt]",
    "start_image": "[source image URL]",
    "aspect_ratio": "[16:9/9:16/1:1]"
  }
}
```

**Run in parallel.** Poll for completion (~2-3 minutes each).

### Step 5: Present Options

```markdown
## Product Video Options Generated

**Source Image:** [URL]
**Motion Style:** [style description]
**Aspect Ratio:** [ratio]

### Option 1: Sora 2
**Video URL:** [URL]
**Generation Time:** ~80s
**Notes:** [any observations]

### Option 2: Veo 3.1 (with audio)
**Video URL:** [URL]
**Generation Time:** ~130s
**Notes:** [any observations]

### Option 3: Kling v2.5
**Video URL:** [URL]
**Generation Time:** ~155s
**Notes:** [any observations]

**Which output do you prefer?**
- Motion quality?
- Matches product positioning?
- Ready to approve or try different style?
```

### Step 6: Approve or Iterate

- **Approved:** Deliver selected video
- **Close but not right:** Adjust prompt, regenerate
- **Wrong style:** Try different motion approach
- **Technical issue:** Debug, regenerate

---

## Quality Checklist

### Technical Quality
- [ ] Resolution matches platform requirements
- [ ] No obvious AI artifacts (warping, morphing)
- [ ] Smooth motion (no jitter, stuttering)
- [ ] Consistent throughout duration
- [ ] Clean compression (no blocking)

### Motion Quality
- [ ] Motion style matches product positioning
- [ ] Speed appropriate for intended feel
- [ ] Camera movement intentional
- [ ] No unwanted elements added
- [ ] Product remains recognizable throughout

### Commercial Quality
- [ ] Looks professionally produced
- [ ] Would work in commercial context
- [ ] Elevates product perception
- [ ] Appropriate for platform
- [ ] Matches brand aesthetic

### Platform Fit
- [ ] Correct aspect ratio
- [ ] Appropriate duration
- [ ] Works with platform compression
- [ ] Loop-friendly (if needed)
- [ ] Safe zones respected (mobile)

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Product morphs/changes | Model interpretation | Simpler motion prompt, use I2V |
| Motion too fast | Prompt too energetic | Add "slow," "elegant," "smooth" |
| Motion too slow | Over-specified slowness | Adjust speed terms |
| Wrong elements appear | Model hallucination | Simpler prompt, different model |
| Reflections wrong | Uncontrolled light | Add "controlled reflections" |
| Looks cheap | Wrong motion style | Match style to positioning |
| Doesn't loop | Not specified | Add "seamless loop" to prompt |
| Wrong aspect | Default used | Specify ratio in API call |
| No audio (Veo) | Not enabled | Set `generate_audio: true` |
| Background changes | Unstable composition | Use cleaner source image |

---

## Iteration Strategies

### When Motion Is Close But Not Right

**Problem:** Almost there but something's off
**Strategy:** Targeted prompt adjustments

```
Too fast → add "slow," "elegant," "deliberate"
Too static → add "dynamic," "moving," "shifting"
Too chaotic → add "smooth," "controlled," "stable"
Wrong mood → adjust atmosphere terms
```

### When Motion Is Completely Wrong

**Problem:** Output doesn't match intent
**Strategy:** Different approach entirely

Don't iterate on broken foundation:
1. Try different motion style
2. Try different model
3. Simplify prompt dramatically
4. Check source image quality

### When Technical Issues Occur

**Problem:** Artifacts, morphing, glitches
**Strategy:** Technical fixes

```
- Use cleaner source image
- Simpler motion request
- Different model
- Lower complexity prompt
```

---

## Output Format

### Single Output
```markdown
## Product Video Generated

**Product:** [name]
**Motion Style:** [style]
**Model:** [selected model]
**Aspect Ratio:** [ratio]
**Duration:** [seconds]

**Video URL:** [URL]

**Motion Prompt Used:**
> [full prompt for reference]

**Quality Check:**
- [ ] Motion quality
- [ ] Product consistency
- [ ] Platform appropriate
- [ ] Commercial quality

**Feedback?**
- Motion style right?
- Speed appropriate?
- Ready to approve or iterate?
```

### Multi-Option Output
```markdown
## Product Video Options

**Source Image:** [URL]
**Motion Style:** [style]

### Option 1: [Model]
- URL: [video URL]
- Observations: [notes]

### Option 2: [Model]
- URL: [video URL]
- Observations: [notes]

### Option 3: [Model]
- URL: [video URL]
- Observations: [notes]

**Select preferred output:**
- [ ] Option 1
- [ ] Option 2
- [ ] Option 3
- [ ] Try different motion style
```

---

## Integration with Pipeline

```
PRODUCT VIDEO PIPELINE

┌─────────────────────────────────────────┐
│  Request arrives                        │
│  → Direct or from ai-creative-workflow  │
│  → Source image required?               │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌──────────────────┐   ┌──────────────────┐
│  Has source      │   │  Needs source    │
│  image           │   │  image           │
└───────┬──────────┘   └────────┬─────────┘
        │                       │
        │                       ▼
        │              ┌──────────────────┐
        │              │  ai-product-     │
        │              │  photo           │
        │              │  → Generate      │
        │              │  → Approve       │
        │              └────────┬─────────┘
        │                       │
        └───────────┬───────────┘
                    ▼
┌─────────────────────────────────────────┐
│  Motion Style Selection                 │
│  → Single style or multiple exploration │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│  ai-product-video (THIS SKILL)          │
│  → Construct motion prompt              │
│  → Multi-model generation               │
│  → Present options                      │
│  → User selects winner                  │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌──────────────────┐   ┌──────────────────┐
│  Delivery        │   │  Route to        │
│  → Final video   │   │  ai-talking-head │
│                  │   │  → Add voiceover │
└──────────────────┘   └──────────────────┘
```

---

## Handoff Protocols

### Receiving from ai-product-photo
```yaml
Receive:
  source_image: "[approved image URL]"
  product: "[product name]"
  aspect_ratio: "[ratio]"
  style_direction: "[if established from image session]"
  platform: "[destination platform]"
```

### Receiving from ai-creative-workflow
```yaml
Receive:
  product: "[product name]"
  video_purpose: "[hero/social/product page/etc.]"
  motion_style: "[if specified]"
  platform: "[destination platform]"
  source_image: "[if available]"
```

### Returning to Workflow
```yaml
Return:
  status: "complete" | "needs_iteration" | "needs_different_approach"
  deliverables:
    - url: "[video URL]"
      model: "[which model]"
      duration: "[seconds]"
      aspect_ratio: "[ratio]"
      has_audio: true/false
      prompt_used: "[motion prompt]"
  additional_options_generated: true/false
```

### Routing to Talking Head
```yaml
Route to ai-talking-head:
  video_url: "[approved product video]"
  voiceover_needed: true
  voiceover_content: "[script or description]"
  integration_style: "[overlay/transition/split]"
```

---

## Pro Tips

### What Makes Product Video Work

1. **Motion matches positioning** — Premium products need premium motion
2. **Less is often more** — Subtle motion > chaotic movement
3. **First frame matters** — Thumbnail is first impression
4. **Consistency throughout** — Product should be recognizable entire duration
5. **Purpose-driven motion** — Every movement should have reason

### Common Mistakes to Avoid

1. **Over-animated** — Too much motion cheapens products
2. **Wrong speed** — Fast motion for luxury = mistake
3. **Generic prompts** — "Product reveal" is too vague
4. **Ignoring source** — Bad source image = bad video
5. **Single model reliance** — Different models excel differently

### The 80/20 of Product Video

80% of results come from:
1. Quality source image (I2V workflow)
2. Appropriate motion style for product
3. Speed matching product positioning
4. Clean, simple motion prompts

Get these four right and you'll outperform most AI product videos.

---

## Example Prompts (Complete)

### Tech Hero Reveal
```
Slow cinematic push-in toward premium wireless headphones,
floating weightlessly against dark gradient background,
dramatic spotlight shifts revealing metallic surfaces,
controlled reflections moving across ear cups,
atmospheric particles drifting through light beam,
premium technology commercial, smooth elegant motion,
5 seconds, 16:9
```

### Skincare Orbit
```
Camera smoothly orbits luxury skincare serum bottle,
elegant 180-degree arc revealing glass bottle from all angles,
light shifts to reveal golden serum liquid inside,
clean white environment, professional product showcase,
beauty commercial quality, sophisticated motion,
5 seconds, 1:1 square
```

### Food Reveal
```
Slow reveal of artisan coffee package on rustic wooden surface,
steam rising from freshly poured cup nearby,
morning light shifting through window, warm golden tones,
fresh coffee beans gently settling, appetizing motion,
food commercial aesthetic, inviting atmosphere,
5 seconds, 9:16 vertical
```

### Watch Showcase
```
Premium watch floating with gentle hover motion,
light dancing across crystal and polished steel,
subtle rotation revealing dial details,
luxury jewelry commercial motion, elegant and sophisticated,
controlled sparkle on metal surfaces,
premium positioning, 5 seconds, 16:9
```

### Fashion Wind
```
Silk scarf with natural wind movement creating elegant flow,
subtle fabric ripples and gentle billowing motion,
fashion editorial quality, aspirational and sophisticated,
light catching silk sheen as fabric moves,
lifestyle commercial aesthetic, 5 seconds, 4:5
```
