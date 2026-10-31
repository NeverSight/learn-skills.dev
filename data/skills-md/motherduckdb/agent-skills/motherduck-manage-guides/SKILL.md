---
name: motherduck-manage-guides
description: Read or maintain MotherDuck Guides for business definitions, join rules, and reusable warehouse conventions.
license: MIT
---

# Manage MotherDuck Guides

## Source Of Truth

- Prefer the current MotherDuck Guides documentation and MCP tool descriptions.
- When MotherDuck MCP is available and the SQL answers a business question, call `get_query_guide` first, then read only the relevant Guide topics and validate their claims against the live schema.
- `get_dive_guide` and `get_flight_guide` automatically include summaries from the reserved `dives` and `flights` topics; do not load those topics separately unless deeper context is needed.

## Default Posture

- Keep one short root orientation Guide only when its guidance applies broadly. Put domain-specific knowledge under shallow, descriptive topics.
- Default new Guides to `access = 'user'`. Organization visibility requires an explicit request and the required admin permission; change it with `set_guide_access` (MCP) or `--access` on `motherduck guide push`.
- Document tables that Flights create under the `data-sources` topic (not `flights`, which holds authoring conventions): source, purpose, grain, key columns, transformations, refresh behavior, and caveats, with references to the table, its producing Flight, and any consuming Dive. Create these with `user` access; when the table's database has an owned share, propose `organization` access and apply it only on request.
- Write one coherent subject per Guide, with a discriminating title and description. Lead with rules, tested SQL, and named pitfalls.
- Attach references to the databases, shares, schemas, tables, columns, Dives, Flights, or Guides the content governs so agents discover it at the right time.
- Validate referenced objects and executable SQL against the live workspace before presenting a Guide as trustworthy.
- Use version comments to explain why guidance changed. Read before update and avoid overwriting concurrent work.
- When a shell is available and Guides should live in Git or be reviewed like code, use `motherduck guide` (see `motherduck-cli`): edit `guide.md` locally, `push` with `--version-description`, and pass the commit SHA as `--external-id` so each version traces to a change.

## Workflow

1. Inspect `get_query_guide` or `list_guides` to understand the visible topic tree and avoid duplication.
2. Read the relevant Guide versions and referenced objects before drafting a change.
3. Choose the narrowest useful topic; leave the topic empty only for organization-wide orientation.
4. Draft concise Markdown that maps business language to exact catalog objects and validated SQL.
5. For a create or update request, apply the change through MCP or the documented SQL function and read it back.
6. Verify metadata, access, references, current version, and change comment. For query work, follow the Guide and still validate the resulting SQL against the live schema.

For answer, review, or planning requests, inspect and draft without creating or modifying Guides. For explicit create/update requests, perform the in-scope mutation and verify it; ask before deletion (`delete_guide`) or expanding visibility beyond the authorized audience. An explicit organization-publication request already authorizes that audience, subject to admin permission.

## References

Read only the reference sections needed for the current task.

- Read `references/GUIDES_PLAYBOOK.md` for topic design, access governance, references, MCP/SQL operations, versioning, and quality checks.

## Related Skills

Load related skills only for missing capabilities; reuse established context.

- `motherduck-explore` for validating referenced catalog objects
- `motherduck-query` for testing SQL and applying Guide-aware analysis
- `motherduck-create-dive` and `motherduck-create-flight` for reserved-topic conventions
- `motherduck-security-governance` for organization visibility and permission boundaries
