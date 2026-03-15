---
name: real-world-aspnetcore
description: Research how production ASP.NET Core apps solve architectural problems using the Real World ASP.NET Core repository. Use when the user wants to know how other apps handle something, find patterns, or compare approaches. Triggers on "aspnetcore patterns", "how do other apps", "real world aspnetcore", "research how apps do", ".NET patterns".
---

# ASP.NET Core Pattern Research

## What This Is

The **Real World ASP.NET Core** repository is a collection of 28 curated, production
ASP.NET Core application source code. The `apps/` directory contains the full source
of each app — controllers, services, models, migrations, middleware, configuration,
and NuGet dependencies.

## Locating the Repository

Look for a directory called `real-world-aspnetcore` with an `apps/` subdirectory.
Check the current working directory first, then `~/src/real-world-aspnetcore`. If
not found, ask the user where it lives.

## What To Do

The user gives you a topic. Spin up parallel agents to search the apps for
how real codebases implement that pattern. Read actual code — controllers,
services, models, EF Core configurations, middleware, Program.cs setup,
dependency injection registrations, query patterns — not just file names.
Synthesize what you find into a clear analysis.

## Key Files to Search

- `*.csproj` — NuGet package references (like Gemfile)
- `Program.cs` / `Startup.cs` — DI configuration and middleware pipeline
- `Controllers/` — API and MVC controllers
- `Services/` or `Application/` — Business logic layer
- `Models/`, `Entities/`, `Domain/` — Domain models
- `Data/`, `Infrastructure/` — Data access, EF Core DbContext
- `Migrations/` — EF Core migrations
- `Middleware/` — Custom middleware
- `Hubs/` — SignalR hubs
- `appsettings.json` — Configuration

## Version Note

Apps span .NET 6 through .NET 10. Older apps use `Startup.cs` with
`ConfigureServices()` and `Configure()`. Modern apps use `Program.cs`
with minimal hosting. Note which pattern each app uses when comparing.

If the user's wording suggests they want help choosing a pattern for their
current project (words like "compare for us", "which fits best",
"adversarial", "debate", "evaluate for our project"), also spin up adversarial
agents that each argue for a different pattern in the context of the current
project's architecture and goals.
