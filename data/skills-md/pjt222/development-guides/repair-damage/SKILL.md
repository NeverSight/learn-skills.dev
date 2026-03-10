---
name: repair-damage
description: >
  Implement regenerative recovery using triage, scaffolding, and progressive
  rebuild. Covers damage assessment, wound classification, emergency
  stabilization, scar tissue management, and resilience strengthening for
  systems that have sustained structural damage. Use when a system has suffered
  an incident needing structured recovery, when a failed transformation left the
  system in a damaged intermediate state, when accumulated technical debt has
  caused partial failure, or when a system is functional but degraded and the
  degradation is worsening.
license: MIT
allowed-tools: Read
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: morphic
  complexity: intermediate
  language: natural
  tags: morphic, repair, regeneration, resilience, wound-healing
---

# Repair Damage

Implement regenerative recovery for systems that have sustained structural damage — whether from incidents, failed migrations, accumulated neglect, or external disruption. Uses biological wound-healing as a framework: triage, stabilization, scaffolding, progressive rebuild, and scar tissue management.

## When to Use

- A system has suffered an incident and needs structured recovery beyond "just fix it"
- A failed transformation (see `adapt-architecture`) left the system in a damaged intermediate state
- Accumulated technical debt has caused partial system failure
- Organizational damage (team departures, knowledge loss, morale collapse) needs structured repair
- Post-defense recovery (see `defend-colony`) when the colony sustained damage
- A system is functional but degraded, and the degradation is worsening

## Inputs

- **Required**: Description of the damage (what broke, when, how severely)
- **Required**: Current system state (what's still working, what's not)
- **Optional**: Root cause (if known — may not be clear yet)
- **Optional**: Pre-damage system state (for comparison)
- **Optional**: Available repair resources (time, people, budget)
- **Optional**: Urgency (is the system actively degrading or stable-but-damaged?)

## Procedure

### Step 1: Triage — Assess and Classify Wounds

Rapidly assess all damage and classify by severity and urgency.

1. Catalog every known point of damage:
   - What specific component, function, or capability is affected?
   - Is the damage complete (non-functional) or partial (degraded)?
   - Is the damage spreading (affecting adjacent components) or contained?
2. Classify each wound:

```
Wound Classification:
┌──────────┬──────────────────────┬────────────────────────────────────┐
│ Class    │ Severity             │ Response                           │
├──────────┼──────────────────────┼────────────────────────────────────┤
│ Critical │ Core function lost,  │ Immediate: stop bleeding, activate │
│          │ data at risk,        │ backup, redirect traffic, page     │
│          │ actively spreading   │ on-call team                       │
├──────────┼──────────────────────┼────────────────────────────────────┤
│ Serious  │ Important function   │ Urgent: fix within hours/days,     │
│          │ degraded, no spread  │ workarounds acceptable short-term  │
├──────────┼──────────────────────┼────────────────────────────────────┤
│ Moderate │ Non-critical function│ Scheduled: fix within sprint,      │
│          │ affected, contained  │ prioritize against other work      │
├──────────┼──────────────────────┼────────────────────────────────────┤
│ Minor    │ Cosmetic or edge     │ Backlog: fix when convenient,      │
│          │ case, no user impact │ may self-resolve                   │
└──────────┴──────────────────────┴────────────────────────────────────┘
```

3. Prioritize repair order:
   - Critical wounds first (stop the bleeding)
   - Then serious wounds (restore important function)
   - Moderate and minor wounds can wait for scheduled repair
4. Check for wound interaction:
   - Do any wounds amplify each other? (A is worse because B is also broken)
   - Would fixing one wound automatically fix others? (shared root cause)
   - Would fixing one wound make another worse? (competing repair strategies)

**Expected:** A complete wound inventory classified by severity, with a prioritized repair order that accounts for wound interactions.

**On failure:** If triage takes too long (the system is actively degrading), skip detailed classification and focus on: "What is the single most critical thing to stabilize?" Fix that first, then return to full triage.

### Step 2: Emergency Stabilization

Stop the damage from spreading before beginning repair.

1. Contain the wound:
   - Isolate damaged components (circuit breakers, network segmentation, traffic rerouting)
   - Prevent cascade: disable non-essential features that depend on damaged components
   - Preserve evidence: take snapshots, save logs, capture the current state before any changes
2. Apply emergency patches:
   - These are not permanent fixes — they're tourniquets
   - Acceptable emergency measures:
     - Redirect traffic to a healthy replica
     - Disable the damaged feature entirely
     - Apply a known-working configuration from backup
     - Scale up healthy components to absorb redirected load
   - Unacceptable emergency measures:
     - Modifying code without testing (creates new wounds)
     - Deleting data to "reset" the problem (destroys recovery options)
     - Hiding the damage (disabling alerts, suppressing errors)
3. Verify stabilization:
   - Is the damage still spreading? If yes, containment failed — try a broader isolation
   - Is the system functional (possibly degraded)? If yes, proceed to repair
   - Are emergency patches holding? If yes, you have time for deliberate repair

**Expected:** The system is stable (not actively degrading) even if degraded. Damage is contained and not spreading. Evidence is preserved for root cause analysis.

**On failure:** If stabilization fails (damage continues spreading despite containment), escalate to full system fallback: activate disaster recovery, switch to backup system, or gracefully degrade to minimal viable operation. Stabilization that takes too long becomes the disaster.

### Step 3: Build Repair Scaffolding

Construct the temporary structures that support the repair process.

1. Set up a repair environment:
   - Branch or copy the damaged system for repair work
   - Ensure repair changes can be tested before applying to production
   - Create a rollback plan for each repair step
