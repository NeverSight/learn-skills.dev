---
name: list-building
description: >
  Build targeted company lists for outbound campaigns using the Extruct API.
  Use when the user wants
  to: (1) find companies matching an ICP, (2) build a prospect or outbound
  list, (3) search for companies by description, (4) discover companies in a
  market segment, (5) create a target account list, (6) research a competitive
  landscape, (7) find lookalike companies from a seed list. Triggers on: "find
  companies", "build a list", "company search", "prospect list", "target
  accounts", "outbound list", "discover companies", "ICP search", "lookalike
  search", "seed company".
---

# List Building

Build company lists using Extruct API methods, guided by a decision tree. Reads from the company context file for ICP and seed companies.

## Official API Reference

- https://www.extruct.ai/docs

## Decision Tree

Before running any queries, determine the right approach:

```
Have a seed company from win cases or context file?
  YES → Method 1: Lookalike Search (pass seed domain)
  NO  ↓

New vertical, need broad exploration?
  YES → Method 2: Semantic Search (3-5 queries from different angles)
  NO  ↓

Need qualification against specific criteria?
  YES → Method 3: Discovery API (criteria-scored async research)
  NO  ↓

Need maximum coverage?
  YES → Combine Search + Discovery (~15% overlap expected)
```

## Before You Start

Read the company context file if it exists:

```
claude-code-gtm/context/{company}_context.md
```

Extract:
- **ICP profiles** — for query design and filters
- **Win cases** — for seed companies in lookalike mode
- **DNC list** — domains to exclude from results. If no DNC list exists in the context file, ask the user: (1) run an Extruct search for competitors to auto-populate, (2) accept a CSV of existing customers/partners, or (3) skip for now

Also check for a hypothesis set at `claude-code-gtm/context/{vertical-slug}/hypothesis_set.md`. If it exists, use the **Search angle** field from each hypothesis to design search queries — these are pre-defined query suggestions tailored to each pain point.

## Environment

| Variable | Service |
|----------|---------|
| `EXTRUCT_API_TOKEN` | Extruct API |

Before making API calls, check that `EXTRUCT_API_TOKEN` is set by running `test -n "$EXTRUCT_API_TOKEN" && echo "set" || echo "missing"`. If missing, ask the user to provide their Extruct API token and set it via `export EXTRUCT_API_TOKEN=<value>`. Do not proceed until confirmed.

Base URL: `https://api.extruct.ai/v1`

## Method 1: Lookalike Search

Use when you have a seed company (from win cases, existing customers, or user input).

**Endpoint:** `GET /companies/{identifier}/similar` where `identifier` is a domain or company UUID.

**Key params:**
- `filters` — JSON with `include` (size, country) and `range` (founded)
- `limit` — max results (default 100, up to 200)
- `offset` — for pagination

**Response fields:** `name`, `domain`, `short_description`, `founding_year`, `employee_count`, `hq_country`, `hq_city`, `relevance_score`

**When to use lookalike:**
- You have a happy customer and want more like them
- Context file has win cases with domains
- User says "find companies similar to X"

**Tips:**
- Run multiple similar-company searches with different seed companies for broader coverage
- Combine with filters to constrain geography or size
- Deduplicate across runs by domain
- Default to `limit=100`; increase up to `200` when broader coverage is needed

## Method 2: Semantic Search — Fast, Broad

**Endpoint:** `GET /companies/search`

**Key params:**
- `q` — natural language query describing the target companies
- `filters` — JSON with `include` (size, country) and `range` (founded)
- `limit` — max results (default 100, up to 200)

**Response fields:** `name`, `domain`, `short_description`, `founding_year`, `employee_count`, `hq_country`, `hq_city`, `relevance_score`

**Query strategy:**
- Write 3-5 queries per campaign, each from a different angle on the same ICP
- Describe the product/use case, not the company type
- Deduplicate across queries by domain — overlap is expected
- Default to `limit=100` per query; increase up to `200` when needed
- Target 200-800 companies total across all queries

**Filters:** See [references/search-filters.md](references/search-filters.md)

## Method 3: Discovery API — Deep, Qualified

**Endpoint:** `POST /discovery_tasks`

**Key params:**
- `query` — 2-3 sentence description of the ideal company (like a job description)
- `desired_num_results` — target result count (default 50 for first pass)
- `criteria` — list of `{ key, name, criterion }` objects for auto-grading (up to 5)

**Poll:** `GET /discovery_tasks/{task_id}` — status: `created | in_progress | done | failed`. Poll every 60 seconds.

**Fetch results:** `GET /discovery_tasks/{task_id}/results` with `limit` and `offset` params.

**Response fields:** `company_name`, `company_website`, `company_description`, `relevance` (0-100), `scores` (per-criteria grade 1-5 with explanation), `founding_year`

**Query strategy:**
- Write queries like a job description — 2-3 sentences describing the ideal company
- Use criteria to auto-qualify — each company gets graded 1-5 per criterion
- Default `desired_num_results=50` for first pass; expand after quality review
- Use up to 5 criteria per task; keep criteria focused and non-overlapping
- Run separate tasks for different ICP segments
- Scans many candidates to find qualified matches — runtime depends on query scope
- Up to 250 results per task

See [references/discovery-api.md](references/discovery-api.md) for full parameters.

## Upload to Table

Create a `company` kind table via `POST /tables` with a single input column (`kind: "input"`, `key: "input"`). Extruct auto-enriches each domain with a Company Profile.

Upload domains in batches of 50 via `POST /tables/{table_id}/rows`. Each row: `{ "data": { "input": "domain.com" } }`. Add 0.5s delay between batches.

Pass `"run": true` in the rows payload to trigger agent columns on upload.

## Re-run After Enrichment

After the `list-enrichment` skill adds data points to this list, consider re-running list building using enrichment insights as Discovery criteria. For example:

- If enrichment reveals that "companies using legacy ERP" are the best fit, create a Discovery task with that as a criterion
- If enrichment shows a geographic cluster, run a Search with tighter geo filters
- This creates a feedback loop: list → enrich → learn → refine list

## Result Size Guidance

| Campaign stage | Target list size | Method |
|---------------|-----------------|--------|
| Exploration | 50-100 | Search (2-3 queries) |
| First campaign | 200-500 | Search (5 queries) + Discovery |
| Scaling | 500-2000 | Discovery (high desired_num_results) + multiple Search |

## Workflow

### Step 0: Verify API reference

1. Read local references: [references/discovery-api.md](references/discovery-api.md), [references/search-filters.md](references/search-filters.md)
2. Fetch live docs: https://www.extruct.ai/docs
3. Compare endpoints, params, and response fields
4. If discrepancies found:
   - Update the local reference file(s)
   - Flag changes to the user before proceeding
5. Proceed with the skill workflow

### Steps

1. Read context file for ICP, seed companies, and DNC list
2. Follow the decision tree to pick the right method
3. Draft queries (3-5 for Search, 1-2 for Discovery)
4. Run queries and collect results
5. Deduplicate across all results by domain
6. Remove DNC domains
7. Upload to Extruct company table for auto-enrichment
8. Add agent columns if user needs custom research
9. Ask user for preferred output: Extruct table link, local CSV, or both
