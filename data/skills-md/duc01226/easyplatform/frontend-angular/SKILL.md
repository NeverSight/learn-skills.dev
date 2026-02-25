---
name: frontend-angular
version: 1.0.0
description: '[Frontend] Use when creating or modifying Angular components, forms, stores, or API services in WebV2 (Angular 19) with proper base class inheritance, state management, and platform patterns.'
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

## Quick Summary

**Goal:** Create or modify Angular 19 frontend code in WebV2 -- components, forms, stores, and API services -- following platform patterns.

**Workflow:**

1. **Pre-Flight** -- Identify app, search similar code, determine type (component/form/store/service)
2. **Select Pattern** -- Choose from Component, Form, Store, or API Service patterns below
3. **Implement** -- Follow BEM template standard, SCSS host+wrapper pattern, platform base classes
4. **Wire Up** -- Route config, module imports, API service integration

**Key Rules:**

- Never extend Platform* directly; always use AppBase* intermediaries
- All HTML elements MUST have BEM classes (`block__element --modifier`)
- Use `.pipe(this.untilDestroyed())` for all subscriptions
- Always extend `PlatformApiService` for HTTP calls, never use `HttpClient` directly
- Always use `PlatformVmStore` for state management, never manual signals
- MUST READ `.ai/docs/frontend-code-patterns.md` and design system docs before implementation

**Prerequisites:** MUST READ `.claude/skills/shared/design-system-check.md` for mandatory design system checks.

## Pre-Flight Checklist

- [ ] Identify correct app: `growth-for-company`, `employee`, etc.
- [ ] **Read the design system docs** for the target application
- [ ] Search for similar code: `grep "{FeatureName}" --include="*.ts"`
- [ ] Determine what you need: component, form, store, API service, or combination
- [ ] **Read** `.ai/docs/frontend-code-patterns.md`

## File Locations

```
src/WebV2/apps/{app-name}/src/app/
  features/
    {feature}/
      {feature}.component.ts          # Component
      {feature}.component.html         # Template
      {feature}.component.scss         # Styles
      {feature}.store.ts               # Store (if complex state)
      {feature}-form.component.ts      # Form component

src/Frontend/libs/apps-domains/src/lib/
  {domain}/
    services/
      {feature}-api.service.ts         # API Service
```

## Code Responsibility Hierarchy (CRITICAL)

**Place logic in the LOWEST appropriate layer to enable reuse and prevent duplication:**

| Layer            | Responsibility                                                            |
| ---------------- | ------------------------------------------------------------------------- |
| **Entity/Model** | Display helpers, static factory methods, default values, dropdown options |
| **Service**      | API calls, command factories, data transformation                         |
| **Component**    | UI event handling ONLY -- delegates all logic to lower layers             |

```typescript
// BAD: Logic in component (leads to duplication)
readonly authTypes = [{ value: AuthType.OAuth2, label: 'OAuth2' }, ...];

// GOOD: Logic in entity/model (single source of truth, reusable)
readonly authTypes = AuthConfigurationDisplay.getApiAuthTypeOptions();
```

---

# Part 1: Components

## Component Hierarchy

```
PlatformComponent                    # Base: lifecycle, subscriptions, signals
  PlatformVmComponent               # + ViewModel injection
  PlatformFormComponent             # + Reactive forms integration
  PlatformVmStoreComponent          # + ComponentStore state management

AppBaseComponent                     # + Auth, roles, company context
  AppBaseVmComponent                # + ViewModel + auth context
  AppBaseFormComponent              # + Forms + auth + validation
  AppBaseVmStoreComponent           # + Store + auth + loading/error
```

## Component Type Decision

| Scenario             | Base Class                | Use When                      |
| -------------------- | ------------------------- | ----------------------------- |
| Simple display       | `AppBaseComponent`        | Static content, no state      |
| With ViewModel       | `AppBaseVmComponent`      | Needs mutable view model      |
| Form with validation | `AppBaseFormComponent`    | User input forms              |
| Complex state/CRUD   | `AppBaseVmStoreComponent` | Lists, dashboards, multi-step |

## Component HTML Template Standard (BEM Classes)

**All UI elements MUST have BEM classes, even without styling needs.** This makes HTML self-documenting.

```html
<!-- GOOD: All elements have BEM classes -->
<div class="feature-list">
    <div class="feature-list__header">
        <h1 class="feature-list__title">Features</h1>
        <button class="feature-list__btn --add" (click)="onAdd()">Add New</button>
    </div>
    <div class="feature-list__content">
        @for (item of vm.items; track trackByItem) {
        <div class="feature-list__item">
            <span class="feature-list__item-name">{{ item.name }}</span>
        </div>
        } @empty {
        <div class="feature-list__empty">No items found</div>
        }
    </div>
</div>
```

