---
name: devic-ui
description: Devic UI is a react component library to integrate AI UI components like chats and agents executions handler directly in your code base connected to devicai API
---

# Devic UI Integration Guide

This guide explains how to integrate the `@devicai/ui` library into your React application to add AI assistant chat capabilities.

## Prerequisites

- Node.js 20+
- React 17+ application
- Devic API key (obtain from Devic dashboard)

## Installation

```bash
npm install @devicai/ui
# or
yarn add @devicai/ui
# or
pnpm add @devicai/ui
```

## Basic Integration

### Step 1: Import Styles

Add the CSS import to your application entry point:

```tsx
// App.tsx or index.tsx
import '@devicai/ui/styles.css';
```

### Step 2: Wrap Your App with DevicProvider

```tsx
import { DevicProvider } from '@devicai/ui';

function App() {
  return (
    <DevicProvider
      apiKey="your-devic-api-key"
      baseUrl="https://api.devic.ai"  // Optional, defaults to this
    >
      <YourApp />
    </DevicProvider>
  );
}
```

### Step 3: Add ChatDrawer Component

```tsx
import { ChatDrawer } from '@devicai/ui';

function YourApp() {
  return (
    <div>
      {/* Your app content */}

      <ChatDrawer
        assistantId="your-assistant-identifier"
        options={{
          position: 'right',
          welcomeMessage: 'Hello! How can I help you today?',
          suggestedMessages: [
            'Help me get started',
            'What can you do?',
          ],
        }}
      />
    </div>
  );
}
```

## Multi-Tenant Integration

For SaaS applications with multiple tenants:

```tsx
<DevicProvider
  apiKey="your-api-key"
  tenantId="global-tenant-id"
  tenantMetadata={{ organizationId: 'org-123' }}
>
  <ChatDrawer
    assistantId="support-assistant"
    tenantId="specific-tenant-override"  // Overrides provider
    tenantMetadata={{
      userId: 'user-456',
      plan: 'enterprise'
    }}
  />
</DevicProvider>
```

## Client-Side Tools (Model Interface Protocol)

Enable the assistant to call functions in your application:

```tsx
import { ChatDrawer, ModelInterfaceTool } from '@devicai/ui';

// Define client-side tools
const tools: ModelInterfaceTool[] = [
  {
    toolName: 'get_user_location',
    schema: {
      type: 'function',
      function: {
        name: 'get_user_location',
        description: 'Get the current user geographic location',
        parameters: {
          type: 'object',
          properties: {},
        },
      },
    },
    callback: async () => {
      return new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
          (pos) => resolve({
            latitude: pos.coords.latitude,
            longitude: pos.coords.longitude,
          }),
          (err) => reject(new Error(err.message))
        );
      });
    },
  },
  {
    toolName: 'get_current_page',
    schema: {
      type: 'function',
      function: {
        name: 'get_current_page',
        description: 'Get the current page URL and title',
        parameters: {
          type: 'object',
          properties: {},
        },
      },
    },
    callback: async () => ({
      url: window.location.href,
      title: document.title,
      pathname: window.location.pathname,
    }),
  },
  {
    toolName: 'navigate_to_page',
    schema: {
      type: 'function',
      function: {
        name: 'navigate_to_page',
        description: 'Navigate the user to a specific page',
        parameters: {
          type: 'object',
          properties: {
            path: {
              type: 'string',
              description: 'The path to navigate to',
            },
          },
          required: ['path'],
        },
      },
    },
    callback: async ({ path }) => {
      window.location.href = path;
      return { success: true, navigatedTo: path };
    },
  },
];

function App() {
  return (
    <ChatDrawer
      assistantId="my-assistant"
      modelInterfaceTools={tools}
      onToolCall={(toolName, params) => {
        console.log(`Tool called: ${toolName}`, params);
      }}
    />
  );
}
```

## Custom Chat UI with Hooks

Build a completely custom chat interface:

```tsx
import { useDevicChat } from '@devicai/ui';

function CustomChat() {
  const {
    messages,
    isLoading,
    status,
    error,
    sendMessage,
    clearChat,
  } = useDevicChat({
    assistantId: 'my-assistant',
    onMessageReceived: (message) => {
      console.log('New message:', message);
    },
    onError: (error) => {
      console.error('Chat error:', error);
    },
  });

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const message = formData.get('message') as string;
    if (message.trim()) {
      sendMessage(message);
      e.currentTarget.reset();
    }
  };

  return (
    <div className="custom-chat">
      <div className="messages">
        {messages.map((msg) => (
          <div key={msg.uid} className={`message ${msg.role}`}>
            <strong>{msg.role}:</strong>
            <p>{msg.content.message}</p>
          </div>
        ))}
        {isLoading && <div className="loading">Thinking...</div>}
        {error && <div className="error">{error.message}</div>}
      </div>

      <form onSubmit={handleSubmit}>
        <input
          name="message"
          placeholder="Type a message..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          Send
        </button>
      </form>

      <button onClick={clearChat}>Clear Chat</button>
    </div>
  );
}
```

## File Uploads

Enable file attachments in chat:

```tsx
<ChatDrawer
  assistantId="document-assistant"
  options={{
    enableFileUploads: true,
    allowedFileTypes: {
      images: true,
      documents: true,
      audio: false,
      video: false,
    },
    maxFileSize: 10 * 1024 * 1024, // 10MB
  }}
/>
```

## Display Modes

ChatDrawer supports two display modes via the `mode` prop:

### Drawer Mode (default)

Renders as an overlay panel with a floating trigger button. Can be toggled open/closed.

```tsx
<ChatDrawer
  mode="drawer"
  assistantId="my-assistant"
  options={{
    position: 'right',
    defaultOpen: false,
    zIndex: 1000,
  }}
/>
```

### Inline Mode

Renders embedded in the page layout, always visible, no trigger button or toggle behavior.

```tsx
<ChatDrawer
  mode="inline"
  assistantId="my-assistant"
  options={{
    width: 400,
    borderRadius: 12,
  }}
/>
```

## Resizable Drawer

Enable drag-to-resize with width constraints:

```tsx
<ChatDrawer
  assistantId="my-assistant"
  options={{
    resizable: true,
    width: 400,
    minWidth: 300,
    maxWidth: 800,
    position: 'right', // resize handle appears on the opposite edge
  }}
/>
```

## Custom Rendering

### Custom Loading Indicator

```tsx
<ChatDrawer
  assistantId="my-assistant"
  options={{
    loadingIndicator: <MySpinner />,
  }}
/>
```

### Custom Send Button

The click handler is managed by an overlay, so the node doesn't need to handle click events.

