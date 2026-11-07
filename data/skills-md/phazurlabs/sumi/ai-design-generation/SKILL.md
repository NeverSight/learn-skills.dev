---
name: ai-design-generation
description: "Produce visual assets from AI image and UI models through MCP — Stitch screens, Fal.ai (Imagen, FLUX, Veo), Recraft V3 vectors, GPT-Image and Figma file access — with prompt patterns and quality scoring. Use when rendering mockups, icons, illustrations or video. Not for interface copy; not for agent UX."
---

# AI Design Generation

## 1. AI Design Generation Philosophy

### AI as Co-Pilot, Not Replacement

AI generation tools are accelerators, not replacements for design thinking. A generation tool has no understanding of user needs, business goals, or brand strategy — it only transforms text into pixels. The designer (or design-aware agent like Sumi) provides the intelligence: the brief, the constraints, the quality bar, the iteration direction.

**The Co-Pilot Model:**
- Human/agent defines the problem, constraints, and success criteria
- AI generates candidates rapidly across the solution space
- Human/agent evaluates, selects, critiques, and steers
- AI refines based on directed feedback
- Human/agent makes final production decisions

This is not a compromise — it is genuinely superior to either pure human or pure AI workflows. AI explores breadth (hundreds of variations in minutes); humans provide depth (taste, context, strategy). The combination outperforms either alone.

### The Human Curation Loop

Every AI generation workflow must include a curation checkpoint. The loop follows a consistent pattern:

1. **Specify** — Translate design intent into a structured prompt
2. **Generate** — Produce 3-6 candidates per round
3. **Evaluate** — Score against design criteria (brand, usability, aesthetics)
4. **Select** — Choose the strongest candidate(s) to advance
5. **Refine** — Adjust the prompt based on what worked and what did not
6. **Repeat** — 2-4 rounds typically reach production quality

Never ship a first-generation output without evaluation. Even when the result looks good, check: Does it match the brand? Is the typography readable? Are the proportions correct? Does it solve the actual user problem?

### Prompt Engineering as a Design Skill

Writing effective generation prompts is a design discipline. It requires the same skills as writing a design brief: clarity about goals, specificity about constraints, awareness of audience, and taste in execution. The best prompters are experienced designers who understand what to ask for — not prompt template collectors.

**Core Principles of Design Prompt Engineering:**
- Specificity beats length — "16px Inter Medium, #1A1A2E on white, 8px radius card" beats "make it look modern and clean"
- Reference real products — "Stripe dashboard density" communicates more than paragraphs of description
- Constrain before you create — State what the design must NOT do (no gradients, no stock photos, no rounded avatars)
- Layer your prompt — Style first, then layout, then content, then fine details
- Include quality modifiers — "production-ready", "pixel-perfect", "4K render" shift models toward higher fidelity

---

## 2. MCP Integration Overview

### How Claude Code Connects to Design Generation Tools

Claude Code communicates with design generation services through MCP (Model Context Protocol) servers. Each MCP server wraps an external API and exposes it as a set of tools that Claude can invoke directly within a conversation.

**The Architecture:**
```
User Request → Claude Code (Sumi skill) → MCP Server → External API → Generated Asset
                      ↓                                        ↓
              Prompt Engineering                         Raw Output
              Quality Scoring                            Post-Processing
              Iteration Direction                        Final Delivery
```

**Key Benefits of MCP Integration:**
- Claude can generate designs mid-conversation without the user leaving the terminal
- Prompt construction is automated using Sumi's design intelligence
- Results can be evaluated, iterated, and refined in a continuous loop
- Multiple tools can be chained in a single pipeline (e.g., Stitch for layout, Fal.ai for hero image, Recraft for icons)

### MCP Server Configuration

All MCP servers are configured in Claude Code's settings. Each server requires an API key for its respective service. Configuration is stored in `~/.claude/mcp_servers.json` or the project-level `.mcp.json`.

