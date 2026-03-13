---
name: design-research
description: Conducts user experience research and analysis to inform design decisions. Use when user says "user research", "persona", "personas", "who are our users", "target audience", "customer segments", "design principles", "user needs", "pain points", "jobs to be done", "JTBD", "user interviews", "discussion guide", "research plan", "competitive analysis", "understand the users", "user data", or "analytics review". Reviews first-party and third-party user data, analyzes industry trends from UX and visual design perspectives, and plans user research studies. Creates personas, customer segments, design principles, design roadmaps, and research discussion guides. Do NOT use when already have approved personas, in implementation/coding phase, need visual mockups (use design-concepts), or reviewing built product (use design-qa).
---

# Design - Research

This skill guides Claude through comprehensive UX research processes using Jobs-to-be-Done (JTBD) methodology to understand user needs, behaviors, and contexts that inform design decisions.

## Core Methodology

### Jobs-to-be-Done Framework
Every research activity focuses on understanding what "job" users are hiring a product to do. Research uncovers:
- **Functional jobs**: The practical tasks users need to accomplish
- **Emotional jobs**: How users want to feel or avoid feeling
- **Social jobs**: How users want to be perceived by others
- **Context**: The circumstances that trigger the job

### Research Process
1. **Scoping & Planning**: Define research questions, identify what needs to be learned
2. **Data Collection**: Gather existing data (analytics, support tickets, reviews) and plan new research
3. **Analysis**: Identify patterns, pain points, and opportunities using JTBD lens
4. **Synthesis**: Create actionable artifacts (personas, principles, roadmaps)
5. **Validation**: Test assumptions and refine understanding

## Tool Usage Patterns

### Initial Information Gathering
**Step 1: Inventory Available Resources**
Before starting research, Claude should:
```
1. Ask user what materials they have:
   - Existing user data (analytics, surveys, interviews)
   - Competitor research or industry reports
   - Current product/website/app to review
   - Business requirements or constraints

2. Use `view` to check uploaded files
3. Use `web_search` for industry trends and competitor analysis
4. Use `web_fetch` to analyze competitor websites and apps
```

**Step 2: Create Research Plan**
Document what needs to be learned and how:
```markdown
# Research Plan
## Research Questions
- What jobs are users trying to accomplish?
- What are current pain points and workarounds?
- What contexts trigger the need for this solution?

## Data Sources
- [ ] Analytics review (if provided)
- [ ] User interviews (plan discussion guide)
- [ ] Competitor analysis
- [ ] Industry trend research

## Timeline & Deliverables
```

### Data Analysis Workflow
When reviewing user data:
1. **Quantitative First**: Look at analytics, usage data, conversion metrics
   - Use `view` to read CSV/Excel files
   - Create summary analysis in markdown
   - Identify behavioral patterns

2. **Qualitative Second**: Review interviews, support tickets, reviews
   - Extract direct user quotes (always cite source)
   - Identify recurring themes
   - Map to JTBD framework

3. **Competitive Analysis**: Research how others solve similar jobs
   - Use `web_search` for competitors: "best [category] apps 2025"
   - Use `web_fetch` to analyze specific competitor sites
   - Screenshot key interactions (if user provides URLs)
   - Document strengths/weaknesses relative to user jobs

### Creating Discussion Guides
For planning user research studies:
```markdown
# User Interview Discussion Guide

## Introduction (5 min)
- Thank participant
- Explain purpose and format
- Get consent to record

## Context Questions (10 min)
[Ask about their current situation and job-to-be-done]
- Walk me through the last time you [relevant activity]
- What triggered you to start looking for a solution?
- What alternatives have you tried?

## Deep Dive (30 min)
[Focus on specific jobs and contexts]
- What would make this task easier/faster/better?
- What's frustrating about current solutions?
- What would success look like?

## Closing (5 min)
- Anything else important we should know?
- Thank participant
```

## Quality Criteria

### Excellent Personas Include:
- **Name and photo** (AI-generated or stock image)
- **Demographics**: Age, location, role (only if relevant to JTBD)
- **Jobs to be done**: 3-5 primary jobs they're trying to accomplish
- **Pain points**: Current struggles and workarounds (with real quotes)
- **Goals & motivations**: What success looks like for them
- **Context**: When/where they experience the need
- **Tech comfort level**: Relevant for product complexity decisions

