---
name: claude-oracle
description: Use when user asks "what exists for X?", before implementing custom MCP servers or plugins from scratch, or when browsing available tools — searches 19 sources and 15,000+ skills, plugins, and MCP servers in one query.
---

# Claude Oracle

Search 15,000+ existing tools before building from scratch.

## When to Use

**User asks about available tools** → `search`. One command checks 19 sources simultaneously.

**Before implementing custom tooling** → An MCP server, plugin, or skill may already exist. Check before building.

**Browsing by category** → `browse` with a category. `sources` to check data source health.

## Quick Reference

| Tool | When | What it returns |
|------|------|----------------|
| `search` | Need something specific | Ranked, deduplicated results with install commands from 19 sources |
| `browse` | Exploring a category | Results filtered by type (MCP, plugin, skill) or category |
| `sources` | Checking data source health | All 19 sources with status and resource counts |

## Sources (19, zero-config)

MCP servers: Smithery, npm, Glama.ai, Official Registry, Playbooks, 3 awesome lists.
Plugins: claude-code-plugins-plus, claude-plugins-official, superpowers-marketplace.
Skills: awesome-agent-skills, 2 awesome-claude-code lists.
Dynamic: GitHub search (query-based), web search (query-based).
Optional: SkillsMP (25,000+ skills, requires API key).

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Building before searching | Always search oracle first — existing tools save hours |
| WebSearch for tools | Oracle has 19 specialized sources, more complete than web |
