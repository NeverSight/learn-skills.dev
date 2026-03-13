---
name: skill-installer
description: Install Agent Skills to your AI coding agent. Supports Claude Code, Goose, OpenCode, Cursor, and other harnesses.
version: 1.0.0
license: MIT
author: "@anthropic-agent-skills"
tags:
  - installation
  - harness
  - setup
---

## Instructions

Use this skill to install Agent Skills from local directories or the catalog to your preferred harness.

### Supported Harnesses

| Harness | Install Path | Status |
|---------|--------------|--------|
| Claude Code | `~/.claude/skills/{name}/` | Supported |
| Goose | `~/.config/goose/skills/{name}/` | Supported |
| OpenCode | `.opencode/skill/{name}/` | Supported |
| Cursor | `.cursor/skills/{name}/` | Supported |

### How to Use

**Install from local directory:**

```bash
python3 install_skill.py /path/to/my-skill --harness claude-code
python3 install_skill.py ./my-skill --harness goose
```

**Install from catalog:**

```bash
python3 install_skill.py anthropic/document-skills --harness claude-code
python3 install_skill.py anthropic/document-skills --harness goose
```

**Auto-detect harness:**

```bash
python3 install_skill.py /path/to/my-skill
# Detects installed harnesses and prompts for selection
```

**List installed skills:**

```bash
python3 install_skill.py --list
python3 install_skill.py --list --harness claude-code
```

**Uninstall a skill:**

```bash
python3 install_skill.py --uninstall my-skill --harness claude-code
```

### Output

```
Installing skill: document-skills
  Source: /path/to/document-skills
  Target: ~/.claude/skills/document-skills/

  Copying files...
    SKILL.md
    scripts/pdf_tools.py
    references/templates/

  Success! Skill installed to Claude Code.

  To use: The skill will be available in your next Claude Code session.
```

## Examples

**Install to Claude Code:**
```
User: Install the skill at ./my-pdf-tool to Claude Code
Agent: Installing skill to Claude Code...

       Installed: my-pdf-tool
       Location: ~/.claude/skills/my-pdf-tool/
       Files: 3 files copied

       Restart Claude Code to use the new skill.
```

**Install to multiple harnesses:**
```
User: Install ./my-skill to both Claude Code and Goose
Agent: Installing to Claude Code... Done
       Installing to Goose... Done

       Skill installed to 2 harnesses.
```

## Limitations

- Catalog installation requires network access
- Some harnesses require restart to detect new skills
- Project-local harnesses (Cursor, OpenCode) install to current directory

## Dependencies

- Python 3.9+
- requests library (for catalog downloads)
