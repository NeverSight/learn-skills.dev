---
name: codebolt-agent-development
description: Build AI agents for the Codebolt platform using @codebolt/agent. When creating an agent, first decide what type you need — (1) CodeboltAgent wrapper for simple prompt-based agents with no custom loop, (2) Base Components for customizing the agentic loop, or (3) Core API for full advanced control. Also covers Remix Agents (no-code), ActionBlocks, tools, workflows, and processors. Permissions are handled by the application, not by the agent.
---

# Codebolt Agent Development

> **SDK Version 2** - This documentation covers Codebolt SDK v2.

> **⚠️ IMPORTANT: Do NOT use `codebolt.waitForConnection()`**
>
> In SDK v2, `waitForConnection()` has been removed. Connection handling is now automatically managed inside `codebolt.onMessage()`. If you're migrating from v1 or see old examples using `waitForConnection()`, simply remove those calls.
>
> ```typescript
> // ❌ OLD (SDK v1) - Do NOT use
> await codebolt.waitForConnection();
> codebolt.onMessage(async (msg:FlatUserMessage) => { ... });
>
> // ✅ NEW (SDK v2) - Use this
> codebolt.onMessage(async (msg:FlatUserMessage) => { ... });
> ```

> **⚠️ IMPORTANT: Use Strict Typings & Always Check for Errors**
>
> Always use strict TypeScript typings when developing agents. **You do NOT need to create custom typings** — types for most Codebolt functionality are already provided by the packages (`@codebolt/codeboltjs`, `@codebolt/agent`, `@codebolt/types`). Just use the existing types.
>
> After writing any agent code, **always run type checking and linting to catch errors before running the agent**.
>
> ```bash
> # Always run after writing code
> npx tsc --noEmit    # Check for type errors
> npx eslint src/     # Check for code quality issues
> ```

## First Decision: What Type of Agent Do You Need?

When creating an agent, **the first thing you need to decide is what type of agent you want.** There are three main types, each giving you progressively more control:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    CHOOSE YOUR AGENT TYPE                            │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Don't need a full agentic loop? Just want a simple prompt agent?    │
│  ──► CodeboltAgent Wrapper (Level 3)                                 │
│      Just provide instructions — the framework handles everything.   │
│                                                                      │
│  Need to modify or customize the agentic loop?                       │
│  ──► Base Components (Level 2)                                       │
│      Compose InitialPromptGenerator + AgentStep + ResponseExecutor.  │
│      Add custom modifiers and processors at each stage.              │
│                                                                      │
│  Want to go deeper and build advanced behavior from scratch?         │
│  ──► Core API (Level 1)                                              │
│      Use codebolt.llm, codebolt.fs, codebolt.mcp directly.          │
│      Full control over every aspect of the agent.                    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

| Type | When to Use | What You Control | Code Needed |
|------|-------------|------------------|-------------|
| **CodeboltAgent Wrapper** | Simple agents, standard behavior, quick setup | Just the instructions and allowed tools | Minimal (~10 lines) |
| **Base Components** | Custom processors, specialized message handling, modified loop | The entire pipeline: modifiers, processors, loop logic | Moderate (~50 lines) |
| **Core API** | Non-standard flows, advanced orchestration, utility scripts | Everything from scratch | Full implementation |

### Important: Permissions Are Handled by the Application

**Agents do NOT need to implement permission logic.** The Codebolt application handles all permissions automatically:

- **Tool execution permissions**: When a tool is executed via `codebolt.mcp.executeTool()`, the application intercepts and can prompt the user for approval. Tools return `[didUserReject, result]` — if rejected, the agent gracefully skips remaining tools.
- **Tool whitelisting**: Agents declare `allowedTools` in config. The `ToolInjectionModifier` filters the tool list before sending to the LLM — only allowed tools are visible.
- **File system access**: All file operations go through the application layer which enforces workspace boundaries.
- **User rejection propagation**: If a user rejects a tool call, the agent automatically stops executing subsequent tools in that batch.

```typescript
// You do NOT write permission code in your agent:
// ❌ if (hasPermission('writeFile')) { ... }

// Just call tools normally. The application handles approval:
// ✅ const result = await codebolt.mcp.executeTool('codebolt', 'writeFile', { path, content });
// The application prompts the user if needed and returns [didUserReject, result]
```

**What the application handles for you:**
- User approval/rejection dialogs for tool execution
- Workspace boundary enforcement
- Tool availability filtering based on agent configuration
- Graceful handling when users deny operations
- Session-level permission state management

---

## Detailed Examples: All Three Agent Types

### Type 1 — CodeboltAgent Wrapper (Simple Prompt-Based)

If you **don't need a full custom agentic loop** and just want to run an agent using a simple prompt, use the `CodeboltAgent` wrapper. You provide instructions, optionally restrict tools, and call `processMessage()`. The framework handles the entire loop — prompt generation, LLM calls, tool execution, and completion detection.

```typescript
import codebolt from '@codebolt/codeboltjs';
import { CodeboltAgent } from '@codebolt/agent/unified';
import { FlatUserMessage } from '@codebolt/types/sdk';

// 1. Define your instructions
const systemPrompt = `
You are a helpful coding assistant. You help users with:
- Reading and understanding code
- Writing new code and fixing bugs
- Running terminal commands

Always explain what you're doing before taking action.
`;

// 2. Create the agent — that's it!
const agent = new CodeboltAgent({
  instructions: systemPrompt,
  enableLogging: true,
  // Optional: restrict which tools the agent can use
  allowedTools: [
    'codebolt--readFile',
    'codebolt--writeFile',
    'codebolt--executeCommand',
    'codebolt--listFiles',
    'codebolt--searchFiles'
  ]
});

// 3. Listen for messages and process them
codebolt.onMessage(async (reqMessage: FlatUserMessage) => {
  try {
    const result = await agent.processMessage(reqMessage);
    if (!result.success) {
      codebolt.chat.sendMessage(`Error: ${result.error}`, {});
    }
  } catch (error) {
    console.error('Agent error:', error);
  }
});
```

**What happens internally:**
- Default modifiers inject chat history, environment context, directory structure, IDE context, system prompt, tools, and @file mentions
- The LLM is called in a loop — if it returns tool calls, they're executed and results fed back
- The loop continues until the LLM calls `attempt_completion` or returns without tool calls

**Continuing from previous context:**

```typescript
const result1 = await agent.processMessage('Read the package.json file');

// Pass previous context to continue the conversation
const agent2 = new CodeboltAgent({
  instructions: systemPrompt,
  context: result1.context  // Preserves conversation history
});
const result2 = await agent2.processMessage('Now update the version to 2.0.0');
```

