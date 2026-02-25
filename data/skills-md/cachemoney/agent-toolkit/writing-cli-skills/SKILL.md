---
name: writing-cli-skills
description: Guide for writing skills that wrap CLI tools. Use when creating a new CLI skill. For review, run through the Checklist section.
---

# Writing CLI Skills

How to write an agent skill for a command-line tool.

## Quick Start

1. **Install the tool and play with it** — don't just read docs. If the tool is unavailable, use WebFetch on official docs + man pages, but note this in your skill as "not hands-on verified"
2. Run `--help` on every subcommand
3. Try the common operations yourself
4. Note what surprises you or isn't obvious
5. Copy `references/template.md` to your new skill directory
6. Fill in sections based on your hands-on experience
7. Delete sections that don't apply

```bash
# First: actually use the tool
my-tool --help
my-tool subcommand --help
my-tool do-something  # try it!

# Then: create the skill
# This will depend on the tool

# Claude Code
ln -s "$PWD/skills/my-tool" ~/.claude/skills/my-tool

# OpenCode
ln -s "$PWD/skills/my-tool" ~/.config/opencode/skills/my-tool

# Clawdbot
ln -s "$PWD/skills/my-tool" ~/clawd/skills/my-tool
```

**Reading docs is no substitute for hands-on use.** You'll discover defaults, gotchas, and real behavior that docs don't mention.

## What NOT to Do

- Do not dump `--help` output verbatim — summarize the useful parts
- Do not document every flag — focus on the 80% use cases
- Do not include commands you haven't tested
- Do not exceed 500 lines — this bloats agent context windows

## Sections

### Required

Every CLI skill needs at minimum:

| Section | Purpose |
|---------|---------|
| **Frontmatter** | name, description (with trigger phrases) |
| **Installation** | How to get the binary |
| **Usage** | The 80% use cases |

### Recommended

| Section | When to Include |
|---------|-----------------|
| Requirements | Tool needs accounts, API keys, or dependencies |
| Quick Start | Tool has a simple "happy path" |
| Output Formats | Tool can output JSON or custom formats |
| Tips & Gotchas | Tool has some edge cases or things an agentic LLM should not use |
| Troubleshooting | Tool has debug modes or common failure modes |
| Configuration | Tool has config files or env vars |
| Uninstall | Tool leaves config/data behind |
| References | When there are useful docs or content that contains more details |

## Writing Good Descriptions

Include trigger phrases so the agent knows when to load the skill:

```yaml
# Good
description: Monitor RSS feeds for updates. Use when tracking blogs, checking for new posts, or building a feed reader workflow.

# Bad  
description: RSS tool.
```

## Organizing Commands

Group by **task**, not by command name:

```markdown
## Usage

### View / List
### Create / Add  
### Edit / Update
### Delete / Remove
### Search
```

## Progressive Disclosure

Keep SKILL.md under ~500 lines. Move details to references/:

```
my-tool/
├── SKILL.md                    # Core usage
├── references/
│   ├── advanced-config.md      # Deep config docs
│   └── api-reference.md        # API details
└── scripts/
    └── helper.sh               # Helper scripts
```

## Frontmatter Reference

```yaml
---
name: tool-name                  # Required, matches directory
description: What + when         # Required, include triggers
---
```

## Checklist

Before publishing a CLI skill:

- [ ] Frontmatter has name + description with trigger phrases
- [ ] Installation covers target platforms
- [ ] Includes verification command (`tool --version`)
- [ ] Config file locations documented
- [ ] Required env vars listed
- [ ] Common operations in usage cover 80% of use cases
- [ ] Examples show realistic usage with sample output
- [ ] Output formats documented (if tool supports JSON/etc)
- [ ] Troubleshooting includes debug mode
- [ ] Uninstall cleans up config and data
- [ ] Under 500 lines (details in references/)

## Template

See `references/template.md` for a complete starting point.
