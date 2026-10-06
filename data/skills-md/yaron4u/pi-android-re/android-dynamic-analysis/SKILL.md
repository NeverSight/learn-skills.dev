---
name: android-dynamic-analysis
description: Write Frida scripts for Android dynamic analysis, runtime hooking, bypass SSL pinning, root detection bypass, anti-frida evasion, biometric bypass, memory patching, crypto monitoring, and native instrumentation. Use when the user wants to hook, intercept, bypass, inject, instrument, or dynamically analyze Android applications at runtime using Frida.
---

# Android Dynamic Analysis (Frida)

Write and inject Frida scripts for runtime hooking, bypass, and instrumentation of Android applications. Covers Java/ART hooking, native Interceptor, memory patching, SSL pinning bypass, root detection bypass, anti-instrumentation evasion, and crypto/network observers.

---

# REQUIRED REFERENCE LOADING

Before creating, modifying, reviewing, or recommending Frida scripts, read the relevant files under `references/`. Do not rely only on memory or random uploaded script variants.

## Reference Files

| File | Read When |
|---|---|
| `references/canonical-scripts.md` | Selecting canonical script IDs before touching variants |
| `references/script-metadata.manifest.json` | Deterministic routing: intent/static-evidence -> preferred/fallback script IDs |
| `references/script-catalog.md` | Understanding folder model and legacy variant landscape |
| `references/workflow-from-static-to-dynamic.md` | Mapping jadx/static findings into dynamic Frida hooks |
| `references/observer-scripts.md` | Writing monitoring scripts for crypto, network, storage, classes, logs, deep links, or runtime behavior |
| `references/bypass-scripts.md` | Writing bypass scripts for SSL pinning, root/emulator/debug checks, biometric, WebView, location, WiFi, or app termination |
| `references/frida-script-best-practices.md` | Hardening old scripts, converting variants, enforcing strict Frida style |
| `references/troubleshooting.md` | Debugging hooks that do not fire, crashes, wrong overloads, class-loader issues, or noisy output |

## Mandatory Workflow

1. Read `references/canonical-scripts.md` first.
2. Read `references/script-metadata.manifest.json` and apply routing rules (`preferred` then `fallback`).
3. Read `references/script-catalog.md` only if canonical/fallback scripts miss required targets.
4. Read `references/workflow-from-static-to-dynamic.md` when static-analysis evidence exists or the user mentions jadx/APK findings.
5. Read either `references/observer-scripts.md` or `references/bypass-scripts.md` based on the task.
6. Read `references/frida-script-best-practices.md` before writing final script code.
7. Read `references/troubleshooting.md` when fixing failed hooks, crashes, class-loader problems, or runtime errors.

The uploaded scripts are reference material, not production quality by default. Extract hook targets and behavior from them, then rewrite using the standards in this skill and the reference files.

---

# FRIDA VERSION COMPATIBILITY

Target **Frida 16.x** by default. If the user specifies Frida 17+, apply these breaking changes:


| Removed (Frida 17+)                   | Replacement                                                  |
| ------------------------------------- | ------------------------------------------------------------ |
| `Module.findBaseAddress(name)`        | `Process.findModuleByName(name).base`                        |
| `Module.getBaseAddress(name)`         | `Process.getModuleByName(name).base`                         |
| `Module.findExportByName(null, name)` | `Process.findModuleByName('libc.so').findExportByName(name)` |
| `Module.findExportByName(lib, name)`  | `Process.findModuleByName(lib).findExportByName(name)`       |
| `Module.enumerateExports(lib)`        | `Process.getModuleByName(lib).enumerateExports()`            |
| `Module.enumerateSymbols(lib)`        | `Process.getModuleByName(lib).enumerateSymbols()`            |
| `Memory.readU32(ptr)`                 | `ptr.readU32()` (instance method)                            |
| `Memory.writeU32(ptr, val)`           | `ptr.writeU32(val)` (instance method)                        |


