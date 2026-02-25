---
name: kmp
description: Kotlin Multiplatform fundamentals - use for project setup, expect/actual patterns, source sets, and platform-specific code
---

# Kotlin Multiplatform (KMP) Fundamentals

Kotlin Multiplatform enables sharing code across Android, iOS, Desktop, Web (WASM), and Server.

## Project Structure

### Multi-Module Architecture (Feature-based + api/impl)

```
your-project-admin/
├── build.gradle.kts              # Root build config
├── settings.gradle.kts           # Module includes
├── gradle/libs.versions.toml     # Version catalog
│
├── core/
│   ├── common/                   # Utilities, Result types, extensions
│   │   └── src/commonMain/kotlin/
│   ├── data/                     # Data abstractions, DataStore
│   │   ├── src/commonMain/kotlin/
│   │   ├── src/androidMain/kotlin/
│   │   └── src/iosMain/kotlin/
│   ├── database/                 # Room (Android/iOS/JVM only)
│   │   └── src/commonMain/kotlin/
│   ├── network/                  # Ktor client
│   │   └── src/commonMain/kotlin/
│   └── ui/                       # Design system, theme
│       └── src/commonMain/kotlin/
│
├── feature/
│   ├── auth/
│   │   ├── api/                  # Public interfaces, models
│   │   │   └── src/commonMain/kotlin/
│   │   └── impl/                 # Implementation, UI
│   │       └── src/commonMain/kotlin/
│   └── home/
│       ├── api/
│       └── impl/
│
├── composeApp/                   # Platform entry points
│   ├── src/commonMain/           # App composition, DI graph
│   ├── src/androidMain/          # MainActivity
│   ├── src/iosMain/              # iOS entry
│   ├── src/jvmMain/              # Desktop main()
│   └── src/wasmJsMain/           # Web entry
│
└── iosApp/                       # Xcode project
```

### Source Sets Hierarchy

```
commonMain
├── androidMain
├── iosMain
│   ├── iosX64Main
│   ├── iosArm64Main
│   └── iosSimulatorArm64Main
├── jvmMain
├── wasmJsMain
└── jsMain (fallback)
```

## Gradle Setup

### Root build.gradle.kts

```kotlin
plugins {
    alias(libs.plugins.kotlinMultiplatform) apply false
    alias(libs.plugins.androidApplication) apply false
    alias(libs.plugins.androidLibrary) apply false
    alias(libs.plugins.composeMultiplatform) apply false
    alias(libs.plugins.composeCompiler) apply false
    alias(libs.plugins.kotlinSerialization) apply false
    alias(libs.plugins.ksp) apply false
    alias(libs.plugins.room) apply false
    alias(libs.plugins.metro) apply false
}
```

### settings.gradle.kts

```kotlin
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "your-project-admin"

// Core modules
include(":core:common")
include(":core:data")
include(":core:database")
include(":core:network")
include(":core:ui")

// Feature modules
include(":feature:auth:api")
include(":feature:auth:impl")
include(":feature:home:api")
include(":feature:home:impl")

// App entry points
include(":composeApp")
```

### gradle/libs.versions.toml