**Avoid**: Generic personas that don't tie to specific jobs, fictional fluff that doesn't inform design decisions

### Excellent Design Principles:
- **Specific to the project**: Not generic ("be simple"), but contextual ("Prioritize speed over options for first-time setup")
- **Actionable**: Designers can use them to make decisions
- **Tied to research insights**: Each principle comes from user data
- **Memorable**: Short, clear, possibly with a tagline
- **3-7 principles**: Enough to guide, not so many they're ignored

**Example Format**:
```markdown
## Design Principles

### 1. Progressive Disclosure Over Feature Parity
*Show what users need now, not everything we can do*
**Insight**: 73% of users abandoned setup because they felt overwhelmed by options they didn't understand yet.

### 2. Forgiveness Over Prevention
*Make it easy to undo, not hard to do wrong*
**Insight**: Users expressed anxiety about "breaking things" - they want to explore confidently.
```

### Excellent Customer Segments:
- **Behavioral-based**: Grouped by how they use product, not just demographics
- **JTBD-aligned**: Each segment has distinct primary jobs
- **Sized**: Approximate % of user base (if data available)
- **Named meaningfully**: "Power Users" not "Segment A"
- **Actionable**: Each segment suggests different design approaches

### Excellent Design Roadmaps:
- **Insight-driven**: Each initiative ties to research finding
- **Prioritized**: Uses framework (Impact/Effort, RICE, etc.)
- **Timeline**: Realistic phases (Discovery → Concept → Build)
- **Success metrics**: How we'll know if it worked
- **Dependencies noted**: What needs to happen first

## Deliverable Formats

### File Organization

**IMPORTANT: Organize all deliverables by feature/assignment in dated folders.**

Each research project should be saved in its own folder with the feature name:
`docs/design/{feature-name}-research-{MMDDYY}/`

**Feature Name Guidelines:**
- Use kebab-case (lowercase with hyphens)
- Examples: `checkout-flow`, `user-profile`, `dashboard-redesign`, `search-filters`
- Ask the user for the feature name if not provided
- Suggest a name based on their description if needed

**Examples:**
- Checkout flow research on Oct 24, 2025: `docs/design/checkout-flow-research-102425/`
- Dashboard redesign research on Nov 1, 2025: `docs/design/dashboard-redesign-research-110125/`
- User profile iteration on Nov 15, 2025: `docs/design/user-profile-research-111525/`

**Rationale:**
- **Immediate clarity**: Know what feature each file relates to
- **Version history**: Same feature can have multiple dated iterations
- **No conflicts**: Different features can have same-named files
- **Organized**: Related research artifacts stay together

**Folder structure:**
```
docs/design/{feature-name}-research-{MMDDYY}/
├── {feature-name}-personas.md
├── {feature-name}-customer-segments.md
├── {feature-name}-design-principles.md
├── {feature-name}-design-roadmap.md
└── {feature-name}-research-discussion-guide.md
```

### Personas
**Location**: `docs/design/{feature-name}-research-{MMDDYY}/`
**File**: `{feature-name}-personas.md`
**Format**: Markdown with clear sections for each persona
**Include**: Photo/avatar, quote, jobs-to-be-done, pain points, goals, context

### Customer Segments
**Location**: `docs/design/{feature-name}-research-{MMDDYY}/`
**File**: `{feature-name}-customer-segments.md`
**Format**: Markdown table + detailed descriptions
**Include**: Segment name, size, primary jobs, characteristics, design implications

### Design Principles
**Location**: `docs/design/{feature-name}-research-{MMDDYY}/`
**File**: `{feature-name}-design-principles.md`
**Format**: Markdown with principle + insight + example
**Include**: 3-7 principles, each with rationale from research

### Design Roadmap
**Location**: `docs/design/{feature-name}-research-{MMDDYY}/`
**File**: `{feature-name}-design-roadmap.md`
**Format**: Markdown with timeline visualization
**Include**: Prioritized initiatives, rationale, timeline, success metrics