Static `Memory.read`* / `Memory.write`* methods are **gone** in Frida 17. Use `NativePointer` instance methods exclusively.

---

# CODING STANDARDS (STRICT ENFORCEMENT)

## 1. Minimalism & Scope

- **Strict Mode:** Every script starts with `"use strict";`.
- **No Global Pollution:** Do not leak variables into the global Frida namespace.
- **Targeted Hooks Only:** Never hook generic base classes (`java.io.File.exists`, `java.lang.String`) unless absolutely necessary. They fire thousands of times per second and choke the entire OS. Target the specific library class (e.g., `com.scottyab.rootbeer.RootBeer`, `okhttp3.CertificatePinner`, `com.datatheorem.android.trustkit.pinning.PinningTrustManager`).
- **No Inline Comments:** If the code isn't self-explanatory, rewrite it. The only exception is documenting a specific, obscure memory offset or reverse-engineered struct layout.

## 2. Performance is King (CRITICAL)

- **Do Not Block Threads:** `onEnter` and `onLeave` block the application's execution thread. Keep them lightning fast. No heavy computation, no string formatting, no JSON serialization inside hot hooks.
- **Cache Arguments:** Never read `args[N]` multiple times. Store it in a local variable once:
  ```javascript
  onEnter(args) {
    const path = args[0];
    if (!path.isNull()) {
      // use 'path', not 'args[0]' again
    }
  }
  ```
- **Throttle IPC:** **NEVER** spam `send()` or `console.log()` inside a hot function (game loop, crypto block, network I/O). Buffer data or evaluate logic inside the JS context before sending to the host.
- **CModule for Hot Paths:** If a native hook fires thousands of times per second, write it in C using `CModule`. JavaScript will choke the target process.

## 3. Safe Memory & Pointers

- **Strict Pointer Checks:** A `NativePointer` is not a string or an integer. Always check `.isNull()` before reading from it.
- **Never Trust Memory:** Wrap `ptr.readUtf8String()` and all memory reads in `try/catch`. Reading unmapped memory crashes the target. That's your fault.
- **Keep Allocations Alive:** `Memory.allocUtf8String()` returns a pointer that gets GC'd when the JS reference dies. Store it in `this.buf` (inside `onEnter`) or in an outer-scope variable. If the pointer gets freed while native code still holds it, the app crashes.
  ```javascript
  onEnter(args) {
    const buf = Memory.allocUtf8String('/dev/null');
    this.buf = buf;
    args[0] = buf;
  }
  ```
- **Never Null a Path Pointer:** If bypassing a native file check (e.g., `fopen` for `/proc/self/maps`), **never** overwrite the path with `ptr(0)`. That's a guaranteed SegFault. Point it to a dummy path via `Memory.allocUtf8String("/dev/null")`.
- **Use `readVolatile()` for Unsafe Memory:** When dumping memory while app threads are running, or when the pointer may reference freed memory, use `ptr.readVolatile(length)` instead of `ptr.readByteArray(length)`.

## 4. Android Java Hooking (ART/Dalvik)

- **Class Resolution Safety:** Do not blindly `Java.use()`. Always wrap in `try/catch`. An unhandled `ClassNotFoundException` is amateur hour.
  ```javascript
  let TargetClass;
  try {
    TargetClass = Java.use('com.target.ClassName');
  } catch (e) {
    console.error('[-] Class not found. Skipping.');
    return;
  }
  ```
- **Overloads are Mandatory:** Java methods have overloads. Use `.overload(...)` explicitly. Do not rely on Frida guessing. If you don't know the exact signature, enumerate them first:
  ```javascript
  TargetClass.targetMethod.overloads.forEach((overload) => {
    overload.implementation = function () {
      console.log(`[+] ${overload.returnType.className} called`);
      return overload.apply(this, arguments);
    };
  });
  ```
