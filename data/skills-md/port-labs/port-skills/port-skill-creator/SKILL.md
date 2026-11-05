---
name: port-skill-creator
description: "Author a new Agent Skill for this repo (port-labs/port-skills): scaffold the skills/port-<name>/ directory, write valid frontmatter, structure the body as a short router into references/ and assets/, validate it, and regenerate the README index. Use when asked to create a new Port skill, add a skill to this repo, help me write a SKILL.md, contribute a skill, port an internal Port AI skill to this repo, or fix a skill that fails validate-skill.js."
license: MIT
compatibility: "Claude Code, Cursor, Codex CLI, GitHub Copilot"
metadata:
  version: "2.0.0"
  author: port-labs
  repository: https://github.com/port-labs/port-skills
  tags: port,meta,skill-authoring,reference
  summary: Author and validate a new skill for this repo
---

# Skill creator

A skill here is a plain file in this git repo, read by a third party's coding
agent, that helps it get a Port job done: build a context lake, write a
mapping, manage Port with Terraform. It is **not** Port's internal in-product
AI skill system (`packages/ai-skills` in `port-labs/port`, which creates a
`skill` entity via `upsert_entity` for Port AI's own runtime). See
[references/skill-writing-guide.md#adapting-an-internal-skill](references/skill-writing-guide.md#adapting-an-internal-skill)
if you're starting from one of those.

This skill itself lives at `.claude/skills/port-skill-creator/`, not under
`skills/`, because it's for someone contributing to *this repo*, not for
someone who installed `skills/` into their own coding agent to work with
their Port account. It never ships to end users; it's only relevant when
working in this repo, so it stays repo-local.

## Prerequisites

None. This is a reference skill, no live Port account or MCP server needed,
just this repo and Node.js to run the scripts below.

## File layout

```text
skills/port-<name>/
├── SKILL.md            # required: short frontmatter + router body
├── references/         # one file per sub-topic, the actual depth
└── assets/              # images, scripts, and complete ready-to-run examples
```

`<name>` must be lowercase, hyphenated, prefixed with `port-`, and match the
frontmatter `name` exactly (enforced by `validate-skill.js`).

## How to build a skill

1. **Scope it.** One sentence on what job this helps do, what it assumes
   already exists, and what's explicitly out of scope (point to the skill
   that owns that instead). Check the [README](../../../../README.md) so scopes
   don't overlap. See [references/skill-writing-guide.md#scope-it-first](references/skill-writing-guide.md#scope-it-first).
2. **Choose reference vs. MCP-powered.** See
   [references/skill-writing-guide.md#choose-a-skill-class](references/skill-writing-guide.md#choose-a-skill-class).
3. **Write the frontmatter, description last.** `description` is the only
   place "when to use this" lives, packed with realistic trigger phrases.
   Never restate it as a body section. See
   [references/skill-writing-guide.md#description-the-trigger-signal](references/skill-writing-guide.md#description-the-trigger-signal).
4. **Write the body as a router, not a manual.** Assume the agent already
   decided to do the job. State prerequisites, then a short numbered list of
   what to do, each step pointing at the `references/*.md` file that has the
   actual depth. Target well under 100 lines. See
   [references/skill-writing-guide.md#body-is-a-router](references/skill-writing-guide.md#body-is-a-router)
   for the shape and a worked example.
   Prerequisites should point to the `port-getting-started` skill for account
   setup and MCP connection instead of restating it, and should say
   explicitly that this skill can use Port's MCP server to apply the work
   directly when connected, and that `search_port_knowledge_sources` covers
   anything the skill itself doesn't. See
   [references/skill-writing-guide.md#prerequisites-port-getting-started-and-mcp](references/skill-writing-guide.md#prerequisites-port-getting-started-and-mcp).
5. **Push real content into references/ and assets/.** One reference file
   per sub-topic (`references/blueprints.md`, `references/mirror-properties.md`,
   not one giant `references/details.md`). Assets are anything ready to use
   as-is: images, scripts, complete examples.
6. **Validate:** `node .claude/skills/port-skill-creator/scripts/validate-skill.js skills/port-<name>` (or `--all`).
7. **Regenerate the README index:** `node .claude/skills/port-skill-creator/scripts/generate-skill-index.js`.
8. **Test it for real.** Install it (`cp -r skills/port-<name> ~/.claude/skills/`),
   run 2-3 realistic trigger prompts in a fresh session, confirm it loads
   and produces correct, ready-to-apply Port config.

## Common pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `validate-skill.js` reports "Unexpected fields in frontmatter" | A field outside `name`, `description`, `license`, `allowed-tools`, `metadata`, `compatibility` | Remove it, or move it under `metadata` |
| "Directory name must match skill name" | `name:` and the `skills/<dir>` folder differ | Rename one to match the other |
| "Skill name must start with the 'port-' prefix" | Every skill in this repo is namespaced `port-*` | Rename the directory and `name:` to `port-<name>` |
| Skill never triggers in real use | `description` is generic instead of listing trigger phrases | Rewrite per [references/skill-writing-guide.md#description-the-trigger-signal](references/skill-writing-guide.md#description-the-trigger-signal) |
| `SKILL.md` reads like a manual, not a router | Real instructions were written inline instead of in `references/` | Move the depth out, leave a one-line pointer per step |
| Body has a "Use this skill when" section | Old convention; that's the `description`'s job now | Delete the section, fold anything useful into `description` |
| README table doesn't show the new skill | `generate-skill-index.js` wasn't run | Run it, commit the README diff |
| Prerequisites restate account signup and MCP setup inline | Should point to `port-getting-started` instead | Replace with a pointer, keep only what's specific to this skill |

## Quick reference

- Layout: `skills/port-<name>/{SKILL.md, references/, assets/}`.
- Frontmatter allowed fields: `name`, `description`, `license`,
  `allowed-tools`, `metadata`, `compatibility`.
- Two classes: **reference** (no live account needed) and **MCP-powered**
  (uses Port MCP tools when connected, documented fallback when not).
- Body is a router: intro, `Prerequisites`, a short numbered list of steps
  that each point into `references/`, nothing more. No `Use this skill
  when` section, that's what `description` is for.
- Prerequisites point to `port-getting-started` for setup, and note that Port's
  MCP server (when connected) can apply the work directly, with
  `search_port_knowledge_sources` for anything uncovered.
- Validate: `node .claude/skills/port-skill-creator/scripts/validate-skill.js skills/port-<name>` (or `--all`).
- Regenerate the README index: `node .claude/skills/port-skill-creator/scripts/generate-skill-index.js`.
- Full authoring guidance, examples, and the skill template:
  [references/skill-writing-guide.md](references/skill-writing-guide.md).
