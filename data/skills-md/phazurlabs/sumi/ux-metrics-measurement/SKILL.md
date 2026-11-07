---
name: ux-metrics-measurement
description: "UX measurement: HEART framework, SUS, UEQ, SUPR-Q, task success and time-on-task metrics, A/B testing statistics, AI-specific metrics, and design system ROI. Use when defining UX KPIs, building a measurement plan, interpreting a usability score, or proving UX impact."
---

# UX Metrics & Measurement — Quantifying User Experience

## Measurement Philosophy

Measure what matters, not what is easy. Vanity metrics (page views, downloads, time on site) tell you what happened but not whether the experience was good. Meaningful UX metrics connect user behavior to user satisfaction to business outcomes. Every metric in the system should answer one of three questions: Is it usable? Is it useful? Is it desirable?

### The Measurement Hierarchy

1. **Behavioral metrics** (what users do) are more reliable than **attitudinal metrics** (what users say).
2. **Task-level metrics** (can users accomplish goals?) matter more than **session-level metrics** (how long did users stay?).
3. **Leading indicators** (early signals of success/failure) are more actionable than **lagging indicators** (outcomes measured after the fact).
4. **Benchmarked metrics** (compared to industry or historical baseline) are more meaningful than **absolute metrics** (numbers without context).

## HEART Framework (Google)

The HEART framework provides a structured approach to selecting user-centered metrics across five dimensions. Developed at Google, it maps product goals to measurable signals to concrete metrics.

### Five Dimensions

**Happiness** — Subjective user satisfaction and sentiment
- Signals: survey responses, ratings, sentiment in feedback
- Example metrics: satisfaction score (CSAT), NPS, SUS score, ease-of-use rating
- Measurement: post-task surveys, in-app ratings, periodic satisfaction surveys

**Engagement** — Depth and frequency of user interaction
- Signals: session frequency, feature usage, content consumption
- Example metrics: DAU/MAU ratio, actions per session, feature adoption rate, session depth
- Measurement: product analytics, event tracking

**Adoption** — New users successfully onboarding
- Signals: signups, onboarding completion, first key action
- Example metrics: signup-to-activation rate, onboarding completion rate, time to first value
- Measurement: funnel analytics, cohort analysis

**Retention** — Users continuing to derive value over time
- Signals: return visits, subscription renewals, continued usage
- Example metrics: D1/D7/D30 retention, churn rate, renewal rate, feature retention
- Measurement: cohort retention curves, survival analysis

**Task Success** — Ability to complete intended goals effectively and efficiently
- Signals: task completion, errors, time spent, help requests
- Example metrics: task success rate, time on task, error rate, lostness score
- Measurement: usability testing, analytics funnels, error logging

### Goals-Signals-Metrics Process

For each product area, work through three columns:

1. **Goal:** What is the desired user outcome? ("Users can find relevant products quickly")
2. **Signal:** What user behavior indicates progress toward the goal? ("Users complete searches and click results")
3. **Metric:** How do you quantify the signal? ("Search-to-click rate, average time from search to product page view")

This process prevents metric selection from being arbitrary. Every metric traces back to a user goal.

## System Usability Scale (SUS)

The most widely used standardized usability questionnaire. Ten questions on a five-point Likert scale, producing a score from 0-100.

### Scoring and Interpretation

- Raw score calculation: alternate positive/negative items, subtract/add from scale anchors, multiply by 2.5.
- Average SUS score across studies: 68 (this is the 50th percentile, not a passing grade).
- Adjective scale mapping: <50 = Awful, 50-67 = Poor to OK, 68 = Passable, 68-80 = Good, 80-90 = Excellent, 90+ = Best Imaginable.
- Grade scale: <60 = F, 60-69 = D, 70-79 = C, 80-89 = B, 90+ = A.
- Percentile benchmarks: 68 = 50th, 74 = 64th, 80 = 85th, 86 = 96th.

### When to Use SUS

- After usability testing sessions (post-study).
- Baseline measurement before redesign.
- Comparative evaluation between design alternatives.
- Longitudinal tracking across releases.
- Industry benchmarking.

### Limitations

- SUS measures perceived usability, not actual usability. A user may rate a system highly despite making errors.
- The 10-item format is not ideal for quick pulse checks — use UMUX-Lite (2 items) for lightweight measurement.
- SUS does not diagnose specific issues — it is a thermometer, not a diagnostic tool.

## UEQ (User Experience Questionnaire)

The UEQ measures six dimensions of user experience: Attractiveness, Perspicuity (clarity), Efficiency, Dependability, Stimulation, and Novelty. It uses 26 semantic differential items (word pairs).

### When to Use UEQ Over SUS

