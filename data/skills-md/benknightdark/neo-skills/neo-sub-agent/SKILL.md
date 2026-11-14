---
name: neo-sub-agent
description: >
  Use this skill when the user asks to design, create, review, or convert sub-agents,
  custom agents, worker/reviewer/planner agents, background agents, or multi-agent
  workflows for Antigravity CLI, Codex, Claude Code, GitHub Copilot CLI, or neutral
  agent blueprints.
---

# Neo Sub-Agent

Use this skill to design and generate focused sub-agent definitions for developer CLIs. Keep the user in control of scope, permissions, and target clients.

## Core Rule
Do not invent client-specific schema. If the requested CLI, field, or file location is not documented in `references/client-adapters.md` or discoverable in the project, state the missing fact and generate only a neutral blueprint.

## Workflow

### 1. Perceive
1. Inspect the project before asking questions:
   - Existing agent definitions: `.claude/agents/`, `.codex/agents/`, `.github/agents/`, `.agents/skills/`.
   - Project guidance: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`.
   - Related skills or conventions in `skills/`, `.agents/skills/`, `.github/skills/`, `.claude/skills/`, `.codex/skills/`.
2. Identify the target clients from the user request or project evidence: `claude`, `codex`, `copilot`, `agy`, or multiple.
3. If multiple clients are plausible and the request does not specify one, ask one concise question before writing files.

### 2. Decide Whether a Sub-Agent Fits
Read `references/sub-agent-design.md` when the request involves architecture, multiple agents, or tradeoffs.

Use a sub-agent when at least one is true:
- The work produces verbose logs, search results, or file reads that should not pollute the main context.
- The work is a repeated specialist role such as code review, planning, test execution, research, migration analysis, or docs verification.
- The work can run independently or in a clearly bounded sequence.
- The role needs stricter tool access, sandboxing, model choice, or output contract than the main agent.

Prefer a normal skill or main-conversation instruction when:
- The task is a quick, targeted change.
- The agent needs frequent back-and-forth with the user.
- Multiple workers would edit the same files concurrently.
- The workflow depends on undocumented client behavior.

### 3. Define the Agent Spec
Collect or infer these fields, using safe defaults where reasonable:
- `name`: lowercase kebab-case, under 64 characters.
- `description`: trigger-focused; state exactly when to use the agent.
- `instructions`: role, workflow, constraints, and output contract.
- `clients`: target clients.
- `scope`: `project` by default; use `user` only when the user asks for reusable personal agents.
- `tools`: use the smallest useful set; prefer read-only for reviewers, researchers, planners, and auditors.
- `model` and reasoning effort: omit unless the user asks or the client-specific reference gives a clear default.
- `handoff`: what the parent agent should pass in and what the sub-agent must return.
- `validation`: commands, checks, or review criteria the sub-agent should run or report.

### 4. Generate Files
Read `references/client-adapters.md` before generating client-specific files.

For repeatable output, create a JSON spec and run:

```bash
uv run skills/neo-sub-agent/scripts/render-sub-agent.py --spec spec.json
```

If `uv` is not available and the script has no external dependencies, use:

```bash
python skills/neo-sub-agent/scripts/render-sub-agent.py --spec spec.json
```

Review the dry-run JSON. If the target paths and content are correct, write files:

```bash
uv run skills/neo-sub-agent/scripts/render-sub-agent.py --spec spec.json --write
```

Use `--force` only when replacing an existing agent file is explicitly intended.

### 5. Review
Before finalizing, check:
- The agent has one narrow job and does not duplicate an existing agent.
- The description is specific enough for automatic delegation.
- Tool permissions match the role and avoid broad write/shell access when unnecessary.
- The output contract is short, concrete, and easy for the parent agent to synthesize.
- Antigravity output is labeled as a skill/delegation blueprint, not a custom sub-agent manifest.

## Output Format
When reporting back to the user, use Traditional Chinese (Taiwan):

```markdown
## 已新增
- [client] `path/to/agent-file`

## 設計重點
- 角色：
- 觸發條件：
- 權限：
- 回傳格式：

## 驗證
- `command`
```

## Constraints
- Do not create broad "do everything" agents.
- Do not give background agents write or shell access unless the task requires it.
- Do not create multiple agents that can edit the same file set in parallel.
- Do not treat model-generated review as a replacement for deterministic tests.