---

### Type 2 — Base Components (Custom Agentic Loop)

If you **need to modify or customize the agentic loop**, use the three base components directly. This gives you control over every stage of the pipeline while still using the framework's building blocks.

```typescript
import codebolt from '@codebolt/codeboltjs';
import {
  InitialPromptGenerator,
  AgentStep,
  ResponseExecutor
} from '@codebolt/agent/unified';
import {
  ChatHistoryMessageModifier,
  EnvironmentContextModifier,
  DirectoryContextModifier,
  IdeContextModifier,
  CoreSystemPromptModifier,
  ToolInjectionModifier,
  AtFileProcessorModifier
} from '@codebolt/agent/processor-pieces';
import { ChatCompressionModifier } from '@codebolt/agent/processor-pieces';
import { ConversationCompactorModifier } from '@codebolt/agent/processor-pieces';
import { FlatUserMessage } from '@codebolt/types/sdk';
import { AgentStepOutput, ProcessedMessage } from '@codebolt/types/agent';

const systemPrompt = `You are an advanced coding assistant.`;

codebolt.onMessage(async (reqMessage: FlatUserMessage) => {
  try {
    // --- Stage 1: Build the initial prompt ---
    // Each modifier adds context to the prompt sent to the LLM.
    // You can add, remove, or reorder modifiers to customize what context the LLM sees.
    const promptGenerator = new InitialPromptGenerator({
      processors: [
        new ChatHistoryMessageModifier({ enableChatHistory: true }),
        new EnvironmentContextModifier({ enableFullContext: true }),
        new DirectoryContextModifier(),
        new IdeContextModifier({
          includeActiveFile: true,
          includeOpenFiles: true,
          includeCursorPosition: true,
          includeSelectedText: true
        }),
        new CoreSystemPromptModifier({ customSystemPrompt: systemPrompt }),
        new ToolInjectionModifier({ includeToolDescriptions: true }),
        new AtFileProcessorModifier({ enableRecursiveSearch: true })
      ],
      baseSystemPrompt: systemPrompt
    });

    let prompt: ProcessedMessage = await promptGenerator.processMessage(reqMessage);
    let completed = false;

    // --- Stage 2: The agentic loop ---
    do {
      // AgentStep handles: PreInferenceProcessors → LLM call → PostInferenceProcessors
      const agentStep = new AgentStep({
        preInferenceProcessors: [
          new ChatCompressionModifier({ enableCompression: true })
        ],
        postInferenceProcessors: []
      });

      const stepResult: AgentStepOutput = await agentStep.executeStep(reqMessage, prompt);
      prompt = stepResult.nextMessage;

      // ResponseExecutor handles: PreToolCallProcessors → Tool execution → PostToolCallProcessors
      const responseExecutor = new ResponseExecutor({
        preToolCallProcessors: [],
        postToolCallProcessors: [
          new ConversationCompactorModifier({
            compactStrategy: 'smart',
            compressionTokenThreshold: 0.5
          })
        ]
      });

      const executionResult = await responseExecutor.executeResponse({
        initialUserMessage: reqMessage,
        actualMessageSentToLLM: stepResult.actualMessageSentToLLM,
        rawLLMOutput: stepResult.rawLLMResponse,
        nextMessage: stepResult.nextMessage
      });

      completed = executionResult.completed;
      prompt = executionResult.nextMessage;

    } while (!completed);

  } catch (error) {
    console.error('Agent error:', error);
    codebolt.chat.sendMessage(`Error: ${error}`, {});
  }
});
```

**Writing a custom MessageModifier:**

```typescript
import { BaseMessageModifier } from '@codebolt/agent/processor-pieces/base';
import { ProcessedMessage } from '@codebolt/types/agent';
import { FlatUserMessage } from '@codebolt/types/sdk';

class DatabaseSchemaModifier extends BaseMessageModifier {
  async modify(
    originalRequest: FlatUserMessage,
    createdMessage: ProcessedMessage
  ): Promise<ProcessedMessage> {
    const schemaInfo = await fetchDatabaseSchema(); // Your custom logic
    createdMessage.message.messages.push({
      role: 'system',
      content: `Database Schema:\n${schemaInfo}`
    });
    return createdMessage;
  }
}

// Use it alongside built-in modifiers
const promptGenerator = new InitialPromptGenerator({
  processors: [
    new ChatHistoryMessageModifier({ enableChatHistory: true }),
    new CoreSystemPromptModifier({ customSystemPrompt: 'You are a DB expert.' }),
    new DatabaseSchemaModifier(),  // Your custom modifier
    new ToolInjectionModifier({ includeToolDescriptions: true })
  ],
  baseSystemPrompt: 'You are a DB expert.'
});
```

**Writing a custom PostToolCallProcessor:**

```typescript
import { BasePostToolCallProcessor } from '@codebolt/agent/processor-pieces/base';
import {
  PostToolCallProcessorInput,
  PostToolCallProcessorOutput
} from '@codebolt/types/agent';

class ErrorCheckProcessor extends BasePostToolCallProcessor {
  async modify(input: PostToolCallProcessorInput): Promise<PostToolCallProcessorOutput> {
    const { nextPrompt, toolResults } = input;

    if (toolResults) {
      for (const result of toolResults) {
        if (typeof result.content === 'string' && result.content.includes('CRITICAL_ERROR')) {
          return { nextPrompt, shouldExit: true };  // Stop the loop
        }
      }
    }

    return { nextPrompt, shouldExit: false };  // Continue
  }
}
```

---

### Type 3 — Core API (Advanced / Full Control)

When you want to **go deeper into agent functionality** and build more advanced behavior, use Codebolt's Core API directly. This gives you full control — you make LLM calls, read files, run commands, and orchestrate everything yourself.

