---
name: adapt-architecture
description: >
  Execute structural metamorphosis using strangler fig migration, chrysalis
  phases, and interface preservation. Covers transformation planning, parallel
  running, progressive cutover, rollback design, and post-metamorphosis
  stabilization for system architecture evolution. Use when assess-form has
  classified the system as READY for transformation, when migrating from
  monolith to microservices, when replacing a core subsystem while dependents
  continue operating, or when any architectural change must be gradual rather
  than big-bang.
license: MIT
allowed-tools: Read
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: morphic
  complexity: intermediate
  language: natural
  tags: morphic, adaptation, architecture, migration, strangler-fig
---

# Adapt Architecture

Execute structural metamorphosis — transforming a system's architecture from its current form to a target form while maintaining operational continuity. Uses strangler fig migration, chrysalis phases, and interface preservation to ensure the system never stops functioning during transformation.

## When to Use

- Form assessment (see `assess-form`) classified the system as READY
- A system must evolve its architecture to meet new requirements without downtime
- Migrating from monolith to microservices (or the reverse)
- Replacing a core subsystem while dependent systems continue operating
- Evolving a data model while maintaining backward compatibility
- Any architectural change that must be gradual rather than big-bang

## Inputs

- **Required**: Current form assessment (from `assess-form` or equivalent analysis)
- **Required**: Target architecture (what the system should become)
- **Required**: Operational continuity requirements (what must not break during transformation)
- **Optional**: Available transformation budget (time, people, compute)
- **Optional**: Rollback requirements (how far back must we be able to retreat?)
- **Optional**: Parallel running duration (how long to run old and new simultaneously)

## Procedure

### Step 1: Design the Transformation Blueprint

Plan the metamorphosis path from current form to target form.

1. Map the transformation as a sequence of intermediate forms:
   - Current form → Intermediate form 1 → ... → Target form
   - Each intermediate form must be operationally viable (can serve traffic, pass tests)
   - No intermediate form should be harder to maintain than the current form
2. Identify the transformation seams:
   - Where can the current form be "cut" to insert the new architecture?
   - Natural seams: existing interfaces, module boundaries, data partitions
   - Artificial seams: interfaces created specifically to enable the cut (anti-corruption layers)
3. Choose the metamorphosis pattern:
   - **Strangler fig**: new system grows around the old, gradually replacing it
   - **Chrysalis**: old system is wrapped in a new shell; internals replaced while shell preserves external interface
   - **Budding**: new system grows alongside the old; traffic gradually shifts (see `scale-colony` for colony budding)
   - **Metamorphic migration**: phased replacement of components in dependency order (leaves first, roots last)
4. Design the interface preservation layer:
   - External consumers must not experience disruption
   - API versioning, backward-compatible contracts, adapter patterns
   - The preservation layer is temporary scaffolding — plan its removal

```
Metamorphosis Patterns:
┌───────────────┬───────────────────────────────────────────────────┐
│ Strangler Fig │ New code intercepts routes one by one;            │
│               │ old code handles everything else until replaced   │
│               │ ┌──────────┐                                     │
│               │ │ Old ████ │ → │ Old ██ New ██ │ → │ New ████ │  │
│               │ └──────────┘                                     │
├───────────────┼───────────────────────────────────────────────────┤
│ Chrysalis     │ Wrap old system in new interface; replace         │
│               │ internals while external shell stays stable       │
│               │ ┌──────────┐     ┌──[new]───┐     ┌──[new]───┐  │
│               │ │ old core │ → │ old core │ → │ new core │  │
│               │ └──────────┘     └──────────┘     └──────────┘  │
├───────────────┼───────────────────────────────────────────────────┤
│ Budding       │ New system runs in parallel; traffic shifts       │
│               │ ┌──────┐ ┌──────┐     ┌──────┐ ┌──────┐         │
│               │ │ Old  │ │ New  │  →  │ Old  │ │ New  │         │
│               │ │ 100% │ │  0%  │     │  0%  │ │ 100% │         │
│               │ └──────┘ └──────┘     └──────┘ └──────┘         │
└───────────────┴───────────────────────────────────────────────────┘
```

**Expected:** A transformation blueprint showing intermediate forms, seams, the chosen metamorphosis pattern, and the interface preservation strategy. Each step is concrete and testable.

**On failure:** If no clean seam can be found, the system may need preliminary dissolution (see `dissolve-form`) to create seams before transformation. If the intermediate forms aren't operationally viable, the transformation steps are too large — decompose into smaller increments.

### Step 2: Build the Scaffolding

Construct the temporary infrastructure that supports metamorphosis.

1. Create the anti-corruption layer:
   - A thin translation layer between the old and new systems
   - Routes requests to the appropriate system (old or new) based on migration state
   - Translates data formats between old and new representations
   - This layer is the "cocoon" that protects the transformation
2. Set up parallel running infrastructure:
   - Both old and new systems must be deployable simultaneously
   - Feature flags control which system handles which traffic
   - Comparison mechanisms validate that old and new produce equivalent results
3. Establish rollback checkpoints:
   - At each intermediate form, verify that rollback to the previous form is possible
   - Rollback must be faster than the forward transformation step
   - Data migration must be reversible (or data must be dual-written during transition)
4. Build the validation harness:
   - Automated tests that verify operational continuity at each intermediate form
   - Performance benchmarks that detect regression
   - Data integrity checks that catch migration errors

**Expected:** Scaffolding infrastructure (anti-corruption layer, parallel running, rollback, validation) is in place before any transformation begins. The scaffolding itself is tested and verified.

**On failure:** If scaffolding is too expensive, simplify: the minimum viable scaffolding is a feature flag and a rollback procedure. Anti-corruption layers and parallel running add safety but are not always necessary for smaller transformations.

