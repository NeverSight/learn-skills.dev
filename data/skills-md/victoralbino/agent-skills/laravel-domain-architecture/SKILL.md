---
name: laravel-domain-architecture
description: >
  Domain-oriented architecture for Laravel without external package dependencies, based on concepts
  from "Laravel Beyond CRUD" (Spatie). Use this skill when the user wants to structure a Laravel project
  using DDD, domain-oriented architecture, or organize code by business concepts instead of technical
  properties. Also activate when the user asks about: Actions, Data Objects (DTOs), lean models,
  States with enums, ViewModels (Blade or API), HTTP Query builders, application layer, or scaling
  Laravel projects beyond simple CRUD. Activate for any mention of "domain layer", "application layer",
  "beyond CRUD", "domain-oriented", or requests to refactor a Laravel project into domain structure.
  Even if the user asks "how to organize a large Laravel project", this skill is relevant.
---

# Laravel Domain Architecture

Guide for creating and refactoring Laravel applications using a pragmatic domain-oriented architecture.
Based on patterns from "Laravel Beyond CRUD" (Brent Roose / Spatie), **simplified to work with pure PHP
and native Laravel features — no mandatory external packages**.

Core philosophy: **group code by business meaning, not by technical property. Don't fight the framework.**

---

## Agent Instructions

- When creating or modifying **Domain layer** components (Actions, Data Objects, Models, Enums, QueryBuilders, Collections, Events) -> consult `references/domain-building-blocks.md`
- When creating or modifying **Application layer** components (Controllers, Requests, Resources, Queries, Jobs, API Versioning) -> consult `references/application-layer.md`
- Do not load both references at once — use only the one relevant to the current task
- Always follow the naming conventions and anti-patterns listed below

---

## When to Use

Projects **larger than average** — 50+ models, multiple developers, multi-year lifespan. For simple CRUD,
stick with Laravel defaults. The tipping point is when navigating the standard `app/` structure starts to hurt.

---

## Project Structure

The architecture adds a `Domain/` layer inside `app/` while keeping the standard Laravel structure
for everything else. **No custom autoload, no custom Application class.**

```
app/
├── Domain/                    # Business logic (the "what")
│   ├── Invoice/
│   ├── Customer/
│   ├── Payment/
│   └── Shared/
├── Http/                      # Standard Laravel HTTP layer
│   ├── Controllers/
│   ├── Requests/
│   ├── Resources/
│   ├── Queries/
│   ├── ViewModels/
│   └── Middleware/
├── Jobs/
├── Listeners/
├── Notifications/
├── Providers/
└── Console/
```

### Domain Folders

Each domain is organized into subfolders by type:

```
app/Domain/Invoice/
├── Actions/
│   ├── CreateInvoiceAction.php
│   ├── MarkInvoiceAsPaidAction.php
│   └── CancelInvoiceAction.php
├── Models/
│   ├── Invoice.php
│   └── InvoiceLine.php
├── Enums/
│   └── InvoiceStatus.php
├── Data/
│   └── InvoiceData.php
├── QueryBuilders/
│   └── InvoiceQueryBuilder.php
├── Collections/
│   └── InvoiceLineCollection.php
├── Events/
│   └── InvoiceCreatedEvent.php
└── Exceptions/
    └── InvalidTransitionException.php
```

-> Detailed implementation of each domain block in `references/domain-building-blocks.md`

---

## Application Layer

The application layer uses **standard Laravel structure**. The internal organization of
Controllers, Requests, Resources, and Queries is up to the developer — group by domain,
by feature, or keep flat as the project requires.

### API Versioning

Only create version folders when the first breaking change happens. While there's
one version, no prefix needed.

Rules:
- **Domain layer is shared** — Actions, Models, Enums are the same across V1 and V2
- **Only version what changes** — If V2 only changes Invoices, don't copy Customers
- **Routes per version** — `routes/api_v1.php`, `routes/api_v2.php`
- **Deprecate, don't delete** — Keep V1 running as long as there are consumers

-> Detailed implementation in `references/application-layer.md`

---

## Naming Conventions

| Type | Suffix | Example |
|---|---|---|
| Action | `*Action` | `CreateInvoiceAction` |
| Data Object | `*Data` | `InvoiceData` |
| Model | — | `Invoice` |
| QueryBuilder | `*QueryBuilder` | `InvoiceQueryBuilder` |
| Collection | `*Collection` | `InvoiceLineCollection` |
| Enum | `*Status` / `*Type` | `InvoiceStatus` |
| Event | `*Event` | `InvoiceCreatedEvent` |
| Exception | `*Exception` | `InvalidTransitionException` |
| Controller | `*Controller` | `InvoiceController` |
| HTTP Query | `*IndexQuery` | `InvoiceIndexQuery` |
| Resource | `*Resource` | `InvoiceResource` |
| Request | `Store*Request` / `Update*Request` | `StoreInvoiceRequest` |
| Job | `*Job` | `SendInvoiceMailJob` |

---

## Core Principles

