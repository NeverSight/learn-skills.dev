---
name: adk-discovery
description: >-
  Find where AI would pay off in a business and pick the first use case,
  before any system is designed: with a rough area in mind, locate where the
  current journey breaks, choose the first workflow to improve and the
  business outcome to measure with its baseline; with no use case at all, go
  from what the business does and the KPIs it watches to the processes that
  drive them and the opportunities in them. Every opportunity gets a
  technology fit (agent, single LLM call, classical machine learning, rules
  or scripting, or a process change) and the portfolio is ranked. Ends with
  a discovery brief and the prompt for adk-system-designer. Do not activate
  when the use case and its measure are already chosen (adk-system-designer),
  for a change to an existing agent (adk-engineer), for market or competitor
  research, or to present results (adk-presenter).
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "cross-cutting"
  sources-reviewed: "2026-10-15"
  verified-against: "not applicable: business discovery; runs no ADK code"
  version: "2026.10.28"
---

# ADK discovery

Turn "we want AI" into one workflow, one measure and one technology choice
that a designer can build from and a stakeholder can read. The deliverable is
a discovery brief at `docs/discovery/<topic>.md` and the exact prompt for
`adk-system-designer`. The skill writes no contracts, architecture, goals or
code; it may conclude that the right first step is ordinary automation, a
process change, or measuring something nobody has measured.

## Establish the entry mode and what is already known

Read the request and any supplied material: strategy notes, funnel exports,
process documents, ticket categories, an existing product's public pages.
Separate what the user said, what a source says (with its date) and what you
assume. Then say which mode this is, in one line the user can correct:

- **A rough area** (a domain or a journey is named): find where that journey
  breaks and choose the first workflow and the outcome to measure.
- **No use case yet**: start from what the business sells, the KPIs the
  sponsor is judged on and the processes that move them, and find the
  opportunities; say early that the answer may not be AI.

If the engineer keeps a practice profile, read
[practice profile](references/practice-profile.md) before the first question;
it pre-fills the business context and scope-gate rows as labelled org defaults.
It can also pre-fill interview questions 1 (business and KPIs), 5 (the
likely system of record), 14 (deciders, reviewers and usual lead times) and
19 (unofficial AI use) for the user to confirm. Past AI attempts and what
stopped them pre-fill the matching stall checks, labelled "reported (org
profile, reviewed <date>)". A sector the profile marks as high-impact raises
the risk questions, never lowers them, and a works council or union adds a
change-management row. Always ask questions 2, 4, 6 and 10: they are about
this case.

Open with that mode's opener from
[the discovery conversation](references/discovery-interview.md): the
abandonment question for a rough area, the KPI question for no use case. Ask
one to three questions per turn, each with the decision it changes and a
default the user can accept in a word; the reference marks which questions
are asked always and which only when the request has not answered them. Keep
one real case (one advertiser, one claim, one order) as the running example;
when the user has none, construct a typical one and label it assumed. For a
one-pass draft or a user who cannot answer, put an assumed-answers table at
the top of the brief and mark the dependent choices provisional instead of
asking further.

## Find the friction and the candidates

Work from signals the business already has (funnel counts by step, time and
queue per step, rework and hand-offs, ticket and call drivers, exceptions
kept in spreadsheets) before naming a technology; record each as measured
(value, source, date) or reported (who said it). Write each candidate as an
activity plus an expected result with units and a frequency, in the user's
job language, never as a feature. Three candidates is usually enough; more
than six is a sign the domain is not yet chosen. Read
[opportunity portfolio](references/opportunity-portfolio.md) for the signals,
the scoring columns and the measure.

## Give every candidate a technology fit

Read [technology fit](references/technology-fit.md) and ask its questions in
order for each candidate: what the current process achieves and whether it is
optimised; structured records or unstructured language; whether the rules are
known and stable; what the output is; what an error costs and whether anyone
reviews it; volume and latency; whether the decision must be deterministic
and auditable. Record the fit as `agent`, `llm`, `ml`, `rules`, `process` or
`unclear`, the nearest alternative rejected and the one observable reason,
and name the mistake when you see it: an LLM doing arithmetic or lookups, an
agent where the step list can be written down, classical ML on forty rows,
an LLM scoring a table, a chatbot in front of a form that already works. A
hybrid takes the fit of its model-driven step. One line of fit per candidate
in the table; the full stakeholder sentence from the reference only for the
chosen one, in section 4 of the brief.

