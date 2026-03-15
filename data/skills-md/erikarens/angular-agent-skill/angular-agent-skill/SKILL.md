---
name: angular-agent-skill
description: Expert Angular, TypeScript, and Tailwind development with modern signal-based patterns, standalone components, and built-in control flow. Use when working on Angular projects, creating components, services, directives, pipes, writing templates, managing state with signals, handling forms, routing, HTTP requests, testing, accessibility (a11y), ARIA, or any Angular-related code. Also use when reviewing Angular code, debugging Angular issues, making architectural decisions, or implementing accessible UI patterns like focus traps, screen reader announcements, keyboard navigation, or ARIA attributes in Angular applications. Use this skill whenever building headless accessible components with @angular/aria — including tabs, accordions, menus, menubars, toolbars, listboxes, select dropdowns, multiselect, autocomplete, combobox, grids, or tree views — even if the user doesn't explicitly mention "aria" or "accessibility".
---

# Angular Development

Expert guidance for building scalable Angular applications using modern APIs: signals, standalone components, built-in control flow, and strict TypeScript.

## Core Architecture

### Project Structure

```
src/
└── app/
    ├── core/           # Non-business features (layout, auth, guards)
    ├── features/       # Business domain features
    ├── shared/         # Reusable "dumb" components, pipes, directives
    ├── services/       # Global and feature-specific services
    ├── interfaces/     # TypeScript interfaces
    ├── types/          # Type definitions, DTOs (requests/, responses/)
    ├── enums/          # Enums
    ├── utils/          # Pure utility functions
    ├── app.component.ts
    ├── app.config.ts
    └── app.routes.ts
```

Feature folders follow: `pages/` (routed), `components/` (non-routed), `guards/`, `feature.routes.ts`.

### Coding Standards

- Single quotes, 2-space indent, `const` by default
- Kebab-case file names with Angular suffixes (`.component.ts`, `.service.ts`)
- Strict typing, never use `any` — define explicit types
- Optional chaining (`?.`) and nullish coalescing (`??`)
- Template literals for string interpolation
- Always declare methods and properties explicitly as `public` or `private` — never rely on implicit public
- Prefix private properties with underscore: `private _state`, `private readonly _http = inject(HttpClient)`
- Use `private readonly` for all DI injections: `private readonly _http = inject(HttpClient)`
- File structure: imports, class, properties, lifecycle, public methods, private methods

## Signals (State Management)

Use Angular's signal system as the primary state management approach.

### Signal Primitives

```typescript
// Writable signal
count = signal(0);
count.set(3);
count.update(v => v + 1);

// Read-only exposure
private readonly _count = signal(0);
readonly count = this._count.asReadonly();

// Computed (lazy, memoized, read-only)
doubleCount = computed(() => this.count() * 2);

// Custom equality for objects
data = signal(['test'], { equal: (a, b) => a.length === b.length });
```

### Signal Inputs, Outputs & Queries

Use function-based APIs instead of decorators:

```typescript
// Inputs
value = input(0);                                    // InputSignal<number>
name = input<string>();                              // InputSignal<string | undefined>
label = input.required<string>();                    // Required, no undefined
disabled = input(false, { transform: booleanAttribute });

// Outputs
closed = output<void>();                             // OutputEmitterRef<void>
valueChanged = output<number>();
this.valueChanged.emit(42);

// Model inputs (two-way binding)
checked = model(false);                              // ModelSignal<boolean>
// Parent: <my-comp [(checked)]="isChecked" />

// Queries
header = viewChild(HeaderComponent);                 // Signal<HeaderComponent | undefined>
items = viewChildren(ItemComponent);                 // Signal<readonly ItemComponent[]>
toggle = contentChild.required(ToggleComponent);     // Signal<ToggleComponent>
```

### linkedSignal

Writable signal that resets when dependencies change. Use for selections that depend on changing data:

```typescript
// Shorthand
selectedOption = linkedSignal(() => this.options()[0]);

// Full form — preserves selection across data changes
selectedOption = linkedSignal({
  source: this.options,
  computation: (newOptions, previous) =>
    newOptions.find(o => o.id === previous?.value.id) ?? newOptions[0],
});
```

### resource / httpResource

Integrate async data into signals. Experimental but ready for use:

