---
name: resume-audit
description: Scores a resume's structure, quantified impact, and ATS keyword coverage against a job description. Reads markdown or plain text (convert PDF/docx first with doc-reader) and checks contact info, standard sections, quantified bullet ratio, action-verb openers, weak phrases ("responsible for"), and — given a JD — which required keywords are missing. Offline, deterministic, no LLM needed.
when_to_use: Before submitting a resume, when tailoring to a specific job posting, or when reviewing someone else's resume as a hiring manager or mentor. NOT a resume writer or a guarantee of an interview — it scores the mechanical signals recruiters and ATS software filter on.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [resume, career, ats, hr, job-search]
---

# Resume Audit

Recruiters and ATS software filter on mechanical signals before a human reads
a word. This scores those signals before you hit submit.

## Commands

```bash
python3 scripts/resume_audit.py resume.md
python3 scripts/resume_audit.py resume.md --jd job-posting.txt --json
python3 scripts/resume_audit.py resume.md --min-bullet-ratio 0.5
```

## Checks

| Check | Pass condition |
|---|---|
| `contact_info` | email, phone, or profile URL present |
| `sections` | experience + skills sections detected |
| `quantified_bullets` | ratio >= `--min-bullet-ratio` (default 0.4) |
| `action_verbs` | >=50% of bullets open with led/built/shipped/grew/... |
| `weak_phrases` | zero "responsible for" / "worked on" / "helped with" |

With `--jd`, reports ATS coverage: which JD keywords appear in the resume,
which tech keywords are missing, and a strong/partial/weak verdict.

## Workflow

1. Convert the resume: `doc-reader resume.pdf > resume.md`
2. Audit: `resume_audit.py resume.md --jd target-role.txt`
3. Fix the failing checks — add numbers to bullets, replace weak phrases,
   weave missing tech keywords into real accomplishments (never keyword-stuff).

## Pairs with

`doc-reader` (format conversion), `nbj-write-clearly` (making the prose land
after the structure passes).
