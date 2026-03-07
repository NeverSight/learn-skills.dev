---
name: firecrawl-research-patterns
description: "Programmatic Firecrawl usage, self-hosted operations, academic paper routing, recursive deep research, and raw corpus persistence. TRIGGERS - firecrawl search, firecrawl scrape, academic paper, arxiv, deep research, recursive search, research pattern, corpus persistence, firecrawl, self-hosted scraping, web scrape, scraper wrapper, littleblack, ZeroTier scraping."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Firecrawl Research Patterns

Programmatic patterns for using self-hosted Firecrawl in research workflows — search, scrape, route academic papers, run recursive deep research, and persist raw results for future re-analysis. Also covers self-hosted deployment, health checks, and recovery.

For archiving AI chat conversations (ChatGPT/Gemini shares), see `Skill(gh-tools:research-archival)`.

---

## FIRST — TodoWrite Task Templates

**MANDATORY**: Select and load the appropriate template before any research work.

### Template A — Single Firecrawl Search + Persist

```
1. Health check — GET http://172.25.236.1:3002/v1/health (fallback: test search)
2. Execute search — POST /v1/search with query, limit, scrapeOptions
3. Persist raw results — save each result page to docs/research/corpus/ with frontmatter
4. Update corpus index — append entries to docs/research/corpus-index.jsonl
5. Extract findings — summarize key learnings from raw corpus files
```

### Template B — Academic Paper Retrieval + Persist

```
1. Identify source — classify URL/DOI per academic-paper-routing.md decision tree
2. Route to scraper — arxiv direct HTML, Semantic Scholar API, Firecrawl, or Jina Reader
3. Scrape content — execute fetch with appropriate method and timeout
4. Persist raw result — save to docs/research/corpus/ with academic-specific frontmatter
5. Update corpus index — append entry to corpus-index.jsonl
6. Summarize paper — extract key claims, methods, results from raw corpus file
```

### Template C — Full Recursive Deep Research with Corpus

```
1. Health check — verify Firecrawl reachable at 172.25.236.1:3002
2. Initialize parameters — set breadth (default 4), depth (default 2), concurrency (default 2)
3. Generate search queries — LLM generates N queries from topic + prior learnings
4. Execute searches — Firecrawl /v1/search for each query via p-limit(concurrency)
5. Persist raw results — save ALL scraped pages to docs/research/corpus/ with provenance
6. Extract learnings — LLM extracts key findings + follow-up questions per result set
7. Recurse — for each follow-up, recurse with breadth=ceil(breadth/2), depth=depth-1
8. Base case — depth=0, return accumulated learnings
9. Synthesize report — LLM generates final markdown from all learnings
10. Write session report — save to docs/research/sessions/ with corpus file references
11. Update corpus index — append all new entries to corpus-index.jsonl
```

### Template D — Corpus Review / Re-Analysis

```
1. Inventory corpus — read docs/research/corpus-index.jsonl, filter by session/topic/date
2. Read raw files — load matching corpus files from docs/research/corpus/
3. Re-analyze — extract new insights with current context/questions
4. Update session report — amend or create new session report in docs/research/sessions/
```

---

## Section 1 — Programmatic Firecrawl Usage

**Instance**: Self-hosted at `http://172.25.236.1:3002` via ZeroTier. No API key needed.

### Why `fetch()` Instead of `@mendable/firecrawl-js` SDK

The official SDK uses `jiti` for dynamic imports, which is incompatible with Bun's module resolution. Direct `fetch()` calls are simpler, more reliable, and have zero dependencies.

### Two Endpoints

| Endpoint          | Purpose               | When to Use                                       |
| ----------------- | --------------------- | ------------------------------------------------- |
| `POST /v1/search` | Search + scrape combo | Research queries — returns multiple scraped pages |
| `POST /v1/scrape` | Single URL scrape     | Known URL — extract markdown from one page        |

See [api-endpoint-reference.md](./references/api-endpoint-reference.md) for full request/response contracts.

### Quick Examples

**Search** (returns multiple results with markdown):

```typescript
const res = await fetch("http://172.25.236.1:3002/v1/search", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    query: "mixture of experts scaling laws",
    limit: 5,
    scrapeOptions: { formats: ["markdown"] },
  }),
});
const { data } = await res.json(); // data: [{ url, markdown, metadata }]
```

**Scrape** (single URL):

```typescript
const res = await fetch("http://172.25.236.1:3002/v1/scrape", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    url: "https://arxiv.org/abs/2401.12345",
    formats: ["markdown"],
    waitFor: 3000, // ms — for JS-heavy pages
  }),
});
const { data } = await res.json(); // data: { markdown, metadata }
```

### Error Handling

