---
name: geo-studio
description: Master GEO content orchestrator that understands user goals and intelligently routes tasks across specialized GEO skills. Automatically selects the right workflow from strategy and audit to content creation, optimization, and human editing. Use as the default starting point for any GEO-related task including creating GEO content, ranking in AI search, auditing content for AI visibility, building GEO strategies, writing AI-citable articles, or when unsure which specific GEO skill to use.
---

# GEO Content Studio

> Powered by **GEOly AI** (geoly.ai) — one entry point for every GEO content task.

Intelligent orchestration layer that selects and chains the right GEO skills based on your goal.

## How It Works

1. **You describe** what you want to accomplish
2. **Studio classifies** your intent automatically
3. **Studio selects** the right skill sequence
4. **Skills execute** in optimal order
5. **You get** the final deliverable

No need to know which specific skill to call — just describe your goal.

## Intent Recognition

Studio silently classifies requests into 5 paths:

| Intent | Signals | Path |
|--------|---------|------|
| **Discover** | "what should I write", "where to start", "competitor", "strategy" | Research → Strategy |
| **Build** | "create", "write", "generate", "need content" | Create → Optimize → Edit |
| **Fix** | "optimize", "improve", "fix", "audit", "rewrite" | Optimize → Edit |
| **Technical** | "schema", "llms.txt", "structured data", "alt text" | Technical setup |
| **Report** | "report", "summary", "performance", "metrics" | Report |

## Workflow Paths

### Path A: Discover (Start from scratch)

For: No content yet, don't know what to create

```
Step 1: geo-prompt-researcher
        → Find target prompts to rank for
        
Step 2: geo-competitor-scanner (if competitors mentioned)
        → Analyze competitor GEO tactics
        
Step 3: geo-som-strategist (if multi-month plan needed)
        → Build 90-day roadmap
```

### Path B: Build (Create new content)

For: Have a topic, need to create content

```
Step 1: geo-citation-writer
        → Draft in right citation format
        
Step 2: geo-structured-writer
        → Apply headers, FAQ, tables
        
Step 3: geo-human-editor
        → Strip AI patterns, check claims
        
Step 4: geo-schema-gen
        → Generate JSON-LD markup
        
Step 5: geo-multimodal-tagger (if images/video)
        → Optimize media assets
```

### Path C: Fix (Improve existing content)

For: Have content that needs improvement

```
Step 1: geo-human-editor
        → Remove AI feel first
        
Step 2: geo-content-optimizer
        → Apply GEO citation patterns
        
Step 3: geo-structured-writer (if structure weak)
        → Add headers, tables, FAQ
        
Step 4: geo-schema-gen (if no schema)
        → Generate markup
        
Step 5: geo-sentiment-optimizer (brand pages only)
        → Strengthen brand signals
```

### Path D: Technical (Infrastructure)

For: Site setup, schema, llms.txt

```
Step 1: geo-site-audit (if full assessment needed)
        → 29-point site audit
        
Step 2: geo-llms-txt
        → Create/update llms.txt
        
Step 3: geo-schema-gen
        → Generate page schema
        
Step 4: geo-multimodal-tagger (if media issues)
        → Optimize image/video metadata
```

### Path E: Report (Performance)

For: Analyze GEO performance

```
Step 1: geo-report-builder
        → Generate structured report
        → May branch to fix issues found
```

## Chaining Rules

**Rule 1: geo-human-editor is always last for content**
Every content path ends with human editing. Non-negotiable.

**Rule 2: Skip research if topic is known**
If you say "write a 'What is GEO?' article", skip prompt research.

**Rule 3: Don't run full audit for single requests**
If you just need FAQ schema, go directly to schema generation.

**Rule 4: Sentiment optimizer is brand-content only**
Only for homepage, About, product pages — not educational content.

**Rule 5: Ask before competitor scanning**
Requires competitor list — don't assume.

**Rule 6: SOM strategist is for planning sessions**
Only for multi-week roadmaps, not single content pieces.

## Opening Question

When triggered with broad request, Studio asks:

> "What's the starting point — do you have existing content to improve, or are you creating something new?"

This determines Path B (Build) vs Path C (Fix), covering 80% of cases.

## Progress Updates

As skills run, brief status updates:

```
Running: geo-prompt-researcher → finding your best target prompts...
Done. Moving to: geo-citation-writer → drafting content structure...
Done. Running: geo-human-editor → stripping AI patterns...
Done. Here's your final content + schema.
```

## Available Skills

| Skill | When Used |
|-------|-----------|
| geo-prompt-researcher | Find what to rank for |
| geo-competitor-scanner | Analyze competitors |
| geo-site-audit | Full site health check |
| geo-som-strategist | Multi-month roadmap |
| geo-citation-writer | Create new content |
| geo-structured-writer | Add structure to drafts |
| geo-content-optimizer | Optimize existing content |
| geo-human-editor | Final human-voice pass |
| geo-schema-gen | Generate JSON-LD |
| geo-llms-txt | Create llms.txt |
| geo-multimodal-tagger | Optimize images/video |
| geo-sentiment-optimizer | Brand page sentiment |
| geo-report-builder | Performance reports |

## Output Contract

Every session ends with:

1. **Brief summary** — What was done, which skills ran
2. **Primary deliverable** — Content, schema, audit, or report
3. **One clear next step** — Single most impactful action to take

Never 10 recommendations — just one clear next step.

## Example Requests

- "Help me create GEO content about AI search"
- "I want to rank in AI search for 'best CRM'"
- "Audit our homepage for AI visibility"
- "Build a GEO strategy for Q2"
- "Write an article AI will cite"
- "Clean up this content and make it GEO-ready"
- "I don't know where to start with GEO"

## Typical Workflows

### Create from Scratch

```
"I need content about project management"
       ↓
geo-prompt-researcher (find "best project management software")
       ↓
geo-citation-writer (comparison guide format)
       ↓
geo-structured-writer (headers, tables, FAQ)
       ↓
geo-human-editor (final polish)
       ↓
geo-schema-gen (Article + FAQPage schema)
       ↓
Content ready to publish
```

### Improve Existing

```
"Fix this blog post for AI search"
       ↓
geo-human-editor (remove AI feel)
       ↓
geo-content-optimizer (add direct answer, FAQ)
       ↓
geo-schema-gen (add schema)
       ↓
Optimized content ready
```

### Technical Setup

```
"Set up our site for GEO"
       ↓
geo-site-audit (find issues)
       ↓
geo-llms-txt (create file)
       ↓
geo-schema-gen (fix schema)
       ↓
Site GEO-ready
```