```typescript
import codebolt from '@codebolt/codeboltjs';
import { FlatUserMessage } from '@codebolt/types/sdk';

codebolt.onMessage(async (reqMessage: FlatUserMessage) => {
  const userMessage = reqMessage.userMessage;

  // Step 1: Classify the task using an LLM call
  const analysis = await codebolt.llm.inference({
    messages: [
      {
        role: 'system',
        content: 'Classify the user request as: "code_change", "question", or "debug". Respond with only the classification.'
      },
      { role: 'user', content: userMessage }
    ]
  });

  const taskType = analysis.completion?.choices?.[0]?.message?.content?.trim() || 'question';
  codebolt.chat.sendMessage(`Task type: ${taskType}`, {});

  // Step 2: Handle based on classification
  if (taskType === 'code_change') {
    await handleCodeChange(userMessage);
  } else if (taskType === 'debug') {
    await handleDebug(userMessage);
  } else {
    await handleQuestion(userMessage);
  }
});

async function handleCodeChange(task: string) {
  // Read the workspace files
  const files = await codebolt.fs.listFiles('/');
  codebolt.chat.sendMessage(`Found ${files.length} files`, {});

  // Ask LLM to plan which files to change
  const planResponse = await codebolt.llm.inference({
    messages: [
      {
        role: 'system',
        content: 'Given the file list and task, output a JSON array of files to modify: [{"file": "path", "action": "create|modify|delete"}]'
      },
      { role: 'user', content: `Files: ${JSON.stringify(files)}\nTask: ${task}` }
    ]
  });

  const plan = JSON.parse(planResponse.completion?.choices?.[0]?.message?.content || '[]');

  // Execute the plan file by file
  for (const step of plan) {
    if (step.action === 'modify') {
      const content = await codebolt.fs.readFile(step.file);

      const editResponse = await codebolt.llm.inference({
        messages: [
          { role: 'system', content: 'Apply the requested change. Return the complete updated file.' },
          { role: 'user', content: `File: ${step.file}\nContent:\n${content}\nTask: ${task}` }
        ]
      });

      const newContent = editResponse.completion?.choices?.[0]?.message?.content || '';
      await codebolt.fs.updateFile(step.file, step.file, newContent);
      codebolt.chat.sendMessage(`Updated ${step.file}`, {});
    }
  }
}

async function handleDebug(task: string) {
  // Run tests and capture output
  const testOutput = await codebolt.terminal.executeCommand('npm test', true);

  // Use LLM to analyze failures
  const debugResponse = await codebolt.llm.inference({
    messages: [
      { role: 'system', content: 'Analyze the test output and suggest fixes.' },
      { role: 'user', content: `Output:\n${testOutput}\nIssue: ${task}` }
    ]
  });

  codebolt.chat.sendMessage(
    debugResponse.completion?.choices?.[0]?.message?.content || 'Unable to debug.',
    {}
  );
}

async function handleQuestion(question: string) {
  // Search the codebase for context
  const searchResults = await codebolt.fs.searchFiles(question, '/');

  // Answer with LLM using codebase context
  const answer = await codebolt.llm.inference({
    messages: [
      { role: 'system', content: 'Answer based on the codebase search results.' },
      { role: 'user', content: `Question: ${question}\nResults:\n${JSON.stringify(searchResults)}` }
    ]
  });

  codebolt.chat.sendMessage(
    answer.completion?.choices?.[0]?.message?.content || 'No answer found.',
    {}
  );
}
```

**Using MCP Tools Directly:**

```typescript
// List available tools from MCP servers
const { data: tools } = await codebolt.mcp.listMcpFromServers(['codebolt']);

// Execute a specific tool — permissions handled by the application
const { data } = await codebolt.mcp.executeTool('codebolt', 'readFile', { path: '/src/index.ts' });
const [didUserReject, fileContent] = data;
if (!didUserReject) {
  console.log('File content:', fileContent);
}
```

**Core API modules available:**

| Module | Key Methods |
|--------|-------------|
| `codebolt.llm` | `inference(params)` |
| `codebolt.fs` | `readFile`, `createFile`, `updateFile`, `deleteFile`, `listFiles`, `searchFiles` |
| `codebolt.terminal` | `executeCommand`, `executeCommandRunUntilError` |
| `codebolt.git` | `init`, `status`, `add`, `commit`, `push`, `pull`, `checkout`, `diff`, `clone` |
| `codebolt.browser` | `goToPage`, `screenshot`, `click`, `type`, `getMarkdown` |
| `codebolt.chat` | `sendMessage`, `getHistory` |
| `codebolt.mcp` | `executeTool`, `listMcpFromServers`, `getTools` |
| `codebolt.agent` | `findAgent`, `startAgent`, `getAgentsList` |
| `codebolt.thread` | `createThreadInBackground` |
| `codebolt.memory` | Memory storage |
| `codebolt.todo` | `getAllIncompleteTodos` |
| `codebolt.state` | State persistence |

---

### Side-by-Side: Same Task, Three Types

The same task — "Read a file and summarize it" — using all three approaches:

**Type 1 (CodeboltAgent — simplest):**
```typescript
const agent = new CodeboltAgent({
  instructions: 'You are a file summarizer. Read files and provide concise summaries.'
});
codebolt.onMessage(async (msg) => await agent.processMessage(msg));
```

**Type 2 (Base Components — custom loop):**
```typescript
codebolt.onMessage(async (msg) => {
  const gen = new InitialPromptGenerator({
    processors: [
      new CoreSystemPromptModifier({ customSystemPrompt: 'Summarize files.' }),
      new ToolInjectionModifier({ includeToolDescriptions: true, allowedTools: ['codebolt--readFile'] })
    ],
    baseSystemPrompt: 'Summarize files.'
  });
  let prompt = await gen.processMessage(msg);
  let done = false;
  do {
    const step = await new AgentStep({}).executeStep(msg, prompt);
    const exec = await new ResponseExecutor({
      preToolCallProcessors: [], postToolCallProcessors: []
    }).executeResponse({
      initialUserMessage: msg, actualMessageSentToLLM: step.actualMessageSentToLLM,
      rawLLMOutput: step.rawLLMResponse, nextMessage: step.nextMessage
    });
    done = exec.completed;
    prompt = exec.nextMessage;
  } while (!done);
});
```

**Type 3 (Core API — full control):**
```typescript
codebolt.onMessage(async (msg) => {
  const filePath = extractFilePath(msg.userMessage);
  const content = await codebolt.fs.readFile(filePath);
  const response = await codebolt.llm.inference({
    messages: [
      { role: 'system', content: 'Summarize the following file.' },
      { role: 'user', content: `File: ${filePath}\n\n${content}` }
    ]
  });
  codebolt.chat.sendMessage(response.completion?.choices?.[0]?.message?.content || '', {});
});
```

---

## Getting Started: Codebolt CLI

Use the **`codebolt-cli`** command-line tool to generate templates for agents and MCP tools. This is the recommended starting point for creating new agents or tools.

### Create an Agent Template

```bash
# Interactive mode (recommended)
npx codebolt-cli createagent

# Quick mode with name
npx codebolt-cli createagent -n "MyAgent" --quick
```

This generates a complete agent project structure with:
- `codeboltagent.yaml` - Agent configuration
- `package.json` - Dependencies
- `src/index.ts` - Entry point with boilerplate code

### Create an MCP Tool Template

