---
name: requirements-elicitation
description: Systematic framework for analyzing product documents (PRDs, feature specs, user stories, roadmaps, one-pagers) to identify gaps, generate clarifying questions for PMs and engineers, and assess technical risks. This skill should be used when engineers or technical leads need to bridge PM documents and implementation by eliciting missing technical details rather than making assumptions. Use when asked to extract technical requirements, review specs, identify what's missing, or prepare clarifying questions from product documents.
license: Complete terms in LICENSE.txt
---

# Requirements Elicitation Skill

This skill provides a systematic framework for analyzing product documents and eliciting technical requirements needed for implementation. It bridges the gap between product management and engineering by identifying ambiguities, generating targeted clarifying questions, and assessing technical risks.

## Core Philosophy

**ELICIT, DON'T INVENT**

This skill is designed to identify gaps and ask questions, NOT to fill in missing details with assumptions. Engineers frequently complain that PM requirements are overly broad. This skill helps narrow and specify requirements through systematic elicitation rather than inventing technical details that aren't in the source document.

### Key Principles

1. **Identify ambiguity** - Point out where requirements are unclear or underspecified
2. **Ask targeted questions** - Generate specific, actionable questions organized by stakeholder
3. **Assess risk** - Evaluate technical risks introduced by missing requirements
4. **Avoid assumptions** - Never invent technical details (tech stack, architecture, data models) that aren't specified
5. **Stay grounded** - Always reference the source document; don't add scope or features

## When to Use This Skill

Use this skill when:
- Analyzing PRDs, feature specs, user stories, epics, roadmap docs, or one-pagers
- Asked to "extract technical requirements" from product documents
- Reviewing specs to identify what's missing from an engineering perspective
- Preparing for technical planning or estimation
- Bridging communication between PM and engineering teams
- Asked to help with requirements that seem too broad or vague

Trigger phrases:
- "Extract the technical requirements from..."
- "Review this spec and identify what's missing..."
- "My PM just gave me this PRD, help me find the technical requirements"
- "What questions should I ask about..."
- "Identify gaps in this feature spec"

## Workflow

Follow this systematic process when analyzing product documents:

### Phase 1: Initial Analysis (Always Do This First)

1. **Read the entire document** to understand the feature and its context
2. **Identify what IS specified** - Note the parts that are clear and well-defined
3. **Load the technical dimensions checklist** from `references/technical_dimensions.md`
4. **Systematically review** the document against each dimension in the checklist
5. **Document gaps** - Create a list of areas where critical details are missing

### Phase 2: Question Generation

1. **Load question templates** from `references/question_templates.md`
2. **Organize questions by stakeholder**:
   - **Questions for PM**: Product intent, user expectations, business rules, scope
   - **Questions for Engineering**: Technical decisions, architecture, implementation approach
3. **Make questions specific** - Reference concrete scenarios from the document
4. **Explain why each question matters** - Brief technical context for impact
5. **Avoid assumption-laden questions** - Don't ask "Should we use Redis for caching?" if caching wasn't mentioned

### Phase 3: Risk Assessment

1. **Load risk framework** from `references/risk_assessment.md`
2. **Identify risks** in categories: Implementation, Performance, Security, Data Integrity, Integration, Operations, UX, Compliance
3. **Assign severity levels** - Critical (blocks work), High (needs assumptions), Medium (creates uncertainty), Low (can resolve later)
4. **Link risks to gaps** - Show how missing requirements create specific risks
5. **Prioritize clarification** - Help stakeholders understand what must be resolved vs what's nice-to-have

### Phase 4: Output Creation

Based on the analysis depth needed, create appropriate outputs:

**For quick reviews** (5-10 minutes):
- Brief summary of critical gaps
- Top 5-10 most important questions
- High-level risk assessment

**For thorough analysis** (20-30 minutes):
- Complete gap analysis using `assets/gap_analysis_template.md`
- Comprehensive questions document using `assets/clarifying_questions_template.md`
- Detailed risk assessment with all severity levels

**Output format options:**
- Markdown document (most common)
- Inline response (for quick reviews)
- Presentation format (for stakeholder meetings)

