---
name: skill-installer
description: Install a skill from a GitHub URL that points to a skill folder by downloading it into .github/skills.
---

# Skill Installer

- Use this skill when the user provides a GitHub URL that points to a specific skill folder and asks to bring it into this repo.
- Run the installer script in .github/skills/skill-installer/scripts/install-skill.js with the GitHub URL. The scripts in that folder are chmod +x, so run them directly (no node prefix).
- If the destination folder already exists, ask whether to overwrite before using the --force flag.
- After installation, confirm that the folder exists under .github/skills/<skill-name> and that SKILL.md is present.
