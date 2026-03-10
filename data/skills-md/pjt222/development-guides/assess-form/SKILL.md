---
name: assess-form
description: >
  Evaluate a system's current structural form, identify transformation pressure,
  and classify transformation readiness. Covers structural inventory, pressure
  mapping, rigidity assessment, change capacity estimation, and readiness
  classification for architectural metamorphosis. Use before any significant
  architectural change to understand the starting point, when a system feels
  stuck without clear reasons, when external pressure from growth or tech debt
  is mounting, or as periodic health checks for long-lived systems.
license: MIT
allowed-tools: Read
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: morphic
  complexity: basic
  language: natural
  tags: morphic, assessment, architecture, transformation-readiness
---

# Assess Form

Evaluate a system's current structural form — its architecture, rigidity, pressure points, and capacity for change — to determine transformation readiness before initiating metamorphosis.

## When to Use

- Before any significant architectural change to understand the starting point
- When a system feels "stuck" but the reasons are unclear
- When external pressure (growth, market shift, tech debt) is mounting but the response is uncertain
- Assessing whether a proposed transformation is feasible given the current form
- Periodic health checks for long-lived systems (annual form assessment)
- Complementing `adapt-architecture` — assess first, then transform

## Inputs

- **Required**: The system to assess (codebase, organization, infrastructure, process)
- **Optional**: Proposed transformation direction (what might the system need to become?)
- **Optional**: Known pain points or pressure sources
- **Optional**: Previous transformation attempts and their outcomes
- **Optional**: Time horizon for potential transformation
- **Optional**: Available resources for transformation effort

## Procedure

### Step 1: Inventory the Current Form

Catalog the system's structural elements without judgment — understand what exists before evaluating it.

1. Map the structural components:
   - **Modules**: distinct functional units (services, teams, packages, departments)
   - **Interfaces**: how modules connect (APIs, protocols, contracts, reporting lines)
   - **Data flows**: how information moves through the system
   - **Dependencies**: what depends on what (direct, transitive, circular)
   - **Load-bearing structures**: components that everything else relies on
2. Document the form's age and history:
   - When was each major component introduced?
   - Which components have changed recently vs. remained static?
   - What is the "geological layer" structure (old core, newer additions, recent patches)?
3. Identify the form's "skeleton" vs. "flesh":
   - Skeleton: structural decisions that are extremely costly to change (language, database, deployment model)
   - Flesh: functional decisions that can change more easily (business logic, UI, configuration)

```
Structural Inventory Template:
┌──────────────┬──────────┬────────────┬───────────────────┬──────────┐
│ Component    │ Age      │ Last       │ Dependencies      │ Type     │
│              │          │ Modified   │ (in / out)        │          │
├──────────────┼──────────┼────────────┼───────────────────┼──────────┤
│ Auth service │ 3 years  │ 6 months   │ In: 12 / Out: 3  │ Skeleton │
│ Dashboard UI │ 1 year   │ 2 weeks    │ In: 2 / Out: 5   │ Flesh    │
│ Data pipeline│ 4 years  │ 1 year     │ In: 3 / Out: 8   │ Skeleton │
│ Config store │ 2 years  │ 3 months   │ In: 0 / Out: 15  │ Skeleton │
└──────────────┴──────────┴────────────┴───────────────────┴──────────┘
```

**Expected:** A complete structural inventory showing components, their ages, modification recency, dependency profiles, and classification as skeleton or flesh. This is the "X-ray" of the current form.

**On failure:** If the inventory is incomplete (components are unknown or undocumented), that itself is a finding — the form has opacity, which is a transformation risk. Document what you can, flag unknowns, and plan discovery for the gaps.

### Step 2: Map Transformation Pressure

Identify the forces pushing the system toward change and the forces resisting it.

1. Catalog external pressures (forces demanding change):
   - Growth pressure: current form can't handle increasing load
   - Market pressure: competitors or users demand capabilities the current form can't support
   - Technology pressure: underlying technology is becoming obsolete or unsupported
   - Regulatory pressure: compliance requirements the current form doesn't meet
   - Integration pressure: must connect with systems the current form wasn't designed for
2. Catalog internal pressures (forces demanding change from within):
   - Technical debt: accumulated shortcuts that slow development
   - Knowledge concentration: critical knowledge held by too few people
   - Morale pressure: team frustration with the current form
   - Operational burden: maintenance cost consuming resources that should go to development
