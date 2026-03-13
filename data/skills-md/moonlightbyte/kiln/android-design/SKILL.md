---
name: android-design
description: |
  This skill should be used when the user asks to "audit Android code", "review Jetpack Compose",
  "check Material Design compliance", "critique Compose design", "verify M3 guidelines",
  "audit Compose screen", "review Material 3", "check M3 compliance", "validate Android UI",
  "fix Compose anti-patterns", "improve Compose performance", "review Android screen",
  "audit Kotlin UI", "check touch targets", "verify accessibility Android",
  or mentions "Material Design 3", "M3", "Jetpack Compose", "Android UI", "Compose patterns",
  "recomposition", "Compose stability", "Android accessibility", "WCAG Android".

  This skill should also be used when the user reports symptoms like "Why is my list lagging?",
  "Scroll is jittery", "Make this look native", "The notch is covering my UI",
  "Build a settings screen", "My Compose is slow", "Recomposition issues",
  or "Screen feels sluggish".

  Provides comprehensive Material Design 3 specifications, Compose anti-patterns database,
  typography scale, color system, touch targets, and severity-based audit checklists.
license: MIT
user-invocable: true
references:
  - ./reference/material-design-3.md
  - ./reference/compose-antipatterns.md
  - ./reference/compose-rules-integration.md
  - ./reference/compiler-metrics-guide.md
  - ./reference/now-in-android-patterns.md
  - ./reference/INTEGRATION_GUIDE.md
---

# Android Design Skill

Expert knowledge of Material Design 3 for Jetpack Compose applications. This skill enforces design excellence, accessibility compliance, and performance best practices.

## Core Principles

### 1. Material Design 3 Foundation
- Use semantic tokens, not hardcoded values
- Apply dynamic color for Android 12+
- Follow M3 shape scale (4dp extraSmall to 28dp extraLarge)
- Use elevation levels (0dp to 5 levels)

### 2. Accessibility First
- Minimum 48x48dp touch targets
- 4.5:1 contrast ratio for normal text
- Proper `contentDescription` on all interactive elements
- Support `fontScale` up to 200%

### 3. Performance Stability
- Mark data classes `@Immutable` or `@Stable`
- Use `remember` and `derivedStateOf` correctly
- Prefer `LazyColumn` over `Column` for lists
- Provide stable keys for list items

---

## Typography Scale (15 Styles)

| Token | Size | Line Height | Weight | Use Case |
|-------|------|-------------|--------|----------|
| `displayLarge` | 57sp | 64sp | 400 | Hero headlines |
| `displayMedium` | 45sp | 52sp | 400 | Page titles |
| `displaySmall` | 36sp | 44sp | 400 | Section headers |
| `headlineLarge` | 32sp | 40sp | 400 | Card titles |
| `headlineMedium` | 28sp | 36sp | 400 | Dialog titles |
| `headlineSmall` | 24sp | 32sp | 400 | List headers |
| `titleLarge` | 22sp | 28sp | 400 | App bar titles |
| `titleMedium` | 16sp | 24sp | 500 | Tab labels |
| `titleSmall` | 14sp | 20sp | 500 | Chip labels |
| `bodyLarge` | 16sp | 24sp | 400 | Body text |
| `bodyMedium` | 14sp | 20sp | 400 | Secondary text |
| `bodySmall` | 12sp | 16sp | 400 | Captions |
| `labelLarge` | 14sp | 20sp | 500 | Buttons |
| `labelMedium` | 12sp | 16sp | 500 | Small buttons |
| `labelSmall` | 11sp | 16sp | 500 | Badges |

### Usage Pattern
```kotlin
// GOOD - Semantic tokens
Text(
    text = "Welcome",
    style = MaterialTheme.typography.headlineLarge
)

// BAD - Hardcoded values
Text(
    text = "Welcome",
    fontSize = 32.sp,
    fontWeight = FontWeight.Normal
)
```

---

## Color System

### Key Colors (5 Primary)
1. **Primary** - Brand color, interactive elements
2. **Secondary** - Less prominent UI
3. **Tertiary** - Accents, special elements
4. **Error** - Error states
5. **Neutral** - Surfaces, backgrounds

### Tonal Palettes (13 Tones)
Each key color generates: 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99, 100

### Usage Pattern
```kotlin
// GOOD - Semantic tokens
Surface(color = MaterialTheme.colorScheme.surface) {
    Text(
        text = "Hello",
        color = MaterialTheme.colorScheme.onSurface
    )
}

// BAD - Hardcoded colors
Surface(color = Color(0xFFFAFAFA)) {
    Text(
        text = "Hello",
        color = Color.Black
    )
}
```

