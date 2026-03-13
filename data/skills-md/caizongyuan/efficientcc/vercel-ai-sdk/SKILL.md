---
name: vercel-ai-sdk
description: This skill should be used when users need to work with the Vercel AI SDK for building AI-powered applications. It provides comprehensive guidance on core APIs (generateText, streamText), UI components (useChat, useCompletion), tool calling, structured data generation, provider management, streaming protocols, and advanced features like middleware and custom providers.
---

# Vercel AI SDK

The Vercel AI SDK is a powerful toolkit for building AI-powered applications in TypeScript and JavaScript. It provides unified APIs for text generation, streaming, chatbot interfaces, tool calling, structured data generation, and multi-provider support. The SDK abstracts away provider differences, enabling seamless integration with OpenAI, Anthropic, Mistral, and other AI models through a consistent interface.

## Quick Start

### Installation
```bash
npm install ai
```

### Basic Patterns

**Text Generation**
```typescript
import { generateText } from 'ai';

const { text } = await generateText({
  model: yourModel,
  prompt: 'Write a story about a robot learning to love'
});
```

**Streaming**
```typescript
import { streamText } from 'ai';

const result = await streamText({
  model: yourModel,
  prompt: 'Explain quantum computing'
});

for await (const textPart of result.textStream) {
  console.log(textPart);
}
```

**Building Chatbots**
```typescript
import { useChat } from 'ai/react';

const { messages, input, handleInputChange, handleSubmit } = useChat();
```

**Tool Calling**
```typescript
import { generateText, tool } from 'ai';
import { z } from 'zod';

const { text } = await generateText({
  model: yourModel,
  tools: {
    weather: tool({
      description: 'Get weather for a location',
      parameters: z.object({
        city: z.string(),
      }),
      execute: async ({ city }) => {
        return getWeather(city);
      },
    }),
  },
});
```

## Core Workflows

### Text Generation & Streaming

The SDK provides two primary functions for text generation:

- **generateText**: Use for non-interactive generation when you need the complete result
- **streamText**: Use for interactive applications requiring real-time streaming

Both functions support identical parameters for prompts, messages, tools, and settings. Key configurations include `maxTokens`, `temperature`, `topP`, and `stopSequences`. Always use `abortSignal` for cancellation in production applications.

Configure settings globally or per-request. Global settings apply across all calls using `defaultSettingsMiddleware`. Per-request settings override global configuration.

Error handling is built-in through callbacks (`onError`) and typed error objects (`AIError`, `NoTextGeneratedError`). Enable warning logging with `globalThis.AI_SDK_LOG_WARNINGS = true`.

**References**: `references/Generating-and-Streaming-Text.md`, `references/Settings.md`, `references/Error-Handling&warnings.md`

### Building Chatbots & UI

The `useChat` hook provides complete chatbot functionality with real-time streaming, state management, and error handling.

**Core Features**
- Automatic message state management
- Real-time streaming from server to client
- Built-in error handling and retry logic
- Support for tool usage and approvals
- Message persistence and resumable streams
- Custom transport configuration

**Additional Hooks**
- **useCompletion**: For text completion interfaces (non-chat)
- **useObject**: For streaming structured JSON object generation
- **readUIMessageStream**: For terminal UIs and custom stream processing

**Generative UI**: Build interfaces where LLMs generate React components dynamically. Use tools that return UI components, then render them in the chat interface with proper streaming and state reconciliation.

**Message Persistence**: Store messages server-side using `generateId()` for unique IDs. Validate messages with `validateUIMessages()` before storage. Implement message loading and saving with automatic UI updates.

**Resumable Streams**: Enable users to reconnect to ongoing AI generation using Redis storage and custom API endpoints. Stream context persists across disconnections.

**Transport Layer**: Customize message transmission with `DefaultChatTransport` or custom implementations. Configure headers, body preparation, and streaming behavior.

**References**: `references/Chatbot.md`, `references/Chatbot-Tool-Usage.md`, `references/Chatbot-Message-Persistence.md`, `references/Chatbot-Resume-Streams.md`, `references/Completion.md`, `references/Generative-User-Interfaces.md`, `references/Object-Generation.md`, `references/Transport.md`

### Tool Calling

Tool calling enables LLMs to execute functions and use the results to formulate responses.

**Definition**
Define tools using the `tool()` function with Zod schemas for parameters:

```typescript
import { tool } from 'ai';
import { z } from 'zod';

const myTool = tool({
  description: 'Tool description',
  parameters: z.object({
    param1: z.string(),
    param2: z.number(),
  }),
  execute: async (params) => {
    // Tool execution logic
    return result;
  },
});
```

**Dynamic Tools**: Use `dynamicTool()` for tools determined at runtime or with dynamic parameters.

