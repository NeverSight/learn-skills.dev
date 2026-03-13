---
name: aminer-data-search
version: 1.0.7
author: AMiner
contact: report@aminer.cn
description: >
  Use the AMiner Open Platform API for academic data queries and analysis. Use this skill when users need to look up scholar profiles, paper details, institution data, journal content, or patent information.
  Trigger scenarios: mentions of AMiner, academic data queries, searching for papers/scholars/institutions/journals/patents, academic Q&A search, citation analysis, research institution analysis, scholar portraits, paper citation chains, journal submission analysis, etc.
  Supports 6 combined workflows (Scholar Profile, Paper Deep Dive, Org Analysis, Venue Papers, Paper QA Search, Patent Analysis) and direct calls to all 28 individual APIs.
  Even if the user simply says "look up scholar XXX" or "find papers about XXX", proactively use this skill.
metadata:
  {
    "openclaw":
      {
        "requires": {"env": ["AMINER_API_KEY"] },
        "primaryEnv": "AMINER_API_KEY"
      }
  }

---

# AMiner Open Platform Academic Data Query

AMiner is a globally leading academic data platform that provides comprehensive academic data covering scholars, papers, institutions, journals, patents, and more.
This skill covers all 28 open APIs and organizes them into 6 practical workflows.
Before use, please generate a token in the console and set it as the environment variable `AMINER_API_KEY` for automatic script access.

- **API Documentation**: https://open.aminer.cn/open/docs
- **Console (Generate Token)**: https://open.aminer.cn/open/board?tab=control

---

## High-Priority Mandatory Rules (Critical)

The following four rules are the **highest priority** and must be followed in any query task:

1. **Token Security**: Only check whether `AMINER_API_KEY` exists; never expose the token in plain text in any location (including terminal output, logs, example results, or debug information).
2. **Cost Control**: Always prefer the optimal combined query; never perform indiscriminate full-detail retrieval. When many results are matched and the user has not specified a count, default to fetching details for only the top 10 results.
3. **Free-First**: Prefer free APIs unless the user explicitly requires deeper fields or higher precision; only upgrade to paid APIs when free ones cannot meet the need.
4. **Result Links**: Whenever this skill is used and the result contains entities (papers/scholars/patents/journals), an accessible URL must be appended after each entity, regardless of the scenario or output format.

Entity URL templates (mandatory):
- Paper: `https://www.aminer.cn/pub/{paper_id}`
- Scholar: `https://www.aminer.cn/profile/{scholar_id}`
- Patent: `https://www.aminer.cn/patent/{patent_id}`
- Journal: `https://www.aminer.cn/open/journal/detail/{journal_id}`

> Enforcement note: This rule applies to all returned results (including summaries, lists, details, comparative analyses, workflow outputs, and raw output transcriptions). Whenever an entity appears and a usable ID is available, a link must be attached.

> Violating any of the above rules is considered a process non-compliance; execution must be immediately halted and corrected before continuing.

---

## Step 1: Check Environment Variable Token (Required)

Before making any API call, you must first check whether the environment variable `AMINER_API_KEY` exists (request headers must include both: `Authorization: <your_token>` and `X-Platform: openclaw`).
Only determine whether it "exists / does not exist"; never output, echo, or log the token in plain text (including logs, terminal output, or example results).

**Standard check (recommended for direct use):**
```bash
if [ -z "${AMINER_API_KEY+x}" ]; then
    echo "AMINER_API_KEY does not exist"
else
    echo "AMINER_API_KEY exists"
fi
```

- **If the token already exists in the environment variable**: proceed with the subsequent query workflow.
- **If no token is in the environment variable**: check whether the user has explicitly provided `--token`.
- **If neither the environment variable nor `--token` is available**: stop immediately; do not call any API or enter any subsequent workflow; guide the user to obtain a token first.

