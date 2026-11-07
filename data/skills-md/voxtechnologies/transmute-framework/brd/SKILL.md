---
name: brd
description: >-
  Generates a comprehensive Business Requirement Document (BRD) from a business plan using parallel agent teams.
  This skill should be used when the user asks to "generate BRD",
  "create business requirements document", "run Stage 1",
  "generate business requirements", "create BRD from business plan",
  or when the transmute-pipeline agent reaches Stage 1 of the pipeline.
metadata:
  version: 1.0.0
effort: high
---

# Transmute — BRD Generation (Stage 1)

Read the detailed guide at `${CLAUDE_SKILL_DIR}/references/brd-detailed-guide.md` for the complete agent team architecture, teammate spawn prompts, token budget management, review agent checklists, remediation procedures, and writing guidelines.

## Prerequisites

Before starting, verify:
1. `./plancasting/businessplan/` directory exists and contains `.md` or `.pdf` files. If missing or empty, STOP: "Stage 1 requires a Business Plan at `./plancasting/businessplan/`. Place your business plan files (.md or .pdf) there before running Stage 1."
2. `./plancasting/tech-stack.md` exists (created by Stage 0). If missing, STOP: "Stage 1 requires `plancasting/tech-stack.md` from Stage 0. Run Stage 0 first."

## Critical Framing

This BRD uses the **Full-Build Approach**: ALL features described in the Business Plan are built as a single, complete product. No MVP, no phased rollout, no feature deferral. If the Business Plan describes "Phase 1, Phase 2, Phase 3" — IGNORE the phasing. Features labeled "future", "planned", "roadmap", or "long-term" are INCLUDED in full scope. Only features explicitly marked "out-of-scope" are excluded.

## Execution Flow

### Step 1: Read and Analyze Inputs

Read and fully internalize:
- All files in `./plancasting/businessplan/` (supported formats: `.md` and `.pdf`)
- `./plancasting/tech-stack.md`

Check `Session Language` in `./plancasting/tech-stack.md`. Generate ALL BRD documents in the specified language. Technical identifiers (requirement IDs like FR-001, section headers, cross-reference codes) remain in English.

**Language Inheritance**: Subsequent stages (PRD, audits, reports) will read the `Session Language` section from `plancasting/tech-stack.md` — NOT from BRD documents. The BRD's language serves as a reference, but the canonical language setting is always in `tech-stack.md`.

Adapt BRD structure based on product type in `plancasting/tech-stack.md`:
- **Web applications**: Standard structure
- **Mobile applications**: Add platform-specific requirement categories (App Store/Play Store guidelines, device permissions, offline capabilities)
- **IoT / Embedded**: Add hardware requirement categories (environmental requirements, power requirements, connectivity protocols, certification requirements)
- **Desktop applications**: Add platform-specific requirements (Windows/macOS/Linux compatibility, installation/update mechanisms, system resource requirements)
- **AI/ML products**: Add model requirement categories (training data requirements, inference latency, accuracy metrics, bias/fairness requirements)

### Step 2: Feature Extraction Sweep

Identify EVERY feature, capability, and function described anywhere in the Business Plan — including those labeled as "future", "Phase 2/3", "nice-to-have", "roadmap", "planned", or "long-term". Compile a master feature inventory.

**Deduplication rule**: Merge variants of the same capability (e.g., "real-time collaboration" and "live editing" both describe concurrent document interaction). Keep distinct features separate (e.g., "user invitations" vs "user roles"). **Variant test**: Two features are variants if they share the same user goal AND the same core data entity AND the same business logic. When in doubt, keep as separate features — merging is harder to undo than splitting.

### Step 3: Create Shared Context

Create `./plancasting/brd/` directory and `./plancasting/brd/_context.md` containing:
- Business Plan summary (market, product, revenue model, customers, risks, financials)
- Technology stack summary from `./plancasting/tech-stack.md`
- Master feature inventory (ALL features from ALL phases) as a markdown table with columns: Feature ID (FEAT-001, etc.), Feature Name, Business Plan Section, FR ID(s), Coverage Status
- Master requirement ID registry with reserved ranges:
  - BR-001–BR-099, FR-001–FR-299, NFR-001–NFR-099, CR-001–CR-049, SR-001–SR-049, BRL-001–BRL-149, DR-001–DR-049, IR-001–IR-049
- Glossary of key terms and acronyms
- Cross-reference conventions and formatting standards
- Note: "This BRD covers the COMPLETE product scope."

### Step 4: Spawn Agent Teams (Phase 2)

Spawn 5 specialized teammates. Each spawn prompt must include: CLAUDE.md Part 1 instructions, full `_context.md` content, file assignments with ID ranges, relevant Business Plan sections, full-scope instruction ("IGNORE all phasing — treat every described feature as in-scope"), and the writing guidelines from the detailed guide.

**Known dependency**: Teammate 3 (data-and-integration) depends on Teammate 2 (technical-infrastructure) for security requirements and data privacy classifications. Either spawn Teammate 3 after Teammate 2 completes, or include Teammate 2's security context in Teammate 3's spawn prompt.

