---
name: agents-ui
description: Build React frontends for LiveKit voice AI agents. Use this skill when creating web interfaces for voice assistants using LiveKit's shadcn-based Agents UI components. Covers AgentSessionProvider, audio visualizers, media controls, chat transcripts, and customization with Tailwind CSS.
---

# LiveKit Agents UI

Build React frontends for LiveKit voice AI agents with shadcn-based components.

## LiveKit MCP server tools

This skill works alongside the LiveKit MCP server, which provides direct access to the latest LiveKit documentation, code examples, and changelogs. Use these tools when you need up-to-date information that may have changed since this skill was created.

**Available MCP tools:**
- `docs_search` - Search the LiveKit docs site
- `get_pages` - Fetch specific documentation pages by path
- `get_changelog` - Get recent releases and updates for LiveKit packages
- `code_search` - Search LiveKit repositories for code examples
- `get_python_agent_example` - Browse 100+ Python agent examples

**When to use MCP tools:**
- You need the latest API documentation or feature updates
- You're looking for recent examples or code patterns
- You want to check if a feature has been added in recent releases
- The local references don't cover a specific topic

**When to use local references:**
- You need quick access to core concepts covered in this skill
- You're working offline or want faster access to common patterns
- The information in the references is sufficient for your needs

Use MCP tools and local references together for the best experience.

## References

Consult these resources as needed:

- ./references/livekit-overview.md -- LiveKit ecosystem overview and how these skills work together
- ./references/components.md -- All component APIs, props, and usage examples

## Prerequisites

- Node.js >= 18
- React 19
- Tailwind CSS 4
- shadcn/ui initialized in your project

## Installation

### 1. Add the LiveKit registry to your shadcn config

In your `components.json`:

```json
{
  "registries": {
    "@agents-ui": "https://livekit.io/ui/r/{name}.json"
  }
}
```

### 2. Install components

```bash
# Install individual components
npx shadcn@latest add @agents-ui/agent-session-provider
npx shadcn@latest add @agents-ui/agent-control-bar
npx shadcn@latest add @agents-ui/agent-audio-visualizer-bar

# Or install multiple at once
npx shadcn@latest add @agents-ui/agent-session-provider @agents-ui/agent-control-bar
```

Components are copied to your `components/agents-ui/` directory for full customization.

## Quick start

### Installation

Agents UI components require both `livekit-client` and `@livekit/components-react`:

```bash
npm install livekit-client @livekit/components-react
```

### Setting up a TokenSource

Before using Agents UI components, you need a `TokenSource` from `livekit-client` to handle authentication.

**For development** (using LiveKit Cloud Sandbox):

```tsx
import { TokenSource } from 'livekit-client';

const tokenSource = TokenSource.sandboxTokenServer({
  sandboxId: 'your-sandbox-id',
});
```

**For production** (using your own token endpoint):

```tsx
import { TokenSource } from 'livekit-client';

const tokenSource = TokenSource.endpoint('/api/token');
```

### Basic voice agent interface

Create a session using `useSession` from `@livekit/components-react`, then pass it to `AgentSessionProvider`:

```tsx
'use client';

import { useRef, useEffect } from 'react';
import { useSession } from '@livekit/components-react';
import { TokenSource, TokenSourceConfigurable } from 'livekit-client';
import { AgentSessionProvider } from '@/components/agents-ui/agent-session-provider';
import { AgentControlBar } from '@/components/agents-ui/agent-control-bar';
import { AgentAudioVisualizerBar } from '@/components/agents-ui/agent-audio-visualizer-bar';

export function VoiceAgent() {
  // Use useRef to prevent recreating TokenSource on each render
  const tokenSource: TokenSourceConfigurable = useRef(
    TokenSource.sandboxTokenServer({ sandboxId: 'your-sandbox-id' })
  ).current;

  // Create session using useSession hook (required for AgentSessionProvider)
  const session = useSession(tokenSource, {
    agentName: 'your-agent-name',
  });

  // Auto-start session with cleanup
  useEffect(() => {
    session.start();
    return () => session.end();
  }, []);

  return (
    <AgentSessionProvider session={session}>
      <div className="flex flex-col items-center gap-8 p-8">
        <AgentAudioVisualizerBar />
        <AgentControlBar />
      </div>
    </AgentSessionProvider>
  );
}
```