### Research Discussion Guide
**Location**: `docs/design/{feature-name}-research-{MMDDYY}/`
**File**: `{feature-name}-research-discussion-guide.md`
**Format**: Markdown with timing and question flow
**Include**: Sections for intro, context, deep dive, closing

## Examples

### Good Research Question Progression
❌ **Poor**: "What do users want?"
✅ **Better**: "What job are users hiring our checkout for, and what's preventing them from completing it?"

❌ **Poor**: "Is the UI confusing?"  
✅ **Better**: "At what point in the flow do users get stuck, and what are they trying to accomplish when it happens?"

### Good Persona Example (Excerpt)
```markdown
## Sarah Chen - The Efficiency Seeker

![Photo: Professional woman, 30s, laptop]

> "I need to get in, get my answer, and get back to my actual work. Every extra click costs me time I don't have."

**Role**: Marketing Manager at mid-size SaaS company
**Primary Jobs**:
1. Quickly generate reports for stakeholder meetings (weekly)
2. Compare campaign performance across channels (daily)
3. Identify trending content topics (monthly)

**Pain Points**:
- Current tool requires 8 clicks to get to the data she needs
- Switching between multiple dashboards wastes 15+ minutes per session
- Can't customize views, so she recreates the same reports manually

**Success Looks Like**: 
"Open app, see my key metrics immediately, export what I need in under 2 minutes."
```

## Common Pitfalls to Avoid

### ❌ Research Without Clear Questions
**Problem**: Gathering data without knowing what decisions it should inform
**Instead**: Start with "What do we need to decide?" then ask "What must we learn to decide?"

### ❌ Personas That Are Just Demographics
**Problem**: "Sarah, 34, lives in Seattle, likes yoga" tells designers nothing useful
**Instead**: Focus on jobs, contexts, pain points, and goals that inform design decisions

### ❌ Analysis Paralysis
**Problem**: Spending weeks analyzing data without creating actionable insights
**Instead**: Set a timebox, create initial insights, plan to validate and refine

### ❌ Ignoring Negative Data
**Problem**: Only highlighting findings that support existing assumptions
**Instead**: Actively look for disconfirming evidence and edge cases

### ❌ Generic Design Principles
**Problem**: Principles like "Be simple" or "User-friendly" that could apply to anything
**Instead**: Create specific principles tied to your research insights and project context

### ❌ Creating Artifacts That Don't Get Used
**Problem**: Beautiful personas that sit in a deck and never inform decisions
**Instead**: Make artifacts scannable, actionable, and reference them in design reviews

### ❌ Skipping Context
**Problem**: Understanding what users do without understanding when/why
**Instead**: Always ask about the circumstances that trigger the job-to-be-done

## Integration Points

### Inputs from Other Teams
- **Product/PM**: Product requirements, business goals, success metrics
- **Data/Analytics**: Usage data, conversion metrics, user behavior patterns
- **Support/Sales**: Customer pain points, common questions, feature requests

### Outputs for Other Skills
- **Design Concepts**: Personas, design principles, key insights to inform concepts
- **Design QA**: User needs context to assess impact of implementation issues
- **Product/PM**: Prioritized opportunities, user segments, roadmap recommendations
- **Engineering**: Context on user needs that inform technical decisions

## Tips for Best Results

1. **Always start by asking what the user already has** - don't recreate existing research
2. **Use real user quotes liberally** - they bring insights to life and build empathy
3. **Create visual representations** when possible - journey maps, flow diagrams
4. **Tie everything back to jobs-to-be-done** - this keeps research actionable
5. **Be specific about confidence levels** - note when insights need more validation
6. **Make artifacts scannable** - use headers, bullets, bold key insights
7. **Include "So what?"** - always answer why each insight matters for design

## Validation Checklist

Before delivering research artifacts, verify:
- [ ] Each insight ties to specific user data or quotes
- [ ] Personas represent distinct jobs-to-be-done, not just demographics
- [ ] Design principles are specific enough to resolve design debates
- [ ] Roadmap priorities are justified by research findings
- [ ] All deliverables are in markdown format in the project's `docs/design/` directory
- [ ] Artifacts are scannable and actionable for designers
- [ ] Sources are cited for all data and quotes
- [ ] Next steps or open questions are clearly identified
