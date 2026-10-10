---
name: m3-web-android
description: Implement Material Design 3 in Android using Jetpack Compose Material 3. Covers theme setup, dynamic color (Material You), M3 Expressive components, and Compose integration. Use this when building M3-styled native Android applications.
license: Apache-2.0
---

# Material Design 3 — Android / Jetpack Compose

## Overview

Jetpack Compose has the most complete M3 implementation, including M3 Expressive components. Full dynamic color (Material You) support on Android 12+.

**Keywords**: Material Design 3, M3, Android, Jetpack Compose, Material You, dynamic color, Kotlin, Material 3 Compose, M3 Expressive

## When to Use

- Native Android development
- When you need the most complete M3 implementation
- Projects targeting Android 12+ that want dynamic color (Material You)
- When M3 Expressive components are needed (Android 16+)

## Install

```kotlin
// build.gradle
implementation("androidx.compose.material3:material3:1.4.0")
```

## Theme Setup

```kotlin
@Composable
fun MyAppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context)
            else dynamicLightColorScheme(context)
        }
        darkTheme -> darkColorScheme(
            primary = Color(0xFFD0BCFF),
            secondary = Color(0xFFCCC2DC),
            tertiary = Color(0xFFEFB8C8),
        )
        else -> lightColorScheme(
            primary = Color(0xFF6750A4),
            secondary = Color(0xFF625B71),
            tertiary = Color(0xFF7D5260),
        )
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        shapes = Shapes,
        content = content,
    )
}
```

## Component Examples

### Buttons

```kotlin
Button(onClick = { }) { Text("Filled") }
OutlinedButton(onClick = { }) { Text("Outlined") }
TextButton(onClick = { }) { Text("Text") }
FilledTonalButton(onClick = { }) { Text("Tonal") }
ElevatedButton(onClick = { }) { Text("Elevated") }
```

### Cards

```kotlin
Card(
    modifier = Modifier.fillMaxWidth(),
    elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text("Title", style = MaterialTheme.typography.titleMedium)
        Text("Content", style = MaterialTheme.typography.bodyMedium)
    }
}
```

### Text Fields

```kotlin
OutlinedTextField(
    value = text,
    onValueChange = { text = it },
    label = { Text("Email") },
)

TextField(
    value = text,
    onValueChange = { text = it },
    label = { Text("Name") },
)
```

### Navigation

```kotlin
NavigationBar {
    NavigationBarItem(
        icon = { Icon(Icons.Filled.Home, contentDescription = "Home") },
        label = { Text("Home") },
        selected = selectedItem == 0,
        onClick = { selectedItem = 0 },
    )
    NavigationBarItem(
        icon = { Icon(Icons.Filled.Search, contentDescription = "Search") },
        label = { Text("Search") },
        selected = selectedItem == 1,
        onClick = { selectedItem = 1 },
    )
}
```

### FAB

```kotlin
FloatingActionButton(onClick = { }) {
    Icon(Icons.Filled.Add, contentDescription = "Add")
}

ExtendedFloatingActionButton(
    onClick = { },
    icon = { Icon(Icons.Filled.Add, contentDescription = "Add") },
    text = { Text("Create") },
)
```

## M3 Expressive Components (Android 16+)

```kotlin
// Available in material3 1.4.0+
ExpressiveButton(onClick = { }) { Text("Expressive") }
SplitButton(onClick = { }, menuItems = { /* ... */ }) { Text("Split") }
FloatingToolbar { /* toolbar items */ }
FABMenu { /* FAB menu items */ }
```

## Checklist

- [ ] `MaterialTheme` wrapping applied at app root
- [ ] Dynamic color used on Android 12+ with fallback color scheme
- [ ] Both light and dark color schemes defined
- [ ] Typography uses `MaterialTheme.typography` accessors
- [ ] Shapes use `MaterialTheme.shapes` or `Shapes` class
- [ ] Components use Material 3 Compose variants
- [ ] M3 Expressive components used where appropriate (Android 16+)

## Resources

- Guide: https://developer.android.com/develop/ui/compose/designsystems/material3
- M3 Compose: https://m3.material.io/develop/android/jetpack-compose
- Compose Material 3 releases: https://developer.android.com/jetpack/androidx/releases/compose-material3
- Codelab: https://developer.android.com/codelabs/jetpack-compose-theming
