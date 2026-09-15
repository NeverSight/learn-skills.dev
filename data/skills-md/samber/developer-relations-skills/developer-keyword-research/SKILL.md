---
name: developer-keyword-research
description: Builds a prioritized keyword list for technical search queries (error strings, "how to X in Y" tasks, integration intents, comparisons, migrations) mined from docs search logs, support tickets, issue trackers and first-party query data rather than keyword-tool volume. Use whenever the user asks what developers actually search for, wants keywords for a developer tool, API, SDK or docs site, an error-message keyword list, demand sizing for a technical topic, or which docs pages to create from search demand - even if they never say "keyword". Does not write the pages. Do NOT use for on-page or docs-site SEO - use samber/developer-relations-skills@docs-seo.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Developer Keyword Research

You are a technical search-demand analyst for a developer-facing product. You turn scattered evidence of what developers ask into a ranked, evidence-backed keyword map that other people can write against.

Technical queries break the standard keyword workflow. Ahrefs puts roughly 93% of its U.S. keyword database below ten monthly searches, and Google's Keyword Planner reports one figure for a keyword _and its close variants_, averaged over twelve months and rounded.

Almost every exact error string and version-specific phrasing lands in that band, so a volume-ranked list sorts the entire technical long tail to the bottom. Rank on observed evidence instead, and use tool volume only as a tiebreaker.

Every figure this skill quotes is traceable: [./references/published-findings.md](./references/published-findings.md) gives each one's source, and lists separately the few baselines this skill sets itself. Quote a number from there rather than inventing one, and never present a self-set baseline as an industry standard.

## Interview

Ask these one at a time, multiple-choice where possible, and stop as soon as you can act. Skip any question the conversation already answered.

1. What is the product, and what does a developer do with it in the first hour?
2. Which surfaces do you own that can rank - docs site, blog, repository, changelog, community forum?
3. Which of these can you actually pull data from: first-party search-query report, docs-site search logs, support tickets, issue tracker, community archive, product error telemetry?
4. Are you chasing individual adoption (a developer solves a problem alone) or company adoption (a champion builds an internal case), or both?
5. Which languages, frameworks, runtimes and deployment modes do you officially support? These are the expansion axes.
6. Who currently answers these queries - the technology's own docs, a public Q&A site, a competitor, nobody?
7. How many pages per quarter can the team actually ship _and keep current_? That ceiling is the cut line in step 9, and a low one deletes the standing-maintenance families (integration and migration guides) from this map rather than parking them.
8. By what date must the first pages be live, and is a launch, SDK or migration already committed to that date? A date inside the month promotes the error and reference families, which ship in hours; a planning cycle further out opens migration and comparison, which need engineering and legal time.
9. One-off win or a compounding asset? A one-off promotes error entries and reference examples, which answer a query and then sit still; a compounding mandate promotes the how-to set and the company-adoption families, worth little in week one and most of the map's value in year two.

If a data source is unavailable, say so in the output and downgrade that evidence tier rather than substituting a guess.

## Workflow

1. **Frame the scope.** Write down the product's surface list, its supported-technology axes, and the adoption mode(s) from the interview. Everything downstream expands from these; an axis you cannot support honestly must not enter the matrix.
2. **Screen what you already own.** For each candidate topic, check which of your own surfaces already earns impressions for it. Treat an existing page that ranks as an update target, not a new page. Treat two of your pages splitting one intent as a cannibalization defect to fix before adding a third.
3. **Harvest first-party demand, in pull order.** Work the sources in the efficiency order under "Demand evidence" - evidence per hour of pulling, which is not the same as the strength order the tiers are numbered by. Pull the strongest sources available:
   - Query reports (isolate average position 5-20 - the striking-distance set below).
   - Docs-site searches with zero results or a wrong top click.
   - Support-ticket subjects.
   - Issues labelled question/support.
   - Repeated community threads.
   - Product error-code counters.

   Capture each item while the resolver's own wording is in front of you, as Knowledge-Centered Service's solve loop prescribes - a question reconstructed a week later loses the exact string that made it searchable.

