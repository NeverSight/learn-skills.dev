---
name: durable-functions-dotnet
description: Build durable, fault-tolerant workflows using Azure Durable Functions with .NET isolated worker and Durable Task Scheduler backend. Use when creating serverless orchestrations, activities, entities, or implementing patterns like function chaining, fan-out/fan-in, async HTTP APIs, human interaction, monitoring, or stateful aggregators. Applies to Azure Functions apps requiring durable execution, state persistence, or distributed coordination with built-in HTTP management APIs and Azure integration.
---

# Azure Durable Functions (.NET Isolated) with Durable Task Scheduler

Build fault-tolerant, stateful serverless workflows using Azure Durable Functions connected to Azure Durable Task Scheduler.

## Quick Start

### Required NuGet Packages

```xml
<ItemGroup>
  <PackageReference Include="Microsoft.Azure.Functions.Worker" Version="2.*" />
  <PackageReference Include="Microsoft.Azure.Functions.Worker.Sdk" Version="2.*" />
  <PackageReference Include="Microsoft.Azure.Functions.Worker.Extensions.Http" Version="3.*" />
  <PackageReference Include="Microsoft.Azure.Functions.Worker.Extensions.Http.AspNetCore" Version="1.*" />
  <PackageReference Include="Microsoft.Azure.Functions.Worker.Extensions.DurableTask" Version="1.*" />
  <PackageReference Include="Microsoft.Azure.Functions.Worker.Extensions.DurableTask.AzureManaged" Version="*" />
  <PackageReference Include="Azure.Identity" Version="1.*" />
</ItemGroup>
```

### host.json Configuration (Durable Task Scheduler)

```json
{
  "version": "2.0",
  "extensions": {
    "durableTask": {
      "storageProvider": {
        "type": "azureManaged",
        "connectionStringName": "DTS_CONNECTION_STRING"
      },
      "hubName": "%TASKHUB_NAME%"
    }
  }
}
```

### local.settings.json

```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "dotnet-isolated",
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "DTS_CONNECTION_STRING": "Endpoint=http://localhost:8080;Authentication=None",
    "TASKHUB_NAME": "default"
  }
}
```

### Minimal Example (Function-Based)

```csharp
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.DurableTask;
using Microsoft.DurableTask.Client;
using Microsoft.Extensions.Logging;

public static class DurableFunctionsApp
{
    // HTTP Starter - triggers orchestration
    [Function("HttpStart")]
    public static async Task<HttpResponseData> HttpStart(
        [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = "orchestrators/{functionName}")] HttpRequestData req,
        [DurableClient] DurableTaskClient client,
        string functionName,
        FunctionContext executionContext)
    {
        string instanceId = await client.ScheduleNewOrchestrationInstanceAsync(functionName);
        
        var logger = executionContext.GetLogger("HttpStart");
        logger.LogInformation("Started orchestration with ID = '{instanceId}'", instanceId);
        
        return await client.CreateCheckStatusResponseAsync(req, instanceId);
    }

    // Orchestrator function
    [Function(nameof(MyOrchestration))]
    public static async Task<string> MyOrchestration(
        [OrchestrationTrigger] TaskOrchestrationContext context)
    {
        ILogger logger = context.CreateReplaySafeLogger(nameof(MyOrchestration));
        logger.LogInformation("Starting orchestration");
        
        var result1 = await context.CallActivityAsync<string>(nameof(SayHello), "Tokyo");
        var result2 = await context.CallActivityAsync<string>(nameof(SayHello), "Seattle");
        var result3 = await context.CallActivityAsync<string>(nameof(SayHello), "London");
        
        return $"{result1}, {result2}, {result3}";
    }

    // Activity function
    [Function(nameof(SayHello))]
    public static string SayHello([ActivityTrigger] string name, FunctionContext executionContext)
    {
        var logger = executionContext.GetLogger(nameof(SayHello));
        logger.LogInformation("Saying hello to {name}", name);
        return $"Hello {name}!";
    }
}
```

### Program.cs Setup

```csharp
using Microsoft.Extensions.Hosting;

var host = new HostBuilder()
    .ConfigureFunctionsWorkerDefaults()
    .Build();

await host.RunAsync();
```

## Pattern Selection Guide

