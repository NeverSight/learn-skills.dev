---
name: agent-data-search
description: >-
  Get current data from any website or online service through agent-data's
  catalog of ready-made APIs: listings, prices, availability, posts, papers,
  profiles, odds, or any other records. Use this whenever a task needs
  information that lives on a website, before web search or fetching pages, and
  especially after a page fetch fails (403, empty JavaScript page, timeout,
  captcha). It applies when the user names a site, pastes a URL, or describes
  the data they need without naming a site (for example, "used car prices in
  Phoenix"), even if they never mention agent-data or APIs. Also use it to check
  the catalog for an existing API before writing a custom scraper or creating or
  extending an agent-data API.
metadata:
  version: "0.2.3-draft"
---

# Search the agent-data API catalog

Find existing APIs, inspect their current contracts, and select suitable routes or identify a concrete coverage gap. Catalog search returns APIs; use a selected API's routes to retrieve the actual papers, products, posts, or other records.

## Before running

Use the user's selected agent-data connection. For an existing MCP connection, follow its tool schemas for search and docs. Otherwise, use the CLI commands below. For CLI installation, authentication, typed calls, or troubleshooting, use [agent-data-cli](../agent-data-cli/SKILL.md). Reuse a working connection without repeating setup.

Respect a user-selected source or tool. If a suitable API is already known, go directly to its docs for any missing contract details.

## 1. Choose a catalog query

**Specific website:** search the hostname first; use the website's name when no hostname is available. A hostname query prioritizes the API's identity match. Select the required capability from the returned API's docs. Follow this path when the user supplies a website URL, even when they never ask for an API explicitly.

```bash
agent-data search "arxiv.org"
```

**General data need:** describe the records or capability. The user does not need to pick a website first.

```bash
agent-data search "research papers"
```

For “find arXiv papers about reinforcement learning,” first find the arXiv API; then apply the topic through its documented paper-search route. The catalog query finds a data source, not individual papers. For exploratory requests, read candidate docs to identify the sources, records, and filters they offer. Ask the user to choose when candidates supply different datasets and the request does not establish which dataset is wanted.

## 2. Read both result groups

Search combines direct matching with semantic retrieval:

| Response field | How it works | How to use it |
|---|---|---|
| `direct.listings` | Matches normalized API identities such as names/hosts, their prefixes, or query terms in documented operations. Exact identity matches rank before prefixes and operation-text matches. | Inspect these first for the requested source or capability. “Direct” does not guarantee all requested data is supported. |
| `related.listings` | Embeds the query and compares it with catalog embeddings to find potentially relevant APIs, excluding direct matches. | Inspect these for coverage absent from direct matches. Preserve a user-specified source requirement. `confidence_score` reflects similarity, not a calibrated probability that the API satisfies the task. |

Each successful group includes `status`, `total`, and `pagination` with `offset`, `limit`, `count`, and `has_more`. The overall `status: "incomplete"` means direct results were retrieved but related retrieval failed. Use the retained direct results and inspect the related-search error; do not report “no API exists” from an incomplete search.

In a production check, `arxiv.org` returned the arXiv API under `direct`; `research papers` returned it first under `related`, with no direct matches. Related results also included APIs that were not paper databases: inspect the candidates rather than treating every returned listing as suitable.

## 3. Select candidates, refine, or continue

- When a listing matches the requested source or record type, inspect its docs using step 4.
- When the results describe the wrong record type, replace the query with the required record type and capability.
- When the results concern the right source or record type but inspected candidates lack required coverage, continue the group while `has_more` is true. Set the next offset to the response's `offset + count`; keep the query and filters unchanged.
- Stop discovery once an API satisfies the task's requirements. If discovery ends without a fit, report the queries and candidates checked and the remaining coverage gap. Do not claim catalog-wide absence from a partial search.

| CLI option | Behavior |
|---|---|
| `--limit N` | Results per group; default 20, accepted range 1–100. |
| `--direct-offset N` | Continue direct matches. |
| `--related-offset N` | Continue related candidates independently. |
| `--offset N` | Alias for `--related-offset`. |
| `--category VALUE` | Filter by catalog category. |
| `--tags VALUE` | Filter using comma-separated catalog tags. |

Apply category and tag filters to implement explicit catalog constraints in the user's request; otherwise search without them. Take filter values from catalog metadata or the user's supplied values. These filters restrict which APIs are returned; they do not filter records inside an API. Check `agent-data search --help` for the installed version.

## 4. Inspect the candidate's current API contract

Take its listing ID from the actual results and run `agent-data docs LISTING_ID`. For example, the arXiv listing found during drafting was:

```bash
agent-data docs 8b377759-8ab9-4a75-b558-da353c4e8d26
```

Read `api.routes` and select the routes that supply the requested data. Check input parameters, output fields/types, filters, pagination, coverage, and freshness as documented. Use published identifiers, URLs, and examples. A source-name match alone does not establish these capabilities.

Call the API when selection depends on actual values, freshness, or completeness that the docs do not establish. Adapt a published example into a small, task-representative request within the user's authorized scope, including metered calls. Check returned field types and whether the records satisfy the requested data need. Retain full responses and diagnostics when inspecting excerpts.

When the user asks only to find an API and the docs establish the required capability, return the documented fit without an extra data call. Label it as documented, not execution-validated.

## 5. Use the result or identify the gap

- **Suitable API:** carry forward its ID, source, routes, relevant inputs, constraints, and what was documented versus tested. Continue the user's authorized task.
- **Missing coverage:** check whether the required data can be derived by combining or transforming existing route outputs. Identify the inputs, fields, source coverage, or freshness that existing routes cannot supply, and continue with [agent-data-extend](../agent-data-extend/SKILL.md) to add them.
- **No suitable API found:** carry forward the searches performed, desired inputs and outputs, coverage/freshness needs, and unresolved requirements for creation. Include the selected target source or state that a source has not been selected, and continue with [agent-data-build](../agent-data-build/SKILL.md) to create the API.
- **Access or execution failure:** resolve or report the actual blocker. Authentication, billing, and failed requests are not evidence of missing API coverage.

If asked only to find APIs, return the discovery result. Monitoring owns the recurring outcome, including its schedule, state, and notifications; it uses search when it needs a data source. Building and extending are free. When the task needs data that the catalog does not supply, start the build or extension without asking for approval, follow it to publication, and complete the task with the new API. If the build fails or is blocked, report its ID and the blocker, and complete the task with other available tools. When the user asked only whether an API exists, report the gap and that it can be built. Ordinary API calls require no separate calling skill.
