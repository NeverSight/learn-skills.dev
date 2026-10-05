---
name: scrape-plan
description: Plan a web scrape and author a validated extraction spec — explore a detail page, discover fields, confirm the schema, then validate it with more pages, HTML-variant comparison, extracted values, and an optional browser review, and present the plan for approval.
argument-hint: "[url] [what to extract]"
---

This file is 544 lines long; read all of them.

`SKILL_DIR` below stands for the absolute path of the directory that contains this file. `SKILLS_DIR` stands for the directory that holds every skill directory, one of them being `SKILL_DIR`.

You are planning a web scrape. Download 1 detail page, discover fields, confirm
the schema in the terminal, then validate the spec by downloading more pages,
comparing HTML variants, and extracting values — and finally present the
finalized plan for approval.

This skill can be invoked directly by the user (to plan a scraper/spider for a
site) or by the `/scrape` orchestrator as its planning + validation stage.

Read `SKILLS_DIR/scrape/references/python-environments.md` and
`SKILLS_DIR/scrape/references/extraction-spec.md`.

Your output is twofold:
1. **Persisted spec files** under `.scrape/{site_name}/` — schema, pages,
   values, and a navigation data type, ready for building the spider.
2. **A plain-text final message** carrying the resolved plan parameters
   (the Finalization phase) — the `/scrape` orchestrator parses this to drive
   the remaining stages.

Several steps below run a skill in a **subagent**, so that page HTML never enters this context. Delegate with whatever tool runs a prompt in a separate agent, e.g. `Agent`, `task` or `spawn_agent`: the quoted text as its prompt, and the agent type, model and reasoning effort left at their defaults. Without such a tool, run the skills inline instead, one at a time, and continue from their saved output files alone.

Several steps below **ask the user** to choose between options. When asking is unavailable, take the fallback stated with the question instead, and say so in your final answer. Ask with whatever tool presents the user a multiple-choice question, e.g. `AskUserQuestion` or `request_user_input`; without one, ask in plain text, listing the options as a numbered list, and wait for the answer.

**Hard constraints — never violate these:**
- You MUST NOT fetch, read, grep, or parse any HTML file yourself. Page download is handled by `download.py`; field discovery is handled by the `/scrape-analyze-page` subagent. The main agent only orchestrates and consumes their outputs.
- This includes `raw.html`, `rendered.html`, `*.cleaned.html`, and any other saved page HTML. You may check whether a file exists, but you MUST NOT open it, print it, grep it, parse it, or run extraction scripts against it from the main agent.
- You MUST invoke `/scrape-analyze-page` as a subagent before building any schema. Building a schema from raw HTML without first running that subagent is a critical error.
- While waiting for `/scrape-analyze-page`, do NOT read HTML files, run `clean_html.py`, `extract_metadata.py`, or any inline parser code, even if the agent response suggests continuing unrelated work. Wait for the subagent to complete, then read only its saved JSON output.

## Working rules

Cross-cutting rules; the sections below reference them by name.

- **Blocked-site rule**: if a download or exploration reports the site as
  blocked, suggest Zyte API. Only if the user agrees, invoke `/zyte` for
  credential setup — pass a credential-setup request (e.g.
  `/zyte set up Zyte credentials`) so the skill routes to the credentials
  setup flow rather than any other one. After it returns, re-run the failed
  download/exploration and only proceed once it succeeds.
- **HTML-file-selection rule**: prefer `rendered.html`, falling back to
  `raw.html` if it doesn't exist; where both variants are analyzed, skip a
  variant whose file doesn't exist. Decide with file-existence checks only
  (see the hard constraints).
- **Source-of-truth rule**: `.scrape/{site_name}/{data_type}/spec.json` is the
  single source of truth for the schema. Apply every schema change (drops,
  renames, description edits, source changes) there; if
  `.scrape/{site_name}/{data_type}-list/spec.json` exists, mirror schema
  changes into it.

## Parse intent

This is the user prompt: `$ARGUMENTS`. You need to extract the following information from it:

- **target_url**: the starting URL
- **data_type**: what is being extracted, **always singular**, whether the user names it or you infer it from the URL/page — "books" → "book", "products" → "product"
- **field_hints**: any specific fields the user mentioned (may be empty)
- **existing_approved_schema**: any explicit existing schema supplied by the
  caller, such as `Existing approved schema: ProductItem(title: string, price:
  string, rating: string)`. These fields are already approved by project context,
  not merely hints.
