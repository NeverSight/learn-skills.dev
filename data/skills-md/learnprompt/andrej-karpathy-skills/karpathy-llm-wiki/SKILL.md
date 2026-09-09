---
name: karpathy-llm-wiki
description: 'Build and maintain an LLM-powered personal knowledge base or wiki. Use this skill when the user wants to organize research notes, build a second brain, set up an Obsidian vault with LLM compilation, ingest papers or articles automatically, or mentions "personal knowledge base", "LLM wiki", "second brain", "knowledge management", "ingest papers", "obsidian + LLM". Based on Karpathy Gist and 59k-like post.'
disable-model-invocation: false
user-invocable: true
related_skills:
  - karpathy-autoresearch
  - karpathy-output-evolution
  - karpathy-education-first
  - karpathy-idea-files
---

# Skill 2: LLM Wiki / Personal Knowledge Base（LLM知识库）

> Source: https://x.com/karpathy/status/2039805659525644595 | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
> "59k likes — LLM Knowledge Bases" — top-2 most-liked post

## Core Principle

**You explore. The LLM maintains.**

You read the world, capture raw signals. The LLM compiles, cross-links, deduplicates, lint-checks, and surfaces contradictions. Your Obsidian vault is the output, not the input.

## Architecture

```
RAW INPUTS                 LLM LAYER                  OUTPUT
──────────                 ─────────                  ──────
Papers (PDF/arXiv)  ──→   ingest.py              ──→  entities/*.md
Articles (URL)      ──→   compile_wiki.py        ──→  index.md
Chat logs           ──→   lint_wiki.py           ──→  contradiction_log.md
Notes (voice/text)  ──→   query_wiki.py          ──→  slides/
                          update_entity.py       ──→  weekly_digest.md
```

## The 5 Core Prompts

### 1. Ingest Prompt
```
You are a knowledge compiler. Given this raw source:

[PASTE RAW CONTENT]

Source URL/title: [SOURCE]
Date: [DATE]

Extract and output:
1. Key entities (people, concepts, tools, papers) — one per line with a 2-sentence description
2. Key claims with confidence level (high/medium/speculative)
3. Connections to existing topics: [LIST YOUR KNOWN TOPICS]
4. Contradictions with anything you know: [WHAT YOU ALREADY BELIEVE]
5. Suggested entity page updates (format: ENTITY_NAME | UPDATE_TEXT)
```

### 2. Compile Wiki Entry Prompt
```
You are maintaining a personal knowledge wiki. Update the entity page for [ENTITY_NAME].

Existing page content:
[CURRENT_PAGE_CONTENT]

New information to integrate:
[NEW_INFO]

Rules:
- Preserve all existing information; only add or correct
- Flag contradictions with: ⚠️ CONFLICT: [old claim] vs [new claim]
- Keep the page under 500 words
- End with: "Last updated: [DATE] | Sources: [LINKS]"
```

### 3. Weekly Ingest Prompt (run every week)
```
Process this week's reading list:
[PASTE 5-10 ITEMS: title + URL + 1-sentence summary]

For each item:
1. Extract top 3 entities to update
2. List 2-3 key claims worth adding to wiki
3. Note any contradictions with existing knowledge
4. Suggest connections to other entities in my wiki

Output as structured markdown, one section per item.
```

### 4. Lint / Contradiction Check Prompt
```
Review these wiki entries for consistency:

[PASTE 3-5 RELATED ENTITY PAGES]

Find and report:
1. Factual contradictions between pages
2. Duplicate information that should be merged
3. Outdated claims that should be flagged
4. Missing cross-links between related entities

Format: ISSUE | PAGE | LINE | SUGGESTED FIX
```

### 5. Query Prompt
```
Search my personal knowledge wiki to answer this question:

Question: [QUESTION]

Wiki context:
[PASTE RELEVANT PAGES]

Answer with:
1. Direct answer (2-3 sentences)
2. Supporting evidence from wiki (with page citations)
3. Gaps: what I don't know yet
4. Suggested reading to fill gaps
```

## Memory / Context Hygiene (Anti-Pollution Rules)

Karpathy noted LLM memory "trying too hard" — a question from 2 months ago poisons every future conversation. Prevent this:

- **Never rely on LLM built-in memory** for knowledge — use your wiki instead
- **Start fresh sessions** for new topics; don't let old context bleed in
- **Explicit resets**: If continuing a long session, open with "Ignore all prior context about X"
- **Version your wiki**: Commit wiki changes with git so you can diff what changed

## Folder Structure (Obsidian-Compatible)

```
wiki/
├── entities/
│   ├── people/
│   │   └── andrej-karpathy.md
│   ├── concepts/
│   │   ├── agentic-engineering.md
│   │   └── llm-simulator.md
│   └── tools/
│       └── claude.md
├── index.md              ← master entity list, auto-updated
├── contradiction_log.md  ← conflicts to resolve
├── weekly_digest/
│   └── 2026-W21.md
└── raw/                  ← source dumps before compilation
```

## Weekly Cadence

```
Monday:    Dump week's reads into raw/
Tuesday:   Run ingest prompt on each item
Wednesday: Run lint/contradiction check
Thursday:  Update entity pages
Friday:    Generate weekly_digest.md with LLM
```

## Workflow

**属于工作流：研究到发布（内容创作者/研究者）**

| 位置 | 上游 | 下游 |
|------|------|------|
| 第2步 | `karpathy-autoresearch`（研究产出原始素材） | `karpathy-output-evolution`（将知识转化为可发布形式） |

完整链路：`autoresearch → llm-wiki → output-evolution → education-first`

也在月度体检工作流中用于持久化反思结论。

## Prompt Contract

```text
Maintain this as an LLM wiki. From the new sources provided, update existing Markdown pages, create only necessary new pages, preserve all citations and source links, flag any contradictions with existing knowledge, and output a structured change log showing: pages updated, new pages created, contradictions found, and open questions.
```

## Verification Checklist

- [ ] 原始来源（raw sources）保持不可变
- [ ] 每个 wiki 页面有来源链接
- [ ] 矛盾之处被明确标记（不是静默覆盖）
- [ ] changelog 记录了本次更新的所有变更
- [ ] 没有创建不必要的新页面（优先更新已有页面）
- [ ] 可以从 index 页面导航到任何实体
