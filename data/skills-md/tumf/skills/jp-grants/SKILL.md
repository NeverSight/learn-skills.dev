---
name: jp-grants
description: |
  Collect and answer questions about Japanese subsidies/grants (補助金・助成金) with up-to-date sources.
  Use when a user asks: which programs they qualify for, eligibility, deadlines, required documents,
  application steps, or where to find official calls for proposals and past award/adoption examples
  (e.g. J-Grants, METI/SME Agency, MHLW, prefectures/municipalities). Includes workflows and scripts
  for web search + structured extraction with citations. This skill is methodology-focused rather than
  program-specific: it provides reusable ways to discover and verify official information across many programs.
---

# jp-grants - Japan Subsidies / Grants (補助金・助成金)

Operate with a "freshness first" mindset: deadlines and rules change frequently. Prefer official sources (e.g. *.go.jp, *.lg.jp, jgrants-portal.go.jp). Always provide URLs and, when possible, short supporting quotes. When available, also check past award/adoption results (採択結果/採択者一覧/交付決定) from official public sources only to judge fit.

## Scope

- This skill is for reusable research workflow, not for maintaining a custom script per subsidy program.
- Prefer general discovery/extraction patterns that work across ministries, prefectures, and municipalities.
- Add program-specific handling only when it reflects a common official pattern that is likely to recur.

## Non-goals

- Do not build or maintain one-off scrapers for each individual subsidy program.
- Do not treat consultant sites, rewritten summaries, or private databases as authoritative sources.
- Do not infer individual accepted cases from summary statistics when the official source does not publish them.

## Operating rules

- Avoid hallucinating program details. If a field is unknown, say so and provide the official URL to verify.
- For past award/adoption examples, use only official public sources. Do not rely on consultant summaries, media rewrites, or private databases.
- Distinguish clearly between:
  - Subsidies/grants (補助金)
  - Employment-related support / allowances (助成金, often MHLW)
  - Loans/financing (融資) and tax incentives (税制) (not grants)
- Do not provide legal/tax advice; provide procedural guidance and point to official documents.

## Minimal intake (ask only if needed)

If the user question is underspecified, ask for only the 3-6 items that most affect eligibility:

1. Applicant type: individual / sole proprietor / SME corporation / NPO / school / other
2. Location: prefecture + city/ward (local programs are common)
3. Purpose: equipment (capex) / IT & DX / hiring & wages / R&D / export / energy saving / disaster recovery / other
4. Company size: employees, capital, sales (rough ranges are fine)
5. Timeline: when they want to apply / start the project
6. Industry constraints: manufacturing / retail / services / construction / healthcare / etc.

If the user refuses details, proceed with generic national programs and give a checklist to narrow down.

## Workflow: answer a user question

1. Restate constraints + assumptions (explicitly).
2. Collect candidate programs from official sources.
3. Choose the branch that matches the user need:
   - current program details -> find current official call pages and extract rules
   - award-result statistics -> find official result announcements and extract counts/breakdowns
   - individual accepted cases -> find official `採択者一覧`, `交付決定一覧`, or case-study pages/PDFs
4. Extract structured details for the chosen branch.
5. Shortlist 3-7 best fits; explain fit and disqualifiers using both current rules and past examples when available.
6. Provide next steps: what to read, what documents to prepare, and where to apply.

## Source strategy

- Primary: official government and local government sites
  - `*.go.jp` (METI, MHLW, SME Agency, etc.)
  - `*.lg.jp` (prefecture/municipality)
  - `jgrants-portal.go.jp` (J-Grants)
- Also look for official result pages/PDFs using terms such as `採択結果`, `採択者一覧`, `採択事例`, `交付決定`.
- For award-result checks, prioritize `chusho.meti.go.jp`, `meti.go.jp`, and `*.lg.jp` before J-Grants.
- Secondary: public support organizations (confirm against primary)
  - J-Net21, chambers of commerce, SME support centers
- Avoid: consultant blogs as an authority (may be outdated).
- For past award/adoption checks, do not use secondary or executing secretariat sites unless they are themselves the official public publisher for that result document.
- Note: `jgrants-portal.go.jp/robots.txt` currently disallows almost all crawling (`Disallow: /`, `Allow: /index.html`), so search/discovery may be incomplete there.

For a curated list of sources and query templates, read `jp-grants/references/sources.md`.

## Scripts (optional but recommended)

These scripts use Firecrawl for web search + structured extraction, plus a direct official fallback for award-result discovery.

- Find candidate pages: `jp-grants/scripts/find_candidates.py`
- Find + extract official award-result pages in one step: `jp-grants/scripts/extract_official_award_results.py`
- Extract official award-result fields: `jp-grants/scripts/extract_award_results.py`
- Extract individual official award cases: `jp-grants/scripts/extract_case_examples.py`
- Extract program fields: `jp-grants/scripts/extract_programs.py`

`find_candidates.py` flags:

- `--include-local`: include local government sites (`site:lg.jp`)
- `--include-executing-sites`: include common executing secretariat sites (discovery only)
- `--include-award-results`: also search for past award/adoption result pages and PDFs

## Practical decision tree

- Need current eligibility/deadlines/required docs -> use `find_candidates.py`, then `extract_programs.py`
- Need official result counts/breakdowns -> use `extract_official_award_results.py`
- Need individual accepted organizations/projects -> use official public `採択者一覧` / `交付決定一覧` / case-study pages, then `extract_case_examples.py`
- If official sources publish only statistics, state that individual cases are not publicly available in the checked source

## Output pattern (what to return to the user)

Provide a short list of candidates with consistent fields:

- Program name + administering body
- What it funds (eligible costs)
- Amount/rate (if specified)
- Key eligibility constraints
- Application window / deadline (with "as-of" date)
- Official URL (required)
- Past award/adoption examples from official public sources (if found) and what they imply about fit
- Why it fits / why it might not

Keep the list short. If there are many, offer a second pass after the user answers 1-2 narrowing questions.
