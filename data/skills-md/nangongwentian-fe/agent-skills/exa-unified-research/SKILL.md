---
name: exa-unified-research
description: "Unified Exa research skill using get_code_context_exa and web_search_advanced_exa. Use for code/API snippet lookup, company research, people/LinkedIn research, financial report search, research paper search, personal site search, and X/Twitter tweet search. Follow progressive disclosure: load only the relevant reference file(s) for the user intent."
---

# Exa Unified Research

## Progressive Disclosure Router

Read only the minimum required reference files:
- Code examples / API docs / debugging: `references/code-search.md`
- Company and market research: `references/company-research.md`
- People and profile research: `references/people-research.md`
- SEC/earnings/filings: `references/financial-report-search.md`
- Academic papers: `references/research-paper-search.md`
- Blogs/portfolios: `references/personal-site-search.md`
- X/Twitter discussion and sentiment: `references/tweet-search.md`

For mixed requests, load only the relevant subset and merge results at the end.

## Global Tool Restriction

Only use:
- `get_code_context_exa`
- `web_search_advanced_exa`

Do not use `web_search_exa` or other Exa tools unless the user explicitly overrides this skill policy.

## Global Token Isolation

Avoid large raw Exa outputs in main context.
Use task/sub-agent delegation when available:
- Run Exa calls inside sub-task
- Deduplicate and normalize before returning
- Return only distilled output to main context

If sub-agent is unavailable, run narrow iterative queries and summarize aggressively.

## Global Query Strategy

- Include explicit domain terms, entities, versions, and constraints in query
- Use 2-3 query variations for recall-sensitive tasks
- Merge and deduplicate by canonical URL/entity key
- Tune `numResults` by user intent instead of hardcoding:
  - "a few": 10-20
  - "comprehensive": 50-100
  - explicit number: follow user request

## Default Output Contract

Return:
1. Structured results (table or compact JSON)
2. Source URLs with one-line relevance
3. Notes on uncertainty/conflicts and coverage gaps
