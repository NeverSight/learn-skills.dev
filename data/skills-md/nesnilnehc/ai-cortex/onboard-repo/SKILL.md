---
name: onboard-repo
description: Orchestrate repository onboarding by running codebase review, architecture assessment, README generation, and Agent entry setup in sequence. Meta skill; no analysis of its own.
tags: [eng-standards, documentation, automation]
version: 1.0.0
license: MIT
related_skills: [review-codebase, review-architecture, generate-standard-readme, write-agents-entry, discover-skills]
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [onboard, onboard repo]
aliases: [onboard]
input_schema:
  type: code-scope
  description: Repository root path or directory to onboard
  defaults:
    scope: repo
output_schema:
  type: diagnostic-report
  description: Aggregated onboarding report with findings, generated docs, and recommendations
---

# Skill: Onboard Repository (Orchestrator)

## Purpose

**This skill does not perform analysis itself.** It is a **meta skill** that orchestrates a fixed sequence of atomic skills to rapidly onboard a new or unfamiliar repository — producing architecture findings, standardized documentation, and actionable recommendations in one pass. Use it when joining a new project, inheriting a codebase, or preparing a repository for team onboarding. For individual tasks (e.g. only generating a README or only reviewing architecture), invoke the corresponding atomic skill directly ([generate-standard-readme](../generate-standard-readme/SKILL.md), [review-architecture](../review-architecture/SKILL.md), etc.).

---

## Core Objective

**Primary Goal**: Produce a comprehensive repository onboarding report by orchestrating atomic skills in a fixed sequence, aggregating architecture findings, standardized documentation, and recommendations.

**Success Criteria** (ALL must be met):

1. ✅ **Codebase review completed**: Architecture, patterns, and tech debt assessed via [review-codebase](../review-codebase/SKILL.md)
2. ✅ **Architecture findings generated**: Module boundaries, dependency direction, and coupling assessed via [review-architecture](../review-architecture/SKILL.md)
3. ✅ **README generated or improved**: Standardized front-page documentation produced via [generate-standard-readme](../generate-standard-readme/SKILL.md)
4. ✅ **AGENTS.md generated or improved**: Agent entry contract established via [write-agents-entry](../write-agents-entry/SKILL.md)
5. ✅ **Aggregated report delivered**: All findings, generated docs, and recommendations merged into a single onboarding report

**Acceptance Test**: Can a new team member understand the repository's architecture, navigate its structure, and start contributing based solely on the onboarding output?

---

## Scope Boundaries

**This skill handles**:

- Orchestrating atomic onboarding skills in fixed order
- Confirming onboarding scope with user (repo root or specific directory)
- Collecting findings and artifacts from each atomic skill
- Aggregating into a single onboarding report with recommendations

**This skill does NOT handle**:

- Direct code analysis (delegated to [review-codebase](../review-codebase/SKILL.md) and [review-architecture](../review-architecture/SKILL.md))
- Direct documentation authoring (delegated to [generate-standard-readme](../generate-standard-readme/SKILL.md) and [write-agents-entry](../write-agents-entry/SKILL.md))
- Code review for correctness or style (use [review-code](../review-code/SKILL.md))
- Implementation of fixes (use development/refactoring skills)
- CI/CD setup (use [generate-github-workflow](../generate-github-workflow/SKILL.md))

**Handoff point**: When the aggregated onboarding report is complete, hand off to user for review or to development workflow for implementing recommendations.

---

## Use Cases

- **New team member onboarding**: Developer joins a project and needs a rapid overview of architecture, patterns, documentation, and contribution guidelines.
- **Repository acquisition or handoff**: Team inherits a codebase from another team or project; need to understand structure, quality, and gaps before taking ownership.
- **Open-source preparation**: Before making a repository public, run the full pipeline to ensure documentation, agent entry, and architecture quality meet standards.

