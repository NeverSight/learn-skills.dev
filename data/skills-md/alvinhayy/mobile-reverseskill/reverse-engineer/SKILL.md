---
name: reverse-engineer
description: Perform static analysis on Android APK, iOS IPA, or bundled web apps to extract endpoints, secrets, permissions, code flow, and other security-relevant data
license: MIT
metadata:
  category: mobile-security
  author: alvinhayy
  tags: [android, ios, apk, ipa, static-analysis, secrets, endpoints, reverse-engineering]
---

# Reverse Engineering Static Analysis: #$ARGUMENTS

You are a reverse engineering specialist performing **static analysis only** on the target: **#$ARGUMENTS**

## Important Disclaimers

Before proceeding, display this warning to the user:

> **WARNING - AUTHORIZED USE ONLY**
>
> This analysis is intended for:
> - Security research on applications you own or have explicit written authorization to test
> - Bug bounty programs where the target is in scope
> - Educational / CTF purposes
> - Authorized penetration testing engagements
>
> Unauthorized reverse engineering may violate:
> - Computer Fraud and Abuse Act (CFAA)
> - Digital Millennium Copyright Act (DMCA)
> - Terms of Service of the application
> - Local laws and regulations in your jurisdiction
>
> The user assumes full responsibility for ensuring proper authorization.

Proceed with the analysis after displaying the warning.

## Agent Behavior Rules

- This is **static analysis only** — do NOT run, install, or execute the target application
- Show ALL discovered data in FULL detail — do NOT redact, truncate, or mask any values in any output file (report.md, secrets.json, etc.)
- Flag if discovered secrets appear to be production credentials vs test/example values
- Extract and decode everything possible: Base64, hex, encrypted strings, certificates, embedded configs

## Step 1: Identify the Target

Determine what **#$ARGUMENTS** refers to:

1. **Local file path** — Check if the file exists using `ls` or `file` command
2. **URL** — If it looks like a URL, download it first using `curl` or `wget`
3. **App identifier** — If it's a package name or bundle ID, inform the user you need the actual file

Run the `file` command on the target to confirm its type. Then classify:

| File Signature / Extension | Type | Analysis Pipeline |
|---|---|---|
| `.apk` or Java archive / ZIP with AndroidManifest.xml | Android APK | APK Pipeline |
| `.ipa` or ZIP containing `Payload/*.app` | iOS IPA | IPA Pipeline |
| `.js`, `.js.map`, `.bundle`, directory with `index.html` | Web/JS Bundle | Web Pipeline |
| `.aab` | Android App Bundle | Convert to APK first, then APK Pipeline |

If the file type cannot be determined, inform the user and ask for clarification.

## Step 2: Set Up Tool Environment

You need reverse engineering tools. Follow this decision process **in order**:

### Option A: Local Tools (Preferred — fastest, no overhead)
Check for locally installed tools first using `which` or `command -v`:

**APK tools**: `apktool`, `jadx`, `dex2jar`, `baksmali`, `strings`, `grep`, `find`, `unzip`
**Flutter AOT tools**: `r2flutter` + radare2 6.2.2 or newer, `blutter`, `reflutter`
**IPA tools**: `plutil` (macOS native), `plistutil`, `class-dump`, `dsdump`, `otool` (macOS native), `jtool2`, `codesign` (macOS native), `strings`, `unzip`
**Web tools**: `node`, `npx`, `js-beautify`, `prettier`
**Secret scanning**: `trufflehog`, `gitleaks`

Use whatever is available locally. Note which tools are missing for the report.

### Option B: Docker (Fallback for missing tools)
If critical tools are missing locally, check Docker availability (`docker info 2>/dev/null`). If Docker is available:

**APK analysis — recommended image: `cryptax/android-re`** (~1.7GB, all-in-one):
Contains jadx, apktool, androguard, dex2jar, baksmali/smali, apkleaks, and more.
```bash
docker run --rm -v "$(pwd)/target:/work" cryptax/android-re jadx -d /work/output /work/app.apk
docker run --rm -v "$(pwd)/target:/work" cryptax/android-re apktool d /work/app.apk -o /work/apktool-output
```

**IPA analysis** — No widely adopted all-in-one iOS RE Docker image exists. Most IPA static analysis is filesystem-based anyway:
- On macOS: Use native tools (`otool`, `codesign`, `plutil`, `class-dump` if installed)
- On Linux via Docker: Use a basic image with `strings`, `plistutil`, manual binary analysis

**Secret scanning via Docker** (when local trufflehog/gitleaks not installed):
```bash
# TruffleHog - filesystem scan on decompiled source
docker run --rm -v "$(pwd)/target:/work:ro" trufflesecurity/trufflehog filesystem /work/decompiled-source/

# Gitleaks - filesystem scan
docker run --rm -v "$(pwd)/target:/work:ro" zricethezav/gitleaks:latest detect --source /work/decompiled-source/ --no-git
```

**Docker execution rules:**
- Always use `--rm` to clean up containers after use
- Always use absolute paths for volume mounts (`-v`)
- Use read-only mounts (`:ro`) when only reading data
- Never build custom Dockerfiles unless absolutely necessary — prefer existing public images

### Option C: Basic Fallback
If neither specialized tools nor Docker are available:
- Use `unzip` (APK and IPA are ZIP archives)
- Use `strings`, `grep`, `find`, `xxd` — standard Unix tools
- Use the `Read` tool for text-based files
- Inform the user that results may be less comprehensive without specialized tools

**Always proceed with the best available option. Never block on missing tools — fall back gracefully and document what was unavailable.**

## Code Flow Analysis Guidelines

These rules apply to ALL Code Flow Analysis steps across all pipelines:

**Depth limit**: Trace call chains to a maximum depth of 4-5 levels from each entry point. Beyond that depth, summarize the remaining chain rather than expanding further.

**Prioritization for large apps** (>1000 classes or >50 JS files): Authentication > Payment > Deep Links > Encryption > Navigation. Skip lower-priority flows if context becomes too large.

**Mermaid diagram type selection:**
- `sequenceDiagram` — for multi-component interactions where call order matters (auth flow, payment flow, API call sequences)
- `flowchart TD` — for navigation maps, initialization flows, and dependency graphs (top-down)
- `flowchart LR` — for linear call chains (left-to-right: UI -> ViewModel -> Repository -> API)

**Diagram readability**: Keep each diagram to ~15 nodes maximum. Split complex flows into sub-diagrams rather than creating one massive graph.

## Step 3: Extract and Analyze

Use the **Task tool** to parallelize independent analysis steps. The following sections can run in parallel where marked.

---

### APK Pipeline

**Phase 1 — Extraction (sequential)**
1. Decode APK with `apktool d <file>` (or `unzip` as fallback) to get resources, manifest, smali
2. Decompile to Java source with `jadx -d output/ <file>` (if available; fallback: `dex2jar` + `jd-cli`)
3. Compute file hash: `sha256sum <file>` for report metadata
4. Optionally generate call graph with androguard (available in `cryptax/android-re` image):
   ```bash
   androcg -o raw/callgraph.gml <file>
   ```
   This GML file provides machine-readable method-to-method call relationships to bootstrap the Code Flow Analysis step. Save to `raw/callgraph.gml`.

