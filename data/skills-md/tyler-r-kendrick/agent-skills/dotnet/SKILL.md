---
name: dotnet
description: |
  Use when working with C#, F#, .NET libraries, ASP.NET Core, Blazor, Entity Framework Core, and the broader .NET ecosystem.
  USE FOR: .NET language features, choosing libraries and frameworks, project structure, package selection, architecture decisions
  DO NOT USE FOR: specific library configuration details (use the sub-skills: web, data, testing, eventing, cloud, etc.)
license: MIT
metadata:
  displayName: ".NET"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
  tags:
    - dotnet
    - csharp
    - fsharp
    - aspnet
    - nuget
compatibility: claude, copilot, cursor
references:
  - title: ".NET Documentation"
    url: "https://learn.microsoft.com/dotnet"
  - title: ".NET Runtime GitHub Repository"
    url: "https://github.com/dotnet/runtime"
  - title: "NuGet Package Gallery"
    url: "https://www.nuget.org"
---

# .NET

## Overview

.NET is Microsoft's open-source, cross-platform framework for building web APIs, cloud services, desktop applications, mobile apps, games, IoT, and AI/ML solutions. The modern .NET platform (6+) unifies what were formerly separate runtimes (.NET Framework, .NET Core, Mono) into a single SDK. C# is the primary language, with F# for functional programming. The ecosystem spans 400,000+ NuGet packages, first-party Azure integration, and tooling through Visual Studio, VS Code, and JetBrains Rider.

## Knowledge Map

```
dotnet/
├── ai/                    # ML.NET, ONNX, Azure AI, Microsoft.Extensions.AI, agents (A2A, MCP)
├── cli/                   # Spectre.Console, CliWrap, command-line cheatsheet
├── cloud/                 # Aspire, Azure Functions, Dapr, Orleans, service discovery
├── configuration/         # Extensions.Configuration, caching, feature flags, OpenFeature
├── data/                  # EF Core, Dapper, Redis, Lucene.NET, FluentStorage
├── dependency-injection/  # Extensions.DI, Generic Host, Spring.NET
├── documentation/         # OpenAPI / Swagger
├── eventing/              # MediatR, MassTransit, NServiceBus, Rebus, Wolverine, Brighter, Akka.NET
├── functional/            # F#, Language.Ext, FParsec, Optional, pidgin
├── general/               # Humanizer, ImageSharp, NodaTime, Stateless, worker services, cheatsheet
├── localization/          # i18n, resource-based localization, MessageFormat
├── logging/               # Serilog, NLog, Extensions.Logging
├── mapping/               # AutoMapper, Mapperly
├── networking/            # gRPC, DotNetty, MimeKit, System.IO.Pipelines, Twilio
├── observability/         # OTLP logging, OpenTelemetry conventions
├── project-system/        # MSBuild/csproj, Roslyn analyzers, source generators, EditorConfig, Fody
├── reactive/              # Rx.NET, System.Threading.Channels, DynamicData, IAsyncEnumerable
├── resilience/            # Polly, Extensions.Resilience
├── security/              # ASP.NET Identity, cryptography, authorization (Topaz, Enforcer)
├── serialization/         # Protobuf-net, Bond, Hyperion, FluentSerializer
├── testing/               # Testcontainers, Moq, AutoFixture, Pact, Reqnroll, Playwright
├── ui/                    # MAUI, Avalonia, Blazor, Uno Platform, Blazorise, MonoGame, Unity
├── validation/            # FluentValidation, Validot, Parse Don't Validate, CommunityToolkit.Guard
└── web/                   # ASP.NET Core, SignalR, YARP, Ocelot, GraphQL, Refit, Orchard CMS
```

## Choosing Guide