| Pattern | Use When |
|---------|----------|
| **Function Chaining** | Sequential steps where each depends on the previous |
| **Fan-Out/Fan-In** | Parallel processing with aggregated results |
| **Async HTTP APIs** | Long-running operations with HTTP status polling |
| **Monitor** | Periodic polling with configurable timeouts |
| **Human Interaction** | Workflow pauses for external input/approval |
| **Aggregator (Entities)** | Stateful objects with operations (counters, accounts) |

See [references/patterns.md](references/patterns.md) for detailed implementations.

## Two Approaches: Function-Based vs Class-Based

### Function-Based (Default)

```csharp
[Function(nameof(MyOrchestration))]
public static async Task<string> MyOrchestration(
    [OrchestrationTrigger] TaskOrchestrationContext context)
{
    string input = context.GetInput<string>()!;
    return await context.CallActivityAsync<string>(nameof(MyActivity), input);
}

[Function(nameof(MyActivity))]
public static string MyActivity([ActivityTrigger] string input)
{
    return $"Processed: {input}";
}
```

### Class-Based (With Source Generator)

Requires `Microsoft.DurableTask.Generators` package:

```csharp
[DurableTask(nameof(MyOrchestration))]
public class MyOrchestration : TaskOrchestrator<string, string>
{
    public override async Task<string> RunAsync(TaskOrchestrationContext context, string input)
    {
        ILogger logger = context.CreateReplaySafeLogger<MyOrchestration>();
        return await context.CallActivityAsync<string>(nameof(MyActivity), input);
    }
}

[DurableTask(nameof(MyActivity))]
public class MyActivity : TaskActivity<string, string>
{
    private readonly ILogger<MyActivity> _logger;
    
    // Activities support DI - orchestrations do NOT
    public MyActivity(ILogger<MyActivity> logger)
    {
        _logger = logger;
    }

    public override Task<string> RunAsync(TaskActivityContext context, string input)
    {
        _logger.LogInformation("Processing: {Input}", input);
        return Task.FromResult($"Processed: {input}");
    }
}
```

## Critical Rules

### Orchestration Determinism

Orchestrations replay from history - all code MUST be deterministic. When an orchestration resumes, it replays all previous code to rebuild state. Non-deterministic code produces different results on replay, causing `NonDeterministicOrchestrationException`.

**NEVER do inside orchestrations:**
- `DateTime.Now`, `DateTime.UtcNow` → Use `context.CurrentUtcDateTime`
- `Guid.NewGuid()` → Use `context.NewGuid()`
- `Random` → Pass random values from activities
- Direct I/O, HTTP calls, database access → Move to activities
- `Thread.Sleep()`, `Task.Delay()` → Use `context.CreateTimer()`
- Non-deterministic LINQ (parallel, unordered)
- `Task.Run()`, `ConfigureAwait(false)`
- Static mutable variables
- Environment variables that may change → Pass as input or use activities

**ALWAYS safe:**
- `context.CallActivityAsync<T>()`
- `context.CallSubOrchestrationAsync<T>()`
- `context.CallHttpAsync()`
- `context.CreateTimer()`
- `context.WaitForExternalEvent<T>()`
- `context.CurrentUtcDateTime`
- `context.NewGuid()`
- `context.SetCustomStatus()`
- `context.CreateReplaySafeLogger()`

### Non-Determinism Patterns (WRONG vs CORRECT)

#### Getting Current Time

```csharp
// WRONG - DateTime.UtcNow returns different value on replay
[Function(nameof(BadOrchestration))]
public static async Task BadOrchestration([OrchestrationTrigger] TaskOrchestrationContext context)
{
    DateTime currentTime = DateTime.UtcNow;  // Non-deterministic!
    if (currentTime.Hour < 12)
    {
        await context.CallActivityAsync(nameof(MorningActivity), null);
    }
}

// CORRECT - context.CurrentUtcDateTime replays consistently
[Function(nameof(GoodOrchestration))]
public static async Task GoodOrchestration([OrchestrationTrigger] TaskOrchestrationContext context)
{
    DateTime currentTime = context.CurrentUtcDateTime;  // Deterministic
    if (currentTime.Hour < 12)
    {
        await context.CallActivityAsync(nameof(MorningActivity), null);
    }
}
```

#### Generating GUIDs

