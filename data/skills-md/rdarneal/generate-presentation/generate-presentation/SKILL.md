---
name: generate-presentation
description: Generate professional slide decks using proven consulting, sales, storytelling, and problem-solving frameworks.
---

# Presentation Framework Skill

## Disclaimer

Framework names referenced in this skill (e.g., Pyramid Principle, Challenger Sale, SCQA, MECE, and others) are the intellectual property of their respective creators and are referenced here for illustrative and reference purposes. The templates in this project are independently developed interpretations, not reproductions of original source material. This project is not affiliated with or endorsed by those authors or organizations.

## Tool Prohibition

**This skill MUST NEVER call any Gamma MCP tool or any other external presentation-generation tool.** This is a hard constraint that applies at every step of the workflow. The following tools are explicitly prohibited:

- `mcp__gamma__generate`
- `mcp__gamma__get_folders`
- `mcp__gamma__get_generation_status`
- `mcp__gamma__get_themes`
- `mcp__claude_ai_Gamma__generate`
- `mcp__claude_ai_Gamma__get_folders`
- `mcp__claude_ai_Gamma__get_generation_status`
- `mcp__claude_ai_Gamma__get_themes`

This list includes ALL known Gamma tool variants. If any new Gamma or presentation-generation MCP tools become available, they are also prohibited. The output of this skill is always a self-contained markdown outline — never a tool call to render, generate, or submit slides.

---

## Overview

This skill enables Claude to create professional presentations using proven frameworks from consulting, sales, storytelling, and problem-solving domains. It employs a **two-layer compositional system** that separates deck architecture from slide design.

**Key Innovation:** Unlike single-framework approaches, this system lets you mix and match patterns. Choose a **meta-flow** for overall narrative, then apply appropriate **slide patterns** within each section.

---

## Two-Layer Architecture

### Layer 1: Meta-Level Flows
**What:** Overall presentation structure and narrative sequence  
**Analogy:** The "table of contents" or story arc  
**Count:** 10 frameworks covering strategy, sales, storytelling, and analysis  
**Rule:** Choose ONE per presentation

### Layer 2: Slide-Level Patterns  
**What:** How to structure individual slides  
**Analogy:** The "paragraph styles" or content templates  
**Count:** 10 reusable patterns for different content types  
**Rule:** Mix and match within sections; multiple patterns per deck

---

## When to Use This Skill

### Primary Triggers
- User asks to create a presentation, pitch deck, or slide deck
- User mentions specific frameworks: "use Pyramid Principle," "build a Challenger pitch," etc.
- User describes presentation context: "board presentation," "sales demo," "data review"
- User provides content and asks for it to be "structured" or "turned into slides"

### Secondary Triggers
- User asks about presentation best practices or structure
- User requests comparison of framework options
- User has existing deck and wants to restructure it

### DO NOT Use This Skill When
- User wants general business writing (reports, memos) -> use docx skill
- User wants data visualization only -> use data analysis skills
- User asks conceptual questions about frameworks without wanting to build anything

---

## Core Workflow

### Step 0: Classify Input & Extract Context

Before gathering parameters, classify the input type and extract what you can.

**Input Classification:**

```
IF input is a long-form document (research report, article, analysis, memo):
    1. Identify document type:
       - Market research -> likely "data_presentation" or "strategy_recommendation"
       - Case study / success story -> likely "case_study"
       - Technical analysis / postmortem -> likely "problem_analysis"
       - Strategic memo / recommendation -> likely "strategy_recommendation"
       - Product/feature brief -> likely "sales_pitch"
       - Vision / thought leadership -> likely "keynote"
    2. Extract key elements:
       - Findings and data points (-> evidence slides)
       - Conclusions and recommendations (-> answer/resolution slides)
       - Context and background (-> situation/setup slides, compress heavily)
       - Methodology or process details (-> omit unless audience is technical)
    3. Infer parameters from content:
       - Purpose: What does the document conclude or recommend?
       - Audience: What level of language/detail is used?
       - Tone: Formal/data-heavy or narrative/persuasive?
    4. Confirm inferred parameters with user before proceeding

IF input is a topic with minimal context ("make a presentation about X"):
    1. Ask for Purpose and Audience (minimum required)
    2. Infer remaining parameters from purpose if not provided
    3. Proceed to Step 1

IF input is an existing slide deck or presentation outline:
    1. Identify current structure:
       - Does it follow a recognizable meta-flow?
       - What slide patterns are in use (if any)?
       - Where does the narrative break down?
    2. Diagnose issues:
       - Topic titles vs action titles
       - Missing sections (no CTA, no evidence, no context)
       - Structural mismatch (building to reveal for exec audience, etc.)
    3. Recommend restructure approach:
       - Suggest a meta-flow that fits the content and audience
       - Map existing content to the new flow's sections
       - Identify gaps that need new content
    4. Confirm approach with user before regenerating

IF input is a specific request with full context:
    1. Proceed directly to Step 1
```

