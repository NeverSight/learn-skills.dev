---
name: morph-warpgrep
description: Integration guide for Morph's WarpGrep (fast agentic code search) and Fast Apply (10,500 tok/s code editing). Use when building coding agents that need fast, accurate code search or need to apply AI-generated edits to code efficiently. Particularly useful for large codebases, deep logic queries, bug tracing, and code path analysis.
---

# Morph WarpGrep & Fast Apply

Morph provides two tools that significantly improve coding agent performance:

- **WarpGrep**: Agentic code search that's 5x faster than regular search, uses parallel tool calls, achieves 0.73 F1 in ~4 steps
- **Fast Apply**: Merges AI edits into code at 10,500 tok/s with 98% accuracy (2x faster than search-replace)

## Prerequisites

1. Get a Morph API key from https://www.morphllm.com/dashboard
2. Set environment variable:

```bash
export MORPH_API_KEY="your-api-key"
```

3. Install the Morph SDK:

```bash
bun add @morphllm/morphsdk
# or
npm install @morphllm/morphsdk
```

4. Ensure `ripgrep` is installed (required for local search):

```bash
# macOS
brew install ripgrep

# Ubuntu/Debian  
sudo apt install ripgrep

# Verify installation
rg --version
```

## Quick Test

After setup, run the included test script on any local repository:

```bash
# Clone a test repo (or use any existing codebase)
git clone https://github.com/letta-ai/letta-code.git test-repo

# Install SDK
cd test-repo
bun add @morphllm/morphsdk

# Run test script
export MORPH_API_KEY="your-key"
bun ../scripts/test-warpgrep.ts .
```

Expected output:
```
======================================================================
MORPH WARPGREP TEST
======================================================================
Repo: .
SDK: @morphllm/morphsdk
======================================================================

| Query                              | Result | Time   | Files |
|------------------------------------|--------|--------|-------|
| Find the main entry point          | ✅     | 5.2s   | 2     |
| Find authentication logic          | ✅     | 4.1s   | 4     |
| Find where configuration is handled | ✅     | 3.8s   | 3     |
| Find error handling patterns       | ✅     | 4.5s   | 5     |

======================================================================
Results: 4 passed, 0 failed
======================================================================
```

---

## When to Use

### Use WarpGrep When:
- Searching large codebases (1000+ files)
- Deep logic queries: bug tracing, code paths, control flow analysis
- Need to find relevant context without polluting the context window
- Regular grep returns too many irrelevant results

### Use Fast Apply When:
- Applying AI-generated code edits to existing files
- Need reliable edit merging (98% accuracy vs ~70% for search-replace)
- Working with large files where diff formats fail

### Don't Use When:
- Simple exact-match searches (regular `grep`/`rg` is free and fast enough)
- Surface-level queries where semantic search suffices
- Cost is a major concern (Morph API has usage costs)

---

## Quick Start: WarpGrep

### Basic Usage

```typescript
import { MorphClient } from '@morphllm/morphsdk';

const morph = new MorphClient({ apiKey: process.env.MORPH_API_KEY });

const result = await morph.warpGrep.execute({
  query: 'Find authentication middleware',
  repoRoot: '.'
});

if (result.success) {
  for (const ctx of result.contexts) {
    console.log(`File: ${ctx.file}`);
    console.log(ctx.content);
  }
} else {
  console.error('Search failed');
}
```

### Response Format

```typescript
interface WarpGrepResult {
  success: boolean;
  contexts: Array<{
    file: string;    // File path relative to repo root
    content: string; // File content with relevant code
  }>;
  summary?: string;  // Human-readable summary
}
```

### Using as an Agent Tool

