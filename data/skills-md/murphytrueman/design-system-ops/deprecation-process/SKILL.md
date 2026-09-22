---
name: deprecation-process
description: "Plan and execute the full deprecation lifecycle for a design system component, token, or pattern — including timeline, migration paths, communication plan, and multi-phase removal. Trigger when someone says: deprecate a component, remove a component, sunset this pattern, phase out these tokens, retire this variant, replace this with, or anything involving removing or replacing something from the design system. Do NOT trigger for communicating non-deprecation changes like new releases or feature updates — use change-communication for those."
references:
  - ../../knowledge-notes/component-governance.md
---

# Deprecation process

A skill for planning and executing the deprecation of components, tokens, or patterns in a design system. Produces a deprecation plan with timeline, consumer communication, and migration guidance.

## Context

Deprecation is the maintenance work that never gets prioritised until it becomes a crisis. Components accumulate. Tokens multiply. Patterns fork. The longer a team waits to deprecate, the more existing usage entrenches, and the more a removal feels disruptive rather than healthy.

A deprecation done well is a contract with consumers: clear notice, a migration path, and a credible timeline. A deprecation done badly is a surprise, and it erodes trust in the system faster than almost anything else.

This skill produces a deprecation plan that is honest about the timeline, specific about migration, and structured to communicate clearly to the teams affected.

---

## Step 1: Identify what is being deprecated

Clarify:
- What is being deprecated? (component, token, pattern, variant, API)
- Why is it being deprecated? (superseded by a better option, unused, causing maintenance burden, design direction change, accessibility non-compliance, etc.)
- What replaces it, if anything?
- Is there a hard removal date in mind, or is this open-ended?

If nothing replaces it: the deprecation plan needs an extra step addressing why the use case should no longer be served and what teams who relied on it should do instead.

## Step 2: Audit current usage

Before writing the plan, understand the exposure. Do not estimate when you can measure.

**Automated usage counting (if codebase access is available):**

Run these searches to produce a concrete usage count, not an estimate:

For component deprecation:
```bash
# Count import statements
grep -r "import.*{.*ComponentName" --include="*.tsx" --include="*.ts" --include="*.jsx" --include="*.js" src/ | wc -l

# Count JSX usage (may exceed imports if used multiple times per file)
grep -r "<ComponentName" --include="*.tsx" --include="*.jsx" src/ | wc -l

# List files with usage (for blast radius mapping)
grep -rl "import.*ComponentName\|<ComponentName" --include="*.tsx" --include="*.ts" --include="*.jsx" --include="*.js" src/
```

For token deprecation:
```bash
# CSS custom properties
grep -r "var(--token-name)" --include="*.css" --include="*.scss" --include="*.tsx" src/ | wc -l

# SCSS variables
grep -r "\$token-name" --include="*.scss" src/ | wc -l

# JS/TS token references
grep -r "tokens\.path\.to\.token\|theme\.path\.to\.token" --include="*.ts" --include="*.tsx" src/ | wc -l
```

**Present the usage count as a structured summary:**

```
Usage audit: DatePicker
─────────────────────────
Import statements:    23 files
JSX instances:        47 usages
Unique consuming apps: 4 (checkout, dashboard, settings, admin)
Critical paths:       2 (checkout date selection, appointment booking)
Test files with refs: 12
Storybook stories:    3
Documentation refs:   5
─────────────────────────
Total blast radius:   47 instances across 23 files in 4 applications
```

If codebase access is not available, ask the user to run the grep commands and provide the output. If neither is possible, flag the usage audit as outstanding and required before soft removal.

**Per-consumer breakdown:** For each consuming application, produce a row showing:

| Consumer | Instances | Critical path? | Estimated migration effort | Contact |
|---|---|---|---|---|
| Checkout | 12 | Yes (date selection) | Medium (1–3 days) | [team/person] |
| Dashboard | 18 | No | Low (<1 day) | [team/person] |
| Settings | 8 | No | Low (<1 day) | [team/person] |
| Admin | 9 | No | Medium (prop differences) | [team/person] |

This table is the deprecation plan's most operationally useful artifact. It tells the deprecation owner exactly who to contact, how much work each team faces, and where the blockers will be.

