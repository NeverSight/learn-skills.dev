---
name: a11y-content-judgment
description: >
  Load this skill when an audit needs the judgment-shaped WCAG criteria that
  scanners cannot decide — are page titles, headings, form labels, link text
  in context, and image alternatives actually useful, meaningful, and
  descriptive for the person relying on them (2.4.2, 2.4.6, 2.4.4, 1.1.1),
  and is navigation consistent across pages (3.2.3, 3.2.4)? It inventories
  every such element across a URL list, attaches deterministic heuristic
  flags, has a model draft a per-row judgment with a rationale, and hands the
  rows to a named human ratifier as a CSV. Output is a DRAFT until human
  ratification; ratification does not itself create a criterion outcome. Never use it to
  flip an outcome-map cell, to judge criteria that need interaction or
  assistive technology, or as a substitute for a11y-test's measurement.
license: Apache-2.0
compatibility: Claude Code-compatible; protocol is model-agnostic; scripts need Node 20+ and playwright
metadata:
  author: zivtech
  version: "0.1.0"
---

# Content Judgment Skill (draft-and-ratify for the judgment criteria)

> **Status: CANDIDATE — promoted 2026-09-02 from one engagement run; eval lane added the same day, gate not met as the rubric stood (rubric revised, re-draw pending — `evals/results/content-judgment-2026-09/`).** Origin: the
> zivtech/a11y-audits (private) EPA interactive-retest engagement, OpenACR lane phase P3 bucket B3,
> where the owner ruled that "determining these things are actually perfect use cases for using AI
> to help with a11y tests" and delegated the *drafting* of B3 judgments to the agent while keeping
> ratification human. First run: 43 views across two products, 1,899 deduplicated rows, 27 judge
> batches. The promotion bar this skill has not yet met: a fixture set with planted defective and
> planted *clean* rows (the false-alarm half matters more), scored across two model tiers and two
> draws. Until then, treat the drafts as detector output behind a mandatory human pass.

Apply this skill when a WCAG-EM or ICT-Baseline audit reaches the rows the crosswalk marks
`partial` — the tests where a scanner can enumerate the elements but cannot say whether the text a
person receives does its job. It sits **after** a11y-test (which measures) and **before**
acr-reporting (which serializes ratified outcomes). It never replaces either.

---

## Core Mandate

**The agent drafts. A named human ratifies. Ratification records the human judgment, not a criterion
outcome: a `yes` remains sample-scoped; a `no` may proceed through the separate finding/receipt path.**

Two reasons this line is where it is, and both are load-bearing:

1. These rows land in conformance-adjacent documents. A fluent model opinion on whether an alt text
   is "adequate," multiplied across thousands of cells, is exactly the dead output an ACR must not
   carry. The rationale column exists so the ratifier can see *why* and disagree.
2. The judgment is about a person's experience, not a rule. "Learn more" is fine inside a paragraph
   that already names the destination and a failure in a grid of five identical cards. The rubric
   forces the draft to name what the person loses; a `no` without that is rejected at spot-check.

---

## What it covers, and what it does NOT

| Criterion | Row type | Decided by |
|---|---|---|
| 2.4.2 Page Titled | `title` (one per view) | model draft → human |
| 2.4.6 Headings and Labels | `heading`, `field` | model draft → human |
| 2.4.4 Link Purpose (In Context) | `link` | model draft → human |
| 1.1.1 Non-text Content | `image` | model draft → human |
| 3.2.4 Consistent Identification | `ident` (same destination, different names) | model draft → human |
| 3.2.3 Consistent Navigation | `nav-consistency.csv` (relative order of shared nav items) | **deterministic**, no model; human reads the note |

**Not covered — route elsewhere and say so:** 1.3.1 beyond the level-skip flag (structure needs the
rendered page and often AT); 1.4.1 use of color (visual); 3.3.x error handling and 3.2.2 on-input
(interaction); 2.2.x timing (temporal observation); 4.1.2/4.1.3 name-role-value and status messages
(screen-reader receipts); media alternatives 1.2.x, flashing 2.3.1, sensory 1.3.3, images of text
1.4.5, CAPTCHA (human observation). A request to extend the CSV to any of those is a scoping error.

