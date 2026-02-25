---
name: ai-creative-strategist
description: "Research-powered creative strategy with visual previews. Use when you need to figure out WHAT to create before creating it. Researches competitors, captures references, generates visual direction previews, and outputs comprehensive briefs. Triggers on: creative strategy, what visuals should I create, creative brief, visual direction. Outputs briefs with actual preview images for feedback."
---

# AI Creative Strategist

**The difference between amateur and professional creative isn't execution—it's strategy.**

This skill researches, strategizes, and **generates visual previews** before full production. You see the direction before committing.

---

## MCP Setup (First Time Only)

These skills use MCP servers for image generation and visual research. If you don't have them installed yet, here's how to set them up.

### Check What's Installed

Ask Claude: "What MCP tools do you have available?"

If you see `glif` or `replicate` tools → you're ready for generation.
If you see `playwright` or `browser_` tools → you're ready for visual research.

### Image Generation (Pick One or Both)

**Option A: Glif** (recommended for beginners)
1. Get your API token at [glif.app](https://glif.app) → Settings → API
2. Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
"glif": {
  "command": "npx",
  "args": ["-y", "@glifxyz/glif-mcp-server@latest"],
  "env": {
    "GLIF_API_TOKEN": "your-token-here"
  }
}
```

**Option B: Replicate** (more models, pay-per-use)
1. Get your API token at [replicate.com](https://replicate.com) → Account → API tokens
2. Add to your Claude Desktop config:

```json
"replicate": {
  "command": "npx",
  "args": ["-y", "replicate-mcp"],
  "env": {
    "REPLICATE_API_TOKEN": "your-token-here"
  }
}
```

### Visual Research (Optional but Recommended)

**Playwright** — captures competitor screenshots for reference
```json
"playwright": {
  "command": "npx",
  "args": ["-y", "@playwright/mcp@latest"]
}
```

### Where's the Config File?

**Claude Desktop (Mac):**
`~/Library/Application Support/Claude/claude_desktop_config.json`

**Claude Desktop (Windows):**
`%APPDATA%\Claude\claude_desktop_config.json`

After editing, restart Claude Desktop to load the new MCPs.

### Claude Code Users

Add to your `~/.claude/settings.json` under `mcpServers`, same format as above.

---

## The Process

```
1. DISCOVER → Diagnose creative needs
2. RESEARCH → Gather competitive intelligence
3. PREVIEW  → Generate visual direction samples ← NEW
4. FEEDBACK → Refine based on what you see
5. BRIEF    → Output comprehensive creative brief
```

---

## When to Use This Skill

**Use when:**
- Starting a new visual campaign or brand
- Launching a product and need visual direction
- Current visuals aren't performing
- Need to differentiate from competitors
- Don't know what style/aesthetic to pursue

**Skip to execution when:**
- You have a clear brief already
- Simple, one-off generations

---

## Phase 1: Discovery

Quick diagnosis before research:

```
## Creative Strategy Intake

**What are we creating for?**
[ ] Product launch
[ ] Brand refresh
[ ] Campaign (ads, social)
[ ] Website/landing page
[ ] Social media presence

**Who is the audience?**
- Primary: _______
- What do they respond to visually?

**Competitors:**
- Direct: _______
- Aspirational brands: _______

**Budget/Volume:**
[ ] Low ($10-50)
[ ] Medium ($50-200)
[ ] High ($200+)
```

---

## Phase 2: Research (MCP-Powered)

### Competitor Visual Analysis (Playwright)

Capture live screenshots as references:

```
1. browser_navigate to competitor site
2. browser_snapshot to find elements
3. browser_take_screenshot for hero, products
4. Analyze: colors, style, lighting, mood
```

### Trend Research (Perplexity)

```
perplexity_research:
  "What are the visual trends for [industry] in 2025?
   - Color palettes
   - Photography styles
   - Overall aesthetic direction"
```

### Competitive Analysis (Firecrawl)

```
firecrawl_scrape competitor sites:
  - Homepage messaging
  - Product positioning
  - Brand voice
```

---

## Phase 3: Visual Direction Previews ⭐ NEW

**Before finalizing the brief, generate actual images to see the direction.**

### Generate 2-3 Direction Options

Based on research, create distinct visual directions:

**Direction A: [Name - e.g., "Premium Minimal"]**
```json
{
  "model_owner": "google",
  "model_name": "nano-banana-pro",
  "input": {
    "prompt": "[Product/concept] with [style A characteristics], [lighting], [mood], professional commercial quality",
    "aspect_ratio": "16:9"
  }
}
```

**Direction B: [Name - e.g., "Bold & Energetic"]**
```json
{
  "model_owner": "google",
  "model_name": "nano-banana-pro",
  "input": {
    "prompt": "[Product/concept] with [style B characteristics], [lighting], [mood], professional commercial quality",
    "aspect_ratio": "16:9"
  }
}
```

**Direction C: [Name - e.g., "Warm Lifestyle"]**
```json
{
  "model_owner": "google",
  "model_name": "nano-banana-pro",
  "input": {
    "prompt": "[Product/concept] with [style C characteristics], [lighting], [mood], professional commercial quality",
    "aspect_ratio": "16:9"
  }
}
```

### Present Visual Options

```markdown
## Visual Direction Previews

Based on research, here are 3 distinct directions:

### Direction A: Premium Minimal
![Preview A](url)
- **Characteristics:** Clean, dark backgrounds, dramatic lighting
- **Mood:** Sophisticated, premium, confident
- **Differentiation:** Stands out from [competitor] with [contrast]

### Direction B: Bold & Energetic
![Preview B](url)
- **Characteristics:** Vibrant colors, dynamic angles, high contrast
- **Mood:** Exciting, modern, disruptive
- **Differentiation:** Opposite of category convention of [typical approach]

### Direction C: Warm Lifestyle
![Preview C](url)
- **Characteristics:** Natural lighting, contextual settings, warm tones
- **Mood:** Approachable, authentic, trustworthy
- **Differentiation:** Human touch vs [competitor's] cold tech feel

---

**Which direction resonates?**
- Pick one to pursue
- Combine elements from multiple
- Request variations on a direction
```

---

## Phase 4: Feedback Loop

Based on visual previews, refine:

```
User: "I like Direction A's lighting but Direction C's warmth"

→ Generate refined preview combining elements:

{
  "prompt": "[Product] with dramatic lighting from Direction A,
   warm color grading from Direction C, [specific adjustments]..."
}

→ Present refined preview
→ Continue iterating until direction is locked
```

**This is the key differentiator:** See actual images, give feedback, refine before committing to full production.

---

## Phase 5: Final Brief

Once direction is approved via previews:

```markdown
# Creative Brief: [Project Name]

## Approved Direction
**Selected:** [Direction name]
**Preview that was approved:** [URL]

## Visual Direction (Validated)

### Mood & Tone
[Based on approved preview]

### Color Direction
- Primary: [extracted from approved preview]
- Secondary: [accents visible in preview]

### Style Characteristics
[What made the approved preview work]

### Prompt Template (Proven)
```
[The exact prompt that generated the approved direction,
ready to scale to other assets]
```

## Asset Requirements

| Asset | Ratio | Notes |
|-------|-------|-------|
| Hero image | 16:9 | [based on preview] |
| Product shots | 1:1 | [same style] |
| Social graphics | 4:5 | [adapted] |

## Model Recommendation
**Nano Banana Pro** for all production (same as previews)

## Budget
- Previews generated: $0.06 (3 × $0.02)
- Production remaining: ~$X for [X assets]

---

**Direction validated. Ready for production.**
→ Route to execution skills
```

---

## Visual Preview Patterns

### Pattern 1: Product Launch

```
Generate previews for:
1. Hero shot (product floating, dramatic)
2. Lifestyle shot (product in context)
3. Abstract/mood shot (brand feeling)

Let user pick which approach for full campaign.
```

### Pattern 2: Brand Refresh

```
Generate previews showing:
1. Evolution of current style
2. Complete departure
3. Competitive differentiation angle

Validate new direction with stakeholders.
```

### Pattern 3: Campaign Creative

```
Generate previews for:
1. Ad creative concept A
2. Ad creative concept B
3. Ad creative concept C

Test different angles before production spend.
```

---

## Research → Preview → Brief Flow

```
┌─────────────────────────────────────────┐
│  1. RESEARCH                            │
│  - Perplexity: Trends                   │
│  - Playwright: Competitor screenshots   │
│  - Firecrawl: Messaging analysis        │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│  2. VISUAL PREVIEWS (Nano Banana Pro)   │
│  - Generate 2-3 direction options       │
│  - Present to user with analysis        │
│  - Gather feedback on what works        │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│  3. ITERATE                             │
│  - Refine based on feedback             │
│  - Generate new previews if needed      │
│  - Lock direction when approved         │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│  4. FINAL BRIEF                         │
│  - Approved preview as reference        │
│  - Proven prompt template               │
│  - Ready for scaled production          │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│  5. EXECUTION (other skills)            │
│  - ai-product-photo                     │
│  - ai-social-graphics                   │
│  - ai-product-video                     │
└─────────────────────────────────────────┘
```

---

## Model for Previews

| Model | Use | Speed | Cost |
|-------|-----|-------|------|
| **Nano Banana Pro** | All previews | ~3min | $0.02 |

**Why Nano Banana Pro for previews:**
- Same quality as production (what you see is what you get)
- Consistent results when scaling approved direction
- Worth the 3min wait for strategic decisions

---

## Example: Full Flow

**User:** "I need visuals for a new AI productivity tool targeting developers"

### Step 1: Research
```
Competitors analyzed: GitHub Copilot, Cursor, Linear
Trend research: Dark mode, minimal, purple/blue palettes
Whitespace found: "Warm + Bold" quadrant underserved
```

### Step 2: Generate Previews

**Direction A: "Dark Sophisticated"**
```
Premium AI interface visualization against dark charcoal gradient,
subtle purple accent lighting, clean minimal composition,
tech startup aesthetic, professional commercial quality
```

**Direction B: "Warm Approachable"**
```
AI productivity concept with warm coral accents on dark background,
soft gradient lighting, friendly but professional feel,
modern developer tool aesthetic, commercial quality
```

**Direction C: "Bold Disruptive"**
```
AI concept with vibrant gradient colors, dynamic composition,
high energy modern design, standing out from typical dev tools,
bold startup aesthetic, commercial quality
```

### Step 3: Present Previews

```markdown
## Visual Direction Previews

### Direction A: Dark Sophisticated
[Image URL]
Aligns with: Linear, Vercel
Differentiation: Premium positioning

### Direction B: Warm Approachable ⭐
[Image URL]
Aligns with: Raycast warmth + Linear sophistication
Differentiation: "Warm" in a cold category

### Direction C: Bold Disruptive
[Image URL]
Differentiation: Maximum contrast to competitors
Risk: May feel less "developer credible"
```

### Step 4: User Feedback

**User:** "I love Direction B - that warmth feels right. Can we try it with more contrast?"

**Generate refined preview:**
```
AI productivity concept with warm coral accents (#FF6B6B) on deep charcoal,
higher contrast dramatic lighting, warm but powerful feel,
sophisticated developer tool aesthetic, commercial quality
```

### Step 5: Lock & Brief

```markdown
# Creative Brief: DevAssist AI

## Approved Direction
**Selected:** Warm Approachable (refined)
**Approved Preview:** [URL]

## Visual Direction
- Warm coral (#FF6B6B) on dark charcoal (#1A1A2E)
- High contrast but warm mood
- "Intelligent warmth" positioning

## Proven Prompt Template
```
[Product/concept] with warm coral accents on deep charcoal,
high contrast dramatic lighting, warm but powerful feel,
sophisticated developer tool aesthetic, commercial quality
```

## Ready for Production
→ Route to ai-product-photo, ai-social-graphics
```

---

## Quality Gate

Before finalizing:

- [ ] Research completed (not assumptions)
- [ ] Visual previews generated (not just descriptions)
- [ ] User feedback incorporated
- [ ] Direction validated with actual images
- [ ] Proven prompt template ready for scaling

---

## Handoff

```markdown
## Creative Strategist Handoff

**Approved Direction Preview:** [URL]
**Proven Prompt Template:** [prompt that worked]

**Research Summary:**
- Competitive landscape: [key insights]
- Differentiation: [why this direction wins]

**Model:** Nano Banana Pro (same as previews)

**Route to:** ai-product-photo / ai-social-graphics / ai-product-video
```
