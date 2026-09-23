---
name: confluence-cli
description: >-
  Interact with Atlassian Confluence from the terminal: list spaces, browse pages, view
  page content, search with CQL, and create pages. Use when the user mentions Confluence,
  a space key (e.g. DEV), or asks about documentation, wiki pages, space content, or
  knowledge base articles. Do not use this skill for unrelated requests; route to the
  nearest named specialist.
license: MIT
compatibility: Requires CONFLUENCE_EMAIL and CONFLUENCE_API_TOKEN env vars (free from
  id.atlassian.com/manage/api-tokens), Python 3.8+, and the `requests` library. Also
  requires CONFLUENCE_SERVER (defaults to your-domain.atlassian.net).
metadata:
  tags: confluence, atlassian, wiki, documentation, knowledge-base, api-client
  sources: https://developer.atlassian.com/cloud/confluence/rest/v2/, https://id.atlassian.com/manage/api-tokens
---

# confluence-cli — Confluence Wiki from the Terminal

Interact with Atlassian Confluence Cloud via the REST API. List spaces, browse pages, view page content with body, search with CQL, and create pages.

## Setup

1. Generate an API token at [id.atlassian.com/manage/api-tokens](https://id.atlassian.com/manage/api-tokens)
2. Set environment variables:

```bash
export CONFLUENCE_EMAIL="your-email@example.com"
export CONFLUENCE_API_TOKEN="your-api-token"
export CONFLUENCE_SERVER="https://your-domain.atlassian.net"
```

`--help` and `--dry-run` work without credentials.

## Essential Commands

### me — Current user profile

```bash
confluence-cli me                       # your account info
confluence-cli me --json                # machine-readable
```

### spaces — List spaces

```bash
confluence-cli spaces                   # all accessible spaces
confluence-cli spaces --limit 50        # more results
confluence-cli spaces --json            # machine-readable
```

### pages — List pages

```bash
confluence-cli pages                                # recent pages across all spaces
confluence-cli pages --space DEV                    # pages in a specific space
confluence-cli pages --space DEV --limit 10          # top 10
confluence-cli pages --space DEV --json             # machine-readable
```

Filters by space key. Resolves the key to an internal ID automatically.

### view — View a page by ID

```bash
confluence-cli view 123456                   # full page with body
confluence-cli view 123456 --json            # machine-readable
```

Shows title, status, version, author, timestamps, and HTML body (stripped to plain text for display). The full HTML body is available in `--json` output up to 5000 chars.

### search — Search with CQL

```bash
confluence-cli search --cql 'text~"deploy"'              # full-text search
confluence-cli search --cql 'space=DEV AND type=page'    # by space and type
confluence-cli search --cql 'creator=currentuser()'      # my content
confluence-cli search --cql 'text~"api"' --limit 5       # top 5 results
```

CQL (Confluence Query Language) is Confluence's search syntax. Common patterns:
- `text~"keyword"` — full-text search
- `space=KEY` — filter by space
- `type=page` — filter by content type
- `creator=currentuser()` — your content
- `label="name"` — by label
- Combine with `AND`: `space=DEV AND text~"deploy"`

### create — Create a page

```bash
confluence-cli create --space DEV --title "My Page"                             # basic
confluence-cli create --space DEV --title "API Docs" --body "<p>Content</p>"    # with HTML body
confluence-cli create --space DEV --title "Test" --parent 123456                # as child page
confluence-cli create --space DEV --title "Test" --dry-run                      # preview
```

Creates pages in Confluence Cloud (v2 API). The body is HTML using Confluence's storage format. For simple pages, basic HTML tags work (`<p>`, `<ul>`, `<h2>`, etc.).

## Global Flags

All flags work in any position:

```bash
confluence-cli --json pages --space DEV              # flag before subcommand
confluence-cli pages --space DEV --json              # flag after subcommand
confluence-cli --dry-run create --space DEV --title "Test"
confluence-cli --quiet pages                         # suppress non-essential output
```

## Known Gotchas

- **Authentication** uses HTTP Basic Auth with email + API token. Same credentials as Jira, but stored under different env var names.
- **Two API versions** — The CLI uses v2 API for most operations (spaces, pages, create) and the legacy rest API for `me` and `search` (CQL). This is transparent to the user.
- **Space keys must be resolved to IDs** — The v2 API requires numeric space IDs for filtering. The CLI resolves keys automatically, which costs one extra API call on `pages --space` and `create --space`.
- **Page body is HTML** — The Confluence storage format uses HTML. The CLI strips HTML tags for display and returns raw HTML in `--json` output (up to 5000 chars). Creating pages with rich formatting requires valid HTML.
- **CQL search quirks** — CQL is case-insensitive for most operators. The `text~` operator searches the full text body. Enclose multi-word phrases in escaped quotes.
- **Rate limits** — Confluence Cloud has rate limits. The CLI does not auto-retry.

## References

- [scripts/confluence-cli](scripts/confluence-cli) — The CLI binary. Built following the cli-builder patterns: non-interactive, `--json`, `--dry-run`, `--quiet`, `--verbose`, dual-output via `emit()`, lazy auth, structured logging.
- [Confluence REST API v2 docs](https://developer.atlassian.com/cloud/confluence/rest/v2/) — Official API reference.
- [CQL (Confluence Query Language)](https://developer.atlassian.com/cloud/confluence/advanced-searching/) — Search syntax reference.
- [API Token Management](https://id.atlassian.com/manage/api-tokens) — Generate and revoke tokens.
