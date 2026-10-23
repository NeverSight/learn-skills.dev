---
name: breakthrough-base-schema-design
description: >
  Design a Lark Base for the user's business through a guided interview: find
  the one unit of work the business repeats, settle where every kind of record
  is born (the Base itself, or software they already use such as accounting, a
  CRM, HR or an online shop) and which way it flows, then derive the tables,
  links and formulas from the numbers the owner wants to see. Ends with a Base
  Blueprint, an acceptance test, and a Plan Sheet a fresh session follows to
  build the Base. Use when the user wants a database or data hub designed
  ("design my Lark Base", "what tables do I need", "帮我设计多维表格",
  "我的业务要怎么建表", "data hub", "把会计软件的资料打通进 Base", "哪个系统为准"),
  when one giant table needs restructuring, or when unsure whether something
  is a field, a select, or its own table. NOT the build itself (a fresh
  session follows the Plan Sheet), NOT reports or dashboards from a filled
  database (breakthrough-database-to-dashboard), NOT a second-brain vault
  (my-second-brain).
---

# Breakthrough Base Schema Design

This skill runs one job: interview a business owner, find the shape of their business, and design a Lark Base that fits it. The job ends when they hold a blueprint they could hand to someone and say "build this", and a Plan Sheet a fresh session can build it from.

**This is a task, not an identity.** It governs the design conversation it was invoked for and nothing beyond it. Every other instruction in the session stays in force exactly as it was: the user's own `CLAUDE.md`, their second-brain vault and its rules if they have one, and any other installed skill. If the finished blueprint gets filed into a `my-second-brain` vault, the vault's own filing law decides where it lands, never this file.

**Who you are talking to.** A business owner or operations lead: smart about their business, not necessarily technical. ⛔ Never say schema, entity, normalisation, cardinality, foreign key, or system of record to them. Say table, row, link, rollup, and home (正本, where a record is born). If they say "source of truth" themselves, use their words. You do not hand people templates; you interview them and design a base that fits.

## The one idea

Every operating base is a **spine** plus **orbits**. The spine is the one thing the business does over and over, the thing they would count at the end of a year. Everything else in the base exists to answer one of four questions about a single spine row:

1. What came in (revenue documents)
2. What went out (cost documents)
3. Who touched it (people, inside and outside)
4. Where is it now (stage, tasks, deliverables, proof)

Businesses differ enormously in what the spine is called. They do not differ much in the fact that there is one. Find it first; everything else falls out of it.

**Every kind of record also has one home**: the one place it is born and changed. Some homes are the Base itself. Others are software the business already uses: invoices in the accounting software, customers in a CRM, staff in HR. When the home is elsewhere, the Base holds a copy that flows one way, in, and nobody edits it here. The rule is per kind of record: one Base can hold copies flowing in and requests flowing out side by side, but each kind of record has exactly one home and one direction. This is what lets the Base become the company's data hub without the same fact drifting apart in two places.

## How the conversation runs

- **One question at a time. Wait for the answer.** Never batch questions into a list.
- ⛔ **Do not propose a single table until the interview reaches its metrics phase** (Phase 6 in the reference). They will push you to design early. Hold the line once, explain that the tables fall out of the numbers they want, then continue.
- **Mirror the user's language**, including mixed Chinese and English if that is how they write.
- When an answer is vague, ask for a real example with real names and real numbers. "A client" is useless. "Last month's job for Tan Sri's foundation, forty two thousand, paid late" is designable.
- When there is a fork, name both sides, state the tradeoff in one sentence, and recommend one.
- **Say when you are guessing.** Never invent a Lark capability you are not sure exists, and never invent a number the owner did not say. The blueprint contains their figures or blanks, nothing made up.
- If they say "just give me the standard one", decline once and explain that the standard one is what fails. Then offer the fast path: four questions (what is the unit of work, how does money come in, what do you pay out per unit, and where does the invoice number come from), a Phase 1 blueprint from those answers, and the full interview later once they have used it.

## The path, and what to load when

Interview in phases, then design, then challenge the design, then deliver the blueprint with a build order and an acceptance test. Load each reference at the moment its stage starts; ⛔ do not preload the set.

| When | Read |
|---|---|
| Before the first interview question | [references/interview.md](references/interview.md) and [references/data-hub-roles.md](references/data-hub-roles.md) (where each kind of record is born is asked from Phase 0 onward) |
| Turning answers into tables, fields, and links | [references/derivation-rules.md](references/derivation-rules.md) |
| Shaping the design layer by layer against a proven base | [references/reference-architecture.md](references/reference-architecture.md) |
| Writing any formula, choosing any field type, sequencing any build step | [references/lark-mechanics.md](references/lark-mechanics.md) |
| Presenting the blueprint, phasing it, closing the session | [references/blueprint-and-build.md](references/blueprint-and-build.md) |
| Writing the Plan Sheet | [references/plan-sheet.md](references/plan-sheet.md) |

## Finishing

Close with five things, in the shape [references/blueprint-and-build.md](references/blueprint-and-build.md) specifies:

1. The Base Blueprint document, including where each kind of record is born.
2. The Phase 1 build order, numbered, with nothing in it that is not Phase 1.
3. The metric traceability table, framed as the acceptance test: build it, enter two real records, and if any of these numbers is wrong, the design is wrong and they come back. Every line to another system is reported at the state it has proven, never as done.
4. One sentence on what was deliberately left out and what would have to change for it to be worth adding.
5. The Plan Sheet ([references/plan-sheet.md](references/plan-sheet.md)), with one line on how to use it: open a new session and ask it to build the Base from the sheet.

Offer to save the blueprint and the Plan Sheet as markdown files where the user chooses. In a second-brain vault, their own filing rules decide the destination.

## What this skill is not

- Not a builder. It designs; it does not create tables in this session. Building happens in a fresh session that follows the Plan Sheet with the Lark skills the user has installed, so the design conversation and the build never share one crowded session.
- Not a connector. It records where each copy comes from, who owns it and how far it has been proven. It does not choose connector tools, promise that a given software can be connected, or build syncs.
- Not a reporting skill. Turning a filled base into dashboards is breakthrough-database-to-dashboard.
- Not a vault or second-brain tool. It coexists with my-second-brain and touches nothing that skill governs.
