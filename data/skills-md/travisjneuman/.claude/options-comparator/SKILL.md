---
name: options-comparator
description: Structured comparison of competing options with weighted scoring matrices, trade-off analysis, decision frameworks, and recommendation templates. Use when evaluating alternatives, making purchase decisions, or comparing strategies.
---

# Options Comparator

Structured frameworks for systematically comparing alternatives, scoring options, and producing defensible recommendations.

## Weighted Scoring Matrix

### Standard Weighted Matrix Template

```
WEIGHTED SCORING MATRIX:

STEP 1: Define criteria and weights (must sum to 100%)

| Criterion       | Weight | Option A | Option B | Option C |
|-----------------|--------|----------|----------|----------|
| [Criterion 1]   |   25%  |   [1-5]  |   [1-5]  |   [1-5]  |
| [Criterion 2]   |   20%  |   [1-5]  |   [1-5]  |   [1-5]  |
| [Criterion 3]   |   20%  |   [1-5]  |   [1-5]  |   [1-5]  |
| [Criterion 4]   |   15%  |   [1-5]  |   [1-5]  |   [1-5]  |
| [Criterion 5]   |   10%  |   [1-5]  |   [1-5]  |   [1-5]  |
| [Criterion 6]   |   10%  |   [1-5]  |   [1-5]  |   [1-5]  |
|-----------------|--------|----------|----------|----------|
| WEIGHTED TOTAL  |  100%  |  [sum]   |  [sum]   |  [sum]   |

STEP 2: Calculate weighted scores
  Weighted score = Raw score x Weight
  Total = Sum of all weighted scores

STEP 3: Interpret results
  4.5-5.0: Excellent fit
  3.5-4.4: Good fit
  2.5-3.4: Acceptable with trade-offs
  1.5-2.4: Poor fit — significant concerns
  1.0-1.4: Disqualified

SCORING RUBRIC:
  5 = Exceeds requirements / best in class
  4 = Fully meets requirements
  3 = Partially meets requirements
  2 = Significant gaps
  1 = Does not meet requirements / disqualifying
```

### Weight Assignment Methods

| Method | How It Works | Best For |
| --- | --- | --- |
| **Direct assignment** | Stakeholders allocate 100 points across criteria | Small groups, quick decisions |
| **Pairwise comparison** | Compare criteria two at a time, derive weights | Rigorous prioritization |
| **MoSCoW ranking** | Must/Should/Could/Won't, then assign within tiers | Requirements-driven decisions |
| **Swing weighting** | Rate criteria by how much best-to-worst matters | Complex multi-attribute decisions |
| **Stakeholder voting** | Each stakeholder distributes 10 votes | Democratic team decisions |

### Weight Validation Checklist

```
BEFORE FINALIZING WEIGHTS:

- [ ] Weights sum to exactly 100%
- [ ] No single criterion exceeds 40% (unless justified)
- [ ] No criterion is below 5% (drop it if irrelevant)
- [ ] Weights reflect stated priorities (not just habit)
- [ ] Stakeholders reviewed and approved weights
- [ ] Weights were set BEFORE scoring options
      (prevents reverse-engineering to a preferred choice)
```

## Pairwise Comparison

### Pairwise Comparison Matrix

```
PAIRWISE COMPARISON TEMPLATE:

Compare criteria A through E. For each pair, indicate
which is more important (mark the winner):

         A      B      C      D      E    WINS  WEIGHT
A  [--]   [ ]    [A]    [ ]    [A]     2     25%
B  [B]    [--]   [B]    [B]    [B]     4     40%
C  [ ]    [ ]    [--]   [ ]    [C]     1     10%
D  [D]    [ ]    [D]    [--]   [D]     3     25%
E  [ ]    [ ]    [ ]    [ ]    [--]    0      0%

Weight = Wins / Total comparisons x 100
Total comparisons = n(n-1)/2 = 5(4)/2 = 10

INSTRUCTIONS:
1. Compare each pair: "Is criterion X more important than Y?"
2. Mark the winner in the matrix
3. Count wins for each criterion
4. Calculate weights from win percentages
5. Adjust if any criterion has 0% but should remain
```

