---
name: lsfg-android-frame-generation
description: Skill for building, configuring, and extending LSFG-Android — a Vulkan frame-generation overlay for Android using lsfg-vk via MediaProjection capture.
triggers:
  - "add frame generation to Android"
  - "build LSFG Android app"
  - "configure LSFG overlay settings"
  - "integrate lsfg-vk on Android"
  - "set up MediaProjection frame interpolation"
  - "troubleshoot LSFG Android overlay"
  - "add Shizuku timing to LSFG"
  - "customize LSFG Android render pipeline"
---

# LSFG-Android Frame Generation Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

LSFG-Android ports the [`lsfg-vk`](https://github.com/PancakeTAS/lsfg-vk) Vulkan frame-generation pipeline to Android. Because Android 12+ blocks external code injection into non-debuggable processes, the app captures the screen via `MediaProjection`, runs LSFG interpolation on-GPU using `AHardwareBuffer` sharing, and composites generated frames into a `SYSTEM_ALERT_WINDOW` or `TYPE_ACCESSIBILITY_OVERLAY` sitting above the target game.

---

## Repository Layout

```
LSFG-Android/          # Android Studio project (Kotlin + Compose + JNI/C++)
lsfg-vk-android/       # Submodule: lsfg-vk 1.0.0 + Android patches (#ifdef __ANDROID__)
```

Both folders **must** be siblings on disk — the CMake path `../../../../../lsfg-vk-android` from inside the JNI sources is hard-coded.

---

## Prerequisites

| Tool | Version |
|------|---------|
| Android Studio | Ladybug or newer |
| NDK | 27.0.12077973 |
| CMake | 3.22.1 |
| JDK | 17 |
| C++ standard | C++20 |
| minSdk | 29 (Android 10) |
| targetSdk | 35 (Android 15) |
| ABIs | `arm64-v8a` (production), `x86_64` (emulator) |

---

## Build & Install

```sh
# Clone with submodule
git clone --recurse-submodules https://github.com/FrankBarretta/LSFG-Android.git
cd LSFG-Android/LSFG-Android

# Debug build
./gradlew :app:assembleDebug

# Release build
./gradlew :app:assembleRelease

# Install directly to connected device
adb install app/build/outputs/apk/debug/app-debug.apk
```

The native `lsfg-vk-android` library is compiled automatically by CMake as part of the Gradle build — no separate `.so` to ship.

---

## First-Run Setup

1. **Grant overlay permission** (`SYSTEM_ALERT_WINDOW`) via Settings → Apps → Special App Access.
2. **Enable `LsfgAccessibilityService`** (for touch-passthrough on strict OEMs).
3. **Load shaders**: pick your legitimately purchased `Lossless.dll` via the Storage Access Framework picker. Shaders are extracted to private storage; the DLL copy is deleted immediately after.
4. **Select target apps**: the overlay arms automatically when a target app comes to the foreground.

---

## Key Configuration Parameters

All parameters are exposed in the live settings drawer. Most trigger a native context re-init; bypass/pacing/Shizuku timing have hot-apply paths.

| Parameter | Range | Notes |
|-----------|-------|-------|
| Multiplier | 2×–8× | Frame generation ratio |
| Flow scale | 0.25–1.0 | Optical-flow resolution |
| Performance mode | bool | Reduces accuracy for speed |
| HDR mode | bool | HDR-aware interpolation |
| Anti-artifacts | bool | Artifact suppression pass |
| Bypass | bool | Hot-apply, no session drop |
| VSync alignment | bool + slack | Aligns output to display vsync |
| Pacing preset | enum | Controls frame pacing strategy |
| Target FPS cap | int | Output FPS ceiling |
| Queue depth | int | Vulkan swapchain queue depth |
| EMA jitter smoothing | float | Exponential moving average factor |

---

## Architecture Overview

```
MediaProjection capture
       │
       ▼
AHardwareBuffer (shared GPU memory)
       │
       ▼
lsfg-vk framegen (Vulkan, arm64-v8a)
  ├── LSFG_3_1 / LSFG_3_1P model
  ├── Optical flow pass
  └── Frame synthesis pass
       │
       ▼
Vulkan swapchain output  ──OR──  CPU-blit fallback
       │
       ▼
SYSTEM_ALERT_WINDOW / TYPE_ACCESSIBILITY_OVERLAY
(composited over target game)
```

---

## JNI / Native Integration Pattern

### Declaring the native interface (Kotlin)

```kotlin
// In your FrameGenBridge.kt or equivalent
object FrameGenBridge {
    init {
        System.loadLibrary("lsfg_android")
    }

    external fun nativeInit(
        surface: Surface,
        width: Int,
        height: Int,
        multiplier: Int,
        flowScale: Float,
        performanceMode: Boolean,
        hdrMode: Boolean
    ): Long  // returns native context handle

    external fun nativeApplyBypass(handle: Long, bypass: Boolean)
    external fun nativeApplyPacing(handle: Long, presetIndex: Int)
    external fun nativeSetTargetFps(handle: Long, targetFps: Int)
    external fun nativeDestroy(handle: Long)
}
```

### Calling from a ViewModel

```kotlin
class FrameGenViewModel : ViewModel() {
    private var nativeHandle: Long = 0L

    fun startSession(surface: Surface, config: FrameGenConfig) {
        nativeHandle = FrameGenBridge.nativeInit(
            surface       = surface,
            width         = config.width,
            height        = config.height,
            multiplier    = config.multiplier,
            flowScale     = config.flowScale,
            performanceMode = config.performanceMode,
            hdrMode       = config.hdrMode
        )
    }

    fun applyBypass(enabled: Boolean) {
        if (nativeHandle != 0L) FrameGenBridge.nativeApplyBypass(nativeHandle, enabled)
    }

    override fun onCleared() {
        if (nativeHandle != 0L) {
            FrameGenBridge.nativeDestroy(nativeHandle)
            nativeHandle = 0L
        }
    }
}
```

---

## MediaProjection Capture Setup

```kotlin
class CaptureService : Service() {
    private lateinit var mediaProjection: MediaProjection
    private lateinit var imageReader: ImageReader

    fun startCapture(
        resultCode: Int,
        data: Intent,
        width: Int,
        height: Int,
        density: Int
    ) {
        val mpManager = getSystemService(MEDIA_PROJECTION_SERVICE) as MediaProjectionManager
        mediaProjection = mpManager.getMediaProjection(resultCode, data)

        imageReader = ImageReader.newInstance(width, height, PixelFormat.RGBA_8888, 2)
        val surface = imageReader.surface

        mediaProjection.createVirtualDisplay(
            "LSFG-Capture",
            width, height, density,
            DisplayManager.VIRTUAL_DISPLAY_FLAG_AUTO_MIRROR,
            surface, null, null
        )

        imageReader.setOnImageAvailableListener({ reader ->
            reader.acquireLatestImage()?.use { image ->
                // Pass AHardwareBuffer to native context
                val hardwareBuffer = image.hardwareBuffer
                if (hardwareBuffer != null) {
                    nativeSubmitFrame(nativeHandle, hardwareBuffer)
                    hardwareBuffer.close()
                }
            }
        }, Handler(Looper.getMainLooper()))
    }
}
```

---

## Overlay Window Setup

```kotlin
class OverlayManager(private val context: Context) {
    private val windowManager = context.getSystemService(WINDOW_SERVICE) as WindowManager

    fun createOverlayView(useAccessibility: Boolean): WindowManager.LayoutParams {
        val type = if (useAccessibility)
            WindowManager.LayoutParams.TYPE_ACCESSIBILITY_OVERLAY
        else
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY

        return WindowManager.LayoutParams(
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.MATCH_PARENT,
            type,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
                WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL or
                WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN or
                WindowManager.LayoutParams.FLAG_HARDWARE_ACCELERATED,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
        }
    }
}
```

---

## Accessibility Service for Touch Passthrough

```kotlin
// LsfgAccessibilityService.kt
class LsfgAccessibilityService : AccessibilityService() {
    override fun onAccessibilityEvent(event: AccessibilityEvent?) {}
    override fun onInterrupt() {}

    override fun onServiceConnected() {
        serviceInfo = serviceInfo.apply {
            flags = flags or AccessibilityServiceInfo.FLAG_REQUEST_TOUCH_EXPLORATION_MODE
        }
        // Notify the overlay that the privileged window type is available
        LocalBroadcastManager.getInstance(this)
            .sendBroadcast(Intent("LSFG_ACCESSIBILITY_CONNECTED"))
    }
}
```

```xml
<!-- res/xml/lsfg_accessibility_service.xml -->
<accessibility-service
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:accessibilityEventTypes="typeAllMask"
    android:accessibilityFeedbackType="feedbackAllMask"
    android:notificationTimeout="0"
    android:canRetrieveWindowContent="false"
    android:settingsActivity=".ui.MainActivity" />
```

---

## Shizuku Integration (Privileged Timing Side Channel)

```kotlin
// Only used for pacing diagnostics — never feeds video buffers
class ShizukuTimingChannel {
    private var connected = false

    private val binderReceiver = object : Shizuku.OnBinderReceivedListener {
        override fun onBinderReceived() {
            connected = true
        }
    }

    fun register() {
        Shizuku.addBinderReceivedListenerSticky(binderReceiver)
    }

    fun queryTargetUidTiming(targetUid: Int): Long {
        if (!connected || !Shizuku.checkSelfPermission().isGranted()) return -1L
        // Use Shizuku to call restricted APIs for per-UID frame timing
        // Feed result to native pacing diagnostics only
        return ShizukuSystemServiceHelper.getUidFrameTiming(targetUid)
    }

    fun unregister() {
        Shizuku.removeBinderReceivedListener(binderReceiver)
    }
}
```

---

## Native CMakeLists.txt Pattern

```cmake
cmake_minimum_required(VERSION 3.22.1)
project(lsfg_android CXX)

set(CMAKE_CXX_STANDARD 20)

# Pull in the lsfg-vk submodule (must be sibling directory)
add_subdirectory(
    ../../../../../lsfg-vk-android/framegen
    ${CMAKE_CURRENT_BINARY_DIR}/lsfg-vk
)

add_library(lsfg_android SHARED
    src/main/cpp/jni_bridge.cpp
    src/main/cpp/vulkan_context.cpp
    src/main/cpp/ahardwarebuffer_share.cpp
    src/main/cpp/mediaprojection_feed.cpp
)

target_link_libraries(lsfg_android
    lsfg_vk          # from submodule
    android
    log
    vulkan
    EGL
    GLESv3
)

target_compile_definitions(lsfg_android PRIVATE __ANDROID__)
```

---

## Android Patch Pattern in lsfg-vk-android

All Android-specific code in the submodule is guarded to keep Linux builds clean:

```cpp
// In lsfg-vk-android/framegen/context.cpp (example pattern)
#ifdef __ANDROID__
#include <android/hardware_buffer.h>

VkResult createContextFromAHB(
    AHardwareBuffer* ahb,
    LsfgContext** outCtx
) {
    AHardwareBuffer_Desc desc{};
    AHardwareBuffer_describe(ahb, &desc);

    // Import AHardwareBuffer as a Vulkan image
    VkAndroidHardwareBufferFormatPropertiesANDROID fmtProps{
        .sType = VK_STRUCTURE_TYPE_ANDROID_HARDWARE_BUFFER_FORMAT_PROPERTIES_ANDROID
    };
    VkAndroidHardwareBufferPropertiesANDROID bufProps{
        .sType = VK_STRUCTURE_TYPE_ANDROID_HARDWARE_BUFFER_PROPERTIES_ANDROID,
        .pNext = &fmtProps
    };
    vkGetAndroidHardwareBufferPropertiesANDROID(device, ahb, &bufProps);

    // ... create VkImage from AHB, bind memory, proceed with framegen init
    return VK_SUCCESS;
}
#endif // __ANDROID__
```

---

## NPU / Post-Processing Pipelines

```kotlin
// Applying an NPU preset via NNAPI
enum class NpuPreset { NONE, SHARPEN, DETAIL_BOOST, CHROMA_CLEAN, GAME_CRISP }

class PostProcessingManager {
    fun applyPreset(preset: NpuPreset, outputSurface: Surface) {
        when (preset) {
            NpuPreset.NONE -> clearNpuPipeline()
            NpuPreset.SHARPEN -> initNnApiModel("lsfg_sharpen.tflite", outputSurface)
            NpuPreset.DETAIL_BOOST -> initNnApiModel("lsfg_detail.tflite", outputSurface)
            NpuPreset.CHROMA_CLEAN -> initNnApiModel("lsfg_chroma.tflite", outputSurface)
            NpuPreset.GAME_CRISP -> initNnApiModel("lsfg_crisp.tflite", outputSurface)
        }
    }
}
```

---

## Compose Settings Drawer Example

```kotlin
@Composable
fun FrameGenSettingsDrawer(
    config: FrameGenConfig,
    onConfigChange: (FrameGenConfig) -> Unit
) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text("Multiplier: ${config.multiplier}×")
        Slider(
            value = config.multiplier.toFloat(),
            onValueChange = { onConfigChange(config.copy(multiplier = it.toInt())) },
            valueRange = 2f..8f, steps = 2
        )

        Text("Flow Scale: ${"%.2f".format(config.flowScale)}")
        Slider(
            value = config.flowScale,
            onValueChange = { onConfigChange(config.copy(flowScale = it)) },
            valueRange = 0.25f..1.0f
        )

        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("Bypass", modifier = Modifier.weight(1f))
            Switch(
                checked = config.bypass,
                onCheckedChange = { onConfigChange(config.copy(bypass = it)) }
            )
        }

        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("Performance Mode", modifier = Modifier.weight(1f))
            Switch(
                checked = config.performanceMode,
                onCheckedChange = { onConfigChange(config.copy(performanceMode = it)) }
            )
        }
    }
}
```

---

## Frame Graph HUD

```kotlin
@Composable
fun FrameGraphHud(stats: FrameStats) {
    Column(
        modifier = Modifier
            .background(Color.Black.copy(alpha = 0.6f))
            .padding(8.dp)
    ) {
        Text(
            text = "Real: ${stats.realFps} FPS | Total: ${stats.totalFps} FPS",
            color = Color.Green,
            fontSize = 12.sp
        )
        Canvas(modifier = Modifier.size(120.dp, 40.dp)) {
            stats.frameTimesMs.forEachIndexed { i, ms ->
                val x = i * (size.width / stats.frameTimesMs.size)
                val h = (ms / 33.3f).coerceIn(0f, 1f) * size.height
                drawRect(
                    color = if (ms > 16.7f) Color.Red else Color.Green,
                    topLeft = Offset(x, size.height - h),
                    size = Size(size.width / stats.frameTimesMs.size - 1f, h)
                )
            }
        }
    }
}
```

---

## Manifest Permissions

```xml
<uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_MEDIA_PROJECTION" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_SPECIAL_USE" />

<service
    android:name=".service.LsfgOverlayService"
    android:foregroundServiceType="mediaProjection|specialUse"
    android:exported="false" />

<service
    android:name=".accessibility.LsfgAccessibilityService"
    android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE"
    android:exported="true">
    <intent-filter>
        <action android:name="android.accessibilityservice.AccessibilityService" />
    </intent-filter>
    <meta-data
        android:name="android.accessibilityservice"
        android:resource="@xml/lsfg_accessibility_service" />
</service>
```

---

## Crash Reporter Integration

```kotlin
class LsfgCrashHandler(private val context: Context) : Thread.UncaughtExceptionHandler {
    private val default = Thread.getDefaultUncaughtExceptionHandler()

    fun install() {
        Thread.setDefaultUncaughtExceptionHandler(this)
        installNativeCrashHandler() // JNI: intercepts SIGSEGV, SIGABRT, etc.
    }

    override fun uncaughtException(t: Thread, e: Throwable) {
        val report = buildString {
            appendLine("=== LSFG-Android Crash Report ===")
            appendLine("Thread: ${t.name}")
            appendLine(e.stackTraceToString())
        }
        saveCrashReport(report)
        default?.uncaughtException(t, e)
    }

    private fun saveCrashReport(report: String) {
        val file = File(context.filesDir, "crash_${System.currentTimeMillis()}.txt")
        file.writeText(report)
    }

    fun shareCrashReport(activity: Activity) {
        val latest = context.filesDir.listFiles()
            ?.filter { it.name.startsWith("crash_") }
            ?.maxByOrNull { it.lastModified() } ?: return

        val uri = FileProvider.getUriForFile(context, "${context.packageName}.provider", latest)
        activity.startActivity(Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_STREAM, uri)
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        })
    }

    private external fun installNativeCrashHandler()
}
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Black overlay, no frames | Shader extraction failed | Re-pick `Lossless.dll` via SAF picker; check logcat for extraction errors |
| `UnsatisfiedLinkError: lsfg_android` | NDK/ABI mismatch | Ensure NDK 27.0.12077973; clean Gradle caches (`./gradlew clean`) |
| CMake can't find submodule | Folders not siblings | Clone with `--recurse-submodules`; ensure `lsfg-vk-android/` is next to `LSFG-Android/` |
| Touch events not passing through | Accessibility service not active | Enable `LsfgAccessibilityService` in Settings → Accessibility |
| 50–80 ms overlay latency | Platform constraint (MediaProjection) | Expected on non-rooted Android; not a bug |
| Overlay not appearing | `SYSTEM_ALERT_WINDOW` not granted | Settings → Apps → Special App Access → Display over other apps |
| Crash on Vulkan init | Unsupported GPU | Requires Adreno 7xx-class or newer; check `adb logcat -s Vulkan` |
| Shizuku timing unavailable | Shizuku not running or permission denied | Start Shizuku via ADB/wireless ADB, grant LSFG the Shizuku permission |
| Native SIGABRT on frame submit | AHardwareBuffer format mismatch | Ensure `ImageReader` uses `PixelFormat.RGBA_8888` and hardware-backed allocation |

---

## Platform Constraints (Non-Negotiable)

- **No Vulkan implicit layer hooking** on non-rooted Android 12+ — platform intentionally blocks it.
- **MediaProjection consent dialog** appears on every session start (system requirement).
- **Not distributable on Google Play** — `SYSTEM_ALERT_WINDOW` + screen capture + `AccessibilityService` violates Play policy. Distribute as sideloaded APK only.
- **Magisk module path** (installing to `/system/etc/vulkan/implicit_layer.d/`) is the only way to match Linux layer experience — out of scope for this project.