**Multi-Thread Detection (runs after Input Classification):**

After classifying the input, check whether it contains multiple parallel items that each need narrative coverage throughout the deck.

```
IF input contains multiple parallel items (initiatives, products, recommendations, etc.):
    1. Identify threads:
       - Explicit lists: "7 initiatives," "5 product lines," "4 recommendations"
       - Implicit parallels: topics that each have their own data, status, or analysis
       - Comparison structures: items benchmarked against each other or a standard
    2. Count threads and classify:
       - 1 thread -> standard single-narrative flow (no special handling)
       - 2-5 threads -> "manageable" — use Thread-per-Pillar strategy
       - 6+ threads -> "complex" — use Tiered Grouping or Thread Matrix strategy
    3. Create a Thread Registry:
       - List each thread by name
       - For each thread, extract: current state, gap/complication, recommendation
       - Flag any threads with incomplete data (ask user to fill gaps)
    4. Confirm thread list and priority ranking with user before proceeding

IF input contains only a single topic or narrative:
    Proceed normally — no thread management needed
```

**Content Prioritization (for long-form inputs):**

When condensing a long document into a slide deck, prioritize content in this order:

1. **Always include:** Recommendations, conclusions, key decisions, calls-to-action
2. **High priority:** Interpreted data (data + "so what"), quantified findings, key comparisons
3. **Medium priority:** Supporting evidence for top recommendations, relevant case examples
4. **Low priority:** Background context (compress to 1-2 Situation slides), process details
5. **Omit unless requested:** Methodology, raw data tables, literature reviews, appendix material

**Density Rule:** Target 1 slide per 200-400 words of source content. A 3,000-word report yields roughly 8-15 slides.

**Density vs. Ceiling:** When the density rule produces a slide count above 15, compress further by: (1) merging related findings into single slides, (2) moving supporting evidence to an appendix section, and (3) prioritizing the top 3-5 insights over comprehensive coverage. The 15-slide ceiling takes precedence over the density formula.

**Multi-Thread Management (for inputs with 2+ parallel threads):**

When Multi-Thread Detection identifies multiple threads (initiatives, products, recommendations, etc.), apply one of these strategies to ensure every thread maintains narrative coherence through the deck.

**Strategy A — Thread-per-Pillar (2-5 threads, standard slide budgets):**
- The outer meta-flow provides the shared narrative arc (shared Situation, shared Complication, shared Answer)
- Each Support pillar is dedicated to ONE thread
- Within each pillar, mirror the outer framework's logic for that thread:
  - SCQA: each pillar shows that thread's situation, complication, and resolution
  - WSWNW: each pillar shows that thread's data, interpretation, and action
  - Pyramid: each pillar argues for that thread's recommendation with thread-specific evidence
- The shared Answer slide includes a summary/ranking of all threads
- Next Steps consolidates actions across all threads with clear ownership

**Strategy B — Tiered Grouping (6+ threads, standard slide budgets):**
- Rank threads by impact, urgency, or strategic importance
- Tier 1 (top 2-3 threads): full Thread-per-Pillar treatment with individual pillar sections
- Tier 2 (remaining threads): single summary slide per section using a comparison matrix
- The shared Answer slide presents the tiered prioritization with rationale
- Appendix includes full detail for Tier 2 threads

**Strategy C — Thread Matrix (many threads, tight slide budgets):**
- Each framework section uses a matrix/comparison layout tracking all threads
- Situation: matrix of current state per thread
- Complication: matrix of gaps/risks per thread
- Answer: prioritized ranking of all threads
- Support: 1-2 slides per priority tier with matrix evidence
- Best for audiences who want comprehensive coverage in minimal slides

**Strategy Selection Rule:**
- Thread count <= 5 AND slide budget >= 10 -> Strategy A (Thread-per-Pillar)
- Thread count > 5 AND slide budget >= 12 -> Strategy B (Tiered Grouping)
- Thread count > 3 AND slide budget < 10 -> Strategy C (Thread Matrix)
- When in doubt, ask the user: "Your input has [N] threads. Should I give each full treatment (longer deck) or prioritize the top items (shorter deck)?"