- **Arrow Functions vs `this`:** Use arrow functions for `Java.perform()` callbacks. Use regular `function` for `.implementation` assignments — you need `this` bound to the Java object instance.
- **Type Conversions (byte[]):** When hooking crypto (`javax.crypto.Cipher`), never concatenate a Java `byte[]` to a string. Convert properly:
  ```javascript
  const jsBytes = Java.array('byte', result);
  const buffer = new Uint8Array(jsBytes).buffer;
  send({ type: 'crypto', op: 'doFinal' }, buffer);
  ```
- **Constructor Hooking:** Hook constructors via `$init`. If re-hooking constructors throws `expected a NativePointer`, call `Java.deoptimizeEverything()` at the top of your `Java.perform` block.
- **Enumerating Classes at Runtime:** Use `Java.enumerateLoadedClasses()` with a filter for the target package, not a blanket dump of every class in the VM.
- **Class Loaders:** If `Java.use()` fails for a dynamically loaded class, use `Java.enumerateClassLoaders()` and `Java.classFactory.loader` to switch to the correct class loader.

## 5. Native Hooking (Interceptor / NativeFunction)

- **Prefer `Module.findExportByName`** over hardcoded offsets. Offsets change between builds. Exports are stable.
- **Pattern Scanning for Non-Exported Functions:**
  ```javascript
  const mod = Process.findModuleByName('libtarget.so');
  const matches = Memory.scanSync(mod.base, mod.size, 'FF 43 01 D1 ?? ?? ?? ?? F4 4F 02 A9');
  if (matches.length > 0) {
    Interceptor.attach(matches[0].address, { ... });
  }
  ```
- **Architecture Awareness:** Use `Process.arch` and `Process.pointerSize`. Do not hardcode `4` or `8`. ARM64 and ARM32 have different calling conventions, register layouts, and pointer sizes.
- **Thumb Mode (ARM32):** When attaching to Thumb functions, OR the address with 1: `ptr(address).or(1)`.
- `**Memory.patchCode` for Binary Patches:**
  ```javascript
  Memory.protect(target, 0x1000, 'rwx');
  Memory.patchCode(target, 8, (code) => {
    const writer = new Arm64Writer(code);
    try {
      writer.putRet();
      writer.flush();
    } finally {
      writer.dispose();
    }
  });
  ```
- **Flutter / React Native SSL Pinning:** These frameworks pin in native code (`libflutter.so`, `libhermes.so`). You cannot bypass them from the Java layer. Use pattern scanning on the native library to find the verification function and patch/hook it.

## 6. Host Communication (I/O)

- **Structured Data:** Always send JSON objects via `send({ type: 'hook', data: ... })`. Do not concatenate strings for the host to parse.
- **Binary Data:** Use `ArrayBuffer` and the second argument of `send()` when transferring raw memory dumps, crypto keys, or certificate chains. **Never** stringify raw bytes.
- **Logging Convention:** Use `[+]` for success, `[-]` for errors, `[*]` for informational, `[!]` for warnings. Keep log lines short and parseable.

## 7. Modern JavaScript Syntax

- **No `var`:** Use `const` by default. Use `let` only if mutation is required.
- **Arrow Functions:** Use them unless you need `this` context (`.implementation` assignments).
- **Template Literals:** Use backtick strings. No `+` concatenation for log messages.
- **No Hungarians:** Don't write `strName` or `ptrBuffer`. Just `name` and `buffer`.

## 8. Bypasses & Anti-Reversing Logic

### Root / Jailbreak Detection

- **Return Correct Types:** Return primitive `false` for methods returning `boolean`. Return `Java.use("java.lang.Boolean").$new(false)` for methods returning `java.lang.Boolean`.
- **Target the Library, Not the OS:** Hook `com.scottyab.rootbeer.RootBeer.isRooted()`, not `java.io.File.exists()`. Hook the detection library's methods, not the system APIs it calls.
- **Multi-Vector Coverage:** A serious root detection library checks multiple vectors (su binary, build tags, dangerous props, busybox, Magisk, test-keys). Hook all detection methods on the library class, not just `isRooted()`.
- **System.exit Bypass:** Many apps call `System.exit(0)` after root detection. Hook it:
  ```javascript
  Java.use('java.lang.System').exit.overload('int').implementation = function (code) {
    console.log('[+] Blocked System.exit(' + code + ')');
  };
  ```

