---
name: bargainbadger-price-update
description: Turn one minimoths crawl session into a dated prices table appended to a product note in the Obsidian vault. Use when asked to update a product note with today's prices, add a prices section, or find the best price for a product after running a search.
---

## What this does

A crawl captures one product term across every store in one session.

This skill turns that session into a dated prices section in the product's vault note.

The updated note is the deliverable.

Even when the request is phrased as a question about the best price, the job is to record the prices, not to pick a winner.

The product is a parameter, so the same steps run for whatever the session searched.

## Read the specification first

Everything factual — the database location, the schema, the field definitions, the sampling queries, the extraction rules, the arithmetic, and the edge cases — lives in the vault.

Read the hub note before touching anything:

```
/Users/mtm/Documents/Obsidian Vault/bargainbadger.md
```

Then read every note its Contents section links to, and follow second-order links where one of those notes defers to another for a definition.

Resolve a wikilink by joining the vault path and the link text with a `.md` suffix.

The Contents list is deliberately not reproduced here, because notes get added, split, and renamed there.

Read what the hub lists today, not what it listed when this skill was written.

This file is a workflow, not a reference.

It states no facts about the data, the database, or the schema, and it must not acquire any.

When a fact about the data, the schema, or the table is missing from the vault, add it to the vault rather than to this file.

The layout of the write-up is the exception, and it belongs here.

How the finished section is arranged on the page says nothing about groceries, so the rules in "Section layout" below are this file's own and are not a gap in the vault specification.

## Trigger

Run this only when asked to write prices into a product note.

Requests that trigger it:

- "I just now did a search for shallots, can you update our shallots markdown file to add a new section for prices based off today"
- "Add a prices section to the leeks note"
- "What is the best price for cultured butter right now"

Requests that do NOT trigger it:

- Sampling the database to develop the schema, which is specification work
- Adding a change log entry
- Anything that does not end in a table written to a product note

## The workflow

1. Read the specification, as above.
2. Identify the session, and confirm what it actually searched before trusting any label attached to it.
3. Resolve the product note in the vault, and never create one as a side effect.
4. Pull the session's rows and narrow them to the product, reporting how many were captured, kept, and dropped.
5. Extract the schema's fields from those rows, in batches, into a scratch file outside the vault.
6. Compute every derived price in code, never by hand.
7. Render the table into a prices section arranged as "Section layout" below requires, inserted above the newest existing one and leaving older sections untouched, or created fresh when the note has none.
8. Commit the note, and delete the scratch file.

Each step's rules come from the specification, apart from the section layout in step 7, which comes from this file.

That includes the table itself — which columns it carries, what each one holds, and how the rows are ordered are the specification's to define, not this file's.

Where the specification is silent, match the most recent prices section already in the note, and report the choice as a gap in the specification rather than adopting it quietly.

An inherited format is a stopgap until the specification defines it.

## Section layout

The reasoning behind a table is worth writing down, and it must never stand between the reader and the table.

So a prices section is the table followed by one subsection:

- The table, directly under the dated heading, with nothing in between.
- `### notes`, holding every word of prose the section has.

The table gets no heading of its own, because the dated heading is already its heading.

That is the whole point of the arrangement: jumping to the dated heading from the note's table of contents lands on the numbers, which is what is wanted most often, and the reasoning is one heading further down for the times it is not.

Resist putting a summary above the table, however short: a reader who wants the numbers is already looking at them, and one who wants the story will open `### notes`.

`### notes` takes all of it, opening with the run id and the number of stores, this section's scope, and the counts of rows captured and kept and dropped, then the headline findings, then how the table was built: narrowing the crawl term to the product, which variants the table holds and which were sent to another note, any vocabulary a column was normalised to, what happened row by row, and which listings produced no row and why.

Do not divide that subsection further, because a reader who has decided to skip the reasoning gains nothing from it being filed into categories.

Order it and group it with lead-in sentences and bullet lists instead, keeping the listings that produced no row last, and link each one named.

When one product needs more than one table, because it is sold in two dimensions that cannot be ranked against each other, the tables cannot both sit bare under the dated heading, so each takes a `###` heading naming its basis, as in `### priced by weight` and `### priced by volume`, and `### notes` follows the last one.

Older sections in the vault carry a spread of other subsection names, and those are not to be copied forward.

## Non-goals

- Deciding schema questions, which belong in the vault notes and their change log.
- Updating the store boolean fields in the note front matter.
- Recommending which product to buy, or which store to buy it from.
- Running the crawl, which the user does before invoking this skill.

## Exclude Single-Serve Pods

Single-serve coffee pods — Keurig, K-Cup, Nespresso, and any other one-cup capsule — never appear in a prices section.

Drop them at the narrowing step and price them nowhere. A pod is a single-use plastic cup thrown away per cup and a bag is not, so the format is out of scope whatever it costs.

This is a standing preference about what the user will buy, not a schema rule.

When a crawl returns both bags and pods, table only the bags. Record in the section's `### notes` that pods were excluded on the standing preference, give the count, and name any store that drops out of the table entirely because it stocks the product only in pods.

## Schema Changes

The authoritative convention lives in the intro of the vault note "bargainbadger change log.md", which the hub note "bargainbadger.md" links to. Read it there before making any schema change.

Every schema change gets a dated entry naming the motivating products, quoting the captured listing text inline with an explanation of what in it forced the change, and giving the productUrl.

Write that evidence in the same edit as the schema change, never as a follow-up.

Never include database row ids or capture timestamps. The database is wiped regularly, so ids, site, and capturedAt are worthless — only the quoted listing text and the productUrl survive.
