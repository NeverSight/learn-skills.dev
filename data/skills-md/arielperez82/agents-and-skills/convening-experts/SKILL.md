---
name: convening-experts
description: Convenes expert panels for problem-solving. Use when user mentions panel, experts, multiple perspectives, MECE, DMAIC, RAPID, Six Sigma, root cause analysis, strategic decisions, or process improvement.
---

# Convening Experts

Convene domain experts and methodological specialists to solve problems through multi-round collaborative discussion. Experts build on each other's insights, challenge assumptions, and synthesize recommendations.

## Panel Format

### Single-Round Consultation

For simpler problems requiring multiple viewpoints:

1. **Assemble panel** (3-5 experts based on problem domain)
2. **Each expert provides independent perspective** (parallel, not sequential)
3. **Synthesize recommendations** with attribution

### Multi-Round Discussion

For complex problems requiring collaborative reasoning:

1. **Round 1**: Each expert analyzes problem independently
2. **Round 2**: Experts respond to each other's insights, building on or challenging points
3. **Round 3** (if needed): Converge on synthesis, resolve disagreements
4. **Final synthesis**: Integrated recommendations with decision framework

## Expert Roles

**Available expertise spans:**

- MSD domain experts (life sciences, engineering, manufacturing, quality, corporate functions)
- Consulting framework specialists (strategic, process improvement, innovation, systems analysis, root cause)

See [references/msd-domain-experts.md](references/msd-domain-experts.md) and [references/consulting-frameworks.md](references/consulting-frameworks.md) for complete role catalog.

Agent loads relevant references based on problem domain.

## Panel Convening Logic

Agent selects 3-5 experts based on problem characteristics:

**Problem type → Primary expert + Supporting experts**

- **Technical troubleshooting** → Domain expert + Systems Thinker + Five Whys Facilitator
- **Strategic decision** → McKinsey Consultant + relevant domain experts + SWOT Analyst
- **Process improvement** → Six Sigma Black Belt + Lean Practitioner + domain Manufacturing Engineer
- **Product innovation** → Design Thinking Facilitator + Jobs-to-Be-Done Specialist + relevant engineers
- **Root cause analysis** → Domain expert + Five Whys Facilitator + Systems Thinker
- **Market positioning** → Porter Framework Expert + Marketing Specialist + BCG Consultant
- **Cross-functional problem** → Relevant domain experts + Bain Consultant (RAPID) + Systems Thinker

## Response Format

### Single-Round Format

```
---
type: assessment
endeavor: <endeavor>
subject: <subject>
date: <YYYY-MM-DD>
status: draft
initiative: <ID> (optional, when part of an initiative)
---

# Assessment: [Topic]

**Purpose:** [Why this panel was convened]
**Context:** [Background and constraints]

---

## Expert Panel: [Topic]

**Panel Members:**
- [Expert 1 Role]
- [Expert 2 Role]
- [Expert 3 Role]

---

### [Expert 1 Role]
[Independent analysis and recommendations]

### [Expert 2 Role]
[Independent analysis and recommendations]

### [Expert 3 Role]
[Independent analysis and recommendations]

---

## Synthesis
[Integrated recommendations with decision framework]

## Recommendations
[Actionable next steps]
```

### Multi-Round Format

```
---
type: assessment
endeavor: <endeavor>
subject: <subject>
date: <YYYY-MM-DD>
status: draft
initiative: <ID> (optional, when part of an initiative)
---

# Assessment: [Topic]

**Purpose:** [Why this panel was convened]
**Context:** [Background and constraints]

---

## Expert Panel: [Topic]

**Panel Members:**
- [Expert 1 Role]
- [Expert 2 Role]
- [Expert 3 Role]

---

## Round 1: Initial Analysis

### [Expert 1 Role]
[Initial perspective]

### [Expert 2 Role]
[Initial perspective]

### [Expert 3 Role]
[Initial perspective]

---

## Round 2: Cross-Examination

### [Expert 1 Role] responds to [Expert 2 Role]
[Builds on or challenges specific points]

### [Expert 2 Role] responds to [Expert 3 Role]
[Integration or disagreement]

### [Expert 3 Role] responds to [Expert 1 Role]
[Synthesis attempt]

---

## Round 3: Convergence (if needed)

[Experts resolve disagreements and converge]

---

## Final Synthesis
[Integrated recommendations, highlighting consensus and productive disagreements]

## Recommendations
[Actionable next steps]
```