### SSL / Certificate Pinning

- **Layered Bypass Strategy:** A professional SSL pinning bypass covers ALL of these in a single script, each wrapped in `try/catch`:
  1. `javax.net.ssl.SSLPeerUnverifiedException` — dynamic auto-patcher
  2. `javax.net.ssl.HttpsURLConnection` — `setDefaultHostnameVerifier`, `setSSLSocketFactory`, `setHostnameVerifier`
  3. `javax.net.ssl.SSLContext.init` — inject a custom `TrustManager` that accepts all certs
  4. `com.android.org.conscrypt.TrustManagerImpl` — `verifyChain` and `checkTrustedRecursive`
  5. `okhttp3.CertificatePinner.check` — all overloads: `(String, List)`, `(String, Certificate)`, `(String, Certificate[])`, and `check$okhttp`
  6. `com.datatheorem.android.trustkit.`* — `OkHostnameVerifier.verify` and `PinningTrustManager.checkServerTrusted`
  7. `com.android.org.conscrypt.OpenSSLSocketImpl.verifyCertificateChain`
  8. Conscrypt `CertPinManager.isChainValid`
  9. Netty `FingerprintTrustManagerFactory.checkTrusted`
- **Each hook wrapped in its own `try/catch`:** If one class doesn't exist in the app, the rest still load. Log `[+]` for hooked, `[ ]` for not found.
- **Register a Custom TrustManager:**
  ```javascript
  const TrustManager = Java.registerClass({
    name: 'com.bypass.TrustManager',
    implements: [Java.use('javax.net.ssl.X509TrustManager')],
    methods: {
      checkClientTrusted(chain, authType) {},
      checkServerTrusted(chain, authType) {},
      getAcceptedIssuers() { return []; }
    }
  });
  ```

### Anti-Frida / Anti-Instrumentation

- **Native `strstr` Hook:** Intercept `strstr` in `libc.so` and return `NULL` when the haystack contains "frida", "xposed", "gadget", or "gum-js-loop":
  ```javascript
  Interceptor.attach(Module.findExportByName('libc.so', 'strstr'), {
    onEnter(args) {
      this.shouldNullify = false;
      const hay = args[0];
      try {
        const str = hay.readUtf8String();
        if (str && (str.includes('frida') || str.includes('xposed') || str.includes('gum-js-loop') || str.includes('gadget'))) {
          this.shouldNullify = true;
        }
      } catch (e) {}
    },
    onLeave(retval) {
      if (this.shouldNullify) retval.replace(ptr(0));
    }
  });
  ```
- `**/proc/self/maps` Filtering:** Hook `fopen` / `open` and redirect reads of `/proc/self/maps`, `/proc/self/status`, and `/proc/self/task/*/status` to `/dev/null` or a pre-filtered version.
- **Port Scanning Detection:** Some apps scan for Frida's default port (27042). Hook `connect()` in libc and block connections to localhost:27042.

### Biometric Bypass

- **Cover Both APIs:** Hook both `android.hardware.biometrics.BiometricPrompt.authenticate` (Android 9+) and `android.hardware.fingerprint.FingerprintManager.authenticate` (legacy).
- **Use `Java.retain()`** to keep callback references alive across async calls.
- **Run on UI Thread:** Authentication callbacks must execute on the main thread. Use `Handler` + `Looper.getMainLooper()`.

## 9. Script Structure & Organization

### Script Header

Every script must have a descriptive header:

```javascript
"use strict";
// Usage: frida -U -f <package> -l <script>.js
```

