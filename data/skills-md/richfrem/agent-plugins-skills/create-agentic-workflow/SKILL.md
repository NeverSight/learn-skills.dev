---
name: create-agentic-workflow
description: Scaffold GitHub Agent files from an existing Agent Skill. Generates IDE/UI agents (invokable from GitHub Copilot Chat via slash command) and/or CI/CD autonomous agents (GitHub Actions quality gates with Kill Switch). Use when converting a Skill into a GitHub-native agent.
allowed-tools: Bash, Read, Write
---
# GitHub Agent Scaffolder

You are tasked with generating **GitHub Agent** files from an existing Agent Skill. There are two distinct GitHub agent types — understand both before asking the user which they need.

## Understanding the Two GitHub Agent Types

| | Type 1: IDE / UI Agent | Type 2: CI/CD — Smart Failure | Type 3: CI/CD — Official Format |
|---|---|---|---|
| **Triggered by** | Human via Copilot Chat | GitHub Actions event | GitHub Actions event |
| **Files generated** | `.agent.md` + `.prompt.md` | `.agent.md` + `.yml` runner | `.md` (intent) + `.lock.yml` (compiled) |
| **Failure signal** | N/A | Kill Switch phrase + grep | Native `safe-outputs` guardrails |
| **Coding engines** | Any Copilot model | Copilot CLI | Copilot CLI, Claude Code, Codex |
| **Compile step?** | No | No | Yes — `gh aw compile` |
| **Status** | GA | Works today | Technical preview (Feb 2026) |

## Execution Steps

### 1. Gather Requirements

Ask the user for the following context before proceeding:

1. **Target Skill**: Path to the Agent Skill directory to convert (e.g., `plugins/my-plugin/skills/my-skill`).

2. **Agent Type**: Ask which type(s) they need:
   - **IDE Agent** — appears in the Copilot Chat agent picker and is invokable via a `/slug` slash command from VS Code or GitHub.com
   - **CI/CD Smart Failure** — runs autonomously on PR/push/schedule and can fail the build via a Kill Switch phrase (works today in any repo)
   - **CI/CD Official** — uses the official GitHub Agentic Workflow format (`.md` + compiled `.lock.yml` with `safe-outputs`). Requires `gh aw compile`. Technical preview Feb 2026.
   - **Both** — IDE Agent + one of the CI/CD formats (user chooses which)

3. **Trigger Events** *(only if CI/CD or Both)*: Which GitHub events should fire this workflow? `workflow_dispatch` (manual) is always included. Pick any additional triggers:
   | Trigger | When it fires | Best for |
   |---|---|---|
   | `pull_request` | On PR open/update | Spec alignment, code quality gates |
   | `push` | On push to main | Post-merge doc sync, changelog checks |
   | `schedule` | On cron schedule | Daily health reports, issue triage |
   | `issues` | On issue creation | Auto-labeling, routing |
   | `release` | On release publish | Release readiness validation |

### 2. Scaffold the Agent Files

Run the deterministic `scaffold_agentic_workflow.py` script with the correct `--mode` flag:

```bash
# IDE agent only (Copilot Chat slash command)
python ./scaffold_agentic_workflow.py \
  --skill-dir <requested-skill-path> \
  --mode ide

# CI/CD Smart Failure agent (Kill Switch pattern — works today)
python ./scripts/scaffold_agentic_workflow.py \
  --skill-dir <path-to-skill-directory> \
  --mode cicd \
  [--triggers pull_request push schedule issues release] \
  [--kill-switch "CUSTOM FAILURE PHRASE"]

# CI/CD Official GitHub Agentic Workflow (technical preview — Feb 2026)
python ./scaffold_agentic_workflow.py \
  --skill-dir <requested-skill-path> \
  --mode cicd \
  --format official \
  [--triggers pull_request push schedule]

# Both IDE + CI/CD (shared persona)
python ./scaffold_agentic_workflow.py \
  --skill-dir <requested-skill-path> \
  --mode both \
  [--triggers pull_request push]
```

**Mode flags:**
- `--mode ide` → generates `.github/skills/name.agent.md` + `.github/prompts/name.prompt.md`
- `--mode cicd` → generates `.github/skills/name.agent.md` + `.github/workflows/name-agent.yml` (or `.md` + `.lock.yml` for official format)
- `--mode both` → generates all files

**Format flags** *(cicd/both only)*:
- `--format smart-failure` *(default)* → Kill Switch grep pattern; works in any repo today
- `--format official` → Official GitHub Agentic Workflow `.md` + `.lock.yml`; requires `gh aw compile` and technical preview access

**Optional flags:**
- `--triggers [pull_request] [push] [schedule] [issues] [release]` → *(cicd/both only)* events that fire the workflow in addition to `workflow_dispatch`. Map to the table in step 1.3.
- `--kill-switch "PHRASE"` → *(cicd/both only)* custom kill switch phrase (default: `CRITICAL FAILURE: SKILL_NAME`)

The script will parse the skill's YAML frontmatter, extract its name and description, and generate compliant files in the repository root's `.github/` folder.

### 3. Post-Scaffold Notes

After generation, remind the user:

- **IDE agents**: The `.agent.md` body is a starting skeleton. For rich workflows (like multi-agent orchestrators), the full instruction set from the source SKILL.md should be manually ported into the `.agent.md` body, and `handoffs:` frontmatter added for chaining to other agents.

- **CI/CD Smart Failure agents**: The `.github/workflows/*.yml` requires a `COPILOT_GITHUB_TOKEN` secret in the repository settings. The Kill Switch phrase must appear verbatim in the `.agent.md` body instructions for the quality gate to work. Furthermore, you MUST explicitly define an **Escalation Trigger Taxonomy** in the `.agent.md` so the agent knows precisely when to halt and trigger the Kill Switch vs when to auto-approve.

- **CI/CD Official format agents**: After generation, run `gh aw compile` to generate the `.lock.yml` file. Commit **both** the `.md` and the `.lock.yml`. Requires the `gh-aw` extension: `gh extension install github/gh-aw`. Technical preview — may require preview access.

- **Both**: The shared `.agent.md` must satisfy both use cases — include the full instruction set AND (if Smart Failure) the Kill Switch phrase.


## Next Actions
- Offer to run `create-github-action` to add CI/CD hooks.
- Offer to run `audit-plugin` to validate YAML syntax.
