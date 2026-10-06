---
name: android-static-analysis
description: Decompile Android APK, XAPK, JAR, and AAR files using jadx or Fernflower/Vineflower. Reverse engineer Android apps, extract HTTP API endpoints (Retrofit, OkHttp, Volley), trace call flows from UI to network layer, analyze obfuscated code. Use when the user wants to decompile, analyze, or reverse engineer Android packages, find API endpoints, follow call flows, or perform static analysis on Android applications.
---

# Android Static Analysis

Decompile Android APK, XAPK, JAR, and AAR files using jadx and Fernflower/Vineflower, trace call flows through application code and libraries, and produce structured documentation of extracted APIs.

## Prerequisites

This skill requires **Java JDK 17+** and **jadx**. **Fernflower/Vineflower** and **dex2jar** are optional but recommended.

Run the dependency checker:

```bash
bash ~/.pi/agent/skills/android-static-analysis/scripts/check-deps.sh
```

If anything is missing, see `references/setup-guide.md` in this skill directory.

---

# REQUIRED REFERENCE LOADING

Before selecting commands, load the static canonical routing references. Do not guess flags or randomly switch engines.

## Reference Files

| File | Read When |
|---|---|
| `references/canonical-scripts.md` | Selecting canonical script/profile IDs before execution |
| `references/script-metadata.manifest.json` | Deterministic routing: intent/file-type -> preferred/fallback profile IDs |
| `references/setup-guide.md` | Installing or repairing missing dependencies |
| `references/jadx-usage.md` | Jadx flags, deobf strategy, and APK workflows |
| `references/fernflower-usage.md` | Fernflower/Vineflower behavior and dex2jar flow |
| `references/api-extraction-patterns.md` | Retrofit/OkHttp/Volley/WebView endpoint extraction patterns |
| `references/call-flow-analysis.md` | UI->ViewModel/Presenter->Repository->Network tracing |

## Mandatory Pre-Routing Workflow

1. Read `references/canonical-scripts.md` first.
2. Read `references/script-metadata.manifest.json` and select the `preferred` canonical profile.
3. Use fallback profiles only if the preferred path fails or misses target output.
4. Then execute the 5-phase workflow below.

---

# THE 5-PHASE REVERSE ENGINEERING WORKFLOW

You are equipped with global CLI tools (`apk-*`). Execute this exact 5-phase workflow when handed an Android application. **Do not deviate.**

## PHASE 1: Verify Dependencies

Before doing anything, ensure the environment isn't garbage.

```bash
apk-check-deps
```

If required dependencies are missing (Exit Code 1):

```bash
apk-install-dep <dep_name>
```

If `apk-install-dep` exits with Code 2 (requires manual sudo), print the exact instructions for the user and halt.

Optional dependencies (vineflower, dex2jar) are highly recommended. Ask the user if they want them installed.

After any installations, re-run `apk-check-deps` to confirm. Do not proceed until all required dependencies pass.

## PHASE 2: Decompile Target

```bash
apk-decompile [OPTIONS] <file>
```

**Engine Selection Strategy (CRITICAL):**


| Situation                            | Engine                                       |
| ------------------------------------ | -------------------------------------------- |
| First pass on any APK/XAPK           | `--engine jadx` (fastest, handles resources) |
| JAR/AAR library analysis             | `--engine fernflower` (better Java output)   |
| Jadx output has warnings/broken code | `--engine both` (compare per class)          |
| Complex lambdas, generics, streams   | `--engine fernflower`                        |
| Quick overview of a large APK        | `jadx --no-res`                              |


**Flags:**

- `-o <dir>`: Custom output directory (default: `<filename>-decompiled`)
- `--deobf`: Enable Jadx deobfuscation (mandatory for obfuscated apps)
- `--no-res`: Skip resources, decompile code only (faster for massive APKs)
- `--engine ENGINE`: `jadx` (default), `fernflower`, or `both`

**XAPK & Split Bundles:**
The script automatically handles XAPKs and bundled splits. If the app is a bundle, the script extracts it and decompiles the `base.apk` into `<output>/base/sources/`. **Look for the `base/` subdirectory before saying the app is empty!**

When using `--engine both`, outputs go into `<output>/jadx/` and `<output>/fernflower/` with a comparison summary.

## PHASE 3: Analyze Structure

Navigate the output using `bash` and `grep`, NEVER by reading the root directory.

1. **Manifest:** Read `<output>/resources/AndroidManifest.xml` (or `<output>/base/resources/AndroidManifest.xml` for bundles).
  - Identify the main launcher Activity
  - List all Activities, Services, BroadcastReceivers, ContentProviders
  - Note permissions (especially `INTERNET`, `ACCESS_NETWORK_STATE`)
  - Find the application class (`android:name` on `<application>`)
2. **Survey the package structure** under `<output>/sources/`:
  - Run `ls` to map top-level packages
  - Distinguish app code from third-party libraries
  - Look for packages named `api`, `network`, `data`, `repository`, `service`, `retrofit`, `http`
3. **Identify the architecture pattern:**
  - MVP: look for `Presenter` classes
  - MVVM: look for `ViewModel` classes and `LiveData`/`StateFlow`
  - Clean Architecture: look for `domain`, `data`, `presentation` packages

