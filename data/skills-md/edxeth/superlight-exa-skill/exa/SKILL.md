---
name: exa
description: Searches the web using Exa's neural embeddings-based search API. Use when needing real-time web information to answer questions, verify facts, debug issues, find code examples, research topics, or clear doubts with authoritative sources. Best for open-ended research, fact-checking, troubleshooting errors with web context, and getting AI answers with citations.
---

# Exa Web Search

AI-powered semantic web search for real-time information, research, and fact verification.

## When to Use

**Use Exa** when you need to:
- Verify facts or clear doubts with current web sources
- Debug errors by searching for solutions and stack traces
- Research topics with up-to-date information
- Find code examples, tutorials, and implementation patterns
- Get AI-generated answers with citations to authoritative sources
- Discover similar pages or find related content
- Search for companies, people, research papers, or news

## Protocol

### Step 1: Web Search

```bash
scripts/exa.sh search "<query>" [numResults] [category]
```

**Categories**: `company`, `research paper`, `news`, `pdf`, `github`, `tweet`, `personal site`, `people`

**Example:**
```bash
scripts/exa.sh search "latest LLM research papers on context windows" 5 "research paper"
```

### Step 2: Get Page Contents (optional)

```bash
scripts/exa.sh contents "<url1>" ["<url2>" ...]
```

**Example:**
```bash
scripts/exa.sh contents "https://arxiv.org/abs/2307.06435"
```

### Step 3: Find Similar Pages

```bash
scripts/exa.sh similar "<url>" [numResults]
```

**Example:**
```bash
scripts/exa.sh similar "https://github.com/anthropics/anthropic-cookbook" 5
```

### Step 4: Get AI Answer with Citations

```bash
scripts/exa.sh answer "<question>"
```

**Example:**
```bash
scripts/exa.sh answer "What is the current valuation of SpaceX?"
```

### Step 5: Search Code Context

```bash
scripts/exa.sh code "<programming query>"
```

**Example:**
```bash
scripts/exa.sh code "React useCallback hook examples with TypeScript"
```

## Critical Rules

1. **Specific queries win** - "React useState TypeScript patterns" beats "react hooks"
2. **Include error messages** - For debugging, include the actual error text in query
3. **Use categories** - Append category for better results (research paper, github, news)
4. **Verify with answer** - Use `answer` command to get fact-checked responses with citations
5. **Current year is 2026** - Use this when recency matters; omit for timeless topics or use older years when historically relevant
6. **No guessing** - If search returns nothing, ask user before proceeding

## Resources

See `reference/troubleshooting.md` for error handling, configuration, and common issues.
