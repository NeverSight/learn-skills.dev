---
name: testing-flow
description: Runs and authors behavioral tests for Robomotion flows using @robomotion/sdk/testing. Use when the user says "test the flow", "write tests for main.ts", "mock this service", "check branch coverage", or when a flow needs regression tests before a change. For pspec schema validation, use validating-flow instead.
---

# Testing a Robomotion Flow

Run behavioral tests for a Robomotion flow. Uses `@robomotion/sdk/testing` + `bun test`.

**For pspec schema validation, use `validating-flow`.**

## Purpose

- Execute `*.test.ts` files with `bun test`
- Author new tests with FlowTester, MockRegistry, SubflowTester
- Inspect structure, mock services, trace execution, exercise Function-node logic

## Workflow

1. **Check for tests** — `ls path/to/flow/*.test.ts`
2. **Run** — `cd path/to/flow && bun test`
3. **Fix failures** — diagnose, edit, re-run

## Quick Start

Create `main.test.ts` next to `main.ts`:

```typescript
import { describe, test, expect, beforeAll, afterAll } from 'bun:test';
import { FlowTester, MockRegistry } from '@robomotion/sdk/testing';

describe('My Flow', () => {
  let tester: FlowTester;

  beforeAll(async () => {
    tester = await FlowTester.load('./main.ts');
  });

  afterAll(() => {
    MockRegistry.clear();
  });

  test('validates', () => {
    expect(tester.validate().valid).toBe(true);
  });

  test('has expected node count', () => {
    expect(tester.getNodes().length).toBe(10);
  });
});
```

## API Map

Load only the reference file(s) you need. Each is self-contained and lives inside this skill under `./reference/`.

| Area | What's in it | Reference |
|------|--------------|-----------|
| Load/inspect flows, run checkpoints, analyze paths and complexity | `FlowTester`, `analyzeFlow`, `findPaths`, `generateDotGraph` | `./reference/flow-tester.md` |
| Mock external services (per-node, per-type, helpers, call tracking) | `MockRegistry`, `mockResponse/Error/Sequence/Conditional` | `./reference/mock-registry.md` |
| Test Function-node JavaScript in isolation | `extractFunc`, `runFunc`, `testFunctionWithCases`, `analyzeFunctionNode` | `./reference/function-extraction.md` |
| Run subflows in isolation; discover them in a flow | `SubflowTester`, `discoverSubflows`, `loadAllSubflows` | `./reference/subflow-tester.md` |
| Unit vs real-service mode via env vars | `isIntegrationMode`, `hasCredentials`, `createTestHelper` | `./reference/integration-mode.md` |

## Complete Example

```typescript
import { describe, test, expect, beforeAll, afterAll, afterEach } from 'bun:test';
import {
  FlowTester, MockRegistry, extractFunc,
  isIntegrationMode, hasCredentials, analyzeFlow,
} from '@robomotion/sdk/testing';

describe('Reddit to WordPress Flow', () => {
  let tester: FlowTester;

  beforeAll(async () => { tester = await FlowTester.load('./main.ts'); });
  afterEach(() => MockRegistry.resetCalls());
  afterAll(() => MockRegistry.clear());

  describe('Structure', () => {
    test('validates', () => expect(tester.validate().valid).toBe(true));
    test('all branches terminate', () => expect(tester.allBranchesTerminate()).toBe(true));
    test('loops have Goto->Label', () => {
      expect(tester.findLoops().every(l => l.hasGotoLabel)).toBe(true);
    });
    test('no dead ends', () => {
      expect(analyzeFlow(tester).deadEnds).toHaveLength(0);
    });
  });

  describe('Transform Logic', () => {
    test('formats Reddit post', () => {
      const transform = extractFunc(tester, '2bf967');
      const out = transform({ post: { title: 'Test', selftext: 'Body', subreddit: 'programming' } });
      expect(out.wpTitle).toContain('Test');
    });
  });

  describe('With Mocked Services', () => {
    beforeAll(() => {
      MockRegistry.registerNode('c8f412', async () => ({
        posts: [{ title: 'Mock 1', selftext: 'c1', score: 100 }],
      }));
      MockRegistry.register('Core.Net.HttpRequest', async (p, m, nodeId) => {
        console.warn(`Unmocked HTTP in ${nodeId}`);
        return { statusCode: 200, body: {} };
      });
    });

    test('fetches posts', async () => {
      const res = await tester.runUntil('c5d901', {
        input: { subreddit: 'programming', limit: 10 },
      });
      expect(res.msg.posts).toHaveLength(1);
      expect(MockRegistry.getCallCount('c8f412')).toBe(1);
    });
  });

  describe('Integration', () => {
    test('real WordPress posting', async () => {
      if (!isIntegrationMode() || !hasCredentials('wordpress')) return;
      const res = await tester.runWithTrace({
        input: { subreddit: 'programming', postLimit: 1 },
        useRealServices: true,
      });
      expect(res.output.publishedUrl).toBeDefined();
    });
  });
});
```

## Tips

- Use node-ID mocks for precise control; type mocks as catch-all.
- Verify mock inputs with `getLastCall()`.
- Clear mocks in `afterAll()` to avoid pollution across files.
- `INTEGRATION=1 bun test` switches to real services.

## Related Skills

- `validating-flow` — schema validation (property names, ports, node types)
- `creating-flow` — generate TypeScript
- `running-flow` — execute on a robot
