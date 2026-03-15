---
name: create-prd
description: Create comprehensive Product Requirements Documents (PRD) from high-level product ideas with structured market analysis, feature definition, and success metrics for both greenfield and brownfield contexts. Use when defining product vision for new projects (greenfield) or formalizing requirements for existing systems (brownfield).
acceptance:
  - prd_complete: "PRD document created with all required sections"
  - features_prioritized: "Features prioritized using MoSCoW method (Must/Should/Could/Won't)"
  - success_metrics_defined: "Success criteria and KPIs clearly defined"
  - user_personas_documented: "Target users and personas identified"
  - ready_for_architecture: "PRD ready for architecture phase or epic breakdown"
inputs:
  product_name:
    type: string
    required: true
    description: "Name of the product or feature"
  product_vision:
    type: string
    required: true
    description: "High-level vision and value proposition"
  problem_statement:
    type: string
    required: true
    description: "Problem this product solves"
  target_users:
    type: string
    required: false
    description: "Target user personas or segments"
  business_objectives:
    type: string
    required: false
    description: "Business goals and objectives"
  success_metrics:
    type: string
    required: false
    description: "Initial success metrics or KPIs"
  competitive_landscape:
    type: string
    required: false
    description: "Competitive context and differentiation"
  project_type:
    type: string
    required: false
    description: "greenfield (new) or brownfield (existing system). Defaults to greenfield."
    default: "greenfield"
outputs:
  prd_created:
    type: boolean
    description: "Whether PRD was successfully created"
  prd_location:
    type: string
    description: "File path to created PRD (e.g., docs/prd.md or workspace/prds/{product-name}-prd.md)"
  feature_count:
    type: number
    description: "Number of features identified and prioritized"
  persona_count:
    type: number
    description: "Number of user personas documented"
telemetry:
  emit: "skill.create-prd.completed"
  track:
    - product_name
    - project_type
    - feature_count
    - persona_count
    - duration_ms
    - prd_location
---

# Create PRD Skill

## Purpose

Create comprehensive Product Requirements Documents (PRD) from high-level product ideas. This skill guides systematic requirements gathering, market analysis, feature definition, and success metrics documentation to produce PRDs ready for architecture design or epic breakdown.

**Core Principles:**
- Structured requirements elicitation
- Market-driven feature prioritization
- Clear success metrics and KPIs
- User-centric design approach
- Supports both greenfield (new products) and brownfield (existing systems) contexts

## Prerequisites

- Product vision or initial concept defined
- Access to stakeholder input (if available)
- Understanding of target market and users
- workspace/ directory exists for PRD storage

---

## Workflow

### Step 1: Requirements Gathering

**Action:** Elicit product vision, objectives, and constraints through structured inquiry.

**Key Activities:**
1. **Product Vision & Value Proposition**
   - What problem does this solve?
   - What value does it provide to users?
   - What makes it unique or different?

2. **Target Users & Personas**
   - Who are the primary users?
   - What are their goals, needs, pain points?
   - What user segments exist?

3. **Business Objectives**
   - What are the business goals?
   - How does this align with strategy?
   - What's the expected ROI or impact?

4. **Constraints & Considerations**
   - Timeline constraints
   - Budget limitations
   - Technical constraints
   - Regulatory requirements
   - Team capabilities

**Example Questions:**
```
- "What problem are we solving for users?"
- "How will users discover and access this?"
- "What success looks like in 6 months?"
- "What are we explicitly NOT building?"
```

**Output:** Core requirements documented (vision, users, objectives, constraints)

**See:** `references/elicitation-guide.md` for comprehensive elicitation techniques

---

### Step 2: Market Analysis

**Action:** Analyze competitive landscape and market positioning.

**Key Activities:**
1. **Competitive Landscape**
   - Who are the direct competitors?
   - Who are indirect competitors or alternatives?
   - What are their strengths/weaknesses?

2. **Market Positioning**
   - How do we differentiate?
   - What's our unique value proposition?
   - What market segment do we target?

3. **Go-to-Market Considerations**
   - Distribution channels
   - Pricing strategy (if applicable)
   - Marketing approach
   - Launch strategy

4. **Market Trends**
   - Relevant industry trends
   - Technology trends
   - User behavior trends

