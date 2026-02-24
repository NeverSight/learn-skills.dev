---
name: codebase-explorer
description: >
  A structured method for exploring and understanding unfamiliar codebases.
  Use this skill whenever the user asks to explore, understand, audit, review,
  or navigate a codebase they haven't worked in before. Also trigger when the
  user says things like "help me understand this code", "what does this repo do",
  "walk me through this codebase", "explore this project", "I inherited this code",
  "onboard me to this system", or asks about the architecture, structure, or
  health of an existing codebase. Trigger even if they just drop a repo path
  and say "what is this". This skill produces structured understanding — not
  summaries, but navigable maps of how code actually works.
---

# Codebase Explorer

A field manual for understanding unfamiliar code. Produces navigable maps of system behavior, not summaries of file contents.

## Core Principle

The file tree is storage, not understanding. Directory structure reflects how a team organized artifacts. Logic traces reveal why code exists and what it does. When these conflict, trust the trace.

Understanding is not "I have read the code." Understanding is "I can tell you what happens when X changes."

You cannot understand a whole system. Build a portfolio of **vertical slices** — complete paths from input to output that let you predict behavior in bounded regions.

---

## Who This Is For

This skill produces different value for different audiences. **Adapt depth and vocabulary to the user's role.**

| Audience                      | What They Need                                         | Emphasize                                                         |
| ----------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------- |
| **Developer inheriting code** | Where to start, what's safe to change                  | Vertical slices, shared fate groups, implicit contracts           |
| **Tech lead / architect**     | Risk map, coupling analysis, refactoring targets       | Smells, shared fate groups, substrate constraints                 |
| **Engineering manager**       | Change cost estimates, team coordination needs         | Risk profile, shared fate groups, unknowns                        |
| **Product manager**           | What's hard to change vs. easy, where bottlenecks live | Risk profile (in business terms), substrate constraints           |
| **Security auditor**          | Attack surface, data flow, trust boundaries            | I/O boundary map, implicit contracts, data lineage                |
| **New hire onboarding**       | Mental model of how the system works                   | Pipeline flow / architecture diagram, atmosphere, vertical slices |
| **Consultant / contractor**   | Fast orientation before making changes                 | Quick Assessment template, archetype classification               |
| **Due diligence reviewer**    | Code quality signal, technical debt inventory          | Smells, activity heat map, unknowns                               |

When the user's role is unclear, default to the developer perspective but include risk profile and unknowns sections — these are universally useful.

---

## When This Skill Shines

This skill adds the most value in these situations:

- **Inherited codebases** with poor or missing documentation
- **Multi-service architectures** where no one person understands the whole system
- **Pre-rewrite assessment** — understanding what exists before deciding what to replace
- **Incident response** on unfamiliar systems — quickly identifying blast radius
- **Open source contribution** — understanding a project before submitting PRs
- **Post-acquisition evaluation** — assessing code quality and technical debt
- **Compliance / security audits** — mapping data flow and trust boundaries
- **Onboarding** — giving new team members a navigable mental model

---

## Workflow

The exploration follows four phases. Complete each before moving to the next.

### Phase 0: Archetype Detection (First 2 Minutes)

Before reading any business logic, determine the **archetype** of the codebase. The archetype determines which vertical slice strategy to use, which smells to prioritize, and what the primary output artifact should be.

**Detection method**: Check the root directory for signature files.

| Signal Files                                                              | Archetype                  |
| ------------------------------------------------------------------------- | -------------------------- |
| `template.yaml` / `serverless.yml` / `statemachine/` / `stepfunctions/`   | **Serverless Pipeline**    |
| `Dockerfile` + route handlers (`app.py`, `server.js`, `main.go`)          | **Backend API**            |
| `package.json` with React/Vue/Svelte/Next + `src/components/`             | **Frontend Application**   |
| `dags/` / `pipeline/` / `airflow.cfg` / `dbt_project.yml`                 | **Data Pipeline**          |
| `setup.py` / `pyproject.toml` with lib structure, no main entry point     | **Library / SDK**          |
| `main.tf` / `*.tf` / `cdk.json` / CloudFormation without Lambda code      | **Infrastructure as Code** |
| CLI entry points (`__main__.py`, `bin/`, `Makefile` as primary interface) | **CLI Tool**               |
| `train.py` / `model/` / notebooks + `requirements.txt` with ML libs       | **ML System**              |