```tsx
<ChatDrawer
  assistantId="my-assistant"
  options={{
    sendButtonContent: <MyCustomIcon />,
  }}
/>
```

### Custom Tool Renderers

Replace the default tool call summary with custom UI per tool name:

```tsx
<ChatDrawer
  assistantId="my-assistant"
  options={{
    toolRenderers: {
      search_products: (input, output) => (
        <ProductGrid products={output.results} query={input.query} />
      ),
    },
    toolIcons: {
      search_products: <SearchIcon />,
    },
  }}
/>
```

### Tool Groups (Grouped Tool Call Rendering)

Group consecutive tool calls into a single unified renderer. Useful for rendering sequences of related tool calls (e.g., terminal commands + file reads) as a cohesive UI block.

```tsx
import { ChatDrawer, ToolGroupCall, ToolGroupConfig } from '@devicai/ui';

const toolGroups: ToolGroupConfig[] = [
  {
    tools: ['run_terminal_command', 'read_sandbox_file'],
    renderer: (calls: ToolGroupCall[]) => (
      <div className="terminal-trace">
        {calls.map((call) => (
          <div key={call.toolCallId} className="trace-entry">
            <code>{call.name}</code>
            <pre>{JSON.stringify(call.input, null, 2)}</pre>
            {call.output && <pre className="output">{JSON.stringify(call.output)}</pre>}
          </div>
        ))}
      </div>
    ),
  },
];

<ChatDrawer
  assistantId="my-assistant"
  options={{
    toolGroups,
    // toolRenderers still works for non-grouped tools
    toolRenderers: {
      search_web: (input, output) => <SearchResult query={input.query} results={output} />,
    },
  }}
/>
```

Tool groups work in all three components: `ChatDrawer`, `AICommandBar`, and `AIGenerationButton`. When consecutive tool calls match the same group's `tools` array, they are accumulated and passed as a single array to the group's `renderer`. Non-matching tools render individually as before (using `toolRenderers` or default rendering).

The `segmentToolCalls` utility is also exported for custom implementations:

```tsx
import { segmentToolCalls, ToolGroupCall, ToolGroupConfig } from '@devicai/ui';

const segments = segmentToolCalls(calls, toolGroups);
// Returns: Array<{ type: 'group', config, calls } | { type: 'single', call, index }>
```

## Theming

### Using Props

All color and typography properties can be set via `options`:

```tsx
<ChatDrawer
  assistantId="my-assistant"
  options={{
    color: '#6366f1',                    // Primary color
    backgroundColor: '#ffffff',          // Drawer background
    textColor: '#1e293b',               // Text color
    secondaryBackgroundColor: '#f8fafc', // Input/selector background
    borderColor: '#e2e8f0',             // Border color
    userBubbleColor: '#6366f1',         // User message bubble
    userBubbleTextColor: '#ffffff',     // User message text
    assistantBubbleColor: '#f1f5f9',    // Assistant message bubble
    assistantBubbleTextColor: '#1e293b',// Assistant message text
    sendButtonColor: '#6366f1',         // Send button background
    fontFamily: '"Inter", sans-serif',  // Font override
  }}
/>
```

### Using CSS Variables

Override the default theme by setting CSS variables:

```css
/* your-styles.css */
:root {
  --devic-primary: #6366f1;        /* Primary color */
  --devic-primary-hover: #4f46e5;  /* Primary hover */
  --devic-primary-light: #eef2ff;  /* Light primary background */
  --devic-bg: #ffffff;             /* Background */
  --devic-bg-secondary: #f8fafc;   /* Secondary background */
  --devic-text: #1e293b;           /* Text color */
  --devic-text-secondary: #64748b; /* Secondary text */
  --devic-text-muted: #94a3b8;     /* Muted text */
  --devic-border: #e2e8f0;         /* Border color */
  --devic-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  --devic-radius: 12px;            /* Border radius */
  --devic-radius-sm: 6px;
  --devic-radius-lg: 20px;
}
```

### Using the color Option

Quick color customization:

```tsx
<ChatDrawer
  assistantId="my-assistant"
  options={{
    color: '#6366f1', // Sets primary color
  }}
/>
```

## Controlled Mode

Control the drawer state externally:

```tsx
function App() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button onClick={() => setIsOpen(true)}>
        Open Chat
      </button>

      <ChatDrawer
        assistantId="my-assistant"
        isOpen={isOpen}
        onOpen={() => setIsOpen(true)}
        onClose={() => setIsOpen(false)}
      />
    </>
  );
}
```

## Continuing Existing Conversations

Load and continue a previous chat:

```tsx
function App() {
  // Get chatUid from URL, localStorage, or your backend
  const existingChatUid = 'previous-chat-uid';

  return (
    <ChatDrawer
      assistantId="my-assistant"
      chatUid={existingChatUid}
      onChatCreated={(newChatUid) => {
        // Save the new chat UID for future reference
        localStorage.setItem('lastChatUid', newChatUid);
      }}
    />
  );
}
```

## Event Callbacks

Handle various chat events:

```tsx
<ChatDrawer
  assistantId="my-assistant"
  onMessageSent={(message) => {
    // Track user messages
    analytics.track('chat_message_sent', {
      messageLength: message.content.message?.length,
    });
  }}
  onMessageReceived={(message) => {
    // Track assistant responses
    analytics.track('chat_message_received', {
      hasToolCalls: !!message.tool_calls?.length,
    });
  }}
  onToolCall={(toolName, params) => {
    // Track tool usage
    analytics.track('chat_tool_called', { toolName });
  }}
  onError={(error) => {
    // Report errors
    errorReporting.capture(error);
  }}
  onChatCreated={(chatUid) => {
    // Store chat reference
    saveChatReference(chatUid);
  }}
  onOpen={() => {
    // Track drawer open
    analytics.track('chat_opened');
  }}
  onClose={() => {
    // Track drawer close
    analytics.track('chat_closed');
  }}
/>
```

## API Client Direct Usage

For advanced use cases, use the API client directly:

```tsx
import { DevicApiClient } from '@devicai/ui';

const client = new DevicApiClient({
  apiKey: 'your-api-key',
  baseUrl: 'https://api.devic.ai',
});

// List available assistants
const assistants = await client.getAssistants();

// Send a message (async mode)
const { chatUid } = await client.sendMessageAsync('assistant-id', {
  message: 'Hello!',
  tenantId: 'tenant-123',
  metadata: { source: 'web-app' },
});

// Poll for response
const checkResponse = async () => {
  const result = await client.getRealtimeHistory('assistant-id', chatUid);

  if (result.status === 'completed') {
    return result.chatHistory;
  } else if (result.status === 'error') {
    throw new Error('Processing failed');
  } else if (result.status === 'handed_off') {
    // Assistant delegated to a subagent
    // result.handedOffSubThreadId contains the subthread ID
    console.log('Handed off to subthread:', result.handedOffSubThreadId);
    // Continue polling until the handoff completes and processing resumes
  }

  // Continue polling
  await new Promise(r => setTimeout(r, 1000));
  return checkResponse();
};

const messages = await checkResponse();
```

