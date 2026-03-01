---
name: oh-my-codex
keyword: omx
description: Multi-agent orchestration layer for OpenAI Codex CLI. Provides 30 specialized agents, 40+ workflow skills, team orchestration in tmux, persistent MCP servers, and staged pipeline execution.
allowed-tools: [Read, Write, Bash, Grep, Glob]
tags: [omx, multi-agent, orchestration, codex, openai, team-mode, mcp-servers, workflow]
platforms: [Codex, Claude, Gemini]
version: 0.4.1
source: Yeachan-Heo/oh-my-codex
---

# oh-my-codex (OMX) - Multi-Agent Orchestration for Codex CLI

## When to use this skill

- Orchestrating complex multi-agent workflows with OpenAI Codex CLI
- Running parallel team workers in tmux for coordinated task execution
- Using persistent MCP servers for state, memory, and code intelligence
- Executing staged pipelines (plan → prd → exec → verify → fix)
- Leveraging role-based agent prompts for specialized tasks

---

## 1. Core Concepts

### Role Prompts (30 Agents)
| Agent Tier | Agents | Use Case |
|------------|--------|----------|
| **Core Development** | architect, planner, executor, debugger, verifier, explore | Main development workflow |
| **Quality Assurance** | style-reviewer, quality-reviewer, api-reviewer, security-reviewer, performance-reviewer | Code review lane |
| **Domain Experts** | dependency-expert, test-engineer, build-fixer, designer, writer, qa-tester | Specialized tasks |
| **Product Strategy** | product-manager, ux-researcher, product-analyst, information-architect | Product planning |

### Workflow Skills (40+)
| Skill | Trigger | Description |
|-------|---------|-------------|
| `autopilot` | `$autopilot` | Full autonomous execution from idea to working code |
| `ralph` | `$ralph` | Self-referential loop with verifier verification until completion |
| `ultrawork` | `$ulw` | Maximum parallelism with parallel agent orchestration |
| `team` | `$team` | N coordinated agents using Codex CLI native teams |
| `plan` | `$plan` | Strategic planning with consensus and review modes |
| `research` | `$research` | Parallel scientist agents for comprehensive research |
| `tdd` | `$tdd` | Test-first development with red-green-refactor cycle |
| `build-fix` | `$build-fix` | Fix build errors, type errors, and toolchain failures |
| `code-review` | `$code-review` | Comprehensive code review across all quality dimensions |
| `security-review` | `$security-review` | Security audit focusing on vulnerabilities and trust boundaries |
| `cancel` | `$cancel` | Stop execution modes and clear active state |

### MCP Servers
| Server | Purpose |
|--------|---------|
| `omx_state` | Persistent mode lifecycle state |
| `omx_memory` | Memory + notepad surfaces for long-running sessions |
| `omx_code_intel` | Code intelligence and context |
| `omx_trace` | Execution tracing and debugging |

---

## 2. Installation & Setup

### Prerequisites
- macOS or Linux (Windows via WSL2)
- Node.js >= 20
- Codex CLI installed (`npm install -g @openai/codex`)
- Codex auth configured

### Install oh-my-codex
```bash
npm install -g oh-my-codex
omx setup
omx doctor
```

### Recommended Launch Profile
```bash
# Trusted environment with high reasoning
omx --xhigh --madmax
```

---

## 3. Usage Patterns

### Role Prompts (Inside Codex)
```text
/prompts:architect "analyze current auth boundaries"
/prompts:executor "implement input validation in login"
/prompts:security-reviewer "audit OAuth flow"
```

### Workflow Skills
```text
$plan "ship OAuth callback safely"
$autopilot "implement user registration"
$team 3:executor "fix all TypeScript errors"
```

### Team Mode (Terminal)
```bash
# Start parallel team workers
omx team 4:executor "parallelize a multi-module refactor"

# Monitor team status
omx team status <team-name>

# Resume team work
omx team resume <team-name>

# Shutdown team
omx team shutdown <team-name>
```

---

## 4. Launch Flags

| Flag | Description |
|------|-------------|
| `--yolo` | Fast execution, minimal verification |
| `--high` | High reasoning effort |
| `--xhigh` | Extra-high reasoning effort |
| `--madmax` | Maps to Codex `--dangerously-bypass-approvals-and-sandbox` |
| `--force` | Force operation |
| `--dry-run` | Preview without execution |
| `--verbose` | Verbose output |

---

## 5. Staged Pipeline

OMX implements a structured execution pipeline:

```
team-plan → team-prd → team-exec → team-verify → team-fix
```

1. **Plan**: Strategic decomposition of work
2. **PRD**: Product requirements definition
3. **Exec**: Parallel execution by team workers
4. **Verify**: Validation of deliverables
5. **Fix**: Automated error resolution

---

## 6. Hook Extensions (v0.4.0+)

### Native Lifecycle Events
- `session-start` / `session-end` / `session-idle`
- `turn-complete`

### Plugin Workflow
```bash
# Enable hook plugins
OMX_HOOK_PLUGINS=1 omx hooks test

# Hook commands
omx hooks init     # Initialize hooks
omx hooks status   # Check hook status
omx hooks validate # Validate configuration
omx hooks test     # Test hook execution
```

Plugin files: `.omx/hooks/*.mjs`

---

## 7. Configuration

### AGENTS.md Injection
By default, OMX injects project-level AGENTS.md:
```bash
-c model_instructions_file="<cwd>/AGENTS.md"
```

### Environment Controls
```bash
# Disable AGENTS.md injection
OMX_BYPASS_DEFAULT_SYSTEM_PROMPT=0 omx

# Custom instructions file
OMX_MODEL_INSTRUCTIONS_FILE=/path/to/instructions.md omx
```

---

## Quick Reference

| Command | Action |
|---------|--------|
| `omx` | Launch Codex with HUD |
| `omx setup` | Install prompts, skills, config wiring |
| `omx doctor` | Installation/runtime diagnostics |
| `omx doctor --team` | Team/swarm diagnostics |
| `omx team <n>:<role> "<task>"` | Start team workers |
| `omx team status <name>` | Show team status |
| `omx team shutdown <name>` | Shutdown team |
| `omx status` | Show active modes |
| `omx cancel` | Cancel execution modes |
| `omx reasoning <mode>` | Set reasoning (low/medium/high/xhigh) |
| `omx hud` | HUD display options |
| `omx help` | Show help |

---

## Resources

- **Website**: https://yeachan-heo.github.io/oh-my-codex-website/
- **GitHub**: https://github.com/Yeachan-Heo/oh-my-codex
- **npm**: https://www.npmjs.com/package/oh-my-codex

---

## License

MIT License