**Thread Completeness Rule:** Every thread identified in the Thread Registry must appear in EVERY major section of the meta-flow (even if compressed to a single bullet in a matrix). No thread should appear in only one section and vanish from others.

---

### Step 1: Understand Context

Gather from user input, extracted context (Step 0), or by asking:

- **Purpose:** What is the presentation trying to achieve?
- **Audience:** Who will see/hear this? (C-suite, prospects, team, etc.)
- **Time:** How long is the presentation? (impacts slide count)
- **Tone:** Formal/analytical or inspirational/emotional?
- **Content:** What information must be included?

**Minimum Viable Parameters:** Purpose and Audience are required. If they cannot be determined from the input, ask. All others have defaults:

| Parameter | Required? | Default if Missing |
|-----------|-----------|-------------------|
| Purpose | Yes -- ask if unclear | Infer from document type (Step 0) |
| Audience | Yes -- ask if unclear | "general professional" |
| Time | No | 20 minutes (~10-12 slides) |
| Tone | No | Infer from purpose: strategy/data -> formal; sales/keynote -> balanced |
| Content | No | Use provided document or topic |

### Step 2: Select Meta-Flow
Use auto-selection logic or honor user preference:

**Strategy/Recommendations:**
- C-suite, <30 min -> **Pyramid Principle** (answer first)
- Need context alignment -> **SCQA** (problem framing)
- Data-heavy -> **What--So What--Now What**

**Sales/Persuasion:**
- Complex B2B -> **Challenger Sale** (teaching approach)
- Product launch -> **AIDA** (funnel progression)
- Emotional pain point -> **PAS** (problem-agitate-solve)

**Storytelling:**
- Keynote/vision -> **Three-Act Structure**
- Behavior change -> **Monroe's Motivated Sequence**

**Analysis:**
- Case study -> **STAR**
- Root cause -> **5 Whys**

### Step 3: Map Slide Patterns to Sections
Each meta-flow has recommended patterns per section. Use the **Pattern Compatibility Matrix** below, or read the selected meta-flow's reference file for section-by-section pattern recommendations.

**Example -- SCQA Meta-Flow:**
- Situation -> SCQA Micro-Narrative pattern
- Complication -> What-So What-Now What pattern
- Answer -> Pyramid Principle pattern
- Support -> Pyramid Principle + MECE patterns

**Multi-Thread Pattern Mapping:**
When using a multi-thread strategy (see Step 0), additional patterns become relevant:
- **Thread overview slides:** Use MECE Decomposition (D) to show all threads in a structured breakdown
- **Per-thread pillar slides:** Use the same pattern you would for single-thread Support, but scoped to one thread
- **Comparison/matrix slides:** Use What-So What-Now What (B) with a matrix layout tracking metrics across threads
- **Priority ranking slides:** Use Pyramid Principle (A) with the ranking as the action title

### Step 4: Load Reference Templates
Read the relevant reference files before generating slides:
- Read `references/meta_[flow].md` for the selected meta-flow's detailed section sequence, slide counts, and section-by-section guidance
- Read `references/slide_[pattern].md` for each slide pattern you will use -- these contain element guides, title formulas, layout diagrams, and quality checklists
- Only load the specific files needed for the selected flow and patterns (not all 20)

**Important:** The `---` dividers inside reference template files are documentation section boundaries, not slide delimiters. When generating the final presentation output, use `---` only as slide boundaries per the Output Format rules below.

### Step 5: Generate Content
- Follow meta-flow section sequence from the reference template
- Apply appropriate slide pattern to each slide
- Ensure titles match pattern requirements (action titles for Pyramid, etc.)
- Maintain consistency within sections

### Step 6: Quality Check

**Content Quality:**
- Does deck follow chosen meta-flow structure?
- Are slide patterns appropriate for content type?
- Would audience get main message from titles alone?
- Is evidence quantified where possible?

**Thread Completeness (for multi-thread inputs):**
- Does every thread from the Thread Registry appear in every major section?
- Are threads consistently named throughout (no thread called "Initiative A" in Situation and "the first project" in Support)?
- Does the Answer slide account for ALL threads (even if some are deprioritized)?
- Could a reader trace any single thread from start to finish through the deck?
- Are threads that received Tier 2 / summary treatment still present (not silently dropped)?

