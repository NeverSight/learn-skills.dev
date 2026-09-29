---
name: lcs-master
description: 'Use this skill as the single entry point / router for the entire Lean Coding Skills (LCS) workflow. Activate when the user wants to "start", "begin", "what should I do next", "route me", has an ambiguous LCS request, or otherwise needs the correct LCS skill selected and invoked. lcs-master actively analyzes user intent, recognizes starting situations (on-ramps), recommends the next skill with rich contextual guidance, and runs in either confirmation mode (asks each step) or autopilot mode (chains skills, stopping at critical points). Enforces the shared contract (path conventions, exact skill-name routing, decision log) on every handoff. Supports multi-workitem management (list, switch, resume, reconciliation). Do NOT activate when request names a specific downstream skill (e.g. "run lcs-toprd") — invoke that skill directly.'
adapters: [claudecode, opencode]
compatibility: [claudecode, opencode]
chain_of_truth_level: Standard
---

# LCS Master — Enhanced Contextual Router / Orchestrator

Shared Coding Contract: Refer to `../lcs-shared/contract.md` for folder conventions, Handoff format, Chain Truth level mapping, token optimization. This skill is a **router**, not an author of artifacts itself. It selects and invokes the correct downstream LCS skill, enforces the contract on every handoff, and records a decision log.

## Purpose

One skill to rule all. `lcs-master` is a **contextual router** over 21 LCS skills:
- Recognizes **starting situations** (on-ramps) and routes the flow accordingly
- Integrates **vocabulary foundation** (domain-modeling, codebase-design) as a layer beneath all skills
- Supports **branching logic** (prototype detour, wayfinder detour) without breaking Chain of Truth
- Provides **rich contextual guidance** with alternative paths and critical warnings
- Enforces **shared contract (SOT)** on every handoff: correct path, exact skill name, decision log
- Performs **precondition check** before the first routing in a new repo
- Supports **multi-workitem operations**: list open items, switch between them, resume from saved phase
- Performs **idempotent reconciliation** of legacy state and work-item directories

## Trigger

Activate when user:
- Says "start", "begin", "what do", "route me", "next step", or similar
- Has an ambiguous or multi-stage LCS request (e.g. "I want to build a feature" without specifying the stage)
- Explicitly names `lcs-master` or asks for "master" / "router" skill
- Reports a bug, huge project, or mid-workflow situation (on-ramps)

Do NOT activate when request names a specific downstream skill (e.g. "run lcs-toprd") — invoke that skill directly.

---

## [NEW] Precondition Check

Sebelum routing pertama di repo baru, verify prerequisites:

### Checklist
1. **`.lcs/` directory exists?** → If no, create it dengan structure dasar
2. **Shared contract accessible?** → Verify `skills/lcs-shared/contract.md` exists
3. **State file exists?** → If no `.lcs/state.md`, create dengan initial state:
   ```yaml
   ---
   title: "LCS State"
   format_version: "okf/0.2"
   authors:
     - type: agent
       name: "lcs-master"
   created: "2026-08-08"
   updated: "2026-08-08"
   tags: [state]
   summary: "Active work item state"
   status: active
   related: []
   artifact_type: state
   source: "runtime"
   cot_level: standard
   version: "1.0"
   type: state
    current_phase: idle
    current_work: null
    work_items: {}
    last_session_note: "Initial setup"
   timestamp: 2026-08-08T00:00:00+07:00
   ---
   ```
4. **Domain setup (optional)?** → Check jika `CONTEXT.md` exists di project root. If no, offer to create empty template untuk domain glossary.

### Behavior
- **Non-blocking:** Jika precondition gagal, guide user through setup, jangan block workflow
- **First-time only:** Skip precondition check jika `.lcs/state.md` exists dengan `current_phase != idle`
- **Log setup:** Append setup actions ke session-log.md

---

## [NEW] Contextual Entry Points (On-ramps)

Recognize starting situations dan route ke flow yang tepat:

### On-ramp 1: Bug Reports & Issues
**Trigger:** User mentions "bug", "error", "regression", "failing test", "unexpected behavior"
**Route:**
- **Single bug** → `lcs-debug` (enhanced 6-phase disciplined loop)
  - Critical Warning: Phase 1 (Build Feedback Loop) MUST complete sebelum hypothesizing
