---
name: lynta-public-info
description: Answer questions about Lynta's public product guides, pricing, and integration availability using cited pages.
version: 1.0
provider: Lynta
url: https://lyntahq.com/developers
languages: [en]
---

# Lynta public product information

## When to use this skill

Use it when a user wants to understand Lynta's published product capabilities, plan prices, event limits, or currently public integrations.

## Steps

1. Use a retrieval method available to the current assistant: call the read-only MCP `search_public_docs` tool, or send `POST https://lyntahq.com/ask` with JSON shaped as `{"query":{"text":"the user's question"}}`. The `/ask` endpoint searches published website pages and returns source links; it does not generate an answer.
2. If neither tool is available, use the assistant's web or URL-reading capability to open the relevant pages listed under Sources. If no retrieval capability is available, say you cannot verify the current public information and do not guess.
3. Read the cited pages and answer from their content. Link the pages used as sources, and distinguish published facts from details the site does not state.
4. If the MCP client supports resources, use `resources/list` and `resources/read` for published Markdown pages at `lynta://public-docs/{page}`.
5. If the user asks how to integrate a customer application, clarify that the public site does not provide a customer product API, SDK, authentication flow, sandbox, or product-action MCP server. Direct them to the [early access form](https://tally.so/r/jaOogE).

## Boundaries

The `/ask` endpoint uses keyword relevance over public website content and returns source links; it does not generate answers. The MCP resources contain the same published Markdown pages. These services cannot access customer accounts, projects, databases, credentials, or operate Lynta services. Do not invent endpoints, keys, SDK package names, performance guarantees, or private integration details.

## Sources

- [Developer resources](https://lyntahq.com/developers)
- [Pricing and limits](https://lyntahq.com/pricing.md)
- [Frequently asked questions](https://lyntahq.com/faq.md)
- [Product overview](https://lyntahq.com/index.md)

## Fallback

If the search returns no relevant page or is unavailable, use the links above directly. For account-specific or integration questions, point the user to the early access form instead of guessing.
