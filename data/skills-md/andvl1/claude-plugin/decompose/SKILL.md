---
name: decompose
description: Decompose navigation and components - use for KMP component architecture, navigation, lifecycle, and state management
---

# Decompose for Kotlin Multiplatform

Component-based architecture with lifecycle management and navigation for KMP.

## Setup

### libs.versions.toml

```toml
[versions]
decompose = "3.5.0"
essenty = "2.5.0"

[libraries]
decompose = { module = "com.arkivanov.decompose:decompose", version.ref = "decompose" }
decompose-compose = { module = "com.arkivanov.decompose:extensions-compose", version.ref = "decompose" }
essenty-lifecycle = { module = "com.arkivanov.essenty:lifecycle", version.ref = "essenty" }
```

### build.gradle.kts

```kotlin
commonMain.dependencies {
    implementation(libs.decompose)
    implementation(libs.decompose.compose)
    implementation(libs.essenty.lifecycle)
    implementation(libs.kotlinx.serialization.json)
}
```

## Core Concepts

### Component

Business logic container with lifecycle. UI-agnostic.

```kotlin
// Interface (public API)
interface HomeComponent {
    val state: Value<HomeState>
    fun onItemClick(item: HomeItem)
    fun onRefresh()
}

// Implementation
class DefaultHomeComponent(
    componentContext: ComponentContext,
    private val repository: HomeRepository,
    private val onNavigateToDetails: (itemId: String) -> Unit
) : HomeComponent, ComponentContext by componentContext {

    private val _state = MutableValue<HomeState>(HomeState.Loading)
    override val state: Value<HomeState> = _state

    private val scope = componentScope()

    init {
        loadData()
    }

    private fun loadData() {
        scope.launch {
            _state.value = HomeState.Loading
            repository.getItems()
                .onSuccess { items ->
                    _state.value = HomeState.Success(items)
                }
                .onError { message, _ ->
                    _state.value = HomeState.Error(message)
                }
        }
    }

    override fun onItemClick(item: HomeItem) {
        onNavigateToDetails(item.id)
    }

    override fun onRefresh() {
        loadData()
    }
}

sealed class HomeState {
    data object Loading : HomeState()
    data class Success(val items: List<HomeItem>) : HomeState()
    data class Error(val message: String) : HomeState()
}
```

### ComponentContext

Provides lifecycle, state preservation, and child management.

```kotlin
class MyComponent(
    componentContext: ComponentContext
) : ComponentContext by componentContext {

    // Access lifecycle
    init {
        lifecycle.subscribe(
            onCreate = { println("Created") },
            onStart = { println("Started") },
            onResume = { println("Resumed") },
            onPause = { println("Paused") },
            onStop = { println("Stopped") },
            onDestroy = { println("Destroyed") }
        )
    }

    // Retain instances across config changes (Android)
    private val viewModel = instanceKeeper.getOrCreate { MyViewModel() }

    // Preserve state during process death
    private var counter: Int by savedState("counter", 0)

    // Create coroutine scope tied to lifecycle
    private val scope = componentScope()
}

// Helper extension - place in core/common module
import com.arkivanov.essenty.lifecycle.doOnDestroy
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancel

fun ComponentContext.componentScope(): CoroutineScope {
    val scope = CoroutineScope(Dispatchers.Main.immediate + SupervisorJob())
    lifecycle.doOnDestroy { scope.cancel() }
    return scope
}
```

## Navigation

### Child Stack (Primary Navigation)

Stack-based navigation like a navigation controller.

```kotlin
interface RootComponent {
    val childStack: Value<ChildStack<Config, Child>>

    sealed class Child {
        data class Home(val component: HomeComponent) : Child()
        data class Details(val component: DetailsComponent) : Child()
        data class Settings(val component: SettingsComponent) : Child()
    }

    @Serializable
    sealed class Config {
        @Serializable data object Home : Config()
        @Serializable data class Details(val itemId: String) : Config()
        @Serializable data object Settings : Config()
    }
}

class DefaultRootComponent(
    componentContext: ComponentContext,
    private val homeComponentFactory: HomeComponent.Factory,
    private val detailsComponentFactory: DetailsComponent.Factory,
    private val settingsComponentFactory: SettingsComponent.Factory
) : RootComponent, ComponentContext by componentContext {

    private val navigation = StackNavigation<RootComponent.Config>()

    override val childStack: Value<ChildStack<RootComponent.Config, RootComponent.Child>> =
        childStack(
            source = navigation,
            serializer = RootComponent.Config.serializer(),
            initialConfiguration = RootComponent.Config.Home,
            handleBackButton = true,  // Auto handle back
            childFactory = ::createChild
        )

    private fun createChild(
        config: RootComponent.Config,
        context: ComponentContext
    ): RootComponent.Child = when (config) {
        RootComponent.Config.Home -> RootComponent.Child.Home(
            homeComponentFactory.create(
                componentContext = context,
                onNavigateToDetails = { itemId ->
                    navigation.push(RootComponent.Config.Details(itemId))
                }
            )
        )
        is RootComponent.Config.Details -> RootComponent.Child.Details(
            detailsComponentFactory.create(
                componentContext = context,
                itemId = config.itemId,
                onBack = { navigation.pop() }
            )
        )
        RootComponent.Config.Settings -> RootComponent.Child.Settings(
            settingsComponentFactory.create(context)
        )
    }

    // Public navigation methods
    fun navigateToSettings() {
        navigation.push(RootComponent.Config.Settings)
    }
}
```