**Teammate 1 — "business-core"**
Files: `00-cover-and-metadata.md`, `01-executive-summary.md`, `02-project-background-and-objectives.md`, `03-current-state-analysis.md`, `06-business-requirements.md`, `07-functional-requirements.md`
Emphasize: Trace every BR/FR to a specific Business Plan section. Use quantified acceptance criteria. Generate mermaid diagrams for all process flows. FRs must cover ALL features from master inventory. FR range is expanded (FR-001–FR-299) to accommodate full scope.

**Teammate 2 — "technical-infrastructure"**
Files: `08-non-functional-requirements.md`, `12-regulatory-and-compliance-requirements.md`, `13-security-requirements.md`
Emphasize: NFRs sized for COMPLETE product — all features active simultaneously, full user base from day one. Scalability targets reflect Business Plan's full growth projections. Mark unstated values as assumptions.

**Teammate 3 — "data-and-integration"**
Files: `09-data-requirements.md`, `10-integration-requirements.md`, `16-migration-and-transition-requirements.md`
Emphasize: Data model accommodates ALL entities across ALL features from day one. Do not design a minimal schema that would need expansion later. Integration requirements cover ALL third-party systems mentioned anywhere, including those described as future integrations.

**Teammate 4 — "user-experience-and-operations"**
Files: `04-stakeholder-analysis.md`, `05-scope-definition.md`, `11-user-experience-requirements.md`, `14-business-rules-and-logic.md`, `15-reporting-and-analytics-requirements.md`
Emphasize: Scope definition must state ALL features are in-scope. Out-of-scope section only contains items NOT mentioned in the Business Plan. Derive personas from ALL customer segments including later-phase targets. Business rules must cover ALL feature interactions including cross-feature rules.

**Teammate 5 — "risk-and-planning"**
Files: `17-acceptance-criteria.md`, `18-assumptions-constraints-dependencies.md`, `19-risk-analysis-and-mitigation.md`, `20-cost-benefit-analysis.md`, `21-timeline-and-milestones.md`
Emphasize: Risk analysis must include full-build-specific risks (complexity risk, integration risk from building all features simultaneously, testing scope risk). Cost-benefit analysis should reflect complete build cost vs. delivering all features at once. Timeline uses parallel workstreams, NOT sequential phases. Gantt chart shows concurrent development converging to a single launch.

### Step 5: Token Budget Management

Each agent has an output token limit per response (see tech-stack.md § Model Specifications). Safe budget per agent: output token limit minus 7K headroom.

**Before spawning**: Estimate output size per file. If a single file exceeds the safe output budget, split by feature group. `07-functional-requirements.md` with 30+ features almost certainly needs splitting.

**If a teammate fails**: Check which files were written, re-spawn for missing/truncated files. If a re-spawned teammate's output is still truncated after reducing scope, split further. Do not proceed to Phase 4 until all files are complete.

### Step 6: Structural Integration (Phase 4)

After all teammates complete:
1. Collect all files into `./plancasting/brd/`
2. Run structural consistency checks:
   - **Full-scope coverage audit**: Every feature in inventory must have at least one FR
   - Verify all requirement IDs are unique (no cross-teammate duplicates)
   - Validate all cross-reference links
   - Verify terminology consistency with glossary
   - Confirm all assumptions marked with `> ⚠️ ASSUMPTION:`
   - **Assumption volume check**: Run `bash ${CLAUDE_SKILL_DIR}/scripts/assumption-volume.sh` and copy its two lines into `_review-log.md` § Assumption Review Status unchanged. Do not count by hand: the Stage 1 gate and the hook read this number. At 30% or more it is CRITICAL and the pipeline stops for operator review
   - Validate mermaid diagram syntax
   - Verify every BR has at least one FR
   - **MoSCoW distribution check**: Flag if Must Have exceeds 70% of total requirements. High Must Have (70%+) may be acceptable for enterprise/regulated products. RED FLAG: if Business Plan describes 'MVP first, phases later' but all requirements are marked Must Have — indicates phasing hasn't been eliminated despite full-build approach.
   - **Cross-feature interaction check**: Identify requirements that interact across what the Business Plan originally described as separate phases. Ensure these interactions are explicitly documented.
3. Generate `22-glossary-and-appendices.md`
4. Generate `README.md` with navigation guide and prominent full-scope note
5. Fix structural inconsistencies

### Step 7: Deep Quality Review (Phase 5)

Spawn 3 review agents. Each reads ALL BRD files, `_context.md`, and the Business Plan. If BRD + Business Plan exceeds 60% of the model's context window (check tech-stack.md § Model Specifications), split each reviewer's scope to a subset of BRD files by domain, and the lead performs cross-file consistency checks in Phase 6 remediation.

Each review agent produces issues in this format: Severity (CRITICAL/HIGH/MEDIUM/LOW), File, Location (section/requirement ID), Category, Description, Recommendation, Affected Requirements.

