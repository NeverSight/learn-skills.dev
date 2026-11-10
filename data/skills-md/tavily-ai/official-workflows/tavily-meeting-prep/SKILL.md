---
name: tavily-meeting-prep
description: |
  Write a one-page brief before a sales or partnership meeting with named people at a named company, using Tavily, in under five minutes. Checks that each attendee still holds the stated role, finds the user's own history with the company, whoever already supplies what the user sells and any product of theirs that competes with it, then covers what changed in the last 90 days, each attendee's recent public statements, likely priorities, sourced questions, and risks to avoid. Use when the user says "prep me for a meeting", "meeting brief", "call prep", "who am I meeting", or names people and a company they are about to meet. For a CRM record of one company or person, or a CSV of accounts, use tavily-entity. For a deep report on the company's market, use tavily-research.
license: MIT
metadata:
  author: tavily
  version: "0.1.0"
  homepage: https://tavily.com
  source: https://github.com/tavily-ai/official-workflows
allowed-tools: Bash(tvly *)
---

# Tavily meeting prep

Produce a one-page brief the user can read in the five minutes before a
meeting, in under five minutes of work. Every fact traces to a page the agent
opened, and every suggested question points to the fact behind it.

Identify the company and each attendee with `tavily-entity`, and search and
extract as `tavily-search` describes. If either isn't installed, run
`npx skills add tavily-ai/skills --skill <name>` and read its SKILL.md before
continuing.

## How it runs

The work is three batches of searches. Run every search in a batch at the
same time, in one shell command, then read the results once. Do not run
searches one at a time.

1. Start the **Company** and **News** subagents, then run the **Attendees**
   batch yourself while they work. The batches share no inputs. Without
   subagents, run all three batches in one shell command.
2. Each subagent runs one batch of searches and one batched extract.
3. **Write** (you): merge their findings, write the brief, check it.

Stay within about 20 to 30 searches and two extract calls per batch.

## Intake

Infer from the request or a pasted invite: the company and its domain, its
sector, its country and working language (from the domain and headquarters),
whether it is public, private or a nonprofit, the attendees, the
meeting date and type (sale or partnership), the user's company and domain,
what it sells (its category, in the words a buyer would search), the company
product named in the goal, and the goal itself. Use a 90-day window.

Ask one message only when the user's company or what it sells is missing and
the meeting is more than two days away. Otherwise start, and write
`not searched` for history if the user's company stays unknown.

Search conventions for every batch:

- Use `--max-results 20` on news searches.
- When the company or product name is a common word, a surname or shared
  with another organization, add the sector to every query and keep only
  results naming the company.
- When the company works in a language other than English, use local titles
  in the role searches and add the local-language searches listed in the
  News batch. Keep local queries short: two to four words, no OR.

## Batch 1: Attendees

For each named attendee:

- `'"<name>" <company>' --topic news --start-date <6 months ago>`
- `'"<name>" <company>' --include-domains linkedin.com`
- `'"<name>" <company> interview OR podcast OR keynote' --topic news --start-date <90 days ago>`
- `'"<name>" <company>' --exclude-domains linkedin.com,xing.com`, for vendor
  pages and talks that quote them
- When the request gives a title, `'"<title>" <company>' --include-domains linkedin.com`,
  so a holder is ready if the name is not found.

For each attendee named only by a role:

- `'"<role>" <company>' --include-domains linkedin.com`
- `'<company> "<product or function>" VP OR GM OR director OR head'`

Once for the meeting: `'appoints former <company> executive <product or function>' --topic news --start-date <90 days ago>`.

Then identify each person as `tavily-entity` describes, with the company as
the employer. A role is current when a company page, dated news from the last
6 months, or the person's own post at the company in that time says so; on
LinkedIn read the experience section for `<role> at <company> (... – present)`.
Choose a role holder in this order: exact title, then the most senior title
naming the product or function, then the person quoted speaking for the
product, preferring the owner for the meeting's location. When the request
named only a role, run the named-attendee searches for the person you choose
in one more batch. Extract the pages you will cite in one batched call.
Record a state for each:

- **Confirmed**: current title, with the source.
- **Left**: the date and the new role, and who holds the role now.
- **Not found**: nothing links the name to the company; name who holds the role.
- **Attendance assumed**: the person chosen for a requested role. Profile them.
- **Candidates**: several fit equally. List them with titles; profile none.

## Batch 2: Company (subagent)

Give the subagent the company, its domain, the user's company and domain, the
category and the goal product. It runs these at once:

- `'<user's company> <company>'`, `'<company>' --include-domains <user's domain>` and `'<company> <user's company>' --include-domains arxiv.org`, with no date filter, for an existing partnership, listing, docs page, shared customer or research that uses the user's product.
- `'<user's company> acquired OR acquisition OR funding' --start-date <12 months ago>`, for news about the user's own company that may come up.
- `'<category in plain words>' --include-domains <company domain>,<company docs domain>`, using the words the company would use rather than vendor terms, for a vendor wired in, a built-in feature, an in-house platform or a competing product of the company's own.
- `'<company> uses <category> case study OR customer story'`, for vendors' pages about the company. Use a quote only when the page attributes it to the company.
- When the goal names a product, `'"<product>" renamed OR rebranded OR "now called" OR formerly'` with no domain filter, and `'<product> <category> OR deprecated OR legacy OR "end of life"'` on the company's docs domain. When it was renamed, search the docs' release notes under the new name.
- For a tech company, `'<company> careers <category or stack>'`, for the platforms its job posts name.