## PHASE 4: Trace Call Flows

Trace execution from the UI down to the network layer. Follow the exact Android Lifecycle:

1. Start at `Activity.onCreate()` or `Fragment.onViewCreated()`.
2. Grep for Click Handlers: `rg 'setOnClickListener|onClick' <output>/sources/`
3. Trace to the **ViewModel/Presenter**: `rg 'ViewModel|Presenter' <output>/sources/`
4. Trace to the **Repository**: `rg 'Repository' <output>/sources/`
5. Map **Dependency Injection (Dagger/Hilt)**: `rg '@Provides|@Binds|@Inject|@Module' <output>/sources/`

See `references/call-flow-analysis.md` for detailed techniques.

## PHASE 5: Extract and Document APIs

```bash
apk-find-apis <output>/sources/ [OPTIONS]
```

Targeted searches:

```bash
apk-find-apis <output>/sources/ --retrofit
apk-find-apis <output>/sources/ --urls
apk-find-apis <output>/sources/ --auth
```

Then read the surrounding source code to extract full endpoint details.

**MANDATORY DOCUMENTATION FORMAT:**

For every API endpoint discovered, document it exactly like this:

```markdown
### `METHOD /path`
- **Source**: `com.example.api.ApiService` (ApiService.java:42)
- **Base URL**: `https://api.example.com/v1` (Found in NetworkModule.java)
- **Path params**: `id` (String)
- **Query params**: `page` (int), `limit` (int)
- **Headers**: `Authorization: Bearer <token>`
- **Request body**: `{ "email": "string", "password": "string" }`
- **Response**: `ApiResponse<User>`
- **Called from**: `LoginActivity -> LoginViewModel -> UserRepository -> ApiService`
```

---

# ADVANCED TECHNIQUES (STRICT ENFORCEMENT)

### Handling Obfuscation (ProGuard / R8)

When the code looks like `a.b.c()`, **do not give up.**

- **Strings are anchors:** URLs, error messages, and JSON keys are never obfuscated. Grep for `"https://"` or `"auth/login"`.
- **Frameworks are anchors:** `Activity`, `Fragment`, and `Intent` keep their names.
- **Annotations are anchors:** Retrofit `@GET` and `@POST` are never obfuscated. If `c.a.b` has `@POST("login")`, it is the Retrofit interface. Trace who calls it.

### Jadx vs Vineflower (Fernflower)

If you read a Java file decompiled by Jadx and see `/* JADX WARNING: ... */` or `// Error: ...` inside a method body, **stop reading.** Jadx failed to build the AST. Re-run with `--engine fernflower` and read the Vineflower output for that specific file instead.

### Native Library Analysis (Ghidra)

- **Headless Only:** Do not attempt to open the Ghidra GUI.
- **Headless Execution:**
  ```bash
  /path/to/ghidra/support/analyzeHeadless /tmp/ghidra_proj target_proj -process libtarget.so -postScript your_script.py
  ```

---

# TOOLS & ACCURACY

**Do not guess. Do not hallucinate.**

1. **USE Context7 MCP** to verify library APIs and tool signatures before writing commands.
2. **USE the browser** if you are unsure about how a decompiler flag works or what a specific Android API does.
3. If `rg` is available, prefer it over `grep`. It is faster.

---

# COMMON PITFALLS (REJECT THESE ON SIGHT)


| Pitfall                    | Why It's Wrong                                | Fix                                                                |
| -------------------------- | --------------------------------------------- | ------------------------------------------------------------------ |
| Reading `classes.dex`      | Compiled Dalvik bytecode. Unreadable.         | Run `apk-decompile` first.                                         |
| `read output/sources/`     | Blows up the context window.                  | `rg "keyword" output/sources/` first.                              |
| Giving up on `a.b.c`       | Obfuscation is a feature, not an excuse.      | Grep for strings/annotations to find anchors.                      |
| Staring at Jadx `// Error` | Jadx failed to decompile the method block.    | Re-run with `--engine fernflower`.                                 |
| Missing the Base URL       | Retrofit interfaces don't contain the domain. | Grep for `Retrofit.Builder().baseUrl()` or Application `onCreate`. |
| "App has no sources"       | It's an XAPK/Split wrapper.                   | Look inside `output/base/sources/`.                                |


---

# OUTPUT

At the end of the workflow, deliver:

1. **Decompiled source** in the output directory
2. **Architecture summary** -- app structure, main packages, pattern used
3. **API documentation** -- all discovered endpoints in the format above
4. **Call flow map** -- key paths from UI to network (especially authentication and main features)

## References

- `references/canonical-scripts.md` -- Canonical script IDs and profile presets
- `references/script-metadata.manifest.json` -- Deterministic routing metadata (preferred/fallback IDs)
- `references/setup-guide.md` -- Installing Java, jadx, Fernflower/Vineflower, dex2jar
- `references/jadx-usage.md` -- jadx CLI options and workflows
- `references/fernflower-usage.md` -- Fernflower/Vineflower CLI options, APK workflow
- `references/api-extraction-patterns.md` -- Library-specific search patterns and documentation template
- `references/call-flow-analysis.md` -- Techniques for tracing call flows in decompiled code