**Slide Format Compliance:**
- Every slide starts with a single `#` heading (the action title)
- `---` is the only slide boundary marker (no other separators)
- No sub-headings (`##`, `###`) appear within any slide
- `**bold**` labels used for section markers within slides (e.g., `**WHAT**`, `**FEATURE**`)
- Each slide body is 30-100 words (depending on density setting)
- Bullet lists use `-` and do not exceed 5 items per slide
- First slide is the title slide with no preceding `---`
- Avoid raw code blocks, tables, or complex markdown within slides (keep portable across presentation tools)

---

## Meta-Level Flows (Layer 1)

### 1. Pyramid Principle
**Type:** Answer-first logic  
**Use:** Executive briefings, strategy recommendations  
**Structure:** Executive summary -> Main recommendation -> Supporting pillars (each with evidence) -> Next steps  
**Key Rule:** Lead with answer, never build to reveal  
**Slide Count:** 5-15 slides

### 2. SCQA  
**Type:** Problem-framing narrative  
**Use:** Context alignment, issue framing  
**Structure:** Situation (stable facts) -> Complication (what changed) -> Question (key question) -> Answer (recommendation) -> Support -> Next steps  
**Key Rule:** SCQ sets context, A leads into Pyramid structure  
**Slide Count:** 5-15 slides

### 3. What--So What--Now What
**Type:** Data -> insights -> action  
**Use:** Analytics reviews, research readouts  
**Structure:** Context -> What (findings) -> So What (interpretation) -> Now What (recommendations)  
**Key Rule:** Minimize "What," maximize "So What" and "Now What"  
**Slide Count:** 5-15 slides

### 4. Challenger Sale
**Type:** Teaching sales approach  
**Use:** Complex B2B, reframing customer thinking  
**Structure:** Warm-up -> Reframe -> Impact quantification -> Emotional impact -> Value prop -> Solution -> Proof  
**Key Rule:** Keep product out of early sections; teach before selling  
**Slide Count:** 8-15 slides

### 5. AIDA
**Type:** Marketing funnel  
**Use:** Product launches, investor pitches  
**Structure:** Attention (hook) -> Interest (features) -> Desire (benefits + proof) -> Action (CTA)  
**Key Rule:** Strong hook, explicit CTA with urgency  
**Slide Count:** 5-15 slides

### 6. PAS
**Type:** Emotional persuasion  
**Use:** Strong pain points, short sales pitches  
**Structure:** Problem -> Agitate -> Solution  
**Key Rule:** Amplify consequences without overdoing fear  
**Slide Count:** 5-14 slides

### 7. Three-Act Structure
**Type:** Narrative arc  
**Use:** Keynotes, vision talks, transformation stories  
**Structure:** Act I (setup + inciting incident) -> Act II (obstacles + rising stakes) -> Act III (resolution + new normal)  
**Key Rule:** Audience is hero, alternate "what is" vs "what could be"  
**Slide Count:** 5-15 slides

### 8. Monroe's Motivated Sequence
**Type:** Behavior change advocacy  
**Use:** Persuasive talks, change management  
**Structure:** Attention -> Need -> Satisfaction -> Visualization -> Action  
**Key Rule:** Strong visualization section (positive/negative scenarios)  
**Slide Count:** 5-15 slides

### 9. STAR
**Type:** Case study narrative  
**Use:** Portfolio presentations, success stories  
**Structure:** Situation -> Task -> Action (bulk of content) -> Result  
**Key Rule:** Focus on Action section; quantify Results  
**Slide Count:** 5-13 slides per case; multi-case max 15 slides

### 10. 5 Whys
**Type:** Root cause investigation  
**Use:** Problem analysis, operational reviews  
**Structure:** Problem statement -> Why cascade -> Root cause -> Countermeasures -> Implementation  
**Key Rule:** Stop at systemic/actionable cause, avoid blaming individuals  
**Slide Count:** 5-12 slides

---

## Slide-Level Patterns (Layer 2)

### A. Pyramid Principle Slide
**Concept:** Title states conclusion, body provides support  
**Structure:** Action title + 3-5 bullets or chart  
**Use In:** Any executive/strategy deck; all Pyramid meta-flow slides  
**Example Title:** "Enterprise segment generates 73% margin vs 51% for SMB"  
**Anti-Pattern:** Topic titles like "Market Analysis"

### B. What--So What--Now What Slide
**Concept:** Data + interpretation + recommendation on single slide  
**Structure:** WHAT (data/chart) -> SO WHAT (insight) -> NOW WHAT (action)  
**Use In:** Data sections, analytics decks, evidence slides  
**Key Rule:** All three elements required; no naked data