**Example Analysis:**
```
Competitive Landscape:
- Direct: [Competitor A] (strength: enterprise features, weakness: poor UX)
- Indirect: [Alternative B] (users use spreadsheets instead)

Differentiation:
- Simple, intuitive UX (vs competitor complexity)
- Mobile-first design (vs desktop-only competitors)
- AI-powered automation (unique capability)
```

**Output:** Market analysis section for PRD

**See:** `references/market-analysis-template.md` for detailed framework

---

### Step 3: Feature Definition

**Action:** Define and prioritize features using MoSCoW method.

**Key Activities:**
1. **Identify Core Features**
   - What must the product do? (Must-haves)
   - What should it do? (Should-haves)
   - What could it do? (Could-haves)
   - What won't it do? (Won't-haves)

2. **Feature Specifications**
   - Brief description of each feature
   - User value/benefit
   - Dependencies between features
   - Technical complexity estimate (if known)

3. **MoSCoW Prioritization**
   - **Must Have:** Critical features, MVP blockers
   - **Should Have:** Important but not launch blockers
   - **Could Have:** Nice-to-haves, future enhancements
   - **Won't Have:** Explicitly out of scope

4. **Feature Validation**
   - Does each feature solve user problem?
   - Is each feature aligned with objectives?
   - Are must-haves achievable within constraints?

**Example Feature Definition:**
```
MUST HAVE (MVP):
1. User Registration & Login
   - Users can create accounts with email/password
   - Enables personalization and data security
   - Depends on: Database, authentication service

2. Dashboard Overview
   - Users see key metrics at a glance
   - Provides immediate value on login
   - Depends on: Data collection, visualization

SHOULD HAVE:
3. Advanced Filtering
   - Users can filter data by multiple criteria
   - Improves data discovery
   - Depends on: Dashboard, search infrastructure

COULD HAVE:
4. Data Export (CSV, PDF)
   - Users can export reports
   - Convenience feature, not core value
   - Depends on: Dashboard, report generation

WON'T HAVE (v1):
5. Real-time Collaboration
   - Out of scope for v1, planned for v2
   - Significant technical complexity
```

**Output:** Prioritized feature list with specifications

**See:** `references/moscow-prioritization-guide.md` for detailed prioritization framework

---

### Step 4: Success Metrics

**Action:** Define measurable success criteria and KPIs.

**Key Activities:**
1. **User Adoption Metrics**
   - Sign-ups, active users (DAU/MAU/WAU)
   - User retention (D1, D7, D30 retention)
   - User engagement (sessions, time-on-site)
   - Feature adoption rates

2. **Business Impact Metrics**
   - Revenue (if applicable)
   - Conversion rates
   - Cost savings
   - Market share
   - Customer satisfaction (NPS, CSAT)

3. **Technical Performance Metrics**
   - Page load time
   - API response time
   - Uptime/availability
   - Error rates
   - Scalability metrics

4. **Success Criteria**
   - Specific targets for each metric
   - Timeframes for achievement
   - How metrics will be measured
   - Baseline vs target values

**Example Success Metrics:**
```
USER ADOPTION:
- 1,000 sign-ups in first month
- 60% D7 retention
- 40% MAU engagement

BUSINESS IMPACT:
- 70% conversion rate (free → paid)
- NPS score >40
- $100K ARR by month 6

TECHNICAL PERFORMANCE:
- <2s page load time (p95)
- 99.9% uptime SLA
- <1% error rate
```

**Output:** Success metrics and KPIs documented

**See:** `references/success-metrics-framework.md` for comprehensive metrics catalog

---

### Step 5: PRD Document Generation

**Action:** Compile all gathered information into comprehensive PRD document.

**Document Structure:**
1. **Executive Summary**
   - Product overview (1-2 paragraphs)
   - Problem statement
   - Value proposition
   - Target users

2. **Product Vision & Objectives**
   - Vision statement
   - Business objectives
   - Success criteria

3. **User Personas & Stories**
   - Persona definitions
   - User journeys
   - Key use cases

4. **Market Analysis**
   - Competitive landscape
   - Market positioning
   - Differentiation strategy

5. **Feature Specifications**
   - Prioritized feature list (MoSCoW)
   - Feature descriptions and user value
   - Dependencies and relationships

6. **User Flows & Journeys**
   - Key user flows
   - Entry points and conversions
   - Edge cases

7. **Non-Functional Requirements**
   - Performance requirements
   - Security requirements
   - Scalability requirements
   - Accessibility requirements

