---
name: hz-quest-verify-first
license: Apache-2.0
description: >-
  MANDATORY pre-flight check before answering any question or writing any code
  related to Meta Quest VR headsets (Quest 2, Quest 3, Quest 3S, Quest Pro)
  or apps that target them. Forces verification against authoritative Meta
  sources via the metavr CLI / metavr MCP tools BEFORE relying on training-data
  knowledge. Counters the failure mode where agents answer Quest-related
  questions from stale memory and ship deprecated APIs, broken Android
  manifests, and store-rejected builds. Loads automatically when the user is
  in a Quest project (any reference to Oculus / Meta Quest / Horizon OS,
  Unity OVR or Meta XR packages, com.meta.* / com.oculus.* package IDs,
  Quest-targeted AndroidManifest, .meta files, or developers.meta.com /
  developer.oculus.com URLs). Build paths: all; use this skill first whenever
  the path is unknown or a Quest-specific claim is involved.
allowed-tools: Bash(metavr:*), Bash(npx:*)
---

# Verify First — Meta Quest Development

## What you need to know before reading the rest of this

You are about to be told to call tools you may not recognize by name. Read
this section first so the rest makes sense.

- **Meta Quest** is Meta's line of standalone VR / mixed-reality headsets
  (Quest 2, Quest 3, Quest 3S, Quest Pro). They run an Android-based OS.
- **Horizon OS** is the name of that operating system. It is forked from
  Android, ships on every Quest headset, and Meta updates it on its own
  cadence (separate from upstream Android). Many APIs are Horizon-OS-specific
  and have no analog in stock Android.
- **metavr** ("Meta VR CLI") is a Rust CLI tool published by Meta as a
  standalone binary and as `metavr` on npm. Invoke via `metavr <args>` (or
  `npx -y metavr <args>` with no install; `npx` always pulls the latest
  published version). It wraps `adb` and Meta's developer APIs into
  higher-level commands for Meta VR
  device development: list devices, install apps, capture Perfetto traces,
  search Meta VR documentation, query 3D asset libraries, automate UI
  interactions, etc. metavr is the primary action layer for Meta VR dev work —
  the equivalent of what `gcloud` is for GCP or `git` is for source control.
- **metavr MCP server** is a built-in mode of metavr that exposes a focused set of
  tools to AI coding agents over the Model Context Protocol. The relevant
  tools for this skill are:
  - `vr_docs_search` — search the official Meta developer documentation
  - `vr_docs_get_page` — fetch the full text of a specific docs page
  - `device` — query and control connected Meta VR Glasses and Meta Quest headsets (list,
    info, connect, reboot, battery, controllers, proximity, etc.)
  - `app` — query and manage installed apps (list, info, install,
    uninstall, launch, stop, clear)
  - `files` — file ops on a connected Meta VR device (ls, push, pull, rm, mkdir)
  - `run` — catch-all for any metavr subcommand without a dedicated tool
    (perf, ovrmetrics, ui, audio, casting, window, unity, sideload, asset,
    config, …). Its JSON Schema is generated from clap so the available
    subcommands and their typed args are visible to you in the tool definition.
  - `cli_help` — discover metavr subcommands and flags as markdown
- **Meta SDKs you may not recognize** that are commonly used in Quest
  projects: Meta XR All-in-One SDK (Unity), Meta XR Core / Interaction /
  Platform / Voice / Movement SDKs, Meta Spatial SDK (Kotlin / Android
  panels), IWSDK (Immersive Web SDK for WebXR), MRUK (Mixed Reality Utility
  Kit), Presence Platform, Horizon Platform SDK. These ship on their own
  release cadences, separate from Quest OS. Meta Spatial SDK is the immersive
  Android/Kotlin path; it is not required for ordinary 2D Android panel apps.