### C. FAB Slide
**Concept:** Feature -> Advantage -> Benefit translation  
**Structure:** Three-part for each capability  
**Use In:** Product demos, solution sections  
**Key Rule:** Benefits tailored to audience role (exec vs end-user)  
**Example:** Real-time sync (F) -> eliminates conflicts (A) -> saves 10 hrs/week (B)

### D. MECE Decomposition Slide
**Concept:** Break topic into mutually exclusive, collectively exhaustive buckets  
**Structure:** Title + 2-5 categories + visual (tree/formula)  
**Use In:** Issue structuring, argument organization  
**Key Rule:** Categories must not overlap and must cover everything  
**Example:** "Revenue driven by: new customers, higher ARPU, lower churn"

### E. SCQA Micro-Narrative Slide
**Concept:** Four-part framing on single slide  
**Structure:** Situation -> Complication -> Question -> Answer  
**Use In:** Framing individual arguments, executive summaries  
**Key Rule:** Keep each element to 1-2 sentences

### F. BAB Mini-Story Slide
**Concept:** Before -> After -> Bridge transformation  
**Structure:** Pain points -> outcomes (quantified) -> how you got them there  
**Use In:** Case studies, social proof sections  
**Key Rule:** Strong quantified contrast between Before and After

### G. Monroe's Visualization Slide
**Concept:** Future scenarios (with/without solution)  
**Structure:** WITH (positive outcomes) vs WITHOUT (negative consequences)  
**Use In:** Persuasive decks, creating urgency  
**Key Rule:** Make scenarios vivid and specific

### H. 5 Whys Cascade Slide
**Concept:** Visual root cause chain  
**Structure:** Problem -> Why? -> Layer 1 -> Why? -> ... -> Root cause  
**Use In:** Problem analysis sections  
**Key Rule:** Typically 3-5 layers deep

### I. STAR Micro-Case Slide
**Concept:** Compressed case study  
**Structure:** Situation (1-2 lines) -> Task (1 line) -> Action (bullets) -> Result (quantified)  
**Use In:** Proof sections, portfolio slides  
**Key Rule:** Emphasize Action and Result

### J. Problem-Solution-Benefit Slide
**Concept:** Straightforward three-part  
**Structure:** PROBLEM -> SOLUTION -> BENEFIT  
**Use In:** Quick pitches, product features  
**Key Rule:** Quantify problem and benefit

---

## Pattern Compatibility Matrix

| Meta-Flow | Recommended Slide Patterns by Section |
|-----------|---------------------------------------|
| **Pyramid Principle** | All sections: Pyramid Principle slides + MECE for structure |
| **SCQA** | Situation: SCQA Micro; Complication: WSWNW; Answer/Support: Pyramid |
| **WSWNW** | Context: SCQA Micro; What/So What/Now What: WSWNW or Pyramid slides |
| **Challenger** | Warm-up: SCQA Micro; Reframe: Pyramid; Impact Quantification: WSWNW; Emotional Impact: Monroe Viz; Value Prop: PSB; Solution: FAB; Proof: BAB |
| **AIDA** | Attention: SCQA Micro; Interest: FAB; Desire: BAB/STAR; Action: PSB |
| **PAS** | Problem: PSB; Agitate: WSWNW/Monroe Viz; Solution: FAB |
| **Three-Act** | Setup: SCQA Micro; Confrontation: BAB/5 Whys; Resolution: Monroe Viz/STAR |
| **Monroe** | Need: WSWNW; Satisfaction: PSB; Visualization: Monroe Viz; Action: Pyramid |
| **STAR** | Situation: SCQA Micro; Task: statement; Action: FAB/Pyramid; Result: WSWNW |
| **5 Whys** | Problem: SCQA Micro; Cascade: 5 Whys; Root: Pyramid; Counter: MECE/PSB |

---

## Auto-Selection Logic

**Variable Definitions:**
- `context_needed`: TRUE when the audience is cross-functional, unfamiliar with the topic, or when the user's input indicates stakeholder alignment is a goal.
- `complexity`: "high" when the sale involves multiple stakeholders, long sales cycles, or requires reframing the buyer's thinking. Otherwise "low".

