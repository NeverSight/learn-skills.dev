---
name: adr
description: Research architecture decisions and create Architecture Decision Records (ADRs). Use when facing complex technical choices requiring deep research, options analysis, and formal documentation. Treats user as CTO for collaborative decision-making. Supports evolutionary architecture - can challenge prior decisions when evidence warrants.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input to identify the decision topic before proceeding.

---

## Overview

This skill conducts deep research on architecture decisions and produces formal ADRs following MADR 4.0 format, aligned with ARC42 Section 9 guidance.

**Key Principles:**
- **Research-heavy**: Minimum 3-5 WebSearch queries per decision
- **Collaborative**: User is the CTO - validate scope, options, and decisions with them
- **Evolutionary**: Can challenge and supersede prior decisions when evidence warrants
- **Constitution-aligned**: Check all options against the 8 governing principles

---

## Phase 1: Scoping & Context Loading

**Goal**: Understand the decision topic and load project context.

### 1.1 Load Architecture Context

Read these files to understand project constraints and prior decisions:

1. `docs/agentlint-architecture-vision.md` - Current architectural direction
2. `docs/design-questions.md` - Open questions, constraints, decision log
3. `.specify/memory/constitution.md` - 8 governing principles

### 1.2 Check Prior Decisions

- Scan `docs/architecture/adr/` for existing ADRs on related topics
- Check Section 11 (Decision Log) in design-questions.md
- Note any decisions that might be affected or superseded

### 1.3 Clarify Scope

Use AskUserQuestion to clarify:
- What specific problem or choice does this address?
- What constraints or requirements apply?
- Any options you're already considering?
- Are there related prior decisions to consider?

---

## Phase 2: Deep Research

**Goal**: Gather comprehensive external and internal context.

### 2.1 Web Research (REQUIRED - Multiple Searches)

Use WebSearch tool for at least 3-5 queries:

```
Search patterns:
- Best practices: "{topic} best practices 2025 2026"
- Documentation: "{technology} documentation guide"
- Comparisons: "{option A} vs {option B} comparison"
- Recent developments: "{topic} latest updates 2025"
- Trade-offs: "{topic} trade-offs considerations"
```

Record key findings with source URLs for citation in the ADR.

### 2.2 Codebase Analysis (If Applicable)

If implementation already exists:
- Use Task(Explore) to understand current patterns
- Identify constraints from existing code
- Note integration points and dependencies

### 2.3 Prior Art Review

- Read related ADRs for consistency in format and terminology
- Cross-reference design-questions.md for constraints
- Check if this relates to unresolved questions in Sections 9-12

### 2.4 Evolutionary Check

Ask yourself:
- Does research reveal better approaches than prior decisions?
- Has technology changed since prior decisions were made?
- Are there new best practices that weren't available before?

If yes, flag potential supersession opportunities with evidence.

---

## Phase 3: Options Analysis

**Goal**: Structure findings into comparable options.

### 3.1 Generate Options

Create 2-4 viable options based on research. Each option should be:
- Distinct (not minor variations)
- Viable (could actually be implemented)
- Relevant (addresses the decision drivers)

### 3.2 Analyze Each Option

For each option, document:

| Aspect | What to Include |
|--------|-----------------|
| Summary | 1-2 sentence description |
| Pros | Benefits, strengths, alignment with goals |
| Cons | Risks, trade-offs, limitations |
| Constitution | Check against 8 principles (see below) |
| Complexity | Low / Medium / High implementation effort |

### 3.3 Constitution Compliance Check

For each option, verify alignment with the 8 constitutional principles:

1. **Local-First**: Does it keep data on user's machine?
2. **Improvement-Oriented**: Does it support continuous improvement?
3. **Causal-First**: Does it enable tracing issues to origin?
4. **Mixed-Methods**: Does it support both quantitative and qualitative?
5. **Language-Agnostic**: Does it work across programming languages?
6. **Agent-Agnostic**: Does it support multiple AI coding agents (via adapters)?
7. **Intelligent Tooling**: Are tools selected based on task needs? Can agent choose freely?
8. **Compounding Value**: Does value compound over time through baselines?