## Server-Side Rendering (SSR)

The library is SSR-compatible. Ensure you only render the ChatDrawer on the client:

```tsx
// Next.js example
import dynamic from 'next/dynamic';

const ChatDrawer = dynamic(
  () => import('@devicai/ui').then(mod => mod.ChatDrawer),
  { ssr: false }
);

function Page() {
  return (
    <div>
      <h1>My Page</h1>
      <ChatDrawer assistantId="my-assistant" />
    </div>
  );
}
```

## TypeScript Support

All types are exported for TypeScript users:

```tsx
import type {
  // Chat types
  ChatMessage,
  ChatDrawerProps,
  ChatDrawerOptions,
  ChatDrawerHandle,

  // AICommandBar types
  AICommandBarProps,
  AICommandBarOptions,
  AICommandBarHandle,
  AICommandBarCommand,
  CommandBarResult,
  ToolCallSummary,

  // AIGenerationButton types
  AIGenerationButtonProps,
  AIGenerationButtonOptions,
  AIGenerationButtonHandle,
  AIGenerationButtonMode,
  GenerationResult,

  // Tool types
  ModelInterfaceTool,
  ModelInterfaceToolSchema,
  ToolGroupCall,
  ToolGroupConfig,

  // Hook types
  UseDevicChatOptions,
  UseDevicChatResult,

  // API types
  RealtimeChatHistory,  // Includes status (with 'handed_off') and handedOffSubThreadId
  RealtimeStatus,       // 'processing' | 'completed' | 'error' | 'waiting_for_tool_response' | 'handed_off'
  AssistantSpecialization,

  // Feedback types
  FeedbackSubmission,
  FeedbackEntry,
  FeedbackTheme,

  // Agent/Handoff types
  ThreadStateTagProps,
  StateConfig,
  HandoffSubagentWidgetProps,
  AgentThreadDto,
  AgentTaskDto,
  AgentDto,
  HandOffToolResponse,
} from '@devicai/ui';

// Import the AgentThreadState enum (value export)
import { AgentThreadState, segmentToolCalls } from '@devicai/ui';

// Use types in your code
const chatOptions: ChatDrawerOptions = {
  position: 'right',
  width: 400,
  welcomeMessage: 'Hello!',
};

const commandBarOptions: AICommandBarOptions = {
  shortcut: 'cmd+k',
  placeholder: 'Ask AI...',
};

const generationOptions: AIGenerationButtonOptions = {
  mode: 'modal',
  modalTitle: 'Generate with AI',
};

const handleMessage = (message: ChatMessage) => {
  console.log(message.content.message);
};

const handleCommandResult = (result: CommandBarResult) => {
  console.log('Chat UID:', result.chatUid);
  console.log('Tool calls:', result.toolCalls.length);
  console.log('Response:', result.message.content);
};

const handleGenerationResult = (result: GenerationResult) => {
  console.log('Generated content:', result.message.content.message);
  console.log('Tool calls executed:', result.toolCalls);
};
```

## ChatDrawer Props Reference

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `mode` | `'drawer' \| 'inline'` | `'drawer'` | Display mode: overlay drawer or embedded inline |
| `assistantId` | `string` | *required* | Assistant identifier |
| `chatUid` | `string` | — | Existing chat UID to continue conversation |
| `options` | `ChatDrawerOptions` | — | Display and behavior options (see below) |
| `enabledTools` | `string[]` | — | Tools enabled from assistant's configured tool groups |
| `modelInterfaceTools` | `ModelInterfaceTool[]` | — | Client-side tools for model interface protocol |
| `tenantId` | `string` | — | Tenant ID (overrides provider) |
| `tenantMetadata` | `Record<string, any>` | — | Tenant metadata (overrides provider) |
| `apiKey` | `string` | — | API key (overrides provider) |
| `baseUrl` | `string` | — | Base URL (overrides provider) |
| `isOpen` | `boolean` | — | Controlled open state (drawer mode only) |
| `className` | `string` | — | Additional CSS class |
| `onMessageSent` | `(message) => void` | — | Fires when user sends a message |
| `onMessageReceived` | `(message) => void` | — | Fires when assistant responds |
| `onToolCall` | `(toolName, params) => void` | — | Fires when a tool is called |
| `onError` | `(error) => void` | — | Fires on error |
| `onChatCreated` | `(chatUid) => void` | — | Fires when a new chat is created |
| `onOpen` | `() => void` | — | Fires when drawer opens |
| `onClose` | `() => void` | — | Fires when drawer closes |
| `onConversationChange` | `(chatUid) => void` | — | Fires when active conversation changes |

## ChatDrawerOptions Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `position` | `'left' \| 'right'` | `'right'` | Drawer position |
| `width` | `number \| string` | `'100%'` | Drawer width (px number or CSS string) |
| `defaultOpen` | `boolean` | `false` | Whether drawer starts open |
| `resizable` | `boolean` | `false` | Enable drag-to-resize handle |
| `minWidth` | `number` | `300` | Minimum width when resizable (px) |
| `maxWidth` | `number` | `800` | Maximum width when resizable (px) |
| `zIndex` | `number` | `1000` | Z-index for the drawer |
| `borderRadius` | `number \| string` | `0` | Border radius for the container |
| `style` | `CSSProperties` | — | Additional inline styles |
| `title` | `string \| ReactNode` | `'Chat'` | Header title |
| `showAvatar` | `boolean` | `false` | Show assistant image next to title |
| `welcomeMessage` | `string` | — | Welcome message shown at start |
| `suggestedMessages` | `string[]` | — | Quick action suggestions |
| `inputPlaceholder` | `string` | `'Type a message...'` | Input placeholder text |
| `showToolTimeline` | `boolean` | `true` | Show tool execution timeline |
| `enableFileUploads` | `boolean` | `false` | Enable file attachments |
| `allowedFileTypes` | `AllowedFileTypes` | — | Filter by file type (images, documents, audio, video) |
| `maxFileSize` | `number` | `10485760` | Max file size in bytes (10MB) |
| `color` | `string` | `'#1890ff'` | Primary theme color |
| `backgroundColor` | `string` | — | Drawer background color |
| `textColor` | `string` | — | Text color |
| `secondaryBackgroundColor` | `string` | — | Input/selector background color |
| `borderColor` | `string` | — | Border color |
| `userBubbleColor` | `string` | — | User message bubble background |
| `userBubbleTextColor` | `string` | — | User message bubble text |
| `assistantBubbleColor` | `string` | — | Assistant message bubble background |
| `assistantBubbleTextColor` | `string` | — | Assistant message bubble text |
| `sendButtonColor` | `string` | — | Send button background color |
| `fontFamily` | `string` | — | Font family override |
| `loadingIndicator` | `ReactNode` | — | Custom loading spinner |
| `sendButtonContent` | `ReactNode` | — | Custom send button content |
| `toolRenderers` | `Record<string, (input, output) => ReactNode>` | — | Custom tool call renderers by tool name |
| `toolIcons` | `Record<string, ReactNode>` | — | Custom tool call icons by tool name |
| `showFeedback` | `boolean` | `true` | Show thumbs up/down feedback buttons on assistant messages |
| `handoffWidgetRenderer` | `(props: { thread, agent, elapsedSeconds, isTerminal }) => ReactNode` | — | Custom renderer for the HandoffSubagentWidget (replaces default UI) |
| `toolGroups` | `ToolGroupConfig[]` | — | Group consecutive tool calls under a single renderer |

