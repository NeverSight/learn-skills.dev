---
name: thumbnail-generator
description: Generate cinematic AI image prompts for YouTube thumbnails, LinkedIn posts, and social media visuals in Dhruv's signature style. Use when user asks for a thumbnail, image prompt, social media visual, cover image, or any AI-generated image for content.
---

# Thumbnail & Image Prompt Generator

## Goal
Generate mind-blowing, cinematic AI image prompts that produce thumbnails and visuals indistinguishable from Hollywood production stills. Every prompt follows Dhruv's proven visual identity and uses advanced prompt engineering techniques from Midjourney V7, Ideogram V3, and fal.ai research.

## THE GOLDEN RULE — Realistic Base + Futuristic Overlay

The best thumbnails look like a **real photograph** with **futuristic elements layered on top**. NOT full CGI. NOT over-processed AI art.

**What works (the mix):**
- Real wooden desk / natural workspace (warm brown tones) — NOT sterile sci-fi
- Natural skin tones, real lighting on face — NOT plastic AI skin
- Real MacBook Pro screen showing actual app UI — NOT glowing abstract screens
- THEN overlay: neon glow accents, floating holographic icons, frosted glass panels, glowing connection lines
- Subtle volumetric fog/haze — NOT drowning in effects

**Think:** iPhone photo in a real room → add holographic floating elements in post-production

## GOLD STANDARD — The Conversa AI Thumbnail (Best Result)

This is the reference image ALL future thumbnails should match in quality and composition:

**What made it the best:**
- **Clean layout** — not messy, elements organized in zones (left = tech badges, center = person + laptop, right = app UI)
- **Tech stack as vertical badge list on LEFT** — Next.js, FastAPI, MongoDB, Redis, AWS as clean pill-shaped labels stacked vertically
- **MacBook showing REAL app UI** — actual chat interface with file upload visible, GPT-4o Vision label, conversation bubbles
- **Frosted glass panels with teal/gunmetal silver-blue neon border** — cool metallic glow on panel edges (NOT pink/purple — use teal + gunmetal silver)
- **Developer working at laptop** — natural pose, typing, not staring at camera. Confident but natural
- **Warm dark room** — bookshelf/plants blurred behind, desk lamp warmth, NOT pure black void
- **Teal/metallic silver-blue neon glow ONLY on the floating UI panels** — room itself stays warm and natural
- **Small code card bottom-right** — frosted glass showing "Python" snippet for credibility
- **NOT overcrowded** — breathing room between elements, clean composition

**The prompt that produced this winner:**
```
Photorealistic DSLR-quality photo. Young Indian male developer with short hair, trimmed beard, and glasses, wearing a plain black t-shirt, sitting at a natural wooden desk working on a MacBook Pro. The laptop screen shows a dark-themed AI chat interface with GPT-4o Vision, file upload area showing PDF, DOCX, image options, and conversation bubbles. On the left side, clean vertical badge-style labels: Next.js, FastAPI, MongoDB, Redis, AWS — stacked neatly with colored brand icons. Floating beside him: frosted glass panels with teal and gunmetal silver-blue neon glow borders showing chat interface previews and a small Python code snippet card. Dark moody room with warm ambient light, bookshelf with plants softly blurred in background. Natural skin tones, warm room lighting with teal and metallic silver-blue neon accents only from the floating panels. Clean composition with breathing room between elements. Photorealistic, 8K, sharp focus, shallow depth of field, DSLR quality, 16:9 YouTube thumbnail ratio.
```

**Composition rule from this winner:**
```
LEFT zone:    Tech stack badges (vertical list, clean pills with brand colors)
CENTER zone:  Developer + MacBook Pro (the anchor, largest element)
RIGHT zone:   Floating app UI previews (frosted glass + neon border)
BOTTOM:       Small credibility element (code snippet, terminal card)
TOP:          Open space for text overlay
```

## CRITICAL RULES — NEVER BREAK THESE

1. **ALWAYS plain black t-shirt** — NEVER hoodie, jacket, suit, or anything else
2. **ALWAYS realistic base** — real room, natural wooden desk, warm ambient light, natural skin tones
3. **ALWAYS MacBook Pro** with actual app/terminal visible on screen
4. **ALWAYS include specific details** — real app names, real numbers, real tools
5. **Futuristic elements are OVERLAYS** — floating icons, neon glow lines, holographic panels are added ON TOP of the realistic base
6. **NEVER full CGI/sci-fi** — must feel like a real photograph first, futuristic second
7. **NEVER over-process** — 70% realistic photography, 30% futuristic elements
8. **ALWAYS include quality modifiers** — 8K, sharp focus, photorealistic, natural lighting

