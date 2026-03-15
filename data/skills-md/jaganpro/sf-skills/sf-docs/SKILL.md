---
name: sf-docs
description: >
  Official Salesforce documentation retrieval skill. Prefer locally indexed
  Salesforce docs via qmd when available; otherwise use Salesforce-aware
  scraping and guide/PDF discovery strategies for developer.salesforce.com and
  help.salesforce.com.
license: MIT
metadata:
  version: "0.1.0"
  author: "Jag Valaiyapathy"
---

# sf-docs: Salesforce Documentation Retrieval & Grounding

Expert Salesforce documentation researcher focused on **official sources**. This skill exists to make documentation lookup reliable when generic web search or naive page fetching fails on Salesforce's JavaScript-heavy docs experience.

`sf-docs` is a **core sf-skills capability**. It should always be installed with the skill suite.

## Core Responsibilities

1. **Official Docs Retrieval**: Find authoritative answers from Salesforce documentation first
2. **Local-First Search**: Use a local qmd index when available for speed and accuracy
3. **Salesforce-Aware Fallback**: When qmd is unavailable or weak, use Salesforce-specific retrieval patterns instead of generic web fetch
4. **Source Grounding**: Return answers with exact source URLs, guide names, and retrieval notes
5. **Cross-Skill Support**: Serve as the documentation lookup layer for other `sf-*` skills

---

## Runtime Modes

### Mode A: qmd-Enabled

Use this mode when qmd is installed and a local Salesforce docs corpus exists.

**Preferred flow:**
1. Detect qmd availability
2. Query qmd first
3. Evaluate result quality
4. If results are strong, answer from local docs
5. If results are weak or missing, fall back to Salesforce-aware scraping

### Mode B: No-qmd

Use this mode when qmd is not installed or no local corpus exists.

**Preferred flow:**
1. Identify the most likely Salesforce doc family
2. Use Salesforce-aware discovery and retrieval patterns
3. Prefer official URLs over summaries from third-party blogs
4. Fall back to official PDFs when web pages are unstable or shell-rendered
5. Return grounded findings with source links and any uncertainty called out

**Claude Code operator shortcut:**
When the local `sf-docs` helper scripts are installed, prefer the built-in retrieval command over ad-hoc search-engine probing:

```bash
python3 ~/.claude/skills/sf-docs/scripts/cli.py retrieve \
  --query "<user question>" \
  --mode no_qmd
```

For hard `help.salesforce.com` questions, this command applies the local no-qmd retrieval flow, including targeted Help article discovery and browser-based rendering.

### Runtime Detection

`sf-docs` should detect qmd **at runtime**, not just rely on installer choices.

Use this detection order:
1. Check whether the `qmd` CLI is available on `PATH`
2. Check whether a local Salesforce docs corpus exists
3. If qmd exists but the local corpus/index is missing or effectively empty, treat the request as **no-qmd mode**
4. If qmd exists and the corpus is populated, use **qmd-enabled mode**

> Reference: [references/local-corpus-layout.md](references/local-corpus-layout.md)

---

## Fallback Triggers

Treat qmd results as **weak** and fall back when any of the following happen:

- No results returned
- Results are clearly from the wrong Salesforce product or guide family
- Results lack the exact concept, API name, CLI command, or error term requested
- Results are too fragmentary to answer confidently
- Results appear stale and the query is obviously release-sensitive

> **Rule**: Prefer a reliable Salesforce-specific fallback over confidently answering from a poor local hit.

---

## Salesforce Documentation Retrieval Playbook

### 1. Identify the Doc Family First

Classify the request before searching:

| Family | Typical Sources | Use For |
|--------|------------------|---------|
| **Developer Docs** | `developer.salesforce.com/docs/...` | Apex, APIs, LWC, metadata, Agentforce developer docs |
| **Salesforce Help** | `help.salesforce.com/...` | Setup UI steps, admin guides, feature configuration |
| **Platform Guides** | `developer.salesforce.com/docs/platform/...` | Newer guide-style docs with cleaner URLs |
| **Atlas / Legacy Guides** | `developer.salesforce.com/docs/atlas.en-us.*` | Older but still official guide and reference material |
| **Official PDFs** | `resources.docs.salesforce.com/...pdf/...` | Large guide bundles, stable offline extraction |

### 2. Prefer Exact Guide Paths Over Homepage Search

Avoid stopping at broad pages like the docs homepage unless you are discovering guide roots.

