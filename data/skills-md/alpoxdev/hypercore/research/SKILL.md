---
name: research
description: Run structured general-purpose research and produce human-readable reports. Use when users ask for fact-finding, comparisons, market/trend analysis, or evidence-based summaries with quick/standard/deep depth.
compatibility: Requires external search-capable tooling (WebSearch/WebFetch/MCP where available) and source-verification capability.
---

# Research Skill

> General research -> human-readable structured report.

<purpose>

Input: topic (natural language) + optional depth (`--quick` / default / `--deep`)
Output: `.hypercore/research/[NN].topic_summary.md`

</purpose>

<trigger_conditions>

| Trigger | Action |
|------|------|
| `/research AI agent framework comparison` | Technical comparison research |
| `/research --deep Korea SaaS market trends` | Deep market research |
| `/research --quick WebSocket vs SSE` | Fast technical comparison |
| "Research X for me" | Clarify topic, then execute |

If ARGUMENT is missing, ask immediately: "What topic should I research?"

</trigger_conditions>

<depth_levels>

| Mode | quick | standard (default) | deep |
|------|------|------|------|
| Query count | 3-5 | 5-10 | 10-15 |
| Agents | researcher 2 + explore 0-1 | researcher 3-4 + explore 0-1 | researcher 4-5 + explore 1 + MCP |
| Iterative pass | No | No | Yes |
| Minimum sources | 5 | 10 | 20+ |
| Report size | 500-1000 chars | 1500-3000 chars | 3000-6000 chars |

</depth_levels>

<topic_classification>

| Type | Keywords | Channels |
|------|------|------|
| Technical comparison | vs, compare | WebSearch + explore(gh) |
| Market/trend | market, trend | WebSearch + Firecrawl |
| Competitor analysis | competitor, alternatives | WebSearch + GitHub MCP |
| Academic/concept | principle, paper | WebSearch(arXiv) + WebFetch |
| Internal project | our code | explore + Grep |
| Library/package | `package@version` | Delegate to docs-fetch |

</topic_classification>

<mandatory_reasoning>

## Mandatory Sequential Thinking

- Always use `sequential-thinking` for Phase 1 (query strategy design).
- For deep mode, also use `sequential-thinking` in Phase 3 (gap analysis and second-pass query planning).
- Include current year (`2026`) in recency-sensitive query sets.
- Do not produce conclusions without explicit structured reasoning.

</mandatory_reasoning>

<parallel_agent_execution>

- Use Agent Teams first when 3+ workers are needed.
- Fallback to parallel Task calls when Agent Teams is unavailable.
- quick mode (<=2 workers) may run direct parallel tasks.

</parallel_agent_execution>

<workflow>

| Phase | Task | Tool |
|------|------|------|
| 0 | Parse input + detect MCP + classify topic | ToolSearch |
| 1 | Build search strategy | Sequential Thinking (2 steps) |
| 2 | Parallel collection | researcher + explore + MCP |
| 3 | Gap analysis + second-pass collection (deep only) | analyst -> researcher |
| 4 | Build report | general-purpose |
| 5 | Save + return concise summary | Write |

### Phase 1 requirements
- Define 3-5 core research questions
- Define scope (time/region/language)
- Generate bilingual query set when useful
- Assign channels/agents intentionally

### Phase 4 writing principles
- Conclusion first (pyramid principle)
- Every key claim must include source URL
- Progressive disclosure (summary -> detail)
- Use comparison tables where relevant

</workflow>

<report_template>

```markdown
# [Topic] Research Report

> Date: YYYY-MM-DD | Depth: quick/standard/deep | Sources: N reviewed, M cited

## Executive Summary
[250-400 chars, conclusion first]

## 1. Research Scope
### 1.1 Background
### 1.2 Scope
### 1.3 Method

## 2. Key Findings
### 2.1 [Finding 1]
Core: [one-line summary]
Details: ...
Source: [Title](URL)

## 3. Comparative Analysis (if needed)
| Criteria | A | B | C |
|------|---|---|---|

## 4. Trends and Implications

## 5. Conclusion and Recommendations

## References
- [Title](URL)
```

</report_template>

<validation>

| Item | Required |
|------|------|
| ARGUMENT | Ask immediately if missing |
| Strategy | Sequential-thinking trace for query strategy |
| Sources | quick 5+, standard 10+, deep 20+ |
| Recency | Include year/date awareness in source checks |
| Output | Executive summary + sources + recommendations |
| Save | `.hypercore/research/[NN].*.md` |

Forbidden:
- Claims without sources
- Comparison conclusions without comparison evidence
- Exiting without saving output

</validation>
