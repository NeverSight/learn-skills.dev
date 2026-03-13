---
name: implementing-chat-streaming
description: Provides SSE streaming patterns for the chat API and frontend. Use when implementing or modifying chat streaming, handling SSE events, or troubleshooting message flow between frontend and backend.
---

# Chat Streaming Implementation

## Backend: SSE Endpoint

```csharp
app.MapPost("/api/chat/stream", async (
    ChatRequest request,
    AgentFrameworkService agentService,
    HttpContext httpContext,
    CancellationToken cancellationToken) =>
{
    httpContext.Response.Headers.Append("Content-Type", "text/event-stream");
    httpContext.Response.Headers.Append("Cache-Control", "no-cache");
    
    var conversationId = request.ConversationId 
        ?? await agentService.CreateConversationAsync(request.Message, cancellationToken);
    
    // Send conversation ID first
    await httpContext.Response.WriteAsync(
        $"data: {{\"type\":\"conversationId\",\"conversationId\":\"{conversationId}\"}}\n\n", 
        cancellationToken);
    await httpContext.Response.Body.FlushAsync(cancellationToken);
    
    // Stream chunks
    await foreach (var chunk in agentService.StreamMessageAsync(
        conversationId, request.Message, request.ImageDataUris, cancellationToken))
    {
        var json = JsonSerializer.Serialize(new { type = "chunk", content = chunk });
        await httpContext.Response.WriteAsync($"data: {json}\n\n", cancellationToken);
        await httpContext.Response.Body.FlushAsync(cancellationToken);
    }
    
    await httpContext.Response.WriteAsync("data: {\"type\":\"done\"}\n\n", cancellationToken);
})
.RequireAuthorization("RequireChatScope");
```

## Backend: IAsyncEnumerable Service

**Actual return type**: `IAsyncEnumerable<StreamChunk>` (not raw strings)