- **Multiple issues piling up** → Manual prioritization 
  - List issues dengan severity (P0-P3), user picks one untuk start
**Flow:** lcs-debug → lcs-toprd (if bug implies missing requirement) → lcs-prd-reviewer → lcs-tosrs → main flow

### On-ramp 2: Huge Foggy Projects
**Trigger:** User describes project yang "too big for one session", "unclear requirements", "greenfield", "multi-week effort"
**Route:**
1. `lcs-wayfinder` → Chart decision map dengan decision tickets
2. Resolve decision tickets one per session
3. When map clears, Handoff to `lcs-toprd` → lcs-prd-reviewer → lcs-tosrs → continue main flow
**Critical Warning:** Do NOT loop wayfinder straight into task-executor. Always collapse decisions into PRD first.

### On-ramp 3: Codebase Maintenance
**Trigger:** User wants to "improve architecture", "refactor", "clean up code", "deepen modules"
**Route:**
1. `lcs-codebase-doc` → Map current state
2. `lcs-domain-modeling` — Sharpen domain language and architecture vocabulary
3. Main flow untuk implementasi: explore → toprd → prd-reviewer → tosrs → task-slicer → ...
**Note:** Maintenance tidak tercampur dengan feature work. Selalu start dengan mapping.

### On-ramp 4: Mid-Workflow Situations
**Trigger:** User sudah di tengah workflow tapi stuck atau butuh situational help
**Route:**
- **Merge conflict** — manual resolution (no dedicated skill yet)
- **Need research** → `lcs-research` (background agent) → return ke main flow
- **Need prototype** → `lcs-prototype` (throwaway validation) → return ke main flow
- **Need wizard** → `lcs-wizard` (human-in-the-loop setup) → user executes manually
**Behavior:** Standalone skills tidak memutus main flow. Setelah complete, return ke skill yang memanggil.

---

## [ENHANCED] Main Flow dengan Branching Logic

Optional: If user wants to register a blank work item first, route to `lcs-new` before `lcs-explore`.

```
lcs-new (optional blank registration)
  ↓ (optional)
lcs-explore (brainstorm)
  ↓
[Branch: Need visual/interactive validation?]
  ├─ Yes → lcs-prototype (throwaway prototype)
  │         ↓
  │       Archive prototype, fold decisions into explore.md
  │         ↓
  └─ No → Continue
  ↓
lcs-toprd (create PRD)
  ↓
[Branch: Multi-session build?]
  ├─ Yes → lcs-wayfinder (chart decision map) → lcs-toprd (when clear)
  └─ No → Continue
  ↓
lcs-prd-reviewer → lcs-tosrs → lcs-task-slicer → lcs-task-executor → lcs-code-review → lcs-doc-finalizer
```

### Branching Rules

**Prototype Detour:**
- **Trigger:** User asks "can we see it?", "I need to validate this visually", "does this logic feel right?"
- **Action:** Invoke `lcs-prototype`, archive after validation, continue main flow
- **CoT Level:** Strict (creates throwaway code)
- **Return:** After prototype complete, fold decisions ke explore.md atau prd.md, continue dari skill yang memanggil

**Wayfinder Detour:**
- **Trigger:** Project description terlalu besar/unclear untuk satu session (>1 week effort)
- **Action:** Invoke `lcs-wayfinder`, resolve decision tickets, handoff back ke main flow
- **CoT Level:** Strict (creates decision map)
- **Return:** When map clears, handoff ke `lcs-toprd` untuk collapse decisions into buildable plan

---

## [NEW] Vocabulary Foundation Layer

Skills that run beneath the main flow sebagai vocabulary sources:

> **Dependency Note:** `lcs-codebase-design` belum ada — jangan route ke skill ini. Saat deep-module vocabulary dibutuhkan, gunakan `lcs-domain-modeling` untuk domain language atau `lcs-codebase-doc` untuk architecture mapping sebagai interim.

### lcs-domain-modeling (Domain Language)
- **Purpose:** Sharpen domain language (CONTEXT.md, ADRs)
- **When to invoke:**
  - Before `lcs-toprd` jika `CONTEXT.md` belum ada atau outdated
  - During `lcs-explore` saat new terms emerge
  - Saat user uses fuzzy/overloaded terms (e.g., "account" doing three jobs)