```bash
# Interactive mode
npx codebolt-cli createtool

# With options
npx codebolt-cli createtool -n "MyTool" -i "my-tool-id" -d "Tool description"
```

This generates an MCP tool project with:
- `codebolttool.yaml` - Tool configuration
- `package.json` - Dependencies
- `src/index.ts` - MCP server boilerplate

### Other Useful CLI Commands

| Command | Description |
|---------|-------------|
| `npx codebolt-cli login` | Authenticate with Codebolt platform |
| `npx codebolt-cli publishagent [path]` | Publish agent to registry |
| `npx codebolt-cli publishtool [path]` | Publish MCP tool to registry |
| `npx codebolt-cli listagents` | List your published agents |
| `npx codebolt-cli listtools` | List your published MCP tools |
| `npx codebolt-cli startagent [path]` | Start agent locally for testing |
| `npx codebolt-cli cloneagent <id> [path]` | Clone an existing agent |
| `npx codebolt-cli inspecttool <file>` | Debug tool with MCP inspector |

### Project Structure

```
my-agent/
├── codeboltagent.yaml    # Agent configuration (required)
├── package.json          # Dependencies
├── src/
│   └── index.ts          # Agent entry point
└── dist/                 # Compiled output
```

### Building the Agent

**IMPORTANT:** After creating or modifying an agent, you MUST build it before running.

```bash
# Install dependencies first
npm install

# Build the agent (compiles TypeScript to JavaScript)
npm run build

# Or use webpack directly if configured
npx webpack
```

The build process:
1. Compiles TypeScript files from `src/` to JavaScript in `dist/`
2. Bundles all dependencies (usually via webpack)
3. Creates the entry point specified in `codeboltagent.yaml` (typically `dist/index.js`)

**Always run these commands after creating an agent:**

```bash
# Complete setup flow
npm install && npm run build

# Verify the build succeeded
ls -la dist/
```

**Common build issues:**
- Missing dependencies: Run `npm install` first
- Type errors: Run `npx tsc --noEmit` to check
- Webpack errors: Check `webpack.config.js` exists and is valid

**Package.json scripts should include:**

```json
{
  "scripts": {
    "build": "npx webpack",
    "dev": "npx tsx src/index.ts",
    "typecheck": "npx tsc --noEmit",
    "lint": "npx eslint src/"
  }
}
```

## Architecture Overview

Codebolt provides a **layered architecture** for building AI agents. The three main types (described above with detailed examples) plus no-code Remix Agents and reusable ActionBlocks:

```
┌─────────────────────────────────────────────────────────────────┐
│  REMIX AGENTS: No-Code Configuration                            │
│  Markdown files with YAML frontmatter + custom instructions     │
│  → Use when: You want agents without writing any code           │
├─────────────────────────────────────────────────────────────────┤
│  CodeboltAgent Wrapper (Level 3): High-Level Abstractions       │
│  CodeboltAgent, Agent, Workflow, Tools                          │
│  → Use when: Simple prompt-based agent, no custom loop needed   │
├─────────────────────────────────────────────────────────────────┤
│  Base Components (Level 2): Custom Agentic Loop                 │
│  InitialPromptGenerator, AgentStep, ResponseExecutor            │
│  → Use when: You need to customize the agentic loop             │
├─────────────────────────────────────────────────────────────────┤
│  Core API (Level 1): Full Control                               │
│  codebolt.llm, codebolt.fs, codebolt.terminal, etc.            │
│  → Use when: Advanced behavior, build everything from scratch   │
└─────────────────────────────────────────────────────────────────┘
         ↑↓ Mix & Match ↑↓
┌─────────────────────────────────────────────────────────────────┐
│  ActionBlocks: Reusable logic units invoked from any level      │
└─────────────────────────────────────────────────────────────────┘

Remember: Permissions, tool approval, and access control are ALL
handled by the Codebolt application — your agent code does not
need to implement any permission logic.
```

## Remix Agents (No-Code)

Remix Agents let you create agents **without writing any code**. They're stored as markdown files with YAML frontmatter in `.codebolt/agents/remix/`.

### File Format

```markdown
---
name: my-code-reviewer
description: A specialized code review agent
model: claude-sonnet-4-20250514
provider: anthropic
tools:
  - codebolt--readFile
  - codebolt--writeFile
  - codebolt--search
maxSteps: 100
reasoningEffort: medium
skills:
  - code-review
remixedFromId: base-coding-agent
remixedFromTitle: Base Coding Agent
version: 1.0.0
---

# Custom Instructions

You are a code review specialist. When reviewing code:

1. Check for security vulnerabilities
2. Identify performance issues
3. Suggest improvements
4. Note style inconsistencies

Always provide constructive feedback with examples.
```

### MarkdownAgent Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Agent identifier (becomes filename) |
| `description` | string | Brief description |
| `model` | string | Model to use (e.g., "claude-sonnet-4-20250514") |
| `provider` | string | Provider name (e.g., "anthropic", "openai") |
| `tools` | string[] | Tools available to the agent |
| `maxSteps` | number | Max agentic iterations |
| `reasoningEffort` | 'low' \| 'medium' \| 'high' | For reasoning models |
| `skills` | string[] | Skills to auto-load |
| `remixedFromId` | string | Original agent ID (when remixing) |
| `additionalSubAgent` | SubAgentConfig[] | Sub-agents to include |

### When to Use Remix Agents

- Quick customization of existing agents
- Non-developers creating agents
- Prototyping before building full code agents
- Sharing agents as portable markdown files
- Compatible with external tools (OpenCode, Factory.ai, Claude Code)

**See:** [references/remix-agents.md](references/remix-agents.md)

## Mixing and Matching Levels

**Levels are NOT exclusive.** You can combine them based on your needs:

```typescript
// Example: Level 3 agent + Level 1 direct API calls outside the loop
import { CodeboltAgent } from '@codebolt/agent/unified';
import codebolt from '@codebolt/codeboltjs';
import { FlatUserMessage } from "@codebolt/types/sdk";

codebolt.onMessage(async (msg:FlatUserMessage) => {
  // Level 1: Send initial status message
  codebolt.chat.sendMessage('Starting analysis...');

  // Level 1: Do pre-processing with direct APIs
  const files = await codebolt.fs.listFile('./src', true);

  // Level 3: Use high-level agent for the main work
  const agent = new CodeboltAgent({ instructions: 'You are a code reviewer.' });
  const result = await agent.processMessage(msg);

  // Level 1: Post-processing with direct APIs
  await codebolt.memory.json.save({ review: result, files: files.data });
  codebolt.chat.sendMessage('Review complete and saved!');
});
```

**Common mixing patterns:**