## Dhruv's Visual Identity (Locked)

```
Subject:     Young Indian male developer, short hair, trimmed beard, glasses, plain black t-shirt
Setting:     Real workspace — natural wooden desk, warm ambient room lighting, slightly dark/moody
Background:  Dark room with warm undertones — NOT pure black, NOT bright white
             Subtle bokeh from room lights, plant or shelf visible in soft blur
MacBook:     Real MacBook Pro showing actual app UI or terminal on screen
Pose:        Confident — arms crossed with smirk, focused at laptop, or sleeping (automation)
Skin:        Natural skin tones, realistic lighting on face — NOT plastic/AI-smoothed
Futuristic:  Floating holographic elements, neon glow lines, frosted glass panels — as OVERLAYS
Vibe:        "Real developer in real room, but with superhuman capabilities visible around him"
```

## Color System — Realistic Base + Neon Overlay

### The Room (Realistic — 70% of the image)
```
Desk:        Natural warm wood / brown desk (real, not CGI)
Room:        Dark moody room with warm ambient light (think evening study room)
Ambient:     Warm undertones from room — soft yellow/warm white from desk lamp or monitor glow
Skin:        Natural warm skin tones — realistic face lighting from laptop screen
```

### The Overlay (Futuristic — 30% of the image)
```
DEFAULT:       Teal (#00D4FF) + gunmetal silver-blue (#8BA4B8) — cool, metallic, futuristic
               This is the DEFAULT for all thumbnails. Clean, professional, premium feel.
Purple Neon:   #9B30FF — ONLY for ghost copies / automation / cloning topics
Frosted Glass: Semi-transparent panels with subtle blur + teal/gunmetal edge glow
Green:         Terminal green text on MacBook screen — for credibility/tech feel
```

### When to Use What
- **Teal + gunmetal silver** = DEFAULT for everything (tech, deploy, MCP, APIs, courses, general)
- **Purple glow** = ONLY for ghost copies / automation / cloning / "sleeping while AI works" topics
- **Mix of both** = when topic covers both automation AND tech stack

## Master Prompt Formula

**Layer 1 (Realistic base):** Describe a real photo in a real room
**Layer 2 (Futuristic overlay):** Add floating holographic elements on top

```
[Real photo setup — natural wooden desk, dark room, warm light]. Young Indian male developer with short hair, trimmed beard, and glasses, wearing a plain black t-shirt, [pose]. MacBook Pro open showing [actual UI/terminal]. [THEN the futuristic overlay — floating holographic icons, neon glow connections, frosted glass panels around him]. [Specific details — real app names, numbers, tools]. Natural skin tones, warm room lighting with [purple/teal] neon accents from the floating elements, photorealistic, 8K, sharp focus, [RATIO].
```

### Quality Modifiers (ALWAYS include)
```
photorealistic, 8K, sharp focus, natural skin tones,
professional photography, cinematic color grading, DSLR quality,
shallow depth of field, realistic lighting
```

### Lighting — Two Layers
```
Room layer:    Warm ambient light, laptop screen glow on face, soft shadows, natural
Overlay layer: Subtle neon rim light from floating elements, teal/purple glow on edges only
               NOT drowning the whole scene in neon — just accents
```

### Material Keywords for Floating Elements
```
frosted glass, glassmorphism, semi-transparent, holographic,
neon edge glow, translucent with blur, glowing connection lines
```

**Key insight:** The floating elements EMIT the neon light. The room itself stays warm and natural. The contrast between warm room + cool neon overlays is what makes it look premium.

### Ratios by Platform
| Platform | Ratio | Style |
|----------|-------|-------|
| YouTube thumbnail | 16:9 | Bold, can be complex |
| LinkedIn post | 4:5 | Cleaner, more professional |
| Instagram/Reels cover | 9:16 or 1:1 | Face-forward, minimal |
| Twitter/X header | 3:1 | Wide cinematic |
| Course/Bootcamp banner | 16:9 | Professional + techy |

## 7 Proven Visual Hooks

### 1. Ghost Copies (Automation, AI agents, productivity)
**Palette:** Purple Neon (A)
```
[X] translucent purple ghost copies of himself working simultaneously — one [task 1], one [task 2], one [task 3]. Each ghost has a neon purple glow outline. The real developer [pose] in the center. Holographic glassmorphism UI panels floating near each ghost.
```