```
IF purpose = "strategy_recommendation":
    IF audience = "c_suite" AND time >= 30:
        meta_flow = "Pyramid Principle"
    ELIF context_needed = TRUE:
        meta_flow = "SCQA"
    ELSE:
        meta_flow = "What-So What-Now What"

ELIF purpose = "sales_pitch":
    IF complexity = "high" AND time >= 30:
        meta_flow = "Challenger Sale"
    ELIF time <= 20:
        meta_flow = "AIDA"
    ELSE:
        meta_flow = "PAS"

ELIF purpose = "data_presentation":
    IF audience = "c_suite":
        meta_flow = "Pyramid Principle"
    ELSE:
        meta_flow = "What-So What-Now What"

ELIF purpose = "keynote":
    IF emphasis = "emotional":
        meta_flow = "Three-Act Structure"
    ELSE:
        meta_flow = "Monroe's Motivated Sequence"

ELIF purpose = "case_study":
    meta_flow = "STAR"

ELIF purpose = "problem_analysis":
    meta_flow = "5 Whys"

ELIF purpose = "training" OR purpose = "education":
    IF emphasis = "behavior_change":
        meta_flow = "Monroe's Motivated Sequence"
    ELSE:
        meta_flow = "Three-Act Structure"

ELIF purpose = "team_update" OR purpose = "status_report":
    meta_flow = "What-So What-Now What"

ELIF purpose = "retrospective":
    IF root_cause_focus = TRUE:
        meta_flow = "5 Whys"
    ELSE:
        meta_flow = "STAR"

ELSE:
    meta_flow = "Pyramid Principle"  # Most universally applicable default
    NOTE: Confirm with user -- Pyramid Principle works for most contexts,
    but ask if a different framework would better suit their needs.
```

---

## Output Format

### Workflow

When creating presentations, Claude should:

1. **State the approach:** "I'll use [Meta-Flow] structure with [key slide patterns] for this [audience/purpose]."
2. **Provide outline:** Show section breakdown with slide counts before building.
3. **Load references:** Read the selected meta-flow and slide-pattern files from `references/` (see Reference Templates section).
4. **Generate slides:** Output the complete presentation outline (see format and delivery rules below).
5. **Include metadata:** Note which pattern each slide uses (for user learning).
6. **Offer alternatives:** If auto-selected, mention other viable frameworks.

### Presentation Outline Format

All presentation output MUST use the following slide-structured markdown format:

- Each slide is separated by a horizontal rule (`---`)
- Each slide begins with a heading (`#`) as the slide title
- Slide content follows the title using standard markdown (bullets, bold, etc.)
- The first slide is the title slide; no `---` precedes it

**Template:**

```markdown
# [Presentation Title]
[Subtitle or tagline]
[Date | Presenter | Company]

---

# [Slide Title -- action title stating the "so what"]

- Key point one
- Key point two
- Key point three

---

# [Next Slide Title]

**[Section Label]**
Content or data point

**[Section Label]**
Content or data point

---

# [Call-to-Action or Closing Title]

- Next step 1
- Next step 2
- Decision needed by [date]
```

**Format Rules:**
- Slide titles MUST be action titles (state the conclusion, not the topic) per the selected slide pattern
- Use `**bold**` for labels, emphasis, or section headers within a slide
- Use `-` bullet lists for supporting points (max 5 per slide)
- Use numbered lists (`1.`) only for sequential steps or ranked items
- Keep slide content to 30-100 words per slide depending on density setting
- Do NOT use sub-headings (`##`, `###`) within a slide -- use `**bold**` labels instead
- The `---` divider is the ONLY slide boundary marker

**Example (Pyramid Principle, 3 slides):**

```markdown
# Growth Strategy Recommendation
Prioritize Enterprise Segment
Q3 2026 | Strategy Team | Acme Corp

---

# We recommend shifting focus to enterprise customers to achieve 40% revenue growth

- Enterprise segment delivers 73% gross margin vs 51% for SMB
- Top 10 enterprise wins validate our sales model effectiveness
- Market window for enterprise expansion closes within 18 months

---

# Enterprise customers deliver 3x higher lifetime value than SMB

**Retention**
Enterprise retention rate is 94% vs 67% for SMB, reducing acquisition cost pressure

**Revenue per Account**
Average enterprise contract is $240K vs $18K for SMB -- a 13x difference

**Expansion Revenue**
82% of enterprise accounts expand within 12 months vs 23% of SMB
```

---

## Quality Standards

### Deck-Level
- Clear meta-flow from start to finish
- Appropriate slide count for time available
- Logical progression between sections
- Main message evident from titles alone

