---
name: gap-analysis
description: Performs route-aware gap analysis. In brownfield mode, compares specifications against existing implementation using AST analysis and /speckit.analyze. In greenfield mode, validates specification completeness and prompts for target technology stack selection. Step 4 of 6 in the reverse engineering process.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Gap Analysis (Route-Aware)

**Step 4 of 6** in the Reverse Engineering to Spec-Driven Development process.

**Estimated Time:** 15 minutes
**Prerequisites:** Step 3 completed (`.specify/` directory exists with specifications)
**Output:** `docs/gap-analysis-report.md`

**Terminology:**
- **specification** = the conceptual document describing a feature
- **spec.md** = the file at `.specify/specs/{feature}/spec.md`
- **Spec Kit** / `/speckit` = the GitHub Spec Kit CLI tool

---

## Step 0: Load Configuration

Read `.stackshift-state.json` to determine route and detection type.

If `.stackshift-state.json` does not exist, halt execution and inform the user: "Step 1 (Analyze) must be completed before running gap analysis. Run the analyze skill first." Do not proceed without route determination.

```bash
if [ ! -f .stackshift-state.json ]; then
  echo "ERROR: .stackshift-state.json not found. Run Step 1 (analyze) first."
  exit 1
fi

DETECTION_TYPE=$(cat .stackshift-state.json | jq -r '.detection_type // .path')
ROUTE=$(cat .stackshift-state.json | jq -r '.route // .path')

if [ -z "$ROUTE" ] || [ "$ROUTE" = "null" ]; then
  echo "ERROR: No route defined in .stackshift-state.json. Re-run Step 1 (analyze)."
  exit 1
fi

echo "Detection: $DETECTION_TYPE"
echo "Route: $ROUTE"
```

**Routes:**
- **greenfield** = building NEW app (tech-agnostic specifications)
- **brownfield** = managing EXISTING app (tech-prescriptive specifications)

Log: "Configuration loaded. Route: $ROUTE, Detection: $DETECTION_TYPE. Proceeding to route-specific analysis."

Based on route, branch to the appropriate section below.

---

## Greenfield Route: Specification Completeness Analysis

**Goal:** Validate specifications are complete enough to build a NEW application.
**Not analyzing:** Old codebase (building new, not fixing old).

### GF-1: Review Specification Completeness

For each spec.md file, check for ambiguities, acceptance criteria, and user stories:

```bash
for spec in .specify/specs/*/spec.md; do
  echo "Analyzing: $(basename "$spec")"
  grep "\[NEEDS CLARIFICATION\]" "$spec" || echo "No clarifications needed"
  grep -A 10 "Acceptance Criteria" "$spec" || echo "WARNING: No acceptance criteria found"
  grep -A 5 "User Stories" "$spec" || echo "WARNING: No user stories found"
done
```

If the `.specify/specs/` directory is empty or missing, halt and inform the user: "No specifications found. Run Step 3 (create-specs) first."

Log: "Specification completeness review done. Proceeding to clarification identification."

### GF-2: Identify Clarification Needs

Mark ambiguous areas with `[NEEDS CLARIFICATION]` tags. Common gaps in greenfield specifications:
- UI/UX details missing (layout, interactions)
- Business rules unclear (edge case behavior)
- Data relationships ambiguous (entity modeling)
- Non-functional requirements vague (performance, security targets)

### GF-3: Ask About Target Tech Stack

Prompt the user to choose a technology stack for the new implementation:

```
I have validated the specifications extracted from the old codebase.
Now we need to decide what to build the NEW application in.

What tech stack would you like to use?

Examples:
A) Next.js 15 + React 19 + Prisma + PostgreSQL + Vercel
B) Python FastAPI + SQLAlchemy + PostgreSQL + AWS ECS
C) Ruby on Rails 7 + PostgreSQL + Heroku
D) Your choice: [describe your preferred stack]
```

Document the chosen stack in the project Constitution for consistency.

### GF-4: Create Implementation Roadmap

Write the greenfield roadmap to `docs/gap-analysis-report.md`. Structure the roadmap by build phases (foundation, core features, advanced features). Mark all features as MISSING since greenfield builds from scratch.

Use the template in `operations/report-template.md` as the output format. Adapt it for greenfield by replacing gap details with build-order phases.

Log: "Greenfield gap analysis complete. Report written to docs/gap-analysis-report.md."

---

## Brownfield Route: Implementation Gap Analysis

**Goal:** Identify gaps between specifications and EXISTING codebase implementation.
**Analysis method:** AST-powered analysis (primary), Spec Kit (fallback), manual review (last resort).

### BF-1: Verify Prerequisites

Check if prerequisite scripts are installed for the fallback analysis path:

```bash
if [ ! -f .specify/scripts/bash/check-prerequisites.sh ]; then
  echo "Note: GitHub Spec Kit scripts not found. /speckit.analyze fallback unavailable."
  echo "AST analysis will be the sole automated method."
fi
```

Log: "Prerequisites checked. Proceeding to analysis."

### BF-2a: Run AST-Powered Analysis (PRIMARY)