The skill also does not compute accessible names. `name` in every row is a DOM approximation
(`aria-labelledby` > `aria-label` > text content > image alt > `title`), recorded as `name_source`.
When the approximation is what makes a row `no`, the ratifier verifies in a browser.

---

## Pipeline

All four steps are files under [references/](references/). Run them from a directory where
`playwright` resolves (they import it as a peer dependency).

### 1. Inventory — `references/content-inventory.mjs`

```bash
node references/content-inventory.mjs --urls-file views.txt --out ./content-inventory
# views.txt lines: url | id<TAB>url | id,product,url[,settle_ms]   (# comments allowed)
# options: --settle 2600 --viewport 1440x900 --only ID,ID --product name --engagement label --no-screenshots
```

Per URL, at one viewport, read-only, nothing activated: title, `lang`, h1 list, meta description,
skip links; every heading with level, name source, and a section preview; every link with name,
text, resolved href, file extension, new-window/external/icon-only signals, and the nearest
enclosing text block as `context`; every image with alt presence, alt emptiness, `aria-hidden`,
the control it sits inside, figcaption, size, and adjacent text; every form field with its computed
label and where the label came from; every navigation landmark with its ordered link list. Caps
per view (headings 250, links 500, images 250, fields 120) are recorded when hit. A navigation
error is an environment note, never product evidence.

### 2. Build rows — `references/build-judgment-rows.mjs --build`

```bash
node references/build-judgment-rows.mjs --build --inventory ./content-inventory   # writes judgment-units.json + batches/*.jsonl
```

- **Dedupes shared chrome.** A unit is keyed on product + type + name + destination (+ a context
  hash for links, + alt/control for images), so a footer link on 19 pages is judged once and fans
  out with `view_count` and the `views` list. On the origin run this took 43 views' raw elements
  down to 1,899 rows.
- **Attaches deterministic flags** so the ratifier sees the machine's reasons separately from the
  model's opinion: `title_shared_by_N_views`, `title_shares_no_word_with_h1`, `no_h1`, `empty_h1`,
  `heading_empty`, `heading_generic`, `heading_numeric_only`, `heading_repeated_in_page`,
  `level_skip_hN_to_hM`, `link_empty_name`, `link_generic_text`, `link_name_is_url`,
  `file_<ext>_not_indicated`, `new_window_not_indicated`, `icon_only_link_weak_alt`,
  `same_name_different_hrefs_in_page`, `img_missing_alt_attr`, `alt_generic`, `alt_is_filename`,
  `functional_image_no_name`, `alt_duplicates_control_text`, `alt_repeats_adjacent_text`,
  `svg_unnamed_not_hidden`, `complex_image_short_alt`, `field_unlabeled_<source>`,
  `label_generic`, `required_not_in_label`, `same_href_multiple_names`. Flags are evidence to
  weigh, not verdicts; the rubric says so to the judge.
- **3.2.3 is decided here, not by a model.** Per product and host, the navigation items present on
  at least half the views (minimum two) form the shared set; each view is checked for the same
  *relative order* of the shared items it carries. Extra or absent items are informational (a
  sub-navigation on detail pages is allowed); an order change is the signal.
- Writes judge worklists of ≤ 90 rows as `batches/<product>-<type>-NN.jsonl`.

### 3. Judge — one subagent per batch, rubric-bound

Give each judge exactly four things: [references/judgment-rubric.md](references/judgment-rubric.md),
[references/judge-prompt.md](references/judge-prompt.md), one batch, and a one-paragraph **product-and-audience
note** (what the product is, who uses it) — the rubric's audience-shorthand rule cannot be applied
without it, and the batch line does not carry it (the origin run leaked product only through the
batch filename, which is the mechanism behind its over-hedging bias). It writes
`<batch>.judged.jsonl` with, per row: `judgment` (`yes` | `no` | `unsure`), `confidence`,
`rationale` (≤ 25 words naming what the person experiences), `fix` (≤ 20 words), `needs_human`,
`drafted_by` (model id). Constraints that matter: native Read/Write only, no nested agents, one
output line per input line, never invent what a destination page contains.

**Model routing:** judgment on the hosted tier (Sonnet-class handled the origin run; see the
calibration record below). A local model may run as a *detector* to pre-sort, never as the
`drafted_by` of record — the local tier's "detector, not verdict authority" rule from this repo's
benchmark lane applies without exception here.

