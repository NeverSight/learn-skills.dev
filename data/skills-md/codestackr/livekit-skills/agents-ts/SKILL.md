---
name: agents-ts
description: Build LiveKit Agent backends in TypeScript or JavaScript. Use this skill when creating voice AI agents, voice assistants, or any realtime AI application using LiveKit's Node.js Agents SDK (@livekit/agents-js). Covers AgentSession, Agent class, function tools with zod, STT/LLM/TTS models, turn detection, and realtime models.
---

# LiveKit Agents TypeScript SDK

Build voice AI agents with LiveKit's TypeScript/Node.js Agents SDK.

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
- ./references/agent-session.md -- AgentSession lifecycle, events, and configuration
- ./references/tools.md -- Function tools with zod schemas
- ./references/models.md -- STT, LLM, TTS plugins and realtime models

## Installation

```bash
pnpm add @livekit/agents@1.x \
    @livekit/agents-plugin-silero@1.x \
    @livekit/agents-plugin-livekit@1.x \
    @livekit/noise-cancellation-node@0.x \
    dotenv
```

## Environment variables

Use the LiveKit CLI to load your credentials into a `.env.local` file:

```bash
lk app env -w
```

Or manually create a `.env.local` file:

```bash
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
LIVEKIT_URL=wss://your-project.livekit.cloud
```

## Quick start

### Basic agent with STT-LLM-TTS pipeline

```typescript
import {
  type JobContext,
  type JobProcess,
  WorkerOptions,
  cli,
  defineAgent,
  voice,
} from '@livekit/agents';
import * as livekit from '@livekit/agents-plugin-livekit';
import * as silero from '@livekit/agents-plugin-silero';
import { BackgroundVoiceCancellation } from '@livekit/noise-cancellation-node';
import { fileURLToPath } from 'node:url';
import dotenv from 'dotenv';

dotenv.config({ path: '.env.local' });

export default defineAgent({
  prewarm: async (proc: JobProcess) => {
    proc.userData.vad = await silero.VAD.load();
  },
  entry: async (ctx: JobContext) => {
    const vad = ctx.proc.userData.vad! as silero.VAD;
    
    const assistant = new voice.Agent({
      instructions: `You are a helpful voice AI assistant.
        Keep responses concise, 1-3 sentences. No markdown or emojis.`,
    });

    const session = new voice.AgentSession({
      vad,
      stt: "assemblyai/universal-streaming:en",
      llm: "openai/gpt-4.1-mini",
      tts: "cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
      turnDetection: new livekit.turnDetector.MultilingualModel(),
    });

    await session.start({
      agent: assistant,
      room: ctx.room,
      inputOptions: {
        // For standard web/mobile participants use BackgroundVoiceCancellation()
        // For telephony/SIP applications use TelephonyBackgroundVoiceCancellation()
        noiseCancellation: BackgroundVoiceCancellation(),
      },
    });

    await ctx.connect();

    const handle = session.generateReply({
      instructions: 'Greet the user and offer your assistance.',
    });
    await handle.waitForPlayout();
  },
});

cli.runApp(new WorkerOptions({ agent: fileURLToPath(import.meta.url) }));
```

### Basic agent with realtime model

```typescript
import {
  type JobContext,
  WorkerOptions,
  cli,
  defineAgent,
  voice,
} from '@livekit/agents';
import * as openai from '@livekit/agents-plugin-openai';
import { BackgroundVoiceCancellation } from '@livekit/noise-cancellation-node';
import { fileURLToPath } from 'node:url';
import dotenv from 'dotenv';

dotenv.config({ path: '.env.local' });

export default defineAgent({
  entry: async (ctx: JobContext) => {
    const assistant = new voice.Agent({
      instructions: 'You are a helpful voice AI assistant.',
    });

    const session = new voice.AgentSession({
      llm: new openai.realtime.RealtimeModel({
        voice: 'coral',
      }),
    });

    await session.start({
      agent: assistant,
      room: ctx.room,
      inputOptions: {
        // For standard web/mobile participants use BackgroundVoiceCancellation()
        // For telephony/SIP applications use TelephonyBackgroundVoiceCancellation()
        noiseCancellation: BackgroundVoiceCancellation(),
      },
    });

    await ctx.connect();

    const handle = session.generateReply({
      instructions: 'Greet the user and offer your assistance.',
    });
    await handle.waitForPlayout();
  },
});

cli.runApp(new WorkerOptions({ agent: fileURLToPath(import.meta.url) }));
```

## Core concepts

### defineAgent

The entry point for defining your agent:

