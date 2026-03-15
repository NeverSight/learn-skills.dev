---
name: android-development
description: Android Kotlin development with Coroutines, Jetpack Compose, Koin, and MockK testing
---

# Android Development Skill

---

## Project Structure

```
project/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── kotlin/com/example/app/
│   │   │   │   ├── data/               # Data layer
│   │   │   │   │   ├── local/          # Room database
│   │   │   │   │   ├── remote/         # Retrofit/Ktor services
│   │   │   │   │   └── repository/     # Repository implementations
│   │   │   │   ├── di/                 # Koin modules
│   │   │   │   ├── domain/             # Business logic
│   │   │   │   │   ├── model/          # Domain models
│   │   │   │   │   ├── repository/     # Repository interfaces
│   │   │   │   │   └── usecase/        # Use cases
│   │   │   │   ├── ui/                 # Presentation layer
│   │   │   │   │   ├── feature/        # Feature screens
│   │   │   │   │   │   ├── FeatureScreen.kt      # Compose UI
│   │   │   │   │   │   └── FeatureViewModel.kt
│   │   │   │   │   ├── components/     # Reusable Compose components
│   │   │   │   │   └── theme/          # Material theme
│   │   │   │   └── App.kt              # Application class
│   │   │   ├── res/
│   │   │   └── AndroidManifest.xml
│   │   ├── test/                       # Unit tests
│   │   └── androidTest/                # Instrumentation tests
│   └── build.gradle.kts
├── build.gradle.kts                    # Project-level build file
├── gradle.properties
├── gradle/
│   └── libs.versions.toml              # Version Catalog
├── settings.gradle.kts
└── CLAUDE.md
```

---

## Gradle Configuration (Kotlin DSL & Version Catalog)

### Version Catalog (gradle/libs.versions.toml)
```toml
[versions]
agp = "8.3.0"
kotlin = "1.9.22"
coreKtx = "1.12.0"
junit = "4.13.2"
junitVersion = "1.1.5"
espressoCore = "3.5.1"
lifecycleRuntimeKtx = "2.7.0"
activityCompose = "1.8.2"
composeBom = "2024.02.00"
ksp = "1.9.22-1.0.17"
room = "2.6.1"
retrofit = "2.9.0"
okhttp = "4.12.0"
koin = "3.5.3"
coil = "2.6.0"
serialization = "1.6.3"
workManager = "2.9.0"
navigation = "2.7.7" # Navigation 3 reference likely refers to new Compose Navigation patterns or alpha versions, using stable 2.7.7 for now or keeping user intent if specific library exists. Assuming standard navigation-compose here mapped to user's 'navigation3' alias for structure consistency.
preference = "1.2.1"
media3 = "1.3.0"
jsoup = "1.17.2"
zxing = "3.5.3"
json = "20231013"
coroutinesTest = "1.7.3"
mockk = "1.13.8"

[libraries]
androidx-core-ktx = { group = "androidx.core", name = "core-ktx", version.ref = "coreKtx" }
androidx-lifecycle-runtime-ktx = { group = "androidx.lifecycle", name = "lifecycle-runtime-ktx", version.ref = "lifecycleRuntimeKtx" }
androidx-activity-compose = { group = "androidx.activity", name = "activity-compose", version.ref = "activityCompose" }
androidx-compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "composeBom" }
androidx-compose-ui = { group = "androidx.compose.ui", name = "ui" }
androidx-compose-ui-graphics = { group = "androidx.compose.ui", name = "ui-graphics" }
androidx-compose-ui-tooling = { group = "androidx.compose.ui", name = "ui-tooling" }
androidx-compose-ui-tooling-preview = { group = "androidx.compose.ui", name = "ui-tooling-preview" }
androidx-compose-ui-test-manifest = { group = "androidx.compose.ui", name = "ui-test-manifest" }
androidx-compose-ui-test-junit4 = { group = "androidx.compose.ui", name = "ui-test-junit4" }
androidx-compose-material3 = { group = "androidx.compose.material3", name = "material3" }
androidx-compose-material-icons-extended = { group = "androidx.compose.material", name = "material-icons-extended" }

androidx-room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
androidx-room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
androidx-room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }
androidx-room-testing = { group = "androidx.room", name = "room-testing", version.ref = "room" }

squareup-retrofit2 = { group = "com.squareup.retrofit2", name = "retrofit", version.ref = "retrofit" }
squareup-retrofit2-converter-gson = { group = "com.squareup.retrofit2", name = "converter-gson", version.ref = "retrofit" }
squareup-okhttp3-logging-interceptor = { group = "com.squareup.okhttp3", name = "logging-interceptor", version.ref = "okhttp" }

androidx-work-runtime-ktx = { group = "androidx.work", name = "work-runtime-ktx", version.ref = "workManager" }
androidx-preference-ktx = { group = "androidx.preference", name = "preference-ktx", version.ref = "preference" }

# Mapping user's 'navigation3' to standard navigation-compose for stability, or update if specific library intended
androidx-navigation3-runtime = { group = "androidx.navigation", name = "navigation-runtime-ktx", version.ref = "navigation" }
androidx-navigation3-ui = { group = "androidx.navigation", name = "navigation-ui-ktx", version.ref = "navigation" }
androidx-lifecycle-viewmodel-navigation3 = { group = "androidx.navigation", name = "navigation-compose", version.ref = "navigation" }

kotlinx-serialization-json = { group = "org.jetbrains.kotlinx", name = "kotlinx-serialization-json", version.ref = "serialization" }

coil-compose = { group = "io.coil-kt", name = "coil-compose", version.ref = "coil" }
google-gson = { group = "com.google.code.gson", name = "gson", version = "2.10.1" }
zxing = { group = "com.google.zxing", name = "core", version.ref = "zxing" }
jsoup = { group = "org.jsoup", name = "jsoup", version.ref = "jsoup" }

androidx-media3-exoplayer = { group = "androidx.media3", name = "media3-exoplayer", version.ref = "media3" }
androidx-media3-ui = { group = "androidx.media3", name = "media3-ui", version.ref = "media3" }

koin-core = { group = "io.insert-koin", name = "koin-core", version.ref = "koin" }
koin-android = { group = "io.insert-koin", name = "koin-android", version.ref = "koin" }
koin-androidx-compose = { group = "io.insert-koin", name = "koin-androidx-compose", version.ref = "koin" }
koin-navigation3 = { group = "io.insert-koin", name = "koin-androidx-navigation", version.ref = "koin" }
koin-androidx-workmanager = { group = "io.insert-koin", name = "koin-androidx-workmanager", version.ref = "koin" }
koin-androidx-startup = { group = "io.insert-koin", name = "koin-androidx-startup", version.ref = "koin" }

junit = { group = "junit", name = "junit", version.ref = "junit" }
org-json = { group = "org.json", name = "json", version.ref = "json" }
kotlinx-coroutines-test = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-test", version.ref = "coroutinesTest" }
mockk = { group = "io.mockk", name = "mockk", version.ref = "mockk" }
androidx-junit = { group = "androidx.test.ext", name = "junit", version.ref = "junitVersion" }
androidx-espresso-core = { group = "androidx.test.espresso", name = "espresso-core", version.ref = "espressoCore" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
kotlin-compose = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
kotlin-serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
```

