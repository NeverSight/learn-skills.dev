---
name: searching-packages
description: Finds Robomotion packages, nodes, and templates via the `robomotion` CLI, which is backed by Bleve full-text search with fuzzy matching and semantic expansion. Use when the user asks to find a package, explore templates, discover what nodes exist for a task, or check exact property names before writing a flow.
---

# Searching Robomotion Packages

Discover Robomotion packages, nodes, and templates. All lookups go through the `robomotion` CLI — no separate MCP client required.

## Four verbs cover every lookup

```bash
robomotion search <query>                        # cross-source fuzzy+semantic search
robomotion get <resource> [query] [flags]        # list or filter a resource
robomotion describe <resource> <name>            # full detail of one thing
robomotion docs <namespace>                      # read a package's llms.txt
```

Resources for `get`: `packages | nodes | templates | categories | tags` (plus `vaults | vault-items | robots` for runtime data).
Resources for `describe`: `node | package | template`.

## Typical workflow when authoring a flow

1. **Find what's available** — if you don't know the package/node yet:
   ```bash
   robomotion search "http request"              # mixed results across sources
   robomotion get nodes click                    # nodes with "click" in the name
   robomotion get nodes --in Core.Browser        # every node in one package
   robomotion get templates bmi                  # match by slug/name/summary
   robomotion get templates --category "Web Scraping"
   robomotion get templates --tag api
   robomotion get categories                     # vocabulary
   robomotion get tags                           # vocabulary
   ```

2. **Verify properties** before writing:
   ```bash
   robomotion describe node Core.Net.HttpRequest
   robomotion describe node Core.Net.HttpRequest,Core.Flow.GoTo   # batch
   ```
   Returns the full card: property names, types, descriptions, enums, defaults, and common properties (`delayBefore`, `continueOnError`, …).

3. **Read package docs** when wiring a non-`Core.*` package:
   ```bash
   robomotion docs Robomotion.WordPress                   # compact (first 100 lines)
   robomotion docs Robomotion.WordPress --full            # whole llms.txt
   robomotion docs Robomotion.WordPress --grep auth       # line-filtered
   robomotion docs Robomotion.WordPress --section CreatePost
   ```
   `docs` carries auth patterns and package-level gotchas that aren't in node schemas. MANDATORY for every non-`Core.*` package you use.

## Search engine capabilities

Under the hood `robomotion search` uses **Bleve** full-text search with:

| Feature | Behavior |
|---------|----------|
| Full-text | BM25 ranking across title, name, description, content, keywords |
| Fuzzy | Levenshtein ≤ 2 — tolerates typos (`browsr` → `browser`, `wordpres` → `wordpress`) |
| Semantic | Synonym expansion — `browser` also matches `chrome`, `firefox`, `web`, `scraping` |
| Multi-source | Package docs (llms.txt) and templates in one call |

Built-in synonym families:
- `browser ↔ chrome · firefox · web · scraping`
- `automation ↔ robot · flow · workflow · process`
- `wordpress ↔ blog · cms · post · article`
- `database ↔ sql · sqlite · query · table`
- `email ↔ mail · smtp · send · message`
- `file ↔ filesystem · directory · folder · path`

## Filter flags

```bash
robomotion search "automation" --limit 5
robomotion get nodes "click" --package Core.Browser
robomotion get templates --tag api --limit 10
robomotion describe node Core.Browser.ClickElement --json     # raw MCP response
```

## First-call warm-up

`robomotion search` spawns `robomotion-sdk-mcp` under the hood; its Bleve index takes ~3–6 s to build on cold start. The CLI retries automatically on `"Search index not ready"`, so you'll see one slow search per session, then near-instant afterward.

## Quick reference

| I want to… | Command |
|------------|---------|
| Find anything by keyword | `robomotion search <query>` |
| List all packages | `robomotion get packages` |
| Find a package | `robomotion get packages <keyword>` |
| List nodes in a package | `robomotion get nodes --in <namespace>` |
| Find nodes by keyword | `robomotion get nodes <keyword>` |
| Get full node schema | `robomotion describe node <type>` |
| Read package docs | `robomotion docs <namespace>` |
| Grep package docs | `robomotion docs <namespace> --grep <pattern>` |
| List available vaults | `robomotion get vaults` |
| List robots | `robomotion get robots` |

## Related Skills

- `creating-flow` — generate a flow from the nodes you found
- `validating-flow` — pspec-check the result
- `running-flow` — submit + stream agent events
