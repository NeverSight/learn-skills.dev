---
name: compose-arch
description: Compose Multiplatform Architecture Framework - strict Screen/View/Component layering, use cases, repositories, and feature slice patterns
---

# Compose Multiplatform Architecture Framework

Strict architectural patterns for building Compose Multiplatform features using feature slices. Enforces separation of concerns through Screen/View/Component layering.

## Core Principles

### Layer Separation (STRICT)

| Layer | Responsibility | Rules |
|-------|----------------|-------|
| **Screen** | Thin adapter | Reads viewState, passes to View. NO logic, NO remember, NO calculations |
| **View** | Pure UI | Only layout, only viewState, only eventHandler. NO side effects |
| **Component** | All logic | State, events, use cases, lifecycle. Uses Decompose |
| **Domain** | Business | Use cases, repositories, data sources |

## Screen Layer

**File**: `<FeatureName>Screen.kt`

```kotlin
@Composable
fun FeatureScreen(component: FeatureComponent) {
    val viewState by component.viewState.subscribeAsState()
    FeatureView(viewState, component::obtainEvent)
}
```

### Screen Rules
- **Maximum**: 1000 lines (hard limit)
- **Recommended**: Under 600 lines
- **Forbidden**:
  - Business logic
  - Navigation logic
  - State management
  - `remember` calls
  - Calculations

## View Layer

**File**: `<FeatureName>View.kt`

```kotlin
@Composable
fun FeatureView(
    viewState: FeatureViewState,
    eventHandler: (FeatureEvent) -> Unit
) {
    // Only layout and viewState rendering
    Column(modifier = Modifier.fillMaxSize()) {
        when (viewState) {
            is FeatureViewState.Loading -> LoadingContent()
            is FeatureViewState.Success -> SuccessContent(
                data = viewState.data,
                onItemClick = { eventHandler(FeatureEvent.ItemClicked(it)) }
            )
            is FeatureViewState.Error -> ErrorContent(
                message = viewState.message,
                onRetry = { eventHandler(FeatureEvent.Retry) }
            )
        }
    }
}
```

### View Rules
- Only layout code
- Only work with viewState
- Only call eventHandler
- **NO** logic
- **NO** remember
- **NO** side effects
- **NO** previews in production code

### UI Guidelines
- Maximum nesting depth: **3 levels**
- Spacing: multiples of **8/16/24** dp
- Use theme: `AppTheme.colors`, `AppTheme.typography`
- Use theme icons consistently
- Extract to `common/ui/` if used in **5+ places**

## Component Layer

**File**: `<FeatureName>Component.kt`

```kotlin
interface FeatureComponent {
    val viewState: Value<FeatureViewState>
    fun obtainEvent(event: FeatureEvent)
}

@Inject
class DefaultFeatureComponent(
    private val getDataUseCase: GetDataUseCase,
    @Assisted componentContext: ComponentContext,
    @Assisted private val onNavigate: (String) -> Unit
) : FeatureComponent, ComponentContext by componentContext {

    private val _viewState = MutableValue<FeatureViewState>(FeatureViewState.Loading)
    override val viewState: Value<FeatureViewState> = _viewState

    private val scope = componentScope()

    init { loadData() }

    override fun obtainEvent(event: FeatureEvent) {
        when (event) {
            is FeatureEvent.ItemClicked -> onNavigate(event.itemId)
            is FeatureEvent.Retry -> loadData()
        }
    }

    private fun loadData() {
        scope.launch {
            _viewState.value = FeatureViewState.Loading
            getDataUseCase.execute()
                .onSuccess { _viewState.value = FeatureViewState.Success(it) }
                .onError { msg, _ -> _viewState.value = FeatureViewState.Error(msg) }
        }
    }

    @AssistedFactory
    interface Factory : FeatureComponent.Factory
}
```

### Component Rules
- **Single source of logic**
- Stores state (`Value<T>` from Decompose)
- Handles all events
- Executes use cases
- Manages lifecycle
- Navigation **ONLY** through Decompose:
  - `StackNavigation` / `childStack`
  - `SlotNavigation` / `childSlot`

### Component Dependencies
Allowed:
- Use cases
- Repositories (indirectly via use cases)
- Platform drivers (via DI)

Forbidden:
- Direct data source access
- UI imports (Compose)

## Use Case Layer

**File**: `<FeatureName><Action>UseCase.kt`

```kotlin
@Inject
class GetFeatureDataUseCase(
    private val repository: FeatureRepository
) {
    suspend fun execute(params: Params): Result<FeatureData> {
        return try {
            val data = repository.getData(params.id)
            Result.success(data)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
```

### Use Case Rules
- **One class per file**
- Returns only `Result<T>`
- Single `execute(params): Result<T>` function
- **NOT** an operator function
- All error handling happens here
- Dependencies:
  - Repository
  - TokenManager (if needed)
  - Platform drivers (if needed)
  - Other UseCases (rarely, for reuse)

## Repository Layer

**File**: `<FeatureName>Repository.kt`

```kotlin
@Inject
class FeatureRepository(
    private val localDataSource: FeatureLocalDataSource,
    private val remoteDataSource: FeatureRemoteDataSource
) {
    suspend fun getData(id: String): FeatureData {
        return try {
            remoteDataSource.fetch(id)
        } catch (e: Exception) {
            localDataSource.get(id) ?: throw e
        }
    }

    suspend fun saveData(data: FeatureData) {
        localDataSource.save(data)
        remoteDataSource.sync(data)
    }
}
```

