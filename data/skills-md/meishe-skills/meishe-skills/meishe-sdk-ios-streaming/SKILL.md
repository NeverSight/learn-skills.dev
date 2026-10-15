---
name: meishe-sdk-ios-streaming
description: Build, integrate, troubleshoot, and explain iOS apps that use the Meishe NvStreamingSdkCore Streaming SDK for camera capture, recording, Timeline editing, LiveWindow preview, captions, stickers, transitions, audio, filters, themes, asset packages, AR Scene, beauty, makeup, human detection, templates, compilation, breakpoint-continuation export, media tools, and custom effects. Use for English or Chinese requests mentioning Meishe iOS SDK, 美摄 iOS SDK, NvStreamingSdkCore, NvsStreamingContext, NvsTimeline, capture, timeline, compile, export, 断点续导, caption, sticker, transition, beauty, makeup, AR Scene, template, or Objective-C/Swift API validation.
---

# Meishe iOS Streaming SDK

Use this skill to explain SDK APIs, generate an iOS application or additive integration patch, and diagnose runtime behavior. Treat Objective-C public headers from the user's framework as signature truth. Use the [official iOS documentation](https://www.meishesdk.com/ios/doc_ch/html/content/index.html) for semantics and technical topics when bundled references are insufficient.

## Priority Rules

- Use only Streaming SDK entry points exposed by `NvStreamingSdkCore.framework`. Do not introduce a separate effects runtime or its lifecycle.
- Generate a new UIKit application in Swift by default. Use Objective-C only when the user explicitly requests it or an existing host contract requires it; Objective-C public headers remain API signature truth in both cases.
- Treat `NvStreamingSdkCore.framework` as the user-supplied dynamic SDK artifact, not a package dependency. Do not produce a dependency list or infer private third-party dependencies.
- Keep `NvsStreamingContext` public calls on the main thread unless a public header explicitly documents an exception.
- Verify the SDK license before obtaining the singleton. Keep initialization flags stable for the singleton lifetime.
- Confirm that the supplied SDK license authorizes the generated app's bundle identifier before device QA. Treat `The current app is not authorised!` as a license-to-app-identity mismatch, not as a framework, signing, Timeline, or preview failure.
- A Timeline width must be divisible by 4 and height by 2. Without `NvsStreamingContextFlag_Support4KEdit`, require `width * height <= 1920 * 1080`; with the flag, require `width * height <= 3840 * 2160`. Return or report failure when `createTimeline` yields `nil`.
- A custom compile height requires `setCustomCompileVideoHeight:` before `compileTimeline`, with `NvsCompileVideoResolutionGradeCustom`. Treat the delegate as final success or failure evidence.
- Every resumable Timeline compile must pass both `NVS_COMPILE_ENABLE_BREAKPOINT_CONTINUATION = true` and a non-empty writable `NVS_COMPILE_CACHE_FILE_PATH` through the `compileConfigurations` overload. The caller owns that cache directory: clear stale cache before a non-resume compile, retain it only for a background-interrupted resume, and clear it after final success, failure, or user cancellation.
- Pass `PHAsset.localIdentifier` directly to `NvsVideoTrack` append/insert/add methods for Photos assets. Check permissions, asset availability, identifier emptiness, and the returned `NvsVideoClip`.
- When calculating a video's display size, do not use `getVideoStreamDimension` alone. Require a valid video stream, read `getVideoStreamPixelAspectRatio`, validate `den != 0`, multiply the stored width by `num / den`, and then swap width and height for `NvsVideoRotation_90` or `NvsVideoRotation_270`. Use this corrected display size for aspect selection, preview layout, crop geometry, and export geometry; use the uncorrected dimension only when stored pixel dimensions are explicitly required.
- Before adding an ordinary HTTP or HTTPS media URL as a clip path, preheat it on a worker queue with `NvsStreamingContext.getAVFileInfo`. Remote metadata retrieval can be slow. Continue only when it returns non-`nil`, then switch to the main thread for the Track append/insert/add call and check the returned clip. Call every SDK API on the main thread unless its public documentation explicitly marks a thread exception. `getAVFileInfo` is one such documented exception; never generalize it to another SDK API. Treat M3U8 separately: download the `.m3u8` file locally before adding it, and accept only the Meishe-specific extended format. Never infer, synthesize, or auto-convert private extensions; direct unknown format details to Meishe technical support.
- Install asset packages only through `installAssetPackage(_:license:type:sync:assetPackageId:)`; there is no completion-closure overload. Before an asynchronous install, retain an object conforming to `NvsAssetPackageManagerDelegate` and assign it to the manager's weak `delegate`. Treat the immediate return as start/validation status and wait for `didFinishAssetPackageInstallation(_:filePath:type:error:)` before using the package ID. Template packages install asynchronously regardless of the `sync` argument. Coordinate delegate ownership in an existing host instead of silently replacing its delegate.
- A generation plan is not implementation evidence. Every module reported as emitted must have dependency-closed source, target membership, required permissions/resources, a callable integration entry, observable failure states, and cleanup. If output remains a placeholder or `contract_only`, report that scope instead of claiming the module was generated.
- When `--framework` or `--license` is explicitly supplied for a new app, copy only those user-supplied inputs into the output project. Embed and sign the dynamic framework, copy the license under a stable app resource name, and add it to the target's Resources phase. Never retain the source path in reusable skill data.
- Do not infer runtime or visual success from generation, static validation, compilation, Xcode build, package installation, setter success, or callback registration. Use the exact evidence level recorded in the verification matrices.
- The skill bundles no framework, license, model, media, font, shader, or asset package. Never invent credentials, private endpoints, material services, or protected resources.
- Hand off a filled build command by default. Run Xcode builds, simulator/device actions, or screenshot validation only when the user explicitly asks.

