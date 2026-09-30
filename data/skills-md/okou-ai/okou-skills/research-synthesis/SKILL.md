---
name: research-synthesis
description: Synthesize user research into insights, personas, opportunities, themes, and prioritized actions.
---

## Core Analytical Methods

### Thematic Coding

A systematic approach to extracting meaning from qualitative data:

1. **Immersion** — Read the full dataset end-to-end without annotating. Build an intuitive sense of the landscape before imposing structure.
2. **Open coding** — Walk through every data point, attaching descriptive labels. Over-code rather than under-code; collapsing is easier than retroactive splitting.
3. **Pattern grouping** — Cluster related codes into candidate themes. Each theme should represent a meaningful pattern relevant to your research questions.
4. **Validation pass** — Revisit the raw data to stress-test each theme. Confirm sufficient supporting evidence exists, themes do not overlap excessively, and together they form a coherent narrative.
5. **Sharpening** — Give each theme a precise name and a one-to-two sentence definition capturing its essence.
6. **Reporting** — Write up themes as findings, each backed by concrete evidence from the data.

### Bottom-Up Clustering (Affinity Approach)

A technique for letting structure emerge organically from observations:

1. **Atomize** — Record every discrete observation, quote, or data point as an individual unit
2. **Group by similarity** — Arrange units into clusters without predefined categories; let the data dictate the groupings
3. **Name each cluster** — Assign a label that captures the shared thread binding the items together
4. **Build hierarchy** — If natural super-groups appear across clusters, organize them into higher-level categories
5. **Read the map** — The cluster structure and inter-cluster relationships reveal your key themes

**Practical guidance:**
- Keep each unit to a single observation — do not bundle multiple insights together
- Rearrange freely; initial placements are provisional
- Oversized clusters typically contain multiple themes and should be subdivided
- Isolated observations that resist grouping are worth examining — outliers often carry signal
- The clustering process itself generates understanding, not just the final arrangement

### Cross-Validation Through Triangulation

Strengthen any finding by confirming it through independent lines of evidence:

- **Method triangulation**: Probe the same question via different techniques (e.g., interviews, surveys, and analytics)
- **Participant triangulation**: Examine the same question across different user segments or cohorts
- **Temporal triangulation**: Look for the same pattern at multiple points in time

Findings backed by several independent sources carry far more weight. When sources diverge, treat the disagreement as informative — it may point to distinct user segments or context-dependent behavior.

## Working with Interview Data

### Extracting Signal from Individual Sessions

For every interview, pull out four categories of information:

**Observed behaviors and expressed attitudes**
- Separate what participants describe doing from what they feel or believe
- Record situational context: frequency, setting, collaborators involved
- Pay special attention to workarounds — each one represents an unmet need

**Illustrative quotations**
- Select quotes that are specific and vivid, not generic platitudes
- Attribute by participant profile rather than name: "Mid-market ops lead, 50-person team" rather than "Participant 7"
- Remember: a quote is evidence supporting a finding, not a finding in itself

**Gaps between stated preferences and actual behavior**
- What people claim to want frequently diverges from what they actually do
- Observable behavior is stronger evidence than self-reported preference
- When a participant requests a feature but their workflow shows no use of analogous existing features, note the discrepancy

**Intensity signals**
- Emotional markers: frustration, enthusiasm, resignation
- Frequency of encounter: daily pain versus rare annoyance
- Effort invested in workarounds
- Downstream consequences when the problem occurs

### Patterns Across Multiple Sessions

After coding individual interviews:
- Identify which observations recur across participants and count their frequency
- Segment by user type — different roles or contexts often yield different patterns
- Surface contradictions between participants; these frequently indicate meaningful audience segments
- Highlight anything that defied your initial expectations

## Interpreting Survey Data

### Quantitative Response Analysis

- **Sample quality**: Evaluate response rate and potential non-response bias before drawing conclusions
- **Look at distributions, not just means**: A bimodal spread (concentrated at extremes) tells a fundamentally different story than a bell curve, even if the averages match
- **Slice by segment**: Aggregate numbers can conceal critical differences between user groups
- **Respect sample size**: Small samples make minor numerical differences unreliable
- **Contextualize with benchmarks**: Compare against previous periods or industry baselines

### Free-Text Response Analysis
- Apply the same thematic coding process used for interview data
- Tally theme frequency across responses
- Extract representative quotes per theme
- Watch for themes that appear in open text but were absent from the structured questions — these reveal blind spots in your survey design

