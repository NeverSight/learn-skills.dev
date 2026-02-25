---
name: rlm-subagent
description: 'Master skill for parallel subagent-driven execution with automatic fallback to single-agent sequential mode. Use when implementing plans with multiple independent sub-phases (SP1, SP2...) to dispatch parallel subagents, or when requiring code review between implementation and testing. Trigger phrases: "parallelize", "dispatch subagent", "split into sub-phases", "code review subagent", "parallel testing".'
---

# Subagent-Driven Execution with Fallback

This skill provides parallel subagent execution for RLM Phase 3 (Implementation), Phase 3.5 (Code Review), and Phase 4 (Testing) with automatic fallback to sequential mode when subagents are unavailable.

## Trigger examples

- `Parallelize Phase 3 across independent sub-phases`
- `Dispatch an implementer subagent for each SP`
- `Run a separate code-reviewer subagent before Phase 4`
- `Subagents aren't available; fall back to sequential mode`

## Quick Reference

| Scenario | Action |
|----------|--------|
| Multiple independent sub-phases | Use **Parallel Mode** (subagents) |
| Single sub-phase or subagents unavailable | Use **Sequential Mode** (fallback) |
| Code review needed | Use **Phase 3.5** (subagent or self-review) |
| Parallel testing | Use **Phase 4** parallel dispatch |

## TODO Discipline for Subagents

**The Iron Law:** NO SUBAGENT COMPLETION REPORT WITHOUT ALL TODOS CHECKED.

### Subagent TODO Requirements

Each subagent (implementer, code-reviewer) MUST:
1. Include `## TODO` section in their work output
2. Check off items as work progresses
3. Verify ALL items checked before reporting completion

### Implementer Subagent TODO Template

```markdown
## TODO

- [ ] Read and understand assigned SP specification
- [ ] Ask clarifying questions (if any)
- [ ] Write failing test (RED phase)
- [ ] Run test and verify failure
- [ ] Implement minimal code (GREEN phase)
- [ ] Run test and verify pass
- [ ] Refactor while keeping tests green
- [ ] Run integration tests
- [ ] Self-review against plan
- [ ] Document changes made
- [ ] Report completion to controller
```

### Code Reviewer Subagent TODO Template

```markdown
## TODO

- [ ] Read original plan (Phase 3)
- [ ] Read implementation summary (Phase 3)
- [ ] Review git diff (BASE_SHA..HEAD_SHA)
- [ ] Verify plan alignment
- [ ] Assess code quality
- [ ] Check TDD compliance
- [ ] Categorize issues (Critical/Important/Minor)
- [ ] Document positive findings
- [ ] Render verdict
- [ ] Report review completion
```

### Controller TODO Management

The controller MUST:
1. Verify subagent outputs include completed TODOs
2. NOT accept completion reports with unchecked items
3. Request subagent to complete remaining items

## Capability Detection

**At start of Phase 3, detect subagent availability:**

```
IF can invoke "agent" or "Task" tool -> Use Parallel Mode
ELSE -> Use Sequential Fallback Mode
```

**Detection rule:** If the platform provides a subagent/task primitive, use parallel mode; otherwise fallback to sequential.

## Parallel Mode (Subagents Available)

### Phase 3: Parallel Sub-Phase Implementation

**Controller responsibilities:**
1. Read locked Phase 3 plan once
2. Extract all sub-phases (SP1, SP2, SP3...)
3. Determine dependencies (independent vs sequential)
4. Dispatch implementer subagent per independent SP
5. Two-stage review after each SP completion
6. Integration testing after all approved

**Dispatch pattern:**
```typescript
// Parallel dispatch for independent SPs
await Promise.all([
  Task({ description: "Implement SP1", prompt: implementerPrompt(SP1) }),
  Task({ description: "Implement SP2", prompt: implementerPrompt(SP2) }),
  Task({ description: "Implement SP3", prompt: implementerPrompt(SP3) })
])
```

**Two-stage review:**
1. **Spec Review:** Verify SP requirements met (plan alignment)
2. **Code Quality Review:** Assess code quality, TDD compliance, standards

### Phase 3.5: Code Review Subagent

**Trigger:** After Phase 3 implementation
**Action:** Dispatch `agents/code-reviewer.md` subagent with:
- BASE_SHA and HEAD_SHA of changes
- Phase 3 plan for alignment check
- Severity classification (Critical/Important/Minor)

**Review loop:** Issues found -> implementer fixes -> re-review

### Phase 4: Parallel Testing

**Dispatch pattern:**
```typescript
// Parallel test execution
await Promise.all([
  Task({ description: "Run unit tests", prompt: testPrompt("unit") }),
  Task({ description: "Run integration tests", prompt: testPrompt("integration") }),
  Task({ description: "Run E2E tests", prompt: testPrompt("e2e") })
])
```

**Result aggregation:**
- Collect results from all subagents
- Summarize pass/fail counts
- Identify any critical failures

## Sequential Fallback Mode (No Subagents)

**Trigger:** Subagent capability check fails

**Characteristics:**
- Execute sub-phases sequentially in main agent context
- Extended self-review checklist per sub-phase
- Integration testing between each sub-phase
- Full context preservation

**Fallback trigger flow:**
```markdown
**Subagent Check:** ❌ NOT AVAILABLE
**Reason:** [Tool not found / Platform limitation / User request]
**Action:** Using SEQUENTIAL fallback mode
```

