---
name: system-benchmark
description: "Benchmark a design system against industry standards and comparable public systems, producing a qualitative comparison across dimensions with specific, named reference points. Goes beyond an internal health assessment to answer 'how does our system compare to what good looks like out there?' Trigger when someone says: benchmark our system, how do we compare, industry comparison, rate our system against others, where do we stand, compare us to Material Design, how mature is our system, are we behind or ahead, competitive assessment of our design system, or anything about comparing a design system's maturity or quality against external benchmarks. Do NOT trigger for an internal health check without external comparison — use system-health for that. Do NOT trigger for auditing a specific dimension — use the specific audit skill for that."
references:
  - ../../knowledge-notes/token-architecture.md
  - ../../knowledge-notes/component-governance.md
  - ../../knowledge-notes/ai-readiness.md
  - ../../knowledge-notes/component-bestiary-reference.md
  - ../../knowledge-notes/output-discipline.md
---

# System Benchmark

A skill for benchmarking a design system against industry standards and comparable public systems, producing a qualitative comparison with specific reference points that answer: "How does our system compare to what good looks like?"

**Output type:** Proposal only. This skill produces analysis and comparisons. It does not make changes. It produces a benchmark report with findings, comparison context, and prioritised improvement areas.

---

## Why this exists

System-health tells you if your system is healthy on its own terms. But it cannot answer: "Is our token architecture actually good? What do systems we admire look like at this layer?"

System Benchmark fills this gap. It compares your system against documented public benchmarks — published design system case studies, open-source system architectures, and industry maturity models — to give your findings context. A team that learns their token architecture is two tiers behind what mature enterprise systems typically have now has a specific target and gap to close.

This is not competitive intelligence. Design systems are not products competing in a market. This is calibration — understanding where your system sits on a maturity curve so you can prioritise investment.

---

## Configuration

Check for `.ds-ops-config.yml` in the project root:

```yaml
benchmark:
  system_type: "enterprise"          # enterprise, product, agency, government
  team_size: 5                        # Full-time design system team members
  system_age_months: 24               # How long the system has been in active development
  consumer_count: 12                  # Number of teams/products consuming the system
  comparison_targets:                 # Specific systems to compare against (optional)
    - "Material Design"
    - "Polaris"
    - "Carbon"
```

If no configuration exists, ask for:
1. System type (enterprise, product, agency, government)
2. Approximate team size
3. How long the system has been active
4. How many teams or products consume it

---

## The benchmark framework

### Twelve benchmark dimensions

The benchmark assesses twelve dimensions grouped into four pillars. For each dimension, assess the current state and compare it against what mature, publicly documented systems look like at that layer.

#### Pillar 1: Foundation quality

**1. Token architecture maturity**
What to look for: Is there a formal token system? How many tiers (flat list, two-tier, three-tier)? Is aliasing consistent? Is the format standards-compliant (DTCG)? Is validation automated? Does it support multi-brand or multi-theme?

What mature systems look like: Full three-tier architecture with consistent aliasing, DTCG-compliant format, automated validation, and multi-brand support.

**2. Component API consistency**
What to look for: Are prop naming conventions consistent across components? Are conventions documented? Are they enforced by linting? Are there typed API contracts?

What mature systems look like: Typed, linted, documented API contracts with automated consumer contract testing.

**3. Accessibility baseline**
What to look for: Are ARIA attributes present and consistent? Is there automated a11y testing in CI? Has manual testing with assistive technology been done? Are keyboard patterns documented? Is reduced motion and high contrast supported?

What mature systems look like: Full WCAG 2.1 AA compliance verified by audit. Screen reader testing in CI. Reduced motion and high contrast support built in.

#### Pillar 2: Documentation and discoverability

**4. Component documentation completeness**
What to look for: Is there documentation beyond source code? Is there a documentation site? Does it include usage guidelines, do/don't examples, and API reference? Is there an interactive playground?

What mature systems look like: Documentation site with interactive playground, usage analytics, and searchable component inventory with metadata.

**5. Token documentation**
What to look for: Are tokens documented beyond code? Are there visual previews? Is semantic intent described? Are there migration guides for token changes?

What mature systems look like: Token documentation with visual previews, intent descriptions, do/don't examples, and automated sync between code and docs.

