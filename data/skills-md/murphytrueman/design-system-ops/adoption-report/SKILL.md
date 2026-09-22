---
name: adoption-report
description: "Produce a design system adoption report separating coverage from actual adoption, with trend direction and risk flags. Trigger when someone says: adoption report, how much is the system being used, usage metrics, adoption status, coverage report, which teams are using the system, who's not using the system, or anything about measuring or reporting on how widely the design system is being used. Here 'coverage' means adoption coverage (how much of the system teams actually use). Do NOT trigger for documentation coverage or doc staleness — use docs-coverage for whether the documentation surface keeps pace with the components."
references:
  - ../../knowledge-notes/output-discipline.md
  - ../../knowledge-notes/adoption-measurement.md
---


# Adoption report

A skill for producing a design system adoption report that distinguishes coverage (who has access and can use the system) from adoption (who is actively using it), with trend direction and risk flags for teams where adoption is low or declining.

## Context

Coverage and adoption are not the same thing, and treating them as equivalent is one of the most common ways design system reports mislead. A system available to twenty product teams has 100% coverage. If only eight of those teams are actively using it, adoption is 40%. Both numbers are true. Only one of them tells you how the system is actually performing.

This skill produces a report that holds both numbers separately and distinguishes between them throughout. It also separates adoption across two dimensions that are frequently conflated: design adoption (are designers using the Figma library?) and engineering adoption (is the code being consumed from the system?). High design adoption with low engineering adoption is a specific kind of problem — the design side is working but the handoff is broken. The reverse is also a specific kind of problem.

---

## Configuration

Before producing output, check for a `.ds-ops-config.yml` file in the project root. If present, load:
- `system.component_count` — informs small-system behaviour
- `system.maturity_level` — informs adoption expectations calibration (see Step 1b)
- `integrations.*` — enables auto-pull for adoption data (see below)
- `recurring.*` — enables trend comparison against previous reports

## Auto-pull integrations

If integrations are configured in `.ds-ops-config.yml`, pull data automatically:

**npm registry** (`integrations.npm.enabled: true`):
- Pull weekly/monthly download statistics for `integrations.npm.package_name` over the reporting period
- Calculate trend direction from download data: increasing, flat, or declining
- For monorepos: pull per-package downloads from `integrations.npm.scoped_packages` — note these are directional signals (see monorepo caveat in component-audit)
- Compare current period downloads against previous period for the engineering adoption trend

**Figma MCP** (`integrations.figma.enabled: true`):
- Pull library analytics from `integrations.figma.file_key` if available via the Figma REST API
- Extract: number of files using the library, component insertion counts, detach rates
- Detach rates are a design adoption quality signal — high detach rates mean designers are pulling components but modifying them, which is partial adoption at best
- Use library file count as the numerator for design adoption percentage
- Track which teams are using the library by analysing team membership in Figma workspace analytics if available

**GitHub** (`integrations.github.enabled: true`):
- Count import references for design system packages across consuming repositories using `gh api search/code`
- Track which repositories import the system — these are the actively adopting engineering teams
- Pull contribution activity: PRs from consuming teams into the design system repo indicate healthy engagement
- Note recency: repositories with no imports in the last 6 months may indicate disengagement or migration to a competitor solution

**Documentation platform** (`integrations.documentation.enabled: true`):
- If the documentation platform has analytics (Zeroheight, Supernova): pull page views per component doc
- High-view-count pages indicate actively used components; zero-view pages indicate unused or undiscoverable documentation
- Track search logs if available — what terms are teams searching for that return no results? These are adoption blockers.

If an integration fails, log it and proceed with manual data gathering. Do not block the adoption report on integration availability.

## Recurring workflow

If `recurring` is configured in `.ds-ops-config.yml`:

1. **Load the previous adoption report** from `recurring.output_directory`.
2. **Auto-populate the trend direction** by comparing current period data against the previous report:
   - Coverage change: +/- teams
   - Adoption change: +/- teams (design and engineering separately)
   - At-risk teams: newly at-risk vs. previously at-risk now recovered
   - Blocker categories: which blockers are persistent vs. newly resolved?
3. **Add a "Period-over-period comparison" section** to the report header showing the deltas
4. **Flag persistent blockers** — any blocker category present in 3+ consecutive reports is a systemic issue, not a one-time finding
5. **Save output** and prune per `recurring.retain_count`.

