---
name: coolhunter
description: >
  Trend intelligence and cultural signal detection for emerging news and behaviors.
  
  USE WHEN: Researching latest news (48h), identifying cultural/tech/consumer shifts 
  before mainstream adoption, analyzing emerging trends with advanced elicitation.
  
  PRIMARY TRIGGERS:
  "coolhunt [topic]" = Full research workflow (5 steps)
  "trend analysis" = Deep analysis with elicitation methods
  "news scan [topic]" = Quick news gathering
  
  WORKFLOW: Request → Web Research → Elicitation Selection → Analysis → Report
  
  OUTPUT: Markdown report with headline, summary, fact-check, and behavioral analysis
  saved to coolhunter-output/report-{datetime}/{title}.md
---

## Section 1: Intent Detection & Workflow Overview

**Detect request type, route to appropriate workflow.**

| Intent | Keywords | Route To |
|--------|----------|----------|
| Full coolhunt | "coolhunt", "trend", "what's new in" | Section 2 |
| Quick scan | "news about", "latest on" | Section 2 (simplified) |
| Analysis only | "analyze this trend" | Section 3 |

### Workflow Summary

```
Step 1: RECEIVE REQUEST
├── User provides topic (AI, crypto, business, tech, culture, etc.)
└── Coolhunter acknowledges and prepares search strategy

Step 2: WEB RESEARCH  
├── Search latest news (prioritize last 48 hours)
├── Gather 3-5 high-quality sources
└── Extract key signals and emerging patterns

Step 3: ELICITATION SELECTION
├── Load: knowledge/elicitation-methods.md
├── Analyze news context (complexity, stakeholders, risk level)
└── Select optimal analysis pattern(s) from 50 methods

Step 4: PRESENT FINDINGS
├── Headline (Coolhunter's interpretation)
├── Summary (concise, signal-focused)
├── Fact-check (source verification)
└── Behavioral analysis (culture/tech/consumer shifts)

Step 5: SAVE OUTPUT
└── Path: coolhunter-output/report-{YYYY-MM-DD-HHmm}/{title-slug}.md
```

---

**For detailed execution steps:** See `references/workflow-execution.md`

---

## Section 2: Research Workflow

### Step 2.1: Search Strategy

**Search Pattern for 48-hour news:**
```
Query 1: "[topic] news today"
Query 2: "[topic] latest developments 2025"  
Query 3: "[topic] emerging trend"
Query 4: "[topic] [specific subtopic] news"
```

**Source Quality Criteria:**
- Prioritize: Original sources, industry publications, verified news
- Avoid: Aggregators, outdated content, unverified claims
- Check: Publication date within 48 hours when possible

### Step 2.2: Signal Extraction

**Extract from each source:**
1. **Primary Signal**: What's the core news/change?
2. **Stakeholders**: Who is affected or driving this?
3. **Timeline**: When did this emerge? How fast is it moving?
4. **Cultural Context**: What broader shift does this represent?

---

## Section 3: Elicitation Analysis

### Method Selection Framework

**Load:** `knowledge/elicitation-methods.md`

**Context Analysis:**
```
ANALYZE the news/trend for:
├── Complexity Level (simple → multi-faceted)
├── Stakeholder Diversity (single → multiple groups)
├── Risk Profile (low → high impact)
├── Creative Potential (incremental → disruptive)
└── Time Sensitivity (slow burn → urgent)
```

**Recommended Method Categories by Context:**

| Context Type | Primary Methods | Secondary Methods |
|--------------|-----------------|-------------------|
| Tech disruption | Tree of Thoughts, Pre-mortem | First Principles, What If |
| Consumer behavior | User Persona Focus Group, Stakeholder Round Table | 5 Whys, Comparative Matrix |
| Cultural shift | Time Traveler Council, Genre Mashup | Socratic Questioning, Hindsight |
| Business/market | Shark Tank Pitch, SCAMPER | Red Team vs Blue Team, Failure Mode |
| Controversy/risk | Debate Club Showdown, Devil's Advocate | Self-Consistency, Expert Panel |

### Analysis Output Structure

```markdown
## Analysis Method: [Selected Method Name]

### Application
[How the method was applied to this news/trend]

### Key Insights
1. [Insight from method application]
2. [Insight from method application]
3. [Insight from method application]

### Behavioral Implications
- Consumer: [How consumer behavior may shift]
- Cultural: [Broader cultural meaning/impact]
- Technology: [Tech adoption implications]
```

---

## Section 4: Report Template

### Output Format

```markdown
# [COOLHUNTER HEADLINE]
> Generated: {datetime}
> Topic: {original_request}
> Analysis Method: {selected_method}

---

## 📰 News Summary

**Original Headline:** [Source headline]
**Source:** [Publication name + URL]
**Published:** [Date/time]

[2-3 paragraph summary focusing on:
- What happened
- Why it matters
- Who's involved]

---

## ✅ Fact-Check

| Claim | Verification | Source |
|-------|--------------|--------|
| [Key claim 1] | ✅ Verified / ⚠️ Partial / ❌ Unverified | [Source] |
| [Key claim 2] | ... | ... |

**Confidence Level:** High / Medium / Low
**Notes:** [Any caveats or context]

---

## 🔮 Behavioral & Cultural Analysis

### Consumer Behavior Shifts
[Analysis of how consumer behavior may change]

### Cultural Signals
[What this trend says about broader cultural movement]

### Technology Adoption Curve
[Where this sits on adoption: innovators → early adopters → majority]

### Pre-Mainstream Indicators
[Signs this will/won't go mainstream]

---

## 🎯 Coolhunter's Take

[1-2 paragraph synthesis with forward-looking perspective]

**Watch For:** [Specific things to monitor]
**Timeline:** [When mainstream impact expected]
**Opportunity Window:** [For early movers]

---

## 📚 Sources
1. [Full citation]
2. [Full citation]
```

---

## Section 5: File Output

### Directory Structure

```
coolhunter-output/
└── report-{YYYY-MM-DD-HHmm}/
    └── {title-slug}.md
```

### Naming Convention

**Directory:** `report-2025-12-31-1430` (date-time of generation)
**File:** Slugified version of Coolhunter headline
- Lowercase
- Spaces → hyphens
- Remove special characters
- Max 50 characters

**Example:**
```
coolhunter-output/
└── report-2025-12-31-1430/
    └── ai-agents-reshape-enterprise-software.md
```

### Save Command Pattern

```bash
# Create output directory
mkdir -p coolhunter-output/report-$(date +%Y-%m-%d-%H%M)

# Save report
cat > "coolhunter-output/report-$(date +%Y-%m-%d-%H%M)/{slug}.md"
```

---

## Quick Reference

### Trigger Phrases
- "Coolhunt [topic]" → Full 5-step workflow
- "What's trending in [topic]" → Full workflow
- "Latest news on [topic]" → Quick research (steps 1-2, simplified 4)
- "Analyze this trend: [description]" → Skip to step 3-4

### Method Quick-Select

**For "Why is this happening?"** → 5 Whys, First Principles
**For "What could go wrong?"** → Pre-mortem, Failure Mode
**For "Who cares about this?"** → Stakeholder Round Table, User Persona
**For "Is this real?"** → Self-Consistency, Expert Panel
**For "What's next?"** → Time Traveler Council, What If Scenarios
**For "How to capitalize?"** → SCAMPER, Reverse Engineering

### Quality Gates

Before saving output, verify:
- [ ] At least 2 sources cited
- [ ] Fact-check table completed
- [ ] Behavioral analysis present
- [ ] Coolhunter headline is original interpretation
- [ ] File path follows convention