**Multi-Step Tool Calling**: The model can call tools multiple times in a single generation. Use `maxSteps` or `stepCountIs()` to control execution. Use `stopWhen()` to conditionally stop based on tool results.

**Tool Approval in Chatbots**: Implement server-side tools (executed automatically) and client-side tools (require user approval). Use `addToolOutput()` to provide results and `addToolApprovalResponse()` for user decisions.

**Error Handling**: Handle tool execution errors gracefully. The model can retry failed tools or continue based on error information.

**References**: `references/Tool-Calling.md`, `references/Chatbot-Tool-Usage.md`

### Structured Data Generation

Generate type-safe structured data using `Output` helpers with Zod schemas.

**Output.object**: Generate complete JSON objects with schema validation
```typescript
const { object } = await generateText({
  model: yourModel,
  output: Output.object({
    schema: z.object({
      name: z.string(),
      age: z.number(),
    }),
  }),
});
```

**Output.array**: Generate arrays with typed elements
**Output.choice**: Generate single values from a defined set of options
**Output.json**: Flexible JSON generation when schema is less strict

For streaming structured data, use `useObject` hook with real-time partial updates. The UI receives incrementally updated objects as generation progresses.

**Best Practices**: Use clear schema descriptions, leverage `.describe()` for field documentation, and test schema robustness with edge cases. Consider provider compatibility when designing complex schemas.

**References**: `references/Generating-Structured-Data.md`, `references/Object-Generation.md`, `references/Prompt-Engineering.md`

### Provider Configuration

**Provider Registry**: Manage multiple providers with `createProviderRegistry()`. Configure different providers for different use cases and switch between them using model aliases.

**Custom Providers**: Build custom providers using the Provider V3 specification. Implement `LanguageModelV3` interface with `doGenerate` and `doStream` methods. Use helper functions like `postJsonToApi` for HTTP requests.

**Model Settings**: Configure default settings per-provider using `defaultSettingsMiddleware`. Apply temperature, max tokens, and other configurations automatically.

**Multi-Provider Setups**: Use `wrapLanguageModel` to chain providers, add telemetry, or modify parameters. Combine multiple providers for A/B testing or fallback strategies.

**References**: `references/Provider&Model-Management.md`, `references/Writing-Custom-Provider.md`

### Advanced Features

**Language Model Middleware**: Intercept and modify all language model calls using `wrapLanguageModel()`. Built-in middleware includes `extractReasoningMiddleware` and `defaultSettingsMiddleware`. Create custom middleware for logging, parameter transformation, or response modification.

**Model Context Protocol (MCP)**: Connect to MCP servers providing tools, resources, and prompts. Use `createMCPClient()` with HTTP, SSE, or stdio transports. Access tools via `mcpClient.tools` and resources via `mcpClient.listResources()`.

**Telemetry**: Enable OpenTelemetry observability with `experimental_telemetry`. Collect spans, attributes, and metrics from `generateText`, `streamText`, and other SDK functions.

**Testing**: Use `MockLanguageModelV3` and `MockEmbeddingModelV3` for deterministic testing without real LLM calls. Simulate streaming with `simulateReadableStream()`.

**Stream Protocols**: Understand how data streams from backend to frontend using AI SDK protocols. Use `toUIMessageStreamResponse` and `toTextStreamResponse` helpers.

**Custom Data Streaming**: Stream application data alongside AI responses using `createUIMessageStream()` and `writer.write()`. Handle data reconciliation with client-side `onData` callbacks.

**References**: `references/Language-Model-Middleware.md`, `references/Model-Context-Protocol(MCP).md`, `references/Telemetry.md`, `references/Testing.md`, `references/Stream-Protocols.md`, `references/Streaming-Custom-Data.md`

### Media Processing

**Embeddings**: Generate embeddings with `embed()` or batch with `embedMany()`. Calculate similarity with `cosineSimilarity()`. Wrap embedding models with `wrapEmbeddingModel()` for customization.

**Reranking**: Improve search relevance with `rerank()`. Reorder documents using specialized models from Cohere, Bedrock, or other providers.

**Image Generation**: Generate images with `generateImage()`. Handle `NoImageGeneratedError` for failed generations. Configure providers like OpenAI or Vertex.

**Speech**: Generate speech with `experimental_generateSpeech()`. Support for multiple speech providers including OpenAI and LMNT.

**Transcription**: Transcribe audio to text with `experimental_transcribe()`. Handle `NoTranscriptGeneratedError` for empty results.

**References**: `references/Embeddings.md`, `references/Reranking.md`, `references/Image-Generation.md`, `references/Speech.md`, `references/Transcription.md`

## Key APIs by Category