### Child Slot (Modals/Dialogs)

Single optional active child.

```kotlin
interface HomeComponent {
    val dialogSlot: Value<ChildSlot<DialogConfig, DialogChild>>
    fun showConfirmDialog(itemId: String)
    fun dismissDialog()
}

@Serializable
sealed class DialogConfig {
    @Serializable data class Confirm(val itemId: String) : DialogConfig()
    @Serializable data class Edit(val item: HomeItem) : DialogConfig()
}

sealed class DialogChild {
    data class Confirm(val component: ConfirmDialogComponent) : DialogChild()
    data class Edit(val component: EditDialogComponent) : DialogChild()
}

class DefaultHomeComponent(
    componentContext: ComponentContext
) : HomeComponent, ComponentContext by componentContext {

    private val dialogNavigation = SlotNavigation<DialogConfig>()

    override val dialogSlot: Value<ChildSlot<DialogConfig, DialogChild>> =
        childSlot(
            source = dialogNavigation,
            serializer = DialogConfig.serializer(),
            childFactory = ::createDialog
        )

    private fun createDialog(
        config: DialogConfig,
        context: ComponentContext
    ): DialogChild = when (config) {
        is DialogConfig.Confirm -> DialogChild.Confirm(
            ConfirmDialogComponent(
                context = context,
                itemId = config.itemId,
                onConfirm = { deleteItem(config.itemId); dismissDialog() },
                onDismiss = ::dismissDialog
            )
        )
        is DialogConfig.Edit -> DialogChild.Edit(
            EditDialogComponent(context, config.item)
        )
    }

    override fun showConfirmDialog(itemId: String) {
        dialogNavigation.activate(DialogConfig.Confirm(itemId))
    }

    override fun dismissDialog() {
        dialogNavigation.dismiss()
    }
}
```

### Navigation Operations

```kotlin
// Stack operations
navigation.push(Config.Details(itemId))           // Add to stack
navigation.pop()                                   // Go back
navigation.pop { config -> config is Config.Home } // Pop to specific
navigation.replaceAll(Config.Home)                 // Clear and replace
navigation.replaceCurrent(Config.Other)            // Replace top

// Slot operations
dialogNavigation.activate(DialogConfig.Confirm(id)) // Show
dialogNavigation.dismiss()                          // Hide
```

## Compose Integration

### Observing State

```kotlin
@Composable
fun HomeScreen(component: HomeComponent) {
    val state by component.state.subscribeAsState()

    when (val currentState = state) {
        is HomeState.Loading -> LoadingIndicator()
        is HomeState.Error -> ErrorContent(
            message = currentState.message,
            onRetry = component::onRefresh
        )
        is HomeState.Success -> HomeContent(
            items = currentState.items,
            onItemClick = component::onItemClick
        )
    }
}
```

### Rendering Child Stack

```kotlin
@Composable
fun RootContent(component: RootComponent) {
    val childStack by component.childStack.subscribeAsState()

    Children(
        stack = childStack,
        modifier = Modifier.fillMaxSize(),
        animation = stackAnimation(fade() + slide())
    ) { child ->
        when (val instance = child.instance) {
            is RootComponent.Child.Home -> HomeScreen(instance.component)
            is RootComponent.Child.Details -> DetailsScreen(instance.component)
            is RootComponent.Child.Settings -> SettingsScreen(instance.component)
        }
    }
}

// Animation options
val animation = stackAnimation(
    fade(),                    // Fade in/out
    slide(),                   // Slide horizontal
    scale(),                   // Scale
    fade() + slide(),          // Combined
    slide(SlideAnimation.Top)  // Slide from top
)
```

### Rendering Child Slot (Dialog)