### Forced Ranking

```
FORCED RANKING METHOD:

List all options and rank from best to worst on each criterion.
No ties allowed (forces differentiation).

| Criterion     | Rank 1 (Best) | Rank 2 | Rank 3 | Rank 4 (Worst) |
|---------------|---------------|--------|--------|-----------------|
| Price         | Option C      | Option A| Option D| Option B       |
| Quality       | Option B      | Option D| Option A| Option C       |
| Speed         | Option A      | Option B| Option C| Option D       |
| Support       | Option D      | Option C| Option B| Option A       |

SCORING:
  Rank 1 = 4 points, Rank 2 = 3, Rank 3 = 2, Rank 4 = 1
  (Or weight the ranking scores by criterion importance)
```

## Pros/Cons with Weights

### Structured Pros/Cons Template

```
WEIGHTED PROS/CONS ANALYSIS:

OPTION: [Name]

PROS:
| # | Advantage                    | Impact | Certainty | Score |
|---|------------------------------|--------|-----------|-------|
| 1 | [Pro description]            | H/M/L  | H/M/L    | [1-9] |
| 2 | [Pro description]            | H/M/L  | H/M/L    | [1-9] |
| 3 | [Pro description]            | H/M/L  | H/M/L    | [1-9] |

CONS:
| # | Disadvantage                 | Impact | Certainty | Score |
|---|------------------------------|--------|-----------|-------|
| 1 | [Con description]            | H/M/L  | H/M/L    | [1-9] |
| 2 | [Con description]            | H/M/L  | H/M/L    | [1-9] |
| 3 | [Con description]            | H/M/L  | H/M/L    | [1-9] |

SCORING GUIDE:
  Impact:    High=3, Medium=2, Low=1
  Certainty: High=3, Medium=2, Low=1
  Score = Impact x Certainty (range: 1-9)

NET SCORE = Sum of Pro scores - Sum of Con scores
  Positive: Pros outweigh cons
  Negative: Cons outweigh pros
  Near zero: Trade-off decision (needs judgment)
```

### Comparative Pros/Cons

| Factor | Option A | Option B | Option C |
| --- | --- | --- | --- |
| **Best for** | [ideal use case] | [ideal use case] | [ideal use case] |
| **Worst for** | [poor fit scenario] | [poor fit scenario] | [poor fit scenario] |
| **Top Pro** | [strongest advantage] | [strongest advantage] | [strongest advantage] |
| **Top Con** | [biggest drawback] | [biggest drawback] | [biggest drawback] |
| **Risk level** | Low / Medium / High | Low / Medium / High | Low / Medium / High |
| **Reversibility** | Easy / Hard / Impossible | Easy / Hard / Impossible | Easy / Hard / Impossible |

## Decision Matrix Template

### Comprehensive Decision Matrix