If multiple signals match, pick the **primary** archetype based on where the most code lives. Note secondary archetypes.

**Output**: Archetype classification with confidence level. This gates all subsequent phases.

---

### Phase 1: Orientation

Before reading business logic, answer four questions about the shape of the system. For each, produce the specified output artifact.

#### Q1: Where is the Dirt?

Map the I/O boundary — where the system touches the world.

1. Identify entry points (main functions, route handlers, event listeners, exported APIs)
2. For each entry point, find the first external call
3. Mark functions: ○ Pure (no I/O) · ● Impure (touches world) · ◐ Mixed
4. Map the boundary: where data enters, where it leaves

**Signals**: `fetch/axios/http` → network · `fs/readFile` → filesystem · `query/execute/find/save` → database · `Date.now()/Math.random()` → non-determinism · `process.env/config.get` → environment coupling

**Output**: I/O boundary map

#### Q2: What is the Substrate?

Identify the hard limits — memory, payload size, timeouts, rate limits — that constrain what the code can actually do.

1. Check dependency manifests for runtime constraints
2. Find config files, note limits: `maxPayloadSize`, `timeout`, `poolSize`, `maxRetries`
3. For web apps: measure initial payload size and request count
4. Search for memory patterns: streams, pagination, cursors, chunking — absence is a smell

**Signals**: Hardcoded round-number timeouts (30000, 60000) · Missing pagination on list endpoints · Synchronous reads of user-provided paths · Unbounded array accumulation

**Output**: Constraint list with compliance notes

#### Q3: What are the Implicit Contracts?

Find magic values — literals that encode business semantics without naming them.

1. Search for string literals in conditionals: `if (x === "some_string")`
2. Search for numeric literals other than -1, 0, 1, 2
3. For each: would this break if the _meaning_ of data changed?
4. Flag literals that assume specific values exist in databases or external systems

**Distinguish**: Config values (ports, batch sizes) are tuning parameters, not magic. Magic values encode _semantics_: status codes, type discriminators, string-matched business logic.

**Output**: Fragility list

#### Q4: Where is Attention Flowing?

Use git history to map organizational memory. **Start with a single probe command** before investing in detailed analysis.

**Step 1 — Probe**: Run `git log --oneline -1` first. If this fails (orphan branch, no commits), skip to fallback signals.

**Step 2a — If history exists**:

1. `git log --oneline -100` — recent activity themes
2. `git log --format='%H' --since='6 months ago' | wc -l` — velocity
3. For key files: `git log --oneline -10 <file>` — change recency
4. Identify files with zero commits in 12+ months

**Signals**: 50+ commits in 3 months → hot zone · Unchanged 2+ years → frozen · Recent "fix"/"hotfix"/"revert" clusters → instability · Single-author files → knowledge silos

**Step 2b — If NO history exists** (orphan branch, fresh repo, extracted code):

1. Check `git status` — staged vs. untracked files reveal intent
2. Check `git remote -v` — presence/absence of remote reveals deployment maturity
3. Check `git branch -a` — orphan branch or missing main = pre-initial-commit
4. Look for deleted files in staging (`AD` prefix) — reveals prior architecture that was replaced
5. Check file modification times via `ls -lt` on key directories

**Output**: Activity heat map (from git history) OR maturity assessment (from fallback signals). State which signal source was used.

---

### Phase 2: Vertical Slices (The Value Trail)

Do not survey the whole system. Trace a single observable value from one end of the system to the other. One complete vertical slice is worth more than a shallow survey of everything.

**The slicing strategy depends on the archetype detected in Phase 0.**