## Persistent Report (Mandatory)

Every expert panel session MUST be written to the assessments directory under `CANONICAL_ROOT` (per `/docs/layout`) as a persistent artifact. The file is the primary deliverable; screen output is a summary.

### File Naming Convention

```
assessment-<endeavor>-<subject>-<YYYY-MM-DD>.md
```

Follow the canonical naming grammar. Examples:

- `assessment-repo-initiative-naming-2026-02-10.md`
- `assessment-product-pricing-strategy-2026-02-25.md`

### Required Frontmatter

```yaml
---
type: assessment
endeavor: <endeavor>
subject: <subject>
date: <YYYY-MM-DD>
status: draft
initiative: <ID>  # optional, when panel is part of an initiative
---
```

### Required Content Sections

The written file must include ALL of:

1. **Purpose and Context** — Why the panel was convened, background, constraints
2. **Panel metadata** — Topic, date, format used, panel members with roles
3. **Full expert analysis** — Every round, every expert's complete contribution
4. **Cross-examination / discussion** — For multi-round panels, the full exchange
5. **Final synthesis** — Integrated findings with decision framework
6. **Actionable recommendations** — Concrete next steps

### Workflow

1. **Write the file first** to the assessments directory under `CANONICAL_ROOT` (per `/docs/layout`) with all sections above
2. **Then summarize to screen** — concise summary with key findings and a reference to the file path

The persistent file is the canonical record. Screen output helps the user quickly understand the outcome and locate the full report.

## Expert Behavior Guidelines

**Domain Experts:**

- Apply MSD context (ECL platform, regulatory constraints, validated systems)
- Use domain-appropriate terminology without over-explanation
- Prioritize practical implementation over theoretical perfection
- Flag domain-specific risks and constraints

**Framework Experts:**

- Apply frameworks systematically (show the structure)
- Adapt frameworks to problem context (not rigid application)
- Explain "why this framework" for this problem
- Integrate domain context when applying generic frameworks

**Cross-Panel Interaction:**

- Reference other experts' points specifically ("Building on [Expert]'s observation about...")
- Challenge constructively ("I see it differently because...")
- Synthesize across disciplines ("This connects [Expert 1]'s technical constraint with [Expert 2]'s business priority...")
- Flag tensions between perspectives explicitly

**Disagreement Handling:**

- Make disagreements productive (what assumptions differ?)
- Present multiple valid approaches when consensus isn't required
- Identify decision criteria to resolve disagreements
- Escalate to user if expert consensus can't be reached

## Decision Frameworks

When panel must recommend action:

**RAPID (Bain)**

- **Recommend**: Panel's recommendation with rationale
- **Agree**: Which stakeholders must agree
- **Perform**: Who implements
- **Input**: Who provides input
- **Decide**: Who makes final decision

**Weighted Decision Matrix**

- Criteria (importance weighted)
- Options scored on each criterion
- Total score with sensitivity analysis

**Risk-Benefit Analysis**

- Upside potential (probability × impact)
- Downside risk (probability × impact)
- Mitigation strategies
- Decision under uncertainty

## MSD Integration

Apply MSD-specific context automatically:

**Technical constraints:**

- ECL platform and assay chemistry
- ISO 13485 compliance and validated systems
- Regulatory requirements (FDA, CE marking)
- Technology stack (Python, AWS, Java, TypeScript)

**Business context:**

- Life sciences market dynamics
- Customer segments (pharma, biotech, CRO, academic)
- Competitive landscape

**Cultural factors:**

- Scientific rigor and data-driven decisions
- Cross-functional collaboration norms
- Innovation balanced with risk management
- Quality and regulatory consciousness

## Examples

### Example 1: Technical Troubleshooting

```
User: Our new assay is showing high background signal in serum samples

Claude convenes:
- Assay Scientist (primary)
- Systems Thinker (feedback loops)
- Five Whys Facilitator (root cause)

Format: Multi-round (technical nuance requires collaboration)
```

### Example 2: Strategic Decision

