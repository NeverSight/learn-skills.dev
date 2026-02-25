---
name: expect-actual
description: Kotlin Multiplatform expect/actual patterns for platform-specific APIs. Learn to declare shared interfaces with platform implementations.
---

# expect/actual Pattern for KMP

The `expect/actual` declaration is Kotlin's mechanism for writing platform-specific implementations while maintaining a shared API surface.

## Core Concept

```kotlin
// shared/commonMain/kotlin/Platform.kt
expect class Platform() {
    val name: String
}

// shared/androidMain/kotlin/Platform.android.kt
actual class Platform {
    actual val name: String = "Android ${Build.VERSION.SDK_INT}"
}

// shared/iosMain/kotlin/Platform.ios.kt
actual class Platform {
    actual val name: String = "iOS \(UIDevice.currentDevice.systemVersion)"
}
```

## Common Patterns

### 1. Platform Information

```kotlin
// commonMain
expect object Platform {
    val name: String
    val version: String
    val isDebug: Boolean
}

// androidMain
actual object Platform {
    actual val name: String = "Android"
    actual val version: String = "${Build.VERSION.SDK_INT}"
    actual val isDebug: Boolean = BuildConfig.DEBUG
}

// iosMain
actual object Platform {
    actual val name: String = "iOS"
    actual val version: String = UIDevice.currentDevice.systemVersion
    actual val isDebug: Boolean = KotlinLifecycleController.isDebug
}
```

### 2. File System Paths

```kotlin
// commonMain
expect class FileSystem {
    fun getDocumentsPath(): String
    fun getCachePath(): String
    fun getTempPath(): String
}

// androidMain
actual class FileSystem {
    actual fun getDocumentsPath(): String {
        return context.filesDir.absolutePath
    }
    actual fun getCachePath(): String {
        return context.cacheDir.absolutePath
    }
    actual fun getTempPath(): String {
        return context.cacheDir.absolutePath + "/tmp"
    }
}

// iosMain
actual class FileSystem {
    actual fun getDocumentsPath(): String {
        return NSSearchPathForDirectoriesInDomains(
            NSDocumentDirectory,
            NSUserDomainMask,
            true
        ).first() as String
    }
    actual fun getCachePath(): String {
        return NSSearchPathForDirectoriesInDomains(
            NSCachesDirectory,
            NSUserDomainMask,
            true
        ).first() as String
    }
    actual fun getTempPath(): String {
        return NSTemporaryDirectory()
    }
}
```

### 3. Date/Time Operations

```kotlin
// commonMain
expect class DateTimeFormatter {
    fun format(timestamp: Long): String
    fun parse(dateString: String): Long
    fun now(): Long
}

// androidMain
actual class DateTimeFormatter {
    private val format = SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault())

    actual fun format(timestamp: Long): String {
        return format.format(Date(timestamp))
    }

    actual fun parse(dateString: String): Long {
        return format.parse(dateString)?.time ?: 0L
    }

    actual fun now(): Long = System.currentTimeMillis()
}

// iosMain
actual class DateTimeFormatter {
    private val formatter = NSDateFormatter().apply {
        dateFormat = "yyyy-MM-dd HH:mm:ss"
    }

    actual fun format(timestamp: Long): String {
        val date = NSDate(timeIntervalSince1970 = timestamp / 1000.0)
        return formatter.stringFromDate(date)
    }

    actual fun parse(dateString: String): Long {
        val date = formatter.dateFromString(dateString) ?: return 0L
        return (date.timeIntervalSince1970 * 1000).toLong()
    }

    actual fun now(): Long = (NSDate().timeIntervalSince1970 * 1000).toLong()
}
```

### 4. Database Paths

```kotlin
// commonMain
expect class DatabasePathProvider {
    fun getDatabasePath(name: String): String
}

// androidMain
actual class DatabasePathProvider(private val context: Context) {
    actual fun getDatabasePath(name: String): String {
        return context.getDatabasePath(name).absolutePath
    }
}

// iosMain
actual class DatabasePathProvider {
    actual fun getDatabasePath(name: String): String {
        val dir = NSSearchPathForDirectoriesInDomains(
            NSDocumentDirectory,
            NSUserDomainMask,
            true
        ).first() as String
        return "$dir/databases/$name"
    }
}
```

### 5. Secure Storage

```kotlin
// commonMain
expect class SecureStorage {
    suspend fun save(key: String, value: String)
    suspend fun load(key: String): String?
    suspend fun delete(key: String)
}

// androidMain
actual class SecureStorage(private val context: Context) {
    private val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()

    private val prefs = EncryptedSharedPreferences.create(
        context,
        "secure",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )

    actual suspend fun save(key: String, value: String) {
        prefs.edit().putString(key, value).apply()
    }

    actual suspend fun load(key: String): String? = prefs.getString(key, null)

    actual suspend fun delete(key: String) {
        prefs.edit().remove(key).apply()
    }
}

// iosMain
actual class SecureStorage {
    private val keychain = KeychainHelper()

    actual suspend fun save(key: String, value: String) {
        keychain.set(key, value)
    }

    actual suspend fun load(key: String): String? {
        return keychain.get(key)
    }

    actual suspend fun delete(key: String) {
        keychain.delete(key)
    }
}
```