## Workflow

1. Classify the request as initialization, complete editor, import, Timeline editing, preview, capture, effects, AR/beauty, captions/stickers, asset packages, audio, export, templates, media tools, or custom rendering.
2. Read [standalone-workflow.md](references/standalone-workflow.md). For project work also read [execution-and-qa-handoff.md](references/execution-and-qa-handoff.md).
3. For complete editors read [editor-architecture.md](references/editor-architecture.md) and [editor-runtime-pitfalls.md](references/editor-runtime-pitfalls.md). Implement import -> aspect ratio -> persisted Timeline state -> LiveWindow -> child tools -> export.
4. Run `scripts/search_skill_index.py --compact "<request>"` before opening broad references. Treat matches as routing, not runtime proof.
5. For an app, broad feature set, or host integration, run `scripts/compose_modules.py --compact` or `scripts/create_ios_project.py --dry-run-plan`. Use the dependency-closed plan.
6. Resolve user-supplied resources through [resource-requirements-index.md](references/resource-requirements-index.md). Do not retain absolute external roots in registries or documentation.
7. For packaged materials read [asset-center-workflow.md](references/asset-center-workflow.md) and [material-application-matrix.md](references/material-application-matrix.md). Keep installation, application, property editing, instance removal, and package uninstallation separate.
8. For vague requests read [capability-catalog.md](references/capability-catalog.md). For broad ordering use [feature-priority-map.md](references/feature-priority-map.md) and [api-priority-map.md](references/api-priority-map.md).
9. For exact APIs use [api-usage-index.md](references/api-usage-index.md), `sdk-signature-map.json`, and the routed class-family reference.
10. Before implementation read the routed dependency, constraint, constant, and call-order maps. Preserve guards, return checks, callback gates, state conflicts, and teardown order.
11. Use [official-docs-index.md](references/official-docs-index.md) only when the local summary is insufficient or the user requests source detail. Actual public headers win for signatures.
12. Read [runtime-verification.md](references/runtime-verification.md) for evidence levels and claim boundaries. Coverage, build, runtime, and production-resource matrices belong to the separate maintenance package and are not runtime skill dependencies; do not claim their results unless the maintenance evidence is explicitly available.
13. Generate implementation only from `simple-code-registry.json` units whose state permits emission. Never render a `contract_only` unit as completed code.
14. Reconcile the generation plan with emitted source, Xcode target membership, Build Phases, resources, callable UI or host entry points, and failure states. Downgrade the manifest when any planned unit remains a shell.
15. Treat an existing Xcode project as `incremental-integration` with `--mode incremental`. Only use a product blueprint when the skill owns the new output directory.
16. Keep skill artifacts, comments, CLI help, and default template copy in English. The default new-app template and executable validation flow use Swift. Localize generated app UI only when the user requests a different language.
17. Generate the smallest sufficient permissions, resources, controllers, callbacks, and lifecycle integration. Exclude signing identities, private services, analytics, and distribution settings.
18. After implementation provide a filled build command. Execute builds, installation, device flows, or visual QA only with explicit authorization.
19. Keep retrieval compact: inspect matched references and exact symbols rather than dumping full indexes or header trees.