```toml
[versions]
kotlin = "2.1.0"
agp = "8.7.3"
compose-multiplatform = "1.7.3"
ktor = "3.1.1"
room = "2.8.4"
datastore = "1.2.0"
decompose = "3.5.0"
metro = "0.1.1"
essenty = "2.5.0"
coroutines = "1.10.1"
serialization = "1.7.3"
ksp = "2.1.0-1.0.29"

[libraries]
# Kotlin
kotlinx-coroutines-core = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-core", version.ref = "coroutines" }
kotlinx-serialization-json = { module = "org.jetbrains.kotlinx:kotlinx-serialization-json", version.ref = "serialization" }

# Ktor
ktor-client-core = { module = "io.ktor:ktor-client-core", version.ref = "ktor" }
ktor-client-cio = { module = "io.ktor:ktor-client-cio", version.ref = "ktor" }
ktor-client-darwin = { module = "io.ktor:ktor-client-darwin", version.ref = "ktor" }
ktor-client-content-negotiation = { module = "io.ktor:ktor-client-content-negotiation", version.ref = "ktor" }
ktor-serialization-kotlinx-json = { module = "io.ktor:ktor-serialization-kotlinx-json", version.ref = "ktor" }

# Room (Android, iOS, JVM only)
androidx-room-runtime = { module = "androidx.room:room-runtime", version.ref = "room" }
androidx-room-compiler = { module = "androidx.room:room-compiler", version.ref = "room" }
androidx-sqlite-bundled = { module = "androidx.sqlite:sqlite-bundled", version = "2.6.2" }

# DataStore
datastore-preferences-core = { module = "androidx.datastore:datastore-preferences-core", version.ref = "datastore" }

# Decompose
decompose = { module = "com.arkivanov.decompose:decompose", version.ref = "decompose" }
decompose-compose = { module = "com.arkivanov.decompose:extensions-compose", version.ref = "decompose" }
essenty-lifecycle = { module = "com.arkivanov.essenty:lifecycle", version.ref = "essenty" }

[plugins]
kotlinMultiplatform = { id = "org.jetbrains.kotlin.multiplatform", version.ref = "kotlin" }
kotlinSerialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }
androidApplication = { id = "com.android.application", version.ref = "agp" }
androidLibrary = { id = "com.android.library", version.ref = "agp" }
composeMultiplatform = { id = "org.jetbrains.compose", version.ref = "compose-multiplatform" }
composeCompiler = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
room = { id = "androidx.room", version.ref = "room" }
metro = { id = "dev.zacsweers.metro", version.ref = "metro" }
```

### Module build.gradle.kts (KMP Library)

```kotlin
// core/common/build.gradle.kts
plugins {
    alias(libs.plugins.kotlinMultiplatform)
    alias(libs.plugins.androidLibrary)
}

kotlin {
    androidTarget {
        compilations.all {
            kotlinOptions {
                jvmTarget = "17"
            }
        }
    }

    listOf(
        iosX64(),
        iosArm64(),
        iosSimulatorArm64()
    ).forEach { iosTarget ->
        iosTarget.binaries.framework {
            baseName = "CoreCommon"
            isStatic = true
        }
    }

    jvm("desktop")

    @OptIn(ExperimentalWasmDsl::class)
    wasmJs {
        browser()
    }

    sourceSets {
        commonMain.dependencies {
            implementation(libs.kotlinx.coroutines.core)
        }

        androidMain.dependencies {
            // Android-specific
        }

        iosMain.dependencies {
            // iOS-specific
        }

        val desktopMain by getting {
            dependencies {
                // Desktop-specific
            }
        }
    }
}

android {
    namespace = "com.your-project.admin.core.common"
    compileSdk = 35

    defaultConfig {
        minSdk = 24
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
```

## expect/actual Pattern

### Declaration (commonMain)

```kotlin
// commonMain/kotlin/Platform.kt
expect class PlatformContext

expect fun getPlatformName(): String

expect fun createDataStorePath(context: PlatformContext): String
```

### Android Implementation

```kotlin
// androidMain/kotlin/Platform.android.kt
actual typealias PlatformContext = android.content.Context

actual fun getPlatformName(): String = "Android ${android.os.Build.VERSION.SDK_INT}"

actual fun createDataStorePath(context: PlatformContext): String {
    return context.filesDir.resolve("datastore").absolutePath
}
```

### iOS Implementation

```kotlin
// iosMain/kotlin/Platform.ios.kt
import platform.Foundation.NSDocumentDirectory
import platform.Foundation.NSFileManager
import platform.Foundation.NSUserDomainMask

actual class PlatformContext

actual fun getPlatformName(): String = "iOS"

actual fun createDataStorePath(context: PlatformContext): String {
    val documentDir = NSFileManager.defaultManager.URLForDirectory(
        NSDocumentDirectory,
        NSUserDomainMask,
        null,
        false,
        null
    )
    return "${documentDir?.path}/datastore"
}
```