---

## Step 1: Gather adoption signals

Ask for or confirm (skip questions already answered by auto-pull):
- Which teams or products are in scope?
- What data is available? (Figma library analytics, npm download stats, component usage in codebases, survey data, self-reported figures)
- What is the reporting period? (Quarter, year, or since last report)
- Is there a previous adoption report to compare against for trend direction?

### Step 1a: Adoption signal inventory

Before proceeding, audit which adoption signals are available and their reliability:

**Direct signals (measured data):**
- npm download statistics
- Figma library analytics (files using library, insertion counts, detach rates)
- Code import counts per repository
- Documentation platform analytics (page views per component)
- Support ticket volume by team or component

**Indirect signals (structural inference):**
- Components added to repositories in recent commits (evidence of recent adoption)
- Component usage in shipped products vs. experimental branches
- Design file inventory (how many files reference the design system library)
- Pull request activity between consuming teams and the system repository
- Team interviews or surveys

Document which signals are available and which are unavailable. Adoption assessment is only as strong as the signals used — if only one signal is available, note that the adoption assessment is based on limited data and may be incomplete.

If data is limited: the adoption report can be conducted as a structured assessment based on available signals rather than hard metrics. Note clearly in the output where figures are estimated rather than measured.

### Step 1b: Adoption measurement calibration

Before calculating any metrics, calibrate the measurement against the system's maturity level and the current reporting period. Raw adoption percentages are misleading without context.

**Maturity-appropriate adoption expectations:**

| Maturity level | Expected adoption range | Interpretation guide |
|---|---|---|
| Level 1 (Ad-hoc) | 0–20% | Any adoption is a positive signal. Focus on whether early adopters are satisfied and whether the system is removing friction for them. Growth potential is high. |
| Level 2 (Managed) | 20–50% | Growth is the key metric. Is adoption increasing quarter-over-quarter? This is the growth phase — adoption should be clearly trending up. |
| Level 3 (Systematic) | 50–75% | Breadth matters. Are most teams using the system for most patterns? This is the critical transition phase — crossing 50% indicates the system is now central infrastructure. |
| Level 4 (Measured) | 75–90% | Depth matters. Are teams using the system deeply, not just superficially? At this level, drops in adoption are concerning. Focus on why teams are not using the system for the remaining 10–25% of patterns. |
| Level 5 (Optimised) | 85%+ | Maintenance matters. Is adoption holding steady without active promotion? At this level, the system should sustain adoption with minimal ongoing messaging. Declines are the primary concern. |

**Calibration note for adoption interpretation:** When writing the adoption picture synthesis in Step 5, frame the adoption percentage against the expected range for the system's maturity level. A Level 2 system at 35% adoption is healthy and growing — the focus is on acceleration. A Level 4 system at 35% adoption has a structural problem — focus is on diagnostic. The same percentage means very different things depending on context.

---

## Step 2: Separate coverage from adoption

Before calculating any metrics, define what "coverage" and "adoption" mean for this reporting period.

### Coverage definition

**Coverage** = teams that have access to the system and can use it, whether they are using it or not.

Signals that indicate coverage:
- Team has the npm package installed in their production codebase
- Team has the Figma library enabled in their workspace
- Team has been formally onboarded or given access
- Team has documentation and knows the system exists

Coverage is the easy metric. A system available to twenty product teams has 100% coverage if all twenty have access. The challenge is *actual usage*.

### Adoption definition

**Adoption** = teams that are actively consuming design system components in shipped product work, not just installed or in explorations.

Before calculating any adoption metrics, align on what "adoption" means for this context. Different definitions produce different numbers — and comparing reports that use different definitions creates misleading trends.

**Adoption definition worksheet:**

1. **What counts as "using the system"?**
   - [ ] Installed the package (weakest signal — installed is not adopted)
   - [ ] Imported at least one component in production code
   - [ ] Using 3+ components in production
   - [ ] Using the system for 50%+ of interface patterns
   - [ ] Other: ___

2. **What counts as "design adoption"?**
   - [ ] Figma library is enabled
   - [ ] Components from the library appear in current design files
   - [ ] Designers are using library components without detaching
   - [ ] Other: ___

3. **What counts as "engineering adoption"?**
   - [ ] Package is installed
   - [ ] Components are imported in production code
   - [ ] Token references are used (not hardcoded values)
   - [ ] Other: ___