### Production example with token endpoint

```tsx
'use client';

import { useRef, useEffect } from 'react';
import { useSession } from '@livekit/components-react';
import { TokenSource, TokenSourceConfigurable } from 'livekit-client';
import { AgentSessionProvider } from '@/components/agents-ui/agent-session-provider';
import { AgentControlBar } from '@/components/agents-ui/agent-control-bar';
import { AgentAudioVisualizerBar } from '@/components/agents-ui/agent-audio-visualizer-bar';

export function VoiceAgent() {
  const tokenSource: TokenSourceConfigurable = useRef(
    TokenSource.endpoint('/api/token')
  ).current;

  const session = useSession(tokenSource, {
    roomName: 'my-room',
    participantIdentity: 'user-123',
    participantName: 'John',
    agentName: 'my-agent',
  });

  useEffect(() => {
    session.start();
    return () => session.end();
  }, []);

  return (
    <AgentSessionProvider session={session}>
      <div className="flex flex-col items-center gap-8 p-8">
        <AgentAudioVisualizerBar />
        <AgentControlBar />
      </div>
    </AgentSessionProvider>
  );
}
```

## Core components

### AgentSessionProvider

Required wrapper that provides session state to all child components. It wraps `SessionProvider` from `@livekit/components-react` and includes `RoomAudioRenderer` for audio playback.

You must create a session using `useSession` from `@livekit/components-react` and pass it to `AgentSessionProvider`:

```tsx
import { useRef, useEffect } from 'react';
import { useSession } from '@livekit/components-react';
import { TokenSource, TokenSourceConfigurable } from 'livekit-client';
import { AgentSessionProvider } from '@/components/agents-ui/agent-session-provider';

function MyApp() {
  // Create tokenSource with useRef to prevent recreation
  const tokenSource: TokenSourceConfigurable = useRef(
    TokenSource.endpoint('/api/token')
  ).current;

  // Create session using useSession hook (required)
  const session = useSession(tokenSource, { agentName: 'your-agent' });

  // Start session when component mounts
  useEffect(() => {
    session.start();
    return () => session.end();
  }, []);

  return (
    <AgentSessionProvider session={session}>
      {/* All Agents UI components must be inside this provider */}
    </AgentSessionProvider>
  );
}
```

### AgentControlBar

Combined media controls with visualizer:

```tsx
<AgentControlBar />
```

### Audio visualizers

Five visualization styles:

```tsx
// Bar visualizer (horizontal bars)
<AgentAudioVisualizerBar />

// Grid visualizer (dot matrix)
<AgentAudioVisualizerGrid />

// Radial visualizer (circular)
<AgentAudioVisualizerRadial />

// Wave visualizer (waveform)
<AgentAudioVisualizerWave />

// Aura visualizer (ambient glow effect)
<AgentAudioVisualizerAura />
```

### Media controls

Individual track controls:

```tsx
// Toggle microphone
<AgentTrackToggle source="microphone" />

// Toggle camera
<AgentTrackToggle source="camera" />

// Toggle screen share
<AgentTrackToggle source="screen_share" />

// Full track control with label
<AgentTrackControl source="microphone" />
```

### Chat components

Display conversation transcripts:

```tsx
// Full chat transcript
<AgentChatTranscript />

// Typing/thinking indicator
<AgentChatIndicator />
```

### Session controls

```tsx
// Disconnect button
<AgentDisconnectButton />

// Start audio (for browsers requiring user interaction)
<StartAudioButton />
```

## Agent states

The AgentSessionProvider tracks these states:

