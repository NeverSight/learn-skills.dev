---
name: tentacle-obsidian-init
description: | 
  Initializes an Obsidian vault with a best-practice directory structure, templates, and AI Agent guardrails optimized for text and image content creators. Use when a user asks to set up a new Obsidian vault, organize a messy vault for AI-assisted content creation, or scaffold the creator folder structures and agent rules/standards. 
  Triggers: "initialize vault", "setup obsidian for creator", "scaffold vault", "create creator structure", "init vault".
---

# Skill: tentacle-obsidian-init

## Purpose

Sets up a high-performance, AI-friendly Obsidian vault architecture tailored for text and image content creators. It combines a PARA-inspired structure (`Inbox`, `Notes`, `Projects`, `Resources`, `Areas`) with strict AI Agent guardrails (`AGENTS.md`).

This ensures any new vault is immediately ready for both human content creation and safe AI assistant operations.

## Vault Scaffolding Initialization

To initialize or restructure the vault, execute the scaffolding script. 

The script will copy all predefined directories, markdown templates, and guardrail rules perfectly into the root vault directory. 

### Execution Command

```bash
uv run .agents/skills/tentacle-obsidian-init/scripts/init_vault.py
```

*Note: The script uses only standard libraries and safely merges layers via `shutil.copytree(dirs_exist_ok=True)`. It does not delete existing user files.*

## Post-Initialization Checklist

After the script runs, kindly remind the user to complete these manual configurations inside Obsidian settings:

- **Attachment settings**: Set *Default location for new attachments* to the `Assets/` folder.
- **Template settings** (if Core Templates plugin is used): Set *Template folder location* to the `Templates/` folder.