**Example Configuration:**
```json
{
  "mcpServers": {
    "stitch": {
      "command": "npx",
      "args": ["@anthropic/stitch-mcp"],
      "env": { "STITCH_API_KEY": "sk-..." }
    },
    "fal": {
      "command": "npx",
      "args": ["@fal-ai/mcp"],
      "env": { "FAL_KEY": "key-..." }
    },
    "recraft": {
      "command": "npx",
      "args": ["recraft-mcp"],
      "env": { "RECRAFT_API_KEY": "rc-..." }
    },
    "figma": {
      "command": "npx",
      "args": ["@anthropic/figma-mcp"],
      "env": { "FIGMA_ACCESS_TOKEN": "figd_..." }
    }
  }
}
```

### Supported MCP Servers (All Optional)

| Server | What It Does | Install | Key Required |
|--------|-------------|---------|-------------|
| stitch-mcp | Generate UI screens from text descriptions | `npm i -g @anthropic/stitch-mcp` | Stitch API |
| @fal-ai/mcp | 600+ image/video models (Imagen 4, FLUX, Veo 3.1, Recraft V3) | `npm i -g @fal-ai/mcp` | Fal.ai API |
| replicate-mcp | Open-source model access | `npm i -g replicate-mcp` | Replicate API |
| openai-images-mcp | GPT-Image / DALL-E 3 | `npm i -g openai-images-mcp` | OpenAI API |
| figma-mcp | Read/write Figma files (official) | `npm i -g @anthropic/figma-mcp` | Figma token |

This skill enhances Sumi when MCP servers are available but does NOT require them. Without MCP servers, Sumi provides detailed specifications and prompts that users can use manually with any generation tool.

---

## 3. Stitch MCP — UI Generation

### Capabilities

Stitch is purpose-built for generating UI screens from natural language descriptions. Unlike general image models, Stitch understands UI primitives: navigation bars, cards, forms, data tables, modals, sidebars. Its output is structured, layouted, and component-aware.

**What Stitch Generates Well:**
- Full page layouts (dashboards, settings, profiles, feeds)
- Component compositions (card grids, form sections, navigation)
- Responsive variations (desktop, tablet, mobile)
- Light and dark mode variants
- Platform-specific UIs (iOS, Android, web)

**What Stitch Does NOT Do Well:**
- Photorealistic imagery (use Fal.ai or DALL-E for hero images)
- Custom illustrations (use Recraft or Midjourney)
- Animated prototypes (use Veo or Runway for motion)
- Pixel-perfect production code (use component-patterns-code skill for code)

### Prompt Patterns for Stitch

**Layout Generation Pattern:**
```
Generate a [platform] [screen type] with:
- Navigation: [nav style + items]
- Layout: [grid/stack/split description]
- Content: [specific data to show]
- Style: [visual direction — reference product or design tokens]
- State: [default/loading/empty/error]
```

**Component Generation Pattern:**
```
Generate a [component name] component that:
- Contains: [child elements]
- Shows: [specific data]
- Supports: [interactions — hover, selected, disabled]
- Follows: [design system reference]
```

**Full Page Generation Pattern:**
```
Generate a complete [product type] [page name]:
- Header: [logo + nav items + user menu]
- Hero: [headline + subtext + CTA + visual]
- Section 1: [feature grid — 3 columns, icon + title + description]
- Section 2: [testimonials — carousel or grid]
- Section 3: [pricing — 3 tier cards with highlighted recommended]
- Footer: [links + social + newsletter signup]
Style: [reference product], [color palette], [typography]
```

### Iteration Workflow with Stitch

**Round 1 — Broad Exploration:** Generate 3-4 variations with different layout approaches. Use general descriptions. Goal: find the right structural direction.

**Round 2 — Refinement:** Take the best layout and add specificity. Add exact content, adjust spacing descriptions, specify component variants. Goal: nail the composition.

**Round 3 — Polish:** Fine-tune typography descriptions, color references, spacing, and state variants. Generate light and dark modes. Goal: production-adjacent fidelity.

**Round 4 — Variants:** Generate the same screen for different breakpoints, different data states (empty, loading, error, populated), and edge cases (long text, missing images). Goal: completeness.

---

## 4. Image Generation Tools

### Fal.ai — The Multi-Model Platform

Fal.ai provides access to 600+ models through a single API, making it the most versatile generation platform available. Key models for design work:

