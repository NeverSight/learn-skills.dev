---

name: dotnet-backend-clean-architecture
description: Clean Architecture + CQRS (MediatR) for .NET backend APIs. Builds and maintains APIs with vertical slice (Features), Commands/Queries, handlers, validators, repositories. Use when creating or refactoring .NET APIs, adding endpoints, commands, queries, entities, or when the user mentions Clean Architecture, CQRS, or MediatR.
---

# Backend .NET – Clean Architecture + CQRS

Guia para criar e manter backends .NET com Clean Architecture, CQRS (MediatR) e organização por **Features** (vertical slice).

## Quando usar esta skill

- Adicionar nova **feature** (nova entidade + CRUD ou operações).
- Adicionar **Command** ou **Query** em uma feature existente.
- Criar **Controller**, **Handler**, **Validator**, **Repository** ou **UnitOfWork**.
- Revisar ou refatorar código para seguir a estrutura do boilerplate.

## Estrutura da solução

```
backend/
├── Boilerplate.Interface/          # API (Controllers, Program, Middlewares)
├── Boilerplate.Application/        # Features/ → Commands e Queries (handlers, validators)
├── Boilerplate.Domain/             # Entities, Interfaces (repositórios, serviços, UnitOfWork)
├── Boilerplate.Infrastructure/      # EF Core, Repositories, UnitOfWork, Persistence/Map
├── Boilerplate.CrossCutting/        # DTOs, Options, Helpers
├── Boilerplate.CrossCutting.IOC/    # ConfigureBindings* (DI)
├── Boilerplate.Migration/           # Migrations
└── Boilerplate.Tests/               # Features/ espelhando Application
```

Regra de dependência: **Interface** → Application, Domain, CrossCutting, CrossCutting.IOC. **Application** e **Infrastructure** referenciam **Domain**. **Application** não referencia Infrastructure.

## Checklist – Nova feature (ex.: Orders)

Use este checklist e crie os itens na ordem indicada.

**Domain**

- [ ] `Entities/Order.cs` implementando `IEntity<TKey>` (ex.: `long`).
- [ ] `Interfaces/Repositories/IOrderRepository.cs` herdando `ICrudRepository<Order, long>`.
- [ ] `Interfaces/UnitOfWork/IOrderUnitOfWork.cs` com `IOrderRepository OrderRepository { get; }` e `Task<int> SaveChangesAsync(CancellationToken)`.

**CrossCutting**

- [ ] `Dto/Orders/OrderDto.cs` (e outros DTOs da API se precisar).

**Infrastructure**

- [ ] `Persistence/Map/OrderEntityConfig.cs` (Fluent API do EF).
- [ ] Registrar entidade no `AppDbContext` (DbSet e `OnModelCreating`).
- [ ] `Repositories/OrderRepository.cs` herdando `RepositoryBase<Order, long>`.
- [ ] `UnitOfWork/OrderUnitOfWork.cs` implementando `IOrderUnitOfWork`.
- [ ] Em **CrossCutting.IOC**: `ConfigureBindingsRepository` e `ConfigureBindingsUnitOfWork` registrando `IOrderRepository` e `IOrderUnitOfWork`.

**Application – Commands (ex.: CreateOrder)**

- [ ] Pasta `Features/Orders/Commands/CreateOrder/`.
- [ ] `CreateOrderCommand.cs`: `record` com parâmetros e `: IRequest<OrderDto>`.
- [ ] `CreateOrderHandler.cs`: `IRequestHandler<CreateOrderCommand, OrderDto>`, injetar `IOrderUnitOfWork` (e serviços/validators se precisar); chamar `ValidateAndThrowAsync` se houver validator; usar repositório via UoW; retornar DTO.
- [ ] `CreateOrderValidator.cs`: `AbstractValidator<CreateOrderCommand>` (quando houver validação de entrada).

**Application – Queries (ex.: ListOrders)**

- [ ] Pasta `Features/Orders/Queries/ListOrders/`.
- [ ] `ListOrdersQuery.cs`: `record ListOrdersQuery() : IRequest<IReadOnlyList<OrderDto>>`.
- [ ] `ListOrdersHandler.cs`: `IRequestHandler<ListOrdersQuery, IReadOnlyList<OrderDto>>`, injetar `IOrderUnitOfWork`, usar repositório, mapear entidades para DTOs.

**Interface**

- [ ] `Controllers/OrdersController.cs`: `[ApiController]`, `[Route("api/orders")]`, injetar `IMediator`; ações chamam `_mediator.Send(Command ou Query, cancellationToken)`; retornos HTTP adequados (Ok, CreatedAtAction, NotFound, NoContent).

**Tests**

- [ ] Em `Boilerplate.Tests/Features/Orders/`: testes para handlers (Commands e Queries) com NSubstitute para UoW/Repository/Services/Validator e FluentAssertions para asserts.

**Migration**

- [ ] Nova migration em `Boilerplate.Migration` após alterar entidades/map.

## Padrões de código

**Command (record)**

```csharp
public sealed record CreateProductCommand(
    string? Name,
    string? Description,
    decimal? Price,
    bool IsActive = true) : IRequest<ProductDto>;
```

**Query (record)**

```csharp
public sealed record ListProductsQuery() : IRequest<IReadOnlyList<ProductDto>>;
```

**Handler**

- Injetar `I{X}UnitOfWork` (e `IValidator<TCommand>` quando houver validator).
- No handler de Command: `await _validator.ValidateAndThrowAsync(request, cancellationToken);` no início.
- Usar apenas repositórios e serviços via interfaces do Domain; retornar DTO (CrossCutting).

**Validator**

- `AbstractValidator<CreateProductCommand>`; regras com `RuleFor` e `.When()` quando condicional.

**Controller**

- Um controller por agregação/recurso (ex.: ProductsController).
- Métodos assíncronos com `CancellationToken`; apenas `Mediator.Send` e retorno HTTP (sem lógica de negócio).

**Entity**

- `public sealed class Product : IEntity<long>` com `Id` e propriedades necessárias.

**Repository (Domain)**

- `public interface IProductRepository : ICrudRepository<Product, long> { }`.

**UnitOfWork (Domain)**

- `IProductUnitOfWork` com `IProductRepository ProductRepository { get; }` e `SaveChangesAsync`.

## Tratamento de erros

- Validação de entrada: FluentValidation; falha lança `ValidationException`.
- Regras de negócio que falham: `InvalidOperationException` (ou exceção de domínio apropriada).
- **Interface** deve ter um middleware global que capture essas exceções e responda com ProblemDetails (ex.: 400 para validação e operação inválida, 500 para exceções não tratadas). Não deixar lógica de negócio no middleware.

## Convenções

- Namespaces: `Boilerplate.Application.Features.{Feature}.Commands.{CommandName}` e `...Queries.{QueryName}`.
- Um **comando/query por pasta** dentro de Commands/ ou Queries/.
- DTOs da API em **CrossCutting.Dto**; entidades apenas no Domain.
- Novos bindings de DI em **CrossCutting.IOC** (novo ou existente `ConfigureBindings*.cs`), chamados em `ConfigureBindingsDependencyInjection.RegisterBindings`.

## Recursos adicionais

- Estrutura detalhada, fluxo de requisição e tabela “Quando usar” por projeto: [reference.md](reference.md).
