---
name: csharp-wolverinefx
description: Build .NET applications with WolverineFX for messaging, HTTP services, and event sourcing. Use when implementing command handlers, message handlers, HTTP endpoints with WolverineFx.HTTP, transactional outbox patterns, event sourcing with Marten, CQRS architectures, cascading messages, batch message processing, or configuring transports like RabbitMQ, Azure Service Bus, or Amazon SQS.
---

# WolverineFX for .NET

## When to Use This Skill

Use this skill when:
- Building message handlers or command handlers with Wolverine
- Creating HTTP endpoints with WolverineFx.HTTP (alternative to Minimal API/MVC)
- Implementing event sourcing with Marten and Wolverine
- Setting up transactional outbox pattern for reliable messaging
- Configuring message transports (RabbitMQ, Azure Service Bus, Amazon SQS, TCP)
- Implementing CQRS with event sourcing
- Processing messages in batches
- Using cascading messages for testable, pure function handlers
- Configuring error handling and retry policies
- Pre-generating code for optimized cold starts

## Related Skills

- **`efcore-patterns`** - Entity Framework Core patterns for data access
- **`csharp-coding-standards`** - Modern C# patterns (records, pattern matching)
- **`http-client-resilience`** - Polly resilience patterns (complementary)
- **`background-services`** - Hosted services and background job patterns
- **`aspire-configuration`** - .NET Aspire orchestration

## Core Principles

1. **Low Ceremony Code** - Pure functions, method injection, minimal boilerplate
2. **Cascading Messages** - Return messages from handlers instead of injecting IMessageBus
3. **Transactional Outbox** - Guaranteed message delivery with database transactions
4. **Code Generation** - Runtime or pre-generated code for optimal performance
5. **Vertical Slice Architecture** - Organize code by feature, not technical layers
6. **Pure Functions for Business Logic** - Isolate infrastructure from business logic

## Required NuGet Packages

### Core Messaging
```xml
<PackageReference Include="Wolverine" />
<PackageReference Include="WolverineFx.Http" />
```

### Persistence Integration
```xml
<PackageReference Include="WolverineFx.Marten" />
```

### Transports
```xml
<PackageReference Include="WolverineFx.RabbitMQ" />
<PackageReference Include="WolverineFx.AzureServiceBus" />
<PackageReference Include="WolverineFx.Kafka" />
<PackageReference Include="WolverineFx.AmazonSQS" />
```

## Basic Setup

### Program.cs (ASP.NET Core)

```csharp
using JasperFx;
using Wolverine;
using Wolverine.Http;

var builder = WebApplication.CreateBuilder(args);

builder.Host.UseWolverine(opts =>
{
    opts.Policies.AutoApplyTransactions();
    opts.Policies.UseDurableLocalQueues();
});

builder.Services.AddWolverineHttp();

var app = builder.Build();

app.MapWolverineEndpoints();

return await app.RunJasperFxCommands(args);
```

## Message Handlers

### Simple Message Handler

```csharp
public record DebitAccount(long AccountId, decimal Amount);

public static class DebitAccountHandler
{
    public static void Handle(DebitAccount command, IAccountRepository repository)
    {
        repository.Debit(command.AccountId, command.Amount);
    }
}
```

### Handler with Cascading Messages

```csharp
public record CreateOrder(Guid OrderId, string[] Items);
public record OrderCreated(Guid OrderId);

public static class CreateOrderHandler
{
    public static (OrderCreated, ShipOrder) Handle(
        CreateOrder command,
        IDocumentSession session)
    {
        var order = new Order { Id = command.OrderId, Items = command.Items };
        session.Store(order);
        
        return (
            new OrderCreated(command.OrderId),
            new ShipOrder(command.OrderId)
        );
    }
}
```

### Using OutgoingMessages for Multiple Messages

```csharp
public static OutgoingMessages Handle(ProcessOrder command)
{
    var messages = new OutgoingMessages
    {
        new OrderProcessed(command.OrderId),
        new SendEmail(command.CustomerEmail, "Order processed"),
        new UpdateInventory(command.Items)
    };
    
    messages.Delay(new CleanupOrder(command.OrderId), 5.Minutes());
    
    return messages;
}
```

