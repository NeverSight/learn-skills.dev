---
name: blecsd-ai
description: Build AI/LLM terminal interfaces with @blecsd/ai. Covers streaming conversation UIs, markdown rendering, token tracking, tool call visualization, and agent workflow displays.
license: MIT
metadata:
  author: blecsd
  version: "2.0.0"
---

# @blecsd/ai Package Skill

The `@blecsd/ai` package provides terminal UI widgets for building AI/LLM interfaces. It includes five major widgets for conversations, streaming markdown, token tracking, tool call visualization, and agent workflow displays. All widgets follow blECSd's functional ECS architecture.

**Install:** `pnpm add @blecsd/ai`
**Peer dependency:** `blecsd >= 0.7.0`
**Import:** `import { conversation, streamingMarkdown, tokenTracker, toolUse, agentWorkflow } from '@blecsd/ai'`

## Architecture Rules

All blECSd rules apply: no classes, no `this`, no direct bitecs imports, functional only, early returns. See the `blecsd-tui` skill for core rules.

Each widget follows the namespace pattern: a frozen plain object of pure functions.

## Widgets

### 1. Conversation Widget

Chat-style conversation thread with streaming support.

```typescript
import { conversation } from '@blecsd/ai';

// Create conversation widget
const eid = conversation.createConversation(world, {
  width: 80,
  height: 30,
});

// Add messages
conversation.addMessage(eid, {
  role: 'user',
  content: 'What is ECS?',
});

// Start streaming response
const msgId = conversation.startStreamingMessage(eid, {
  role: 'assistant',
  content: '',
});

// Append chunks as they arrive from the LLM
conversation.appendToMessage(eid, msgId, 'Entity ');
conversation.appendToMessage(eid, msgId, 'Component ');
conversation.appendToMessage(eid, msgId, 'System...');

// End streaming
conversation.endStreamingMessage(eid, msgId);

// Expand/collapse messages
conversation.collapseMessage(eid, msgId);
conversation.expandMessage(eid, msgId);

// Search
const results = conversation.searchMessages(eid, 'ECS');

// Get visible messages for rendering
const visible = conversation.getVisibleMessages(eid);

// Format for display
const display = conversation.formatConversationDisplay(eid, { width: 80 });

// Type check
if (conversation.isConversation(world, eid)) { /* ... */ }
```

**Key functions:**
- `createConversation(world, config)` - Create widget entity
- `addMessage(eid, msg)` - Add user/assistant/system message
- `startStreamingMessage(eid, msg)` - Begin streaming response
- `appendToMessage(eid, msgId, content)` - Append to active stream
- `endStreamingMessage(eid, msgId)` - Finalize stream
- `collapseMessage(eid, msgId)` / `expandMessage(eid, msgId)` - Toggle visibility
- `searchMessages(eid, query)` - Full-text search
- `getVisibleMessages(eid)` - Get visible message list
- `formatConversationDisplay(eid, config)` - Format for terminal output
- `isConversation(world, eid)` - Type guard

### 2. Streaming Markdown Widget

Real-time markdown rendering for terminal display.

```typescript
import { streamingMarkdown } from '@blecsd/ai';

const eid = streamingMarkdown.createStreamingMarkdown(world, {
  width: 80,
  height: 40,
});

// Stream markdown content as it arrives
streamingMarkdown.appendMarkdown(eid, '# Hello\n\n');
streamingMarkdown.appendMarkdown(eid, 'This is **bold** and ');
streamingMarkdown.appendMarkdown(eid, '`code`.\n\n```typescript\n');
streamingMarkdown.appendMarkdown(eid, 'const x = 1;\n```');

// Scroll
streamingMarkdown.scrollMarkdownByLines(eid, 5);   // Scroll down 5 lines
streamingMarkdown.scrollMarkdownToLine(eid, 0);     // Scroll to top

// Parse and render manually
const blocks = streamingMarkdown.parseStreamingBlocks('# Title\n\nParagraph');
const rendered = streamingMarkdown.renderAllBlocks(blocks, 80);

// Inline formatting
const formatted = streamingMarkdown.formatInline('**bold** and *italic*', {});

// Word wrap
const wrapped = streamingMarkdown.wrapText('Long text...', 80);

// Clear state
streamingMarkdown.clearMarkdownState(eid);
```

**Key functions:**
- `createStreamingMarkdown(world, config)` - Create widget
- `appendMarkdown(eid, markdown)` - Stream in content
- `clearMarkdownState(eid)` - Reset content
- `scrollMarkdownByLines(eid, delta)` / `scrollMarkdownToLine(eid, lineNum)` - Navigation
- `parseStreamingBlocks(markdown)` - Parse markdown into blocks
- `renderBlock(block, width)` / `renderAllBlocks(blocks, width)` - Render to strings
- `formatInline(text, styles)` - Format inline elements
- `wrapText(text, width)` - Word wrap

### 3. Token Tracker Widget

Track and display LLM token usage.

```typescript
import { tokenTracker } from '@blecsd/ai';

const eid = tokenTracker.createTokenTracker(world, {
  width: 40,
  height: 10,
});

// Record token usage
tokenTracker.recordTokens(eid, { inputTokens: 100, outputTokens: 200 });
tokenTracker.recordTokens(eid, { inputTokens: 50, outputTokens: 150 });