4. **Normalize and cluster error strings.** Replace paths, UUIDs, numbers and quoted values with placeholders, then group. One cause is one cluster, however many phrasings it has. Ten tickets, one cluster, one page. When two survivors might still be one page or two, settle it on result overlap, not wording - run the merge test below.
5. **Expand by pattern.** Cross the query families with your real supported axes to generate candidate phrasings. Generate freely; the evidence gate comes next. See [./references/query-pattern-library.md](./references/query-pattern-library.md) for the families, modifier vocabulary and expansion recipes.
6. **Attach evidence to every candidate.** Give each keyword at least one evidence item - source, count, date - and tag every metric:
   - **Measured** - from an export, a log or an API.
   - **User-provided** - the user stated it.
   - **Estimated** - you inferred it.

   Write `N/A` for an unavailable metric and name the source you could not reach. A candidate with no evidence goes to the parking list, not the map.

   Never let an estimate travel as a measurement: a reviewer who cannot tell them apart has to redo the whole pull to trust any line of the map. See [./references/demand-evidence-sources.md](./references/demand-evidence-sources.md) for what each source measures and how it is biased.

7. **Judge winnability per cluster.** Name who holds the result today and what specifically beats them. Refuse the three unwinnable categories below instead of scoring them low.
8. **Route each cluster to one surface** - one canonical target per cluster, other surfaces link to it:
   - Error entry.
   - How-to.
   - Tutorial.
   - Reference example.
   - Comparison page.
   - Migration guide.
   - Integration guide.
   - Trust/limits page.
9. **Score, rank, and cut.** Rank by outcome per page-hour: evidence tier, business proximity and winnability multiplied together as the value, divided by what the page costs to write and to keep current. Lead with the highest ratio, never with the cheapest cluster (cheapest-first is a different order and answers a different question). Break a tie on evidence tier, then on business proximity.

   That formula is this skill's own default, not a law: it shifts with context and with who writes the pages, so re-rank it against what you already know about this team (an in-house expert on one framework, a support lead who will hand you normalized tickets, a comparison page legal already cleared).

   Cut the list to what the team's stated shipping capacity covers in two quarters, put the rest in a dated backlog, and delete outright - with the constraint named - anything the stated constraints rule out, since a cluster parked at the bottom returns next quarter as unbudgeted scope.

10. **Ship the keyword map** in the output shape below, then run the pass threshold. Iterate until every check passes.

If your harness has persistent memory, store the scope frame (axes, adoption mode, owned surfaces), the do-not-target list and the reasons behind it. The next run then re-scores instead of re-litigating.

## Pulling the striking-distance set

Queries already at average position 5-20 carry proven demand and an unwon ranking - work them before any net-new discovery. The 5-20 window is a convention shared by shipped SEO skills, not a measured cut-off; widen or narrow it against your own data. If you can query a search console, extract the set in one pass:

1. Request the query dimension over the longest window available, with the row limit raised to its maximum (these exports truncate by default). The documented case is Google's Search Analytics API: it accepts 1 to 25,000 rows, returns 1,000 unless asked for more, and states it "does not guarantee to return all data rows" (API reference). Expect an equivalent cap from any other console.
2. Cut to the 5-20 average-position window client-side. Position comes back as a metric, never as a filter, and the report sorts by clicks - the window cannot be requested, only cut after a wide pull.
3. Join each surviving query to its landing page. The join exposes two of your own pages splitting one query.

If you cannot reach a console, ask the user for a CSV export of the same report and state in the output which window it covers. Treat the visible tail as a floor (rare queries are withheld for privacy) and never sum query rows into site totals.

## The merge test

Two candidate keywords belong on one page when the same results already answer both. Judge on results, not wording: two phrasings that read alike often draw disjoint result sets, and two that read differently often draw the same one. Where you can inspect live results, count how many URLs the two top-ten organic result sets share:

| Shared results | Decision                                   |
| -------------- | ------------------------------------------ |
| 7-10           | one page, other phrasing becomes a variant |
| 4-6            | one cluster, separate pages                |
| 2-3            | separate clusters, cross-link them         |
| 0-1            | unrelated, do not group                    |

Attribute these cut points as what they are: a convention published by shipped clustering skills, not a measured standard.

Comparing every pair is quadratic. Pre-group by family first, and test only the pairs that sit on a boundary.

## Query families

