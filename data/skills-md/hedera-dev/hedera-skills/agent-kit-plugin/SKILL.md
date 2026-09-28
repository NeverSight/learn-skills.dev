---
name: agent-kit-plugin
description: This skill should be used when the user asks to "create a hedera plugin", "build a hedera agent kit plugin", "extend hedera agent kit", "create custom hedera tools", "add hedera functionality", "write a hedera tool", "implement hedera tool", or needs guidance on Hedera Agent Kit plugin architecture, tool definitions, mutation tools, query tools, or parameter schemas using Zod.
version: 2.0.0
---

# Creating Hedera Agent Kit Plugins

This skill provides guidance for creating custom plugins that extend the Hedera Agent Kit. Plugins allow adding new tools for Hedera network interactions—token operations, account management, consensus service, smart contracts, and custom integrations.

## Quick Start

To create a Hedera plugin in 5 steps:

1. **Install dependencies**: Set up a TypeScript project with `@hashgraph/hedera-agent-kit` and `@hiero-ledger/sdk`
2. **Create plugin structure**: Create an `index.ts` with the plugin definition and a `tools/` directory
3. **Define tools**: Each tool is a class extending `BaseTool` — this opts the tool into the hooks/policies lifecycle
4. **Export properly**: Export the plugin object and tool name constants
5. **Register with agent**: Import and pass the plugin in the toolkit `configuration.plugins` array

## Plugin Interface

Every Hedera plugin implements this interface from `@hashgraph/hedera-agent-kit`:

```typescript
import { Plugin } from '@hashgraph/hedera-agent-kit';

export interface Plugin {
  name: string;           // Unique kebab-case identifier
  version?: string;       // Semantic version (e.g., "1.0.0")
  description?: string;   // Brief explanation of plugin purpose
  tools: (context: Context) => Tool[];  // Factory returning tools
}
```

The `tools` function receives a `Context` object containing network configuration and returns an array of `Tool` objects. `BaseTool` itself implements `Tool`, so a `BaseTool` subclass instance is a valid return value.

## `BaseTool`

Tools are written as classes extending `BaseTool`, which implements `Tool` and runs a 7-stage lifecycle:

```text
[1] preToolExecutionHook
[2] normalizeParams        ← your logic
[3] postParamsNormalizationHook
[4] coreAction             ← your logic
[5] postCoreActionHook
[6] secondaryAction        ← your logic (skipped via shouldSecondaryAction for queries)
[7] postToolExecutionHook
```

Hooks and policies registered on the agent kit fire at stages 1, 3, 5, and 7 automatically — you never call them manually.

A subclass must provide:

| Member | Type | Notes |
|---|---|---|
| `method` | `string` | Snake-case identifier with `_tool` suffix |
| `name` | `string` | Human-readable display name |
| `description` | `string` | LLM-facing description (typically built in the constructor from a prompt function) |
| `parameters` | `z.ZodObject` | Zod schema for input validation |
| `normalizeParams(params, context, client)` | async | Stage 2 — resolve defaults, validate format |
| `coreAction(normalised, context, client)` | async | Stage 4 — build the transaction or perform the query |
| `secondaryAction(request, client, context)` | async | Stage 6 — sign/submit the transaction (no-op for queries) |

Optional overrides: `outputParser`, `shouldSecondaryAction` (return `false` for query-only tools), `handleError`, and the four hook methods.

### Tool Types

**Mutation tools** — state-changing operations (token create/mint/transfer, account update, topic submit). `coreAction` builds the `Transaction`, `secondaryAction` calls `handleTransaction()`. Use `transactionToolOutputParser`.

**Query tools** — read-only operations (token info, balances, mirror-node fetches). `coreAction` returns the result directly. Override `shouldSecondaryAction` to return `false`. Use `untypedQueryOutputParser`.

## File Structure Pattern

Follow this structure for all Hedera plugins:

```
my-hedera-plugin/
├── index.ts                    # Plugin definition and exports
└── tools/
    └── category/               # Group related tools
        ├── create-something.ts
        └── get-something.ts
```

## Creating a Tool

### Step 1: Define the Tool Constant

```typescript
export const MY_TOOL_NAME = 'my_tool_name_tool';
```

Use UPPER_SNAKE_CASE with `_TOOL` suffix for the constant. The value should be lowercase snake_case.

### Step 2: Create the Prompt Function

```typescript
const myToolPrompt = (context: Context = {}) => {
  return `This tool does X on Hedera.
Parameters:
- param1 (str, required): Description of param1
- param2 (int, optional): Description of param2, defaults to 0`;
};
```

