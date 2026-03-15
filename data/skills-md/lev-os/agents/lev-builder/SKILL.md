---
name: lev-builder
description: |
  [WHAT] Builder workflow for developing `~/lev` and migrating proven work to core paths.
  [HOW] Assess existing code, run prior art checks, decide placement against `~/lev/docs`, apply patches, validate E2E.
  [WHEN] Use when formalizing POCs, placing modules, or migrating workshop output into production architecture.
  [WHY] Prevents drift and duplicate effort by enforcing file-based routing and docs-aligned placement.

  Triggers: "build feature", "migrate poc", "where should this go", "prior art check", "placement decision", "formalize"
skill_type: workflow
category: process-builder

lifecycle_integration:
  stage: manifesting
  input_artifact: design doc + POC code
  output_artifact: production code in lev/core
---

# lev-builder: POC → Formalize → Migrate

**Core principle:** Build in a workspace POC, prove it works, migrate to `~/lev` canonical paths.

## Why This Exists

```
PROBLEM:
- Work happens across mixed workspaces (project-local, workshop, plugins)
- BD issues are in lev (lev-* prefix)
- Need to know WHERE to put things in Leviathan
- Need prior art check before creating new

SOLUTION:
- lev-builder orchestrates the full workflow
- POC in `~/lev/workshop/poc` (or project-local skills) → migrate to `~/lev/core` when proven
- Uses graph operations for decisioning, then applies explicit filesystem patches during migration
```