- **Auto-invoke rule:** Jika user input contains terms yang tidak ada di `CONTEXT.md`, prompt untuk clarify dan update inline
- **Integration:** Referenced oleh semua skills yang generate PRD/SRS/tasks

### Vocabulary Invocation Rules
- **Lazy invocation:** Hanya invoke saat needed, bukan setiap routing
- **Context-aware:** Jika "working in a repo" → invoke domain-modeling. Jika "not in a repo" → skip (use stateless flow)
- **Inline updates:** Domain-modeling updates `CONTEXT.md` immediately, bukan batch up

---

## Routing Modes

### Confirmation Mode (default)
1. Recognize starting situation (on-ramp atau main flow)
2. Check vocabulary foundation (auto-invoke domain-modeling jika needed)
3. Generate rich contextual guidance (recommended skill + reason + context + flow + alternatives + warnings)
4. Ask user untuk confirm atau choose alternative
5. After invoked skill completes, stop dan ask lagi untuk next step
6. Log routing decision ke session-log.md

### Autopilot Mode (opt-in)
User must explicitly choose autopilot. Before chaining:
- If workflow has not yet gathered enough context (no `explore.md` / no clear intent), invoke `lcs-explore` first
- Then chain forward dengan branching logic: explore → [prototype detour?] → toprd → [wayfinder detour?] → prd-reviewer → tosrs → task-slicer → (task-executor / debug-ext)
- **Autopilot STOPS (no prompting) dan writes a SOT blocker** when it reaches a critical point (see Stop Matrix). User reviews blocker later dan resumes.

### Stop Matrix (Autopilot Critical Points)
- After `lcs-explore` → Stop untuk user confirm explore.md
- After `lcs-toprd` → Stop untuk user confirm PRD
- After `lcs-prd-reviewer` → Stop untuk user review enhanced PRD
- After `lcs-task-slicer` → Stop untuk user approve task breakdown
- After each `lcs-task-executor` → Stop untuk user review code changes
- After `lcs-code-review` → Stop untuk user review findings

---

## [NEW] Standalone Skills (Off-Flow)

Skills yang tidak fit main flow tapi dibutuhkan dalam situasi khusus:

### lcs-research (Background Agent)
- **Purpose:** Investigate primary sources, capture cited findings
- **When to use:** User needs facts sebelum decision (API docs, library comparison, RFC review)
- **Integration:** Findings feed back into main flow (e.g., research → explore → toprd)
- **CoT Level:** Standard
- **Trigger:** "Research X", "Find out about Y", "Compare Z libraries"

### lcs-wizard (Human-in-the-Loop)
- **Purpose:** Generate interactive bash scripts untuk manual procedures
- **When to use:** Infrastructure setup, credentials configuration, one-off migrations
- **Integration:** Standalone, user executes manually
- **CoT Level:** Standard
- **Trigger:** "Setup AWS credentials", "Configure CI secrets", "Run migration wizard"

### lcs-resolving-merge-conflicts (Future Enhancement)
- **Purpose:** Resolve git merge/rebase conflicts by intent, not line-by-line
- **When to use:** Mid-merge conflict situation
- **Integration:** Standalone, never `--abort`
- **CoT Level:** Strict
- **Trigger:** "Merge conflict", "Rebase conflict", "Git conflict"

---

## Multi-Workitem Operations

`lcs-master` supports managing multiple open work items via the shared state registry.

### Reconciliation

Before list, switch, or resume operations, `lcs-master` MUST perform idempotent reconciliation:

1. Read `.lcs/state.md`.
2. If `work_items` key is missing, initialize `work_items: {}` and migrate eligible entries:
   - If `current_work` refers to an eligible existing work-item directory, register it with title inferred from slug, canonical path, phase from legacy `current_phase`, `status: open`, and timestamps from the work ID.
   - Scan `.lcs/work-items/` for other eligible legacy work-item directories and import them.
   - Preserve the original selected item and ensure `current_phase` matches.
3. If `work_items` exists, verify:
   - Every `current_work` key exists in the registry.
   - `current_phase` matches the selected entry's phase.
   - Repair mismatches by preferring the registry entry's phase.

