---
name: frida-troubleshooting
description: Diagnose Frida attach, spawn, version, frida-server, Gadget, hook, crash, Java, ObjC, class-loader, anti-instrumentation, and device connectivity failures.
---

# Frida Troubleshooting

Use this skill before changing hook logic when Frida itself may be failing.

## First Evidence

Collect exact commands and output:

```bash
frida --version
frida-ls-devices
frida-ps -Uai
```

For Android:

```bash
adb devices
adb shell getprop ro.product.cpu.abi
adb shell /data/local/tmp/frida-server --version
```

For iOS:

```bash
frida-ps -Uai
```

## Diagnosis Order

1. Version mismatch: host `frida-tools`/Python package vs `frida-server`/Gadget.
2. Device transport: USB, remote, emulator, jailbreak/root state, permissions.
3. Mode mismatch: spawn needed for early code, attach sufficient only after target load.
4. Runtime availability: `Java.available`, `Java.perform()`, `ObjC.available`.
5. Loader/module timing: class, symbol, or module not loaded yet.
6. Wrong overload/signature/address.
7. App protection or anti-instrumentation causing early exit.

## Practitioner Triage

- Reproduce with a minimal script that only logs platform/runtime availability. Load the real agent only after the minimal script works.
- If CodeShare or a universal bypass "works partly", extract which hook fired and which endpoint/behavior changed before adding more bypasses.
- If traffic still does not appear after pinning bypass, check proxy trust store, certificate transparency, native TLS, HTTP/3/QUIC, alternate endpoints, backend device integrity checks, and non-HTTP protocols.
- If a hook does not fire in an obfuscated app, hook data boundaries and stack traces instead of chasing renamed classes.
- If the app exits without logs, inspect native anti-instrumentation and early lifecycle hooks with spawn mode.

## Hook Does Not Fire

- Prove the code path is executed without Frida.
- Log module/class loading before installing the hook.
- For Android, enumerate overloads and class loaders.
- For iOS/Swift, enumerate symbols/modules and hook Objective-C-visible surfaces first.
- For native code, verify signature and architecture, then attach to caller/callee boundaries.

## Crash After Hook

- Remove mutation and keep logging only.
- Guard null pointers and invalid ObjC/Java objects.
- Copy values inside callbacks; do not store recycled `retval`.
- Check string lifetime when replacing pointer arguments.
- Narrow broad hooks that fire too often or recurse.

## References

Read `references/error-playbook.md` for common errors, likely causes, and next checks.