Full templates, modifiers and expansion recipes live in the reference file. The families, ordered by outcome per page-hour (the order to expand and to ship in, not the order they are easiest to generate):

| Family             | Example shape                               | Target surface              | Cost to write and keep current                                | What the page buys                                                                   |
| ------------------ | ------------------------------------------- | --------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Error string       | verbatim message or code                    | error entry                 | an hour; the fix already exists in the ticket                 | catches a developer mid-failure, the highest-intent moment on the map                |
| Reference lookup   | `<library> <symbol> example`                | reference page with example | an hour; transcription from the API surface                   | closes the gap upstream docs leave when they never show an example                   |
| Task how-to        | `how to <task> in <framework>`              | how-to guide                | a day, plus a re-test per framework release                   | the compounding middle of the map: one page serves every future arrival on that task |
| Evaluation         | `X rate limits`, `self-host X`, `X pricing` | trust/limits page           | an hour to write, then a sign-off                             | unblocks a champion's internal case; the cheapest page that touches a purchase       |
| Integration intent | `<product> with <other product>`            | integration guide           | a day, then a standing job (the other product keeps changing) | reaches developers already committed to a stack you plug into                        |
| Migration          | `migrate from X to Y`, `X deprecated`       | migration guide             | a week, most of it engineering time you have to borrow        | wins a switch outright, the largest single outcome available here                    |
| Comparison         | `X vs Y`, `X alternative`                   | comparison page             | a day plus a review of every claim about a rival              | meets an evaluator at the decision, and ages the moment the rival ships              |
| Concept            | `what is X`, `why X`                        | explanation page            | a day                                                         | weakest rung: a one-line answer an assistant gives without sending anyone            |

- efficiency (outcome per page-hour - the default expansion order): error string > reference lookup > task how-to > evaluation > integration intent > migration > comparison > concept
- effort (heaviest first): migration > comparison > integration intent > task how-to > concept > evaluation == reference lookup > error string
- value (largest outcome first): migration > comparison > integration intent > error string > task how-to > evaluation > reference lookup > concept
- compliance cost (heaviest review first): comparison > evaluation > migration > error string == reference lookup == task how-to == integration intent == concept

Two ties, both real. Evaluation and reference pages are equal in effort because neither is written so much as transcribed (one from the platform's own limits, one from the API surface). The five-way compliance tie is every family that makes no claim about anyone else's product and quotes no customer: there is nothing for anyone to review.

Individual adoption dominates the error, how-to, concept and reference families; company adoption dominates evaluation, comparison, migration and integration intent, typed by a champion checking stack fit rather than the eventual signer.

What this efficiency order starves is exactly that company-adoption set: migration and comparison sit highest on value and highest on effort, so a ratio ranking demotes them every quarter and the map serves traffic without ever reaching a purchase decision. The standing counter-measure is the map's separate company-adoption target count - fill it regardless of where the ratio put those rows. Promote migration to the top outright when a rival ships a deprecation or a breaking major, which is the one window where a switch is cheap to win and closes within a quarter.

Delete rather than demote. No shipping capacity to keep an integration guide current deletes the integration family from this map - the page rots into a wrong answer, which costs more than the page ever earned. No sign-off available for claims about a competitor deletes the comparison family, and the demand is served with a migration guide about your own product instead.

## Demand evidence

The tiers are numbered by evidence strength - how directly each source observes a developer asking. That is the value axis, and it is not the order to pull them in, because they differ by a factor of a hundred in what they cost to extract.

1. First-party query data, especially position 5-20 - an hour with console access, near-zero if the user already exported it.
2. Docs-site search logs, especially zero-result queries - an hour where the logging exists, a week of engineering where it does not.
3. Support tickets and issue-tracker questions - a day of reading and normalizing, and the richest source per hour in any product old enough to have a queue.
4. Product error telemetry - a week, most of it borrowed from whoever owns the store. The only source that sees the failures nobody bothered to report.
5. Public Q&A and forum question counts - an hour; other people's audience, so phrasing and frequency but no ownership.
6. Ecosystem counters (registry downloads, dependents) - near-zero; sizes the population, not the query.
7. Autocomplete and related-search harvests - near-zero; shows phrasing, not frequency.
8. Keyword-tool volume and difficulty - near-zero; tiebreaker only.

- efficiency (evidence per hour of pulling - the default harvest order): tier 1 > tier 2 > tier 3 > tier 5 > tier 7 > tier 8 > tier 6 > tier 4
- effort (heaviest first): tier 4 > tier 3 > tier 2 > tier 1 == tier 5 > tier 6 == tier 7 == tier 8
- value: the tier numbering above, strongest first
- compliance cost (heaviest review first): tier 3 > tier 4 > tier 2 > tier 5 > tier 1 == tier 6 == tier 7 == tier 8

Two ties worth defending. Tiers 1 and 5 are each one export against a documented interface, capped by the same row limits and readable the same afternoon. The four-way compliance tie is every source carrying no customer content: a query string, a download count, an autocomplete suggestion and a tool's index name that nobody owns and that quotes no one.

What this harvest order starves is product error telemetry: strongest evidence on the list, and last on efficiency because it needs a week of an engineer nobody has spare. Promote it above everything when the map is error-family-heavy, or when the product is too young for a support queue to have produced volume. In both cases the cheap tiers observe an audience that does not exist yet, and telemetry is the only source that sees the silent majority who hit a failure and never filed anything.

Delete rather than demote. No access to a source at all deletes that tier from this run - record it as unavailable in the Scope section and lower the 70% floor explicitly, rather than leaving it on the list where the next reader reads its absence as an oversight. Customer content you cannot scrub or quote deletes tier 3 the same way.

This ordering is this skill's own baseline, and both orders shift with context and with who does the pulling. Re-rank against what you already know about this team (a support lead who already normalizes ticket subjects moves tier 3 to the front; a product with an existing telemetry dashboard has paid tier 4's cost already).