**BEM Naming:** Block = component name, Element = `block__element`, Modifier = separate `--modifier` class.

## Component SCSS Standard

Always style both the **host element** and the **main wrapper class**:

```scss
@import '~assets/scss/variables';

// Host element -- makes Angular element a proper block container
my-component {
    display: flex;
    flex-direction: column;
}

// Main wrapper with full styling
.my-component {
    display: flex;
    flex-direction: column;
    width: 100%;
    flex-grow: 1;

    &__header {
        /* ... */
    }
    &__content {
        flex: 1;
        overflow-y: auto;
    }
}
```

## Pattern: List Component with Store

```typescript
@Component({
    selector: 'app-feature-list',
    templateUrl: './feature-list.component.html',
    styleUrls: ['./feature-list.component.scss'],
    providers: [FeatureListStore]
})
export class FeatureListComponent extends AppBaseVmStoreComponent<FeatureListState, FeatureListStore> implements OnInit {
    trackByItem = this.ngForTrackByItemProp<FeatureDto>('id');

    constructor(store: FeatureListStore) {
        super(store);
    }

    ngOnInit(): void {
        this.store.loadItems();
    }

    onRefresh(): void {
        this.reload();
    }

    onDelete(item: FeatureDto): void {
        this.store.deleteItem(item.id);
    }
}
```

```html
<app-loading-and-error-indicator [target]="this">
    @if (vm(); as vm) {
    <div class="feature-list">
        <div class="feature-list__header">
            <h1 class="feature-list__title">Features</h1>
            <button class="feature-list__btn --refresh" (click)="onRefresh()" [disabled]="isStateLoading()()">Refresh</button>
        </div>
        @for (item of vm.items; track trackByItem) {
        <div class="feature-list__item">
            <span class="feature-list__item-name">{{ item.name }}</span>
            <button class="feature-list__item-btn --delete" (click)="onDelete(item)">Delete</button>
        </div>
        } @empty {
        <div class="feature-list__empty">No items found</div>
        }
    </div>
    }
</app-loading-and-error-indicator>
```

## Pattern: Simple Component

```typescript
@Component({
    selector: 'app-feature-card',
    template: `
        <div class="feature-card" [class.--selected]="isSelected">
            <h3 class="feature-card__title">{{ feature.name }}</h3>
            <p class="feature-card__desc">{{ feature.description }}</p>
            @if (canEdit) {
                <button class="feature-card__btn --edit" (click)="onEdit.emit(feature)">Edit</button>
            }
        </div>
    `
})
export class FeatureCardComponent extends AppBaseComponent {
    @Input() feature!: FeatureDto;
    @Input() isSelected = false;
    @Output() onEdit = new EventEmitter<FeatureDto>();

    get canEdit(): boolean {
        return this.hasRole('Admin', 'Manager');
    }
}
```

## Key Platform APIs (Components)

```typescript
// Auto-cleanup subscription
this.data$.pipe(this.untilDestroyed()).subscribe();

// Track request state
observable.pipe(this.observerLoadingErrorState('requestKey'));

// Check states in template
isLoading$('requestKey')();
getErrorMsg$('requestKey')();
isStateLoading()();

// Response handling
observable.pipe(
    this.tapResponse(
        result => {
            /* success */
        },
        error => {
            /* error */
        }
    )
);

// Track-by for @for loops
trackByItem = this.ngForTrackByItemProp<Item>('id');
```

---

# Part 2: Forms

## Form Base Class Selection

| Base Class              | Use When                |
| ----------------------- | ----------------------- |
| `PlatformFormComponent` | Basic form without auth |
| `AppBaseFormComponent`  | Form with auth context  |

## Pattern: Basic Form