4. **What is the threshold for "partial" vs "full" adoption?**
   - Partial: ___
   - Full: ___

Document the chosen definitions at the top of the report. Use the same definitions for every subsequent report to enable meaningful trend comparison.

### Why separate design from engineering adoption

Design adoption and engineering adoption are independent. Common patterns:

- **High design adoption, low engineering adoption:** Design system is working, but engineering handoff is broken. The components are being designed with the system, but engineers are not implementing them from the code library. Investigate: are the code components available? Are they what designers think they are? Is there a documentation or discovery gap?

- **Low design adoption, high engineering adoption:** Engineers are adopting the system's code, but designers are not using the Figma library. Investigate: is the design library up to date? Is it discoverable? Are there design tokens being used that are not reflected in the code?

- **Both low:** System has not crossed the adoption threshold. The focus is on why — is there a blocker that explains both, or are design and engineering facing different problems?

---

## Step 3: Identify adopting teams and assess adoption depth

### Gather team-by-team adoption data

For each team in scope, determine:
1. **Design adoption status** — Active / Partial / Not adopting
2. **Engineering adoption status** — Active / Partial / Not adopting
3. **Usage indicators** — specific components used, frequency, recency
4. **Engagement signals** — questions asked, contributions made, documentation viewed

Sources for per-team data:
- Code import analysis (which repos import the system)
- Figma team access logs and component usage
- Support tickets and questions attributed to teams
- Direct interviews or surveys with team leads
- Git commit history (who is merging PRs that add system components)

### Assessment categories

For each team, assign a status:

- **Actively adopting:** Team is shipping products with system components regularly. Usage is recent (within the last 30 days). Both design and engineering are engaged or one is engaged and the other is appropriately delegated.

- **Partially adopting:** Team has shipped with system components, but adoption is inconsistent. May be using the system for some patterns but building locally for others. Engagement is intermittent.

- **Not adopting:** Team has access but is not actively using the system in shipped work. Usage may have been exploratory or one-time.

- **No engagement:** Team has no known contact with the system. May not be aware it exists.

Document the assessment criteria you use so that this assessment can be repeated in future reporting periods.

---

## Step 4: Identify at-risk teams and analyse blockers

### At-risk team signals

Flag teams where adoption is declining, where there has been no engagement for an extended period, or where known blockers exist.

For each at-risk team, identify:
1. **The signal** — declining usage over time, no recent engagement (6+ weeks without contact), known issue report, or team communication indicating plans to move away from the system
2. **The likely cause** if known — from blocker analysis, support conversations, or team feedback
3. **Recommended next step** — reach out to discuss the blockers, offer support, gather more information, or schedule a working session

At-risk teams are the most actionable section of the report. Adoption work is most effective early — a team that has disengaged for six months is significantly harder to re-engage than a team that has been quiet for six weeks.

### Adoption blockers analysis

Based on what is known from team interactions, support requests, and survey data: what are the most commonly cited reasons for non-adoption or partial adoption?

Group blockers into categories:

- **Missing components or patterns:** the system does not have what teams need
- **Documentation gaps:** teams cannot find how to use what exists
- **Integration friction:** technical barriers to consuming the system (installation, build integration, framework compatibility)
- **Awareness gaps:** teams do not know the system exists or have not discovered what they need
- **Tooling misalignment:** the system is built for a different tech stack or tooling context than some teams use
- **Governance or process friction:** the contribution process is unclear, or the system feels gatekept rather than collaborative
- **Reliability concerns:** the system has had breaking changes without migration paths, causing teams to maintain local copies for stability

For each category: how many teams or incidents cite this as a blocker, and what would address it.

Flag if one blocker category dominates. If "missing components" is cited by 80% of at-risk teams, that is a different problem than if "awareness gaps" dominates. The remediation is category-specific.

---

## Step 5: Produce the report

---

### Design system adoption report

**Period:** [reporting period]
**Date:** [date]
**Previous report:** [link or date, if applicable]
**Adoption definition:** [the agreed definition from Step 2]
**Maturity level:** [current system maturity — Level 1/2/3/4/5]

---

#### Period-over-period comparison (if recurring)

