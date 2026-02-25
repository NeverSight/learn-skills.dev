---
name: skill-management
description: |
  Creates, audits, and validates agent skills following the Agent Skills open standard. Covers YAML frontmatter, description writing, progressive disclosure, directory structure, 9-phase audits, severity classification, and manifest-implementation drift detection.

  Use when creating new skills, writing skill descriptions, auditing existing skills, detecting version drift, validating implementations match manifests, or debugging skill discovery issues.
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: https://agentskills.io
disable-model-invocation: true
---

# Skill Management

## Overview

Guides creation, auditing, and validation of agent skills conforming to the Agent Skills open standard at <https://agentskills.io>. Covers the full lifecycle from scaffolding a new skill through production-quality review.

**When to use:** Creating skills, improving descriptions for discoverability, restructuring skills for progressive disclosure, running quality audits, validating manifest-implementation alignment.

**When NOT to use:** Writing application code, general markdown editing, project management unrelated to skill authoring.

## Quick Reference

| Task                      | Approach                                     | Key Points                                                                     |
| ------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------ |
| Skill directory           | `skill-name/SKILL.md` + optional directories | Only `SKILL.md` is required; `scripts/`, `references/`, `assets/` are optional |
| Frontmatter `name`        | Lowercase, hyphens, 4-64 chars               | Must match directory name, no leading/trailing `-`, no `--`                    |
| Frontmatter `description` | 1-1024 chars with trigger phrases            | Third-person voice, include "Use when" scenarios                               |
| Progressive disclosure    | Metadata -> SKILL.md -> references/scripts   | Keep SKILL.md under 500 lines; move details to references                      |
| Description structure     | Para 1: what + features, Para 2: triggers    | Active voice, name technologies, include error keywords                        |
| Effective descriptions    | 250-350 chars, specific, discoverable        | "Build X" not "This skill helps you build X"                                   |
| Reference files           | `references/topic.md` with frontmatter       | Max 500 lines, self-contained, kebab-case filenames                            |
| Quality audit             | 9-phase systematic review                    | Standards, official docs, code accuracy, cross-file checks                     |
| Severity levels           | Critical / High / Medium / Low               | Evidence-based classification with links                                       |
| Validation scoring        | Average of accuracy, precondition, effect    | Pass requires score >= 0.8 and zero high-severity issues                       |
| Excluded files            | `README.md`, `metadata.json`, `_*` files     | Skills CLI strips these during installation                                    |

## Common Mistakes

| Mistake                                                        | Correct Pattern                                                                 |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Including `README.md` in skill directory                       | Skills CLI excludes `README.md` during installation; use only `SKILL.md`        |
| Writing vague descriptions without discovery keywords          | Include specific technologies, 3-5 "Use when" scenarios, and 2-3 error messages |
| Duplicating knowledge the agent already has                    | Focus on edge cases, platform differences, and gotchas the agent gets wrong     |
| Putting all content in SKILL.md without progressive disclosure | Keep SKILL.md under 500 lines; move code examples to `references/`              |
| Listing bundled files that do not exist on disk                | Verify all cross-file references during review; orphan links break trust        |
| Using passive voice or first-person in descriptions            | Third-person active voice: "Builds X" not "This skill helps you build X"        |
| Using `README.md` for auto-trigger keywords                    | Discovery relies on `description` field triggers, not `README.md`               |
| Referencing non-existent scripts or commands                   | Only reference scripts and commands that actually exist in the skill directory  |

## Delegation

- **Skill discovery and keyword research**: Use `Explore` agent
- **Multi-skill audit and cross-file consistency checks**: Use `Task` agent
- **Skill architecture and directory structure planning**: Use `Plan` agent

> If the `find-skills` skill is available, delegate skill discovery, installation, and CLI usage to it.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s find-skills -a claude-code -y`

## References

- [Creating skills: structure, frontmatter, descriptions, progressive disclosure](references/creating-skills.md)
- [Auditing skills: 9-phase review, severity classification, fix decisions](references/auditing-skills.md)
- [Validating skills: implementation vs manifest, drift detection, pass criteria](references/validation.md)
