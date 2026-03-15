---
name: us-program-research
description: This skill should be used when the user needs structured research and ranking of US academic programs (PhD, Master
license: MIT
---

# US Academic Program Research — Complete Workflow

## Purpose

Run structured research on US academic programs with credential analysis, parallel discovery, adaptive scorecards, and generation of an actionable application plan in a deliverable format.

## When to Use

Use this skill when the task requires:
- Selecting and ranking programs (PhD, Master's, or Bachelor's) in the US
- Detailed comparison of curriculum, costs, and admission requirements
- Application strategy based on profile, budget, and timeline
- A final consolidated document for decision-making and execution

## Progress Tracking

Display progress before each research phase:

```
[███░░░░░░░░░░░░░░░░░] 15% — Phase 0: Program Type Detection & Input Collection
[██████░░░░░░░░░░░░░░] 30% — Phase 1: Profile & Credential Analysis
[█████████░░░░░░░░░░░] 45% — Phase 2: Parallel Discovery (4 subagents)
[████████████░░░░░░░░] 60% — Phase 3: Parallel Deep Research (4 subagents)
[███████████████░░░░░] 75% — Phase 4: Adaptive Scorecards & Ranking
[█████████████████░░░] 85% — Phase 5: Document Generation
[████████████████████] 100% — Phase 6: Inline Report & Recommendations
```

## Workflow

Follow the phases defined below in sequence, maintaining source traceability and separating facts from inferences.

Personalized research on US academic programs (PhD, Master's MS/MBA/MPS, or Bachelor's).
Analyzes the candidate's profile, runs parallel searches via subagents, identifies hidden gems,
applies an adaptive scorecard, and generates a complete ACTION_PLAN.md with rankings, curricula, costs,
and a step-by-step checklist.

**Output language:** Portuguese (matches user research context). **Queries/subagents:** English (required for search quality).

---

## Execution Instructions

1. PHASE 0 — detect program type (FIRST QUESTION)
2. PHASE 0B — collect all inputs before researching
3. PHASE 2 — launch 4 subagents in ONE message (true parallelism)
4. PHASE 3 — launch 4 deep-research subagents in ONE message
5. PHASE 4 — apply adaptive scorecard after all research is complete
6. PHASE 5 — generate full document and save
7. PHASE 6 — present inline report to user

> CRITICAL: All search queries and subagent prompts MUST be in English.

---

## PHASE 0 — Program Type Detection

Use AskUserQuestion with:
**"What type of US academic program are you looking for?"**

Options:
1. **PhD / Doctorate** — 4–7 years of research. Usually fully-funded (stipend + tuition).
2. **Master's** — MS, MBA, MPS, MEng (1.5–3 years). Executive, technical, online or in-person.
3. **Bachelor's / Undergraduate** — First or second degree (BS, BA). 2–4 years.

The entire workflow adapts to this answer.

---

## PHASE 0B — Input Collection (2 rounds of AskUserQuestion)

### Round A — Personal profile (all types, max 4 questions):
1. Full name + email
2. Country of origin + language(s) of diplomas
3. Highest current degree: institution, diploma type, GPA/grade (e.g., "8.1/10")
4. Desired field of study (e.g., Computer Science, Business Analytics, AI, Finance...)

### Round B — Logistics and preferences (max 4 questions):
5. Target city/state in the US (or "open to any location")
6. Preferred format: in-person / 100% online / hybrid / no preference
7. Total budget: under $20k / $20–50k / $50–80k / over $80k / seeking funding
8. Desired start date: 2026 / 2027 / 2028 / flexible

Additional type-specific question:
- **PhD:** Specific research area? Known advisors? Funded programs only?
- **Master's:** Current role/level (Junior/Manager/Director/VP/C-Level)? Will you work during the program?
- **Bachelor's:** First or second degree? Transferable credits? Large/small campus preference?

Optional inputs (offer, do not require): CV, academic transcripts, prior executive courses,
US immigration status (Green Card / F1-OPT / H1-B / other).

---

## PHASE 1 — Profile & Credential Analysis

Determine foreign degree equivalency and evaluation strategy BEFORE scoring any program.

**Action:** Consult `references/credential-analysis.md` for:
- Degree equivalency table by country (includes risk for Brazilian Tecnólogo degree)
- WES vs ECE comparison by program type
- WES ICAP step-by-step logistics (8 steps + 2 scenarios: favorable vs unfavorable result)
- Anti-downgrading analysis for VP/C-Level candidates (Master's only)
- Advisor fit analysis for PhD + contact email template
- In-state tuition logic (Green Card + 12-month domicile = eligible)

> Brazilian Tecnólogo = HIGH RISK. WES may evaluate as Associate's instead of Bachelor's.
> Recommend institutional letter + ECE as second opinion if WES result is unfavorable.

---

## PHASE 2 — Parallel Discovery (4 Subagents)

**CRITICAL: Launch all 4 subagents in ONE SINGLE message (Task tool × 4 simultaneous).**

Divide research among 4 subagents with `subagent_type="general-purpose"`:

| Subagent | Focus                        | Minimum Programs |
|:--------:|:-----------------------------|:----------------:|
| A        | Regional / Local In-Person   | 4                |
| B        | National Online / Brand Equity | 5              |
| C        | Hidden Gems (low cost)       | 3                |
| D        | Reference Rankings           | Top 20 context   |

**Action:** Consult `references/subagent-prompts.md` for the full prompts (in English)
for each subagent, including all fields to collect and search queries.

**After all 4 subagents complete:**
- Deduplicate programs (same school may appear in multiple subagents)
- Verify accreditation: AACSB (business), ABET (engineering) — absence penalizes Brand Equity
- For PhD: verify if fully-funded vs self-funded
- Classify into groups: 1 (primary in-person), 1.5 (online brand equity), 2 (technical/deprioritized)
- Target: 12–20 unique programs for Phase 3

---

## PHASE 3 — Parallel Deep Research (4 Subagents)

**CRITICAL: Split the 12–20 programs into 4 groups (3–5 each) and launch in ONE single message.**

For each program, collect: full curriculum, verified cost on official website, student reviews
(Niche/Reddit/GMAT Club/GradCafe), admission requirements (GMAT/TOEFL/letters/deadline), alumni network.

**Action:** Consult `references/subagent-prompts.md` for the full deep research template
(section "Deep Research Template") with all queries in English.

---

## PHASE 4 — Adaptive Scorecards

**Action:** Consult `references/scorecards.md` for the complete scorecards.

### Scorecard Selection by Program Type:

| Type       | Scorecard  | Key Criteria                                    |
|:----------:|:----------:|:------------------------------------------------|
| Master's   | Scorecard A| Brand + Exec Readiness + Flexibility + Network + ROI + Satisfaction |
| PhD        | Scorecard B| Research Reputation + Advisor Fit + Funding + Placement + Satisfaction |
| Bachelor's | Scorecard C| Brand + Career Launch + ROI + Campus Life + Satisfaction |

### Master's — Adaptive Weights by Candidate Level:

| Criterion             | EXECUTIVE | SENIOR | STANDARD | CAREER_LAUNCH | OPT_CRITICAL |
|:----------------------|:---------:|:------:|:--------:|:-------------:|:------------:|
| Brand Equity          |    25     |   23   |    23    |      23       |     22       |
| Executive Readiness*  |    25     |   22   |    18    |      10       |     20       |
| Flexibility           |    16     |   16   |    14    |      12       |     16       |
| Network Quality       |    15     |   15   |    15    |      15       |     12       |
| ROI / Cost-Benefit    |    12     |   14   |    16    |      20       |     14       |
| Student Satisfaction  |    10     |   10   |    10    |      10       |     10       |
| STEM Designation      |     0     |    0   |     0    |       0       |      6       |

*For VP/C-Level = "Executive Readiness". For non-executives = "Career Launch Potential".

### Tier Classification:

| Tier    | Score  | Label              | Action           |
|:-------:|:------:|:-------------------|:-----------------|
| Top 5   | ≥ 80   | Highest Priority   | MUST APPLY       |
| Tier 2  | 70–79  | If Budget Allows   | IF BUDGET ALLOWS |
| Tier 3  | 55–69  | Backup             | BACKUP ONLY      |
| Tier 4  | < 55   | Avoid              | AVOID            |

**💎 Hidden Gem** = Score ≥ 70 AND Cost ≤ 50% of budget AND Satisfaction ≥ 8.0/10

---

## PHASE 5 — Document Generation

Save as: `{CANDIDATE_NAME}_US_PROGRAM_ACTION_PLAN.md` (in current directory).

**Action:** Consult `references/action-plan-template.md` for the full document template
in Portuguese, including all sections, ~30 aligned tables, and the Table Formatting Policy.

**Required sections in the generated document:**
General Status → Priority Next Actions → Phase 1 (WES/ECE) → Phase 2 (Tests) →
Phase 3 (Contact) → Phase 4 (Submission) → Evaluators → Selected Programs by Tier →
Adaptive Scorecard + Full Ranking → Curriculum Comparison → Detailed Curricula →
Cost Comparison → Admission Comparison → Why Each Program → Document Inventory → Notes.

---

## PHASE 6 — Inline Report

Present to the user in chat (in Portuguese) after saving the file:

**Block 1 — Candidate Profile** (max 5 lines): type, field, role/education, estimated GPA, immigration status.

**Block 2 — Top 5 Recommendations** (compact table):
`| Rank | Program | Score | Cost | Highlight |`

**Block 3 — 💎 Hidden Gems** (if identified): score ≥ 70 + low cost + satisfaction ≥ 8.0.

**Block 4 — ⚠️ Alerts**: programs without reviews (red flag), daytime-only for executives,
advisors without recent publications (PhD), borderline degree → WES urgent.

**Block 5 — URGENT Next Action**: "What to do TODAY" — usually: start WES/ECE or contact advisor.

**Block 6 — Generated File**: `✅ Document saved: {NAME}_US_PROGRAM_ACTION_PLAN.md ({N} lines, {N} tables)`

---

## Additional Resources

### Reference Files

Consult as needed during execution:

- **`references/credential-analysis.md`** — Degree equivalencies, full WES/ECE logistics,
  anti-downgrading, advisor fit (PhD), in-state tuition logic
- **`references/scorecards.md`** — Complete Scorecards A/B/C with detailed rubrics, ROI formula
  with numeric example, tier thresholds, and hidden gem definition
- **`references/subagent-prompts.md`** — Complete prompts (in English) for the 8 subagents:
  4 discovery (Phases 2A/B/C/D) and deep research template (Phase 3)
- **`references/action-plan-template.md`** — Complete ACTION_PLAN.md template in Portuguese
  with all sections and aligned tables
- **`references/research-sources.md`** — Mandatory research sources and universal red flags
  by program type

## Critical Rules

- All research queries and subagent prompts must be in English.
- Do not skip credential analysis before scoring/ranking.
- Do not present a final recommendation without citing sources and criteria.
- Clearly differentiate confirmed data, assumptions, and recommendations.

## Error Handling

| Error | Likely Cause | Action |
|-------|-------------|--------|
| Program URL unavailable (404) | University program page moved or removed | Note inaccessibility; use cached data or alternative sources for that program |
| No funding data found | Program doesn't publish funding info publicly | Mark as "funding data unavailable"; recommend user contact program directly |
| Insufficient programs match criteria | Filters too restrictive (budget, location, ranking) | Relax constraints and explain tradeoffs to user |
| Budget eliminates all options | Target budget below typical program tuition | Inform user of realistic cost ranges; suggest funded programs or assistantships |
| Credential gap detected | User credentials unlikely to meet minimum requirements | Flag disqualifiers; recommend strengthening credentials before applying |
| WebFetch blocked by university site | Bot-blocking or requires login | Use alternate sources (US News, Grad Cafe, QS rankings) for that program's data |

## Example Usage

1. "Rank MS in Data Science programs in the US with a budget of USD 50k."
2. "Compare funded PhD options in Computer Science focused on distributed systems."
3. "Build an application plan for an MBA starting in 2027."