// Get stats
const stats = tokenTracker.getTokenStats(eid);
// { totalInput, totalOutput, totalTokens, requestCount, avgInput, avgOutput }

// Format for display
const display = tokenTracker.formatTokenDisplay(stats, { width: 40 });

// Reset
tokenTracker.resetTokenState(eid);
```

**Key functions:**
- `createTokenTracker(world, config)` - Create tracker widget
- `recordTokens(eid, { inputTokens, outputTokens })` - Record usage
- `getTokenStats(eid)` - Get aggregated statistics
- `formatTokenDisplay(stats, config)` - Format for terminal
- `resetTokenState(eid)` - Reset counters
- `isTokenTracker(world, eid)` - Type guard

### 4. Tool Use Widget

Visualize AI agent tool/function calls.

```typescript
import { toolUse } from '@blecsd/ai';

const eid = toolUse.createToolUse(world, {
  width: 80,
  height: 30,
});

// Add a tool call
const callId = toolUse.addToolCall({
  toolName: 'search',
  params: { query: 'ECS architecture' },
});

// Update status
toolUse.updateToolCallStatus(callId, 'running');
toolUse.updateToolCallStatus(callId, 'complete');

// Or set error
toolUse.setToolCallError(callId, 'Connection timeout');

// Expand/collapse details
toolUse.toggleToolCallExpand(callId);

// Get execution time
const duration = toolUse.getToolCallDuration(callId);

// Get timeline of all calls
const timeline = toolUse.getToolCallTimeline();

// Format for display
const display = toolUse.formatToolCallDisplay(timeline[0], { width: 80 });
```

**Key functions:**
- `createToolUse(world, config)` - Create widget
- `addToolCall({ toolName, params })` - Add new call
- `updateToolCallStatus(callId, status)` - Update status ('pending'|'running'|'complete'|'error')
- `setToolCallError(callId, error)` - Set error message
- `toggleToolCallExpand(callId)` - Expand/collapse details
- `getToolCallDuration(callId)` - Get execution duration
- `getToolCallTimeline()` - Get all calls in order
- `formatToolCallDisplay(call, config)` - Format for terminal

### 5. Agent Workflow Widget

Visualize multi-step agent workflows with hierarchy.

```typescript
import { agentWorkflow } from '@blecsd/ai';

const eid = agentWorkflow.createAgentWorkflow(world, {
  width: 80,
  height: 30,
});

// Add workflow steps (supports hierarchy via parentId)
agentWorkflow.addWorkflowStep({
  id: 'plan',
  label: 'Planning',
  status: 'complete',
  parentId: null,
});

agentWorkflow.addWorkflowStep({
  id: 'research',
  label: 'Research',
  status: 'running',
  parentId: 'plan',
});

agentWorkflow.addWorkflowStep({
  id: 'implement',
  label: 'Implementation',
  status: 'pending',
  parentId: null,
});

// Update step
agentWorkflow.updateWorkflowStep('research', { status: 'complete' });

// Collapse/expand
agentWorkflow.toggleWorkflowCollapse('plan');

// Query
const visible = agentWorkflow.getVisibleSteps(eid);
const children = agentWorkflow.getStepChildren('plan');
const depth = agentWorkflow.getStepDepth('research');
const duration = agentWorkflow.getStepDuration('plan');
const stats = agentWorkflow.getWorkflowStats(eid);

// Format
const display = agentWorkflow.formatWorkflowDisplay(eid, { width: 80 });
const durationStr = agentWorkflow.formatDuration(12345); // "12.3s"
```

**Key functions:**
- `createAgentWorkflow(world, config)` - Create widget
- `addWorkflowStep({ id, label, status, parentId })` - Add step
- `updateWorkflowStep(stepId, updates)` - Update step status/label
- `toggleWorkflowCollapse(stepId)` - Expand/collapse
- `getVisibleSteps(eid)` - Get visible steps (respecting collapse)
- `getStepChildren(stepId)` / `getStepDepth(stepId)` / `getStepDuration(stepId)` - Query
- `getWorkflowStats(eid)` - Get workflow statistics
- `formatWorkflowDisplay(eid, config)` / `formatDuration(ms)` - Format for display

## Store Management

Each widget has store cleanup functions for testing:

```typescript
import {
  resetConversationStore,
  resetStreamingMarkdownStore,
  resetTokenTrackerStore,
  resetToolUseStore,
  resetWorkflowStore,
} from '@blecsd/ai';

// Call in test teardown
afterEach(() => {
  resetConversationStore();
  resetToolUseStore();
});
```

## Best Practices

1. **Always end streaming messages.** Call `endStreamingMessage` when the LLM stream completes to finalize state.
2. **Use namespaces for API discoverability.** `conversation.createConversation` is clearer than a bare `createConversation` import.
3. **Reset stores in tests.** Each widget maintains internal state maps. Always reset in `afterEach`.
4. **Handle streaming errors gracefully.** If the LLM stream errors, call `endStreamingMessage` anyway, then update the message content with an error indicator.
5. **Token tracking is cumulative.** Call `resetTokenState` to start fresh counting.
6. **Workflow steps support nesting.** Use `parentId` to create hierarchical step trees.