### Repository Rules
- **Concrete class** (no interfaces needed for internal repos)
- Dependencies: only DataSources
- Returns clean data
- Coordinates local/remote sources

## DataSource Layer

**Files**:
- `<FeatureName>LocalDataSource.kt`
- `<FeatureName>RemoteDataSource.kt`

```kotlin
@Inject
class FeatureLocalDataSource(
    private val database: AppDatabase
) {
    suspend fun get(id: String): FeatureData? {
        return database.featureDao().getById(id)?.toDomain()
    }

    suspend fun save(data: FeatureData) {
        database.featureDao().insert(data.toEntity())
    }
}

@Inject
class FeatureRemoteDataSource(
    private val apiClient: ApiClient
) {
    suspend fun fetch(id: String): FeatureData {
        return apiClient.get("/features/$id").body<FeatureDto>().toDomain()
    }
}
```

### DataSource Rules
- Simple provider pattern
- Dependencies:
  - Local storage (Room, DataStore)
  - Platform APIs
  - Network client (Ktor)

## ViewState and Events

**File**: `<FeatureName>ViewState.kt`

```kotlin
sealed class FeatureViewState {
    data object Loading : FeatureViewState()
    data class Success(val data: List<FeatureItem>) : FeatureViewState()
    data class Error(val message: String) : FeatureViewState()
}
```

**File**: `<FeatureName>ViewEvent.kt`

```kotlin
sealed class FeatureEvent {
    data class ItemClicked(val itemId: String) : FeatureEvent()
    data object Retry : FeatureEvent()
    data object BackPressed : FeatureEvent()
}
```

## File Rules (HARD)

**One class per file**:
- Screen → separate file
- View → separate file
- ViewState → separate file
- ViewEvent → separate file
- Component → separate file
- UseCase → separate file (each)
- Repository → separate file
- DataSource → separate file (each)

**NO god files** - split immediately if file grows beyond responsibility.

## Feature Directory Structure

```
feature/<featureName>/
├── api/                          # Public interfaces
│   └── src/commonMain/kotlin/
│       ├── <Name>Component.kt    # Interface only
│       ├── <Name>Models.kt       # Domain models
│       └── <Name>Repository.kt   # Interface (if public)
│
└── impl/                         # Implementation
    └── src/commonMain/kotlin/
        ├── screen/
        │   └── <Name>Screen.kt
        ├── view/
        │   ├── <Name>View.kt
        │   ├── <Name>ViewState.kt
        │   └── <Name>ViewEvent.kt
        ├── component/
        │   └── Default<Name>Component.kt
        ├── domain/
        │   ├── usecase/
        │   │   ├── Get<Name>UseCase.kt
        │   │   └── Update<Name>UseCase.kt
        │   └── repository/
        │       └── <Name>Repository.kt
        ├── data/
        │   └── datasource/
        │       ├── <Name>LocalDataSource.kt
        │       └── <Name>RemoteDataSource.kt
        └── di/
            └── <Name>Module.kt
```

## DI Module

**File**: `<FeatureName>Module.kt`

```kotlin
@BindingContainer
class FeatureModule {
    @Provides
    fun provideFeatureRepository(
        localDataSource: FeatureLocalDataSource,
        remoteDataSource: FeatureRemoteDataSource
    ): FeatureRepository = FeatureRepository(localDataSource, remoteDataSource)
}
```

## Code Rules

| Rule | Details |
|------|---------|
| Serialization | Only Kotlinx Serialization |
| JSON | Single instance via DI |
| Repository return | Clean domain data |
| UseCase return | Always `Result<T>` (or `Result<Flow<T>>`) |
| Error handling | All in UseCase (where Result is created) |
| State | Never use `remember` in View - state from Component |

## Common Components

Extract to `common/ui/<ComponentName>.kt` when:
- Used in **5+ locations**
- Generic enough for reuse
- No feature-specific logic

```kotlin
// common/ui/LoadingButton.kt
@Composable
fun LoadingButton(
    text: String,
    loading: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Button(
        onClick = onClick,
        enabled = !loading,
        modifier = modifier
    ) {
        if (loading) {
            CircularProgressIndicator(
                modifier = Modifier.size(16.dp),
                strokeWidth = 2.dp
            )
        } else {
            Text(text)
        }
    }
}
```

## Validation Checklist

Before completing a feature, verify:

- [ ] Screen has no business logic
- [ ] View has no remember/side effects
- [ ] Component handles all logic
- [ ] All navigation in Component via Decompose
- [ ] UseCases return Result<T>
- [ ] One class per file
- [ ] No god files
- [ ] UI nesting <= 3 levels
- [ ] Spacing uses 8/16/24 multiples
- [ ] Common components extracted if 5+ uses

## Anti-Patterns to Avoid

| Anti-Pattern | Correct Pattern |
|--------------|-----------------|
| Logic in Screen | Move to Component |
| remember in View | State from Component |
| Direct API calls in Component | Use UseCase |
| UseCase calling DataSource | Use Repository |
| God file with multiple classes | Split to separate files |
| Deep nesting (4+ levels) | Extract sub-components |
| Hardcoded colors/dimensions | Use theme |

## Resources

- [Decompose Documentation](https://arkivanov.github.io/Decompose/)
- [Compose Multiplatform](https://www.jetbrains.com/compose-multiplatform/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
