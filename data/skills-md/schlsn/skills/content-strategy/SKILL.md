---
name: content-strategy
description: "Use when the user wants to create a topical map, content pillars, topic clusters, or a phased content calendar. Triggers: \"content strategy\", \"topical map\", \"content pillars\", \"topic clusters\", \"what should I write\", \"content plan\", \"content calendar\", \"blog strategy\". This skill produces a structured blueprint — it does NOT write the actual articles. For writing individual pieces, see copywriting. For SEO audits, see seo-audit."
metadata:
  version: 2.0.0
---

# Topical Map & Content Pillars

You are a strategic SEO content planner. Your goal is to produce a complete **topical map** — a structured blueprint that organises a website's content into pillars and clusters so that search engines perceive the site as a topical authority. The map tells the user **what to write, which keywords to target, and how to structure the site**; it does not produce the articles themselves.

---

## Phase 1: Data Collection & Input Definition

Before building the map you need context and data. A quality topical map is built from market analysis, not guesswork.

### 1.1 Core Business Inputs (Ask if not provided)

| Input | Example |
|-------|---------|
| **Niche / Industry** | IVF clinics, SaaS project management, coffee e-shop… |
| **Target Audience** | Couples dealing with infertility aged 30–42, CTOs of small teams… |
| **Content Goals** | Organic traffic, leads, authority building, affiliate revenue… |
| **Own Domain** (optional) | pronatal.cz — not needed if planning a brand-new site |
| **Competitor Domains** (optional) | gennet.cz, ivfcube.cz — for gap analysis |
| **Language & Market** | cs/CZ, en/US, de/DE… |

### 1.2 Data Sources for Deep Research

A quality map relies on **real SEO data**, not guessing:

| Source | What It Provides | Relevant Skill |
|--------|-----------------|----------------|
| **Google Ads Keyword Planner** | Search volume, CPC, competition, keyword ideas | `google-ads-keyword-planner` |
| **Google Autocomplete / Suggest** | Long-tail variations, intent signals, user questions | `google-autocomplete` |
| **Google SERP Scrape** | Organic results, PAA (People Also Ask), Related Searches | `google-serp` |
| **DataForSEO Competitors** | Competitor keywords (top 20), search volume, KD, intent | `dataforseo-competitors` |
| **Google Search Console** | CTR, positions, impressions for existing sites | `duckdb-keywords` (table `search_console`) |
| **DuckDB Keywords** | Central storage for all keyword data per project | `duckdb-keywords` |
| **Keyword Categorization** | Semantic clustering of keywords into categories | `keyword-categorization` |
| **PostgreSQL (Hetzner)** | SERP data, competitor keywords — `seo_kws.*` and `seo.competitor_keywords` | `google-serp`, `dataforseo-competitors` |

### 1.3 Customer & Qualitative Data

- **Sales call transcripts** — look for the exact words customers use
- **Support tickets** — recurring questions and frustrations
- **Surveys / NPS** — specific problems and wishes
- **Forums & communities** — Reddit, Quora, industry groups (real frustrations and questions)

### 1.4 Data Collection Workflow (Database-First)

**Always check existing data in PostgreSQL and DuckDB before fetching anything new.** Only run fetch scripts for data sources where no recent data (< 30 days) exists.

#### Step 1 — Audit existing data

Run these queries via SSH to see what data already exists for the project:

```bash
# Competitor keywords in PostgreSQL
ssh hetzner-n8n "docker exec n8n-stack-postgres-1 psql -U n8n -d n8n -c \"
  SELECT competitor_domain, COUNT(*) AS keywords, MAX(downloaded_at) AS last_fetch,
         NOW()::date - MAX(downloaded_at) AS days_old
  FROM seo.competitor_keywords
  WHERE project = '<PROJECT>'
  GROUP BY competitor_domain
  ORDER BY last_fetch DESC;
\""

# SERP data in PostgreSQL
ssh hetzner-n8n "docker exec n8n-stack-postgres-1 psql -U n8n -d n8n -c \"
  SELECT j.id, j.name, j.status, j.total_keywords, j.completed_keywords,
         c.slug AS client, j.created_at::date
  FROM seo_kws.jobs j
  JOIN seo_kws.clients c ON c.id = j.client_id
  WHERE c.slug = '<PROJECT>'
  ORDER BY j.id DESC LIMIT 10;
\""

# DuckDB local data
python3 duckdb-keywords/scripts/kw_db.py tables <PROJECT>
```

#### Step 2 — Identify gaps

Based on the audit, determine which data sources are **missing or stale** (> 30 days old):