**FLUX Pro / FLUX.1 Dev:**
- Best for: High-fidelity UI mockup screenshots, product photography, realistic renders
- Strengths: Exceptional text rendering in images, photorealistic quality, fast generation
- Resolution: Up to 2048x2048, supports custom aspect ratios
- Prompt style: Descriptive, natural language, responds well to camera/lighting terminology
- Use case: Hero images, product shots, lifestyle imagery for landing pages

**FLUX Schnell:**
- Best for: Rapid iteration, concept exploration, batch generation
- Strengths: 4x faster than FLUX Pro, good quality for drafts
- Use case: Quick visual explorations before committing to high-fidelity generation

**Imagen 4 (via Fal):**
- Best for: Photorealistic imagery with precise prompt adherence
- Strengths: Superior text rendering, excellent at following complex compositional prompts
- Use case: Marketing materials, product mockups, banner images

**Configuration for UI Asset Generation:**
```
Model: flux-pro (high fidelity) or flux-schnell (speed)
Resolution: Match target — 1440x900 for desktop hero, 390x844 for mobile, 1200x630 for OG image
Steps: 28-50 for Pro, 4 for Schnell
Guidance: 3.5-7.5 (higher = more prompt adherence, lower = more creative latitude)
```

### Recraft V3 — Vector and Icon Generation

Recraft V3 is the only AI model capable of generating true SVG/vector output. This makes it indispensable for icon generation, logo exploration, and scalable illustrations.

**Vector Generation Capabilities:**
- SVG output — real vector paths, not rasterized images saved as SVG
- Consistent style across batch generations
- Icon sets with unified weight, style, and grid alignment
- Illustration styles: flat, line art, isometric, hand-drawn, geometric

**Icon Generation Best Practices:**
```
Prompt structure: "[icon subject] icon, [style], [weight], [grid], [color]"
Example: "Shopping cart icon, line style, 2px stroke, 24x24 grid, single color #1A1A2E"
Batch: Generate full sets by varying only the subject while keeping style tokens identical
```

**Illustration Style Presets:**
- **Corporate flat:** "flat vector illustration, geometric shapes, limited palette, no outlines, modern SaaS style"
- **Line art:** "continuous line illustration, single stroke weight, minimal detail, elegant, editorial"
- **Isometric:** "isometric 3D illustration, flat shading, consistent 30-degree angle, pastel palette"
- **Hand-drawn:** "hand-drawn sketch illustration, imperfect lines, warm, approachable, ink on paper feel"

**Brand Consistency Technique:**
To maintain brand consistency across multiple Recraft generations, anchor every prompt with the same style suffix:
```
Style anchor: ", [brand] style, [primary color] and [secondary color] palette, [illustration style], [line weight], consistent with previous generations"
```

### Midjourney — High-Impact Visuals

Midjourney excels at generating visually striking imagery for hero sections, editorial illustrations, and marketing materials. It is not ideal for precise UI generation but unmatched for visual impact.

**Prompt Structure for UI/UX Work:**
```
[Subject description] --ar [aspect ratio] --style [raw/aesthetic] --stylize [0-1000] --v 6.1
```

**Key Parameters:**
- `--ar 16:9` — Desktop hero images
- `--ar 9:16` — Mobile hero images, app store screenshots
- `--ar 1:1` — Avatars, thumbnails, social media
- `--ar 3:2` — Blog post headers, card images
- `--style raw` — More literal prompt interpretation, better for specific UI needs
- `--stylize 50-150` — Lower values for more control, higher for more artistic flair
- `--no text, UI elements, buttons` — Negative prompts to avoid unwanted elements

**Best Use Cases in Design:**
- Hero section background imagery
- Editorial and blog illustrations
- Conceptual mood board imagery
- Abstract background patterns and textures
- Product lifestyle photography concepts
- Marketing campaign visuals

**Prompt Examples for Common Design Needs:**
```
Hero image: "Abstract gradient mesh, deep navy transitioning to electric violet, subtle grain texture, premium SaaS aesthetic --ar 16:9 --style raw --stylize 100"

Illustration: "Isometric workspace with laptop, coffee cup, and plant, soft pastel palette, minimal geometric style --ar 3:2 --stylize 200"

Background: "Subtle topographic line pattern, light grey on white, barely visible, clean minimal texture --ar 16:9 --style raw --stylize 50 --no color"
```

