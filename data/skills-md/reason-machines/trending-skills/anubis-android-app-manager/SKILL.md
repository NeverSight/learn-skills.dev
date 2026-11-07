---
name: anubis-android-app-manager
description: Android app manager with VPN integration that freezes/unfreezes app groups based on VPN connection state using Shizuku's pm disable-user
triggers:
  - set up Anubis app manager
  - freeze apps based on VPN state
  - manage app groups with VPN integration
  - configure Shizuku app freezing
  - add VPN client to Anubis
  - create app groups for VPN control
  - integrate Anubis with custom VPN client
  - troubleshoot Anubis app freezing
---

# Anubis Android App Manager

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Anubis is an Android app manager that uses Shizuku to completely disable (`pm disable-user`) app groups based on VPN connection state. Unlike sandboxing solutions (Island, Shelter), disabled apps cannot run code, access network interfaces, or detect VPN presence at all.

## Core Concepts

| Group Policy | Behavior |
|---|---|
| **Local** | Frozen when VPN is active; runs without VPN |
| **VPN Only** | Frozen when VPN is inactive; runs through VPN |
| **Launch with VPN** | Never frozen; launching triggers VPN activation |

## Requirements

- Android 10+ (API 29)
- [Shizuku](https://shizuku.rikka.app/) installed and running
- At least one VPN client installed

## Setup

1. Install and start Shizuku (via ADB or Wireless Debugging):
   ```bash
   adb shell sh /sdcard/Android/data/moe.shizuku.privileged.api/start.sh
   ```
2. Install Anubis APK
3. Grant Shizuku permission when prompted
4. Grant VPN permission when prompted (needed for dummy VPN disconnect)
5. Go to **Apps** tab → assign apps to groups
6. Select VPN client in **Settings**
7. Toggle stealth mode on **Home** screen

## Building

```bash
git clone https://github.com/sogonov/anubis
cd anubis

# Debug build
./gradlew assembleDebug

# Release build (requires signing config)
./gradlew assembleRelease
```

Create `signing.properties` in project root for release builds:
```properties
storeFile=release.keystore
storePassword=${KEYSTORE_PASSWORD}
keyAlias=${KEY_ALIAS}
keyPassword=${KEY_PASSWORD}
```

## Tech Stack

- Kotlin + Jetpack Compose (Material 3)
- Shizuku API 13.1.5 (AIDL UserService pattern)
- Room database with TypeConverters for app groups
- `ConnectivityManager` NetworkCallback for VPN state monitoring
- `ShortcutManager` for pinned shortcuts

## Project Structure

```
app/src/main/java/
├── data/
│   ├── AppGroup.kt          # Room entity: group name, policy, package list
│   ├── AppGroupDao.kt       # DAO: CRUD for app groups
│   └── AppDatabase.kt       # Room database setup
├── service/
│   ├── ShizukuService.kt    # AIDL UserService: pm/am shell commands
│   ├── VpnStateMonitor.kt   # ConnectivityManager NetworkCallback
│   └── FreezeManager.kt     # Orchestrates freeze/unfreeze logic
├── vpn/
│   ├── VpnClient.kt         # Enum: SEPARATE, TOGGLE, MANUAL
│   └── VpnClientRegistry.kt # Known clients + custom client support
└── ui/
    ├── HomeScreen.kt         # Launcher grid, VPN toggle
    ├── AppsScreen.kt         # Group assignment UI
    └── SettingsScreen.kt     # VPN client selection
```

## Room Database: App Groups

```kotlin
@Entity(tableName = "app_groups")
data class AppGroup(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val name: String,
    val policy: GroupPolicy,
    val packages: List<String> // stored via TypeConverter
)

enum class GroupPolicy {
    LOCAL,        // frozen when VPN active
    VPN_ONLY,     // frozen when VPN inactive
    LAUNCH_WITH_VPN // never frozen, VPN triggered on launch
}
```

```kotlin
@Dao
interface AppGroupDao {
    @Query("SELECT * FROM app_groups")
    fun getAllGroups(): Flow<List<AppGroup>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertGroup(group: AppGroup)

    @Delete
    suspend fun deleteGroup(group: AppGroup)

    @Update
    suspend fun updateGroup(group: AppGroup)
}
```

## Shizuku Integration (AIDL UserService Pattern)

Define the AIDL interface:
```kotlin
// IShizukuService.aidl
interface IShizukuService {
    String executeCommand(String command);
    void destroy();
}
```

Implement the UserService:
```kotlin
class ShizukuUserService : IShizukuService.Stub() {
    override fun executeCommand(command: String): String {
        return try {
            val process = Runtime.getRuntime().exec(arrayOf("sh", "-c", command))
            process.inputStream.bufferedReader().readText()
        } catch (e: Exception) {
            "ERROR: ${e.message}"
        }
    }

    override fun destroy() {
        exitProcess(0)
    }
}
```

Bind to the UserService:
```kotlin
class FreezeManager(private val context: Context) {

    private var service: IShizukuService? = null

    private val serviceConnection = object : ServiceConnection {
        override fun onServiceConnected(name: ComponentName, binder: IBinder) {
            service = IShizukuService.Stub.asInterface(binder)
        }
        override fun onServiceDisconnected(name: ComponentName) {
            service = null
        }
    }

    private val userServiceArgs = Shizuku.UserServiceArgs(
        ComponentName(context, ShizukuUserService::class.java)
    ).processNameSuffix("service").debuggable(false).version(1)

    fun bindService() {
        if (Shizuku.checkSelfPermission() == PackageManager.PERMISSION_GRANTED) {
            Shizuku.bindUserService(userServiceArgs, serviceConnection)
        }
    }

    fun unbindService() {
        Shizuku.unbindUserService(userServiceArgs, serviceConnection, true)
    }

    suspend fun freezePackage(packageName: String) {
        service?.executeCommand("pm disable-user --user 0 $packageName")
    }

    suspend fun unfreezePackage(packageName: String) {
        service?.executeCommand("pm enable --user 0 $packageName")
    }
}
```

## VPN State Monitoring

```kotlin
class VpnStateMonitor(private val context: Context) {

    private val connectivityManager =
        context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager

    private val _isVpnActive = MutableStateFlow(false)
    val isVpnActive: StateFlow<Boolean> = _isVpnActive.asStateFlow()

    private val networkCallback = object : ConnectivityManager.NetworkCallback() {
        override fun onAvailable(network: Network) {
            val capabilities = connectivityManager.getNetworkCapabilities(network)
            if (capabilities?.hasTransport(NetworkCapabilities.TRANSPORT_VPN) == true) {
                _isVpnActive.value = true
            }
        }

        override fun onLost(network: Network) {
            // Re-check if any VPN network remains
            val hasVpn = connectivityManager.allNetworks.any { net ->
                connectivityManager.getNetworkCapabilities(net)
                    ?.hasTransport(NetworkCapabilities.TRANSPORT_VPN) == true
            }
            _isVpnActive.value = hasVpn
        }
    }

    fun startMonitoring() {
        val request = NetworkRequest.Builder()
            .addTransportType(NetworkCapabilities.TRANSPORT_VPN)
            .build()
        connectivityManager.registerNetworkCallback(request, networkCallback)
    }

    fun stopMonitoring() {
        connectivityManager.unregisterNetworkCallback(networkCallback)
    }
}
```

## VPN Client Control

```kotlin
enum class VpnControlMethod { SEPARATE, TOGGLE, MANUAL }

data class VpnClientConfig(
    val packageName: String,
    val method: VpnControlMethod,
    val startAction: String? = null,
    val stopAction: String? = null,
    val toggleAction: String? = null,
    val receiverClass: String? = null
)

val KNOWN_VPN_CLIENTS = mapOf(
    "com.v2ray.ang" to VpnClientConfig(
        packageName = "com.v2ray.ang",
        method = VpnControlMethod.TOGGLE,
        toggleAction = "com.v2ray.ang.action.widget.click",
        receiverClass = "com.v2ray.ang.receiver.WidgetProvider"
    ),
    "moe.nb4a" to VpnClientConfig(
        packageName = "moe.nb4a",
        method = VpnControlMethod.SEPARATE,
        startAction = "moe.nb4a.ui.QuickEnable",
        stopAction = "moe.nb4a.ui.QuickDisable"
    ),
    "com.happproxy" to VpnClientConfig(
        packageName = "com.happproxy",
        method = VpnControlMethod.TOGGLE,
        toggleAction = "com.happproxy.action.widget.click",
        receiverClass = "com.happproxy.receiver.WidgetProvider"
    )
)
```

Start/stop VPN via shell:
```kotlin
suspend fun startVpn(config: VpnClientConfig) {
    when (config.method) {
        VpnControlMethod.TOGGLE, VpnControlMethod.SEPARATE -> {
            val action = config.startAction ?: config.toggleAction!!
            if (config.receiverClass != null) {
                // Broadcast to widget receiver
                service?.executeCommand(
                    "am broadcast -a $action -n ${config.packageName}/${config.receiverClass}"
                )
            } else {
                // Start exported activity (NekoBox SEPARATE style)
                service?.executeCommand(
                    "am start -n ${config.packageName}/$action"
                )
            }
        }
        VpnControlMethod.MANUAL -> {
            // Open app for user to connect manually
            val intent = context.packageManager
                .getLaunchIntentForPackage(config.packageName)
            context.startActivity(intent)
        }
    }
}

suspend fun stopVpn(config: VpnClientConfig) {
    // Step 1: API stop (SEPARATE clients only)
    if (config.method == VpnControlMethod.SEPARATE && config.stopAction != null) {
        service?.executeCommand("am start -n ${config.packageName}/${config.stopAction}")
        delay(1000)
    }
    // Step 2: Force-stop as fallback
    service?.executeCommand("am force-stop ${config.packageName}")
}
```

## Detecting Active VPN Client

```kotlin
suspend fun detectVpnOwnerPackage(): String? {
    val output = service?.executeCommand("dumpsys connectivity") ?: return null

    // Find VPN network owner UID
    val vpnLine = output.lines().firstOrNull { it.contains("type: VPN[") }
        ?: return null

    val uidMatch = Regex("ownerUid=(\\d+)").find(output) ?: return null
    val uid = uidMatch.groupValues[1]

    // Resolve UID to package name
    val pmOutput = service?.executeCommand("pm list packages --uid $uid") ?: return null
    return pmOutput.substringAfter("package:").substringBefore(" ").trim()
        .takeIf { it.isNotEmpty() }
}
```

## Adding a Custom VPN Client

Use APK analysis to discover broadcast actions:

1. Open APK in [jadx](https://github.com/skylot/jadx)
2. **Resources** → find `app_widget_name` in `strings.xml`
3. **Manifest** → find `<receiver>` with `android.appwidget.provider` metadata
4. **Receiver code** → find `setAction("...")` calls
5. Verify toggle pattern: `isRunning ? stop : start`

All v2ray/xray forks share the same pattern:
```kotlin
// Discovery template for v2ray forks:
val packageName = "com.example.vpnclient"
val toggleAction = "$packageName.action.widget.click"
val receiverClass = "$packageName.receiver.WidgetProvider"

// Verify manually via ADB:
// adb shell am broadcast -a $toggleAction -n $packageName/$receiverClass
```

Register custom client in Settings UI:
```kotlin
// SettingsViewModel.kt
fun setCustomVpnClient(packageName: String) {
    val config = VpnClientConfig(
        packageName = packageName,
        method = VpnControlMethod.MANUAL // upgrade to TOGGLE if action known
    )
    preferences.edit().putString("custom_vpn_client", packageName).apply()
}
```

## Pinned Shortcuts

```kotlin
fun createAppShortcut(
    context: Context,
    packageName: String,
    label: String,
    icon: Icon
) {
    val shortcutManager = context.getSystemService(ShortcutManager::class.java)
    if (shortcutManager.isRequestPinShortcutSupported) {
        val intent = Intent(context, LaunchActivity::class.java).apply {
            action = Intent.ACTION_VIEW
            putExtra("package_name", packageName)
        }
        val shortcut = ShortcutInfo.Builder(context, "shortcut_$packageName")
            .setShortLabel(label)
            .setIcon(icon)
            .setIntent(intent)
            .build()
        shortcutManager.requestPinShortcut(shortcut, null)
    }
}
```

## Compose UI: App Group Management

```kotlin
@Composable
fun AppGroupCard(
    group: AppGroup,
    onPolicyChange: (GroupPolicy) -> Unit,
    onAddApp: () -> Unit,
    onRemoveApp: (String) -> Unit
) {
    Card(modifier = Modifier.fillMaxWidth().padding(8.dp)) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(group.name, style = MaterialTheme.typography.titleMedium)

            // Policy selector
            Row {
                GroupPolicy.entries.forEach { policy ->
                    FilterChip(
                        selected = group.policy == policy,
                        onClick = { onPolicyChange(policy) },
                        label = { Text(policy.name) },
                        modifier = Modifier.padding(end = 4.dp)
                    )
                }
            }

            // App list with frozen state indicators
            group.packages.forEach { pkg ->
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(pkg, modifier = Modifier.weight(1f))
                    IconButton(onClick = { onRemoveApp(pkg) }) {
                        Icon(Icons.Default.Remove, "Remove")
                    }
                }
            }
            TextButton(onClick = onAddApp) {
                Icon(Icons.Default.Add, "Add app")
                Text("Add App")
            }
        }
    }
}
```

## Freeze Orchestration on VPN State Change

```kotlin
class AppOrchestrator(
    private val freezeManager: FreezeManager,
    private val groupDao: AppGroupDao,
    private val vpnMonitor: VpnStateMonitor
) {
    suspend fun onVpnStateChanged(isVpnActive: Boolean) {
        val groups = groupDao.getAllGroups().first()
        groups.forEach { group ->
            when (group.policy) {
                GroupPolicy.LOCAL -> {
                    if (isVpnActive) freezeGroup(group) else unfreezeGroup(group)
                }
                GroupPolicy.VPN_ONLY -> {
                    if (!isVpnActive) freezeGroup(group) else unfreezeGroup(group)
                }
                GroupPolicy.LAUNCH_WITH_VPN -> {
                    // Never auto-freeze; handled at launch time
                }
            }
        }
    }

    private suspend fun freezeGroup(group: AppGroup) {
        group.packages.forEach { pkg ->
            freezeManager.freezePackage(pkg)
        }
    }

    private suspend fun unfreezeGroup(group: AppGroup) {
        // Safety: never unfreeze while VPN is still transitioning
        if (!vpnMonitor.isVpnActive.value || group.policy == GroupPolicy.LOCAL) {
            group.packages.forEach { pkg ->
                freezeManager.unfreezePackage(pkg)
            }
        }
    }
}
```

## Troubleshooting

### Shizuku Permission Denied
```kotlin
// Check and request Shizuku permission
if (Shizuku.checkSelfPermission() != PackageManager.PERMISSION_GRANTED) {
    if (Shizuku.shouldShowRequestPermissionRationale()) {
        // Show rationale dialog
    } else {
        Shizuku.requestPermission(REQUEST_CODE_SHIZUKU)
    }
}
```

### App Not Freezing
```bash
# Verify pm disable-user works manually
adb shell pm disable-user --user 0 com.example.app
# Check current state
adb shell pm list packages -d  # lists disabled packages
# Re-enable manually if stuck
adb shell pm enable --user 0 com.example.app
```

### VPN Detection Failing
```bash
# Debug dumpsys output
adb shell dumpsys connectivity | grep -A5 "type: VPN"
# Check UID resolution
adb shell pm list packages --uid 1234
```

### Custom VPN Client Toggle Not Working
```bash
# Test broadcast manually
adb shell am broadcast -a com.example.vpn.action.widget.click \
  -n com.example.vpn/.receiver.WidgetProvider
# Expected: result=0 (RESULT_OK) or check logcat for errors
adb logcat | grep -i "widgetprovider\|broadcast"
```

### Apps Remain Frozen After VPN Disconnect
- Anubis never unfreezes apps while VPN is still active
- Check VPN is fully disconnected: `adb shell dumpsys connectivity | grep VPN`
- Manually unfreeze via long-press on app icon → "Unfreeze"

## Gradle Dependencies

```kotlin
// build.gradle.kts
dependencies {
    // Shizuku
    implementation("dev.rikka.shizuku:api:13.1.5")
    implementation("dev.rikka.shizuku:provider:13.1.5")

    // Room
    implementation("androidx.room:room-runtime:2.6.1")
    implementation("androidx.room:room-ktx:2.6.1")
    ksp("androidx.room:room-compiler:2.6.1")

    // Compose
    implementation(platform("androidx.compose:compose-bom:2024.02.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.material3:material3")

    // Coroutines + ViewModel
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
}
```