| Problem | Sub-Skill | Notes |
|---------|-----------|-------|
| Build a web API or microservice | `web/aspnet-core` | Minimal APIs for simple endpoints, controllers for complex APIs |
| Add real-time push to a web app | `web/signalr` | WebSocket abstraction with automatic fallback to SSE/long-polling |
| Reverse proxy or API gateway | `web/yarp` or `web/ocelot` | YARP for high-perf programmatic proxy, Ocelot for config-driven gateway |
| GraphQL API | `web/graphql` | Hot Chocolate server with filtering, sorting, subscriptions |
| Access a relational database | `data/entity-framework-core` | Full ORM with migrations, change tracking, LINQ queries |
| Lightweight SQL queries | `data/dapper` | Micro-ORM, raw SQL with object mapping, best for read-heavy paths |
| Distributed cache | `data/redis` or `configuration/extensions-caching` | Redis for shared cache, IMemoryCache/IDistributedCache for local/hybrid |
| Event-driven / CQRS architecture | `eventing/mediatr` | In-process mediator; combine with `eventing/masstransit` for cross-service |
| Message bus (RabbitMQ, Kafka, Azure SB) | `eventing/masstransit` | Abstraction over transports with sagas, retries, and outbox pattern |
| Build a .NET Aspire app | `cloud/aspire` | Orchestrate multi-project apps with built-in service discovery and telemetry |
| Serverless functions | `cloud/azure-functions` | Isolated worker model for Azure Functions with DI and middleware |
| Resilience (retries, circuit breakers) | `resilience/polly` | Configurable policies; use `resilience/extensions-resilience` for DI integration |
| Structured logging | `logging/serilog` | Sinks for Console, Seq, Elasticsearch, Application Insights |
| Object mapping | `mapping/mapperly` | Source-generator-based mapper (zero reflection, compile-time safe) |
| Input validation | `validation/fluent-validations` | Fluent rules with DI integration and ASP.NET Core auto-validation |
| Integration testing with real DBs | `testing/testcontainers` | Docker-based throwaway containers for Postgres, SQL Server, Redis |
| Mocking in unit tests | `testing/moq` | Proxy-based mocking with LINQ setup expressions |
| Contract testing | `testing/pact` | Consumer-driven contract tests for microservice boundaries |
| BDD / Gherkin | `testing/reqnroll` | SpecFlow successor — Given/When/Then with .NET 8+ support |
| Cross-platform desktop app | `ui/avalonia` | XAML-based UI for Windows, macOS, Linux, iOS, Android, WebAssembly |
| Mobile + desktop from one codebase | `ui/maui` | Microsoft's official cross-platform UI framework (.NET 8+) |
| Interactive web UI in C# | `ui/blazor` | Server-side or WebAssembly rendering with Razor components |
| Functional programming in C# | `functional/language-ext` | Immutable collections, Option/Either monads, pattern matching extensions |
| F# language guidance | `functional/fsharp` | Type providers, computation expressions, pipelines, domain modeling |
| AI/ML inference | `ai/microsoft-extensions-ai` | Unified abstraction for OpenAI, Azure AI, Ollama, and custom providers |
| Train ML models in .NET | `ai/mlnet` | AutoML, classification, regression, anomaly detection, recommendation |
| Build a CLI tool | `cli/spectre-console` | Rich terminal UI with tables, trees, progress bars, prompts |
| Source generators | `project-system/generators-cheatsheet` | Compile-time code generation with Roslyn incremental generators |
| Roslyn code analysis | `project-system/roslyn-analyzers` | Custom analyzers and code fixes for enforcing team conventions |

## .NET Version Landscape

| Version | Release | Support | Key Features |
|---------|---------|---------|-------------|
| **.NET 6** | Nov 2021 | LTS (ended Nov 2024) | Minimal APIs, hot reload, `DateOnly`/`TimeOnly`, HTTP/3, AOT groundwork |
| **.NET 7** | Nov 2022 | STS (ended May 2024) | Native AOT for console apps, rate limiting middleware, output caching |
| **.NET 8** | Nov 2023 | LTS (until Nov 2026) | .NET Aspire, `FrozenDictionary`, keyed DI, native AOT for web, `TimeProvider` |
| **.NET 9** | Nov 2024 | STS (until May 2026) | `System.Threading.Lock`, LINQ `CountBy`/`AggregateBy`, `TypedResults` improvements |

### Choosing a Version

- **Starting a new project?** Use .NET 8 (LTS) for stability, or .NET 9 for latest features.
- **In production with .NET 6?** Plan migration to .NET 8 — .NET 6 support has ended.
- **Need native AOT?** .NET 8+ supports AOT for ASP.NET Core minimal APIs and gRPC.
- **Using Aspire for orchestration?** Requires .NET 8+.

## C# Quick Reference

### Modern C# Features (10-13)

```csharp
// Global usings (C# 10) — reduce boilerplate across files
global using System.Text.Json;
global using Microsoft.Extensions.Logging;

// File-scoped namespaces (C# 10)
namespace MyApp.Services;

// Records with positional syntax — immutable data types
public record OrderPlaced(Guid OrderId, string CustomerId, decimal Total, DateTime PlacedAt);

// Primary constructors (C# 12) — DI without field ceremony
public class OrderService(IOrderRepository repo, ILogger<OrderService> logger)
{
    public async Task<Order> GetAsync(Guid id)
    {
        logger.LogInformation("Fetching order {OrderId}", id);
        return await repo.FindAsync(id) ?? throw new NotFoundException(id);
    }
}

// Collection expressions (C# 12)
int[] numbers = [1, 2, 3, 4, 5];
List<string> names = ["Alice", "Bob", "Charlie"];
ReadOnlySpan<byte> header = [0x48, 0x54, 0x54, 0x50];

// Pattern matching with list patterns (C# 11)
string Describe(int[] values) => values switch
{
    [] => "empty",
    [var single] => $"one item: {single}",
    [var first, .., var last] => $"from {first} to {last}",
};

// Raw string literals (C# 11) — no escaping needed
var json = """
    {
        "name": "Widget",
        "price": 29.99,
        "tags": ["electronics", "sale"]
    }
    """;

// Required members (C# 11)
public class Config
{
    public required string ConnectionString { get; init; }
    public required int MaxRetries { get; init; }
    public TimeSpan Timeout { get; init; } = TimeSpan.FromSeconds(30);
}

// Switch expressions with property patterns
decimal CalculateDiscount(Order order) => order switch
{
    { Total: > 1000, Customer.IsPremium: true } => order.Total * 0.15m,
    { Total: > 500 } => order.Total * 0.10m,
    { Customer.IsPremium: true } => order.Total * 0.05m,
    _ => 0m,
};
```