### Sequential Execution Pattern

```
For each SP in [SP1, SP2, SP3...]:
  1. Execute SP implementation
  2. Self-review against plan (extended checklist)
  3. Document in Phase 4 artifact
  4. Run integration tests
  5. Proceed to next SP
```

### Sequential Review Pattern

**Phase 3.5 equivalent:**
- Main agent performs extended self-review
- Use comprehensive checklist from `agents/code-reviewer.md`
- Document findings in Phase 3.5 artifact

## Subagent Prompts

### Implementer Subagent

**File:** `agents/implementer.md`

**Key requirements:**
- Self-contained context (full SP text provided)
- TDD discipline enforcement
- Question-before-work protocol
- Self-review checklist before completion

**Usage:**
```markdown
You are an Implementer Agent. Implement this sub-phase:

**SP Text:** [full sub-phase text]
**BASE_SHA:** [commit SHA]
**Context:** [relevant files]

Follow the process in agents/implementer.md
```

### Code Reviewer Subagent

**File:** `agents/code-reviewer.md`

**Key requirements:**
- Plan alignment verification
- Code quality assessment
- Severity classification (Critical/Important/Minor)
- Clear verdict (Approved / Changes Required)

**Usage:**
```markdown
You are a Code Reviewer Agent. Review this implementation:

**Plan:** [Phase 3 TO-BE]
**Git Range:** [BASE_SHA..HEAD_SHA]
**Implementation:** [Phase 4 summary]

Follow the process in agents/code-reviewer.md
```

## Artifact Documentation

**Phase 4 artifact must include:**
```markdown
## Execution Mode
- **Mode:** Parallel / Sequential
- **Subagents Used:** [names and counts]
- **Fallback Reason:** [if applicable]

## Sub-phase Results
- SP1: [status] - [subagent name or "main agent"]
- SP2: [status] - [subagent name or "main agent"]
...

## Review Results
- SP1 Review: [status] - [reviewer name or "self-review"]
- SP2 Review: [status] - [reviewer name or "self-review"]
...
```

**Phase 3.5 artifact (if used):**
```markdown
## Review Scope
- Git range: [BASE_SHA..HEAD_SHA]
- Execution Mode: Parallel (subagent) / Sequential (self-review)
- Reviewer: [subagent name / self]

## Issues Found
- Critical: [count]
- Important: [count]
- Minor: [count]

## Verdict
[APPROVED / APPROVED WITH NOTES / CHANGES REQUIRED]
```

**Phase 4 artifact must include:**
```markdown
## Execution Mode
- **Mode:** Parallel / Sequential
- **Test Suites:**
  - Unit: [subagent name] / Main agent
  - Integration: [subagent name] / Main agent
  - E2E: [subagent name] / Main agent

## Results Summary
- Total execution time: [X] minutes
- Estimated sequential time: [Y] minutes
- Speedup: [Z]x
```

## Decision Tree

```
Starting Phase 4
        │
        ▼
Subagent available? ──NO──► SEQUENTIAL MODE
        │                   - Execute SPs sequentially
        │                   - Extended self-review
        │                   - Document as sequential
        │
       YES
        │
        ▼
3+ independent SPs? ──NO──► SEQUENTIAL MODE
        │                   - Single sub-phase
        │                   - No parallelism benefit
        │
       YES
        │
        ▼
   PARALLEL MODE
   - Dispatch implementer per SP
   - Two-stage review
   - Integration after all done
```

## Quality Maintenance

**Both modes enforce:**
- TDD discipline
- Artifact locking
- Gate compliance
- Integration testing

**Parallel Mode advantages:**
- Fresh context per sub-phase
- Independent verification
- Faster execution (3-5x)

**Sequential Mode advantages:**
- No subagent dependency
- Simpler coordination
- Full context accumulation

## Common Patterns

### Pattern 1: Multi-Domain Feature

**Scenario:** Feature touches API, UI, and database

**Phase 3 plan:**
```markdown
## Sub-phases
- SP1: API changes (backend/)
- SP2: UI changes (frontend/)
- SP3: Database migration (migrations/)
```

**Phase 4 execution:**
- SP1, SP2, SP3 dispatched in parallel (independent domains)
- Each implementer works on isolated files
- Integration testing after all complete

### Pattern 2: Sequential Dependencies

**Scenario:** SP2 depends on SP1 output

**Phase 3 execution:**
- Dispatch SP1 -> wait -> review -> approve
- Dispatch SP2 (with SP1 context) -> wait -> review -> approve
- Sequential, not parallel

### Pattern 3: High-Risk Change

**Scenario:** Critical auth system change

**Phase 3:** Implement with TDD
**Phase 3.5:** Mandatory code review
**Phase 4:** Parallel testing (unit + integration + E2E)

## Troubleshooting

### Subagent fails to complete
- Check if prompt was self-contained
- Verify BASE_SHA was provided
- Review logs for errors
- Retry with clearer instructions

### Integration tests fail after parallel SPs
- Check for file conflicts between SPs
- Verify no shared mutable state
- Review commit history for ordering issues

### Sequential mode too slow
- Consider breaking into more granular SPs
- Check if platform supports subagents
- Verify tool detection is working

## References

- Main workflow: `SKILL.md`
- Implementer subagent: `agents/implementer.md`
- Code reviewer subagent: `agents/code-reviewer.md`
- Artifact templates: `references/artifact-template.md`
