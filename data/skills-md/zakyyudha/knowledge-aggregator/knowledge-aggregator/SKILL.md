---
name: knowledge-aggregator
description: "Install, initialize, scan modules, retrieve knowledge, and maintain Obsidian-vault documentation for knowledge-aggregator. Trigger on /knowledge-aggregator flags (--init, --scan-module, --generate='<topic>', --rearrange-knowledge), or natural queries like 'initialize knowledge vault', 'scan modules', 'document repository', 'search knowledge vault', 'how does <feature> work', 'sync knowledge', or 'push vault'."
version: 0.1.0
---

# Knowledge Aggregator

Single portable skill and slash command for repository knowledge integration, automated module inventory, local-first retrieval, cross-repository semantic hybrid retrieval, and deeply comprehensive Markdown vault maintenance.

## Commands

```text
/knowledge-aggregator --init
/knowledge-aggregator --scan-module
/knowledge-aggregator --generate="<topic>"
/knowledge-aggregator --rearrange-knowledge
```

## Agent Routing

Read `references/shared.md` first for every invocation.

| Intent / Command | Action | Read Reference Files |
|---|---|---|
| `/knowledge-aggregator --init` | Initialize sidecar, config, vault, Index/Glossary | `references/shared.md`<br>`references/init.md` |
| `/knowledge-aggregator --scan-module` | Inventory source modules into tracker & scan report | `references/shared.md`<br>`references/scan-module.md` |
| `/knowledge-aggregator --generate="<topic>"` | Generate/update verified, deep, comprehensive documentation | `references/shared.md`<br>`references/generate.md`<br>`references/llm-wiki.md` |
| Question / Retrieval ("how does X work?", "search vault") | Local-first search, aggregator semantic hybrid MCP fallback | `references/shared.md`<br>`references/retrieve.md` |
| `/knowledge-aggregator --rearrange-knowledge` | Reorganize vault files & update bidirectional wikilinks (human-directed) | `references/shared.md`<br>`references/rearrange.md`<br>`references/llm-wiki.md` |
| Push / Delivery ("push notes", "sync to aggregator") | Run configured push command and verify | `references/shared.md`<br>`references/delivery.md` |

## Core Principles

1. **Single-Skill Rule:** This skill owns both the sidecar repository integration and the LLM Wiki procedures. Do not require or load a separate `llm-wiki` skill.
2. **Deep Documentation Standard (No Skeletal Notes):** Notes generated with `--generate` must be comprehensive, implementation-accurate, and production-grade. They must cover architectural patterns, exact interfaces/schemas, data pipelines, configuration tables, failure modes, and bidirectional `[[wikilinks]]`.
3. **Local-First, MCP-Backed:** Query local `knowledge/` first. When notes are missing or cross-repo/cross-product knowledge is needed, query the aggregator via MCP.
4. **Cross-Repo Semantic Hybrid Discovery & Dataset Routing:** `search_knowledge` leverages RAGFlow dense vector embeddings (`Qwen3-Embedding-8B`) combined with PostgreSQL full-text search. Repositories maintain `.knowledge.json` with descriptions and keywords, allowing AI agents calling `list_repos` to pinpoint the best dataset or query across federated vaults.
5. **Scan Never Overwrites Notes:** `--scan-module` strictly inventories code and tracks coverage; only `--generate` or explicit user instruction creates or edits notes.
6. **Preserve Existing State:** Never overwrite `.knowledge-aggregator/config.json`, `module-tracker.json`, or existing notes unless explicitly repairing missing fields.
