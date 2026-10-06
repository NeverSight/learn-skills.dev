---
name: frida-android-instrument
description: "DYNAMIC: inspect an authorized Android app's Java runtime through Frida: list loaded classes, enumerate method signatures, or install observation-only hooks that report arguments and return values without intentionally changing them. Use for runtime discovery when static APK/DEX analysis is insufficient. Attaches to or spawns the app on a BYO Frida-capable USB device; executes the target and is consent-gated."
---

# Frida Android Instrumentation

Inspect Java/Kotlin behavior in an authorized Android app without copying one-off
Frida snippets between investigations. The bundled runner uses the Frida CLI so
current Frida releases provide their Java bridge to the loaded agent.

## Choose the operation

- `classes`: list loaded class names, optionally filtered with `--match`.
- `methods`: enumerate signatures for `--class-name`; use `--match` to narrow the
  method-name glob.
- `hook`: observe every overload of `--method` on `--class-name`, reporting bounded
  argument and return-value previews while calling the original implementation.

Start with discovery and narrow progressively:

```bash
rekit run --allow-dynamic frida-android-instrument com.example.app \
  --mode classes --match com.example --format json

rekit run --allow-dynamic frida-android-instrument com.example.app \
  --mode methods --class-name com.example.LoginActivity --match 'on*'

rekit run --allow-dynamic frida-android-instrument com.example.app \
  --mode hook --class-name com.example.LoginActivity --method verify --timeout 30
```

Use `--spawn` when the behavior occurs during app startup. Without it, the runner
attaches to the running application by identifier. Use `--device-id` instead of the
default USB device when more than one Frida endpoint is available.

## Device boundary

The runner does not root a device, install `frida-server`, patch an APK, or embed
Frida Gadget. Supply a device or emulator on which Frida is already reachable:

- Rooted/emulator path: run a matching `frida-server` and confirm `frida-ps -U`.
- Gadget path: use an app you are authorized to repackage and connect to its exposed
  Gadget endpoint using the appropriate Frida device configuration.

Keep the host tools and remote server/Gadget versions compatible. Treat all observed
arguments and returns as potentially sensitive; retain only what the investigation
requires.

## Safety and interpretation

- This is dynamic execution. Use a disposable, authorized analysis environment.
- Hooks are observation-only by design, but instrumentation can still perturb timing,
  trigger anti-instrumentation, or crash the process.
- A class absent from `classes` may not be loaded yet or may use another class loader;
  absence is not proof that it does not exist in the APK.
- Hook coverage reports installed overloads. No call events means only that no observed
  call occurred during the bounded window.
- Pair results with `jvm-decompile` for static context and `dex-dump` when runtime
  class loading hides the relevant DEX from on-disk analysis.

The runner emits one JSON object in `--format json`, including installed hooks,
bounded events, truncation state, and runtime errors.