### Core APIs
- **generateText**: Generate complete text non-interactively
- **streamText**: Stream text for interactive applications
- **smoothStream**: Smooth streaming for better UX
- **Output.object**: Generate structured JSON objects
- **Output.array**: Generate typed arrays
- **Output.choice**: Generate from predefined choices
- **Output.json**: Flexible JSON generation
- **tool**: Define tools with Zod schemas
- **dynamicTool**: Define runtime-dynamic tools
- **stopWhen**: Conditionally stop tool execution
- **stepCountIs**: Control multi-step tool calling

### UI Hooks
- **useChat**: Build chatbots with streaming and state management
- **useCompletion**: Text completion interface
- **useObject**: Stream structured JSON objects
- **readUIMessageStream**: Process streams for custom UIs
- **DefaultChatTransport**: Configure chat message transmission
- **prepareSendMessagesRequest**: Prepare chat API requests

### Provider & Model Management
- **customProvider**: Create custom AI providers
- **createProviderRegistry**: Manage multiple providers
- **wrapLanguageModel**: Middleware for language models
- **defaultSettingsMiddleware**: Apply default model settings
- **transformParams**: Transform request parameters

### Advanced Features
- **createMCPClient**: Connect to MCP servers
- **experimental_telemetry**: Enable OpenTelemetry
- **MockLanguageModelV3**: Test with mocked language models
- **simulateReadableStream**: Test streaming behavior
- **createUIMessageStream**: Custom data streaming
- **extractReasoningMiddleware**: Extract model reasoning

### Media APIs
- **embed**: Generate single embedding
- **embedMany**: Generate batch embeddings
- **cosineSimilarity**: Calculate embedding similarity
- **rerank**: Reorder documents by relevance
- **generateImage**: Generate images from text
- **experimental_generateSpeech**: Text-to-speech generation
- **experimental_transcribe**: Audio-to-text transcription

### Utility & Configuration
- **maxTokens, temperature, topP**: Configure generation parameters
- **abortSignal**: Cancel ongoing requests
- **onError**: Handle errors globally
- **validateUIMessages**: Validate chat messages
- **generateId**: Generate unique message IDs
- **toUIMessageStreamResponse**: Format UI message streams
- **toTextStreamResponse**: Format text streams

## When to Reference Original Docs

Consult detailed documentation in the `references/` directory for:

**Core Implementation Details**
- **Generating-and-Streaming-Text.md**: Deep dive into text generation, streaming transformations, and advanced patterns
- **Settings.md**: Complete reference for all configuration options and their effects
- **Error-Handling&warnings.md**: Comprehensive error handling strategies and warning types
- **Prompt-Engineering.md**: Best practices for prompts, tools, and schema design

**Chatbot & UI Development**
- **Chatbot.md**: Complete chatbot implementation guide with all features
- **Chatbot-Tool-Usage.md**: Server-side, client-side, and user approval tool workflows
- **Chatbot-Message-Persistence.md**: File-based storage, validation, and ID generation
- **Chatbot-Resume-Streams.md**: Redis-backed resumable stream implementation
- **Completion.md**: useCompletion hook patterns and examples
- **Generative-User-Interfaces.md**: Dynamic component generation from LLM output
- **Object-Generation.md**: Real-time structured object streaming
- **Message-Metadata.md**: Attach and access custom message metadata
- **Reading-UI-Message-Streams.md**: Terminal UI patterns and custom processing
- **Transport.md**: Custom transport implementation and configuration

**Tools & Structured Data**
- **Tool-Calling.md**: Complete tool calling guide with patterns and edge cases
- **Generating-Structured-Data.md**: All Output helpers and schema design

**Provider & Advanced Features**
- **Provider&Model-Management.md**: Multi-provider setups, registries, and configuration
- **Writing-Custom-Provider.md**: Build providers matching V3 specification
- **Language-Model-Middleware.md**: Built-in and custom middleware patterns
- **Model-Context-Protocol(MCP).md**: MCP client setup and usage
- **Stream-Protocols.md**: Backend-to-frontend streaming architecture
- **Streaming-Custom-Data.md**: Custom data streaming with reconciliation
- **Telemetry.md**: OpenTelemetry integration and observability
- **Testing.md**: Mock providers and test helpers

**Media Processing**
- **Embeddings.md**: Embedding generation, batching, and similarity
- **Reranking.md**: Document reranking for search relevance
- **Image-Generation.md**: Image generation with multiple providers
- **Speech.md**: Text-to-speech generation
- **Transcription.md**: Audio-to-text transcription

Each reference document contains comprehensive examples, edge case handling, type signatures, and production-ready patterns. Reference them when implementing specific features or encountering complex scenarios beyond basic usage.
