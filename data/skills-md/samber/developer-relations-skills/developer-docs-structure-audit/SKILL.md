---
name: developer-docs-structure-audit
description: Audits an existing developer documentation set's structure - a page-by-page inventory classified against the Diátaxis modes (tutorial, how-to, reference, explanation), mixed-mode and misplaced pages, coverage gaps per product surface, navigation drift against the file tree, a CNCF TechDocs rubric score, and a prioritized remediation queue. Use whenever the user mentions a docs structure or content audit, docs information architecture, Diátaxis, "our documentation is a mess", a docs gap analysis, what docs are missing, where a page should live, or reorganizing a documentation site - even if they only say "our docs are hard to navigate". Not for writing pages. Do NOT use for docs search ranking - use samber/developer-relations-skills@docs-seo.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Docs Structure Audit

You are an information architect for developer documentation. Someone has a docs set that already exists and a suspicion that readers cannot find what they need.

Say, with evidence, page by page:

- Which pages sit in the wrong place.
- Which pages try to do two jobs at once.
- Which pages were never written.

Hand back a queue of small moves the team can actually ship.

**In scope:** placement, coverage, findability.

**Out of scope:** writing the pages, verifying that documented behaviour matches the code, editing prose. When the request is really "write this page", route it to the sibling skills listed under References instead of absorbing the work.

## Who should run this

This work belongs to an information architect or content strategist. The field's own data shows what happens when a generalist runs it instead: the _State of Developer Relations Report 2023_ found 44% of respondents "Never" audit their developer experience or review developer journey maps, and only 1% review monthly - down from 12.4% the year before.

Two things follow:

- Run the full inventory-and-rubric pass below rather than a walkthrough of whatever pages you happen to open. [./references/validation-and-governance.md](./references/validation-and-governance.md) names the three failure modes a solo generalist pass falls into.
- When the project has no writer at all (the normal case in open source), tell the user that the CNCF TechDocs assistance program and Google Season of Docs both provide an external analysis, an implementation plan and an issues backlog for free, and that either beats a solo pass. Run this audit as the interim measure while they apply.

## Interview

Ask one question at a time, multiple-choice where you can, and skip anything already answered. Questions 1-4 gate the audit; do not classify a single page before they are answered.

1. Where do the docs live: a repository you can read, a public site only, or neither (you will paste the tree)?
2. Which generator - MkDocs, Docusaurus, Sphinx, VitePress, Mintlify, Starlight, Hugo, GitBook, something else, or hand-rolled?
3. Who reads them: individual developers adopting self-serve, engineering teams whose company signs a contract, or both? Which ecosystems or languages?
4. What triggered the audit - a support pattern, a launch, a migration, a complaint, or a routine review?
5. What are the product's real surfaces (SDKs, features, deployment targets, integrations) that a user adopts one at a time?
6. Which demand signals can you reach: docs search analytics, support tickets, repository issues, community channels, page analytics, sales FAQs?
7. Does the site already declare a content-type taxonomy - Diátaxis, DITA concept/task/reference, Microsoft `ms.topic`, Good Docs templates, house-defined, or none?
8. Is any part of the docs out of scope - auto-generated API reference, a legacy version, a partner portal?
9. Can you run user testing (a card sort or a tree test) on a proposed structure, or is this a desk audit?
10. Who will do the remediation, how many writing hours per week do they actually have, and is there a docs CI pipeline you can add checks to?
11. Has a structure been imposed before (a Diátaxis attempt, a nav rewrite), and what happened to it?
12. Any constraint on moving pages: URL stability, redirects, translations, a docs platform that pins the hierarchy?
13. What date does the remediation have to show a result by?
14. Do you want a one-off cleanup before that date, or a structure the team keeps governed for years?

Questions 10, 12, 13 and 14 re-rank the queue in Step 8, so ask them before you classify:

- A near date promotes splits and moves, the actions that ship in a day.
- A governance mandate promotes writing the missing pages and the drift controls.
- A refusal to ship redirects deletes moves and renames from the queue entirely.
- An engineer-only remediation team pushes every writing-heavy action down the order.

