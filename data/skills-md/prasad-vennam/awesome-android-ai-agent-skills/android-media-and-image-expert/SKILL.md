---
name: android-media-and-image-expert
description: "Use when loading images with Coil/Glide, implementing video playback with Media3/ExoPlayer, or handling media metadata in Android."
category: ui-ux
risk: low
source: community
date_added: "2026-03-31"
metadata:
  triggers:
    - "@android-media"
    - "coil-loading"
    - "video-playback"
    - "media3-exoplayer"
    - "image-compression"
    - "bitmap-scaling"
---

# Android Media & Image Excellence 🎞️🖼️

Professional strategies for high-performance image loading, video streaming, and media management in modern Android applications.

## ⚡ When to Use
- **Image Loading**: Performance-first loading with Coil (Compose-native).
- **Video Playback**: Streaming using ExoPlayer or the new Media3 library.
- **Media Management**: Displaying local media (Photos/Videos) with proper metadata.
- **Image Optimization**: Sizing, Caching, and format support (WebP, AVIF).
- **Audio Playback**: Playing background music or voice notes.

## 🖼️ Image Loading with Coil (The Android Standard)

- **Rule**: ALWAYS use **Coil** for Compose. It's lightweight, efficient, and uses Coroutines.
- **Rule**: NEVER load the full image if displayed in a small box. Use `size(Size.ORIGINAL)` or explicit `size()`.

### 1. The `AsyncImage` Composable
```kotlin
AsyncImage(
    model = ImageRequest.Builder(LocalContext.current)
        .data(url)
        .crossfade(true)
        .placeholder(R.drawable.loading)
        .error(R.drawable.error)
        .build(),
    contentDescription = null,
    modifier = Modifier.clip(CircleShape)
)
```

### 2. Best Practices
- [ ] **Disk Caching**: Ensure `ImageLoader` is configured to cache properly.
- [ ] **Memory Caching**: Control cache size for apps with many images.
- [ ] **SVGs**: Use `SvgDecoder` for sharp, vector-based illustrations.

## 🎥 Video Playback (Media3 / ExoPlayer)

- **Rule**: Use the **Media3** library as the modern wrapper for ExoPlayer.
- **Lifecycle**: Ensure the player is released in `onDispose` to avoid memory leaks and battery drain.

### 1. Basic Player Setup
```kotlin
val exoPlayer = remember {
    ExoPlayer.Builder(context).build().apply {
        setMediaItem(MediaItem.fromUri(url))
        prepare()
    }
}

AndroidView(
    factory = { ctx ->
        PlayerView(ctx).apply {
            player = exoPlayer
        }
    },
    update = { _ -> },
    modifier = Modifier.fillMaxWidth()
)
```

## 🚀 Media Optimization Checklist

- [ ] **Format Support**: Prefer **WebP** or **AVIF** over JPEG for small payloads.
- [ ] **Bitmap Downsampling**: Only load the necessary resolution into memory.
- [ ] **Hardware Acceleration**: Enable hardware decoding for 4K/HDR videos.
- [ ] **Placeholder strategy**: Use unified placeholders for a smoother UI.

## 📏 UI Performance & UX

- **Shimmer Loading**: Use a themed shimmer effect (skeleton) while media is loading.
- **Error States**: Always provide a "Retry" button or clear error icon for failed media.
- **Audio Focus**: Ensure your app respects other audio sources (Pause media when music starts elsewhere).

## 🧪 Testing and Verification

- **Slow Network Testing**: Use ADB or a proxy to test UI behavior under poor network conditions.
- **Memory Profiler**: Verify that media is being cleared from the heap when screens are closed.
- **Accessibility**: Provide `contentDescription` for all meaningful images.

## 🔗 Related Resources
- [Android Media3 Guide](https://developer.android.com/guide/topics/media/media3)
- [Coil Documentation](https://coil-kt.github.io/coil/)
- [Image Optimization FAQ](https://developer.android.com/topic/performance/graphics)