**completeness-reviewer**: Coverage gaps, vagueness, traceability.
- Every feature in master inventory has at least one FR
- Every BR has at least one corresponding FR
- Every FR has measurable acceptance criteria (not "fast", "user-friendly", "intuitive")
- Every FR specifies behavior for normal operation, error conditions, edge cases, boundary conditions
- Every IR specifies authentication, error handling, retry policy, fallback
- Every DR specifies data types, validation rules, constraints, retention
- Every BRL specifies trigger conditions, actions, exceptions, conflict resolution
- Every SR is specific and testable
- All CR cite specific regulations with section numbers
- NFRs have quantified targets
- No requirement is a verbatim copy of Business Plan text
- No placeholders, TODOs, or TBD entries remain
- Cross-feature interactions documented for features spanning originally-separate Business Plan phases

**consistency-reviewer**: Contradictions, duplications, terminology.
- No contradictory requirements across files
- No duplicate requirements with different IDs
- Terminology matches `_context.md` glossary throughout
- MoSCoW priorities consistent across files
- Numerical targets consistent across files
- User roles, data entities, and relationships consistent
- Business rules do not conflict with each other
- Integration requirements align with `plancasting/tech-stack.md`
- Timeline milestones consistent with scope
- Cost estimates align with technical complexity

**technical-reviewer**: Technical feasibility, accuracy, completeness.
- FRs feasible with specified tech stack
- NFR targets realistic
- Data model supports all described FRs
- Integration requirements reference real, available APIs
- Security requirements follow current best practices
- Scalability requirements align with chosen infrastructure
- Mermaid diagrams syntactically valid
- Performance requirements account for full feature set running simultaneously
- Data volume projections realistic
- DR/backup requirements achievable with specified stack

Issue severity definitions: CRITICAL (blocks development), HIGH (causes rework), MEDIUM (reduces clarity), LOW (polish).

### Step 8: Remediation (Phase 6)

1. Consolidate review reports, remove duplicate findings
2. CRITICAL and HIGH issues: remediation is MANDATORY
3. Fix root causes, not symptoms. When fixing contradictions, consult the Business Plan for the correct version. When adding missing requirements, follow the same ID conventions.
4. If >15 CRITICAL+HIGH fixes, perform targeted re-review of modified files (single pass — do not enter recursive loop)
5. Create `./plancasting/brd/_review-log.md` with all findings, including:
   - **Assumption Review Status** section (required if assumption volume ≥ 30%): assumption percentage, CRITICAL flag, operator review marker (operator must update to YES before Stage 2B can pass)
6. Output Final Summary: requirement counts by category, feature coverage, assumptions flagged, assumption percentage, mermaid diagrams, cross-feature interactions, quality metrics (issues found/resolved/remaining). End the summary with one of two lines: `Stage 1 gate: PASS (assumption volume N% < 30%)` or `Stage 1 gate: AWAITING OPERATOR REVIEW (assumption volume N% ≥ 30%)`. The second line means the business plan is too thin to build from unreviewed: the pipeline stops here, and the operator either revises the plan and re-runs Stage 1 or reviews the assumptions and sets `Operator reviewed: YES` in `_review-log.md` (Stage 2B fails without it)

## Known Failure Patterns to Avoid

1. **Vague acceptance criteria**: Use specific metrics ("response time < 200ms"), not unmeasurable adjectives ("fast").
2. **Copy-pasting business plan text**: Translate into structured requirement format with IDs and priority.
3. **MoSCoW inflation**: Maintain reasonable distribution across Must/Should/Could/Won't. Healthy distribution: Must 50-65%, Should 20-30%, Could 10-15%, Won't 0-5%.
4. **Missing negative requirements**: Specify what the system must not do.
5. **Circular traceability**: Each requirement level must add specificity.
6. **NFRs without measurement methods**: Define how metrics are measured and monitored.
7. **Mermaid syntax errors**: Validate syntax before including. Common errors: missing quotes around labels with special characters, incorrect arrow syntax, unclosed subgraph blocks.
8. **Thin business plan extrapolation**: If >30% of requirements are assumptions, flag as CRITICAL.

## Writing Guidelines Summary

- Every requirement traces to a specific Business Plan section
- Measurable acceptance criteria (no "fast", "user-friendly", "scalable" without quantification)
- Mark assumptions with `> ⚠️ ASSUMPTION:` blockquotes (must explain reasoning and impact)
- Use mermaid syntax for all diagrams
- Relative markdown links for cross-references
- Lowercase anchors in heading IDs (`#br-001` not `#BR-001`)
- Clear, precise, professional tone in session language
- Active voice ("The system validates" not "The input is validated")

## Output Specification

| Output | Location | Description |
|---|---|---|
| BRD files | `./plancasting/brd/` | 23 numbered markdown files (00-22) |
| Shared context | `./plancasting/brd/_context.md` | ID registry, glossary, feature inventory |
| Review log | `./plancasting/brd/_review-log.md` | Quality review findings, assumption review status |
| Navigation hub | `./plancasting/brd/README.md` | File descriptions, reading order |

Expected total: 26 files (23 numbered specification files + 3 supporting files)
