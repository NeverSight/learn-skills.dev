---
name: thinkwell
description: >-
  Write TypeScript code using the Thinkwell framework. Covers the @JSONSchema
  syntax, Plan fluent API, agent lifecycle, tools, skills, thought
  streams, and the thinkwell CLI.
---

# Thinkwell

Thinkwell is a TypeScript framework for blending deterministic code with LLM-powered reasoning. It provides a fluent `Plan` API for composing prompts, attaching tools, and getting structured JSON responses.

For detailed API signatures, see [references/api-reference.md](references/api-reference.md).
For `@JSONSchema` details, see [references/schema-guide.md](references/schema-guide.md).
For complete working examples, see [references/examples.md](references/examples.md).

## Core Concepts

### 1. The @JSONSchema Pattern

Annotate an interface with `@JSONSchema` in a JSDoc comment. Thinkwell auto-generates a `TypeName.Schema` namespace that provides the JSON schema at runtime:

```typescript
/**
 * A summary of content.
 * @JSONSchema
 */
export interface Summary {
  /** A brief title */
  title: string;
  /** Key points from the content */
  points: string[];
  /**
   * Word count of the original
   * @minimum 0
   */
  wordCount: number;
}

// Summary.Schema is auto-generated — use it with agent.think()
```

Works with interfaces, type aliases, enums, and classes. JSDoc comments on properties become descriptions in the generated schema. Annotations like `@minimum`, `@maximum`, `@minLength`, `@maxLength`, `@pattern`, and `@format` map to JSON Schema validation keywords.

### 2. Agent Lifecycle

```typescript
import { open } from "thinkwell";

const agent = await open('claude');  // Or: 'codex', 'gemini', 'kiro', 'opencode', 'auggie'
try {
  const result = await agent
    .think(Summary.Schema)           // Start builder with output schema
    .text("Summarize this:")         // Add prompt text
    .quote(content)                  // Add quoted content
    .run();                          // Execute → returns typed Summary
  console.log(result.title);
} finally {
  agent.close();                     // Always close when done
}
```

The pattern is always: **open → think → plan → run → close**.

### 3. Plan Fluent API

`agent.think(schema)` returns a `Plan`. Chain methods to compose the prompt, then call `.run()` or `.stream()`:

**Content methods:**
- `.text(content)` — Add literal text
- `.textln(content)` — Add text with trailing newline
- `.quote(content, label?)` — Add content in XML-style tags (e.g., `<feedback>...</feedback>`)
- `.code(content, language?)` — Add content as a fenced code block

**Tool methods:**
- `.tool(name, description, handler)` — Register a tool (no input schema)
- `.tool(name, description, inputSchema, handler)` — Register a tool with typed input
- `.tool(name, description, inputSchema, outputSchema, handler)` — Full form with both schemas
- `.defineTool(...)` — Same overloads, but hidden from the prompt text

**Skill methods:**
- `.skill(path)` — Attach a stored skill from a SKILL.md directory
- `.skill({ name, description, body, tools? })` — Attach a virtual skill

**Configuration:**
- `.cwd(path)` — Set the working directory for the session

**Execution:**
- `.run()` — Execute and return the typed result
- `.stream()` — Execute and return a `ThoughtStream` for streaming events + result

> **Note:** `Plan` was previously named `ThinkBuilder`. The old name still works as a deprecated alias.

### 4. Tools

Tools let the agent call back into your code. Three overloads:

**Simple tool (no input schema):**
```typescript
.tool(
  "current_time",
  "Returns the current date and time.",
  async () => ({
    time: new Date().toLocaleTimeString(),
    date: new Date().toLocaleDateString(),
    timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
  })
)
```

**Tool with typed input:**
```typescript
/** @JSONSchema */
interface SearchInput {
  /** Glob pattern to match files */
  pattern: string;
  /** Maximum results to return */
  limit?: number;
}

.tool(
  "search_files",
  "Search for files matching a glob pattern.",
  SearchInput.Schema,
  async (input) => {
    // input is typed as SearchInput
    const files = await glob(input.pattern);
    return { files: files.slice(0, input.limit ?? 10) };
  }
)
```

### 5. Thought Streaming

Use `.stream()` instead of `.run()` to get real-time events:

