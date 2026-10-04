---
name: ohos-system-app-dev
description: Develop, sign, deploy, and verify standalone OpenHarmony apps whose APIs or permissions may require `hos_system_app`, an elevated APL, ACL/provisioning, or a Full SDK system API. Use for privileged inspection or control of other apps or protected device state and for `Not System App` failures, then verify requirements against the exact SDK metadata. For public ordinary-app capabilities use `ohos-app-dev`; for OHOS source-tree components use `ohos-system-dev`.
---

# OpenHarmony System App Dev

Privilege-preflight and inner-loop skill for a standalone SDK project whose HAP may need
to run as a system app. This is the middle case between an ordinary application and a
platform component: it uses the normal application project structure, but a privileged
build must carry `hos_system_app` identity, the required APL, any permitted ACLs, and a
certificate chain trusted by the target image.

Use **`devecocli`** for lint, build, device discovery, logs, and UI operations. Use the
Full OpenHarmony SDK's `hap-sign-tool.jar` for offline profile/HAP signing. This workflow
does not require Huawei-account signing for the SDK development-signing path.

> **Prereqs:** an existing OpenHarmony application project, a Full OpenHarmony SDK matching
> the project's compile API, a JDK containing `java` and `keytool`, and a development target
> that trusts the SDK's OpenHarmony development certificate chain. The SDK development key
> is for local development only, never production distribution.

## Routing rule

Route by a suspected entitlement requirement, not by the apparent scope of the feature.
Select this skill when an API or permission may require system-app identity, an elevated
APL, ACL/provisioning, a Full SDK system API, or system-app signing. Product requests for
privileged inspection or control of other apps or protected device state are clues that
require this preflight even when the user does not say "system app."

Do not classify an application solely because a feature is cross-app or device-wide.
Ordinary applications can use public inter-application APIs, while some system APIs operate
entirely within one application. Inspect the exact target SDK's API annotations and
permission definitions first. If every required capability is available to an ordinary
application, continue with `ohos-app-dev`; otherwise continue with this skill.

## When to use

Use this skill when a standalone application:

- calls an API that reports `Not System App` or is declared as a system API;
- requests a permission whose definition requires system-app identity, elevated APL, or ACL;
- must be installed as `isSystemApp: true` on a compatible emulator/development device; or
- needs an offline, reproducible system-profile experiment without Huawei account services.

Route an ordinary standalone application to **`ohos-app-dev`**. Route SystemUI, launcher,
other OHOS source-tree components, and genuinely persistent/reboot-to-reload bundles to
**`ohos-system-dev`**. System-app identity does not by itself make a bundle persistent.

## Tool boundary

- **Scaffold:** `ohos-app-scaffold` / `devecocli create`, then continue here in a separate
  development step.
- **Edit/lint/build/device/UI/logs:** use the normal `ohos-app-dev` guidance and `devecocli`.
- **System signing:** use [`scripts/system-app-sign.mjs`](scripts/system-app-sign.mjs).
- **Exact HAP install and launch:** use the DevEco toolchain's `hdc` because `devecocli run`
  does not accept an arbitrary post-build signed HAP path.
- **Custom/OEM signing:** read [`references/signing.md`](references/signing.md) and require
  user-provided trusted material; never substitute the SDK development identity silently.

## Privilege preflight

Before signing or changing configuration:

1. Read `build-profile.json5` and confirm `compileSdkVersion`, `targetSdkVersion`,
   `compatibleSdkVersion`, and `runtimeOS`. Use a Full OpenHarmony SDK when the API is not
   part of the public SDK.
2. Read every requested permission's definition from that exact SDK. Record its grant mode,
   permission APL, system-app restriction, and whether ACL/provisioning is allowed. Adding a
   name to `allowed-acls` cannot make an ineligible permission grantable.
3. Treat `202 Not System App`, `9568289 grant request permissions failed`, and signing
   failures as different gates. Do not infer from an emulator's Release label that all
   elevated applications are rejected.
4. Ensure the signing work directory and generated HAPs are gitignored. Never edit an SDK
   template or SDK keystore in place, copy a private key into the project, or print passwords.
5. If the project already has custom signing configuration or material, preserve it. The
   post-build workflow below does not require adding or replacing `signingConfigs`.

## Inner-loop workflow

1. **Edit** the standalone application using the normal ArkTS/ArkUI architecture guidance.
2. **Lint** with `devecocli check lint` and treat zero checked files as weak evidence.
3. **Build** with `devecocli build`; require `BUILD SUCCESSFUL` and exit code `0`.
4. **Select the exact unsigned HAP.** Never sign "the newest HAP" or guess among modules.
5. **Sign and verify** the selected artifact with the helper:

   ```powershell
   node <skill-dir>/scripts/system-app-sign.mjs `
     --project-dir <project-dir> `
     --sdk-dir <full-sdk-api-dir> `
     --hap <exact-unsigned-hap> `
     --apl system_basic `
     --acl ohos.permission.EXAMPLE
   ```

   Repeat `--acl` for each required ACL. Supply the complete set in one invocation because
   the generated profile contains exactly the requested list.
6. **Device gate:** run `devecocli device list`. Resolve multiple targets explicitly.
7. **Install the exact verified HAP:**

   ```powershell
   hdc -t <serial> install -r <signed-hap>
   ```

   On `9568332`, stop before uninstalling and request explicit approval to replace the
   differently signed package. On `9568289`, return to the privilege/profile audit.
8. **Verify Bundle Manager state:**

   ```powershell
   hdc -t <serial> shell bm dump -n <bundle-name>
   ```

   Require `isSystemApp: true` and the expected requested permission state.
9. **Launch separately**; a standalone system app is not assumed to be persistent:

   ```powershell
   hdc -t <serial> shell aa start -b <bundle-name> -a <ability-name>
   ```

10. **Observe** with `devecocli log`, `devecocli ui layout`, and
    `devecocli ui screenshot`. Completion requires visible/runtime evidence in addition to
    signer and installer success.

## Signing helper contract

`scripts/system-app-sign.mjs` performs the fragile work deterministically:

- reads bundle/version information without changing the project;
- copies the unsigned release profile template to a project-local work directory;
- exports the SDK root and application CA certificates as DER `.cer` files;
- generates a CA-issued certificate chain for the SDK's Application Release key;
- writes `hos_system_app`, the requested APL, and the complete ACL set into the copied profile;
- signs and verifies the profile;
- signs the exact input HAP and runs `verify-app` with accepted `.cer` / `.p7b` outputs; and
- checks the embedded profile before emitting the signed HAP path and SHA-256 as JSON.

The helper refuses to overwrite generated outputs unless `--force` is supplied. `--force`
applies only to its named outputs inside the selected work directory; it does not delete
project source, SDK files, installed packages, or arbitrary directories.

## Proof required

Do not report success from a build or install message alone. Keep four independent gates:

1. `verify-app` and embedded-profile verification pass.
2. Installation exits successfully.
3. `bm dump` reports system identity and expected permissions.
4. The intended system API or behavior succeeds at runtime.

## Reference

- [`references/signing.md`](references/signing.md) - profile fields, failure routing,
  development-signing limits, and custom/OEM signing boundaries.
- ArkTS strictness, application architecture, and ordinary UI/debug operations remain in
  **`ohos-app-dev`**; this skill adds only the standalone system-identity workflow.