```typescript
export interface FeatureFormVm {
    id?: string;
    name: string;
    code: string;
    status: FeatureStatus;
    isActive: boolean;
}

@Component({
    selector: 'app-feature-form',
    templateUrl: './feature-form.component.html'
})
export class FeatureFormComponent extends AppBaseFormComponent<FeatureFormVm> {
    @Input() featureId?: string;

    protected initialFormConfig = () => ({
        controls: {
            name: new FormControl(this.currentVm().name, [Validators.required, Validators.maxLength(200), noWhitespaceValidator]),
            code: new FormControl(this.currentVm().code, [Validators.required, Validators.pattern(/^[A-Z0-9_-]+$/)]),
            status: new FormControl(this.currentVm().status, [Validators.required]),
            isActive: new FormControl(this.currentVm().isActive)
        }
    });

    protected initOrReloadVm = (isReload: boolean) => {
        if (!this.featureId) {
            return of<FeatureFormVm>({ name: '', code: '', status: FeatureStatus.Draft, isActive: true });
        }
        return this.featureApi.getById(this.featureId);
    };

    onSubmit(): void {
        if (!this.validateForm()) return;
        this.featureApi
            .save(this.currentVm())
            .pipe(
                this.observerLoadingErrorState('save'),
                this.tapResponse(
                    saved => this.onSuccess(saved),
                    error => this.onError(error)
                ),
                this.untilDestroyed()
            )
            .subscribe();
    }

    constructor(private featureApi: FeatureApiService) {
        super();
    }
}
```

## Pattern: Async Validation

```typescript
protected initialFormConfig = () => ({
    controls: {
        code: new FormControl(
            this.currentVm().code,
            [Validators.required, Validators.pattern(/^[A-Z0-9_-]+$/)],
            [ifAsyncValidator(ctrl => ctrl.valid, this.checkCodeUniqueValidator())]
        )
    }
});

private checkCodeUniqueValidator(): AsyncValidatorFn {
    return async (control: AbstractControl): Promise<ValidationErrors | null> => {
        if (!control.value) return null;
        const exists = await firstValueFrom(
            this.featureApi.checkCodeExists(control.value, this.currentVm().id).pipe(debounceTime(300))
        );
        return exists ? { codeExists: 'Code already exists' } : null;
    };
}
```

## Pattern: Dependent Validation

```typescript
protected initialFormConfig = () => ({
    controls: {
        startDate: new FormControl(this.currentVm().startDate, [Validators.required]),
        endDate: new FormControl(this.currentVm().endDate, [
            Validators.required,
            startEndValidator('invalidRange', ctrl => ctrl.parent?.get('startDate')?.value, ctrl => ctrl.value, { allowEqual: true })
        ])
    },
    dependentValidations: {
        endDate: ['startDate']  // Re-validate endDate when startDate changes
    }
});
```

## Pattern: FormArray

```typescript
protected initialFormConfig = () => ({
    controls: {
        name: new FormControl(this.currentVm().name, [Validators.required]),
        specifications: {
            modelItems: () => this.currentVm().specifications,
            itemControl: (spec: Specification) => new FormGroup({
                name: new FormControl(spec.name, [Validators.required]),
                value: new FormControl(spec.value, [Validators.required])
            })
        }
    }
});

get specificationsArray(): FormArray { return this.form.get('specifications') as FormArray; }

addSpecification(): void {
    this.updateVm(vm => ({ specifications: [...vm.specifications, { name: '', value: '' }] }));
    this.specificationsArray.push(new FormGroup({
        name: new FormControl('', [Validators.required]),
        value: new FormControl('', [Validators.required])
    }));
}

removeSpecification(index: number): void {
    this.updateVm(vm => ({ specifications: vm.specifications.filter((_, i) => i !== index) }));
    this.specificationsArray.removeAt(index);
}
```

## Form Template

```html
<form class="feature-form" [formGroup]="form" (ngSubmit)="onSubmit()">
    <div class="feature-form__field">
        <label class="feature-form__label" for="name">Name *</label>
        <input class="feature-form__input" id="name" formControlName="name" />
        @if (formControls('name').errors?.['required'] && formControls('name').touched) {
        <span class="feature-form__error">Name is required</span>
        }
    </div>
    <div class="feature-form__field">
        <label class="feature-form__label" for="code">Code *</label>
        <input class="feature-form__input" id="code" formControlName="code" />
        @if (formControls('code').pending) {
        <span class="feature-form__info">Checking availability...</span>
        } @if (formControls('code').errors?.['codeExists']) {
        <span class="feature-form__error">{{ formControls('code').errors?.['codeExists'] }}</span>
        }
    </div>
    <div class="feature-form__actions">
        <button class="feature-form__btn --cancel" type="button" (click)="onCancel()">Cancel</button>
        <button class="feature-form__btn --submit" type="submit" [disabled]="!form.valid || isLoading$('save')()">
            {{ isLoading$('save')() ? 'Saving...' : 'Save' }}
        </button>
    </div>
</form>
```

## Built-in Validators