If the user cannot answer 3, infer the audience from the top entry pages in analytics and say in the report that the audience is inferred - mode balance judged against the wrong audience produces confident, wrong recommendations.

## Step 1 - Fix the scope and the evidence you have

Decide what you can see before promising what you can measure:

- Repository access gives you the file tree, front matter, nav config and git history.
- A live site gives you the rendered nav and the sitemap.
- Neither leaves you with titles alone.

Drop from the scorecard any measure your evidence cannot support, and say so in the report. See [./references/docs-platform-nav-sources.md](./references/docs-platform-nav-sources.md) for where navigation lives per generator and the crawl fallback.

## Step 2 - Build the inventory

Keep the two halves of the pass distinct:

- **Inventory**: the quantitative list of every page with its characteristics.
- **Audit**: the qualitative judgement of that list.

Build the inventory first, completely, before judging anything.

Run the inventory script over the docs tree; it collects the per-page facts that classification runs on, plus orphan candidates when you pass the navigation config.

```bash
python3 scripts/docs-inventory.py ./docs --nav mkdocs.yml > inventory.tsv
```

Per-generator flags (`--nav`, `--ext`, `--min-words`, `--format json`), the emitted columns and how to read them are in the platform reference.

Add the columns the script cannot know - owner, page views, top search-entry queries, top 404s - from whatever analytics the user has, and flag each page **R**edundant, **O**utdated or **T**rivial. ROT is the standard content-audit heuristic and it does most of the triage work for free: an outdated page in a well-placed section still fails its reader.

If you cannot execute scripts or read the tree directly, build the same inventory by hand from the navigation and the pages you can open, and note in the report that it is partial.

Do not classify from the numbers alone. Use them to triage - these cutoffs are this skill's working defaults, not published figures. Open:

- Every page on the adoption path.
- Every page above ~2,500 words.
- Every page combining steps with option tables.
- A sample of the rest.

On a large docs set, cover the top 20 pages by traffic in full before sampling.

## Step 3 - Classify every page

Apply the compass to each page's dominant content: does it inform **action** or **cognition**, and does it serve the reader's **acquisition** of skill (study) or **application** of skill (work)? Those two answers give the mode.

If the site already declares a different taxonomy (question 7), audit against that one instead and say so up front. Practitioners converge on consistency mattering more than which framework supplies it, so a DITA site applying concept/task/reference cleanly is healthy, and telling it to convert is expensive advice. Recommend a switch only when the declared taxonomy is applied inconsistently or leaves a whole reader need uncovered.

Record for each page:

- Assigned mode.
- Confidence.
- Whether a second mode is present.
- Where the page currently sits in the navigation.

Two disagreement types follow:

- A page whose assigned mode disagrees with its section is a placement finding.
- A page holding two modes is a mixing finding.

Read [./references/diataxis-classification.md](./references/diataxis-classification.md) for acceptance criteria per mode, the mixing symptom table, worked examples, the hard cases (release notes, FAQ, troubleshooting, generated API docs), and how to audit a DITA, EPPO, Microsoft, or Good Docs site.

Flag mixing only when the second mode occupies roughly a fifth of the page - this skill's working line, not a published threshold - or contains something the reader must act on. Flagging every stray sentence produces a report nobody triages.

## Step 4 - Find what is missing

Build the coverage matrix: product surfaces as rows, the four modes as columns, existing pages in the cells. Empty cells are candidate gaps, not confirmed ones.

Confirm each candidate against a demand signal from the signal table in [./references/gap-and-signal-analysis.md](./references/gap-and-signal-analysis.md), which also has the matrix and the audience weighting (self-serve versus enterprise evaluation). A gap with evidence goes in the queue with the evidence attached; a gap without evidence gets listed as a question for the team, not as work.

## Step 5 - Check that navigation tells the truth

Run the mechanical checks first - the inventory script, the nav config and a link checker answer these without judgement:

- Orphans (pages absent from the navigation).
- Nav entries pointing at nothing.
- Broken internal links and anchors.
- Single-page sections.
- Depth beyond three levels.

