---
name: writing-csharp-code
description: Provides C# and ASP.NET Core coding standards for this repository. Use when writing or modifying C# code, implementing API endpoints, configuring middleware, or working with authentication in the backend.
---

# C# Coding Standards

**Goal**: Write clean, secure ASP.NET Core code with proper authentication

## Hot Reload Development Workflow

**The backend runs in watch mode** (`dotnet watch run`). When you edit C# code:

1. **Save the file** - .NET automatically recompiles
2. **Check the terminal** - Look for compilation output in the "Backend: ASP.NET Core API" terminal
3. **Verify via console logs** - New requests will use updated code immediately

**VS Code Tasks** (use `Run Task` command or check terminal panel):
- `Backend: ASP.NET Core API` - Runs `dotnet watch run` with live recompilation
- Logs are visible directly in VS Code terminal

**No restart needed** - Just edit, save, and test. Watch for compilation errors in the terminal.

**Testing changes**: Use Playwright browser tools to make requests and check browser console logs, or call endpoints directly.

## Minimal API Patterns

Use typed request models, CancellationToken, and IHostEnvironment:

```csharp
app.MapPost("/api/endpoint", async (
    RequestModel request,
    MyService service,
    IHostEnvironment env,
    CancellationToken cancellationToken) =>
{
    try
    {
        var result = await service.ProcessAsync(request, cancellationToken);
        return Results.Ok(result);
    }
    catch (Exception ex)
    {
        return ErrorResponseFactory.CreateFromException(ex, env);
    }
})
.RequireAuthorization("RequireChatScope")
.WithName("EndpointName");
```

## Authentication Setup

**JWT Bearer with Entra ID**:

```csharp
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApi(options =>
    {
        builder.Configuration.Bind("AzureAd", options);
        options.TokenValidationParameters.ValidAudiences = new[]
        {
            builder.Configuration["AzureAd:ClientId"],
            $"api://{builder.Configuration["AzureAd:ClientId"]}"
        };
    }, options => builder.Configuration.Bind("AzureAd", options));
```

## Async Best Practices

```csharp
// ✅ Use async/await with CancellationToken
public async Task<Result> ProcessAsync(Request req, CancellationToken ct)
{
    return await _service.ExecuteAsync(req, ct);
}

// ❌ Never block on async
var result = _service.ExecuteAsync(req).Result;  // WRONG
```

## IAsyncEnumerable for Streaming

```csharp
public async IAsyncEnumerable<string> StreamAsync(
    string input,
    [EnumeratorCancellation] CancellationToken cancellationToken = default)
{
    await foreach (var chunk in source.WithCancellation(cancellationToken))
    {
        yield return chunk;
    }
}
```

## Credential Strategy

```csharp
TokenCredential credential = env.IsDevelopment()
    ? new ChainedTokenCredential(
        new AzureCliCredential(),
        new AzureDeveloperCliCredential())  // Supports 'azd auth login'
    : new ManagedIdentityCredential(miClientId); // User-assigned MI in production
```

**Why ChainedTokenCredential**: Avoids `DefaultAzureCredential`'s "fail fast" mode issues. Explicit, predictable credential chain.

## IDisposable Pattern

```csharp
public class MyService : IDisposable
{
    private readonly SemaphoreSlim _lock = new(1, 1);
    private readonly CancellationTokenSource _disposeCts = new();
    private bool _disposed;

    public void DoWork()
    {
        ObjectDisposedException.ThrowIf(_disposed, this);
        // ...
    }

    public void Dispose()
    {
        if (_disposed) return;
        _disposed = true;
        
        // Cancel pending operations first
        try { _disposeCts.Cancel(); }
        catch (ObjectDisposedException) { }
        
        _disposeCts.Dispose();
        _lock.Dispose();
    }
}
```

## Error Responses (RFC 7807)

Use `ErrorResponseFactory.CreateFromException()` for consistent error responses.

See: `backend/WebApp.Api/Models/ErrorResponse.cs`

## Common Mistakes

- ❌ Using `.Result` or `.Wait()` on async methods
- ❌ Forgetting `CancellationToken` parameter
- ❌ Missing `.RequireAuthorization()` on endpoints
- ❌ Exposing internal errors in production
- ❌ Forgetting disposal guards in `IDisposable`