**6. AI readiness**
What to look for: Do components have structured metadata? Are descriptions consistent and machine-optimised? Is there a machine-readable manifest? Are composition rules explicit?

What mature systems look like: AI-optimised descriptions, machine-readable composition rules, validation schemas, and components that are self-describing.

#### Pillar 3: Governance and process

**7. Release process maturity**
What to look for: Is there a formal release process? Is semantic versioning applied? Are changelogs consistent? Is there an automated pipeline with quality gates? Are consumers notified?

What mature systems look like: Full release pipeline with canary releases, consumer impact assessment, and automated migration codemods.

**8. Contribution model**
What to look for: Is there a contribution process? Are there guidelines? Is there a review process with SLAs? Is the model federated with clear ownership?

What mature systems look like: Federated contribution model with automated validation, community engagement metrics, and regular office hours.

**9. Deprecation discipline**
What to look for: Is there a deprecation process? Are there timelines and recommended replacements? Are there migration guides and codemods? Is consumer adoption tracked?

What mature systems look like: Automated deprecation pipeline — notice, codemod, migration assistance, sunset — with consumer adoption dashboard.

#### Pillar 4: Adoption and impact

**10. Adoption breadth**
What to look for: What percentage of eligible products use the system? Are custom builds exceptions or the norm? Do custom builds require approval?

What mature systems look like: Over 90% adoption. Off-system builds are rare and tracked. The system is the default.

**11. Adoption depth**
What to look for: Do teams use just basic components or the full stack (tokens, components, patterns, layout, content guidelines)? Do team extensions feed back into the system?

What mature systems look like: Full system consumption across all layers. Team extensions follow contribution guidelines and feed back into the system.

**12. Developer experience**
What to look for: How long does it take to get started? Are there starter templates? Is there good TypeScript support? Are error messages helpful?

What mature systems look like: CLI scaffold, framework templates, IDE plugins, hot-reload dev environment. Under 5 minutes to first component.

---

## Step 0: Gather system data

### From available sources

1. **Run or reference system-health output** — Use existing health findings as the foundation
2. **Read token files** — Assess token architecture maturity directly
3. **Read component source** — Check API consistency, a11y patterns, TypeScript usage
4. **Check documentation** — Does a doc site exist? What is in it?
5. **Check CI/CD** — What automated checks exist?
6. **Check release history** — Is there a CHANGELOG? Are there tagged releases?

### From the user
Ask about what cannot be observed from code:
- Adoption numbers (how many teams, what percentage)
- Contribution model (who can contribute, what process)
- Team size and age
- Known pain points

---

## Step 1: Assess each dimension

For each of the twelve dimensions:

1. **Gather evidence** — Specific observations from code, docs, or user input
2. **Describe the current state** — What exists, what is missing, what is partially done
3. **Compare against the mature reference** — How far is the current state from what mature systems look like?
4. **Identify the gap** — What specific things would need to change to close the distance?

Be honest about the current state. Describe what you found, not what you hope is there.

---

## Step 2: Place in context

### Industry reference points

Based on published case studies and documented design system characteristics, these are typical maturity profiles for different system types:

**Mature enterprise (Material, Carbon, Polaris level):** Strong across nearly all dimensions. Full token architecture, automated pipelines, documented governance, high adoption. Gaps tend to be in AI readiness and developer experience refinement.

**Established enterprise (1–3 years, dedicated team):** Foundation quality and documentation are typically functional. Governance and deprecation discipline are often the weakest layers. Adoption breadth may be high but depth is inconsistent.

**Early enterprise (first year, part-time team):** Token architecture and component APIs are still forming. Documentation is partial. Governance is informal. Focus should be on getting foundations right rather than chasing breadth.

**Mature product (GitHub Primer, Adobe Spectrum level):** Strong developer experience and API consistency. Documentation often excellent. Governance may be lighter (smaller team, less formal process needed).

**Government systems (USWDS, GOV.UK level):** Accessibility baseline is typically the strongest dimension. Token architecture and AI readiness vary widely. Governance is often strong due to procurement and compliance requirements.

**Agency systems:** Tend to be strong on developer experience (need fast onboarding) but weaker on governance and deprecation discipline (client turnover disrupts continuity).

Use these profiles to contextualise the system's current state — "your token architecture is typical for an established enterprise system" or "your governance is behind what we'd expect at this maturity level."

---

## Step 3: Identify comparison targets

### Automatic comparison