### Slide-Level
- Each slide uses identifiable pattern
- Titles match pattern requirements (action vs topic)
- Evidence quantified where possible
- Visual hierarchy clear

### Content
- No jargon without definition
- MECE logic where categorizing
- Data has source and interpretation
- Recommendations are concrete and actionable

---

## Common Mistakes to Avoid

### Meta-Flow Mistakes
- Building to reveal (except storytelling flows)
- Mixing incompatible meta-flows simultaneously
- Wrong flow for audience (Three-Act for time-pressed exec)
- Skipping context when needed (jumping to Answer without Situation)

### Slide-Pattern Mistakes
- Topic titles when Pyramid pattern requires action titles
- Features without benefits (incomplete FAB)
- Data without interpretation (naked WHAT without SO WHAT)
- Multiple patterns fighting on one slide
- MECE violations (overlapping or incomplete categories)

### Multi-Thread Mistakes
- Scattering threads randomly across sections instead of tracking each one through the full narrative
- Letting the "loudest" thread (most data, most dramatic) dominate while others vanish
- Treating multi-thread input as a single narrative — producing one Situation that only covers 3 of 7 threads
- Inconsistent thread naming (switching between labels makes threads hard to follow)
- Failing to prioritize when thread count exceeds slide budget — trying to cover all equally and covering none well

### Execution Mistakes
- Too many bullets (>5 per slide)
- Inconsistent pattern within section
- Missing quantification ("significant" vs "43%")
- No clear call-to-action in action-oriented flows

---

## Advanced Techniques

### Pattern Mixing
Combine patterns within a section when appropriate:
- **MECE + Pyramid:** Use MECE to structure arguments, Pyramid pattern to execute each
- **SCQA + Pyramid:** SCQA for framing, Pyramid for supporting slides
- **FAB + WSWNW:** FAB for features, WSWNW for impact analysis

### Audience Adaptation
- **C-Suite:** Pyramid meta-flow + Pyramid slides (answer first everywhere)
- **Prospects:** Match to buying stage (early: Challenger; late: AIDA)
- **General:** Storytelling flows (Three-Act, Monroe)
- **Technical:** Data flows (WSWNW) with detailed evidence

### Time Adaptation
- **5-10 min:** 3-7 slides, compact meta-flow
- **15-20 min:** 8-12 slides, full flow
- **30-45 min:** 10-15 slides, complete framework with evidence (use appendix for depth)
- **60+ min:** 12-15 slides + extensive appendix for discussion and deep dives

---

## Reference Templates

Detailed templates for each framework are maintained in `references/`. Read the relevant files during Step 4 of the Core Workflow.

### Meta-Flow Templates (Layer 1)
| # | Flow | File |
|---|------|------|
| 1 | Pyramid Principle | `references/meta_pyramid_principle.md` |
| 2 | SCQA | `references/meta_scqa.md` |
| 3 | What--So What--Now What | `references/meta_wswnw.md` |
| 4 | Challenger Sale | `references/meta_challenger_sale.md` |
| 5 | AIDA | `references/meta_aida.md` |
| 6 | PAS | `references/meta_pas.md` |
| 7 | Three-Act Structure | `references/meta_three_act.md` |
| 8 | Monroe's Motivated Sequence | `references/meta_monroe.md` |
| 9 | STAR | `references/meta_star.md` |
| 10 | 5 Whys | `references/meta_5_whys.md` |

### Slide-Pattern Templates (Layer 2)
| ID | Pattern | File |
|----|---------|------|
| A | Pyramid Principle Slide | `references/slide_pyramid.md` |
| B | What--So What--Now What Slide | `references/slide_wswnw.md` |
| C | FAB Slide | `references/slide_fab.md` |
| D | MECE Decomposition Slide | `references/slide_mece.md` |
| E | SCQA Micro-Narrative Slide | `references/slide_scqa_micro.md` |
| F | BAB Mini-Story Slide | `references/slide_bab.md` |
| G | Monroe's Visualization Slide | `references/slide_monroe_viz.md` |
| H | 5 Whys Cascade Slide | `references/slide_5whys_cascade.md` |
| I | STAR Micro-Case Slide | `references/slide_star_micro.md` |
| J | PSB Slide | `references/slide_psb.md` |

---

## Example Invocations

### User Request Examples

**Example 1:**  
*"Create a board presentation recommending we expand to Europe"*