2. Build diagnostic infrastructure:
   - Enhanced monitoring on damaged areas (detect regression immediately)
   - Logging that captures the repair process (what was changed, when, why)
   - Comparison tools: before-damage state vs. current vs. after-repair
3. Design the repair sequence:
   - For each wound (in priority order from triage):
     a. Root cause identification (why did this break?)
     b. Repair approach (fix the cause, not just the symptom)
     c. Verification method (how to confirm the repair worked)
     d. Regression check (did the repair break anything else?)
4. Identify scar tissue risk:
   - Repairs done under pressure often introduce scar tissue (workarounds, special cases, technical debt)
   - Plan for scar tissue management (Step 5) from the start

**Expected:** A repair environment with diagnostic capability, a sequenced repair plan, and awareness of scar tissue risk.

**On failure:** If setting up a proper repair environment is too slow (system urgency demands immediate production changes), apply changes directly but with extreme discipline: one change at a time, tested by the available means, rolled back if it doesn't help.

### Step 4: Execute Progressive Rebuild

Repair damage systematically, verifying each fix before proceeding.

1. For each wound (in triage priority order):
   a. Identify root cause:
      - Is this a code bug? Configuration error? Data corruption? Dependency failure?
      - Is this a symptom of a deeper structural problem?
      - Would fixing the root cause also address other wounds?
   b. Implement the repair:
      - Fix the root cause, not just the symptom
      - If the root cause can't be fixed immediately, implement a deliberate workaround and document it
      - Keep repairs minimal — fix what's broken, don't refactor the neighborhood
   c. Verify the repair:
      - Does the specific damaged function work correctly now?
      - Does the repair pass automated tests?
      - Is the system's overall health improved or at least unchanged?
   d. Check for regression:
      - Did this repair break anything else?
      - Are emergency patches from Step 2 still needed, or can some be removed?
2. After all critical and serious wounds are repaired:
   - Remove emergency patches that are no longer needed
   - Restore disabled features
   - Return traffic to normal routing
3. Schedule moderate and minor wound repairs:
   - These enter the normal development workflow
   - Track them to completion (don't let them become "accepted" damage)

**Expected:** Critical and serious wounds are repaired with verified fixes. Emergency patches are removed. The system is restored to functional operation.

**On failure:** If a repair attempt fails or causes regression, roll back to the previous state and reassess. If multiple repair attempts fail for the same wound, the damage may be too deep for local repair — consider whether the affected component needs full replacement rather than repair (see `dissolve-form`).

### Step 5: Manage Scar Tissue and Strengthen

Address the workarounds and shortcuts introduced during emergency repair, and strengthen against recurrence.

1. Inventory scar tissue:
   - Emergency patches that became permanent
   - Workarounds that were never replaced with proper fixes
   - Special cases added to handle damage-related edge cases
   - Disabled features that were never re-enabled
2. For each piece of scar tissue, decide:
   - **Remove**: the workaround is no longer needed (damage is fully repaired)
   - **Replace**: the workaround addresses a real need but should be implemented properly
   - **Accept**: the workaround is the most practical long-term solution (rare, document why)
3. Strengthen against recurrence:
   - Root cause analysis: why did this damage occur?
   - Prevention: what would have prevented it? (monitoring, testing, architecture change)
   - Detection: how could we detect this faster next time? (alerts, health checks)
   - Recovery: how could we recover faster? (runbooks, backup procedures, automation)
4. Update immune memory:
   - Add the incident pattern to monitoring and alerting (see `defend-colony` immune memory)
   - Update runbooks with the repair procedure that worked
   - Share learnings across the team/organization

**Expected:** Scar tissue is managed (removed, replaced, or accepted with documentation). The system is not only repaired but more resilient than before the damage. Learnings are captured for future incidents.

**On failure:** If scar tissue management is deprioritized ("it works, don't touch it"), schedule it explicitly. Unmanaged scar tissue accumulates and eventually contributes to the next incident. If the root cause can't be identified, strengthen detection and recovery speed as compensating controls.

## Validation

- [ ] All damage is inventoried and classified by severity
- [ ] Emergency stabilization stopped the spread of damage
- [ ] Evidence is preserved for root cause analysis
- [ ] Critical and serious wounds are repaired with verified fixes
- [ ] Emergency patches are removed after proper repair
- [ ] Scar tissue is inventoried and managed (removed, replaced, or documented)
- [ ] Root cause analysis identifies prevention and detection improvements
- [ ] System resilience is improved compared to pre-damage state

## Common Pitfalls

- **Repairing without stabilizing**: Attempting to fix the root cause while the system is actively bleeding. Stabilize first, then repair. Tourniquets before surgery
- **Permanent emergency patches**: Emergency measures that become the permanent solution create compounding technical debt. Always follow up with proper repair
- **Root cause assumption**: Assuming the root cause is known without investigation. Many "obvious" causes are symptoms of deeper issues. Investigate before committing to a repair strategy
- **Repair-induced damage**: Rushing repairs without testing creates new wounds. One verified fix per iteration — never batch untested changes
- **Ignoring scar tissue**: "It works now" is not the same as "it's healthy." Scar tissue from hasty repairs is the seed of the next incident

## Related Skills

- `assess-form` — damage assessment shares methodology with form assessment
- `adapt-architecture` — architectural adaptation may be needed if damage reveals structural weakness
- `dissolve-form` — for components too damaged to repair; dissolve and rebuild
- `defend-colony` — defense triggers repair; post-incident recovery feeds back into defense
- `shift-camouflage` — surface adaptation can mask damage while repair proceeds (with caution)
- `conduct-post-mortem` — structured post-incident analysis complements root cause identification
- `write-incident-runbook` — repair procedures should be captured as runbooks for future incidents