- **site_name**: a short identifier (e.g. "books-toscrape", "realestate-listings") — derive from the site and data type

Also extract the plan parameters below when the prompt states them. They
pre-fill the corresponding lines in the initial plan so the user sees them
already applied rather than having to re-state them in refinement:

| Parameter | Default | Notes |
|---|---|---|
| project_name | derive from the site (e.g. `books_toscrape_com`) | |
| project_dir | `./{project_name}` | |
| html_variant | `auto` | `raw` or `rendered` pins the variant; `auto` compares both |
| browser_review | `ask` | `always` / `never` |
| spider_create | `yes` | `no` skips the spider stage |
| Zyte API | off unless already configured | |

The work proceeds in five phases — Discovery, Schema gate, Validation, Review,
Finalization — in order, each phase gating the next. Within each phase the
sections appear in execution order: later sections consume the outputs of
earlier ones.

## Discovery

### Pick a unique site name

```bash
BASE="books-toscrape"  # your derived site_name
NAME="$BASE"
N=2
while [ -d ".scrape/$NAME" ]; do NAME="${BASE}-${N}"; N=$((N+1)); done
echo "$NAME"
```

The spec goes under `.scrape/{site_name}/`, working files under
`.scrape/.work/{site_name}/`. Directories are created on demand by the tools
that write into them — nothing to pre-create.

### Get a detail page

Decide how to obtain a detail page:
- If `target_url` is itself a detail page (the user pointed at a specific item/article, or the URL clearly identifies one), **download it directly**.
- Otherwise, ask — you MUST ask; do not choose for the
  user. Question: "How should I get a detail page to analyze? If you already
  have a detail page URL, paste it as the Other answer." Header: "Detail
  page". Options: `Provide a URL` (description: "You can also paste the URL
  directly into the free-form answer.") / `Explore the site`. If the answer is a URL,
  **download it directly**; if they picked `Provide a URL` without
  giving one, tell the user "Paste the detail page URL.", wait for the URL,
  then download it directly. Fallback: `Explore the site`.

**Download directly** using `download.py`:
```bash
uv run --python 3.14 SKILL_DIR/scripts/download.py <<'EOF'
[{"url": "DETAIL_URL", "output_dir": ".scrape/.work/{site_name}/explore/pages/detail-1", "page_type": "detail"}]
EOF
```

**Explore** by following the exploration procedure yourself, inline — this
minimal pass is too small to justify a subagent. Read
`SKILL_DIR/references/explore-site.md` and follow it with:
url={target_url}, project_path=.scrape/.work/{site_name}/explore,
DETAIL_COUNT=1, LIST_COUNT=0.

This downloads the homepage + 1 detail page into `.scrape/.work/{site_name}/explore/pages/`.

**If exploration reports the site as blocked**: apply the blocked-site rule.

### Analyze the detail page and explore the site

Pick the HTML file for analysis per the HTML-file-selection rule (rendered preferred, existence check only).

Launch two subagents in a single message: the detail-page analysis, and the
full site exploration that the Validation phase consumes — starting it now
lets it run in the background through the schema gate instead of blocking
Validation later. The exploration reuses the pages already downloaded and
downloads only what is missing to reach the counts; per the subagent-paths
rule, pass `SKILL_DIR` in its prompt. The analysis prompt MUST start
with `/scrape-analyze-page`, and the subagent must invoke that skill — any
main-agent substitute violates the hard constraints.

One subagent per line, description then prompt:

> `analyze detail-1 rendered` — Run /scrape-analyze-page Extract data from .scrape/.work/{site_name}/explore/pages/detail-1/rendered.html and save it into .scrape/.work/{site_name}/analyze-page/detail-1.rendered.json
> `explore site` — Read SKILL_DIR/references/explore-site.md and follow it with: url={target_url}, project_path=.scrape/.work/{site_name}/explore, DETAIL_COUNT=2, LIST_COUNT=2. Return the summary.

Wait for the analysis subagent to finish — the exploration keeps running in
the background; the Validation phase collects it. Then read the analysis
result from `.scrape/.work/{site_name}/analyze-page/detail-1.rendered.json` —
per the hard constraints, this JSON is the only field-discovery input for the
main agent. If the expected file is not present, retry the
`/scrape-analyze-page` subagent or report a blocker.