| Metric | This period | Previous period | Change | Trend |
|---|---|---|---|---|
| Teams in scope | [n] | [n] | [+/-] | |
| Coverage | [%] | [%] | [+/-] | |
| Active adoption | [%] | [%] | [+/-] | |
| Design adoption | [%] | [%] | [+/-] | |
| Engineering adoption | [%] | [%] | [+/-] | |
| At-risk teams | [n] | [n] | [+/-] | |

---

#### Coverage vs adoption summary

| | Design | Engineering | Combined |
|---|---|---|---|
| Teams in scope | [n] | [n] | [n] |
| Teams with access (coverage) | [n] ([%]) | [n] ([%]) | [n] ([%]) |
| Teams actively adopting | [n] ([%]) | [n] ([%]) | [n] ([%]) |
| Change from last period | [+/- n] | [+/- n] | [+/- n] |

---

#### Adoption picture

One paragraph synthesising the adoption state. Include:
- Overall direction: growing, stable, declining, or mixed
- Whether adoption is ahead of or behind maturity-level expectations
- The most significant finding across design and engineering adoption
- One sentence about what is driving the direction

Example: "Design adoption is growing (55%, up from 45%) and ahead of Level 3 expectations. Engineering adoption is stable (42%, no change) and slightly below expected growth for this maturity level. The design side is working — designers are actively using the Figma library. The gap is in the engineering handoff: code components are available but not widely integrated into shipping products."

---

#### Trend direction

State the overall direction in one sentence: growing, stable, declining, or mixed. A mixed signal (design adoption growing while engineering adoption is flat) is worth naming explicitly.

If this is the first report: no trend direction is available. Flag that this report establishes the baseline and that trend analysis will be available from the next reporting period.

Frame the trend against maturity-level expectations. What is the expected direction for this system at this maturity level? Is the actual trend ahead of or behind expectations?

---

#### Adoption signals used

Document which signals informed this report:
- Direct signals used (e.g., "npm download stats, Figma library analytics, code import counts")
- Signals unavailable (e.g., "documentation platform analytics not available; assessment includes inferred data")
- Data completeness: are all teams represented in the data, or is this a sample?

Example: "Report is based on npm download statistics (reliable), Figma library usage (reliable), and interviews with 8 of 12 teams (partial coverage). Figures for the 4 teams not interviewed are estimated from code import analysis."

---

#### Team-by-team breakdown

For each team in scope:

| Team | Design adoption | Engineering adoption | Status | Notes |
|---|---|---|---|---|
| [Team name] | Active / Partial / Not adopting | Active / Partial / Not adopting | On track / At risk / No engagement | [relevant context] |

For teams with "Partial" adoption: note which areas of the system are being used and which are not. Partial adoption often indicates that the system does not yet serve a specific use case this team has, which is actionable information.

Example: "Team Checkout — Partial / Active: Using form components and buttons (40% of shipping patterns). Building custom payment flow locally (not in system scope). Engagement high. No blockers identified."

---

#### At-risk teams

Flag teams where adoption is declining, where there has been no engagement for an extended period, or where known blockers exist.

For each at-risk team:

| Team | Signal | Likely cause | Recommended action |
|---|---|---|---|
| [Team name] | Declining usage (from 60% to 20% in last quarter) | System does not have date picker; team building locally | Assess date picker as contribution candidate |
| | No recent engagement (last contact 8 weeks ago) | Unknown | Reach out for a conversation |
| | Active parallel solution being built | Framework incompatibility with system | Assess whether to support this team's framework or document local exception |

At-risk teams are the most actionable section of the report.

---

#### Coverage gaps

Which teams do not yet have access to the system? This is a different category from teams that have access but are not adopting — these teams have not been onboarded at all.

For each uncovered team: whether they have expressed interest, what their likely use case would be, and what would be required to extend coverage.

Example: "Team Platform — Not in scope. High interest in using design system for admin tools. Would require: framework support for Django templates (currently system supports React only), evaluation of how admin-specific patterns map to existing component library."

---

#### Adoption blockers

Based on what is known from team interactions, support requests, and survey data: what are the most commonly cited reasons for non-adoption or partial adoption?

Present as a table:

| Blocker category | Cited by | Example | Remediation |
|---|---|---|---|
| Missing components | 6 teams | Date picker, data table, drag-and-drop | Component audit + contribution planning |
| Documentation gaps | 3 teams | "How do I use the Button component in our framework?" | Improve component doc search and examples |
| Integration friction | 4 teams | Installation process, build integration | Simplify setup, provide templates |
| Awareness gaps | 2 teams | Teams did not know system existed | Onboarding outreach |
| Tooling misalignment | 1 team | System uses Vue, team uses Svelte | Assess Svelte support or document local exception |

