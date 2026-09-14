---
name: living-artifacts
description: Apply when producing any markdown artifact for someone else (or future-you) to read — READMEs, analysis documents, Confluence pages, status reports, troubleshooting write-ups, skill content, conversation summaries, ticket descriptions, post-mortems, snapshots of system state, or any document that contains concrete current-state values. Defines the "snapshot + reproducer" rule (every static value must be paired with the command/query/script that regenerates it), the single-source-of-truth rule (reference canonical homes instead of duplicating values), and fact-vs-assumption marking. Trigger keywords include writing or producing or creating or drafting a README, analysis, Confluence page, status update, summary, snapshot, current state, documenting data, posting findings, file tree, port number, version number, table count, or any concrete value that may drift over time.
---

# Living Artifacts

When producing any markdown artifact, every static snapshot of state must be paired with the command, query, or script that regenerates it. The reader must be able to re-derive the value later without guessing where it came from.

## What Counts As A Snapshot

Anything likely to drift between writing and reading time:

- File trees, directory listings, project layouts
- Port numbers, hostnames, URLs, file paths
- Version numbers, deployed commits, image tags
- Row counts, table contents, API response bodies
- Lists of users, repos, tables, services, env vars
- "Currently failing tests" or other status snapshots
- Configuration values that have a canonical home elsewhere
- Counts and aggregates

## The Pattern

For each snapshot, include nearby:

1. The reproducer first — exact command, query, or script that produces the value.
2. The snapshot — clearly framed as a time-of-writing view, not eternal truth.
3. A drift caveat — a short note that the value may have changed and can be refreshed with the reproducer.

## Single Source Of Truth

When a value already has a canonical home, reference the source instead of duplicating the value in the artifact.

| Bad | Good |
| --- | --- |
| Hardcoded port in docs | Reference the env var or config that defines it |
| Listing names manually in a README | Point to the directory or generated listing |
| Hardcoded git SHA | Command that resolves the SHA at read time |
| API field list copied into docs | Command that introspects the live API |

## File References Must Be Clickable

Whenever a markdown artifact mentions a concrete file path, wrap it in a markdown link so readers can jump to it and broken links surface drift quickly.

Apply this to:

- Source files
- Config files
- Sibling docs
- Scripts
- Skill files
- Generated artifacts the reader should inspect

Use relative paths from the markdown file's location. Do not link placeholders, globs, or path-like CLI fragments inside code blocks.

## Facts Vs Assumptions

- Facts are verifiable now and should have a reproducer.
- Assumptions are not currently verifiable and must be marked explicitly.

Separate measured facts from interpretations so readers can tell what was observed versus inferred.

## Audience Targeting

Setup READMEs are for end users. Contributor docs and `AGENTS.md` are for maintainers. Put the right level of detail in the right home.

## Self-Check

Before publishing, scan every concrete value and ask:

1. Will this still be correct in three months?
2. If not, is the reproducer next to it?
3. If the reader runs the reproducer, will they get the same value?

If not, the artifact is incomplete.
