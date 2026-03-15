---
name: kairos-ai-docs
description: Find and run the zero-drift minimal template for writing AI instructions via KAIROS. Use when the user invokes /ai-docs or asks to write, generate, or update AI instructions using the zero-drift template.
compatibility: Requires KAIROS MCP server to be configured and connected.
metadata:
  version: "3.0.1"
  author: kairos-mcp
  protocol: references/KAIROS.md
  protocol_query: write AI instructions zero-drift minimal template
allowed-tools: kairos_search kairos_begin kairos_next kairos_mint kairos_attest
---

# kairos-ai-docs

Find and run the **zero-drift minimal template for AI instructions** protocol via KAIROS. The protocol is bundled in [references/KAIROS.md](references/KAIROS.md). If it is not yet installed in your KAIROS space, mint it first, then run it.

## Versioning

- **Skill version:** In frontmatter above (`metadata.version`). Bumped when the skill instructions or protocol reference change.
- **Protocol version:** In [references/KAIROS.md](references/KAIROS.md) frontmatter (`version`). Bumped when the protocol steps or challenges change.

## Workflow

1. **Search** — Call `kairos_search` with query `write AI instructions zero-drift minimal template` (or the user’s phrasing). Use the `space` parameter if the user or environment specifies one; otherwise omit (default space).
2. **If no strong match** (e.g. no choice with `score` ≥ 0.5) — Pick the **refine** choice from the response and run that protocol to improve the query, then search again.
3. **If no match** — Read [references/KAIROS.md](references/KAIROS.md). If it has YAML frontmatter (lines between `---`), pass only the markdown **after** the closing `---` to `kairos_mint` so the document starts with the H1. Use the same space as for search. Then search again.
4. **If match but stored protocol is outdated** — Read the `version` from [references/KAIROS.md](references/KAIROS.md) frontmatter. Compare with the match choice’s `protocol_version`. If the bundled version is newer (e.g. semver) or the stored protocol has no `protocol_version`, call `kairos_mint` with the full protocol document and `force_update: true` (and optional `protocol_version` from frontmatter), then search again and proceed with the chosen match.
5. **Run** — Follow the chosen match’s `next_action`: `kairos_begin` → `kairos_next` (loop) → `kairos_attest`. Echo nonces and proof hashes from the server. Do not respond to the user before `kairos_attest` when `must_obey: true`.
6. **Apply** — After attestation, use the protocol content (e.g. MISSION, STRUCTURE, CONTENT TYPES, MUST ALWAYS, MUST NEVER) and the validation checklist when generating or updating AI instructions so structure and output stay in zero-drift mapping.

## Protocol summary

The zero-drift template defines how to embed AI instructions in config files: MISSION (what to edit, 1-to-1 mapping constraint), STRUCTURE (data model), CONTENT TYPES (rendering rules), MUST ALWAYS / MUST NEVER. Use it for YAML, JSON, or other structured files that drive generated output (markdown, HTML, etc.).