```kotlin
@Composable
fun HomeScreen(component: HomeComponent) {
    val state by component.state.subscribeAsState()
    val dialogSlot by component.dialogSlot.subscribeAsState()

    Scaffold { paddingValues ->
        // Main content
        HomeContent(
            modifier = Modifier.padding(paddingValues),
            state = state,
            onItemLongClick = { component.showConfirmDialog(it.id) }
        )

        // Dialog overlay
        dialogSlot.child?.instance?.let { dialogChild ->
            when (dialogChild) {
                is DialogChild.Confirm -> ConfirmDialog(dialogChild.component)
                is DialogChild.Edit -> EditDialog(dialogChild.component)
            }
        }
    }
}

@Composable
private fun ConfirmDialog(component: ConfirmDialogComponent) {
    AlertDialog(
        onDismissRequest = component::onDismiss,
        title = { Text("Delete Item?") },
        text = { Text("This action cannot be undone.") },
        confirmButton = {
            TextButton(onClick = component::onConfirm) {
                Text("Delete")
            }
        },
        dismissButton = {
            TextButton(onClick = component::onDismiss) {
                Text("Cancel")
            }
        }
    )
}
```

## State Preservation

### InstanceKeeper (Config Changes)

Survives configuration changes on Android. Does NOT survive process death.

```kotlin
class MyComponent(componentContext: ComponentContext) : ComponentContext by componentContext {

    // Approach 1: Manual
    private val viewModel = instanceKeeper.getOrCreate("viewModel") {
        MyViewModel()
    }

    // Approach 2: Extension
    private val viewModel by retainedInstance { MyViewModel() }

    class MyViewModel : InstanceKeeper.Instance {
        val state = MutableStateFlow<UiState>(UiState.Initial)

        override fun onDestroy() {
            // Cleanup when component truly destroyed
        }
    }
}
```

### StateKeeper (Process Death)

Survives process death. Data must be serializable.

```kotlin
class MyComponent(componentContext: ComponentContext) : ComponentContext by componentContext {

    // Approach 1: Delegate property
    private var searchQuery: String by savedState("searchQuery", "")
    private var selectedTab: Int by savedState("selectedTab", 0)

    // Approach 2: Complex state
    @Serializable
    data class SavedState(
        val query: String = "",
        val filters: List<Filter> = emptyList(),
        val scrollPosition: Int = 0
    )

    private var savedState: SavedState by savedState("state", SavedState())

    // Approach 3: Manual
    init {
        stateKeeper.register("manualState") {
            SavedState(query = currentQuery, filters = currentFilters)
        }

        stateKeeper.consume<SavedState>("manualState")?.let { restored ->
            currentQuery = restored.query
            currentFilters = restored.filters
        }
    }
}
```

## Component Hierarchy Pattern

### Feature Module Structure

```
feature/home/impl/src/commonMain/kotlin/
├── HomeComponent.kt          # Interface
├── DefaultHomeComponent.kt   # Implementation
├── HomeState.kt              # State sealed class
├── di/
│   └── HomeModule.kt         # Metro bindings
└── ui/
    ├── HomeScreen.kt         # Compose UI
    └── HomeContent.kt        # UI components
```

### Component Interface Pattern

```kotlin
// feature/home/api/src/commonMain/kotlin/HomeComponent.kt
interface HomeComponent {
    val state: Value<HomeState>
    val dialogSlot: Value<ChildSlot<*, DialogChild>>

    fun onItemClick(item: HomeItem)
    fun onRefresh()
    fun showDeleteDialog(itemId: String)
    fun dismissDialog()

    interface Factory {
        fun create(
            componentContext: ComponentContext,
            onNavigateToDetails: (String) -> Unit
        ): HomeComponent
    }
}
```

### Factory with DI

```kotlin
// feature/home/impl/src/commonMain/kotlin/DefaultHomeComponent.kt
@Inject
class DefaultHomeComponent(
    private val repository: HomeRepository,
    @Assisted componentContext: ComponentContext,
    @Assisted private val onNavigateToDetails: (String) -> Unit
) : HomeComponent, ComponentContext by componentContext {

    // Implementation...

    @AssistedFactory
    interface Factory : HomeComponent.Factory {
        override fun create(
            componentContext: ComponentContext,
            onNavigateToDetails: (String) -> Unit
        ): DefaultHomeComponent
    }
}
```

## Deep Linking

```kotlin
class DefaultRootComponent(
    componentContext: ComponentContext,
    deepLink: DeepLink? = null
) : RootComponent, ComponentContext by componentContext {

    private val navigation = StackNavigation<Config>()

    init {
        deepLink?.let { handleDeepLink(it) }
    }

    private fun handleDeepLink(deepLink: DeepLink) {
        when (deepLink) {
            is DeepLink.ItemDetails -> {
                navigation.replaceAll(
                    Config.Home,
                    Config.Details(deepLink.itemId)
                )
            }
            is DeepLink.Settings -> {
                navigation.replaceAll(Config.Home, Config.Settings)
            }
        }
    }
}

sealed class DeepLink {
    data class ItemDetails(val itemId: String) : DeepLink()
    data object Settings : DeepLink()
}

// Parse in platform code
fun parseDeepLink(uri: String): DeepLink? {
    return when {
        uri.contains("/item/") -> {
            val itemId = uri.substringAfter("/item/")
            DeepLink.ItemDetails(itemId)
        }
        uri.contains("/settings") -> DeepLink.Settings
        else -> null
    }
}
```