Run the AST analysis for deep code inspection:

```bash
node ~/stackshift/scripts/run-ast-analysis.mjs roadmap . --format=markdown
```

**Failure detection:** If this command exits with a non-zero code or produces no output, skip to BF-2b. If it produces output, skip BF-2b and BF-2c entirely.

AST analysis provides:
- Function signature verification (not just existence checks)
- Stub detection (functions returning placeholder text)
- Missing parameter detection
- Business logic pattern analysis
- Test coverage gaps
- Confidence scoring (0-100%)
- Phased roadmap with priorities and effort estimates

Log: "AST analysis complete. Found [N] partial, [M] missing features. Proceeding to detailed gap analysis."

### BF-2b: Run Spec Kit Analysis (FALLBACK)

Only execute this step if BF-2a produced no output or failed.

```bash
> /speckit.analyze
```

**Failure detection:** If this command fails with "Script not found" or produces no output, proceed to BF-2c.

Spec Kit checks:
- Specifications marked COMPLETE but implementation missing
- Implementation exists but not documented in specifications
- Inconsistencies between related specifications
- Conflicting requirements across specifications
- Outdated implementation status

Log: "Spec Kit analysis complete. Proceeding to detailed gap analysis."

### BF-2c: Manual Gap Analysis (LAST RESORT)

Only execute this step if both BF-2a and BF-2b failed. Use manual analysis only as a last resort -- it is the least thorough option.

```bash
for spec in .specify/specs/*/spec.md; do
  feature=$(dirname "$spec" | xargs basename)
  echo "Analyzing: $feature"
  status=$(grep "^## Status" "$spec" -A 1 | tail -1)
  echo "  Status: $status"
  clarifications=$(grep -c "\[NEEDS CLARIFICATION\]" "$spec" 2>/dev/null || echo "0")
  echo "  Clarifications needed: $clarifications"
  echo ""
done
```

Log: "Manual analysis complete. Proceeding to detailed gap analysis."

### BF-3: Detailed Gap Analysis

For each finding from the analysis (BF-2a, BF-2b, or BF-2c), perform deeper review:

**A. Review PARTIAL features.** For each partial feature, answer:
- What exists? (backend, frontend, tests, docs)
- What is missing? (specific components, endpoints, UI)
- Why incomplete? (deprioritized, time constraints)
- Effort to complete? (hours estimate)
- Blockers? (dependencies, unclear requirements)

**B. Review MISSING features.** For each missing feature, answer:
- Is it actually needed? (or can it be deprioritized?)
- User impact if missing? (critical, important, nice-to-have)
- Implementation complexity? (simple, moderate, complex)
- Dependencies? (what must be done first)

**C. Assess technical debt** from `docs/reverse-engineering/technical-debt-analysis.md`:
- Code quality issues
- Missing tests (unit, integration, E2E)
- Documentation gaps
- Security vulnerabilities
- Performance bottlenecks

**D. Mark ambiguous areas** with `[NEEDS CLARIFICATION]` tags for unclear requirements, missing UX/UI details, undefined behavior, and unspecified constraints.

Log: "Detailed gap analysis complete. Proceeding to prioritization."

### BF-4: Prioritize and Create Roadmap

Assign each gap a priority level using these criteria:

- **P0 - Critical:** Blocking major use cases, security vulnerabilities, data integrity issues, broken core functionality.
- **P1 - High:** Important for core user value, high user impact, competitive differentiation, problematic technical debt.
- **P2 - Medium:** Nice-to-have features, improvements to existing features, minor technical debt, edge cases.
- **P3 - Low:** Future enhancements, polish, non-critical optimizations.

Phase the work into three groups: Phase 1 (P0 items), Phase 2 (P1 features), Phase 3 (P2/P3 enhancements). Estimate hours for each phase.

### BF-5: Write Gap Report

Write the report to `docs/gap-analysis-report.md` using the template in `operations/report-template.md`. Populate all sections with findings from BF-3 and BF-4.

Log: "Brownfield gap analysis complete. Report written to docs/gap-analysis-report.md."

---

## Post-Analysis: Spec Kit Integration

After writing the gap report, inform the user of these follow-up commands:

- `/speckit.analyze` - Re-run after making changes to track progress
- `/speckit.tasks {feature}` - Generate tasks for a specific feature
- `/speckit.implement {feature}` - Implement a feature step-by-step
- `/speckit.clarify {feature}` - Interactive Q&A to fill specification gaps

---

## Success Criteria

Verify these outputs exist before reporting completion:

- AST analysis results reviewed (or fallback method executed)
- All inconsistencies documented
- PARTIAL features analyzed (what exists vs what is missing)
- MISSING features categorized
- Technical debt cataloged
- `[NEEDS CLARIFICATION]` markers added where needed
- Priorities assigned (P0/P1/P2/P3)
- Phased implementation roadmap created
- `docs/gap-analysis-report.md` written
- Ready to proceed to Step 5 (Complete Specification)

---

## Next Step

Proceed to **Step 5: Complete Specification** -- use the complete-spec skill to resolve all `[NEEDS CLARIFICATION]` markers interactively.
