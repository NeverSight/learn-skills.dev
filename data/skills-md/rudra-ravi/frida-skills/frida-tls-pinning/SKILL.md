---
name: frida-tls-pinning
description: Analyze and bypass TLS or SSL pinning with Frida on Android, iOS, Flutter, React Native, native BoringSSL/OpenSSL, Conscrypt, OkHttp, NSURLSession, SecTrust, and app-specific trust code.
---

# Frida TLS Pinning

Use this skill when HTTPS traffic is blocked by certificate pinning or custom trust validation.

## Identify The Stack First

- Android Java: OkHttp, TrustManager, Conscrypt, WebView, network security config.
- Android native: BoringSSL, OpenSSL, Cronet, proxygen, Flutter engine.
- iOS: `NSURLSession`, delegate trust challenges, `SecTrustEvaluate*`, native BoringSSL.
- Cross-platform: React Native, Flutter, Unity, custom native networking.

Do not start with a universal bypass as the final answer. Use public scripts to discover which hook fires, then keep only the needed hooks.

## Android Probe

```js
Java.perform(() => {
  for (const name of [
    "okhttp3.CertificatePinner",
    "com.android.org.conscrypt.TrustManagerImpl",
    "javax.net.ssl.SSLContext"
  ]) {
    try { console.log("found", name, Java.use(name)); } catch (_) {}
  }
});
```

## iOS Probe

```js
if (ObjC.available) {
  for (const name of Object.keys(ObjC.classes).filter(n => n.includes("Trust") || n.includes("Session"))) {
    console.log(name);
  }
}
```

## Native Probe

```js
for (const m of Process.enumerateModules()) {
  if (/ssl|crypto|boring|cronet|liger/i.test(m.name)) console.log(m.name, m.base, m.path);
}
```

## Verification

- Proxy is trusted by the device or app profile.
- The hook logs during the exact request that was blocked.
- The same request succeeds after mutation.
- Traffic is visible or the app behavior proves trust validation was bypassed.
- The final script documents app version, platform, library, and rollback command.

## References

Read `references/tls-patterns.md` for framework-specific hook options.