```typescript
const stream = agent
  .think(Schema)
  .text("Analyze this codebase")
  .stream();

for await (const event of stream) {
  switch (event.type) {
    case "thought":    // Agent's internal reasoning
      process.stderr.write(event.text);
      break;
    case "message":    // Agent's visible response
      process.stdout.write(event.text);
      break;
    case "tool_start": // Tool invocation started
      console.log(`Using tool: ${event.title}`);
      break;
    case "tool_done":  // Tool completed
      break;
    case "plan":       // Agent's execution plan
      for (const entry of event.entries) {
        console.log(`[${entry.status}] ${entry.content}`);
      }
      break;
  }
}

const result = await stream.result;  // Final typed result
```

The stream and result promise are independent — you can iterate events, await the result, or both.

### 6. Sessions (Multi-Turn)

For conversations where the agent needs to remember context across calls:

```typescript
const session = await agent.createSession({ cwd: "/my/project" });

const analysis = await session
  .think(AnalysisSchema)
  .text("Analyze this codebase")
  .run();

// Same session — agent remembers the analysis
const fixes = await session
  .think(FixesSchema)
  .text("Suggest fixes for the top issues")
  .run();

session.close();
```

Each `agent.think()` creates an ephemeral session. Use `agent.createSession()` when you need multi-turn context.

### 7. Skills

Attach reusable instruction packages to a prompt:

**Stored skill (from filesystem):**
```typescript
.skill("./skills/code-review")
```

**Virtual skill (programmatic):**
```typescript
.skill({
  name: "test-writer",
  description: "Generates unit tests for TypeScript functions.",
  body: `
# Test Writer

## Steps
1. Analyze function signatures
2. Generate test cases covering edge cases
3. Use the \`count-assertions\` tool to verify coverage

## Available Tools

### count-assertions
Count assertions in a test file.
Input: \`{ "path": "string" }\`
  `,
  tools: [{
    name: "count-assertions",
    description: "Count assertions in a test file",
    handler: async ({ path }) => {
      const content = await fs.readFile(path, "utf-8");
      const matches = content.match(/expect\(/g) || [];
      return { count: matches.length };
    },
  }],
})
```

### 8. schemaOf() Helper

For schemas without `@JSONSchema` (e.g., inline or dynamic schemas):

```typescript
import { schemaOf } from "thinkwell";

const result = await agent
  .think(schemaOf<{ answer: string }>({
    type: "object",
    properties: { answer: { type: "string" } },
    required: ["answer"]
  }))
  .text("What is 2 + 2?")
  .run();
```

## CLI Usage

### Running Scripts

```bash
# Run a script directly
thinkwell script.ts

# Or use a shebang
#!/usr/bin/env thinkwell
```

Scripts use standard npm imports (`import { open } from "thinkwell"`).

### IDE Support

Generate declaration files for `TypeName.Schema` autocomplete:

```bash
thinkwell types          # One-time generation
thinkwell types --watch  # Watch mode for development
```

Add `*.thinkwell.d.ts` to your tsconfig's `include` array and `.gitignore`.

Alternatively, install the Thinkwell VSCode extension for automatic IDE support without generating files.

### Type Checking

```bash
thinkwell check          # Type-check the project (supports @JSONSchema)
```

## Recommended Method Chain Order

```typescript
const result = await agent
  .think(OutputSchema)               // 1. Schema (always first) → returns Plan
  .cwd("/my/project")                // 2. Configuration
  .skill("./skills/code-review")     // 3. Skills
  .text("Analyze this code:")        // 4. Prompt content
  .code(sourceCode, "typescript")
  .tool("helper", "...", handler)    // 5. Tools
  .run();                            // 6. Execute (always last)
```

## Common Patterns

### Prompt-Only (No Tools)

```typescript
const summary = await agent
  .think(Summary.Schema)
  .text("Summarize the following content:")
  .quote(content)
  .run();
```

### Tool + Streaming

```typescript
const stream = agent
  .think(Greeting.Schema)
  .text("Create a time-appropriate greeting")
  .tool("current_time", "Get current time", async () => new Date())
  .stream();

for await (const event of stream) {
  if (event.type === 'message') process.stdout.write(event.text);
}
const greeting = await stream.result;
```

### Custom Agent Command

```typescript
const agent = await open({ cmd: 'my-custom-agent --acp' });
```

### Environment Variable Override

```bash
# Override the agent for all scripts
THINKWELL_AGENT=gemini thinkwell script.ts

# Override with a custom command
THINKWELL_AGENT_CMD="my-agent --acp" thinkwell script.ts
```