| Data Source | Where to Check | What's Missing? |
|-------------|---------------|-----------------|
| Competitor keywords | `seo.competitor_keywords` (PostgreSQL) | No rows for key competitors, or `downloaded_at` > 30 days |
| SERP organic + PAA + Related | `seo_kws.serp_organic` / `serp_paa` / `serp_related` (PostgreSQL) | No completed job for the project, or old data |
| Google Ads / Keyword Planner | `duckdb-keywords` tables `google_ads`, `keyword_planner` | Empty tables or old `downloaded_at` |
| Autocomplete suggestions | `duckdb-keywords` table `suggestions` | Empty table |
| Search Console | `duckdb-keywords` table `search_console` | Empty table (only available for existing sites) |

#### Step 3 — Fetch only what's missing

For each gap identified above, run the corresponding skill:

1. **Missing autocomplete data** → Run `google-autocomplete` for 5–10 seed keywords
2. **Missing search volumes** → Run `google-ads-keyword-planner` with seed keywords
3. **Missing competitor data** → Run `dataforseo-competitors` for 2–3 competitors (respects 30-day freshness check)
4. **Missing SERP data** → Run `google-serp` (ingest 20–30 keywords via n8n webhook)
5. **Import any new results** into `duckdb-keywords` project

#### Step 4 — Cluster and analyse

6. **Run `keyword-categorization`** on the merged CSV → semantic clusters as the foundation for pillars

---

## Phase 2: Defining Content Pillars

The goal is to identify **3–5 main pillars** (up to 10 for larger sites) — overarching topics in which you want to be perceived as an authority. Pillars become your "Hub" pages.

### 2.1 How to Identify the Right Pillars

| Approach | Guiding Question |
|----------|-----------------|
| **Product-led** | What main categories of problems does your product solve? |
| **Audience-led** | What does your ideal customer need to learn to succeed? |
| **Search-led** | Which broad, high-volume topics have the biggest potential in your niche? |
| **Competitor-led** | Which topics are your competitors building authority on? |

### 2.2 Good Pillar Criteria

Each pillar must be:
- ✅ **Broad enough** — can be broken down into dozens of subtopics
- ✅ **Highly relevant** — directly related to your business
- ✅ **Searched** — has search volume and/or social interest
- ✅ **Distinct** — clearly differentiated from other pillars

### 2.3 Pillar Output Format

For each pillar, provide:

| Field | Description |
|-------|-------------|
| Pillar name | Short, natural name (not a raw keyword) |
| Primary keyword | Target keyword for the Hub page |
| Search Volume | Monthly search volume |
| KD (Keyword Difficulty) | Difficulty score (0–100) |
| Planned cluster articles | Number of articles planned under this pillar |
| Product connection | How the pillar naturally leads to your product/service |

---

## Phase 3: Building Article Clusters

Around each pillar, create a cluster of supporting articles targeting specific long-tail keywords. The map should contain **50–100+ article ideas** to start with.

### 3.1 Classification by Buyer Stage

| Stage | Query Type | Modifiers | Example |
|-------|-----------|-----------|---------|
| **Awareness** | Informational | what is, how to, guide, introduction | "What is IVF and how does it work" |
| **Consideration** | Comparative | best, alternatives, vs, comparison | "Best IVF clinics in Prague" |
| **Decision** | Conversion | pricing, reviews, buy, order | "IVF clinic pricing 2026" |
| **Implementation** | Practical | template, tutorial, setup, step-by-step | "IVF preparation step by step" |

### 3.2 Distribution Type

| Type | Characteristics | Example |
|------|----------------|---------|
| **Searchable** | Keyword-targeted, answers a query, optimised for Google | "How does artificial insemination work" |
| **Shareable** | Original data, thought leadership, myth-busting, social-first | "5 IVF myths people still believe" |

### 3.3 Article Output Format

For each article in a cluster, provide:

| Field | Description |
|-------|-------------|
| Parent pillar | Which pillar this article belongs to |
| Article title | Working title |
| Target keyword | Primary keyword |
| Search Volume | Monthly search volume |
| KD (Keyword Difficulty) | Difficulty (0–100) |
| Buyer stage | Awareness / Consideration / Decision / Implementation |
| Distribution type | Searchable / Shareable / Both |
| Content type | Informational, commercial, lead magnet, case study, data-driven… |
| Publishing phase | 1 / 2 / 3 / 4 (see Phase 5) |

---

## Phase 4: Semantic Structure & Internal Linking

This step is **critical** for search engines to correctly understand the relationships between your content.

### 4.1 Linking Rules

```
Pillar A (Hub)
  ↑ ↑ ↑
  │ │ │
  ├── Cluster article A1  ──────────╮
  ├── Cluster article A2  ─── cross-link ──→  Cluster article B3 (different pillar)
  └── Cluster article A3  ──────────╯
```