| Pattern | Description |
|---------|-------------|
| Level 3 + Level 1 outside loop | Use CodeboltAgent but add direct API calls before/after |
| Level 2 + custom loop logic | Use base components but add custom iteration control |
| Level 3 + ActionBlocks | Use CodeboltAgent with ActionBlocks for reusable subtasks |
| Workflow + ActionBlocks | Workflow steps that invoke ActionBlocks |

## The Agent Loop Pattern

Codebolt agents follow a standard execution pattern:

```
┌────────────────────────────────────────────────────────────────┐
│  1. onMessage() receives user message                          │
│  2. Process into initial prompt (attach context, tools, etc.)  │
│  3. AGENT LOOP:                                                │
│     ├─► Send prompt to LLM                                     │
│     ├─► Get response (may include tool_calls)                  │
│     ├─► If tool_calls: execute tools, add results to prompt    │
│     ├─► Check for async events (child agents, completions)     │
│     └─► Repeat until no tool_calls AND no pending events       │
│  4. Return final response                                      │
└────────────────────────────────────────────────────────────────┘
```

### Basic Pattern

```typescript
import type { ProcessedMessage, AgentStepOutput, ResponseExecutorResult } from '@codebolt/types/agent';

codebolt.onMessage(async (reqMessage: FlatUserMessage): Promise<void> => {
  // 1. Process message into prompt
  let prompt: ProcessedMessage = await promptGenerator.processMessage(reqMessage);

  // 2. Agent loop
  let completed: boolean = false;
  let execResult: ResponseExecutorResult;
  while (!completed) {
    const stepResult: AgentStepOutput = await agentStep.executeStep(reqMessage, prompt);
    execResult = await responseExecutor.executeResponse({
      initialUserMessage: reqMessage,
      actualMessageSentToLLM: stepResult.actualMessageSentToLLM,
      rawLLMOutput: stepResult.rawLLMResponse,
      nextMessage: stepResult.nextMessage
    });

    completed = execResult.completed;
    prompt = execResult.nextMessage;
  }

  return execResult!.finalMessage;
});
```

### With Async Event Handling (Orchestrator Pattern)

```typescript
const eventQueue = codebolt.agentEventQueue;
const agentTracker = codebolt.backgroundChildThreads;

codebolt.onMessage(async (reqMessage:FlatUserMessage) => {
  let prompt = await promptGenerator.processMessage(reqMessage);
  let continueLoop = true;

  do {
    // Run agent loop until no tool calls
    const result = await runAgentLoop(reqMessage, prompt);
    prompt = result.prompt;

    // Check for events from child agents
    if (agentTracker.getRunningAgentCount() > 0 ||
        eventQueue.getPendingExternalEventCount() > 0) {
      const events = await eventQueue.getPendingQueueEvents();
      // Process events, add to prompt
      continueLoop = true;
    } else {
      continueLoop = false;
    }
  } while (continueLoop);
});
```

### Long-Running Orchestrator (Never Exits)

```typescript
// For orchestrators that wait for child agents indefinitely
while (true) {
  const event = await eventQueue.waitForAnyExternalEvent();
  // Process event...
}
```

**See:** [references/level2-base-components.md](references/level2-base-components.md) for full details.

## ActionBlocks

ActionBlocks are **reusable, independently executable units** of logic that can be invoked from agents, workflows, or other ActionBlocks.

> **⚠️ CRITICAL: Do NOT Write Inline Action Block Logic in Agents**
>
> When generating agent code, **NEVER write action block logic inline within the agent code**. ActionBlocks are designed as **separate, reusable components** that exist independently in the `/action-blocks/` directory.
>
> ```typescript
> import type { FlatUserMessage } from '@codebolt/types/sdk';
>
> // ❌ WRONG - Do NOT write inline action block logic in agents
> codebolt.onMessage(async (msg: FlatUserMessage): Promise<void> => {
>   // Don't implement planning logic directly here
>   const plan = await createPlanInline(msg);  // BAD!
>   const jobs = await breakIntoJobsInline(plan);  // BAD!
>   // ...inline implementation...
> });
>
> // ✅ CORRECT - Invoke existing ActionBlocks by name
> codebolt.onMessage(async (msg: FlatUserMessage): Promise<void> => {
>   // Call the reusable ActionBlock
>   const planResult = await codebolt.actionBlock.start('create-plan-for-given-task', {
>     userMessage: msg
>   });
>
>   if (planResult.success) {
>     const jobsResult = await codebolt.actionBlock.start('break-task-into-jobs', {
>       plan: planResult.result
>     });
>   }
> });
> ```
>
> **Why?** ActionBlocks are:
> - **Reusable** across multiple agents and workflows
> - **Independently testable** and deployable
> - **Discoverable** via `codebolt.actionBlock.list()`
> - **Documented** with typed inputs/outputs in `actionblock.yml`

### When to Use ActionBlocks

- Extract complex logic into reusable components
- Share functionality across multiple agents
- Create modular, testable units of work
- Build orchestration pipelines with Workflows
- **Always invoke existing ActionBlocks** instead of reimplementing their logic inline

### Quick Start

```typescript
// Invoke an ActionBlock
const result = await codebolt.actionBlock.start('create-plan-for-given-task', {
  userMessage: reqMessage
});

if (result.success) {
  console.log('Plan created:', result.result.planId);
}
```

### Creating an ActionBlock

```typescript
// src/index.ts
import codebolt from '@codebolt/codeboltjs';

// Define types for ActionBlock invocation (see references/action-blocks.md for full definitions)
interface ThreadContext {
  params?: Record<string, unknown>;
  [key: string]: unknown;
}

interface ActionBlockInvocationMetadata {
  sideExecutionId: string;
  threadId: string;
  parentAgentId: string;
  parentAgentInstanceId: string;
  timestamp: string;
}

codebolt.onActionBlockInvocation(async (threadContext: ThreadContext, metadata: ActionBlockInvocationMetadata) => {
  const params = threadContext?.params || {};
  const { task, options } = params;

  // Validate
  if (!task) {
    return { success: false, error: 'task is required' };
  }

  // Send status
  codebolt.chat.sendMessage(`Processing: ${task.name}`);

  // Do work
  const result = await processTask(task, options);

  // Return structured result
  return { success: true, data: result };
});
```

### ActionBlocks + Workflows