---

#### Strategy A: Frontend Applications — Trace a Visible Value

**Step 1 — Pick a Value**: Something visible and concrete. "The green marker." "The number 63 in the header."

**Step 2 — Trace Upstream** (Render → Logic): Find the code that produces this value. You want the _render site_.

**Step 3 — Trace Data** (Logic → State): Follow backward through assignments. You want the _decision point_.

**Step 4 — Trace Source** (State → Input): Find where the data originates — API, database, user input. You want the _boundary_.

**Step 5 — Record**: Entry point, decision points, render site, impure calls along the path.

---

#### Strategy B: Pipelines — Trace a Record Through Stages

Pipelines have no "render site." Data transforms as it flows. The natural slice is: follow one entity from ingestion to final output.

**Step 1 — Pick an Entity**: A concrete data object the pipeline processes. "One arXiv paper." "One customer order."

**Step 2 — Trace Forward** (Ingestion → Output): At each stage, answer:

- What fields does this stage **read**?
- What fields does this stage **add, modify, or remove**?
- What **external calls** happen?
- What is the **storage location** where the result lands?
- What **implicit contracts** exist with the next stage?

**Step 3 — Map Schema Evolution**: How does the entity's shape change at each stage? This is the pipeline's real architecture.

**Step 4 — Identify Inter-Stage Contracts**: For each handoff:

- Serialization format (JSON, JSONL, Parquet)
- Storage location convention (hardcoded vs. config)
- Which fields the next stage assumes exist
- Whether validation happens at the boundary

**Step 5 — Record**: Produce a **data lineage map**: stage → transformation → output location → next stage. Mark each boundary with its contract type.

This is the **primary artifact** for pipeline codebases.

---

#### Strategy C: Backend APIs — Trace a Request

**Step 1 — Pick a Request**: A concrete endpoint that touches multiple layers.

**Step 2 — Trace Inward**: Route → middleware → handler → service → persistence.

**Step 3 — Trace the Response**: How is data shaped for return? Where are errors caught?

**Step 4 — Record**: Route → middleware chain → handler → service calls → data access → response shaping.

---

#### Strategy D: Libraries / SDKs — Trace a Public API

**Step 1 — Pick an Exported Function**: The most-used public API (check README or tests).

**Step 2 — Trace Inward**: Public interface → internal modules → core logic.

**Step 3 — Map Abstraction Layers**: Where does the library hide complexity?

**Step 4 — Record**: Public API → internal dispatch → core logic → edge case handling.

---

#### Strategy E: Infrastructure as Code — Trace Resource Dependencies

**Step 1 — Pick a Core Resource**: The one other resources depend on most.

**Step 2 — Trace Dependents**: What breaks if this changes? Follow `Ref`, `!GetAtt`, `depends_on`.

**Step 3 — Identify Blast Radius**: What must deploy together?

**Step 4 — Record**: Resource → dependents → blast radius → deployment order.

---

#### General Guidance

Repeat for 3–5 slices. These usually reveal the system's true architecture.

For advanced techniques (handling trace convergence, recognizing dead code), see `references/advanced-techniques.md`.

---

### Phase 3: Smell Detection

Scan for architectural smells — patterns that signal structural problems. Prioritize smells that match the detected archetype.

Read `references/smell-catalog.md` for the full catalog with signals, risks, and verification procedures.

**Universal smells** (check regardless of archetype):

| Smell           | Signal                                  | Risk                        |
| --------------- | --------------------------------------- | --------------------------- |
| Hidden Schema   | String-matching values in conditionals  | Fragility to data migration |
| Silent Overflow | Unbound iteration without size guards   | Scale failure               |
| God Object      | 1000+ line files, 20+ method classes    | Comprehension collapse      |
| Orphaned Error  | Empty catch blocks, log-and-forget      | Silent failure              |
| Time Bomb       | Hardcoded years, fixed date comparisons | Predictable future failure  |

**Pipeline-specific smells** (prioritize for Data Pipeline / Serverless Pipeline):

