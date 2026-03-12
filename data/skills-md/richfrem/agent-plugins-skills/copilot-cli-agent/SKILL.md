---
name: copilot-cli-agent
description: >
  Copilot CLI sub-agent system for persona-based analysis. Use when piping
  large contexts to GitHub Copilot models for security audits, architecture reviews,
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

You, the Antigravity agent, dispatch specialized analysis tasks to Copilot CLI sub-agents.

## 🛠️ Core Pattern
```bash
cat <PERSONA_PROMPT> | copilot -p "<INSTRUCTION>" <INPUT> > <OUTPUT>
```
*Note: Copilot uses `-p` or `--prompt` for non-interactive scripting runs.*

## ⚠️ CLI Best Practices

### 1. Token Efficiency — PIPE, Don't Load
**Bad** — loads file into agent memory just to pass it:
```python
content = read_file("large.log")
run_command(f"copilot -p 'Analyze: {content}'")
```
**Good** — direct shell piping:
```bash
copilot -p "Analyze this log" < large.log > analysis.md
```

### 2. Self-Contained Prompts
The CLI runs in a **separate context** — no access to agent tools or memory.
- **Add**: "Do NOT use tools. Do NOT search filesystem."
- Ensure prompt + piped input contain 100% of necessary context.
- **Security Check**: Copilot CLI has explicit permission flags (e.g. `--allow-all-tools`, `--allow-all-paths`). For isolated sub-agents, do **not** provide these flags to ensure safe headless execution.

### 3. Output to File
Always redirect output to a file (`> output.md`), then review with `view_file`.

### 4. Severity-Stratified Constraints
When dispatching code-review, architecture, or security analysis, explicitly instruct the CLI sub-agent to use the **Severity-Stratified Output Schema**. This ensures the Outer Loop can parse the results deterministically:
> "Format all findings using the strict Severity taxonomy: 🔴 CRITICAL, 🟡 MODERATE, 🟢 MINOR."

## ✅ Smoke Test (Copilot CLI)

Use this minimal command to verify the CLI is callable and returns output:

```bash
copilot -p "Reply with exactly: COPILOT_CLI_OK"
```

Expected result:
- CLI prints `COPILOT_CLI_OK` (or very close equivalent) and exits successfully.

If the test fails:
- Confirm `copilot` is on `PATH`.
- Ensure you are authenticated in the Copilot CLI session.
- Retry without any permission flags; keep the test minimal and isolated.
- **Model Support Warning**: If you specify a model (e.g., `--model gpt-5.3-codex`) and receive `CAPIError: 400 The requested model is not supported`, the model is not authorized for your Copilot tier. Run without the `--model` flag to use the default router instead.

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