### Frequent Pitfalls in Survey Analysis
- Reporting means without showing distributions — identical averages can mask radically different response shapes
- Overlooking non-response bias — those who skipped the survey may differ systematically from those who completed it
- Treating small score fluctuations as meaningful — a fraction-of-a-point shift is usually noise
- Assuming equal intervals on Likert scales — the psychological distance between "Strongly Agree" and "Agree" is not necessarily the same as between "Agree" and "Neutral"
- Drawing causal conclusions from cross-tabulated correlations

## Bridging Qualitative and Quantitative Evidence

### The Iterative Loop

- **Start qualitative**: Interviews and observation uncover the what and the why. They generate hypotheses about user behavior.
- **Quantify**: Surveys and analytics measure how widespread and how frequent. They validate or challenge hypotheses at scale.
- **Return to qualitative**: Dive back in to explain surprising quantitative results.

### Combining Evidence Effectively
- Weight qualitative findings by their quantitative reach — a theme from interviews matters more if analytics show it touches a large user base
- Use qualitative data to decode quantitative anomalies — a retention dip is a number; interviews reveal the onboarding redesign confused new users
- Present integrated evidence: "42% of respondents flagged difficulty with X (survey data). Interviews trace the root cause to Y (qualitative finding)."

### When Data Sources Conflict
- Conflicting evidence across methods is a feature, not a flaw — it demands investigation
- Check whether the divergence stems from different populations being measured
- Consider whether self-reported preferences (survey) diverge from actual behavior (analytics)
- Verify whether the survey question truly captured the intended construct
- Report the conflict transparently and pursue follow-up rather than arbitrarily choosing one source

## Building Personas from Data

### From Behavioral Clusters to Profiles

Personas must be grounded in observed patterns, not assumptions:

1. **Detect behavioral clusters**: Identify groups of participants who share similar goals, behaviors, and contexts
2. **Isolate differentiating dimensions**: Determine what separates one cluster from another — usage intensity, company size, technical sophistication, primary job-to-be-done, etc.
3. **Draft persona profiles** for each cluster:
   - Descriptive label and summary
   - Characteristic behaviors and objectives
   - Core frustrations and unaddressed needs
   - Contextual details (role, organization type, adjacent tools)
   - Supporting quotes from research
4. **Ground-truth with quantitative data**: Estimate the size of each persona segment using analytics or survey demographics

### Persona Profile Structure
```
[Label] — [One-sentence characterization]

Background:
- Role, organization type and scale, experience level
- How they discovered and adopted the product

Objectives:
- Primary goals and jobs to be done
- How they define success

Product Relationship:
- Usage frequency and depth
- Key workflows and features relied upon
- Complementary tools in their stack

Frustrations:
- Top unmet needs (limit to 3)
- Workarounds they have built

Decision Drivers:
- What they prioritize in a solution
- What would push them to leave or upgrade

Voice of the User:
- 2-3 verbatim quotes capturing this persona's perspective
```

### Persona Anti-Patterns
- **Demographic framing**: Defining personas by age, gender, or geography instead of behavior. Behavioral attributes predict product needs far more reliably.
- **Persona proliferation**: More than five personas dilutes focus. Aim for three to five.
- **Assumption-based personas**: Profiles invented without research data are fiction, not tools.
- **Stale personas**: Personas that are never revisited as the product and market shift lose their usefulness.
- **Decorative personas**: If a persona does not influence at least one product decision, it is not earning its keep.

## Sizing and Scoring Opportunities

### Estimating the Scale of Each Opportunity

For every insight or opportunity area that emerges from synthesis, estimate:

- **Affected population**: How many users face this problem? Ground the estimate in analytics, survey data, or market sizing.
- **Encounter frequency**: How often does the problem occur for each affected user? (Daily, weekly, monthly, one-time)
- **Impact when it occurs**: What is the severity — complete blocker, meaningful friction, or minor irritant?
- **Commercial signal**: Would solving this drive upgrades, reduce churn, or attract new customers?

### Scoring Framework

Rank opportunities along four dimensions:

- **Impact** = (Affected users) x (Frequency) x (Severity)
- **Evidence quality** = How robust is the supporting data? (Multiple methods and sources >> single data point; behavioral evidence >> self-report)
- **Strategic fit** = Does this align with company direction and product vision?
- **Execution feasibility** = Can this realistically be built? Consider technical complexity, resource requirements, and time to value.

### Communicating Opportunity Estimates
- Make your assumptions visible — show the reasoning chain, not just the conclusion
- Use ranges to convey uncertainty honestly: "Affects 1,500 to 2,500 users per month" rather than spurious precision like "2,137 users"
- Integrate qualitative and quantitative evidence: "Support ticket volume suggests roughly 2,000 monthly occurrences. Interview data indicates approximately 60% of those affected consider it a serious blocker."
- Rank opportunities relative to each other — comparative positioning is often more useful than absolute scores