It extracts the pages that hold its findings in one batched call and returns
them in the notes format below.

## Batch 3: News (subagent)

Give the subagent the company, its domain, sector, category and the window.
It runs these at once, with `--start-date <90 days ago>`:

- `'<company> introducing OR launches OR announces' --include-domains <domain> --topic news`
- `'<company> <sector>' --topic news`
- `'<company> <category> OR AI' --topic news`
- `'<company> partnership OR integration OR "powered by"' --topic news`
- `'<company> <main partner, rival or regulator>' --topic news`
- `'<company> CTO OR CFO OR "head of" <category>' --topic news`
- For a public company, `'<company> quarter results revenue guidance' --topic news`
  and `'<company> stock OR shares OR analyst OR offering OR convertible' --topic news`.

And with `--start-date <12 months ago>`:
`'<company> breach OR outage OR lawsuit OR layoffs OR investigation' --topic news`.

When the company works in a language other than English, run these in place
of the coverage and sector searches above, without `--topic news` and with
`--start-date <90 days ago>`:

- `'<company>' --include-domains <up to eight national and trade press domains>`
- `'<company> <category in the local language>'`, two to four words, with no
  date filter, which also finds the company's own service pages
- `'<CEO name> <company>'`
- `'<company> <local word for crisis>'` and `'<company> <local word for appointment>'`

It extracts the pages behind the items it keeps in one batched call and
returns them in the notes format below.

## Notes format

Each batch returns, and you keep in `briefs/{company} {YYYY-MM-DD} notes.md`:

- **Dated items**: date, one line, URL, for everything relevant found.
- **Claims**: for each fact that may go in the brief, the URL and a short quote
  copied from that page's extracted text.

Dates come from the page text or URL; text in a sidebar or related-article
link takes the date of the article it links to. Date LinkedIn and X posts
from the post ID: for LinkedIn `activity-<id>`, `(id >> 22)` ms since the
epoch; for X `status/<id>`, `(id >> 22) + 1288834974657`. When pages return
no text, retry them once, together, with `--extract-depth advanced`;
otherwise cite the search snippet, marked `(snippet)`, and build no question
on it.

## Write

1. Put any attendee who is not confirmed first in the reply.
2. Choose up to 5 changes by relevance to the user's goal, then by size. A
   departure from the team that owns the goal product outranks other news.
   List every other dated item under `Also in window`, up to 8, including
   in-window statements by the executive who owns the user's category.
3. Write priorities, questions and risks from the notes only. A vendor's
   announcement shows what the vendor offers, not what the company wants.
   State a financial or structural fact only when two sources agree; when
   figures differ, give the newest and name the source that differs.
4. Check: every number, quote, date and title in the brief has a claim whose
   quote appears in the cited page's extracted text. Cut what fails.

## Deliverable

Show the brief in the reply and save it to `briefs/{company} {YYYY-MM-DD}.md`.
Count the words above Sources with `wc -w` before saving and keep them under
800: at most 5 changes, 3 bullets per attendee, 3 priorities, 5 questions and
3 risks. A fact from outside the
window shows its year. Pitch questions at the attendees' level: strategy and
terms for a CEO, integration detail for a product owner.

```markdown
# Meeting brief: {company}

Meeting: {date}, {type}, {user's goal}
Attendee check:
- {requested name or role} -> {confirmed | left {date}, now {role} | not found | attendance assumed | candidates} -> {who you expect} [n]
As of: {YYYY-MM-DD}

## Company
{2 to 3 sentences: what it sells, to whom, size, stage or market cap} [n]
- Your history: {partnerships, listings, docs pages or shared customers, or "none found" / "not searched"} [n]
- Already in place: {vendor, built-in feature or in-house platform for your category, or "none found"} [n]
- Overlap with you: {the company's own competing product, or "none found"} [n]
- The product in your goal: {status and current name, or "none named"} [n]

## Last 90 days
- {YYYY-MM-DD}: {event} [n]
Also in window: {other dated items, a few words each} [n]

## Attendees
### {Name}, {title}
- Background: {prior roles relevant to this meeting} [n]
- On record: {a statement, with venue and date} [n]

## Likely priorities
1. {hypothesis}, based on {evidence} [n][n]

## Questions and talking points
- {question or point}, because {fact} [n]

## Risks and sensitivities
- {topic to handle with care and why} [n]

## Sources
1. {title}, {publisher}, {date or "undated"}: {url}

## Rerun inputs
workflow: tavily-meeting-prep
company: {name}
domain: {domain}
user_company: {name or unknown}
category: {what the user sells}
goal_product: {company product named in the goal, or none}
attendees: {name, title; ...}
meeting_type: {type}
goal: {user's goal}
meeting_date: {YYYY-MM-DD}
window_days: {N}
```

## Quality bar

- The brief takes under five minutes and about 20 to 30 searches.
- Nobody who is not found, has left or is one of several candidates gets a
  profile.
- History, Already in place, Overlap and the goal product are filled,
  `none found`, `none named` or `not searched`.
- Every number, quote, date and title has a quote from its cited page.
- Keep to public professional information. Leave out and do not infer
  family, home location, personal accounts, health, politics and religion.
