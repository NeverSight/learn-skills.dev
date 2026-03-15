---
name: kairos-create-protocol
description: Run the KAIROS "Create New KAIROS Protocol Chain" protocol. Use when the user invokes /k create new protocol, or asks to create a new protocol, mint a workflow, or build a protocol (when kairos_search found no match and user confirms).
compatibility: Requires KAIROS MCP server to be configured and connected.
metadata:
  version: "3.0.1"
  author: kairos-mcp
  protocol: references/KAIROS.md
  protocol_query: create new KAIROS protocol chain
allowed-tools: kairos_search kairos_begin kairos_next kairos_mint kairos_attest
---

# kairos-create-protocol

Run the **Create New KAIROS Protocol Chain** protocol via KAIROS. The protocol is bundled in [references/KAIROS.md](references/KAIROS.md). If it is not yet installed in your KAIROS space, mint it first, then run it.

## Versioning

- **Skill version:** In frontmatter above (`metadata.version`). Bumped when the skill instructions or protocol reference change.
- **Protocol version:** In [references/KAIROS.md](references/KAIROS.md) frontmatter (`version`). When this skill is shipped from the KAIROS MCP repo, it matches the MCP package version (e.g. same as `package.json`). So a newer bundled protocol version than the match’s `protocol_version` usually means a newer MCP server release is available — offer the user to update the MCP server.

## Workflow

1. **Search** — Call `kairos_search` with query `create new KAIROS protocol chain` (or the user’s phrasing, e.g. "create new protocol", "mint a workflow"). Use the `space` parameter if the user or environment specifies one; otherwise omit (default space).
2. **If no strong match** (e.g. no choice with `score` ≥ 0.5) — Pick the **refine** choice from the response and run that protocol to improve the query, then search again.
3. **If no match** — Read [references/KAIROS.md](references/KAIROS.md). If it has YAML frontmatter (lines between `---`), pass only the markdown **after** the closing `---` to `kairos_mint` so the document starts with the H1. Use the same space as for search. Then search again.
4. **If match but stored protocol is outdated** — Read the `version` from [references/KAIROS.md](references/KAIROS.md) frontmatter. Compare with the match choice’s `protocol_version`. If the bundled version is newer (e.g. semver) or the stored protocol has no `protocol_version`, call `kairos_mint` with the full protocol document and `force_update: true` (and optional `protocol_version` from frontmatter), then search again and proceed with the chosen match.
5. **When bundled protocol is newer than the match (skill ahead of MCP)** — If the bundled protocol version (from references/KAIROS.md frontmatter) is newer than the match choice’s `protocol_version`, after re-minting (step 4) **also offer the user to get a newer MCP server**. Do not block the run — re-mint from the skill so they can run the protocol now; the offer is informational. Phrase it depending on who controls the server: **If the user runs the MCP server themselves** (local or their deployment): suggest updating it (e.g. `npm update @debian777/kairos-mcp` or redeploy with a newer version). **If the MCP server is remote** (shared instance, another team’s deployment): do not suggest npm on the user’s machine; instead say that a newer KAIROS MCP release is available and suggest they ask the administrator or team that runs the server to upgrade when possible.
6. **Run** — Follow the chosen match’s `next_action`: `kairos_begin` → `kairos_next` (loop) → `kairos_attest`. Echo nonces and proof hashes from the server. Do not respond to the user before `kairos_attest` when `must_obey: true`.

## Protocol summary

The protocol guides creating a new executable protocol chain: confirm intent, gather requirements (title, steps, challenges), draft markdown (H1, H2, Natural Language Triggers, Completion Rule, challenge blocks), user review, then call `kairos_mint`. Every step that can be verified has a challenge (user_input, comment, or mcp).
