---
name: durable-task-dotnet
description: Build durable, fault-tolerant workflows in .NET using the Durable Task SDK with Azure Durable Task Scheduler. Use when creating orchestrations, activities, entities, or implementing patterns like function chaining, fan-out/fan-in, human interaction, or stateful agents. Applies to any .NET application requiring durable execution, state persistence, or distributed transactions without Azure Functions dependency.
---

# Durable Task .NET SDK with Durable Task Scheduler

Build fault-tolerant, stateful workflows in .NET applications using the Durable Task SDK connected to Azure Durable Task Scheduler.

## Quick Start

### Required NuGet Packages

```xml
<ItemGroup>
  <PackageReference Include="Microsoft.DurableTask.Client.AzureManaged" Version="1.*" />
  <PackageReference Include="Microsoft.DurableTask.Worker.AzureManaged" Version="1.*" />
  <PackageReference Include="Microsoft.DurableTask.Generators" Version="1.*" OutputItemType="Analyzer" />
  <PackageReference Include="Azure.Identity" Version="1.*" />
  <PackageReference Include="Grpc.Net.Client" Version="2.*" />
</ItemGroup>
```

### Minimal Worker Setup

```csharp
using Microsoft.DurableTask;
using Microsoft.DurableTask.Worker;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = Host.CreateApplicationBuilder(args);

// Connection string format: "Endpoint={url};TaskHub={name};Authentication={type}"
var connectionString = Environment.GetEnvironmentVariable("DURABLE_TASK_SCHEDULER_CONNECTION_STRING") 
    ?? "Endpoint=http://localhost:8080;TaskHub=default;Authentication=None";

builder.Services.AddDurableTaskWorker()
    .AddTasks(registry =>
    {
        registry.AddAllGeneratedTasks(); // Registers all [DurableTask] decorated classes
    })
    .UseDurableTaskScheduler(connectionString);

var host = builder.Build();
await host.RunAsync();
```

### Minimal Client Setup

```csharp
using Microsoft.DurableTask.Client;

var connectionString = Environment.GetEnvironmentVariable("DURABLE_TASK_SCHEDULER_CONNECTION_STRING")
    ?? "Endpoint=http://localhost:8080;TaskHub=default;Authentication=None";

var client = DurableTaskClientBuilder.UseDurableTaskScheduler(connectionString).Build();

// Schedule an orchestration
string instanceId = await client.ScheduleNewOrchestrationInstanceAsync("MyOrchestration", input);

// Wait for completion
var result = await client.WaitForInstanceCompletionAsync(instanceId, getInputsAndOutputs: true);
```

## Pattern Selection Guide

| Pattern | Use When |
|---------|----------|
| **Function Chaining** | Sequential steps where each depends on the previous |
| **Fan-Out/Fan-In** | Parallel processing with aggregated results |
| **Human Interaction** | Workflow pauses for external input/approval |
| **Durable Entities** | Stateful objects with operations (counters, accounts) |
| **Sub-Orchestrations** | Reusable workflow components or version isolation |

See [references/patterns.md](references/patterns.md) for detailed implementations.

## Orchestration Structure

### Basic Orchestration

```csharp
[DurableTask(nameof(MyOrchestration))]
public class MyOrchestration : TaskOrchestrator<string, string>
{
    public override async Task<string> RunAsync(TaskOrchestrationContext context, string input)
    {
        // Call activities
        var result1 = await context.CallActivityAsync<string>(nameof(Step1Activity), input);
        var result2 = await context.CallActivityAsync<string>(nameof(Step2Activity), result1);
        return result2;
    }
}
```

### Basic Activity

```csharp
[DurableTask(nameof(MyActivity))]
public class MyActivity : TaskActivity<string, string>
{
    private readonly ILogger<MyActivity> _logger;
    
    public MyActivity(ILoggerFactory loggerFactory)
    {
        _logger = loggerFactory.CreateLogger<MyActivity>();
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
Orchestrations replay from history - all code MUST be deterministic:

**NEVER do inside orchestrations:**
- `DateTime.Now`, `DateTime.UtcNow` → Use `context.CurrentUtcDateTime`
- `Guid.NewGuid()` → Use `context.NewGuid()`
- `Random` → Pass random values from activities
- Direct I/O, HTTP calls, database access → Move to activities
- `Task.Delay()` → Use `context.CreateTimer()`
- Non-deterministic LINQ (parallel, unordered)

**ALWAYS safe:**
- `context.CallActivityAsync<T>()`
- `context.CallSubOrchestrationAsync<T>()`
- `context.CreateTimer()`
- `context.WaitForExternalEvent<T>()`
- `context.CurrentUtcDateTime`
- `context.NewGuid()`
- `context.SetCustomStatus()`

### Error Handling

```csharp
public override async Task<string> RunAsync(TaskOrchestrationContext context, string input)
{
    try
    {
        return await context.CallActivityAsync<string>(nameof(RiskyActivity), input);
    }
    catch (TaskFailedException ex)
    {
        // Activity failed - implement compensation or retry
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

## Connection & Authentication

### Connection String Formats

```csharp
// Local emulator (no auth)
"Endpoint=http://localhost:8080;TaskHub=default;Authentication=None"

// Azure with DefaultAzureCredential
"Endpoint=https://my-scheduler.region.durabletask.io;TaskHub=my-hub;Authentication=DefaultAzure"

// Azure with Managed Identity
"Endpoint=https://my-scheduler.region.durabletask.io;TaskHub=my-hub;Authentication=ManagedIdentity"

// Azure with specific credential
"Endpoint=https://my-scheduler.region.durabletask.io;TaskHub=my-hub;Authentication=AzureCLI"
```

### Authentication Helper

```csharp
static string GetConnectionString()
{
    var endpoint = Environment.GetEnvironmentVariable("ENDPOINT") ?? "http://localhost:8080";
    var taskHub = Environment.GetEnvironmentVariable("TASKHUB") ?? "default";
    
    var authType = endpoint.StartsWith("http://localhost") ? "None" : "DefaultAzure";
    return $"Endpoint={endpoint};TaskHub={taskHub};Authentication={authType}";
}
```

## Local Development with Emulator

```bash
# Pull and run the emulator
docker pull mcr.microsoft.com/dts/dts-emulator:latest
docker run -d -p 8080:8080 -p 8082:8082 --name dts-emulator mcr.microsoft.com/dts/dts-emulator:latest

# Dashboard available at http://localhost:8082
```

## References

- **[patterns.md](references/patterns.md)** - Detailed pattern implementations (Fan-Out/Fan-In, Human Interaction, Entities, Sub-Orchestrations)
- **[setup.md](references/setup.md)** - Azure Durable Task Scheduler provisioning and deployment
