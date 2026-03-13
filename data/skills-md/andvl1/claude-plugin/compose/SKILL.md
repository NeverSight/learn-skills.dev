---
name: compose
description: Compose Multiplatform UI patterns - use for shared UI components, theming, resources, and platform-specific adaptations
---

# Compose Multiplatform

Declarative UI framework for Android, iOS, Desktop, and Web with shared code.

## Setup

### build.gradle.kts (Compose module)

```kotlin
plugins {
    alias(libs.plugins.kotlinMultiplatform)
    alias(libs.plugins.androidLibrary)
    alias(libs.plugins.composeMultiplatform)
    alias(libs.plugins.composeCompiler)
}

kotlin {
    androidTarget()
    iosX64()
    iosArm64()
    iosSimulatorArm64()
    jvm("desktop")

    @OptIn(ExperimentalWasmDsl::class)
    wasmJs { browser() }

    sourceSets {
        commonMain.dependencies {
            implementation(compose.runtime)
            implementation(compose.foundation)
            implementation(compose.material3)
            implementation(compose.components.resources)
            implementation(compose.components.uiToolingPreview)
        }

        androidMain.dependencies {
            implementation(compose.uiTooling)
            implementation(libs.androidx.activity.compose)
        }

        val desktopMain by getting {
            dependencies {
                implementation(compose.desktop.currentOs)
            }
        }
    }
}

compose.resources {
    publicResClass = true
    packageOfResClass = "com.your-project.admin.resources"
    generateResClass = auto
}
```

## Resources

### Directory Structure

```
src/commonMain/composeResources/
├── drawable/              # Images (PNG, WebP, SVG)
│   ├── ic_logo.xml       # Vector drawable
│   └── bg_pattern.png
├── drawable-dark/         # Dark theme variants
├── font/                  # TTF/OTF fonts
│   ├── Inter-Regular.ttf
│   └── Inter-Bold.ttf
├── values/
│   └── strings.xml        # Default strings
├── values-ru/
│   └── strings.xml        # Russian strings
└── files/                 # Raw files
    └── config.json
```

### strings.xml Format

```xml
<!-- values/strings.xml -->
<resources>
    <string name="app_name">My Application</string>
    <string name="welcome_message">Welcome, %1$s!</string>
    <string name="items_count">%1$d items</string>
</resources>

<!-- values-ru/strings.xml -->
<resources>
    <string name="app_name">Мое Приложение</string>
    <string name="welcome_message">Добро пожаловать, %1$s!</string>
    <string name="items_count">%1$d элементов</string>
</resources>
```

### Using Resources

```kotlin
import com.your-project.admin.resources.Res
import com.your-project.admin.resources.*
import org.jetbrains.compose.resources.*

@Composable
fun ResourcesDemo() {
    // Strings
    val appName = stringResource(Res.string.app_name)
    val welcome = stringResource(Res.string.welcome_message, userName)
    val count = stringResource(Res.string.items_count, itemCount)

    // Images
    Image(
        painter = painterResource(Res.drawable.ic_logo),
        contentDescription = "Logo"
    )

    // Fonts
    val typography = Typography(
        bodyLarge = TextStyle(
            fontFamily = FontFamily(Font(Res.font.Inter_Regular))
        ),
        titleLarge = TextStyle(
            fontFamily = FontFamily(Font(Res.font.Inter_Bold, FontWeight.Bold))
        )
    )
}

// Async resource loading (for files)
@Composable
fun ConfigLoader() {
    var config by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(Unit) {
        config = Res.readBytes("files/config.json").decodeToString()
    }
}
```

## Theme

### Color Scheme

```kotlin
// core/ui/src/commonMain/kotlin/theme/Theme.kt
private val DarkColorScheme = darkColorScheme(
    primary = Color(0xFF6200EE),
    onPrimary = Color.White,
    secondary = Color(0xFF03DAC6),
    onSecondary = Color.Black,
    background = Color(0xFF121212),
    surface = Color(0xFF1E1E1E),
    error = Color(0xFFCF6679)
)

private val LightColorScheme = lightColorScheme(
    primary = Color(0xFF6200EE),
    onPrimary = Color.White,
    secondary = Color(0xFF03DAC6),
    onSecondary = Color.Black,
    background = Color(0xFFFAFAFA),
    surface = Color.White,
    error = Color(0xFFB00020)
)

@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme

    MaterialTheme(
        colorScheme = colorScheme,
        typography = AppTypography,
        shapes = AppShapes,
        content = content
    )
}
```

### Typography