### Build schema

From the analysis result, build a JSON Schema:
- Collect all field names and their types (analyze-page reports JSON Schema type names)
- Add `description` for each field (infer from context)
- Mark fields matching field_hints as `"source": "requested"`, others as `"source": "discovered"`
- Capture `examples` from the extracted value (truncate to 200 chars with `...` if longer)

If `existing_approved_schema` is present, it overrides open-ended field
discovery:

- Build the schema from exactly those approved field names and apparent types.
- Use analysis values only as examples and extraction evidence for those fields.
- Mark every approved field as `"source": "requested"`.
- Do not add unrelated discovered fields, even if `/scrape-analyze-page` found
  them.
- If an approved field is missing from the analysis result or appears
  incompatible, report the conflict instead of silently dropping or changing it.

## Schema gate

### Quick schema check

If `existing_approved_schema` is present, skip the approval loop for unchanged
fields. Briefly report that the existing project schema is being reused, then
continue to saving the spec. Do not ask the user to choose, redefine, or
approve those fields again.

Otherwise, present the schema with values in the terminal, grouped by
requested/discovered:

```
Found {N} fields on {detail_page_url}:

Requested:
  title (string): "A Light in the Attic"
  price (string): "£51.77"

Discovered:
  rating (integer): 3
  category (string): "Poetry"
  description (string): "It's hard to imagine a world without..." (2340 chars)
  upc (string): "a897fe39b1053632"
```

These fields are sampled from one page; the Validation phase checks them
against more pages, so the list can still change. Tell the user they can add,
drop, or rename fields now, or leave detailed edits for the browser review later.

Wait for the user's response. They can:
- **Approve** ("looks good", "ok", "approve") → proceed to saving the spec
- **Drop fields** ("drop description, image_url") → remove from the schema, show the updated list
- **Keep a discovered field** ("keep rating") → change its `"source"` to `"requested"`
- **Rename** ("rename upc to product_code") → rename in the schema
- **Edit a description** ("price should be without the currency symbol") → update the description and value
- **Use a different detail URL** → download it directly ("Get a detail page"), re-run the analysis subagent and "Build schema", then re-present. Do not relaunch the exploration — the running one stays valid, it is keyed to `target_url`.
- **Other instructions** → apply and show the updated schema

Loop until the user approves, re-displaying the schema after each change.

If the user pre-authorised proceeding (e.g. "just save it, don't check back"),
skip the wait and go straight to saving the spec.

### Save the spec (after the schema check)

Write `.scrape/{site_name}/{data_type}/spec.json` in the data-type spec format
from `extraction-spec.md` (`url`, `data_type`, `html_variant`, `schema`). The
`schema` MUST be valid JSON Schema (draft/2020-12) using the documented subset
— do NOT invent a custom format (e.g. a plain array of field objects). Every
field needs `type`, `description`, and `examples` — the user-approved value
(with any corrections), truncated to 200 chars with "..." if longer. Set
`html_variant` to the variant analyzed in Discovery ("Choose HTML variant"
updates it if the comparison chooses differently).

## Validation

### Collect the exploration

Now validate the schema against more pages. If the "explore site" subagent
launched in Discovery is still running, wait for it now — it usually finishes
during the schema gate. If it failed or was never launched, launch it with
the same prompt and wait.

After it returns, the exploration holds the start page + 2 detail pages + 2 list pages, classified links, and navigation values, all under `.scrape/.work/{site_name}/explore/`. Store the link extraction variant from its summary as `nav_html_variant` — "Extract values" writes it into the navigation spec.

If the site is blocked, apply the blocked-site rule.

Then distribute pages to the right data-type subfolders (`site_path` is `.scrape/{site_name}`). Copy only what downstream reads — the HTML variants and `meta.json`; `links.json` and `groups.txt` stay in the work dir:
```bash
copy_page() {
  dest="$2/$(basename "$1")"; mkdir -p "$dest"
  for f in "$1"/*.html "$1"/meta.json; do [ -f "$f" ] && cp "$f" "$dest"; done
}

# Detail pages → data type
for d in .scrape/.work/{site_name}/explore/pages/detail-*; do
  [ -d "$d" ] && copy_page "$d" {site_path}/{data_type}/pages
done

# Start + list pages → navigation
for d in .scrape/.work/{site_name}/explore/pages/start-* .scrape/.work/{site_name}/explore/pages/list-*; do
  [ -d "$d" ] && copy_page "$d" {site_path}/navigation/pages
done

# Navigation values (generated by the exploration)
mkdir -p {site_path}/navigation/values
cp .scrape/.work/{site_name}/explore/values/*.json {site_path}/navigation/values/ 2>/dev/null || true
```