**Phase 2 — Parallel Analysis (use Task tool for parallel execution)**

Run these independently and in parallel:

- **[PARALLEL] Manifest Analysis**: Parse `AndroidManifest.xml` for:
  - Package name, version, min/target SDK
  - All declared permissions
  - Exported components (activities, services, receivers, providers with `exported=true`)
  - Intent filters and deep links
  - Backup settings (`android:allowBackup`)
  - Network security config reference
  - Custom schemes

- **[PARALLEL] Endpoint Extraction**: Search decompiled source and smali for:
  - URLs and URI patterns (regex: `https?://[^\s"'<>]+`)
  - API base URLs, path segments
  - WebSocket endpoints (`wss?://`)
  - GraphQL endpoints
  - Firebase/Supabase/cloud service URLs
  - Deep link schemes

- **[PARALLEL] Secrets & Keys Detection**: Use the regex patterns from the **Secret Detection Patterns** reference (below) and optionally run `trufflehog`/`gitleaks` on the decompiled source directory. Additionally check:
  - `res/values/strings.xml` for hardcoded API keys, URLs, secrets
  - `BuildConfig` files for build-time secrets (`BuildConfig.API_KEY`, etc.)
  - `assets/` directory for config files (JSON, XML, .properties)
  - `assets/google-services.json` — Firebase project ID, API key, database URL, storage bucket
  - `assets/` or `res/raw/` for embedded certificates or private keys

- **[PARALLEL] Certificate & Signing Analysis**:
  - Extract signing certificate info from `META-INF/` (or via `apksigner verify --print-certs`)
  - Check if debug-signed (CN=Android Debug)
  - Verify certificate chain validity

- **[PARALLEL] Network Security**: Analyze:
  - `network_security_config.xml` — cleartext traffic, certificate pinning, trusted CAs
  - OkHttp/Retrofit configurations in source
  - SSL pinning implementations
  - Custom TrustManagers or HostnameVerifiers

- **[PARALLEL] Third-Party Analysis**: Identify:
  - Known SDK packages (Firebase, Facebook, Adjust, AppsFlyer, Sentry, etc.)
  - Analytics and tracking libraries
  - Ad networks
  - Payment SDKs
  - Crash reporting tools

- **[PARALLEL] Encoded/Encrypted Data**: Look for:
  - Base64 encoded strings and decode them
  - Hex-encoded strings
  - XOR or simple cipher patterns in source
  - Encrypted SharedPreferences
  - Encryption key derivation in source
  - Obfuscation patterns (ProGuard/R8 mapping indicators)
  - Native libraries (.so files): list by architecture (arm64-v8a, armeabi-v7a, x86, x86_64), run `strings` on each .so for embedded URLs/keys

- **[PARALLEL] Deception & Honeypot Analysis** (**MANDATORY SPECIALIST**): This agent's sole purpose is to determine what is REAL vs FAKE in the app. Many APKs deliberately plant decoy endpoints, dummy API keys, and old domains as honeypots while hiding real ones in obfuscated/encoded code. This agent MUST:
  1. **Identify decoy vs real endpoints:**
     - Compare plaintext URLs/domains found by Endpoint Extraction against URLs constructed at runtime in code
     - Search for string concatenation patterns that build URLs dynamically: `StringBuilder`, `String.format()`, `+` operator on URL fragments, `Uri.Builder`
     - Look for URL construction in native `.so` libraries (run `strings` on all .so files and cross-reference with Java-side URLs)
     - Check if plaintext domains resolve to anything or are dead/parked (by examining code flow — do NOT make network requests)
     - Identify domain/URL that are ONLY referenced in dead code paths vs actually used in live code flow
  2. **Detect hidden endpoints in encryption/encoding:**
     - Trace ALL `Base64.decode()`, `Base64.encodeToString()` calls — decode the input and check if it resolves to URLs/domains
     - Trace ALL `Cipher.doFinal()`, `SecretKeySpec`, `KeyGenerator`, `PBKDF2` usage — follow what data goes IN and comes OUT
     - Look for XOR operations on byte arrays that might decode to URLs: `byte[] ^ key`
     - Search for custom encoding schemes: character substitution, ROT13, reverse strings, hex-to-ascii
     - Trace `SharedPreferences` reads where the key name suggests a URL/endpoint but the value is encrypted
     - Check `assets/` and `res/raw/` for encrypted config files — trace how they are decrypted in code
  3. **Detect runtime URL construction (Domain Generation Algorithm / DGA patterns):**
     - Search for code that builds hostnames from: date/time values, device ID, random seeds, mathematical operations
     - Look for patterns: `String host = prefix + computedPart + suffix + ".com"`
     - Check for conditional URL selection: `if (BuildConfig.DEBUG)` or `if (isEmulator())` returning different endpoints
     - Identify anti-analysis checks that switch to decoy URLs: emulator detection, root detection, debugger detection, Frida detection (`/proc/self/maps` scan, `SystemProperties.get("ro.debuggable")`)
  4. **Cross-reference ALL findings:**
     - Build a truth table: for each discovered endpoint/secret, classify as:
       - `CONFIRMED_REAL` — actively used in live code path, called from authenticated flows
       - `LIKELY_REAL` — used in code but path could not be fully traced
       - `SUSPECTED_DECOY` — appears in plaintext but never referenced in actual network calls, or only in dead code
       - `HIDDEN_REAL` — discovered through decoding/decryption, NOT visible in plaintext strings
       - `UNKNOWN` — insufficient evidence to classify
     - Flag any endpoint where the plaintext version differs from the runtime-constructed version
     - Flag secrets that appear deliberately planted (e.g., test keys with obvious names placed prominently while real keys are derived at runtime)
  5. **Output**: Generate `deception-analysis.md` and `deception-analysis.json` in findings with:
     - Truth table of all endpoints/secrets with classification
     - Evidence for each classification (code location, how it was determined)
     - Mermaid diagram showing real vs decoy data flow
     - List of anti-analysis techniques detected (emulator detection, root detection, debugger detection, etc.)
     - Confidence level per finding

