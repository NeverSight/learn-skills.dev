---
name: angular-modularize
description: >
  Modularizes existing Angular components and projects following official
  angular.dev best practices, SOLID principles, and the Smart/Presentational
  pattern. Use when the user asks to "modularize", "refactor component",
  "split component", "extract component", "decompose component", "organize
  Angular project", "apply Angular best practices", "split into feature
  modules", "restructure project", or "improve project structure".
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
---

# Angular Modularization — Universal Best Practices

You are an expert Angular architect. These guidelines are **universal** for any
Angular project. Always detect the Angular version first and adapt accordingly.

**Sources:** angular.dev style guide, angular.dev component/signals/DI guides,
Smart/Presentational pattern, SOLID principles.

---

## Step 1: Analyze Before Changing

Before making ANY change:

1. **Read `package.json`** → detect `@angular/core` version
2. **Scan structure** → `Glob("**/*.component.ts")`, `Glob("**/*.module.ts")`, `Glob("**/*.routes.ts")`
3. **Detect standalone** → `Grep("standalone", glob="**/*.component.ts")`
4. **Identify large components** → read `.ts` and `.html` files, count lines, list responsibilities
5. **Map dependencies** → which components use which services, check imports
6. **Present findings** to the user and **ask confirmation** before proceeding

---

## Step 2: Identify Components That Need Modularization

### Single Responsibility Principle (SRP)

> "Each class should have only ONE reason to change." — SOLID

Ask: **what responsibilities does this component have?** If you describe it with
more than one "AND", it violates SRP and needs refactoring.

**Violation example:** "This component fetches users AND renders the list AND
handles the create form AND validates input AND manages pagination."

### Smell Indicators — When a Component MUST Be Split

| Indicator | Threshold | Action |
|-----------|-----------|--------|
| Template (HTML) lines | > 100 lines | Extract child components |
| Component class lines | > 200 lines | Extract logic to services |
| File total lines | > 400 lines | Split responsibilities (angular.dev style guide) |
| `inject()` calls or constructor params | > 5 | Too many concerns, split |
| Distinct `@if` blocks (or `*ngIf` in legacy) | > 3 unrelated sections | Each section → child component |
| Distinct `@for` loops (or `*ngFor` in legacy) | > 2 different data sources | Each list → child component |
| Component fetches data AND renders | Mixed smart/presentational | Split into container + presentational |
| Repeated HTML blocks | Same block 2+ times | Extract to shared component |
| Multiple form groups | > 2 in same component | Each form section → child component |
| Generic component name | `MainComponent`, `PageComponent` | Rename to reflect single responsibility |

### When a Component Should NOT Be Split

| Criteria | Reason |
|----------|--------|
| Template < 50 lines with single responsibility | Already small enough |
| Used only once, no children | No reuse benefit |
| Simple wrapper (< 3 inputs, no logic) | Already granular |
| Splitting needs > 5 inputs passed down | Creates prop drilling (worse) |
| Tightly coupled to parent lifecycle | Splitting breaks interaction |
| Feature has < 3 files total | Module overhead exceeds benefit |
| App has < 10 components total | Over-engineering |

---

## Step 3: Decompose a Monolithic Component

### 3.1 List Every Responsibility

Read the component and enumerate what it does:

```
Analysis of a monolithic OrderPageComponent:
1. Fetches order data from API          → Extract to OrderService
2. Displays order header info           → OrderHeaderComponent (presentational)
3. Renders line items table             → OrderItemsTableComponent (presentational)
4. Handles payment form                 → PaymentFormComponent (presentational)
5. Manages form validation              → Validators file or form service
6. Handles error/loading states         → Keep in smart component
```

### 3.2 Classify: Smart vs Presentational

| Type | Characteristics | Rules |
|------|----------------|-------|
| **Smart (Container)** | Injects services via `inject()`, fetches data, manages state with signals, coordinates children | One per route/feature. Knows WHERE data comes from. |
| **Presentational (Dumb)** | Receives data via `input()`/`input.required()`, emits events via `output()`, renders UI only | No service injection. No business logic. Reusable in any context. Does NOT know where data comes from. |

**Key test:** If the component wouldn't work in a different app without modification → smart.
If it would → presentational.

### 3.3 Where Each Responsibility Goes

| Responsibility | Destination | Rule |
|----------------|------------|------|
| API calls, data fetching | Service with `httpResource()` or `HttpClient` | Never in presentational components |
| Business logic, calculations | Service or utility file | Components should not contain business rules |
| Reusable UI block | `shared/components/` | If used in 2+ features |
| Feature-specific UI block | Child component in same feature dir | If used only here |
| Form validation rules | Validators file or service | Testable and reusable |
| State management | Service with `signal()`, `computed()`, `linkedSignal()` | Components are NOT the source of truth |

