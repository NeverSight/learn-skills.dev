---
name: claude-skill-spec-audit
description: >
  Audit skill SKILL.md files for compliance with the agentskills.io specification.
  Checks frontmatter fields (name, description, compatibility, metadata, argument-hint)
  and metadata sub-fields (author, scope, confirms). Use when adding new skills,
  reviewing skill quality, or ensuring all skills follow the spec.
  Triggers: "audit skills", "check skill spec", "skill compliance", "are my skills
  up to spec", "/claude-skill-spec-audit".
argument-hint: "[skill-name ...] [--fix]"
compatibility: Designed for Claude Code
metadata:
  author: jackchuka
  scope: generic
  confirms:
    - add missing frontmatter fields
---

# Skill Spec Audit

Check installed skills against the [agentskills.io specification](https://agentskills.io/specification) and local conventions for metadata completeness.

## Arguments

- **Skill names**: tokens after the command -> filter to those skills only
- **--fix**: automatically add missing fields (prompts for values)
- **Default**: scan all non-symlinked skills in `~/.claude/skills/`

## Spec Requirements (agentskills.io)

| Field           | Required | Notes                                                          |
| --------------- | -------- | -------------------------------------------------------------- |
| `name`          | Yes      | 1-64 chars, lowercase, hyphens only, must match directory name |
| `description`   | Yes      | 1-1024 chars, non-empty                                        |
| `compatibility` | No       | Max 500 chars, environment requirements                        |
| `metadata`      | No       | Arbitrary key-value map                                        |
| `allowed-tools` | No       | Space-delimited tool list (experimental)                       |

## Naming Conventions

Skill names follow the pattern: `[scope]-[platform/org]-[group]-[name]`

### Rules

1. Lowercase, kebab-case, no consecutive hyphens, 2-4 words, max 40 chars
2. Role-noun suffixes allowed (`-writer`, `-scheduler`, `-namer`)
3. Standardized action synonyms: `audit` (compliance), `scan` (broad analysis), `search` (lookup), `triage` (classify+act)

### Scope prefix (required)

Derived from `metadata.scope`:

| Scope          | Prefix | Example                                |
| -------------- | ------ | -------------------------------------- |
| `personal`     | `p-`   | `p-slack-triage`, `p-daily-standup`    |
| `organization` | `o-`   | `o-org-release-digest`                 |
| `generic`      | (none) | `skill-spec-audit`, `gh-dep-pr-triage` |

### Platform prefix (when single-platform dependent)

| Platform         | Prefix   | When to use                           |
| ---------------- | -------- | ------------------------------------- |
| GitHub           | `gh-`    | Skill requires `gh` CLI or GitHub API |
| Git              | `git-`   | Skill requires git but not GitHub     |
| Slack            | `slack-` | Skill requires Slack MCP server       |
| Google Workspace | `gws-`   | Skill requires `gws` CLI              |

**Multi-platform or general skills stay unprefixed.** If a skill touches 2+ platforms, no platform prefix — the scope prefix alone is enough.

### Group prefix (when 2+ skills share a domain)

| Group    | Skills in group                                                |
| -------- | -------------------------------------------------------------- |
| `daily-` | standup, report, reflection                                    |
| `skill-` | dry-run, prereq-audit, spec-audit                              |
| `blog-`  | writer, post-mining                                            |
| `oss-`   | release, release-prep                                          |
| `org-`   | release-digest, incident-investigation, sync-skills-to-plugins |

When creating a new skill, check for existing siblings. If a second skill appears in the same domain, retroactively add a shared prefix to both.

## Local Conventions (beyond spec)

These are project-specific conventions enforced on top of the spec:

| Field               | Expected                  | Values                                         |
| ------------------- | ------------------------- | ---------------------------------------------- |
| `argument-hint`     | If skill accepts args     | Short usage hint string                        |
| `metadata.author`   | Always                    | Must be present (non-empty)                    |
| `metadata.scope`    | Always                    | `generic`, `personal`, or `organization`       |
| `metadata.confirms` | If skill has side effects | List of operations requiring user confirmation |

## Workflow

### Phase 1: Discover Skills

1. Glob for `~/.claude/skills/*/SKILL.md`
2. Also check `.claude/skills/*/SKILL.md` (project-level)
3. **Skip symlinks** — those point to `.agents/skills/` and have their own conventions
4. If user specified skill names, filter to matching directories
5. Read each SKILL.md frontmatter

### Phase 2: Validate Each Skill

For each SKILL.md, check:

**Spec compliance:**

1. `name` exists, matches directory name, is lowercase with hyphens only, no consecutive hyphens, 1-64 chars
2. `description` exists, is non-empty, 1-1024 chars
3. `compatibility` exists (warn if missing — not required by spec but expected locally)

**Naming conventions:**

4. Scope prefix matches `metadata.scope`: `p-` for personal, `o-` for organization, none for generic
5. Platform prefix present if skill depends on a single platform (`gh-`, `git-`, `slack-`, `gws-`)
6. No platform prefix if skill uses 2+ platforms
7. Action synonym is standardized: `audit` not `review`/`check`, `scan` not `inspect`
8. No single-word names (must have at least one hyphen)
9. Max 40 chars, 2-4 words
10. Abbreviations only from allowlist: `pr`, `cli`, `oss`, `dep`, `mcp`, `gh`, `gws`

**Local conventions:**

11. `metadata.author` is present and non-empty
12. `metadata.scope` is one of: `generic`, `personal`, `organization`
13. `metadata.confirms` exists if the skill body references any of these patterns:

- Slack: `send_message`, `post message`, `post to Slack`
- Git: `git commit`, `git push`, `create commit`, `push to remote`
- GitHub: `merge`, `approve`, `create PR`, `create issue`, `create release`, `gh release`
- Calendar: `create event`, `insert event`
- Files: `save to`, `write to`, `create file`
- Install: `brew install`, `install`

7. `argument-hint` exists if the skill body references arg parsing, `## Arguments`, or accepts parameters

### Phase 3: Report

Print a table:

```
## Skill Spec Audit

| Skill | name | naming | desc | compat | author | scope | confirms | arg-hint | Issues |
|-------|------|--------|------|--------|--------|-------|----------|----------|--------|
| gh-dep-pr-triage | ok | ok | ok | ok | ok | ok | ok | — | 0 |
| p-blog-writer | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| new-skill | ok | MISS:scope-prefix | ok | MISS | MISS | MISS | WARN | — | 4 |

Legend: ok = present and valid, MISS = missing, WARN = likely needed but missing, — = not applicable
Summary: N skills checked, M fully compliant, X issues found
```

### Phase 4: Fix (if --fix or user asks)

For each issue, prompt the user for the value or infer it:

| Field               | Inference strategy                                                    |
| ------------------- | --------------------------------------------------------------------- |
| `compatibility`     | Scan for CLI tools, MCP servers in body -> suggest "Requires X, Y"    |
| `metadata.author`   | Infer from existing skills or ask user                                |
| `metadata.scope`    | Ask user: generic, personal, or organization?                         |
| `metadata.confirms` | Extract side-effect patterns from body, present list for confirmation |
| `argument-hint`     | Extract from `## Arguments` section if present, otherwise ask         |

After fixing, use Edit to insert missing fields before the closing `---`.

Re-run validation and show updated table.

## Determining `metadata.scope`

| Scope          | Criteria                                                          |
| -------------- | ----------------------------------------------------------------- |
| `generic`      | Works for anyone, no personal/org-specific data                   |
| `personal`     | References your specific accounts, channels, search terms, voice  |
| `organization` | References company repos, internal tools, team-specific workflows |

## Determining `metadata.confirms`

Only add `confirms` if the skill can perform **irreversible or externally-visible operations**. Read-only skills (scanning, searching, reporting) do NOT need confirms.

Common confirms patterns:

| Operation             | confirms entry           |
| --------------------- | ------------------------ |
| Post Slack message    | `send Slack messages`    |
| Merge PR              | `merge PRs`              |
| Approve PR            | `approve PRs`            |
| Create GitHub issue   | `create GitHub issues`   |
| Create GitHub release | `create GitHub releases` |
| Create calendar event | `create calendar event`  |
| Git commit            | `create git commit`      |
| Git push              | `push to remote`         |
| Write files           | `save to filesystem`     |
| Install tools         | `install missing tools`  |
| Create PR             | `create PR`              |
| Modify settings       | `modify settings files`  |
