---
name: multi-agent-skill
description: |
  Multi-agent workflow engineering skill. Use when designing, building, reviewing, or debugging
  multi-agent systems. Covers typed schemas, action schemas, MCP contracts, orchestration patterns,
  failure modes, and testing strategies. Framework-agnostic TypeScript/Zod patterns that work with
  any multi-agent implementation (Claude Code, LangChain, CrewAI, custom).
license: MIT
compatibility: "Requires TypeScript 5+ and Zod 3+ for schema templates."
metadata:
  version: "1.0.0"
  last_verified: "2026-02-26"
  source: "https://github.blog/ai-and-ml/generative-ai/multi-agent-workflows-often-fail-heres-how-to-engineer-ones-that-dont/"
---

# Multi-Agent Workflow Engineering Skill

## Table of Contents
- [Quick Start](#quick-start)
- [Core Principle](#core-principle)
- [The Three Patterns](#the-three-patterns)
- [Design Principles](#design-principles)
- [Decision Framework](#decision-framework)
- [Failure Modes](#failure-modes)
- [Anti-Patterns](#anti-patterns)
- [Bundled Resources](#bundled-resources)

---

## Quick Start

Three patterns form the foundation of reliable multi-agent systems. Each uses TypeScript and Zod to enforce contracts at agent boundaries.

### 1. Typed Schema - Validate Agent Handoff Data

```typescript
import { z } from "zod";

const AgentHandoff = z.object({
  sourceAgent: z.string(),
  targetAgent: z.string(),
  timestamp: z.string().datetime(),
  payload: z.object({
    taskId: z.string().uuid(),
    status: z.enum(["pending", "in_progress", "completed", "failed"]),
    data: z.record(z.unknown()),
  }),
  metadata: z.object({
    correlationId: z.string().uuid(),
    retryCount: z.number().int().min(0).default(0),
    schemaVersion: z.literal("1.0"),
  }),
});

type AgentHandoff = z.infer<typeof AgentHandoff>;

// Validate on send
const validated = AgentHandoff.parse(outgoingData);

// Validate on receive
const received = AgentHandoff.parse(incomingData);
```

### 2. Action Schema - Constrain Agent Behavior

```typescript
import { z } from "zod";

const AgentAction = z.discriminatedUnion("type", [
  z.object({
    type: z.literal("delegate"),
    targetAgent: z.string(),
    task: z.string(),
    deadline: z.string().datetime().optional(),
  }),
  z.object({
    type: z.literal("respond"),
    content: z.string(),
    confidence: z.number().min(0).max(1),
  }),
  z.object({
    type: z.literal("escalate"),
    reason: z.string(),
    severity: z.enum(["low", "medium", "high", "critical"]),
  }),
  z.object({
    type: z.literal("retry"),
    originalAction: z.string(),
    backoffMs: z.number().int().positive(),
  }),
]);

type AgentAction = z.infer<typeof AgentAction>;

// Exhaustive matching ensures no action is missed
function handleAction(action: AgentAction): void {
  switch (action.type) {
    case "delegate":
      return routeToAgent(action.targetAgent, action.task);
    case "respond":
      return sendResponse(action.content);
    case "escalate":
      return notifyHuman(action.reason, action.severity);
    case "retry":
      return scheduleRetry(action.originalAction, action.backoffMs);
  }
}
```

### 3. MCP Contract - Define Tool Interfaces

```typescript
import { z } from "zod";

const SearchToolInput = z.object({
  query: z.string().min(1).max(500),
  filters: z.object({
    dateRange: z.object({
      from: z.string().datetime(),
      to: z.string().datetime(),
    }).optional(),
    maxResults: z.number().int().min(1).max(100).default(10),
  }).optional(),
});

const SearchToolOutput = z.object({
  results: z.array(z.object({
    id: z.string(),
    title: z.string(),
    relevance: z.number().min(0).max(1),
    snippet: z.string(),
  })),
  totalCount: z.number().int().min(0),
  executionMs: z.number().int().min(0),
});

const searchTool = {
  name: "search_documents",
  description: "Search documents with structured filters and validated results.",
  inputSchema: SearchToolInput,
  outputSchema: SearchToolOutput,
  handler: async (input: z.infer<typeof SearchToolInput>) => {
    const validated = SearchToolInput.parse(input);
    const results = await performSearch(validated);
    return SearchToolOutput.parse(results);
  },
};
```

---

## Core Principle

> **Treat agents like distributed systems, not chat flows.**

Most multi-agent failures stem from treating agents as cooperative conversation partners that naturally understand each other. In reality, agents are unreliable network services. This mental model shift changes everything about how you design multi-agent systems.

**Chat flow thinking** assumes agents share context, understand intent implicitly, pass data freely, and recover gracefully from errors. This works in demos but fails in production.

**Distributed systems thinking** assumes agents have no shared context, intent must be explicit in every message, data must be validated at every boundary, and failures are inevitable and must be handled. This is what makes multi-agent systems reliable.

The practical implications:

- **Explicit contracts**: Every agent boundary has a typed schema. No agent trusts data from another agent without validation.
- **Validation at boundaries**: Data is validated on send AND on receive. Schema mismatches surface immediately as errors, not as subtle downstream bugs.
- **Failure handling**: Every agent interaction has a timeout, a retry strategy, and an escalation path. No "happy path only" designs.
- **Observability**: Every message carries a correlation ID. Every state transition is logged. When something fails at 3 AM, you can trace exactly what happened.

---

## The Three Patterns

### Pattern 1: Typed Schemas

**Problem**: Agents pass unstructured data between each other. A planning agent emits a JSON blob, a coding agent consumes it, and somewhere in between a field name changes or a type shifts from string to number. The system doesn't crash -- it silently produces wrong results.

**Solution**: Define Zod schemas at every agent boundary. Validate data when sending and when receiving.

**Key rules**:
1. **Validate on send AND receive** - The sender validates it produced correct output. The receiver validates it got correct input. Both sides check.
2. **Version your schemas** - Include a `schemaVersion` field. When schemas evolve, old and new agents can coexist during rollout.
3. **No `any` types** - Every field has an explicit type. `z.unknown()` is acceptable only inside `z.record()` for truly dynamic data, and even then the consumer must narrow the type before use.
4. **Fail loudly** - Use `.parse()` not `.safeParse()` at boundaries. A schema violation should throw, not return a success-with-undefined.

```typescript
const TaskResult = z.object({
  taskId: z.string().uuid(),
  agentId: z.string(),
  schemaVersion: z.literal("1.0"),
  result: z.discriminatedUnion("status", [
    z.object({ status: z.literal("success"), output: z.string() }),
    z.object({ status: z.literal("failure"), error: z.string(), retryable: z.boolean() }),
  ]),
});
```

### Pattern 2: Action Schemas

**Problem**: Agents take ambiguous actions. An agent decides to "process" something, but what does "process" mean? Does it transform data, delegate to another agent, store a result, or call an external API? Ambiguity leads to unpredictable behavior and debugging nightmares.

**Solution**: Define a discriminated union type that enumerates every possible action an agent can take. Each action variant has its own typed payload.

**Key rules**:
1. **Exhaustive matching** - Use TypeScript's `never` type or a switch statement to ensure every action variant is handled. If you add a new action, the compiler tells you everywhere it needs handling.
2. **Explicit intent** - The action `type` field is a literal string that describes exactly what the agent intends. No ambiguous verbs like "process" or "handle".
3. **No implicit actions** - If an agent can do it, it must be in the union. Side effects that happen outside the action schema are bugs.
4. **Typed payloads** - Each action variant carries only the data it needs. A "delegate" action has a target agent and task. A "respond" action has content and confidence. No shared bag-of-properties.

```typescript
const WorkflowAction = z.discriminatedUnion("type", [
  z.object({ type: z.literal("fetch_data"), source: z.string().url(), timeout: z.number() }),
  z.object({ type: z.literal("transform"), inputKey: z.string(), outputKey: z.string() }),
  z.object({ type: z.literal("store_result"), key: z.string(), value: z.unknown() }),
  z.object({ type: z.literal("notify"), channel: z.string(), message: z.string() }),
]);
```

### Pattern 3: MCP Contracts

**Problem**: Tool interfaces drift over time. An MCP tool changes its expected input format, but the agents calling it still send the old format. Or a tool starts returning additional fields that downstream agents don't expect. Integration breaks silently.

**Solution**: Define MCP tool contracts with Zod schemas for both input and output. Validate before execution (reject bad requests early) and after execution (ensure the tool produced what it promised).

**Key rules**:
1. **Pre-execution validation** - Validate input before calling the tool handler. Return a structured error if validation fails. Don't let bad data reach the implementation.
2. **Typed responses** - The tool output schema is not optional. Every tool declares what it returns, and the output is validated before being sent back to the calling agent.
3. **Contract tests** - Write tests that verify the tool's schema contract independently of its implementation. If the schema changes, the test fails before any agent integration breaks.
4. **Versioned endpoints** - When a tool's contract changes, bump the version and support both old and new versions during migration.

```typescript
function createMcpTool<I extends z.ZodType, O extends z.ZodType>(config: {
  name: string;
  description: string;
  inputSchema: I;
  outputSchema: O;
  handler: (input: z.infer<I>) => Promise<z.infer<O>>;
}) {
  return {
    ...config,
    execute: async (rawInput: unknown) => {
      const input = config.inputSchema.parse(rawInput);
      const result = await config.handler(input);
      return config.outputSchema.parse(result);
    },
  };
}
```

---

## Design Principles

Six principles derived from engineering reliable multi-agent systems in production:

### 1. Design for Failure First

Before writing the happy path, answer: What happens when this agent times out? What happens when it returns garbage? What happens when it's unavailable for 30 seconds? Design the failure path first, then build the success path on top of it.

### 2. Validate Every Agent Boundary

Every time data crosses from one agent to another, validate it with a schema. This applies to agent-to-agent handoffs, agent-to-tool calls, tool-to-agent responses, and external API interactions. No boundary is too trivial to validate.

### 3. Constrain Actions Before Adding Complexity

Start with the smallest possible action schema. An agent that can only `respond` or `escalate` is easier to reason about than one that can `respond`, `delegate`, `transform`, `store`, `notify`, and `retry`. Add actions only when you have a concrete need and a test for each one.

### 4. Log Intermediate State

Every agent should log its input, its decision, and its output as structured data with a correlation ID. When a 5-agent pipeline produces a wrong result, you need to trace the exact point where correct data became incorrect. Logging only the final output is not enough.

### 5. Make Agent Intent Explicit

An agent should never "just do something". Every action it takes must be represented in its action schema with a clear type literal. If you're debugging and an agent took an action that isn't in its schema, you have a design bug, not a runtime bug.

### 6. Test Contracts, Not Just Outputs

Don't only test that the system produces the right final output. Test that each agent's input and output conform to their schemas. Test that action schemas are handled exhaustively. Test that MCP tool contracts are stable. Contract tests catch integration bugs before they reach production.

---

## Decision Framework

### When to Use Single Agent vs Multi-Agent

Score each dimension from 1 (single agent) to 5 (multi-agent). Sum the scores to guide your decision.

| Dimension | Single Agent (1-2) | Multi-Agent (3-5) |
|-----------|-------------------|-------------------|
| **Task decomposability** | Monolithic, sequential steps that share heavy context | Naturally parallel subtasks with clear boundaries |
| **Skill specialization** | One domain of expertise (e.g., only code generation) | Multiple distinct domains (code, review, testing, deploy) |
| **State complexity** | Simple shared state that fits in one context window | Complex, partitioned state across different concerns |
| **Failure isolation** | Acceptable blast radius -- one failure means start over | Need independent failure domains -- one agent failing shouldn't block others |
| **Scaling requirements** | Fixed throughput is sufficient | Variable, elastic needs -- some subtasks need more compute |

**Scoring guide**:
- **5-12**: Use a single agent. The overhead of multi-agent coordination will slow you down without meaningful benefit.
- **13-18**: Consider multi-agent. Evaluate whether the coordination cost is justified by the gains in specialization and isolation.
- **19-25**: Use multi-agent. The task naturally decomposes, the domains are distinct, and you need failure isolation.

**Important**: A multi-agent system is not inherently better than a single agent. It is inherently more complex. Only add agents when the complexity buys you something concrete -- better failure isolation, independent scaling, or domain specialization that a single agent cannot achieve.

---

## Failure Modes

The six most common failure modes in multi-agent systems, with prevention strategies.

### 1. Schema Drift

**What happens**: Agent A's output schema and Agent B's input schema diverge over time. A field gets renamed, a type changes, or an optional field becomes required. Neither agent fails -- they just silently produce wrong results.

**Prevention**: Shared schema definitions imported by both agents. Schema version fields that trigger explicit errors on mismatch. Contract tests that run on every build.

### 2. Action Ambiguity

**What happens**: Two agents interpret the same action type differently. Agent A thinks "process" means "transform data". Agent B thinks "process" means "store result". The system appears to work until edge cases reveal the divergence.

**Prevention**: Literal string type discriminators (`z.literal("transform")` not `z.string()`). One canonical action schema shared across all agents. Exhaustive switch statements that the compiler verifies.

### 3. State Corruption

**What happens**: Multiple agents modify shared state concurrently. Agent A reads state, Agent B modifies it, Agent A writes its changes based on stale data. The result is a state that neither agent intended.

**Prevention**: Immutable state with event sourcing. Each agent produces events, a single reducer applies them in order. Optimistic concurrency with version fields. No direct state mutation.

### 4. Cascade Failure

**What happens**: Agent A depends on Agent B, which depends on Agent C. Agent C fails. Agent B retries, creating load. Agent A times out waiting for B. The entire pipeline collapses because one leaf agent had a transient error.

**Prevention**: Circuit breakers at every agent boundary. Timeouts with escalation (don't just retry -- escalate to a human or fallback after N retries). Bulkhead isolation so one failing path doesn't consume all resources.

### 5. Ordering Violation

**What happens**: The system assumes agents execute in a specific order, but under load or during retries, the order changes. Agent B processes before Agent A has finished, working with incomplete data.

**Prevention**: Explicit dependency declarations in the orchestrator. Agents declare their prerequisites. The orchestrator enforces ordering. No implicit ordering assumptions in agent logic.

### 6. Silent Data Loss

**What happens**: An agent receives data that doesn't match its expected schema, silently drops the unrecognized fields, and continues processing. The dropped fields were critical for a downstream agent.

**Prevention**: Strict schema validation with `.parse()` (not `.safeParse()` with silent fallbacks). Schema rules like `.strict()` that reject unexpected fields. Logging of every validation error with the full payload for debugging.

---

## Anti-Patterns

| Anti-Pattern | DON'T | DO |
|---|---|---|
| **God Agent** | One agent does everything -- plans, executes, reviews, deploys | Decompose by responsibility. Each agent has one clear domain. |
| **Implicit Contract** | Agents assume data shapes based on convention or past behavior | Explicit Zod schemas at every boundary. Import shared schema definitions. |
| **Fire and Forget** | Send a message to another agent and assume it was processed | Validate receipt and processing. Use acknowledgment schemas. Implement timeouts. |
| **Shared Mutable State** | Global mutable objects that multiple agents read and write | Immutable state with event sourcing. Each agent emits events, a reducer applies them. |
| **Retry Storm** | Unlimited retries with no backoff when an agent fails | Circuit breaker pattern. Exponential backoff with jitter. Max retry count with escalation. |
| **Log Nothing** | No intermediate logging -- only log the final result | Correlation IDs on every message. Structured logs at every agent boundary. Trace the full request path. |

---

## Bundled Resources

### References (12 files)
| # | File | Topic |
|---|------|-------|
| 01 | [foundations](references/01-foundations.md) | Why multi-agent fails |
| 02 | [typed-schemas](references/02-typed-schemas.md) | Typed schema deep-dive |
| 03 | [action-schemas](references/03-action-schemas.md) | Action schema deep-dive |
| 04 | [mcp-contracts](references/04-mcp-contracts.md) | MCP contract enforcement |
| 05 | [orchestration-patterns](references/05-orchestration-patterns.md) | Sequential, parallel, supervisor |
| 06 | [state-management](references/06-state-management.md) | Immutable state, event sourcing |
| 07 | [failure-modes-catalog](references/07-failure-modes-catalog.md) | Comprehensive failure catalog |
| 08 | [retry-escalation](references/08-retry-escalation.md) | Retry strategies, circuit breakers |
| 09 | [observability-logging](references/09-observability-logging.md) | Logging, tracing, correlation IDs |
| 10 | [testing-multi-agent](references/10-testing-multi-agent.md) | Testing strategies |
| 11 | [single-vs-multi-decision](references/11-single-vs-multi-decision.md) | Scoring rubric (5 dimensions) |
| 12 | [anti-patterns](references/12-anti-patterns.md) | God Agent, Implicit Contract, etc. |

### Templates (14 files)
| Category | File | Purpose |
|----------|------|---------|
| schemas | [typed-data-schema.ts](templates/schemas/typed-data-schema.ts) | Typed handoff schema with versioning |
| schemas | [action-schema.ts](templates/schemas/action-schema.ts) | Discriminated union action types |
| schemas | [agent-state-schema.ts](templates/schemas/agent-state-schema.ts) | Immutable agent state definition |
| schemas | [event-envelope.ts](templates/schemas/event-envelope.ts) | Event envelope with correlation IDs |
| mcp | [mcp-tool-definition.ts](templates/mcp/mcp-tool-definition.ts) | MCP tool with input/output validation |
| mcp | [mcp-server-scaffold.ts](templates/mcp/mcp-server-scaffold.ts) | MCP server boilerplate |
| mcp | [mcp-validation-middleware.ts](templates/mcp/mcp-validation-middleware.ts) | Validation middleware for MCP tools |
| orchestration | [sequential-pipeline.ts](templates/orchestration/sequential-pipeline.ts) | Sequential agent pipeline |
| orchestration | [fan-out-fan-in.ts](templates/orchestration/fan-out-fan-in.ts) | Parallel fan-out with aggregation |
| orchestration | [supervisor-worker.ts](templates/orchestration/supervisor-worker.ts) | Supervisor-worker delegation |
| orchestration | [retry-with-escalation.ts](templates/orchestration/retry-with-escalation.ts) | Retry with circuit breaker and escalation |
| testing | [schema-contract-test.ts](templates/testing/schema-contract-test.ts) | Schema contract validation tests |
| testing | [agent-boundary-test.ts](templates/testing/agent-boundary-test.ts) | Agent boundary integration tests |
| testing | [mcp-tool-contract-test.ts](templates/testing/mcp-tool-contract-test.ts) | MCP tool contract tests |

### Specialized Agents (5)
| Agent | Specialty |
|-------|-----------|
| [workflow-architect](agents/workflow-architect.md) | Design multi-agent topologies and orchestration strategies |
| [schema-engineer](agents/schema-engineer.md) | Create and evolve typed schemas and action schemas |
| [contract-reviewer](agents/contract-reviewer.md) | Review agent boundaries for contract violations |
| [failure-analyst](agents/failure-analyst.md) | Diagnose failure modes and design prevention strategies |
| [orchestration-optimizer](agents/orchestration-optimizer.md) | Optimize orchestration patterns for reliability and performance |

### Slash Commands (6)
| Command | Purpose |
|---------|---------|
| `/design-workflow` | Design a multi-agent workflow from requirements |
| `/review-agents` | Review existing agents for contract and reliability issues |
| `/generate-schemas` | Generate typed schemas for agent boundaries |
| `/generate-mcp-tool` | Scaffold an MCP tool with validated input/output |
| `/failure-analysis` | Analyze a multi-agent system for failure modes |
| `/single-vs-multi` | Run the 5-dimension scoring framework |

### Quick References
- **Source Blog Post**: https://github.blog/ai-and-ml/generative-ai/multi-agent-workflows-often-fail-heres-how-to-engineer-ones-that-dont/
- **Zod Documentation**: https://zod.dev/
- **MCP Specification**: https://modelcontextprotocol.io/
- **TypeScript Handbook**: https://www.typescriptlang.org/docs/