```
User: Should we build internal ML infrastructure or use vendor solutions?

Claude convenes:
- Software Engineer (implementation)
- McKinsey Consultant (strategic framing)
- Finance Analyst (cost analysis)
- DevOps Engineer (operational implications)

Format: Single-round → RAPID framework synthesis
```

### Example 3: Process Improvement

```
User: Manufacturing yield dropped 8% after equipment upgrade

Claude convenes:
- Manufacturing Engineer (primary domain)
- Six Sigma Black Belt (DMAIC)
- Systems Thinker (unintended consequences)

Format: Multi-round (root cause needs collaborative analysis)
```

## Craft Flow Integration

Expert panels integrate into the `/craft` SDLC flow as opt-in quality checkpoints at phase gates. The orchestrator recommends panels based on initiative complexity; users can accept or skip.

### Blast-Radius Classification

Initiatives are classified into 5 complexity tiers after Phase 0 approval. The tier determines which phases offer panel checkpoints:

| Tier | Panel Phases | Description |
|------|-------------|-------------|
| Strategic | 0, 1, 2, 3 | Cross-initiative, 4+ domains, or 15+ steps |
| Complex | 0, 1, 2 | 2+ domains with high blast radius |
| Medium | 2 | Code/mixed with 4+ steps |
| Light | 2 | Docs-only with 2+ downstream consumers |
| Trivial | (none) | Low complexity, no panels |

### Panel Templates

Four panel templates are available for craft flow checkpoints. See [references/craft-panel-templates.md](references/craft-panel-templates.md) for full composition, format, and prompt templates:

- **Discovery Panel** — Phase 0, Complex+. Validates problem framing and value proposition.
- **Requirements Panel** — Phase 1, Complex+. Validates user stories and acceptance criteria.
- **Design Panel** — Phase 2, Light+. Reviews architecture with ops and domain perspectives.
- **Plan Review Panel** — Phase 3, Strategic only. Validates plan decomposition and dependencies.

### Phase-Panel Mapping

| Phase | Panel | Minimum Tier | Format |
|-------|-------|-------------|--------|
| 0: Discover | Discovery | Complex | 3-round |
| 1: Define | Requirements | Complex | 3-round |
| 2: Design | Design | Light | Single-round (Light) / 3-round (Medium+) |
| 3: Plan | Plan Review | Strategic | 3-round |

For full orchestration logic and checkpoint behavior, see [commands/craft/craft.md](../../commands/craft/craft.md).

## Constraints

**Never:**

- Use fictional names for experts (use role titles only: "Software Engineer", not "Dr. John Smith, Software Engineer")
- Invent MSD-specific details beyond general domain knowledge
- Apply frameworks rigidly without problem context
- Create artificial consensus when legitimate disagreements exist
- Include experts who add no value (quality over quantity)
- Make experts repeat information (each should contribute uniquely)

**Always:**

- Write the complete panel session to the assessments directory under `CANONICAL_ROOT` (per `/docs/layout`) as a persistent assessment document
- Select experts genuinely relevant to problem
- Show framework structure when applying consulting methods
- Make cross-expert references specific and substantive
- Provide decision-ready synthesis (not "here are perspectives, you decide")
- Acknowledge uncertainty explicitly when present

## Activation Decision Tree

```
Is problem complex with multiple valid approaches?
├─ Yes → Expert panel
│   ├─ Spans multiple domains? → Multi-round discussion
│   └─ Needs diverse perspectives? → Single-round consultation
└─ No → Direct answer (don't force panel format)

Requires systematic framework?
├─ Yes → Include framework expert
└─ No → Domain experts only

MSD-specific context relevant?
├─ Yes → Include domain experts, apply MSD constraints
└─ No → Generic consulting approach
```

## Quality Indicators

**Good panel:**

- Each expert contributes unique insight
- Cross-references are specific and substantive
- Framework application shows structure and reasoning
- Synthesis provides decision-ready recommendations
- Disagreements are productive and resolved (or flagged)

**Poor panel:**

- Experts repeat same points
- Generic advice not grounded in frameworks or domain
- No synthesis or integration across perspectives
- Consensus forced despite legitimate disagreements
- Panel format used when direct answer would suffice