### 4. Merge, spot-check, hand off — `--merge`

```bash
node references/build-judgment-rows.mjs --merge --inventory ./content-inventory
# writes draft-judgments.csv, draft-judgments-<product>.csv, nav-consistency.csv, draft-judgments.json
```

Before handing the CSV over, the orchestrating session **spot-checks**: every `unsure`, every row
where a heuristic flag and the draft disagree (flagged but `yes`, clean but `no`), and a random
10 % of the rest, reading the row's context and, where the call hinges on it, the screenshot or the
live page. Write the results to `spot-checks.jsonl` (`{id, spot_check: agree|overturn, judgment?, note?}`);
the merge renders them in the `spot_check` column and carries the effective value in
`session_judgment` (the overturned value where one exists, else the draft). `--sample` writes
`spot-check-sample.jsonl` with exactly that selection (seeded, reproducible). This is the step that
makes the drafts *the session's* draft rather than a delegated one — still a draft. Run it with a stronger tier
than the first pass where one is available, and have the reader check each rationale against the
row: on the origin run, first-pass rationales occasionally named chemicals, landmarks, or titles
that were not in the captured row, with the verdict still correct on what the row did show.

CSV columns: `status, id, product, type, sc, view_count, views, name, detail, href, context, landmark,
selector, visible, flags, draft_judgment, confidence, rationale, fix, needs_human, drafted_by,
spot_check, session_draft_judgment, ratified_by, ratified_judgment, ratifier_note`. `status` is the
first column on every row (`DRAFT_NOT_RATIFIED` until a person signs that row) so no consumer can
read a draft as a verdict; `session_draft_judgment` is named for what it is. The last three are blank on delivery and
are display fields populated from the human's durable return, not edits to the generated CSV. Rows sort `no` → `unsure` → `yes`, widest fan-out first, so the
ratifier's first hour lands on the rows that matter.

For a portable human handoff, use [the content-review return loop](references/content-review-return-loop.md).
`review-content-judgments.mjs --export` generates a draft worklist, a CSV for an ordinary tracker
workspace, and a blank response template. `--apply` validates the returned observation against
the exact inventory snapshot, unit pin, and prior decision before updating `ratifications.jsonl`;
run `--merge` afterward to refresh the views. It does not write to a tracker or authenticate the
person named. Assignments, disagreements, and next work actions remain in the receiving tracker.
The wrapper covers WCAG content judgments only; direct JSONL retains the separate client scope.

---

## Receipt discipline

- `draft-judgments.json` carries `status` (`DRAFT_NOT_RATIFIED` → `PARTIALLY_RATIFIED` →
  `RATIFIED`), the units file hash, the rubric filename, and a `coverage_basis` block (views
  inventoried, viewport, caps, activation = none). It is never an input to an outcome map.
- **A `yes` row is evidence of no defect in the captured sample only; it never supports a criterion
  outcome.** One viewport, nothing activated, capped counts: everything behind interaction, every
  other viewport, and everything past the caps was never inventoried, so an all-`yes` ratified CSV
  is not evidence for "Supports" on 2.4.4 or 1.1.1. Only a ratified `no` travels (as a finding).
- Ratification is a file, not a CSV edit: `ratifications.jsonl` lines of
  `{id, ratified_by, ratified_judgment, ratifier_note, ratified_utc, ruling}`; `--merge` fills the
  ratifier columns from it. A family ruling ("every logo that is a link is named by its destination")
  is one `ruling` id fanned out over its rows, so the CSV shows which sentence of the owner's decided
  each row. Rows a ratifier defers or skips carry a note and no `ratified_by`.
- **A name alone does not complete a return.** `--merge` requires a name, a `yes | no | unsure`
  judgment (or a nonblank client result), and a valid review date before exposing effective
  ratifier fields. New pinned or correction records require a real UTC timestamp ending in `Z`.
  Historical records without pins or correction fields also accept a calendar-valid `YYYY-MM-DD`,
  labeled `date_precision: day` and `legacy_unpinned`; no time is invented. Shape alone cannot
  authenticate a historical record's age. Incomplete records remain draft with diagnostics. Malformed JSON,
  invalid IDs/scopes/fields/values, stale supplied unit pins, or conflicting records exit `2`
  before generated outputs change; only a missing optional file is treated as absent. This is
  validation atomicity, not a transaction across sequential output writes on a failing filesystem.