### Multi-Hook Scripts (Compound Bypasses)

Structure compound bypass scripts with isolated try/catch blocks per target:

```javascript
"use strict";

Java.perform(() => {
  try {
    const Cls1 = Java.use('com.target.Class1');
    Cls1.method.overload().implementation = function () { return false; };
    console.log('[+] Class1.method');
  } catch (e) {
    console.log('[ ] Class1.method');
  }

  try {
    const Cls2 = Java.use('com.target.Class2');
    Cls2.method.overload().implementation = function () { return true; };
    console.log('[+] Class2.method');
  } catch (e) {
    console.log('[ ] Class2.method');
  }
});
```

### Observer Scripts (Monitoring / Tracing)

When building observer scripts (crypto, network, storage), hook ALL relevant overloads of each method.

Use `setImmediate()` wrapper if the hooks need to survive early classloader races:

```javascript
"use strict";

setImmediate(() => {
  Java.perform(() => {
    // hooks here
  });
});
```

## 10. TypeScript Workflow (Recommended for Complex Projects)

For projects with more than 3 scripts, use TypeScript + `frida-compile` or `esbuild`:

```
npm install -D frida-compile typescript
```

`tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2024",
    "module": "ESNext",
    "strict": true,
    "esModuleInterop": true
  }
}
```

Compile: `frida-compile agent.ts -o agent.js`
Inject: `frida -U -f com.target.app -l agent.js`

---

# TOOLS & ACCURACY

**Do not guess. Do not hallucinate.**

1. **API Signatures:**
  - **USE Context7 MCP** to verify Frida API signatures before writing code. Check exact method names, parameter types, and return values for `Memory`, `Process`, `Module`, `Java`, `Interceptor`, `NativePointer`, `NativeFunction`.
  - I don't want to see `TypeError: undefined is not a function` because you guessed the Frida API.
2. **Architecture:**
  - Account for pointer sizes. Use `Process.pointerSize`. Do not hardcode `4` or `8`.
  - Check `Process.arch` for ARM64 vs ARM32 vs x86 differences.
3. **Android API Levels:**
  - Know which Android APIs exist at which API level. `BiometricPrompt` is API 28+. `FingerprintManager` is API 23-27. `TrustManagerImpl.verifyChain` exists on Android 7+. Don't hook APIs that don't exist on the target.

---

# COMMON PITFALLS (REJECT THESE ON SIGHT)


| Pitfall                                               | Why It's Wrong                                     | Fix                                                                  |
| ----------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------------------------- |
| `var` keyword                                         | Leaks to function scope, not block scope           | `const` / `let`                                                      |
| Missing `.overload()`                                 | Frida guesses wrong, throws at runtime             | Specify explicit overload signature                                  |
| No `try/catch` on `Java.use()`                        | `ClassNotFoundException` kills the script          | Wrap it                                                              |
| `console.log("data: " + javaByteArray)`               | Prints `[object Object]` or garbage                | Convert to hex or use `send()` with `ArrayBuffer`                    |
| `args[0] = ptr(0)` in native hooks                    | SegFault — null pointer dereference                | `args[0] = Memory.allocUtf8String('/dev/null')` + store ref          |
| Hooking `java.io.File.exists` globally                | Called thousands of times, freezes the app         | Hook the specific detection library                                  |
| `Memory.readUtf8String(args[0])` without `try/catch`  | Unmapped memory = crash                            | Wrap in try/catch                                                    |
| Spamming `send()` in a hot loop                       | Saturates IPC, freezes target process              | Buffer, throttle, or use CModule                                     |
| Using `setTimeout` without understanding spawn timing | Hooks may load after the target class already ran  | Use `frida -f` (spawn) + `Java.perform()`                            |
| Not calling original method                           | Breaks app functionality, causes cascading crashes | Always call `this.methodName(args)` unless intentionally suppressing |


---

# TRAINING EXAMPLES

### Example 1: RootBeer Bypass (Bad -> Good)

