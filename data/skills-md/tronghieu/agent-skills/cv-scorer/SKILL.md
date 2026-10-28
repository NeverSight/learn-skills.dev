---
name: cv-scorer
description: "Score candidate CVs on a 100-point scale against a Job Description. Use this skill when the user wants to evaluate, score, rank, or screen candidate CVs/resumes against a JD. Also trigger when the user mentions 'review CV', 'screen resume', 'rate candidates', 'shortlist', or any context involving matching resumes to job requirements."
---

# CV Scorer — Candidate CV Evaluation

This skill evaluates how well a candidate's CV matches a specific Job Description (JD), producing a structured score out of 100.

## Workflow

### Step 1: Identify Inputs

Two inputs are required:
- **Job Description (JD)**: The job posting with requirements, qualifications, and responsibilities
- **CV(s)**: One or more candidate CVs (markdown, text, or PDF)

If the user hasn't provided a JD, ask for it. If the JD is already available in context (e.g., a file on Drive or in the project directory), read it directly.

**Reading PDF files:** Use the `/pdf` skill to extract text from PDF CVs — it handles multi-page documents and formatted layouts reliably.

### Step 2: Analyze the JD

Before scoring, extract from the JD:
- Must-have skills vs nice-to-have skills
- Experience requirements (years, seniority level, domain)
- Education requirements
- Special requirements (languages, certifications, travel, etc.)

### Step 3: Score Against Rubric

Score each CV across 5 criteria using `references/scoring-rubric.md`:

| Criterion | Weight | Max Points |
|-----------|--------|------------|
| JD Matching | ×3 | 30 |
| Work Experience | ×2.5 | 25 |
| Project & Impact | ×1.5 | 15 |
| Education | ×1.5 | 15 |
| CV Quality | ×1.5 | 15 |
| **Total** | | **100** |

### Step 4: Output

Output JSON for each CV using the format in `references/output-format.md`.

**Recommendation thresholds:**
- **Recommend** (≥ 70): Invite for interview
- **Maybe** (50–69): Consider if candidate pool is thin
- **Pass** (< 50): Not a fit

### Step 5: Batch Processing

When scoring multiple CVs:
1. Score each CV independently — no cross-comparison during scoring (safe to parallelize)
2. After all CVs are scored, produce a summary ranking (highest to lowest)
3. Use the batch summary format in `references/output-format.md`

## Scoring Principles

- **Objective**: Score based on facts in the CV, avoid over-inference
- **Fair**: Apply the same standard consistently across all candidates
- **Red flag detection**: Repetitive content, inflated metrics, unexplained career gaps, contradictory information
- **Output language**: Match the user's language (respond in the same language the user is using)
- **No bias**: Do not evaluate based on age, gender, ethnicity, or personal factors unrelated to the job