Based on the system's type and maturity, select 3–5 comparison targets from publicly documented systems:

**Enterprise**: Material Design 3 (Google), Carbon (IBM), Polaris (Shopify), Atlassian Design System, Lightning Design System (Salesforce)

**Government**: US Web Design System (USWDS), Australian Government Design System (AGDS), GOV.UK Design System, Canada Design System

**Product**: Primer (GitHub), Spectrum (Adobe), Paste (Twilio), Base Web (Uber)

**Agency**: Orbit (Kiwi.com), Garden (Zendesk)

### What to compare

For each comparison target, document (from published information):
- Approximate component count
- Token architecture approach
- Documentation quality (based on their public doc site)
- Known governance model
- Estimated maturity level
- Notable strengths and weaknesses

Do not fabricate data about comparison targets. Only include information that is publicly documented or observable from their open-source repositories and documentation sites.

---

## Step 4: Produce the benchmark report

---

### Design system benchmark report

Open with a headline sentence that tells the reader the overall state and where to focus.

**Generated by:** Design System Ops — system-benchmark
**Date:** [date]
**System:** [system name]
**Type:** [enterprise / product / government / agency]
**Team size:** [N] | **Active since:** [date/duration] | **Consumers:** [N teams/products]

---

#### Overall benchmark position

**System type:** [enterprise / product / government / agency]
**Maturity band:** [Early / Established / Mature]
**Closest comparable:** [named public system at a similar stage]
**Strongest pillar:** [pillar name]
**Weakest pillar:** [pillar name]

---

#### Pillar summaries

| Pillar | Status | Summary |
|---|---|---|
| Foundation quality | ✅ Strong / ⚠️ Functional / ❌ Weak | [One sentence] |
| Documentation & discoverability | | |
| Governance & process | | |
| Adoption & impact | | |

---

#### Dimension detail

For each of the twelve dimensions:

**[Dimension name]:** ✅ Strong / ⚠️ Functional / ❌ Weak / ❌ Absent

Evidence: [What was observed]
Gap: [What specifically needs to happen to reach the next level of maturity]
Comparison: [How this compares to similar systems — "Material Design has X at this layer, which your system lacks"]

---

#### Comparison matrix

| Dimension | Your system | [Target 1] | [Target 2] | [Target 3] |
|---|---|---|---|---|
| Token architecture | [Status] | [What they have] | [What they have] | [What they have] |
| API consistency | [Status] | | | |
| ... | ... | ... | ... | ... |

---

#### Strengths (top 3 dimensions)

List the three strongest dimensions with why they are strong and what to protect.

---

#### Priority improvement areas (bottom 3 dimensions)

List the three weakest dimensions with:
- Current state and evidence
- What the next level of maturity looks like
- Specific actions to get there
- Estimated effort (small / medium / large)
- Expected timeline

---

#### Maturity roadmap

Based on the benchmark, map a progression path:

**Current state:** [Maturity band] — [key characteristics]
**6-month target:** Focus on [2–3 specific dimensions] — what "done" looks like for each
**12-month target:** Focus on [next 2–3 dimensions] — what "done" looks like for each
**18-month aspiration:** Approaching [comparison target] level in [specific areas]

---

## Recurring workflow

If `recurring` is configured:

1. Load the previous benchmark report
2. Compare dimension statuses — which improved, which held steady, which regressed
3. Add a "Benchmark trend" section showing movement
4. Highlight any dimension that changed status
5. Update the maturity roadmap targets based on actual progress

---

## Closing note (include in every report)

End the report with:

> **A note on context:** This benchmark compares your system against structural best practices — it does not see the constraints, priorities, or trade-offs that shaped it. Some dimensions may be intentionally deprioritised at your current maturity stage. If any finding flags a known, accepted gap, let me know — I'll calibrate future benchmarks to your system's actual priorities. The goal is to highlight opportunities, not to penalise deliberate focus.

---

## Quality checks

- All twelve dimensions are assessed with evidence
- No status is assigned without observable evidence
- Comparison targets are real, publicly documented systems
- No data about comparison targets is fabricated
- The improvement roadmap is specific (not "improve tokens" but "add semantic tier aliases for feedback and status categories")
- The report acknowledges its limitations: comparison target assessments are based on public information, not audited
- Provenance marker is present
- The closing note about intentional deviations is present