## Message Feedback

Both ChatDrawer and AICommandBar support message feedback (thumbs up/down with optional comments). Feedback is submitted to the Devic API and associated with the chat.

### ChatDrawer Feedback

Feedback buttons appear on assistant messages by default. Users can click thumbs up/down and optionally add a comment via a modal.

```tsx
<ChatDrawer
  assistantId="my-assistant"
  options={{
    showFeedback: true, // default: true
  }}
/>
```

### AICommandBar Feedback

When `showResultCard` is enabled, feedback buttons appear below the response. The feedback UI automatically adapts to the command bar's theme.

```tsx
<AICommandBar
  assistantId="my-assistant"
  options={{
    showResultCard: true,
    // Feedback inherits theme from these options:
    backgroundColor: '#1f2937',
    textColor: '#f9fafb',
    borderColor: '#374151',
  }}
/>
```

### Feedback Theming

The feedback modal and action buttons automatically inherit theme colors from the parent component. For custom implementations, you can pass a `FeedbackTheme` object:

```tsx
interface FeedbackTheme {
  backgroundColor?: string;      // Modal background
  textColor?: string;            // Primary text
  textMutedColor?: string;       // Muted/secondary text
  secondaryBackgroundColor?: string; // Button backgrounds, hover states
  borderColor?: string;          // Modal borders
  primaryColor?: string;         // Primary action color
  primaryHoverColor?: string;    // Primary button hover
}
```

### Feedback API

Feedback is automatically submitted to the Devic API using these endpoints:

- `POST /api/v1/assistants/:identifier/chats/:chatUid/feedback` - Submit feedback
- `GET /api/v1/assistants/:identifier/chats/:chatUid/feedback` - Get feedback entries

You can also use the API client directly:

```tsx
import { DevicApiClient, FeedbackSubmission } from '@devicai/ui';

const client = new DevicApiClient({ apiKey: 'your-api-key' });

// Submit feedback
const feedback: FeedbackSubmission = {
  messageId: 'message-uid',
  feedback: true,  // true = positive, false = negative
  feedbackComment: 'Very helpful response!',
  feedbackData: { category: 'accuracy' },
};

await client.submitChatFeedback('assistant-id', 'chat-uid', feedback);

// Get all feedback for a chat
const entries = await client.getChatFeedback('assistant-id', 'chat-uid');
```

### Feedback Types

```tsx
import type {
  FeedbackSubmission,
  FeedbackEntry,
  FeedbackTheme,
} from '@devicai/ui';

// Submission payload
interface FeedbackSubmission {
  messageId: string;
  feedback?: boolean;              // true = positive, false = negative
  feedbackComment?: string;        // Optional comment
  feedbackData?: Record<string, any>; // Custom metadata
}

// Response from API
interface FeedbackEntry {
  _id: string;
  requestId: string;
  chatUID?: string;
  feedback?: boolean;
  feedbackComment?: string;
  feedbackData?: Record<string, any>;
  creationTimestamp: string;
  lastEditTimestamp?: string;
}
```

## AICommandBar Component

A floating command bar (similar to Spotlight/Command Palette) for quick AI interactions. It provides a minimal input interface that processes messages, shows tool execution progress, and displays results in a compact card.

### Basic Usage

```tsx
import { AICommandBar } from '@devicai/ui';

function App() {
  return (
    <AICommandBar
      assistantId="my-assistant"
      options={{
        placeholder: 'Ask AI...',
        shortcut: 'cmd+k',
      }}
      onResponse={({ message, toolCalls }) => {
        console.log('Response:', message.content);
      }}
    />
  );
}
```

### Fixed Position with Keyboard Shortcut

```tsx
<AICommandBar
  assistantId="support-assistant"
  options={{
    position: 'fixed',
    fixedPlacement: { bottom: 20, right: 20 },
    shortcut: 'cmd+j',
    placeholder: 'Ask AI about your data...',
    showShortcutHint: true,
  }}
/>
```

### Integration with ChatDrawer

Hand off conversations to the full ChatDrawer after getting a quick answer:

```tsx
import { useRef } from 'react';
import { AICommandBar, ChatDrawer, ChatDrawerHandle } from '@devicai/ui';

function App() {
  const drawerRef = useRef<ChatDrawerHandle>(null);

  return (
    <>
      <AICommandBar
        assistantId="my-assistant"
        onExecute="openDrawer"
        chatDrawerRef={drawerRef}
        options={{
          shortcut: 'cmd+k',
          showResultCard: false, // Don't show result since drawer opens
        }}
      />

      <ChatDrawer
        ref={drawerRef}
        assistantId="my-assistant"
      />
    </>
  );
}
```

### Command History

Command history is enabled by default. Users can:
- Press **Arrow Up/Down** to navigate through previous prompts
- Use the `/history` command to see the history list
- Click on a history item to reuse it

```tsx
<AICommandBar
  assistantId="my-assistant"
  options={{
    enableHistory: true,           // default: true
    maxHistoryItems: 50,           // default: 50
    historyStorageKey: 'my-app-command-history', // localStorage key
    showHistoryCommand: true,      // adds /history command
  }}
/>
```

### Commands System

Define slash commands that trigger predefined messages:

```tsx
<AICommandBar
  assistantId="my-assistant"
  options={{
    commands: [
      {
        keyword: 'summarize',
        description: 'Summarize the current page',
        message: 'Please summarize the content of this page.',
        icon: <SummarizeIcon />,
      },
      {
        keyword: 'translate',
        description: 'Translate selected text',
        message: 'Translate the following text to Spanish: ',
      },
      {
        keyword: 'explain',
        description: 'Explain like I\'m five',
        message: 'Explain this concept in simple terms: ',
      },
    ],
  }}
/>
```

When the user types `/`, a dropdown shows available commands. Arrow keys navigate, Enter selects, Tab autocompletes.

### Custom Tool Rendering

Display tool calls with custom icons and renderers:

```tsx
<AICommandBar
  assistantId="my-assistant"
  options={{
    toolIcons: {
      search_database: <DatabaseIcon />,
      fetch_weather: <WeatherIcon />,
    },
    toolRenderers: {
      search_database: (input, output) => (
        <div className="custom-result">
          Found {output.count} results for "{input.query}"
        </div>
      ),
    },
  }}
/>
```

### Theming

```tsx
<AICommandBar
  assistantId="my-assistant"
  options={{
    color: '#6366f1',              // Primary color (spinner, badges)
    backgroundColor: '#ffffff',    // Bar background
    textColor: '#1f2937',          // Text color
    borderColor: '#e5e7eb',        // Border color
    borderRadius: 12,              // Border radius (px or string)
    fontFamily: 'Inter, sans-serif',
    fontSize: 14,
    padding: '12px 16px',
    boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
    animationDuration: 200,        // ms
  }}
/>
```

### Controlled Visibility

```tsx
function App() {
  const [isVisible, setIsVisible] = useState(false);
  const commandBarRef = useRef<AICommandBarHandle>(null);

  return (
    <>
      <button onClick={() => commandBarRef.current?.toggle()}>
        Toggle Command Bar
      </button>

      <AICommandBar
        ref={commandBarRef}
        assistantId="my-assistant"
        isVisible={isVisible}
        onVisibilityChange={setIsVisible}
        onOpen={() => console.log('Opened')}
        onClose={() => console.log('Closed')}
      />
    </>
  );
}
```

### Using the Hook Directly

For custom UI implementations:

```tsx
import { useAICommandBar, formatShortcut } from '@devicai/ui';

function CustomCommandBar() {
  const {
    isVisible,
    open,
    close,
    toggle,
    inputValue,
    setInputValue,
    inputRef,
    focus,
    isProcessing,
    currentToolSummary,
    toolCalls,
    result,
    error,
    history,
    showingHistory,
    showingCommands,
    filteredCommands,
    submit,
    reset,
    handleKeyDown,
  } = useAICommandBar({
    assistantId: 'my-assistant',
    options: { shortcut: 'cmd+k' },
    onResponse: (result) => console.log(result),
  });

  if (!isVisible) return null;

  return (
    <div className="my-command-bar">
      {isProcessing ? (
        <span>{currentToolSummary || 'Processing...'}</span>
      ) : (
        <input
          ref={inputRef}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask AI..."
        />
      )}
    </div>
  );
}
```

## AICommandBar Props Reference

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `assistantId` | `string` | *required* | Assistant identifier |
| `apiKey` | `string` | — | API key (overrides provider) |
| `baseUrl` | `string` | — | Base URL (overrides provider) |
| `tenantId` | `string` | — | Tenant ID (overrides provider) |
| `tenantMetadata` | `Record<string, any>` | — | Tenant metadata |
| `options` | `AICommandBarOptions` | — | Display and behavior options |
| `isVisible` | `boolean` | — | Controlled visibility state |
| `onVisibilityChange` | `(visible: boolean) => void` | — | Fires when visibility changes |
| `onExecute` | `'openDrawer' \| 'callback'` | `'callback'` | What to do on completion |
| `chatDrawerRef` | `RefObject<ChatDrawerHandle>` | — | Ref to ChatDrawer (for openDrawer mode) |
| `onResponse` | `(result: CommandBarResult) => void` | — | Fires on completion (callback mode) |
| `modelInterfaceTools` | `ModelInterfaceTool[]` | — | Client-side tools |
| `onSubmit` | `(message: string) => void` | — | Fires when user submits |
| `onToolCall` | `(toolName, params) => void` | — | Fires when a tool is called |
| `onError` | `(error: Error) => void` | — | Fires on error |
| `onOpen` | `() => void` | — | Fires when bar opens |
| `onClose` | `() => void` | — | Fires when bar closes |
| `className` | `string` | — | Additional CSS class |

## AICommandBarOptions Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `position` | `'inline' \| 'fixed'` | `'inline'` | Positioning mode |
| `fixedPlacement` | `{ top?, right?, bottom?, left? }` | — | Position offsets for fixed mode |
| `shortcut` | `string` | — | Keyboard shortcut (e.g., `'cmd+k'`, `'ctrl+j'`) |
| `showShortcutHint` | `boolean` | `true` | Show shortcut badge in bar |
| `placeholder` | `string` | `'Ask AI...'` | Input placeholder |
| `icon` | `ReactNode` | Sparkles icon | Custom icon for idle state |
| `width` | `number \| string` | `400` | Bar width |
| `maxWidth` | `number \| string` | `'100%'` | Maximum width |
| `zIndex` | `number` | `9999` | Z-index |
| `showResultCard` | `boolean` | `true` | Show result card on completion |
| `resultCardMaxHeight` | `number \| string` | `300` | Max height for result card |
| `processingMessage` | `string` | `'Processing...'` | Fallback message during processing |
| `color` | `string` | `'#3b82f6'` | Primary color |
| `backgroundColor` | `string` | `'#ffffff'` | Background color |
| `textColor` | `string` | `'#1f2937'` | Text color |
| `borderColor` | `string` | `'#e5e7eb'` | Border color |
| `borderRadius` | `number \| string` | `12` | Border radius |
| `fontFamily` | `string` | System fonts | Font family |
| `fontSize` | `number \| string` | `14` | Font size |
| `padding` | `number \| string` | `'12px 16px'` | Bar padding |
| `boxShadow` | `string` | Light shadow | Box shadow |
| `animationDuration` | `number` | `200` | Animation duration (ms) |
| `toolRenderers` | `Record<string, (input, output) => ReactNode>` | — | Custom tool renderers |
| `toolIcons` | `Record<string, ReactNode>` | — | Custom tool icons |
| `enableHistory` | `boolean` | `true` | Enable command history |
| `maxHistoryItems` | `number` | `50` | Max history items to store |
| `historyStorageKey` | `string` | `'devic-command-bar-history'` | localStorage key |
| `commands` | `AICommandBarCommand[]` | — | Slash commands |
| `showHistoryCommand` | `boolean` | `true` | Add built-in /history command |
| `toolGroups` | `ToolGroupConfig[]` | — | Group consecutive tool calls under a single renderer |