## HTTP Endpoints (WolverineFx.HTTP)

### Basic GET Endpoint

```csharp
[WolverineGet("/users/{id}")]
public static Task<User?> GetUser(int id, IQuerySession session)
    => session.LoadAsync<User>(id);
```

### POST with Message Publishing

```csharp
[WolverinePost("/orders")]
public static async Task<IResult> CreateOrder(
    CreateOrderRequest request,
    IDocumentSession session,
    IMessageBus bus)
{
    var order = new Order { Id = Guid.NewGuid(), Items = request.Items };
    session.Store(order);
    
    await bus.PublishAsync(new OrderCreated(order.Id));
    
    return Results.Created($"/orders/{order.Id}", order);
}
```

### Compound Handler (Load/Validate/Handle)

```csharp
public static class UpdateOrderEndpoint
{
    public static async Task<(Order?, IResult)> LoadAsync(
        UpdateOrder command,
        IDocumentSession session)
    {
        var order = await session.LoadAsync<Order>(command.OrderId);
        return order != null
            ? (order, new WolverineContinue())
            : (order, Results.NotFound());
    }

    [WolverinePut("/orders")]
    public static void Handle(UpdateOrder command, Order order, IDocumentSession session)
    {
        order.Items = command.Items;
        session.Store(order);
    }
}
```

## Event Sourcing with Marten

### Aggregate Handler Workflow

```csharp
public class Order
{
    public Guid Id { get; set; }
    public int Version { get; set; }
    public Dictionary<string, Item> Items { get; set; } = new();
    public DateTimeOffset? Shipped { get; private set; }

    public void Apply(ItemReady ready) => Items[ready.Name].Ready = true;
    public void Apply(IEvent<OrderShipped> shipped) => Shipped = shipped.Timestamp;

    public bool IsReadyToShip() => Shipped == null && Items.Values.All(x => x.Ready);
}

public record MarkItemReady(Guid OrderId, string ItemName, int Version);

[AggregateHandler]
public static IEnumerable<object> Handle(MarkItemReady command, Order order)
{
    if (order.Items.TryGetValue(command.ItemName, out var item))
    {
        item.Ready = true;
        yield return new ItemReady(command.ItemName);
    }
    
    if (order.IsReadyToShip())
    {
        yield return new OrderReady();
    }
}
```

### Read Aggregate (Read-Only)

```csharp
[WolverineGet("/orders/{id}")]
public static Order GetOrder([ReadAggregate] Order order) => order;
```

### Write Aggregate with Validation

```csharp
public static IEnumerable<object> Handle(
    MarkItemReady command,
    [WriteAggregate(Required = true, OnMissing = OnMissing.ProblemDetailsWith404)] Order order)
{
    order.Items[command.ItemName].Ready = true;
    yield return new ItemReady(command.ItemName);
}
```

### Returning Updated Aggregate

```csharp
[AggregateHandler]
public static (UpdatedAggregate, Events) Handle(
    MarkItemReady command,
    Order order)
{
    var events = new Events();
    events.Add(new ItemReady(command.ItemName));
    return (new UpdatedAggregate(), events);
}
```

## Transactional Outbox

### Marten Integration

```csharp
builder.Services.AddMarten(opts =>
{
    opts.Connection(connectionString);
}).IntegrateWithWolverine();

builder.Host.UseWolverine(opts =>
{
    opts.Policies.AutoApplyTransactions();
});
```

### Using Outbox in Controllers

```csharp
[HttpPost("/orders")]
public async Task Post(
    [FromBody] CreateOrder command,
    [FromServices] IDocumentSession session,
    [FromServices] IMartenOutbox outbox)
{
    outbox.Enroll(session);
    
    var order = new Order { Id = command.OrderId };
    session.Store(order);
    
    await outbox.PublishAsync(new OrderCreated(command.OrderId));
    
    await session.SaveChangesAsync();
}
```