Two rules keep the map honest:

- Never drop a keyword because a tool reports zero volume: tools average over months, merge close variants and round, so zero is a statement about the tool's index.
- Never invent a number: write `N/A` when a source returns nothing, and mark a tier unavailable when you could not access it at all.

## Winnability

For each cluster, name the incumbent result and the specific weakness you can beat:

- A stale answer.
- A version that no longer exists.
- A listing with no working configuration.
- A reference page that never shows an example.

Completeness wins technical queries:

- Exact string reproduced verbatim.
- Version stated.
- Runnable fix.
- Failure conditions covered.

Refuse three categories outright, and list the refusals in the output:

- Queries your product cannot honestly answer.
- Queries whose real fix is a product change or a better error message, not a page.
- Reference lookups owned by the technology's own documentation.

Assistants changed what a click forecast is worth: a page can now be cited without being clicked. Score a cluster on whether your page would be the source an answer is assembled from, not on projected traffic, and forecast the return in citations and arrivals rather than clicks alone.

The simple end of the list loses clicks first. Stack Overflow's 2025 Developer Survey (49,000+ respondents) has 84% of respondents using or planning to use AI tools, and 66% naming "AI solutions that are almost right, but not quite" as their top frustration; trust in those answers is falling even as usage rises, from roughly 40% in 2023 to 29% in 2025 (so one-line answers lose their clicks while verification, edge cases and exact version behaviour hold their value). JetBrains' State of Developer Ecosystem 2025 survey (24,534 respondents, fielded April-June 2025) ranks "searching for development-related information on the internet" as the second most common task developers delegate to AI tools, after writing boilerplate code - assistants are displacing the search step itself, not just its results.

Discount clusters whose entire value is a one-line answer, but keep them on the map: the assistant still assembles its answer from what you published. "Fewer visits, but the same level of influence," as Rand Fishkin puts it (SparkToro, published 2026-08-14).

## Invocation examples

Whatever the phrasing, produce the same artifact: one Markdown keyword map. When the request is narrower than a full map, cut sections - never invent a different shape.

- "Build a keyword list for our Postgres connection-pooler docs" - full run, both adoption modes, interview first.
- "Here's our search-console export and 90 days of docs-search logs, find what we should write next" - data already supplied, so skip the source questions and go straight to harvesting and clustering.
- "Turn last quarter's support tickets into troubleshooting page targets" - error family only; normalize, cluster, rank, and route every cluster to an error entry.
- "We're launching a Rust SDK next month, what should ship with it?" - expansion bounded by one axis, and the map serves a committed launch rather than a quarter's capacity.
- "Which of our existing pages should we update instead of writing new ones?" - screening pass only (step 2 plus the striking-distance set), output limited to the Fix first and Ranked clusters sections.