### Desktop Implementation

```kotlin
// desktopMain/kotlin/Platform.jvm.kt
import java.io.File

actual class PlatformContext

actual fun getPlatformName(): String =
    "${System.getProperty("os.name")} ${System.getProperty("os.version")}"

actual fun createDataStorePath(context: PlatformContext): String {
    val home = System.getProperty("user.home")
    return File(home, ".your-project-admin/datastore").absolutePath
}
```

### WASM Implementation

```kotlin
// wasmJsMain/kotlin/Platform.wasmJs.kt
actual class PlatformContext

actual fun getPlatformName(): String = "Web (WASM)"

actual fun createDataStorePath(context: PlatformContext): String {
    return "your-project-admin-datastore"  // Uses localStorage
}
```

## Module Dependencies

### Dependency Rules

```
composeApp
├── feature:auth:impl
│   ├── feature:auth:api
│   ├── core:ui
│   └── core:network
├── feature:home:impl
│   ├── feature:home:api
│   ├── core:ui
│   └── core:database
├── core:ui
│   └── core:common
├── core:network
│   └── core:common
├── core:database
│   └── core:common
└── core:data
    └── core:common
```

### api/impl Pattern

```kotlin
// feature/auth/api/build.gradle.kts
plugins {
    alias(libs.plugins.kotlinMultiplatform)
}

kotlin {
    // Targets...

    sourceSets {
        commonMain.dependencies {
            // Only models and interfaces - no implementations
            api(projects.core.common)
        }
    }
}

// feature/auth/impl/build.gradle.kts
plugins {
    alias(libs.plugins.kotlinMultiplatform)
    alias(libs.plugins.composeMultiplatform)
    alias(libs.plugins.composeCompiler)
}

kotlin {
    sourceSets {
        commonMain.dependencies {
            implementation(projects.feature.auth.api)
            implementation(projects.core.ui)
            implementation(projects.core.network)
            implementation(libs.decompose)
            implementation(libs.decompose.compose)
        }
    }
}
```

## Common Patterns

### Result Type

```kotlin
// core/common/src/commonMain/kotlin/Result.kt
sealed class AppResult<out T> {
    data class Success<T>(val data: T) : AppResult<T>()
    data class Error(val message: String, val cause: Throwable? = null) : AppResult<Nothing>()
    data object Loading : AppResult<Nothing>()
}

inline fun <T, R> AppResult<T>.map(transform: (T) -> R): AppResult<R> = when (this) {
    is AppResult.Success -> AppResult.Success(transform(data))
    is AppResult.Error -> this
    is AppResult.Loading -> this
}

inline fun <T> AppResult<T>.onSuccess(action: (T) -> Unit): AppResult<T> {
    if (this is AppResult.Success) action(data)
    return this
}

inline fun <T> AppResult<T>.onError(action: (String, Throwable?) -> Unit): AppResult<T> {
    if (this is AppResult.Error) action(message, cause)
    return this
}
```

### Repository Interface (api module)

```kotlin
// feature/auth/api/src/commonMain/kotlin/AuthRepository.kt
interface AuthRepository {
    suspend fun login(email: String, password: String): AppResult<User>
    suspend fun logout(): AppResult<Unit>
    fun observeAuthState(): Flow<AuthState>
}

data class User(
    val id: String,
    val email: String,
    val name: String
)

sealed class AuthState {
    data object Unauthenticated : AuthState()
    data class Authenticated(val user: User) : AuthState()
}
```

### Repository Implementation (impl module)

