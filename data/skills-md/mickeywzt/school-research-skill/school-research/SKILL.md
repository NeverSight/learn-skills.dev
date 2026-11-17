---
name: school-research
description: Create deep research profiles and readable PDF reports for one specific school, college, university, boarding school, international school, or academic program. Use when the user names a particular school and asks for school research, admissions requirements, deadline checks, tuition or scholarship research, program fit, campus or student-life research, application strategy, risks, source-backed school briefs, a one-school due-diligence report, or a polished visual PDF.
---

# School Research

## Overview

Use this skill to turn one named school into an evidence-backed research profile for application planning. Prioritize current official sources, separate verified facts from interpretation, and produce a practical single-school brief or polished PDF report with risks and next actions.

## Workflow

1. Clarify the research target.
   - Confirm the exact school name, campus, country, student level, intended major or curriculum, applicant status, entry year, and application route.
   - Disambiguate similarly named schools before researching.
   - If student context is missing, still research the school generally and mark applicant-fit judgments as conditional.

2. Build a source plan.
   - Use current web research for admissions requirements, deadlines, tuition, scholarships, rankings, policy, and program availability unless the user explicitly says not to browse.
   - Prefer official school, admissions, department, financial aid, international student, and Common Data Set pages.
   - Use rankings, forums, blogs, consultants, and student reviews only as secondary context.
   - Record accessed date for unstable facts.
   - For deep research, cover the minimum source set in `references/research-standards.md` before writing the final report. If any source category cannot be found, state that gap.

3. Extract decision facts.
   - Confirm program fit, admissions route, required curriculum, standardized tests, English requirements, GPA or grade expectations, recommendation letters, essays, interviews, portfolios, deadlines, tuition, aid, housing, student outcomes, and application platform.
   - Mark facts as `verified`, `inferred`, or `unclear`.
   - Keep direct quotes short and cite source links.

4. Evaluate fit.
   - Separate academic fit, admissions competitiveness, financial fit, environment fit, and strategic value.
   - Use reach/target/likely only if the user provides enough applicant context; otherwise describe selectivity and required evidence.
   - Avoid deterministic admissions claims. Phrase estimates as judgments based on available evidence.

5. Produce the requested artifact.
   - For quick research, answer with a concise school profile and action list.
   - For deeper research, produce a full single-school due-diligence report, source log, uncertainties, and next actions.
   - When the user wants a polished deliverable, produce a PDF report. Use `references/pdf-report-design.md` for structure and `scripts/render_school_pdf.py` when a deterministic PDF renderer is useful.
   - If the user writes in Chinese, output in Chinese unless they request otherwise. Preserve official English school and program names.

## Output Standards

- Lead with the decision-relevant conclusion before details.
- Cite sources for each school-specific factual claim.
- Include concrete dates for deadlines and accessed dates for web facts.
- Distinguish current facts from historical data or reputation signals.
- Flag risks such as outdated pages, country-specific requirements, unavailable aid for international students, or unclear test policies.
- Do not call the work "deep research" unless admissions, program, cost/aid, international/applicant support, student life, outcomes, and official data/profile sources have all been attempted.
- For PDF deliverables, include a cover, decision summary, visual fit scorecard, admissions checklist, timeline, risk register, source log, and page numbers.
- For PDF deliverables, render or otherwise inspect the final PDF before delivery when local PDF tooling is available. Check for clipped text, unreadable glyphs, overlapping tables, missing citations, and broken page flow.
- End with the next 3-5 actions the student should take.

## Resources

- Read `references/research-standards.md` when planning source strategy or handling uncertain admissions facts.
- Read `references/output-templates.md` when creating a school profile, due-diligence report, application checklist, or source log.
- Read `references/pdf-report-design.md` when creating a polished PDF deliverable.
- Use `scripts/render_school_pdf.py` to generate a readable ReportLab PDF from structured JSON.
- Use `assets/single_school_profile.csv` as a starter table when the user wants a spreadsheet-style one-school research file.

## Common Requests

- "Research NYU for an international student applying to economics."
- "Make a deep school profile for Phillips Exeter Academy."
- "Check whether USC still requires SAT/ACT for 2027 entry."
- "Research the University of Toronto computer science application requirements."
- "Help me decide whether this one school is worth applying to."
- "Make the final school research report as a polished PDF."