```
DECISION MATRIX:

DECISION: [Clear statement of what you are deciding]
DATE:     [Date of analysis]
OWNER:    [Decision maker(s)]
DEADLINE: [When decision must be made]

OPTIONS UNDER CONSIDERATION:
  A. [Option name and brief description]
  B. [Option name and brief description]
  C. [Option name and brief description]
  D. [Status quo / do nothing]

MUST-HAVE CRITERIA (pass/fail — eliminates options):
| Requirement          | Option A | Option B | Option C | Option D |
|----------------------|----------|----------|----------|----------|
| [Hard requirement 1] | Pass/Fail| Pass/Fail| Pass/Fail| Pass/Fail|
| [Hard requirement 2] | Pass/Fail| Pass/Fail| Pass/Fail| Pass/Fail|
| [Hard requirement 3] | Pass/Fail| Pass/Fail| Pass/Fail| Pass/Fail|

NICE-TO-HAVE CRITERIA (scored and weighted):
| Criterion    | Weight | Opt A | Opt B | Opt C | Opt D |
|-------------|--------|-------|-------|-------|-------|
| [Criterion] |   X%   | [1-5] | [1-5] | [1-5] | [1-5] |
| [Criterion] |   X%   | [1-5] | [1-5] | [1-5] | [1-5] |
| [Criterion] |   X%   | [1-5] | [1-5] | [1-5] | [1-5] |
|-------------|--------|-------|-------|-------|-------|
| TOTAL       |  100%  | [sum] | [sum] | [sum] | [sum] |

RECOMMENDATION: [Option letter] because [1-2 sentence rationale]

RISKS OF CHOSEN OPTION:
1. [Risk and mitigation plan]
2. [Risk and mitigation plan]

NEXT STEPS:
1. [Action item, owner, deadline]
2. [Action item, owner, deadline]
```

## Trade-Off Analysis Framework

### Trade-Off Mapping

```
TRADE-OFF ANALYSIS:

STEP 1: Identify the key trade-off dimensions
  Common trade-offs:
  - Cost vs Quality
  - Speed vs Thoroughness
  - Flexibility vs Standardization
  - Control vs Convenience
  - Short-term vs Long-term
  - Risk vs Reward
  - Simplicity vs Capability

STEP 2: Map options on trade-off axes

              HIGH QUALITY
                  |
                  |    Option B
                  |       *
                  |
  LOW COST -------+--------- HIGH COST
                  |
          Option A|
              *   |
                  |    Option C
                  |       *
              LOW QUALITY

STEP 3: Identify the efficient frontier
  Options on the frontier are rationally competitive.
  Options below the frontier are dominated
  (another option is better on all axes).

STEP 4: Choose based on priorities
  "We are optimizing for [dimension] while keeping
  [other dimension] above [minimum threshold]."
```

### Trade-Off Decision Rules

| Rule | When to Use | How It Works |
| --- | --- | --- |
| **Maximize one, threshold others** | Clear primary objective | Set minimums for secondary criteria, then pick highest on primary |
| **Satisfice** | Time-pressured, good enough is fine | Pick first option that meets all minimum thresholds |
| **Lexicographic** | Clear priority ordering | Sort by most important criterion first, break ties with second |
| **Minimax regret** | High uncertainty | Choose option that minimizes worst-case disappointment |
| **Expected value** | Quantifiable outcomes and probabilities | Probability x payoff for each scenario, pick highest EV |

## Sensitivity Analysis for Decisions

### Weight Sensitivity Testing

```
SENSITIVITY ANALYSIS:

PURPOSE: Test if the recommendation changes when weights shift.

BASELINE WEIGHTS:
  Cost: 30% | Quality: 25% | Speed: 20% | Support: 15% | Risk: 10%
  Winner: Option B (score: 3.85)

SCENARIO 1 — Cost-focused (Cost +15%, others proportionally reduced):
  Cost: 45% | Quality: 20% | Speed: 16% | Support: 12% | Risk: 7%
  Winner: [recalculate]

SCENARIO 2 — Quality-focused (Quality +15%):
  Cost: 24% | Quality: 40% | Speed: 16% | Support: 12% | Risk: 8%
  Winner: [recalculate]

SCENARIO 3 — Risk-averse (Risk +20%):
  Cost: 22% | Quality: 19% | Speed: 15% | Support: 14% | Risk: 30%
  Winner: [recalculate]

INTERPRETATION:
  If the same option wins in all scenarios → ROBUST decision
  If winner changes in 1 scenario → Note the sensitivity
  If winner changes in 2+ scenarios → Decision depends on priorities
```

### Score Sensitivity Testing

