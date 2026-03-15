---
name: kmp-navigation
description: Navigation libraries for KMP. Voyager, Decompose, and platform-specific navigation (Compose Navigation, SwiftUI).
---

# KMP Navigation

Cross-platform navigation strategies for Kotlin Multiplatform.

## Navigation Options

### 1. Voyager (Recommended)

```kotlin
// build.gradle.kts
dependencies {
    implementation("cafe.adriel.voyager:voyager-navigator:1.0.0")
    implementation("cafe.adriel.voyager:voyager-screen-model:1.0.0")
}
```

```kotlin
// commonMain/kotlin/navigation/VoyagerNavigation.kt
@Serializable
data object HomeScreen : Screen

@Serializable
data class DetailScreen(val id: String) : Screen

@Composable
fun AppNavigation() {
    Navigator(HomeScreen) { navigator ->
        VoyagerNavigation(
            navigator = navigator,
            screenModels = { rememberScreenModel { AppScreenModel() } }
        )
    }
}

@Composable
fun HomeScreen() {
    Screen { // Voyager's Screen composable
        val navigator = LocalNavigator.currentOrThrow

        Button(onClick = { navigator.push(DetailScreen("123")) }) {
            Text("Go to Detail")
        }
    }
}
```

### 2. Decompose

```kotlin
// build.gradle.kts
dependencies {
    implementation("com.arkivanov.decompose:decompose:2.1.0")
    implementation("com.arkivanov.decompose:extensions-compose-jetpack:2.1.0")
}
```

```kotlin
// commonMain/kotlin/navigation/DecomposeNavigation.kt
sealed class Config : Parcelable {
    @Parcelize
    data object Home : Config()

    @Parcelize
    data class Detail(val id: String) : Config()
}

@Composable
fun AppNavigation() {
    val navigator = rememberNavigator()

    Decomanavigation(
        navigator = navigator,
        initialConfiguration = Config.Home
    ) {
        when (val config = it.configuration) {
            is Config.Home -> HomeScreen(
                onNavigateToDetail = { navigator.push(Config.Detail(it)) }
            )
            is Config.Detail -> DetailScreen(
                id = config.id,
                onBack = { navigator.pop() }
            )
        }
    }
}
```

### 3. Platform-Native Bridge

```kotlin
// commonMain/kotlin/navigation/Navigator.kt
sealed class Screen : Parcelable {
    @Parcelize
    data object Home : Screen()

    @Parcelize
    data class Detail(val id: String) : Screen()
}

interface Navigator {
    val navigationStack: StateFlow<List<Screen>>
    fun navigateTo(screen: Screen)
    fun navigateBack()
}

expect class Navigator() : Navigator

// androidMain - Compose Navigation
actual class Navigator : Navigator {
    private val _stack = MutableStateFlow(listOf(Screen.Home))
    override val navigationStack: StateFlow<List<Screen>> = _stack.asStateFlow()

    @Composable
    fun SetupNavigation() {
        val navController = rememberNavController()

        NavHost(navController, startDestination = "home") {
            composable("home") {
                HomeScreen(
                    onNavigateToDetail = { navController.navigate("detail/$it") }
                )
            }
            composable("detail/{id}") { backStackEntry ->
                val id = backStackEntry.arguments?.getString("id") ?: ""
                DetailScreen(id, onBack = { navController.popBackStack() })
            }
        }
    }
}

// iosMain - SwiftUI Navigation wrapper
actual class Navigator : Navigator {
    private val _stack = MutableStateFlow(listOf(Screen.Home))
    override val navigationStack: StateFlow<List<Screen>> = _stack.asStateFlow()

    fun toSwiftUI() -> some View {
        // Bridge to SwiftUI NavigationStack
    }
}
```

## Tab Navigation

### Voyager Tabs

```kotlin
// commonMain/kotlin/navigation/TabNavigation.kt
enum class Tab {
    HOME,
    SEARCH,
    PROFILE
}

@Composable
fun TabNavigation() {
    val navigator = rememberTabNavigator()

    TabNavigator(tab = navigator.current) {
        // Tab content
    }
}
```

### Decompose Tabs

```kotlin
// commonMain/kotlin/navigation/Tabs.kt
enum class Tab {
    HOME,
    SEARCH,
    PROFILE
}

@Composable
fun Tabs(
    navigator: StackNavigator,
    selectedTab: MutableState<Tab>
) {
    Row {
        Tab.values().forEach { tab ->
            Button(
                onClick = { selectedTab.value = tab }
            ) {
                Text(tab.name)
            }
        }
    }
}
```

## Deep Linking

```kotlin
// commonMain/kotlin/navigation/DeepLink.kt
sealed class Screen : Parcelable {
    @Parcelize
    data object Home : Screen()

    @Parcelize
    data class Detail(val id: String) : Screen()

    companion object {
        fun fromDeepLink(url: String): Screen? {
            return when {
                url.contains("/home") -> Home
                "/detail/([a-z0-9]+)".toRegex().find(url) != null -> {
                    val id = "/detail/([a-z0-9]+)".toRegex().find(url)!!.groupValues[1]
                    Detail(id)
                }
                else -> null
            }
        }
    }
}
```

## Navigation Arguments

### Type-Safe Arguments

```kotlin
// ✅ Sealed class with arguments
@Serializable
sealed class Screen : Parcelable {
    @Parcelize
    data object Home : Screen()

    @Parcelize
    data class UserDetail(
        val userId: String,
        val section: String? = null
    ) : Screen()

    @Parcelize
    data class EditItem(
        val itemId: String,
        val mode: EditMode = EditMode.View
    ) : Screen()
}

@Serializable
enum class EditMode {
    View, Edit, Create
}
```

## State Preservation

### Voyager ScreenModel

```kotlin
class DetailScreenModel(
    private val userId: String,
    private val repository: UserRepository
) : ScreenModel {
    val user = mutableStateOf<User?>(null)
    val isLoading = mutableStateOf(false)

    init {
        loadUser()
    }

    private fun loadUser() {
        viewModelScope.launch {
            isLoading.value = true
            user.value = repository.getUser(userId)
            isLoading.value = false
        }
    }
}

@Composable
fun DetailScreen(
    userId: String,
    onBack: () -> Unit
) {
    val model = rememberScreenModel { DetailScreenModel(userId) }

    if (model.isLoading.value) {
        CircularProgressIndicator()
    } else {
        model.user.value?.let { user ->
            UserContent(user, onBack)
        }
    }
}
```

---

**Remember**: Choose navigation library based on project needs. Voyager for simplicity, Decompose for control, platform-native for full platform feature support.