---

## Project-Specific: Middleware Pipeline

**Goal**: Serve static files → validate auth → route APIs → SPA fallback

```csharp
app.UseDefaultFiles();     // index.html for /
app.UseStaticFiles();      // wwwroot/* assets  
app.UseCors();             // Dev only
app.UseAuthentication();   // Validate JWT
app.UseAuthorization();    // Enforce scope
// Map endpoints here
app.MapFallbackToFile("index.html");  // MUST BE LAST
```

## Project-Specific: AgentFrameworkService

**See**: `backend/WebApp.Api/Services/AgentFrameworkService.cs`

**SDK Packages**:
- `Azure.AI.Projects` — Main entry point, v2 Agents API (see `*.csproj` for version)
- `Microsoft.Agents.AI.AzureAI` — Agent Framework extensions (see `*.csproj` for version)

**Sub-namespaces**: `Azure.AI.Projects.OpenAI`, `OpenAI.Responses`, `Microsoft.Agents.AI`, `Microsoft.Extensions.AI`

**Key patterns**:
- `IDisposable` implementation with `_agentLock.Dispose()`
- Disposal guards (`ObjectDisposedException.ThrowIf`) in all public methods
- Environment-aware credential selection (ChainedTokenCredential vs ManagedIdentityCredential)
- Cached `ChatClientAgent` instance with `SemaphoreSlim` for thread safety
- Configuration validation (`AI_AGENT_ENDPOINT`, `AI_AGENT_ID`)

**Agent Loading** (via Microsoft Agent Framework extension methods):
```csharp
// Uses Agent Framework for simplified agent loading
ChatClientAgent agent = await projectClient.GetAIAgentAsync(
    name: agentId,            // Human-readable agent name
    cancellationToken: ct);

// Access AgentVersion from ChatClientAgent for metadata
AgentVersion? version = agent.GetService<AgentVersion>();
```

**Streaming** (direct ProjectResponsesClient — required for specialized types):
```csharp
// Direct SDK for streaming — IChatClient doesn't expose MCP/annotations
ProjectResponsesClient responsesClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(
    new AgentReference(agentId), conversationId);
```

**Why direct streaming?** The `IChatClient` abstraction doesn't expose:
- `McpToolCallApprovalRequestItem` for MCP approval flows
- `FileSearchCallResponseItem` for file search quotes
- `MessageResponseItem.OutputTextAnnotations` for citations

**Streaming Pattern**: Returns `IAsyncEnumerable<StreamChunk>` where `StreamChunk` contains either:
- Text delta (`chunk.IsText`, `chunk.TextDelta`)
- Annotations/citations (`chunk.HasAnnotations`, `chunk.Annotations`)

**Streaming Response Types** (from `OpenAI.Responses`):
- `StreamingResponseOutputTextDeltaUpdate` - Text content delta
- `StreamingResponseOutputItemDoneUpdate` - Item completion (has annotations)
- `StreamingResponseCompletedUpdate` - Response completion with usage stats

**Image Validation** (in `BuildUserMessage()`):
- Maximum 5 images per request
- Maximum 5MB per image (decoded size)
- Allowed: `image/png`, `image/jpeg`, `image/gif`, `image/webp`
- Returns HTTP 400 with validation details if constraints violated

**Annotation Types** (from `OpenAI.Responses`): 
- `UriCitationMessageAnnotation` - Bing, Azure AI Search, SharePoint
- `FileCitationMessageAnnotation` - File search (vector stores)
- `FilePathMessageAnnotation` - Code interpreter output
- `ContainerFileCitationMessageAnnotation` - Container file citations

**Starter Prompts**: Parsed from agent metadata (`starterPrompts` key, newline-separated).

## Project-Specific: Configuration Loading

Auto-load `.env` file before building configuration:

```csharp
var envFile = Path.Combine(Directory.GetCurrentDirectory(), ".env");
if (File.Exists(envFile))
{
    foreach (var line in File.ReadAllLines(envFile)
        .Where(l => !string.IsNullOrWhiteSpace(l) && !l.StartsWith("#")))
    {
        var parts = line.Split('=', 2);
        if (parts.Length == 2)
            Environment.SetEnvironmentVariable(parts[0].Trim(), parts[1].Trim());
    }
}
```

