---
name: researching-azure-ai-sdk
description: Provides research patterns for Foundry Agent Service SDK. Use when implementing agent features, looking up SDK methods, finding code samples, or troubleshooting Azure.AI.Projects API usage.
---

# Researching Azure AI SDK

**CRITICAL**: Don't guess SDK usage. Follow this research workflow.

## Subagent Delegation for Research

**Multi-repo research blows up context** (1000+ tokens per file). Delegate to subagent for:
- Searching across 3+ repositories
- Reading 5+ files for patterns
- Comprehensive API surface exploration
- Finding all usages of a method/type

### Delegation Pattern

```text
runSubagent(
  prompt: "RESEARCH task - do NOT write code.
    
    **Question**: [specific SDK question]
    
    **Search these sources in order**:
    1. Azure.AI.Projects SDK: github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Projects
    2. Azure.AI.Agents.Persistent samples: .../Azure.AI.Agents.Persistent/samples
    3. Microsoft Foundry Samples: github.com/microsoft-foundry/foundry-samples
    
    **Find**:
    - Method signatures for [specific API]
    - Usage examples (pseudocode only)
    - Any gotchas or edge cases
    
    **Return** (max 20 lines):
    - Key method name and signature
    - Code pattern (pseudocode)
    - File path where found (for later reference)
    
    Do NOT include full file contents.",
  description: "SDK research: [topic]"
)
```

### When to Delegate vs Inline

| Delegate to Subagent | Keep Inline |
|----------------------|-------------|
| Multi-repo code search | Local codebase grep |
| Finding all usages | Known method lookup |
| API surface exploration | Single file read |
| Pattern comparison | Quick signature check |
| Sample discovery | Using known pattern |

## SDK Architecture Overview

The Foundry Agent Service SDK has **two API surfaces** for agents:

| API | Endpoint | ID Format | SDK Access |
|-----|----------|-----------|------------|
| **v2 Agents API** | `/agents/` | Human-readable (e.g., `dadjokes`) | `AIProjectClient.Agents` |
| **OpenAI Assistants API** | `/assistants/` | OpenAI format (e.g., `asst_xxx`) | `PersistentAgentsClient` |

**This project uses v2 Agents API** for human-readable agent IDs.

```text
Azure.AI.Projects (Main Entry Point)
├── AIProjectClient
│   ├── .Agents.GetAgentAsync() → AgentRecord (v2 Agents API)
│   ├── .GetPersistentAgentsClient() → PersistentAgentsClient (Assistants API)
│   └── .OpenAI.GetProjectResponsesClientForAgent() → ProjectResponsesClient (Responses API)
└── Sub-namespaces:
    ├── Azure.AI.Projects.OpenAI (Responses API, conversations)
    └── OpenAI.Responses (streaming types)
```

## 1. Primary SDK Repository (Start Here)

**Azure.AI.Projects SDK**: https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Projects

- README: Core client patterns, authentication, basic operations
- Samples: `tests/Samples/` folder with full examples

**Azure.AI.Agents.Persistent SDK**: https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Agents.Persistent

- 33+ samples covering streaming, file search, Bing grounding, MCP, Azure Functions
- Key samples:
  - `Sample9_PersistentAgents_Streaming.md` - Basic streaming pattern
  - `Sample8_PersistentAgents_FunctionsWithStreaming.md` - Tool calls with streaming
  - `Sample27_PersistentAgents_MCP_Streaming.md` - MCP server integration

## 2. Official Quickstart Samples

**Microsoft Foundry Samples**: https://github.com/microsoft-foundry/foundry-samples

- `samples/csharp/quickstart/quickstart-chat-with-agent.cs` - **Responses API pattern**
- `samples/csharp/quickstart/` - Multiple quickstart examples

**Key pattern from official quickstart**:
```csharp
AIProjectClient projectClient = new(new Uri(projectEndpoint), new AzureCliCredential());
ProjectConversation conversation = projectClient.OpenAI.Conversations.CreateProjectConversation();
ProjectResponsesClient responsesClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(
    defaultAgent: agentName,
    defaultConversationId: conversation.Id);
ResponseResult response = responsesClient.CreateResponse("Your prompt");
```