Flag any violations or tensions explicitly.

### 3.4 Identify Decision Drivers

List the forces shaping this decision:
- Technical constraints (from research/codebase)
- Project principles (from constitution)
- Resource considerations (complexity, dependencies)
- Risk tolerance (what failure modes are acceptable?)

### 3.5 Formulate Recommendation

Based on the analysis, recommend one option with clear reasoning:
- Why it best addresses the decision drivers
- How it aligns with constitutional principles
- What trade-offs are being accepted

---

## Phase 4: Collaborative Decision

**Goal**: Get user validation and final decision.

### 4.1 Present Research Summary

Report to the user:
1. **Key findings** from web research (with source links)
2. **Options table** with recommendation marked
3. **Constitution compliance** notes for each option
4. **Concerns** about existing architecture (if any)

### 4.2 Get User Decision

Use AskUserQuestion to:
- Present options with your recommendation first (add "(Recommended)" to label)
- Allow user to select an option or provide alternative
- Validate key assumptions made during research
- Confirm the decision drivers are accurate

### 4.3 Handle Supersession (If Applicable)

If this decision would supersede an existing ADR:
- Present the evidence for reconsideration
- Link to the ADR being superseded
- Get explicit approval before proceeding
- Note: User must explicitly approve supersession

---

## Phase 5: ADR Creation

**Goal**: Document the decision formally.

### 5.1 Get ADR Filepath (MUST USE SCRIPT)

**CRITICAL**: You MUST run the numbering script to get the correct ADR path:

```bash
ADR_PATH=$(bash .claude/commands/adr/scripts/create-adr.sh "Decision Title Here")
```

This script:
- Ensures sequential numbering (0001, 0002, etc.)
- Creates `docs/architecture/adr/` directory if needed
- Returns the full filepath for the new ADR

**DO NOT** manually construct the ADR path or number.

### 5.2 Generate ADR Content

Use the template from `references/madr-template.md` to create the ADR:
- Fill all required sections
- Include links to architecture vision and related ADRs
- Cite research sources in "More Information" section
- Set status to "accepted"

### 5.3 Write ADR File

Write the ADR content to the path returned by the script.

### 5.4 Update Decision Log

Add an entry to Section 11 of `docs/design-questions.md`:

```markdown
| {ADR Number} | {Date} | {Title} | {Brief rationale} |
```

### 5.5 Handle Supersession Updates

If superseding a prior ADR:
- Update the old ADR's status to "superseded by ADR-NNNN"
- Add a note in the old ADR linking to the new one

### 5.6 Report Completion

Report to user:
- Path to new ADR
- Summary of decision
- Suggested next steps (see Handoffs below)

---

## Handoffs

After ADR creation, suggest relevant next steps:

- `/speckit.specify` - If the decision enables new feature work
- `/adr` again - If the decision surfaces related questions needing their own ADRs

**Note**: Always handoff to `/speckit.specify` for new work. The speckit workflow flows: specify → plan → tasks → implement. Don't skip steps.

---

## Quality Gates

Before finalizing an ADR, verify using `references/quality-checklist.md`:

- [ ] At least 2 options considered
- [ ] Each option has documented pros/cons
- [ ] Decision drivers are explicit
- [ ] Consequences (positive, negative, neutral) documented
- [ ] Constitution compliance verified (8 principles)
- [ ] Research sources cited
- [ ] Links to related ADRs included
- [ ] User has approved the final decision
- [ ] Numbering script was used for filepath

---

## Key Rules

1. **Always deep research**: No shortcuts. 3-5+ web searches minimum.
2. **Always collaborate**: Use AskUserQuestion at scoping (Phase 1) and decision (Phase 4).
3. **Always use the script**: Never manually construct ADR numbers or paths.
4. **Always check constitution**: Every option must be evaluated against 8 principles.
5. **Always cite sources**: Every ADR must include research sources.
6. **Never finalize without approval**: User must explicitly approve the decision.