| Validator               | Import                | Usage                    |
| ----------------------- | --------------------- | ------------------------ |
| `noWhitespaceValidator` | `@libs/platform-core` | No empty strings         |
| `startEndValidator`     | `@libs/platform-core` | Date/number range        |
| `ifAsyncValidator`      | `@libs/platform-core` | Conditional async        |
| `validator`             | `@libs/platform-core` | Custom validator factory |

## Key Form APIs

| Method              | Purpose                   | Example                             |
| ------------------- | ------------------------- | ----------------------------------- |
| `validateForm()`    | Validate and mark touched | `if (!this.validateForm()) return;` |
| `formControls(key)` | Get form control          | `this.formControls('name').errors`  |
| `currentVm()`       | Get current view model    | `const vm = this.currentVm()`       |
| `updateVm()`        | Update view model         | `this.updateVm({ name: 'new' })`    |
| `mode`              | Form mode                 | `this.mode === 'create'`            |
| `isViewMode()`      | Check view mode           | `if (this.isViewMode()) return;`    |

---

# Part 3: Stores (State Management)

## Store Architecture

```
PlatformVmStore<TState>
  State: TState (reactive signal)
  Selectors: select() -> Signal<T>
  Effects: effectSimple() -> side effects
  Updaters: updateState() -> mutations
  Loading/Error: observerLoadingErrorState()
```

## Pattern: Basic CRUD Store

```typescript
export interface FeatureListState {
    items: FeatureDto[];
    selectedItem?: FeatureDto;
    filters: FeatureFilters;
    pagination: PaginationState;
}

@Injectable()
export class FeatureListStore extends PlatformVmStore<FeatureListState> {
    protected override vmConstructor = (data?: Partial<FeatureListState>) =>
        ({ items: [], filters: {}, pagination: { pageIndex: 0, pageSize: 20, totalCount: 0 }, ...data }) as FeatureListState;

    // Selectors
    public readonly items$ = this.select(state => state.items);
    public readonly selectedItem$ = this.select(state => state.selectedItem);
    public readonly hasItems$ = this.select(state => state.items.length > 0);

    // Effects
    public loadItems = this.effectSimple(() => {
        const state = this.currentVm();
        return this.featureApi
            .getList({
                ...state.filters,
                skipCount: state.pagination.pageIndex * state.pagination.pageSize,
                maxResultCount: state.pagination.pageSize
            })
            .pipe(
                this.tapResponse(result => {
                    this.updateState({ items: result.items, pagination: { ...state.pagination, totalCount: result.totalCount } });
                })
            );
    }, 'loadItems');

    public saveItem = this.effectSimple(
        (item: FeatureDto) =>
            this.featureApi.save(item).pipe(
                this.tapResponse(saved => {
                    this.updateState(state => ({ items: state.items.upsertBy(x => x.id, [saved]), selectedItem: saved }));
                })
            ),
        'saveItem'
    );

    public deleteItem = this.effectSimple(
        (id: string) =>
            this.featureApi.delete(id).pipe(
                this.tapResponse(() => {
                    this.updateState(state => ({
                        items: state.items.filter(x => x.id !== id),
                        selectedItem: state.selectedItem?.id === id ? undefined : state.selectedItem
                    }));
                })
            ),
        'deleteItem'
    );

    // Updaters
    public setFilters(filters: Partial<FeatureFilters>): void {
        this.updateState(state => ({ filters: { ...state.filters, ...filters }, pagination: { ...state.pagination, pageIndex: 0 } }));
    }

    public setPage(pageIndex: number): void {
        this.updateState(state => ({ pagination: { ...state.pagination, pageIndex } }));
    }

    constructor(private featureApi: FeatureApiService) {
        super();
    }
}
```

## Pattern: Store with Dependent Data

```typescript
@Injectable()
export class EmployeeFormStore extends PlatformVmStore<EmployeeFormState> {
    public loadFormData = this.effectSimple(
        (employeeId?: string) =>
            forkJoin({
                employee: employeeId ? this.employeeApi.getById(employeeId) : of(this.createNewEmployee()),
                departments: this.departmentApi.getActive(),
                positions: this.positionApi.getAll()
            }).pipe(this.tapResponse(result => this.updateState(result))),
        'loadFormData'
    );
}
```

## Pattern: Store with Caching