Instead, resolve toward:
- A specific guide root
- A specific article or page
- A guide PDF when page-level retrieval is unstable

### 3. Retrieval Patterns for `developer.salesforce.com`

Use these patterns deliberately:

- **Modern platform guide**: `developer.salesforce.com/docs/platform/...`
- **Legacy Atlas guide**: `developer.salesforce.com/docs/atlas.en-us.<book>.meta/...`
- **Guide PDF candidate**: derive `<book>` and try the matching official PDF URL

When an HTML page fails because of JavaScript rendering, shell content, or soft errors, try:
1. the guide root
2. the legacy Atlas variant if known
3. the official PDF

### 4. Retrieval Patterns for `help.salesforce.com`

Help pages often fail with generic web fetch because of client-side rendering and site chrome.

Use this approach:
- Prefer exact `help.salesforce.com/s/articleView?id=...` URLs or article identifiers when available
- If you only have a product/topic query, start from a targeted official hub and discover linked Help articles from there
  - Agentforce queries: start from the Agentforce developer guide and follow linked Help articles
  - Messaging / Enhanced Web Chat queries: start from the Enhanced Web Chat docs or landing Help article, then follow one hop to child setup/security articles
- Expect navigation shell noise and incomplete body extraction
- Focus on retrieving the actual article body, not the rendered header/footer shell
- Reject shell or soft-404 pages such as "We looked high and low but couldn't find that page"
- Cross-check titles, product area, and article body before trusting a result

### 5. PDFs Are a Valid Official Fallback

Use PDFs when:
- The guide has a stable official PDF
- HTML extraction is inconsistent
- A long-form developer guide is easier to search locally after normalization

PDFs may be stored **locally** and indexed later, but should **not** be committed into the public repo.

---

## Answer Requirements

When using `sf-docs`, answers should include:

1. **Source type** — qmd local hit, official HTML page, or official PDF
2. **Guide/article name**
3. **Exact official URL**
4. **Any retrieval caveat** — for example, if fallback scraping was needed or if the content appeared partially rendered

If the evidence is weak, say so plainly.

---

## Cross-Skill Integration

| Skill | How `sf-docs` Helps |
|-------|----------------------|
| `sf-ai-agentforce` | Find Agentforce, PromptTemplate, Models API, and setup docs |
| `sf-ai-agentscript` | Find Agent Script syntax, CLI, and reasoning engine docs |
| `sf-apex` | Find Apex language and reference docs |
| `sf-lwc` | Find LWC guides, component references, and wire docs |
| `sf-integration` | Find REST, SOAP, Named Credential, and auth docs |
| `sf-deploy` | Find CLI, deployment, packaging, and metadata references |

**Delegation rule**: If another skill needs authoritative Salesforce documentation, it should use `sf-docs` as the retrieval layer rather than improvising generic web search.

---

## Local Storage Policy

- `sf-docs` is part of the core skill suite
- qmd remains an **optional external dependency**
- Downloaded PDFs, scraped markdown, manifests, and indexes should live on the **user's machine**
- Official Salesforce docs content should **not** be stored in this public Git repository

### Default Local Corpus Layout

Use a stable local root such as:

```text
~/.sf-docs/
```

Recommended structure:
- `~/.sf-docs/manifest/` — discovery manifests and fetch/index status
- `~/.sf-docs/raw/pdf/` — downloaded official PDFs
- `~/.sf-docs/raw/html/` — optional raw HTML captures
- `~/.sf-docs/normalized/md/` — canonical markdown corpus for qmd indexing
- `~/.sf-docs/qmd/` — qmd-specific config notes
- `~/.sf-docs/logs/` — optional diagnostics and fetch logs

> Full reference: [references/local-corpus-layout.md](references/local-corpus-layout.md)

---

## First-Version Behavior

The initial implementation should optimize for correctness and operational simplicity:

1. qmd-first when available
2. Sequential fallback to Salesforce-aware scraping
3. Targeted retrieval, not broad crawling, during normal lookups
4. Grounded responses with official source links

### Query-Time Runtime Flow

1. Detect qmd and local corpus availability
2. Run qmd lookup if available
3. Evaluate hit quality
4. On weak/missing results, use Salesforce-specific HTML/PDF fallback
5. Answer with source grounding and retrieval caveats when needed

> Full runtime guide: [references/runtime-workflow.md](references/runtime-workflow.md)