**Bad Input:**

```javascript
Java.perform(function() {
  var File = Java.use("java.io.File");
  File.exists.implementation = function() {
    var name = this.getName();
    if (name === "su") return false;
    return this.exists();
  }
});
```

Hooking `java.io.File.exists` globally to bypass a 3rd-party library? That's a sledgehammer for a fly. It'll freeze the entire OS. Target the actual library.

**Fixed:**

```javascript
"use strict";

Java.perform(() => {
  let RootBeer;
  try {
    RootBeer = Java.use("com.scottyab.rootbeer.RootBeer");
  } catch (e) {
    console.error("[-] RootBeer class not found. Skipping.");
    return;
  }

  RootBeer.isRooted.overload().implementation = function () {
    console.log("[+] Bypassed RootBeer.isRooted()");
    return false;
  };

  RootBeer.isRootedWithoutBusyBoxCheck.overload().implementation = function () {
    console.log("[+] Bypassed RootBeer.isRootedWithoutBusyBoxCheck()");
    return false;
  };
});
```

---

### Example 2: AES Cipher Hook (Bad -> Good)

**Bad Input:**

```javascript
Java.perform(function() {
  var Cipher = Java.use('javax.crypto.Cipher');
  Cipher.doFinal.implementation = function(args) {
    console.log("Cipher data: " + args);
    return this.doFinal(args);
  }
});
```

No overload specified, concatenating raw bytes to a string. You're going to crash the ART VM.

**Fixed:**

```javascript
"use strict";

Java.perform(() => {
  let Cipher;
  try {
    Cipher = Java.use('javax.crypto.Cipher');
  } catch (e) {
    return;
  }

  Cipher.doFinal.overload('[B').implementation = function (data) {
    const result = this.doFinal(data);

    try {
      const jsArray = Java.array('byte', result);
      const buffer = new Uint8Array(jsArray).buffer;
      send({ type: 'crypto', op: 'doFinal', algo: this.getAlgorithm() }, buffer);
    } catch (e) {
      console.error(`[-] doFinal parse error: ${e.message}`);
    }

    return result;
  };
});
```

---

### Example 3: Anti-Frida Native Bypass (Bad -> Good)

**Bad Input:**

```javascript
Interceptor.attach(Module.findExportByName("libc.so", "strstr"), {
  onEnter: function(args) {
    this.haystack = args[0];
    this.needle = args[1];
    this.frida = Boolean(0);
    haystack = Memory.readUtf8String(this.haystack);
    needle = Memory.readUtf8String(this.needle);
    if (haystack.indexOf("frida") !== -1 || haystack.indexOf("xposed") !== -1) {
      this.frida = Boolean(1);
    }
  },
  onLeave: function(retval) {
    if (this.frida) {
      retval.replace(0);
    }
    return retval;
  }
});
```

Global variable leaks (`haystack`, `needle`), no `try/catch` on `readUtf8String`, reading args twice, `Boolean(0)` instead of just `false`. Embarrassing.

**Fixed:**

```javascript
"use strict";

Interceptor.attach(Module.findExportByName('libc.so', 'strstr'), {
  onEnter(args) {
    this.shouldNullify = false;
    const hay = args[0];
    try {
      const str = hay.readUtf8String();
      if (str && (str.includes('frida') || str.includes('xposed') || str.includes('gum-js-loop') || str.includes('gadget'))) {
        this.shouldNullify = true;
      }
    } catch (e) {}
  },
  onLeave(retval) {
    if (this.shouldNullify) {
      retval.replace(ptr(0));
    }
  }
});
```

---

### Example 4: SharedPreferences Observer (Clean)