- **Corrections name what they replace.** Identical records are retries, not additional decisions.
  A changed record requires `supersedes` equal to the prior computed decision ID and a nonblank
  `supersession_reason`. Orphan and forward references fail. The merged rows expose decision IDs,
  including incomplete drafts, along with `ratification_state`, unit pin, pin status, and diagnostics;
  client scope has independent `client_ratification_*` columns. Existing complete unpinned records
  remain compatible and explicitly `legacy_unpinned`; they are not retroactively pinned evidence.
- A client-standard ruling is a **separate scope**: `{..., scope: "client", ratified_client_result,
  ruling: "<rule id>"}` renders as `client_ratified_*` columns and leaves the WCAG judgment column
  alone. A page title that is fine under 2.4.2 can sit on a page with three h1s that fails the
  client's one-h1 rule; the two verdicts must not overwrite each other, and the receipt that reaches
  an outcome map cites only the WCAG-scope one.
- Hand the ratifier a **worklist**, not the CSV: family decisions first (one answer settles many
  rows), then the rows that need a look (`unsure`, or a `no` with no fact class behind it), then the
  fact classes to sign once (missing alt attribute, empty link name, unlabeled field, raw-URL text).
  On the origin run that turned 1,847 rows into 8 questions, 53 rows, and 10 signatures; the owner
  answered the 8 questions in one message.
- A client may publish its own web standards beside WCAG. The origin run applied one such standard
  as a **separate client scope** — see the worked example in
  [references/client-standards-example-epa.md](references/client-standards-example-epa.md) — and the
  merge accepts a `standards.jsonl` (`{id, <prefix>_rules, <prefix>_result, <prefix>_note}` — any single
  prefix, read by suffix; the worked example uses `epa_`) that it renders as `client_rules` /
  `client_result` / `client_note`. That is the whole of what this skill
  provides: the matcher is engagement-specific, this skill does not prescribe a client-standards
  pass, and generalizing the rules to a table is deliberately not done until a second client
  standard exists. Client-scope results never reach the WCAG-scope receipt.
- A ratified row feeds the evaluation report's per-SC outcome map only through a receipt that names
  `ratified_by`, the ratification date, and the row `id`. The report contract's `outcomes` entry cites
  the receipt, not the CSV. `drafted_by` travels with it so nobody later mistakes the draft for the
  judgment.
- Rows with `view_count > 1` ratify once and apply to every listed view; the receipt lists the views.
- Keep new captures in new inventory directories and retain their predecessors. IDs are stable
  grouping keys, not universal evidence revisions: a title unit, for example, is keyed to its view
  even when its text changes. New returned decisions therefore carry `unit_sha256`, the canonical
  unit snapshot hash; a supplied pin must match the current unit. The portable loop also pins the
  whole inventory snapshot. Changed source requires a fresh capture/review bundle, not editing or
  discarding historical ratifications to pass validation.

---

## Gotchas from the origin run (do not re-learn)

- **URL fragments AND query strings are part of identity.** Skip links (`/#main`) collapsed into the
  home page until the destination key kept the hash; then 25 city and region links collapsed into
  the bare home URL, two PubMed articles into one, and ten map tabs into one, until it kept the
  query string too. Each collapse produced a false "different names for one destination" row that
  the first-pass judge could only mark `unsure`. The second reader caught the pattern from the
  rationale wording ("likely a lost parameter"); the fix is in the builder, not the rubric.
- **`javascript:`/`void(0)` hrefs are not destinations.** Basemap and zoom controls marked up as
  links grouped as seven names for one destination. Excluded from the 3.2.4 rows.
- **Paired table columns are not a 3.2.4 case.** An ID column and a name column that both link to
  the same record, on the same page, in `main`, produced 60 rows the first pass judged `yes` and the
  second reader confirmed as the table pattern. The builder skips a destination whose every name
  variant sits on the identical view set inside `main`. On the origin run this took the 3.2.4 rows
  from 103 to 25, all of which are now real questions (a version-number link in the header and a
  "Release Notes" link in the footer for one destination, on nearly every view, is the clearest).
