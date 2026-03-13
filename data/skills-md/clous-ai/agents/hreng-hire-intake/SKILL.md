---
name: hreng-hire-intake
description: Use when the user wants to start or refine an engineering hiring process and needs a structured, legally-aware intake document for a new or replacement role.
version: 1.0.0
license: MIT
---

# HR Engineering Hiring Intake

## Overview

Transform unstructured hiring needs into comprehensive, structured intake documents that define role context, requirements, compensation, and timeline while respecting legal and equity constraints.

## When to Use

Use this skill when:
- Starting a **new engineering role requisition**.
- Replacing a **departing team member** (backfill).
- Planning **future headcount** for upcoming quarters.
- Converting a **contractor role to full-time**.
- Cleaning up **ad-hoc hiring** into a documented intake process.

## Inputs Required

- Role title and level.
- Team, reporting line, and location requirements.
- Business context and urgency.
- Must-have and nice-to-have requirements.
- Compensation constraints (if any) and pay band information.

## Outputs Produced

- A **structured intake JSON** matching `templates/intake-template.json` or `templates/intake-minimal.json`.
- A clear **checklist of open questions** if information is missing.

## Tooling Rule

- If MCP tools are available, prefer them for HRIS or employee data lookups.
- Use scripts to validate intake and detect biased language before finalizing.

## Core Process

### 1. Gather Role Context

Clarify **why this role exists** and how it fits:

**Role identity:**
- Job title (use standard titles: “Senior Backend Engineer”, not “Code Ninja”).
- Team and department.
- Reporting structure (manager, skip-level where relevant).
- Location requirements (remote, hybrid, specific office, time zone constraints).

**Business context:**
- Why is this role needed? (new headcount, backfill, growth, experiment).
- What problem does this role solve?
- What happens if the role remains unfilled for 3–6 months?
- Target start date and urgency (critical/high/medium/low).

**Team structure:**
- Current team size and level mix.
- Team distribution (locations, time zones).
- Related roles that frequently interact with this position.
- Expected team/org evolution over the next 12–24 months.

### 2. Define Requirements

Create clear, **legally-aware** requirements:

**Must-have requirements (non-negotiable):**
- Technical skills with proficiency levels (e.g., “production experience with Python and Postgres”).
- Domain expertise (e.g., “distributed systems”, “data platforms”).
- Behavioral competencies (e.g., “can lead cross-functional projects”).
- Legal requirements (e.g., specific certifications, work authorization) where applicable.

**Nice-to-have requirements (differentiators):**
- Additional technical skills or stacks.
- Relevant industry or product experience.
- Tooling familiarity (observability stack, infrastructure-as-code).
- Advanced degrees/certifications if they materially change expectations.

**Legal/compliance checks:**
- Avoid any mention of **protected classes** (age, race, gender, etc.).
- Use years of experience as **guidance**, not strict filters (and validate with `references/legal-compliance.md`).
- Focus on **skills, outcomes, and responsibilities**, not demographics.

### 3. Map Competencies

Define what success looks like across competency areas:

**Technical competency (typically 60–70%):**
- Core technical skills required.
- Complexity and autonomy of technical problems.
- Expected design and architectural responsibilities.

**Leadership competency (typically 10–30%):**
- Mentoring expectations.
- Technical leadership or people management scope.
- Expected influence beyond the immediate team.

**Collaboration competency (typically 10–20%):**
- Cross-functional collaboration needs (PM, design, data, GTM).
- Communication expectations.
- Stakeholder management complexity.

Ensure weights across competencies sum to **1.0** (or 100%).

### 4. Define Compensation

Design competitive, equitable compensation within constraints:

**Base salary range:**
- Use `references/compensation-research.md` to anchor to market data.
- Consider level, location, funding stage, and market conditions.
- Use a **15–25% spread** (e.g., `$180k–220k`) and document why.

**Equity/stock options:**
- Typical grant bands for level and location.
- Vesting schedule (often 4-year with 1-year cliff).
- Refresh policy assumptions.

**Total compensation:**
- Combine base, equity, and material benefits.
- Note whether the role is **market rate, below, or above** and why.

**Legal considerations:**
- Pay transparency laws (e.g., CA, CO, NY, WA) – make sure ranges are publishable.
- Internal equity vs. existing similar roles.
- Documentation of rationale for future audits.

### 5. Plan Timeline

Create a realistic hiring timeline based on **capacity and urgency**:

**Key milestones:**
- Intake approval date.
- Job description completion.
- Sourcing start date.
- Interview loop availability windows.
- Target offer date and start date.

**Interview capacity:**
- Number of interviewers and slots per week.
- Expected weeks from first screen to offer.
- Buffer for scheduling delays and decision-making.

**Urgency assessment:**
- Critical role (blocks major initiatives) → may require compressed process and trade-offs.
- Important but not blocking → standard process.
- Long-term pipeline → slower process with more emphasis on quality signals.

