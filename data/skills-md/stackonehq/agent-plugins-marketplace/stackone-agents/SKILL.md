---
name: stackone-agents
description: Build AI agents that call StackOne-linked accounts using TypeScript SDK, Python SDK, MCP server, or A2A protocol. Use when user asks to "add StackOne tools to my agent", "set up MCP with StackOne", "list employees from BambooHR in my agent", "integrate StackOne with OpenAI", "build a multi-tenant agent", or "use StackOne with LangChain". Supports OpenAI, Vercel AI SDK, Claude, LangChain, CrewAI, PydanticAI. Do NOT use for account linking setup (use stackone-connect) or platform management (use stackone-platform).
license: MIT
compatibility: Requires network access to fetch live documentation. TypeScript SDK requires Node.js and zod>=3.25. Python SDK requires Python 3.9+.
metadata:
  author: stackone
  version: "2.0"
---

# StackOne Agents — AI Integration

## Important

SDK APIs change frequently. Before writing code:
1. For TypeScript: fetch `https://raw.githubusercontent.com/stackoneHQ/stackone-ai-node/refs/heads/main/README.md`
2. For Python: fetch `https://raw.githubusercontent.com/stackoneHQ/stackone-ai-python/refs/heads/main/README.md`
3. For MCP setup: fetch `https://docs.stackone.com/mcp/quickstart`

These sources contain the latest code examples and API surface. Do not rely solely on this skill for code snippets.

## Instructions

### Step 1: Choose an integration method

| Method | Best for | Language |
|--------|----------|----------|
| **TypeScript SDK** (`@stackone/ai`) | Custom agents with OpenAI, Vercel AI, Claude, Claude Agent SDK | TypeScript/JavaScript |
| **Python SDK** (`stackone-ai`) | Custom agents with LangChain, CrewAI, PydanticAI, Google ADK | Python |
| **MCP Server** | Claude Code, Claude Desktop, ChatGPT, Cursor, Windsurf — no code needed | Any (config only) |
| **A2A Protocol** | Agent-to-agent communication | Any |

Consult `references/integration-guide.md` for a detailed decision tree.

### Step 2a: TypeScript SDK path

```bash
npm install @stackone/ai zod
```

```typescript
import { StackOneToolSet } from "@stackone/ai";

// Initialize — reads STACKONE_API_KEY from environment
const toolset = new StackOneToolSet();

// Fetch tools for a specific linked account
const tools = await toolset.fetchTools({
  accountIds: ["account-123"],
});

// Convert to your framework's format
const openaiTools = tools.toOpenAI();           // OpenAI Chat Completions
const anthropicTools = tools.toAnthropic();     // Anthropic Claude
const vercelTools = await tools.toAISDK();      // Vercel AI SDK
```

**Tool naming**: `{provider}_{operation}_{entity}` (e.g., `bamboohr_list_employees`)

**Filtering tools**:
```typescript
const tools = await toolset.fetchTools({
  providers: ["hibob", "bamboohr"],    // Only these providers
  actions: ["*_list_employees"],        // Glob pattern matching
  accountIds: ["account-123"],
});
```

**Utility tools** for dynamic discovery:
```typescript
const utilityTools = await tools.utilityTools();
// tool_search — find tools by natural language query
// tool_execute — execute a discovered tool
```

For framework-specific integration code, fetch the GitHub README — it has complete examples for each framework.

### Step 2b: Python SDK path

```bash
pip install stackone-ai
```

Fetch the Python README for usage examples and framework integrations:
`https://raw.githubusercontent.com/stackoneHQ/stackone-ai-python/refs/heads/main/README.md`

The Python SDK supports: OpenAI, LangChain, CrewAI, PydanticAI, Google ADK.

### Step 2c: MCP Server path (no code required)

StackOne's MCP server is at `https://api.stackone.com/mcp`.

For client-specific setup instructions, fetch the relevant guide:
- Claude Code: `https://docs.stackone.com/mcp/framework-guides/claude-code`
- Claude Desktop: `https://docs.stackone.com/mcp/app-guides/claude-desktop`
- Other clients: fetch `https://docs.stackone.com/llms.txt` and search for the client name

**Testing the MCP connection**:
```bash
npx @modelcontextprotocol/inspector https://api.stackone.com/mcp
```

### Step 3: Handle multi-tenant access

For applications serving multiple customers, each with their own connected accounts:

```typescript
// Option 1: Specify at fetch time
const tools = await toolset.fetchTools({
  accountIds: ["customer-123-bamboohr"],
});

// Option 2: Change dynamically
tools.setAccountId("customer-456-bamboohr");
```

The `accountId` maps to a linked account created via the Connect Session flow (see the `stackone-connect` skill for setup).

## Examples

### Example 1: User wants to add StackOne to an OpenAI agent

User says: "I want my OpenAI agent to list employees from BambooHR"

Actions:
1. Confirm they have a StackOne API key and a linked BambooHR account
2. Install `@stackone/ai` and `zod`
3. Fetch tools with `accountIds` and `actions: ["bamboohr_list_employees"]`
4. Convert with `tools.toOpenAI()` and pass to the OpenAI chat completions call
5. Fetch the TypeScript GitHub README for the complete OpenAI example

Result: Working agent that can query BambooHR employees through StackOne.

### Example 2: User wants to set up MCP with Claude Code

User says: "How do I use StackOne MCP in Claude Code?"

Actions:
1. Fetch `https://docs.stackone.com/mcp/framework-guides/claude-code` for the setup guide
2. Walk through adding the MCP server config with their API key and account ID
3. Test with `npx @modelcontextprotocol/inspector` first

Result: Claude Code can call StackOne tools directly.

### Example 3: User is building a multi-tenant SaaS

User says: "Each of my customers has their own BambooHR. How do I handle that?"

Actions:
1. Explain the account-per-customer model: each customer links their own BambooHR via Connect Sessions
2. Show how to pass the customer's `accountId` when fetching tools
3. Recommend using `toolset.fetchTools({ accountIds: [customerAccountId] })` per request

Result: Understanding of the multi-tenant pattern with code to implement it.

## Troubleshooting

### Error: "Cannot find module 'zod'"
**Cause**: Missing peer dependency.
- `@stackone/ai` requires `zod` version >=3.25.0 <5
- Run `npm install zod` explicitly

### fetchTools returns empty array
**Cause**: No tools match the filter criteria.
- Check that the `accountId` corresponds to an active linked account
- Verify the provider name in `providers` filter matches exactly (e.g., `bamboohr` not `BambooHR`)
- Try without filters first to see all available tools

### MCP server returns 401
**Cause**: Authentication misconfigured.
- MCP uses Basic auth: `Authorization: Basic base64(api_key:)`
- The `x-account-id` header must reference a valid, active linked account
- Test with MCP Inspector to isolate auth vs. config issues

### SDK version mismatch with framework
**Cause**: Breaking changes between SDK versions.
- Always fetch the latest GitHub README for current compatibility
- Pin specific SDK versions in production
- Check the npm/PyPI changelog for migration guides