### App-level build.gradle.kts
```kotlin
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.kotlin.serialization)
    alias(libs.plugins.ksp)
}

android {
    namespace = "com.example.app"
    compileSdk {
        version = release(36)
    }

    defaultConfig {
        applicationId = "com.example.app"
        minSdk = 24
        targetSdk = 36
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    
    kotlin {
        compilerOptions {
            jvmTarget = org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_11
            allWarningsAsErrors.set(true)
            freeCompilerArgs.addAll(
                "-opt-in=org.koin.core.annotation.KoinExperimentalAPI",
                "-opt-in=androidx.compose.material3.ExperimentalMaterial3Api",
                "-opt-in=kotlinx.coroutines.ExperimentalCoroutinesApi",
                "-opt-in=kotlinx.coroutines.FlowPreview",
            )
        }
    }

    buildFeatures {
        compose = true
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.activity.compose)
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.ui)
    implementation(libs.androidx.compose.ui.graphics)
    implementation(libs.androidx.compose.ui.tooling.preview)
    implementation(libs.androidx.compose.material3)
    implementation(libs.androidx.compose.material.icons.extended)

    // Room
    implementation(libs.androidx.room.runtime)
    implementation(libs.androidx.room.ktx)
    ksp(libs.androidx.room.compiler)

    // Network
    implementation(libs.squareup.retrofit2)
    implementation(libs.squareup.retrofit2.converter.gson)
    implementation(libs.squareup.okhttp3.logging.interceptor)
    implementation(libs.google.gson)
    implementation(libs.kotlinx.serialization.json)

    // WorkManager & Preference
    implementation(libs.androidx.work.runtime.ktx)
    implementation(libs.androidx.preference.ktx)

    // Navigation
    implementation(libs.androidx.navigation3.runtime)
    implementation(libs.androidx.navigation3.ui)
    implementation(libs.androidx.lifecycle.viewmodel.navigation3)

    // Image & Utils
    implementation(libs.coil.compose)
    implementation(libs.zxing)
    implementation(libs.jsoup)

    // Media
    implementation(libs.androidx.media3.exoplayer)
    implementation(libs.androidx.media3.ui)

    // Koin
    implementation(libs.koin.core)
    implementation(libs.koin.android)
    implementation(libs.koin.androidx.compose)
    implementation(libs.koin.navigation3)
    implementation(libs.koin.androidx.workmanager)
    implementation(libs.koin.androidx.startup)

    // Testing
    testImplementation(libs.junit)
    testImplementation(libs.org.json)
    testImplementation(libs.kotlinx.coroutines.test)
    testImplementation(libs.mockk)
    testImplementation(libs.androidx.room.testing)
    
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(platform(libs.androidx.compose.bom))
    androidTestImplementation(libs.androidx.compose.ui.test.junit4)
    debugImplementation(libs.androidx.compose.ui.tooling)
    debugImplementation(libs.androidx.compose.ui.test.manifest)
}
```

