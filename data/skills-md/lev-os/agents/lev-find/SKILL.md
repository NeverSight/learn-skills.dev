---
name: lev-find
description: |
  [WHAT] Context retrieval backend for `lev get` (legacy name: lev-find).
  [HOW] RRF fusion across indexes (codebase, docs, sessions, tasks, memory) plus optional research backends.
  [WHEN] Use for context gathering, prior art, and memory recall.
  [WHY] Keeps one root primitive (`get`) while preserving `find/search` aliases.

  Triggers: "find", "search", "lookup", "where is", "locate", "discover", "what do we have on",
            "related work", "prior art", "recall", "remember", "what did we discuss",
            "search memory", "find in history", "conversation history"

  Category: GET (context gathering, memory recall, semantic search)
  Indexes: codebase, documentation, ideas, sessions, tasks, skills, memory
skill_type: tool
category: process-get
primary_primitive: get
legacy_aliases: [find, search, lookup]

lifecycle_integration:
  stage: all stages (GET operation)
  input_artifact: query string
  output_artifact: ranked search results with RRF fusion
---

# lev-find (Backend for `lev get`)

> `lev find` remains a compatibility alias. Prefer `lev get`.

## Overview

`lev get` orchestrates semantic search across multiple indexes (codebase, docs, ideas, sessions, tasks) and fuses results using Reciprocal Rank Fusion (RRF) for comprehensive discovery.

## When to Use

Use `lev get` when:
- **Cross-domain search** - Finding related code, docs, and discussions
- **Architecture discovery** - Locating design decisions and patterns
- **Context gathering** - Understanding how something works across the codebase
- **Task awareness** - Finding related work and TODOs

Use Grep/Glob when:
- **Exact matches** - Searching for specific strings or patterns
- **Known locations** - You know approximately where to look
- **File listing** - Just need to find files by name

## Basic Usage

```bash
# Search everywhere (auto-selects relevant indexes)
lev get "error handling"

# Search with explicit indexes
lev get "auth" --indexes codebase,documentation

# Include tasks in search
lev get "TODO authentication" --indexes codebase,tasks
```

## External Search Backends

**MANDATE:** All research/find queries MUST load and use **exa** + **deep-research** + **valyu** for comprehensive discovery.

### Exa (Neural Web + GitHub Search)

Exa provides semantic web search and GitHub code discovery.

**Setup:**
```bash
export EXA_API_KEY="your-key-here"
```

**Usage:**
```bash
# Search web for docs/examples
lev get "react authentication patterns" --scope=web

# Search GitHub repos
lev get "voice assistant typescript" --scope=github

# Combined: local code + web
lev get "deployment strategies" --scope=code,web
```

### Valyu (Recursive Deep Research)

Valyu provides turn-based iterative refinement with confidence scoring (1-10 turns).

**Usage:**
```bash
# Recursive research with automatic refinement
valyu research "authentication best practices 2026" \
  --turns 5 \
  --threshold 0.85 \
  --strategy balanced

# Research strategies:
# - breadth: 20 sources, broad coverage
# - depth: 10 sources, comprehensive understanding
# - balanced: 15 sources, general-purpose (default)

# Deep research (mandate exa + deep-research + valyu)
lev get "authentication patterns" --scope=research
```

**How it works:**
1. Turn 1: Initial search + AI answer with confidence scoring
2. AI suggests refined query based on knowledge gaps
3. Turns 2-N: Iterative deepening until confidence >= threshold
4. Final synthesis across all turns

**Mandatory Loading:**
- `--scope=research` → MUST load exa + deep-research + valyu
- Any deep research → Use valyu for iterative refinement
- Any find/research skill invocation → Load all backends

**Config:**
```yaml
index:
  backends:
    exa:
      enabled: true
      api_key: ${EXA_API_KEY}
      scopes: [web, github, research]
    valyu:
      enabled: true
      api_key: ${VALYU_API_KEY}
      required_for: [research, deep_research]
```

**See:** `skill://valyu` for complete recursive research documentation.

---

## Index Types

| Index | Content | Tool |
|-------|---------|------|
| `codebase` | Source code (agent, core, plugins) | ck |
| `documentation` | Docs, ADRs, architecture | leann |
| `ideas` | Ideas, brainstorming, vision docs | leann |
| `sessions` | Session notes, discussions | leann |
| `tasks` | bd issues and TODOs | bd |
| `skills` | POC skills from ~/lev/workshop/poc/lookup | lookup CLI |
| `memory` | AutoMem stored memories (decisions, context) | memory_search |
| `web` | External web search via Exa neural search | exa-plus skill |