```javascript
"use strict";

setImmediate(() => {
  Java.perform(() => {
    let Editor;
    try {
      Editor = Java.use('android.app.SharedPreferencesImpl$EditorImpl');
    } catch (e) {
      console.error('[-] SharedPreferencesImpl$EditorImpl not found');
      return;
    }

    const methods = ['putString', 'putBoolean', 'putFloat', 'putInt', 'putLong'];

    methods.forEach((name) => {
      Editor[name].overloads.forEach((overload) => {
        overload.implementation = function () {
          const key = arguments[0];
          const val = arguments[1];
          send({ type: 'sharedprefs', op: name, key: `${key}`, value: `${val}` });
          return overload.apply(this, arguments);
        };
      });
    });

    console.log('[+] SharedPreferences observer active');
  });
});
```

---

### Example 5: Comprehensive SSL Pinning Bypass (Production Quality)

```javascript
"use strict";

Java.perform(() => {
  console.log('[*] SSL Pinning Bypass loading...');

  try {
    const X509TrustManager = Java.use('javax.net.ssl.X509TrustManager');
    const SSLContext = Java.use('javax.net.ssl.SSLContext');

    const TrustManager = Java.registerClass({
      name: 'com.bypass.TrustManager',
      implements: [X509TrustManager],
      methods: {
        checkClientTrusted(chain, authType) {},
        checkServerTrusted(chain, authType) {},
        getAcceptedIssuers() { return []; }
      }
    });

    const TrustManagers = [TrustManager.$new()];

    SSLContext.init.overload(
      '[Ljavax.net.ssl.KeyManager;',
      '[Ljavax.net.ssl.TrustManager;',
      'java.security.SecureRandom'
    ).implementation = function (km, tm, sr) {
      SSLContext.init.overload(
        '[Ljavax.net.ssl.KeyManager;',
        '[Ljavax.net.ssl.TrustManager;',
        'java.security.SecureRandom'
      ).call(this, km, TrustManagers, sr);
    };
    console.log('[+] SSLContext.init');
  } catch (e) {
    console.log('[ ] SSLContext.init');
  }

  try {
    const TrustManagerImpl = Java.use('com.android.org.conscrypt.TrustManagerImpl');
    TrustManagerImpl.verifyChain.implementation = function (untrusted, trustAnchor, host, clientAuth, ocsp, tlsSct) {
      return untrusted;
    };
    console.log('[+] TrustManagerImpl.verifyChain');
  } catch (e) {
    console.log('[ ] TrustManagerImpl.verifyChain');
  }

  try {
    const Pinner = Java.use('okhttp3.CertificatePinner');
    Pinner.check.overload('java.lang.String', 'java.util.List').implementation = function () {};
    console.log('[+] OkHTTP3 CertificatePinner.check(String, List)');
  } catch (e) {
    console.log('[ ] OkHTTP3 CertificatePinner.check(String, List)');
  }

  try {
    const Pinner = Java.use('okhttp3.CertificatePinner');
    Pinner['check$okhttp'].implementation = function () {};
    console.log('[+] OkHTTP3 CertificatePinner.check$okhttp');
  } catch (e) {
    console.log('[ ] OkHTTP3 CertificatePinner.check$okhttp');
  }

  try {
    const Conn = Java.use('javax.net.ssl.HttpsURLConnection');
    Conn.setDefaultHostnameVerifier.implementation = function () {};
    Conn.setSSLSocketFactory.implementation = function () {};
    Conn.setHostnameVerifier.implementation = function () {};
    console.log('[+] HttpsURLConnection');
  } catch (e) {
    console.log('[ ] HttpsURLConnection');
  }

  try {
    const Trustkit = Java.use('com.datatheorem.android.trustkit.pinning.PinningTrustManager');
    Trustkit.checkServerTrusted.implementation = function () {};
    console.log('[+] Trustkit PinningTrustManager');
  } catch (e) {
    console.log('[ ] Trustkit PinningTrustManager');
  }

  console.log('[*] SSL Pinning Bypass loaded.');
});
```

This covers 90% of Android apps in a single script. Each target is isolated. If a class doesn't exist, the rest still load. That's how you write a compound bypass.