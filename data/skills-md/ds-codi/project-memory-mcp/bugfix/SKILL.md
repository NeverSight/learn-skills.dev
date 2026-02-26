---
name: bugfix
description: One-command automatic bug-fix orchestrator for this Project Memory MCP workspace using Revisionist → Executor → Reviewer loops plus testing.
argument-hint: <symptom-or-error> [scope]
---

# Bugfix Bot

Use this skill to run an automatic fix workflow from one command like `/bugfix "npm test fails in vscode-extension"`.

## Behavior

When invoked, run this sequence:

1. Capture bug context
   - Extract symptom, failing command, and scope from arguments
   - If missing details, infer from recent terminal/test outputs

2. Start a Project Memory plan
   - Register workspace via `memory_workspace(action: "register")`
   - Create a `bug`/`debug` plan with explicit success criteria (repro fixed + tests passing)
   - Store input context via `memory_context(action: "store_initial")`

3. Orchestrate fix loop
   - `Researcher` (optional): gather failure context and likely root causes
   - `Revisionist`: create minimal remediation steps
   - `Executor`: apply targeted fixes only
   - `Reviewer`: build-check + code review
   - `Tester`: run focused tests then broader suite as needed
   - Repeat `Revisionist → Executor → Reviewer → Tester` until pass

4. Guardrails
   - Do not broaden scope beyond failing area without explicit rationale
   - Do not silently ignore failing tests
   - Keep terminal surface contracts correct (`memory_terminal` vs `memory_terminal_interactive`)
   - Prefer registered build/test scripts when available

5. Completion criteria
   - Reproduction no longer fails
   - Relevant tests/build pass
   - Plan has no blocked active steps
   - Plan archived with fix summary and artifacts

## Output Format

Return a concise bugfix report:
- Root cause
- Fix summary
- Commands/tests run
- Final status (pass/fail)
- Any remaining risks

## Example Invocations

- `/bugfix "npx mocha out/suite/replay-harness-core.test.js fails"`
- `/bugfix "interactive-terminal cargo test fails after cxxqt refactor" interactive-terminal`
