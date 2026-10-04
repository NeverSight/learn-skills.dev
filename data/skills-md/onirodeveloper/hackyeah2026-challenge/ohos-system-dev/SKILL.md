---
name: ohos-system-dev
description: Develop, build, deploy, and verify OpenHarmony SYSTEM / persistent bundles (e.g. systemui, launcher) and components built inside the OHOS source tree. Use for platform components, multi-module assembleHap, and install-and-reboot-to-reload work. For standalone system apps use `ohos-system-app-dev`; for ordinary apps use `ohos-app-dev`.
---

# OpenHarmony System Dev

Platform work has its own rules that normal-app development doesn't. A system/persistent
bundle (systemui, launcher, a gesture-nav service) is **not** reloaded by reinstalling it —
it reloads on **reboot** — and it's signed/installed differently. This skill captures that
loop. Everything routes through the **`devecocli` CLI** where the documented commands support it (cross-platform; stdout=results,
stderr=logs) with raw `hdc` / `bm` / `param` as the escape hatch.

> Platform builds assume access to an OHOS **source tree** and a device/emulator that
> accepts system bundles (a dev image, or `system_app` signing). Paths like
> `applications/standard/systemui` below are illustrative.

## Windows toolchain selection

Require the caller's `PATH` to put the DevEco Studio Node directory first, followed by
the npm global bin directory and DevEco toolchain directories. Do not hard-code, probe,
or modify installation paths in this skill. Verify the resolved tools:

```powershell
Get-Command node, npm, devecocli
node --version; npm --version; devecocli -V
```

Do not mix executables from different Node installations. If the resolved tools are not
the intended DevEco environment, stop and report the PATH issue.

## When to use

"Build/deploy systemui (or another system bundle)", "install a persistent service",
"build a component in the OHOS source tree", "it installed but the change didn't take",
"sign a platform HAP", "reboot and check the service came back". Standalone HAP projects
requiring `hos_system_app` identity → `ohos-system-app-dev`. Ordinary standalone app →
`ohos-app-dev`.

## The core difference: install ≠ reload

Reinstalling a persistent bundle with `hdc install -r` does **not** restart it; `aa
force-stop` / `kill -9` of a system process is typically blocked. The new code loads only
after a **reboot**, and you must then verify a **fresh pid**.

The DevEco CLI does not document a dedicated system-bundle install/reload command.
Do not infer installation, reboot, signing, or process-reload behavior from `devecocli build`.
For persistent bundles, use the supported DevEco project/Studio deployment workflow and
confirm the result with `devecocli device view` and `devecocli log`.

```
devecocli build
devecocli device list
devecocli device view
```

## Build

- **Standalone module / multi-module assembleHap** (against the installed SDK): use
  `devecocli build` — it builds the project; use documented module-selection options when available. For one module of a
  many-module project, name it so the *right* HAP is installed:
  ```
  devecocli build
  ```
  `devecocli build` invokes the available DevEco toolchain; do not assume fallback behavior
  or invoke unsupported wrappers through this skill.
- **Inside the OHOS source tree** (full image / component): that's the OS build system
  (e.g. `./build.sh --product-name <x> --ccache`, or the vendor docker image), **not**
  `devecocli build`. After a fast rebuild, beware the **staleness trap**: the freshly
  built artifact under `out/.../oniro_soc_products/...` may differ from what's packaged
  under `packages/phone/...` — verify you're deploying the just-built file.

## Signing realities

- `signatures/` and the `signingConfigs` block of `build-profile.json5` are usually
  **gitignored** (outside HEAD). On a fresh worktree, bootstrap them before building:
  ```
  # DevEco CLI does not expose signature generation; configure signing through DevEco Studio.
  ```
- **Dev images** often bypass HAP signature checks; production devices do not.
- System bundles need **`system_app`**-tier signing (vs `hos_normal_app`); a mismatch shows
  up as the `9568332` sign-info-inconsistent error during installation.

## Verify the new code actually loaded

After deployment through the supported DevEco workflow:
```
devecocli device view
devecocli log
```
Review the device details and logs to confirm the target loaded the change. The
CLI does not expose a pid-wait or on-device artifact-inspection command.

## Instrument BEFORE the expensive deploy

The single biggest time-saver on persistent bundles is adding diagnostic logging at every
suspect point before the deployment cycle, then using `devecocli log` once the target loads.

## Inspect window / render state without a rebuild

When a UI bug is about z-order / surface presence rather than logic:
```
devecocli ui window list
devecocli ui layout
```

## Gotchas

- **Search scoping:** the OHOS tree is huge — a `grep`/find from the root times out. Always
  scope to a subdirectory (e.g. the component path).
- **Gesture injection:** use `devecocli ui swipe`, `fling`, `dircfling`, or `drag`.
- **Verify transient UI** (gesture arrows, boot animation) with `devecocli ui screenshot`.
- **Reboot modes:** the DevEco CLI does not document a reboot command. For bootloader/recovery, the underlying
  `hdc shell reboot <mode>`; the canonical OS reboot is `param set ohos.startup.powerctrl reboot`.

## Reference

API-level mapping and the normal inner-loop commands live in **`ohos-app-dev`** — this skill
only adds the platform/persistent specifics on top of it. Standalone SDK projects that need
system-app identity or system permissions belong to **`ohos-system-app-dev`**.
