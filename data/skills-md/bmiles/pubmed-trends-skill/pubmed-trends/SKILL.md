---
name: pubmed-trends
description: >
  Query PubMed publication trends via x402 micropayments to identify emerging research fields,
  compare therapeutic areas, detect publication spikes, find key papers, and profile authors.
  Use when analyzing biotech/pharma landscapes, writing grant applications, evaluating drug targets,
  or researching scientific trends. Requires the x402 skill from coinbase/agentic-wallet-skills
  for payment commands.
---

# PubMed Trends API

Pay-per-query research intelligence from 37M+ PubMed articles. No API keys, no subscriptions — just USDC micropayments on Base via x402.

**Base URL:** `https://pubmed.sekgen.xyz`

**Companion skill:** Install `x402` from `coinbase/agentic-wallet-skills` for payment commands.

## Endpoints

### GET /api/v1/snapshot — $0.01

Single-year publication count. Cheapest option for quick lookups.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `query` | Yes | — | PubMed search query |
| `year` | No | current year | Year to query |

```bash
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/snapshot?query=CRISPR&year=2025'
```

Returns `count`, `total_pubmed`, `proportion` (share of all PubMed articles).

### GET /api/v1/trends — $0.01

Year-by-year publication counts with growth analytics over a range.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `query` | Yes | — | PubMed search query |
| `start_year` | No | current - 10 | First year |
| `end_year` | No | current year | Last year |
| `source` | No | pubmed | `pubmed` or `openalex` |

```bash
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/trends?query=GLP-1+agonist&start_year=2015'
```

Returns yearly `count`, `yoy_growth`, plus analytics: `cagr`, `trend_direction` (growing/declining/stable/emerging), `peak_year`, `acceleration`.

### GET /api/v1/compare — $0.02

Compare publication trends across 2–5 search terms. Identifies which field is growing fastest and detects crossover points.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `terms` | Yes | — | Comma-separated search terms (2–5) |
| `start_year` | No | current - 10 | First year |
| `end_year` | No | current year | Last year |
| `source` | No | pubmed | `pubmed` or `openalex` |

```bash
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/compare?terms=CAR-T,bispecific+antibodies,antibody+drug+conjugate'
```

Returns per-term series with `cagr` and `trend_direction`, plus `ranking_by_growth` and `crossover_years` (when one term overtook another).

### GET /api/v1/pulse — $0.02

Real-time publication pulse with 7d/30d/90d windows and year-over-year change.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `query` | Yes | — | PubMed search query |

```bash
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/pulse?query=prime+editing'
```

Returns `current` and `year_ago` counts for 7d/30d/90d windows, plus `change` (fractional, e.g. 0.35 = 35% increase YoY).

### GET /api/v1/keypapers — $0.03

Scored key papers for a query within a time window. Papers are ranked by a composite score based on journal prestige, publication type, MeSH relevance, and citation impact (via OpenAlex).

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `query` | Yes | — | PubMed search query |
| `start_year` | No | current - 5 | First year |
| `end_year` | No | current year | Last year |

```bash
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/keypapers?query=base+editing&start_year=2023&end_year=2025'
```

Returns scored papers with `pmid`, `title`, `journal`, `pub_year`, `pub_type`, `score`, `score_breakdown` (top_journal, review_or_trial, mesh_major_topic, multi_strategy_hit, relevance_rank, citation_impact), `cited_by_count`, `fwci` (field-weighted citation impact), `open_access` status, and `authors_enriched` (name, institution, country).

### GET /api/v1/digest — $0.08

Full research digest combining scored key papers, MeSH term landscape, and frequent authors. The most comprehensive single-call endpoint.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `query` | Yes | — | PubMed search query |
| `start_year` | No | current - 5 | First year |
| `end_year` | No | current year | Last year |

```bash
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/digest?query=NF2+schwannomatosis+treatment&start_year=2022&end_year=2025'
```

Returns everything from `/keypapers` plus `mesh_terms` (array of MeSH descriptors across the result set) and `authors` (recurring authors with appearance counts).

### GET /api/v1/hottest-weekly — $0.05

Hottest topics in a category ranked by weekly spike ratio (last 7d vs 30d average). Use `category` for PubMed curated terms (default) or `topic` + `source=openalex` for free-text search.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `category` | Yes* | — | See categories below |
| `topic` | Yes* | — | Free-text topic (when `source=openalex`) |
| `source` | No | pubmed | `pubmed` or `openalex` |

*One of `category` or `topic` required depending on source.

```bash
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/hottest-weekly?category=oncology'
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/hottest-weekly?topic=microbiome&source=openalex'
```

Returns topics sorted by `spike_ratio`. Values >1.0 mean more activity than usual this week.

### GET /api/v1/emerging — $0.05

Scan a category for topics with accelerating publication rates. Use `category` for PubMed curated terms (default) or `topic` + `source=openalex` for free-text search.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `category` | Yes* | — | See categories below |
| `topic` | Yes* | — | Free-text topic (when `source=openalex`) |
| `source` | No | pubmed | `pubmed` or `openalex` |
| `window_years` | No | 3 | Years to evaluate growth |
| `min_growth_rate` | No | 0.3 | Minimum CAGR threshold (0.3 = 30%) |
| `limit` | No | 10 | Max results |

*One of `category` or `topic` required depending on source.

```bash
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/emerging?category=gene+therapy&min_growth_rate=0.5'
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/emerging?topic=CRISPR&source=openalex'
```

Returns topics meeting the growth threshold, sorted by `recent_cagr`.

