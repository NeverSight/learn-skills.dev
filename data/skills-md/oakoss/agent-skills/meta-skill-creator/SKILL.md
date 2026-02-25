---
name: meta-skill-creator
description: >
  Create agent skills following the Agent Skills open standard.
  Use when building new skills for Claude Code, Cursor, Gemini CLI, or other agents.
  Use for skill structure, SKILL.md authoring, frontmatter configuration, progressive disclosure, reference files, validation, and distribution.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: https://agentskills.io
disable-model-invocation: true
---

# Meta Skill Creator

## Overview

Agent Skills are portable folders of instructions, scripts, and resources that agents discover and load on demand. They follow the [Agent Skills open standard](https://agentskills.io) and work across 27+ compatible agents including Claude Code, Cursor, Gemini CLI, OpenAI Codex, VS Code, GitHub Copilot, Windsurf, Goose, and Roo Code. This skill covers the complete workflow for creating, structuring, and validating skills.

## Quick Reference

| Concept                | Summary                                                                  | Key Rule                                         |
| ---------------------- | ------------------------------------------------------------------------ | ------------------------------------------------ |
| Directory structure    | `skill-name/SKILL.md` plus optional `references/`, `scripts/`, `assets/` | `SKILL.md` is the only required file             |
| Frontmatter (required) | YAML block with `name` and `description`                                 | `name` must match directory, max 64 chars        |
| Frontmatter (optional) | `license`, `compatibility`, `metadata`, `allowed-tools`                  | Defined by open standard, portable across agents |
| Agent-specific fields  | `model`, `context`, `agent`, `hooks`, `user-invocable`                   | Claude Code extensions, not portable             |
| Description triggers   | Include "Use when..." or "Use for..." phrases                            | Keyword-rich, third-person voice                 |
| Progressive disclosure | Metadata -> Instructions -> Resources (three tiers)                      | SKILL.md loaded in full; references on demand    |
| SKILL.md size          | Target 100-150 lines, max 500                                            | No code examples in SKILL.md                     |
| SKILL.md sections      | Overview, Quick Reference, Common Mistakes, Delegation, References       | All five sections required                       |
| Reference files        | `references/[topic].md` with frontmatter                                 | Max 500 lines each, self-contained               |
| Reference frontmatter  | `title`, `description`, `tags` fields                                    | Required for all reference files                 |
| Scripts                | `scripts/` directory, executable code                                    | Agents run scripts, not read source              |
| Name format            | Lowercase letters, numbers, hyphens                                      | No `--`, no leading/trailing `-`, min 4 chars    |
| Excluded filenames     | `README.md`, `metadata.json`, `_*` files                                 | Not installed by distribution CLI                |
| Validation             | `skills-ref validate` or project-specific validators                     | Always validate before distributing              |

## Skill Creation Workflow

1. **Create directory** at the appropriate location with a `SKILL.md`
2. **Write frontmatter** with `name` (matching directory) and trigger-rich `description`
3. **Write required sections**: Overview, Quick Reference, Common Mistakes, Delegation, References
4. **Extract code examples** into `references/` files (no code in SKILL.md)
5. **Validate** with your project validator or `skills-ref validate`

## Common Mistakes

| Mistake                                 | Correct Pattern                                                   |
| --------------------------------------- | ----------------------------------------------------------------- |
| Missing "Use when" or "Use for" trigger | Include trigger phrases in description for agent discovery        |
| Code examples in SKILL.md               | Move all code to `references/` files                              |
| SKILL.md over 500 lines                 | Split detailed content into reference files                       |
| Reference files cross-referencing       | Keep references self-contained, one level deep from SKILL.md      |
| Name does not match directory           | `name` field must exactly match parent directory name             |
| Name contains uppercase or spaces       | Use only lowercase letters, numbers, and hyphens                  |
| Vague description without keywords      | Pack triggers with synonyms, abbreviations, library names         |
| Code blocks without language specifier  | Always specify language on fenced code blocks                     |
| Supporting files not linked in SKILL.md | Agents discover files through explicit links in SKILL.md          |
| Using excluded filenames                | Avoid `README.md`, `metadata.json`, files starting with `_`       |
| Blank line before frontmatter           | `---` must be on line 1, no preceding blank lines                 |
| Description in first-person voice       | Use third-person: "Extracts text", not "I help you"               |
| Deeply nested reference chains          | Keep one level deep: SKILL.md links to references directly        |
| Missing required SKILL.md sections      | Include all five: Overview, Quick Ref, Mistakes, Delegation, Refs |
| Reference file missing frontmatter      | Every reference needs `title`, `description`, and `tags`          |

## Skill Locations

Skills can be installed at different scopes depending on visibility needs:

| Location    | Path                | Scope                |
| ----------- | ------------------- | -------------------- |
| Personal    | `~/.claude/skills/` | You, all projects    |
| Project     | `.claude/skills/`   | Anyone in repository |
| Distributed | Via `skills` CLI    | Plugin users         |

## Delegation

- **Specification questions**: Refer to the [Agent Skills open standard](https://agentskills.io/specification)
- **Pattern discovery**: Use `Explore` agent to analyze existing skills for structure examples
- **Validation**: Run project validator or `skills-ref validate` before committing

## References

- [Skill anatomy: directory structure, SKILL.md sections, progressive disclosure, and size thresholds](references/skill-anatomy.md)
- [Frontmatter: required and optional YAML fields with constraints and usage guidance](references/frontmatter.md)
- [Validation: checklist, common issues, and testing your skill](references/validation.md)