```csharp
// WRONG - Guid.NewGuid() generates different value on replay
[Function(nameof(BadOrchestration))]
public static async Task<string> BadOrchestration([OrchestrationTrigger] TaskOrchestrationContext context)
{
    string orderId = Guid.NewGuid().ToString();  // Non-deterministic!
    await context.CallActivityAsync(nameof(CreateOrder), orderId);
    return orderId;
}

// CORRECT - context.NewGuid() replays the same value
[Function(nameof(GoodOrchestration))]
public static async Task<string> GoodOrchestration([OrchestrationTrigger] TaskOrchestrationContext context)
{
    string orderId = context.NewGuid().ToString();  // Deterministic
    await context.CallActivityAsync(nameof(CreateOrder), orderId);
    return orderId;
}
```

#### Random Numbers

```csharp
// WRONG - Random produces different values on replay
[Function(nameof(BadOrchestration))]
public static async Task BadOrchestration([OrchestrationTrigger] TaskOrchestrationContext context)
{
    int delay = new Random().Next(1, 10);  // Non-deterministic!
    await context.CreateTimer(context.CurrentUtcDateTime.AddSeconds(delay), CancellationToken.None);
}

// CORRECT - generate random in activity, pass to orchestrator
[Function(nameof(GetRandomDelay))]
public static int GetRandomDelay([ActivityTrigger] object? input)
{
    return new Random().Next(1, 10);  // OK in activity
}

[Function(nameof(GoodOrchestration))]
public static async Task GoodOrchestration([OrchestrationTrigger] TaskOrchestrationContext context)
{
    int delay = await context.CallActivityAsync<int>(nameof(GetRandomDelay), null);
    await context.CreateTimer(context.CurrentUtcDateTime.AddSeconds(delay), CancellationToken.None);
}
```

#### Sleeping/Delays

```csharp
// WRONG - Thread.Sleep/Task.Delay don't persist and block
[Function(nameof(BadOrchestration))]
public static async Task BadOrchestration([OrchestrationTrigger] TaskOrchestrationContext context)
{
    await context.CallActivityAsync(nameof(Step1), null);
    await Task.Delay(60000);  // Non-durable! Lost on restart, wastes resources
    await context.CallActivityAsync(nameof(Step2), null);
}

// CORRECT - context.CreateTimer is durable
[Function(nameof(GoodOrchestration))]
public static async Task GoodOrchestration([OrchestrationTrigger] TaskOrchestrationContext context)
{
    await context.CallActivityAsync(nameof(Step1), null);
    await context.CreateTimer(context.CurrentUtcDateTime.AddMinutes(1), CancellationToken.None);  // Durable
    await context.CallActivityAsync(nameof(Step2), null);
}
```

#### HTTP Calls and I/O

```csharp
// WRONG - HttpClient in orchestrator is non-deterministic
[Function(nameof(BadOrchestration))]
public static async Task<string> BadOrchestration([OrchestrationTrigger] TaskOrchestrationContext context)
{
    using var client = new HttpClient();
    var response = await client.GetStringAsync("https://api.example.com/data");  // Non-deterministic!
    return response;
}

// CORRECT Option 1 - use CallHttpAsync (built-in durable HTTP)
[Function(nameof(GoodOrchestration1))]
public static async Task<string> GoodOrchestration1([OrchestrationTrigger] TaskOrchestrationContext context)
{
    DurableHttpResponse response = await context.CallHttpAsync(
        HttpMethod.Get, new Uri("https://api.example.com/data"));  // Deterministic
    return response.Content;
}

// CORRECT Option 2 - move I/O to activity
[Function(nameof(FetchData))]
public static async Task<string> FetchData([ActivityTrigger] string url)
{
    using var client = new HttpClient();
    return await client.GetStringAsync(url);  // OK in activity
}

[Function(nameof(GoodOrchestration2))]
public static async Task<string> GoodOrchestration2([OrchestrationTrigger] TaskOrchestrationContext context)
{
    return await context.CallActivityAsync<string>(nameof(FetchData), "https://api.example.com/data");
}
```

#### Database Access

