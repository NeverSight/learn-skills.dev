---
name: kairos-create-skill
description: Run the KAIROS protocol for creating a KAIROS skill (Agent Skill with optional references/KAIROS.md or multiple references/KAIROS-{alias}.md protocols). Use when the user wants to create a KAIROS skill, create a skill with a KAIROS protocol, write SKILL.md, or asks about skill structure and Agent Skills format (agentskills.io).
compatibility: Requires KAIROS MCP server to be configured and connected.
metadata:
  version: "3.0.1"
  author: kairos-mcp
  protocol: references/KAIROS.md
  protocol_query: create KAIROS skill with KAIROS.md protocol
allowed-tools: kairos_search kairos_begin kairos_next kairos_mint kairos_attest
---

# kairos-create-skill

Run the **Create KAIROS skill (with KAIROS.md protocol)** protocol via KAIROS. The protocol is bundled in [references/KAIROS.md](references/KAIROS.md). If it is not yet installed in your KAIROS space, mint it first, then run it.

## Single vs multiple protocols (aliases)

- **Single protocol:** One protocol in `references/KAIROS.md`. Set `metadata.protocol` and `metadata.protocol_query` in SKILL.md.
- **Multiple protocols (aliases):** One protocol per alias in `references/KAIROS-{alias}.md` (e.g. `references/KAIROS-workflow-test.md`, `references/KAIROS-ai-mcp-integration.md`). Set `metadata.protocols` in SKILL.md to map alias → file path; optionally `metadata.protocol_queries` to map alias → search query. The agent picks the protocol from the user’s alias/trigger (e.g. `/workflow-test` → `references/KAIROS-workflow-test.md`).

## Versioning

- **Skill version:** In frontmatter above (`metadata.version`). Bumped when the skill instructions or protocol reference change.
- **Protocol version:** In each protocol file frontmatter (`version`). Bumped when that protocol’s steps or challenges change.

## Workflow

1. **Search** — Call `kairos_search` with query `create KAIROS skill with KAIROS.md protocol` (or the user’s phrasing, e.g. "create KAIROS skill", "create skill with protocol"). Use the `space` parameter if the user or environment specifies one; otherwise omit (default space).
2. **If no strong match** (e.g. no choice with `score` ≥ 0.5) — Pick the **refine** choice from the response and run that protocol to improve the query, then search again.
3. **If no match** — Read [references/KAIROS.md](references/KAIROS.md). If it has YAML frontmatter (lines between `---`), pass only the markdown **after** the closing `---` to `kairos_mint` so the document starts with the H1. Use the same space as for search. Then search again.
4. **Run** — Follow the chosen match’s `next_action`: `kairos_begin` → `kairos_next` (loop) → `kairos_attest`. Echo nonces and proof hashes from the server. Do not respond to the user before `kairos_attest` when `must_obey: true`.

## Protocol summary

The protocol has seven steps: (1) **Verify skill directory structure** — directory name matches `name`, SKILL.md present, optional references/ scripts/ assets/. (2) **Consult Agent Skills specification via Context7**. (3) **Gather requirements and draft SKILL.md** — purpose, triggers, location, and whether the skill has one protocol or multiple aliases; frontmatter and body. (4) **Create protocol(s) via KAIROS** — for each alias (or single default), produce a protocol doc and save to `references/KAIROS.md` or `references/KAIROS-{alias}.md`. (5) **Mint protocol(s)** — for each existing `references/KAIROS.md` or `references/KAIROS-*.md`, strip frontmatter and call kairos_mint; report chain head URIs or skip. (6) **Verify by execution** — run the minted protocol(s) or skill in a subagent or new chat; report pass/fail. (7) **Lint skill** — run skills-ref validate. Use for personal (~/.cursor/skills/) or project (.cursor/skills/) skills.
