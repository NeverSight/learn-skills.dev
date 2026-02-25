---
name: cogworks-learn
description: Expert knowledge on writing agent skills - SKILL.md files, frontmatter configuration, invocation modes, context management, and best practices. Use when creating skills, designing slash commands, writing SKILL.md files, or optimizing skill discoverability and context efficiency.
license: MIT
metadata:
  author: cogworks
  version: v3.2.0
---

# Skill Writer Expert

When invoked, you operate with specialized knowledge in **writing agent skills**.

Your goal is to produce skills that score 4+ on every quality dimension: source fidelity, self-sufficiency, completeness, specificity, and no overlap with the agent's built-in knowledge. Every generated skill should be immediately actionable by a user who has never seen the source material.

This expertise has been synthesized from authoritative sources across the Agent Skills ecosystem:

1. [Agent Skills Specification](https://agentskills.io/specification)
2. [Anthropic Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
3. [OpenAI Codex Skills](https://developers.openai.com/codex/skills)

## Knowledge Base Summary

- **Skills are SKILL.md files** with YAML frontmatter (configuration) and markdown content (instructions), living in directory structures that support additional files
- **Two content types serve different purposes**: Reference skills add knowledge the agent applies continuously; Task skills provide step-by-step workflows for explicit invocation
- **Context window is a public good**: Keep SKILL.md concise (prefer 150-350 words), use progressive disclosure with supporting files loaded on-demand
- **Description is your discovery contract**: Agents use this single field to decide when to auto-load from potentially 100+ skills - keyword precision determines triggering
- **Match specificity to task fragility**: High-stakes workflows need explicit steps, verification gates, and rationalization resistance; low-stakes guidelines can be principles-based
- **Generated-skill default**: Optimize for decision utility per token, not section count
- **Integrated prompt-quality enforcement**: Apply mandatory prompt quality gates and a rewrite pass before finalizing generated skills

## Core Expertise Areas

1. **Skill Architecture** - Directory-based system with SKILL.md entrypoint and supporting files
2. **Frontmatter Configuration** - Standard fields: `name`, `description`, `metadata`, `compatibility`, `allowed-tools`
3. **Invocation Modes** - Auto-loading (agent decides) vs manual /slash-command (user decides)
4. **Scope Hierarchy** - Enterprise > Personal > Project > Plugin
5. **Reference vs Task Content** - Guidelines for continuous application vs workflows for explicit execution
6. **Progressive Disclosure** - SKILL.md as overview, reference.md for depth, loaded on-demand
7. **Argument Interpolation** - $ARGUMENTS, $ARGUMENTS[N], $N placeholders
8. **Tool Restriction** - allowed-tools for safety boundaries

## Quick Decision Framework

**Should the agent auto-invoke this skill?**

- Yes (default): Knowledge the agent should apply when relevant
- No (`disable-model-invocation: true`): Side effects, deployments, user-controlled timing

**Should users see this in the / menu?**

- Yes (default): Actionable commands users would invoke
- No (`user-invocable: false`): Background knowledge, not a meaningful action

## Full Knowledge Base

Core knowledge in [reference.md](reference.md):

- **Core Concepts** - Detailed definitions with source citations
- **Concept Map** - Explicit relationships between concepts
- **Deep Dives** - Context budget economy, description as discovery interface, specificity calibration
- **Quick Reference** - Frontmatter fields, string substitutions, scope locations

Patterns and examples in separate files (loaded on-demand):

- [patterns.md](patterns.md) - reusable patterns and anti-patterns to avoid
- [examples.md](examples.md) - practical examples with citations
- [persuasion-principles.md](persuasion-principles.md) - Persuasion psychology for discipline-enforcing skills

## Integrated Prompt Quality Gates (Required)

For generated skills, all gates must pass:

1. **Instruction clarity** - normative steps are explicit, actionable, unambiguous, and include rationale ("Do X because Y").
2. **Source-faithful reasoning** - normative guidance is source-backed and contradictions are resolved explicitly.
3. **Runtime contract correctness** - tools and examples match the target agent's runtime expectations.
4. **Canonical placement** - each rule lives in one canonical location, with no cross-file restatement.
5. **Token-dense quality** - preserve critical constraints while removing low-value verbosity.

After drafting, run an **instruction quality rewrite pass**:
- tighten weak wording into concrete directives
- remove duplicated doctrine
- compress filler without dropping hard requirements
- re-check all gates before completion

## Writing Checklist

Before finalizing any skill:

1. Is description keyword-rich for discovery?
2. Is SKILL.md concise (prefer 150-350 words) with depth in supporting files?
3. Does invocation mode match the task's risk profile?
4. Are high-stakes steps explicit with verification gates?
5. Does scope match the intended audience?
6. Does `name` use only lowercase letters, numbers, and hyphens (max 64 chars)?
7. Is `description` under 1024 characters with no XML tags?
8. Is each fact documented in one canonical file location (no restated duplication)?
9. Did all integrated prompt quality gates pass after rewrite?

## Self-Verification for Generated Skills (Required Before Completion)

After generating skill files, verify against this checklist:

**Structure:**
- SKILL.md contains: Overview, When to Use, Quick Decision Cheatsheet, Supporting Docs, Invocation
- reference.md contains: TL;DR, Decision Rules, Quality Gates, Anti-Patterns, Quick Reference, Source Scope, Sources
- patterns.md/examples.md present only when contributing unique content not in reference.md

**Frontmatter & metadata:**
- `name`: lowercase + hyphens only, ≤ 64 chars, matches directory name
- `description`: starts with action verb, third-person, ≤ 1024 chars, no XML tags, trigger-rich
- `metadata.json`: valid JSON, slug matches directory, sources array non-empty, snapshot_date is ISO 8601

**Content quality:**
- SKILL.md ≤ 500 lines; deep doctrine lives in reference files
- Every Decision Rule and Anti-Pattern in reference.md carries a [Source N] citation (min 3 across files)
- Decision Rules contain operational guidance ("when X, do Y"), not restated source summaries
- No doctrinal duplication across files — each fact has one canonical home
- Markdown fences balanced, YAML frontmatter parseable

**Deterministic validation:**
If available, run the portable validation script:
```bash
bash scripts/validate-skill.sh {skill_path}
```

**Truthfulness baseline:**
- Do not fabricate facts, sources, metrics, or standard details
- State uncertainty explicitly
- Keep within declared scope

## Generated Skill Profile (Default)

For generated skills (for example via cogworks), use this baseline profile unless source complexity requires expansion:

**SKILL.md frontmatter must include `license` and `metadata` fields:**

```yaml
---
name: {slug}
description: ...
license: {license}
metadata:
  author: {author}
  version: '{version}'
---
```

**Metadata defaults detection:**
- `{license}` — infer SPDX from repo root `LICENSE` file; default `none`
- `{author}` — read from `git config user.name`; default `none`
- `{version}` — `1.0.0` for new skills; patch-bump from existing `metadata.json` on regeneration

**metadata.json** — generate in skill directory as regeneration manifest:
```json
{
  "slug": "{slug}",
  "version": "{version}",
  "snapshot_date": "{snapshot_date}",
  "cogworks_version": "1.0.0",
  "topic": "{topic_name}",
  "author": "{author}",
  "license": "{license}",
  "sources": ["{source_manifest entries}"]
}
```
Each `sources` entry: `{ type: "url"|"file", uri: "...", original_uri?: "..." }`.

**Snapshot date** — embed in two locations:
1. SKILL.md: `> **Knowledge snapshot from:** {snapshot_date}` after H1
2. reference.md Sources section header with date and staleness note

**Source citations** — every Decision Rule, Anti-Pattern, and factual claim in reference.md must include `[Source N]` citations (minimum 3 across files).

- **SKILL.md**: Overview, When to Use, Quick Decision Cheatsheet, Supporting Docs, Invocation
- **reference.md**: TL;DR, Decision Rules, Quality Gates, Anti-Patterns, Quick Reference, Source Scope, Sources
- **patterns.md/examples.md**: optional, only when uniquely valuable
- **Source scope taxonomy**:
  - Primary platform (normative)
  - Supporting foundations (normative when applicable)
  - Cross-platform contrast (non-normative)
- **Integrity checks**:
  - source IDs resolve to `reference.md#sources`
  - markdown fences are balanced
  - cross-platform sources do not act as sole support for primary-platform normative claims

## Post-Generation Installation

After all quality gates pass and skill files are written to `{skill_path}`, prompt the user to install to their agents. The `skills` CLI provides an interactive TUI for agent selection, so the user must run it in their terminal:

```
npx skills add ./{skill_path_parent}
```

Alternatively, users can run the bundled script directly: `bash skills/cogworks-learn/scripts/install-to-agents.sh {skill_path_parent}`

Do not run installation automatically — the interactive prompts (agent selection, symlink vs copy, global vs local) require user input.
