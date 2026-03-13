---
name: create-prd
description: Use when creating a Product Requirements Document from a conversation or feature request through structured context gathering
---

# Create PRD: Generate Product Requirements Document

## Overview

Generate a comprehensive Product Requirements Document (PRD) through strict context gathering, API research, and structured documentation. This command produces a production-ready PRD serving as the single source of truth for implementation.

**Output File**: `$ARGUMENTS` (default: `PRD.md` in project root)

---

## ⚠️ CRITICAL INSTRUCTIONS

**DO NOT CREATE THE PRD UNTIL YOU HAVE COMPLETE CONTEXT**

**Workflow**:
1. **Discover** project type and scope through targeted questions
2. **Research** external APIs/SDKs if applicable (mandatory, not optional)
3. **Gather** all required information - ask questions until complete
4. **Confirm** with user before writing
5. **Write** PRD using appropriate template
6. **Backup** existing file if one exists

**Principles**:
- ❌ **No assumptions** - ask instead of guessing
- ❌ **No placeholder sections** - complete or explicitly skipped by user
- ✅ **Complete context first** - gather all info before writing
- ✅ **Research external dependencies** - understand APIs before documenting

---

## STEP 1: PROJECT TYPE & CONTEXT DISCOVERY

**Required Questions** - Ask the user:

1. **Project Type**: AI Agent / Web App / API/Service / Library/Package / CLI Tool / Desktop App / Mobile App / Other
2. **Core Functionality**: In 2-3 sentences, what does this product do?
3. **Target Users**: Who will use this? Technical level?
4. **MVP Scope**: What must be in first version vs. later?
5. **Technology Preferences**: Required/preferred technologies?
6. **External Dependencies**: External APIs, services, or SDKs?
7. **Deployment Context**: How deployed/distributed?
8. **Existing Documentation**: Related docs or research?

**Do not proceed without**:
- ✓ What you're building (type + core function)
- ✓ Who it's for (target users)
- ✓ What's in scope for MVP
- ✓ What external dependencies exist

---

## STEP 2: API RESEARCH (IF APPLICABLE)

**Mandatory if external APIs or unfamiliar SDKs involved.**

### Identify & Determine Research Needs

List all external APIs/SDKs, then **ask user for each**:
```
This project integrates with [API name].

Options:
1. Do you have existing research documents? (provide paths)
2. Should I research [API name] before creating PRD?
3. Skip research and document based on current knowledge (not recommended for unfamiliar APIs)

Your preference?
```

### Conduct Research

For each API requiring research:
1. **Execute**: `/explore-api [API name]`
2. **Read**: `.agents/research/[api]-research.md`
3. **Verify**: POC tests passed

### Critical Verification Requirements

**For EVERY external API/service, research MUST verify:**

1. **Feasibility**: Is what we want to achieve **technically possible** with this API?
   - Does the API provide the required features/endpoints?
   - Are there version/compatibility constraints?
   - Are there known limitations that block our use case?

2. **Allowability**: Is what we want to achieve **permitted** by the service?
   - Rate limits sufficient for our needs?
   - API tier/plan supports required features?
   - Terms of Service allow our intended use?
   - Geographic/regulatory restrictions?

3. **Setup Requirements**: What external setup is needed?
   - Account creation/API key generation steps
   - Dashboard/console configuration
   - Webhooks or callback URL setup
   - OAuth app registration
   - Service-specific prerequisites