### Step 3: Define Parameters with Zod

```typescript
import { z } from 'zod';

const myToolParameters = (_context: Context = {}) => {
  return z.object({
    param1: z.string().describe('Description of param1'),
    param2: z.number().optional().describe('Description of param2'),
  });
};

type MyToolParams = z.infer<ReturnType<typeof myToolParameters>>;
```

See `references/zod-schema-patterns.md` for common Hedera parameter patterns.

### Step 4: Implement the BaseTool subclass (mutation example)

```typescript
import { Client, Status } from '@hiero-ledger/sdk';
import {
  BaseTool,
  Context,
  handleTransaction,
  RawTransactionResponse,
  transactionToolOutputParser,
} from '@hashgraph/hedera-agent-kit';

const postProcess = (response: RawTransactionResponse) =>
  `Operation completed.
Transaction ID: ${response.transactionId}`;

export class MyTool extends BaseTool<MyToolParams, MyToolParams> {
  method = MY_TOOL_NAME;
  name = 'My Tool Display Name';
  description: string;
  parameters: ReturnType<typeof myToolParameters>;
  outputParser = transactionToolOutputParser;

  constructor(context: Context) {
    super();
    this.description = myToolPrompt(context);
    this.parameters = myToolParameters(context);
  }

  // Stage 2 — resolve defaults
  async normalizeParams(params: MyToolParams) {
    return params;
  }

  // Stage 4 — build the transaction (do not sign here)
  async coreAction(params: MyToolParams, _context: Context, _client: Client) {
    // return new SomeTransaction()...;
    return undefined as any;
  }

  // Stage 6 — sign and submit
  async secondaryAction(transaction: any, client: Client, context: Context) {
    return handleTransaction(transaction, client, context, postProcess);
  }

  async handleError(error: unknown) {
    const message = 'Failed to execute' + (error instanceof Error ? `: ${error.message}` : '');
    console.error(`[${MY_TOOL_NAME}]`, message);
    return { raw: { status: Status.InvalidTransaction, error: message }, humanMessage: message };
  }
}
```

### Step 5: Export a Factory

```typescript
const tool = (context: Context): BaseTool => new MyTool(context);
export default tool;
```

The factory pattern lets the plugin's `tools(context)` function instantiate a fresh tool per request with the right context bound.

### Query-tool variant — skip stage 6

For read-only tools, override `shouldSecondaryAction` so the lifecycle stops after `coreAction`, and have `secondaryAction` pass the result through unchanged:

```typescript
export class MyQueryTool extends BaseTool<MyToolParams, MyToolParams> {
  // ... method/name/description/parameters as above ...
  outputParser = untypedQueryOutputParser;

  async normalizeParams(params: MyToolParams) {
    return params;
  }

  async coreAction(params: MyToolParams, _context: Context, client: Client) {
    return await someHederaQuery(params, client);
  }

  async shouldSecondaryAction() {
    return false;
  }

  async secondaryAction(result: any) {
    return result;
  }
}
```

## Creating the Plugin Index

```typescript
import { Context, Plugin } from '@hashgraph/hedera-agent-kit';
import myTool, { MY_TOOL_NAME } from './tools/category/my-tool';

export const myPlugin: Plugin = {
  name: 'my-hedera-plugin',
  version: '1.0.0',
  description: 'A plugin for custom Hedera operations',
  tools: (context: Context) => {
    return [
      myTool(context),
    ];
  },
};

export const myPluginToolNames = {
  MY_TOOL_NAME,
} as const;

export default { myPlugin, myPluginToolNames };
```

## Post-Processing Results

`secondaryAction` typically delegates to `handleTransaction`, which calls a `postProcess` function with the raw transaction response:

```typescript
const postProcess = (response: RawTransactionResponse) => {
  if (response.scheduleId) {
    return `Scheduled transaction created.
Transaction ID: ${response.transactionId}
Schedule ID: ${response.scheduleId.toString()}`;
  }
  return `Operation completed.
Transaction ID: ${response.transactionId}`;
};
```

## `RETURN_BYTES` mode — `raw.bytes` is a `Uint8Array`

When a tool runs in `RETURN_BYTES` mode, `raw.bytes` returned by `ResponseParserService` is always a plain `Uint8Array` in both Node.js and browser environments. Pass it directly to `Transaction.fromBytes()` — no manual conversion is needed.

