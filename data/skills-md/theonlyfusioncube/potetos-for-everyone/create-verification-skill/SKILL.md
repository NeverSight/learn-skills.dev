---
name: create-verification-skill
description: Generate a project-local verification skill that drives the real app and captures evidence. Use when setting up automated verification for a repo.
---
# Create Verification Skill

1. Interview the repository to discover primary user-facing surfaces (web UI, CLI, API, app).
2. Identify the canonical local start command, ports, environment variables, and required seed data.
3. Determine how an agent can programmatically drive the system (browser/CDP, PTY/CLI, HTTP requests) and capture evidence (screenshots, transcripts, logs, exit codes).
4. Verify isolation requirements: identify if instances can run concurrently or need dedicated ports/profiles.
5. Create `.agents/skills/verify-<app>/SKILL.md` with explicit launch, drive, observe, and cleanup instructions.
