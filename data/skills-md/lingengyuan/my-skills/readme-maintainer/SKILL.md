---
name: readme-maintainer
description: Update or rewrite project README files directly with the current session model (Codex/Claude Code) using local repository facts, without calling external README generation APIs. Use when users ask to "update README", "rewrite readme.md", "generate project documentation", "refresh usage/install sections", or "align README with latest code changes" for a local repo.
---

# Readme Maintainer

## Overview

Maintain `README.md` as a code-adjacent artifact: grounded in the current repository state, clear for users, and safe from hallucinated commands. Use the active assistant model in this session; do not route through `readme-ai` provider APIs. Default to bilingual parity (English + Simplified Chinese) unless the user explicitly asks for single-language output.

## Workflow

1. Resolve target repo path:
- Default to current working directory if user does not specify a path.
- Use explicit path if the user provides one.
- Confirm `README.md` destination (`README.md` by default).

2. Collect project facts:
- Run `scripts/collect_repo_facts.sh <repo-path>`.
- Read existing `README.md` first (if present), then read only relevant source/config files.
- Prefer authoritative files: `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Makefile`, and entrypoint modules.

3. Draft content with repository truth as source of record:
- Keep or improve useful existing sections.
- Add missing core sections only when supported by codebase facts.
- If data is unknown, state TODO/placeholder text explicitly instead of inventing details.
- If README is bilingual or user audience is mixed, draft mirrored English and Chinese sections with equivalent meaning and scope.

4. Apply update:
- Write directly to `README.md` unless user asks for preview file.
- Preserve user-specific sections where possible (`Contributing`, `Roadmap`, `Acknowledgements`) unless user asks for full rewrite.

5. Validate before finishing:
- Re-check all commands and paths against files in repo.
- Ensure install/run/test steps exist and are executable in principle.
- Run quick sanity checks when cheap (`rg` for referenced scripts/targets).
- For bilingual README, run `scripts/check_bilingual_readme.sh README.md` and fix missing paired headings.

6. Report changes:
- Summarize what sections changed and why.
- Note any assumptions or unresolved gaps.

## Required Constraints

- Use the current session model for generation and editing.
- Do not call external README generation providers or ask user for provider switching.
- Do not fabricate metrics, compatibility claims, or benchmark numbers.
- Do not claim commands work unless they are grounded in repo files.
- Default to bilingual output (`## English` and `## 简体中文`) for externally facing project README files.
- Keep English and Chinese sections synchronized: each required section in one language must have its counterpart in the other language unless user explicitly opts out.

## Output Shape

Prefer this structure, adapting to project reality:
- Project title + one-line value proposition
- Features / capabilities
- Install
- Quick start / usage
- Configuration (if applicable)
- Development and testing
- Project structure (short tree)
- Contributing / license

For bilingual mode (default), keep a mirrored section map:
- `### Project Description` <-> `### 项目说明`
- `### Features` <-> `### 功能特性`
- `### Quick Start` <-> `### 快速开始`
- `### Skill Catalog` <-> `### 技能目录`
- `### Project Structure` <-> `### 项目结构`
- `### Configuration` <-> `### 配置` (when environment variables or service setup are required)
- `### Development and Testing` <-> `### 开发与测试`
- `### Contributing` <-> `### 贡献指南`
- `### Maintenance Guide` <-> `### 维护指南`
- `### License` <-> `### 许可证`

Read `references/readme-checklist.md` when drafting.

## Commands

```bash
# Gather repo facts before editing README
scripts/collect_repo_facts.sh <repo-path>

# Validate bilingual section parity
scripts/check_bilingual_readme.sh README.md
```