### Dynamic Color (Android 12+)
```kotlin
val colorScheme = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
    if (darkTheme) dynamicDarkColorScheme(context)
    else dynamicLightColorScheme(context)
} else {
    if (darkTheme) DarkColorScheme
    else LightColorScheme
}
```

---

## Shape Scale

| Token | Radius | Use Case |
|-------|--------|----------|
| `extraSmall` | 4dp | Badges, chips |
| `small` | 8dp | Small cards, buttons |
| `medium` | 12dp | Cards, dialogs |
| `large` | 16dp | Large sheets |
| `extraLarge` | 28dp | FABs, full sheets |

---

## Touch Targets

### Requirements
- **Minimum**: 48x48dp (M3 requirement)
- **Recommended**: 48x48dp with 8dp spacing
- **WCAG 2.2**: 24x24 CSS px minimum (Level AA)

### Implementation
```kotlin
// GOOD - Proper touch target
IconButton(
    onClick = { /* action */ },
    modifier = Modifier.minimumInteractiveComponentSize()
) {
    Icon(
        imageVector = Icons.Default.Close,
        contentDescription = "Close dialog"
    )
}

// BAD - No touch target guarantee
Icon(
    imageVector = Icons.Default.Close,
    modifier = Modifier
        .size(24.dp)
        .clickable { /* action */ }
)
```

---

## Spacing Scale

Base unit: 4dp

| Size | dp | Use Case |
|------|-----|----------|
| xs | 4dp | Inline spacing |
| sm | 8dp | Related elements |
| md | 12dp | Group spacing |
| lg | 16dp | Section spacing |
| xl | 24dp | Major divisions |
| 2xl | 32dp | Page margins |
| 3xl | 48dp | Large gaps |
| 4xl | 64dp | Hero spacing |

---

## DO / DON'T

### State Management

**DO**: Hoist state to appropriate level
```kotlin
@Composable
fun SearchScreen(viewModel: SearchViewModel = viewModel()) {
    val query by viewModel.searchQuery.collectAsState()
    SearchBar(query = query, onQueryChange = viewModel::updateQuery)
}
```

**DON'T**: Create state in leaf composables
```kotlin
@Composable
fun SearchBar() {
    var query by remember { mutableStateOf("") } // Can't test, can't share
    TextField(value = query, onValueChange = { query = it })
}
```

### Modifiers

**DO**: Create modifiers outside composable body
```kotlin
private val cardModifier = Modifier
    .fillMaxWidth()
    .padding(16.dp)

@Composable
fun MyCard() {
    Card(modifier = cardModifier) { /* content */ }
}
```

**DON'T**: Create modifiers inside composition
```kotlin
@Composable
fun MyCard() {
    Card(
        modifier = Modifier // Creates new object every recomposition
            .fillMaxWidth()
            .padding(16.dp)
    ) { /* content */ }
}
```

### Collections

**DO**: Use immutable collections for stable recomposition
```kotlin
@Immutable
data class UiState(
    val items: ImmutableList<Item> = persistentListOf()
)
```

**DON'T**: Use mutable collections in state
```kotlin
data class UiState(
    val items: List<Item> = emptyList() // Unstable!
)
```

### LazyColumn Keys

**DO**: Provide stable keys
```kotlin
LazyColumn {
    items(items, key = { it.id }) { item ->
        ItemRow(item)
    }
}
```

**DON'T**: Rely on index-based keys
```kotlin
LazyColumn {
    items(items.size) { index -> // Breaks on reorder
        ItemRow(items[index])
    }
}
```

---

## Severity Levels

When auditing, classify issues as:

| Level | Icon | Description | Example |
|-------|------|-------------|---------|
| **Critical** | 🔴 | Blocks accessibility or causes crashes | Missing contentDescription |
| **Important** | 🟠 | Violates M3 guidelines or hurts UX | Touch target < 48dp |
| **Warning** | 🟡 | Suboptimal but functional | Hardcoded color |
| **Suggestion** | 🔵 | Polish opportunities | Non-standard spacing |

---

## References

For detailed specifications, see:
- [Material Design 3 Foundation](./reference/material-design-3.md)
- [Compose Anti-Patterns Database](./reference/compose-antipatterns.md)
- [Compose Rules Integration](./reference/compose-rules-integration.md)
- [Compiler Metrics Guide](./reference/compiler-metrics-guide.md)
- [Now in Android Patterns](./reference/now-in-android-patterns.md)
- [Integration Guide](./reference/INTEGRATION_GUIDE.md)
