---
name: create-controller
description: Create an API controller for a given entity in an ASP.NET Core Web API project. Use when the user wants to scaffold a new controller, create REST API endpoints, or set up CRUD operations with Entity Framework Core and OpenAPI annotations.
---

# Create API Controller

Create a controller for a given entity in an ASP.NET Core Web API project.

## Pre-requisites

- Use Controller-based APIs
- Use System.Text.Json for all JSON data
- The project uses Entity Framework Core 9 — do not install additional packages, the project is already set up.

## Steps

1. Create an empty controller with the naming rule: `{EntityName}Controller`

2. Set up DI and inject Entity Framework context and `ILogger<T>`.

3. Do not use Entity Class for model binding. Create DTO classes for each CRUD operation instead.

4. Add CRUD REST API methods with required OpenAPI-related annotations.

5. Add `OperationId` to each action method. Example:

   ```cs
   // Before
   [HttpGet]

   // After
   [HttpGet(Name = "GetCourses")]
   ```

   Give each `OperationId` a meaningful name.

6. Apply `[ProducesResponseType]` attribute to each action reflecting API behavior.

7. Edit `coursemanagement.http` for testing:
   - Do not touch the existing `@HostAddress` variable definition.
   - Use the `HostAddress` variable.
   - Reference related Entity Class for test payloads.
   - When writing POST method, don't add Primary Key from the entity.

8. Run `dotnet build` to verify everything compiles.

9. Add `Swashbuckle.AspNetCore.SwaggerUI` package:
   ```sh
   dotnet add package Swashbuckle.AspNetCore.SwaggerUI
   ```

10. Add the following code to `Program.cs`:
    ```cs
    app.UseSwaggerUI(options =>
    {
        options.SwaggerEndpoint("/openapi/v1.json", "OpenAPI V1");
    });
    ```

11. Run `dotnet run` to verify the application starts successfully.