| Smell                         | Signal                                                    | Risk                                   |
| ----------------------------- | --------------------------------------------------------- | -------------------------------------- |
| Drifting Duplicates           | Same config value in multiple stages                      | Silent inconsistency                   |
| Implicit Inter-Stage Contract | Dict access without schema validation at boundaries       | Silent breakage when upstream changes  |
| Path Convention as Schema     | Storage paths hardcoded in every stage                    | Rename requires finding all stages     |
| Assembly Without Validation   | Final stage assembles N inputs without completeness check | Partial output published as complete   |
| Shared Utility SPOF           | One function imported by 50%+ of stages                   | Total pipeline failure from single bug |

---

### Phase 4: Risk Profile and Unknowns

This is where exploration becomes actionable. Synthesize findings into decisions the reader can make.

**Risk Profile** — be specific, not vague:

- Not "complex" but: "Changing the User model requires migration + API update + frontend update."
- Not "risky" but: "This function has 8 callers and no tests. A bug here breaks scoring for all papers."

**Unknowns** — explicitly mark what you didn't explore and why. Unstated assumptions become false beliefs.

**Verification pointers** — for each high-risk area, note what you'd test first. See `references/advanced-techniques.md` for verification procedures.

---

## Output Artifacts

Read `references/documentation-templates.md` for complete templates. Choose based on archetype and audience.

### Choosing the Right Template

| Situation                            | Template                    |
| ------------------------------------ | --------------------------- |
| Full exploration, any archetype      | Full Exploration Report     |
| Full exploration, pipeline archetype | Pipeline Exploration Report |
| Time-limited or narrow scope         | Quick Assessment            |
| Tracing a single value               | Vertical Slice Record       |
| Pipeline data flow                   | Data Lineage Map            |
| Focused health check                 | Smell Report                |
| Non-technical stakeholder briefing   | Stakeholder Brief           |

### Output Principles

**Maps, not lists.** Group code by **shared fate** — components that fail together, change together, or depend on the same external resource.

**Decisions, not descriptions.** Every section should help the reader decide something: where to look, what to change, what to avoid, who to coordinate with.

**Audience-appropriate language.** For technical audiences, use file paths and function names. For PMs and managers, translate to business impact: "This component is fragile" → "Changes to the scoring algorithm require updating two files that aren't linked — if someone updates one and forgets the other, newsletter quality degrades silently."

---

## Quick Reference

### Phase 0: Archetype → Strategy Mapping

| Archetype                  | Slice Strategy                   | Primary Artifact         |
| -------------------------- | -------------------------------- | ------------------------ |
| Frontend Application       | A: Trace visible value           | Render-site trace        |
| Data / Serverless Pipeline | B: Trace record through stages   | Data lineage map         |
| Backend API                | C: Trace a request               | Request lifecycle trace  |
| Library / SDK              | D: Trace public API              | Abstraction layer map    |
| Infrastructure as Code     | E: Trace resource dependencies   | Blast radius map         |
| CLI Tool                   | D (adapted): Trace a command     | Command execution trace  |
| ML System                  | B (adapted): Trace training data | Data + model lineage map |

### Orientation Checklist

| Question                         | Output                                   |
| -------------------------------- | ---------------------------------------- |
| What is this? (Phase 0)          | Archetype classification                 |
| Where is the dirt?               | I/O boundary map                         |
| What is the substrate?           | Constraint list                          |
| What are the implicit contracts? | Fragility list                           |
| Where is attention flowing?      | Activity heat map OR maturity assessment |

### Value Trail Steps (by archetype)

**Frontend (A)**: Pick value → render site → decision point → input boundary → record

**Pipeline (B)**: Pick entity → trace through stages → map schema evolution → identify contracts → data lineage map

**Backend API (C)**: Pick request → trace inward → trace response → record

**Library (D)**: Pick public API → trace inward → map abstractions → record

**IaC (E)**: Pick resource → trace dependents → identify blast radius → record