```typescript
// Always set a timeout
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 15_000);

try {
  const res = await fetch(url, { ...opts, signal: controller.signal });
  if (!res.ok) throw new Error(`Firecrawl: ${res.status} ${res.statusText}`);
  const json = await res.json();
  if (!json.data || (Array.isArray(json.data) && json.data.length === 0)) {
    // Empty results — not an error, but no content to process
  }
} finally {
  clearTimeout(timeoutId);
}
```

### Health Check

```typescript
// Quick health check before starting a research session
const res = await fetch("http://172.25.236.1:3002/v1/health");
if (!res.ok)
  throw new Error(
    "Firecrawl unhealthy — see self-hosted-operations.md and self-hosted-troubleshooting.md references",
  );
```

---

## Section 2 — Academic Paper Routing

Route paper retrieval to the most effective method based on source. Full decision tree in [academic-paper-routing.md](./references/academic-paper-routing.md).

### Quick Reference

| Source            | Best Method                           | Fallback                  |
| ----------------- | ------------------------------------- | ------------------------- |
| arxiv.org         | Direct HTML (`/html/ID`)              | Firecrawl `/v1/scrape`    |
| Semantic Scholar  | API (`api.semanticscholar.org`)       | Firecrawl search by title |
| ACL Anthology     | Firecrawl `/v1/scrape`                | Direct PDF download       |
| NeurIPS/ICML/ICLR | Firecrawl `/v1/scrape` with `waitFor` | Search by title           |
| IEEE Xplore       | Firecrawl with `waitFor: 3000`        | Author's website          |
| ACM DL            | Firecrawl with `waitFor: 3000`        | Author's website          |
| Author blogs      | Jina Reader (`r.jina.ai`)             | Firecrawl `/v1/scrape`    |
| Google Scholar    | Firecrawl `/v1/search`                | Direct search query       |

### DOI Resolution

```typescript
// DOI → publisher URL → route to appropriate scraper
const res = await fetch(`https://doi.org/${doi}`, { redirect: "follow" });
const publisherUrl = res.url; // e.g., https://dl.acm.org/doi/10.1145/...
// Then route publisherUrl through the decision tree above
```

---

## Section 3 — Recursive Research Protocol

The iterative search → extract → recurse → synthesize pattern. Full step-by-step protocol in [recursive-research-protocol.md](./references/recursive-research-protocol.md).

### Algorithm Overview

```
deepResearch(topic, breadth=4, depth=2, concurrency=2):
   1. Generate N search queries (N = breadth) from topic + prior learnings
   2. For each query (via p-limit concurrency):
      a. Firecrawl /v1/search → get results
      b. PERSIST each raw result to docs/research/corpus/
      c. Extract learnings + follow-up questions
   3. For each follow-up question:
      → Recurse with breadth=ceil(breadth/2), depth=depth-1
   4. Base case: depth=0 → return accumulated learnings
   5. Synthesize final report from all learnings
   6. Write session report to docs/research/sessions/