## AICommandBarHandle Reference

Methods exposed via ref:

| Method | Description |
|--------|-------------|
| `open()` | Open the command bar |
| `close()` | Close the command bar |
| `toggle()` | Toggle visibility |
| `focus()` | Focus the input |
| `submit(message?: string)` | Submit a message |
| `reset()` | Reset state (clear input, result, errors) |

## AIGenerationButton Component

A button component for triggering AI generation with three configurable interaction modes. Useful for "Generate with AI" buttons in forms, editors, and other UI contexts.

### Basic Usage

```tsx
import { AIGenerationButton } from '@devicai/ui';

function App() {
  return (
    <AIGenerationButton
      assistantId="my-assistant"
      options={{
        mode: 'modal',
        modalTitle: 'Generate Content',
        placeholder: 'Describe what you want to generate...',
      }}
      onResponse={({ message }) => {
        console.log('Generated:', message.content.message);
      }}
    />
  );
}
```

### Interaction Modes

#### Direct Mode

Sends a predefined prompt immediately when clicked. Best for specific, predetermined actions.

```tsx
<AIGenerationButton
  assistantId="my-assistant"
  options={{
    mode: 'direct',
    prompt: 'Generate a product description based on the form data',
    label: 'Auto-Generate Description',
    loadingLabel: 'Generating...',
  }}
  onBeforeSend={(prompt) => {
    // Optionally modify the prompt before sending
    return `${prompt}\n\nProduct: ${productName}`;
  }}
  onResponse={({ message }) => setDescription(message.content.message)}
/>
```

#### Modal Mode (Default)

Opens a modal dialog for the user to enter a custom prompt.

```tsx
<AIGenerationButton
  assistantId="my-assistant"
  options={{
    mode: 'modal',
    modalTitle: 'Generate with AI',
    modalDescription: 'Describe what you want and the AI will generate it for you.',
    placeholder: 'E.g., Create a function that validates email addresses...',
    confirmText: 'Generate',
    cancelText: 'Cancel',
  }}
  onResponse={({ message }) => {
    // Handle the generated content
    setCode(message.content.message);
  }}
/>
```

#### Tooltip Mode

Shows a compact inline input next to the button. Good for quick prompts without modal interruption.

```tsx
<AIGenerationButton
  assistantId="my-assistant"
  options={{
    mode: 'tooltip',
    tooltipPlacement: 'bottom', // 'top' | 'bottom' | 'left' | 'right'
    tooltipWidth: 350,
    placeholder: 'What should I generate?',
  }}
  onResponse={handleGeneration}
/>
```

### Button Styling

```tsx
<AIGenerationButton
  assistantId="my-assistant"
  options={{
    // Button variant
    variant: 'primary', // 'primary' | 'secondary' | 'outline' | 'ghost'

    // Button size
    size: 'medium', // 'small' | 'medium' | 'large'

    // Label and icon
    label: 'Generate with AI',
    hideLabel: false, // Set true for icon-only button
    icon: <CustomSparkleIcon />, // Custom icon
    hideIcon: false,

    // Loading state
    loadingLabel: 'Generating...',
  }}
/>
```

### Theming

```tsx
<AIGenerationButton
  assistantId="my-assistant"
  options={{
    color: '#6366f1',           // Primary color
    backgroundColor: '#ffffff',  // Button background (for secondary/outline variants)
    textColor: '#1f2937',        // Text color
    borderColor: '#e5e7eb',      // Border color
    borderRadius: 8,             // Border radius
    fontFamily: 'Inter, sans-serif',
    fontSize: 14,
    zIndex: 10000,               // Z-index for modal/tooltip
    animationDuration: 200,      // Animation duration in ms
  }}
/>
```

### Custom Button Content

Use `children` to completely customize the button appearance:

```tsx
<AIGenerationButton
  assistantId="my-assistant"
  options={{ mode: 'modal' }}
  onResponse={handleResponse}
>
  <span className="my-custom-button">
    <SparkleIcon /> Generate Code
  </span>
</AIGenerationButton>
```

### Programmatic Control

Use ref to control the component programmatically:

```tsx
import { useRef } from 'react';
import { AIGenerationButton, AIGenerationButtonHandle } from '@devicai/ui';

function Editor() {
  const buttonRef = useRef<AIGenerationButtonHandle>(null);

  const handleKeyboardShortcut = (e: KeyboardEvent) => {
    if (e.metaKey && e.key === 'g') {
      buttonRef.current?.open(); // Open modal/tooltip
    }
  };

  const generateDirectly = async () => {
    const result = await buttonRef.current?.generate('Generate a summary');
    if (result) {
      console.log('Generated:', result.message.content.message);
    }
  };

  return (
    <AIGenerationButton
      ref={buttonRef}
      assistantId="my-assistant"
      options={{ mode: 'modal' }}
      onResponse={handleResponse}
    />
  );
}
```

### Using the Hook Directly

For completely custom UI implementations:

```tsx
import { useAIGenerationButton } from '@devicai/ui';

function CustomGenerateButton() {
  const {
    isOpen,
    isProcessing,
    inputValue,
    setInputValue,
    error,
    result,
    inputRef,
    open,
    close,
    generate,
    reset,
    handleKeyDown,
  } = useAIGenerationButton({
    assistantId: 'my-assistant',
    onResponse: (result) => console.log('Generated:', result),
    onError: (error) => console.error('Error:', error),
  });

  return (
    <div>
      <button onClick={() => open()}>
        {isProcessing ? 'Generating...' : 'Generate'}
      </button>

      {isOpen && (
        <div className="custom-modal">
          <textarea
            ref={inputRef}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe what to generate..."
          />
          <button onClick={() => generate()} disabled={isProcessing}>
            {isProcessing ? 'Working...' : 'Generate'}
          </button>
          <button onClick={close}>Cancel</button>
          {error && <p className="error">{error.message}</p>}
        </div>
      )}
    </div>
  );
}
```

## AIGenerationButton Props Reference

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `assistantId` | `string` | *required* | Assistant identifier |
| `apiKey` | `string` | — | API key (overrides provider) |
| `baseUrl` | `string` | — | Base URL (overrides provider) |
| `tenantId` | `string` | — | Tenant ID (overrides provider) |
| `tenantMetadata` | `Record<string, any>` | — | Tenant metadata |
| `options` | `AIGenerationButtonOptions` | — | Display and behavior options |
| `modelInterfaceTools` | `ModelInterfaceTool[]` | — | Client-side tools |
| `onResponse` | `(result: GenerationResult) => void` | — | Fires on successful generation |
| `onBeforeSend` | `(prompt: string) => string \| undefined` | — | Modify prompt before sending |
| `onError` | `(error: Error) => void` | — | Fires on error |
| `onStart` | `() => void` | — | Fires when processing starts |
| `onOpen` | `() => void` | — | Fires when modal/tooltip opens |
| `onClose` | `() => void` | — | Fires when modal/tooltip closes |
| `disabled` | `boolean` | `false` | Disable the button |
| `className` | `string` | — | Additional CSS class for button |
| `containerClassName` | `string` | — | CSS class for container |
| `children` | `ReactNode` | — | Custom button content |
| `theme` | `FeedbackTheme` | — | Theme for modal/tooltip |

