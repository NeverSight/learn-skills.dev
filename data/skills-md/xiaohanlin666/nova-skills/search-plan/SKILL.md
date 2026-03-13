---
name: search-plan
description: Search for Test Plans in HP Nova by various conditions such as title, plan code, status, owner, category, and keyword. Supports pagination and sorting. Use this skill whenever the user wants to find, search, or list Test Plans in Nova.
version: 0.0.1
author: Matt Xiao
---

# Search Plan Skill

Search for Test Plans in the HP Nova test management platform using the `nova_search_plan` MCP tool.

## When to Use

Invoke this skill when the user says something like:

- "Search for plans with title containing xxx"
- "Find all Published plans in Nova"
- "List plans owned by xxx"
- "Show me all Draft test plans"
- "Look up plan code PLNxxxxxx"
- "Search plans by keyword"

## Supported Query Parameters

| Parameter | Description | Example Values |
|-----------|-------------|----------------|
| `title` | Fuzzy match on plan title | `nova`, `regression` |
| `code` | Exact match on plan code | `PLN300000009` |
| `keyword` | Full-text keyword search | `smoke test` |
| `status` | Filter by status | `All` (default), `Draft`, `Published`, `Revoked` |
| `ownerId` | Filter by owner ID | `Bjorn_Deng` |
| `ownerSite` | Filter by owner's site | `BJS`, `SHH` |
| `siteCode` | Filter by site code | `BJS` |
| `category1Id` | Level-1 category ID | |
| `category2Id` | Level-2 category ID | |
| `category3Id` | Level-3 category ID | |
| `odmId` | ODM ID | |
| `isHpSite` | HP site flag (boolean) | `true` / `false` |
| `pageNum` | Page number (default: 1) | `1`, `2`, `3` |
| `pageSize` | Results per page (default: 10) | `10`, `20`, `50` |
| `titleSort` | Sort by title | `asc`, `desc` |
| `updateDateSort` | Sort by last updated time | `asc`, `desc` |

## Behavior

1. Extract query conditions from the user's natural language input and map them to the corresponding parameters.
2. Call the `nova_search_plan` tool with the extracted parameters.
3. Present the results in a clear Markdown table with columns: Plan Code, Title, Status, Owner, Category, Cases, and Last Updated.
4. Show total count and current pagination info below the table.
5. If there are more pages, ask the user whether they want to see the next page.
6. If no results are found, inform the user politely and suggest relaxing the search criteria.

## Output Format Example

Found **N** plan(s) (page X, page size 10):

| # | Plan Code | Title | Status | Owner | Category | Cases | Last Updated |
|---|-----------|-------|--------|-------|----------|-------|--------------|
| 1 | PLN300000009 | Nova Test | Published | Bjorn_Deng | Function Test | 23 | 2026-01-27 |

> Total N result(s), page X of Y. Would you like to see the next page?

## Notes

- `status` defaults to `All`; omit it if the user does not specify a status filter.
- Only pass parameters explicitly provided or clearly implied by the user; leave all others at their defaults.
- The same plan code may appear multiple times due to different versions — this is expected behavior.