### Phase 5: Post-Clarification (Only After Conversation)

After questions have been answered and gaps filled through discussion:

1. **Technical Specification** - Now create detailed tech specs with actual technical decisions
2. **Implementation Stories** - Break down into stories with acceptance criteria
3. **API Contracts** - Define interfaces and data models based on clarified requirements
4. **Architecture Decisions** - Document technical approach with rationale

**CRITICAL:** Do not create these detailed technical artifacts in Phase 1-4. Only create them after the elicitation conversation has filled in the gaps.

## Reference Files

### `references/technical_dimensions.md`
Comprehensive checklist of technical aspects to consider:
- Data & State Management
- Interfaces & Integration
- Performance & Scale
- Security & Privacy
- Reliability & Operations
- Business Logic & Rules
- Dependencies & Constraints
- User Experience & Behavior
- Testing & Validation

**When to use:** During Phase 1 (Initial Analysis) to systematically review all technical dimensions.

### `references/question_templates.md`
Templates for structuring questions and examples of effective elicitation:
- Question structuring principles
- Categories of questions by audience (PM vs Engineering)
- Good vs bad requirements analysis examples
- Common requirement anti-patterns
- Output structure templates

**When to use:** During Phase 2 (Question Generation) to formulate clear, actionable questions.

### `references/risk_assessment.md`
Framework for identifying and categorizing technical risks:
- Risk categories (Implementation, Performance, Security, Data, Integration, Operations, UX, Compliance)
- Severity levels (Critical, High, Medium, Low)
- Risk identification process
- Common risk patterns
- Communication guidelines

**When to use:** During Phase 3 (Risk Assessment) to evaluate technical risks introduced by requirement gaps.

## Asset Files

### `assets/gap_analysis_template.md`
Comprehensive template for documenting requirements gaps:
- Executive summary with readiness assessment
- Critical gaps that block implementation
- Technical dimensions analysis
- Risk assessment
- Assumptions to validate
- Recommended next steps

**When to use:** For thorough analysis where a formal gap analysis document is needed.

### `assets/clarifying_questions_template.md`
Structured template for organizing questions by stakeholder:
- Sections for PM questions vs Engineering questions
- Space for discussion notes
- Follow-up action items

**When to use:** When preparing questions for review meetings or async communication with stakeholders.

## Examples

### Example 1: Quick Review

**User Request:**
"Review this feature spec and identify what's missing from an engineering perspective: [attaches document about adding social login]"

**Good Response Process:**
1. Read document noting it mentions "users can log in with social providers"
2. Review technical dimensions checklist
3. Generate targeted questions:
   - For PM: Which social providers? Account linking behavior? Auto-create accounts?
   - For Engineering: Where to store OAuth tokens? Session management strategy? Integration with current auth?
4. Note risks: Missing security details (HIGH), unclear user flow (MEDIUM)
5. Output concise list of questions and risks inline

**Bad Response Process:**
❌ Immediately jumping to: "You'll need to implement OAuth 2.0 with Google and Facebook, store JWT tokens in localStorage..."

### Example 2: Thorough Analysis

**User Request:**
"My PM just gave me this PRD for a notification system. Help me find the technical requirements."

**Good Response Process:**
1. Read entire PRD about notifications
2. Load `references/technical_dimensions.md` and systematically check each dimension
3. Load `references/question_templates.md` for structuring
4. Identify gaps: trigger logic undefined, delivery channels unspecified, no performance requirements, missing error handling
5. Load `references/risk_assessment.md` and categorize risks
6. Create documents using both templates:
   - `gap_analysis_template.md` filled with findings
   - `clarifying_questions_template.md` with organized questions
7. Output both documents

**Bad Response Process:**
❌ Creating a full technical specification with "We'll use Firebase for push, SendGrid for email, notifications triggered by database updates..."

### Example 3: Scope Clarification

**User Request:**
"Extract technical requirements from this one-pager about search functionality"