## AIGenerationButtonOptions Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mode` | `'direct' \| 'modal' \| 'tooltip'` | `'modal'` | Interaction mode |
| `prompt` | `string` | — | Predefined prompt (required for direct mode) |
| `placeholder` | `string` | `'Describe what you want to generate...'` | Input placeholder |
| `modalTitle` | `string` | `'Generate with AI'` | Modal title |
| `modalDescription` | `string` | — | Modal description text |
| `confirmText` | `string` | `'Generate'` | Confirm button text |
| `cancelText` | `string` | `'Cancel'` | Cancel button text |
| `tooltipPlacement` | `'top' \| 'bottom' \| 'left' \| 'right'` | `'top'` | Tooltip position |
| `tooltipWidth` | `number \| string` | `300` | Tooltip width |
| `variant` | `'primary' \| 'secondary' \| 'ghost' \| 'outline'` | `'primary'` | Button variant |
| `size` | `'small' \| 'medium' \| 'large'` | `'medium'` | Button size |
| `icon` | `ReactNode` | Sparkles icon | Custom button icon |
| `hideIcon` | `boolean` | `false` | Hide button icon |
| `label` | `string` | `'Generate with AI'` | Button label |
| `hideLabel` | `boolean` | `false` | Hide button label (icon-only) |
| `loadingLabel` | `string` | `'Generating...'` | Label during processing |
| `color` | `string` | `'#3b82f6'` | Primary color |
| `backgroundColor` | `string` | — | Background color |
| `textColor` | `string` | — | Text color |
| `borderColor` | `string` | — | Border color |
| `borderRadius` | `number \| string` | `8` | Border radius |
| `fontFamily` | `string` | System fonts | Font family |
| `fontSize` | `number \| string` | `14` | Font size |
| `zIndex` | `number` | `10000` | Z-index for overlays |
| `animationDuration` | `number` | `200` | Animation duration (ms) |
| `toolRenderers` | `Record<string, (input, output) => ReactNode>` | — | Custom tool call renderers by tool name |
| `toolIcons` | `Record<string, ReactNode>` | — | Custom tool icons by tool name |
| `processingMessage` | `string` | `'Processing...'` | Message shown during processing |
| `toolGroups` | `ToolGroupConfig[]` | — | Group consecutive tool calls under a single renderer |

## AIGenerationButtonHandle Reference

Methods exposed via ref:

| Method | Description |
|--------|-------------|
| `generate(prompt?: string)` | Trigger generation (returns Promise with result) |
| `open()` | Open modal/tooltip (for modal and tooltip modes) |
| `close()` | Close modal/tooltip |
| `reset()` | Reset component state |
| `isProcessing` | Boolean indicating if processing |

## Subagent Handoff System

The library supports assistant-to-subagent handoff, where an assistant delegates work to a specialized agent. During handoff, the chat input is automatically disabled and a widget displays the subagent's progress in real time.

### How It Works

1. The assistant calls a `hand_off_subagent` tool, which creates a subthread on the backend
2. The realtime polling response status changes to `handed_off` with a `handedOffSubThreadId` field
3. `useDevicChat` detects the `handed_off` status, stops main polling, and sets `handedOff: true` with the subthread ID
4. ChatInput is disabled with a "Waiting for subagent to complete" notice
5. A `HandoffSubagentWidget` renders inline in the tool timeline, polling the subthread every 5s for status, tasks progress, and summary
6. A background handoff poll checks the realtime endpoint every 5s to detect when the parent thread is no longer in `handed_off` state
7. When the subthread reaches a terminal state (completed, failed, terminated), the widget calls `onHandoffCompleted` which clears handoff state and resumes main polling to pick up the parent thread's continuation

### Automatic Handoff in ChatDrawer

When using `ChatDrawer`, handoff is handled automatically. No extra configuration is needed — the widget appears inline when a `hand_off_subagent` tool call is detected, and the input is disabled until completion.

```tsx
<ChatDrawer
  assistantId="my-assistant"
  // Handoff works out of the box
/>
```

### Custom Handoff Widget

Replace the default handoff widget UI using `handoffWidgetRenderer`:

```tsx
<ChatDrawer
  assistantId="my-assistant"
  options={{
    handoffWidgetRenderer: ({ thread, agent, elapsedSeconds, isTerminal }) => (
      <div className="my-custom-handoff">
        <span>{agent?.name || 'Subagent'} is working...</span>
        {thread?.tasks && (
          <span>
            {thread.tasks.filter(t => t.completed).length}/{thread.tasks.length} tasks
          </span>
        )}
        {isTerminal && <span>Done!</span>}
      </div>
    ),
  }}
/>
```

### HandoffSubagentWidget (Standalone)

Use `HandoffSubagentWidget` directly for custom chat UIs:

```tsx
import { HandoffSubagentWidget } from '@devicai/ui';

<HandoffSubagentWidget
  subThreadId="thread-abc-123"
  onCompleted={() => console.log('Subagent finished')}
  renderWidget={({ thread, agent, elapsedSeconds, isTerminal }) => (
    <MyCustomWidget thread={thread} agent={agent} />
  )}
/>
```

### HandoffSubagentWidget Props Reference

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `subThreadId` | `string` | *required* | The subthread ID to monitor |
| `onCompleted` | `() => void` | — | Called when subthread reaches a terminal state |
| `apiKey` | `string` | — | API key (overrides provider) |
| `baseUrl` | `string` | — | Base URL (overrides provider) |
| `renderWidget` | `(props: { thread, agent, elapsedSeconds, isTerminal }) => ReactNode` | — | Custom renderer replacing the entire widget |

### useDevicChat Handoff Fields

When building custom UIs with `useDevicChat`, the hook exposes handoff state:

```tsx
import { useDevicChat } from '@devicai/ui';

function CustomChat() {
  const {
    messages,
    sendMessage,
    handedOff,              // true when a handoff is active
    handedOffSubThreadId,   // subthread ID being monitored
    onHandoffCompleted,     // callback for HandoffSubagentWidget
    // ...other fields
  } = useDevicChat({ assistantId: 'my-assistant' });

  return (
    <div>
      {/* Render messages, detect hand_off_subagent tool calls */}
      {handedOff && handedOffSubThreadId && (
        <HandoffSubagentWidget
          subThreadId={handedOffSubThreadId}
          onCompleted={onHandoffCompleted}
        />
      )}

      <input disabled={handedOff} placeholder="Type a message..." />
    </div>
  );
}
```

| Field | Type | Description |
|-------|------|-------------|
| `handedOff` | `boolean` | Whether the assistant has handed off to a subagent (set when realtime status is `handed_off`) |
| `handedOffSubThreadId` | `string \| null` | The active subthread ID (from `RealtimeChatHistory.handedOffSubThreadId`) |
| `onHandoffCompleted` | `() => void` | Callback that clears handoff state and resumes main polling when subagent finishes |
| `status` | `RealtimeStatus \| 'idle'` | Current status — includes `'handed_off'` when a handoff is active |

## ThreadStateTag Component

A standalone component that displays the current state of an agent thread as a colored tag with an interactive dropdown for actions (explain, pause, resume, approve, complete).

### Basic Usage

```tsx
import { ThreadStateTag, AgentThreadState } from '@devicai/ui';

<ThreadStateTag
  state={AgentThreadState.PROCESSING}
  threadId="thread-abc-123"
  agentName="Research Agent"
/>
```

### Interactive Actions

When `interactive` is true (default), clicking the tag opens a dropdown with context-specific actions:

- **Explain Thread**: AI-generated explanation of what the thread has done (with typing animation)
- **Pause/Resume**: Pause a processing thread or resume a paused one
- **Review Approval**: Approve or reject a thread waiting for approval
- **Complete Manually**: Admin action to manually complete/fail/terminate a thread

```tsx
<ThreadStateTag
  state={AgentThreadState.PAUSED_FOR_APPROVAL}
  threadId="thread-abc-123"
  agentName="Deployment Agent"
  showAdminActions={true}
  onActionComplete={(info) => {
    if (info === 'WAITING_FOR_RESPONSE_EXPIRED') {
      console.log('Response window expired');
    }
    refreshThread();
  }}
/>
```

### Display-Only Mode

Disable the dropdown for read-only contexts:

```tsx
<ThreadStateTag
  state={thread.state}
  threadId={thread._id}
  agentName="My Agent"
  interactive={false}
/>
```

### Thread States

The `AgentThreadState` enum defines all 12 possible states:

| State | Tag Color | Description |
|-------|-----------|-------------|
| `QUEUED` | Gold | Waiting to start |
| `PROCESSING` | Blue (processing) | Actively running |
| `COMPLETED` | Green | Successfully finished |
| `FAILED` | Red | Failed with error |
| `TERMINATED` | Red | Manually terminated |
| `PAUSED` | Gold | Paused by user or system |
| `PAUSED_FOR_APPROVAL` | Gold | Waiting for approval |
| `APPROVAL_REJECTED` | Red | Approval was rejected |
| `WAITING_FOR_RESPONSE` | Purple | Waiting for external input |
| `PAUSED_FOR_RESUME` | Gold | Paused and waiting to resume |
| `HANDED_OFF` | Blue | Delegated to subagent(s) |
| `GUARDRAIL_TRIGGER` | Red | Guardrail violation |

### ThreadStateTag Props Reference

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `state` | `AgentThreadState \| string` | *required* | Current thread state |
| `threadId` | `string` | *required* | Thread ID for API actions |
| `agentName` | `string` | *required* | Agent name shown in modals |
| `showIcon` | `boolean` | `true` | Show icon next to state text |
| `customIcon` | `ReactNode` | — | Replace the default state icon |
| `pausedReason` | `string` | — | Reason for pause (shown in tooltip) |
| `approvalRejectedMessage` | `string` | — | Message when approval rejected |
| `finishReason` | `string` | — | Reason the thread finished |
| `onActionComplete` | `(info?) => void` | — | Callback after actions (explain, pause, approve, etc.) |
| `pauseUntil` | `number` | — | Timestamp until which thread is paused |
| `subthreadCount` | `number` | — | Number of parallel subthreads (shown in handed_off tooltip) |
| `showAdminActions` | `boolean` | `false` | Show admin actions (complete manually) |
| `apiKey` | `string` | — | API key (overrides provider) |
| `baseUrl` | `string` | — | Base URL (overrides provider) |
| `interactive` | `boolean` | `true` | Enable dropdown on click |

## Agent API Client Methods

The `DevicApiClient` includes methods for managing agent threads:

```tsx
import { DevicApiClient } from '@devicai/ui';

const client = new DevicApiClient({ apiKey: 'your-api-key' });

// Get thread details (optionally with tasks)
const thread = await client.getThreadById('thread-id', true);

// Get agent details
const agent = await client.getAgentDetails('agent-id');

// Get AI explanation of thread execution
const explanation = await client.explainAgentThread('thread-id');

// Pause or resume a thread
await client.pauseResumeThread('thread-id', 'paused');
await client.pauseResumeThread('thread-id', 'queued');

// Handle approval (approve/reject with optional retry and message)
await client.handleThreadApproval('thread-id', true, false, 'Looks good');

// Manually complete a thread
await client.completeThread('thread-id', 'completed');

// Get full chat content (used after handoff completes)
const messages = await client.getChatHistoryContent('assistant-id', 'chat-uid');
```

## Troubleshooting

### Chat not loading

1. Verify your API key is correct
2. Check the browser console for errors
3. Ensure the assistant identifier exists

### Styles not applied

1. Make sure you imported the CSS: `import '@devicai/ui/styles.css'`
2. Check for CSS conflicts with your application styles
3. Try increasing specificity or using CSS variables

### Tools not being called

1. Verify the tool schema matches OpenAI function calling format
2. Check that `toolName` matches `function.name` in schema
3. Ensure the assistant has been configured to use client-side tools

### Handoff widget not appearing

1. Ensure the assistant is configured with a `hand_off_subagent` tool on the backend
2. The widget renders inside the tool timeline — verify `showToolTimeline` is not set to `false`
3. Check that the API key has permission to access agent thread endpoints
4. Verify the realtime response returns `status: 'handed_off'` with `handedOffSubThreadId` — the handoff detection relies on this
5. Check console for `[useDevicChat] Handoff state set:` logs to confirm the subthread ID is being received

### File uploads not working

1. Enable file uploads in options: `enableFileUploads: true`
2. Check allowed file types configuration
3. Verify file size is within limits

## Support

For issues and feature requests, visit the [GitHub repository](https://github.com/devic-ai/devic-ui).