**Do not proceed without**:
- ✓ User confirmation on research approach
- ✓ Completed API research (if chosen)
- ✓ Research documents read (if provided)
- ✓ **Feasibility verified** (we CAN do what we want)
- ✓ **Allowability verified** (we're ALLOWED to do what we want)
- ✓ **Setup requirements documented** (we know HOW to configure it)

---

## STEP 3: GATHER COMPLETE REQUIREMENTS

### Information Gathering Strategy

For each template section:
1. Check conversation history for details
2. Ask specific questions for missing info
3. Confirm understanding before next section
4. Mark sections to skip (with explicit confirmation)

### Required Information Checklist

**Business Context**:
- [ ] Product mission and value proposition
- [ ] Target user personas and needs
- [ ] MVP success criteria

**Technical Context**:
- [ ] Technology stack with versions
- [ ] Architecture approach and patterns
- [ ] External API integrations (with research if applicable)
- [ ] Security and configuration

**Scope Definition**:
- [ ] In-scope features for MVP
- [ ] Explicit out-of-scope items
- [ ] User stories with examples
- [ ] Implementation phases with parallelization strategy

**Parallel Execution Design**:
- [ ] Workstream boundaries identified
- [ ] Interface contracts between teams defined
- [ ] Shared context and dependencies mapped
- [ ] Integration checkpoints planned
- [ ] Mock/stub strategies for blocked work

**Risk Management**:
- [ ] 3-5 key risks identified
- [ ] Mitigation strategy per risk
- [ ] API integration risks (if applicable)

### Example Questions (Adapt to Project Type)

**AI Agents**: Tools/capabilities? Registration pattern? Conversation flow? Result presentation?
**Web Apps**: User workflows? Frontend framework? API design? Auth requirements?
**APIs/Services**: Endpoints? Request/response formats? Rate limiting? Versioning?
**Libraries**: Public API surface? Installation? Usage examples? Dependencies?
**Universal**: Error handling? Logging? Tests (unit/integration/e2e)? Documentation?

**Parallel Execution Planning**:
- Can frontend and backend be built concurrently?
- What shared interfaces/contracts need to be defined first?
- Which components have no dependencies and can start immediately?
- What mock/stub strategies enable parallel development?
- Where are the integration points that require synchronization?

---

## STEP 4: FILE HANDLING & PRD CREATION

### Backup Existing PRD

If PRD exists:
```bash
mv PRD.md PRD.backup-$(date +%Y%m%d-%H%M%S).md
```

### Confirm Before Writing

```
Ready to create PRD:
- Project Type: [type]
- Target File: [path]
- API Research: [completed/skipped/N/A]
- Sections: [number]
- Skipped: [list or "none"]

Proceed? (y/n)
```

---

## PRD TEMPLATE STRUCTURE

Follow this hierarchical structure. Adapt sections based on project type.

### Section Format

Each section below shows:
- **Req**: Required/Optional
- **Format**: Markdown syntax
- **Examples**: For different project types (AI Agent, Web App, API, Library)

---

### `# Product Requirements Document: [Product Name]`

**Req**: Yes | **Format**: H1 with "Product Requirements Document: " prefix

---

### `## Executive Summary`

**Req**: Yes | **Format**: H2, 2-3 paragraphs

**`[Product Name]` - [One-liner]**
- AI Agent: `**Paddy** is an AI agent enabling Obsidian users to interact with vaults using natural language.`
- Web App: `**TaskFlow** is a collaborative PM app helping remote teams coordinate through task boards and async video.`
- API: `**PaymentHub** is a unified payment API abstracting multiple providers behind one interface.`

**`MVP Goal:` [One sentence]**
- AI Agent: Enable vault query/management through natural language with user's choice of LLM.
- Web App: Allow teams to create task boards and share video updates without real-time presence.

---

### `## Mission`

**Req**: Yes | **Format**: H2, 1-2 sentences

**`### Core Principles`** - Numbered list with bold names

```markdown
1. **[Principle]** - [Explanation]
2. **[Principle]** - [Explanation]
3. **[Principle]** - [Explanation]
```

---

### `## Target Users`

**Req**: Yes | **Format**: H2 with subsections

**`[User Group]` who want to:**
- Bullet list of goals

**`Technical Comfort Level:`** [Description]

---

### `## MVP Scope`

**Req**: Yes | **Format**: H2 with H3 subsections

**`### In Scope`** - Categorized bullets:
- **Core Functionality**: User-facing features
- **Technical**: Implementation details
- **Integration**: Third-party tools (if applicable)
- **Deployment**: Packaging/distribution

**`### Out of Scope (Future Considerations)`** - Bullet list

---

### `## User Stories`

**Req**: Yes | **Format**: H2 with H3 subsections

**`### Primary User Stories`** - Numbered list:

```markdown
1. **As a [role], I want to [action]**, so that [benefit].
   - Example: "[concrete example]"
```

**`### Technical User Stories`** - Same format (optional)

---

### `## Core Architecture & Patterns`

**Req**: Yes | **Format**: H2 with H3 subsections

**`### Architecture`**
- Architecture style/pattern name
- High-level description
- Directory structure (code block)

**`### Key Patterns`** - Numbered, bold-labeled:

```markdown
**1. [Pattern]**
- [Description]
- [Code example if helpful]
```

---

### `## Tools` (AI Agents) OR `## Features` (Others)

**Req**: Yes | **Format**: H2 with H3 per tool/feature

**For AI Agents**:
```markdown
### Tool N: `tool_name`

**Purpose:** [What it does]
**Operations:**
- [Operation 1]
- [Operation 2]

**Key Features:**
- [Notable feature 1]
```

**For Other Products**:
```markdown
### Feature N: [Name]

**Description:** [What users get]
**Components:**
- [Component 1]

**User Experience:**
- [Interaction pattern]
```

---

### `## Technology Stack`

**Req**: Yes | **Format**: H2 with H3 per category

```markdown
### [Category]

- **[Tool]** (version) - [Purpose]
```

Categories: Backend / Frontend / Database / Infrastructure / Testing

---

### `## Parallel Execution Architecture`

**Req**: Yes | **Format**: H2 with H3 subsections

**Purpose**: Enable independent team/agent workstreams to execute concurrently

```markdown
## Parallel Execution Architecture

### Team Structure

**Workstream Teams:**
- **Team A - [Name]**: [Responsibility scope]
  - Focus: [What they build]
  - Expertise: [Required skills]
  - Works with: [Other teams they depend on]

- **Team B - [Name]**: [Responsibility scope]
  - Focus: [What they build]
  - Expertise: [Required skills]
  - Works with: [Other teams]

### Interface Contracts

**CRITICAL**: These contracts enable parallel development

#### Contract 1: [Name] (Team A → Team B)

**Provider:** Team A
**Consumer:** Team B

**Interface Definition:**
```[language]
# API endpoint, data schema, or contract definition
```

**Delivery Timeline:** [When available for consumption]
**Mock Strategy:** [How Team B can work before Team A completes]

#### Contract 2: [Name]

[Repeat structure for each interface]

### Shared Context

**What ALL teams must know:**
- [Global architectural decision 1]
- [Global constraint 1]
- [Naming convention 1]

**Central Configuration:**
```[language]
# Shared config that all teams use
```

### Synchronization Points

**Integration Checkpoint 1:** [When]
- **Participants:** Teams A, B, C
- **Purpose:** [What gets validated]
- **Success Criteria:** [How to verify integration works]

**Integration Checkpoint 2:** [When]
- [Repeat structure]

### Dependency Graph

```
Phase 1 (Parallel)
├── Workstream A: [Independent]
├── Workstream B: [Independent]
└── Workstream C: [Independent]
    ↓
Phase 2 (After Phase 1 completes)
├── Workstream D: [Depends on A, B]
└── Workstream E: [Depends on C]
    ↓
Phase 3 (Final Integration)
└── Workstream F: [Depends on D, E]
```

### Risk Mitigation for Parallel Work

**Risk:** [Parallel workstreams diverge or create conflicts]
**Mitigation:**
- [Strategy 1 - e.g., daily integration tests]
- [Strategy 2 - e.g., shared type definitions]

**Risk:** [Blocked waiting for dependencies]
**Mitigation:**
- [Strategy - e.g., mock implementations, contract-first development]
```

---

### `## Security & Configuration`

**Req**: Yes | **Format**: H2 with H3/H4 subsections

**`### Authentication`** (if applicable)
```markdown
#### **[Method]:** [Details]
[Explanation paragraph or bullets]
```

**`### Deployment Method & Data Access`** (if applicable)
```markdown
#### **[Mechanism]:**
[Description]

#### **How It Works:**
1. [Step 1]
2. [Step 2]

#### **Security Benefits:**
- [Benefit 1]
```

**`### Configuration Management`**
```markdown
#### **Environment Variables (`.env`):**
```[language]
# Variables
```

#### **[Orchestration] Configuration:**
```[language]
# Config file
```

#### **Configuration Class:**
```[language]
# Settings code
```
```

**`### Security Scope`**
```markdown
#### **In Scope:**
- [Measure 1]

#### **Out of Scope (Keep Simple):**
- [Excluded 1]
```

---

### `## API Specification`

**Req**: If applicable | **Format**: H2 with H3 sections

**`### External API Integrations`** (if applicable) - H4 per API:

```markdown
#### API: [Name] v[Version]

**Documentation:** [URL]
**Research Document:** `.agents/research/[api]-research.md` (if applicable)
**Purpose:** [Why used]
**Authentication:** [Method]

**Supported Features:**
- [Feature X]: ✓ Supported via [method]
- [Feature Y]: ✗ Not supported - Alternative: [approach]

**Integration Pattern:**
```[language]
# Init, usage, error handling examples
```

**Compatibility Notes:**
- [Requirement/limitation]

**Validation Strategy:**
- POC: [Description]
- Expected: [Success criteria]
- Fallback: [Alternative]
```

**`### Internal Endpoints`** (if applicable) - H4 per endpoint:

```markdown
#### Endpoint: `[METHOD] [PATH]`

**Purpose:** [What it does]

**Request:**
```[language]
[Example]
```

**Response:**
```[language]
[Example]
```

**Authentication:** [How]
**Error Responses:**
- `[Code]`: [Condition]
```

---

### `## Success Criteria`

**Req**: Yes | **Format**: H2 with H3

**`### MVP Success Definition`** - Three bold-labeled lists:

```markdown
**Functional Requirements:**
- [Must work 1]

**Quality Indicators:**
- [Quality bar 1]

**User Experience:**
- [UX goal 1]
```

---

### `## Implementation Phases`

**Req**: Yes | **Format**: H2 with H3 per phase

**CRITICAL FOR PARALLEL EXECUTION**: Each phase must include:
- **Parallelization Strategy**: Which workstreams can run concurrently
- **Team Assignments**: Suggested agent roles for each workstream
- **Dependencies**: What must complete before this phase starts
- **Integration Points**: Where parallel work synchronizes
- **Handoff Artifacts**: What each workstream delivers to others

```markdown
### Phase 1: [Name] ([Period])

**CRITICAL FOR EXTERNAL DEPENDENCIES:**
If project uses external APIs/services, Phase 1 MUST include:
- **External Service Setup**: Complete all account creation, API key generation, dashboard configuration
- **External Service Verification**: Test that ALL external services work as expected with our requirements
- **Fallback Planning**: Document what to do if external service setup/verification fails

**Goal:** [One sentence]

**Parallelization Strategy:**
- **Concurrent Workstreams**: [Number] independent workstreams
- **Can Start After**: External service verification passes (if applicable), or "Day 1" (if no external dependencies)

**Workstreams:**

#### Workstream A: External Service Setup & Verification (If Applicable)
**Assigned To:** integration-specialist
**Dependencies:** None - must happen FIRST
**Deliverables:**
- All external API accounts created and configured
- API keys/credentials securely stored
- Dashboard/console settings configured
- Connectivity tests passing
- Feature compatibility verified

**Setup Tasks:**
- Create accounts on [Service A], [Service B]
- Generate API keys and store in secure config
- Configure webhooks/callbacks if needed
- Set up OAuth apps if needed
- Test basic API connectivity

**Verification Tests:**
```bash
# Test each external service
# Verify required features are accessible
# Confirm rate limits and quotas are sufficient
```

**Critical Checkpoints:**
- [ ] All external services accessible with credentials
- [ ] Required API features verified as available
- [ ] No blocking compatibility issues discovered
- [ ] Setup documented for team reference

**If Verification Fails:**
- Document the blocker (missing feature, access denied, etc.)
- Evaluate alternatives (different API tier, alternative service)
- Update implementation plan OR escalate for requirement changes
- DO NOT PROCEED to Phase 2 until resolved

#### Workstream B: [Name]
**Assigned To:** [Agent role - e.g., backend-specialist, frontend-specialist, test-specialist]
**Dependencies:** [Workstream A if external APIs involved / None otherwise]
**Deliverables:**
- [Item 1]
- [Item 2]

**Integration Points:**
- **Provides to Workstream C**: [API contract, data schema, etc.]
- **Receives from Workstream A**: [Verified external service access, configuration]

**Validation:**
```bash
# Commands to verify this workstream's completion
```

#### Workstream C: [Name]
**Assigned To:** [Agent role]
**Dependencies:** [Workstream dependencies]
**Deliverables:**
- [Item 1]

**Integration Points:**
- **Provides to**: [What it delivers]
- **Receives from**: [What it needs]

**Validation:**
```bash
# Commands to verify completion
```

**Phase 1 Integration Test:**
```bash
# Commands to verify all workstreams integrate correctly
# MUST include external service integration tests if applicable
```

---

### Phase N: [Name] ([Period])

**Goal:** [One sentence]

**Parallelization Strategy:**
- **Concurrent Workstreams**: [Number] independent workstreams
- **Can Start After**: Phase [X] completes (or "Day 1" if no dependencies)

**Workstreams:**

#### Workstream A: [Name]
**Assigned To:** [Agent role]
**Dependencies:** [None / Workstream X from Phase Y]
**Deliverables:**
- [Item 1]
- [Item 2]

**Integration Points:**
- **Provides to Workstream B**: [API contract, data schema, etc.]
- **Receives from Workstream C**: [Configuration, endpoints, etc.]

**Validation:**
```bash
# Commands to verify this workstream's completion
```

**Phase Integration Test:**
```bash
# Commands to verify all workstreams integrate correctly
```
```

---

### `## Future Considerations (Post-MVP)`

**Req**: Yes | **Format**: H2 with three bold-labeled lists

```markdown
**Potential Enhancements:**
- [Enhancement 1]

**Integration Opportunities:**
- [Integration 1]

**Advanced Features:**
- [Feature 1]
```

---

### `## Risks & Mitigations`

**Req**: Yes | **Format**: H2 with H3 per risk

```markdown
### Risk: [Name]

**Mitigation:**
- [Strategy 1]
- [Strategy 2]
```

**Include API-specific risks if external APIs used.**

---

### `## Appendix`

**Req**: Optional | **Format**: H2 with H3 subsections

**`### Related Documents`** - Bullet list of links
**`### Key Dependencies`** - Categorized links
**`### Repository Structure`** - Directory tree in code block

---

## POST-CREATION VERIFICATION

**Completeness**:
- [ ] All required sections present
- [ ] No placeholders ("[TODO]")
- [ ] User stories have examples
- [ ] Tech stack has versions
- [ ] APIs documented (if applicable)
- [ ] Phases are specific
- [ ] Risks have mitigations
- [ ] Parallel execution architecture defined
- [ ] Workstreams identified with clear boundaries
- [ ] Interface contracts specified

**Consistency**:
- [ ] Terminology consistent
- [ ] Tech choices align with architecture
- [ ] User stories support MVP scope
- [ ] Workstream boundaries align with architecture
- [ ] Interface contracts match tech stack capabilities

**Quality**:
- [ ] Executive summary concise
- [ ] Core principles actionable
- [ ] Code examples valid
- [ ] No empty sections without user approval
- [ ] API research complete (if applicable)
- [ ] Parallelization strategy maximizes team efficiency
- [ ] Integration checkpoints are testable and measurable

---

## OUTPUT CONFIRMATION

Present to user:

```
✅ PRD Created Successfully

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Product: [Product Name]
📄 File Location: [path]
📦 Project Type: [type]
🔬 API Research: [Completed/Skipped/N/A - list APIs]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 PRD Summary:
- Mission: [1-sentence]
- Target Users: [group]
- MVP Scope: [X] features in-scope, [Y] deferred
- Technology: [primary stack]
- Timeline: [duration]

⚠️  Assumptions Made: (if any)
- [Assumption 1]

📊 Next Steps:
1. Review PRD with stakeholders
2. Refine unclear sections
3. Begin planning (/plan-feature)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Notes

- Adapt section depth based on project complexity
- For technical products: emphasize architecture and stack
- For user-facing products: emphasize user stories and experience
- API research is **mandatory** for unfamiliar external integrations
- Template ensures consistency across project types
