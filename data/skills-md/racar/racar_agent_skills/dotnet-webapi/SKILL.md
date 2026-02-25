---
name: dotnet-webapi
description: Build ASP.NET Core Web APIs with .NET 10 (C# 14.0). Supports project scaffolding, CRUD operations, Entity Framework integration, dependency injection, testing with xUnit, Docker containerization, and following 2025 best practices. Use when creating REST APIs, microservices, backend services, implementing CRUD operations, setting up Entity Framework, adding authentication/authorization, or containerizing .NET applications. Triggers on .NET, ASP.NET Core, C#, Web API, REST API, microservices, dotnet, csharp development tasks.
---

# .NET 10 Web API Development

Build production-ready ASP.NET Core Web APIs with .NET 10 using best practices from 2025.

## Quick Start

Create a new Web API project:

```bash
scripts/new_api.sh <project_name> [output_directory]
```

**Example:**
```bash
scripts/new_api.sh ProductsApi
cd ProductsApi
dotnet build
dotnet run --project ProductsApi.Api
```

This creates:
- Solution with API and Test projects
- Controller-based Web API (.NET 10)
- xUnit test project with integration testing setup
- Proper folder structure (Controllers, Models, Services)
- .gitignore configured for .NET

---

## Core Features

### 1. Project Scaffolding

**Create New API Project:**
```bash
scripts/new_api.sh MyApi ./projects
```

Generates:
- `MyApi.Api` - Main API project with controllers
- `MyApi.Tests` - xUnit test project with integration testing
- Solution file linking both projects
- Standard folder structure
- Test dependencies (FluentAssertions, WebApplicationFactory)

### 2. Add CRUD Entities

**Generate Entity with Controller and Service:**
```bash
scripts/add_entity.sh <entity_name> <project_path>
```

**Example:**
```bash
scripts/add_entity.sh Product ./MyApi
scripts/add_entity.sh Customer ./MyApi
```

Generates for each entity:
- Model class (`Models/Product.cs`)
- Service interface (`Services/IProductService.cs`)
- Service implementation (`Services/ProductService.cs`)
- CRUD controller (`Controllers/ProductController.cs`)
- Automatic service registration in DI container

**API Endpoints Created:**
```
GET    /api/Product        - Get all
GET    /api/Product/{id}   - Get by ID
POST   /api/Product        - Create
PUT    /api/Product/{id}   - Update
DELETE /api/Product/{id}   - Delete
```

### 3. Package Management

**Add NuGet Packages:**
```bash
scripts/add_package.sh <project_path> <package_name|preset>
```

**Presets:**
```bash
# Entity Framework with PostgreSQL
scripts/add_package.sh ./MyApi ef-postgres

# Entity Framework with SQL Server
scripts/add_package.sh ./MyApi ef-sqlserver

# JWT Authentication
scripts/add_package.sh ./MyApi auth

# FluentValidation
scripts/add_package.sh ./MyApi validation

# Individual package
scripts/add_package.sh ./MyApi Newtonsoft.Json
```

### 4. Docker Support

**Generate Dockerfile and docker-compose:**
```bash
scripts/generate_dockerfile.sh <project_path>
```

**Example:**
```bash
scripts/generate_dockerfile.sh ./MyApi
```

Generates:
- Multi-stage optimized Dockerfile
- docker-compose.yml with PostgreSQL
- .dockerignore
- Non-root user configuration
- Health check setup

**Build and run:**
```bash
docker-compose up -d
docker-compose logs -f api
```

---

## .NET 10 Features

### Built-in Features

**OpenAPI 3.1 Support:**
```csharp
// Program.cs
builder.Services.AddOpenApi();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi(); // /openapi/v1.json
}
```

**Automatic Minimal API Validation:**
DataAnnotations are automatically validated in .NET 10 for Minimal APIs and controllers.

**Output Caching:**
```csharp
builder.Services.AddOutputCache();
app.UseOutputCache();

[OutputCache(Duration = 300)]
[HttpGet]
public async Task<IActionResult> GetAll()
```

**Rate Limiting:**
```csharp
builder.Services.AddRateLimiter(options =>
{
    options.AddFixedWindowLimiter("api", config =>
    {
        config.PermitLimit = 100;
        config.Window = TimeSpan.FromMinutes(1);
    });
});
```

### C# 14.0 Features

Use latest C# features:
- Primary constructors
- Collection expressions
- Required members
- Init-only properties

---

## Development Workflows

### Typical Development Flow

1. **Create project:**
   ```bash
   scripts/new_api.sh OrderService
   cd OrderService
   ```

2. **Add entities:**
   ```bash
   scripts/add_entity.sh Order .
   scripts/add_entity.sh OrderItem .
   ```

3. **Add database:**
   ```bash
   scripts/add_package.sh . ef-postgres
   ```

4. **Build and run:**
   ```bash
   dotnet build
   dotnet run --project OrderService.Api
   ```

5. **Test:**
   ```bash
   dotnet test
   ```

6. **Dockerize:**
   ```bash
   scripts/generate_dockerfile.sh .
   docker-compose up
   ```

### Entity Framework Integration

After adding EF packages, configure DbContext:

```csharp
// Data/ApplicationDbContext.cs
public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options) { }

    public DbSet<Product> Products => Set<Product>();
}

// Program.cs
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));

// appsettings.json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Database=mydb;Username=postgres;Password=postgres"
  }
}
```

**Run migrations:**
```bash
dotnet ef migrations add Initial --project MyApi.Api
dotnet ef database update --project MyApi.Api
```

### Authentication Setup

After adding auth package:

```csharp
// Program.cs
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["Jwt:Issuer"],
            ValidAudience = builder.Configuration["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"]))
        };
    });

app.UseAuthentication();
app.UseAuthorization();

// Protect endpoints
[Authorize]
[HttpGet("admin")]
public IActionResult AdminOnly() => Ok("Admin data");
```

---

## Best Practices

### Controller Pattern

Generated controllers follow best practices:

```csharp
[ApiController]
[Route("api/[controller]")]
public class ProductController : ControllerBase
{
    private readonly IProductService _service;
    private readonly ILogger<ProductController> _logger;

    // Constructor injection
    public ProductController(
        IProductService service,
        ILogger<ProductController> logger)
    {
        _service = service;
        _logger = logger;
    }

    // Documented endpoints
    /// <summary>
    /// Get all products
    /// </summary>
    [HttpGet]
    [ProducesResponseType(StatusCodes.Status200OK)]
    public async Task<ActionResult<IEnumerable<Product>>> GetAll()

    // Proper status codes
    [HttpPost]
    [ProducesResponseType(StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<Product>> Create(Product entity)
    {
        var created = await _service.CreateAsync(entity);
        return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
    }
}
```

### Service Layer Pattern

```csharp
// Interface
public interface IProductService
{
    Task<IEnumerable<Product>> GetAllAsync();
    Task<Product?> GetByIdAsync(int id);
    Task<Product> CreateAsync(Product entity);
    Task<Product?> UpdateAsync(int id, Product entity);
    Task<bool> DeleteAsync(int id);
}

// Implementation with business logic
public class ProductService : IProductService
{
    // In-memory for demo, replace with repository/DbContext
    private readonly List<Product> _entities = new();

    public async Task<Product> CreateAsync(Product entity)
    {
        entity.Id = _nextId++;
        entity.CreatedAt = DateTime.UtcNow;
        _entities.Add(entity);
        return entity;
    }
}
```

---

## Testing

Generated test projects include integration testing setup:

```csharp
public class ProductsEndpointTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public ProductsEndpointTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task GetAll_ReturnsSuccessStatusCode()
    {
        var response = await _client.GetAsync("/api/products");
        response.EnsureSuccessStatusCode();
    }
}
```

**Run tests:**
```bash
dotnet test
dotnet test --logger "console;verbosity=detailed"
```

---

## References

For detailed guidance, see:

### API Best Practices
`references/api_best_practices.md` - Comprehensive guide covering:
- RESTful API design
- HTTP status codes
- Error handling patterns
- Validation strategies
- Authentication & authorization
- Dependency injection
- Logging best practices
- Performance optimization
- OpenAPI documentation

### Testing Patterns
`references/testing_patterns.md` - Testing guide including:
- xUnit fundamentals
- Unit testing with Moq
- Integration testing with WebApplicationFactory
- Test data builders
- FluentAssertions usage
- Common testing patterns

### Common Packages
`references/common_packages.md` - NuGet package guide for:
- Database providers (EF Core, Dapper)
- Authentication (JWT, Identity)
- Validation (FluentValidation)
- Testing tools (xUnit, Moq, FluentAssertions)
- Logging (Serilog)
- Utilities (AutoMapper, MediatR, Polly)

---

## Common Scenarios

### Scenario 1: New CRUD API

```bash
# Create project
scripts/new_api.sh InventoryApi

# Add entities
scripts/add_entity.sh Product ./InventoryApi
scripts/add_entity.sh Category ./InventoryApi

# Add database
scripts/add_package.sh ./InventoryApi ef-postgres

# Run
cd InventoryApi
dotnet run --project InventoryApi.Api
```

### Scenario 2: Microservice with Docker

```bash
# Create and setup
scripts/new_api.sh OrderService
scripts/add_entity.sh Order ./OrderService
scripts/add_package.sh ./OrderService ef-postgres
scripts/generate_dockerfile.sh ./OrderService

# Deploy
cd OrderService
docker-compose up -d
```

### Scenario 3: Authenticated API

```bash
scripts/new_api.sh SecureApi
scripts/add_entity.sh User ./SecureApi
scripts/add_package.sh ./SecureApi auth
scripts/add_package.sh ./SecureApi validation
```

---

## Troubleshooting

### .NET SDK Not Found

Ensure .NET 10 SDK is installed:
```bash
dotnet --version  # Should be 10.x
```

Install from: https://dotnet.microsoft.com/download/dotnet/10.0

### Port Already in Use

Change port in Properties/launchSettings.json or use environment variable:
```bash
ASPNETCORE_HTTP_PORTS=5001 dotnet run --project MyApi.Api
```

### Docker Build Fails

Ensure Docker daemon is running:
```bash
docker ps
```

Check Dockerfile paths match project structure.

### EF Migrations Fail

Ensure connection string is correct and database is accessible:
```bash
dotnet ef database update --verbose --project MyApi.Api
```

---

## Integration with Other Skills

Works well with:
- `postgres-query` - Query databases created by your API
- `postgres-backup-restore` - Restore test data for development
- `ruby-rails` - Interop with Rails backends

---

## Summary

This skill provides:

✅ Rapid project scaffolding
✅ CRUD entity generation
✅ NuGet package management
✅ Docker containerization
✅ .NET 10 best practices
✅ Testing setup included
✅ Production-ready code structure
✅ Comprehensive documentation

Start building modern Web APIs with .NET 10 today!