```
BREAKEVEN ANALYSIS:

"How much would Option A's score on [criterion] need
to improve to overtake Option B?"

Current:
  Option A total: 3.45
  Option B total: 3.85
  Gap: 0.40

Criterion X (weight 25%):
  Option A score: 2
  Required score to close gap: 2 + (0.40 / 0.25) = 3.6 → round to 4
  Is this plausible? [Yes/No]
  If yes → decision is sensitive to this criterion
  If no → decision is robust on this dimension
```

## Recommendation Memo Template

### Executive Decision Memo

```
DECISION RECOMMENDATION MEMO

TO:       [Decision maker(s)]
FROM:     [Analyst / Team]
DATE:     [Date]
RE:       Recommendation: [Decision topic]

─────────────────────────────────────────────

EXECUTIVE SUMMARY:
We recommend [Option X] for [one-sentence rationale].
This option scores highest across our evaluation criteria,
particularly in [top 2 criteria]. Estimated [cost/timeline]:
[key number]. Key risk: [top risk and mitigation].

─────────────────────────────────────────────

BACKGROUND:
[2-3 sentences on why this decision is needed now]

OPTIONS EVALUATED:
  A. [Option and one-line description]
  B. [Option and one-line description]
  C. [Option and one-line description]

EVALUATION CRITERIA AND WEIGHTS:
  [Criterion 1] (X%) | [Criterion 2] (X%) | [Criterion 3] (X%)

SCORING SUMMARY:
| Option | Score | Rank | Key Strength         | Key Weakness        |
|--------|-------|------|----------------------|---------------------|
| A      | 3.45  | 2    | [strength]           | [weakness]          |
| B      | 3.85  | 1    | [strength]           | [weakness]          |
| C      | 2.90  | 3    | [strength]           | [weakness]          |

RECOMMENDATION: Option B
Rationale: [3-5 sentences explaining why, addressing trade-offs]

SENSITIVITY: This recommendation holds under all tested scenarios
except [edge case], which would require [condition].

RISKS AND MITIGATIONS:
1. [Risk]: [Mitigation plan]
2. [Risk]: [Mitigation plan]

IMPLEMENTATION PLAN:
1. [Step, owner, date]
2. [Step, owner, date]
3. [Decision review checkpoint, date]

─────────────────────────────────────────────

APPENDIX: Detailed scoring matrix, sensitivity analysis
```

## Vendor Evaluation Scorecard

### Vendor Assessment Template

```
VENDOR EVALUATION SCORECARD:

VENDOR:          [Company name]
EVALUATED BY:    [Names]
DATE:            [Date]
PRODUCT/SERVICE: [What you are evaluating]

CATEGORY 1: PRODUCT FIT (30% weight)
| Criterion                  | Score (1-5) | Notes                |
|----------------------------|-------------|----------------------|
| Feature completeness       |             |                      |
| Integration capability     |             |                      |
| Scalability                |             |                      |
| Customization options      |             |                      |
| User experience / UI       |             |                      |
| Category subtotal          |     /25     |                      |

CATEGORY 2: COMMERCIAL (25% weight)
| Criterion                  | Score (1-5) | Notes                |
|----------------------------|-------------|----------------------|
| Total cost of ownership    |             |                      |
| Pricing transparency       |             |                      |
| Contract flexibility       |             |                      |
| Payment terms              |             |                      |
| ROI timeline               |             |                      |
| Category subtotal          |     /25     |                      |

CATEGORY 3: SUPPORT AND SERVICE (20% weight)
| Criterion                  | Score (1-5) | Notes                |
|----------------------------|-------------|----------------------|
| Implementation support     |             |                      |
| Training resources         |             |                      |
| Ongoing customer support   |             |                      |
| SLA commitments            |             |                      |
| Account management         |             |                      |
| Category subtotal          |     /25     |                      |

CATEGORY 4: COMPANY VIABILITY (15% weight)
| Criterion                  | Score (1-5) | Notes                |
|----------------------------|-------------|----------------------|
| Financial stability        |             |                      |
| Market position            |             |                      |
| Product roadmap            |             |                      |
| Customer references        |             |                      |
| Industry reputation        |             |                      |
| Category subtotal          |     /25     |                      |

CATEGORY 5: RISK (10% weight)
| Criterion                  | Score (1-5) | Notes                |
|----------------------------|-------------|----------------------|
| Data security / compliance |             |                      |
| Vendor lock-in risk        |             |                      |
| Migration complexity       |             |                      |
| Business continuity plan   |             |                      |
| Reference check results    |             |                      |
| Category subtotal          |     /25     |                      |

OVERALL WEIGHTED SCORE: [calculated] / 5.0
RECOMMENDATION: Proceed / Shortlist / Reject
```