## The Builder Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    LEV-BUILDER WORKFLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣ ASSESS (What exists?)                                       │
│  ├─ lev get "topic" --indexes codebase,docs,skills            │
│  ├─ Check ~/lev/core/* for existing modules                    │
│  ├─ Check ~/lev/workshop/poc/* for prior POCs                  │
│  └─ Output: Related code, docs, skills found                   │
│                                                                 │
│  2️⃣ PRIOR ART CHECK (Duplicate prevention)                      │
│  ├─ ./scripts/prior-art-check.sh "topic"                       │
│  ├─ bd search "topic"                                          │
│  ├─ Skill lookup: ~/lev/workshop/poc/lookup/                   │
│  └─ Output: Existing work to patch vs. new work to create      │
│                                                                 │
│  3️⃣ PLACEMENT DECISION (Where does it go?)                      │
│  ├─ Escalate to user if ambiguous                              │
│  │   "Should this be in core/auth or core/vault?"              │
│  ├─ Consult LEVIATHAN_PATHS.md                                 │
│  └─ Output: Target path confirmed                              │
│                                                                 │
│  4️⃣ GRAPH PLAN + FILE PATCH                                     │
│  ├─ Generate graph mutation plan from design doc              │
│  ├─ Materialize approved changes as filesystem patch          │
│  ├─ Apply to target location                                  │
│  └─ Output: Files created/modified                            │
│                                                                 │
│  5️⃣ E2E VALIDATION (Confirm it works)                           │
│  ├─ Run relevant tests                                         │
│  ├─ Typecheck: bun run typecheck                               │
│  ├─ Integration test if applicable                             │
│  └─ Output: Validation results                                 │
│                                                                 │
│  6️⃣ MIGRATE (POC → Production)                                  │
│  ├─ If POC in workshop/project skills: move to lev/core        │
│  ├─ Update skill registry                                      │
│  ├─ Create migration PR/commit                                 │
│  └─ Output: Migration complete                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Leviathan Paths Reference

```yaml
# Where things go in Leviathan

~/lev/core/
├── harness/          # Agent execution, adapters, Ralph
├── auth/             # Fleet RBAC, permissions (NEW)
├── cdo/              # Graph runtime, state machines
├── commands/         # CLI commands
├── config/            # Configuration system
├── daemons/          # Background services
├── graph/            # Graph primitives
├── lifecycle/        # Entity lifecycle, state transitions
├── memory/           # Memory layer
├── vault/            # Data vault, leases (NEW)
└── ...

~/lev/workshop/
├── intake/           # Ingested external projects
├── poc/              # Proof of concepts
│   └── lookup/       # Skill discovery system
└── ...
```

## Quick Commands

### 1. Assess Topic

```bash
# If `lev get` is not available yet in your CLI build, substitute `lev find`.
# Full assessment
lev get "fleet authorization" --indexes codebase,docs,skills,tasks

# Check core modules
ls ~/lev/core/ | grep -i auth

# Check POCs
ls ~/lev/workshop/poc/ | grep -i auth

# Check skills
ls ~/.agents/skills/ | grep -i auth
```

### 2. Prior Art Check

```bash
# Deterministic check
./scripts/prior-art-check.sh "data vault leases"

# BD search
bd search "vault" --root-path ~/lev
bd search "lease" --root-path ~/lev

# Skill lookup
node ~/lev/workshop/poc/lookup/cli.js search "authorization"
```

### 3. Escalate Decision

```python
# In agent context
escalate({
  type: "PLACEMENT_DECISION",
  question: "Should fleet-rbac.ts go in core/auth or core/permissions?",
  options: [
    { path: "core/auth/fleet-rbac.ts", reason: "Auth is about identity" },
    { path: "core/permissions/fleet-rbac.ts", reason: "RBAC is permissions" }
  ],
  context: "Fleet auth controls who can spawn agents and access data"
})
```

### 4. Graph Plan + File Patch

```bash
# Generate patch plan from design doc
cat pm/designs/fleet-swarm-authorization.md | \
  ./scripts/design-to-patch.sh > patches/fleet-auth.patch

# Apply patch (preview)
./scripts/apply-patch.sh patches/fleet-auth.patch --dry-run

# Apply patch (execute)
./scripts/apply-patch.sh patches/fleet-auth.patch --target ~/lev/core/auth/
```

### 5. Validate E2E

```bash
# Typecheck
cd ~/lev && bun run typecheck

# Run tests for module
bun test core/auth/

# Integration test
bun test:integration --filter "fleet"
```

### 6. Migrate POC

```bash
# Move skill from workshop POC to lev
./scripts/migrate-skill.sh ~/lev/workshop/poc/lev-builder ~/lev/core/builder

# Update registry
./scripts/update-skill-registry.sh

# Commit
cd ~/lev && git add . && git commit -m "feat: migrate lev-builder from POC"
```

## Integration with Other Skills

| Skill | Role in Builder |
|-------|-----------------|
| `lev get` | Assessment - search across indexes |
| `lev-patch` | Prior art - check before creating |
| `planning` | Spec authoring backend - CDO graph to execution |
| `ralph` | Execution - run tasks with validation |
| `lev-cdo` | Graph operations - state machines |

## Common Workflows

### Workflow 1: New Feature

```
USER: "Add fleet authorization to Leviathan"

BUILDER:
1. ASSESS: lev get "fleet\|authorization\|rbac"
   → Found: core/config has some auth, no fleet module
   
2. PRIOR ART: bd search "authorization"
   → Found: lev-qtpq.7 task exists for this
   
3. PLACEMENT: Escalate "core/auth vs core/permissions?"
   → User: "core/auth"
   
4. PATCH: Generate fleet-rbac.ts from design doc
   → Created: ~/lev/core/auth/fleet-rbac.ts
   
5. VALIDATE: bun run typecheck && bun test core/auth/
   → Passed
   
6. MIGRATE: N/A (already in lev/core)
```

### Workflow 2: POC to Production

```
USER: "Migrate lev-builder skill to production"

BUILDER:
1. ASSESS: ls ~/lev/workshop/poc/lev-builder/
   → Found: SKILL.md, scripts/
   
2. PRIOR ART: ls ~/lev/core/builder/
   → Not found (new module)
   
3. PLACEMENT: "core/builder" (builder is core infra)
   → Confirmed
   
4. PATCH: Copy + adapt for lev structure
   → Created: ~/lev/core/builder/
   
5. VALIDATE: bun test core/builder/
   → Passed
   
6. MIGRATE: git commit, update registry
   → Done
```

### Workflow 3: Assess & Consolidate

```
USER: "What exists for caching in Leviathan?"

BUILDER:
1. ASSESS: 
   lev get "cache\|caching" --indexes codebase,docs
   → Found: 
     - core/config/cache.ts (config caching)
     - workshop/poc/redis-cache/ (POC)
     - docs/adr/ADR-045-caching.md (decision)
   
2. REPORT:
   "Caching exists in 3 places:
    - Config cache: production (core/config)
    - Redis POC: not migrated (workshop/poc)
    - ADR-045: recommends unified cache layer
    
    Recommend: Consolidate into core/cache/"

3. ESCALATE: "Proceed with consolidation?"
```

## Escalation Patterns

```typescript
// Decision types that trigger escalation
const ESCALATION_TRIGGERS = [
  "PLACEMENT_DECISION",      // Where to put code
  "CONSOLIDATION_DECISION",  // Merge vs keep separate
  "ARCHITECTURE_DECISION",   // Significant design choice
  "MIGRATION_APPROVAL",      // Moving POC to production
  "DEPENDENCY_ADDITION",     // Adding new dependencies
];

// Escalate via Telegram (approval buttons)
await escalate({
  type: "PLACEMENT_DECISION",
  question: "...",
  options: [...],
  buttons: [
    { text: "Option A", callback_data: "placement:core/auth" },
    { text: "Option B", callback_data: "placement:core/permissions" },
    { text: "Discuss", callback_data: "placement:discuss" },
  ]
});
```

## State Tracking

```jsonl
# .lev/builder/state.jsonl
{"ts":"...","action":"assess","topic":"fleet auth","results":["core/auth","lev-qtpq.7"]}
{"ts":"...","action":"prior_art","topic":"fleet auth","found":true,"matches":1}
{"ts":"...","action":"escalate","type":"PLACEMENT_DECISION","resolved":true,"choice":"core/auth"}
{"ts":"...","action":"patch","target":"core/auth/fleet-rbac.ts","status":"created"}
{"ts":"...","action":"validate","target":"core/auth/","passed":true}
```

## Summary

**lev-builder answers:**
1. **What exists?** → Assess with lev get
2. **Is there prior art?** → Check with lev-patch
3. **Where does it go?** → Escalate placement decisions
4. **How to apply?** → Graph plan + explicit filesystem patch
5. **Does it work?** → E2E validation
6. **Ready for production?** → Migrate POC to lev/core

## Relates

### Master Router
- **Lev Master Router** (`lev/SKILL.md`) - Routes all lev-* skills
  Parent skill that dispatches to this skill based on keywords/context

## Technique Map
- **Role definition** - Clarifies operating scope and prevents ambiguous execution.
- **Context enrichment** - Captures required inputs before actions.
- **Output structuring** - Standardizes deliverables for consistent reuse.
- **Step-by-step workflow** - Reduces errors by making execution order explicit.
- **Edge-case handling** - Documents safe fallbacks when assumptions fail.

## Technique Notes
These techniques improve reliability by making intent, inputs, outputs, and fallback paths explicit. Keep this section concise and additive so existing domain guidance remains primary.

## Prompt Architect Overlay
### Role Definition
You are the prompt-architect-enhanced specialist for lev-builder, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

### Input Contract
- Required: clear user intent and relevant context for this skill.
- Preferred: repository/project constraints, existing artifacts, and success criteria.
- If context is missing, ask focused questions before proceeding.

### Output Contract
- Provide structured, actionable outputs aligned to this skill's existing format.
- Include assumptions and next steps when appropriate.
- Preserve compatibility with existing sections and related skills.

### Edge Cases & Fallbacks
- If prerequisites are missing, provide a minimal safe path and request missing inputs.
- If scope is ambiguous, narrow to the highest-confidence sub-task.
- If a requested action conflicts with existing constraints, explain and offer compliant alternatives.