- `initializing` - Agent is starting up
- `listening` - Agent is listening for user input
- `thinking` - Agent is processing/generating response
- `speaking` - Agent is speaking

Use these states to customize your UI with the local `useAgentState` hook (installed with the Agents UI components):

```tsx
// This hook is local to your project (copied via shadcn CLI)
import { useAgentState } from '@/components/agents-ui/hooks/use-agent-state';

function StatusIndicator() {
  const state = useAgentState();
  
  return (
    <div className="flex items-center gap-2">
      <div className={cn(
        "w-2 h-2 rounded-full",
        state === "speaking" && "bg-green-500",
        state === "listening" && "bg-blue-500",
        state === "thinking" && "bg-yellow-500 animate-pulse",
      )} />
      <span className="capitalize">{state}</span>
    </div>
  );
}
```

## Styling

Components use Tailwind CSS and support className overrides:

```tsx
<AgentAudioVisualizerBar 
  className="h-32 w-64 bg-slate-900 rounded-lg"
/>

<AgentControlBar 
  className="gap-4 p-4 bg-white/10 backdrop-blur rounded-full"
/>
```

## Customization

Since components are copied to your project, you can modify them directly:

```tsx
// components/agents-ui/agent-control-bar.tsx
export function AgentControlBar({ className }: { className?: string }) {
  return (
    <div className={cn("flex items-center gap-2", className)}>
      {/* Customize the layout, add/remove controls */}
      <AgentTrackToggle source="microphone" />
      <AgentAudioVisualizerBar className="flex-1" />
      <AgentDisconnectButton />
    </div>
  );
}
```

## Required packages

Install both `livekit-client` and `@livekit/components-react`:

```bash
npm install livekit-client @livekit/components-react
```

These packages provide:
- `TokenSource` from `livekit-client` - Factory for creating token sources (sandbox, endpoint, custom)
- `useSession` from `@livekit/components-react` - Required hook for creating sessions for `AgentSessionProvider`

You do NOT need UI components from `@livekit/components-react` (like `LiveKitRoom`, `BarVisualizer`, or `VoiceAssistantControlBar`) when using Agents UI components. Use Agents UI components instead for the UI.

## Using hooks from @livekit/components-react

Agents UI requires `@livekit/components-react` for the `useSession` hook. You can also use additional hooks from this package for custom behavior. These hooks work inside `AgentSessionProvider`:

**Required hook:**

- `useSession` - Creates the session object required by `AgentSessionProvider`

**Additional hooks for custom behavior:**

- `useAgent` - Get full agent state with lifecycle helpers (requires session from `useSession`)
- `useVoiceAssistant` - Get agent state, tracks, and transcriptions
- `useTrackToggle` - Build custom track toggle buttons
- `useChat` - Send and receive chat messages
- `useParticipants` - Access all participants in the room
- `useConnectionState` - Monitor connection status

```tsx
import { useVoiceAssistant } from '@livekit/components-react';

// This works inside AgentSessionProvider
function CustomAgentDisplay() {
  const { state, audioTrack, agentTranscriptions } = useVoiceAssistant();
  
  return (
    <div>
      <p>Agent is {state}</p>
      {agentTranscriptions.map((t) => (
        <p key={t.id}>{t.text}</p>
      ))}
    </div>
  );
}
```

See the **livekit-react-hooks** skill for full hook documentation.

## Best practices

1. **Always wrap with AgentSessionProvider** - All Agents UI components require this context.
2. **Use useSession to create sessions** - Create a session with `useSession` from `@livekit/components-react` and pass it to `AgentSessionProvider`.
3. **Use useRef for TokenSource** - Always wrap `TokenSource` creation in `useRef` to prevent recreation on each render.
4. **Start and end sessions properly** - Call `session.start()` in a `useEffect` and `session.end()` in the cleanup function.
5. **Handle audio permissions** - Use StartAudioButton for browsers requiring user interaction.
6. **Customize via Tailwind** - Use className props for styling adjustments.
7. **Modify source directly** - Components are copied to your project for full control.
