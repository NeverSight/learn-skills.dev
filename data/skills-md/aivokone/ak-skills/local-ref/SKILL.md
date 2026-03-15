---
name: local-ref
description: Local docs cache for the project. Always check docs/reference/ before fetching externally. Use for init (set up cache), update (refresh docs), lookup (local-first search), and save (persist fetched docs). If external docs are fetched (Context7/web), save a tailored topic file to docs/reference/ and add a verbal pointer in AGENTS.md.
---

# Local Reference

Cache library documentation locally so every session reads from disk instead of re-fetching from external sources. Local docs load via `Read` tool (free, instant) instead of API calls (tokens + latency).

## Sources

Fetch documentation from any of these, in order of preference:

1. **Context7 API** — curated library docs with code examples. See `references/context7-api.md`.
2. **WebFetch** — official documentation sites (e.g., developer.wordpress.org, getbootstrap.com)
3. **Manual** — user-provided docs, internal wikis, or CLI `--help` output

## Commands

### Init — `local-ref init`

Set up local documentation cache for a project.

1. **Detect project technologies** from these sources:
   - `package.json` (JS/Node dependencies)
   - `composer.json` (PHP dependencies)
   - `AGENTS.md` / `CLAUDE.md` (mentioned frameworks)
   - `requirements.txt` / `pyproject.toml` (Python)
   - `Gemfile` (Ruby)
   - `go.mod` (Go)

2. **Confirm with user** which technologies to cache. Suggest the top 3-5 most relevant. Skip generic/obvious ones (e.g., don't cache "JavaScript" docs for a JS project).

3. **For each technology:**
   a. Scan project code to identify which APIs/patterns are actually used
   b. Fetch documentation from best available source (see Sources above)
   c. Filter fetched content to patterns relevant to this project

4. **Write project-specific docs** to `docs/reference/<topic>.md`:
   - Start each file with the standard header (see File Header Format below)
   - Include only patterns relevant to this project's actual code
   - Cross-reference actual project files when possible (e.g., "Used in `lib/acf.php`")
   - Target 100-200 lines per file — enough to be useful, small enough to read quickly

5. **Update AGENTS.md** — add a `## Local Reference Documentation` section with verbal references (NOT `@`-references) to the docs:
   ```markdown
   ## Local Reference Documentation

   The `docs/reference/` directory contains project-specific API references.
   Check these files before using external documentation tools:

   - `docs/reference/<file>.md` — <brief description>
   ```

### Update — `local-ref update`

Refresh existing local docs.

1. Read `docs/reference/` to find existing doc files
2. For each file, parse the `<!-- source="..." -->` header to determine source type and parameters (`libraryId`/`query` for context7, `url` for webfetch)
3. Re-fetch based on source type:
   - `context7` — re-fetch using `libraryId` and `query`
   - `webfetch` — re-fetch from `url`
   - `manual` — skip (flag for user review if stale)
4. Merge new content while preserving project-specific annotations and cross-references
5. Update the `<!-- cached="..." -->` date
6. Report what changed (updated, skipped manual, failed)

### Lookup — `local-ref lookup <topic>`

Find documentation, local-first.

1. Check `docs/reference/` for a matching file (grep for topic keywords)
2. If found, read the local file and quote/apply the relevant sections to the current task
3. If not found, fetch from external source, then ask user if the result should be saved locally

### Save — `local-ref save` (opportunistic, mid-project)

When working on a project and you fetch documentation from an external source (Context7, WebFetch, etc.) that would be useful across sessions:

1. After using the fetched docs to complete the current task, offer: "This documentation could be useful in future sessions. Save to `docs/reference/`?"
2. If user agrees, write a project-specific version (not raw dump) to `docs/reference/<topic>.md` with the standard header (see File Header Format)
3. Add the new file to the AGENTS.md `## Local Reference Documentation` bullet list so future sessions discover it
4. Continue with the original task

This keeps docs growing organically as the project evolves, without requiring explicit `init` or `update` runs.

## Passive Behavior (via AGENTS.md)

The `init` command adds a `## Local Reference Documentation` section to AGENTS.md. This section loads every session (~80 tokens) and tells Claude to check `docs/reference/` before external lookups. This passive guidance works without loading the skill itself.

## File Header Format

Every cached doc file MUST start with this machine-readable header. The `update` command depends on it.

```markdown
# Vite Asset Pipeline — Project Reference
<!-- source="context7" libraryId="/vitejs/vite" query="build manifest plugin configuration" -->
<!-- cached="2026-02-16" -->

Content here...
```

Header fields:

| Field | Required | Values |
|-------|----------|--------|
| `source` | yes | `context7`, `webfetch`, `manual` |
| `libraryId` | if context7 | Context7 library ID |
| `url` | if webfetch | Source URL |
| `query` | if applicable | Query used to fetch content |
| `cached` | yes | ISO date (`YYYY-MM-DD`) of last fetch |

For manually created docs, use `source="manual"`:

```markdown
# Internal Auth API — Project Reference
<!-- source="manual" cached="2026-02-16" -->
```

## When NOT to Cache

Skip local caching when:

- **Rapidly evolving APIs** — bleeding-edge or pre-1.0 libraries where docs change weekly
- **One-off lookups** — if you only need one fact, fetching is cheaper than maintaining a file
- **Already in AGENTS.md** — if the project's agent instructions already cover the topic

When in doubt, cache. Stale docs are better than no docs — `update` can refresh context7 and webfetch sources automatically (manual sources are flagged for review).

## Key Design Rules

- **Verbal references only** — never add `@docs/reference/...` to AGENTS.md (would bloat system prompt). Use plain text descriptions so Claude reads files on-demand.
- **Project-specific over generic** — don't dump raw API output. Tailor examples to the project's actual code, file structure, and patterns.
- **Cross-reference project files** — mention where patterns are used (e.g., "see `lib/assets.php` for implementation").
- **One file per topic** — keep docs modular. Don't create one giant reference file.
- **100-200 lines per file** — see target in `init` command above.

## File Naming Convention

Use descriptive kebab-case names:
```
docs/reference/
├── acf-patterns.md
├── vite-asset-pipeline.md
├── wordpress-cpt-taxonomy.md
├── bootstrap-grid-components.md
└── react-hooks-patterns.md
```

## External Source References

See `references/context7-api.md` for Context7 API endpoints and common library IDs.