1. **Upward linking**: All cluster articles link to their parent pillar page (Hub)
2. **Cross-linking**: Articles also link to each other where topics naturally overlap — even across different pillars
3. **URL structure**: In most cases `/blog/article-title` suffices. Use dedicated structures like `/topic/subtopic` only for multi-level pillar guides

### 4.2 Structure Visualisation

For each pillar, provide:

```
Pillar: [Pillar Name]
Hub page: /blog/main-topic
├── /blog/cluster-article-1  (Awareness, KD 15, SV 320)
├── /blog/cluster-article-2  (Consideration, KD 25, SV 210)
├── /blog/cluster-article-3  (Decision, KD 40, SV 150)
│   └── cross-link → /blog/article-from-another-pillar
└── /blog/cluster-article-4  (Implementation, KD 10, SV 90)
```

---

## Phase 5: Prioritisation & Content Calendar

### 5.1 Scoring System for Each Idea

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Customer Impact** | 40% | How often the topic appears in research; how strong a pain point it addresses |
| **Content-Market Fit** | 30% | How naturally the topic leads to your product; whether you have unique expertise |
| **Search Potential (SEO)** | 20% | Monthly search volume and competition level |
| **Resource Requirements** | 10% | Time, data, and assets needed to create the content |

### 5.2 Four-Phase Content Calendar

| Phase | Name | What It Contains | Goal |
|-------|------|-----------------|------|
| **1** | Quick Wins | Highly relevant informational content with low KD (under 30) | Earn initial traffic, start building search engine trust |
| **2** | Core Pillars | Launch all 3–5 (up to 10) Hub pages targeting broad, high-volume terms | Capture internal links from Quick Wins, establish pillar structure |
| **3** | Expansion & Commercial | Consideration + Decision articles: comparisons, alternatives, reviews, use-cases | Move closer to conversion, monetisation |
| **4** | Authority Building | Hardest keywords (high KD), extensive case studies, data analyses, thought leadership | Attack competitive terms that require an established domain |

---

## Overall Output Format

The final topical map is delivered as a **CSV file** (or table for Google Sheets / Excel) with these columns:

| Column | Description |
|--------|-------------|
| `pillar` | Pillar name |
| `pillar_keyword` | Main keyword of the pillar |
| `article_title` | Working title of the article |
| `target_keyword` | Target keyword for the article |
| `search_volume` | Monthly search volume |
| `keyword_difficulty` | KD score (0–100) |
| `buyer_stage` | Awareness / Consideration / Decision / Implementation |
| `content_type` | blog, guide, comparison, review, case-study, lead-magnet… |
| `distribution` | Searchable / Shareable / Both |
| `phase` | 1 / 2 / 3 / 4 |
| `priority_score` | Overall score (see 5.1) |
| `internal_links_to` | List of URLs the article links to |
| `url_slug` | Proposed URL slug |

In addition to the CSV, deliver a **visual overview** (mermaid diagram or structured text tree) mapping the relationships: pillar → clusters → cross-links.

---

## Workflow: Step by Step

1. **Gather inputs** (Phase 1) — ask about niche, audience, goals, competitors, language/market
2. **Audit existing data** — query PostgreSQL (`seo.competitor_keywords`, `seo_kws.*`) and DuckDB project tables
3. **Identify gaps** — determine which data sources are missing or stale (> 30 days)
4. **Fetch only what's missing** — run the corresponding skills:
   - `google-autocomplete` → long-tail variations
   - `google-ads-keyword-planner` → search volume, CPC
   - `dataforseo-competitors` → competitor keywords and gaps
   - `google-serp` → PAA, Related Searches, SERP landscape
5. **Import new data** into `duckdb-keywords` project
6. **Run `keyword-categorization`** → semantic clusters
7. **Define pillars** (Phase 2) based on clusters and data
8. **Create article clusters** (Phase 3) with buyer-stage classification
9. **Design internal linking** (Phase 4)
10. **Score and prioritise** (Phase 5) → 4-phase calendar
11. **Export CSV** and visual overview

---

## Data Sources & Related Skills

| Skill | Role in Topical Map |
|-------|---------------------|
| `google-autocomplete` | Seed-keyword expansion, question queries |
| `google-ads-keyword-planner` | Search volume, CPC, competition index |
| `dataforseo-competitors` | Competitor gap analysis, ranked keywords |
| `google-serp` | SERP landscape, PAA, Related Searches |
| `duckdb-keywords` | Central SQL database for all keyword data |
| `keyword-categorization` | Semantic clustering of keywords into Main/Subcategories |
| `copywriting` | For writing individual articles |
| `seo-audit` | For technical SEO and on-page optimisation |
| `programmatic-seo` | For programmatic content creation at scale |

---

## Important Rule

> **A topical map creates the strategy** — it tells you what to write, which keywords to target, and how to structure the site. The actual writing is up to you (or the `copywriting` skill).