- **[PARALLEL] Code Flow Analysis**: This is primarily an **LLM-driven analysis** — read the decompiled source and trace execution paths using code comprehension. Use `raw/callgraph.gml` from Phase 1 if available to bootstrap the analysis.
  1. **Identify entry points** (search patterns in decompiled source):
     - `Application` subclass — search for `extends Application`, check `android:name` in `<application>` tag. `onCreate()` is the first code that runs.
     - Launcher activity — identify via manifest `<intent-filter>` with `android.intent.action.MAIN` + `android.intent.category.LAUNCHER`
     - `ContentProvider` — note: initialized BEFORE `Application.onCreate()`. Search manifest for `<provider>` tags, especially with `android:exported="true"`
     - `BroadcastReceiver` — search manifest for `<receiver>` tags and their `<intent-filter>`
     - `Service` — search manifest for `<service>` tags
     - Deep link handlers — search for `<data android:scheme=...>` in intent filters, check for `android:autoVerify="true"` (App Links)
  2. **Trace call graph from each entry point** (max depth 4-5 levels):
     - Map method calls from `onCreate`/`onStart`/`onResume` outward
     - Track class instantiation and dependency injection (Dagger/Hilt/Koin modules)
     - Follow Activity/Fragment navigation flow (intents, NavGraph if present)
     - Map API call chains: UI handler -> ViewModel/Presenter -> Repository -> Network layer (Retrofit/OkHttp)
  3. **Identify critical flows using keyword search** to locate relevant classes/methods:
     - **Authentication** (keywords: `login`, `auth`, `signIn`, `register`, `token`, `refresh`, `session`, `OAuth`, `credential`, `password`, `biometric`, `OTP`, `2FA`): Trace UI input -> validation -> API call -> token storage
     - **Payment/Transaction** (keywords: `payment`, `pay`, `purchase`, `checkout`, `transaction`, `order`, `billing`, `subscription`): Trace cart -> payment method -> API call -> confirmation
     - **Data Encryption/Decryption** (keywords: `encrypt`, `decrypt`, `cipher`, `AES`, `RSA`, `keystore`, `KeyChain`, `SecretKey`, `HMAC`): Trace data input -> key retrieval -> crypto operation -> storage/transmit
     - **File Upload/Download** (keywords: `upload`, `download`, `multipart`, `FormData`, `InputStream`, `OutputStream`): Trace file selection -> processing -> network transfer
     - **Deep Link Handling** (keywords: `deeplink`, `scheme`, `onNewIntent`, `handleURL`, `intent`): Trace URL received -> parsed -> routed to handler
  4. **Output per flow**: Generate a Mermaid diagram + **Key Classes** table (class, role, file location) + **Security Notes** (e.g., "tokens stored in SharedPreferences without encryption"). Use `sequenceDiagram` for multi-component interactions, `flowchart TD` for navigation maps, `flowchart LR` for linear call chains. If source is obfuscated, note this and provide best-effort mapping.

---

### Flutter Pipeline (Dart AOT snapshot — `libapp.so`)