**Small-system note (fewer than 5 components):** Deprecating one component when you only have four is removing 25% of the system. The usage audit (this step) becomes mandatory, not optional — the blast radius is proportionally much larger. Consider whether the component should be archived or hidden rather than fully deprecated, since small systems have fewer alternatives and consumers may have no migration path. The communication step should be a direct conversation with every affected team, not a written announcement — with a system this size, you know who is using what.

## Step 3: Write the deprecation plan

---

### Deprecation plan: [component/token/pattern name]

**Item being deprecated:** [name]
**Deprecated in version:** [version number or date]
**Planned removal:** [version or date, or "TBD — see timeline"]
**Replacement:** [name of replacement, or "none — see migration guidance"]
**Owner:** [who is responsible for this deprecation]

---

#### Why this is being deprecated

One to three sentences. Be direct. "This component has a lower-quality replacement that covers all existing use cases and is more accessible" is more useful than "this component has reached the end of its lifecycle."

Include the decision record reference if one exists.

#### What replaces it

If there is a direct replacement: name it, link to it, and describe in one sentence what makes it the right choice for teams currently using the deprecated item.

If there is no direct replacement: explain what teams should do instead. This might be composing from more primitive components, using a pattern that does not require a specific component, or accepting that a particular UI pattern is being retired.

Do not leave this section vague. "Use the updated component instead" without specifics is not a migration path.

#### Migration path decision tree

Not every deprecation has a clean 1:1 replacement. When the replacement does not cover 100% of the deprecated item's use cases, use this decision tree:

1. **Does the replacement cover 80%+ of use cases?**
   - Yes → Proceed with standard deprecation. Document the uncovered use cases in the "Exceptions and edge cases" section with recommended workarounds.
   - No → Go to step 2.

2. **Are the uncovered use cases still valid needs?**
   - Yes → The deprecation is premature. Either extend the replacement to cover the gap, or maintain both items until the replacement is complete.
   - No → Proceed with deprecation. Document why the uncovered use cases are no longer supported and what teams should do instead.

3. **Can the uncovered use cases be served by a composition of existing components?**
   - Yes → Document the composition pattern as part of the migration guide. Consider whether the composition should become a documented pattern (use the `pattern-documentation` skill).
   - No → The gap needs a new solution. Pause the deprecation timeline until the solution is available, or extend the deprecation window to give teams time to build local solutions.

The key principle: never deprecate without a path. A deprecation that leaves teams with no alternative is not a deprecation — it is an abandonment.

#### Migration guidance

Provide step-by-step migration instructions at a level of specificity that a developer can follow without additional context.