## Result Passing

### Callbacks

```kotlin
class DetailsComponent(
    componentContext: ComponentContext,
    private val itemId: String,
    private val onResult: (DetailsResult) -> Unit
) : ComponentContext by componentContext {

    fun onSave(data: ItemData) {
        // Save logic...
        onResult(DetailsResult.Saved(data))
    }

    fun onDelete() {
        // Delete logic...
        onResult(DetailsResult.Deleted)
    }
}

sealed class DetailsResult {
    data class Saved(val data: ItemData) : DetailsResult()
    data object Deleted : DetailsResult()
}

// In parent
private fun createDetailsChild(
    config: Config.Details,
    context: ComponentContext
): Child.Details = Child.Details(
    DetailsComponent(
        componentContext = context,
        itemId = config.itemId,
        onResult = { result ->
            when (result) {
                is DetailsResult.Saved -> refreshList()
                DetailsResult.Deleted -> navigation.pop()
            }
        }
    )
)
```

## Platform Entry Points

### Android

```kotlin
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val deepLink = intent.data?.toString()?.let(::parseDeepLink)

        val graph = createGraph<AndroidAppGraph>()
        val rootComponent = graph.rootComponentFactory.create(
            componentContext = defaultComponentContext(),
            deepLink = deepLink
        )

        setContent {
            AppTheme {
                RootContent(component = rootComponent)
            }
        }
    }
}
```

### iOS

```kotlin
fun MainViewController(deepLink: DeepLink? = null): UIViewController {
    return ComposeUIViewController {
        val rootComponent = remember {
            val graph = createGraph<IosAppGraph>()
            graph.rootComponentFactory.create(
                componentContext = DefaultComponentContext(
                    lifecycle = ApplicationLifecycle()
                ),
                deepLink = deepLink
            )
        }

        AppTheme {
            RootContent(component = rootComponent)
        }
    }
}
```

### Desktop

```kotlin
fun main() = application {
    val lifecycle = LifecycleRegistry()

    val graph = createGraph<DesktopAppGraph>()
    val rootComponent = runOnUiThread {
        graph.rootComponentFactory.create(
            componentContext = DefaultComponentContext(lifecycle)
        )
    }

    Window(onCloseRequest = ::exitApplication, title = "My Application") {
        LifecycleController(lifecycle)

        AppTheme {
            RootContent(component = rootComponent)
        }
    }
}
```

## Best Practices

### Do's
- Keep components UI-agnostic (no Compose imports)
- Use interfaces for component public API
- Use `Value<T>` for observable state (not StateFlow)
- Handle back navigation via `handleBackButton = true`
- Use `@Serializable` for all Config classes
- Preserve necessary state in StateKeeper
- Use componentScope for coroutines

### Don'ts
- Don't put Compose code in components
- Don't store Context/Activity in components
- Don't use StateFlow for component state (use Value)
- Don't skip Config serialization
- Don't create ComponentContext manually
- Don't forget to handle deep links

## Testing

```kotlin
class HomeComponentTest {
    @Test
    fun `initial state is loading`() {
        val component = DefaultHomeComponent(
            componentContext = TestComponentContext(),
            repository = FakeHomeRepository(),
            onNavigateToDetails = {}
        )

        assertEquals(HomeState.Loading, component.state.value)
    }

    @Test
    fun `loads items successfully`() = runTest {
        val fakeRepo = FakeHomeRepository(items = listOf(testItem))

        val component = DefaultHomeComponent(
            componentContext = TestComponentContext(),
            repository = fakeRepo,
            onNavigateToDetails = {}
        )

        advanceUntilIdle()

        val state = component.state.value
        assertTrue(state is HomeState.Success)
        assertEquals(1, (state as HomeState.Success).items.size)
    }
}

// Test helper
class TestComponentContext : ComponentContext {
    override val lifecycle = LifecycleRegistry()
    override val stateKeeper = StateKeeperDispatcher()
    override val instanceKeeper = InstanceKeeperDispatcher()
    override val backHandler = BackDispatcher()
}
```

## Resources

- [Decompose Docs](https://arkivanov.github.io/Decompose/)
- [Decompose GitHub](https://github.com/arkivanov/Decompose)
- [Decompose Template](https://github.com/arkivanov/Decompose-multiplatform-template)
