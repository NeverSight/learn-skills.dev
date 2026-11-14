---
name: neo-dotnet-minimal-apis
description: >
  Use this skill when building, debugging, refactoring, or reviewing ASP.NET Core
  Minimal APIs, lightweight endpoints, route groups, endpoint filters, typed results,
  OpenAPI metadata, or high-performance .NET API services without controllers.
compatibility: "Supports .NET 6.0 through 11.0 environments. Requires .NET SDK installed locally."
metadata:
  version: "1.1.0"
  category: "Framework"
---

# .NET Minimal APIs Expert Skill

## Trigger On
- The user requests to create, debug, refactor, or review .NET Minimal APIs.
- The project's `Program.cs` contains `WebApplication.CreateBuilder(args)` and is not configured with a Controllers directory.
- The target framework is .NET 6.0 (LTS) and above.
- There is a need to optimize API performance or simplify Web API architecture.

## Workflow
1. **Perceive (Architecture Awareness):**
   - Check `.csproj` to identify `TargetFramework`.
   - Analyze `Program.cs` to distinguish whether it uses simple endpoints or adopts a Module-based or Vertical Slice organization.
   - Identify whether OpenAPI (Swagger) support has been configured.
2. **Reason (Planning Phase):**
   - Evaluate whether "Route Groups" need to be introduced to optimize organizational structure.
   - Determine whether to use "Endpoint Filters" to handle cross-cutting concerns (such as parameter validation).
   - Choose the most appropriate syntax based on the .NET version (e.g., `TypedResults` in .NET 7+).
3. **Act (Execution Phase):**
   - Write clean, high-performance Minimal API code, prioritizing Lambdas or extension methods.
   - Implement strong typing and DTOs (prioritize using `record`).
   - Integrate dependency injection, avoiding the Service Locator pattern.
4. **Validate (Standard Validation):**
   - Validate whether the endpoints correctly return expected HTTP status codes.
   - Check whether the generated OpenAPI documentation is complete.
   - Ensure asynchronous operations correctly pass the `CancellationToken`.

## Feature Roadmap (.NET 6 - 11)

### .NET 6 & 7 (Foundation)
- **Minimal Hosting**: Simplified startup process and top-level statements.
- **Route Groups**: Use `MapGroup` to consolidate prefixes and authentication.
- **Endpoint Filters**: Implement interception logic within Minimal APIs.
- **Typed Results**: Improved unit testing and Swagger support.

### .NET 8 & 9 (Productivity)
- **Antiforgery**: Built-in anti-forgery token support.
- **Form Binding**: Support for `[FromForm]` parameter binding.
- **HybridCache**: High-performance multi-level caching support.
- **OpenAPI Improvements**: Better OpenAPI code generation.

### .NET 10 (AOT & Middleware)
- **Native AOT Optimization**: AOT-optimized compilation tailored for Minimal APIs.
- **Enhanced Middleware Patterns**: New middleware designed for lightweight architectures.

### .NET 11+ (Version-Specific Features)
- **Asynchronous Validation Support**: Native async validation rules across Minimal API endpoints and parameter binding, awaiting validation logic seamlessly.
- **OpenAPI 3.2 by Default**: Updated default specification to OpenAPI 3.2, with support for `OpenApiGenerationEnvironment` in build-time generation.
- **Zstandard (zstd) Compression**: Native high-ratio, low-latency compression provider for response compression and request decompression.
- **Runtime Async Performance**: Reduced task state machine allocations and cleaner async stack traces across endpoint handlers.

## Coding Standards
- **Clean Routing**: Prioritize using extension methods to modularize routes.
- **Strong Typing**: Prioritize using `TypedResults` and `Results<T1, T2>`.
- **Async Safety**: Always accept and pass down `CancellationToken`.
- **DI Best Practices**: Services should be defined directly in the Handler parameters.

## Deliver
- **Version-Optimized API Code**: Provide the most appropriate modern API code based on the target .NET version.
- **Modular Architecture**: Provide structural suggestions for extracting `Program.cs` routes into extension methods.
- **OpenAPI Configuration**: Provide comprehensive Swagger/OpenAPI configuration suggestions.

## Validate
- Ensure the provided code executes correctly in a .NET 6+ environment.
- Validate endpoint security (authentication, authorization, Antiforgery).
- Check if the code complies with high-performance best practices for Minimal APIs (e.g., avoiding closures, reducing allocations).

## Documentation
### Official References
- [What's new in ASP.NET Core in .NET 11](https://learn.microsoft.com/en-us/aspnet/core/release-notes/aspnetcore-11.0)
- [Minimal APIs Overview](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis)
- [Route groups and filters](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/route-handlers)
- [Typed responses in Minimal APIs](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/responses)

### Internal References
- [Minimal APIs Coding Style and Naming Conventions](reference/coding-style.md)
- [Minimal APIs Anti-Patterns and Best Practices](reference/anti-patterns.md)
- [Minimal APIs Modern Patterns Guide](reference/patterns.md)
