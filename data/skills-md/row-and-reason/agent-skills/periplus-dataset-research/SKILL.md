---
name: periplus-dataset-research
description: Build an evidence-backed dataset for a research question using Periplus where useful. Use for landscape studies, inventories, comparisons and investigations that need defined records, coverage checks and reusable source evidence.
---

# Dataset research

Translate the question into a usable dataset, then interpret what the evidence supports. Work forward with reasonable assumptions; ask only when an unresolved choice would materially change the answer. When the user starts from a loose topic rather than defined rows, show a small sample of what the sources support and get their agreement before expanding coverage substantially (a large crawl, many captures, pins or schedules). Once a scope is agreed, carry it out without asking per step.

## Shape the dataset

Define what one row represents, the population and time period, inclusion and exclusion rules, and the fields needed to answer the question. Separate entities from observations: a company with five pages is not five companies. State a working definition for ambiguous concepts such as “active”, “available” or “European”. Record units and the relevant geography.

Use supplied files, authoritative sources, available search tools and existing captures as appropriate. Periplus corpus search searches captured material, not the live web. An empty result leaves coverage unresolved. When URLs are missing, use appropriate discovery outside Periplus or bounded link following from relevant seeds.

## Learn from contrasting sources

Inspect examples that could change the extraction or interpretation: a typical record, a different template, a missing field, a subsidiary, an out-of-scope result. Derive fields and evidence rules from the actual sources. Do not require artificial source categories or a fixed sample count.

Choose sources by their authority for each claim. A homepage, directory, filing and product page may disagree because they describe different dates, organizations or offerings. Keep these distinctions rather than silently resolving them into a convenient value.

Expand coverage as the question requires. Compare source-stated totals with discovered URLs, acquired pages, extracted records and deduplicated entities separately. Inspect failed pages, pagination, unvisited branches and regional variants. Neither a completed crawl nor a non-truncated query proves a complete population. Continue discovery or disclose the specific gap.

## Validate and deliver

Check duplicates, conflicting identities, missing fields, implausible values and boundary cases. Verify a contrasting sample against source content and inspect every material exception. Distinguish absent information, acquisition failure, ambiguous interpretation and a supported negative finding. Use explicit denominators when reporting rates or totals.

Keep source URL, capture ID and observation time with each derived claim; retain field-level evidence where a row combines sources. Preserve raw values beside normalized fields and distinguish observed facts from inference. Capture time is not publication or event time.

Deliver the dataset, concise findings, coverage limits and provenance in the user's requested format. Identify what has actually been saved:

- A captured observation is source evidence with its own retention lifetime.
- A saved query preserves SQL for rerunning; its rows can change.
- A frozen dataset requires an exported/materialized result, its extraction logic and parameters, a capture manifest and an appropriate evidence-retention arrangement. A source snapshot alone does not retain evidence.

## Live product reference

Read [MCP operational contracts](https://docs.periplus.dev/mcp#agent-workflow) through the connected docs tools before operations. Use live schema discovery and the relevant [SQL](https://docs.periplus.dev/sql), [provenance](https://docs.periplus.dev/provenance), [requests](https://docs.periplus.dev/requests) and [pins](https://docs.periplus.dev/pins) guides for mechanics. Follow current permissions and the user's acquisition and retention constraints.