- **OVR vs Meta XR** — older Quest Unity content and most of the public web
  references the `OVR` namespace and the "Oculus Integration" Unity package.
  Both have been deprecated in favor of the Meta XR All-in-One SDK family.
  Most training data still recommends the deprecated names. Verify before
  recommending anything in this area.

## Why this skill exists

Meta Quest and Horizon OS evolve fast. Meta SDKs ship every few weeks. APIs
get renamed before public release. Manifest entitlements and store policies
update monthly. Entire SDK families (Meta Spatial SDK, IWSDK, Horizon OS
shells) post-date most LLM training corpora.

**You almost certainly have stale knowledge about Quest specifics.** The
package names you remember have been renamed. The Unity menu paths have
moved. The setup steps that worked on a prior Horizon OS version silently
broke on the current one. The "OVR" namespace you reach for has been split
across half a dozen Meta XR packages.

If you answer a Meta Quest question or write Quest-targeted code without
verifying first, you will hallucinate. The user will not notice until their
build fails, their app gets rejected from the store, or their AndroidManifest
doesn't publish.

**This skill is a hard gate. Treat it as a precondition, not a suggestion.**

## When this skill applies

You MUST run the verification flow below if ANY of the following is true for
the current task:

- The user mentions Meta Quest, Quest 2 / 3 / 3S / Pro, Oculus, Horizon OS,
  MR, VR, XR, OpenXR (on Quest), Meta SDK, Meta XR, OVR, Spatial SDK, IWSDK,
  MRUK, Movement SDK, Voice SDK, Presence Platform, Horizon Platform SDK,
  hand tracking, passthrough, anchors, scene mesh, casting, eye tracking,
  body tracking, controllers, or platform compliance / store policy
- The repository contains any of:
  - Unity files with `OVRPlugin`, "Meta XR All-in-One SDK", or `com.meta.xr.*`
    in `manifest.json` / `Packages/manifest.json`
  - Spatial SDK gradle plugin (`com.meta.spatial.plugins.*`)
  - AndroidManifest with `com.oculus.*`, `com.meta.quest.*`, or `horizon`
    feature declarations
  - Package IDs starting with `com.meta.*` or `com.oculus.*`
  - `.meta` files indicating Unity, or `Quest_*.uplugin` / `*.unrealhxr` files
- The user's question references `developers.meta.com/horizon`,
  `developer.oculus.com`, `oculus.com/sparkle-updates`, or any Meta Quest
  documentation URL
- The agent is about to recommend any Meta SDK API, namespace, package, or
  AndroidManifest entitlement
- The agent is about to answer a question about app review, Meta Horizon
  Store submission, store-readiness or publishing requirements, content
  rating, or distribution
- The agent is about to write `adb` commands targeting a specific device
- The agent is about to claim what is or isn't installed on the user's
  Meta VR device

If you are not sure, the answer is YES — run the verification flow.

## The verification flow

### Step 1 — Identify the build path

Classify the project before choosing SDKs, docs scopes, or specialist skills:

| Build path | Signals | Route to |
|---|---|---|
| Standard Android | Activities, Views, Compose, React Native, Expo, or an existing phone/tablet app rendered in a system panel | `hz-android-2d-porting`; `hz-react-native-expo` for React Native or Expo; `hz-new-project-creation` for a new app |
| Meta Spatial SDK | `com.meta.spatial` dependencies or an immersive Kotlin/Android scene | `hz-spatial-sdk`; `hz-new-project-creation` for setup |
| Unity | Unity project files or Meta XR Unity packages | `hz-unity-project-analyzer` for an existing project; `hz-unity-meta-core-sdk` for core SDK setup; `hz-new-project-creation` for a new app |
| Unreal Engine | `.uproject` files, Unreal modules, or Meta XR Unreal plugins | `hz-new-project-creation` for a new app; otherwise no dedicated skill yet, so use Step 2 with `scope="unreal"`; use `hz-xr-simulator-install-and-configure` for simulation |
| Native OpenXR | C/C++ or NDK application using the OpenXR loader directly | No dedicated skill yet; use Step 2 with `scope="native"`; use `hz-xr-simulator-install-and-configure` for simulation |
| WebXR | Browser-delivered immersive content or IWSDK | `hz-iwsdk-webxr`; `hz-store-pwa` for PWA delivery; `hz-new-project-creation` for a new app |