8. **Success Metrics & KPIs**
   - Adoption metrics
   - Business impact metrics
   - Technical metrics
   - Success criteria with targets

9. **Timeline & Milestones**
   - High-level roadmap
   - Key milestones
   - Launch criteria

10. **Assumptions & Constraints**
    - Technical assumptions
    - Business assumptions
    - Known constraints
    - Dependencies

11. **Open Questions & Risks**
    - Unresolved questions
    - Identified risks
    - Mitigation strategies

**File Location:**
- Greenfield: `docs/prd.md` or `workspace/prds/{product-name}-prd.md`
- Brownfield: `docs/brownfield-prd.md` (if updating existing system)

**Validation:**
- All required sections present
- Features prioritized with clear MoSCoW categories
- Success metrics specific and measurable
- Assumptions and risks documented
- Ready for next phase (architecture or epic breakdown)

**Output:** Complete PRD document

**See:** `references/prd-template.md` for complete PRD template with all sections

---

## Common Scenarios

### Scenario 1: Greenfield Product (New Product)

**Context:** Creating PRD for entirely new product with no existing system.

**Approach:**
- Focus on user problem and market opportunity
- Emphasize differentiation and unique value
- Start with minimal MVP features
- Plan iterative releases

**See:** `references/greenfield-examples.md` for complete examples

---

### Scenario 2: Brownfield Product (Existing System)

**Context:** Creating PRD for enhancements to existing product.

**Approach:**
- Document current state briefly
- Focus on gaps and improvements
- Consider migration and compatibility
- Balance new features with technical debt

**Note:** For comprehensive brownfield PRD generation from codebase analysis, use `create-brownfield-prd` skill instead.

---

### Scenario 3: Insufficient Information

**Context:** Stakeholders haven't provided enough detail.

**Approach:**
1. Document known information
2. Create "Assumptions" section with reasonable assumptions
3. Create "Open Questions" section with specific questions
4. Mark PRD as "DRAFT - Pending Stakeholder Input"
5. Share with stakeholders for feedback

---

### Scenario 4: Too Many Features

**Context:** Stakeholders want everything in MVP.

**Approach:**
1. Apply strict MoSCoW prioritization
2. Identify true MVP (minimum viable)
3. Create phased roadmap (v1.0, v1.1, v2.0)
4. Use data/evidence to defend prioritization
5. Escalate if stakeholder insists on unrealistic scope

**See:** `references/scope-management-guide.md` for scope negotiation strategies

---

## Best Practices

1. **Be User-Centric** - Always frame features in terms of user value, not technical implementation
2. **Keep It Clear** - Use simple language, avoid jargon, be specific and concrete
3. **Prioritize Ruthlessly** - Not everything can be "must have"; be honest about MVP scope
4. **Be Data-Driven** - Use market research, user feedback, and metrics to validate decisions
5. **Document Assumptions** - Make implicit assumptions explicit to avoid misalignment later
6. **Stay Flexible** - PRD is a living document; expect it to evolve as you learn more
7. **Cross-Reference** - Link to other documents (architecture, task specs, user research)
8. **Get Feedback** - Share early drafts with stakeholders for validation and buy-in

---

## Reference Files

- `references/elicitation-guide.md` - Techniques for gathering requirements
- `references/market-analysis-template.md` - Competitive and market analysis framework
- `references/moscow-prioritization-guide.md` - Feature prioritization methodology
- `references/success-metrics-framework.md` - Comprehensive metrics catalog
- `references/prd-template.md` - Complete PRD template with all sections
- `references/greenfield-examples.md` - Example PRDs for new products
- `references/scope-management-guide.md` - Managing scope and stakeholder expectations

---

## When to Escalate

**Escalate to stakeholders when:**
- Critical information missing (target users, business objectives)
- Conflicting requirements or priorities
- Unrealistic scope or timeline expectations
- Budget constraints conflict with must-have features
- Regulatory or compliance requirements unclear

**Escalate to architect when:**
- Technical feasibility of features uncertain
- Significant architectural decisions needed
- Integration requirements complex

**Use alternative skill when:**
- Existing codebase needs analysis → Use `create-brownfield-prd` skill
- PRD too large (>100 features) → Use `shard-document` skill after creation
- Interactive validation needed → Use `interactive-checklist` skill for PO review

---

*Part of BMAD Enhanced Planning Suite*
