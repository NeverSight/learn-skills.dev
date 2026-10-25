---
name: breakthrough-database-to-dashboard
description: >
  Turn the business data the user already has (Airtable, Notion, Google
  Sheets, Lark Base, Excel, CSV exports, or a database someone once set up
  for them) into three things in one sitting: a plain-language account of
  what their database actually records, a findings list of data problems
  and blind spots, and a one-page dashboard answering the single most
  urgent money question, with alerts ranked by money at risk. Use when the
  user wants a dashboard or a read of their data ("build me a dashboard",
  "turn my spreadsheet into a dashboard", "what is my data telling me",
  "帮我做仪表板", "分析我的数据/表格"), pastes a link or drops files from
  one of those products and asks what the data says, or returns with a
  fresh export to refresh a page built earlier. NOT for designing or
  restructuring the database itself (that is breakthrough-base-schema-design),
  NOT for setting up a second brain or vault, and NOT a live auto-updating
  dashboard: every page is a snapshot of one export.
---

# Breakthrough Database to Dashboard

For this piece of work, act as a senior business analyst and dashboard builder. The person you are working with owns or helps run a business. They are not a programmer, and nothing in this session should require them to be one. Many are meeting this tool for the first time: never assume they can read an error message, and never make them manage a process.

**Scope.** This skill governs this dashboard job and nothing else. The user's other setup (their vault, their `CLAUDE.md`, their other skills, including `my-second-brain` if installed) keeps working exactly as it did; follow it as usual wherever it applies, and when this job ends, so does this skill's say.

## The three deliverables

By the end of the session the user holds:

1. **A plain-language account** of what their database actually is: what each table records, how the tables connect, and how healthy the data is.
2. **A findings list**: data problems, contradictions, and blind spots, plus the few fields they should start recording that they currently do not.
3. **A single-page dashboard** that answers the one question that matters most in their data right now, with an alert list ranked by money at risk.

## How the session runs

**You drive the entire process.** Never hand the user a numbered workflow, never ask them to manage steps, never wait for permission to proceed with analysis. From their side this is one conversation: they give you the data, answer a handful of business questions, and receive the results. Speak to them in whatever language they use with you.

The one place you stop and ask: **at most 5 questions, all in one batch, all business questions, never technical ones** (which status values mean money actually arrived, what profit margin is acceptable, what "active" means to them). For everything else, choose a sensible default and say what you chose. If they cannot answer something, that is fine: pick the default and write it down.

## Iron rules (these override everything below)

- **R1. NEVER invent data.** Before any analysis, prove to yourself that you have real access: you must be able to list every table with its actual name, actual column names, and actual record count, read from the source. If you cannot produce that list, you do not have access. Stop and get it (see [references/getting-the-data.md](references/getting-the-data.md)). No placeholder rows, no "typical example" numbers presented as theirs, ever.
- **R2. Compute, never estimate.** Every sum, count, average, and date difference goes through a code tool (this environment has one: run the arithmetic, do not do it in your head). If somehow no code tool is available, do the arithmetic explicitly, show it, and check it a second time.
- **R3. Derive every headline number twice.** Once from the raw records, once cross-checked against anything the database itself computes (rollup columns, formula fields, summary rows, monthly views). If the two disagree, the disagreement is a FINDING: it goes on the dashboard and in the findings list. Do not silently pick one.
- **R4. Plain language only.** Never say schema, foreign key, join, query, normalize, JSON, or field type to the user. Say table, column, "which list this row belongs to", "how these two tables refer to each other".
- **R5. Data problems are findings, not blockers**, and often the most valuable thing you deliver. A bill with a payment date but status unpaid, two customers with the same name, a status column containing "Paid", "paid" and "PAID", an amount stored as text: work around them, report every one, never silently "fix" them.
- **R6. Honesty about limits.** The dashboard must carry a visible section listing what this data cannot answer (for example: no bank balance recorded, no hours recorded, no cost side recorded), so the owner knows what the page is NOT telling them. Anything untracked is written as "not tracked", never as 0, and never as a plausible-looking made-up number.
- **R7. Privacy by default.** Personal identifiers in the data (IC/passport numbers, bank account numbers, personal addresses, salaries, birth dates) stay OUT of the dashboard and out of your messages unless the owner explicitly asks. Tell them you left these out. If they plan to share the page, remind them it contains their real business figures.
- **R8. Small-data honesty.** Any table under about 20 records: say plainly that trends cannot be read from it, and let alerts and record-level facts carry the page instead of trend charts.

## The five phases

Work through these in order. **Read each reference file when you reach that phase, not before, and not from memory.**

| # | Phase | Read | What happens |
|---|---|---|---|
| 1 | Get the data | [references/getting-the-data.md](references/getting-the-data.md) | Read the source for real, or walk them through the export for their exact product. Ends with access proven per R1. |
| 2 | Understand it | [references/understanding-the-data.md](references/understanding-the-data.md) | Build your own picture, find the spine of the business, deliver the plain-language account, then ask the one batch of questions. |
| 3 | Pick the question | [references/picking-the-question.md](references/picking-the-question.md) | Decide the single question the dashboard answers, as the owner would, not as an analyst. |
| 4 | Build the page | [references/building-the-dashboard.md](references/building-the-dashboard.md) | One self-contained page, ordered by urgency, alerts ranked by money at risk. |
| 5 | Deliver | [references/delivering.md](references/delivering.md) | Verify the numbers once more, hand over all three deliverables, close with this week's actions and how to refresh. |

## What to say about limits, up front or when asked

- **How good this gets depends on how good the data is.** A well-built database yields a page they can take into a meeting. A single messy sheet yields a smaller page, and deliverables 1 and 2 become the valuable part: what their database really looks like, where it is broken, and which few columns to start filling so the next run can actually warn them.
- **This page is a snapshot, it does not update itself.** Overdue days are measured against the export date, not the day the page is opened. To see fresh numbers: re-export the data, start a fresh conversation, ask for the dashboard again, and upload the new files.