```typescript
userResource = resource({
  params: () => ({ id: this.userId() }),
  loader: ({ params, abortSignal }) =>
    fetch(`/api/users/${params.id}`, { signal: abortSignal }).then(r => r.json()),
});

// Access: userResource.value(), .status(), .isLoading(), .error(), .hasValue()
// Actions: userResource.reload(), .set(), .update()
```

### effect

For side effects only — logging, localStorage sync, DOM interop. Never use for state propagation (use `computed` or `linkedSignal` instead):

```typescript
constructor() {
  effect((onCleanup) => {
    const user = this.currentUser();
    const timer = setTimeout(() => console.log(user), 1000);
    onCleanup(() => clearTimeout(timer));
  });
}
```

### RxJS Interop

```typescript
// Observable → Signal
counter = toSignal(this.counter$, { initialValue: 0 });
// Use requireSync: true for BehaviorSubject

// Signal → Observable
query$ = toObservable(this.query);
```

For detailed signal patterns, see [references/signals.md](references/signals.md).

## Templates

### Built-in Control Flow

Always use the built-in block syntax. Never use `*ngIf`, `*ngFor`, `*ngSwitch`:

```html
@if (user(); as user) {
  <h1>{{ user.name }}</h1>
} @else {
  <p>Loading...</p>
}

@for (item of items(); track item.id) {
  <li>{{ item.name }}</li>
} @empty {
  <li>No items found.</li>
}

@switch (role()) {
  @case ('admin') { <admin-panel /> }
  @case ('editor') { <editor-panel /> }
  @default { <viewer-panel /> }
}
```

`@for` requires `track`. Use a unique identifier; use `$index` only for static lists. Available context: `$index`, `$first`, `$last`, `$even`, `$odd`, `$count`.

### Deferrable Views

Reduce initial bundle size by deferring non-critical content:

```html
@defer (on viewport; prefetch on idle) {
  <heavy-chart [data]="chartData()" />
} @placeholder (minimum 200ms) {
  <div class="skeleton"></div>
} @loading (after 100ms; minimum 500ms) {
  <spinner />
} @error {
  <p>Failed to load chart.</p>
}
```

Triggers: `on idle`, `on viewport`, `on interaction`, `on hover`, `on timer(500ms)`, `on immediate`, `when condition`.

For detailed template patterns, see [references/templates.md](references/templates.md).

## Components & DI

### Standalone by Default

All components are standalone by default (Angular 19+). Import dependencies directly:

```typescript
@Component({
  selector: 'app-user-card',
  imports: [DatePipe, RouterLink],
  templateUrl: './user-card.component.html',
  styleUrl: './user-card.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class UserCardComponent {
  user = input.required<User>();
  selected = output<void>();
}
```

### Dependency Injection

Use `inject()` function, not constructor injection. Always use `private readonly` with underscore prefix:

```typescript
export class UserService {
  private readonly _http = inject(HttpClient);
  private readonly _config = inject(ConfigService);
}
```

Services use `providedIn: 'root'` for tree-shakeable singletons.

### HTTP

Convert observables to promises with `firstValueFrom`:

```typescript
public async getUser(id: string): Promise<User> {
  return firstValueFrom(
    this._http.get<User>(`/api/users/${id}`)
  );
}
```

Configure with functional API:

```typescript
provideHttpClient(
  withInterceptors([authInterceptor]),
  withFetch(),  // Use Fetch API, required for SSR streaming
)
```

### Functional Interceptors

```typescript
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = inject(AuthService).getToken();
  if (token) {
    req = req.clone({ setHeaders: { Authorization: `Bearer ${token}` } });
  }
  return next(req);
};
```

### Lifecycle & Cleanup

- Use `afterNextRender()` / `afterRenderEffect()` for DOM operations (browser-only)
- Prefer `DestroyRef` + `takeUntilDestroyed()` for subscription cleanup:

```typescript
// In constructor (injection context) — no argument needed
this.route.params.pipe(takeUntilDestroyed()).subscribe(/*...*/);

// Outside constructor — pass DestroyRef
private readonly _destroyRef = inject(DestroyRef);
public ngOnInit() {
  this.obs$.pipe(takeUntilDestroyed(this._destroyRef)).subscribe(/*...*/);
}
```