3. Catalog resistance forces (forces opposing change):
   - Inertia: the existing form works "well enough"
   - Dependency lock-in: too many things depend on the current form
   - Knowledge loss risk: transformation might destroy institutional knowledge
   - Cost: transformation requires investment with uncertain return
   - Fear: previous transformation attempts failed

**Expected:** A pressure map showing the direction and magnitude of forces acting on the system. If transformation pressure significantly exceeds resistance, transformation is overdue. If resistance significantly exceeds pressure, transformation will fail without first reducing resistance.

**On failure:** If pressure mapping produces a balanced picture (neither strong pressure nor strong resistance), the system may not need transformation — or the analysis is surface-level. Dig deeper: interview stakeholders, measure specific pain points, project forward 12-18 months. What pressures will intensify?

### Step 3: Assess Structural Rigidity

Determine how flexible or rigid the current form is — can it bend, or will it break?

1. Test interface flexibility:
   - Can modules be replaced without cascading changes? (loose coupling = flexible)
   - Are interfaces well-defined and stable? (contract clarity = flexible)
   - How many "god modules" exist (modules that everything depends on)? (concentration = rigid)
2. Test data flexibility:
   - Is data migration straightforward? (schema evolution tools, versioning)
   - Are data formats standardized or bespoke? (bespoke = rigid)
   - How entangled is business logic with data structure? (entangled = rigid)
3. Test process flexibility:
   - Can the team ship changes quickly? (deployment pipeline health)
   - Is the test suite comprehensive? (safety net for change)
   - How many "don't touch" components exist? (forbidden zones = rigid)
4. Calculate the rigidity score:

```
Rigidity Assessment:
┌──────────────────────┬─────┬──────────┬──────┬──────────────────────┐
│ Dimension            │ Low │ Moderate │ High │ Your Assessment      │
├──────────────────────┼─────┼──────────┼──────┼──────────────────────┤
│ Interface coupling   │ 1   │ 2        │ 3    │ ___                  │
│ God module count     │ 1   │ 2        │ 3    │ ___                  │
│ Data entanglement    │ 1   │ 2        │ 3    │ ___                  │
│ Deployment friction  │ 1   │ 2        │ 3    │ ___                  │
│ Test coverage gaps   │ 1   │ 2        │ 3    │ ___                  │
│ "Don't touch" zones  │ 1   │ 2        │ 3    │ ___                  │
├──────────────────────┼─────┴──────────┴──────┼──────────────────────┤
│ Total (max 18)       │ 6-9: flexible         │ ___                  │
│                      │ 10-13: moderate        │                      │
│                      │ 14-18: rigid           │                      │
└──────────────────────┴───────────────────────┴──────────────────────┘
```

**Expected:** A rigidity score that quantifies how much structural resistance transformation will encounter. Flexible systems (6-9) can transform incrementally. Rigid systems (14-18) need dissolution before reconstruction (see `dissolve-form`).

**On failure:** If the rigidity assessment is inconclusive (moderate score but unclear where the real problems are), focus on the highest-scoring dimensions. A system can be flexible overall but have one extremely rigid component that blocks transformation. Target that component specifically.

### Step 4: Estimate Change Capacity

Assess the system's (and team's) ability to absorb and execute transformation.

1. Available transformation energy:
   - What percentage of team capacity can be allocated to transformation?
   - Is there organizational support (budget, mandate, patience)?
   - Are the right skills available (architecture, migration, testing)?
2. Change absorption rate:
   - How many changes can the system absorb per time unit without destabilizing?
   - What is the recovery time after a significant change?
   - Is there a staging/canary mechanism for incremental transformation?
3. Transformation experience:
   - Has the team successfully transformed similar systems before?
   - Are there transformation tools and practices in place (feature flags, strangler fig, blue-green)?
   - What is the team's risk tolerance?
4. Calculate change capacity:
   - High capacity: dedicated team, strong tooling, prior experience, organizational support
   - Moderate capacity: part-time allocation, some tooling, limited experience
   - Low capacity: no dedicated resources, no tooling, no experience, resistant organization

**Expected:** A change capacity assessment that indicates whether the system/team can execute the proposed transformation given current resources, skills, and organizational support.

