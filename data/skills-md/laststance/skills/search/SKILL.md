---
name: search
description: Multi-tool cited research
argument-hint: "<question or topic to research>"
---

# /search — Iterative Multi-Tool Research

## Codex Compatibility
When running this skill in Codex, translate Claude Code-only primitives before acting: `AskUserQuestion` -> chat/request_user_input, `TodoWrite` -> `update_plan`, `Task`/`TaskCreate`/`TeamCreate`/`SendMessage` -> `spawn_agent`/`send_input`/`wait_agent` when available and allowed, and `EnterPlanMode`/`ExitPlanMode` -> a concise chat plan plus explicit approval.
Resolve `Read`/`Write`/`Edit`/`Bash`/`WebSearch`/`WebFetch` to Codex file/shell/web tools, and map `~/.claude/...` paths to `~/.agents/...` or `~/.codex/...` unless the task explicitly targets Claude Code.

## Cursor Compatibility
When running this skill in Cursor Agent, translate Claude Code-only primitives before acting: `AskUserQuestion` -> `AskQuestion`; `TodoWrite` -> Cursor `TodoWrite` or an equivalent checklist; `Task`/`TaskCreate`/`TeamCreate`/`SendMessage`/multi-agent flows -> Cursor `Task` (subagents), parallel Tasks, or `run_in_background` when allowed (`TeamCreate`/`SendMessage` may have no exact match); `EnterPlanMode`/`ExitPlanMode` -> Plan mode (`SwitchMode` / `CreatePlan`) plus explicit user approval.
Resolve `Read`/`Write`/`Edit`/`StrReplace`/`Bash`/web/search/MCP via Cursor Composer or Agent equivalents. MCP names written as `mcp__server__tool` typically map to `call_mcp_tool` with configured server identifiers. Map `~/.claude/...` to `~/.cursor/skills/`, `.cursor/skills/`, and `.cursor/rules/` unless the task explicitly targets Claude Code.


Research the user's question by orchestrating every available search tool — WebSearch, WebFetch, and installed MCPs (Exa, Perplexity, Tavily, Context7, DeepWiki) — iterating with **different tool families** until the answer is satisfactory or three passes are exhausted.

## Workflow

### Step 1 — Classify the question

Pick the best **first tool** based on question type. Use the table below; if the chosen MCP is not installed, fall back to the next row.

| Question type | First tool | Why |
|---|---|---|
| Named library / framework / SDK API | `mcp__context7__resolve-library-id` → `mcp__context7__query-docs` | Authoritative, version-correct |
| Specific GitHub repo internals | `mcp__deepwiki__ask_question` | Indexed wiki + code |
| Known URL to read | `WebFetch` (or `mcp__exa__web_fetch_exa`) | Direct content |
| Comparison / "which is better" / synthesis | `mcp__perplexity__reason` | Built for reasoning across sources |
| Deep multi-source research | `mcp__perplexity__deep_research` or `mcp__tavily__tavily_research` | Long-form, multi-citation |
| Recent events / news | `WebSearch` + `mcp__tavily__tavily_search` | Fresh index |
| General factual lookup | `WebSearch` | Fast default |

If no MCPs are installed, use `WebSearch` + `WebFetch` only.

### Step 2 — Search loop (max 3 passes)

```
Pass 1: Run the best-fit tool with a focused query.
        → Apply Step 3 satisfaction criteria.
Pass 2: If gaps remain → switch to a DIFFERENT tool family
        (different web index or different reasoning style).
Pass 3: If still unresolved → escalate to deep_research
        / tavily_research, OR fetch the most promising URL
        directly with WebFetch.
```

Stop early as soon as the answer is satisfactory. After Pass 3, surface what is known with a confidence label and ask the user to narrow scope rather than burning more passes.

### Step 3 — Satisfaction criteria

A result is satisfactory only when **all** of the following hold:

- The core question is directly answered (not just adjacent topics).
- At least one citation / source URL backs each non-trivial claim.
- No major contradiction between sources. If contradicted, reconcile or flag.
- Recency matches the question (current-events questions → sources < 6 months old).

If any criterion fails, run another pass with a **different tool family** or a **materially refined query** (new keywords, narrower scope, different framing).

### Step 4 — Tool diversity rule

Each pass MUST use a different tool family. Re-running the same tool with reworded text rarely yields new information. Prefer crossing these boundaries:

- WebSearch ↔ Tavily ↔ Perplexity (different web indices)
- Context7 ↔ DeepWiki (different doc sources)
- Search ↔ Fetch (broad → specific)

### Step 5 — Answer format

Respond in the user's language. Default template:

```
**Answer**: <one or two sentences, direct>

**Why** (key evidence):
- <claim> — <source url>
- <claim> — <source url>

**Confidence**: high / medium / low
**Tools used**: <list>
**Open questions** (if any): <…>
```

Keep raw tool dumps out of the answer — synthesize, then cite.

## Tool quick-reference

**Always available**
- `WebSearch` — generic web search
- `WebFetch` — fetch a known URL

**MCPs (use whichever are installed)**
- `mcp__exa__web_search_exa`, `mcp__exa__web_fetch_exa` — Exa search & fetch
- `mcp__perplexity__search` — Perplexity quick search
- `mcp__perplexity__reason` — synthesis / comparison
- `mcp__perplexity__deep_research` — long-form research
- `mcp__tavily__tavily_search` — Tavily search
- `mcp__tavily__tavily_extract` — extract content from a URL
- `mcp__tavily__tavily_research` — Tavily deep research
- `mcp__tavily__tavily_crawl`, `mcp__tavily__tavily_map` — site exploration
- `mcp__context7__resolve-library-id` → `mcp__context7__query-docs` — library docs
- `mcp__deepwiki__ask_question`, `read_wiki_contents`, `read_wiki_structure` — GitHub wiki

## Anti-patterns

- Re-running the **same tool** with a slightly reworded query — switch tool families instead.
- Skipping classification (Step 1) and defaulting to `WebSearch` for everything.
- Stopping at Pass 1 when the answer is partial or uncited.
- Going past Pass 3 — diminishing returns; surface what is known and ask the user to narrow scope.
- Pasting raw tool output as the answer — always synthesize and cite.
- Using `deep_research` / `tavily_research` on Pass 1 — too slow; reserve for escalation.

## Examples

### Example 1 — "How do I use Suspense with `use()` in React 19?"
- Pass 1: `context7__resolve-library-id` → `query-docs` for React 19.
- Satisfactory? Yes (official docs, code example, version-correct) → answer with cited snippet. Done in one pass.

### Example 2 — "Latest funding round for Anthropic"
- Pass 1: `WebSearch` → news headlines.
- Pass 2: `tavily_search` to confirm date and amount across multiple outlets.
- Cross-checked → answer with two source URLs and confidence: high.

### Example 3 — "Why is my Next.js v16 build slow with Turbopack?"
- Pass 1: `context7__query-docs` for Next.js v16 perf docs.
- Pass 2: `deepwiki__ask_question` on `vercel/next.js` for known issues.
- Pass 3: `WebSearch` for recent GitHub discussions / blog posts.
- Synthesize root causes with citations; flag any unresolved hypotheses as open questions.