## Rank and choose

Start the brief now: copy the
[discovery brief template](assets/discovery-brief-template.md) to
`docs/discovery/<topic>.md` (or the project's own convention; look in `docs/`
for an existing brief or decision-record format) and fill its portfolio table
with four scores per candidate (value, feasibility, data readiness, risk),
the fit, the measure and the baseline, saying whose judgements the scores
are. Then run the helper from the project root with any Python 3.9 or later,
resolving `SKILL_DIR` to this skill's directory:

```bash
python3 "$SKILL_DIR/scripts/rank_opportunities.py" --brief docs/discovery/<topic>.md
```

Paste its ranking and findings under the table, verbatim; never paraphrase
a finding it did not print, and never write the closing summary before the
brief and the helper run exist. A first candidate with no
measure or an unclear fit blocks the handoff; an unknown baseline makes
measurement the first goal; a risk of 4 or 5 or data readiness of 1 or 2 is
a reason to choose a lower-risk candidate or to put a person before every
effect. When the user's judgement overrides the order, rerun with
`--pick <ID>` and record the reason beside the table. The first use case is
the one that can succeed, is not trivial, and shows a measured result within
months; the bigger idea stays in the portfolio with its trigger.

## Define the measure and write the brief

Fill section 4 of the brief completely for the chosen use case; the template
lists every field, from the outcome measure (observable in an existing
system; usage counts are not outcomes) and its baseline or "unknown" to the
counter-metric, the price of each error type beside today's rates, the
hypothesis chain with every arrow a hypothesis, the workflow before and
after with its validation points, the data register, the correction loop,
the embedding rule and the 90-day sentence. Then fill
the stall checks (section 7) from
[why projects stall](references/why-projects-stall.md): one row per known
cause, each citing the section that answers it or recording a gap with who
settles it. A candidate with no named owner, no data access and no path
into the real workflow is tinkering, not a first use case; say so and pick
the next one or make those three the first goals.

Fill the scope-gate table with what the conversation already established (deadline, people, money, judge, data, who approves the next
step and when) and mark the rest "unknown: ask", so the designer skips what
is answered; expect the ADK-familiarity row to be an ask. Put the decision
calendar in the brief: each approval or review is a presentation goal the
plan will carry for `adk-presenter`. Record assumptions and open questions
with how each is settled.

## Hand over

Read [handoff](references/handoff-to-design.md) for the line between this
skill and the designer and for the one prompt that ends the work. Fill that
prompt in, put it in section 9 of the brief, and end the conversation in chat
with: where the brief is saved, the first use case in one sentence with its
measure and baseline, the technology fit in the stakeholder sentence, the
next decision and its date, and the same prompt in a copyable block. When
the fit is `process`, name the role that owns the change and what will be
measured instead.

Then ask one closing question: whether the user wants the proof-of-concept
approval presentation drafted now, before the design exists. If the decision
calendar names an approval, offer the prompt; `adk-presenter` drafts it from
the brief alone, with every number labelled as the brief labels it and the
cost and scope slides marked "pending design":

```text
/adk-presenter Prepare the proof-of-concept approval presentation for a
business audience from docs/discovery/<topic>.md. The design does not exist
yet: mark cost and scope as pending and label every hypothesis. Fifteen
minutes; the decider is <name> on <date>.
```

Say that the deck is redrafted from the design and plan once they exist, so
the user can choose to design first. Local discovery work authorises no cloud operations,
no purchases of data and no contact with the user's customers; it reads what
the user supplies and public pages, and cites them with dates.

With a practice profile, offer its harvest ([practice profile](references/practice-profile.md), step 5).

Independent community project; not affiliated with or endorsed by Google.