- **Informational flags must not drive spot-check selection.** `no_h1`, `h1_count_N`,
  `level_skip_*`, `name_from_*`, `title_duplicates_text`, `new_window_not_indicated` describe the
  page, not the row's own judgment; counting them as "flagged" pulled 25 structurally fine titles
  into the disagreement sample. The sampler ignores them.
- **Navigation landmarks fragment and nest.** One site wrapped each top-level menu button in its own
  `<nav>` (nineteen `nav` landmarks, most with one item); another nested three `nav`s and reused an
  `id` on the detail-page tab nav. Comparing nav *signatures* across views flagged half the pages
  as inconsistent; comparing relative order of the shared items flagged none, which matched the
  pages. That is why 3.2.3 is relative-order, not equality.
- **Two-view groups make every item "shared."** Minimum shared count is two, so a pair of pages is
  compared only on items both carry.
- **Detail-page sub-navigation is not a 3.2.3 failure.** Absent shared items are reported as
  informational; only order changes are the signal.
- **Application shells (maps, single-page tools) have no shared navigation.** The note says so;
  it is not a finding.
- **A bare site name as `<title>` on most pages is the single most common 2.4.2 miss** and the
  `title_shared_by_N_views` flag catches it before any model runs. On the origin run most views of
  one product shared a single bare title.
- **Grid-heavy pages produce hundreds of near-identical field rows** (column filters). Dedupe on
  type + label + label source keeps them to one row each; the ratifier is not asked 300 times.
- **Never treat `alt=""` as automatically right or wrong.** The image row records the control it
  sits inside; an empty alt on the only content of a link is `functional_image_no_name`, an empty
  alt beside a text label is usually correct. The rubric routes on that distinction.

---

## Calibration record

Filled per run. A run that skips this section has not finished. Read the split, not the average.
The agreement column is **second-reader agreement** — one model class reading another's drafts —
not a human base rate; the ratifier's own overturn rate is a separate column filled from
`ratifications.jsonl` and was not captured on the origin run. The `unsure` and clean-but-`no`
rates say where the first pass needs the second reader most, so a budget-constrained run should
second-read those two groups first and sample the rest.

| Run | Rows | Draft model | Spot-checked | Second-reader agreement | Ratifier overturn rate | Systematic biases observed |
|---|---|---|---|---|---|---|
| 2026-09-02 origin (two federal products, 43 views) | 1,899 drafted (1,847 after the builder fixes) | claude-sonnet-5 | 501 rows (479 before the builder fixes, 22 after): every `unsure`, every flag/draft disagreement, 10 % random; second reader claude-opus-5 on four chunks, the orchestrating session on three | 88.0 % overall (60/501 overturned: 56 across the four named groups plus 4 among the 22 post-fix rows); **random rows 98.6 %** (2/146 overturned); flagged-but-`yes` 98.1 % (3/162); **clean-but-`no` 78.1 %** (16/73); **`unsure` 64.3 %** (35/98 settled by the reader, 29 of them to `yes`) | not captured (the owner ruled by family; per-row overturns were not recorded) | (1) Over-hedging: audience-standard shorthand (HTTr, ADME, IVIVE) and repeated ID-link constructs drafted `unsure`; (2) inconsistency within a batch on identical fact patterns; (3) rationales asserting facts not in the row (a chemical name with empty context, an unrecorded landmark label) with the verdict still right; (4) a few `no` verdicts held to a bar the rubric does not set (an icon alt that names the thing but not what it means). No systematic false-`yes` found. |

---

## Boundaries with sibling skills

- **a11y-test** measures and enumerates; it never judges descriptiveness. This skill consumes the
  same kind of URL list and can run beside `references/baseline-url-scan.mjs` on the same views.
- **a11y-critic** reviews design decisions and plans; if a `no` row implies a systemic pattern
  (every card grid uses "Learn more"), that pattern goes to the critic as one finding, not 40 rows.
- **bug-reporting** turns a ratified `no` into a filable issue; the row's `selector`, `href`,
  `views`, and `fix` are the inputs it needs.
- **acr-reporting** serializes ratified outcomes; its own text now carries the refusal rule (a
  content-judgment CSV row whose `status` is not `RATIFIED` is never an outcome input), and even a
  ratified `yes` is sample-scoped evidence, not a supports term.
