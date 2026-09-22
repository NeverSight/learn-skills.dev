---
name: frida-android-hooks
description: Create and debug Frida hooks for Android apps, including Java.perform, overloads, constructors, class loaders, Kotlin, JNI, pinning, spawn, and Gadget.
---

# Frida Android Hooks

Use this skill when instrumenting Android Java/Kotlin/JNI behavior.

## Setup Checks

1. Verify host and device versions match:
   ```bash
   frida --version
   adb shell /data/local/tmp/frida-server --version
   frida-ps -Uai
   ```
2. Use spawn for early initialization:
   ```bash
   frida -U -f com.example.app -l agent.js --no-pause
   ```
3. Use attach for behavior reachable after app startup:
   ```bash
   frida -U -n com.example.app -l agent.js
   ```

## Java Hook Pattern

```js
Java.perform(() => {
  const Target = Java.use("com.example.Target");
  Target.method.overload("java.lang.String").implementation = function (value) {
    console.log("[Target.method]", value);
    const result = this.method(value);
    console.log("[Target.method] ->", result);
    return result;
  };
});
```

## Android Rules

- Always hook inside `Java.perform()` unless only native APIs are used.
- Resolve overloads explicitly. Do not rely on ambiguous method names.
- Hook constructors through `$init`.
- For Kotlin, expect companion classes, synthetic methods, default-argument helpers, and obfuscated names.
- If a class is not found, inspect class loaders and set `Java.classFactory.loader` to the app loader that can see it.
- For native methods, bridge to `frida-native-hooks` after identifying the loaded `.so` and JNI symbol.

## Practitioner Patterns

- For obfuscated code, hook meaningful platform boundaries first: URL/request builders, JSON parsers, Base64, crypto, SharedPreferences, keystore, file I/O, WebView, class loading, and native library loading.
- Log Java stack traces on high-signal hooks to find the app-owned caller before writing app-specific hooks.
- Convert byte arrays deliberately. Print both hex and UTF-8/ASCII only when valid; binary crypto material is often not text.
- Hook reflection and dynamic loading when classes appear late: `Class.forName`, `ClassLoader.loadClass`, `DexClassLoader`, `PathClassLoader`, and `Runtime.loadLibrary*`.
- For TLS/pinning, identify the actual stack before bypassing: OkHttp/CertificatePinner, TrustManager, Conscrypt, WebView, Flutter/BoringSSL, or native custom validation.
- For root/emulator/integrity bypasses, avoid blind mega-scripts as the final answer. Use them to reveal checks, then keep the smallest hooks that change the target behavior.

## Discovery Snippets

```js
Java.perform(() => {
  const groups = Java.enumerateMethods("*crypto*!*/isu");
  console.log(JSON.stringify(groups, null, 2));
});
```

```js
Java.perform(() => {
  Java.enumerateClassLoaders({
    onMatch(loader) {
      try {
        Java.classFactory.loader = loader;
        Java.use("com.example.Target");
        console.log("loader:", loader);
      } catch (_) {}
    },
    onComplete() {}
  });
});
```

## Pinning and Auth Work

- Treat public bypass snippets as reconnaissance, not final proof.
- Identify the actual trust path: platform trust manager, OkHttp, Conscrypt, WebView, native TLS, custom signature, or backend challenge.
- Log inputs/outputs before replacing trust decisions.
- Preserve evidence: hooked class, stack trace, endpoint, certificate or hash material observed, and app version.

## References

Read `references/android-patterns.md` for overload, constructor, class-loader, JNI, OkHttp, WebView, and spawn timing patterns.