### Key NuGet Package Categories

| Category | Go-To Packages | When to Use |
|----------|---------------|-------------|
| **Web Framework** | ASP.NET Core (built-in) | REST APIs, Razor Pages, Blazor, gRPC |
| **ORM** | EF Core, Dapper | EF Core for full ORM, Dapper for raw SQL performance |
| **Validation** | FluentValidation, Validot | Fluent rule definitions, DI-friendly, auto-wire with ASP.NET |
| **Mapping** | Mapperly, AutoMapper | Mapperly for source-gen (zero reflection), AutoMapper for convention-based |
| **Serialization** | System.Text.Json, Protobuf-net | STJ for JSON (built-in), Protobuf for binary/gRPC |
| **Logging** | Serilog, NLog | Structured logging with sinks for Seq, Elastic, AppInsights |
| **Testing** | xUnit, Moq, AutoFixture, Testcontainers | xUnit as test framework, Moq for mocks, Testcontainers for integration |
| **Resilience** | Polly, Extensions.Resilience | Retry, circuit breaker, timeout, rate limiter policies |
| **Messaging** | MassTransit, MediatR, NServiceBus | MassTransit for bus abstraction, MediatR for in-process CQRS |
| **DI** | Extensions.DI (built-in) | Constructor injection, scoped/transient/singleton lifetimes |
| **Caching** | Extensions.Caching, StackExchange.Redis | IMemoryCache for local, IDistributedCache for Redis/SQL |
| **HTTP Client** | Refit, RestSharp | Refit for interface-defined clients, RestSharp for simpler REST calls |
| **CLI** | Spectre.Console, System.CommandLine | Rich terminal UIs, argument parsing, help generation |
| **Cloud** | .NET Aspire, Azure.Identity | Aspire for orchestration, Azure.Identity for managed identity auth |

## Best Practices

1. **Use the latest LTS release** (.NET 8) for production workloads. LTS releases receive 3 years of security patches and bug fixes.

2. **Enable nullable reference types** (`<Nullable>enable</Nullable>`) in every project. This catches null-reference bugs at compile time:
   ```xml
   <PropertyGroup>
     <TargetFramework>net8.0</TargetFramework>
     <Nullable>enable</Nullable>
     <ImplicitUsings>enable</ImplicitUsings>
   </PropertyGroup>
   ```

3. **Use `IOptions<T>` pattern** for configuration instead of reading values directly. This provides validation, reload support, and testability:
   ```csharp
   public class SmtpOptions
   {
       public const string Section = "Smtp";
       public required string Host { get; init; }
       public int Port { get; init; } = 587;
       public required string FromAddress { get; init; }
   }

   // In Program.cs
   builder.Services.AddOptions<SmtpOptions>()
       .BindConfiguration(SmtpOptions.Section)
       .ValidateDataAnnotations()
       .ValidateOnStart();
   ```

4. **Prefer records for data transfer objects and events**. Records provide value equality, immutability, and concise syntax. Use `record class` for heap-allocated (default) and `record struct` for stack-allocated small types.

5. **Use primary constructors for DI** in services and controllers (C# 12). This eliminates boilerplate `private readonly` fields while keeping constructor injection.

6. **Avoid `async void`** — it swallows exceptions. Always return `Task` or `ValueTask` from async methods. The only exception is event handlers.

7. **Use `CancellationToken` everywhere** — pass it through all async call chains so requests can be cancelled cleanly when clients disconnect:
   ```csharp
   app.MapGet("/orders/{id}", async (Guid id, IOrderRepository repo, CancellationToken ct) =>
       await repo.FindAsync(id, ct) is { } order
           ? Results.Ok(order)
           : Results.NotFound());
   ```

8. **Register services with the correct lifetime** — `Singleton` for stateless/thread-safe services, `Scoped` for per-request state (EF DbContext), `Transient` for lightweight stateless operations. Never inject Scoped into Singleton.

9. **Use source generators over reflection** where available (Mapperly, System.Text.Json source gen, Roslyn analyzers). Source generators run at compile time, eliminate reflection costs, and are compatible with Native AOT.

10. **Structure solutions with clear project boundaries** — separate API host, domain logic, infrastructure, and tests into distinct projects. Use `<ProjectReference>` and enforce dependency direction (domain has no external references).