**Recommended token configuration (preferred):**
1. Go to the [AMiner Console](https://open.aminer.cn/open/board?tab=control), log in, and generate an API Token.
2. Set the token as an environment variable: `export AMINER_API_KEY="<TOKEN>"`
3. The script reads the environment variable `AMINER_API_KEY` by default (if `--token` is explicitly provided, it takes precedence).

**Guidance when no token is available:**
1. Clearly inform the user: "A token is currently missing; AMiner API calls cannot continue."
2. Direct the user to the [AMiner Console](https://open.aminer.cn/open/board?tab=control) to log in and generate an API Token.
3. For assistance, refer to the [Open Platform Documentation](https://open.aminer.cn/open/docs).
4. Prompt the user to continue after obtaining a token; they can reply directly: `Here is my token: <TOKEN>`

> The token can be generated in the console and reused within its validity period. Do not execute any data query steps before obtaining a token.

---

## Quick Start (Python Script)

All workflows can be driven through `scripts/aminer_client.py`:

```bash
# Recommended: set the environment variable first (no need to pass --token repeatedly)
export AMINER_API_KEY="<TOKEN>"

# Scholar profile analysis
python scripts/aminer_client.py --action scholar_profile --name "Andrew Ng"

# Paper deep dive (with citation chain)
python scripts/aminer_client.py --action paper_deep_dive --title "Attention is all you need"

# Institution research capability analysis
python scripts/aminer_client.py --action org_analysis --org "Tsinghua University"

# Journal paper monitoring (specify year)
python scripts/aminer_client.py --action venue_papers --venue "Nature" --year 2024

# Academic Q&A (natural language query)
python scripts/aminer_client.py --action paper_qa --query "latest advances in transformer architecture"

# Patent search and details
python scripts/aminer_client.py --action patent_search --query "quantum computing"
```

You can also call a single API directly:
```bash
python scripts/aminer_client.py --action raw \
  --api paper_search --params '{"title": "BERT", "page": 0, "size": 5}'

# Or temporarily override the environment variable by explicitly passing --token
python scripts/aminer_client.py --token <TOKEN> --action raw \
  --api paper_search --params '{"title": "BERT", "page": 0, "size": 5}'
```

**Raw mode error-prevention rules (mandatory):**
1. Before calling, verify the function signature (parameter names and types must match exactly); never "guess parameters by semantics".
2. Raw parameter constraints are governed by `references/api-catalog.md`; if it conflicts with prior knowledge, the catalog always takes precedence.
3. `paper_info` is only for batch basic information; the parameter must be `{"ids": [...]}`.
4. `paper_detail` only supports single-paper details; the parameter must be `{"paper_id": "..."}`. **Never** pass `ids`.
5. When multiple paper details are needed: first use low-cost interfaces for filtering (e.g., `paper_info` / `paper_search_pro`), then call `paper_detail` only for the target subset (default top 10 if the user has not specified a count).
6. Before executing, output "the function name to be called + parameter JSON" for self-inspection, then make the request.

---

## Stability and Failure Handling Strategy (Must Read)

The client `scripts/aminer_client.py` has built-in request retry and fallback strategies to reduce the impact of network fluctuations and transient service errors on results.

- **Timeout and Retry**
  - Default request timeout: `30s`
  - Maximum retries: `3`
  - Backoff strategy: exponential backoff (`1s -> 2s -> 4s`) + random jitter
- **Retryable Status Codes**
  - `408 / 429 / 500 / 502 / 503 / 504`
- **Non-Retryable Scenarios**
  - Common `4xx` errors (e.g., parameter errors, authentication issues) are not retried by default; an error structure is returned directly.
- **Workflow Fallback**
  - `paper_deep_dive`: automatically falls back to `paper_search_pro` if `paper_search` yields no results.
  - `paper_qa`: automatically falls back to `paper_search_pro` if the `query` mode yields no results.
- **Traceable Call Chain**
  - Combined workflow output includes `source_api_chain`, marking which APIs were combined to produce the result.

---

## Paper Search API Selection Guide

When the user says "search for papers", first determine whether the goal is "find an ID", "filter results", "Q&A", or "generate an analysis report", then select the API:

| API | Focus | Use Case | Cost |
|---|---|---|---|
| `paper_search` | Title search, quickly get `paper_id` | Known paper title, locate the target paper first | Free |
| `paper_search_pro` | Multi-condition search and sorting (author/institution/journal/keywords) | Topic search, sort by citations or year | ¥0.01/call |
| `paper_qa_search` | Natural language Q&A / topic keyword search | User describes need in natural language; semantic search first | ¥0.05/call |
| `paper_list_by_search_venue` | Returns more complete paper info (suitable for analysis) | Need richer fields for analysis/reports | ¥0.30/call |
| `paper_list_by_keywords` | Multi-keyword batch retrieval | Batch thematic retrieval (e.g., AlphaFold + protein folding) | ¥0.10/call |
| `paper_detail_by_condition` | Retrieve details by year + journal dimension | Journal annual monitoring, venue selection analysis | ¥0.20/call |

Recommended routing (default):

1. **Known title**: `paper_search -> paper_detail -> paper_relation`
2. **Conditional filtering**: `paper_search_pro -> paper_detail`
3. **Natural language Q&A**: `paper_qa_search` (fall back to `paper_search_pro` if no results)
4. **Journal annual analysis**: `venue_search -> venue_paper_relation -> paper_detail_by_condition`

Supplementary rules (strongly recommended):

1. **When searching by title only**, always use `paper_search` first (free) to quickly locate the paper ID.
2. **For complex semantic retrieval** (natural language, multi-condition, fuzzy expressions), prefer `paper_qa_search`.
3. When using `paper_qa_search`, first break the natural language need into structured conditions, then fill in the fields (e.g., year, topic keywords, author/institution, etc.).
4. `query` and `topic_high/topic_middle/topic_low` are **mutually exclusive**: choose one; do not pass both simultaneously.
5. When using `query` mode, fill in a natural language string directly; when using `topic_*` mode, first expand with synonyms/English variants before filling in.
6. Example: querying "AI-related papers from 2012":
   - `year` → `[2012]`
   - Option A: `query` → `"artificial intelligence"`
   - Option B: `topic_high` → `[["artificial intelligence","ai","Artificial Intelligence"]]` (with `use_topic` enabled)

---

## Handling Out-of-Workflow Requests (Required)

When the user's request **falls outside the 6 workflows above**, or existing workflows cannot directly cover it, the following steps must be executed:

1. First read `references/api-catalog.md` to confirm available interfaces, parameter constraints, and response fields.
2. Select the most appropriate API based on the user's goal and design the shortest viable call chain (locate ID first, then supplement details, then expand relationships).
3. When necessary, combine multiple APIs to complete the query, and annotate `source_api_chain` in the result to clearly describe the data source path.
4. If multiple combination approaches exist, prefer the one with lower cost, higher stability, and fields that satisfy the requirement.
5. Use the "optimal query combination" as much as possible; avoid indiscriminate full retrieval; perform low-cost search and filtering first, then fetch details for a small set of targets.
6. When results are large and the user has not specified a count, default to querying only the top 10 details and returning a summary first; for example, when 1000 papers are matched, do not call the detail API for all 1000 to reduce user costs.
7. For `raw` calls, parameter-level validation is required: e.g., `paper_info` uses `ids`, `paper_detail` uses `paper_id`; do not mix them up.
8. When the user has not explicitly requested deep information, prefer the free path (e.g., `paper_search` / `paper_info` / `venue_search`); only supplement with necessary paid APIs after confirming they are insufficient.
9. When returning the final entity list, the corresponding URL must be included; if entity IDs are missing, supplement them before outputting results.

> Do not give up on a query simply because "no existing workflow fits"; actively complete the API combination based on `api-catalog`.

---

## 6 Combined Workflows

### Workflow 1: Scholar Profile

**Use Case**: Understand a scholar's complete academic profile, including bio, research interests, published papers, patents, and research projects.

**Call Chain:**
```
Scholar search (name → person_id)
    ↓
Parallel calls:
  ├── Scholar details (bio/education/honors)
  ├── Scholar portrait (research interests/experience/work history)
  ├── Scholar papers (paper list)
  ├── Scholar patents (patent list)
  └── Scholar projects (research projects/funding info)
```

**Command:**
```bash
python scripts/aminer_client.py --token <TOKEN> --action scholar_profile --name "Yann LeCun"
```

**Sample output fields:**
- Basic info: name, institution, title, gender
- Personal bio (bilingual)
- Research interests and domains
- Education history (structured)
- Work experience (structured)
- Paper list (ID + title)
- Patent list (ID + title)
- Research projects (title/funding amount/dates)

---

### Workflow 2: Paper Deep Dive

**Use Case**: Retrieve complete paper information and citation relationships based on a paper title or keywords.

**Call Chain:**
```
Paper search / Paper search pro (title/keyword → paper_id)
    ↓
Paper details (abstract/authors/DOI/journal/year/keywords)
    ↓
Paper citations (which papers this paper cites → cited_ids)
    ↓
(Optional) Batch retrieve basic info for cited papers
```

**Command:**
```bash
# Search by title
python scripts/aminer_client.py --token <TOKEN> --action paper_deep_dive --title "BERT"

# Search by keyword (using pro API)
python scripts/aminer_client.py --token <TOKEN> --action paper_deep_dive \
  --keyword "large language model" --author "Hinton" --order n_citation
```

---

### Workflow 3: Org Analysis

**Use Case**: Analyze an institution's scholar size, paper output, and patent count; suitable for competitive research or partnership evaluation.

**Call Chain:**
```
Org disambiguation pro (raw string → org_id, handles alias/full-name differences)
    ↓
Parallel calls:
  ├── Org details (description/type/founding date)
  ├── Org scholars (scholar list)
  ├── Org papers (paper list)
  └── Org patents (patent ID list, supports pagination, up to 10,000)
```

> If multiple institutions share the same name, org search returns a candidate list; use org disambiguation pro for precise matching.

**Command:**
```bash
python scripts/aminer_client.py --token <TOKEN> --action org_analysis --org "MIT"
# Specify raw string (with abbreviation/alias)
python scripts/aminer_client.py --token <TOKEN> --action org_analysis --org "Massachusetts Institute of Technology, CSAIL"
```

---

### Workflow 4: Venue Papers

**Use Case**: Track papers published in a specific journal for a given year; useful for submission research or research trend analysis.

**Call Chain:**
```
Venue search (name → venue_id)
    ↓
Venue details (ISSN/type/abbreviation)
    ↓
Venue papers (venue_id + year → paper_id list)
    ↓
(Optional) Batch paper detail query
```

**Command:**
```bash
python scripts/aminer_client.py --token <TOKEN> --action venue_papers --venue "NeurIPS" --year 2023
```

---

### Workflow 5: Paper QA Search

**Use Case**: Intelligently search for papers using natural language or structured keywords; supports SCI filtering, citation-based sorting, author/institution constraints.

**Core API**: `Paper QA Search` (¥0.05/call), supports:
- `query`: natural language question; system automatically breaks it into keywords
- `topic_high/middle/low`: fine-grained keyword weight control (nested array OR/AND logic)
- `sci_flag`: show SCI papers only
- `force_citation_sort`: sort by citation count
- `force_year_sort`: sort by year
- `author_terms / org_terms`: filter by author name or institution name
- `author_id / org_id`: filter by author ID or institution ID (recommended for disambiguation)
- `venue_ids`: filter by conference/journal ID list

**Command:**
```bash
# Natural language Q&A
python scripts/aminer_client.py --token <TOKEN> --action paper_qa \
  --query "deep learning methods for protein structure prediction"

# Fine-grained keyword search (must contain A and B, bonus for C)
python scripts/aminer_client.py --token <TOKEN> --action paper_qa \
  --topic_high '[["transformer","self-attention"],["protein folding"]]' \
  --topic_middle '[["AlphaFold"]]' \
  --sci_flag --sort_citation
```

---

### Workflow 6: Patent Analysis

**Use Case**: Search for patents in a specific technology domain, or retrieve a scholar's/institution's patent portfolio.

**Call Chain (standalone search):**
```
Patent search (query → patent_id)
    ↓
Patent details (abstract/filing date/application number/assignee/inventor)
```

**Call Chain (via scholar/institution):**
```
Scholar search → Scholar patents (patent_id list)
Org disambiguation → Org patents (patent_id list)
    ↓
Patent info / Patent details
```

**Command:**
```bash
python scripts/aminer_client.py --token <TOKEN> --action patent_search --query "quantum computing chip"
python scripts/aminer_client.py --token <TOKEN> --action scholar_patents --name "Shou-Cheng Zhang"
```

---

## Individual API Quick Reference

> For complete parameter descriptions, read `references/api-catalog.md`

| # | Title | Method | Price | API Path (Base domain: datacenter.aminer.cn/gateway/open_platform) |
|---|------|------|------|------|
| 1 | Paper QA Search | POST | ¥0.05 | `/api/paper/qa/search` |
| 2 | Scholar Search | POST | Free | `/api/person/search` |
| 3 | Paper Search | GET | Free | `/api/paper/search` |
| 4 | Paper Search Pro | GET | ¥0.01 | `/api/paper/search/pro` |
| 5 | Patent Search | POST | Free | `/api/patent/search` |
| 6 | Org Search | POST | Free | `/api/organization/search` |
| 7 | Venue Search | POST | Free | `/api/venue/search` |
| 8 | Scholar Details | GET | ¥1.00 | `/api/person/detail` |
| 9 | Scholar Projects | GET | ¥3.00 | `/api/project/person/v3/open` |
| 10 | Scholar Papers | GET | ¥1.50 | `/api/person/paper/relation` |
| 11 | Scholar Patents | GET | ¥1.50 | `/api/person/patent/relation` |
| 12 | Scholar Portrait | GET | ¥0.50 | `/api/person/figure` |
| 13 | Paper Info | POST | Free | `/api/paper/info` |
| 14 | Paper Details | GET | ¥0.01 | `/api/paper/detail` |
| 15 | Paper Citations | GET | ¥0.10 | `/api/paper/relation` |
| 16 | Patent Info | GET | Free | `/api/patent/info` |
| 17 | Patent Details | GET | ¥0.01 | `/api/patent/detail` |
| 18 | Org Details | POST | ¥0.01 | `/api/organization/detail` |
| 19 | Org Patents | GET | ¥0.10 | `/api/organization/patent/relation` |
| 20 | Org Scholars | GET | ¥0.50 | `/api/organization/person/relation` |
| 21 | Org Papers | GET | ¥0.10 | `/api/organization/paper/relation` |
| 22 | Venue Details | POST | ¥0.20 | `/api/venue/detail` |
| 23 | Venue Papers | POST | ¥0.10 | `/api/venue/paper/relation` |
| 24 | Org Disambiguation | POST | ¥0.01 | `/api/organization/na` |
| 25 | Org Disambiguation Pro | POST | ¥0.05 | `/api/organization/na/pro` |
| 26 | Paper Search by Venue | GET | ¥0.30 | `/api/paper/list/by/search/venue` |
| 27 | Paper Batch Query | GET | ¥0.10 | `/api/paper/list/citation/by/keywords` |
| 28 | Paper Details by Year and Venue | GET | ¥0.20 | `/api/paper/platform/allpubs/more/detail/by/ts/org/venue` |

---

## References

- Full API parameter documentation: read `references/api-catalog.md`
- Python client source: `scripts/aminer_client.py`
- Test cases: `evals/evals.json`
- Official documentation: https://open.aminer.cn/open/docs
- Console: https://open.aminer.cn/open/board?tab=control