### 2. Holographic Command Center (Full-stack, dashboards, multi-tool)
**Palette:** Blue Metallic (B)
```
Surrounded by floating holographic displays showing [specific content]. Frosted glass UI panels with teal and cyan neon glow. Brushed aluminum desk surface reflecting holographic light. Semi-transparent data dashboards layered at different depths.
```

### 3. Pipeline Flow (CI/CD, deployment, workflows)
**Palette:** Blue Metallic (B)
```
Above the laptop, a holographic pipeline showing: "[Step 1] → [Step 2] → [Step 3]" with green checkmarks on each step. Glowing cyan connection lines between stages. Each stage rendered as a frosted glass card with the tool's logo. Chrome connectors between cards.
```

### 4. Before/After Split (Transformation, productivity)
**Palette:** Mixed (red/warm left, blue/cool right)
```
Split image. Left side (warm red tint, stressed): [chaotic scene — multiple tabs, overwhelmed]. Right side (cool teal tint, calm): [clean automated scene — single terminal, everything flowing]. Dramatic frosted glass dividing line in center with neon glow.
```

### 5. USB/Connection Hub (MCP, APIs, integrations)
**Palette:** Blue Metallic (B)
```
Holding a glowing USB cable/connection hub that splits into [X] glowing cyan connections, each plugging into a floating frosted glass icon panel: [service 1], [service 2], [service 3]. Chrome and brushed metal cable connectors. Behind him, massive dark screen showing "[CONCEPT]" in bold neon cyan letters.
```

### 6. Sleeping While Ghosts Work (Passive income, automation running)
**Palette:** Purple Neon (A)
```
Sleeping peacefully at desk with head resting on arms, MacBook Pro open showing terminal with "[script].py running..." in green text. Behind him, [X] translucent purple ghost copies wide awake and working — each operating a different floating holographic screen. Volumetric fog between the ghosts and the sleeping developer.
```

### 7. Floating Tech Logos Orbit (Tech stack showcase, tutorials)
**Palette:** Blue Metallic (B)
```
Sitting at MacBook Pro with confident expression. Floating around him in orbital rings: frosted glass cards each containing a tech logo — [Logo 1], [Logo 2], [Logo 3]. Each card has a subtle cyan neon edge glow. Brushed aluminum ring connecting the orbiting cards. Holographic connection lines between related technologies.
```

## Text Overlay Rules

- **Max 2-4 words** highlighted in yellow or cyan
- **Rest in white** on dark background
- **Keep total text under 6 words** (readable at mobile size)
- **Formula:** `[HOOK WORD] + [NUMBER/RESULT] + [ACTION WORD]`
- **Yellow highlights on:** numbers, results, power words
- **Cyan highlights for:** tech terms, tool names (matches blue metallic palette)

**Proven examples:**
- "1 DEVELOPER, **6x RESULTS**: THE **CLONE EFFECT**!"
- "I BUILT **ChatGPT** IN **ONE PROMPT**"
- "**5 MCP SERVERS** IN **8 DAYS**"
- "FROM **PROMPT** TO **PRODUCTION** IN 1 DAY"
- "**AI IS HERE** — BUILD WORKFLOWS"

## Ready-to-Use Templates

### Template A: Automation / Ghost Effect
```
Cinematic movie still, dark moody workspace. Young Indian male developer with short hair, trimmed beard, and glasses, wearing a plain black t-shirt, [pose]. [X] translucent purple ghost copies of himself working simultaneously — one [task 1], one [task 2], one [task 3]. Each ghost has a neon purple glow outline. Holographic glassmorphism panels floating near each ghost showing [specific screens]. The MacBook Pro screen shows a terminal with green text "[command]". Dark navy background, purple and teal neon ambient lighting, volumetric fog, dramatic rim lighting, cinematic shallow depth of field, 8K, sharp focus, hyperrealistic, Unreal Engine 5 lighting, [RATIO].
```

### Template B: Full-Stack / Deployment (Blue Metallic)
```
Wide-angle cinematic still, futuristic workspace with brushed aluminum and chrome surfaces. Young Indian male developer with short hair, trimmed beard, and glasses, wearing a plain black t-shirt, [pose]. The MacBook Pro screen shows [app interface]. Floating around him: frosted glass UI panels showing [icons/logos] — all connected by glowing cyan arrows flowing into [destination]. Above: a holographic pipeline "[Step 1] → [Step 2] → [Step 3]" with green checkmarks. Small floating tech logos: [stack]. Dark navy background (#0A0A1A), ice blue and teal neon ambient lighting, frosted glass overlays, volumetric lighting with cyan rim glow, brushed metal surfaces, 8K, sharp focus, hyperrealistic, film grain, [RATIO].
```