## Reference Routing

- **Core workflow and integration:** [standalone-workflow.md](references/standalone-workflow.md), [ios-integration.md](references/ios-integration.md), [project-structure-rules.md](references/project-structure-rules.md), and [execution-and-qa-handoff.md](references/execution-and-qa-handoff.md).
- **Composition:** [module-contract-schema.md](references/module-contract-schema.md), `sdk-module-registry.json`, [app-blueprints.md](references/app-blueprints.md), `simple-code-registry.json`, and `skill-lookup-index.json`.
- **Feature and API selection:** [capability-map.md](references/capability-map.md), [api-usage-index.md](references/api-usage-index.md), [feature-list.md](references/feature-list.md), [api-list.md](references/api-list.md), and the priority/dependency/constraint/call-order maps.
- **Resources:** [resource-requirements-index.md](references/resource-requirements-index.md), [asset-center-workflow.md](references/asset-center-workflow.md), and [material-application-matrix.md](references/material-application-matrix.md).
- **Verification:** [runtime-verification.md](references/runtime-verification.md). Maintenance-only coverage and verification matrices are intentionally not bundled or referenced as runtime files.

### Class-family routing

| Request or public class | Read |
|---|---|
| Context, license, singleton, capture, playback, seek, compile | [nvs-streaming-context.md](references/nvs-streaming-context.md) |
| LiveWindow, preview, fill mode, coordinate mapping | [nvs-live-window.md](references/nvs-live-window.md) |
| Timeline, tracks, themes, Timeline-level objects | [nvs-timeline.md](references/nvs-timeline.md) |
| VideoTrack, VideoClip, Photos identifiers, trim, speed | [nvs-video-track-clip.md](references/nvs-video-track-clip.md) |
| AudioTrack, AudioClip, music, voiceover | [nvs-audio-track-clip.md](references/nvs-audio-track-clip.md) |
| Captions, modular captions, compound captions, spans | [nvs-caption.md](references/nvs-caption.md) |
| Animated stickers, transforms, animation, Z order | [nvs-animated-sticker.md](references/nvs-animated-sticker.md) |
| Capture/Clip/Track/Timeline/Audio effects | [nvs-fx.md](references/nvs-fx.md) |
| Video or audio transitions | [nvs-transition.md](references/nvs-transition.md) |
| Asset package installation and state | [nvs-asset-package-manager.md](references/nvs-asset-package-manager.md) |
| Adaptive, standard, and AE templates; template install/apply/post-process/edit | [nvs-templates.md](references/nvs-templates.md) |
| Human detection, AR Scene, beauty, shaping, makeup | [nvs-ar-scene.md](references/nvs-ar-scene.md) |
| AR Scene builtin-effect full parameter table (key/type/range/default) | [builtin_effects/ar-scene.md](references/builtin_effects/ar-scene.md) |
| File information, frame retrievers and receivers | [nvs-media-info-retriever.md](references/nvs-media-info-retriever.md) |
| Thumbnails, icons, waveform generation | [nvs-generators.md](references/nvs-generators.md) |
| Media and passthrough conversion | [nvs-convertors.md](references/nvs-convertors.md) |
| Custom video/audio effects and transitions | [nvs-custom-effects.md](references/nvs-custom-effects.md) |
| Graph, storyboard, mask, mesh, 3D composition | [nvs-advanced-composition.md](references/nvs-advanced-composition.md) |
| Structures, time, resolution, enums, flags, keys | [nvs-common-types.md](references/nvs-common-types.md) |

## Specialized Routing And Feature Guards