```typescript
import { MorphClient } from '@morphllm/morphsdk';
import Anthropic from '@anthropic-ai/sdk';

const morph = new MorphClient({ apiKey: process.env.MORPH_API_KEY });
const anthropic = new Anthropic();

// Define WarpGrep as a tool
const tools = [{
  name: 'warpgrep_search',
  description: 'Search codebase for relevant code. Use for finding implementations, tracing bugs, or understanding code flow.',
  input_schema: {
    type: 'object',
    properties: {
      query: { type: 'string', description: 'What to search for' }
    },
    required: ['query']
  }
}];

// Handle tool calls
async function handleToolCall(name: string, input: { query: string }) {
  if (name === 'warpgrep_search') {
    const result = await morph.warpGrep.execute({
      query: input.query,
      repoRoot: process.cwd()
    });
    
    if (result.success) {
      return result.contexts.map(c => `## ${c.file}\n${c.content}`).join('\n\n');
    }
    return 'No results found';
  }
}
```

---

## Quick Start: Fast Apply

Fast Apply merges AI-generated edits into existing code:

```typescript
import { MorphClient } from '@morphllm/morphsdk';

const morph = new MorphClient({ apiKey: process.env.MORPH_API_KEY });

const result = await morph.fastApply.apply({
  originalCode: `function divide(a, b) {
  return a / b;
}`,
  editSnippet: `function divide(a, b) {
  if (b === 0) throw new Error("Division by zero");
  return a / b;
}`
});

console.log(result.mergedCode);
```

### Direct API (Alternative)

```typescript
const response = await fetch('https://api.morphllm.com/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.MORPH_API_KEY}`
  },
  body: JSON.stringify({
    model: 'morph-v3-fast',  // or 'morph-v3-large' for complex edits
    messages: [{
      role: 'user',
      content: `<instruction>Add error handling</instruction>
<code>function divide(a, b) { return a / b; }</code>
<update>function divide(a, b) {
  if (b === 0) throw new Error("Division by zero");
  return a / b;
}</update>`
    }],
    temperature: 0
  })
});

const data = await response.json();
const mergedCode = data.choices[0].message.content;
```

---

## Tested Results

Tested on the [letta-code](https://github.com/letta-ai/letta-code) repository (~300 TypeScript files) using SDK v0.2.103:

| Query | Result | Time | Files Found |
|-------|--------|------|-------------|
| "Find authentication logic" | ✅ | 4.2s | `src/auth/oauth.ts`, `src/auth/setup.ts`, +2 |
| "Find the main CLI entry point" | ✅ | 5.8s | `src/index.ts`, `src/cli/App.tsx` |
| "Find where models are configured" | ✅ | 3.1s | `src/agent/model.ts`, `src/models.json`, +1 |
| "Find how memory blocks work" | ✅ | 3.9s | `src/agent/memory.ts`, `src/agent/memoryFilesystem.ts`, +1 |
| "Find the settings manager" | ✅ | 2.9s | `src/settings-manager.ts`, `src/settings.ts` |

**5/5 tests passed**

### Performance Summary

- **Average time**: 4.0 seconds
- **Token efficiency**: 39% fewer input tokens vs manual search
- **Accuracy**: Finds relevant code in 2-4 turns

---

## How WarpGrep Works

WarpGrep is an agentic search that runs up to 4 turns:

```
┌─────────────────────────────────────────────────────────────┐
│  Turn 1: Analyze query, map repo structure, initial search  │
├─────────────────────────────────────────────────────────────┤
│  Turn 2-3: Refine search, read specific files               │
├─────────────────────────────────────────────────────────────┤
│  Turn 4: Return all relevant code locations                 │
└─────────────────────────────────────────────────────────────┘
```

The SDK handles the multi-turn conversation automatically, executing local tools:

| Tool | Description | Implementation |
|------|-------------|----------------|
| `grep` | Regex search across files | Uses ripgrep (`rg`) |
| `read` | Read file contents | Local filesystem |
| `list_dir` | Show directory structure | Local filesystem |

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Your Code / Agent                         │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│              @morphllm/morphsdk                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 1. Build repo structure                                 │ │
│  │ 2. Send query to Morph API                              │ │
│  │ 3. Execute local tools (grep, read, list_dir)           │ │
│  │ 4. Multi-turn refinement                                │ │
│  │ 5. Return relevant code contexts                        │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────┬───────────────────────────────────┘
                           │
            ┌──────────────┴──────────────┐
            ▼                             ▼
┌───────────────────────┐    ┌───────────────────────┐
│    Morph API          │    │   Local Filesystem    │
│  (morph-warp-grep-v1) │    │   (ripgrep, fs)       │
└───────────────────────┘    └───────────────────────┘
```