**Exclusions:** Never import as managed work items:
- `*-lcs-master` routing-log directories
- `*-debug-ext` report-only directories
- `.lcs/docs/`, `.lcs/archive/`, `.lcs/codebase/`
- Flat singleton files (e.g. `onboarding.md`)
- Empty directories without recognized main-flow artifact markers

**Recognized markers:** `explore.md`, `debug.md`, `prd.md`, `prd-enhanced.md`, `srs.md`, `tests.md`, `traceability.md`, `task-coverage.md`, `task/` directory, `code-review.md`, `architecture-improvement.md`.

**Non-destructive rules:**
- Never delete an open registry entry because a scan didn't find an artifact.
- If a `new`-phase entry points to a missing directory, keep it (blank `lcs-new` items may be registry-backed).
- If a non-`new` entry points to a missing directory, report stale state.

### List Work Items

Intent: "list work items", "show open work", "apa saja work item yang belum selesai"

Behavior:
1. Reconcile first.
2. Display each entry from `work_items`: ID, title, phase, and a `*` marker for the currently selected item.
3. Do not change selection.

### Switch / Select

Intent: "switch to feature-a", "pindah ke payment gateway", "select 20260917-090000-payment-gateway"

Resolution order:
1. Exact work-item ID match.
2. Exact case-insensitive title match.
3. Unique slug/title substring match.
4. If ambiguous, show candidates and require explicit ID.

On success, update only:
```yaml
current_work: "{target-id}"
current_phase: "{work_items[target-id].phase}"
```
Do not modify other registry entries.

### Resume / Continue

1. Reconcile registry.
2. If `current_work` points to a valid item, resume it.
3. If `current_work` is null and exactly one open item exists, select it and resume.
4. If `current_work` is null and multiple items exist, list them and require selection.
5. Route based on stored phase (e.g. `explore` → `lcs-explore`, `prd` → `lcs-toprd`, `execution` → `lcs-task-executor`).

### New Work Item Routing

- If user explicitly asks only to register/create a blank work item → route to `lcs-new`.
- If user asks to brainstorm immediately → route to `lcs-explore` (which may create/register the work item per the shared state contract).

---

## [ENHANCED] Contextual Guidance Format

Setiap recommendation harus mengikuti format 6-part:

### Format
```
**Recommended:** <skill-name>
**Reason:** <one-line reason>

**Context:** <why this flow is appropriate for the situation>

**Flow:** <full path dari current state ke completion>

**Alternative paths:**
- <alternative 1>: <when to use>
- <alternative 2>: <when to use>

**Critical warnings:**
- <warning 1> (P0 decision, hard to reverse)
- <warning 2> (Phase 1 violation, etc.)
```

### Example 1: User says "I want to build a new feature"
```
**Recommended:** lcs-explore
**Reason:** Start dengan brainstorming untuk clarify requirements

**Context:** You're describing a new feature from scratch. The main flow starts dengan `lcs-explore` untuk evaluate options sebelum committing ke PRD.

**Flow:** lcs-explore → lcs-toprd → lcs-prd-reviewer → lcs-tosrs → lcs-task-slicer → lcs-task-executor → lcs-code-review → lcs-doc-finalizer

**Alternative paths:**
- Skip ke lcs-toprd: If you already have clear requirements
- Add lcs-wayfinder: If this is a huge project (>1 week)
- Add lcs-prototype: If you need visual validation

**Critical warnings:**
- None for this flow
```

### Example 2: User says "There's a bug in production"
```
**Recommended:** lcs-debug (enhanced 6-phase loop)
**Reason:** Investigate bug systematically

**Context:** You're reporting a production bug. This is an on-ramp situation, not a new feature. The enhanced `lcs-debug` uses a 6-phase disciplined loop.

**Flow:** lcs-debug → lcs-toprd (if bug implies missing requirement) → main flow

**Alternative paths:**
- Skip ke lcs-toprd: If bug is well-understood dan only needs fix
- Add lcs-research: If bug requires investigating external systems

**Critical warnings:**
- ⚠️ Phase 1 (Build Feedback Loop) MUST complete sebelum hypothesizing. No guessing allowed until you have a deterministic command that goes RED on this specific bug.
- ⚠️ Post-mortem MUST ask "What architectural change would have prevented this?" Handoff ke codebase maintenance jika needed.
```