## 3. Azure Architecture Center Samples

**Baseline Chat App**: https://github.com/Azure-Samples/microsoft-foundry-baseline

- Full production architecture with Entra ID auth
- `website/chatui/Controllers/ChatController.cs` - SSE streaming pattern

**Basic Chat Example**: https://github.com/Azure-Samples/microsoft-foundry-basic

- Simpler example of Foundry agent chat integration

**Semantic Kernel + Foundry**: https://github.com/Azure-Samples/app-service-agentic-semantic-kernel-ai-foundry-agent

- Integration pattern for Semantic Kernel with Foundry Agents

## 4. UI Reference Samples (React Patterns)

### Primary UI Reference

**Azure AI Agents React Sample**: https://github.com/Azure-Samples/get-started-with-ai-agents

This is the **primary UI reference** for this project. Many UI patterns were borrowed from here:
- Chat interface components
- Message rendering with citations/annotations
- Streaming text display
- Responsive layout patterns

### Agent Framework DevUI (Python)

**Agent Framework DevUI**: https://github.com/microsoft/agent-framework/tree/main/python/packages/devui

Alternative UI patterns for agent development:
- Development-focused chat interface
- Multi-agent visualization
- Tool call debugging UI

### UI Component Inspiration

When implementing new UI features, check these sources in order:
1. `get-started-with-ai-agents` - React + TypeScript patterns for chat UI
2. `agent-framework/devui` - Development UI patterns
3. Fluent UI Copilot Components - Base component library (already used)

## 5. Semantic Kernel Integration

**Repository**: https://github.com/microsoft/semantic-kernel

