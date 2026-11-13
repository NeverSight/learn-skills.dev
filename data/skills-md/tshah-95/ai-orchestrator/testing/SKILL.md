---
name: testing
description: |
  Test and verify AI orchestrator features using CLI runner, unit tests, and E2E tests.
  ALWAYS use this skill when: implementing new features, fixing bugs, making changes to agents/orchestrator/TUI,
  or when asked to verify something works. Claude MUST test changes before marking tasks complete.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# AI Orchestrator Testing

## Core Principle

**Never ship untested code.** Before marking ANY task as complete, you MUST:
1. Run relevant unit tests
2. Use the CLI test runner to verify the feature works end-to-end
3. Add or update tests to cover new functionality
4. Ensure all tests pass

## Testing Infrastructure

### 1. CLI Test Runner (Primary Tool for Verification)

The CLI lets you send messages and see responses WITHOUT the interactive TUI:

```bash
# Basic usage - send a message and see the response
npm run cli -- "Create a PRD for user authentication"

# With verbose output (shows status messages)
npm run cli -- --verbose "Create a PRD for auth"

# JSON output (for programmatic verification)
npm run cli -- --json "Test message"

# Custom timeout (default is 120 seconds)
npm run cli -- --timeout 60000 "Quick test"
```

**Use this to verify:**
- Intent classification works correctly
- Agents receive and process tasks
- Responses contain expected content
- The full message flow works end-to-end

### 2. Unit Tests (Vitest)

```bash
# Run all unit tests
npm test

# Watch mode during development
npm run test:watch

# With coverage report
npm run test:coverage
```

**Test locations:**
- `packages/shared/src/__tests__/` - Type helpers, event creators
- `packages/orchestrator/src/__tests__/` - Router, classification
- `packages/agents/src/__tests__/` - Agent logic

### 3. E2E Integration Tests

```bash
# Run E2E tests (auto-manages backend lifecycle)
npm run test:e2e
```

**Location:** `packages/e2e/src/__tests__/`

These tests start the backend, send real messages through queues, and verify responses.

## Testing Workflow

### When Implementing a New Feature

1. **Before coding:** Understand what tests exist
   ```bash
   npm test  # See current test status
   ```

2. **During development:** Use CLI to verify changes
   ```bash
   npm run cli -- --verbose "Test the new feature"
   ```

3. **After implementation:** Add tests
   - Unit tests for new helper functions
   - Integration tests for new message flows
   - Update existing tests if behavior changed

4. **Before completing:** Run full test suite
   ```bash
   npm test && npm run cli -- "Verify feature works"
   ```

### When Fixing a Bug

1. **First:** Write a failing test that reproduces the bug
2. **Then:** Fix the bug
3. **Verify:** Test passes and CLI shows correct behavior
4. **Finally:** Ensure no regressions with `npm test`

### When Refactoring

1. **Before:** Run `npm test` to establish baseline
2. **After each change:** Run tests to catch regressions
3. **Use CLI:** Verify behavior hasn't changed

## Test Requirements by Area

### Shared Package (`packages/shared/`)
- All helper functions MUST have unit tests
- All type creators MUST have unit tests
- Test file: `src/__tests__/types.test.ts`, `src/__tests__/events.test.ts`

### Orchestrator (`packages/orchestrator/`)
- Intent classification MUST be tested
- Routing logic MUST be tested
- Add tests for new intent types

### Agents (`packages/agents/`)
- Agent response formatting MUST be tested
- Error handling MUST be tested

### TUI (`packages/tui/`)
- Use CLI runner for integration testing
- Component logic can have unit tests

## Quality Gates

Before marking a task complete, verify:

- [ ] `npm test` passes (all unit tests)
- [ ] CLI verification shows expected behavior
- [ ] New code has corresponding tests
- [ ] No test regressions (existing tests still pass)
- [ ] Edge cases are covered

## Example: Verifying a Change

Say you modified the intent classification. Here's how to verify:

```bash
# 1. Run unit tests
npm test

# 2. Test classification via CLI
npm run cli -- --verbose "Create a PRD for authentication"
# Should show: [Status] Understanding your request...
# Should route to: product-manager

# 3. Test edge case
npm run cli -- --verbose "random gibberish text"
# Should show error response about not understanding

# 4. If you added new intent type, add test:
# packages/orchestrator/src/__tests__/router.test.ts
```

## Adding New Tests

### Unit Test Template
```typescript
import { describe, it, expect } from 'vitest';

describe('MyFeature', () => {
  it('does something correctly', () => {
    const result = myFunction('input');
    expect(result).toBe('expected');
  });

  it('handles edge cases', () => {
    expect(() => myFunction(null)).toThrow();
  });
});
```

### E2E Test Template
```typescript
import { describe, it, expect } from 'vitest';
import { sendTestMessage } from '@ai-orchestrator/test-utils';

describe('E2E: MyFeature', () => {
  it('works end-to-end', async () => {
    const response = await sendTestMessage('Test my feature', {
      timeout: 60000,
      verbose: true,
    });

    expect(response.status).toBe('complete');
    expect(response.parts[0].content).toContain('expected text');
  });
});
```

## Remember

1. **Test early, test often** - Don't wait until the end
2. **CLI is your friend** - Use it liberally to verify changes
3. **Tests are documentation** - They show how features should work
4. **Regressions are bugs** - If a test breaks, fix it before continuing
5. **Coverage matters** - New features need new tests

## Additional References

- [TEST-UTILS.md](TEST-UTILS.md) - Detailed API reference for test utilities
- [QUALITY-CONTRACT.md](QUALITY-CONTRACT.md) - Definition of done and quality gates