```csharp
// WRONG - database query in orchestrator
[Function(nameof(BadOrchestration))]
public static async Task BadOrchestration([OrchestrationTrigger] TaskOrchestrationContext context)
{
    using var conn = new SqlConnection(connectionString);  // Non-deterministic!
    await conn.OpenAsync();
    // ...
}

// CORRECT - database access in activity
[Function(nameof(GetUser))]
public static async Task<User> GetUser([ActivityTrigger] string userId)
{
    using var conn = new SqlConnection(connectionString);  // OK in activity
    await conn.OpenAsync();
    // ...
    return user;
}

[Function(nameof(GoodOrchestration))]
public static async Task<User> GoodOrchestration([OrchestrationTrigger] TaskOrchestrationContext context)
{
    string userId = context.GetInput<string>()!;
    return await context.CallActivityAsync<User>(nameof(GetUser), userId);
}
```

#### Environment Variables

```csharp
// WRONG - env var might change between replays
[Function(nameof(BadOrchestration))]
public static async Task BadOrchestration([OrchestrationTrigger] TaskOrchestrationContext context)
{
    string apiEndpoint = Environment.GetEnvironmentVariable("API_ENDPOINT")!;  // Could change!
    await context.CallActivityAsync(nameof(CallApi), apiEndpoint);
}

// CORRECT - pass config as input
[Function(nameof(GoodOrchestration))]
public static async Task GoodOrchestration([OrchestrationTrigger] TaskOrchestrationContext context)
{
    var config = context.GetInput<WorkflowConfig>()!;
    string apiEndpoint = config.ApiEndpoint;  // From input, deterministic
    await context.CallActivityAsync(nameof(CallApi), apiEndpoint);
}

// ALSO CORRECT - read env var in activity
[Function(nameof(CallApi))]
public static async Task CallApi([ActivityTrigger] object? input)
{
    string apiEndpoint = Environment.GetEnvironmentVariable("API_ENDPOINT")!;  // OK in activity
    // make the call...
}
```

#### Collection Iteration Order

```csharp
// WRONG - Dictionary iteration order may vary
[Function(nameof(BadOrchestration))]
public static async Task BadOrchestration([OrchestrationTrigger] TaskOrchestrationContext context)
{
    var items = context.GetInput<Dictionary<string, object>>()!;
    foreach (var key in items.Keys)  // Order not guaranteed!
    {
        await context.CallActivityAsync(nameof(Process), key);
    }
}

// CORRECT - use sorted keys for deterministic order
[Function(nameof(GoodOrchestration))]
public static async Task GoodOrchestration([OrchestrationTrigger] TaskOrchestrationContext context)
{
    var items = context.GetInput<Dictionary<string, object>>()!;
    foreach (var key in items.Keys.OrderBy(k => k))  // Guaranteed order
    {
        await context.CallActivityAsync(nameof(Process), key);
    }
}
```

### Logging in Orchestrations

Use `CreateReplaySafeLogger` to avoid duplicate log entries during replay:

```csharp
[Function(nameof(MyOrchestration))]
public static async Task<string> MyOrchestration([OrchestrationTrigger] TaskOrchestrationContext context)
{
    ILogger logger = context.CreateReplaySafeLogger(nameof(MyOrchestration));
    logger.LogInformation("Orchestration started");  // Only logs once, not on each replay
    
    var result = await context.CallActivityAsync<string>(nameof(MyActivity), "input");
    
    logger.LogInformation("Activity completed with result: {Result}", result);
    return result;
}
```

### Error Handling

```csharp
[Function(nameof(OrchestrationWithErrorHandling))]
public static async Task<string> OrchestrationWithErrorHandling(
    [OrchestrationTrigger] TaskOrchestrationContext context)
{
    string input = context.GetInput<string>()!;
    try
    {
        return await context.CallActivityAsync<string>(nameof(RiskyActivity), input);
    }
    catch (TaskFailedException ex)
    {
        // Activity failed - implement compensation
        context.SetCustomStatus(new { Error = ex.Message });
        return await context.CallActivityAsync<string>(nameof(CompensationActivity), input);
    }
}
```

### Retry Policies

```csharp
var options = new TaskOptions
{
    Retry = new RetryPolicy(
        maxNumberOfAttempts: 3,
        firstRetryInterval: TimeSpan.FromSeconds(5),
        backoffCoefficient: 2.0,
        maxRetryInterval: TimeSpan.FromMinutes(1))
};

await context.CallActivityAsync<string>(nameof(UnreliableActivity), input, options);
```

## HTTP Management APIs

Durable Functions exposes built-in HTTP APIs for orchestration management:

### CreateCheckStatusResponse