**Relevant paths**:
- `dotnet/src/Agents/OpenAI/` - OpenAI Responses API integration
- `dotnet/samples/GettingStartedWithAgents/AzureAIAgent/`
- `dotnet/samples/Concepts/Agents/` (Step##_*.cs files)

## 6. OpenAI .NET SDK (Streaming Types)

**Repository**: https://github.com/openai/openai-dotnet

- `docs/guides/streaming-responses/` - Streaming patterns
- Source of `StreamingResponseOutputTextDeltaUpdate` and related types

## 7. GitHub Code Search (For Specific Patterns)

Use GitHub search to find usage examples:

```text
# Find streaming patterns
"StreamingResponseOutputTextDeltaUpdate language:csharp"

# Find Responses API usage
"ProjectResponsesClient CreateResponseStreamingAsync language:csharp"

# Find conversation patterns
"ProjectConversation GetProjectResponsesClientForAgent language:csharp"
```

## Current SDK Packages

| Package | Purpose |
|---------|---------|
| `Azure.AI.Projects` | Main entry point, `AIProjectClient`, v2 Agents API, Responses API |
| `Azure.Identity` | Authentication (`AzureDeveloperCliCredential`, `ManagedIdentityCredential`) |
| `Microsoft.Identity.Web` | JWT Bearer authentication for API |

**Note**: Check `WebApp.Api.csproj` for current versions. This project requires `Azure.AI.Projects` with v2 Agents API support (`AIProjectClient.Agents`).

**Sub-namespaces available** (not separate packages):
- `Azure.AI.Projects.OpenAI` - Responses API, conversations
- `OpenAI.Responses` - Streaming types

**Available Package**: `Microsoft.Agents.AI.AzureAI` (prerelease) supports v2 Agents API via `AIProjectClient` extension methods. See "Microsoft Agent Framework" section below.

**Key Resources**:
- NuGet (Azure.AI.Projects): https://www.nuget.org/packages/Azure.AI.Projects
- SDK Source: https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Projects
- v2 Migration Guide: https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/migrate
- API Reference: https://learn.microsoft.com/en-us/dotnet/api/azure.ai.projects
- Product Docs: https://learn.microsoft.com/azure/ai-studio/
- Infrastructure Bicep Templates: https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep

## Official Azure AI Foundry Agent Service Documentation

**Start here** when researching agent capabilities, limits, or new features:

| Topic | URL |
|-------|-----|
| **Agent Service overview** | https://learn.microsoft.com/azure/ai-foundry/agents/overview |
| **Quickstart: Create an agent** | https://learn.microsoft.com/azure/ai-foundry/agents/quickstart |
| **Agent concepts & architecture** | https://learn.microsoft.com/azure/ai-foundry/agents/concepts |
| **Supported models** | https://learn.microsoft.com/azure/ai-foundry/agents/concepts/supported-models |
| **Tools: File Search** | https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools/file-search |
| **Tools: Code Interpreter** | https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools/code-interpreter |
| **Tools: Bing Grounding** | https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools/bing-grounding |
| **Tools: Azure AI Search** | https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools/azure-ai-search |
| **Tools: Azure Functions** | https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools/azure-functions |
| **MCP server tools** | https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools/mcp-servers |
| **v2 Agents API migration** | https://learn.microsoft.com/azure/ai-foundry/agents/how-to/migrate |
| **REST API reference** | https://learn.microsoft.com/rest/api/azureai/agents |
| **Quotas & limits** | https://learn.microsoft.com/azure/ai-foundry/agents/concepts/quotas-limits |

**Agent Framework (Microsoft.Agents) docs**:

| Topic | URL |
|-------|-----|
| **Agent Framework overview** | https://learn.microsoft.com/microsoft-agents/overview |
| **Agent Framework .NET SDK** | https://github.com/microsoft/Agents-for-net |
| **NuGet package** | https://www.nuget.org/packages/Microsoft.Agents.AI.AzureAI |
| **IChatClient abstraction** | https://learn.microsoft.com/dotnet/api/microsoft.extensions.ai.ichatclient |

## Annotation Types in Responses

The SDK provides several annotation types for citations (from `OpenAI.Responses` namespace):

| Type | Class | Use Case | Key Properties |
|------|-------|----------|----------------|
| URI Citation | `UriCitationMessageAnnotation` | Bing, Azure AI Search, SharePoint | `Uri`, `Title`, `StartIndex`, `EndIndex` |
| File Citation | `FileCitationMessageAnnotation` | File search (vector stores) | `FileId`, `Filename`, `Index` |
| File Path | `FilePathMessageAnnotation` | Code interpreter output | `FileId`, `Index` |
| Container Citation | `ContainerFileCitationMessageAnnotation` | Container file citations | `FileId`, `Filename`, `ContainerId`, `StartIndex`, `EndIndex` |

**Note**: `FileCitationMessageAnnotation` uses `Index` (not `StartIndex`/`EndIndex`) per the SDK. See `ExtractAnnotations()` in `AgentFrameworkService.cs` for mapping to `AnnotationInfo`.

### Container File Download

The C# SDK does not yet have a typed client for container file downloads. Use the REST API directly with a bearer token scoped to `https://ai.azure.com/.default`:

```
GET {projectEndpoint}/openai/v1/containers/{containerId}/files/{fileId}/content
Authorization: Bearer {token}
```

For standard (non-container) files (`cfile_` prefix absent), use `OpenAI.Files.FileClient` instead. The backend endpoint `GET /api/files/{fileId}?containerId={id}` abstracts this: it routes `cfile_`-prefixed files through the REST API and standard files through `FileClient`.

## Streaming Response Types (from OpenAI.Responses namespace)

| Type | Purpose |
|------|---------|
| `StreamingResponseOutputTextDeltaUpdate` | Text content delta chunks |
| `StreamingResponseOutputItemDoneUpdate` | Item completion signals |
| `StreamingResponseCompletedUpdate` | Response completion with usage |
| `ResponseItem` | Base type for response items |

**Pattern used in this project**:
```csharp
await foreach (var update in responsesClient.CreateResponseStreamingAsync(...))
{
    if (update is StreamingResponseOutputTextDeltaUpdate textUpdate)
        yield return new StreamChunk { Text = textUpdate.Delta };
    if (update is StreamingResponseOutputItemDoneUpdate itemDone)
        // Extract annotations from itemDone.Item
}
```

## Microsoft Agent Framework (Used — Hybrid Approach)

**Package**: `Microsoft.Agents.AI.AzureAI` (see `WebApp.Api.csproj` for version)

**Status**: ✅ **Installed and active**. Agent Framework supports v2 Agents API via `AIProjectClient` extension methods.

### Current Usage Pattern

This project uses a **hybrid approach**:
- **Agent Framework** for simplified agent loading and metadata
- **Direct SDK** for streaming (required for specialized response types)

```csharp
// ✅ Agent loading via Agent Framework (simple)
ChatClientAgent agent = await aiProjectClient.GetAIAgentAsync(
    name: "dadjokes",           // Human-readable agent name
    cancellationToken: ct);

// Access AgentVersion for metadata
AgentVersion? version = agent.GetService<AgentVersion>();
var definition = version?.Definition as PromptAgentDefinition;

// ❌ Direct SDK for streaming (Agent Framework can't do this yet)
ProjectResponsesClient responsesClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(
    new AgentReference(_agentId), conversationId);
await foreach (var update in responsesClient.CreateResponseStreamingAsync(...)) { }
```

### Why Not Full Agent Framework for Streaming?

`ChatClientAgent.RunStreamingAsync()` returns `IAsyncEnumerable<AgentRunResponseUpdate>`, which provides:
- `Text` — text content (✅ works)
- `RawRepresentation` — underlying SDK object (can cast at runtime)

**The problem**: The `IChatClient` abstraction doesn't directly expose:
- `McpToolCallApprovalRequestItem` for MCP approval flows
- `FileSearchCallResponseItem` for file search quotes
- `MessageResponseItem.OutputTextAnnotations` for citations

**Workaround exists but adds complexity**: Cast `RawRepresentation` to underlying types:
```csharp
await foreach (var update in agent.RunStreamingAsync(message, thread))
{
    if (update.RawRepresentation is StreamingResponseOutputItemDoneUpdate itemDone)
    {
        if (itemDone.Item is McpToolCallApprovalRequestItem mcpApproval)
        {
            // Handle MCP approval...
        }
    }
}
```

**Why we use direct SDK instead**: 
1. Casting `RawRepresentation` defeats the abstraction benefit
2. MCP approval flow requires `ResponseItem.CreateMcpApprovalResponseItem()` anyway
3. Direct SDK approach is clearer and matches SDK samples

### What Agent Framework IS Good For

- **Simple streaming** — just text output with `.Text` property
- **Multi-agent orchestration** — sequential, concurrent, handoff patterns
- **Graph-based workflows** — streaming with checkpointing
- **Built-in observability** — OpenTelemetry integration
- **Tool invocation** — automatic `AIFunction` handling

### Future Consideration

When Agent Framework matures to expose annotations/MCP through its abstractions, we could simplify to:
```csharp
// Hypothetical future API
await foreach (var update in agent.RunStreamingAsync(message, thread))
{
    if (update.IsMcpApproval) { }       // Doesn't exist yet
    if (update.HasAnnotations) { }      // Doesn't exist yet  
}
```

Track progress at: https://github.com/microsoft/Agents-for-net

**Resources**:
- NuGet: https://www.nuget.org/packages/Microsoft.Agents.AI.AzureAI
- Documentation: https://learn.microsoft.com/agent-framework/
- Source: https://github.com/microsoft/Agents-for-net/tree/main/src/libraries
- API Reference: https://learn.microsoft.com/en-us/dotnet/api/microsoft.agents.ai.chatclientagent.runstreamingasync

## Migration Notes

`AIProjectClient` requires a project endpoint URI (not a connection string):

```csharp
var projectClient = new AIProjectClient(new Uri(projectEndpoint), new DefaultAzureCredential());
```

Connection-string constructors are deprecated. See: https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Projects/AGENTS_MIGRATION_GUIDE.md

## Additional SDK Resources

### Fetch SDK Source from GitHub (Authoritative)

Type definitions live in these repos—read them directly:

- **Azure.AI.Projects source**: https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Projects/src
- **Azure.AI.Agents.Persistent samples**: https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Agents.Persistent/samples
- **OpenAI.Responses types**: https://github.com/openai/openai-dotnet/tree/main/src



### GitHub Code Search

Search across all .NET codebases for real-world usage:

```text
"ProjectResponsesClient CreateResponseStreamingAsync" language:csharp
"StreamingResponseOutputTextDeltaUpdate" language:csharp
```

This finds how other projects use these APIs, revealing patterns and edge cases.

### PowerShell Reflection (When Docs Lag Behind)

Use when SDK docs are outdated or incomplete — the DLLs are the ground truth.

Works even when `dotnet build` fails (loads from NuGet cache):

```powershell
cd backend/WebApp.Api; dotnet restore

# Option A: Load from build output (requires successful build)
$asm = [Reflection.Assembly]::LoadFrom((Resolve-Path "bin/Debug/net9.0/Azure.AI.Projects.dll"))

# Option B: Load from NuGet cache (works even if build fails — use for pre-release migrations)
$dll = Get-ChildItem "$env:USERPROFILE\.nuget\packages\azure.ai.projects" -Recurse -Filter "Azure.AI.Projects.dll" | Select-Object -Last 1
$asm = [Reflection.Assembly]::LoadFrom($dll.FullName)

# Find types matching a pattern
$asm.GetExportedTypes() | Where-Object { $_.Name -like "*Streaming*" } | ForEach-Object { $_.FullName }

# Get method signatures with parameter details
$type = $asm.GetType("Azure.AI.Projects.OpenAI.ProjectResponsesClient")
$type.GetMethods() | Where-Object { $_.Name -like "*Async*" } | Select-Object Name, ReturnType, @{N='Params';E={($_.GetParameters() | ForEach-Object { "$($_.ParameterType.Name) $($_.Name)" }) -join ', '}}
```

**Agent Framework assemblies** (for Microsoft.Agents.AI.AzureAI migrations):

```powershell
# Load Agent Framework DLL from NuGet cache
$pkg = Get-ChildItem "$env:USERPROFILE\.nuget\packages\microsoft.agents.ai.azureai" -Recurse -Filter "Microsoft.Agents.AI.AzureAI.dll" | Select-Object -Last 1
$asm = [Reflection.Assembly]::LoadFrom($pkg.FullName)

# Dump all exported types to see what changed between versions
$asm.GetExportedTypes() | ForEach-Object { $_.FullName } | Sort-Object

# Check if types you depend on still exist
@("ChatClientAgent", "AgentVersion", "PromptAgentDefinition", "AgentReference") | ForEach-Object {
    $match = $asm.GetExportedTypes() | Where-Object { $_.Name -eq $_ }
    if ($match) { Write-Host "FOUND: $($match.FullName)" } else { Write-Host "MISSING: $_" -ForegroundColor Red }
}

# Inspect extension methods (GetAIAgentAsync, etc.)
$asm.GetExportedTypes() | Where-Object { $_.GetMethods([Reflection.BindingFlags]::Static -bor [Reflection.BindingFlags]::Public) | Where-Object { $_.IsDefined([Runtime.CompilerServices.ExtensionAttribute], $false) } } | ForEach-Object {
    $_.GetMethods() | Where-Object { $_.IsDefined([Runtime.CompilerServices.ExtensionAttribute], $false) } | ForEach-Object { Write-Host "$($_.DeclaringType.Name).$($_.Name)" }
}
```

**When to use**: SDK upgrade with breaking changes, pre-release packages where docs lag, verifying actual API surface before writing migration code.

**Key insight**: Load from NuGet cache (`$env:USERPROFILE\.nuget\packages\`) to inspect the *new* version's types even when the build is broken.