## Troubleshooting SDK Issues

**When things break**: SDK type mismatches and missing methods almost always happen after a package upgrade. Check `backend/WebApp.Api/WebApp.Api.csproj` for current versions:

- `Azure.AI.Projects` - check `WebApp.Api.csproj` for current version
- `Azure.Identity` - check `WebApp.Api.csproj` for current version

If types don't match documentation or samples, verify you're looking at docs for the **same version** installed in the project.

### GitHub SDK Source (For Deep Dives)

When you need to understand SDK internals, fetch the actual source:

- **Azure.AI.Projects**: https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Projects/src
- **SDK samples**: https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Agents.Persistent/samples
- **OpenAI.Responses**: https://github.com/openai/openai-dotnet/tree/main/src

### Quick Structure Checks (CLI)

For project-level overviews only—use sparingly:

```powershell
# List public types in backend (overview, not deep exploration)
Get-ChildItem -Path backend -Recurse -Include *.cs | 
    Select-String -Pattern "^\s*(public|internal)\s+(class|record|interface)\s+(\w+)" |
    ForEach-Object { $_.Matches.Groups[3].Value } | Sort-Object -Unique

# Find IDisposable implementations
Get-ChildItem -Path backend -Recurse -Include *.cs |
    Select-String -Pattern ":\s*.*IDisposable"
```

**Use for**: Quick inventory of what exists. Follow up with pattern search or IDE navigation for understanding.

### PowerShell Reflection for .NET Assemblies

Use when you need to discover exact type members on any .NET assembly (especially beta SDKs):

```powershell
# 1. Build first to ensure DLLs are current
cd backend/WebApp.Api; dotnet build --no-restore

# 2. Find and load any assembly by name
$dll = Get-ChildItem -Path "bin/Debug" -Recurse -Filter "SomePackage.dll" | Select-Object -First 1
$asm = [System.Reflection.Assembly]::LoadFrom($dll.FullName)

# 3. Inspect a specific type's properties
$type = $asm.GetType("SomeNamespace.SomeClass")
Write-Host "Type: $($type.FullName)"
Write-Host "Assembly: $($asm.GetName().Name) v$($asm.GetName().Version)"
$type.GetProperties() | ForEach-Object { Write-Host "  $($_.PropertyType.Name) $($_.Name)" }

# 4. Check base type for inherited members
Write-Host "Base: $($type.BaseType.Name)"
$type.BaseType.GetProperties() | ForEach-Object { Write-Host "    $($_.PropertyType.Name) $($_.Name)" }
```

**Finding types by pattern** (when you don't know exact namespace):

```powershell
# Search for types matching a pattern
$asm.GetTypes() | Where-Object { $_.Name -like "*Response*" } | ForEach-Object { Write-Host $_.FullName }

# Find methods on a type
$type.GetMethods() | Where-Object { $_.Name -like "*Async*" } | Select-Object Name, ReturnType
```

**Common assemblies to inspect** (after `dotnet build`):

| Assembly | Path | Contains |
|----------|------|----------|
| `Azure.AI.Projects.dll` | bin/Debug/net9.0/ | AIProjectClient, AgentRecord, Conversations |
| `Microsoft.Agents.AI.AzureAI.dll` | bin/Debug/net9.0/ | ChatClientAgent, AgentVersion, GetAIAgentAsync extension |
| `Microsoft.Agents.AI.Abstractions.dll` | bin/Debug/net9.0/ | IChatClient, AgentReference, PromptAgentDefinition |
| `OpenAI.dll` | bin/Debug/net9.0/ | ResponseItem, StreamingResponse*, annotations |
| `Azure.Identity.dll` | bin/Debug/net9.0/ | Credential types |

**When to use**: Beta SDK properties aren't in docs, IDE tooltips are incomplete, or you need to verify a type's actual API surface.

**Limitation**: Returns raw API surface without intent or usage guidance. Combine with GitHub source for context.

## Related Skills

- **implementing-chat-streaming** - SSE streaming patterns and backend endpoint implementation
- **troubleshooting-authentication** - MSAL/JWT debugging for 401 errors
- **researching-azure-ai-sdk** - SDK research workflow and sample repositories