```csharp
[Function("HttpStart")]
public static async Task<HttpResponseData> HttpStart(
    [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = "orchestrators/{functionName}")] HttpRequestData req,
    [DurableClient] DurableTaskClient client,
    string functionName)
{
    // Parse input from request body
    string? input = await new StreamReader(req.Body).ReadToEndAsync();
    
    string instanceId = await client.ScheduleNewOrchestrationInstanceAsync(functionName, input);
    
    // Returns 202 Accepted with management URLs in response
    return await client.CreateCheckStatusResponseAsync(req, instanceId);
}
```

Response includes:
- `statusQueryGetUri` - GET endpoint to check status
- `sendEventPostUri` - POST endpoint to raise events
- `terminatePostUri` - POST endpoint to terminate
- `purgeHistoryDeleteUri` - DELETE endpoint to purge history

### Client Operations

```csharp
[DurableClient] DurableTaskClient client

// Schedule new orchestration
string instanceId = await client.ScheduleNewOrchestrationInstanceAsync("MyOrchestration", input);

// Schedule with custom instance ID
string instanceId = await client.ScheduleNewOrchestrationInstanceAsync(
    "MyOrchestration", input, new StartOrchestrationOptions { InstanceId = "my-custom-id" });

// Get status
OrchestrationMetadata? state = await client.GetInstanceAsync(instanceId, getInputsAndOutputs: true);

// Wait for completion
OrchestrationMetadata? result = await client.WaitForInstanceCompletionAsync(
    instanceId, getInputsAndOutputs: true, cancellationToken);

// Raise external event
await client.RaiseEventAsync(instanceId, "ApprovalEvent", approvalData);

// Terminate
await client.TerminateInstanceAsync(instanceId, "User cancelled");

// Suspend/Resume
await client.SuspendInstanceAsync(instanceId, "Pausing for maintenance");
await client.ResumeInstanceAsync(instanceId, "Resuming operation");

// Purge history
await client.PurgeInstanceAsync(instanceId);
```

## Connection & Authentication

### Connection String Formats

```csharp
// Local emulator (no auth)
"Endpoint=http://localhost:8080;Authentication=None"

// Azure with Managed Identity (recommended for production)
"Endpoint=https://my-scheduler.region.durabletask.io;Authentication=ManagedIdentity"

// Azure with specific client ID (user-assigned managed identity)
"Endpoint=https://my-scheduler.region.durabletask.io;Authentication=ManagedIdentity;ClientId=<client-id>"
```

Note: Durable Task Scheduler supports identity-based authentication only - no connection strings with keys.

## Local Development with Emulator

```bash
# Start Azurite (required for Azure Functions)
azurite start

# Pull and run the Durable Task Scheduler emulator
docker pull mcr.microsoft.com/dts/dts-emulator:latest
docker run -d -p 8080:8080 -p 8082:8082 --name dts-emulator mcr.microsoft.com/dts/dts-emulator:latest

# Dashboard available at http://localhost:8082

# Start the function app
func start
```

## Durable HTTP Calls

Make HTTP calls directly from orchestrations (persisted and replay-safe):

```csharp
[Function(nameof(CallExternalApi))]
public static async Task<string> CallExternalApi([OrchestrationTrigger] TaskOrchestrationContext context)
{
    // Simple GET
    DurableHttpResponse response = await context.CallHttpAsync(HttpMethod.Get, new Uri("https://api.example.com/data"));
    
    if (response.StatusCode != HttpStatusCode.OK)
    {
        throw new Exception($"API call failed: {response.StatusCode}");
    }
    
    return response.Content;
}

// With headers and body
var request = new DurableHttpRequest(
    HttpMethod.Post,
    new Uri("https://api.example.com/data"))
{
    Headers = { ["Content-Type"] = "application/json" },
    Content = JsonSerializer.Serialize(payload)
};

DurableHttpResponse response = await context.CallHttpAsync(request);

// With managed identity authentication
var request = new DurableHttpRequest(
    HttpMethod.Get,
    new Uri("https://management.azure.com/..."))
{
    TokenSource = new ManagedIdentityTokenSource("https://management.azure.com/.default")
};
```

## References

- **[patterns.md](references/patterns.md)** - Detailed pattern implementations (Fan-Out/Fan-In, Human Interaction, Entities, Sub-Orchestrations, Monitor)
- **[setup.md](references/setup.md)** - Azure Durable Task Scheduler provisioning, deployment, and project templates
