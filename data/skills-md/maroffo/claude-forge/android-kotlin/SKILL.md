---
name: android-kotlin
description: "Android development with Kotlin 2.x, Jetpack Compose, Clean Architecture, and performance. Use when working with .kt files, build.gradle.kts, AndroidManifest.xml, or Compose UI."
compatibility: "Requires Android SDK, Gradle. Optional: ktlint."
allowed-tools: [mcp__acp__Read, mcp__acp__Edit, mcp__acp__Write, mcp__acp__Bash]
---

# ABOUTME: Android/Kotlin - Compose, architecture, testing, performance
# ABOUTME: Kotlin 2.x, Compose 1.7+, type-safe navigation, Baseline Profiles

# Android/Kotlin

## Commands
```bash
./gradlew assembleDebug|assembleRelease|test|connectedAndroidTest|lint|ktlintFormat
./gradlew :feature:home:build                    # Module-specific
```

**See:** `_AST_GREP.md` (sg patterns) | `_PATTERNS.md` | `source-control`

---

## Architecture

### Clean Architecture Structure
```
feature/
├── data/repository/, datasource/local/, datasource/remote/
├── domain/model/, repository/ (interface), usecase/
└── presentation/screen/, viewmodel/
```

### Use Cases
Single responsibility, orchestration here (NOT in ViewModel).
```kotlin
class SignInUseCase(private val auth: AuthRepository, private val user: UserRepository) {
    suspend operator fun invoke(email: String, password: String): Result<User> {
        val result = auth.signIn(email, password).getOrElse { return Result.failure(it) }
        user.saveUserLocally(result)
        return Result.success(result)
    }
}
```

### ViewModel Pattern
```kotlin
class FeedViewModel(private val getFeed: GetFeedUseCase) : ViewModel() {
    private val _uiState = MutableStateFlow<FeedUiState>(FeedUiState.Loading)
    val uiState = _uiState.asStateFlow()

    private val _sideEffects = Channel<FeedSideEffect>(Channel.BUFFERED)
    val sideEffects = _sideEffects.receiveAsFlow()

    fun loadFeed() = viewModelScope.launch {
        _uiState.value = FeedUiState.Loading
        getFeed().onSuccess { _uiState.value = FeedUiState.Success(it) }
                 .onFailure { _uiState.value = FeedUiState.Error(it.message) }
    }
}

sealed interface FeedUiState { /* Loading, Success, Error */ }
sealed interface FeedSideEffect { /* NavigateToDetail, ShowSnackbar */ }
```

---

## Dependency Injection

| Aspect | Hilt | Koin |
|--------|------|------|
| Type | Compile-time | Runtime |
| Build time | Slower | Faster |
| Error detection | Compile | Runtime |
| KMP support | No | Yes |
| Best for | Large/enterprise | Small-medium/KMP |

**Hilt:** `@HiltAndroidApp`, `@AndroidEntryPoint`, `@HiltViewModel`, `@Inject constructor`
**Koin:** `module { }`, `single`, `factory`, `viewModelOf`, `koinViewModel()`

See `references/compose-patterns.md` for setup examples.

---

## Compose Essentials

**State hoisting:** Lift state to the caller, pass callbacks down.
```kotlin
@Composable
fun UserCard(user: User, onClick: () -> Unit, modifier: Modifier = Modifier) {
    Card(onClick = onClick, modifier = modifier) { /* content */ }
}
```

**State management:**
- `remember { mutableStateOf() }`, lost on config change
- `rememberSaveable { mutableStateOf() }`, survives config change
- `derivedStateOf`, computed state

**Side effects:** `LaunchedEffect(key)`, `DisposableEffect`

**Type-safe navigation:** `@Serializable` routes (2.8.0+)

See `references/compose-patterns.md` for detailed examples.

---

## Code Review Checklists

### Architecture
- [ ] VMs don't chain use cases (orchestration in domain)
- [ ] VMs don't call repositories directly
- [ ] Use cases have single responsibility
- [ ] State immutable (use `copy()`)
- [ ] Side effects use Channel/SharedFlow (not StateFlow)

### Compose
- [ ] State hoisted appropriately
- [ ] `remember` vs `rememberSaveable` correct
- [ ] Side effects use correct APIs
- [ ] Stable types for parameters
- [ ] `key` used in LazyColumn/LazyRow

### Red Flags
| Critical | High |
|----------|------|
| Network/DB on main thread | Use case chaining in VM |
| StateFlow for one-time events | Mutable state exposed from VM |
| Hardcoded strings in UI | Missing `key` in LazyColumn |
| Missing error handling | collectAsState vs collectAsStateWithLifecycle |
| R8 disabled in release | |

---

## Quick Reference

**Kotlin 2.x features:** Guard conditions (2.1), context parameters (2.2), K2 compiler benefits → `references/kotlin-features.md`

**Compose patterns:** State, side effects, navigation, image loading → `references/compose-patterns.md`

**Networking & Data:** Retrofit, Ktor, Room, DataStore → `references/data-layer.md`

**Testing:** Compose UI tests, ViewModel tests, snapshot tests → `references/testing-patterns.md`

**Performance:** R8, Baseline Profiles, Compose optimization → `references/performance.md`

---

## Resources

**Official:** [android.com/kotlin](https://developer.android.com/kotlin) | [compose](https://developer.android.com/develop/ui/compose) | [architecture](https://developer.android.com/topic/architecture) | [type-safe nav](https://developer.android.com/guide/navigation/design/type-safety) | [baseline profiles](https://developer.android.com/topic/performance/baselineprofiles)

**Kotlin:** [2.2](https://kotlinlang.org/docs/whatsnew22.html) | [2.1.20](https://kotlinlang.org/docs/whatsnew2120.html) | [2.3](https://blog.jetbrains.com/kotlin/2025/12/kotlin-2-3-0-released/)

**Libraries:** [Coil](https://coil-kt.github.io/coil/) | [Koin](https://insert-koin.io/) | [Hilt](https://dagger.dev/hilt/) | [Retrofit](https://square.github.io/retrofit/) | [Ktor](https://ktor.io/docs/client.html) | [Room](https://developer.android.com/training/data-storage/room)

**Testing:** [Compose testing](https://developer.android.com/develop/ui/compose/testing) | [Paparazzi](https://github.com/cashapp/paparazzi) | [Turbine](https://github.com/cashapp/turbine)