For each category: how many teams or incidents cite this as a blocker, and what would address it.

Flag if one blocker category dominates. Focus remediation effort on the category affecting the most teams.

---

#### Recommendations

Prioritised actions based on the report findings:

1. **Immediate actions for at-risk teams**
   - List specific teams and specific next steps (reach out, offer support, schedule working session)

2. **Adoption blocker remediation in priority order**
   - Ranked by number of teams affected
   - Include effort estimate if known
   - Link to which skill would execute the work (e.g., "component-audit for missing components gap")

3. **Coverage extension opportunities**
   - List teams not yet onboarded
   - Note what would be required to onboard them
   - Prioritise by strategic value

4. **Metrics improvements**
   - Where is the data incomplete, and what would improve future reporting accuracy?
   - Examples: "Implement GitHub integration to track code imports automatically," "Add documentation platform analytics for visibility into what teams are reading"

---

#### Platform reliability metrics (staff-level)

At the staff level, adoption reports should include infrastructure reliability signals alongside usage metrics. These help explain WHY adoption is where it is.

**Release reliability:**
- Number of releases in the reporting period
- Number of breaking changes in the reporting period
- Were breaking changes accompanied by migration paths? (Y/N per breaking change)
- Median time from bug report to fix for system-level bugs

**Documentation currency:**
- % of components where documentation matches the current released version
- Number of documentation-related support requests in the period (high number = documentation is stale or unclear)

**Integration friction score:**
- Average time from "team decides to adopt" to "first component in production" for teams that onboarded in this period
- What were the most common setup blockers? (Installation, configuration, framework incompatibility, token integration)

Frame these as leading indicators: reliability metrics predict future adoption trends. A system with two breaking changes, no migration paths, and stale documentation will lose adoption even if current numbers look healthy.

---

#### AI tooling adoption (staff-level)

If the system has AI-ready metadata (structured descriptions, machine-readable manifests, MCP integration):

- Are AI tools (Claude, GitHub Copilot, Cursor, etc.) using the system's metadata to generate component usage?
- What is the quality of AI-generated output? (Are AI agents selecting the right components, configuring them correctly, avoiding anti-patterns?)
- Are teams using AI-assisted workflows with the system, or is the AI metadata unused?

This is a forward-looking metric. Even if AI tooling adoption is currently zero, documenting AI readiness positions the system for the next wave of tooling.

---

#### Small-system note (fewer than 5 components)

For systems this size, the coverage-vs-adoption framing still works but the metrics change. Coverage is likely 100% — if you have three components, every team that uses the system has access to all of them. Adoption is better measured as scope coverage: what percentage of the team's actual interface needs does the system serve? A system with 3 components that covers 80% of a team's UI patterns has stronger adoption than a 30-component system covering 20%.

The team-by-team breakdown may reduce to a single team or two — that is fine, but go deeper per team: which patterns are they using the system for, and which are they building locally?

The "at-risk teams" section may not apply if there is only one consuming team. Replace it with an "unserved needs" section listing the interface patterns the team is building outside the system. These are your roadmap.

For reporting, treat partial adoption as "using the system for [%]% of patterns" rather than "using 3 of 5 components."

---

## Quality checks

- Coverage and adoption are reported separately throughout — they are never combined into a single figure
- Design adoption and engineering adoption are reported separately
- Trend direction is stated, not implied
- At-risk teams are flagged with a specific signal, not just a low number
- Adoption blockers are specific and grouped by category, not listed as individual team complaints
- The adoption definition is documented and will enable consistent comparison in the next reporting period
- Where figures are estimated rather than measured, this is stated
- Adoption picture is framed against maturity-level expectations
- If period-over-period comparison is included, the previous report was actually loaded and compared
- If platform reliability metrics are included, they are framed as adoption predictors, not separate metrics
- If AI tooling adoption is included, it is framed as forward-looking and not penalised if currently zero
- Signals used are documented (which signals were available, which were unavailable, which were estimated)
- At-risk team recommendations are specific and actionable, not generic
- Recommendations include which skill would execute the work, where applicable