## Memory Index (AutoMem Integration)

The `memory` index connects to Clawdbot's AutoMem extension:

```bash
# Search memories
lev get "authentication decision" --indexes memory

# Combined search (code + memory)
lev get "why did we choose JWT" --indexes codebase,documentation,memory
```

**Direct AutoMem tools** (available via clawdbot skill):
- `memory_search` - Semantic search across stored memories
- `memory_get` - Retrieve specific memory by ID
- `memory_store` - Store new memory
- `memory_forget` - Delete memory

**Bash fallback** (when MCP unavailable):
```bash
# Direct AutoMem API query
curl -s "http://localhost:8001/search?q=authentication&limit=5" | jq '.results'

# Store a memory
curl -X POST "http://localhost:8001/store" \
  -H "Content-Type: application/json" \
  -d '{"content": "We chose JWT for stateless auth", "tags": ["decision", "auth"]}'
```

**Session history search** (conversation grep):
```bash
# Find in recent sessions
find ~/.clawdbot/agents/main/sessions -name "*.jsonl" -mtime -1 \
  -exec grep -l "keyword" {} \;

# Parse session content
jq -r 'select(.type=="message") | .message.content[0].text // empty' \
  < ~/.clawdbot/agents/main/sessions/{ID}.jsonl | grep -i "keyword"
```

## Search Patterns

### Finding Code Patterns
```bash
lev get "authentication middleware implementation"
lev get "how to handle errors" --indexes codebase
```

### Finding Architectural Decisions
```bash
lev get "why hexagonal architecture" --indexes documentation
lev get "ADR memory system" --indexes documentation
```

### Finding Related Work
```bash
lev get "what exists for caching" --indexes codebase,documentation,tasks
lev get "previous discussion about X" --indexes sessions
```

### Finding Tasks
```bash
lev get "blocked on oauth" --indexes tasks
lev get "TODO refactor" --indexes codebase,tasks
```

### Finding Skills (Decision Frameworks, Patterns)
```bash
lev get "decision making" --indexes skills
lev get "how to handle complexity" --indexes skills,documentation
lev get "debugging patterns" --indexes skills,codebase
```

## Understanding Results

Results are fused using RRF (Reciprocal Rank Fusion):
- Results from multiple sources are merged
- Duplicate paths are deduplicated
- Final ranking reflects consensus across indexes

Output includes:
- **path** - File or issue location
- **score** - RRF fusion score (higher = more relevant)
- **source** - Which index matched
- **snippet** - Relevant text excerpt

## Routing Rules

The manifest auto-routes queries:
- `TODO|FIXME|task` → tasks index
- `idea|vision` → ideas + _global
- Default → codebase + documentation + _global

Override with `--indexes` for explicit control.

## Integration with bd

Search creates trackable jobs:
```bash
# View search history
bd list --label find-job

# Resume interrupted search
lev get --resume job-a3f8e9
```

## Tips

### Narrow Results
```bash
# Too many results? Add specificity
lev get "JWT token refresh" --indexes codebase

# Or filter by path patterns
lev get "auth" | grep middleware
```

### Broaden Results
```bash
# Missing results? Search more indexes
lev get "caching" --indexes codebase,documentation,ideas,tasks
```

### Domain Expansion Ladder (When Stuck)

If initial search fails, climb the abstraction ladder:

```
Level 1: File/Function    → "find auth.ts" (exact match)
Level 2: Component        → "authentication module" (scope wider)
Level 3: Topic            → "auth patterns" (pattern match)
Level 4: Similar          → "how NextAuth does this" (prior art)
Level 5: Goals            → "secure user sessions" (problem space)
Level 6: Ideas            → "zero-trust principles" (concepts)
```

**Usage:** Start at your certainty level, climb UP when results sparse:
```bash
# Level 1 failed? → Expand to Level 2
lev get "bd-daemon" --indexes codebase       # 0 results
lev get "daemon sync module" --indexes codebase,documentation  # 29 results

# Level 2 too specific? → Climb to Level 3
lev get "auto-sync patterns" --indexes codebase,ideas,sessions

# Unfamiliar domain? → Jump to Level 5-6
lev get "what problem does caching solve" --indexes ideas,sessions
```

**Rule:** Level 2 (component) is typically the sweet spot for codebase searches.

### Combine with Other Tools
```bash
# Find then read
lev get "error handling" | head -5  # Get top results
# Then use Read tool on specific files

# Find then grep for specific lines
lev get "auth middleware" --indexes codebase
# Then grep -n "function" in the matched files
```

## Query Expansion Features

### Empty Query: Random Skill Discovery

When searching the skills index without a query, get 5 random skills for exploration:

```bash
lev get "" --indexes skills
# Returns 5 random skills from the POC catalog
```

**Use case**: Discover new decision frameworks and patterns you didn't know existed.

### Related Query Suggestions

After search results, lev-find suggests 2-3 related queries to explore:

```bash
lev get "authentication patterns" --indexes skills

# Results shown...

💡 Related searches you might find useful:
  - "authorization access control"
  - "session management security"
  - "identity verification methods"
```

### Skill Categories for Exploration

Browse skills by category to understand the landscape:

```bash
# Categories available:
- dev         (Software engineering, patterns, architecture)
- strategy    (Business strategy, competitive analysis)
- cognitive   (Mental models, biases, heuristics)
- decision    (Decision-making frameworks)
- systems     (Systems thinking, complexity)
- design      (UI/UX, product design)

# Example: Explore all decision-making skills
lev get "decision" --indexes skills
# Then use category filter if integrated with lookup CLI
```

## Related Search Tools

**lev-find is the unified orchestrator. For specialized searches, use:**

| Tool | Specialty | Use When |
|------|-----------|----------|
| **lev-find** (this) | Unified local + external search | Default choice, cross-domain discovery |
| **lev-research** | Multi-perspective orchestration | Architecture analysis, research workflows |
| **deep-research** | Tavily multi-query synthesis | Complex research, iterative refinement |
| **valyu** | Recursive turn-based research | Confidence-driven, automatic query expansion |
| **brave-search** | Quick web search | Fast lookups, documentation |
| **tavily-search** | AI-optimized single search | Clean snippets, current info |
| **exa-plus** | Neural web search | GitHub, LinkedIn, research papers |
| **grok-research** | X/Twitter, real-time | Social sentiment, trending topics |
| **firecrawl** | Web scraping | Content extraction, site mapping |
| **qmd** | Local markdown/JSONL search | Session history, conversation search |
| **agent-browser** | Interactive web automation | Form filling, testing, screenshots |

**Decision tree:**
```
Need to search? → Start here:
├─ Local (code/docs/sessions) → lev get
├─ External web (quick) → brave-search or tavily-search
├─ External web (deep) → deep-research or valyu
├─ Social/real-time → grok-research
├─ Structured scraping → firecrawl
├─ Interactive browser → agent-browser
└─ Multi-perspective → lev-research
```

**See also:**
- `skill://lev-research` - Main research orchestrator
- `skill://deep-research` - Tavily deep research
- `skill://valyu` - Recursive research

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `lev get "query"` | Search all default indexes |
| `lev get "query" --indexes X,Y` | Search specific indexes |
| `lev get "" --indexes skills` | Random skill discovery (5 samples) |
| `lev get --resume ID` | Resume interrupted search |
| `bd list --label find-job` | Search history |

## Integration with lookup CLI

The skills index is powered by ~/lev/workshop/poc/lookup CLI:

```bash
# Direct CLI usage (alternative to lev get)
cd ~/lev/workshop/poc/lookup
./cli.js find "decision making"
./cli.js list --tag=decision
./cli.js load <skill-id>
```

See lookup CLI documentation for advanced features like hybrid search, tag filtering, and skill loading.

## Relates

### Master Router
- **Lev Master Router** (`lev/SKILL.md`) - Routes all lev-* skills
  Parent skill that dispatches to this skill based on keywords/context

## Technique Map
- **Role definition** - Clarifies operating scope and prevents ambiguous execution.
- **Context enrichment** - Captures required inputs before actions.
- **Output structuring** - Standardizes deliverables for consistent reuse.
- **Step-by-step workflow** - Reduces errors by making execution order explicit.
- **Edge-case handling** - Documents safe fallbacks when assumptions fail.

## Technique Notes
These techniques improve reliability by making intent, inputs, outputs, and fallback paths explicit. Keep this section concise and additive so existing domain guidance remains primary.

## Prompt Architect Overlay
### Role Definition
You are the prompt-architect-enhanced specialist for lev-find, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

### Input Contract
- Required: clear user intent and relevant context for this skill.
- Preferred: repository/project constraints, existing artifacts, and success criteria.
- If context is missing, ask focused questions before proceeding.

### Output Contract
- Provide structured, actionable outputs aligned to this skill's existing format.
- Include assumptions and next steps when appropriate.
- Preserve compatibility with existing sections and related skills.

### Edge Cases & Fallbacks
- If prerequisites are missing, provide a minimal safe path and request missing inputs.
- If scope is ambiguous, narrow to the highest-confidence sub-task.
- If a requested action conflicts with existing constraints, explain and offer compliant alternatives.