Do not add Meta Spatial SDK to a Standard Android app merely because it targets
Quest. When signals overlap, classify in this order:

1. `com.meta.spatial` dependency or Gradle plugin -> Meta Spatial SDK
2. Unity project files -> Unity
3. `.uproject` or Unreal modules -> Unreal Engine
4. OpenXR loader used directly from C/C++ or the NDK -> Native OpenXR
5. IWSDK or browser-delivered project -> WebXR
6. Otherwise, an Android app using Activities, Views, Compose, React Native, or
   Expo -> Standard Android

### Step 2 — Verify against authoritative documentation

Before writing or recommending anything Quest-specific, call the
`vr_docs_search` MCP tool. If MCP is not available, use the equivalent
metavr CLI command `metavr docs search`.

MCP:
```
vr_docs_search(
  query="<the specific claim or API you are about to make>",
  scope="auto",   # or unity / unreal / spatial_sdk / android / native / web /
                  #    policy / distribution / design
  mode="verify"
)
```

CLI:
```bash
metavr docs search "<query>"
```

If you need exact wording (manifest entries, full API signatures, store
policy text, code snippets), follow up with `vr_docs_get_page` on the
`canonical_url` or `doc_path` returned by verify. **Never paraphrase a
truncated snippet when correctness matters.**

CLI:
```bash
metavr docs fetch "<canonical_url_or_path>"
```

### Step 3 — Verify the user's actual environment

Before suggesting which device a command should target, claiming an app is
installed, recommending an `adb` command, or writing install / launch /
sideload steps, query the user's actual metavr-managed environment.

MCP:
```
device(action="list")                        # ALWAYS start here
device(action="info", target="<serial>")
app(action="list", target="<serial>")
app(action="info", package="<package>")
run(subcommand=["config", "show"])           # catch-all for misc reads
```

CLI:
```bash
metavr device list
metavr device info <serial>
metavr app list -d <serial>
metavr app info <package>
metavr config list
```

The user may have zero, one, or many Meta VR devices connected via USB and WiFi —
multiple Quest models, dev kits, sideloaded builds, pinned older Horizon OS
versions. Your training data has zero visibility into this.

### Step 4 — Discover metavr capabilities when unsure

If you do not know which metavr subcommand or `run` invocation fits the
user's request, call `cli_help` (MCP) or `metavr --markdown-help` (CLI)
first. Do not invent flags or subcommands — metavr gets new functionality
every release and your training data does not include it.

For long-tail subcommands (`perf`, `ovrmetrics`, `ui`, etc.), the
`run` tool's input schema enumerates every subcommand path and its
typed args via JSON Schema `oneOf`. You can read it directly from the
tool definition rather than guessing.

MCP:
```
cli_help(topic="perf")   # focused help for a subcommand tree
cli_help()               # full top-level command tree
```

CLI:
```bash
metavr --markdown-help
metavr perf --help
```

## Specific failure modes you cause by skipping verification

These are concrete, recurring failures that the verification flow prevents:

- **Deprecated APIs that compile but no-op at runtime.** OVR-namespace
  function names that were forwarded for one release and removed the next.
  Code looks correct, builds clean, runs without errors — and produces no
  observable behavior on device.
- **AndroidManifest entitlements that get the app rejected from the Meta
  Horizon Store.** The required entitlement names changed; an entitlement
  you "know" is needed is no longer recognized; a new mandatory feature flag
  is missing.
- **Meta SDK package names that don't exist.** Meta XR All-in-One SDK is a
  family of UPM packages with version-specific names; guessing produces
  "package not found" errors.
