---
name: deepwiki
description: Optional codebase intelligence skill — wraps Devin's DeepWiki MCP server to provide structured documentation lookup, topic discovery, and natural-language Q&A about any GitHub repository indexed by Devin. Supports public and private repositories (private requires Devin API key). Falls back gracefully to Glob/Grep/Read + QMD if not configured. Invokable standalone or called by other skills as a data source.
location: managed
context: fork
allowed-tools:
  - ToolSearch
  - mcp__devin__read_wiki_structure
  - mcp__devin__read_wiki_contents
  - mcp__devin__ask_question
  - Glob
  - Grep
  - Read
---

# DeepWiki: Codebase Intelligence Data Source

Execute this skill to retrieve structured, AI-grounded codebase understanding from Devin's DeepWiki. Use it as an optional data source when Glob/Grep/Read gives you file contents but not architectural intent, or when QMD doesn't have the repository indexed.

---

## What DeepWiki Provides

DeepWiki indexes GitHub repositories and generates structured documentation — architecture, component relationships, design decisions, API contracts — then exposes it through three MCP tools:

| Tool | Purpose | When to use |
|------|---------|-------------|
| `read_wiki_structure` | Lists all documentation topics for a repo | Explore what's documented — find the right topic before reading |
| `read_wiki_contents` | Retrieves documentation for a specific topic | Read architectural intent, component descriptions, design decisions |
| `ask_question` | Natural-language Q&A grounded in the indexed repo | Get answers that synthesize across multiple parts of the codebase |

**vs. Glob/Grep/Read:** Those tools give you raw file contents. DeepWiki gives you synthesized understanding — what the code *means*, not just what it says.

**vs. QMD:** QMD indexes your local markdown documents (specs, ADRs, docs). DeepWiki indexes the codebase itself and generates documentation from it. Complementary, not overlapping.

---

## Step 1: Pre-Flight — Check Availability

Before using any DeepWiki tool, verify the MCP server is configured:

```
ToolSearch: "devin"
```

If `mcp__devin__read_wiki_structure`, `mcp__devin__read_wiki_contents`, and `mcp__devin__ask_question` appear → **DeepWiki is available**.

If not found → **fall back to local tools** (see Fallback section below).

**Setup for callers who get SKIPPED:** DeepWiki requires a Devin API key. Configure via:
```bash
claude mcp add -s user -t http devin https://mcp.devin.ai/mcp -H "Authorization: Bearer <API_KEY>"
```
Once configured, ToolSearch will find the tools on next invocation.

---

## Step 2: Identify Target Repository

DeepWiki operates on GitHub repositories. Extract the target repo from context:

```yaml
target:
  repo: "{owner}/{repo}"         # e.g., "anthropics/claude-code"
  question_or_topics: []         # What you want to know
```

**To find the repo URL:** Check `git remote -v`, `package.json`, `go.mod`, or ask the user.

---

## Step 3: Discover Documentation Structure

Always start with structure before reading content — it tells you what topics exist and saves you from reading irrelevant sections:

```
mcp__devin__read_wiki_structure(repo="{owner}/{repo}")
```

Returns a list of topic titles and descriptions. Scan for topics relevant to your question.

---

## Step 4: Read Topic Content or Ask a Question

### Option A: Read specific documentation

When you know which topic from Step 3 is relevant:

```
mcp__devin__read_wiki_contents(repo="{owner}/{repo}", topic="{topic from Step 3}")
```

Returns structured documentation for that topic: architecture, design decisions, component descriptions, API contracts.

### Option B: Ask a natural-language question

When you need a synthesized answer across multiple topics:

```
mcp__devin__ask_question(repo="{owner}/{repo}", question="{your question}")
```

**Good questions for `ask_question`:**
- "What is the main entry point for HTTP request handling?"
- "How does authentication flow work end-to-end?"
- "What does the job queue system use for persistence?"
- "Which components are responsible for {domain concern}?"
- "What are the primary dependencies between module A and module B?"
- "What design pattern does this codebase use for {pattern area}?"

**Poor questions** (better served by Grep): "What does function X do?" — ask_question is for architectural/cross-cutting questions, not per-function lookup.

---

## Usage Patterns by Calling Context

### Called by context (domain detection)

```
Question: "What are the primary domains this codebase deals with? What are the main technical concerns?"
→ Use answer to supplement domain-registry signal matching
```

### Called by bridge-claude / domain experts (pre-analysis context)

```
Question: "What is the architecture of {component}? What design decisions constrain how it works?"
→ Pass answer as context to domain expert Task agent — reduces blind spots from reading code without intent
```

### Called by deep-research (technical background)

```
Question: "How does {feature} currently work in this codebase before I research alternatives?"
→ Grounds external research findings in current implementation reality
```

### Called by deep-council (scope understanding)

```
Topics: read_wiki_structure → identify relevant docs → read_wiki_contents for scope areas
→ Attach to bridge_input.context_summary to give bridges richer understanding
```

### Standalone invocation (direct codebase exploration)

Invoke directly when the user asks a high-level architectural question:
```
User: "How does the payment processing work in this repo?"
→ ask_question(repo="...", question="How does payment processing work? What are the components involved?")
```

---

## Output Format

Return structured context from DeepWiki:

```json
{
  "source": "deepwiki",
  "repo": "{owner}/{repo}",
  "method": "read_wiki_contents | ask_question",
  "topic": "{topic name, if applicable}",
  "question": "{question asked, if applicable}",
  "answer": "{content from DeepWiki}",
  "confidence": "high | medium | low",
  "confidence_note": "high = DeepWiki answer; medium = local fallback; low = neither available",
  "availability": "deepwiki | local_fallback | unavailable"
}
```

---

## Fallback — When DeepWiki Is Not Available

If `mcp__devin__*` tools are not configured, fall back in this order:

```
1. QMD (if available): qmd vector_search "{question}" —collection "{project}"
2. Glob + Read: find architecture docs, ADRs, README, module structure
3. Grep: search for relevant patterns in source files
4. Flag in output: availability = "local_fallback", confidence = "medium"
```

Fallback output should note: "DeepWiki not configured — answers from local file analysis. Configure via: claude mcp add -s user -t http devin https://mcp.devin.ai/mcp -H 'Authorization: Bearer <API_KEY>'"

**Fallback is non-blocking.** Callers receive reduced-confidence context, not an error.

---

## Notes

- **Public repos**: Accessible without authentication via the public DeepWiki at app.devin.ai/wiki/{owner}/{repo}
- **Private repos**: Require Devin API key (team plan or above) — see setup above
- **Index freshness**: DeepWiki indexes are generated periodically; recent code changes may not be reflected immediately
- **Not a substitute for reading code**: DeepWiki gives intent and architecture; Glob/Grep/Read gives exact current implementation. Use both.
- **Graceful SKIP**: If neither DeepWiki nor local tools provide useful context, return `availability: "unavailable"` — callers continue without codebase context
