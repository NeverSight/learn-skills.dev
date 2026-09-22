---
name: backlog-generator
description: "Transform audit findings into sprint-ready work items with effort estimates, acceptance criteria, and stakeholder-friendly rationale. This converts existing findings into tickets, NOT the process for contributing new components to the system. Trigger when someone says: generate backlog items, create tickets from audit, turn findings into work items, sprint planning from audit, create issues from report, backlog from diagnostic, or anything about converting audit output into actionable work items. Do NOT trigger for defining the contribution process or guidelines for new components — use contribution-workflow for that."
references:
  - ../../knowledge-notes/component-governance.md
---

# Backlog Generator

## Context

The gap between "here are the problems" and "here is the plan for the next eight weeks" is where most audit value dies. Findings get filed, not acted on. Teams read the audit, nod, then move on because the step from "TA-07: Button component tokens not aliased correctly" to "what do we build next sprint?" is too large.

This skill bridges that gap by transforming audit output into structured work items that engineers and product managers can prioritise, estimate, and execute without needing to re-read the audit or negotiate what "fix the tokens" means. The output is sprints, not a wall of problems.

## Boundaries

This skill transforms existing audit findings into work items. It does not run audits itself — if no audit output exists, run the relevant audit skill first. If the audit produced zero findings, there is no backlog to generate; confirm this with the user and stop. If the findings lack severity ratings or remediation guidance, flag the gap and produce work items with what is available, but note the missing context.

---

## Steps

### 1. Accept and Parse Input

Accept input in any form: copy-paste audit report, file path, reference to prior audit skill output, or natural language description of findings.

Parse findings and extract:
- Finding ID (e.g., TA-01, COL-03)
- Severity: Critical, High, Medium, Low
- Category: Token structure, component API, documentation, tooling, process
- Current state: the problem as written in the audit
- Remediation: what the audit says should happen

Do not assume findings are complete. If a finding is vague ("tokens are broken"), ask clarifying questions before proceeding.

### 2. Classify Work Item Type

For each finding, assign one of these work item types:

- **Bug fix:** Something is broken and prevents correct usage (e.g., token alias creates circular reference, component prop ignored in doc site)
- **Tech debt:** Working-as-designed but the design itself is unsustainable (e.g., token hierarchy is flat, component prop not typed)
- **Enhancement:** New capability that enables better practice (e.g., new token tier, new component variant)
- **Migration:** Moving from one system to another (e.g., migrating component token refs from old to new tier)
- **Documentation:** Clarifying existing behaviour or adding examples

Document your reasoning for each classification. Different teams prioritise differently — tech debt might be lower priority than bugs, and that's a decision, not a mistake.

### 3. Generate Structured Work Item

For each finding, produce a work item with all of these fields:

**Title:** Action-oriented, engineer-readable. Prefer "Route component tokens through semantic tier" over "Fix TA-01" or "Token aliasing issue". The title should be understandable without the audit context.

**Type:** Bug fix, tech debt, enhancement, migration, or documentation (from step 2).

**Effort estimate:** T-shirt size with sizing rationale.
- S: <2 hours (single-file change, tests included, no API review needed)
- M: 2–8 hours (multi-file or 1-day work, API implications, needs review)
- L: 1–3 days (multi-component impact, migration step, cross-team coordination)
- XL: 3+ days (system-wide change, major migration, new tooling)

Include 2–3 sentences of sizing rationale (e.g., "M because the Button component changes are isolated to one file, but we need to update three variants and test accessibility scenarios"). Do not estimate from severity — a critical bug might be 30 minutes (S) if it's a one-line fix.

**Acceptance criteria:** 2–4 testable statements. Each should be verifiable by a reviewer without ambiguity.
- Good: "No component token directly references a primitive token (checked via regex in token definitions)"
- Bad: "Fix tier leakage" or "Make tokens work better"

**Rationale:** 1–2 sentences explaining why this work matters to the system and team, not just a technical description. Address: What breaks or becomes harder if this is deferred? Who does this unblock? Example: "Prevents new components from accidentally breaking the token hierarchy; unblocks the Q2 component library expansion."

