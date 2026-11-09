---
name: rea-mobile-app-recovery
description: Complete Android (APK/AAB/DEX/JNI/Flutter/React Native/Unity) and iOS (IPA/Mach-O/Swift/ObjC) reverse engineering, full project reconstruction, and OWASP MASVS / PTKD 5-Pillar mobile vulnerability scanner using REA MCP, JADX, Apktool, Blutter, hermes-dec, Ghidra, Frida, and MobSF.
---

# REA Mobile App Recovery & 5-Pillar Vulnerability Scanner (Android & iOS)

## Scope & Authorization
Covers all first-party mobile application reverse engineering, lost source code reconstruction, and automated security vulnerability scanning for Android (`.apk`, `.aab`, `.dex`, `.so`) and iOS (`.ipa`, Mach-O) applications.

---

## 1. The 5-Pillar Mobile Vulnerability Scanner Checklist (PTKD & OWASP MASVS)

Whenever the user asks to scan, audit, or check weakpoints in their mobile app (or asks what vulnerabilities to look for), systematically inspect and report on these 5 pillars with exact file/line evidence and remediation code:

### Pillar 1: In the Manifest (`AndroidManifest.xml` / `Info.plist`)
- **Exported Components (`android:exported="true"`):** Flag any Activity, Service, BroadcastReceiver, or ContentProvider with `android:exported="true"` (or implicit intent-filters) that lacks strict permission guards—which lets third-party apps launch private screens, steal data via ContentProviders, or trigger background actions.
- **Deep Link & Intent Hijacking:** Audit `<data android:scheme="..." />` handlers for unvalidated URI parameters and intent redirection.
- **Build & Backup Flags:** Flag `android:debuggable="true"` and `android:allowBackup="true"` in production manifests.

### Pillar 2: In Local Storage (`/data/data/<package_name>/` & External Storage)
- **Plaintext SharedPreferences & SQLite:** Flag storing passwords, JWT/OAuth tokens, session cookies, or PII in unencrypted `shared_prefs/*.xml` or plaintext SQLite `.db` files (recommend migrating to `EncryptedSharedPreferences` / JetPack DataStore with Tink / SQLCipher / Android Keystore / iOS Keychain).
- **External Storage (SD Card / Public Folders):** Flag any use of `getExternalStorageDirectory()`, `getExternalFilesDir()`, or `MODE_WORLD_READABLE` / `MODE_WORLD_WRITEABLE` where any other app on the device can read or modify sensitive app files.

### Pillar 3: Inside Decompiled Code (Java / Kotlin / Swift / Dart / JS)
- **Hardcoded Secrets:** Scan all decompiled classes, `BuildConfig.java`, `res/values/strings.xml`, and native `.so` rodata for hardcoded API keys, AWS credentials (`AKIA...`), Firebase/Supabase service keys, payment keys, or static AES encryption keys/IVs.
- **Active Debug Logs (`logcat` Leaks):** Flag active `Log.d()`, `Log.v()`, `Log.i()`, `System.out.println()`, or `printStackTrace()` statements that leak sensitive tokens, payloads, or user credentials into the phone's public system logs (`adb logcat`).
- **Weak Cryptography:** Flag `AES/ECB`, static IVs, `MD5`/`SHA1` password hashing, and `java.util.Random` (must use `AES/GCM/NoPadding` and `SecureRandom`).

### Pillar 4: In Network Settings & Traffic
- **HTTP Cleartext Traffic:** Flag `http://` endpoints, `android:usesCleartextTraffic="true"`, or permissive `res/xml/network_security_config.xml` (and iOS `NSAllowsArbitraryLoads`), which allow attackers on public Wi-Fi to intercept traffic.
- **Missing SSL/TLS Certificate Pinning:** Check whether `network_security_config.xml` (`<pin-set>`), OkHttp `CertificatePinner`, or TrustKit is configured, and flag custom `X509TrustManager` or `HostnameVerifier` implementations that blindly accept all certificates (`ALLOW_ALL_HOSTNAME_VERIFIER`).

### Pillar 5: In WebViews (In-App Browsers)
- **Unrestricted JavaScript & File Access:** Flag `webView.getSettings().setJavaScriptEnabled(true)` when combined with untrusted URLs, `addJavascriptInterface()` (RCE risk), `setAllowFileAccess(true)`, `setAllowFileAccessFromFileURLs(true)`, or `setAllowUniversalAccessFromFileURLs(true)`, which allow malicious web content to execute code inside the app and exfiltrate local private files.

---

## 2. Complete 10-Stage Android & iOS Reverse Engineering Toolchain

### Stage 1: Basic Environment & Prerequisites
- **Java Development Kit (JDK 11/17+):** Powers `jadx`, `apktool`, and `apksigner`.
- **Android SDK Platform-Tools (`adb`):** Connects to devices/emulators (`list_adb_devices`, `pull_adb_package`, `read_adb_logcat`, `inspect_adb_package`).
- **Python 3:** Runs Frida, Objection, and custom binary/crypto scripts.
- **Test Device / Emulator:** Rooted physical device (Magisk) or Android Studio AVD / Genymotion.

### Stage 2: Unpacking & Resource Extraction
- **Apktool (`inspect_apktool_client`, `decode_android_resources`):** Decodes `AndroidManifest.xml`, `res/`, `assets/`, and Smali disassembly.
- **7-Zip / Unzip:** Extracts raw `classes*.dex`, `lib/<abi>/*.so`, and `assets/`.
- **`aapt` / `aapt2`:** Rapidly inspects package metadata, permissions, and resource configurations.