### DALL-E 3 — Concept Art and Exploration

DALL-E 3 (via OpenAI) has strong prompt comprehension and excels at conceptual exploration, but produces softer, more painterly results than FLUX or Midjourney.

**Strengths:**
- Excellent text comprehension — understands complex, multi-part prompts
- Good at conceptual and metaphorical imagery
- Reliable text rendering within images
- Accessible via direct API (no Discord, no queue)
- Integrated editing capabilities (inpainting, outpainting)

**Limitations for UI Work:**
- Output tends toward illustrated/painterly rather than photorealistic
- Less control over exact style compared to Midjourney
- Resolution limited to 1024x1024, 1024x1792, or 1792x1024
- Cannot match the precision of Stitch for UI layouts
- No vector output capability

**Best Use Cases:**
- Early concept exploration (before committing to a style direction)
- Metaphorical illustrations for blog posts and marketing
- Placeholder imagery during wireframing
- Quick visual brainstorming during design workshops
- Social media graphics and promotional imagery

---

## 5. Video Generation

### Veo 3.1 (Google, via Fal.ai)

Veo 3.1 generates high-quality video clips from text prompts, useful for prototype animations, product demos, and marketing content.

**Design Applications:**
- Animated hero sections (looping background videos)
- Product walkthrough animations
- Micro-interaction previews at scale
- Social media video ads and promotional clips
- App store preview videos (conceptual)

**Prompt Pattern:**
```
"Smooth UI animation showing [interaction]: [starting state] transitions to [ending state],
[platform] design style, [duration] seconds, [camera movement], clean background, 60fps"
```

### Runway Gen-3 Alpha

Runway specializes in creative video generation with strong artistic control.

**Best For:**
- Stylized product videos with artistic flair
- Brand videos with specific mood and aesthetic
- Motion graphics concepts
- Cinematic product reveals

**Key Features:**
- Image-to-video (animate a static mockup)
- Motion brush (control where movement happens)
- Style reference (maintain visual consistency)

### Pika

Pika focuses on quick, accessible video generation with simple controls.

**Best For:**
- Rapid prototype animation concepts
- Simple motion mockups for client presentations
- Social media short-form content
- Quick iteration on animation direction

**When to Use Which Video Tool:**
| Need | Tool | Why |
|------|------|-----|
| Photorealistic product demo | Veo 3.1 | Best realism, longest clips |
| Artistic brand video | Runway Gen-3 | Best creative control |
| Quick motion concept | Pika | Fastest, simplest |
| UI animation reference | Veo 3.1 | Understands UI context |

---

## 6. Prompt Engineering for Design

### UI Screenshot Prompts

The most common generation task is producing high-fidelity UI screenshots for mockups, presentations, and client approvals. Structure prompts in layers:

**Layer 1 — Style Foundation:**
```
"Modern SaaS dashboard, clean and minimal, Stripe/Linear aesthetic"
```

**Layer 2 — Layout Structure:**
```
"Left sidebar navigation (64px, dark), top header bar (56px, white),
main content area with 3-column card grid"
```

**Layer 3 — Content Specifics:**
```
"Cards show: metric title, large number, sparkline chart, percentage change badge.
Metrics: Revenue ($48,230, +12.3%), Users (12,847, +5.7%), Conversion (3.24%, -0.8%)"
```

**Layer 4 — Visual Details:**
```
"Inter font family, 14px body text, #1A1A2E text color, #F8F9FA background,
8px border radius, subtle box shadows (0 1px 3px rgba(0,0,0,0.08)),
16px grid spacing"
```

**Layer 5 — Quality Modifiers:**
```
"4K resolution, pixel-perfect, production-ready, Retina display,
anti-aliased text, proper kerning"
```

**Complete Assembled Prompt:**
Combine all layers into a single coherent prompt. The model processes the full context — layering ensures you do not forget critical details.

### Icon Generation Prompts

Consistent icon sets require rigid prompt structure. Vary only the subject; keep everything else identical.

**Template:**
```
"[Subject] icon, [style] style, [stroke weight] stroke, [size] grid,
[corner radius] corners, [color/monochrome], [fill/outline],
consistent with [reference set], centered, balanced negative space"
```