**Dependencies:** List other work item IDs or titles that must complete first. Be strict — only list blocking dependencies, not nice-to-haves. If a task has no dependencies, write "None".

**Priority:** Inherit from audit severity (Critical → P0, High → P1, Medium → P2, Low → P3), but adjust upward if the item unblocks multiple other items, or downward if high-effort with low impact.

### 4. Group into Phases

Sort work items into phases based on dependencies and effort:

- **Immediate (Sprint 1):** Critical items and P1 work that has no dependencies or depends only on other Sprint 1 items. Aim for 1–2 weeks of effort.
- **Near-term (Sprint 2–3):** P1–P2 items that depend on Immediate work, or independent P2 items. Aim for 2–4 weeks of effort.
- **Backlog (future):** P3 items, nice-to-have enhancements, documentation that can wait.

Do not create a phase assignment that violates dependency order (e.g., assigning a Sprint 1 item that depends on a Sprint 2 item). Review the dependency DAG before finalising phase groups.

### 5. Build Dependency Map

Create a visual or textual dependency map showing which items block which other items. Format: simple text DAG or a markdown table with columns for Item, Depends On, Unblocks.

Flag any circular dependencies immediately — they indicate a misunderstanding of the problem or a need to re-scope work items. Example: If Item A depends on Item B and Item B depends on Item A, stop and clarify the actual order with the team.

### 6. Produce Markdown Output

Generate a markdown document with:

**Summary section:**
- Total findings analysed
- Work item count by type (bugs, tech debt, enhancements, migrations, docs)
- Work item count by phase (Immediate, Near-term, Backlog)
- Total effort (sum of all T-shirt size estimates, translated to weeks if helpful)
- Dependency warnings, if any

**Summary table:**
All work items in a single table with columns: ID, Title, Type, Effort, Priority, Phase, Dependencies. Keep descriptions short; readers will dive into detailed cards for context.

**Detailed cards:**
One card per work item with all fields from step 3 (title, type, estimate with rationale, acceptance criteria, rationale, dependencies, priority).

**Dependency section:**
Text or ASCII representation of the dependency DAG. Highlight any chain longer than 3 items (suggests the phase grouping may be too aggressive).

**Tool mapping section:**
Guidance for translating this markdown output into Jira, Linear, GitHub Issues, or Asana without tool-specific API calls. Include field mapping (e.g., "Effort = Story Points or custom field; Priority = Jira priority label; Phase = Sprint or custom field"). Do not write scripts or API calls — keep this human-readable guidance.

## Quality Checks

1. **Every work item title is action-oriented and engineer-readable.** A developer should understand what to build without re-reading the audit. Titles like "Flatten token hierarchy" or "Add size variant to Button" pass; "Fix token issue" does not.

2. **Acceptance criteria are testable.** Each criterion should be verifiable by code review, test output, or inspection without debate. "Button component uses semantic tokens" is vague; "Button component has zero direct references to primitive tokens" is testable.

3. **Effort estimates include sizing rationale, not just a letter.** Why is this S and not M? Why is that L and not XL? Document the reasoning (scope, risk, coordination overhead, etc.).

4. **Rationale explains business impact, not just technical description.** Do not repeat the audit finding. Explain why engineers should care, what risk the team avoids, what capability it unblocks.

5. **Dependencies form a valid DAG.** No circular references. If Item A depends on Item B, Item B cannot depend on Item A (directly or transitively). Run a topological sort to verify.

6. **Phase grouping respects dependency order.** No Sprint 1 item can depend on a Sprint 2 item. No Sprint 2 item can depend on a Backlog item (unless you're willing to schedule Backlog work early). Review the dependency map against phase assignments before finalising.

## Small-System Note

For audit reports with fewer than 10 findings, produce a single prioritised list (Immediate, Near-term, Backlog) rather than phased sprints. The structure is the same; the grouping is simpler. Dependencies still matter even for small systems.