```typescript
import { Workflow } from '@codebolt/agent/unified';
import codebolt from '@codebolt/codeboltjs';
import type { FlatUserMessage } from '@codebolt/types/sdk';
import type { WorkflowStepResult, WorkflowContext } from '@codebolt/types/agent';

interface OrchestrationContext extends WorkflowContext {
  userMessage: FlatUserMessage;
  planId?: string;
  jobs?: Array<{ id: string; name: string }>;
}

const orchestrationWorkflow: Workflow = new Workflow({
  name: 'Task Orchestration',
  steps: [
    {
      id: 'create-plan',
      execute: async (ctx: OrchestrationContext): Promise<WorkflowStepResult<{ planId: string }>> => {
        const result = await codebolt.actionBlock.start('create-plan-for-given-task', {
          userMessage: ctx.userMessage
        });
        return { success: result.success, data: { planId: result.result?.planId } };
      }
    },
    {
      id: 'create-jobs',
      execute: async (ctx: OrchestrationContext): Promise<WorkflowStepResult<{ jobs: Array<{ id: string; name: string }> }>> => {
        const result = await codebolt.actionBlock.start('create-jobs-from-plan', {
          planId: ctx.planId
        });
        return { success: result.success, data: { jobs: result.result?.jobs } };
      }
    }
  ]
});
```

**See:** [references/action-blocks.md](references/action-blocks.md)

## Choosing the Right Level