- When you need dimensional insight beyond a single usability score.
- When hedonic qualities (stimulation, novelty) matter alongside pragmatic qualities (perspicuity, efficiency, dependability).
- When comparing products across multiple experience dimensions.
- UEQ+ (modular version) allows selecting only relevant scales.

## UMUX-Lite

A two-item questionnaire that correlates strongly with SUS (r = 0.83). Useful for: in-app pulse surveys, post-task quick checks, high-frequency measurement where survey fatigue is a concern.

Items: (1) "[System] capabilities meet my requirements." (2) "[System] is easy to use." Both rated on a seven-point Likert scale.

## SUPR-Q (Standardized User Experience Percentile Rank Questionnaire)

Web-specific measurement covering four factors: Usability, Trust/Credibility, Appearance, and Loyalty. Produces a percentile rank against a database of 200+ websites. Best for benchmarking web experiences against industry competitors.

## Task-Based Metrics

### Task Success Rate

The most fundamental UX metric. Percentage of users who successfully complete a defined task.

- **Binary success:** Did the user complete the task? Yes/No.
- **Partial success:** Weighted scoring for partially completed tasks (e.g., 0 = fail, 0.5 = completed with significant difficulty, 1 = success).
- **Benchmark:** Industry average for web tasks is approximately 78%. Below 70% indicates serious usability problems.

### Time on Task

How long users take to complete a task. Lower is generally better, but context matters — rushed completion may indicate skipped steps.

- Measure from task start to task completion.
- Use geometric mean (not arithmetic mean) because time data is typically right-skewed.
- Compare against baseline or competitor benchmarks.
- Distinguish between first-time and repeat users.

### Error Rate

Frequency and severity of errors during task completion.

- **Error frequency:** Number of errors per task attempt.
- **Error taxonomy:** Classify errors as slips (wrong action, right intention), mistakes (wrong intention), or system errors (not user-caused).
- **Recovery rate:** Percentage of errors the user successfully recovers from.
- **Error impact:** Which errors cause task abandonment versus temporary friction.

### Lostness Score

Measures navigation efficiency. Calculated as: Lostness = sqrt((N/S - 1)^2 + (R/N - 1)^2) where N = number of pages visited, S = minimum pages needed, R = unique pages visited.

- Score of 0 = optimal path. Score above 0.4 = user is seriously lost.
- Useful for evaluating information architecture and navigation design.

## Behavioral Analytics

### Funnel Analysis

Track user progression through multi-step flows. Identify where users drop off and why.

- Define funnels for every critical flow: onboarding, checkout, feature activation, upgrade.
- Measure step-to-step conversion rate, overall completion rate, and time per step.
- Segment funnels by user cohort, acquisition channel, device, and user experience level.
- Investigate drop-off points with session recordings and qualitative research.

### Cohort Analysis

Group users by shared characteristic (signup date, acquisition channel, plan tier) and track behavior over time.

- Retention cohorts: What percentage of users who signed up in Week 1 are still active in Week 4, 8, 12?
- Feature cohorts: How does behavior differ between users who adopted Feature X versus those who did not?
- Identify the "aha moment" — the action most correlated with long-term retention.

### Retention Curves

Plot the percentage of active users over time since signup.

- **Flattening curve:** Healthy product — a stable base of users finds lasting value.
- **Declining curve:** Problem — users are not finding enough value to stay.
- **Smiling curve:** Recovery — initial drop-off followed by increasing engagement (often from re-engagement campaigns).

## Experimentation

### A/B Testing

Compare two design variants with random user assignment to determine which performs better on a defined metric.

- **Hypothesis template:** "If we [change], then [metric] will [improve/decrease] by [amount] because [reasoning]."
- **Sample size:** Calculate before launching using a power calculator. Specify minimum detectable effect, significance level (typically 0.05), and power (typically 0.80).
- **Duration:** Run for at least one full business cycle (minimum 1-2 weeks). Do not peek at results and stop early.
- **One variable:** Test one change at a time for clear causation. Multivariate testing requires exponentially larger samples.
- **Guard rails:** Monitor guardrail metrics (crash rate, load time, error rate) to ensure the variant does not cause harm even if the primary metric improves.

### Sequential Testing

Alternative to fixed-horizon A/B testing. Allows checking results continuously without inflating false positive rate. Useful when you need faster decisions or have variable traffic.

## Benchmarking

### Industry Benchmarks

- **SUS:** Average across studies is 68. B2B software averages 65-72. Consumer apps average 70-78.
- **Task success rate:** Web average 78%. E-commerce checkout 65-70%. Mobile forms 60-75%.
- **NPS:** Average varies by industry. SaaS averages 30-40. B2C averages 40-60.
- **Time on task:** Highly variable. Compare against your own historical baseline rather than cross-industry.