### GET /api/v1/trending-subtopics — $0.05

Discover which sub-topics within a research field are growing fastest. Uses OpenAlex topic breakdown over a multi-year window.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `query` | Yes | — | Research field to decompose |
| `window` | No | 3 | Window size in years (2–5) |
| `limit` | No | 10 | Max results (1–25) |

```bash
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/trending-subtopics?query=ulcerative+colitis&window=3'
```

Returns sub-topics with `topic_id`, `topic_name`, per-year `counts`, `cagr`, `trend_direction`, `latest_year_count`, and `growth_score`.

### GET /api/v1/explore — $0.10

Discover interesting research signals. Two modes:

1. **With `topics` param** — OpenAlex multi-domain scan: searches topics, computes spike_ratio x CAGR, ranks by explore_score.
2. **Without `topics`** — D1 MeSH anomaly detection: z-score anomalies from stored baselines.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `topics` | No | — | Comma-separated research topics to scan (max 4) |
| `limit` | No | 5 | Max results (1–20) |
| `min_z_score` | No | 2.0 | Minimum z-score for anomaly mode (without `topics`) |
| `days` | No | 7 | Lookback days for anomaly mode (1–30, without `topics`) |

```bash
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/explore?topics=neurodegeneration,epigenetics&limit=5'
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/explore'
```

Returns ranked results with `explore_score`, `spike_ratio`, `cagr_3y`, `trend_direction`, and `latest_year_count`.

### GET /api/v1/author — $0.02

Author analytics profile powered by OpenAlex. Returns citation metrics, institutional affiliation, and publication trajectory.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `name` | Yes* | — | Author name to look up |
| `orcid` | Yes* | — | ORCID identifier (alternative to name) |

*One of `name` or `orcid` required.

```bash
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/author?name=David+Liu'
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/author?orcid=0000-0001-8277-943X'
```

Returns `name`, `orcid`, `works_count`, `cited_by_count`, `h_index`, `i10_index`, `current_institution` (name, country), `top_topics`, `counts_by_year` (works, cited_by per year).

## Categories

Used by `/hottest-weekly` and `/emerging` (PubMed mode):

- **oncology** — CAR-T, bispecific antibodies, ADCs, checkpoint inhibitors, liquid biopsy, KRAS inhibitors, PARP inhibitors, radiopharmaceuticals, cancer vaccines, spatial transcriptomics
- **neuroscience** — anti-amyloid antibodies, brain-computer interfaces, psychedelic therapy, GLP-1 neurodegeneration, antisense oligonucleotides, deep brain stimulation
- **immunology** — mRNA vaccines, CAR-T autoimmune, JAK inhibitors, regulatory T cells, microbiome immunotherapy, complement inhibitors
- **gene therapy** — CRISPR, base editing, prime editing, AAV gene therapy, lipid nanoparticle mRNA, epigenome editing, RNA interference
- **cardiology** — PCSK9 inhibitors, SGLT2 inhibitors, cardiac gene therapy, lipoprotein(a) inhibitors, AI cardiac imaging, wearable ECG

## Free Endpoints

These do not require payment:

- `GET /` — Service info and pricing
- `GET /health` — Health check
- `GET /docs` — Interactive documentation (HTML, or Markdown with `Accept: text/markdown`)
- `GET /llms.txt` — Machine-readable documentation

## Example Workflows

**Quick fact check ($0.01):**
> "How much CRISPR research was published in 2025?"
```bash
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/snapshot?query=CRISPR&year=2025'
```

**Technology race ($0.02):**
> "Is base editing overtaking traditional CRISPR?"
```bash
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/compare?terms=CRISPR+gene+editing,base+editing,prime+editing&start_year=2018'
```

**Weekly research briefing ($0.10):**
> "What's spiking in oncology and neuroscience right now?"
```bash
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/hottest-weekly?category=oncology'
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/hottest-weekly?category=neuroscience'
```

**Drug target validation ($0.03):**
> "Is GLP-1 for neurodegeneration actually gaining traction?"
```bash
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/trends?query=GLP-1+agonist+neurodegeneration&start_year=2018'
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/pulse?query=GLP-1+agonist+neurodegeneration'
```

**Deep dive into a disease area ($0.13):**
> "What are the key papers and sub-topics for NF2 schwannoma treatment?"
```bash
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/keypapers?query=NF2+schwannoma+treatment&start_year=2022&end_year=2025'
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/trending-subtopics?query=neurofibromatosis+type+2&window=3'
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/pulse?query=NF2+schwannoma+treatment'
```

**Full research digest ($0.08):**
> "Give me a comprehensive overview of NF2 schwannomatosis treatment research"
```bash
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/digest?query=NF2+schwannomatosis+treatment&start_year=2022&end_year=2025'
```

**Author profiling ($0.02):**
> "Who is Scott Plotkin and what's his publication record?"
```bash
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/author?name=Scott+Plotkin'
```

**Discovery mode ($0.10):**
> "What's interesting happening across neurodegeneration and epigenetics?"
```bash
awal x402 pay 'https://pubmed.sekgen.xyz/api/v1/explore?topics=neurodegeneration,epigenetics&limit=5'
```

## Error Handling

- **402** — Payment required. Ensure you're authenticated (`awal auth login`) with USDC balance.
- **400** — Invalid parameters. Check required fields and constraints (max 50-year range, 2–5 terms for compare).
- **502** — Upstream NCBI error. Retry after a moment.
- **503** — Service temporarily unavailable. Retry after a moment.
