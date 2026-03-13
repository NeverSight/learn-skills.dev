---
name: external-sync
model-invocable: true
description: Search an external knowledge source and sync relevant content as notes into the Obsidian vault
allowed-tools: Read, Write, Glob, Grep, Edit, Task
---

# External Source → Obsidian Sync

Search an external knowledge source for articles relevant to current areas of focus and create corresponding notes in the Obsidian vault at `~/Documents/obsidian-vault/`.

The Obsidian vault is the preferred workspace for user/model collaboration. The external source (e.g. Notion, Confluence, Google Docs) is upstream. This skill bridges the two — pulling relevant content into the vault where it becomes part of the interlinked knowledge graph.

**Note:** This skill template uses Notion as the example external source. Replace the MCP tool calls (`mcp__notion__notion-search`, `mcp__notion__notion-fetch`) with whatever API your external source exposes.

## Procedure

### 1. Determine Areas of Focus

Identify what to search for by reading the vault:

- Read the most recent daily note(s) to find active work, backlog items, and session topics.
- Run a tag-line grep (`^#` across the vault) to get the current topic landscape.
- Derive 3–8 search queries from: active projects, services under development, open decisions, backlog items, and architectural themes.

If invoked with an explicit topic (e.g. `/external-sync auth service`), use that as the primary focus and derive 1–2 additional related queries from vault context.

### 2. Search the External Source

For each area of focus, search the external source with a focused semantic query.

Collect candidate pages — titles, IDs, and snippet context. Discard results that are clearly irrelevant.

### 3. Deduplicate Against the Vault

Before fetching any page, check whether a corresponding note already exists in the vault:

- Grep for the page URL or title in existing vault notes.
- If a vault note already links to the same page (via its `**Source**:` line), skip it unless the user explicitly asked for a refresh.

### 4. Preview and Confirm

**Do not write any vault notes yet.** Present the user with:

1. **A TLDR for each high-value page** — 2–3 sentences summarising what the page contains and why it's relevant to current work.
2. **A proposed sync plan** — table of pages to sync vs skip, with reasoning:

```
| Page | Action | Proposed vault name | Tags | Reason |
|------|--------|---------------------|------|--------|
| Auth Architecture | Sync | auth-architecture.md | #architecture #service/auth #external | Design doc for auth service |
| Sprint Retro Notes | Skip | — | — | Not relevant to current work |
```

3. **Ask for confirmation** — wait for the user to approve, request changes, or ask questions before proceeding.

Only proceed to step 5 after the user confirms.

### 5. Fetch and Transform

For each approved page, fetch its full content.

Transform into a vault note following all PKM conventions:

1. **H1 title** — use a clear, descriptive title.
2. **Tags on line 2** — apply the vault's tag taxonomy. Always include a source tag (e.g. `#external` or `#notion`) to mark the note's origin.
3. **Source line** — immediately after tags, add:
   ```
   **Source**: [<page title>](<URL>)
   ```
4. **Overview paragraph** — a concise summary of the page's content and why it's relevant.
5. **Structured content** — distill the page into well-structured markdown. Do not blindly copy — reorganise and condense for the vault's conventions.
6. **Wiki-links** — link to existing vault notes wherever concepts overlap. This is critical for integrating synced content into the knowledge graph.

### 6. Report

After syncing, output a summary:

```
## Sync Summary

**Queries searched**: <list>
**Pages found**: <N>
**Notes created**: <N>
**Skipped (already in vault)**: <N>

### New notes
- [[note-name]] — one-line description (from: <page title>)
```

## Constraints

- **External source is read-only** — never create or modify pages in the external source.
- **Vault conventions are mandatory** — every note created must follow the PKM skill's conventions (flat structure, tags, wiki-links, naming).
- **Don't duplicate** — if the vault already has a note covering the same content, prefer adding a `**Source**:` link to the existing note rather than creating a duplicate.
- **Condense, don't dump** — external pages can be verbose. Distill to what's useful.
- **Prefer quality over quantity** — it's better to sync 3 high-value notes than 15 shallow ones.
- **Source of truth chain** — codebase > external page > vault note. If a vault note from the external source conflicts with the codebase, the codebase wins. The vault note should flag the discrepancy.
- **Always preview first** — never write vault notes without showing the user what will be synced and getting confirmation.

## Usage

```
/external-sync                    # Auto-detect areas of focus from vault, search and sync
/external-sync <topic>            # Search for a specific topic and sync relevant pages
/external-sync refresh <topic>    # Re-sync even if notes already exist (updates existing notes)
```