```typescript
@Injectable({ providedIn: 'root' }) // Singleton for caching
export class LookupDataStore extends PlatformVmStore<LookupDataState> {
    protected override get enableCaching() {
        return true;
    }
    protected override cachedStateKeyName = () => 'LookupDataStore';
    protected override get cacheExpirationMs() {
        return 5 * 60 * 1000;
    }

    public loadCountries = this.effectSimple(() => {
        if (this.currentVm().countries.length > 0) return EMPTY;
        return this.lookupApi.getCountries().pipe(this.tapResponse(countries => this.updateState({ countries })));
    }, 'loadCountries');
}
```

## Key Store APIs

| Method                        | Purpose              | Example                                             |
| ----------------------------- | -------------------- | --------------------------------------------------- |
| `select()`                    | Create selector      | `this.select(s => s.items)`                         |
| `updateState()`               | Update state         | `this.updateState({ items })`                       |
| `effectSimple()`              | Create effect        | `this.effectSimple(() => api.call(), 'requestKey')` |
| `currentVm()`                 | Get current state    | `const state = this.currentVm()`                    |
| `observerLoadingErrorState()` | Track loading/error  | Use outside effectSimple only                       |
| `tapResponse()`               | Handle success/error | `.pipe(this.tapResponse(success, error))`           |
| `isLoading$()`                | Loading signal       | `this.store.isLoading$('loadItems')`                |

---

# Part 4: API Services

## Pattern: Basic CRUD API Service

```typescript
@Injectable({ providedIn: 'root' })
export class FeatureApiService extends PlatformApiService {
    protected get apiUrl(): string {
        return environment.apiUrl + '/api/Feature';
    }

    getList(query?: FeatureListQuery): Observable<PagedResult<FeatureDto>> {
        return this.get<PagedResult<FeatureDto>>('', query);
    }

    getById(id: string): Observable<FeatureDto> {
        return this.get<FeatureDto>(`/${id}`);
    }

    save(command: SaveFeatureCommand): Observable<FeatureDto> {
        return this.post<FeatureDto>('', command);
    }

    update(id: string, command: Partial<SaveFeatureCommand>): Observable<FeatureDto> {
        return this.put<FeatureDto>(`/${id}`, command);
    }

    delete(id: string): Observable<void> {
        return this.deleteRequest<void>(`/${id}`);
    }

    checkCodeExists(code: string, excludeId?: string): Observable<boolean> {
        return this.get<boolean>('/check-code-exists', { code, excludeId });
    }
}
```

## Pattern: API Service with Caching

```typescript
@Injectable({ providedIn: 'root' })
export class LookupApiService extends PlatformApiService {
    protected get apiUrl(): string {
        return environment.apiUrl + '/api/Lookup';
    }

    getCountries(): Observable<CountryDto[]> {
        return this.get<CountryDto[]>('/countries', null, { enableCache: true, cacheKey: 'countries', cacheDurationMs: 60 * 60 * 1000 });
    }

    invalidateCountriesCache(): void {
        this.clearCache('countries');
    }
    invalidateAllCache(): void {
        this.clearAllCache();
    }
}
```

## Pattern: File Upload/Download

```typescript
@Injectable({ providedIn: 'root' })
export class DocumentApiService extends PlatformApiService {
    protected get apiUrl(): string {
        return environment.apiUrl + '/api/Document';
    }

    upload(file: File, metadata?: DocumentMetadata): Observable<DocumentDto> {
        const formData = new FormData();
        formData.append('file', file, file.name);
        if (metadata) formData.append('metadata', JSON.stringify(metadata));
        return this.postFormData<DocumentDto>('/upload', formData);
    }

    download(id: string): Observable<Blob> {
        return this.getBlob(`/${id}/download`);
    }

    downloadAndSave(id: string, fileName: string): Observable<void> {
        return this.download(id).pipe(
            tap(blob => {
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.download = fileName;
                link.click();
                window.URL.revokeObjectURL(url);
            }),
            map(() => void 0)
        );
    }
}
```

## Pattern: Search/Autocomplete API

```typescript
@Injectable({ providedIn: 'root' })
export class EmployeeApiService extends PlatformApiService {
    protected get apiUrl(): string {
        return environment.apiUrl + '/api/Employee';
    }

    search(term: string): Observable<EmployeeDto[]> {
        if (!term || term.length < 2) return of([]);
        return this.get<EmployeeDto[]>('/search', { searchText: term, maxResultCount: 10 });
    }

    autocomplete(prefix: string): Observable<AutocompleteItem[]> {
        return this.get<AutocompleteItem[]>(
            '/autocomplete',
            { prefix },
            {
                enableCache: true,
                cacheKey: `autocomplete-${prefix}`,
                cacheDurationMs: 30 * 1000
            }
        );
    }
}
```