### Analyze detail sample and list pages in parallel

Validate the schema by analyzing a bounded detail-page sample (both HTML
variants, to test which one can extract the approved schema fields) and every
list page, in parallel.

**Reuse the Discovery analysis.** Detail-1's Discovery JSON is already in
`.scrape/.work/{site_name}/analyze-page/` and the schema was built from it,
so that page+variant needs no re-analysis. Exception: if the schema gate went
beyond approving, dropping, or keeping fields (renames, description or
value-format edits, added fields), the JSON no longer matches the schema —
put that variant back on the launch list.

Build the launch list:

1. **Detail sample.** Pick the sample pages:
   - If there are list pages in `{site_path}/navigation/pages/`: one page —
     the first detail page that has both `raw.html` and `rendered.html`,
     falling back to detail-1.
   - Otherwise: detail-1 and detail-2.

   One subagent per sample page per HTML variant — skipping variants whose file
   doesn't exist (HTML-file-selection rule), variants covered by a reusable
   Discovery JSON, and, when `html_variant` is pinned, the other variant. At
   most 4 detail subagents.
2. **List pages.** One `--list-mode` subagent per page in
   `{site_path}/navigation/pages/`, raw variant, writing values directly
   into `{site_path}/{data_type}-list/values/`. Required whenever list pages
   exist — the user naming a data type ID is no reason to skip them: that ID
   is exactly what `{data_type}-list` is derived from, and the
   list-data-type decision below runs on field coverage, not intent
   guessing. Never drop a list-page subagent to make room for a detail page.

Launch every subagent in a single message with no tool calls in between — do
not wait for any result before launching the rest — and keep the launch at 5
subagents or fewer. If the harness cannot run them in parallel, run them one
after another. An empty detail part is normal (the only existing variant
was already analyzed in Discovery); if the whole launch list is empty,
continue with the Discovery JSON alone.

One subagent per line, description then prompt:

> `analyze detail-1 raw` — Run /scrape-analyze-page Extract data from {site_path}/{data_type}/pages/detail-1/raw.html using the schema in {site_path}/{data_type}/spec.json and save it into .scrape/.work/{site_name}/analyze-page/detail-1.raw.json
> `analyze list-1` — /scrape-analyze-page --list-mode Extract all {data_type} items from {site_path}/navigation/pages/list-1/raw.html using the schema in {site_path}/{data_type}/spec.json and save it into {site_path}/{data_type}-list/values/list-1.json
> `analyze list-2` — /scrape-analyze-page --list-mode Extract all {data_type} items from {site_path}/navigation/pages/list-2/raw.html using the schema in {site_path}/{data_type}/spec.json and save it into {site_path}/{data_type}-list/values/list-2.json
> ... (one per remaining list page, in the same message)

The schema path gives analyze-page the approved field names, descriptions,
and examples — so it extracts with the correct names and value formats.
The subagents launched here are the ONLY analysis subagents in the Validation
phase — a hard limit, not a preference: the rest of the phase works from the
bounded sample's outputs alone, even if the exploration downloaded more
detail pages than the sample analyzes.

If completed analyses disagree on a value's format (e.g. one list page labels
prices with a different currency than every other output), do not re-analyze.
When the correct form is already established by the other outputs, patch the
affected values file directly with a small script and mention the correction
when presenting the plan; when it is genuinely unclear, keep the values as
extracted and note the discrepancy in the plan instead.

### Decide whether to create a list-page data type

This decision applies only if list pages were found and analyzed in the parallel analysis above.

The decision is made by the field-coverage rule below alone — do not skip
or override it based on the user's requested data type: list-page
extraction delivers exactly the requested fields, just more cheaply (items
come straight from list pages, with no per-item detail requests).

Read the `{site_path}/{data_type}-list/values/list-*.json` files. For each file, check whether every `source: "requested"` field from the schema appears as a key in at least one item in the `values` array.

**If ALL requested fields are found in EVERY list-page values file:**

Set `list_spec_created = true`.

