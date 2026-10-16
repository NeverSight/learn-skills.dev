---
name: distilly
description: "Set up the owner profile so a personal agent knows who it works for (first-run setup, \"get to know me\"), or distill colleague, relationship, or celebrity source material into reusable Person Profiles for agents."
argument-hint: "[character] [name-or-slug]"
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> **Language**: These instructions are written in English. Detect the user's language from their first message and reply to the user in that language throughout.

> **Skill Root**: Before reading a bundled prompt or running a bundled script, resolve the absolute directory of the `SKILL.md` that the host actually loaded. In the instructions below, `{distilly_skill_root}` means that exact directory. Claude Code exposes it as `${CLAUDE_SKILL_DIR}`; on every other host, use the loaded-skill path supplied by that host's discovery context. Do not assume the shell's current working directory is the Skill root, and do not guess or hard-code an install path. If the host does not expose the loaded path or more than one Distilly installation is ambiguous, ask the user to identify the active installation before running code.
>
> Keep the shell in the user's current workspace so relative output paths such as `./skills/...` remain project-local. Resolve every `tools/...` and `prompts/...` resource against `{distilly_skill_root}`. For example, run `tools/owner_profile.py` as `python3 "{distilly_skill_root}/tools/owner_profile.py"`; replace the placeholder with the resolved absolute path in the actual tool call.

# Distilly Creator

> Distilly was formerly **Colleague Skill / colleague-skill**. The current Skill frontmatter name and creator entrypoint are both `distilly`.

## Route the request

Read only the flow file the request needs, then follow it.

| The user says | Flow |
|---------------|------|
| "Set up my profile" / "Get to know me" / "Who am I to you", "distill myself", or a host's first run with no owner profile yet | `prompts/flows/owner.md` |
| `/distilly`, "Help me create a skill", "Create a new skill", "I want to distill someone", "Make a skill for XX" | `prompts/flows/create.md` (its Step 0 sends `owner` back to the owner flow) |
| "I have new files" / "append", "That's wrong" / "He wouldn't do that" / "He should be", `/update-skill {character} {slug}`, or the alias `/update-colleague {slug}` | `prompts/flows/evolve.md` |
| "Show my skills", roll back or delete a generated skill | `prompts/flows/manage.md` |

The create flow pulls in `prompts/flows/sources.md` for importing material and, for `celebrity`, `prompts/flows/celebrity_research.md`. Each flow names the prompts it needs; read those when the flow gets there, not up front.

## Rules for every flow

- **Storage**: generated skills live under `./skills/colleague/{slug}/`, `./skills/relationship/{slug}/` or `./skills/celebrity/{slug}/` in the user's workspace. For a global path, pass `--base-dir` with that family's storage root.
- **Writes**: create and update generated skills only through `tools/skill_writer.py`; never hand-build or hand-edit their files.
- **Credentials**: App Secrets, access or refresh tokens, Bot Tokens and OAuth codes never enter the conversation. Never ask for them; the user runs a collector's `--setup` / `--login` in their own terminal. `prompts/flows/sources.md` has the details.

## Compatible hosts

Claude Code, OpenClaw, Hermes, Codex, DeepSeek Harness, Pi coding agent, Grok Build and OpenCode. Invoke with `/distilly` in Claude Code, Hermes, DeepSeek Harness and Grok Build; `/distilly` or `/skill distilly` in OpenClaw; `$distilly` or `/skills` in Codex; `/skill:distilly` in Pi. OpenCode loads Skills natively and has no dedicated command. Grok Bot cannot import this directory directly; do not present this repository as a Grok Bot install.