## Technology Selection Framework

### Technology Evaluation Criteria

```
TECHNOLOGY SELECTION MATRIX:

FUNCTIONAL FIT:
- [ ] Meets core requirements (pass/fail list)
- [ ] Handles expected scale (users, data, transactions)
- [ ] Integrates with existing stack
- [ ] Supports required platforms/environments

DEVELOPER EXPERIENCE:
- [ ] Documentation quality and completeness
- [ ] Community size and activity (GitHub stars, forums)
- [ ] Learning curve for the team
- [ ] Tooling and IDE support
- [ ] Error messages and debugging experience

OPERATIONAL:
- [ ] Deployment model fits infrastructure
- [ ] Monitoring and observability support
- [ ] Backup and disaster recovery
- [ ] Security track record and patching cadence

STRATEGIC:
- [ ] Aligned with technology direction
- [ ] Vendor/project longevity (not abandonware)
- [ ] Hiring market (can you find people who know it?)
- [ ] Exit strategy (migration path if you switch later)

TOTAL COST:
- [ ] License / subscription fees
- [ ] Infrastructure costs
- [ ] Training and ramp-up time
- [ ] Maintenance and operations
- [ ] Opportunity cost of alternatives
```

### Build vs Buy Decision

| Factor | Build | Buy | Hybrid |
| --- | --- | --- | --- |
| Core differentiator? | Yes — build it | No — buy it | Customize a platform |
| Team has expertise? | Yes | No | Partial |
| Time to value | Months | Weeks | Weeks-Months |
| Long-term cost | Higher (maintenance) | Predictable (subscription) | Mixed |
| Control | Full | Limited | Moderate |
| Risk | Technical debt | Vendor dependency | Both |
| Best when | Unique requirements, strategic IP | Commodity functionality | 80/20 fit |

## Decision Anti-Patterns

```
COMMON DECISION MISTAKES:

1. ANALYSIS PARALYSIS
   Symptom: Endless evaluation, no decision made
   Fix: Set a decision deadline and "good enough" threshold

2. ANCHORING TO FIRST OPTION
   Symptom: First option evaluated becomes the default
   Fix: Evaluate all options before scoring any

3. CONFIRMATION BIAS
   Symptom: Seeking data that supports preferred option
   Fix: Assign a devil's advocate for each option

4. SUNK COST FALLACY
   Symptom: Sticking with an option because of past investment
   Fix: Evaluate options on future value only

5. RECENCY BIAS
   Symptom: Overweighting the last demo or reference call
   Fix: Standardize evaluation timing and criteria

6. GROUPTHINK
   Symptom: Team converges without genuine debate
   Fix: Independent scoring before group discussion

7. FEATURE COUNTING
   Symptom: Most features = best option (ignoring fit)
   Fix: Weight criteria by importance, not count

8. IGNORING STATUS QUO
   Symptom: Not comparing options against doing nothing
   Fix: Always include "do nothing" as Option D
```

## See Also

- [Business Strategy](../business-strategy/SKILL.md)
- [Product Management](../product-management/SKILL.md)
- [Risk Management](../risk-management/SKILL.md)