1. **Actions** — Classes with an `execute()` method. Represent user stories. Compose via constructor injection. Primary place for business logic.
2. **Lean Models** — Only relationships, casts, custom QueryBuilders, and custom Collections. No business logic.
3. **Data Objects** — Use typed `readonly` classes (pure PHP 8.3+) only when data comes from multiple sources or the Action is reused across contexts. For simple controller -> action flows, passing the Request or individual parameters is fine.
4. **Enums with methods** — Replace the state pattern in most cases. Include `color()`, `label()`, `canTransitionTo()` directly in the enum. Transitions are done via Actions.
5. **Jobs are infrastructure** — Manage queues and retries. Business logic stays in Actions called from `handle()`.
6. **Don't fight the framework** — Use standard `app/`, standard namespaces, standard artisan. The only addition is `Domain/`.

---

## Cross-Domain Communication

Domains communicate pragmatically based on the **nature of the interaction**, not on rigid boundaries.

### Rules

| Situation | Approach |
|---|---|
| Read a model/enum from another domain | Direct import |
| Validate a precondition from another domain | Direct call |
| Orchestrate actions atomically (transaction) | Direct call |
| Side effect (notify, log, sync) | Event |
| Async reaction (can fail without affecting the flow) | Event |
| Multiple domains react to the same fact | Event |

### Direct Import (models, enums, preconditions)

```php
namespace App\Domain\Invoice\Actions;

use App\Domain\Customer\Exceptions\InactiveCustomerException;
use App\Domain\Customer\Models\Customer;
use App\Domain\Invoice\Data\InvoiceData;
use App\Domain\Invoice\Models\Invoice;

class CreateInvoiceAction
{
    public function execute(InvoiceData $data, Customer $customer): Invoice
    {
        if (! $customer->isActive()) {
            throw new InactiveCustomerException();
        }

        return Invoice::create([
            'customer_id' => $customer->id,
            'number' => $data->number,
        ]);
    }
}
```

### Orchestration (needs the result, must be atomic)

When multiple domains must succeed together, the **app layer** orchestrates:

```php
class CheckoutController
{
    public function store(CheckoutRequest $request)
    {
        return DB::transaction(function () use ($request) {
            $invoice = app(CreateInvoiceAction::class)->execute($invoiceData);
            $payment = app(ProcessPaymentAction::class)->execute($invoice, $paymentData);

            return new CheckoutResource($invoice, $payment);
        });
    }
}
```

### Events (side effects, reactions)

```php
class CreateInvoiceAction
{
    public function execute(InvoiceData $data): Invoice
    {
        $invoice = Invoice::create([...]);
        event(new InvoiceCreatedEvent($invoice));

        return $invoice;
    }
}

// Another domain reacts via listener — no direct coupling
class ReconcilePaymentListener
{
    public function handle(InvoiceCreatedEvent $event): void
    {
        app(ReconcilePaymentAction::class)->execute($event->invoice);
    }
}
```

### What's Prohibited

- **Circular dependencies** — If A calls B and B calls A, extract to `Domain/Shared/` or use events
- **Side effects disguised as direct calls** — If the caller doesn't need the result, it should be an event

---

## Domain Service Providers

Each domain **can** have its own ServiceProvider when it needs to register
bindings, event listeners, or specific configurations:

```
app/Providers/
├── InvoiceServiceProvider.php
└── CustomerServiceProvider.php
```

For simple domains (no custom bindings), don't create a ServiceProvider — Laravel's auto-discovery
and auto-injection already handle it.

---

## Anti-patterns

- **Logic in Models** — Models don't calculate, don't send emails, don't validate business rules. That goes in Actions.
- **Overly generic Actions** — `ProcessInvoiceAction` that does 10 things. Prefer specific: `CreateInvoiceAction`, `MarkInvoiceAsPaidAction`.
- **Repository pattern** — Eloquent already is the repository. Use custom QueryBuilders instead.
- **Interfaces for everything** — Only create interfaces when there are multiple real implementations (e.g., payment gateways).
- **Giant Domain/Shared** — If `Shared/` grows too large, it has code that should be in its own domain.
- **DTOs for everything** — Don't create a DTO when the controller just passes 2-3 fields to an Action.
- **Fighting the framework** — Custom Application class, custom autoload, custom directory structure that breaks artisan. If it requires a hack, rethink the approach.

---

## Testing Strategy

- **Actions**: The most important tests. Pattern: **setup -> execute -> assert**
- **Models**: Test custom QueryBuilders and Collections in isolation
- **Enums**: Test behavior methods and transition rules
- **Data Objects**: Minimal testing — the type system does the heavy lifting

-> Complete examples in `references/domain-building-blocks.md`

---

## Migration Strategy

No need to adopt everything at once. Recommended order:

1. **Actions** — Extract business logic from controllers and models
2. **Domain folders** — Group related code when directories become large
3. **Data Objects** — Replace arrays with typed DTOs where justified
4. **Enums with methods** — Replace conditionals with behavior in the enum
5. **Custom QueryBuilders** — Extract complex scopes
6. **API Versioning** — Structure when the API needs breaking changes

Domains can and should change over time. Start pragmatically, refactor as understanding grows.

---

## Reference Files

- `references/domain-building-blocks.md` — Data Objects, Actions, Models, Enums, QueryBuilders, Collections, Events, Cross-Domain Communication, Tests
- `references/application-layer.md` — Controllers, Requests, Resources, HTTP Queries, ViewModels, Jobs, API Versioning