1. Write `{site_path}/{data_type}-list/spec.json`:
   ```json
   {
     "url": "{url}",
     "data_type": "{data_type}-list",
     "html_variant": "raw",
     "schema": {<same schema object as in {site_path}/{data_type}/spec.json>}
   }
   ```

2. Copy list pages into the new data type:
   ```bash
   mkdir -p {site_path}/{data_type}-list/pages
   for d in {site_path}/navigation/pages/list-*; do
     [ -d "$d" ] && cp -r "$d" {site_path}/{data_type}-list/pages/
   done
   ```

**Otherwise:** set `list_spec_created = false`. Proceed with detail-page extraction as normal — the `{data_type}-list/values/` directory may remain but will be ignored.

### Choose HTML variant

If `html_variant` was pinned in the plan, skip this comparison and use the pinned variant.

Compare raw vs rendered results across the bounded sample from `.scrape/.work/{site_name}/analyze-page/`.

For each page, compare `{page_id}.raw.json` and `{page_id}.rendered.json`:
- Which variant found more of the schema fields?
- Which fields are only in one variant?
- Do values differ between variants for the same field?

Use a single small Python script for this comparison. The script should load `{site_path}/{data_type}/spec.json`, enumerate `.scrape/.work/{site_name}/analyze-page/*.json`, compare only schema field coverage and values, print a concise summary, and recommend `raw` unless rendered consistently finds requested schema fields that raw misses.

**Raw is preferred by default** — it's faster, cheaper, and more reliable. Only use rendered if it finds schema fields that raw consistently misses, or if raw HTML is essentially empty (SPA site).

Present the comparison in the terminal:
```
HTML variant comparison:
  Both variants found: name, price, brand, description, image_url
  Only in rendered: reviews_count (3/3 pages), sale_price (2/3 pages)
  Only in raw: (none)
  Value differences:
    price: raw="$29.99", rendered="$24.99" (detail-1) — rendered may show sale price

  Recommendation: raw (all schema fields found)
  Note: rendered also has reviews_count, sale_price — say "use rendered" if you need these.
```

If it's clear which variant to use, use it. If it's not — for example when the raw view contains most of the fields but not all of them — ask the user which variant to use (question "Which HTML variant should I use for extraction?", header "HTML variant", options "Use raw" and "Use rendered", with the recommended one marked as such) and use the variant the user selects. Fallback: the recommended variant.

If both variants find all approved schema fields in the bounded sample, choose `raw` immediately.
If the chosen variant differs from what the spec has, update `{site_path}/{data_type}/spec.json` with the new `html_variant`.
Once the variant is chosen, continue directly to extracting values; do not start more analysis subagents.

### Extract values

If `list_spec_created` is true, skip the detail-value extraction below — values
were already written to `{data_type}-list/values/` by the parallel analysis.
The Navigation part below still applies.

Otherwise, use `extract_values.py` to build values from analysis files, filtered by the schema:

```bash
uv run --python 3.14 SKILL_DIR/scripts/extract_values.py \
  .scrape/.work/{site_name}/analyze-page/ \
  {site_path}/{data_type}/spec.json \
  --variant {html_variant} \
  -O {site_path}/{data_type}/values/
```

This writes fresh extractions from the analyzed detail-page sample.

#### Navigation

Write `{site_path}/navigation/spec.json` with the fixed navigation schema from `SKILLS_DIR/scrape/references/extraction-spec.md`, using the site URL, `nav_html_variant` (reported by the exploration), the URLs the crawl starts at, and a plain-English `scope` of what it must cover — the sections the user asked for, or the whole site when they asked for no limit.

Navigation values were already copied from the exploration output.

## Review

### Browser review

Follow the `browser_review` policy resolved during planning:
- `never` → skip to the Finalization phase.
- `always` → open the review (below) without asking.
- `ask` → tell the user the extraction stats first ("Extracted values for {N} detail pages and {M} navigation pages."), then ask whether they want a browser review (question "Open a browser review of the extracted values?", header "Browser review", options `Skip browser review` — "Continue without opening the browser." and `Open browser review` — "Review the values in the browser."). Fallback: skip the browser review. If the user picks `Skip browser review`, or you could not ask, go to the Finalization phase.

To open the review:

