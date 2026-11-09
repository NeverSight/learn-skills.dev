---
name: resume-writer
description: Writes and rewrites high-impact resumes and CVs that pass ATS screening and win recruiter attention — translating raw work history into quantified, outcome-driven bullet points, choosing the right format, and tailoring to a target role. Use this skill when a user asks to "write my resume", "fix my CV", "make my resume ATS-friendly", "tailor my resume to this job", "turn my experience into bullet points", or wants help with a professional summary, skills section, or resume formatting.
license: MIT
---

# Resume Writer

## Overview
This skill turns a messy work history into a focused, quantified, ATS-passable resume tailored to a specific target role. It optimizes for two readers at once: the **applicant tracking system** (keyword match, parseable structure) and the **human recruiter** who skims for ~7 seconds before deciding.

**Keywords**: resume, CV, curriculum vitae, ATS, job application, bullet points, professional summary, work experience, achievements, cover, career change, recruiter.

## When to use vs. not
Use this to write, rewrite, restructure, or tailor a resume. This skill does not fabricate experience, invent metrics, or guarantee an interview — every claim must trace back to something the user actually did. When the user has no numbers, help them *estimate honestly* ("supported ~40 customers/week"), never invent precise figures.

## Inputs to gather first
Ask only for what's missing; infer the rest:
1. **Target role + a job description** (the single most important input — it drives keywords and emphasis).
2. **Work history**: companies, titles, dates, and what they actually did/achieved.
3. **Education, certifications, key skills/tools.**
4. **Seniority & career stage** (student/new-grad, IC, manager, executive, career-changer).
5. **Region/format norms** (US 1-page no-photo vs. EU CV vs. academic CV — see `references/format-by-region.md`).

## Workflow
1. **Pick the format.** Reverse-chronological by default. Use functional/hybrid only for career changers or large gaps — and warn that ATS and recruiters distrust purely functional resumes. See `references/format-by-region.md`.
2. **Mine the job description.** Extract the role's must-have keywords, tools, and outcomes. These become the vocabulary the resume must mirror (ATS matches on exact terms).
3. **Write the headline + summary.** A 1-line title and a 2–3 line summary stating who they are, their strongest proof, and what they're targeting. No "results-oriented team player" filler.
4. **Rewrite every bullet with the impact formula.** `Action verb + what you did + quantified result/context`. Lead with the outcome when it's strong. See `references/bullet-formulas.md` and the verb bank.
5. **Quantify relentlessly.** Money, %, time, scale, frequency, or rank. If no hard number exists, use scope ("across 3 teams", "for a 12k-user platform").
6. **Order by relevance, not just recency.** Within each role, put the bullets that match the target job first. Trim bullets older/irrelevant roles to 1–2 lines.
7. **Build the skills section** from real, demonstrated skills that also appear in the JD. Group them (Languages / Tools / Domains). Don't list skills you can't defend in an interview.
8. **Tighten for ATS.** Standard section headings, no tables/columns/text-boxes/images for the parsed version, real bullet characters, common fonts, `.docx` or text-based PDF. See `references/ats-rules.md`.
9. **Cut to length.** 1 page for <10 yrs experience, 2 pages otherwise (academic/EU CVs differ). Remove the objective, references-on-request, and anything pre-dating ~15 years unless pivotal.
10. **Proofread + tailor check.** Consistent tense (past for past roles, present for current), parallel structure, zero typos. End with a gap analysis: which JD requirements the resume still doesn't address, and how the user might.

## Decision framework
| If the candidate… | Then… |
| --- | --- |
| Has a linear career in one field | Reverse-chronological, lead with experience |
| Is a new grad / student | Education + projects + internships up top, skills prominent |
| Is changing careers | Hybrid: summary + transferable-skills block, reframe old bullets toward the new target |
| Has employment gaps | Use years not months, add a brief context line, lead with strongest content |
| Is senior/executive | Lead with scope, P&L, team size, strategic outcomes; 2 pages OK |

## Worked example
See `examples/before-after.md` for a vague bullet turned into a quantified, ATS-aligned one, plus a full summary rewrite.

## Best Practices
- **Tailor per application.** One generic resume loses to ten targeted ones. Mirror the JD's language.
- **Lead with outcomes, not duties.** "Cut onboarding time 40%" beats "responsible for onboarding."
- **One idea per bullet, 1–2 lines max.** Recruiters skim.
- **Strong verbs, no first person.** "Led," "shipped," "reduced" — never "I was responsible for."
- **Keep a master resume** with everything, then cut down per role.

## Common Pitfalls
- **Inventing or inflating metrics** — a single caught lie sinks the candidacy. Estimate honestly instead.
- **Duty-listing instead of achievement-showing.**
- **Fancy templates with columns/graphics** that ATS parsers scramble.
- **Buzzword soup** ("synergistic," "go-getter") with no evidence.
- **Same resume for every job** — no keyword match, no tailoring.
- **Typos and inconsistent tense/formatting** — instant credibility loss.