```

### Default Parameters (from working implementation)

| Parameter     | Default | Max | Rationale                                               |
| ------------- | ------- | --- | ------------------------------------------------------- |
| `breadth`     | 4       | —   | Number of parallel search queries per level             |
| `depth`       | 2       | 5   | Recursion levels (depth > 5 yields diminishing returns) |
| `concurrency` | 2       | —   | Parallel Firecrawl requests (self-hosted, be gentle)    |
| `limit`       | 5       | —   | Results per search query                                |
| `timeout`     | 15000ms | —   | Per-search timeout                                      |

### Token Budget

Each search returns up to 5 pages. Trim each page to ~25,000 tokens before LLM processing:

```typescript
function trimToTokenLimit(text: string, maxTokens: number): string {
  if (!text) return "";
  const estimatedTokens = Math.ceil(text.length / 3.5);
  if (estimatedTokens <= maxTokens) return text;
  const maxChars = Math.floor(maxTokens * 3.5 * 0.8);
  return text.slice(0, maxChars);
}
```

### Partial Failure Principle

**Partial results are better than total failure.** If a query fails, log it and continue with remaining queries. Never abort the entire research session because one query timed out.

---

## Section 4 — Raw Corpus Persistence

**Critical principle**: Every Firecrawl-scraped page must be persisted in its **original raw markdown** with provenance metadata. Synthesized reports reference these originals but never replace them.

Full format specification in [corpus-persistence-format.md](./references/corpus-persistence-format.md).

### Directory Layout

```
{project-root}/
├── docs/research/
│   ├── corpus/                              # Raw scraped pages (committed)
│   │   └── YYYY-MM-DD-{slug}.md             # One file per scraped URL
│   ├── sessions/                            # Research session reports (committed)
│   │   └── YYYY-MM-DD-{topic-slug}.md       # Synthesized report with corpus refs
│   └── corpus-index.jsonl                   # Append-only registry (committed)
```

### Corpus File Frontmatter

```yaml
---
source_url: https://arxiv.org/html/2401.12345
scraped_at: "2026-02-25T14:30:00Z"
scraper: firecrawl
firecrawl_endpoint: /v1/search
search_query: "mixture of experts scaling"
result_index: 2
research_session: "2026-02-25-moe-scaling"
depth_level: 1
claude_code_uuid: SESSION_UUID
content_tokens_approx: 4200
---
[RAW MARKDOWN FROM FIRECRAWL — NEVER MODIFIED]
```

### Key Rules

1. Content below `---` is the **exact markdown Firecrawl returned** — no summarization, trimming, or reformatting
2. One file per URL per scrape — if the same URL is scraped in multiple sessions, each gets its own timestamped file
3. File naming: `YYYY-MM-DD-{slug}.md` where slug is kebab-case from page title or URL path (max 60 chars)
4. Session reports in `docs/research/sessions/` reference corpus files by relative path

### Corpus Index (JSONL)

```json
{
  "url": "https://arxiv.org/html/2401.12345",
  "file": "corpus/2026-02-25-moe-scaling-arxiv-2401-12345.md",
  "scraped_at": "2026-02-25T14:30:00Z",
  "session": "2026-02-25-moe-scaling",
  "tokens": 4200,
  "scraper": "firecrawl"
}
```

### Why This Matters

- **LLM re-analysis**: Future sessions can re-read raw corpus files and extract different insights with better prompts or newer models
- **No information loss**: Synthesis drops details; raw files preserve everything Firecrawl captured
- **Deduplication awareness**: The JSONL index lets agents skip URLs already in the corpus
- **Git-friendly**: Markdown files diff cleanly, JSONL is append-only

---

## Section 5 — Self-Hosted Operations

The Firecrawl instance runs on **littleblack** (172.25.236.1) via ZeroTier. No API key needed.

| Port | Service         | Type   | Purpose                    |
| ---- | --------------- | ------ | -------------------------- |
| 3002 | Firecrawl API   | Docker | Core scraping engine       |
| 3003 | Scraper Wrapper | Bun    | Saves to file, returns URL |
| 8080 | Caddy           | Binary | Serves saved markdown      |

For architecture diagrams, health checks, recovery commands, and deployment details, see:

- [Self-Hosted Operations](./references/self-hosted-operations.md) — Architecture, health checks, recovery commands
- [Self-Hosted Bootstrap Guide](./references/self-hosted-bootstrap-guide.md) — Fresh installation (7 steps)
- [Self-Hosted Best Practices](./references/self-hosted-best-practices.md) — Docker restart policies, monitoring
- [Self-Hosted Troubleshooting](./references/self-hosted-troubleshooting.md) — Symptom-based diagnosis

---

## Anti-Patterns

| #   | Anti-Pattern                                | Why It Fails                                     | Correct Approach                                |
| --- | ------------------------------------------- | ------------------------------------------------ | ----------------------------------------------- |
| 1   | Using `@mendable/firecrawl-js` SDK          | `jiti` dynamic imports break in Bun              | Direct `fetch()` calls                          |
| 2   | Searching paywalled sites without `waitFor` | JS SPAs return empty shell                       | Use `waitFor: 3000` for IEEE, ACM DL            |
| 3   | Setting depth > 5                           | Exponential query explosion, diminishing returns | Cap at depth 5 (`clampDepth()`)                 |
| 4   | No timeout on `fetch()`                     | Hangs indefinitely on unreachable pages          | Always use `AbortController` with 15s timeout   |
| 5   | Not trimming long page content              | Exceeds LLM context window                       | `trimToTokenLimit(text, 25_000)` per page       |
| 6   | Aborting on partial failure                 | Loses all completed work                         | Log failures, continue with remaining queries   |
| 7   | Not checking Firecrawl health first         | Wastes time on queries that all fail             | `GET /v1/health` or test search before starting |
| 8   | Saving only synthesis without raw originals | Loses source material, prevents re-analysis      | Always persist raw Firecrawl markdown to corpus |

---

## References

- [API Endpoint Reference](./references/api-endpoint-reference.md) — `/v1/search` and `/v1/scrape` contracts
- [Academic Paper Routing](./references/academic-paper-routing.md) — Decision tree for paper sources
- [Recursive Research Protocol](./references/recursive-research-protocol.md) — Step-by-step recursive pattern
- [Corpus Persistence Format](./references/corpus-persistence-format.md) — Raw content archival format + directory layout
- [Self-Hosted Operations](./references/self-hosted-operations.md) — Architecture, health checks, recovery
- [Self-Hosted Bootstrap Guide](./references/self-hosted-bootstrap-guide.md) — Fresh installation guide
- [Self-Hosted Best Practices](./references/self-hosted-best-practices.md) — Docker restart policies, monitoring
- [Self-Hosted Troubleshooting](./references/self-hosted-troubleshooting.md) — Symptom-based diagnosis and recovery