### 6. Generate Structured Output

Produce JSON intake document conforming to the schema in `templates/intake-template.json`:

```json
{
  "role": {
    "title": "string",
    "level": "string (Junior/Mid/Senior/Staff/Principal)",
    "team": "string",
    "department": "string",
    "reports_to": "string",
    "location": "string",
    "employment_type": "string (Full-time/Contract/Part-time)"
  },
  "business_context": {
    "role_type": "string (new_headcount/backfill/conversion)",
    "business_need": "string",
    "impact_if_unfilled": "string",
    "urgency": "string (critical/high/medium/low)"
  },
  "requirements": {
    "must_have": ["array of strings"],
    "nice_to_have": ["array of strings"],
    "years_experience": "string (e.g., '5-8 years')",
    "education": "string or null"
  },
  "competencies": {
    "technical": {
      "weight": 0.70,
      "description": "string",
      "key_skills": ["array"]
    },
    "leadership": {
      "weight": 0.20,
      "description": "string",
      "expectations": ["array"]
    },
    "collaboration": {
      "weight": 0.10,
      "description": "string",
      "expectations": ["array"]
    }
  },
  "compensation": {
    "base_range": "string (e.g., '$180k-220k')",
    "equity_range": "string",
    "total_comp_target": "string",
    "market_positioning": "string (market-rate/below/above)",
    "rationale": "string"
  },
  "timeline": {
    "target_start_date": "YYYY-MM-DD",
    "intake_approval_date": "YYYY-MM-DD",
    "sourcing_start_date": "YYYY-MM-DD",
    "interview_slots_per_week": 5,
    "estimated_weeks_to_offer": 4
  },
  "metadata": {
    "created_date": "YYYY-MM-DD",
    "created_by": "string",
    "approved_by": "string or null",
    "version": "1.0"
  }
}
```

Save output to `intake-{role-title}-{date}.json`.

### 7. Validate and Review

Run validation checks using **`scripts/validate-hreng-hire-intake.py`** (canonical; `validate-intake.py` is a legacy alias):

```bash
python scripts/validate-hreng-hire-intake.py intake-senior-backend-2026-01-22.json
```

Validation checks:
- ✓ Schema compliance.
- ✓ No protected class language.
- ✓ Competency weights sum to 1.0.
- ✓ Compensation range is reasonable (15–25% spread).
- ✓ Timeline is realistic for interview capacity.
- ✓ All required fields populated.

Review checklist:
- [ ] Role title uses industry-standard terminology.
- [ ] Requirements focus on skills/outcomes, not demographics.
- [ ] Compensation is competitive and internally equitable.
- [ ] Timeline accounts for interview capacity and decision-making.
- [ ] Business need is clearly articulated.
- [ ] Approval chain is documented.

## Using Supporting Resources

### Templates

- **`templates/intake-template.json`** – Complete schema with examples.
- **`templates/intake-minimal.json`** – Minimal required fields for quick intake.

### References

- **`references/legal-compliance.md`** – EEOC guidelines, state laws, protected classes.
- **`references/compensation-research.md`** – Market data sources, benchmarking methodology (stub: expand with your sources).
- **`references/competency-frameworks.md`** – Competency definitions by level (stub: link to ladder or HR docs).

### Scripts

- **`scripts/validate-hreng-hire-intake.py`** – Schema and compliance validation (canonical).
- **`scripts/validate-intake.py`** – Legacy alias for the above.
- **`scripts/analyze-requirements.py`** – Detect biased or exclusionary language.

## Example Workflow

User request: “We need to hire a senior backend engineer for the platform team.”

High-level response steps:
1. Ask clarifying questions about role context, urgency, and team structure.
2. Gather must-have vs. nice-to-have requirements.
3. Define competency expectations and weights.
4. Research compensation ranges for level and location.
5. Plan a realistic timeline based on interview capacity.
6. Generate the structured JSON intake document.
7. Run validation scripts and summarize any issues or risks.
8. Present the intake JSON and recommend next steps (JD, sourcing, interview loop).

## Next Steps After Intake

Once intake is complete:
1. If you need sourcing strategy or interview loop design, run the `hreng-hire-eval` / hiring agents with this intake document.
2. Confirm intake completeness before moving to offer and onboarding planning.
3. Create a job description directly from the intake fields.
4. Get intake approved by hiring manager and HR/legal.

## Legal Disclaimer

This skill provides guidance based on common best practices and legal frameworks; it is **not** legal advice. Always consult HR and legal counsel before finalizing hiring decisions, especially regarding:
- Protected class compliance.
- Pay transparency requirements.
- Offer letter language.
- Background check policies.

Jurisdictions differ; see `references/legal-compliance.md` for jurisdiction-specific considerations.