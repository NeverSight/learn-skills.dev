---
name: "Oracle InfoGenius"
description: "AI Architect-grade visual generation for Oracle Cloud Infrastructure. Research-grounded, technically validated, zero-typo architecture imagery."
version: "2.0.0"
triggers:
  - "oracle infogenius"
  - "oracle architecture image"
  - "oci visual"
  - "oracle diagram image"
  - "ai architect visual"
preferences: "../preferences/oracle-infogenius-preferences.md"
---

# /oracle-infogenius - AI Architect Visual Generation

**Think Like an AI Architect. Visualize Like Oracle. Zero Typos.**

## Mission

Generate **enterprise-grade, technically-validated Oracle Cloud architecture visuals** that meet the standards of a Senior AI Architect. Every image must be:

- **Research-Grounded** - Validated against Oracle documentation via Google Search
- **Technically Accurate** - Correct service names, capabilities (26ai, Command A, Llama 4)
- **Brand-Compliant** - Official Oracle colors (#C74634), typography
- **Zero Text Errors** - Perfect spelling, grammar, no truncation
- **Presentation-Ready** - Professional quality for customer engagements

---

## Default Style: ISOMETRIC

**Isometric 3D is the ONLY recommended style** because:
- Clear layered structure with tier labels on left margin
- True 3D perspective adds depth without visual chaos
- Professional blueprint/technical documentation aesthetic
- Every component readable and properly positioned
- Flow lines show data movement logically
- Suitable for customer presentations AND technical documentation

Other styles available only if explicitly requested.

---

## Quick Start Pipeline

```
RESEARCH → ARCHITECT → COMPOSE → GENERATE → VALIDATE
```

### Step 1: RESEARCH (Always)
```javascript
WebSearch("OCI {service} features capabilities 2026")
```
Validate current service names before generating.

### Step 2: ARCHITECT
- **Audience**: C-Suite / IT Leadership / Technical
- **Style**: ISOMETRIC (default) | executive | technical
- **Layers**: 4 standard tiers

### Step 3: COMPOSE PROMPT (Include Text Quality Block)

**MANDATORY: Include this in EVERY prompt:**
```
TEXT QUALITY REQUIREMENTS (CRITICAL - ZERO TOLERANCE):
- All text must be perfectly spelled with zero typos
- Use complete words only - NEVER truncate (e.g., "Optimizer" not "Optimizr")
- Professional English grammar throughout
- Technical terms must match official Oracle naming exactly
- Font must be clean, readable sans-serif, consistently sized
- Verify all service names against current Oracle documentation
- Double-check every label before rendering
```

Oracle Brand Colors:
- **Primary**: Oracle Red `#C74634`
- **AI/Agents**: Purple `#7B1FA2`
- **Security**: Green `#388E3C`
- **Data**: Orange `#F57C00`
- **Channels**: Blue `#1976D2`

### Step 4: GENERATE
```javascript
mcp__nanobanana__generate_image({
  prompt: "{constructed_prompt_with_text_quality_block}",
  aspect_ratio: "16:9",
  model_tier: "pro",
  enable_grounding: true,    // ALWAYS - validates facts AND text
  thinking_level: "high",
  resolution: "high",
  negative_prompt: "blurry text, typos, misspellings, truncated words, inconsistent fonts, grammar errors, pixelated text, amateur design, wrong technical names"
})
```

### Step 5: VALIDATE
Check BEFORE delivering:
- [ ] All text perfectly spelled (scan every word)
- [ ] All Oracle service names current and correct
- [ ] All model names match official naming
- [ ] Visual follows isometric style
- [ ] Grounding was enabled during generation
- [ ] Font clean and readable at presentation size

---

## Current Oracle Service Catalog (January 2026)

### Database
| Service | Correct Name | NEVER Use |
|---------|--------------|-----------|
| **Oracle AI Database 26ai** | AI Vector Search, HNSW, True Cache | 23ai, 23c |

### Generative AI
| Service | Correct Name | NEVER Use |
|---------|--------------|-----------|
| **OCI Generative AI** | Cohere Command A (256K context) | Command R, Command |
| **OCI Generative AI** | Meta Llama 4 Maverick | Llama 3, Llama 2 |
| **Agent Hub** | OCI Agent Hub (multi-agent orchestration) | just "Agent Hub" |
| **Embeddings** | Cohere Embed 4 | Embed v3 |

### Standard Architecture Layers
1. **DATA INGESTION LAYER** - Sources + OCI Streaming
2. **INTELLIGENCE PLATFORM** - Database + Storage + Cache
3. **AI ORCHESTRATION** - Agent Hub + Specialized Agents
4. **CHANNEL DISTRIBUTION** - Output channels

---

## ISOMETRIC Template (Default)

```
Create a 16:9 isometric 3D technical architecture diagram for "{TOPIC}".

TEXT QUALITY REQUIREMENTS (CRITICAL - ZERO TOLERANCE):
- All text must be perfectly spelled with zero typos
- Use complete words only - NEVER truncate (e.g., "Optimizer" not "Optimizr")
- Professional English grammar throughout
- Technical terms must match official Oracle naming exactly
- Font must be clean, readable sans-serif, consistently sized
- Double-check every label before rendering

VISUAL STYLE:
- True isometric 3D perspective (30-degree angles)
- Clean white/light gray background
- Tier labels on LEFT MARGIN (vertical text): "DATA INGESTION LAYER", "INTELLIGENCE PLATFORM", "AI ORCHESTRATION", "CHANNEL DISTRIBUTION"
- Professional blueprint/technical documentation aesthetic

ORACLE BRANDING:
- Oracle Red (#C74634) 3D blocks for OCI services
- Purple (#7B1FA2) blocks for AI components
- Blue (#1976D2) blocks for output channels
- Orange (#F57C00) blocks for data sources
- "ORACLE" logo prominent at top
- Soft drop shadows on white background

ARCHITECTURE TIERS:
[Specify your 4-tier architecture here]

COMPOSITION:
- Isometric 3D blocks with consistent depth and shadows
- Connecting pipes/tubes showing data flow between tiers
- Clear readable labels on EVERY component
- Flow direction: top-to-bottom or left-to-right
```

---

## Executive Template (On Request Only)

```
Create a 16:9 professional executive-style architecture infographic for "{TOPIC}".

TEXT QUALITY REQUIREMENTS (CRITICAL - ZERO TOLERANCE):
- All text must be perfectly spelled with zero typos
- Use complete words only - NEVER truncate
- Professional English grammar throughout
- Technical terms must match official Oracle naming exactly
- Font must be clean, readable sans-serif, consistently sized

VISUAL STYLE:
- Clean white background
- Minimal design, maximum clarity
- Large readable fonts (minimum 14pt equivalent)
- 4 horizontal layers maximum

ORACLE BRANDING:
- Oracle Red (#C74634) for headers, borders, key services
- Oracle Black (#312D2A) for body text
- White background (#FFFFFF)
- "ORACLE" logo badge in top-right

COMPOSITION:
- Clean horizontal layers with clear separation
- Large service icons with bold labels
- Directional flow arrows
- Bottom metrics bar with key KPIs
```

---

## Negative Prompt (Always Include)

```
blurry text, typos, misspellings, truncated words, inconsistent fonts,
grammar errors, pixelated text, amateur design, flat 2D (for isometric),
low detail, wrong technical names, outdated service names, chaotic layout,
hard to read labels, incomplete words
```

---

## Output Directory

```
/mnt/c/Users/Frank/oracle-work/projects/deliverables/images/
```

---

## Example Invocations

```bash
# Default isometric style (recommended)
/oracle-infogenius "RAG Platform on OCI"

# Isometric explicitly
/oracle-infogenius "Multi-Agent Marketing Automation" --style isometric

# Executive only if specifically needed
/oracle-infogenius "Board Presentation Architecture" --style executive
```

---

## Rejected Styles

| Style | Reason | Status |
|-------|--------|--------|
| Futuristic/Neon | Too chaotic, prioritizes "cool" over "useful" | NOT RECOMMENDED |

---

*Oracle InfoGenius v2.0 - Zero Typos. AI Architect Grade.*