- Render phases: `earlyRead` → `write` → `mixedReadWrite` → `read`

## Routing

Use functional guards and resolvers. Lazy-load feature routes:

```typescript
export const routes: Routes = [
  {
    path: 'dashboard',
    loadComponent: () => import('./features/dashboard/pages/dashboard.component'),
    canActivate: [() => inject(AuthService).isAuthenticated()],
  },
  {
    path: 'user/:id',
    loadComponent: () => import('./features/user/pages/user-detail.component'),
    resolve: { user: (route: ActivatedRouteSnapshot) => inject(UserService).getUser(route.paramMap.get('id')!) },
  },
];
```

Enable `withComponentInputBinding()` to automatically bind route params, query params, and resolve data to component inputs:

```typescript
// app.config.ts
provideRouter(routes, withComponentInputBinding(), withViewTransitions())

// Component — 'id' auto-bound from route param ':id', 'user' from resolve
export class UserDetailComponent {
  id = input<string>();
  user = input<User>();
}
```

## App Configuration

```typescript
// app.config.ts
export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes, withComponentInputBinding(), withViewTransitions()),
    provideHttpClient(withInterceptors([authInterceptor]), withFetch()),
    provideAnimationsAsync(),
    provideClientHydration(withEventReplay()),
    // provideExperimentalZonelessChangeDetection(), // Zoneless (experimental)
  ],
};
```

## Performance

- `ChangeDetectionStrategy.OnPush` on all components
- `track` with unique IDs in `@for` loops
- `@defer` for below-fold and heavy components
- `NgOptimizedImage` for all images with `priority` on LCP image
- Pure pipes for repeated template computations
- Signals automatically optimize re-renders with granular tracking
- `takeUntilDestroyed()` to prevent subscription memory leaks

## Accessibility (a11y)

Use semantic HTML first. Add ARIA attributes only when native elements aren't sufficient. Always bind ARIA attributes with `[attr.aria-*]` (not `[aria-*]`) since they have no DOM properties.

### @angular/aria — Headless Accessible Components

For common interactive UI patterns, use `@angular/aria` (`npm install @angular/aria`). These headless directives implement WAI-ARIA patterns with full keyboard navigation, ARIA attributes, and focus management built in — you provide HTML structure and CSS styling.

Available components:

| Need | Component | Import |
|------|-----------|--------|
| Collapsible sections | Accordion | `@angular/aria/accordion` |
| Tabbed panels | Tabs | `@angular/aria/tabs` |
| Selection list | Listbox | `@angular/aria/listbox` |
| Dropdown (<20 options) | Select | `@angular/aria/combobox` + `listbox` |
| Multi-select dropdown | Multiselect | `@angular/aria/combobox` + `listbox` |
| Searchable dropdown | Autocomplete | `@angular/aria/combobox` + `listbox` |
| Context/action menu | Menu | `@angular/aria/menu` |
| Navigation bar | Menubar | `@angular/aria/menu` |
| Grouped actions | Toolbar | `@angular/aria/toolbar` |
| Interactive table/calendar | Grid | `@angular/aria/grid` |
| Hierarchical data | Tree | `@angular/aria/tree` |

All components are headless (bring your own styles), support RTL, use Angular signals for state, and import directly into standalone components.

```typescript
// Example: Accessible tabs with @angular/aria
import { Tabs, TabList, Tab, TabPanel, TabContent } from '@angular/aria/tabs';

@Component({
  imports: [Tabs, TabList, Tab, TabPanel, TabContent],
  template: `
    <div ngTabs>
      <div ngTabList selectionMode="follow" selectedTab="general">
        <div ngTab value="general">General</div>
        <div ngTab value="security">Security</div>
      </div>
      <div ngTabPanel [preserveContent]="true" value="general">
        <ng-template ngTabContent>General settings</ng-template>
      </div>
      <div ngTabPanel [preserveContent]="true" value="security">
        <ng-template ngTabContent>Security settings</ng-template>
      </div>
    </div>
  `,
})
```

For detailed API reference, inputs, keyboard interactions, and examples for all components, see [references/angular-aria.md](references/angular-aria.md).

### CDK a11y Module