Parallel qmd + scraping can be considered later if benchmarks justify the added complexity.

---

## Success Criteria

`sf-docs` is successful when it does the following better than generic web search:

- Finds the right Salesforce page or PDF more often
- Avoids failed fetches on `help.salesforce.com`
- Reduces hallucinations by grounding on official sources
- Improves the documentation quality available to the rest of the `sf-*` skills

---

## References

| Document | Purpose |
|----------|---------|
| [references/local-corpus-layout.md](references/local-corpus-layout.md) | Local-only corpus structure and runtime detection rules |
| [references/discovery-manifest.md](references/discovery-manifest.md) | Guide discovery manifest schema, mixed doc family handling, HTML vs PDF policy |
| [references/qmd-integration.md](references/qmd-integration.md) | qmd collection, context, and retrieval strategy |
| [references/runtime-workflow.md](references/runtime-workflow.md) | Query-time flow, fallback rules, sync/index separation, and local persistence policy |
| [references/ingestion-workflow.md](references/ingestion-workflow.md) | Targeted HTML/PDF fetch, normalization, and qmd bootstrap workflow |
| [references/salesforce-scraper-techniques.md](references/salesforce-scraper-techniques.md) | Salesforce-aware browser extraction techniques, Shadow DOM handling, and PDF fallback rationale |
| [references/pilot-scope.md](references/pilot-scope.md) | Initial guide scope for v1 ingestion |
| [references/benchmark-protocol.md](references/benchmark-protocol.md) | qmd-first and no-qmd validation protocol |
| [references/cli-workflow.md](references/cli-workflow.md) | Unified CLI workflow for discover, sync, bootstrap, diagnose, and benchmark scoring |
| [references/implementation-order.md](references/implementation-order.md) | Recommended v1 execution order |
| [references/final-architecture.md](references/final-architecture.md) | Final architectural recommendation |

## Assets & Scripts

| File | Purpose |
|------|---------|
| [assets/discovery-manifest.seed.json](assets/discovery-manifest.seed.json) | Starter guide manifest seed |
| [assets/retrieval-benchmark.json](assets/retrieval-benchmark.json) | Expanded core retrieval benchmark cases for exact identifiers, guide routing, and evidence grounding |
| [assets/retrieval-benchmark.results-template.json](assets/retrieval-benchmark.results-template.json) | Template for recording qmd-first and no-qmd core benchmark outcomes |
| [assets/retrieval-benchmark.robustness.json](assets/retrieval-benchmark.robustness.json) | Negative / wrong-guide rejection benchmark for hardening fallback behavior |
| [assets/retrieval-benchmark.robustness.results-template.json](assets/retrieval-benchmark.robustness.results-template.json) | Template for recording robustness benchmark outcomes |
| [scripts/cli.py](scripts/cli.py) | Unified sf-docs CLI for discover, sync, bootstrap-qmd, status, diagnose, retrieve, and benchmarking |
| [scripts/discover_salesforce_docs.py](scripts/discover_salesforce_docs.py) | Enrich guide seeds into a discovery manifest and optionally verify PDF candidates |
| [scripts/salesforce_dom_scraper.mjs](scripts/salesforce_dom_scraper.mjs) | Salesforce-aware browser scraper with Shadow DOM, legacy doc container, iframe, and help-page heuristics |
| [scripts/sync_sf_docs.py](scripts/sync_sf_docs.py) | Fetch targeted HTML/PDF sources into the local corpus and normalize them into markdown |
| [scripts/bootstrap_qmd.py](scripts/bootstrap_qmd.py) | Configure a single qmd collection over the normalized sf-docs corpus |
| [scripts/sf_docs_runtime.py](scripts/sf_docs_runtime.py) | Detect qmd/corpus readiness, build sequential lookup plans, and evaluate qmd result strength |
| [scripts/retrieve_sf_docs.py](scripts/retrieve_sf_docs.py) | End-to-end qmd-first or no-qmd retrieval execution with Salesforce-aware fallback |
| [scripts/run_retrieval_benchmark.py](scripts/run_retrieval_benchmark.py) | Execute the benchmark cases through qmd-first and no-qmd retrieval modes |
| [scripts/score_retrieval_benchmark.py](scripts/score_retrieval_benchmark.py) | Score benchmark results for qmd-first and no-qmd modes |

---

## License

MIT License. See LICENSE file in the repo root.
Copyright (c) 2024–2026 Jag Valaiyapathy
