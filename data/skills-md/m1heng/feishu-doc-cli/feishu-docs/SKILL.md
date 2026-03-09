---
name: feishu-docs
description: Look up Feishu (Lark) Open Platform developer documentation. Use when the user asks about Feishu/Lark APIs, bot development, web apps, docs add-ons, base extensions, cards, authentication, or any Feishu integration topic.
allowed-tools: Bash(feishu-doc *)
---

# Feishu Open Platform Docs

Read Feishu developer documentation directly from the terminal via `feishu-doc` CLI.

## Prerequisites

Install once (requires Node.js >= 18):

```bash
npm install -g feishu-doc-cli
```

## Commands

```bash
feishu-doc search "<keyword>"     # Search docs by title
feishu-doc read "<path>"          # Read a document (outputs Markdown)
feishu-doc tree --depth 2         # Browse the doc tree
feishu-doc tree "<path>"          # Browse a subtree
```

Add `--lang en` for English.

## Workflow

1. **Start with `search`** to find relevant documents:
   ```bash
   feishu-doc search "知识库"
   ```

2. **Read a document** using the path from search results:
   ```bash
   feishu-doc read "/ukTMukTMukTM/uUDN04SN0QjL1QDN/wiki-overview"
   ```

3. **Follow links** — document content contains links in various formats. Copy any link href and pass it directly to `read`:
   ```bash
   # All these formats work — just copy the href as-is:
   feishu-doc read "/ssl:ttdoc/ukTMukTMukTM/uUDN04SN0QjL1QDN/wiki-v2/space/list"
   feishu-doc read "https://open.feishu.cn/document/client-docs/intro"
   feishu-doc read "https://open.larkoffice.com/document/client-docs/bot-v3/bot-overview"
   ```

4. **Browse by category** if you need to explore an area:
   ```bash
   feishu-doc tree "/uAjLw4CM/ukTMukTMukTM" --depth 2   # Server APIs
   ```

## Top-level doc categories

| Category | Tree path |
|----------|-----------|
| Developer Guides | `/uAjLw4CM/ukzMukzMukzM` |
| Developer Tutorials | `/uAjLw4CM/uMzNwEjLzcDMx4yM3ATM` |
| Server API | `/uAjLw4CM/ukTMukTMukTM` |
| Client API | `/uAjLw4CM/uYjL24iN` |
| MCP | `/mcp_open_tools` |
