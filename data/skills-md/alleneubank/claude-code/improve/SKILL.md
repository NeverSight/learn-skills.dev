---
name: improve
description: Use after completing a task, before claiming done, before handoff, or when asked "what are some improvements?" Surfaces concrete suggestions grounded in session observations.
---

# Improve

Structured improvement pass grounded in what was observed during this session.

## Principles (Always Active)

- Every suggestion must cite a specific observation — file path, error seen, pattern noticed, or behavior verified. "I saw X" beats "common practice suggests Y."
- Distinguish grounded suggestions (observed evidence) from speculative ones (general knowledge). Mark speculative suggestions explicitly.
- Prioritize by impact to the user, not by ease of description.
- Do not suggest improvements that would change public API contracts, auth boundaries, or data schemas without flagging as high-risk.
- Simplicity is a feature. Do not suggest adding complexity unless it prevents a concrete problem observed in this session.

## When to Use

- User asks "knowing what you know now, what are some improvements?" or similar
- Before claiming done in a ralph loop (self-check)
- Before generating a handoff
- After completing a significant chunk of work
- When reviewing code that was just written or modified

## When Not to Use

- At the start of a session before meaningful work has been done
- When the user explicitly asks to skip review and ship
- For architectural redesigns (use spec/plan flow instead)

## Dimensions

Analyze across these dimensions. Skip any dimension with nothing grounded to say.

### Correctness
Error handling gaps, unhandled edge cases, type safety issues, race conditions, missing validation at system boundaries.

### Simplicity
Unnecessary indirection, dead code, naming that obscures intent, over-engineered abstractions, complexity that doesn't earn its keep. Reference the `simplify` skill for implementation.

### Security
Auth boundary gaps, input validation holes, secret handling issues, OWASP concerns observed in touched code.

### Test Coverage
Untested code paths observed during the session, missing test layers (unit/integration/e2e), fixture realism gaps, assertions that don't verify meaningful behavior.

### Performance
Bottlenecks observed during the session (slow queries, N+1 patterns, unnecessary recomputation). Only flag what was actually observed, not hypothetical.

### Developer Experience
API ergonomics issues, missing documentation for non-obvious behavior, CLI friction, configuration that should be extracted.

## Workflow

1. **Gather context**: Review what happened this session — files changed, commands run, errors encountered, tests written, patterns established.

2. **Analyze each dimension**: For each, check whether session observations surface anything concrete. Skip dimensions with nothing to say.

3. **Structure each suggestion**:

```
[IMP-N] effort/gate: summary
  Observation: what was seen (file:line, error message, test gap, etc.)
  Suggestion: concrete change
  Grounded: yes/no
```

Where:
- `effort`: `trivial` (< 5 min) | `small` (< 30 min) | `medium` (hours)
- `gate`: which delivery gate this strengthens: `TDD` | `DEV` | `E2E` | `REVIEW` | `CI`

4. **Sort by impact** (highest first), not by dimension.

5. **Present as actionable list**. If in a ralph loop, address trivial/small improvements inline before claiming done. Log medium improvements as decisions for the user to prioritize.

## Integration with Ralph Loops

When running inside a ralph loop (`.rl/state.json` exists):

- Run the improvement pass before `.rl/rl done`
- Address `trivial` improvements inline — just fix them
- Address `small` improvements if they're within the current milestone scope
- Log `medium` improvements: `.rl/rl log decision "IMP-N deferred: [reason]"`
- Do not expand scope beyond the task's milestones for medium improvements

## Integration with Handoffs

When generating a handoff, include unaddressed improvements in the `<next_steps>` section. Use the same `[IMP-N]` format so the receiving agent can reference them.

## Output Format

```markdown
## Improvements

N suggestions (X grounded, Y speculative)

[IMP-1] trivial/DEV: Extract magic number to config constant
  Observation: `src/server.ts:42` uses hardcoded port 3000, but other services read from env
  Suggestion: Read from `PORT` env var with 3000 as default
  Grounded: yes

[IMP-2] small/TDD: Add boundary test for empty input
  Observation: `processItems([])` path untested — saw it handle non-empty arrays only in test suite
  Suggestion: Add test case for empty array input in `process-items.test.ts`
  Grounded: yes

[IMP-3] medium/E2E: Add timeout handling for external API calls
  Observation: Catalog search took 1.2s avg in profiling — no timeout configured
  Suggestion: Add configurable timeout with bounded retry
  Grounded: yes
```

## Red Flags

- Suggestions without observations — if you can't point to something specific, don't suggest it
- More than 10 suggestions — focus on the top 5-7 by impact
- Suggestions that expand scope beyond what was touched — stay within the blast radius of the current work
- Generic "add more tests" without specifying which paths are untested