**When to use**: When the user wants a **comprehensive onboarding pass** across analysis and documentation dimensions. When the user wants only one dimension (e.g. "generate a README" or "review architecture"), use the atomic skill instead.

---

## Behavior

### Orchestration only

- **Do not** analyze code or write documentation yourself. **Do** invoke (or simulate invoking) the following skills **in order**, then aggregate their outputs.
- Execution order is fixed so that Cursor or an agent can follow it step by step.

### Interaction policy

- **Pre-flight**: Before execution, confirm the onboarding scope with the user. Offer: *Onboard from repo root?* [default] *Or pick a subdirectory?* — user selects; do not assume.
- **Existing docs**: If README.md or AGENTS.md already exist, ask: *Improve existing documentation?* [default: Yes] *Or skip documentation steps?*
- **Optional step**: `discover-skills` is optional. If the user wants only analysis and docs, skip it and note the skip in the report.
- Always state which steps were executed and which were skipped (with reason).

### Defaults

| Item | Default | When to deviate |
| :--- | :--- | :--- |
| **Scope** | **Repo root** | User chooses a specific subdirectory. |
| **Existing README** | **Improve** (do not overwrite blindly) | User chooses "skip" or "overwrite". |
| **Existing AGENTS.md** | **Improve** (do not overwrite blindly) | User chooses "skip" or "overwrite". |
| **discover-skills** | **Run** | User chooses "skip optional steps". |

### Pre-flight: confirm before running

**Resolve the following with the user once, before executing any step.** Prefer **confirm default** or **select from options**; avoid asking for free-text input when a default exists.

| Item | If unclear | Action |
| :--- | :--- | :--- |
| **Scope** | Path not stated | Offer: *Onboard from repo root?* [default] *Or pick path: [repo root] [current dir] [list top-level dirs]* |
| **Existing docs** | README or AGENTS.md present | Offer: *Improve existing?* [default: Yes] *Or skip doc generation?* |
| **Optional skills** | Not stated | Offer: *Include skill discovery?* [default: Yes] |

After pre-flight, run the pipeline without further questions; report which steps ran and which were skipped.

### Execution order

When performing this skill, **sequentially apply** the following steps. For each step, load and run the corresponding skill's instructions, collect its output, then proceed to the next step.

1. **review-codebase** — Understand architecture, patterns, tech debt  
   Load [review-codebase](../review-codebase/SKILL.md) and run it on the confirmed scope. Collect all findings (architecture, design, tech debt). This step provides the foundational understanding for subsequent steps.

2. **review-architecture** — Assess boundaries, dependencies, coupling  
   Load [review-architecture](../review-architecture/SKILL.md) and run it on the same scope. Collect architecture-specific findings (module boundaries, dependency direction, cyclic dependencies, interface stability, coupling). This deepens the structural understanding from step 1.

3. **generate-standard-readme** — Create or improve the README  
   Load [generate-standard-readme](../generate-standard-readme/SKILL.md) and run it. Use findings from steps 1–2 to inform content (project purpose, architecture overview, setup instructions). If README exists, improve it; otherwise create from scratch.

4. **write-agents-entry** — Create or improve AGENTS.md  
   Load [write-agents-entry](../write-agents-entry/SKILL.md) and run it. Use findings from steps 1–2 to establish the Agent entry contract (project identity, authoritative sources, behavioral expectations). If AGENTS.md exists, improve it; otherwise create from scratch.

5. **discover-skills** *(optional)* — Recommend additional skills  
   Load [discover-skills](../discover-skills/SKILL.md) and run it on the repository. Based on the stack, patterns, and gaps identified in steps 1–2, recommend skills that would benefit the project (e.g. language-specific review skills, CI/CD skills). If skipped, note in report.

6. **Aggregation**  
   Merge all collected outputs into **one onboarding report**. Structure the report using the diagnostic-report format (see Appendix). Include:
   - Summary of repository (language, framework, size, key patterns)
   - Architecture findings (from steps 1–2)
   - Documentation status (generated or improved README + AGENTS.md)
   - Skill recommendations (from step 5, if run)
   - Action items and next steps

