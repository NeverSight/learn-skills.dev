---
name: bmad-synthesize
description: Auto-generate BMAD artifacts (PRD, Architecture, Epics, UX Design) from StackShift reverse-engineering docs. Three modes - YOLO (fully automatic), Guided (ask on ambiguities), Interactive (full conversation with pre-loaded context). Bridges the gap between StackShift's deep code analysis and BMAD's collaborative artifact format.
---

# BMAD Synthesize

**Auto-generate BMAD planning artifacts from StackShift reverse-engineering documentation.**

**Estimated Time:** 10-30 minutes (depending on mode)
**Prerequisites:** Gear 2 (Reverse Engineer) completed with 9+ docs
**Output:** 4 BMAD artifacts in `_bmad-output/planning-artifacts/`

---

## Compatibility

| Reverse Engineer Version | Docs Produced | Coverage |
|---|---|---|
| v2.0+ (11 docs) | Full set | 100% |
| v1.x (9 docs) | Missing business-context, decision-rationale | ~85% average |

Both are fully supported. With 9 docs, some sections will use inferred content from related docs, clearly marked with `[INFERRED FROM: source-doc]`.

---

## When to Use This Skill

Use this skill when:
- Gear 2 has generated 9+ reverse-engineering docs
- You want BMAD artifacts without running the full BMAD conversation flow
- You chose `bmad-autopilot` as the implementation framework in Gear 1
- You want to convert existing reverse-engineering docs into BMAD format
- You need a PRD, Architecture doc, Epics, or UX spec generated from code analysis

**Trigger Phrases:**
- "Generate BMAD artifacts from reverse-engineering docs"
- "Create PRD from the codebase analysis"
- "Auto-generate BMAD planning documents"
- "Synthesize BMAD artifacts"
- "Run BMAD auto-pilot"

---

## What This Skill Does

Reads all available reverse-engineering docs (9 core + 2 optional) and maps their content into 4 BMAD planning artifacts:

| BMAD Artifact | Primary Source Docs | Coverage (11 docs) | Coverage (9 docs) | Fallback Sources for Optional Docs |
|---|---|---|---|---|
| `prd.md` | functional-specification, business-context **[OPTIONAL]**, technical-debt-analysis, integration-points | ~90% | ~80% | business-context fallback: functional-specification (Executive Summary, User Stories, Success Criteria) + visual-design-system (persona UX context) |
| `architecture.md` | data-architecture, integration-points, operations-guide, decision-rationale **[OPTIONAL]**, configuration-reference, observability-requirements | ~85% | ~75% | decision-rationale fallback: configuration-reference (tech stack, framework choices) + data-architecture (schema design decisions) + integration-points (integration choice rationale) |
| `epics.md` | functional-specification (FRs grouped by domain), business-context **[OPTIONAL]** (personas), technical-debt-analysis (migration matrix) | ~75% | ~70% | business-context fallback: functional-specification (User Personas, Product Positioning) |
| `ux-design-specification.md` | visual-design-system, business-context **[OPTIONAL]** (personas), functional-specification (user stories) | ~65% | ~55% | business-context fallback: functional-specification (User Personas) + visual-design-system (user flows, accessibility) |

---

## Three Modes

### Mode 1: YOLO (Fully Automatic)

**Time:** ~10 minutes
**User input:** None

- Maps all available docs (9-11) to BMAD artifacts automatically
- For questions the docs can't answer, infers from available context
- Treats `[INFERRED]` items as accepted
- Resolves `[NEEDS USER INPUT]` items with best-effort inference
- Generates all 4 artifacts in one shot

**Best for:** Quick artifact generation, overnight runs, batch processing, when you plan to refine later.

### Mode 2: Guided (Recommended)

**Time:** ~15-20 minutes
**User input:** 5-10 targeted questions

- Auto-populates everything the docs can answer (high confidence)
- Presents targeted questions ONLY for genuinely ambiguous items:
  - Business vision refinement (from business-context.md `[NEEDS USER INPUT]` items)
  - Priority trade-offs between competing requirements
  - Persona validation (are the inferred personas correct?)
  - Architecture preferences not visible in code
  - Epic scoping decisions
- Generates all 4 artifacts with user input incorporated