```kotlin
// core/ui/src/commonMain/kotlin/theme/Type.kt
val AppTypography = Typography(
    displayLarge = TextStyle(
        fontFamily = FontFamily(Font(Res.font.Inter_Bold)),
        fontSize = 57.sp,
        lineHeight = 64.sp
    ),
    headlineMedium = TextStyle(
        fontFamily = FontFamily(Font(Res.font.Inter_Bold)),
        fontSize = 28.sp,
        lineHeight = 36.sp
    ),
    bodyLarge = TextStyle(
        fontFamily = FontFamily(Font(Res.font.Inter_Regular)),
        fontSize = 16.sp,
        lineHeight = 24.sp
    ),
    labelLarge = TextStyle(
        fontFamily = FontFamily(Font(Res.font.Inter_Regular)),
        fontSize = 14.sp,
        lineHeight = 20.sp,
        fontWeight = FontWeight.Medium
    )
)
```

### Shapes

```kotlin
// core/ui/src/commonMain/kotlin/theme/Shapes.kt
val AppShapes = Shapes(
    extraSmall = RoundedCornerShape(4.dp),
    small = RoundedCornerShape(8.dp),
    medium = RoundedCornerShape(12.dp),
    large = RoundedCornerShape(16.dp),
    extraLarge = RoundedCornerShape(24.dp)
)
```

## Component Patterns

### Base Component

```kotlin
// core/ui/src/commonMain/kotlin/components/AppButton.kt
@Composable
fun AppButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    loading: Boolean = false,
    style: ButtonStyle = ButtonStyle.Primary
) {
    Button(
        onClick = onClick,
        modifier = modifier.height(48.dp),
        enabled = enabled && !loading,
        colors = when (style) {
            ButtonStyle.Primary -> ButtonDefaults.buttonColors()
            ButtonStyle.Secondary -> ButtonDefaults.outlinedButtonColors()
            ButtonStyle.Destructive -> ButtonDefaults.buttonColors(
                containerColor = MaterialTheme.colorScheme.error
            )
        }
    ) {
        if (loading) {
            CircularProgressIndicator(
                modifier = Modifier.size(20.dp),
                strokeWidth = 2.dp
            )
        } else {
            Text(text)
        }
    }
}

enum class ButtonStyle { Primary, Secondary, Destructive }
```

### Card Component

```kotlin
@Composable
fun AppCard(
    modifier: Modifier = Modifier,
    onClick: (() -> Unit)? = null,
    content: @Composable ColumnScope.() -> Unit
) {
    val cardModifier = if (onClick != null) {
        modifier.clickable(onClick = onClick)
    } else {
        modifier
    }

    Card(
        modifier = cardModifier,
        shape = MaterialTheme.shapes.medium,
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surface
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            content = content
        )
    }
}
```

### Loading State Component

```kotlin
@Composable
fun LoadingContent(
    isLoading: Boolean,
    modifier: Modifier = Modifier,
    loadingContent: @Composable () -> Unit = { DefaultLoadingIndicator() },
    content: @Composable () -> Unit
) {
    Box(modifier = modifier) {
        if (isLoading) {
            loadingContent()
        } else {
            content()
        }
    }
}

@Composable
private fun DefaultLoadingIndicator() {
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        CircularProgressIndicator()
    }
}
```

### Error State Component

```kotlin
@Composable
fun ErrorContent(
    message: String,
    onRetry: (() -> Unit)? = null,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Icon(
            imageVector = Icons.Default.Warning,
            contentDescription = null,
            modifier = Modifier.size(48.dp),
            tint = MaterialTheme.colorScheme.error
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = message,
            style = MaterialTheme.typography.bodyLarge,
            textAlign = TextAlign.Center
        )

        if (onRetry != null) {
            Spacer(modifier = Modifier.height(24.dp))

            AppButton(
                text = stringResource(Res.string.retry),
                onClick = onRetry
            )
        }
    }
}
```

## Screen Pattern

```kotlin
// feature/home/impl/src/commonMain/kotlin/HomeScreen.kt
@Composable
fun HomeScreen(
    component: HomeComponent,
    modifier: Modifier = Modifier
) {
    val state by component.state.subscribeAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(stringResource(Res.string.home_title)) }
            )
        },
        modifier = modifier
    ) { paddingValues ->
        Box(modifier = Modifier.padding(paddingValues)) {
            when (val currentState = state) {
                is HomeState.Loading -> LoadingContent(isLoading = true) {}
                is HomeState.Error -> ErrorContent(
                    message = currentState.message,
                    onRetry = component::retry
                )
                is HomeState.Success -> HomeContent(
                    data = currentState.data,
                    onItemClick = component::onItemClick
                )
            }
        }
    }
}

@Composable
private fun HomeContent(
    data: List<HomeItem>,
    onItemClick: (HomeItem) -> Unit
) {
    LazyColumn(
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(data, key = { it.id }) { item ->
            HomeItemCard(
                item = item,
                onClick = { onItemClick(item) }
            )
        }
    }
}
```