**On failure:** If change capacity is low but transformation pressure is high, the first transformation isn't the system — it's the team's capability. Invest in tooling, training, and organizational buy-in before attempting the architectural transformation.

### Step 5: Classify Transformation Readiness

Combine pressure, rigidity, and capacity assessments into a readiness classification.

1. Plot the system on the readiness matrix:

```
Transformation Readiness Matrix:
┌─────────────────┬────────────────────────┬────────────────────────┐
│                  │ Low Rigidity           │ High Rigidity          │
├─────────────────┼────────────────────────┼────────────────────────┤
│ High Pressure   │ READY — Transform now  │ PREPARE — Reduce       │
│ + High Capacity │ using adapt-architecture│ rigidity first, then   │
│                 │                        │ use dissolve-form       │
├─────────────────┼────────────────────────┼────────────────────────┤
│ High Pressure   │ INVEST — Build capacity│ CRITICAL — Invest in   │
│ + Low Capacity  │ first, then transform  │ capacity AND reduce    │
│                 │                        │ rigidity before change │
├─────────────────┼────────────────────────┼────────────────────────┤
│ Low Pressure    │ OPTIONAL — Transform   │ DEFER — No urgency,    │
│ + Any Capacity  │ if strategic value is  │ monitor pressure and   │
│                 │ clear, otherwise defer │ reassess quarterly     │
└─────────────────┴────────────────────────┴────────────────────────┘
```

2. Document the readiness classification with:
   - Classification label (READY / PREPARE / INVEST / CRITICAL / OPTIONAL / DEFER)
   - Key findings from each assessment dimension
   - Recommended next step
   - Risk factors that could change the classification
3. If READY: proceed to `adapt-architecture`
4. If PREPARE: proceed to `dissolve-form` to reduce rigidity
5. If INVEST: build capacity (training, tooling, organizational support), then reassess
6. If CRITICAL: address capacity and rigidity simultaneously (may require external help)
7. If OPTIONAL/DEFER: document the assessment and set a reassessment date

**Expected:** A clear, justified transformation readiness classification with specific next steps. The classification enables informed decision-making about when and how to transform.

**On failure:** If the classification is ambiguous (e.g., moderate pressure, moderate rigidity, moderate capacity), default to PREPARE — reduce rigidity incrementally while monitoring pressure. This builds capability and reduces risk whether or not full transformation is eventually needed.

## Validation

- [ ] Structural inventory is complete with components, ages, dependencies, and types
- [ ] Transformation pressure is mapped (external, internal, resistance forces)
- [ ] Rigidity score is calculated across all dimensions
- [ ] Change capacity is assessed (resources, absorption rate, experience)
- [ ] Readiness classification is determined with justified reasoning
- [ ] Next steps are documented based on the classification
- [ ] Reassessment date is set (even if currently READY)

## Common Pitfalls

- **Assessing only the technical system**: Transformation readiness includes organizational readiness. A technically flexible system with an organizationally rigid team will still fail to transform
- **Optimistic capacity estimation**: Teams consistently overestimate their capacity for change while maintaining normal operations. Use 50% of stated capacity as the realistic estimate
- **Ignoring resistance forces**: Pressure mapping that only catalogs change forces misses the resistance that will slow or stop transformation. Resistance is often stronger than it appears
- **Assessment paralysis**: The form assessment should take hours to days, not weeks. If it's taking too long, the system is too complex to assess fully — assess at a higher abstraction level and drill into problem areas
- **Confusing rigidity with stability**: A rigid system is not the same as a stable system. Stability comes from well-designed flexibility; rigidity is the absence of designed flexibility

## Related Skills

- `adapt-architecture` — the primary transformation skill; assess-form determines readiness for it
- `dissolve-form` — for systems classified as PREPARE or CRITICAL, rigidity reduction before transformation
- `repair-damage` — for systems that need repair before assessment can be meaningful
- `shift-camouflage` — surface-level adaptation that may resolve pressure without full transformation
- `forage-resources` — resource exploration informs form assessment when the question is "what should we become?"
- `review-software-architecture` — complementary skill for detailed technical architecture evaluation
- `assess-context` — AI self-application variant; maps structural assessment to reasoning context malleability, rigidity mapping, and transformation readiness