**Best for:** Most projects. Good balance of speed and quality.

### Mode 3: Interactive

**Time:** ~25-30 minutes
**User input:** Full conversation

- Pre-loads all available docs (9-11) as context (you don't start from zero)
- Walks through each BMAD artifact section by section
- Shows draft content for each section, asks for approval/changes
- Most thorough, but slowest
- Essentially BMAD's collaborative flow with a massive head start

**Best for:** Critical projects, when precision matters, when you want full control.

---

## Document Mapping (Detailed)

### prd.md Generation

```
Source → BMAD PRD Section
─────────────────────────────────────────────────────────────────
business-context.md [OPTIONAL]
  ├── Product Vision           → ## Product Vision
  ├── Target Users & Personas  → ## Target Users
  ├── Business Goals           → ## Success Criteria / ## KPIs
  ├── Competitive Landscape    → ## Market Context
  ├── Stakeholder Map          → ## Stakeholders
  └── Business Constraints     → ## Constraints & Assumptions
  │
  └── [FALLBACK if missing - ~70% coverage for above sections]:
        functional-specification.md (Executive Summary → Product Vision,
          User Stories + User Personas → Target Users,
          Success Criteria → Success Criteria / KPIs,
          Product Positioning → Market Context)
        visual-design-system.md (persona UX context → Target Users supplement)

functional-specification.md
  ├── Functional Requirements  → ## FR1: Title, ## FR2: Title, ...
  ├── Non-Functional Reqs      → ## NFR1: Title, ## NFR2: Title, ...
  ├── User Stories             → Embedded in FRs as acceptance criteria
  ├── Business Rules           → ## Business Rules
  ├── System Boundaries        → ## Scope
  ├── Success Criteria         → ## Success Criteria
  ├── User Personas            → Supplements ## Target Users
  └── Product Positioning      → Supplements ## Product Vision

technical-debt-analysis.md
  ├── Migration Priority Matrix → ## Known Issues & Constraints
  └── Security Vulnerabilities  → ## NFR: Security Requirements

integration-points.md
  ├── External Services        → ## External Dependencies
  └── Auth Flows               → ## NFR: Authentication & Authorization
```

### architecture.md Generation

```
Source → BMAD Architecture Section
─────────────────────────────────────────────────────────────────
data-architecture.md
  ├── Data Models              → ## Data Models
  ├── API Endpoints            → ## API Contracts
  ├── Database ER Diagram      → ## Data Layer
  ├── JSON/GraphQL Schemas     → ## API Contracts (detail)
  └── Domain Model / Contexts  → ## Domain Model

integration-points.md
  ├── External Services        → ## External Integrations
  ├── Internal Service Deps    → ## Service Architecture
  ├── Data Flow Diagrams       → ## System Architecture Diagram
  ├── Auth Flows               → ## Authentication Architecture
  └── Webhook Integrations     → ## Event Architecture

operations-guide.md
  ├── Deployment Procedures    → ## Deployment Architecture
  ├── Infrastructure Overview  → ## Infrastructure
  ├── Scalability Strategy     → ## Scalability & Performance
  └── Monitoring               → ## Observability Architecture

decision-rationale.md [OPTIONAL]
  ├── Technology Selection     → ## Technology Stack
  ├── ADRs                     → ## ADR-001: Title, ## ADR-002: Title, ...
  ├── Design Principles        → ## Design Principles
  └── Trade-offs               → ## Trade-offs & Constraints
  │
  └── [FALLBACK if missing - ~60% coverage for above sections]:
        configuration-reference.md (tech stack, framework choices → Technology Stack)
        data-architecture.md (schema design decisions → ADRs supplement)
        integration-points.md (integration choice rationale → ADRs supplement)

configuration-reference.md
  ├── Environment Variables    → ## Configuration Architecture
  └── Feature Flags            → ## Feature Management

observability-requirements.md
  ├── Logging Strategy         → ## Observability Architecture
  ├── Monitoring Strategy      → ## Monitoring & Alerting
  └── Alerting Rules           → ## SLA & SLO Targets
```

### epics.md Generation

```
Source → BMAD Epics
─────────────────────────────────────────────────────────────────
functional-specification.md
  ├── FRs grouped by domain    → ## Epic N: Domain Name
  ├── User Stories per FR      → ### Story N.M: Title
  └── Acceptance Criteria      → Acceptance Criteria per story

business-context.md [OPTIONAL]
  ├── Personas                 → "As a [persona]..." in user stories
  └── Business Goals           → Epic priority ordering
  │
  └── [FALLBACK if missing]:
        functional-specification.md (User Personas → persona names,
          Product Positioning → priority ordering context)

technical-debt-analysis.md
  ├── Migration Priority Matrix → ## Epic: Technical Debt Resolution
  └── Quick Wins               → High-priority stories in debt epic

integration-points.md
  └── External Integrations    → ## Epic: Integration & Connectivity
```

**Epic Grouping Strategy:**
1. Group FRs by domain/feature area (auth, data management, reporting, etc.)
2. Each group becomes an Epic
3. Each FR within a group becomes a Story
4. Add a "Technical Foundation" epic for infrastructure/debt items
5. Add an "Integration" epic for external service work
6. Priority ordering: P0 epics first, then P1, P2, P3

### ux-design-specification.md Generation

```
Source → BMAD UX Design Section
─────────────────────────────────────────────────────────────────
visual-design-system.md
  ├── Component Library        → ## Component Inventory
  ├── Design Tokens            → ## Design Tokens
  ├── Responsive Breakpoints   → ## Responsive Design
  ├── Accessibility Standards  → ## Accessibility Requirements
  └── User Flows               → ## User Flows

business-context.md [OPTIONAL]
  ├── Personas                 → ## User Personas (with journey maps)
  └── Business Constraints     → ## Design Constraints
  │
  └── [FALLBACK if missing]:
        functional-specification.md (User Personas → persona definitions)
        visual-design-system.md (User Flows, Accessibility → journey context)

functional-specification.md
  ├── User Stories             → ## Key User Journeys
  └── Business Rules           → ## Interaction Patterns
```

---

## Process

### Step 0: Verify Prerequisites

```bash
# Check that Gear 2 is complete
DOCS_DIR="docs/reverse-engineering"

# 9 core docs (always produced by reverse-engineer v1.x+)
CORE_DOCS=("functional-specification.md" "integration-points.md" "configuration-reference.md" "data-architecture.md" "operations-guide.md" "technical-debt-analysis.md" "observability-requirements.md" "visual-design-system.md" "test-documentation.md")

# 2 optional docs (produced by reverse-engineer v2.0+)
OPTIONAL_DOCS=("business-context.md" "decision-rationale.md")

CORE_MISSING=0
OPTIONAL_MISSING=0
OPTIONAL_MISSING_LIST=()

for doc in "${CORE_DOCS[@]}"; do
  if [ ! -f "$DOCS_DIR/$doc" ]; then
    echo "MISSING (core): $doc"
    CORE_MISSING=$((CORE_MISSING + 1))
  fi
done

for doc in "${OPTIONAL_DOCS[@]}"; do
  if [ ! -f "$DOCS_DIR/$doc" ]; then
    echo "MISSING (optional): $doc"
    OPTIONAL_MISSING=$((OPTIONAL_MISSING + 1))
    OPTIONAL_MISSING_LIST+=("$doc")
  fi
done

if [ $CORE_MISSING -gt 0 ]; then
  echo "ERROR: $CORE_MISSING core docs missing. Run Gear 2 first: /stackshift.reverse-engineer"
  exit 1
fi

TOTAL_FOUND=$((9 + 2 - OPTIONAL_MISSING))

if [ $OPTIONAL_MISSING -gt 0 ]; then
  echo "WARNING: $TOTAL_FOUND/11 docs found. Missing optional: ${OPTIONAL_MISSING_LIST[*]}"
  echo "Proceeding in 9-doc mode (~85% average coverage). Missing content will be inferred from related docs."
else
  echo "All 11 reverse-engineering docs found. Ready to synthesize at full coverage."
fi
```

**If core docs are missing:** Error. Guide user to run `/stackshift.reverse-engineer` first.
**If all 11 exist:** Proceed at full coverage.
**If only 9 core exist:** Warn about reduced coverage (~85% average), then proceed to Step 0.5 to infer missing content.

### Step 0.5: Infer Missing Documents

**Only runs if optional docs are missing.** Extracts equivalent content from related core docs.

#### If `business-context.md` is missing:

Extract business context from:
- **`functional-specification.md`**: Executive Summary (product vision), User Stories (persona behavior), Success Criteria (business goals), User Personas (target users), Product Positioning (market context)
- **`visual-design-system.md`**: Persona UX context (user flows, accessibility standards imply target audience)

Map inferred content to the sections that would have come from business-context.md:
- Product Vision → from Executive Summary / Product Positioning
- Target Users & Personas → from User Personas + visual-design-system user flows
- Business Goals → from Success Criteria
- Competitive Landscape → `[INFERRED FROM: functional-specification.md - limited data, review recommended]`
- Stakeholder Map → `[INFERRED FROM: functional-specification.md - limited data, review recommended]`
- Business Constraints → from NFRs (performance, security, compliance constraints)

**Note:** Coverage for sections sourced from business-context.md drops to ~70% (vs ~90% with the full doc). Persona depth and competitive landscape are most affected.

#### If `decision-rationale.md` is missing:

Extract technology decisions from:
- **`configuration-reference.md`**: Tech stack identification (languages, frameworks, versions from environment variables and config), framework choices (build tools, deployment targets)
- **`data-architecture.md`**: Schema design decisions (why certain data models, relationships, indexing strategies)
- **`integration-points.md`**: Integration choice rationale (why specific external services, API patterns, auth providers)

Map inferred content to the sections that would have come from decision-rationale.md:
- Technology Stack → from configuration-reference.md environment/config analysis
- ADRs → synthesized from observable choices across all three docs, marked `[INFERRED FROM: configuration-reference.md, data-architecture.md, integration-points.md]`
- Design Principles → `[INFERRED FROM: codebase patterns - review recommended]`
- Trade-offs → inferred from technical-debt-analysis.md (debt items imply past trade-offs)

**Note:** Coverage for sections sourced from decision-rationale.md drops to ~60% (vs ~85% with the full doc). ADR rationale and design principles are most affected since "why" decisions were made is harder to infer than "what" decisions were made.

### Step 1: Load All Reverse-Engineering Docs

Read all available docs (9-11) from `docs/reverse-engineering/` into memory. If Step 0.5 inferred content for missing optional docs, include that inferred content alongside the core docs. Parse each for structured content:
- Extract all FRs, NFRs, user stories, personas
- Extract all data models, API contracts, integration points
- Extract all ADRs, technology selections, design principles (from docs or inferred in Step 0.5)
- Extract all business context, goals, constraints (from docs or inferred in Step 0.5)
- Note all `[INFERRED]`, `[INFERRED FROM: source-doc]`, and `[NEEDS USER INPUT]` markers

### Step 2: Choose Mode

Ask the user which mode to use:

```
How should BMAD artifacts be generated?

A) YOLO - Fully automatic, no questions asked (~10 min)
   Best for: Quick generation, batch processing, refine later

B) Guided - Auto-fill + 5-10 targeted questions (~15-20 min) (Recommended)
   Best for: Most projects, good balance of speed and quality

C) Interactive - Section-by-section review (~25-30 min)
   Best for: Critical projects, maximum precision
```

### Step 3: Generate Artifacts (Mode-Dependent)

#### YOLO Mode

1. **Generate prd.md**: Map all source sections per the mapping above. For `[NEEDS USER INPUT]` items, use best-effort inference and mark with `[AUTO-INFERRED - review recommended]`.
2. **Generate architecture.md**: Map all technical docs. Generate Mermaid diagrams for system architecture and data flow.
3. **Generate epics.md**: Group FRs into domain-based epics. Create stories with "As a [persona]" format. Set priorities from FR priorities.
4. **Generate ux-design-specification.md**: Map visual design system + persona journey maps.
5. Write all artifacts to `_bmad-output/planning-artifacts/`.
6. Generate a coverage report showing what percentage of each artifact was filled from docs vs inferred.

#### Guided Mode

1. **Parse and score**: Read all docs, identify `[NEEDS USER INPUT]` items and low-confidence sections.
2. **Auto-fill high-confidence sections**: Everything that maps cleanly from docs.
3. **Present targeted questions** (5-10 max):
   - "The codebase suggests [X] as the primary user persona. Is this accurate, or would you refine it?"
   - "Business goals appear to center on [X]. What are the top 3 success metrics?"
   - "The architecture uses [X]. For the BMAD architecture doc, should we document the current state or a target state?"
   - "FRs group naturally into [N] domains: [list]. Does this epic structure make sense?"
   - "The competitive landscape suggests [X]. Any corrections?"
4. **Incorporate answers** into artifacts.
5. Write all artifacts.

#### Interactive Mode

1. **Create context brief**: One-page summary of all available docs (9-11) for quick reference, noting any inferred content from Step 0.5.
2. **Walk through prd.md** section by section:
   - Show draft for each section
   - Ask: "Approve as-is, or modify?"
   - Incorporate changes
3. **Walk through architecture.md** section by section (same approach).
4. **Walk through epics.md**: Present epic groupings, ask for approval, refine stories.
5. **Walk through ux-design-specification.md**: Present design system mapping, ask for approval.
6. Write all artifacts.

### Step 4: Write Output

Create `_bmad-output/planning-artifacts/` directory and write all 4 artifacts:

```
_bmad-output/
└── planning-artifacts/
    ├── prd.md
    ├── architecture.md
    ├── epics.md
    └── ux-design-specification.md
```

Each artifact includes YAML frontmatter:

```yaml
---
stepsCompleted: [1, 2, 3]
inputDocuments:
  - docs/reverse-engineering/functional-specification.md
  - docs/reverse-engineering/business-context.md
  - docs/reverse-engineering/integration-points.md
  # ... all source docs used
workflowType: prd  # or architecture, epics, ux-design
project_name: "<from state file>"
date: "<current date>"
synthesize_mode: "yolo"  # or guided, interactive
coverage_score: 92  # percentage of sections filled from docs
source_doc_count: 9  # or 11 - how many reverse-engineering docs were available
inferred_sections: []  # list of sections that used fallback sources, e.g. ["Product Vision", "ADRs"]
---
```

### Step 5: Generate Synthesis Report

Output a summary showing:

```
BMAD Synthesis Complete
═══════════════════════

Mode: Guided
Time: 18 minutes

Artifacts Generated:
  prd.md                    - 94% from docs, 6% user input
  architecture.md           - 88% from docs, 12% inferred
  epics.md                  - 82% from docs, 18% structured from FRs
  ux-design-specification.md - 68% from docs, 32% inferred

Items Requiring Review:
  - prd.md: 2 items marked [AUTO-INFERRED]
  - architecture.md: 1 ADR with [INFERRED] rationale
  - epics.md: Story priorities may need reordering

Next Steps:
  - Review artifacts in _bmad-output/planning-artifacts/
  - Install BMAD: npx bmad-method@alpha install
  - Run: *workflow-init (BMAD will use these artifacts as starting point)
  - Or: Manually refine artifacts before handing off to BMAD
```

---

## Output Format

### prd.md Structure

```markdown
---
stepsCompleted: [1, 2, 3, 4, 5]
workflowType: prd
project_name: "..."
date: "..."
synthesize_mode: "guided"
source_doc_count: 9  # or 11
inferred_sections: ["Product Vision", "Target Users", "Market Context"]  # empty if 11 docs
---

# [Product Name] - Product Requirements Document

## Product Vision
[From business-context.md Product Vision]
[Or INFERRED FROM: functional-specification.md Executive Summary + Product Positioning]

## Target Users
[From business-context.md Personas + functional-spec User Personas]
[Or INFERRED FROM: functional-specification.md User Personas + visual-design-system.md user flows]

### Persona 1: [Name]
- **Role:** ...
- **Goals:** ...
- **Pain Points:** ...

## Success Criteria
[From functional-spec Success Criteria + business-context Business Goals]
- Criterion 1
- Criterion 2

## Functional Requirements

### FR1: [Title]
**Priority:** P0
**Description:** [From functional-spec FR-001]
**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

### FR2: [Title]
...

## Non-Functional Requirements

### NFR1: [Title]
**Priority:** P1
**Description:** [From functional-spec NFR-001]

## External Dependencies
[From integration-points.md]

## Constraints & Assumptions
[From business-context.md Business Constraints]

## Known Issues
[From technical-debt-analysis.md high-priority items]
```

### architecture.md Structure

```markdown
---
stepsCompleted: [1, 2, 3]
workflowType: architecture
source_doc_count: 9  # or 11
inferred_sections: ["Technology Stack", "ADRs", "Design Principles"]  # empty if 11 docs
---

# [Product Name] - Technical Architecture

## System Architecture Diagram
[Mermaid diagram from integration-points Data Flow Diagrams]

## Technology Stack
[From decision-rationale.md Technology Selection]
[Or INFERRED FROM: configuration-reference.md tech stack and framework choices]

## Domain Model
[From data-architecture.md Domain Model / Bounded Contexts]

## API Contracts
[From data-architecture.md API Endpoints]

### GET /api/resource
**Description:** ...
**Request:** ...
**Response:** ...

## Data Models
[From data-architecture.md Data Models]

### ModelName
- **field1**: type - description
- **field2**: type - description

## ADR-001: [Decision Title]
**Context:** [From decision-rationale.md]
[Or INFERRED FROM: configuration-reference.md, data-architecture.md, integration-points.md]
**Decision:** ...
**Rationale:** ...

## Deployment Architecture
[From operations-guide.md]

## Scalability & Performance
[From operations-guide.md Scalability Strategy]

## Observability Architecture
[From observability-requirements.md]
```

---

## Integration with Existing Workflows

### From Spec Kit → BMAD Synthesize

If you already ran Gears 1-5 with Spec Kit and want BMAD artifacts too:
1. The reverse-engineering docs are already generated
2. Run `/stackshift.bmad-synthesize` directly
3. BMAD artifacts supplement (don't replace) `.specify/` structure

### From BMAD Synthesize → BMAD Workflow

After generating artifacts:
1. Install BMAD: `npx bmad-method@alpha install`
2. Run `*workflow-init`
3. BMAD agents will find and use the pre-generated artifacts
4. PM agent refines PRD, Architect agent refines Architecture
5. Much faster than starting from scratch

### Batch Mode Integration

When running batch processing (`/stackshift.batch`):
- Batch session can include `synthesize_mode: "yolo"` in answers
- Each repo gets BMAD artifacts generated automatically after Gear 2
- Useful for enterprise-scale documentation of many services

---

## Success Criteria

- ✅ All 4 BMAD artifacts generated in `_bmad-output/planning-artifacts/`
- ✅ prd.md contains FRs, NFRs, personas, success criteria, constraints
- ✅ architecture.md contains data models, API contracts, ADRs, deployment architecture
- ✅ epics.md contains domain-grouped epics with user stories
- ✅ ux-design-specification.md contains design system and user journey maps
- ✅ Each artifact has YAML frontmatter with source tracking
- ✅ Synthesis report shows coverage percentages
- ✅ `[AUTO-INFERRED]` items clearly marked for review

---

## Next Steps

After BMAD Synthesize:

1. **Review artifacts** in `_bmad-output/planning-artifacts/`
2. **Refine manually** or hand off to BMAD agents for collaborative refinement
3. **Install BMAD** (if not installed): `npx bmad-method@alpha install`
4. **Run BMAD workflow**: `*workflow-init` — agents will use your artifacts as starting point
5. **Or use directly**: Artifacts are valid BMAD format, can be used as-is for implementation

---

## Technical Notes

- Read all available docs (9-11) using the Read tool (parallel reads recommended)
- If only 9 docs present, run Step 0.5 inference before proceeding to artifact generation
- For Mermaid diagrams in architecture.md, generate from integration-points.md data flow descriptions
- Epic grouping uses domain clustering: analyze FR titles and descriptions for common themes
- User story format: "As a [persona from business-context or functional-specification], I want [FR description], so that [business goal]"
- Priority inheritance: Stories inherit priority from their source FR
- ADR numbering: Sequential from decision-rationale.md (or inferred from config/data/integration docs), preserving original order
- All inferred content must be tagged with `[INFERRED FROM: source-doc]` so users can verify accuracy