---

## Kotlin Coroutines & Flow

### ViewModel with StateFlow
```kotlin
class UserViewModel(
    private val getUserUseCase: GetUserUseCase,
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val _uiState = MutableStateFlow(UserUiState())
    val uiState: StateFlow<UserUiState> = _uiState.asStateFlow()

    private val userId: String = checkNotNull(savedStateHandle["userId"])

    init {
        loadUser()
    }

    fun loadUser() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }

            getUserUseCase(userId)
                .catch { e ->
                    _uiState.update {
                        it.copy(isLoading = false, error = e.message)
                    }
                }
                .collect { user ->
                    _uiState.update {
                        it.copy(isLoading = false, user = user, error = null)
                    }
                }
        }
    }

    fun clearError() {
        _uiState.update { it.copy(error = null) }
    }
}

data class UserUiState(
    val user: User? = null,
    val isLoading: Boolean = false,
    val error: String? = null
)
```

### Repository with Flow
```kotlin
interface UserRepository {
    fun getUser(userId: String): Flow<User>
    fun observeUsers(): Flow<List<User>>
    suspend fun saveUser(user: User)
}

class UserRepositoryImpl(
    private val api: UserApi,
    private val dao: UserDao,
    private val dispatcher: CoroutineDispatcher = Dispatchers.IO
) : UserRepository {

    override fun getUser(userId: String): Flow<User> = flow {
        // Emit cached data first
        dao.getUserById(userId)?.let { emit(it) }

        // Fetch from network and update cache
        val remoteUser = api.getUser(userId)
        dao.insert(remoteUser)
        emit(remoteUser)
    }.flowOn(dispatcher)

    override fun observeUsers(): Flow<List<User>> =
        dao.observeAllUsers().flowOn(dispatcher)

    override suspend fun saveUser(user: User) = withContext(dispatcher) {
        api.saveUser(user)
        dao.insert(user)
    }
}
```

---

## Jetpack Compose

### Screen with ViewModel
```kotlin
@Composable
fun UserScreen(
    viewModel: UserViewModel = koinViewModel(),
    onNavigateBack: () -> Unit
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    UserScreenContent(
        uiState = uiState,
        onRefresh = viewModel::loadUser,
        onErrorDismiss = viewModel::clearError,
        onNavigateBack = onNavigateBack
    )
}

@Composable
private fun UserScreenContent(
    uiState: UserUiState,
    onRefresh: () -> Unit,
    onErrorDismiss: () -> Unit,
    onNavigateBack: () -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("User Profile") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, "Back")
                    }
                }
            )
        }
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            when {
                uiState.isLoading -> {
                    CircularProgressIndicator(
                        modifier = Modifier.align(Alignment.Center)
                    )
                }
                uiState.user != null -> {
                    UserContent(user = uiState.user)
                }
            }

            uiState.error?.let { error ->
                Snackbar(
                    modifier = Modifier.align(Alignment.BottomCenter),
                    action = {
                        TextButton(onClick = onErrorDismiss) {
                            Text("Dismiss")
                        }
                    }
                ) {
                    Text(error)
                }
            }
        }
    }
}
```

---

## Sealed Classes for State

---

## Koin Dependency Injection

### Koin Modules
```kotlin
val appModule = module {
    single<UserRepository> { UserRepositoryImpl(get(), get()) }
    factory { GetUserUseCase(get()) }
    viewModel { params -> UserViewModel(get(), params.get()) }
}

val networkModule = module {
    single { Retrofit.Builder()...build().create(UserApi::class.java) }
}
```