### Step 3: Execute Progressive Cutover

Migrate functionality from old form to new form incrementally.

1. Order components for migration:
   - Start with the least-coupled, lowest-risk component (build confidence)
   - Progress toward more critical, more coupled components
   - Save the most coupled/critical component for last (by which point the team has experience)
2. For each component:
   a. Implement the new version behind the anti-corruption layer
   b. Run parallel: both old and new process the same inputs
   c. Compare outputs — they should be equivalent (or the differences should be expected and documented)
   d. When confident, switch traffic to the new version (feature flag flip)
   e. Monitor for anomalies (increase monitoring sensitivity post-cutover)
   f. After a stability period, decommission the old version of this component
3. Maintain continuous delivery throughout:
   - Each cutover step is a normal deployment, not a special event
   - The system is always in a known, tested, operational state
   - If a cutover causes issues, roll back to the previous state (which is still operational)

**Expected:** Functionality migrates component by component with validation at each step. The system is always operational. Each cutover builds confidence for the next.

**On failure:** If parallel running reveals discrepancies, the new implementation has a bug — fix it before cutting over. If a cutover causes performance degradation, the new component may need optimization or the anti-corruption layer is adding too much overhead. If the team loses confidence mid-migration, pause and stabilize — a half-migrated system in a known state is far better than a rushed full migration.

### Step 4: Manage the Chrysalis Phase

Navigate the most vulnerable period — when the system is between forms.

1. Acknowledge the chrysalis reality:
   - During migration, the system is partly old and partly new
   - This hybrid state is inherently more complex than either pure state
   - Complexity peaks at the midpoint of migration, then decreases
2. Chrysalis discipline:
   - No new features during the chrysalis phase (transformation only)
   - Minimal external changes (freeze non-essential deployments)
   - Increased monitoring and on-call coverage
   - Daily check-ins on migration progress and system health
3. Mid-chrysalis assessment:
   - At the halfway point, assess: is the target form still the right goal?
   - Has anything changed (market, requirements, team) that affects the target?
   - Should the transformation continue, pause, or redirect?
4. Protect the chrysalis:
   - Keep the rollback path clear at all times
   - Document the current hybrid state thoroughly (future debuggers will need it)
   - Resist the temptation to "clean up" temporary scaffolding before migration is complete

**Expected:** The chrysalis phase is managed as a deliberate, time-bounded period with increased discipline and monitoring. The team understands that temporary complexity is the cost of safe transformation.

**On failure:** If the chrysalis phase drags on too long, the hybrid state becomes the new normal — which is worse than either old or new. Set a time limit. If the limit is reached, either accelerate the remaining migration or accept the hybrid state as the "new form" and stabilize it.

### Step 5: Complete Metamorphosis and Stabilize

Finish the transformation and remove scaffolding.

1. Final cutover:
   - Migrate the last component(s) to the new form
   - Run full validation suite against the complete new system
   - Performance test under production-equivalent load
2. Remove scaffolding:
   - Decommission the anti-corruption layer (it's no longer needed)
   - Remove feature flags related to the migration
   - Clean up parallel running infrastructure
   - Archive (don't delete) the old system code for reference
3. Post-metamorphosis stabilization:
   - Run in the new form for 2-4 weeks with enhanced monitoring
   - Address any issues that emerge under real-world conditions
   - Update documentation to reflect the new architecture
4. Retrospective:
   - What went well in the transformation?
   - What was harder than expected?
   - What would we do differently next time?
   - Update the team's transformation playbook

**Expected:** The transformation is complete. The system operates in its new form. Scaffolding is removed. Documentation is updated. The team has captured learnings for future transformations.

**On failure:** If the new form is unstable after cutover, maintain the rollback path and continue stabilization. If stabilization takes more than the planned period, there may be a design issue in the new architecture — consider whether targeted fixes or a partial rollback of the most problematic component is appropriate.

## Validation

- [ ] Transformation blueprint shows viable intermediate forms
- [ ] Scaffolding (anti-corruption layer, rollback, validation harness) is in place before migration starts
- [ ] Components migrate in order from lowest to highest risk
- [ ] Parallel running validates equivalence at each step
- [ ] Chrysalis phase is time-bounded with feature freeze discipline
- [ ] All scaffolding is removed after transformation completes
- [ ] Post-metamorphosis stabilization period passes without critical issues
- [ ] Retrospective captures learnings

## Common Pitfalls

- **Big-bang migration**: Attempting to transform everything at once. This abandons the safety of incremental cutover and maximizes blast radius. Always migrate incrementally
- **Permanent scaffolding**: Anti-corruption layers and feature flags that are never removed become technical debt. Plan scaffolding removal as part of the transformation, not as an afterthought
- **Chrysalis denial**: Pretending the hybrid state is normal leads to feature development on unstable foundations. Acknowledge the chrysalis phase and enforce its discipline
- **Target fixation**: Becoming so committed to the target architecture that signs of a better alternative are ignored. The mid-chrysalis assessment exists for this reason
- **Transformation fatigue**: Long migrations exhaust teams. Keep each transformation step small enough to complete in days, not weeks. Celebrate milestones to maintain momentum

## Related Skills

- `assess-form` — prerequisite assessment that determines if the system is ready for transformation
- `dissolve-form` — for systems too rigid to transform directly; dissolution creates the seams needed here
- `repair-damage` — recovery skill for when transformation introduces damage
- `shift-camouflage` — surface adaptation that may suffice without deep architectural change
- `coordinate-swarm` — swarm coordination informs the sequencing of transformation across distributed systems
- `scale-colony` — growth pressure is a common trigger for architectural adaptation
- `implement-gitops-workflow` — GitOps provides the deployment infrastructure for progressive cutover
- `review-software-architecture` — complementary review skill for evaluating the target architecture
