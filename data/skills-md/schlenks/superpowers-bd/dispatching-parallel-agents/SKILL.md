---
name: dispatching-parallel-agents
description: Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies
---

# Dispatching Parallel Agents

## When to Use

**Use when:**
- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from others
- No shared state between investigations

**Don't use when:**
- Failures are related (fix one might fix others)
- Need to understand full system state
- Agents would interfere with each other (editing same files, using same resources)
- Exploratory debugging (you don't know what's broken yet)

## The Pattern

### 1. Identify Independent Domains
Group failures by what's broken (e.g., File A: tool approval flow, File B: batch completion, File C: abort functionality). Each domain is independent -- fixing one doesn't affect the others.

### 2. Create Focused Agent Tasks
Each agent gets: specific scope (one test file/subsystem), clear goal (make these tests pass), constraints (don't change other code), expected output (summary of findings and fixes).

### 3. Dispatch in Parallel
```typescript
Task("Fix agent-tool-abort.test.ts failures")
Task("Fix batch-completion-behavior.test.ts failures")
Task("Fix tool-approval-race-conditions.test.ts failures")
// All three run concurrently
```

### 4. Review and Integrate
Read each summary, verify fixes don't conflict, run full test suite, integrate all changes.

## Agent Prompt Structure

Three rules for good agent prompts:
1. **Focused** -- one clear problem domain
2. **Self-contained** -- all context needed to understand the problem
3. **Specific about output** -- what should the agent return?

**Example:**
```markdown
Fix the 3 failing tests in src/agents/agent-tool-abort.test.ts:
1. "should abort tool with partial output capture" - expects 'interrupted at'
2. "should handle mixed completed and aborted tools" - fast tool aborted
3. "should properly track pendingToolCount" - expects 3 results, gets 0

These are timing/race condition issues. Replace arbitrary timeouts with
event-based waiting. Do NOT just increase timeouts.
Return: Summary of root cause and changes made.
```

See `references/agent-prompt-example.md` for full annotated version.

## Common Mistakes

- **Too broad** ("Fix all the tests") -> **Be specific** ("Fix agent-tool-abort.test.ts")
- **No context** ("Fix the race condition") -> **Paste error messages and test names**
- **No constraints** (agent refactors everything) -> **Scope explicitly** ("Fix tests only")
- **Vague output** ("Fix it") -> **Request summary** ("Return root cause and changes")

## Verification

After agents return:
1. Review each summary -- understand what changed
2. Check for conflicts -- did agents edit same code?
3. Run full suite -- verify all fixes work together
4. Spot check -- agents can make systematic errors

## Reference Files

- `references/agent-prompt-example.md`: full annotated prompt example with test names and constraints
- `references/real-session-example.md`: complete scenario: dispatch, results, integration, time saved
- `references/real-world-impact.md`: stats from debugging session (2025-10-03)

<!-- compressed: 2026-02-11, original: 643 words, compressed: 461 words -->