## Base PlatformApiService Methods

| Method               | Purpose              | Example                                  |
| -------------------- | -------------------- | ---------------------------------------- |
| `get<T>()`           | GET request          | `this.get<User>('/users/1')`             |
| `post<T>()`          | POST request         | `this.post<User>('/users', data)`        |
| `put<T>()`           | PUT request          | `this.put<User>('/users/1', data)`       |
| `patch<T>()`         | PATCH request        | `this.patch<User>('/users/1', partial)`  |
| `deleteRequest<T>()` | DELETE request       | `this.deleteRequest('/users/1')`         |
| `postFormData<T>()`  | POST with FormData   | `this.postFormData('/upload', formData)` |
| `getBlob()`          | GET binary data      | `this.getBlob('/file/download')`         |
| `clearCache()`       | Clear specific cache | `this.clearCache('cacheKey')`            |
| `clearAllCache()`    | Clear all cache      | `this.clearAllCache()`                   |

## Request Options

```typescript
interface RequestOptions {
    enableCache?: boolean;
    cacheKey?: string;
    cacheDurationMs?: number;
    headers?: { [key: string]: string };
    responseType?: 'json' | 'text' | 'blob' | 'arraybuffer';
    reportProgress?: boolean;
    observe?: 'body' | 'events' | 'response';
}
```

---

# Anti-Patterns to AVOID

**Wrong base class:**

```typescript
// BAD: using PlatformComponent when auth needed
export class MyComponent extends PlatformComponent {}
// GOOD:
export class MyComponent extends AppBaseComponent {}
```

**Manual subscription management:**

```typescript
// BAD
private sub: Subscription;
ngOnDestroy() { this.sub.unsubscribe(); }
// GOOD
this.data$.pipe(this.untilDestroyed()).subscribe();
```

**Direct HTTP calls:**

```typescript
// BAD
constructor(private http: HttpClient) { }
// GOOD
constructor(private featureApi: FeatureApiService) { }
```

**Missing loading states:**

```html
<!-- BAD -->
<div>{{ items }}</div>
<!-- GOOD -->
<app-loading-and-error-indicator [target]="this">
    <div>{{ items }}</div>
</app-loading-and-error-indicator>
```

**Not using validateForm():**

```typescript
// BAD
onSubmit() { this.api.save(this.currentVm()); }
// GOOD
onSubmit() { if (!this.validateForm()) return; this.api.save(this.currentVm()); }
```

**Async validator always runs:**

```typescript
// BAD
new FormControl('', [], [asyncValidator]);
// GOOD
new FormControl('', [], [ifAsyncValidator(ctrl => ctrl.valid, asyncValidator)]);
```

**Mutating state directly:**

```typescript
// BAD
this.currentVm().items.push(newItem);
// GOOD
this.updateState(state => ({ items: [...state.items, newItem] }));
```

**Missing BEM classes:**

```html
<!-- BAD -->
<div><label>Name</label><input formControlName="name" /></div>
<!-- GOOD -->
<div class="form__field"><label class="form__label">Name</label><input class="form__input" formControlName="name" /></div>
```

---

# Verification Checklist

## Components

- [ ] Correct base class selected for use case
- [ ] Store provided at component level (if using store)
- [ ] Loading/error states handled with `app-loading-and-error-indicator`
- [ ] Subscriptions use `untilDestroyed()`
- [ ] Track-by functions used in `@for` loops
- [ ] Auth checks use `hasRole()` from base class
- [ ] API calls use service extending `PlatformApiService`

## Forms

- [ ] `initialFormConfig` returns form configuration
- [ ] `initOrReloadVm` loads data for edit mode
- [ ] `validateForm()` called before submit
- [ ] Async validators use `ifAsyncValidator`
- [ ] `dependentValidations` configured for cross-field validation
- [ ] Error messages displayed for all validation rules

## Stores

- [ ] State interface defines all required properties
- [ ] `vmConstructor` provides default state
- [ ] Effects use `effectSimple()` with request key
- [ ] Effects use `tapResponse()` for handling
- [ ] Selectors memoized with `select()`
- [ ] State updates are immutable
- [ ] Store provided at correct level (component vs root)

## API Services

- [ ] Extends `PlatformApiService`
- [ ] `apiUrl` getter returns correct base URL
- [ ] All methods have return type annotations
- [ ] DTOs defined for request/response
- [ ] `@Injectable({ providedIn: 'root' })` for singleton
