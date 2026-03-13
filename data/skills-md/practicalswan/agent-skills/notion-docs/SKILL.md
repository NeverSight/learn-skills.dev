---
name: notion-docs
description: Notion workspace management via MCP - create databases, pages, comments, and knowledge bases. Use when building Notion documentation, organizing project wikis, or managing Notion content.
license: Complete terms in LICENSE.txt
---

# Notion Documentation

Use this skill when Notion is the system of record for specs, runbooks, project tracking, or knowledge management.

## Current MCP Reality

As of March 2026, Notion documents two supported ways to use its MCP server:

- Hosted remote MCP endpoint: `https://mcp.notion.com/mcp`
- Local stdio server package: `@notionhq/notion-mcp-server`

Hosted mode uses OAuth. Local mode uses an internal integration token. Official docs also list supported tools for searching content, reading pages, comments, users, and working with pages and databases.

## Activation Conditions

- Creating or updating Notion pages
- Building project trackers or engineering knowledge bases
- Organizing specs, ADRs, and onboarding docs in Notion
- Adding review comments or using database-backed workflows

## Practical Workflow

1. Confirm whether the client exposes the hosted Notion MCP server or a local stdio connection.
2. Read or search existing pages before creating duplicates.
3. Use databases for tracked work and pages for long-form documents.
4. Keep properties simple: owner, status, last reviewed, tags.
5. If MCP is unavailable in the current client, fall back to local content prep using the included script and templates.

## Operational Notes

- Official Notion guidance currently documents an average rate limit of 20 requests per second for integrations.
- Tool names can vary slightly by MCP host, but the supported capabilities are stable: search, fetch page content, create or update pages, create or update databases, manage comments, and read user context.

## References & Resources

### Documentation
- [Notion Markdown Spec](./references/notion-markdown-spec.md) - Notion-flavored Markdown constraints and conversion notes
- [Database Properties](./references/database-properties.md) - Practical property patterns for docs and project trackers
- [Notion MCP Quickstart](./references/notion-mcp-quickstart.md) - Hosted endpoint, local package, auth options, and usage notes

### Scripts
- [Notion Templates](./scripts/notion-templates.js) - Local page and database template helpers for environments without Notion MCP access

### Examples
- [Workspace Setup Example](./examples/workspace-setup-example.md) - Example team workspace structure using pages, databases, and review comments

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [notebooklm-management](../notebooklm-management/SKILL.md) | Alternative research and knowledge workflow |
| [documentation-authoring](../documentation-authoring/SKILL.md) | Create source docs before publishing them into Notion |