```typescript
import { defineAgent, type JobContext, type JobProcess } from '@livekit/agents';

export default defineAgent({
  // Optional: Preload models before jobs start
  prewarm: async (proc: JobProcess) => {
    proc.userData.vad = await silero.VAD.load();
  },
  
  // Required: Main entry point for each job
  entry: async (ctx: JobContext) => {
    // Your agent logic here
  },
});
```

### voice.Agent

Define agent behavior. You can use the `voice.Agent` constructor directly or extend the class:

```typescript
import { voice, llm } from '@livekit/agents';
import { z } from 'zod';

// Option 1: Direct instantiation
const assistant = new voice.Agent({
  instructions: 'Your system prompt here',
  tools: {
    getWeather: llm.tool({
      description: 'Get the current weather for a location',
      parameters: z.object({
        location: z.string().describe('The city name'),
      }),
      execute: async ({ location }) => {
        return `The weather in ${location} is sunny and 72°F`;
      },
    }),
  },
});

// Option 2: Class extension (recommended for complex agents)
class Assistant extends voice.Agent {
  constructor() {
    super({
      instructions: 'Your system prompt here',
      tools: {
        getWeather: llm.tool({
          description: 'Get the current weather for a location',
          parameters: z.object({
            location: z.string().describe('The city name'),
          }),
          execute: async ({ location }) => {
            return `The weather in ${location} is sunny and 72°F`;
          },
        }),
      },
    });
  }
}
```

### voice.AgentSession

The session orchestrates the voice pipeline:

```typescript
const session = new voice.AgentSession({
  stt: "assemblyai/universal-streaming:en",
  llm: "openai/gpt-4.1-mini",
  tts: "cartesia/sonic-3:voice_id",
  vad: await silero.VAD.load(),
  turnDetection: new livekit.turnDetector.MultilingualModel(),
});
```

Key methods:
- `session.start({ agent, room })` - Start the session
- `session.say(text)` - Speak text directly
- `session.generateReply({ instructions })` - Generate LLM response
- `session.interrupt()` - Stop current speech
- `session.updateAgent(newAgent)` - Switch to different agent

## Running the agent

Add scripts to `package.json`:

```json
{
  "scripts": {
    "dev": "tsx agent.ts dev",
    "build": "tsc",
    "start": "node agent.js start",
    "download-files": "tsc && node agent.js download-files"
  }
}
```

```bash
# Development mode with auto-reload
pnpm dev

# Production mode
pnpm build && pnpm start

# Download required model files
pnpm download-files
```

## LiveKit Inference model strings

Use model strings for simple configuration without API keys:

**STT (Speech-to-Text)**:
- `"assemblyai/universal-streaming:en"` - AssemblyAI streaming
- `"deepgram/nova-3:en"` - Deepgram Nova
- `"cartesia/ink"` - Cartesia STT

**LLM (Large Language Model)**:
- `"openai/gpt-4.1-mini"` - GPT-4.1 mini (recommended)
- `"openai/gpt-4.1"` - GPT-4.1
- `"openai/gpt-5"` - GPT-5
- `"gemini/gemini-3-flash"` - Gemini 3 Flash

**TTS (Text-to-Speech)**:
- `"cartesia/sonic-3:{voice_id}"` - Cartesia Sonic 3
- `"elevenlabs/eleven_turbo_v2_5:{voice_id}"` - ElevenLabs
- `"deepgram/aura:{voice}"` - Deepgram Aura

## Package structure

```
@livekit/agents                    # Core framework
@livekit/agents-plugin-openai      # OpenAI (LLM, STT, TTS, Realtime)
@livekit/agents-plugin-deepgram    # Deepgram (STT, TTS)
@livekit/agents-plugin-elevenlabs  # ElevenLabs (TTS)
@livekit/agents-plugin-silero      # Silero (VAD)
@livekit/agents-plugin-livekit     # Turn detector
@livekit/agents-plugin-gemini      # Google Gemini
@livekit/agents-plugin-groq        # Groq
@livekit/noise-cancellation-node   # Noise cancellation
```

## Best practices

1. **Always use LiveKit Inference model strings** as the default for STT, LLM, and TTS. This eliminates the need to manage individual provider API keys. Only use plugins when you specifically need custom models, voice cloning, or self-hosted models.
2. **Use defineAgent pattern** for proper lifecycle management.
3. **Prewarm VAD models** in the `prewarm` function for faster job startup.
4. **Use the appropriate noise cancellation** for your use case:
   - `BackgroundVoiceCancellation()` for standard web/mobile participants
   - `TelephonyBackgroundVoiceCancellation()` for SIP/telephony applications
5. **Call ctx.connect()** after session.start() to connect to the room.
6. **Await generateReply** with `waitForPlayout()` when you need to wait for the greeting to complete.
7. **Use `lk app env -w`** to load LiveKit Cloud credentials into your environment.