### Stage 3: Source Code Decompilation (DEX to Java/Kotlin)
- **JADX (GUI & CLI) & REA MCP (`inspect_android_package`, `search_android_classes`, `inspect_android_class`, `inspect_android_method`, `trace_android_references`):** Decompiles `classes*.dex` directly into structured Java/Kotlin source code with cross-reference navigation.
- **`dex2jar (d2j)` + `CFR` / `Procyon` / `JD-GUI` / `Bytecode Viewer`:** Secondary decompilation pipeline for complex bytecode constructs.

### Stage 4: Cross-Platform Framework Tools (Flutter, React Native, Unity)
- **Flutter (`identify_flutter_build`, `inspect_dart_aot`, `Blutter`, `reFlutter`):** Parses `libapp.so` (Dart AOT snapshot) and `libflutter.so` to recover Dart packages, class structures, functions, and offsets.
- **React Native (`hermes-dec`, `hbctool`):** Disassembles and decompiles React Native Hermes bytecode (`assets/index.android.bundle`).
- **Unity (`Il2CppDumper`, `AssetStudio`):** Recovers C# class, method, and field definitions from `libil2cpp.so` + `global-metadata.dat` and extracts 3D/2D game assets.
- **`uber-apk-signer`:** Aligns (`zipalign`) and re-signs repackaged APKs for testing.

### Stage 5: Native Library Analysis (C/C++ `.so` & iOS Mach-O)
- **REA MCP (`open_binary`, `list_procedures`, `procedure_pseudo_code`, `batch_decompile`, `xrefs`, `inspect_macho`, `get_objc_classes`, `analyze_swift_types`, `demangle_swift`):** Disassembles and decompiles ARM64/ARMv7/x86_64 native binaries.
- **Ghidra / IDA Pro / Binary Ninja / Rizin (Cutter):** Deep control-flow and `JNI_OnLoad` / `Java_*` / `RegisterNatives` inspection.
- **`strings` / `readelf` / `objdump` / `nm`:** Extracts native strings, ELF headers, and imported/exported symbol tables.

### Stage 6: Protection, Obfuscation & Packer Detection
- **`APKiD`:** Identifies compilers, obfuscators (R8/ProGuard, DexGuard), and commercial packers (SecNeo, Bangcle, Tencent Legu, Jiagu).
- **`Simplify` / `de4js`:** Deobfuscates virtualized Smali/JS logic and string encryption routines.
- **`Frida-DEXDump`:** Dumps decrypted `.dex` payloads directly from runtime memory on packed applications.

### Stage 7: Network & API Traffic Analysis
- **Burp Suite / OWASP ZAP / HTTP Toolkit / `mitmproxy` / Reqable:** Intercepts and analyzes HTTP/HTTPS, REST, GraphQL, and WebSocket API traffic.
- **Wireshark & REA MCP (`inspect_pcap_capture`, `inspect_packet_fields`):** Inspects raw TCP/UDP, DNS, TLS handshakes, and custom binary protocols.

### Stage 8: Dynamic Analysis & Runtime Instrumentation
- **Frida & REA MCP (`list_frida_devices`, `start_frida_session`, `instrument_with_frida`, `observe_native_calls`):** Hooks Java/Kotlin methods and native C/C++ functions at runtime to inspect arguments, return values, cryptographic keys, and certificate pinning posture.
- **Objection:** Runtime exploration of memory, Android Keystore / iOS Keychain, file systems, and activities without custom scripts.
- **LSPosed / Xposed Framework:** On-device method hooking.

### Stage 9: Local Storage, Databases & Cryptography Inspection
- **SQLite (`inspect_sqlite_database`, `sqlite3`, DB Browser for SQLite):** Inspects `/data/data/<package_name>/databases/*.db`.
- **SharedPreferences & Plists (`inspect_plist`, `inspect_keyed_archive`):** Audits `shared_prefs/*.xml` and iOS `NSUserDefaults` / `NSKeyedArchiver` files.
- **KeyStore Explorer / `keytool` / `apksigner`:** Verifies APK signing certificates and v1/v2/v3/v4 signature schemes.

### Stage 10: Automated Security Scanners
- **MobSF (Mobile Security Framework), PTKD, Quark-Engine, APKHunt, QARK, AndroBugs, Guardsquare AppSweep:** Automated static and dynamic vulnerability scanning mapped against OWASP Mobile Top 10 and OWASP MASVS.

---

## 3. Standard 5-Step Mobile Analysis & Recovery Workflow Checklist

Execute these 5 steps automatically on every mobile task:
1. **Fingerprint:** Run `APKiD` / `inspect_android_package` / `identify_flutter_build` to identify the tech stack (Kotlin/Java, Flutter, React Native, Unity, Swift/ObjC) and any obfuscation/packing.
2. **Decode Manifest & Resources:** Run `Apktool` / `decode_android_resources` to audit `AndroidManifest.xml` (permissions, `android:exported="true"`, deep links, `network_security_config.xml`) and `res/values/strings.xml`.
3. **Decompile Code:** Use `JADX` / REA MCP `search_android_classes` & `inspect_android_class` to recover full source code, API endpoints, models, and cryptographic logic.
4. **Analyze Native & Framework Code:** Use `Ghidra` / REA MCP `open_binary` for `.so` libraries or framework-specific tools (`Blutter`/`inspect_dart_aot`, `hermes-dec`, `Il2CppDumper`).
5. **Dynamic Audit & Full Project Reconstruction:** Run dynamic checks with `Frida` / `adb` if a device is connected, and reconstruct a 100% complete, zero-skeleton Android Studio / Xcode project or security remediation report.