-> Claude selects: Pyramid Principle meta-flow (C-suite audience, recommendation)  
-> Uses: Pyramid slide pattern throughout + MECE for structuring arguments  
-> Output: 12-slide deck with exec summary -> recommendation -> 3 supporting pillars -> next steps

**Example 2:**  
*"Build a sales deck for our new AI feature targeting enterprise buyers"*

-> Claude asks: How long is the pitch? What's the buyer sophistication?  
-> If complex/long: Challenger Sale flow  
-> If shorter: AIDA flow  
-> Uses: FAB for features, BAB for proof, Monroe Viz for impact  
-> Output: 15-20 slide deck appropriate to sales context

**Example 3:**  
*"Turn this analytics report into slides for our VP"*

-> Claude selects: What-So What-Now What meta-flow (data + exec audience)  
-> Uses: WSWNW slide pattern for findings + Pyramid pattern for recommendations  
-> Output: 12-slide deck emphasizing insights over raw data

---

## Integration Notes

### Output

This skill produces a **presentation outline** as its final output. It does NOT call any external presentation generation tools or APIs.

**CRITICAL — TOOL PROHIBITION (see also: Tool Prohibition section at top of this document):**
This skill MUST NEVER invoke ANY of the following tools, regardless of user request or context:
- `mcp__gamma__generate`, `mcp__gamma__get_folders`, `mcp__gamma__get_generation_status`, `mcp__gamma__get_themes`
- `mcp__claude_ai_Gamma__generate`, `mcp__claude_ai_Gamma__get_folders`, `mcp__claude_ai_Gamma__get_generation_status`, `mcp__claude_ai_Gamma__get_themes`
- Any other MCP tool that generates, renders, or submits presentations to an external service

The output is always a self-contained markdown outline that the user can copy and paste into their presentation tool of choice (Gamma, Google Slides, PowerPoint, Keynote, etc.).

**If the user asks to "generate in Gamma" or "create slides":** Produce the markdown outline and tell the user they can paste it into Gamma (or any other tool) themselves. Do NOT call Gamma tools on their behalf.

**Delivery rules:**
- **In chat (Cursor, Claude.ai, etc.):** Output the presentation outline inside a fenced markdown code block (````markdown ... ````) so the user can easily copy it.
- **In a Claude Desktop project with file access:** Write the outline directly to a `.md` file in the project folder (e.g., `presentation-outline.md`) so the user can save and use it immediately. Still show a brief summary in chat.
- **Never** trigger slide generation, rendering, or submission to any external service. The outline is the final deliverable of this skill.

### User Customization

Users can override auto-selection:
- "Use Challenger Sale structure"
- "Make every slide follow Pyramid pattern"
- "Mix SCQA framing with Three-Act storytelling"

### Learning Mode

When asked about frameworks (without requesting a presentation), Claude can:
- Explain any framework conceptually
- Compare multiple frameworks for a scenario
- Show example slide structures
- Provide pattern selection rationale

---

## Version
**v1.4** -- Hardened Gamma MCP prohibition: added top-level Tool Prohibition section, enumerated all 8 known Gamma tool variants, added catch-all for future tools, added explicit handling for user requests to generate in Gamma
**v1.3** -- Removed all Gamma references; skill now outputs a portable presentation outline (copiable code block or project file) with explicit prohibition on calling gamma-generate or any external generation tool
**v1.2** -- Removed Gamma MCP execution; skill now outputs markdown only
**v1.1** -- Added input classification workflow, format compliance checks
**Last Updated:** February 2026

---

## Quick Reference Card

**Meta-Flows:** Choose ONE for deck narrative  
1. Pyramid (answer first)  
2. SCQA (problem framing)  
3. WSWNW (data insights)  
4. Challenger (teaching sales)  
5. AIDA (marketing funnel)  
6. PAS (emotional persuasion)  
7. Three-Act (narrative)  
8. Monroe (behavior change)  
9. STAR (case study)  
10. 5 Whys (root cause)

**Slide-Patterns:** Mix within sections  
A. Pyramid slide (action title)  
B. WSWNW slide (data + insight + action)  
C. FAB (feature -> benefit)  
D. MECE (categorization)  
E. SCQA micro (framing)  
F. BAB (before/after)  
G. Monroe viz (scenarios)  
H. 5 Whys cascade (root cause)  
I. STAR micro (case)  
J. PSB (problem/solution/benefit)

**Default Approach:**
1. Understand context -> 2. Select meta-flow -> 3. Map slide patterns -> 4. Load references -> 5. Generate -> 6. Quality check