**Why direct SDK?** Uses `ProjectResponsesClient` directly (not Agent Framework's `ChatClientAgent.RunStreamingAsync()`) because the `IChatClient` abstraction doesn't expose MCP approvals, file search quotes, or citation annotations. See `.github/skills/researching-azure-ai-sdk/SKILL.md` for full rationale.

```csharp
public async IAsyncEnumerable<StreamChunk> StreamMessageAsync(
    string conversationId,
    string message,
    List<string>? imageDataUris = null,
    [EnumeratorCancellation] CancellationToken cancellationToken = default)
{
    ObjectDisposedException.ThrowIf(_disposed, this);
    
    // Stream response - yields StreamChunk with text deltas OR annotations
    await foreach (var update in responsesClient.CreateResponseStreamingAsync(...))
    {
        if (update is StreamingResponseOutputTextDeltaUpdate deltaUpdate)
        {
            yield return StreamChunk.Text(deltaUpdate.Delta);
        }
        else if (update is StreamingResponseOutputItemDoneUpdate itemDoneUpdate)
        {
            var annotations = ExtractAnnotations(itemDoneUpdate.Item, fileSearchQuotes);
            if (annotations.Count > 0)
            {
                yield return StreamChunk.WithAnnotations(annotations);
            }
        }
    }
}
```

**StreamChunk model** (`backend/WebApp.Api/Models/StreamChunk.cs`):
- `IsText` / `TextDelta` - Text content
- `HasAnnotations` / `Annotations` - Citation metadata

## Frontend: Action Flow

```text
CHAT_SEND_MESSAGE 
  → CHAT_ADD_ASSISTANT_MESSAGE 
  → CHAT_START_STREAM 
  → (repeat CHAT_STREAM_CHUNK) 
  → CHAT_STREAM_ANNOTATIONS (optional, for citations)
  → CHAT_STREAM_COMPLETE (with usage metrics)
```

If user cancels: `CHAT_CANCEL_STREAM` sets status to `idle`.

## Frontend: ChatService Pattern

See: `frontend/src/services/ChatService.ts`

Key patterns:
- AbortController for cancellation
- EventSource or fetch with ReadableStream
- Parse SSE `data:` lines
- Dispatch actions for each event type

## Image Validation

**Backend limits** (see `AzureAIAgentService.cs`):
- Max 5 images per request
- Max 5MB per image (decoded)
- Allowed: `image/png`, `image/jpeg`, `image/gif`, `image/webp`

**Frontend limits** (see `frontend/src/utils/fileAttachments.ts`):
- Same limits with user-friendly error messages
- Toast notifications for validation feedback

---

## Project-Specific: Full Endpoint Implementation

```csharp
app.MapPost("/api/chat/stream", async (
    ChatRequest request,
    AgentFrameworkService agentService,
    HttpContext httpContext,
    IHostEnvironment env,
    CancellationToken cancellationToken) =>
{
    httpContext.Response.Headers.Append("Content-Type", "text/event-stream");
    httpContext.Response.Headers.Append("Cache-Control", "no-cache");
    
    var conversationId = request.ConversationId 
        ?? await agentService.CreateConversationAsync(request.Message, cancellationToken);
    
    await httpContext.Response.WriteAsync(
        $"data: {{\"type\":\"conversationId\",\"conversationId\":\"{conversationId}\"}}\n\n", 
        cancellationToken);
    await httpContext.Response.Body.FlushAsync(cancellationToken);
    
    await foreach (var chunk in agentService.StreamMessageAsync(
        conversationId, request.Message, request.ImageDataUris, cancellationToken))
    {
        var json = System.Text.Json.JsonSerializer.Serialize(new { type = "chunk", content = chunk });
        await httpContext.Response.WriteAsync($"data: {json}\n\n", cancellationToken);
        await httpContext.Response.Body.FlushAsync(cancellationToken);
    }
    
    await httpContext.Response.WriteAsync("data: {\"type\":\"done\"}\n\n", cancellationToken);
})
.RequireAuthorization("RequireChatScope")
.WithName("StreamChatMessage");
```

## Project-Specific: Service Implementation

**See**: `backend/WebApp.Api/Services/AgentFrameworkService.cs`

**Key patterns in `StreamMessageAsync`**:
- Disposal guard before processing
- Multi-modal message support (text + image data URIs)
- `IAsyncEnumerable<StreamChunk>` with `[EnumeratorCancellation]`
- `StreamingResponseOutputTextDeltaUpdate` for text content
- `StreamingResponseOutputItemDoneUpdate` for annotations
- Collects file search quotes via `FileSearchCallResponseItem` for citation context
- Usage captured from `StreamingResponseCompletedUpdate`

## Project-Specific: Frontend State Flow

```text
CHAT_SEND_MESSAGE 
  → CHAT_ADD_ASSISTANT_MESSAGE 
  → CHAT_START_STREAM 
  → (repeat CHAT_STREAM_CHUNK) 
  → CHAT_STREAM_ANNOTATIONS (optional, for citations)
  → CHAT_STREAM_COMPLETE (with usage: promptTokens, completionTokens, totalTokens, duration)
```

**Cancel**: `CHAT_CANCEL_STREAM` sets status to `idle` and re-enables input.

**Error**: `CHAT_ERROR` with `AppError` containing message, optional retry action, timestamp.

## SSE Event Types

| Event Type | Payload | Description |
|------------|---------|-------------|
| `conversationId` | `{ conversationId: string }` | Sent first for new conversations |
| `chunk` | `{ content: string }` | Text delta from agent response |
| `annotations` | `{ annotations: [...] }` | Citations (uri_citation, file_citation, etc.) |
| `usage` | `{ duration, promptTokens, completionTokens, totalTokens }` | Token metrics |
| `done` | `{}` | Stream complete |
| `error` | `{ message: string }` | Error occurred |

## Project-Specific: Dev Logging

Each state change prints (dev only):

```text
🔄 [HH:MM:SS] ACTION_TYPE
Action: { … }
Changes: { field: before → after }
```

## Related Skills

- **writing-csharp-code** - Backend coding standards and AgentFrameworkService patterns
- **writing-typescript-code** - Frontend React patterns and ChatService implementation
- **troubleshooting-authentication** - Token acquisition for authenticated streaming