```typescript
const bytes = toolCall.parsedData.raw.bytes;
const tx = Transaction.fromBytes(bytes);
```

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Plugin name | kebab-case | `my-token-plugin` |
| Plugin variable | camelCase | `myTokenPlugin` |
| Tool class | PascalCase + `Tool` | `CreateTokenTool` |
| Tool constant | UPPER_SNAKE_CASE + `_TOOL` | `CREATE_TOKEN_TOOL` |
| Tool method value | snake_case + `_tool` | `create_token_tool` |
| Tool file | kebab-case | `create-token.ts` |
| Tool names export | camelCase + `ToolNames` | `myTokenPluginToolNames` |

## Common Imports

```typescript
// From @hashgraph/hedera-agent-kit (core)
import {
  Context,
  Plugin,
  BaseTool,
  handleTransaction,
  RawTransactionResponse,
  transactionToolOutputParser,
  untypedQueryOutputParser,
} from '@hashgraph/hedera-agent-kit';

// Built-in plugins live in the /plugins subpath
import { coreTokenPlugin, coreAccountPlugin } from '@hashgraph/hedera-agent-kit/plugins';

// Hedera SDK is a peer dependency
import { Client, Status } from '@hiero-ledger/sdk';

// For parameter validation
import { z } from 'zod';
```

## Additional Resources

### Reference Files

For detailed patterns and techniques, consult:
- **`references/plugin-interface.md`** - Plugin interface, `BaseTool` lifecycle in depth
- **`references/zod-schema-patterns.md`** - Common Zod schemas for Hedera parameters
- **`references/prompt-patterns.md`** - Prompt generation patterns for tool descriptions
- **`references/error-handling.md`** - Error handling and output parsing patterns

### Example Files

Working examples in `examples/`:
- **`examples/simple-plugin/`** - Minimal `BaseTool` query (starter template)
- **`examples/token-plugin/`** - Mutation (`CreateTokenTool`) and query (`GetTokenInfoTool`) `BaseTool` subclasses

## Best Practices

1. **One file per tool**, named after the tool in kebab-case
2. **Group related tools** under category directories in `tools/`
3. **Stable class names**: `<DoesWhat>Tool` (e.g., `CreateTokenTool`)
4. **Resolve defaults in `normalizeParams`**, not in `coreAction` — keeps the build step pure
5. **Build, don't submit, in `coreAction`** — submission belongs in `secondaryAction` where hooks can react
6. **Override `handleError`** so logs are tagged with the tool method
7. **Validate with Zod's `.describe()`** — every field; descriptions guide the agent
8. **Export tool name constants** so consumers can reference tools programmatically

## Registering a Plugin with a Toolkit

Plugins are passed explicitly to the toolkit you choose. Toolkits live in dedicated packages — pick the one that matches your framework:

| Framework | Toolkit package |
|---|---|
| LangChain | `@hashgraph/hedera-agent-kit-langchain` |
| Vercel AI SDK | `@hashgraph/hedera-agent-kit-ai-sdk` |
| ElizaOS | `@hashgraph/hedera-agent-kit-elizaos` |
| MCP | `@hashgraph/hedera-agent-kit-mcp` |

> **Empty `plugins` array means zero tools.** List every plugin you need explicitly, or use `allCorePlugins` from the `/plugins` subpath to load every built-in core plugin at once.

```typescript
import { Client, PrivateKey } from '@hiero-ledger/sdk';
import { AgentMode } from '@hashgraph/hedera-agent-kit';
import { coreTokenPlugin, coreAccountPlugin } from '@hashgraph/hedera-agent-kit/plugins';
import { HederaLangchainToolkit } from '@hashgraph/hedera-agent-kit-langchain';
import { myPlugin } from './my-hedera-plugin';

const client = Client.forTestnet().setOperator(
  process.env.ACCOUNT_ID!,
  PrivateKey.fromStringECDSA(process.env.PRIVATE_KEY!),
);

const toolkit = new HederaLangchainToolkit({
  client,
  configuration: {
    plugins: [coreTokenPlugin, coreAccountPlugin, myPlugin],
    context: { mode: AgentMode.AUTONOMOUS },
  },
});

const tools = toolkit.getTools();
```

To load every built-in core plugin at once, import `allCorePlugins`:

```typescript
import { allCorePlugins } from '@hashgraph/hedera-agent-kit/plugins';
// ...
plugins: [...allCorePlugins, myPlugin],
```

## Workflow Summary

1. Create plugin directory with `index.ts` and `tools/` subdirectory
2. For each tool, write a `BaseTool` subclass and a factory function in its own file
3. Export tools from `index.ts` along with tool name constants
4. Pass the plugin in the toolkit's `configuration.plugins` array
5. Tools become available to the AI agent

For complete working examples, see the `examples/` directory.