| Need | Type | What to Use |
|------|------|-------------|
| No-code agent creation | Remix | Markdown file with YAML frontmatter |
| Simple prompt-based agent, no custom loop | CodeboltAgent Wrapper | `CodeboltAgent` with `instructions` |
| Custom agent loop logic | Base Components | `InitialPromptGenerator` + `AgentStep` + `ResponseExecutor` |
| Full manual control, advanced behavior | Core API | Direct `codebolt.*` APIs |
| Multi-step orchestration | CodeboltAgent Wrapper | `Workflow` with steps |
| Orchestrator with child agents | Base Components | Agent loop + `agentEventQueue` |
| Long-running orchestrator | Base Components | `waitForAnyExternalEvent()` loop |
| Reusable logic units | ActionBlocks | `codebolt.actionBlock.start()` (**invoke, don't inline!**) |
| Tools for single agent | CodeboltAgent Wrapper | `createTool()` with Zod schemas |
| Shared tools across agents | MCP | `MCPServer` from `@codebolt/mcp` |
| Custom context injection | Any | Extend `BaseMessageModifier` |

> **Remember:** When an ActionBlock exists for a task (planning, job creation, etc.), **always invoke it** via `codebolt.actionBlock.start('action-block-name', params)` rather than implementing the logic inline in your agent.
>
> **Remember:** Permissions (tool approval, file access, workspace boundaries) are handled by the Codebolt application. Your agent does not need to implement any permission logic.

## Tool Execution Architecture

**ResponseExecutor** automatically handles tool execution from LLM responses. You should use it instead of manually parsing and executing tools.

### Built-in Tool Routes

The `ResponseExecutor` routes tools based on naming conventions:

| Tool Pattern | Route | Execution |
|--------------|-------|-----------|
| `toolbox--toolname` | MCP | `codebolt.mcp.executeTool(toolbox, toolname, args)` |
| `subagent--agentname` | Subagent | `codebolt.agent.startAgent(agentname, task)` |
| `codebolt--thread_management` | Thread | `codebolt.thread.createThreadInBackground(options)` |
| `attempt_completion` | Completion | Marks task as complete |

### When to Use What

| Need | Approach |
|------|----------|
| Standard MCP tools | Just use `ResponseExecutor` - it handles them automatically |
| Custom local tools | Add a `PreToolCallProcessor` to intercept and handle |
| Enhance tool results | Add a `PostToolCallProcessor` to modify results |
| Manual control | Level 1 direct APIs (not recommended for production) |

### Adding Custom/Local Tools

Use `PreToolCallProcessor` to intercept tool calls and execute custom logic:

```typescript
import { BasePreToolCallProcessor } from '@codebolt/agent/processor-pieces';
import type { PreToolCallProcessorInput, ProcessedMessage } from '@codebolt/types/agent';

class MyLocalToolProcessor extends BasePreToolCallProcessor {
  async modify(input: PreToolCallProcessorInput): Promise<{
    nextPrompt: ProcessedMessage;
    shouldExit: boolean;
  }> {
    const toolCalls = input.rawLLMResponseMessage.choices?.[0]?.message?.tool_calls || [];

    for (const toolCall of toolCalls) {
      if (toolCall.function.name === 'my_local_tool') {
        // Execute your custom tool
        const args = JSON.parse(toolCall.function.arguments);
        const result = await myLocalHandler(args);

        // Add result to message history
        input.nextPrompt.message.messages.push({
          role: 'tool',
          tool_call_id: toolCall.id,
          content: JSON.stringify(result)
        });
      }
    }

    return { nextPrompt: input.nextPrompt, shouldExit: false };
  }
}

// Register with ResponseExecutor
const responseExecutor = new ResponseExecutor({
  preToolCallProcessors: [new MyLocalToolProcessor()],
  postToolCallProcessors: []
});
```

**See:** [references/level2-base-components.md](references/level2-base-components.md) for complete examples, [references/processors.md](references/processors.md) for processor details.

## Agent Configuration (codeboltagent.yaml)

Every code-based agent requires a `codeboltagent.yaml` file that defines how Codebolt reads and presents the agent.

### Basic Structure

```yaml
title: My Agent
unique_id: my-agent
version: 1.0.0
author: your-name

initial_message: Hello! How can I help you today?
description: Short description of the agent
longDescription: >
  A longer description explaining what this agent does,
  its capabilities, and use cases.

tags:
  - coding
  - review

avatarSrc: https://example.com/avatar.png
avatarFallback: MA

metadata:
  agent_routing:
    worksonblankcode: true
    worksonexistingcode: true
    supportedlanguages:
      - typescript
      - javascript
    supportedframeworks:
      - react
      - node
    supportRemix: true

  defaultagentllm:
    strict: true
    modelorder:
      - claude-sonnet-4-20250514
      - gpt-4-turbo

  llm_role:
    - name: documentationllm
      description: LLM for documentation tasks
      strict: false
      modelorder:
        - gpt-4-turbo
        - claude-sonnet-4-20250514

actions:
  - name: Review
    description: Review code for issues
    detailDescription: Performs comprehensive code review
    actionPrompt: Please review this code
  - name: Refactor
    description: Refactor selected code
    detailDescription: Improves code structure
    actionPrompt: Please refactor this code
```

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Display name of the agent |
| `unique_id` | string | Unique identifier (used internally) |
| `version` | string | Semantic version (e.g., "1.0.0") |
| `initial_message` | string | First message shown to user |
| `description` | string | Short description (shown in agent list) |
| `longDescription` | string | Detailed description |
| `tags` | string[] | Categorization tags |
| `avatarSrc` | string | URL to agent avatar image |
| `avatarFallback` | string | Fallback text for avatar |
| `author` | string | Agent author/creator |

### Metadata Fields

| Field | Description |
|-------|-------------|
| `agent_routing.worksonblankcode` | Can work on new projects |
| `agent_routing.worksonexistingcode` | Can work on existing projects |
| `agent_routing.supportedlanguages` | List of supported languages |
| `agent_routing.supportedframeworks` | List of supported frameworks |
| `agent_routing.supportRemix` | Allow users to remix this agent |
| `defaultagentllm.strict` | Require exact model match |
| `defaultagentllm.modelorder` | Preferred models in order |
| `llm_role` | Role-specific LLM configurations |

### Actions

Actions are quick commands users can trigger:

```yaml
actions:
  - name: ActionName
    description: Short description shown in UI
    detailDescription: Longer explanation
    actionPrompt: The prompt sent to the agent
```

**See:** [references/agent-yaml.md](references/agent-yaml.md) for full reference.

## Level 1: Direct APIs

For building agents manually without any framework.

**Use the existing skills:**
- **`codebolt-api-access`** - TypeScript SDK calls (`codebolt.fs`, `codebolt.llm`, etc.)
- **`codebolt-mcp-access`** - MCP tool execution (`codebolt.tools.executeTool`)

**See:** [references/level1-direct-apis.md](references/level1-direct-apis.md)

## Level 2: Base Components

For custom agent loop with helper functions.

```typescript
import { InitialPromptGenerator, AgentStep, ResponseExecutor } from '@codebolt/agent/unified';
import { ChatHistoryMessageModifier, CoreSystemPromptModifier } from '@codebolt/agent/processor-pieces';
import type { FlatUserMessage } from '@codebolt/types/sdk';
import type { ProcessedMessage, AgentStepOutput, ResponseExecutorResult } from '@codebolt/types/agent';

const promptGenerator: InitialPromptGenerator = new InitialPromptGenerator({
  processors: [new ChatHistoryMessageModifier(), new CoreSystemPromptModifier()]
});
const agentStep: AgentStep = new AgentStep({});
const responseExecutor: ResponseExecutor = new ResponseExecutor({});

let prompt: ProcessedMessage = await promptGenerator.processMessage(userMessage);
let completed: boolean = false;
while (!completed) {
  const stepResult: AgentStepOutput = await agentStep.executeStep(userMessage, prompt);
  const execResult: ResponseExecutorResult = await responseExecutor.executeResponse({
    initialUserMessage: userMessage,
    actualMessageSentToLLM: stepResult.actualMessageSentToLLM,
    rawLLMOutput: stepResult.rawLLMResponse,
    nextMessage: stepResult.nextMessage
  });
  completed = execResult.completed;
  prompt = execResult.nextMessage;
}
```

**See:** [references/level2-base-components.md](references/level2-base-components.md)

## Level 3: High-Level Abstractions

For production-ready agents with minimal setup.

```typescript
import { CodeboltAgent } from '@codebolt/agent/unified';
import type { AgentResult } from '@codebolt/types/agent';

const agent: CodeboltAgent = new CodeboltAgent({
  instructions: 'You are a coding assistant.',
  enableLogging: true
});

const result: AgentResult = await agent.processMessage({
  userMessage: 'Help me write a function',
  threadId: 'thread-123',
  messageId: 'msg-456'
});

if (result.success) {
  console.log('Result:', result.result);
} else {
  console.error('Error:', result.error);
}
```

**See:** [references/level3-high-level.md](references/level3-high-level.md)

## Creating Custom Tools

Two approaches for adding custom tools:

| Approach | Package | Use Case |
|----------|---------|----------|
| **Local Tools** | `@codebolt/agent` | Tools used within your agent code |
| **MCP Servers** | `@codebolt/mcp` | Standalone tool servers, shared across agents |

### Local Tools (Quick)

```typescript
import { createTool } from '@codebolt/agent/unified';
import { z } from 'zod';

const searchTool = createTool({
  id: 'search-files',
  description: 'Search for files matching a pattern',
  inputSchema: z.object({ pattern: z.string(), directory: z.string().optional() }),
  execute: async ({ input }) => ({ files: ['file1.ts', 'file2.ts'] })
});
```

### Custom MCP Servers (Shared)

```typescript
import { MCPServer } from '@codebolt/mcp';
import { z } from 'zod';

interface GreetArgs {
  name: string;
}

const server: MCPServer = new MCPServer({ name: 'my-tools', version: '1.0.0' });

server.addTool({
  name: 'greet',
  description: 'Greet someone',
  parameters: z.object({ name: z.string() }),
  execute: async (args: GreetArgs): Promise<string> => {
    return 'Hello, ' + args.name + '!';
  }
});

await server.start({ transportType: 'stdio' });
```

**See:** [references/tools.md](references/tools.md)

## Creating Custom Modifiers & Processors

```typescript
import { BaseMessageModifier } from '@codebolt/agent/processor-pieces';
import type { FlatUserMessage } from '@codebolt/types/sdk';
import type { ProcessedMessage } from '@codebolt/types/agent';

class MyModifier extends BaseMessageModifier {
  async modify(
    originalRequest: FlatUserMessage,
    createdMessage: ProcessedMessage
  ): Promise<ProcessedMessage> {
    createdMessage.message.messages.push({ role: 'system', content: 'Custom context' });
    return createdMessage;
  }
}
```

**See:** [references/processors.md](references/processors.md)

## Building Workflows

```typescript
import { Workflow } from '@codebolt/agent/unified';
import type { WorkflowStepResult, WorkflowContext } from '@codebolt/types/agent';

const workflow: Workflow = new Workflow({
  name: 'Code Review',
  steps: [
    { id: 'lint', execute: async (ctx: WorkflowContext): Promise<WorkflowStepResult<object>> => ({ success: true, data: {} }) },
    { id: 'test', execute: async (ctx: WorkflowContext): Promise<WorkflowStepResult<object>> => ({ success: true, data: {} }) }
  ]
});

const result = await workflow.executeAsync();
```

**See:** [references/workflows.md](references/workflows.md)

## Key Imports

```typescript
// Level 3 - High-level
import { CodeboltAgent, Agent, Workflow, createTool } from '@codebolt/agent/unified';

// Level 2 - Base components
import { InitialPromptGenerator, AgentStep, ResponseExecutor } from '@codebolt/agent/unified';

// Processors & Modifiers
import {
  BaseMessageModifier, CoreSystemPromptModifier, ChatHistoryMessageModifier,
  ToolInjectionModifier, EnvironmentContextModifier, DirectoryContextModifier,
  IdeContextModifier, BasePreInferenceProcessor, BasePostInferenceProcessor,
  BasePreToolCallProcessor, BasePostToolCallProcessor
} from '@codebolt/agent/processor-pieces';

// Custom MCP Servers
import { MCPServer } from '@codebolt/mcp';

// Level 1 - Direct APIs, ActionBlocks & Event Queue
import codebolt from '@codebolt/codeboltjs';
// codebolt.actionBlock.start(), codebolt.actionBlock.list()
// codebolt.agentEventQueue.getPendingQueueEvents()
// codebolt.agentEventQueue.waitForAnyExternalEvent()
// codebolt.backgroundChildThreads.getRunningAgentCount()

// SDK Types (from @codebolt/types/sdk)
import type {
  FlatUserMessage,          // User message input
  LLMCompletion,            // Raw LLM response
  ChatMessage,              // Message in conversation
  ToolCall,                 // Tool call from LLM
  MessageObject             // Generic message object
} from '@codebolt/types/sdk';

// Agent Types (from @codebolt/types/agent)
import type {
  ProcessedMessage,         // Output from InitialPromptGenerator
  AgentStepOutput,          // Output from AgentStep.executeStep()
  ResponseExecutorResult,   // Output from ResponseExecutor.executeResponse()
  AgentResult,              // Output from CodeboltAgent.processMessage()
  WorkflowStepResult,       // Result from workflow step execute()
  WorkflowContext,          // Workflow execution context
  PreToolCallProcessorInput,  // Input to pre-tool call processor
  PostToolCallProcessorInput  // Input to post-tool call processor
} from '@codebolt/types/agent';
```

## References

| Topic | File |
|-------|------|
| Agent YAML Configuration | [references/agent-yaml.md](references/agent-yaml.md) |
| Remix Agents (No-Code) | [references/remix-agents.md](references/remix-agents.md) |
| Mixing & Matching Levels | This file (above) |
| Level 1: Direct APIs | [references/level1-direct-apis.md](references/level1-direct-apis.md) |
| Level 2: Base Components | [references/level2-base-components.md](references/level2-base-components.md) |
| Level 3: High-Level | [references/level3-high-level.md](references/level3-high-level.md) |
| ActionBlocks | [references/action-blocks.md](references/action-blocks.md) |
| Tools | [references/tools.md](references/tools.md) |
| Processors & Modifiers | [references/processors.md](references/processors.md) |
| Workflows | [references/workflows.md](references/workflows.md) |
| Examples | [references/examples.md](references/examples.md) |

## Code Quality: Linting & Error Checking

**IMPORTANT:** After writing or modifying agent code, **ALWAYS** lint and check for errors before running. This is a critical step that should never be skipped.

### Use Strict Typings

**You do NOT need to create custom typings.** Types for most Codebolt functionality are already provided by the packages:

- `@codebolt/codeboltjs` - Types for direct SDK APIs
- `@codebolt/agent` - Types for agent components, workflows, tools
- `@codebolt/types` - Shared type definitions

Simply use the existing types — they are automatically available when you import from these packages:

```typescript
// Types are included with the packages - no separate install needed
import codebolt from '@codebolt/codeboltjs';
import { CodeboltAgent, Workflow, createTool } from '@codebolt/agent/unified';

// Common SDK types
import type { FlatUserMessage, MessageObject, LLMCompletion } from '@codebolt/types/sdk';
import type { ProcessedMessage, AgentConfig } from '@codebolt/types/agent';
```

### Run Error Checks

```bash
# Run TypeScript compiler to check for type errors
npx tsc --noEmit

# Run ESLint to check for code quality issues
npx eslint src/

# Or if the project has npm scripts configured
npm run lint
npm run typecheck
```

### Common Checks to Perform

1. **Type errors** - Ensure all TypeScript types are correct (use `@codebolt/types`)
2. **Import errors** - Verify all imports resolve correctly
3. **Unused variables** - Remove or use declared variables
4. **Missing dependencies** - Install required packages
5. **Schema validation** - Validate `codeboltagent.yaml` structure
6. **Async/await errors** - Ensure proper handling of promises

**Tip:** Configure your IDE to show errors inline, or run `npx tsc --watch` during development for real-time feedback.

## Best Practices for Agent Development

### 1. Always Invoke ActionBlocks, Never Inline Their Logic

**This is the most important rule when generating agent code:**

```typescript
// ✅ DO: Invoke existing ActionBlocks by name
const result = await codebolt.actionBlock.start('create-plan-for-given-task', {
  userMessage: msg
});

// ❌ DON'T: Implement action block logic inline in your agent
// const prompt = new InitialPromptGenerator({...});
// const plan = await generatePlanInline(msg); // BAD!
```

### 2. Discover Before Implementing

Before writing any complex logic, check if an ActionBlock already exists:

```typescript
// List available ActionBlocks
const blocks = await codebolt.actionBlock.list();

// Check if there's one for your use case
const planningBlock = blocks.data.find(b => b.name.includes('plan'));
if (planningBlock) {
  // Use it instead of writing inline logic
  const result = await codebolt.actionBlock.start(planningBlock.name, params);
}
```

### 3. Keep Agents Thin

Agents should be **orchestrators**, not **implementors**:
- Use ActionBlocks for complex logic (planning, job creation, task decomposition)
- Use Workflows for multi-step orchestration
- Keep agent code focused on flow control and user interaction

### 4. Type-Safe ActionBlock Calls

```typescript
// Define expected response type
interface PlanResult {
  planId: string;
  tasks: Array<{ id: string; name: string }>;
}

// Use typed response
const result = await codebolt.actionBlock.start<PlanResult>('create-plan-for-given-task', {
  userMessage: msg
});

if (result.success && result.result) {
  const planId = result.result.planId;  // TypeScript knows this exists
}
```

## Related Skills

Use these skills to get detailed information about Codebolt APIs and MCP tools:

- **codebolt_api_access** - Access detailed documentation for all direct TypeScript SDK APIs (`codebolt.fs`, `codebolt.llm`, `codebolt.terminal`, `codebolt.chat`, etc.). Use this skill when you need to understand the exact method signatures, parameters, and return types for Level 1 direct API calls.

- **codebolt-mcp-access** - Access documentation for MCP (Model Context Protocol) functions and tool execution (`codebolt.tools.executeTool`, `codebolt.tools.getTools`, etc.). Use this skill when you need to understand how to execute MCP tools, list available tools, or build custom MCP servers.