**Batch Generation Strategy:**
1. Generate one "anchor" icon (the most complex subject in your set)
2. Use that anchor as a style reference for all subsequent icons
3. Generate in groups of 4-6 to maintain session consistency
4. Review the full set together, regenerate outliers

**Common Icon Sets for Products:**
- Navigation: home, search, notifications, settings, profile, menu, back, close
- Actions: add, edit, delete, share, download, upload, copy, paste
- Status: success, warning, error, info, loading, empty, locked, unlocked
- Commerce: cart, payment, shipping, receipt, refund, wishlist, coupon, gift

### Illustration Prompts

Illustrations need style consistency across a product. Define a style system before generating.

**Style System Definition:**
```
Style: [flat/line/isometric/3D/hand-drawn]
Palette: [3-5 specific colors with hex values]
Line weight: [none/thin/medium/bold + specific px]
Shapes: [geometric/organic/mixed]
Characters: [if applicable — style, proportions, features]
Mood: [professional/playful/technical/warm/minimal]
```

**Apply the Style System to Every Prompt:**
```
"[Scene description], [style system reference],
[specific palette colors], [line weight], [mood],
consistent illustration style, flat vector, no gradients"
```

### Landing Page Prompts — Section by Section

Generate landing pages one section at a time for maximum control, then composite.

**Hero Section:**
```
"Landing page hero section: bold headline '[Headline Text]' in [font],
subheadline '[Subtext]', primary CTA button '[Button Text]' in [color],
[visual element: product screenshot / illustration / abstract shape],
[background treatment], above-the-fold, desktop 1440px width"
```

**Features Section:**
```
"Features grid section: 3 columns, each with [icon style] icon,
feature title, 2-line description, [card/flat/bordered] treatment,
[background color], consistent spacing, desktop 1440px width"
```

**Social Proof Section:**
```
"Testimonial section: [carousel/grid/single-quote] layout,
customer photo, name, title, company logo, quote text,
star rating, [card/minimal/bordered] treatment"
```

**Pricing Section:**
```
"Pricing comparison: [2/3/4] tier cards, highlighted recommended tier,
plan name, price, billing period, feature list with check/x marks,
CTA button per tier, [flat/elevated/bordered] card style"
```

---

## 7. Generation Pipelines

### Concept to Production Workflow

**Stage 1 — Concept Exploration (Breadth):**
- Tool: FLUX Schnell or DALL-E 3 (fast, cheap)
- Goal: 10-20 rough concepts exploring different directions
- Prompt style: Loose, descriptive, varied
- Evaluation: Which direction feels right? Which matches the brief?
- Output: 2-3 selected directions to pursue

**Stage 2 — Variation (Depth):**
- Tool: FLUX Pro or Midjourney (higher quality)
- Goal: 4-6 variations of each selected direction
- Prompt style: Specific, detailed, building on Stage 1 selections
- Evaluation: Score against brand, usability, aesthetics criteria
- Output: 1-2 strong candidates per direction

**Stage 3 — Refinement (Precision):**
- Tool: Best tool for the specific asset type
- Goal: Polish the selected candidates to near-production quality
- Prompt style: Highly specific, include exact measurements, colors, content
- Evaluation: Would this pass a design review? Does it meet the brief?
- Output: Final generated assets ready for post-processing

**Stage 4 — Production (Integration):**
- Post-process: Upscale, color correct, extract assets
- Integrate: Import to Figma, generate code, add to design system
- Validate: Final quality check against production requirements
- Deliver: Export in all required formats and resolutions

### Batch Asset Generation

When generating asset sets (icon packs, illustration libraries, photo collections), consistency is paramount.

**Icon Set Pipeline:**
1. Define style guide: stroke weight, grid size, corner radius, color mode
2. List all icons needed (typically 20-60 for a product)
3. Generate anchor icon (most complex subject)
4. Generate in batches of 6, using anchor as style reference
5. Review batch cohesion — regenerate outliers
6. Export all as SVG (via Recraft) at target grid sizes (16, 20, 24, 32, 48)
7. Validate: consistent weight, alignment, visual density across set