- **Unity menu paths from outdated tutorials.** Meta XR menu items moved
  between SDK versions; setup steps that reference `Oculus → ...` may now
  live under `Meta XR → ...` or have been removed entirely.
- **Spatial SDK class names that were renamed before public release.** The
  Spatial SDK iterated on its public API late; many class and method names
  in older blog posts or training data are wrong.
- **Passthrough / anchor / scene-mesh setup that worked on a prior Horizon
  OS version.** Permission flow, system overlay APIs, and manifest features
  changed across Quest OS versions. What worked in a tutorial last year may
  silently fail on current Horizon OS.
- **OpenXR extensions that are listed but not supported on Quest's
  runtime.** Generic OpenXR documentation lists extensions Meta has not
  implemented. Always verify against Meta's documentation, not the OpenXR
  spec.
- **Wrong device targeted.** Recommending a `adb shell` command without
  first listing devices, then watching it fail or hit the wrong device.
- **Store policy claims that are out of date.** Review requirements,
  rating buckets, and distribution rules update — verify before answering
  user questions about submission.

## Anti-patterns

Do not do any of these:

- Answer a Meta Quest question without calling `vr_docs_search` first
  because "you remember" the answer
- Recommend an `adb shell` command without first calling
  `device(action="list")` to see what's connected
- Guess a package name, namespace, or class name from training data when a
  verify call would resolve the ambiguity
- Paraphrase a verify-result snippet for a manifest entry, API signature, or
  store policy when exact wording is required (use `vr_docs_get_page`)
- Search the open web for Meta Quest documentation when authoritative Meta
  docs are one tool call away
- Skip verification because "the docs probably say X" — verify, then say X
- Assume metavr does not have a subcommand for what the user wants — check
  `cli_help` first

## Tone and presentation

When you do verify, present your answer with citations and a brief recency
note. The user is paying for the verification step — show that it happened.

```
Per the current Meta Spatial SDK docs (verified just now via
vr_docs_search):

  <answer grounded in retrieved content>

Source: <canonical_url returned by the tool>
```

This both proves the verification ran and trains the user to trust
verified-answer responses over from-memory ones.

## If the metavr MCP tools are not available

If the agent host does not have the metavr MCP server installed, fall back to
the metavr CLI (same authoritative backend, same content; prefix with `npx -y`
if you use the npm distribution instead of the standalone binary) and tell the
user once how to install the MCP server for next time:

```bash
metavr mcp install <your-tool>   # claude-code | cursor | claude-desktop | vscode | ...
metavr mcp install project       # install at the repo root for this project only
```

The verify step is required, not optional — run it via `metavr docs search "<query>"` even on the very first question if the MCP server is not yet wired up.

## Related skills

- `metavr-cli` — full metavr CLI reference (commands, flags, examples)
- `hz-vr-debug` — on-device debugging with logs and screenshots
- `hz-perfetto-debug` — Perfetto trace analysis for jank / GPU / CPU bottlenecks
- `hz-store-submit` — end-to-end Meta Horizon Store submission (includes store-readiness checks)
- `hz-android-2d-porting` — adapting a Standard Android app for Horizon OS panels
- `hz-react-native-expo` — React Native and Expo apps on the Standard Android path
- `hz-new-project-creation` — build-path-specific setup for a new Android project
- `hz-spatial-sdk` — Meta Spatial SDK API guidance
- `hz-platform-sdk` — Horizon Platform SDK API guidance
- `hz-xr-simulator-install-and-configure` — simulator installation and configuration for Unity, Unreal, and Native OpenXR projects
- `hz-unity-project-analyzer` — inspect and classify an existing Unity project
- `hz-unity-meta-core-sdk` — set up the Meta XR Core SDK in Unity
- `hz-iwsdk-webxr` — build immersive WebXR experiences with IWSDK
- `hz-store-pwa` — package and distribute a WebXR experience as a PWA