### Summary for Cursor/Agent

- **When performing this skill, sequentially apply:**
  1. review-codebase (architecture, patterns, debt)
  2. review-architecture (boundaries, dependencies, coupling)
  3. generate-standard-readme (create or improve README)
  4. write-agents-entry (create or improve AGENTS.md)
  5. discover-skills (optional; recommend skills)
  6. aggregate all outputs into one onboarding report
- **Aggregate all outputs into a single diagnostic report** using the format in the Appendix. Do not analyze code or write docs in this skill; only orchestrate and aggregate.

---

## Input & Output

### Input

- **Repository scope**: Path to the repository root or a specific directory to onboard.
- **User preferences**: Whether to improve existing docs, skip optional steps, etc.

### Output

- **Single aggregated onboarding report** in diagnostic-report format (see Appendix) containing: repository summary, architecture findings, documentation status, skill recommendations, and action items.
- **Generated or improved documentation**: README.md and AGENTS.md files (produced by delegated skills).

---

## Restrictions

### Hard Boundaries

- **Do not** perform any code analysis inside this skill. Only orchestrate other skills and aggregate.
- **Do not** write documentation directly. Delegate to `generate-standard-readme` and `write-agents-entry`.
- **Do not** change the execution order; keep review-codebase → review-architecture → generate-standard-readme → write-agents-entry → discover-skills.
- **Do not** invent findings; only include outputs produced by the atomic skills you run.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- **Code review**: Running full review pipeline → Use [review-code](../review-code/SKILL.md)
- **Diff review**: Reviewing current changes → Use [review-diff](../review-diff/SKILL.md)
- **Security audit**: Deep security analysis → Use [review-security](../review-security/SKILL.md)
- **CI/CD setup**: Creating workflows → Use [generate-github-workflow](../generate-github-workflow/SKILL.md)
- **Skill creation**: Writing new skills → Use [refine-skill-design](../refine-skill-design/SKILL.md)

**When to stop and hand off**:

- Onboarding report delivered → User reviews and decides next steps
- User asks "review my code" → Hand off to `review-code`
- User asks "set up CI" → Hand off to `generate-github-workflow`

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **Codebase review completed**: Architecture, patterns, and tech debt assessed via review-codebase
- [ ] **Architecture findings generated**: Boundaries, dependencies, coupling assessed via review-architecture
- [ ] **README generated or improved**: Standardized documentation produced via generate-standard-readme
- [ ] **AGENTS.md generated or improved**: Agent entry contract established via write-agents-entry
- [ ] **Aggregated report delivered**: All findings, docs, and recommendations in one diagnostic report

### Process Quality Checks

- [ ] Was the execution order followed (review-codebase → review-architecture → generate-standard-readme → write-agents-entry → discover-skills)?
- [ ] Were pre-flight items (scope, existing docs handling, optional steps) confirmed with the user before running?
- [ ] Were findings only collected from the atomic skills, not invented?
- [ ] Did this skill refrain from analyzing code or writing documentation directly?
- [ ] Were skipped steps noted with reasons in the report?

### Acceptance Test

**Can a new team member understand the repository's architecture, navigate its structure, and start contributing based solely on the onboarding output?**

If NO: Onboarding is incomplete. Identify missing information and re-run relevant steps.
If YES: Onboarding is complete. Hand off to user.

---

## Examples

### Example 1: Full onboarding of a Node.js monorepo