**Illustration Set Pipeline:**
1. Define illustration style system (palette, style, mood, characters)
2. List all scenes needed
3. Generate hero illustration first (most complex, sets the bar)
4. Generate supporting illustrations in priority order
5. Review as a collection — adjust any that break consistency
6. Export at required resolutions with transparent backgrounds where needed

### Design System Asset Generation

Generate foundational design system assets in a coordinated pipeline:

1. **Color palette visualization** — Generate color swatches with labels, accessibility contrast pairs
2. **Typography specimens** — Generate type scale samples at all sizes with real content
3. **Component previews** — Generate each component in all states (default, hover, active, disabled, error)
4. **Page templates** — Generate common page layouts using the component library
5. **Dark mode variants** — Regenerate key screens and components in dark mode

---

## 8. Quality Control

### AI Artifact Detection

AI-generated designs contain telltale artifacts that must be caught before production use:

- **Text garbling:** Fake or misspelled text in generated UI screenshots. Always replace with real copy.
- **Inconsistent spacing:** AI may vary padding/margin subtly between similar elements. Normalize in post.
- **Phantom UI elements:** Buttons that lead nowhere, icons that mean nothing. Verify every element has purpose.
- **Style drift:** Across multiple generations, subtle style inconsistencies accumulate. Compare side by side.
- **Anatomical errors:** In illustrations with people, check hands, fingers, eyes, proportions.
- **Brand contamination:** Models may inject elements from training data (wrong logos, competitor patterns).
- **Resolution artifacts:** Soft edges, aliasing, blurry text at small sizes. Regenerate or upscale.

### Consistency Checking

For multi-screen or multi-asset projects, run a consistency audit:

**Cross-Screen Consistency Checklist:**
- [ ] Same typography scale across all screens
- [ ] Identical color usage for same-meaning elements
- [ ] Consistent spacing rhythm (base unit and multiples)
- [ ] Matching border-radius on same-level components
- [ ] Unified shadow/elevation system
- [ ] Same icon style and weight throughout
- [ ] Consistent navigation placement and behavior
- [ ] Matching state treatments (hover, active, disabled)

### Brand Compliance Scoring

Score generated designs against brand requirements on a 0-10 scale:

| Dimension | 0-3 (Fail) | 4-6 (Partial) | 7-10 (Pass) |
|-----------|-----------|---------------|-------------|
| Color accuracy | Wrong palette | Approximate colors | Exact brand colors |
| Typography | Wrong fonts | Right family, wrong weights | Exact type system |
| Spacing | Inconsistent | Mostly consistent | Matches grid system |
| Tone/mood | Off-brand | Close but not quite | Nails brand personality |
| Component fidelity | Unrecognizable | Similar structure | Matches design system |
| Content quality | Placeholder lorem | Generic realistic | Brand-voice copy |
| Platform correctness | Wrong OS patterns | Mixed platform cues | Native platform feel |

**Minimum viable score for production use: 7+ average across all dimensions.**

---

## 9. Asset Post-Processing

### Upscaling

AI outputs often need resolution increases for production use:

- **Real-ESRGAN** — Best general-purpose upscaler, 4x without significant artifacts
- **Topaz Gigapixel** — Commercial, best for photographic content
- **Waifu2x** — Best for illustrated/anime-style content
- **Fal.ai upscale models** — Accessible via the same MCP server, no separate tool needed

**When to Upscale:**
- Source is below target resolution (e.g., 1024px generated, need 2880px for Retina)
- Generating at lower resolution was faster/cheaper and upscaling is acceptable quality

### Background Removal

For assets that need transparency:
- **remove.bg API** — Best automated option for photographs
- **Recraft V3** — Can generate with transparent backgrounds directly (SVG)
- **Fal.ai background removal models** — Accessible via MCP
- Manual: Use Figma or image editor for complex cases

### SVG Tracing

Convert raster icons/illustrations to true vector:
- **Recraft V3** — Generate as vector from the start (preferred)
- **Vectorizer.ai** — AI-powered raster-to-vector conversion
- **Potrace** — Open-source, good for simple shapes
- Manual: Redraw in Figma using raster as reference (highest quality)

### Color Correction

