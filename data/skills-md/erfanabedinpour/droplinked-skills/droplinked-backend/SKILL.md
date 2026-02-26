---
name: droplinked-backend
description: |
  Code style, architecture patterns, and development guide for the Droplinked e-commerce backend.
  NestJS + Prisma (MongoDB) with strict layered architecture: Controller to Service Facade to UseCase to Repository.

  Use this skill when:
  (1) Creating new features, modules, or endpoints in the Droplinked backend
  (2) Refactoring existing code to follow project patterns
  (3) Writing tests for use cases and services
  (4) Reviewing code for architectural compliance
  (5) Understanding the data model (shops, products, orders, carts, merchants, customers)
  (6) Implementing cross-module communication
  (7) Adding event-driven side effects
  (8) Working with Prisma and MongoDB in this codebase

  Triggers: droplinked, nest module, usecase, service facade, repository pattern, cart, order, shop, product, merchant
---

# Droplinked Backend Development Guide

## Architecture Overview

Strict layered architecture with clear separation of concerns:

```
Controller -> Service Facade -> UseCase -> Repository
```

| Layer | Role | Rules |
|-------|------|-------|
| **Controller** | HTTP only | Transform params, call service. No logic. Use `@CurrentUser()`, `IsObjectIdPipe` |
| **Service Facade** | Thin orchestration | Get UseCase via `ModuleRef`, call `execute()`. No business logic |
| **UseCase** | All business logic | Extend `UseCase<T,R>`, implement `validate()` + `doExecute()` |
| **Repository** | Data access only | Extend `Repository<T>`, use Prisma. Semantic methods like `findCartForCheckout()` |

## Module Structure

All file names in `kebab-case`:

```
src/modules/<module-name>/
├── controllers/          # HTTP Controllers
│   └── <module>.controller.ts
├── services/             # Service Facades
│   └── <module>.service.ts
├── use-cases/            # Business Logic (one file per operation)
│   ├── create-order.use-case.ts
│   └── get-order.use-case.ts
├── repositories/         # Data Access Layer
│   └── <entity>.repository.ts
├── dtos/                 # Validation with class-validator
│   ├── create-order.dto.ts
│   └── order-response.dto.ts
├── events/               # EventEmitter definitions
│   └── order-created.event.ts
├── listeners/            # @OnEvent handlers
│   └── order.listener.ts
├── <module>.module.ts
└── docs.md               # UseCase documentation
```

## UseCase Implementation Pattern

Extend `UseCase<TRequest, TResponse>` from `src/common/services/use-case.base.ts`:

```typescript
@Injectable()
export class CreateOrderUseCase extends UseCase<CreateOrderRequest, CreateOrderResponse> {
  validate(request: CreateOrderRequest): void {
    if (!isValidObjectId(request.cartId))
      throw new BadRequestException('Invalid cart ID');
  }

  async doExecute(request: CreateOrderRequest): Promise<CreateOrderResponse> {
    // 1. Fetch and validate context
    const context = await this.validateAndFetchContext(request);

    // 2. Perform core business logic
    const result = this.performCoreLogic(context);

    // 3. Persist changes
    await this.persistChanges(result);

    // 4. Return final result
    return this.fetchFinalResult(result.id);
  }

  // Use interfaces for data between private methods
  private async validateAndFetchContext(req: Request): Promise<ExecutionContext> { ... }
  private performCoreLogic(ctx: ExecutionContext): CalculationResult { ... }
}
```

**Key rules:**
- `doExecute` reads like a table of contents, not the implementation
- Use numbered comments for step-by-step flow
- Define `interface`s for data passed between private methods
- Never call `this.prisma` directly in `doExecute`; use semantic private methods

## Cross-Module Data Access

**CRITICAL**: Never query another module's tables directly.

```typescript
// WRONG: Direct Prisma access to another module's table
const user = await this.prisma.user.findUnique({ where: { id } });

// CORRECT: Use the owning module's service
const user = await this.userService.findUserById(id);
```

Each module owns its tables exclusively. Cross-module data flows through Service Facades.

## Validation Strategy

### Layer 1: Syntactic (DTOs)

All fields require `@Is...` decorators from `class-validator`:

```typescript
export class CreateOrderDto {
  @IsString()
  @IsNotEmpty()
  cartId: string;

  @IsOptional()
  @IsString()
  note?: string;
}
```

### Layer 2: Controller Params

Use `IsObjectIdPipe` for MongoDB ObjectIds:

```typescript
@Get(':id')
findOne(@Param('id', IsObjectIdPipe) id: string) { ... }
```

### Layer 3: Semantic (UseCase)

Business rules checked in `validate()` or early in `doExecute()`:

```typescript
private async validateBusinessRules(cart: CartV2, product: Product) {
  if (cart.shopId !== product.shopId) {
    throw new BadRequestException('Product does not belong to this shop');
  }
  if (product.inventory < 1) {
    throw new BadRequestException('Product out of stock');
  }
}
```

## Event-Driven Side Effects

Use `EventEmitter2` for non-blocking operations (emails, analytics, webhooks):

```typescript
// Publisher (in UseCase)
this.eventEmitter.emit('order.created', new OrderCreatedEvent(order));

// Subscriber (in listeners/)
@OnEvent('order.created')
async handleOrderCreated(payload: OrderCreatedEvent) {
  await this.emailService.sendReceipt(payload.order.email);
}
```

**When to use events:**
- Sending notifications (email, SMS)
- Updating analytics/logs
- Syncing with external systems (webhooks)

**When NOT to use events:**
- Core logic requiring strict consistency (use direct calls)

## Database Conventions (Prisma + MongoDB)

- Schema at `prisma/schema.prisma`
- Use `select` to fetch only needed fields
- Use `Promise.all` for independent parallel queries
- Use `findUnique` over `findFirst` for indexed lookups
- Semantic repository methods: `findOrderWithRelations()`, not `findOne()`

```typescript
// Good: Parallel independent queries
const [user, cart] = await Promise.all([
  this.fetchUser(userId),
  this.fetchCart(cartId),
]);

// Good: Select only needed fields
this.prisma.product.findUnique({
  where: { id },
  select: { id: true, price: true },
});
```

## Quick Commands

```bash
npm run db:generate     # Prisma generate + Swagger docs
npm run start:dev       # Development with watch
npm run test:e2e        # End-to-end tests
npm run docs:generate   # Generate unified Swagger
```

## Reference Files

- **Architecture patterns**: See [references/architecture.md](references/architecture.md) for detailed UseCase patterns, Saga pattern, and repository guidelines
- **Entity models**: See [references/entities.md](references/entities.md) for core data models (Shop, Product, Order, Cart, Customer, Merchant)
- **Developer checklist**: See [references/checklists.md](references/checklists.md) for pre-commit and PR review checklists
