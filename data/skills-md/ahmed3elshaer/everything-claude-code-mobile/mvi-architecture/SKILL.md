---
name: mvi-architecture
description: Model-View-Intent architecture patterns for Android with unidirectional data flow, state management, and side effects.
---

# MVI Architecture

Unidirectional data flow architecture for Android.

## Core Concepts

```
Intent → ViewModel → State → UI
   ↑                        │
   └────────────────────────┘
```

## State

```kotlin
@Immutable
data class HomeState(
    val isLoading: Boolean = false,
    val items: List<Item> = emptyList(),
    val error: ErrorState? = null,
    val searchQuery: String = ""
) {
    sealed interface ErrorState {
        data class Network(val message: String) : ErrorState
        data object Unauthorized : ErrorState
    }
}
```

## Intent

```kotlin
sealed interface HomeIntent {
    object LoadItems : HomeIntent
    object Refresh : HomeIntent
    data class Search(val query: String) : HomeIntent
    data class ItemClicked(val id: String) : HomeIntent
    object ClearError : HomeIntent
}
```

## Side Effects

```kotlin
sealed interface HomeSideEffect {
    data class NavigateToDetail(val itemId: String) : HomeSideEffect
    data class ShowSnackbar(val message: String) : HomeSideEffect
    object NavigateToLogin : HomeSideEffect
}
```

## ViewModel

```kotlin
class HomeViewModel(
    private val getItemsUseCase: GetItemsUseCase
) : ViewModel() {

    private val _state = MutableStateFlow(HomeState())
    val state: StateFlow<HomeState> = _state.asStateFlow()

    private val _sideEffects = Channel<HomeSideEffect>(Channel.BUFFERED)
    val sideEffects: Flow<HomeSideEffect> = _sideEffects.receiveAsFlow()

    fun onIntent(intent: HomeIntent) {
        when (intent) {
            is HomeIntent.LoadItems -> loadItems()
            is HomeIntent.Refresh -> loadItems(refresh = true)
            is HomeIntent.Search -> search(intent.query)
            is HomeIntent.ItemClicked -> {
                viewModelScope.launch {
                    _sideEffects.send(HomeSideEffect.NavigateToDetail(intent.id))
                }
            }
            is HomeIntent.ClearError -> _state.update { it.copy(error = null) }
        }
    }

    private fun loadItems(refresh: Boolean = false) {
        viewModelScope.launch {
            if (!refresh) _state.update { it.copy(isLoading = true) }
            
            getItemsUseCase()
                .onSuccess { items ->
                    _state.update { it.copy(isLoading = false, items = items, error = null) }
                }
                .onFailure { error ->
                    _state.update { it.copy(isLoading = false, error = mapError(error)) }
                }
        }
    }
    
    private fun mapError(error: Throwable): HomeState.ErrorState {
        return when (error) {
            is UnauthorizedException -> HomeState.ErrorState.Unauthorized
            else -> HomeState.ErrorState.Network(error.message ?: "Unknown error")
        }
    }
}
```

## UI Integration

```kotlin
@Composable
fun HomeScreen(
    viewModel: HomeViewModel = koinViewModel(),
    onNavigateToDetail: (String) -> Unit,
    onNavigateToLogin: () -> Unit
) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    val snackbarHostState = remember { SnackbarHostState() }
    
    // Handle side effects
    LaunchedEffect(Unit) {
        viewModel.sideEffects.collect { effect ->
            when (effect) {
                is HomeSideEffect.NavigateToDetail -> onNavigateToDetail(effect.itemId)
                is HomeSideEffect.ShowSnackbar -> snackbarHostState.showSnackbar(effect.message)
                is HomeSideEffect.NavigateToLogin -> onNavigateToLogin()
            }
        }
    }
    
    // Load data
    LaunchedEffect(Unit) {
        viewModel.onIntent(HomeIntent.LoadItems)
    }
    
    HomeContent(
        state = state,
        onIntent = viewModel::onIntent,
        snackbarHostState = snackbarHostState
    )
}

@Composable
private fun HomeContent(
    state: HomeState,
    onIntent: (HomeIntent) -> Unit,
    snackbarHostState: SnackbarHostState
) {
    Scaffold(
        snackbarHost = { SnackbarHost(snackbarHostState) }
    ) { padding ->
        when {
            state.isLoading -> LoadingIndicator()
            state.error != null -> ErrorContent(
                error = state.error,
                onRetry = { onIntent(HomeIntent.LoadItems) }
            )
            else -> ItemList(
                items = state.items,
                onItemClick = { onIntent(HomeIntent.ItemClicked(it)) }
            )
        }
    }
}
```

## Testing

```kotlin
@Test
fun `when LoadItems succeeds, state contains items`() = runTest {
    val items = listOf(Item("1", "Test"))
    coEvery { getItemsUseCase() } returns Result.success(items)
    
    viewModel.state.test {
        awaitItem() // Initial
        
        viewModel.onIntent(HomeIntent.LoadItems)
        
        awaitItem().isLoading shouldBe true
        awaitItem().items shouldBe items
    }
}
```

---

**Remember**: MVI = predictable state, testable logic, debuggable flow.