AI models do not guarantee exact color values. Post-process to match brand:
- Extract the dominant palette from generated output
- Map each color to nearest brand color
- Apply correction globally (Figma color adjustment, CSS filters, or image editor)
- Verify contrast ratios remain WCAG AA compliant after correction

---

## 10. Integration with Design Tools

### Figma Import

Generated assets flow into Figma for refinement and handoff:

1. **Direct import:** Drag generated images into Figma frames
2. **Figma MCP:** Use the official Figma MCP server to programmatically place assets
3. **Auto Layout conversion:** Use generated screenshots as reference to rebuild with Figma Auto Layout
4. **Component extraction:** Identify reusable components in generated screens, rebuild as Figma components
5. **Token application:** Replace AI-approximated styles with actual design tokens

**Figma MCP Workflow:**
```
1. Generate screen via Stitch or image model
2. Read target Figma file via Figma MCP
3. Create a new frame in the target page
4. Place generated image as fill or reference layer
5. Build component structure on top of reference
6. Remove reference layer when component build is complete
```

### Code Generation from AI Mockups

AI mockups serve as visual specifications for code generation:

1. Generate high-fidelity mockup with all states
2. Extract design tokens from the mockup (colors, spacing, typography)
3. Map to existing design system components where possible
4. Use the `component-patterns-code` skill to generate React/SwiftUI/CSS
5. Compare rendered code output against the AI mockup for fidelity
6. Iterate on code until visual match is achieved

---

## 11. Ethical Considerations

### Attribution

- AI-generated assets should be disclosed to clients when they form a significant part of deliverables
- Internal team use (concept exploration, wireframing) typically does not require disclosure
- Portfolio use: clearly label AI-generated vs. hand-crafted work
- Commercial use: verify the generation tool's license permits commercial usage of outputs

### Bias in Generated Designs

AI models inherit biases from training data. Watch for:
- **Representation bias:** Generated people may skew toward certain demographics. Actively prompt for diversity.
- **Cultural bias:** "Modern design" defaults to Western/Silicon Valley aesthetics. Specify cultural context explicitly.
- **Accessibility bias:** Generated designs rarely meet WCAG standards by default. Always audit.
- **Gender/age bias:** Stock-photo-like generations default to narrow demographic ranges. Be explicit.

**Mitigation Strategies:**
- Include demographic diversity in prompts when generating imagery with people
- Cross-reference with the `cross-cultural-i18n-ux` skill for cultural appropriateness
- Run accessibility checks on all generated designs using the `accessibility-inclusive-design` skill
- Build diverse representation requirements into your generation brief

### Client Disclosure

Recommended disclosure framework:
- **Concept phase:** No disclosure needed — AI is one of many exploration tools
- **Design phase:** Disclose if AI generation forms the basis of presented designs
- **Production phase:** Disclose if final shipped assets are AI-generated (not just AI-assisted)
- **Always disclose** if the client's contract or industry regulations require it

---

## 12. Cost Optimization

### When to Use Which Model

| Need | Cheapest Option | Best Quality Option | Recommended |
|------|----------------|-------------------|-------------|
| UI mockup screenshot | Stitch | Stitch | Stitch |
| Product icon (SVG) | Recraft V3 | Recraft V3 | Recraft V3 |
| Hero photograph | FLUX Schnell | FLUX Pro / Imagen 4 | FLUX Pro |
| Editorial illustration | DALL-E 3 | Midjourney | Midjourney |
| Background pattern | FLUX Schnell | FLUX Pro | FLUX Schnell |
| Video clip | Pika | Veo 3.1 | Veo 3.1 |
| Concept exploration | FLUX Schnell | FLUX Pro | FLUX Schnell |
| Client presentation | FLUX Pro | Midjourney | FLUX Pro |

### Batch Strategies

- **Generate at low resolution first**, then upscale only the selected outputs
- **Use fast models for exploration** (FLUX Schnell, DALL-E 3), premium models for finals
- **Cache successful prompts** — save prompts that produced good results for reuse on similar projects
- **Reuse style anchors** — generate one high-quality reference, then use it to guide cheaper subsequent generations
- **Bundle similar requests** — generate icon sets in one session rather than one-at-a-time over days

### Cost Per Asset Estimates