### 3.4 Extract — Before and After

**BEFORE — Monolithic (violates SRP, uses legacy patterns to show what to refactor):**

```typescript
// BEFORE: legacy patterns — *ngFor, *ngIf, constructor injection, no OnPush, no signals
@Component({
  selector: 'app-order-page',
  template: `
    <div class="header">
      <h1>{{ order?.title }}</h1>
      <span>{{ order?.status }}</span>
    </div>
    <table>
      <tr *ngFor="let item of order?.items">
        <td>{{ item.name }}</td>
        <td>{{ item.price | currency }}</td>
      </tr>
    </table>
    <form [formGroup]="paymentForm" (ngSubmit)="submitPayment()">
      <input formControlName="cardNumber">
      <div *ngIf="paymentForm.get('cardNumber')?.errors?.['required']">
        Card number is required
      </div>
      <button type="submit" [disabled]="paymentForm.invalid">Pay</button>
    </form>
  `
})
export class OrderPageComponent implements OnInit {
  order: Order | null = null;
  paymentForm: FormGroup;

  constructor(
    private http: HttpClient,
    private route: ActivatedRoute,
    private fb: FormBuilder,
    private router: Router,
    private notificationService: NotificationService
  ) {
    this.paymentForm = this.fb.group({
      cardNumber: ['', [Validators.required, Validators.minLength(16)]],
      expDate: ['', Validators.required],
      cvv: ['', [Validators.required, Validators.minLength(3)]]
    });
  }

  ngOnInit(): void {
    const id = this.route.snapshot.params['id'];
    this.http.get<Order>(`/api/orders/${id}`).subscribe(order => this.order = order);
  }

  submitPayment(): void {
    this.http.post('/api/payments', {
      orderId: this.order?.id,
      ...this.paymentForm.value
    }).subscribe({
      next: () => this.router.navigate(['/orders']),
      error: () => this.notificationService.error('Payment failed')
    });
  }
}
```

**AFTER — Modularized with modern Angular (v19+):**

```typescript
// order.service.ts — Data fetching (uses httpResource for reads, HttpClient for mutations)
@Injectable({ providedIn: 'root' })
export class OrderService {
  private readonly http = inject(HttpClient);

  readonly orderResource = httpResource<Order>(() => ({
    url: `/api/orders/${this.currentOrderId()}`
  }));

  readonly currentOrderId = signal<string>('');

  submitPayment(orderId: string, payment: PaymentData): Observable<PaymentResult> {
    return this.http.post<PaymentResult>('/api/payments', { orderId, ...payment });
  }
}
```

