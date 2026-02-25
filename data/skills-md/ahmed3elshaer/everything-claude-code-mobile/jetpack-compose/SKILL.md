---
name: jetpack-compose
description: Jetpack Compose patterns for declarative UI, state management, theming, animations, and performance optimization.
---

# Jetpack Compose Patterns

Modern declarative UI patterns for Android.

## State Management

### State Hoisting

```kotlin
// ✅ CORRECT: Stateless composable
@Composable
fun Counter(
    count: Int,
    onIncrement: () -> Unit,
    modifier: Modifier = Modifier
) {
    Row(modifier = modifier) {
        Text("Count: $count")
        Button(onClick = onIncrement) {
            Text("+")
        }
    }
}

// Parent owns state
@Composable
fun CounterScreen() {
    var count by rememberSaveable { mutableStateOf(0) }
    
    Counter(
        count = count,
        onIncrement = { count++ }
    )
}
```

### Remember Variants

```kotlin
// remember - Survives recomposition
val alpha by remember { mutableStateOf(1f) }

// rememberSaveable - Survives config change
var count by rememberSaveable { mutableStateOf(0) }

// remember with key - Resets on key change
val animation = remember(itemId) { Animatable(0f) }

// derivedStateOf - Computed, updates only when result changes
val isValid by remember {
    derivedStateOf { email.isNotBlank() && password.length >= 8 }
}
```

## Composition Patterns

### Slot API

```kotlin
@Composable
fun AppBar(
    title: @Composable () -> Unit,
    navigationIcon: @Composable () -> Unit = {},
    actions: @Composable RowScope.() -> Unit = {}
) {
    TopAppBar(
        title = { title() },
        navigationIcon = { navigationIcon() },
        actions = actions
    )
}

// Usage
AppBar(
    title = { Text("Home") },
    navigationIcon = { IconButton(onClick = {}) { Icon(Icons.Default.Menu, null) } },
    actions = {
        IconButton(onClick = {}) { Icon(Icons.Default.Search, null) }
    }
)
```

### Modifier Pattern

```kotlin
@Composable
fun CustomButton(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,  // First optional parameter
    enabled: Boolean = true,
    content: @Composable RowScope.() -> Unit
) {
    Button(
        onClick = onClick,
        modifier = modifier,  // Apply modifier first
        enabled = enabled,
        content = content
    )
}
```

## Side Effects

### LaunchedEffect

```kotlin
@Composable
fun HomeScreen(viewModel: HomeViewModel) {
    // Runs once
    LaunchedEffect(Unit) {
        viewModel.loadData()
    }
    
    // Runs when key changes
    LaunchedEffect(userId) {
        viewModel.loadUser(userId)
    }
}
```

### DisposableEffect

```kotlin
@Composable
fun LifecycleObserver(onResume: () -> Unit) {
    val lifecycleOwner = LocalLifecycleOwner.current
    
    DisposableEffect(lifecycleOwner) {
        val observer = LifecycleEventObserver { _, event ->
            if (event == Lifecycle.Event.ON_RESUME) onResume()
        }
        lifecycleOwner.lifecycle.addObserver(observer)
        
        onDispose {
            lifecycleOwner.lifecycle.removeObserver(observer)
        }
    }
}
```

## Theming

### Material 3

```kotlin
@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme
    
    MaterialTheme(
        colorScheme = colorScheme,
        typography = AppTypography,
        content = content
    )
}

// Usage
val backgroundColor = MaterialTheme.colorScheme.surface
val textStyle = MaterialTheme.typography.bodyLarge
```

## Lists

### LazyColumn

```kotlin
LazyColumn {
    items(
        items = users,
        key = { it.id }  // Critical for performance
    ) { user ->
        UserItem(user = user)
    }
}
```

## Animations

### Animate Values

```kotlin
val alpha by animateFloatAsState(
    targetValue = if (visible) 1f else 0f,
    animationSpec = tween(durationMillis = 300)
)

val size by animateDpAsState(
    targetValue = if (expanded) 200.dp else 100.dp
)
```

### AnimatedContent

```kotlin
AnimatedContent(
    targetState = state,
    transitionSpec = {
        fadeIn() togetherWith fadeOut()
    }
) { targetState ->
    when (targetState) {
        is Loading -> LoadingContent()
        is Success -> SuccessContent(targetState.data)
        is Error -> ErrorContent()
    }
}
```

---

**Remember**: Compose is declarative. Describe the UI, don't command it.