For lower-level accessibility utilities (focus traps, focus monitoring, screen reader announcements, custom keyboard navigation), use `@angular/cdk/a11y`. Services are `providedIn: 'root'` — no module import needed:

```typescript
import { CdkTrapFocus, CdkMonitorFocus, CdkAriaLive } from '@angular/cdk/a11y';
```

### Focus Management

Use `CdkTrapFocus` for modals/dialogs to trap Tab focus. Use `cdkFocusInitial` to mark the initial focus target:

```html
<div role="dialog" aria-modal="true" [attr.aria-labelledby]="titleId"
     cdkTrapFocus [cdkTrapFocusAutoCapture]="true">
  <h2 [id]="titleId">{{ title() }}</h2>
  <input cdkFocusInitial />
  <button (click)="close()">Close</button>
</div>
```

Use `FocusMonitor` to detect how an element received focus and show keyboard-only focus rings:

```typescript
private readonly _focusMonitor = inject(FocusMonitor);
// _focusMonitor.monitor(el) → Observable<FocusOrigin>
// _focusMonitor.focusVia(el, 'keyboard') → programmatic focus with origin
```

### Screen Reader Announcements

Use `LiveAnnouncer` for dynamic status updates:

```typescript
private readonly _liveAnnouncer = inject(LiveAnnouncer);
this._liveAnnouncer.announce('Item saved', 'polite');    // Waits for current speech
this._liveAnnouncer.announce('Error occurred', 'assertive'); // Interrupts
```

Or `CdkAriaLive` in templates: `<div [cdkAriaLive]="'polite'">{{ status() }}</div>`

### Keyboard Navigation

`FocusKeyManager` — roving tabindex pattern (moves DOM focus between items):

```typescript
keyManager = new FocusKeyManager(this.items()).withWrap().withVerticalOrientation();
// Items implement: focus(), disabled?, getLabel?()
```

`ActiveDescendantKeyManager` — uses `aria-activedescendant` (focus stays on host, e.g. combobox):

```typescript
keyManager = new ActiveDescendantKeyManager(this.options()).withWrap().withTypeAhead();
// Items implement: setActiveStyles(), setInactiveStyles(), disabled?
// Host: [attr.aria-activedescendant]="keyManager.activeItem?.id"
```

### Accessible Forms

```html
<label for="email">Email</label>
<input id="email" type="email"
  [attr.aria-invalid]="emailInvalid() ? 'true' : null"
  [attr.aria-describedby]="emailInvalid() ? 'email-error' : null"
  [attr.aria-required]="'true'" />
@if (emailInvalid()) {
  <span id="email-error" role="alert">Please enter a valid email.</span>
}
```

For detailed CDK a11y patterns and full API reference, see [references/accessibility.md](references/accessibility.md).

## Security

- Never use `innerHTML` — rely on Angular's built-in sanitization
- Sanitize dynamic content with Angular's DomSanitizer when necessary

## Testing

- Arrange-Act-Assert pattern
- Test services, components, and utilities with high coverage

## SSR / Hybrid Rendering

Configure per-route rendering in `app.routes.server.ts`:

```typescript
export const serverRoutes: ServerRoute[] = [
  { path: '', renderMode: RenderMode.Client },
  { path: 'about', renderMode: RenderMode.Prerender },
  { path: 'profile', renderMode: RenderMode.Server },
];
```

Use `afterNextRender()` for browser-only code. `@defer` blocks render `@placeholder` on server.

## References

- **[references/signals.md](references/signals.md)** — Detailed signal API reference, patterns for resource, linkedSignal, effect cleanup, and RxJS interop
- **[references/templates.md](references/templates.md)** — Control flow details, @defer triggers, SSR considerations, and template best practices
- **[references/angular-aria.md](references/angular-aria.md)** — `@angular/aria` headless accessible components: Accordion, Tabs, Listbox, Select, Multiselect, Autocomplete, Combobox, Menu, Menubar, Toolbar, Grid, Tree — with full API, inputs, keyboard interactions, and examples
- **[references/accessibility.md](references/accessibility.md)** — CDK a11y utilities: FocusTrap, FocusMonitor, LiveAnnouncer, AriaDescriber, KeyManagers, InteractivityChecker, InputModalityDetector, HighContrastModeDetector, and accessible component patterns
