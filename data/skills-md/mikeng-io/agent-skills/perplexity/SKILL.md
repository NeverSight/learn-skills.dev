---
name: perplexity
description: Optional AI-synthesized web search via Perplexity MCP. Returns AI-grounded answers with inline citations rather than raw search results — best for synthesis-heavy questions, current consensus queries, and cross-validation of research findings. Non-blocking — falls back to other search tools if unavailable.
location: managed
context: fork
allowed-tools:
  - ToolSearch
  - mcp__perplexity__search
---

# Perplexity MCP — Optional AI-Synthesized Search

This skill wraps the Perplexity MCP server. Unlike raw web search tools that return a list of URLs, Perplexity returns AI-synthesized answers with inline citations — it reads the web for you and summarizes what it finds.

**Best for:** "What is the current consensus on X?", "Compare A vs B", "What changed in X since version Y?"
**Not ideal for:** Retrieving specific raw URLs, domain-specific technical documentation, anything requiring exact source control

**Setup:** Requires the Perplexity MCP server and a Perplexity API key.

```bash
# Add to MCP config (one-time setup)
claude mcp add -s user perplexity npx @perplexity-ai/mcp-server
# Then set: PERPLEXITY_API_KEY=your_key_here
# Get an API key at: https://www.perplexity.ai/settings/api
```

---

## Pre-Flight: Check Availability

```yaml
ToolSearch: "perplexity"
  → Returns: mcp__perplexity__search
  → If found: proceed to Step 1
  → If not found: return availability: "unavailable", skip — other search tools handle raw web
```

**Non-blocking:** Perplexity is a complement to web search, not a replacement. If unavailable, research continues normally with Brave Search and other tools.

---

## Step 1: Identify High-Value Query Types

Perplexity shines for these query patterns:

```yaml
high_value_use_cases:
  consensus_synthesis:
    description: "What does the community/industry currently think about X?"
    examples:
      - "What is the current consensus on Go vs Rust for systems programming?"
      - "What are the most common criticisms of event sourcing in practice?"
    why: Returns synthesized view across many sources, not just one opinion

  comparison_analysis:
    description: "Compare A vs B across multiple criteria"
    examples:
      - "Compare Redis vs Memcached for session storage in 2025"
      - "Compare Kafka vs RabbitMQ for event streaming at scale"
    why: AI synthesis better at multi-dimensional comparison than individual sources

  current_state_snapshot:
    description: "What is the current state of X?"
    examples:
      - "What is the current state of WebAssembly browser support in 2025?"
      - "What authentication standards are recommended in 2025?"
    why: Perplexity indexes recent content and synthesizes the current picture

  cross_validation:
    description: Use to validate or challenge findings from other sources
    examples:
      - "Are there known limitations or criticisms of [finding from web search]?"
    why: Provides a second synthesis pass to surface what raw search might miss
```

**Not ideal for:**
- Retrieving specific URLs or raw source lists (use Brave Search)
- Deep technical documentation (use context7 or direct docs)
- Codebase-specific questions (use DeepWiki)

---

## Step 2: Execute Query

```
mcp__perplexity__search(query="your synthesis question here")
```

**Query construction tips:**
- Frame as a question requiring synthesis: "What is...", "How does... compare to...", "What are the tradeoffs of..."
- Include context: "in production Go services", "for startups in 2025"
- Ask for recency: "currently", "as of 2025", "latest recommendations"
- Request specific framing: "from a security perspective", "in terms of developer experience"

---

## Step 3: Process Response

Perplexity returns a synthesized answer with inline citations. Process it as:

```json
{
  "source": "perplexity",
  "query": "the query executed",
  "answer": "Synthesized answer text with [citation] references",
  "citations": [
    {
      "index": 1,
      "url": "https://source-url",
      "title": "Source title"
    }
  ],
  "credibility": "MEDIUM",    // always MEDIUM — AI synthesis, not primary source
  "type": "ai-synthesis",
  "key_points": ["Extracted key point 1", "Extracted key point 2"]
}
```

**Credibility note:** Always tag Perplexity outputs as `credibility: MEDIUM` — the underlying sources may be HIGH, but the synthesis layer introduces potential for hallucination. Use inline citations to verify critical claims.

---

## Calling Context Integration

### When invoked by `deep-research`

Complement domain researcher queries. Run Perplexity in parallel with Brave Search for synthesis-heavy topics. Pattern:

1. Domain researcher runs Brave Search for raw source collection
2. Perplexity runs for consensus synthesis on the same topic
3. Cross-reference: does Perplexity's synthesis align with the raw sources?
4. Discrepancies become noted contradictions or gaps in research findings

### When invoked for cross-validation

After primary research is complete, run Perplexity with: "What are the main criticisms or limitations of [primary finding]?" — surfaces counter-perspectives that raw search might have missed.

### When invoked standalone

Execute 1-3 synthesis queries, return structured answer with citations. Suitable for quick orientation on an unfamiliar topic before deeper research.

---

## Output

```json
{
  "skill": "perplexity",
  "availability": "available | unavailable",
  "queries_executed": ["list of queries"],
  "results": [
    {
      "query": "...",
      "answer": "...",
      "citations": [...],
      "key_points": [...]
    }
  ],
  "validation_note": "AI-synthesized answers — verify critical claims via inline citations"
}
```

If unavailable:
```json
{
  "skill": "perplexity",
  "availability": "unavailable",
  "reason": "MCP server not configured",
  "setup_hint": "claude mcp add -s user perplexity npx @perplexity-ai/mcp-server",
  "alternative": "Use brave-search or web-search-prime for raw web results"
}
```

---

## Why Perplexity vs Other Search Tools?

| Tool | Returns | Best for |
|------|---------|----------|
| `brave-search` | Raw web results with URLs | Source collection, specific URL retrieval |
| `perplexity` | AI synthesis with citations | Consensus questions, comparison, current state |
| `web-search-prime` | Raw web results | General fallback search |
| `deepwiki` | Codebase wiki answers | Codebase-specific questions |

Perplexity and Brave Search are **complementary, not competing** — run both for comprehensive research coverage.