### 6. Network Connectivity

```kotlin
// commonMain
expect class ConnectivityMonitor {
    val isOnline: Flow<Boolean>
    fun startMonitoring()
    fun stopMonitoring()
}

// androidMain
actual class ConnectivityMonitor(private val context: Context) {
    private val _isOnline = MutableStateFlow(true)
    actual val isOnline: StateFlow<Boolean> = _isOnline.asStateFlow()

    private val callback = object : ConnectivityManager.NetworkCallback() {
        override fun onAvailable(network: Network) {
            _isOnline.value = true
        }
        override fun onLost(network: Network) {
            _isOnline.value = false
        }
    }

    actual fun startMonitoring() {
        val cm = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        cm.registerNetworkCallback(
            NetworkRequest.Builder().build(),
            callback
        )
    }

    actual fun stopMonitoring() {
        val cm = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        cm.unregisterNetworkCallback(callback)
    }
}

// iosMain
actual class ConnectivityMonitor {
    private val _isOnline = MutableStateFlow(true)
    actual val isOnline: StateFlow<Boolean> = _isOnline.asStateFlow()

    private val monitor = NWPathMonitor()
    private val queue = dispatch_queue_create("network", null)

    actual fun startMonitoring() {
        monitor.pathUpdateHandler = {
            _isOnline.value = monitor.currentPath.status == .satisfied
        }
        monitor.start(queue)
    }

    actual fun stopMonitoring() {
        monitor.cancel()
    }
}
```

### 7. Logging

```kotlin
// commonMain
enum class LogLevel { DEBUG, INFO, WARN, ERROR }

expect class Logger {
    fun log(level: LogLevel, tag: String, message: String, throwable: Throwable?)
}

// androidMain
actual class Logger {
    actual fun log(level: LogLevel, tag: String, message: String, throwable: Throwable?) {
        when (level) {
            LogLevel.DEBUG -> Log.d(tag, message, throwable)
            LogLevel.INFO -> Log.i(tag, message, throwable)
            LogLevel.WARN -> Log.w(tag, message, throwable)
            LogLevel.ERROR -> Log.e(tag, message, throwable)
        }
    }
}

// iosMain
actual class Logger {
    actual fun log(level: LogLevel, tag: String, message: String, throwable: Throwable?) {
        val fullMessage = if (throwable != null) "$message: $throwable" else message
        println("[$tag] [$level] $fullMessage")
        os_log(OSLogDefault, level.toOSLogType(), "%{public}@", fullMessage)
}

private fun LogLevel.toOSLogType() = when (this) {
    LogLevel.DEBUG -> OS_LOG_TYPE_DEBUG
    LogLevel.INFO -> OS_LOG_TYPE_INFO
    LogLevel.WARN -> OS_LOG_TYPE_DEFAULT
    LogLevel.ERROR -> OS_LOG_TYPE_ERROR
}
```

## Best Practices

### ✅ DO

```kotlin
// ✅ Keep expect declarations simple
expect class PlatformInfo {
    val platform: String
}

// ✅ Use factory functions for dependencies
expect fun createPlatformService(): PlatformService

// ✅ Group related functionality
expect class FileService {
    fun read(path: String): ByteArray
    fun write(path: String, data: ByteArray)
    fun delete(path: String)
}

// ✅ Provide default implementations when possible
expect class Analytics {
    fun track(event: String, properties: Map<String, Any>)
    fun flush()
}
```

### ❌ DON'T

```kotlin
// ❌ Don't add complex logic in expect declarations
expect class Platform {
    // Complex logic here won't compile
    fun calculateSomething(): Int {
        // This causes errors
    }
}

// ❌ Don't use expect for pure Kotlin logic
// Use commonMain instead
expect fun add(a: Int, b: Int): Int  // ❌ This doesn't need expect/actual

// ❌ Don't create too many small expect classes
// Consolidate related functionality
expect class FileReader
expect class FileWriter
expect class FileDeleter  // ❌ Should be one FileService class
```

## File Organization

```
shared/
├── commonMain/
│   └── kotlin/
│       └── com/example/platform/
│           ├── Platform.kt          (expect class Platform)
│           ├── FileSystem.kt        (expect class FileSystem)
│           └── DatabasePath.kt      (expect class DatabasePath)
├── androidMain/
│   └── kotlin/
│       └── com/example/platform/
│           ├── Platform.android.kt  (actual class Platform)
│           ├── FileSystem.android.kt
│           └── DatabasePath.android.kt
├── iosMain/
│   └── kotlin/
│       └── com/example/platform/
│           ├── Platform.ios.kt      (actual class Platform)
│           ├── FileSystem.ios.kt
│           └── DatabasePath.ios.kt
└── desktopMain/
    └── kotlin/
        └── com/example/platform/
            ├── Platform.desktop.kt
            └── FileSystem.desktop.kt
```

## Testing with expect/actual

```kotlin
// commonTest
class PlatformTest {
    @Test
    fun `platform name is not empty`() {
        assertTrue(Platform.name.isNotEmpty())
    }
}

// Test runs on all platforms with actual implementations
```

---

**Remember**: Use `expect/actual` only when you truly need platform-specific APIs. Keep as much code as possible in `commonMain`.