For a component migration:
1. Find all instances of [deprecated component] in your codebase
2. Replace with [replacement component]
3. Map the deprecated props to replacement props: [prop mapping table]
4. Check for [specific behavioural differences that need testing]
5. Remove any local overrides that compensated for [deprecated component's known weaknesses]

For a token migration:
1. Find all references to [deprecated token name]
2. Replace with [replacement token name]
3. Verify the computed value matches expectations — [deprecated token] resolved to [value], [replacement token] resolves to [value]. [Note any differences and why they exist.]

If the migration is complex, note where to find additional help: a migration script, a specific Slack channel, a pairing offer from the design systems team.

#### Timeline

**Deprecation notice date:** [date]
**Migration support window:** [start – end] — during this period, the design systems team will actively support migration
**Soft removal date:** [date] — deprecated item will generate warnings but remain functional
**Hard removal date:** [date] — deprecated item is removed from the system

The minimum deprecation window should be proportional to the usage footprint. A rarely-used internal component might have a four-week window. A foundational component used across dozens of products needs at least one full release cycle, possibly two.

**Timeline visual:**

Include a visual timeline in the deprecation plan output. Use this Mermaid gantt chart format that renders in GitHub, GitLab, Notion, and most documentation platforms:

```mermaid
gantt
    title Deprecation timeline: [Component name]
    dateFormat YYYY-MM-DD
    axisFormat %b %d

    section Notice
    Deprecation announced           :milestone, m1, [date], 0d
    Teams notified                  :active, notify, [date], 3d

    section Migration
    Migration support window        :active, migrate, after notify, [duration]
    Reminder: 2 weeks to soft removal :milestone, m2, [date], 0d

    section Soft removal
    Warnings enabled, still functional :crit, soft, [date], [duration]
    Reminder: 2 weeks to hard removal  :milestone, m3, [date], 0d

    section Hard removal
    Component removed               :milestone, m4, [date], 0d
```

Replace the bracketed values with the actual dates and durations from the timeline above. If the team's documentation platform does not render Mermaid, provide the same information as an ASCII timeline:

```
[Notice date] ──── Migration support ──── [Soft removal] ──── [Hard removal]
    │                    │                      │                    │
    ▼                    ▼                      ▼                    ▼
 Announced        Teams migrate         Warnings enabled      Fully removed
 [date]           [date range]          [date]                [date]
```

The visual timeline should be included in both the deprecation plan document and the communication announcement. It is the single most referenced artifact in a deprecation — teams pin it, share it, and check it weekly.

#### Communication plan

Who needs to know, and how will they be told?

- **Immediate notice:** [channels — e.g. Slack #design-system, release notes, direct outreach to high-usage teams]
- **In-system warning:** Add deprecation notice to the component's documentation and, if possible, a code-level deprecation warning in the component itself
- **Follow-up reminders:** Two weeks before soft removal, two weeks before hard removal

Write the communication announcement as a draft ready to send. See the `change-communication` skill if a full change communication package is needed.

#### Exceptions and edge cases

Are there any known uses that cannot follow the standard migration path? Document them here and note how they will be handled — extended timeline, custom migration support, or accepted divergence.

---

#### Blast radius analysis (staff-level)

Before committing to a deprecation timeline, model the blast radius:

**Direct impact:**
- How many consuming applications import or reference the deprecated item?
- How many instances of usage exist across all consumers? (A single application might use the deprecated component 50 times.)
- Are any critical paths (checkout, authentication, core navigation) affected?

**Indirect impact:**
- Does any other system component compose the deprecated component? Those components need migration too, and they block consumer migration.
- Do any token aliases or theme configurations reference the deprecated item?
- Are there third-party integrations, design tool configurations, or CI pipelines that reference it?

**Migration effort estimation:**
For each consuming application, estimate migration effort:
- **Low (< 1 day):** Simple find-and-replace. Props map 1:1. No behavioural differences.
- **Medium (1–3 days):** Some prop changes. Minor behavioural differences requiring targeted testing.
- **High (3+ days):** Significant API differences. Composition changes. Requires refactoring consuming code.

**Codemod recommendation:**
If the migration is a mechanical transformation (rename a prop, swap one component for another with predictable prop mapping), recommend producing a codemod. For JavaScript/TypeScript projects, jscodeshift or ts-morph scripts can automate the migration. A codemod that handles 80% of cases and flags the remaining 20% for manual review is worth producing when the blast radius exceeds 50 instances.

Include the blast radius analysis in the deprecation plan. The timeline should be proportional to the blast radius — not just the usage footprint, but the migration effort.

#### Rollback contingency

Document what happens if the deprecation fails:
- Under what conditions would the deprecation be reversed? (e.g., migration proves impossible for a critical consumer within the timeline)
- Can the deprecated item be un-deprecated without data loss or version confusion?
- Is there a version pinning strategy that allows consumers to stay on the old version beyond the hard removal date if needed?

This is not an invitation to avoid deprecations. It is an acknowledgement that infrastructure changes sometimes fail and having a rollback plan is responsible engineering.

## Step 4: Add the deprecation notice to documentation

The deprecated item's documentation page should be updated immediately with:
- A deprecation banner at the top of the page
- A note stating what replaces it and linking to the replacement
- The planned removal date
- A link to this deprecation plan

Do not remove the documentation page until hard removal. Teams often discover deprecations through documentation during unrelated work, and the page needs to be there when they look.

## Quality checks

- A migration path exists for every current use case, or the absence of one is explicitly acknowledged
- The timeline is realistic given the usage footprint
- The communication plan names specific channels, not just "notify affected teams"
- The deprecation notice on the documentation page is ready to publish alongside this plan
- Usage audit has been completed or flagged as outstanding
- Exceptions and edge cases are explicitly documented, not glossed over