---

## Morph's Benchmarks

From Morph's SWE-bench evaluation with Claude 4.5 Opus:

| Metric | Without WarpGrep | With WarpGrep | Improvement |
|--------|------------------|---------------|-------------|
| Input Tokens | 14K | 9K | **39% fewer** |
| Agent Turns | 35.0 | 26.0 | **26% fewer** |
| Tasks Solved | 74.4% | 81.9% | **10% more** |

Source: [Morph WarpGrep Benchmarks](https://www.morphllm.com/benchmarks/warp-grep)

---

## Common Patterns

### Reconnaissance-Then-Action

```typescript
import { MorphClient } from '@morphllm/morphsdk';

const morph = new MorphClient({ apiKey: process.env.MORPH_API_KEY });

// 1. Search for relevant code
const result = await morph.warpGrep.execute({
  query: 'Where is the payment processing logic?',
  repoRoot: '.'
});

// 2. Use found contexts to inform next steps
if (result.success) {
  const relevantFiles = result.contexts.map(c => c.file);
  console.log('Found relevant files:', relevantFiles);
  // Now read/edit these specific files
}
```

### Combining WarpGrep + Fast Apply

```typescript
import { MorphClient } from '@morphllm/morphsdk';

const morph = new MorphClient({ apiKey: process.env.MORPH_API_KEY });

// 1. Find the code to modify
const search = await morph.warpGrep.execute({
  query: 'Find the user validation function',
  repoRoot: '.'
});

if (search.success && search.contexts.length > 0) {
  const targetFile = search.contexts[0];
  
  // 2. Apply an edit
  const result = await morph.fastApply.apply({
    originalCode: targetFile.content,
    editSnippet: '// Add your modified version here'
  });
  
  console.log(result.mergedCode);
}
```

---

## MCP Integration

For personal use with Claude Code, Cursor, or other MCP clients:

```bash
# Install MCP server
claude mcp add morph --scope user -e MORPH_API_KEY=YOUR_API_KEY --npx -y @morphllm/morphmcp
```

This adds a `warpgrep_codebase_search` tool to your MCP client.

---

## Troubleshooting

### ripgrep Not Found

```bash
# Install ripgrep
brew install ripgrep  # macOS
sudo apt install ripgrep  # Ubuntu/Debian

# Verify
rg --version
```

### API Key Issues

```bash
# Verify API key works
curl -X POST https://api.morphllm.com/v1/chat/completions \
  -H "Authorization: Bearer $MORPH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"morph-v3-fast","messages":[{"role":"user","content":"test"}]}'
```

### SDK Version Issues

Ensure you're using the latest SDK:

```bash
bun add @morphllm/morphsdk@latest
# or
npm install @morphllm/morphsdk@latest
```

---

## Cost Considerations

- WarpGrep uses **1-4 API calls** per search (typically 2-3)
- Fast Apply uses **1 API call** per edit
- Pricing: $0.80 per 1M tokens (input and output)
- Monitor usage via [Morph Dashboard](https://www.morphllm.com/dashboard)
- Use regular grep/ripgrep for simple exact-match searches (free)

---

## Resources

- [Morph Documentation](https://docs.morphllm.com)
- [WarpGrep Guide](https://docs.morphllm.com/sdk/components/warp-grep)
- [WarpGrep Benchmarks](https://www.morphllm.com/benchmarks/warp-grep)
- [Fast Apply Benchmarks](https://www.morphllm.com/benchmarks/fast-apply)
- [Morph Dashboard](https://www.morphllm.com/dashboard)
- [Morph Discord](https://discord.gg/AdXta4yxEK)
