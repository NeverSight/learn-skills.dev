---
name: kairos-refine-search
description: Run the KAIROS "Get help refining your search" protocol when kairos_search has no strong match (score ≥ 0.5). Use when the response suggests refining the query or improving the search.
compatibility: Requires KAIROS MCP server to be configured and connected.
metadata:
  version: "3.0.1"
  author: kairos-mcp
  protocol: references/KAIROS.md
  protocol_query: get help refining your search
allowed-tools: kairos_search kairos_begin kairos_next kairos_attest
---

# kairos-refine-search

Run the **Get help refining your search** protocol via KAIROS. The protocol is bundled in [references/KAIROS.md](references/KAIROS.md). If it is not yet installed in your KAIROS space, mint it first, then run it.

## Versioning

- **Skill version:** In frontmatter above (`metadata.version`). Bumped when the skill instructions or protocol reference change.
- **Protocol version:** In [references/KAIROS.md](references/KAIROS.md) frontmatter (`version`). When this skill is shipped from the KAIROS MCP repo, it matches the repo's last stable version. A newer bundled protocol version than the match's `protocol_version` usually means a newer MCP server release is available — offer the user to update the MCP server when relevant.

## Workflow

1. **When to run** — After `kairos_search` returned no strong match (score ≥ 0.5) or only weak/ambiguous ones, or the response included a **refine** choice. Follow that choice's `next_action` (typically `kairos_begin` with the refine protocol URI).
2. **If protocol not installed** — Read [references/KAIROS.md](references/KAIROS.md), pass the markdown after the closing frontmatter `---` to `kairos_mint`, then run the protocol.
3. **Run** — Follow the match's `next_action`: `kairos_begin` → `kairos_next` (loop) → `kairos_attest`. Echo nonces and proof hashes. Do not respond to the user before `kairos_attest` when `must_obey: true`.

## Protocol summary

The protocol helps turn the user's vague request into a better query so the next `kairos_search` can find the right protocol. Steps may include user_input (confirm intent), comment, or other challenge types.