- Determine whether an effect belongs to Capture, Clip, Track, Timeline, or Audio before choosing an API. Built-in names and packaged IDs are different identities.
- Stop conflicting playback, seek, capture, or compile operations before structural Timeline mutation or removal.
- For media import, classify the input before appending: local path, Photos local identifier, ordinary HTTP/HTTPS media URL, or M3U8. For ordinary remote media, perform the slow first `getAVFileInfo` lookup on a worker queue, require a non-`nil` result, and return to the main thread to append. Localize M3U8 first and reject unconfirmed standard playlists.
- A complete capture flow includes permission gates, LiveWindow connection, device/camera controls as supported, start return checks, recording callbacks, and teardown.
- A complete editor is not a preview shell. It includes import, resolution/aspect choice, persisted state, Timeline reconstruction, LiveWindow, child editors, applied-material state, and compile/export.
- Material installation is not application. Collect required user input first, apply to the semantic target, expose supported property editing, remove the instance separately, and persist stable target relations.
- For asynchronous package installation, route completion through `NvsAssetPackageManagerDelegate`; never generate an invented trailing closure, an `op` token, or a closure-only package ID. Match the callback by the requested file path and asset type, and handle concurrent requests explicitly.
- For templates, read [nvs-templates.md](references/nvs-templates.md). Keep adaptive, standard, and AE/variant-image-size workflows distinct; separate package installation, descriptor inspection, Timeline creation, geometry post-processing, text/media replacement, source trim, and picture crop. Generate only workflows verified by public Streaming SDK APIs.
- For AR visibility failures, check license, required detection features/data, physical-device preview, package type, package installation, parameter key/type/range, strength, action prompts, and subject conditions. Do not claim visibility without visual evidence.

## Independence And Resource Boundary

- Normal lookup, composition, and generation read only bundled skill files plus user-provided projects and resources.
- Public headers and the official documentation may be used for maintenance or exact verification; original input documents and non-bundled local source trees are not runtime dependencies.
- Never copy full sample sources, private service clients, signing configurations, licenses, model bundles, or unselected large materials.
- Store only capability-oriented signature data and verification scope. Do not store user absolute paths or SDK release identifiers.

## Project Structure Rules

- Require explicit `EDITOR_OWNED` or `HOST_OWNED` Timeline ownership for incremental integration. Never remove or rebuild a host-owned Timeline without an explicit host contract.
- Preflight incremental writes transactionally. Identical files are no-ops; any differing host file stops application before mutation. `--force` may replace staging output only.
- Keep `GENERATION_PLAN.json`, emitted sources, target membership, Build Phases, copied resources, and reported capability scope consistent. A project shell must never be presented as a working feature module.
- Keep view controllers thin. Route SDK work through context, Timeline session, editor coordinator, playback, capture, asset, export, and persistence controllers.
- Persist reconstructable JSON with stable IDs and atomic writes; never persist SDK object pointers.
- Clear LiveWindow and show an empty state after deleting the final clip. Reconnect preview when media is added again.
- Keep Timeline aspect ratio, visible LiveWindow container, fill mode, coordinate mapping, and compile geometry consistent.

## Delivery Contract

- Treat create/integrate/fix as authorization to edit only the scoped project, not to build, sign, install, drive a device, or capture screenshots.
- Hand back a filled `xcodebuild` command using the actual project, scheme, configuration, destination, and `CODE_SIGNING_ALLOWED=NO` when appropriate.
- When device QA is requested, state required signing and resource inputs, exercise only the requested deterministic flow, and report exact evidence levels: generated, structurally validated, Objective-C typechecked, Swift compiled, Xcode built, simulator launched, device installed, flow executed, and visually confirmed.
- Treat a missing Development Team, signing identity, or provisioning profile as a device-installation prerequisite, not as an SDK runtime failure. Never read, retain, or fill Apple Account credentials.

## Template Use

Inspect generator options with `scripts/create_ios_project.py --help`.

Create a new dependency-closed Swift app skeleton (Swift is also the default when `--language` is omitted):

```bash
python3 scripts/create_ios_project.py /absolute/output --bundle-id com.example.meisheapp --app-name MeisheStudio --language swift --blueprint short-video-editor --modules caption-editor,sticker-editor,filter-editor
```

Stage an additive patch for an existing Xcode project:

```bash
python3 scripts/create_ios_project.py /absolute/staging --mode incremental --host-project /absolute/host --target-name HostApp --modules timeline-preview,caption-editor,export-compile
```

Generate controllers and a usage contract without an application shell:

```bash
python3 scripts/create_ios_project.py /absolute/output --mode api-only --language swift --modules sdk-runtime,timeline-preview,export-compile
```

Only apply optional feature overlays returned by lookup/composition or explicitly requested by the user.