### Template C: MCP / API / Integrations (Blue Metallic)
```
Cinematic still, dramatic composition. Young Indian male developer with short hair, trimmed beard, and glasses, wearing a plain black t-shirt, holding a glowing cyan USB-style connector that splits into [X] glowing teal connections. Each connection plugs into a floating frosted glass panel containing: [service 1 icon], [service 2 icon], [service 3 icon]. Chrome and brushed aluminum cable connectors. Behind him, massive holographic text "[CONCEPT]" in electric cyan. Dark navy background, ice blue neon rim lighting, volumetric fog, frosted glassmorphism panels at multiple depths, 8K, sharp focus, Unreal Engine 5, hyperrealistic, [RATIO].
```

### Template D: LinkedIn Post (4:5 Vertical — Cleaner)
```
Cinematic portrait, dark moody workspace. Young Indian male developer with short hair, trimmed beard, and glasses, wearing a plain black t-shirt, [pose]. [Core visual hook — simplified for vertical frame, fewer floating elements]. Frosted glass panel behind with subtle data visible through it. Dark navy background, [blue metallic OR purple neon] ambient lighting, rim light from behind, cinematic shallow depth of field, 8K, sharp focus, hyperrealistic, 4:5 ratio.
```

### Template E: Course / Bootcamp Banner (Professional)
```
Wide cinematic still, professional futuristic setting. Young Indian male developer with short hair, trimmed beard, and glasses, wearing a plain black t-shirt, standing confidently with arms crossed. Behind him, massive holographic screen showing [course topic] with glowing node connections and data flows. Floating frosted glass cards around him showing: [tool 1], [tool 2], [tool 3]. Brushed aluminum and chrome accents on desk/podium. Dark navy background, ice blue and teal neon lighting, volumetric light rays from above, frosted glassmorphism overlays, 8K, sharp focus, hyperrealistic, professional photography, 16:9 ratio.
```

## Process (Every Time)

1. **Identify topic** — what's the video/post about?
2. **Pick color palette** — Blue Metallic (B) by default, Purple Neon (A) for automation/clone topics
3. **Pick visual hook** — which of the 7 hooks tells this story best?
4. **Fill in specifics** — real app names, real numbers, real tools, real screens
5. **Add materials** — frosted glass, brushed metal, chrome (blue metallic) or translucent glow (purple)
6. **Add lighting** — rim light + volumetric fog + neon ambient (ALWAYS)
7. **Add quality modifiers** — 8K + sharp focus + hyperrealistic + Unreal Engine 5
8. **Set ratio** — 16:9 YouTube, 4:5 LinkedIn
9. **Suggest text overlay** — max 6 words, 2-3 highlighted
10. **Generate 2-3 options** — different hooks for same topic

## Anti-Patterns (NEVER DO THESE)

- NEVER hoodie, jacket, suit — plain black t-shirt ONLY
- NEVER generic laptop — MacBook Pro ONLY
- NEVER full CGI/sci-fi background — real room with natural wood desk + dark ambient
- NEVER over-process skin — natural skin tones, realistic face lighting
- NEVER drown entire scene in neon — neon comes ONLY from floating elements as accents
- NEVER sterile/clean backgrounds — should feel like a real developer's workspace
- NEVER generic descriptions — specific floating elements with real app names
- NEVER more than 6 words text overlay — mobile readability
- NEVER more than 3 highlighted words
- NEVER make floating elements solid — they must be translucent/holographic/frosted glass
- NEVER forget the warm-cool contrast — warm room + cool neon overlays = the signature

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `topic` | string | Yes | What the video/post is about |
| `platform` | string | Yes | youtube / linkedin / instagram / twitter / course |
| `palette` | string | No | 'blue-metallic' (default) or 'purple-neon' |
| `key_details` | string | No | Specific tools, numbers, results to include |
| `text_overlay` | string | No | Specific text the user wants on the thumbnail |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `prompt` | string | Ready-to-use AI image generation prompt |
| `text_overlay` | string | Suggested bold text for the thumbnail |
| `alt_prompts` | array | 2 alternative prompt options |

### Credentials
None required (text-only skill — generates prompts, not images)

### Composable With
Skills that chain well: `title-variants`, `cross-niche-outliers`, `recreate-thumbnails`, `video-edit`, `nano-banana-images`

### Cost
Free (prompt generation only)