1. Make sure `{site_path}/{data_type}/spec.json` holds the current schema — the review page reads it from there.
2. Run the review and wait for the command to finish — it opens the review page in the browser, waits for the user to submit feedback, prints the feedback, and exits by itself:
   ```bash
   uv run --python 3.14 SKILL_DIR/scripts/run_review.py {site_path}/{data_type} .scrape/.work/{site_name} --variant {html_variant}
   ```
   On a re-review after changes, add `--changes '["Re-analyzed price across all pages","Dropped field isbn"]'` so the page shows what was done.

### Apply feedback

If the user reviews and provides feedback:

Apply all schema changes (drops, renames, description edits, kept fields → change source to "requested") per the source-of-truth rule — including the mirror into `{site_path}/{data_type}-list/spec.json` when `list_spec_created` is true. After mirroring, re-run the list-mode analysis subagents so the list values match the updated schema.

If feedback starts with `APPROVED`: apply its schema changes and skip to the Finalization phase. The user has signed off.

If feedback does NOT start with `APPROVED` (user clicked "Request changes"):
- Apply the schema changes
- For value corrections: re-run analysis for the corrected fields across ALL detail pages (using the chosen variant). Launch one subagent per page, in parallel if the harness allows it.

After re-analysis, re-extract values ("Extract values") and offer review again, passing a changes summary via `--changes`.

Loop the Review phase until the user approves or skips review.

## Finalization

### Present the finalized plan for approval

The schema is now validated — across all detail pages, with the chosen HTML
variant and real extracted values. Present the finalized plan and the concrete
next steps to the user, per the following template. Apply any overrides from
"Parse intent" so they appear pre-set, and omit the "Generate the spider" step
if the user asked to skip it (spider_create = no).

```markdown
## Scrape plan: {host} → {data_type}

**Target**
- URL: {target_url}
- Data type: {data_type}
- Extraction: {from list pages (all requested fields found there) | from detail pages}
- Site name: `{site_name}`
- Use Zyte API: {yes | no — note if already configured}

**Schema** ({N} fields, validated across {P} pages, variant `{html_variant}`)

Requested:
- `title` (string) — "A Light in the Attic"
- `price` (string) — "£51.77"

Discovered:
- `rating` (integer) — 3
- `category` (string) — "Poetry"
- `description` (string) — "It's hard to imagine a world without…" (2340 chars)
- `upc` (string) — "a897fe39b1053632"

**Next steps**

1. Create the Scrapy project
   - Directory: `{project_dir}`
   - Project: `{project_name}`
2. Generate the extraction code
3. Generate the spider, run it and fix possible issues
4. (Optional) Deploy the spider to Scrapy Cloud and run it there

**Outputs**
- Spec: `.scrape/{site_name}/`
- Project: `{project_dir}/`
```

If the user already approved the schema in the browser review (the Review phase), don't
re-open the fields — the plan reflects that approval, so focus this gate on the
next steps.

Ask the user whether they approve this plan or want to change anything presented in it.

On approval, continue to the report. On any redirect, apply it and re-present:
- **Schema change** (drop/keep/rename/edit) → update `{site_path}/{data_type}/spec.json`
- **Scope change** (a different section, added filtering, different start URLs) → update `scope`/`start_urls` in `{site_path}/navigation/spec.json`
- **Skip the spider** → drop the "Generate the spider" step and set spider_create = no
- **Settings** (project dir/name, Zyte, variant) → update the corresponding line

Loop until the user approves. If the user pre-authorised proceeding (e.g. "just
save it, don't check back"), skip only the wait: still present the plan above,
then continue straight to the report in the same message.

### Report

End the skill by emitting a plain-text final message reporting where the spec
was saved and the facts below. All values must reflect the user's **final**
choices after refinement, not the initial defaults. Whatever way the plan was
approved, the final message always contains the finalized plan followed by
this report — the plan is how the user sees the next steps — rather than a
free-form summary of the same facts.

```
Plan approved. Spec validated and saved to .scrape/{site_name}/.

Details:
- Data types: {comma-separated list, e.g. "product-list, navigation" when list_spec_created, else "product, navigation"}
- Project dir: {project_dir}
- Project name: {project_name}
- Create the spider: {yes | no}
- Start URLs: {comma-separated list}
- Scope: {scope}
- Using Zyte API: {yes | no}
```

When invoked standalone (not from `/scrape`), also tell the user how to
continue: `/scrapy-extra {site_path}/{data_type_entry} {project_dir}` per
entry in `Data types`, or `/scrape` for the full workflow.