## Transport Configuration

### RabbitMQ

```csharp
builder.Host.UseWolverine(opts =>
{
    opts.UseRabbitMq("host=localhost")
        .AutoProvision()
        .AutoPurgeOnStartup();
    
    opts.PublishAllMessages()
        .ToRabbitExchange("wolverine.events", exchange =>
        {
            exchange.ExchangeType = ExchangeType.Topic;
        });
});
```

### Azure Service Bus

```csharp
builder.Host.UseWolverine(opts =>
{
    opts.UseAzureServiceBus(asbConnectionString)
        .AutoProvision()
        .ConfigureQueue(q => q.MaxDeliveryCount = 5);
});
```

### Amazon SQS

```csharp
builder.Host.UseWolverine(opts =>
{
    opts.UseAmazonSqs(sqsConfig)
        .AutoProvision();
});
```

## Batch Message Processing

### Configure Batching

```csharp
builder.Host.UseWolverine(opts =>
{
    opts.BatchMessagesOf<SubTaskCompleted>(batching =>
    {
        batching.BatchSize = 500;
        batching.TriggerTime = 1.Seconds();
    });
});
```

### Batch Handler

```csharp
public static class ItemBatchHandler
{
    public static void Handle(Item[] items, IRepository repository)
    {
        foreach (var item in items)
        {
            repository.Process(item);
        }
    }
}
```

### Custom Batching Strategy

```csharp
public record SubTaskCompleted(string TaskId, string SubTaskId);
public record SubTaskBatch(string TaskId, string[] SubTaskIds);

public class SubTaskBatcher : IMessageBatcher
{
    public IEnumerable<Envelope> Group(IReadOnlyList<Envelope> envelopes)
    {
        var groups = envelopes
            .GroupBy(x => x.Message!.As<SubTaskCompleted>().TaskId);
        
        foreach (var group in groups)
        {
            var subTaskIds = group
                .Select(x => x.Message)
                .OfType<SubTaskCompleted>()
                .Select(x => x.SubTaskId)
                .ToArray();
            
            yield return new Envelope(
                new SubTaskBatch(group.Key, subTaskIds),
                group);
        }
    }

    public Type BatchMessageType => typeof(SubTaskBatch);
}
```

## Error Handling

### Retry Policies

```csharp
builder.Host.UseWolverine(opts =>
{
    opts.Policies.OnException<SqlException>()
        .RetryWithCooldown(50.Milliseconds(), 100.Milliseconds(), 250.Milliseconds());
    
    opts.Policies.OnException<TimeoutException>()
        .RetryTimes(3);
    
    opts.Policies.OnException<InvalidOperationException>()
        .Requeue();
    
    opts.Policies.OnAnyException()
        .MoveToErrorQueue();
});
```

### Circuit Breaker

```csharp
opts.ListenToRabbitQueue("incoming")
    .CircuitBreaker(cb =>
    {
        cb.PauseTime = 1.Minutes();
        cb.FailurePercentageThreshold = 50;
        cb.MinimumThreshold = 10;
    });
```

## Scheduled Messages

### Delayed Messages

```csharp
public static IEnumerable<object> Handle(OrderCreated command)
{
    yield return new ProcessPayment(command.OrderId);
    yield return new ShipOrder(command.OrderId)
        .DelayedFor(30.Minutes());
}
```

### Scheduled at Specific Time

```csharp
yield return new GenerateReport()
    .ScheduledAt(DateTime.Today.AddDays(1));
```

### Using OutgoingMessages

```csharp
var messages = new OutgoingMessages();
messages.Delay(new Reminder(orderId), TimeSpan.FromHours(24));
messages.Schedule(new MonthlyReport(), DateTime.Today.AddMonths(1));
```

## Request/Reply Pattern

### Sending with Response Request

```csharp
public async Task<OrderStatus> GetOrderStatus(IMessageBus bus, Guid orderId)
{
    return await bus.InvokeAsync<OrderStatus>(new GetOrder(orderId));
}
```

### Handler with Response