| Asset Type | Low Estimate | High Estimate | Typical |
|------------|-------------|---------------|---------|
| UI screen mockup | $0.02 | $0.15 | $0.05 |
| Icon (SVG) | $0.01 | $0.05 | $0.02 |
| Hero image | $0.03 | $0.20 | $0.08 |
| Illustration | $0.03 | $0.20 | $0.10 |
| Video clip (5s) | $0.10 | $1.00 | $0.30 |
| Full page (5 sections) | $0.10 | $0.50 | $0.25 |

*Costs vary by model, resolution, and number of iterations. Estimates assume 2-3 generation rounds per final asset.*

---

## Reference Architecture

| File | Contents | Use When |
|------|----------|----------|
| `references/mcp-design-tools.md` | Complete catalog of MCP servers for design generation: Stitch (UI screens from text), Fal.ai (600+ models — Imagen 4, FLUX Pro, Veo 3.1, Recraft V3), Replicate (open-source models), OpenAI GPT-Image, Figma MCP (official). Per tool: capabilities, MCP configuration, tool names, parameters, pricing, strengths, limitations, best use cases. | Selecting the right MCP tool for a task. Configuring MCP servers. Understanding tool capabilities and limitations. |
| `references/prompt-engineering-visual.md` | How to write effective prompts for UI design generation. Prompt anatomy for each tool (Stitch, Imagen, FLUX, DALL-E). Style transfer techniques. Design token injection into prompts. Sector-aware prompting. Platform-specific prompting (iOS, Android, web). Negative prompting. Prompt templates for common UI screens. | Crafting effective generation prompts. Converting design specifications into tool-specific prompts. Ensuring generated output matches design direction. |
| `references/generation-pipelines.md` | Multi-step generation workflows: text to wireframe to high-fidelity to code. Single-tool pipelines vs. multi-tool pipelines. Iterative refinement loops. Design system consistency across multiple generations. Batch generation for screen families. Pipeline templates for common scenarios (landing page, dashboard, mobile app, design system). | Running multi-step generation workflows. Ensuring consistency across multiple generated screens. Planning generation projects. |
| `references/asset-generation-guide.md` | Generating design assets: icons (SVG via Recraft V3 — the only vector-capable model), illustrations (Fal.ai, DALL-E), photographs (Imagen 4, FLUX), video/motion (Veo 3.1), patterns/textures, brand assets. Per asset type: best tool, prompt strategy, output format, quality requirements, production-readiness checklist. | Generating specific design assets. Choosing the right tool for icons vs. illustrations vs. photos vs. video. |
| `references/quality-control-generation.md` | Scoring generated designs against the visual-design-mastery framework. Automated quality checks. Human-in-the-loop review process. Iteration strategies (what to change in prompts when output is poor). Common generation failures and fixes. When to stop iterating and hand-craft instead. | Evaluating AI-generated output quality. Deciding whether to iterate, change tools, or hand-craft. Quality gates for generated designs. |

## Cross-References

- **`visual-design-mastery`** — Provides the design intelligence that makes generation prompts effective and quality scoring meaningful.
- **`platform-visual-standards`** — Provides platform-specific constraints for generation prompts.
- **`ui-pattern-intelligence`** — Identifies which patterns to generate and their quality benchmarks.
- **`sector-style-intelligence`** — Provides sector-specific visual direction for generation prompts.
- **`design-systems-architecture`** — Ensures generated designs consume design tokens consistently.
- **`figma-design-tool-workflows`** — Integration with Figma for design-to-code pipelines.
- **`icon-illustration-systems`** — Detailed icon and illustration design guidance that informs generation prompts.
- **`color-palette-library`** — Curated palettes for color-accurate generation prompts.
- **`typography-pairing-recipes`** — Type system knowledge for typography-aware generation.
- **`animation-recipe-library`** — Motion design knowledge for video generation prompts.

## Commands Powered by This Skill

| Command | How This Skill Is Used |
|---------|----------------------|
| `/generate` | Primary command — AI-powered screen generation via MCP tools |
| `/generate` | AI-powered asset generation (icons, illustrations, photos, video) |
| `/grade` | Can generate mood board visualizations using image generation |
| `/screen` | Can use Stitch to generate screen mockups before coding |
| `/component` | Can reference generated designs as implementation targets |
