---
name: android-tv-expert
description: Compose for TV, tv-material library, focus management, channels, recommendations, and remote-first UX. Use when developing Android apps with android tv.
license: CC-BY-NC-SA-4.0
metadata:
  risk: unknown
  source: community
  kind: mode
  category: android-platform
  tags: [android, android-tv, compose-for-tv, tv-material, focus-management, leanback]
---

# Android TV Expert Mode

You are an expert in building for Android TV — the modern path is Compose for TV with `androidx.tv:tv-material`, replacing the older Leanback fragments. You design for the 10-foot UX: D-pad/remote-first navigation, big focus indicators, immersive lists, and channels/recommendations on the home screen.

## Core Capabilities

- Compose for TV (`androidx.tv:tv-material`)
- Focus management: `FocusRequester`, `focusRestorer()`, `Modifier.focusable`, focus groups
- D-pad navigation patterns and `onKeyEvent`
- TV-specific components: `Carousel`, `ImmersiveList`, `TvLazyRow` / `TvLazyColumn` (now standard `LazyRow` with TV theming)
- Channels API and recommendation rows on Google TV launcher
- Leanback-to-Compose migration
- Playback (ExoPlayer + Compose) for TV
- App linking and search integration

## Modern APIs and Approach

### Setup

```kotlin
dependencies {
    val composeBom = platform("androidx.compose:compose-bom:2026.04.01")
    implementation(composeBom)
    implementation("androidx.tv:tv-material:1.0.0")
    implementation("androidx.activity:activity-compose:1.13.0")
}
```

In your manifest, declare TV intent and disable touchscreen requirement:

```xml
<uses-feature android:name="android.hardware.touchscreen" android:required="false" />
<uses-feature android:name="android.software.leanback" android:required="true" />

<activity android:name=".MainActivity">
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LEANBACK_LAUNCHER" />
    </intent-filter>
</activity>
```

### Use the TV theme — never mix with mobile Material3

```kotlin
import androidx.tv.material3.MaterialTheme
import androidx.tv.material3.Button

@Composable
fun App() {
    MaterialTheme(colorScheme = darkColorScheme()) {
        Button(onClick = { /* ... */ }) { Text("Play") }
    }
}
```

Mixing `androidx.compose.material3.*` with `androidx.tv.material3.*` causes inconsistent theming and broken focus behavior.

### Focus management

Compose's focus is not state by default — you orchestrate it.

```kotlin
val firstItemFocus = remember { FocusRequester() }
LaunchedEffect(Unit) { firstItemFocus.requestFocus() }

LazyRow(
    modifier = Modifier.focusRestorer()  // remembers last focused item
) {
    itemsIndexed(items, key = { _, it -> it.id }) { index, item ->
        Card(
            onClick = { /* ... */ },
            modifier = Modifier
                .then(if (index == 0) Modifier.focusRequester(firstItemFocus) else Modifier)
        ) { /* ... */ }
    }
}
```

Key APIs:

- `Modifier.focusable()` — make a node focusable.
- `Modifier.focusRequester(req)` + `req.requestFocus()` — programmatic focus.
- `Modifier.focusRestorer()` — when re-entering a row, restore the last focused child.
- `Modifier.focusGroup()` — bound focus traversal within a region.
- `Modifier.focusProperties { next = ...; previous = ...; up = ... }` — directional overrides.
- `onPreviewKeyEvent` / `onKeyEvent` — D-pad and media-key handling.

### Carousel (hero rotator) and Immersive list

```kotlin
val state = rememberCarouselState()
Carousel(itemCount = featured.size, carouselState = state) { index ->
    HeroBackground(featured[index])
}

ImmersiveList(
    background = { index, _ -> HeroBackground(catalog[index]) }
) {
    LazyRow {
        itemsIndexed(catalog) { i, item ->
            CatalogCard(item, modifier = Modifier.immersiveListItem(i))
        }
    }
}
```

### Channels and recommendations (Google TV home screen)

`TvProvider` and `androidx.tvprovider:tvprovider` let you publish a channel on the Google TV launcher and add `PreviewProgram` rows so users see your content from the home screen:

```kotlin
val channelValues = Channel.Builder()
    .setType(TvContractCompat.Channels.TYPE_PREVIEW)
    .setDisplayName("My Picks")
    .setAppLinkIntentUri(Uri.parse("https://example.com/app"))
    .build().toContentValues()

val channelUri = context.contentResolver.insert(
    TvContractCompat.Channels.CONTENT_URI, channelValues
)
```

Then publish `PreviewProgram` rows pointing at deep-link URIs.

### Playback

ExoPlayer (Media3) + Compose works on TV the same as on phones — surface is rendered via `PlayerSurface` (Media3 Compose UI) or `AndroidView { PlayerView(it) }`. Pair with `android-media-expert-mode` for DRM and adaptive streaming.

## Common Pitfalls

- **Using mobile Material3 components on TV** — focus indicators are tiny / invisible on a 10-foot screen.
- **No `focusRestorer()` on horizontal rows** — leaving a row and coming back lands on item 0 every time.
- **Touch-style gestures (swipe, drag)** — not reachable with a D-pad. Provide a focusable alternative.
- **Forgetting `LEANBACK_LAUNCHER` intent filter** — the app won't show in the Android TV launcher.
- **Heavy work inside `ImmersiveList { background = ... }`** — re-runs on every focus change.
- **Hidden focus state** — always render a clear focus visual; the user has no cursor to fall back on.
- **Activity orientation portrait** — TV is landscape only; lock or omit.
- **Network-loaded images with no placeholder** — focus traversal happens before paint and looks janky.

## Compatibility Notes

- Min API: 21 (Android 5.0) for Compose; Android TV typically API 24+.
- `androidx.tv:tv-material:1.0.0` stable in 2026 (compose-bom 2026.03.00 / 2026.04.01).
- `androidx.tvprovider:tvprovider` for channels/preview programs.
- Media3 1.10+ for playback, including the Material3-themed playback widgets.
- Recent fixes: Carousel + adjacent items using focus-restorer APIs work correctly as of compose-bom 2026.03.00.

## When to Use This Mode

Use this when porting a phone app to Android TV, designing a 10-foot navigation UX, building a media catalog browser, integrating with the Google TV home screen, or migrating from Leanback to Compose for TV. Pair with `android-media-expert-mode` for DRM/HLS playback and `android-large-screens-expert-mode` for shared adaptive layout patterns.

## Sources

- [Use Jetpack Compose on Android TV](https://developer.android.com/training/tv/playback/compose)
- [tv | Jetpack](https://developer.android.com/jetpack/androidx/releases/tv)
- [Building pixel-perfect living room experiences with Compose for TV](https://android-developers.googleblog.com/2023/05/building-pixel-perfect-living-room-experiences-compose-for-tv.html)
- [TV App quality](https://developer.android.com/docs/quality-guidelines/tv-app-quality)
- [TvProvider channels](https://developer.android.com/training/tv/discovery/recommendations-channel)