```csharp
public record GetOrder(Guid OrderId);
public record OrderStatus(Guid OrderId, string Status);

public static class GetOrderHandler
{
    public static OrderStatus Handle(GetOrder query, IQuerySession session)
    {
        var order = session.Load<Order>(query.OrderId);
        return new OrderStatus(query.OrderId, order?.Status ?? "NotFound");
    }
}
```

## Middleware

### Custom Middleware

```csharp
public class LoggingMiddleware
{
    public void Before(Envelope envelope, ILogger logger)
    {
        logger.LogInformation("Processing {MessageType}", envelope.MessageType);
    }

    public void After(Envelope envelope, ILogger logger)
    {
        logger.LogInformation("Completed {MessageType}", envelope.MessageType);
    }
}

builder.Host.UseWolverine(opts =>
{
    opts.Handlers.AddMiddleware<LoggingMiddleware>();
});
```

### Transaction Middleware

```csharp
builder.Host.UseWolverine(opts =>
{
    opts.Policies.AutoApplyTransactions();
});
```

## Code Generation

### Pre-Generate Types

```bash
dotnet run -- codegen write
```

Generated code appears in `./Internal/Generated/WolverineHandlers/`

### Configure for AOT/Trimming

```csharp
builder.Host.UseWolverine(opts =>
{
    opts.CodeGeneration.TypeLoadMode = TypeLoadMode.Auto;
});
```

## Multi-Tenancy

### Conjoined Tenancy

```csharp
builder.Host.UseWolverine(opts =>
{
    opts.Policies.ConjoinedTenancy(x =>
    {
        x.TenantIdStyle = TenantIdStyle.PerRequest;
    });
});
```

### Publishing to Specific Tenant

```csharp
await bus.PublishAsync(new OrderCreated(orderId), 
    new DeliveryOptions { TenantId = "tenant-1" });
```

## Marten Side Effects

```csharp
public static IMartenOp Handle(CreateTodo command)
{
    var todo = new Todo { Name = command.Name };
    return MartenOps.Store(todo);
}

public static IMartenOp Handle(DeleteTodo command)
{
    return MartenOps.Delete<Todo>(command.Id);
}
```

## Ancillary Stores (Modular Monolith)

```csharp
public interface IPlayerStore : IDocumentStore;

builder.Host.UseWolverine(opts =>
{
    opts.Services.AddMartenStore<IPlayerStore>(m =>
    {
        m.Connection(connectionString);
        m.DatabaseSchemaName = "players";
    })
    .IntegrateWithWolverine();
});

[MartenStore(typeof(IPlayerStore))]
public static class PlayerMessageHandler
{
    public static IMartenOp Handle(PlayerMessage message)
    {
        return MartenOps.Store(new Player { Id = message.Id });
    }
}
```

## Command Line Tools

### Available Commands

```bash
dotnet run -- help           # List all commands
dotnet run -- describe       # Application description
dotnet run -- resources      # Resource management
dotnet run -- storage        # Message storage admin
dotnet run -- codegen write  # Pre-generate code
```

## Best Practices

1. **Prefer pure functions** - Business logic should be testable without mocks
2. **Use cascading messages** - Return messages instead of injecting IMessageBus
3. **Keep call stacks short** - Avoid deep service hierarchies
4. **Pre-generate code** - Optimize cold starts in production
5. **Use compound handlers** - Separate load/validate/handle logic
6. **Configure error handling** - Let Wolverine handle retries and errors
7. **Use transactional outbox** - Guarantee message delivery
8. **Batch when appropriate** - Improve throughput for high-volume messages

## Anti-Patterns to Avoid

1. **Injecting IMessageBus deep in call stack** - Makes workflow hard to reason about
2. **Over-using constructor injection** - Prefer method injection
3. **Ignoring transactional outbox** - Can lose messages on failure
4. **Not pre-generating code** - Slow cold starts in production
5. **Mixing too many concerns in one handler** - Keep handlers focused
6. **Not configuring error handling** - Messages end up in error queue unexpectedly
