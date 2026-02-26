---
name: skill-quality-auditor
description: Self-audit tool for the Gemini Skills monorepo. Ensures SKILL.md quality, script functionality, and test coverage for all skills.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    description: Project root directory
  - name: skill
    short: s
    type: string
    description: Audit a single skill by name
  - name: min-score
    type: number
    description: Minimum passing score (0-12)
category: Governance & Security
last_updated: '2026-02-13'
tags:
  - compliance
  - gemini-skill
  - qa
---

# Skill Quality Auditor

Self-audit tool that scores every implemented skill against a 12-point quality checklist.

## Usage

node skill-quality-auditor/scripts/audit.cjs [options]

## Options

| Flag          | Alias | Type   | Required | Description                             |
| ------------- | ----- | ------ | -------- | --------------------------------------- |
| `--dir`       | `-d`  | string | No       | Project root directory (default: cwd)   |
| `--skill`     | `-s`  | string | No       | Audit a single skill by name            |
| `--min-score` |       | number | No       | Minimum passing score 0-12 (default: 0) |

## Quality Checks (12 total)

1. SKILL.md has valid frontmatter (name, description, status)
2. SKILL.md has Troubleshooting section
3. SKILL.md has Usage section
4. Has package.json
5. Has executable script in scripts/
6. Uses skill-wrapper (runSkill/runSkillAsync)
7. Uses yargs for CLI arguments
8. Uses validators.cjs for input validation
9. Has TypeScript type definitions
10. Has unit test coverage
11. Has integration test coverage
12. Has proper error handling

## Troubleshooting

| Error                         | Cause                                | Fix                                             |
| ----------------------------- | ------------------------------------ | ----------------------------------------------- |
| `SKILL.md not found`          | Running from wrong directory         | Ensure `--dir` points to monorepo root          |
| `No implemented skills found` | No skills with `status: implemented` | Check SKILL.md frontmatter in skill directories |

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