### Historical Tracking

- Track key metrics across every release. Plot trendlines.
- Set regression thresholds: alert when a metric drops more than 5% from baseline.
- Celebrate improvements with the team — measurement should drive positive reinforcement.

## AI-Specific UX Metrics

- **Trust calibration score:** How closely does user confidence in AI output match actual AI accuracy?
- **Appropriate reliance rate:** Percentage of times users correctly accept accurate AI outputs and correctly reject inaccurate ones.
- **AI feature adoption:** Opt-in rate, prompt frequency, feature retention over time.
- **Correction frequency:** How often users edit or override AI outputs.
- **Time saved:** Measured difference in task time with AI versus without.

## Design System Metrics

- **Adoption rate:** Percentage of UI built with design system components versus custom implementations.
- **Component reuse:** Average instances per component across products.
- **Consistency score:** Visual regression pass rate across products.
- **Contribution rate:** External PRs per month to the design system.
- **Developer satisfaction:** Quarterly NPS survey of design system consumers.
- **Design system ROI:** [(Time efficiency gains + Quality gains + Scale gains + Consistency gains) - (Initial cost + Maintenance cost)] / (Initial + Maintenance) x 100%.
- Sparkbox research data: 38% design efficiency, 31% dev efficiency, 228% higher ROI with mature DesignOps.

## Routing

For **choosing and scoring a framework** — HEART in depth, SUS scoring, UEQ,
UMUX-Lite, SUPR-Q, task metrics, NPS/CES/CSAT used correctly in a UX context,
analytics metric design, and experimentation: read
`references/metrics-frameworks-compendium.md`.

For **measuring an AI feature** — the AI-specific metric taxonomy, affective and
emotion metrics, cross-platform measurement, experimentation designs that survive
non-determinism, continuous discovery, atomic research, and the pitfalls unique
to AI experiments: read `references/ai-ux-metrics-experimentation.md`.

## Cross-Referencing

- For heuristic evaluation methodology, reference `nng-ux-heuristics`.
- For research methodology, reference `ux-research-methods`.
- For AI-specific metrics detail, reference `ux-metrics-measurement/references/ai-ux-metrics-experimentation`.
- For design system metrics detail, reference `design-systems-architecture/references/governance-scaling`.
- For usability testing protocols that produce metrics, reference `ux-research-methods/references/research-protocols`.

## v3.0 Cross-References

The v3.0 upgrade adds reference materials that extend measurement into design system maturity, AI-specific quality metrics, and notification effectiveness.

**Design System Maturity Metrics**
See `design-systems-architecture/references/maturity-model-multi-brand.md` for the 5-level design system maturity assessment rubric with quantifiable metrics at each level — including adoption rate thresholds (Level 3 requires 60%+ component coverage), contribution velocity benchmarks, token coverage ratios, cross-platform parity scores, and governance process maturity indicators. This reference provides the structured assessment framework that complements the Design System Metrics section above, enabling teams to measure where they stand and define concrete advancement targets.

**AI-Specific Quality and Trust Metrics**
See `agentic-ai-generative-ux/references/llm-hallucination-design-guardrails.md` for expanded AI-specific metrics beyond the AI-Specific UX Metrics section above — including hallucination rate measurement methodology (per-claim factual accuracy scoring), confidence calibration metrics (Expected Calibration Error measuring alignment between stated confidence and actual correctness), trust calibration accuracy (user trust vs. system reliability correlation), verification engagement rate (how often users check AI citations), and AI quality gate pass/fail rates for production deployment monitoring. These metrics are essential for any team shipping LLM-powered features.

**Notification Effectiveness Metrics**
See `performance-states-patterns/references/notification-system-design.md` for metrics specific to notification system evaluation — including notification-to-action rate (percentage of notifications that lead to meaningful user action), dismissal rate by notification type, opt-out rate trending, notification fatigue indicators (declining engagement over time), time-to-action measurement, and notification channel effectiveness comparison (push vs. in-app vs. email). These metrics connect directly to the HEART framework's Engagement dimension for notification-driven features.

## Key Sources

- Google HEART Framework (Rodden, Hutchinson, Fu)
- Sauro, J. & Lewis, J.: "Quantifying the User Experience"
- MeasuringU: 48 UX Metrics (2025)
- Brooke, J.: SUS — A Quick and Dirty Usability Scale
- Schrepp, M.: User Experience Questionnaire (UEQ)
- Frontiers in Computer Science: UX Measurement Frameworks
- Sparkbox: Design System ROI Research
- NNG Group: UX Maturity Model, DesignOps 101