```kotlin
// feature/auth/impl/src/commonMain/kotlin/AuthRepositoryImpl.kt
class AuthRepositoryImpl(
    private val apiService: AuthApiService,
    private val tokenStorage: TokenStorage
) : AuthRepository {

    private val _authState = MutableStateFlow<AuthState>(AuthState.Unauthenticated)

    override suspend fun login(email: String, password: String): AppResult<User> {
        return try {
            val response = apiService.login(LoginRequest(email, password))
            tokenStorage.saveToken(response.token)
            _authState.value = AuthState.Authenticated(response.user)
            AppResult.Success(response.user)
        } catch (e: Exception) {
            AppResult.Error("Login failed: ${e.message}", e)
        }
    }

    override suspend fun logout(): AppResult<Unit> {
        tokenStorage.clearToken()
        _authState.value = AuthState.Unauthenticated
        return AppResult.Success(Unit)
    }

    override fun observeAuthState(): Flow<AuthState> = _authState.asStateFlow()
}
```

## Platform Checks at Runtime

```kotlin
// When expect/actual is overkill, use runtime checks
enum class Platform {
    Android, iOS, Desktop, Web
}

expect val currentPlatform: Platform

// androidMain
actual val currentPlatform: Platform = Platform.Android

// iosMain
actual val currentPlatform: Platform = Platform.iOS

// desktopMain
actual val currentPlatform: Platform = Platform.Desktop

// wasmJsMain
actual val currentPlatform: Platform = Platform.Web

// Usage
@Composable
fun AdaptiveComponent() {
    when (currentPlatform) {
        Platform.Android -> AndroidSpecificUI()
        Platform.iOS -> IOSSpecificUI()
        Platform.Desktop -> DesktopSpecificUI()
        Platform.Web -> WebSpecificUI()
    }
}
```

## Testing

### Shared Tests (commonTest)

```kotlin
// core/common/src/commonTest/kotlin/ResultTest.kt
class ResultTest {
    @Test
    fun `map transforms success value`() {
        val result: AppResult<Int> = AppResult.Success(5)
        val mapped = result.map { it * 2 }

        assertTrue(mapped is AppResult.Success)
        assertEquals(10, (mapped as AppResult.Success).data)
    }

    @Test
    fun `map preserves error`() {
        val result: AppResult<Int> = AppResult.Error("test error")
        val mapped = result.map { it * 2 }

        assertTrue(mapped is AppResult.Error)
    }
}
```

### Platform-Specific Tests

```kotlin
// androidTest - uses Robolectric or instrumented tests
// iosTest - runs on simulator
// jvmTest - standard JUnit
```

## Best Practices

### Do's
- Put as much code as possible in `commonMain`
- Use expect/actual only for platform APIs
- Keep platform-specific implementations minimal
- Use dependency injection for platform differences
- Test shared code in `commonTest`
- Use version catalogs for dependencies

### Don'ts
- Don't put platform-specific code in common modules
- Don't duplicate code across platform source sets
- Don't use platform-specific types in public APIs
- Don't skip proper module separation (api/impl)
- Don't ignore WASM limitations for database

## WASM Limitations

**Important limitations when targeting WebAssembly:**

### Database
- **Room**: NOT supported on WASM
- Use `localStorage` or `IndexedDB` via expect/actual pattern
- Consider skipping database for wasmJsMain source set

```kotlin
// commonMain - interface only
expect class AppStorage {
    fun getString(key: String): String?
    fun putString(key: String, value: String)
}

// wasmJsMain - browser storage
actual class AppStorage {
    actual fun getString(key: String): String? =
        window.localStorage.getItem(key)
    actual fun putString(key: String, value: String) {
        window.localStorage.setItem(key, value)
    }
}
```

### Network
- **CORS**: All HTTP requests subject to browser CORS policy
- **WebSocket**: Works but needs CORS-compatible server

### File System
- No direct file system access
- Use virtual file APIs or blob URLs

### Threading
- No `Dispatchers.IO` (use `Dispatchers.Default`)
- Web Workers for background tasks (limited)

## Resources

- [Kotlin Multiplatform Docs](https://kotlinlang.org/docs/multiplatform.html)
- [KMP Getting Started](https://developer.android.com/kotlin/multiplatform)
- [Compose Multiplatform](https://www.jetbrains.com/compose-multiplatform/)
- [KMP Wizard](https://kmp.jetbrains.com/)