### Example 3: User says "I want to refactor the authentication module"
```
**Recommended:** lcs-codebase-doc
**Reason:** Map current state sebelum refactoring

**Context:** You're describing codebase maintenance, not a new feature. Always start dengan mapping untuk understand current architecture.

**Flow:** lcs-codebase-doc → lcs-domain-modeling (vocabulary) → lcs-explore → lcs-toprd → ...

**Alternative paths:**
- Skip ke lcs-explore: If you already have clear understanding of current state
- Add lcs-research: If you need to research best practices untuk authentication refactor

**Critical warnings:**
- ⚠️ Do NOT start coding tanpa mapping. Refactoring tanpa understanding current state leads ke regressions.
- ⚠️ Use expand-contract pattern untuk wide refactors (rename column, retype symbol) untuk keep CI green.
```

---

## Contract (SOT) Enforcement — 3 Responsibilities

Sebelum EVERY handoff ke downstream skill, lcs-master MUST:

### 1. Path Enforcer
Verify target skill uses correct path per `../lcs-shared/contract.md`:
- `lcs-doc-finalizer` → `.lcs/docs/`, NOT `.lcs/work-items/docs/`
- `lcs-self-improvement` → `.lcs/docs/self-improvements/`
- `lcs-onboarding` → `.lcs/work-items/onboarding.md` (singleton, no timestamp)
- `lcs-debug-ext` → `.lcs/work-items/{timestamp}-{slug}-debug-ext/`
- All others → `.lcs/work-items/{timestamp}-{slug}/`

**Behavior:** Jika target skill would violate path contract, block handoff dan report conflict.

### 2. Exact-Name Routing
Route menggunakan folder name yang EXACTLY matches `name:` field di target skill's `SKILL.md` frontmatter (AGENTS.md §6).
- ✅ `lcs-task-executor` (correct)
- ❌ `task-executor` (missing prefix)
- ❌ `LCS-Task-Executor` (wrong case)

**Behavior:** No alternate spellings, no typos. Jika skill name ambiguous, ask user untuk clarify.

### 3. Decision Log (SOT)
Append audit-trail entry ke `.lcs/work-items/{timestamp}-lcs-master/session-log.md` recording:
```yaml
- timestamp: 2026-08-08T11:30:00+07:00
  routed-to: lcs-explore
  reason: "User wants to build new feature, starting dari brainstorming"
  mode: confirmation
  situation-type: main-flow
  alternatives-offered: ["Skip to lcs-toprd", "Add lcs-wayfinder", "Add lcs-prototype"]
  warnings-given: []
```

**Behavior:**
- Create log file (dengan OKF frontmatter `type: artifact, artifact_type: session_log`) pada first routing of session
- Append-only (no modifications to existing entries)
- Log all routing decisions, termasuk precondition check dan vocabulary invocation

---

## Prompt Templates

- **Starter:** "Start LCS workflow"
- **On-ramp (bug):** "There's a bug in production: <description>"
- **On-ramp (huge project):** "I want to build a huge feature: <description>"
- **On-ramp (maintenance):** "I want to refactor <module>"
- **Main flow:** "I want to build a new feature: <description>"
- **Autopilot:** "Start LCS workflow in autopilot mode"
- **Escape hatch:** "I need to research <topic> before continuing"

---

## Chain of Truth Report

| Stage | Detail |
|-------|--------|
| **Source** | User input, `.lcs/state.md`, `CONTEXT.md`, skill inventory |
| **Assumption** | User wants LCS workflow assistance |
| **Plan** | Analyze intent → identify on-ramp → route to appropriate skill |
| **Action** | Route to skill with rich contextual guidance |
| **Verification** | Skill invoked correctly, contract enforced |
| **Report** | Decision logged in session-log.md |

## Handoff

Next recommended skill: {determined-by-routing-logic}
Next file to read: .lcs/state.md
Current phase: routing
Current confidence: high
Blocking questions: None
Risks to carry forward: Enforce shared contract on every handoff (path conventions, exact skill names, decision log)
Source of Truth Bundle: .lcs/state.md, session-log.md
Must Preserve IDs: None
Unresolved IDs: None
Suggested next command: {determined-by-routing-logic}

## Chain of Truth Level

Level: Standard

This skill follows the LCS Chain of Truth protocol at the declared level.
