---
name: job-application-operator
description: Assist Arthur with human-reviewed job applications using local private profile data, document manifests, browser automation, and strict stop-before-submit rules.
---

# Job Application Operator

## Contract

Use this skill when Arthur wants to apply to a job, inspect an application form, prepare documents, fill application fields, or update learned application answers.

This skill is for supervised job applications, not blind auto-apply.

## Private Files

Load private data from:

- `~/.config/AgentDesk/personal-profile.yaml`
- `~/.config/AgentDesk/job-applications/profile.yaml`
- `~/.config/AgentDesk/job-applications/document-manifest.yaml`
- `~/.config/AgentDesk/job-applications/field-answers.yaml`
- `~/.config/AgentDesk/job-applications/application-log.jsonl`

Never commit real private profile data or private PDFs to Git.

## Hard Rules

- Never submit an application without Arthur explicitly confirming in the current session.
- Never bypass CAPTCHA, MFA, bot checks, login walls, or account creation.
- Never store passwords.
- Never use stealth, proxies, or CAPTCHA-solving services.
- Stop on salary, work authorization, visa, demographic, disability, military/veteran, legal, relocation, notice-period, or motivation questions unless a policy exists and still ask before final submission.
- Upload only documents that match the field label.
- Stop before the final submit button.
- Do not mention Russian citizenship unless the form explicitly asks for all citizenships or nationalities.
- Skip or flag defense/export-control/military roles if citizenship restrictions create a likely blocker.
- Fully remote roles are manual-review only because Arthur prefers hybrid or office-based work.

## Preferred Browser Backend

Codex Chrome extension is not assumed to be available.

Use available browser automation in this order:

1. Codex Desktop direct browser/computer-use if available.
2. `agent-browser` CLI.
3. Playwright MCP.
4. `browser-harness` only as fallback.

## Application Loop

1. Open exactly one job application URL.
2. Identify platform:
   - Ashby
   - Lever
   - Personio
   - Greenhouse
   - Workday
   - YC
   - custom
   - unknown
3. Create a field inventory:
   - label
   - field type
   - required/optional
   - current value
   - select options
   - file upload fields
   - sensitive fields
   - unknown fields
4. Fill only safe high-confidence fields.
5. Ask Arthur for unknown or sensitive fields.
6. Save reusable answers to `field-answers.yaml`.
7. Upload files using `document-manifest.yaml`.
8. Stop at final review/submit.
9. Log result to `application-log.jsonl`.

## Known Profile Policies

### Location

Preferred:

- Munich
- Augsburg

Acceptable:

- Berlin
- Germany

Munich is first choice. Augsburg is even better. Berlin is acceptable because it has a strong job market. Other locations require review.

### Work Mode

Arthur prefers hybrid or office-based work with at least 2 office days per week. Some home office is a benefit. Fully remote roles are not preferred and require manual review.

### Salary

For relevant AI / FDE / AI Solutions Engineer applications, salary expectation anchor is EUR 85k-90k gross annual base.

Do not auto-submit salary fields. If a field requires one number, ask Arthur before using 90000.

### Work Authorization

Arthur has German citizenship. For Germany/EU work authorization questions, answer yes. For Germany/EU visa sponsorship needed, answer no.

Do not mention Russian citizenship unless explicitly asked.

### Languages

German: native or near-native.
Russian: native or near-native.
English: fluent, TOEFL 109/120.

### Links

LinkedIn:
`https://www.linkedin.com/in/arthurzakirov`

GitHub:
`https://github.com/ArthurZakirov`

Portfolio:
`https://arthur-zakirov.vercel.app/`

Skip Twitter/X and Google Scholar unless required.

## Document Upload Policy

Use CV only for:

- Resume
- CV
- Lebenslauf

Use degree document only for:

- Degree
- Diploma
- Certificate
- Abschluss
- Zeugnis
- Education proof

Use transcript only for:

- Transcript
- Grades
- Notenspiegel
- Academic record

Use reference letters only for:

- References
- Recommendation
- Arbeitszeugnis
- Internship certificate

Use supporting bundle only for:

- Additional documents
- Other documents
- Supporting documents
- Weitere Unterlagen

Do not upload all documents by default.

## Output After Each Application

Return:

- application URL
- platform
- fields filled
- fields skipped
- unknown questions
- sensitive questions
- documents uploaded
- blockers
- whether final submit is ready
- next action for Arthur