- **Input**: User says "onboard this repo" pointing at a Node.js monorepo with existing README but no AGENTS.md.
- **Expected**:
  1. Run review-codebase on repo root → collect architecture findings (monorepo structure, shared packages, build pipeline, tech debt).
  2. Run review-architecture → collect boundary and dependency findings (package coupling, cyclic deps, interface stability).
  3. Run generate-standard-readme → improve existing README with standardized structure (add missing sections: architecture overview, setup instructions, contribution guide).
  4. Run write-agents-entry → create AGENTS.md from scratch (project identity, authoritative sources, behavioral expectations).
  5. Run discover-skills → recommend review-typescript, review-react (frontend packages), generate-github-workflow (missing CI).
  6. Aggregate into onboarding report: repository summary, architecture findings, documentation status (README improved, AGENTS.md created), recommendations.

### Example 2: Onboarding a Go microservice

- **Input**: User says "onboard src/services/auth-service" targeting a Go authentication microservice with no existing docs.
- **Expected**:
  1. Run review-codebase on `src/services/auth-service` → collect findings (handler patterns, middleware, database layer, test coverage gaps).
  2. Run review-architecture → collect findings (layer boundaries, dependency injection, external API coupling).
  3. Run generate-standard-readme → create README from scratch.
  4. Run write-agents-entry → create AGENTS.md from scratch.
  5. Run discover-skills → recommend review-go, review-security (auth service), review-sql (database layer).
  6. Aggregate into onboarding report.

### Edge case: Empty or minimal repository

- **Input**: User says "onboard this repo" on a newly initialized repository with only a `.gitignore` and empty `src/` directory.
- **Expected**:
  1. Run review-codebase → findings note: no meaningful code to analyze; report repository as empty/scaffolding stage.
  2. Run review-architecture → findings note: no architecture to assess; skip with reason "no code present".
  3. Run generate-standard-readme → create a minimal README with project name and placeholder sections.
  4. Run write-agents-entry → create a minimal AGENTS.md with project identity and placeholder sections.
  5. Run discover-skills → recommend skills based on intended stack (if detectable from config files like `package.json`, `go.mod`, etc.) or skip with reason "insufficient context".
  6. Aggregate: report clearly states the repository is at scaffolding stage, documentation has been bootstrapped, and recommends running onboard-repo again once code is in place.

---

## Appendix: Output contract

The aggregated onboarding report MUST use the following diagnostic-report structure:

| Section | Content | Source |
| :--- | :--- | :--- |
| **Repository Summary** | Language, framework, size, key patterns, overall health | review-codebase |
| **Architecture Findings** | Module boundaries, dependency direction, coupling, cyclic dependencies, interface stability | review-codebase + review-architecture |
| **Tech Debt & Quality** | Identified debt items, pattern violations, quality concerns | review-codebase |
| **Documentation Status** | README: created/improved/skipped; AGENTS.md: created/improved/skipped; links to generated files | generate-standard-readme + write-agents-entry |
| **Skill Recommendations** | Recommended skills for the repo's stack and patterns; install commands | discover-skills |
| **Action Items** | Prioritized list of next steps (e.g. "fix cyclic dependency in pkg/auth", "add CI workflow", "increase test coverage") | Aggregated from all steps |

### Finding format (for architecture findings)

Findings within the Architecture Findings section use the standard format:

| Element | Requirement |
| :--- | :--- |
| **Location** | `path/to/file.ext` (optional line or range) |
| **Category** | `codebase`, `architecture`, `documentation`, `recommendation` |
| **Severity** | `critical`, `major`, `minor`, `suggestion` |
| **Title** | Short one-line summary |
| **Description** | 1–3 sentences |
| **Suggestion** | Concrete fix or improvement (optional) |

### Report format

```markdown
# Onboarding Report: <repository-name>

## Repository Summary
<!-- Language, framework, size, key patterns -->

## Architecture Findings
<!-- Grouped findings from review-codebase + review-architecture -->

## Tech Debt & Quality
<!-- Debt items, pattern violations -->

## Documentation Status
<!-- README and AGENTS.md status -->

## Skill Recommendations
<!-- Recommended skills with install commands -->

## Action Items
<!-- Prioritized next steps -->
```