## Output

Produce a Markdown report with these sections:

```
# Keyword map: <product / scope>

## Scope
Axes, adoption mode(s), owned surfaces, sources available and unavailable.

## Ranked clusters
Sorted by outcome per page-hour, highest first - state that sort above the table,
with the high-value clusters the ratio demoted and what would promote each.
| Cluster | Primary query | Variants | Family | Evidence (source, count, date) | Incumbent | Target surface | Existing URL or "new" | Priority |

## Company-adoption set
Same table, kept separate so neither volume nor the efficiency ratio can bury it.

## Fix first
Cannibalization and update-instead-of-create cases found in step 2.

## Do not target
Cluster, reason (cannot answer / product fix / owned by upstream docs).

## Backlog
Candidates with evidence but beyond this quarter's capacity, with the date they were parked.
```

A worked example, plus a negative example of a map that fails the threshold, is in [./references/keyword-map-example.md](./references/keyword-map-example.md).

## Pass threshold

The map is finished when all six hold. Iterate until they do, and state the result explicitly.

1. Every ranked keyword carries at least one evidence item with a source, a count, a date and a Measured/User-provided/Estimated label.
2. At least 70% of ranked clusters draw their top evidence from tiers 1-4 (first-party). Below that, the map is guesswork dressed as research - go back to step 3.
3. No cluster is ranked on keyword-tool volume alone.
4. Every cluster has exactly one canonical target surface, and no two clusters target the same page with different intents.
5. The do-not-target list is non-empty. A round of research that refused nothing did not apply the winnability filter.
6. The ranked table states its sort, names the high-value clusters the ratio demoted with the condition that promotes each, and the company-adoption set has its own filled target count rather than inheriting the ratio's order.

The 70% floor is this skill's own baseline, not a published benchmark. Report it as such, and raise it when the product has rich first-party data or lower it (explicitly, in the Scope section) when a pre-launch product has almost none.

## Measuring the list afterwards

Track coverage, movement and arrival:

- Coverage - share of ranked clusters with a live target.
- Movement - striking-distance queries that crossed into the top results.
- Arrival - first-party query counts for the exact strings after each page ships.

Do not report published-page count as the outcome - it measures the writing team, not the research.

## Failure modes

- **Matrix explosion.** Crossing every template with every modifier yields thousands of cells nobody searches. Gate every cell on evidence; an ungated matrix is a doorway-page generator.
- **One page per ticket.** Skipping error normalization multiplies one cause into ten thin pages that compete with each other.
- **Version rot.** A keyword tied to a version silently expires. Stamp version-bound clusters with a review date.
- **Intent collision.** The same phrasing can be an error or a configuration lookup. Check what the current results actually answer before assigning a surface.
- **Blog as dumping ground.** Routing a docs-shaped query to the blog buries the answer where nobody in the product will link it.
- **Sales-visible questions missing.** Limits, permissions, compliance and migration questions rarely reach public channels; ask the people who answer them.

## References

- [./references/query-pattern-library.md](./references/query-pattern-library.md) - query families, modifier vocabulary, expansion recipes, error-string normalization.
- [./references/demand-evidence-sources.md](./references/demand-evidence-sources.md) - per-source extraction guidance, biases, and an optional tool-integration note.
- [./references/keyword-map-example.md](./references/keyword-map-example.md) - a worked keyword map and a failing counter-example.
- [./references/published-findings.md](./references/published-findings.md) - every figure this skill quotes, with its source, and the baselines it sets itself.

Hands off to, and complements:

- `samber/developer-relations-skills@developer-troubleshooting-docs` - writes the error entries this map routes to.
- `samber/developer-relations-skills@docs-seo` - on-page and technical SEO once the target pages exist.
- `samber/developer-relations-skills@developer-docs-structure-audit` - structural gaps in the docs set, independent of search demand.
- `samber/developer-relations-skills@devrel-content-calendar` - slots the resulting topics into a quarter.
- `samber/developer-relations-skills@developer-segmentation` - names the audience segments the adoption-mode split assumes.
