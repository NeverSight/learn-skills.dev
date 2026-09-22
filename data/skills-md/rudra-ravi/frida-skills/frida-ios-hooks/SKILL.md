---
name: frida-ios-hooks
description: Create and debug Frida hooks for iOS apps, including Objective-C, Swift symbols, modules, Interceptor, TLS pinning, rootless jailbreaks, Gadget, and ObjC issues.
---

# Frida iOS Hooks

Use this skill when instrumenting iOS Objective-C, Swift, or native behavior.

## Setup Checks

```bash
frida --version
frida-ps -Uai
frida -U -f com.example.app -l agent.js --no-pause
```

Confirm runtime availability:

```js
console.log("ObjC.available =", ObjC.available);
console.log(Process.platform, Process.arch);
```

If `ObjC.available` is false for an iOS app, use `frida-troubleshooting` before assuming the script is wrong.

## Objective-C Hook Pattern

```js
if (ObjC.available) {
  const cls = ObjC.classes.NSURLSession;
  const method = cls["- dataTaskWithRequest:completionHandler:"];
  Interceptor.attach(method.implementation, {
    onEnter(args) {
      const request = new ObjC.Object(args[2]);
      console.log("[NSURLSession]", request.URL().toString());
    }
  });
}
```

## Swift and Native Rules

- Enumerate modules and symbols before guessing Swift mangled names.
- Hook Objective-C-visible Swift through ObjC classes when possible.
- For pure Swift/native functions, resolve symbols and use `frida-native-hooks`.
- Spawn when hooks must run before app delegate, network stack, or anti-tamper initialization.
- Prefer observation hooks for trust evaluation, crypto, signature generation, and request building before mutating results.

## Practitioner Patterns

- Start with Objective-C runtime surfaces when available: delegates, URL loading, keychain, pasteboard, file APIs, crypto wrappers, and jailbreak-detection selectors.
- For Swift-heavy apps, use module/symbol enumeration plus caller stack traces; do not assume selectors exist unless Swift exposes them to Objective-C.
- For pinning, check both Objective-C frameworks and native `Security`/BoringSSL/CommonCrypto paths. Apps often mix them.
- Use CodeShare tools such as ObjC method observers for discovery, then replace them with narrow hooks once class/method names are known.
- On rootless jailbreaks, keep a minimal "runtime available" script separate from the real agent so setup failures are not confused with hook bugs.

## Discovery Snippets

```js
if (ObjC.available) {
  for (const name of Object.keys(ObjC.classes).filter(n => n.includes("Trust"))) {
    console.log(name);
  }
}
```

```js
for (const m of Process.enumerateModules()) {
  if (m.name.includes("Target")) console.log(m.name, m.base, m.path);
}
```

## Pinning and Rootless Notes

- Identify whether pinning is in `NSURLSession`, `SecTrustEvaluate*`, a third-party framework, or native custom code.
- Rootless jailbreak setups may need matching Frida packages, correct bootstrap path, and updated tooling. Version skew often looks like attach failure or missing ObjC bridge.
- Use Gadget when normal attach is blocked but app modification is in scope.

## References

Read `references/ios-patterns.md` for Objective-C, Swift symbol, `SecTrust`, module, and rootless troubleshooting patterns.