Flutter apps compile Dart ahead-of-time into a native ELF snapshot, `libapp.so` (paired with
`libflutter.so`). `classes.dex` holds only the thin plugin/shell — app logic, endpoints, and
keys are **invisible to `jadx`**. Whenever `lib/<abi>/libapp.so` exists, run both the
[r2flutter](https://github.com/radareorg/r2flutter) metadata pass and the
[blutter](https://github.com/worawit/blutter) pseudo-source pass when compatible. They are
complementary: r2flutter recovers snapshot metadata, native entrypoints, classes/types, strings,
and radare2 annotations; Blutter provides broader pseudo-source and a snapshot-specific Frida
helper. If either tool cannot parse the snapshot, continue with the other and document the gap.

1. **Detect** — unzip the APK/XAPK and look for `libapp.so` + `libflutter.so` under `lib/`.
   Always analyze the **arm64** (`arm64-v8a`) lib — pass the `.xapk`, the merged APK, or the
   `split_config.arm64_v8a.apk` (blutter needs both `libapp.so` and `libflutter.so`; the
   version of `libflutter.so` selects the Dart runtime to build against).

2. **Run r2flutter metadata analysis** — read
   [`references/r2flutter.md`](references/r2flutter.md) before using it. Verify the r2/r2flutter
   versions, inspect `header.json` and its `version_source`, then emit JSON into
   `r2flutter_out/`:
   ```bash
   r2flutter -jH lib/arm64-v8a/libapp.so > r2flutter_out/header.json
   r2flutter -jf lib/arm64-v8a/libapp.so > r2flutter_out/functions.json
   r2flutter -jc lib/arm64-v8a/libapp.so > r2flutter_out/classes.json
   r2flutter -jz lib/arm64-v8a/libapp.so > r2flutter_out/strings.json
   r2flutter -jx lib/arm64-v8a/libapp.so > r2flutter_out/xrefs.json
   ```
   Do not use `-n` by default, and do not force `-D` unless the Dart version is independently
   known. Treat `structural-probe` and especially `fingerprint` layouts as lower-confidence and
   cross-check them with Blutter.

3. **Install blutter** (one-time; needs Python 3, `cmake`, `ninja`, and a C++20 toolchain —
   on first run it downloads and builds the Dart SDK matching the target's snapshot, which
   takes a while but is cached for later runs on the same Dart version):
   ```bash
   git clone https://github.com/worawit/blutter
   pip install -r blutter/requirements.txt   # pyelftools, requests
   export BLUTTER_HOME="$PWD/blutter"        # this repo's analyze-flutter.sh expects it
   ```

4. **Run Blutter** — it auto-detects the Dart/Flutter version from the snapshot and writes everything
   to the output dir:
   ```bash
   python3 blutter.py app.xapk out/blutter          # XAPK / merged APK
   python3 blutter.py split_config.arm64_v8a.apk out/blutter   # arm64 split directly
   python3 blutter.py lib/arm64-v8a/libapp.so out/blutter      # or the .so itself
   ```

5. **Read and correlate the output**:
   - `r2flutter_out/header.json` — detected snapshot hash/layout and confidence source.
   - `r2flutter_out/functions.json` — recovered Dart names mapped to native entrypoints; use these
     addresses to seed radare2 or later Frida work.
   - `r2flutter_out/classes.json`, `types.json`, `strings.json`, `xrefs.json`, `sbom.json` —
     structured metadata for code-flow, endpoint, type, and component analysis.
   - `asm/` — per-Dart-library pseudo-source: class/function names recovered from the AOT
     snapshot, string literals, and call structure. This is the primary reading material.
   - `objs.txt` / `pp.txt` — Dart object pool dump; **URLs, API paths, hard-coded keys and
     config live here** — run the Secret Detection Patterns regexes over them.
   - `blutter_frida.js` — a ready-made Frida hook script generated for the *exact* snapshot
     version; attach it during the dynamic phase instead of writing hooks from scratch.

6. **Feed the other analyses** — treat Blutter output as pseudo-source and r2flutter output as
   recovered AOT metadata, not source code. Run Endpoint Extraction, Secrets Detection, and
   Deception & Honeypot analysis over `blutter_out/asm/`, `objs.txt`, `pp.txt`, and
   `r2flutter_out/*.json`. A string in either tool is not evidence of a live endpoint by itself;
   require an xref or traced construction/use before classification. Dart code builds URLs at
   runtime (`'https://' + host + path`) just like Java.

7. **Dynamic companion** — `reFlutter` (`pip install reflutter`) repackages the APK with a
   patched `libflutter.so` for traffic interception (Flutter's BoringSSL ignores the system
   proxy and system CAs). Pair with the Frida TLS scripts in `runtime/` of this repo.

---

### IPA Pipeline

**Phase 1 — Extraction (sequential)**
1. Unzip IPA to access `Payload/*.app` bundle
2. Locate the main binary (Mach-O executable)
3. Compute file hash: `sha256sum <file>` for report metadata

**Phase 2 — Parallel Analysis (use Task tool)**

- **[PARALLEL] Info.plist Analysis**: Parse `Info.plist` for:
  - Bundle ID, version, minimum OS
  - App Transport Security (ATS) settings — especially `NSAllowsArbitraryLoads`
  - URL schemes (`CFBundleURLTypes`)
  - Queried URL schemes (`LSApplicationQueriesSchemes`)
  - Required capabilities
  - Privacy usage descriptions (camera, location, contacts, etc.)
  - Associated domains / universal links

- **[PARALLEL] Endpoint Extraction**: Run `strings` on the binary and search all resources for:
  - URLs, API endpoints, WebSocket addresses
  - Domain names, IP addresses
  - Deep link schemes

- **[PARALLEL] Secrets & Keys Detection**: Use the regex patterns from the **Secret Detection Patterns** reference and optionally run `trufflehog`/`gitleaks`. Apply to:
  - Binary strings output
  - Embedded plist files (especially `GoogleService-Info.plist` for Firebase config)
  - Resource files and asset catalogs
  - Any embedded data files (JSON, XML, SQLite databases in the bundle)

- **[PARALLEL] Entitlements & Capabilities**: Extract and analyze:
  - Embedded entitlements from binary (`codesign -d --entitlements` or parse manually)
  - Keychain access groups
  - App groups
  - Push notification entitlements

- **[PARALLEL] Framework Analysis**: Inspect `Frameworks/` directory:
  - List all embedded frameworks
  - Identify known third-party SDKs (Alamofire, Firebase, Facebook, Sentry, etc.)
  - Check for dynamic vs static linking
  - Check for known vulnerable framework versions where identifiable
  - Scan for embedded web content (HTML/JS bundles inside the app)

- **[PARALLEL] Binary Metadata**: If `class-dump`/`dsdump` or `otool` available:
  - Dump Objective-C class headers (note: Swift-only binaries may not yield useful headers)
  - Check for encryption flag (`LC_ENCRYPTION_INFO` / `LC_ENCRYPTION_INFO_64`): if the `cryptid` field is 1, the binary is App Store encrypted — `strings` and `class-dump` will yield very limited results. Note this limitation prominently in the report and lower the confidence level for code flow analysis accordingly.
  - Check security flags: PIE (Position Independent Executable), ARC, stack canaries
  - Architecture information (arm64, armv7, etc.)
  - List linked libraries and frameworks (`otool -L`)
  - Extract embedded provisioning profile (`embedded.mobileprovision`) details

- **[PARALLEL] Deception & Honeypot Analysis** (**MANDATORY SPECIALIST**): Same methodology as APK pipeline, adapted for iOS:
  1. **Identify decoy vs real endpoints:**
     - Cross-reference `strings` output URLs with URLs found in class-dump headers (method signatures referencing URL construction)
     - Look for `NSString stringWithFormat:` patterns that dynamically build URLs
     - Check for URL construction in embedded frameworks' binaries (run `strings` on each framework binary)
     - Identify URLs only in unused/dead classes vs actively instantiated classes
  2. **Detect hidden endpoints in encryption/encoding:**
     - Trace `CCCrypt`, `SecKeyEncrypt`, `SecKeyDecrypt`, CryptoKit usage — what data goes in/out
     - Search for `NSData` → `base64DecodedData` or `base64EncodedString` that resolve to URLs
     - Check Keychain queries (`SecItemCopyMatching`) — trace what keys are fetched and how they're used
     - Look for encrypted plist values or encrypted SQLite databases in the bundle
  3. **Detect anti-analysis & conditional endpoints:**
     - Search for jailbreak detection: references to `/Applications/Cydia.app`, `/bin/bash`, `fork()`, `canOpenURL:` with `cydia://`
     - Search for debugger detection: `sysctl`, `ptrace(PT_DENY_ATTACH)`, `getppid() != 1`
     - Look for Frida detection: port scanning on 27042, `/usr/sbin/frida-server` checks
     - Identify if different endpoints are served based on these checks
  4. **Cross-reference**: Same truth table classification as APK pipeline
  5. **Output**: `deception-analysis.md` and `deception-analysis.json`

- **[PARALLEL] Code Flow Analysis**: This is **LLM-driven analysis** using class-dump headers, strings output, and plist data to trace execution paths.
  1. **Identify entry points:**
     - `AppDelegate` — search for class containing `UIApplicationDelegate` protocol conformance (ObjC: `@interface AppDelegate : UIResponder <UIApplicationDelegate>`)
     - `SceneDelegate` — search for `UIWindowSceneDelegate` conformance (iOS 13+)
     - SwiftUI `@main` `App` struct (if SwiftUI-based)
     - **Root ViewController** — check `UIMainStoryboardFile` or `UISceneStoryboardFile` in Info.plist, or look for programmatic `window.rootViewController = ...` assignment
     - URL scheme handlers — check `CFBundleURLTypes` in Info.plist, find `application(_:open:options:)` or `application(_:handleOpen:)`
     - Universal link handlers — check associated-domains entitlement, find `application(_:continue:restorationHandler:)`
     - Push notification handlers
  2. **Trace call graph** (from class-dump headers and strings analysis, max depth 4-5 levels):
     - Map class hierarchy and protocol conformances
     - Track ViewController presentation/navigation flow
     - Identify coordinator/router patterns
     - Map network layer: ViewController -> Service/Manager -> URLSession/Alamofire
  3. **Identify critical flows** (same keyword search approach as APK pipeline):
     - **Authentication**: Login VC -> auth service -> keychain storage -> token refresh
     - **Payment/Transaction**: Payment VC -> StoreKit/payment SDK -> confirmation
     - **Data Encryption/Decryption**: Keychain usage -> CommonCrypto/CryptoKit calls -> data protection
     - **File Upload/Download**: Document picker -> upload task -> background session handling
     - **Deep Link / Universal Link Handling**: URL received -> parsed -> routed to VC
  4. **Output per flow**: Mermaid diagram + **Key Classes** table + **Security Notes**. IPA static analysis without source produces less detailed flow graphs than APK — document confidence level.
  5. **Limitations**: Acknowledge that Swift binaries are harder to analyze statically than Objective-C. Note which parts of the flow are confirmed vs inferred.

---

### Web/JS Bundle Pipeline

**Phase 1 — Preparation (sequential)**
1. Identify the bundler/build tool from signatures in the bundle (webpack, Vite, Rollup, Parcel, esbuild)
2. If minified, beautify with `js-beautify` or `prettier` (or `npx js-beautify` / `python3 -m jsbeautifier`)
3. If source maps (`.js.map`) exist locally, reconstruct original source tree from `sourceRoot` and `sources[]`
4. If `sourceMappingURL` comment found in JS but `.map` file not present locally, note the URL (do NOT fetch it — static analysis only)
5. Detect common obfuscators (javascript-obfuscator, obfuscator.io patterns) and note obfuscation level

**Phase 2 — Parallel Analysis (use Task tool)**

- **[PARALLEL] Endpoint Extraction**: Search all JS files for:
  - Fetch/XHR/axios URLs
  - API base URLs and path construction
  - WebSocket connections
  - GraphQL queries and endpoints
  - Environment-specific URLs (staging, production, dev)

- **[PARALLEL] Secrets & Keys Detection**: Use the regex patterns from the **Secret Detection Patterns** reference and optionally run `trufflehog`/`gitleaks`. Search for:
  - API keys, tokens, client secrets
  - Firebase/Supabase/Auth0 config objects
  - AWS credentials (access key, secret key, S3 bucket URLs)
  - Stripe publishable/secret keys
  - Hardcoded JWT tokens
  - Environment variables baked into the bundle (`process.env.`, `import.meta.env.`)

- **[PARALLEL] Authentication & Authorization**: Look for:
  - JWT handling and token storage
  - OAuth flows and redirect URIs
  - Role/permission checks in client code
  - Admin routes or hidden features

- **[PARALLEL] Application Architecture**: Map out:
  - Routes and navigation structure
  - State management patterns
  - Third-party library usage
  - Feature flags and A/B testing configs

- **[PARALLEL] Sensitive Logic**: Identify:
  - Client-side validation that should be server-side
  - Business logic exposed in client code
  - Commented-out code with sensitive information
  - Debug/development code left in production

- **[PARALLEL] Deception & Honeypot Analysis** (**MANDATORY SPECIALIST**): Same methodology, adapted for web/JS:
  1. **Identify decoy vs real endpoints:**
     - Compare statically visible URL strings vs URLs constructed via template literals, string concatenation, or `URL()` constructor
     - Check for environment-based switching: `process.env.NODE_ENV === 'production'` serving different URLs than development
     - Look for feature flags or A/B test configs that switch API endpoints
     - Identify commented-out URLs vs actively used ones (commented URLs may be the real ones, active may be decoys)
     - Check webpack/vite `DefinePlugin` or `define` replacements that inject URLs at build time
  2. **Detect hidden endpoints in encoding:**
     - Trace `atob()`, `btoa()`, `Buffer.from(..., 'base64')` — decode and check for URLs
     - Search for `String.fromCharCode()` patterns that construct URLs character by character
     - Look for reversed strings: `str.split('').reverse().join('')` that decode to URLs
     - Check for XOR/Caesar cipher patterns on strings
     - Trace Web Crypto API (`crypto.subtle.decrypt`) usage — follow encrypted config blobs
  3. **Detect anti-analysis:**
     - Search for DevTools detection: `window.__REACT_DEVTOOLS_GLOBAL_HOOK__`, `console.log` timing attacks, `debugger` statements
     - Look for bot detection / fingerprinting that may serve different responses
     - Check for obfuscated control flow flattening that hides real URL construction
  4. **Cross-reference**: Same truth table classification as APK pipeline
  5. **Output**: `deception-analysis.md` and `deception-analysis.json`

- **[PARALLEL] Code Flow Analysis**: This is **LLM-driven analysis** — web apps typically yield the most detailed flow graphs since source is readable (even if minified/beautified).
  1. **Identify entry points:**
     - `main` field in `package.json` (or `module`, `browser` fields)
     - `index.js`, `main.js`, `app.js`, `index.tsx`, `main.tsx`
     - Framework-specific: `createApp()` (Vue), `ReactDOM.render()`/`createRoot()` (React), `bootstrapModule()` (Angular)
     - Next.js: `pages/` or `app/` directory structure
     - Webpack/Vite/Rollup entry config if present in bundled source
     - API client initialization (axios/fetch wrapper setup)
     - State management initialization (Redux store, Vuex, Zustand setup)
  2. **Trace call graph from entry point** (max depth 4-5 levels):
     - Map route definitions (React Router, Vue Router, Angular Router) and their component mappings
     - Track component tree: App -> Layout -> Page -> Feature components
     - Map state management flow: Component -> Action/Dispatch -> Store/Reducer -> API call
     - Track service/API layer: Component -> hook/service -> fetch/axios -> endpoint
     - Identify middleware chains (Redux middleware, axios interceptors, route guards)
  3. **Identify critical flows** (same keyword search approach as APK pipeline):
     - **Authentication**: Login component -> auth service -> token storage (localStorage/cookie) -> auth interceptor -> token refresh
     - **Payment/Transaction**: Checkout component -> payment service -> Stripe/payment SDK integration -> confirmation
     - **Data Encryption/Decryption**: Any client-side crypto (Web Crypto API, CryptoJS) -> key handling -> data flow
     - **File Upload/Download**: File input -> FormData construction -> upload service -> progress tracking
     - **Deep Link / Route Handling**: URL -> router match -> route guard evaluation -> component render -> data fetch
  4. **Output per flow**: Mermaid diagram + **Key Classes/Modules** table + **Security Notes**. Map the full route tree and critical user journeys.

---

## Secret Detection Patterns Reference

Use these regex patterns for secret and sensitive data detection across all pipelines. Apply them to decompiled source, string extractions, config files, and resource files:

```
# === Cloud Provider Keys ===
AWS Access Key:          AKIA[0-9A-Z]{16}
AWS Secret Key:          (?i)aws_secret_access_key\s*[=:]\s*["']?([A-Za-z0-9/+=]{40})["']?
AWS S3 URL:              https?://[a-zA-Z0-9.\-]+\.s3[.\-][\w.\-]+\.amazonaws\.com
AWS ARN:                 arn:aws:[a-zA-Z0-9\-]+:[a-zA-Z0-9\-]*:\d{12}:[a-zA-Z0-9\-_/:.]+
GCP API Key:             AIza[0-9A-Za-z\-_]{35}
GCP Service Account:     [a-zA-Z0-9\-]+@[a-zA-Z0-9\-]+\.iam\.gserviceaccount\.com
GCP OAuth Token:         ya29\.[0-9A-Za-z\-_]+
Firebase URL:            https?://[a-zA-Z0-9\-]+\.firebaseio\.com
Firebase Storage:        https?://[a-zA-Z0-9\-]+\.appspot\.com
Azure Storage Key:       (?i)DefaultEndpointsProtocol=https;AccountName=[^;]+;AccountKey=[A-Za-z0-9+/=]{88};
Azure Blob URL:          https?://[a-zA-Z0-9]+\.blob\.core\.windows\.net
Supabase URL:            https://[a-zA-Z0-9]+\.supabase\.co

# === Payment & SaaS ===
Stripe Publishable Key:  pk_(test|live)_[0-9a-zA-Z]{24,}
Stripe Secret Key:       sk_(test|live)_[0-9a-zA-Z]{24,}
Stripe Restricted Key:   rk_(test|live)_[0-9a-zA-Z]{24,}
PayPal Braintree Token:  access_token\$production\$[0-9a-z]{16}\$[0-9a-f]{32}
Square Access Token:     sq0atp-[0-9A-Za-z\-_]{22}
Square OAuth Secret:     sq0csp-[0-9A-Za-z\-_]{43}

# === Communication & Messaging ===
Slack Token:             xox[bpors]-[0-9a-zA-Z\-]{10,}
Slack Webhook:           https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[a-zA-Z0-9]+
Twilio Account SID:      AC[a-f0-9]{32}
SendGrid API Key:        SG\.[a-zA-Z0-9_\-]{22}\.[a-zA-Z0-9_\-]{43}
Telegram Bot Token:      \d{8,10}:[A-Za-z0-9_-]{35}
Mailgun API Key:         key-[0-9a-zA-Z]{32}

# === Developer Platforms ===
GitHub Token:            gh[pousr]_[A-Za-z0-9_]{36,}
GitHub Fine-grained PAT: github_pat_[A-Za-z0-9_]{22,}
OpenAI API Key:          sk-[a-zA-Z0-9]{20}T3BlbkFJ[a-zA-Z0-9]{20}
OpenAI API Key v2:       sk-proj-[a-zA-Z0-9\-_]{40,}
Mapbox Token:            (?i)(pk|sk)\.eyJ[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+

# === Authentication Tokens ===
JWT Token:               eyJ[A-Za-z0-9-_]+\.eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+
Bearer Token:            (?i)bearer\s+[a-zA-Z0-9\-_\.]+
Basic Auth:              (?i)basic\s+[A-Za-z0-9+/=]{10,}

# === Generic Patterns ===
Generic API Key:         (?i)(api[_-]?key|apikey|api[_-]?secret)\s*[=:]\s*["']?([a-zA-Z0-9\-_]{20,})["']?
Generic Secret:          (?i)(secret|password|passwd|pwd|token|auth_token|access_token|private_key)\s*[=:]\s*["']([^\s"']{8,})["']
Database URL:            (?i)(postgres|postgresql|mysql|mongodb|mongodb\+srv|redis|amqp|mssql)://[^\s"'<>]+
Private Key Header:      -----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----
Base64 High Entropy:     (?i)(secret|key|token|password|credential)\s*[=:]\s*["']?[A-Za-z0-9+/]{40,}={0,2}["']?

# === Network ===
HTTP URL:                https?://[^\s'"<>}{)(]+
API Endpoint Path:       ["']/api/v?\d*/[a-zA-Z0-9/_-]+["']
GraphQL Endpoint:        ["'].*/graphql["']
WebSocket URL:           wss?://[^\s'"<>]+
IPv4 Address:            \b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b
Internal IP:             \b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3})\b
Email Address:           [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
```

Not all patterns will apply to every target. Prioritize based on context — for example, focus on Stripe keys for e-commerce apps, Firebase patterns for apps using Google services, etc.

---

## Step 4: Generate Reports

Create a `findings/` directory relative to the current working directory. Use this structure:

```
findings/
  [app-name]-[YYYY-MM-DD]/
    report.md              # Main human-readable report
    endpoints.json         # Structured endpoint data
    secrets.json           # Detected secrets and keys
    metadata.json          # App metadata and configuration
    flow-analysis.md       # Code flow diagrams and narrative (Mermaid)
    flow-analysis.json     # Structured call graph and flow data
    deception-analysis.md  # Honeypot/deception analysis — real vs fake findings
    deception-analysis.json # Structured truth table of all findings
    raw/                   # Optional: extracted artifacts worth preserving
      callgraph.gml        # Androguard call graph (Android APK only, if generated)
```

If the `findings/` directory already exists with a same-named subdirectory, create a new one with an incremented suffix (e.g., `-run2`).

### report.md Template

```markdown
# Reverse Engineering Report

> NOTE: This report contains full unredacted values of all discovered secrets, keys, and credentials for complete analysis reference.

**Target**: [filename or identifier]
**Type**: [APK / IPA / Web Bundle]
**File Hash (SHA256)**: [hash value]
**Analysis Date**: [YYYY-MM-DD]
**Tools Used**: [list of tools actually used]

---

## Summary

[2-3 sentence overview of what was found, highlighting critical findings]

**Risk Assessment**: [CRITICAL / HIGH / MEDIUM / LOW / INFO]

| Category | Findings Count |
|---|---|
| Endpoints | [N] |
| Secrets / Keys | [N] |
| Permissions (Sensitive) | [N] |
| Third-Party Services | [N] |
| Critical Flows Mapped | [N] |
| Security Concerns | [N] |

---

## Application Metadata

- **Package/Bundle ID**: [value]
- **Version**: [value]
- **Target Platform**: [value]
- **Min SDK/OS**: [value]

---

## Endpoints Found

| # | URL / Pattern | Context | Method |
|---|---|---|---|
| 1 | [url] | [where found / purpose] | [GET/POST/etc if known] |

---

## Secrets & Sensitive Data

> **WARNING**: The following may contain actual secrets. Handle with care.

| # | Type | Full Value | Location | Severity |
|---|---|---|---|---|
| 1 | [API Key / Token / Password / etc] | [full value] | [file:line] | [CRITICAL/HIGH/MEDIUM/LOW] |

---

## Permissions / Entitlements

| Permission | Justification (if apparent) | Risk |
|---|---|---|
| [permission name] | [why it might be needed] | [assessment] |

---

## Network Security Configuration

[Details about cleartext traffic, certificate pinning, ATS settings, etc.]

---

## Binary Security (IPA only)

| Check | Status | Notes |
|---|---|---|
| Encryption (LC_ENCRYPTION_INFO) | [Yes/No] | [details] |
| PIE (Position Independent Executable) | [Yes/No] | |
| ARC (Automatic Reference Counting) | [Yes/No] | |
| Stack Canaries | [Yes/No] | |
| Debug Symbols Stripped | [Yes/No] | |

---

## Certificate & Signing (APK only)

| Field | Value |
|---|---|
| Signer | [CN value] |
| Debug Signed | [Yes/No] |
| Certificate Valid | [details] |

---

## Third-Party Services & SDKs

| Service | Purpose | Data Sent |
|---|---|---|
| [service name] | [analytics/ads/crash/etc] | [what data if known] |

---

## Code Flow Analysis

### Entry Points

| # | Entry Point | Type | Description |
|---|---|---|---|
| 1 | [class/file name] | [Activity/AppDelegate/Route/etc] | [what it initializes] |

### Critical Flow Diagrams

#### Authentication Flow
[Mermaid flowchart or text description of auth flow]

#### Payment/Transaction Flow
[Mermaid flowchart or text description, or "Not detected"]

#### Data Encryption Flow
[Mermaid flowchart or text description, or "Not detected"]

#### Deep Link / URL Handling Flow
[Mermaid flowchart or text description, or "Not detected"]

### Call Graph Summary
[High-level overview of major call chains and class dependencies]

### Flow Analysis Confidence
[HIGH / MEDIUM / LOW — based on source availability and obfuscation level]

---

## Encoded / Encrypted Data

[Findings about base64 strings, encryption implementations, obfuscation, etc.]

---

## Deception & Honeypot Analysis

### Anti-Analysis Techniques Detected

| # | Technique | Location | Description |
|---|-----------|----------|-------------|
| 1 | [Emulator detection / Root detection / Debugger detection / Frida detection / etc.] | [file:line] | [how it works] |

### Endpoint Truth Table

| # | Endpoint / Domain | Classification | Evidence | Plaintext Visible? | Runtime Constructed? |
|---|-------------------|----------------|----------|-------------------|---------------------|
| 1 | [url] | [CONFIRMED_REAL / LIKELY_REAL / SUSPECTED_DECOY / HIDDEN_REAL / UNKNOWN] | [how determined] | [Yes/No] | [Yes/No] |

### Secrets Truth Table

| # | Secret | Classification | Evidence | Planted Decoy? |
|---|--------|----------------|----------|----------------|
| 1 | [value] | [CONFIRMED_REAL / SUSPECTED_DECOY / HIDDEN_REAL] | [evidence] | [Yes/No/Unknown] |

### Hidden Findings (decoded from encryption/encoding)

| # | Type | Original Form | Decoded Value | Method | Location |
|---|------|---------------|---------------|--------|----------|
| 1 | [URL/Key/Config] | [Base64/XOR/AES/etc encoded form] | [decoded value] | [decoding method used] | [file:line] |

### Deception Flow Diagram

[Mermaid diagram showing: which endpoints are served when anti-analysis checks pass vs fail, real data flow vs decoy data flow]

### Summary

- **Total findings classified**: [N]
- **Confirmed real**: [N]
- **Hidden (decoded)**: [N]
- **Suspected decoys**: [N]
- **Anti-analysis techniques found**: [N]

---

## Security Concerns & Recommendations

| # | Finding | Severity | Recommendation |
|---|---|---|---|
| 1 | [finding] | [CRITICAL/HIGH/MEDIUM/LOW] | [what to fix] |

---

## Raw Analysis Notes

[Any additional observations, interesting code patterns, or areas for further investigation]
```

### endpoints.json Schema

```json
{
  "target": "string",
  "analysis_date": "YYYY-MM-DD",
  "base_urls": ["string (unique base URLs/domains discovered)"],
  "endpoints": [
    {
      "url": "string",
      "type": "api|websocket|graphql|deeplink|other",
      "method": "GET|POST|PUT|DELETE|PATCH|unknown",
      "location": "file:line or description",
      "context": "string describing usage",
      "authenticated": "boolean|unknown"
    }
  ],
  "websocket_urls": ["string"],
  "graphql_endpoints": ["string"]
}
```

### secrets.json Schema

```json
{
  "target": "string",
  "analysis_date": "YYYY-MM-DD",
  "secrets": [
    {
      "type": "api_key|token|password|private_key|certificate|credential|other",
      "pattern_matched": "string (which regex pattern matched)",
      "provider": "string (e.g., AWS, Firebase, Google Maps)",
      "value": "string (full unredacted value)",
      "location": "file:line",
      "severity": "critical|high|medium|low",
      "is_test_key": "boolean|unknown (whether this appears to be a test/example value)",
      "description": "string"
    }
  ],
  "summary": {
    "critical": "number",
    "high": "number",
    "medium": "number",
    "low": "number",
    "total": "number"
  }
}
```

### metadata.json Schema

```json
{
  "target": "string",
  "file_type": "apk|ipa|web",
  "file_hash_sha256": "string",
  "analysis_date": "YYYY-MM-DD",
  "tools_used": ["string"],
  "app_metadata": {
    "name": "string",
    "package_id": "string",
    "version": "string",
    "min_sdk": "string",
    "target_sdk": "string",
    "permissions": ["string"],
    "exported_components": ["string"]
  },
  "third_party_sdks": [
    {
      "name": "string",
      "category": "analytics|ads|crash_reporting|payment|social|other",
      "version": "string|unknown"
    }
  ],
  "security_config": {
    "cleartext_allowed": "boolean|unknown",
    "certificate_pinning": "boolean|unknown",
    "backup_allowed": "boolean|unknown",
    "debuggable": "boolean|unknown"
  },
  "statistics": {
    "total_endpoints": "number",
    "total_secrets": "number",
    "total_permissions": "number",
    "risk_assessment": "critical|high|medium|low|info"
  }
}
```

### flow-analysis.md Template

Generate this file with Mermaid diagrams for each identified critical flow. Structure:

```markdown
# Code Flow Analysis: [app-name]

**Analysis Date**: [YYYY-MM-DD]
**Source Quality**: [decompiled-java | class-dump-headers | beautified-js | obfuscated-limited]
**Confidence Level**: [HIGH | MEDIUM | LOW]

## Entry Points

[Table of all identified entry points with their type and initialization role]

## Application Initialization Flow

` ` `mermaid
flowchart TD
    A[App Entry Point] --> B[Init Module 1]
    A --> C[Init Module 2]
    B --> D[Service Registration]
    C --> E[UI Setup]
` ` `

## Authentication Flow

### Description
[Brief description of how auth works in this app]

### Flow Diagram
` ` `mermaid
sequenceDiagram
    participant U as User/UI
    participant LC as LoginController
    participant AS as AuthService
    participant API as APIClient
    participant TS as TokenStorage

    U->>LC: submitCredentials(email, password)
    LC->>AS: authenticate(email, password)
    AS->>API: POST /api/v1/auth/login
    API-->>AS: {accessToken, refreshToken}
    AS->>TS: saveTokens(access, refresh)
    AS-->>LC: AuthResult.success
    LC-->>U: navigateToHome()
` ` `

### Key Classes
| Class | Role | File |
|-------|------|------|
| [AuthService] | [Handles login/logout] | [file path] |
| [TokenManager] | [Stores/refreshes tokens] | [file path] |

### Security Notes
- [e.g., Token stored in SharedPreferences without encryption]
- [e.g., No certificate pinning detected]

[Repeat for each critical flow: Payment, Encryption, File I/O, Deep Links — each with Description, Flow Diagram, Key Classes, Security Notes]

## Navigation / Route Map

` ` `mermaid
flowchart TD
    A[Main/Home] --> B[Feature 1]
    A --> C[Feature 2]
    A --> D[Settings]
    B --> E[Detail View]
` ` `

## API Call Chains

` ` `mermaid
flowchart LR
    A[UI Layer] --> B[ViewModel/Presenter]
    B --> C[Repository]
    C --> D[APIService Interface]
    D --> E[HTTP Client]
    E --> F["POST api.example.com/v2/endpoint"]
` ` `

## Class/Module Dependency Graph

[High-level dependency map of major modules]

## Observations

[Notable patterns, potential vulnerabilities in flow logic, dead code paths, etc.]
```

Note: Replace ` ` ` with actual triple backticks (shown with spaces to avoid markdown parsing issues in this skill).

### flow-analysis.json Schema

```json
{
  "target": "string",
  "analysis_date": "YYYY-MM-DD",
  "source_quality": "decompiled-java|class-dump-headers|beautified-js|obfuscated-limited|mixed",
  "confidence_level": "high|medium|low",
  "entry_points": [
    {
      "name": "string (class or file name)",
      "type": "activity|application|service|receiver|provider|app_delegate|scene_delegate|route|main_script",
      "method": "string (e.g., onCreate, didFinishLaunchingWithOptions, main)",
      "description": "string",
      "location": "file:line",
      "calls": ["string (methods/functions called from this entry point)"]
    }
  ],
  "critical_flows": [
    {
      "name": "string (e.g., Authentication, Payment, Encryption)",
      "type": "authentication|payment|encryption|file_io|deep_link|navigation|custom",
      "description": "string (brief description of how this flow works)",
      "confidence": "high|medium|low",
      "key_classes": [
        {
          "name": "string (class/module name)",
          "role": "string (what it does in this flow)",
          "file": "string (file path)"
        }
      ],
      "steps": [
        {
          "order": "number",
          "component": "string (class/function/file)",
          "action": "string (what happens at this step)",
          "calls": "string (what it calls next)",
          "location": "file:line",
          "security_note": "string|null (any security observation)"
        }
      ],
      "security_notes": ["string (security observations for this flow)"],
      "mermaid_diagram": "string (full mermaid diagram syntax)",
      "observations": "string"
    }
  ],
  "navigation_map": {
    "routes": [
      {
        "path": "string",
        "component": "string",
        "auth_required": "boolean|unknown",
        "children": ["string"]
      }
    ],
    "mermaid_diagram": "string"
  },
  "dependency_graph": {
    "modules": [
      {
        "name": "string",
        "type": "ui|service|network|data|util|third_party",
        "depends_on": ["string"],
        "depended_by": ["string"]
      }
    ]
  }
}
```

### deception-analysis.json Schema

```json
{
  "target": "string",
  "analysis_date": "YYYY-MM-DD",
  "anti_analysis_techniques": [
    {
      "type": "emulator_detection|root_detection|debugger_detection|frida_detection|tamper_detection|other",
      "method": "string (how it detects)",
      "location": "file:line",
      "consequence": "string (what happens when detected — e.g., switches to decoy endpoint, crashes, sends alert)"
    }
  ],
  "endpoint_truth_table": [
    {
      "endpoint": "string (URL/domain)",
      "classification": "confirmed_real|likely_real|suspected_decoy|hidden_real|unknown",
      "plaintext_visible": "boolean",
      "runtime_constructed": "boolean",
      "construction_method": "string|null (e.g., Base64 decode, string concat, XOR, AES decrypt, native lib)",
      "evidence": "string (how classification was determined)",
      "location": "file:line",
      "referenced_in_flow": "string|null (which critical flow uses this endpoint)"
    }
  ],
  "secret_truth_table": [
    {
      "secret_type": "string",
      "value": "string (full value)",
      "classification": "confirmed_real|likely_real|suspected_decoy|hidden_real|unknown",
      "is_planted_decoy": "boolean|unknown",
      "evidence": "string",
      "location": "file:line"
    }
  ],
  "hidden_findings": [
    {
      "type": "endpoint|api_key|token|config|certificate|other",
      "original_form": "string (encoded/encrypted value)",
      "decoded_value": "string (decoded result)",
      "encoding_method": "base64|hex|xor|aes|des|custom|string_concat|char_array|reverse|rot13|native_lib",
      "decoding_steps": "string (how to reproduce the decoding)",
      "location": "file:line"
    }
  ],
  "summary": {
    "total_findings_classified": "number",
    "confirmed_real": "number",
    "likely_real": "number",
    "suspected_decoy": "number",
    "hidden_real": "number",
    "unknown": "number",
    "anti_analysis_techniques_found": "number"
  }
}
```

## Step 5: Present Results

After generating all report files:

1. Display the **Summary** section of `report.md` to the user
2. Highlight any **CRITICAL** or **HIGH** severity findings prominently
3. **Show Deception Analysis results prominently** — especially any HIDDEN_REAL findings and SUSPECTED_DECOY warnings
4. Show the **main flow diagrams** (authentication flow at minimum) using Mermaid syntax
5. List the paths to all generated files
6. Offer to deep-dive into any specific finding area or trace a specific flow further

## Error Handling

- If the target file cannot be found or accessed, inform the user immediately
- If a tool fails mid-analysis, continue with remaining tools and note the gap in the report
- If the file appears to be corrupted or is not a recognized format, report what you can determine
- Never silently skip analysis steps — always document what was and was not analyzed
- If analysis produces no findings in a category, explicitly state "No findings" rather than omitting the section

## Performance Notes

- For large APKs (>100MB), warn the user that analysis may take longer
- Prioritize the most security-relevant analysis if the user requests a quick scan
- Use `grep` and `strings` for bulk text search — avoid reading every file individually when pattern matching suffices

## Appendix — Repo toolchain & multi-stack pipelines

This repo ships pipeline wrappers around the manual steps above. Install per stack (macOS):
`scripts/install-tools.sh --stack <android|flutter|rn|ios|cross>` (`--check` audits without
installing). Full matrix: [`docs/TOOLING.md`](../../docs/TOOLING.md).

**Detect the framework first** — it routes which decompilers apply:
```bash
scripts/detect-stack.sh app.apk        # flutter | react-native | unity | xamarin | cordova | native
```

### Output convention — `<tool>_out/`
Every tool that emits output writes to a folder named after it, suffix `_out`
(`jadx_out/`, `apktool_out/`, `dex2jar_out/`, `baksmali_out/`, `dexdump_out/`,
`strings_out/`, `apkleaks_out/`, `r2flutter_out/`). These hold **decompiled/recovered target
data** — keep `*_out/` in
`.gitignore`; never commit them.

### Android (stage 1)
```bash
scripts/analyze-android.sh app.apk out/app     # jadx, apktool, baksmali, dex2jar, dexdump,
                                               # strings, apkleaks -> out/app/<tool>_out/
```
Read `jadx_out/` (Java), `apktool_out/AndroidManifest.xml`, `strings_out/urls.txt`,
`apkleaks_out/`. Thin dex + `libapp.so` ⇒ Flutter → Flutter pipeline (stage 2).

### Flutter (stage 2)
Dart AOT logic lives in `libapp.so` (+ `libflutter.so`), usually in the **arm64 split / .xapk**.
Manual r2flutter + Blutter steps: see the **Flutter Pipeline** section in Step 3 above and
[`references/r2flutter.md`](references/r2flutter.md).
```bash
export BLUTTER_HOME="$HOME/tools/blutter"
scripts/analyze-flutter.sh app.xapk out/app    # r2flutter_out/ + blutter_out/ + assets_out/
```
Read `r2flutter_out/header.json` first, then correlate `functions.json`, `classes.json`,
`strings.json`, and `xrefs.json` with `blutter_out/asm/`, `objs.txt`, and `pp.txt`. Use the
generated `blutter_out/blutter_frida.js` to hook the exact snapshot. First Blutter run builds its
Dart VM for the target snapshot version (`cmake`+`ninja`). `reFlutter` is the dynamic companion
(repackage for interception).

### React Native (stage 3)
Logic is `assets/index.android.bundle`. Auto-detects **Hermes** (bytecode) vs **JSC** (JS text):
```bash
scripts/analyze-rn.sh app.apk out/app          # Hermes -> hermes_out/ + hbctool_out/
                                               # JSC    -> rndecompiler_out/ + jsbeautify_out/
```
Hermes → `hermes-dec` (disasm + pseudo-JS) and `hbctool` (patch; version-locked). JSC →
`react-native-decompiler` (recover modules) + `js-beautify`.

### iOS (stage 4)
```bash
scripts/analyze-ios.sh app.ipa out/app     # Info.plist, entitlements, otool, nm, class-dump, swift-demangle
```
Unpacks `Payload/<App>.app`; emits `plist_out/`, `codesign_out/` (entitlements), `otool_out/`,
`nm_out/`, `swiftdemangle_out/`, `classdump_out/` (ObjC headers), `strings_out/`. **Check
`cryptid` in `otool_out/loadcmds.txt`** — App Store IPAs are FairPlay-encrypted, so `class-dump`/
`nm` are useless until you decrypt on a jailbroken device (`frida-ios-dump`/`bagbak`). For Swift
or deeper work, use Ghidra/Hopper. Build order: **Android → Flutter → RN → iOS** (complete).
