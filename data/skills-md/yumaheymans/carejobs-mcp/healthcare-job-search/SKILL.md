---
name: healthcare-job-search
description: Find open US healthcare jobs (nursing, CNA, allied health, therapy, imaging, pharmacy, physicians and more) and the hourly pay employers post, using CareJobs.Now's free MCP server or its public JSON endpoints. Use when someone asks for healthcare or nursing jobs in a US place, what a healthcare job pays, or which hospitals are hiring.
license: MIT
---

# Healthcare job search (US)

CareJobs.Now reads the career sites of 258 US hospitals, health systems, clinic groups and care companies every day (170,000+ open jobs) and keeps the pay each employer posts. This skill answers job and pay questions from that data, and always gives the person a link where they can apply.

## When to use

- "Find night-shift ICU nurse jobs in Boston" / "CNA jobs near Austin with posted pay"
- "What do respiratory therapists get paid in Ohio?"
- "Which hospitals are hiring travel nurses in California?"
- Comparing posted pay between kinds of healthcare job or states

## Option 1: the MCP server (preferred)

Connect the hosted server once (no API key): `https://carejobs.now/api/mcp` (Streamable HTTP). In Claude Code: `claude mcp add --transport http carejobs https://carejobs.now/api/mcp`. That command adds the server to your Claude Code MCP configuration (remove it with `claude mcp remove carejobs`). Option 2 below needs no setup at all.

Then use its tools:

- `search_healthcare_jobs`: words (a unit, a shift, a town), kind of job, state, shift and pay filters. Returns title, employer, kind of job, pay, place and a job link. The pay is one of two things: the rate the posting itself states, or, when the posting states none, the typical range for that kind of job at that employer, which the server marks "(typical of ... at <employer>, measured from its open jobs; not a rate this posting states)". Results with no pay at all have none posted.
- `get_healthcare_pay`: posted hourly pay by kind of job and/or employer (median and typical range). It has no state filter.
- `get_healthcare_jobs_by_state`: open jobs and employers per state; with a state (and optionally a kind of job), that state's open jobs and the hourly pay its jobs post. Use it for pay in one state.
- `get_healthcare_job_market`, `list_healthcare_employers`, `get_healthcare_employer`: market size, the employers covered, and one employer's jobs and pay.

## Option 2: the public JSON endpoints (no MCP client needed)

- `GET https://carejobs.now/pay.json`: `pay_by_work_type[]` with `label`, `median`, `typical_low`, `typical_high` (USD per hour), `rate_samples`, `open_total`.
- `GET https://carejobs.now/roles.json`: `totals` and `open_by_work_type[]` (aggregate open-job counts per kind of job and per employer, not individual postings; list openings with the MCP job search).
- Both are CC BY 4.0 (separate from the MIT licence of this skill), CORS-enabled and refreshed daily. Cite "CareJobs.Now" with a link to https://carejobs.now/data and the file's `temporal_coverage` date.

## How to answer

1. Pin down the kind of job, the place (state or town) and any shift or pay limits. Ask only if the request is too vague to search.
2. Search, then list the best matches with employer, place, pay and the job link. Keep the two kinds of pay apart: call a rate the posting states "posted pay", and call a range the server marks as typical "typical for this kind of job at <employer>, not stated in this posting". Never present a typical range as the posting's own pay. Say "pay not posted" when there is none.
3. For pay questions, give the median and typical range and say it is what employers post on open jobs, before shift differentials and bonuses, not what everyone earns.
4. Never invent jobs or pay. If nothing matches, say so and widen the search (nearby state, related kind of job).
5. The kind of job is read from each posting's title. If a result's title plainly names another kind of job than the one asked for, leave it out of the answer.

Source and method: https://carejobs.now/data