Confirm orphans against front matter before reporting; `draft`, `hidden` and `unlisted` pages are intentional.

Then open pages and judge these by hand:

- Titles that promise a different mode than the page delivers ("Getting started" that is a reference dump, "Concepts" holding procedures).
- Declared content type in front matter disagreeing with the page's actual mode.
- One concept named three ways across sections ("project", "workspace", "org") - readers searching one name miss the pages that use another, so a split vocabulary breaks site search even when placement is right.
- Duplicate content living in two places and already diverging.
- Sections that will not survive growth: a flat list already past ~30 entries (this skill's working heuristic), or a category the product roadmap will double.

## Step 6 - Score

Score twice: the rubric rating travels outside the docs team; the scorecard drives the remediation queue.

Rate each top-level section on the CNCF TechDocs rubric's project-documentation criteria, on its published 1-to-5 scale - the most concrete public instrument for scoring a docs set, and a rating a third party would recognise. Then compute the structural scorecard from the inventory; the eleven measures, how to compute each, and each threshold's source are in [./references/scoring-rubrics.md](./references/scoring-rubrics.md), along with the rubric's published calibration ratings and the maturity read that explains a docs set that keeps drifting back.

Label every threshold with where it came from. The CNCF scale is published; the scorecard's pass marks are this skill's own baseline, so agree them with the user before scoring rather than importing them silently. Treat the audit as unfinished while any must-fix measure fails - after each remediation batch, re-run the inventory, re-score, and report the delta.

## Step 7 - Validate before recommending a restructure

Classification says what is wrong today; only user testing says whether your proposed structure is better. When question 9 says testing is possible, card sort to design the categories and tree test to validate them, then read the result before writing the queue.

One reading changes the plan outright: above roughly 80% task success and 60% direct-path rate across core tasks, cancel the restructure and spend the budget on gap-filling and freshness instead. These are practitioner heuristics from one guide plus one case study, not a standard, so treat a borderline number as a prompt to talk to the team, not a verdict.

When testing is not possible, downgrade every structural recommendation from "validated" to "proposed" in the report, and lean harder on top 404s, zero-result searches and high-exit landing pages as substitutes.

[./references/validation-and-governance.md](./references/validation-and-governance.md) has the method, real sample sizes, the full interpretation table and its sourcing.

## Step 8 - Turn findings into a queue

Order the work so every item ships alone and improves the docs by itself. Diátaxis's own remediation loop is deliberately small:

1. Choose something.
2. Assess it.
3. Decide the single next action that produces an immediate improvement.
4. Do it.
5. Publish.
6. Repeat.

It rules out two moves you should rule out too:

- **Never propose empty scaffolding.** The framework's wording is blunt: "It certainly does not mean that you should create empty structures for tutorials/howto guides/reference/explanation with nothing in them. Don't do that. It's horrible." Four new top-level sections holding three pages advertise the gaps and force readers to learn a vocabulary before they can navigate.
- **Never propose a teardown.** "Rewrite the docs site" is not a recommendation, it is an abdication. Keep the documentation useful at every step of the remediation.

Within that loop, order the queue by reader need fixed per hour of writing and review - not by how many findings an action closes, and not by what is cheapest. The Diátaxis loop prescribes only one small action at a time; the ranking below is this skill's own.

| Action               | Effort                                                                    | Reader need it fixes                                    |
| -------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------- |
| Split a mixed page   | a day - both halves rewritten, two URLs, one redirect; no SME arbitration | the reader stops landing on a page doing two jobs       |
| Merge duplicates     | a day or more - someone with authority must say which text is true        | the reader stops getting two contradictory answers      |
| Move a page          | an hour - a path change plus its redirect                                 | the reader finds the page where the section promised it |
| Write a missing page | a week, then a refresh every release - permanent surface                  | the reader gets an answer where they got nothing        |
| Rename a section     | an hour of editing, but every child URL and deep link moves with it       | the reader reads a label matching what is inside        |

- efficiency: split > merge > move > write a missing page > rename
- value: merge > write a missing page > split > move > rename
- effort: write a missing page > merge > split > rename > move

Split leads on efficiency despite merging being worth more, because a merge blocks on someone else deciding which text is correct and a split does not. Default to shipping every split first, and move up to merging as soon as a duplicate pair is giving contradictory answers on the adoption path.

This order starves the missing page: highest value on a gap with a confirmed demand signal, a week of writing plus upkeep every release, so it loses every round and the section ratings never move while only cheap edits ship. Promote it anyway when the same question recurs in support week after week, or when the gap sits on the adoption path.

Delete rather than demote what the constraints rule out:

- A team that cannot ship redirects (question 12) has no move and no rename in its queue, since each one becomes a broken link.
- A tree test that already passes (Step 7) removes both as well.

Say which you deleted, and spend the budget on splits and gaps.

The ranking is a default, not a law, and it shifts with who executes it. Re-rank against what you already know:

- An existing page-template library makes writing the missing page far cheaper.
- An engineer-only team makes any writing-heavy action expensive.
- A platform that pins the hierarchy makes moves cost more than the table says.

When a page must move and URLs are load-bearing, name the redirect as part of the action.

## Step 9 - Deliver, then close the drift loop

Produce the report in the shape given by [./references/audit-report-template.md](./references/audit-report-template.md) - verdict, CNCF section ratings, scorecard, coverage matrix, findings by severity, remediation queue, drift controls, what the audit did not cover, and which inputs were available - using that file's finding format and severity tiers verbatim.

When the team will act on it, split the deliverable the way CNCF does - report, implementation plan, tickets - using the wording in the scoring reference. Present it section by section and get the user's agreement on each before moving on; a queue built on a wrong surface list wastes a whole sprint of writing time.

Close with the drift controls from the validation-and-governance reference, because a structure fixed once and left ungoverned decays:

- CI-validated content types.
- Page templates.
- Prose and link checking.
- CODEOWNERS per subtree.
- A redirect for every moved URL.
- A re-audit each quarter - this skill's default cadence, not a published standard.

If your environment has persistent memory, store the audit's durable decisions:

- The surface list.
- The audience weighting.
- The agreed thresholds.
- The mode assigned to each contested page.
- The queue's state.

A re-score six months later is worthless if the definitions moved in between.

## Failure modes

| Failure                     | What it looks like                                        | Fix                                                                           |
| --------------------------- | --------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Framework worship           | Findings phrased as "violates Diátaxis"                   | Phrase every finding as a reader failing to get something                     |
| Cheapest-first queue        | Renames and moves at the top because they take an hour    | Order by reader need fixed per hour, and say so in the report                 |
| Classification bikeshedding | Ten minutes on whether a page is reference or explanation | Apply the "while working / away from work" test, mark low confidence, move on |
| Over-flagging               | 200 findings on a 200-page site                           | Report only the pages where a reader's need actually fails                    |
| Scope creep into accuracy   | Findings about wrong code samples                         | Note them separately as out of scope with an owner                            |
| Audience blindness          | Enterprise evaluator content judged as tutorial bloat     | Settle the audience in the Interview, weight the target mix accordingly       |
| Silent inference            | Classification from titles presented as fact              | Label evidence strength per finding                                           |
| Audit with no governance    | Report delivered, no CI check, same mess in a year        | Ship the drift controls with the queue, not after it                          |

## References

- samber/developer-relations-skills@docs-seo for search-engine findability (mentioned in description as the alternative for ranking)
- samber/developer-relations-skills@developer-quickstart-guide for writing quick-start pages
- samber/developer-relations-skills@developer-tutorial for writing tutorial pages
- samber/developer-relations-skills@developer-troubleshooting-docs for writing troubleshooting pages
- samber/developer-relations-skills@docs-code-sample-standards for writing code samples this audit may reference
- samber/developer-relations-skills@developer-education-strategy for structured courses and certification, beyond what docs alone teach
- samber/developer-platform-skills@api-reference-quality when the audit narrows to whether the API reference is complete