## Platform Adaptations

### Safe Area Handling

```kotlin
@Composable
fun SafeAreaScreen(content: @Composable () -> Unit) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .windowInsetsPadding(WindowInsets.safeDrawing)
    ) {
        content()
    }
}

// Or in Scaffold
Scaffold(
    contentWindowInsets = WindowInsets.safeDrawing
) { paddingValues ->
    // Content
}
```

### Platform-Specific UI

```kotlin
@Composable
expect fun BackHandler(enabled: Boolean, onBack: () -> Unit)

// androidMain
@Composable
actual fun BackHandler(enabled: Boolean, onBack: () -> Unit) {
    androidx.activity.compose.BackHandler(enabled = enabled, onBack = onBack)
}

// iosMain (no back handler on iOS)
@Composable
actual fun BackHandler(enabled: Boolean, onBack: () -> Unit) {
    // No-op on iOS
}

// desktopMain
@Composable
actual fun BackHandler(enabled: Boolean, onBack: () -> Unit) {
    // Handle keyboard shortcut or window close
}
```

### Adaptive Layout

```kotlin
@Composable
fun AdaptiveLayout(
    compactContent: @Composable () -> Unit,
    expandedContent: @Composable () -> Unit
) {
    BoxWithConstraints {
        if (maxWidth < 600.dp) {
            compactContent()
        } else {
            expandedContent()
        }
    }
}

// Usage
AdaptiveLayout(
    compactContent = { PhoneLayout() },
    expandedContent = { TabletLayout() }
)
```

## Entry Points

### Android

```kotlin
// composeApp/src/androidMain/kotlin/MainActivity.kt
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val rootComponent = DefaultRootComponent(
            componentContext = defaultComponentContext()
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
// composeApp/src/iosMain/kotlin/MainViewController.kt
fun MainViewController(): UIViewController {
    return ComposeUIViewController {
        val rootComponent = remember {
            DefaultRootComponent(
                componentContext = DefaultComponentContext(
                    lifecycle = ApplicationLifecycle()
                )
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
// composeApp/src/desktopMain/kotlin/Main.kt
fun main() = application {
    val lifecycle = LifecycleRegistry()
    val rootComponent = runOnUiThread {
        DefaultRootComponent(
            componentContext = DefaultComponentContext(lifecycle)
        )
    }

    Window(
        onCloseRequest = ::exitApplication,
        title = "My Application"
    ) {
        LifecycleController(lifecycle)

        AppTheme {
            RootContent(component = rootComponent)
        }
    }
}
```

### Web (WASM)

```kotlin
// composeApp/src/wasmJsMain/kotlin/Main.kt
fun main() {
    val lifecycle = LifecycleRegistry()

    val rootComponent = DefaultRootComponent(
        componentContext = DefaultComponentContext(lifecycle)
    )

    CanvasBasedWindow(canvasElementId = "ComposeTarget") {
        AppTheme {
            RootContent(component = rootComponent)
        }
    }
}
```

## Best Practices

### Do's
- Use Material3 components and theme
- Keep composables stateless when possible
- Use `remember` and `derivedStateOf` for performance
- Extract reusable components to core:ui
- Use string resources for all user-visible text
- Handle all UI states (loading, error, empty, success)
- Use WindowInsets for safe areas

### Don'ts
- Don't use hardcoded colors or dimensions
- Don't put business logic in composables
- Don't ignore preview annotations
- Don't skip accessibility (contentDescription)
- Don't use platform-specific APIs directly in common code
- Don't create composables with side effects without LaunchedEffect

## Previews

```kotlin
@Preview
@Composable
private fun AppButtonPreview() {
    AppTheme {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            AppButton(text = "Primary", onClick = {})
            AppButton(text = "Loading", onClick = {}, loading = true)
            AppButton(text = "Disabled", onClick = {}, enabled = false)
            AppButton(text = "Destructive", onClick = {}, style = ButtonStyle.Destructive)
        }
    }
}
```

## Resources

- [Compose Multiplatform](https://www.jetbrains.com/compose-multiplatform/)
- [Resources API](https://www.jetbrains.com/help/kotlin-multiplatform-dev/compose-multiplatform-resources.html)
- [Material3 Components](https://developer.android.com/develop/ui/compose/components)