**Good Response Process:**
1. Read one-pager noting it says "users can search transactions"
2. Identify it lacks: searchable fields, matching behavior, performance targets, result ordering
3. Ask questions: "What fields are searchable?" "Exact or fuzzy matching?" "Expected data volume?" "Acceptable latency?"
4. Note risks: Performance risk (no volume/latency specified), UX risk (result display undefined)
5. Explicitly note: "I'm not assuming a search technology (Elasticsearch, etc.) since requirements don't specify performance or scale needs yet"

**Bad Response Process:**
❌ "Implement Elasticsearch with fuzzy matching, index these fields, return 25 results per page..."

## Common Pitfalls to Avoid

### 1. Inventing Technical Details
❌ "This requires a Redis cache with 15-minute TTL"
✅ "No caching strategy specified. Question for Engineering: Do we need caching? What are the performance targets?"

### 2. Assuming Tech Stack
❌ "We'll use React for the frontend and Express for the backend"
✅ "Frontend interaction model not specified. Where should this functionality live?"

### 3. Adding Scope
❌ "We should also add email notifications even though the doc only mentions push"
✅ "Document specifies push notifications. Should confirm if other channels needed."

### 4. Making Architecture Decisions
❌ "This needs a microservice with event-driven architecture"
✅ "Integration approach not specified. How should this integrate with existing systems?"

### 5. Over-Specifying Prematurely
❌ Creating detailed API contracts before clarifying questions are answered
✅ Asking "What operations need API endpoints?" and only designing APIs after answers

### 6. Ignoring What IS Specified
❌ Treating everything as a gap
✅ Acknowledging "The document clearly specifies X, Y, and Z. Gaps are in areas A, B, C."

### 7. Generic Questions
❌ "What are the requirements?"
✅ "The document mentions 'real-time updates' - does real-time mean <100ms latency or is 1-2 seconds acceptable?"

## Best Practices

### Be Specific and Concrete
- Reference exact text from the document
- Use concrete scenarios: "What happens when..." not "How does this work?"
- Quantify when possible: "How many users?" not "What's the scale?"

### Organize Clearly
- Group questions by stakeholder (PM vs Engineering)
- Categorize by dimension (Data, Security, Performance, etc.)
- Prioritize by criticality (Critical > High > Medium > Low)

### Explain Impact
- For each question, briefly explain why it matters technically
- Connect gaps to specific risks
- Help stakeholders understand prioritization

### Stay Objective
- Avoid judging the document quality
- Focus on what's needed for implementation
- Be helpful, not critical

### Know When to Transition
- Phase 1-4: Focus on elicitation (questions and gaps)
- Phase 5: Only after gaps are filled, create detailed specs
- Don't create technical artifacts prematurely

### Use Templates Appropriately
- Quick reviews: Inline response with key questions
- Formal analysis: Use both templates for comprehensive documentation
- Async communication: Clarifying questions template
- Stakeholder presentations: Gap analysis template

## Adapting to Document Types

### PRDs (Product Requirements Documents)
- Usually most comprehensive, but watch for missing technical details
- Focus on data models, APIs, performance, security
- Good source for business rules and user flows

### Feature Specs
- Often focused on user-facing behavior
- May lack backend/integration details
- Check for error handling, edge cases, data consistency

### User Stories / Epics
- Typically brief, expect many gaps
- Focus on acceptance criteria and edge cases
- Need to elicit technical approach entirely

### Roadmap Documents
- Highest level, least detail
- Focus on scope clarification and feasibility
- Identify large unknowns early

### One-Pagers
- Very brief, expect significant gaps
- Start with understanding goals and constraints
- May need follow-up documents before technical planning

## Success Criteria

A successful requirements elicitation produces:

1. **Clear gap identification** - Stakeholders understand what's missing
2. **Actionable questions** - Questions can be directly answered
3. **Risk visibility** - Technical risks are surfaced and prioritized
4. **No false assumptions** - Technical details only included if in source document
5. **Efficient communication** - Engineers and PMs aligned on what needs clarification
6. **Implementation readiness** - After clarification, team can confidently estimate and implement

The goal is not a perfect requirements document - it's identifying exactly what questions need answering to get there.