### Application Class
```kotlin
class App : Application() {
    override fun onCreate() {
        super.onCreate()
        startKoin {
            androidContext(this@App)
            modules(appModule, networkModule)
        }
    }
}
```

---

## Sealed Classes for State

### Result Wrapper
```kotlin
sealed interface Result<out T> {
    data class Success<T>(val data: T) : Result<T>
    data class Error(val exception: Throwable) : Result<Nothing>
    data object Loading : Result<Nothing>
}

fun <T> Result<T>.getOrNull(): T? = (this as? Result.Success)?.data

inline fun <T, R> Result<T>.map(transform: (T) -> R): Result<R> = when (this) {
    is Result.Success -> Result.Success(transform(data))
    is Result.Error -> this
    is Result.Loading -> this
}
```

---

## Testing with MockK & Turbine

### ViewModel Tests
```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class UserViewModelTest {

    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    private val getUserUseCase: GetUserUseCase = mockk(relaxed = true)
    private val savedStateHandle = SavedStateHandle(mapOf("userId" to "123"))

    private lateinit var viewModel: UserViewModel

    @Before
    fun setup() {
        // MockK setup
    }

    @Test
    fun `loadUser success updates state with user`() = runTest {
        val user = User("123", "John Doe", "john@example.com")
        coEvery { getUserUseCase("123") } returns flowOf(user)
        
        viewModel = UserViewModel(getUserUseCase, savedStateHandle)

        viewModel.uiState.test {
            val initial = awaitItem()
            assertFalse(initial.isLoading)

            viewModel.loadUser()

            val loading = awaitItem()
            assertTrue(loading.isLoading)

            val success = awaitItem()
            assertFalse(success.isLoading)
            assertEquals(user, success.user)
        }
    }
}

class MainDispatcherRule(
    private val dispatcher: TestDispatcher = UnconfinedTestDispatcher()
) : TestWatcher() {
    override fun starting(description: Description) {
        Dispatchers.setMain(dispatcher)
    }
    override fun finished(description: Description) {
        Dispatchers.resetMain()
    }
}
```

---

### Integration Test with Koin
```kotlin
class UserIntegrationTest : KoinTest {

    private val userRepository: UserRepository by inject()

    @get:Rule
    val koinTestRule = KoinTestRule.create {
        modules(appModule, networkModule)
    }

    @Test
    fun `repository is injected correctly`() {
        assertNotNull(userRepository)
    }
}
```

---

## GitHub Actions

```yaml
name: Android Kotlin CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v3

      - name: Run Detekt
        run: ./gradlew detekt

      - name: Run Ktlint
        run: ./gradlew ktlintCheck

      - name: Run Unit Tests
        run: ./gradlew testDebugUnitTest

      - name: Build Debug APK
        run: ./gradlew assembleDebug
```

---

## Lint Configuration

### detekt.yml
```yaml
build:
  maxIssues: 0

complexity:
  LongMethod:
    threshold: 20
  LongParameterList:
    functionThreshold: 4
  TooManyFunctions:
    thresholdInFiles: 10

style:
  MaxLineLength:
    maxLineLength: 120
  WildcardImport:
    active: true

coroutines:
  GlobalCoroutineUsage:
    active: true
```

---

## Kotlin Anti-Patterns

- ❌ **Blocking coroutines on Main** - Never use `runBlocking` on main thread
- ❌ **GlobalScope usage** - Use structured concurrency with viewModelScope/lifecycleScope
- ❌ **Collecting flows in init** - Use `repeatOnLifecycle` or `collectAsStateWithLifecycle`
- ❌ **Mutable state exposure** - Expose `StateFlow` not `MutableStateFlow`
- ❌ **Not handling exceptions in flows** - Always use `catch` operator
- ❌ **Lateinit for nullable** - Use `lazy` or nullable with `?`
- ❌ **Hardcoded dispatchers** - Inject dispatchers for testability
- ❌ **Not using sealed classes** - Prefer sealed for finite state sets
- ❌ **Side effects in Composables** - Use `LaunchedEffect`/`SideEffect`
- ❌ **Unstable Compose parameters** - Use stable/immutable types or `@Stable`
- ❌ **Not-null assertion (!!)** - Never use `!!`, always use safe call `?.`, elvis operator `?:`, or `requireNotNull`/`checkNotNull` with message
- ❌ **In-code OptIn annotations** - Do not use `@OptIn(Experimental...)` in code. Configure `freeCompilerArgs` in `build.gradle.kts` instead.

