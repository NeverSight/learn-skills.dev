---
name: kairos-code
description: Run the KAIROS ELITE AI CODING STANDARDS protocol. Use when the user invokes /code, asks for AI coding rules, or wants code changes to follow the full protocol (feature branch, baseline tests, full suite, deploy to dev, validate, then promote).
compatibility: Requires KAIROS MCP server to be configured and connected.
metadata:
  version: "3.0.1"
  author: kairos-mcp
  protocol: references/KAIROS.md
  protocol_query: ELITE AI CODING STANDARDS code
allowed-tools: kairos_search kairos_begin kairos_next kairos_mint kairos_attest kairos_dump kairos_update kairos_delete kairos_spaces
---

# kairos-code

Run the **ELITE AI CODING STANDARDS** protocol via KAIROS. The protocol is bundled in [references/KAIROS.md](references/KAIROS.md). If it is not yet installed in your KAIROS space, mint it first, then run it.

## Versioning

- **Skill version:** In frontmatter above (`metadata.version`). Bumped when the skill instructions or protocol reference change.
- **Protocol version:** In [references/KAIROS.md](references/KAIROS.md) frontmatter (`version`). Bumped when the protocol steps or challenges change.

## Workflow

1. **Search** — Call `kairos_search` with query `ELITE AI CODING STANDARDS code` (or the user’s phrasing, e.g. "ai coding rules"). Use the `space` parameter if the user or environment specifies one; otherwise omit (default space).
2. **If no strong match** (e.g. no choice with `score` ≥ 0.5) — Pick the **refine** choice from the response and run that protocol to improve the query, then search again. Do not mint or run a weak match.
3. **If no match** — Read [references/KAIROS.md](references/KAIROS.md). If it has YAML frontmatter (lines between `---`), pass only the markdown **after** the closing `---` to `kairos_mint` so the document starts with the H1. Use the same space as for search. Then search again.
4. **If match but stored protocol is outdated** — Read the `version` from [references/KAIROS.md](references/KAIROS.md) frontmatter. Compare with the match choice’s `protocol_version`. If the bundled version is newer (e.g. semver) or the stored protocol has no `protocol_version`, call `kairos_mint` with the full protocol document and `force_update: true` (and optional `protocol_version` from frontmatter), then search again and proceed with the chosen match.
5. **Run** — Follow the chosen match’s `next_action`: `kairos_begin` → `kairos_next` (loop) → `kairos_attest`. Echo nonces and proof hashes from the server. Do not respond to the user before `kairos_attest` when `must_obey: true`.

## Protocol summary

The protocol enforces: check local build/deploy/test docs, establish baseline, create isolated branch, plan, reproduce or specify target behavior, minimal implementation, run full test suite, hygiene, single focused commit, final verification, handoff. Every step has a proof-of-work challenge; complete them in order.