```typescript
// order-header.component.ts — Presentational (display only, no services)
@Component({
  selector: 'app-order-header',
  template: `
    <div class="header">
      <h1>{{ order().title }}</h1>
      <span class="status">{{ order().status }}</span>
      <p>{{ order().date | date:'longDate' }}</p>
    </div>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [DatePipe]
})
export class OrderHeaderComponent {
  readonly order = input.required<Order>();
}
```

```typescript
// order-items-table.component.ts — Presentational
@Component({
  selector: 'app-order-items-table',
  template: `
    <table>
      @for (item of items(); track item.id) {
        <tr>
          <td>{{ item.name }}</td>
          <td>{{ item.price | currency }}</td>
          <td>{{ item.quantity }}</td>
        </tr>
      } @empty {
        <tr><td colspan="3">No items</td></tr>
      }
      <tr class="total">
        <td colspan="2">Total</td>
        <td>{{ total() | currency }}</td>
      </tr>
    </table>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CurrencyPipe]
})
export class OrderItemsTableComponent {
  readonly items = input.required<OrderItem[]>();

  protected readonly total = computed(() =>
    this.items().reduce((sum, item) => sum + item.price * item.quantity, 0)
  );
}
```

```typescript
// payment-form.component.ts — Presentational (form UI, no API calls)
@Component({
  selector: 'app-payment-form',
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <input formControlName="cardNumber" placeholder="Card number">
      <input formControlName="expDate" placeholder="MM/YY">
      <input formControlName="cvv" placeholder="CVV">
      @if (form.get('cardNumber')?.hasError('required')) {
        <div class="error">Card number is required</div>
      }
      <button type="submit" [disabled]="form.invalid || submitting()">Pay</button>
    </form>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [ReactiveFormsModule]
})
export class PaymentFormComponent {
  private readonly fb = inject(FormBuilder);

  readonly submitting = input(false);
  readonly paymentSubmitted = output<PaymentData>();

  protected readonly form = this.fb.group({
    cardNumber: ['', [Validators.required, Validators.minLength(16)]],
    expDate: ['', Validators.required],
    cvv: ['', [Validators.required, Validators.minLength(3)]]
  });

  protected onSubmit(): void {
    if (this.form.valid) {
      this.paymentSubmitted.emit(this.form.value as PaymentData);
    }
  }
}
```

```typescript
// order-page.component.ts — Smart/Container (orchestrates children, manages state)
@Component({
  selector: 'app-order-page',
  template: `
    @if (orderService.orderResource.hasValue()) {
      <app-order-header [order]="orderService.orderResource.value()!" />
      <app-order-items-table [items]="orderService.orderResource.value()!.items" />
      <app-payment-form
        [submitting]="submitting()"
        (paymentSubmitted)="onPaymentSubmit($event)" />
    } @else if (orderService.orderResource.isLoading()) {
      <p>Loading order...</p>
    } @else if (orderService.orderResource.error()) {
      <p>Error loading order</p>
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [OrderHeaderComponent, OrderItemsTableComponent, PaymentFormComponent]
})
export class OrderPageComponent {
  protected readonly orderService = inject(OrderService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly notificationService = inject(NotificationService);

  protected readonly submitting = signal(false);

  constructor() {
    this.orderService.currentOrderId.set(this.route.snapshot.params['id']);
  }

  protected onPaymentSubmit(payment: PaymentData): void {
    this.submitting.set(true);
    const orderId = this.orderService.orderResource.value()!.id;
    this.orderService.submitPayment(orderId, payment).subscribe({
      next: () => {
        this.notificationService.success('Payment completed');
        this.router.navigate(['/orders']);
      },
      error: () => {
        this.notificationService.error('Payment failed');
        this.submitting.set(false);
      }
    });
  }
}
```

### 3.5 Handle Shared State Between Split Components

| Pattern | When to Use |
|---------|------------|
| Parent passes data via `input()` | Simple flow, < 3 levels deep |
| Shared service with `signal()` / `computed()` | Multiple siblings need same reactive state |
| `output()` events up + `input()` down | Parent orchestrates child interactions |
| `model()` two-way binding | Parent and child need to sync a value |
| `linkedSignal()` | Dependent state that resets when source changes but remains writable |
| NgRx / signal store | Complex state with many consumers across features |

**Rule:** Never create a service just to avoid passing one input. Use services when
3+ components need the same state or prop drilling exceeds 3 levels.

---

## Step 4: Project-Level Structure

### Angular v19+ (Standalone by default)

Components are standalone by default. No need for `standalone: true` explicitly.

```
src/app/
├── app.component.ts
├── app.config.ts                    # provideRouter, provideHttpClient, etc.
├── app.routes.ts
├── core/                            # Singletons — imported ONCE at root
│   ├── interceptors/
│   │   └── auth.interceptor.ts      # functional interceptor
│   ├── guards/
│   │   └── auth.guard.ts            # functional guard (CanActivateFn)
│   └── services/
│       └── auth.service.ts          # providedIn: 'root'
├── shared/                          # Reusable, STATELESS
│   ├── components/
│   │   └── data-table/
│   │       ├── data-table.component.ts
│   │       ├── data-table.component.html
│   │       ├── data-table.component.css
│   │       └── data-table.component.spec.ts
│   ├── directives/
│   ├── pipes/
│   └── models/
└── features/                        # Lazy-loaded business domains
    └── users/
        ├── user-list/
        │   ├── user-list.component.ts       # smart/container
        │   ├── user-list.component.html
        │   ├── user-list.component.spec.ts
        │   └── components/                  # presentational children
        │       └── user-card/
        │           ├── user-card.component.ts
        │           └── user-card.component.spec.ts
        ├── user-detail/
        ├── services/
        │   └── user.service.ts
        ├── models/
        │   └── user.model.ts
        └── users.routes.ts
```

### Angular v14-v16 (NgModules)

```
src/app/
├── app.module.ts
├── app-routing.module.ts
├── core/
│   └── core.module.ts
├── shared/
│   └── shared.module.ts
└── features/
    └── users/
        ├── users.module.ts
        ├── users-routing.module.ts
        ├── components/
        ├── services/
        └── models/
```

### Module Boundary Rules

| Directory | Contains | Rules |
|-----------|----------|-------|
| **core/** | Auth, interceptors, guards, app-wide services | `providedIn: 'root'`. Imported ONCE at root. Never in features. |
| **shared/** | Reusable UI: buttons, tables, pipes, directives | **Stateless only**. No services with state. Barrel exports for public API. |
| **features/** | Business domains with routing | Self-contained. Lazy-loaded. No cross-feature imports. Smart + presentational. |

### When TO Create a Feature Directory

- Feature has its own route
- 3+ related components
- Benefits from lazy loading
- Distinct business domain

### When NOT to Create a Feature Directory

- App < 10 components total
- Single component with no subroutes
- Would create circular dependencies
- Always loads at startup anyway

---

## Step 5: Lazy Loading

### Route-based (v19+)

```typescript
// app.routes.ts
export const routes: Routes = [
  {
    path: 'users',
    loadChildren: () => import('./features/users/users.routes')
      .then(m => m.USERS_ROUTES)
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./features/dashboard/dashboard.component')
      .then(c => c.DashboardComponent)
  }
];
```

### Deferred Loading with `@defer` (v17+)

For heavy components within a page. Component inside `@defer` MUST be standalone.

```html
@defer (on viewport) {
  <app-heavy-chart [data]="chartData()" />
} @placeholder (minimum 200ms) {
  <div class="skeleton">Chart loading...</div>
} @loading (after 100ms; minimum 500ms) {
  <app-spinner />
} @error {
  <p>Failed to load chart</p>
}
```

**Triggers:** `on idle` (default), `on viewport`, `on interaction`, `on hover`,
`on timer(500ms)`, `when condition`, `on immediate`.

**Prefetching:** `@defer (on interaction; prefetch on idle)` — loads JS in background
before user triggers it.

### NgModules (v14-v16)

```typescript
const routes: Routes = [
  {
    path: 'users',
    loadChildren: () => import('./features/users/users.module')
      .then(m => m.UsersModule)
  }
];
```

---

## Step 6: Modern Angular APIs (v19+)

### Signals — Reactive State

```typescript
// Writable signal
protected readonly count = signal(0);

// Read-only computed
protected readonly doubled = computed(() => this.count() * 2);

// Dependent writable state (resets when source changes, but still writable)
protected readonly selectedOption = linkedSignal(() => this.options()[0]);

// Side effects
effect(() => {
  console.log('Count changed:', this.count());
});
```

### Component Communication

```typescript
// Inputs (signal-based, read-only)
readonly name = input<string>();                    // optional
readonly id = input.required<number>();             // required
readonly disabled = input(false);                   // with default
readonly width = input(0, { transform: numberAttribute }); // with transform

// Two-way binding (writable input + automatic output)
readonly value = model(0);                          // parent uses [(value)]="signal"

// Outputs (event emitter)
readonly closed = output<void>();
readonly selected = output<User>();
```

### Data Fetching

```typescript
// httpResource for GET requests (reactive, signal-based)
readonly usersResource = httpResource<User[]>(() => '/api/users');

// resource() for custom async operations
readonly dataResource = resource({
  params: () => ({ id: this.userId() }),
  loader: ({ params, abortSignal }) =>
    fetch(`/api/data/${params.id}`, { signal: abortSignal }).then(r => r.json())
});

// HttpClient for mutations (POST, PUT, DELETE)
this.http.post('/api/users', userData).subscribe();
```

### Template Control Flow

```html
@if (user(); as u) {
  <h1>{{ u.name }}</h1>
} @else {
  <p>No user</p>
}

@for (item of items(); track item.id) {
  <app-item-card [item]="item" />
} @empty {
  <p>No items found</p>
}

@switch (status()) {
  @case ('active') { <app-active-badge /> }
  @case ('inactive') { <app-inactive-badge /> }
  @default { <span>Unknown</span> }
}
```

### Dependency Injection

```typescript
// inject() function — preferred over constructor injection
private readonly http = inject(HttpClient);
private readonly router = inject(Router);
private readonly destroyRef = inject(DestroyRef);

// Cleanup with DestroyRef (replaces ngOnDestroy)
constructor() {
  this.destroyRef.onDestroy(() => {
    // cleanup logic
  });
}
```

### Lifecycle

```typescript
// Still valid: ngOnInit, ngOnChanges, ngOnDestroy, etc.
// Modern additions:
afterNextRender(() => {
  // DOM manipulation after first render (SSR-safe)
});

afterEveryRender(() => {
  // runs after every render cycle
});
```

---

## Step 7: Component Best Practices Summary

Every component MUST follow these rules:

- **`ChangeDetectionStrategy.OnPush`** on ALL components
- **`inject()` function** for dependency injection (not constructor params)
- **`input()` / `input.required()`** for inputs (not `@Input()` decorator)
- **`output()`** for events (not `@Output()` decorator)
- **`model()`** for two-way binding
- **Signals** (`signal`, `computed`, `linkedSignal`) for reactive state
- **`@if`, `@for`, `@switch`** control flow (not `*ngIf`, `*ngFor`)
- **`readonly`** on properties initialized by Angular (`input`, `output`, queries)
- **`protected`** for members only used in templates
- **Co-locate** `.ts`, `.html`, `.css`, `.spec.ts` in same directory
- **One concept per file** — one component/service/directive per file
- **kebab-case** file names: `user-profile.component.ts`

---

## Step 8: Naming Conventions

- **Files:** `<name>.<type>.ts` → `user-list.component.ts`, `auth.guard.ts`, `date-format.pipe.ts`
- **Classes:** `UserListComponent`, `AuthService`, `DateFormatPipe`
- **Selectors:** `app-user-list` (kebab-case with prefix)
- **Event handlers:** name by action performed, not trigger → `saveUser()` not `handleClick()`
- **Avoid:** `utils.ts`, `helpers.ts`, `common.ts` — be specific
- **Barrel exports** (`index.ts`) only for public APIs, never for internals

---

## Step 9: NgModule → Standalone Migration

When project uses NgModules and Angular v14+:

1. **Leaf components first** (no children) → add `standalone: true` + `imports` array
2. **Shared components** next → convert and update all consumers
3. **Feature modules** one at a time → replace `.module.ts` with `.routes.ts`
4. **Update routing** → `loadChildren` with module → `loadComponent`/`loadChildren` with routes
5. **Remove empty modules** → delete `.module.ts` when all declarations are standalone
6. **Hybrid is OK** → not everything must be migrated at once

### Do NOT Migrate

- Third-party modules without standalone support
- Modules with complex providers → migrate providers to `app.config.ts` first
- Library entry point modules

---

## Step 10: Anti-Patterns

| Anti-Pattern | Fix |
|-------------|-----|
| God component (> 200 lines class) | Split into smart + presentational |
| God module (50+ declarations) | Split into feature modules |
| Prop drilling (> 3 levels) | Shared service with signals |
| Cross-feature imports | Communicate via shared services |
| Services in `shared/` | Move stateful services to `core/` |
| Business logic in templates | Move to `computed()` or methods |
| Fat templates (> 100 lines) | Extract child components |
| Generic file names | Name by specific responsibility |
| Circular dependencies | Restructure module boundaries |
| `@Input`/`@Output` decorators | Use `input()`/`output()` signal APIs |
| `*ngIf`/`*ngFor` directives | Use `@if`/`@for` control flow |
| Constructor injection | Use `inject()` function |
| Default change detection | Use `ChangeDetectionStrategy.OnPush` |
| `subscribe()` for GET requests | Use `httpResource()` or `resource()` |
| Manual `ngOnDestroy` cleanup | Use `DestroyRef.onDestroy()` |

---

## Step 11: Refactoring Checklist

Execute in this order:

1. **Identify large components** → read `.html` and `.ts` files, list candidates by thresholds
2. **Split monolithic components** → apply Step 3 for each candidate
3. **Create directory structure** → `core/`, `shared/`, `features/`
4. **Extract core services** → auth, interceptors, guards → `core/`
5. **Extract shared components** → reusable UI → `shared/`
6. **Group into features** → related components → `features/<name>/`
7. **Set up lazy loading** → configure routes + `@defer` blocks
8. **Update all imports** → fix paths across the application
9. **Modernize APIs** → replace deprecated patterns (see Anti-Patterns table)
10. **Build the project** → `npx ng build` to detect errors and circular dependencies
11. **Run ALL tests** → `npx ng test --watch=false`
12. **Serve and verify** → `npx ng serve`, test navigation and lazy loading

---

## Step 12: Unit Testing

Every file must have a `.spec.ts`:

- **Presentational**: test rendering with different `input()` values, `output()` emissions, user interactions
- **Smart**: test service calls, signal state management, child coordination
- **Services**: test public methods, HTTP calls with `HttpTestingController`
- **Guards**: test access conditions and redirects
- **Pipes**: test transformations with edge cases
- After restructuring, run ALL existing tests to verify nothing broke

---

## Important Reminders

- **Always present before/after** structure to the user
- **Ask confirmation** before moving files or splitting components
- **Preserve git history** → use `git mv` for file moves
- **Update `tsconfig.json`** path aliases after restructuring
- **Verify `angular.json`** references after file moves
- **Do not over-modularize** → if splitting adds more complexity than it solves, don't split
- **Adapt to version** → use legacy APIs only if the project's Angular version requires it
