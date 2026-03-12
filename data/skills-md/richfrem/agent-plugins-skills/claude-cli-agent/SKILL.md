---
name: claude-cli-agent
description: >
  Claude CLI sub-agent system for persona-based analysis. Use when piping
  large contexts to Anthropic models for security audits, architecture reviews,
  QA analysis, or any specialized analysis requiring a fresh model context.
allowed-tools: Bash, Read, Write
dependencies: ["skill:dual-loop"]
---
## Ecosystem Role: Inner Loop Specialist

This skill provides specialized **Inner Loop Execution** for the [`dual-loop`](../../../agent-loops/skills/dual-loop/SKILL.md).

- **Orchestrated by**: [`agent-orchestrator`](../../agent-orchestrator/skills/orchestrator-agent/SKILL.md)
- **Use Case**: When "generic coding" is insufficient and specialized expertise (Security, QA, Architecture) is required.
- **Why**: The CLI context is naturally isolated (no git, no tools), making it the perfect "Safe Inner Loop".

## Identity: The Sub-Agent Dispatcher 🎭

You, the Antigravity agent, dispatch specialized analysis tasks to Claude CLI sub-agents.

## 🛠️ Core Pattern
```bash
cat <PERSONA_PROMPT> | claude -p "<INSTRUCTION>" < <INPUT> > <OUTPUT>
```

## ⚠️ CLI Best Practices

### 1. Token Efficiency — PIPE, Don't Load
**Bad** — loads file into agent memory just to pass it:
```python
content = read_file("large.log")
run_command(f"claude -p 'Analyze: {content}'")
```
**Good** — direct shell piping:
```bash
claude -p "Analyze this log" < large.log > analysis.md
```

### 2. Self-Contained Prompts
The CLI runs in a **separate context** — no access to agent tools or memory.
- **Add**: "Do NOT use tools. Do NOT search filesystem."
- Ensure prompt + piped input contain 100% of necessary context

### 3. File Size & Permission Limitations
- The `claude` CLI will block reading massive files (e.g. 5MB+) natively via pipe or `--file` flag. If conducting whole-repository analysis, you MUST build a python script to semantically chunk or scan rather than trying to stuff the whole system into a single bash pipe.
- Always run automated scripts containing `claude` with `--dangerously-skip-permissions` if you are passing complex generated files, otherwise the CLI will hang waiting for User UI approval.
- Ensure the operating environment has an active session (`claude login`) before dispatching autonomous CLI commands, or it will fail silently in the background.

### 4. Output to File
Always redirect output to a file (`> output.md`), then review with `view_file`.

### 5. Severity-Stratified Constraints
When dispatching code-review, architecture, or security analysis, explicitly instruct the CLI sub-agent to use the **Severity-Stratified Output Schema**. This ensures the Outer Loop can parse the results deterministically:
> "Format all findings using the strict Severity taxonomy: 🔴 CRITICAL, 🟡 MODERATE, 🟢 MINOR."

## 🎭 Persona Categories

| Category | Personas | Use For |
|:---|:---|:---|
| Security | security-auditor | Red team, vulnerability scanning |
| Development | 14 personas | Backend, frontend, React, Python, Go, etc. |
| Quality | architect-review, code-reviewer, qa-expert, test-automator, debugger | Design validation, test planning |
| Data/AI | 8 personas | ML, data engineering, DB optimization |
| Infrastructure | 5 personas | Cloud, CI/CD, incident response |
| Business | product-manager | Product strategy |
| Specialization | api-documenter, documentation-expert | Technical writing |

All personas in: `plugins/personas/`

## 🔄 Recommended Audit Loop
1. **Red Team** (Security Auditor) → find exploits
2. **Architect** → validate design didn't add complexity
3. **QA Expert** → find untested edge cases

Run architect **AFTER** red team to catch security-fix side effects.
