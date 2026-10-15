---
name: meishe-sdk-harmony-streaming
description: Generate, build, integrate, troubleshoot, and explain HarmonyOS ArkTS/ETS Stage apps that use the Meishe libNvStreamingSdkCore Streaming SDK. Supports clean new-app generation, api-only and incremental staging, OHPM/Hvigor builds, initialization, Timeline and audio editing, LiveWindow preview, NvsStreamingContext capture, captions, stickers, transitions, FX parameters, beauty, AR Scene, asset packages, templates, compile/export, media tools, callbacks, and custom NAPI video effects. Use for English or Chinese requests mentioning HarmonyOS, 鸿蒙, ArkTS, ETS, Stage, hvigor, 生成鸿蒙工程, libnvstreamingsdkcore, NvStreamingSdkCore, NvsStreamingContext, NvsTimeline, NvsLiveWindow, capture, compile, caption, sticker, transition, beauty, AR Scene, template, or Meishe Streaming SDK APIs. Keep standalone NvsEffectSdkContext/NvsEffectScheduler EffectSDK flows outside this skill.
---

# Meishe Harmony Streaming SDK

Use this skill to generate, build, explain, and integrate Meishe `libnvstreamingsdkcore` APIs in HarmonyOS ArkTS/ETS projects. Treat the SDK package's public `.d.ets` declarations as signature truth. Demo code is evidence for call patterns only, never the source of public API truth.

## Priority Rules

- Use only Streaming SDK entry points exported by `libnvstreamingsdkcore` / `@meishe/libnvstreamingsdkcore`. Do not introduce a separate EffectSDK runtime unless the user explicitly asks for EffectSDK.
- In this skill, capture AR Scene uses `NvsStreamingContext.appendBuiltinCaptureVideoFx('AR Scene')`; never replace it with a standalone `NvsEffectSdkContext` / `NvsEffectScheduler` pipeline.
- Import the SDK through the host project's established wrapper when present, such as `util/NvSDKHeader.ets`; otherwise import the default `NvsStreamingContext` and named types from `libnvstreamingsdkcore`.
- Initialize with `NvsStreamingContext.init(context, licensePath, flags)` before calling `NvsStreamingContext.getInstance()`. Keep initialization flags stable for the singleton lifetime.
- Keep public Streaming SDK calls on the UI thread unless the `.d.ets` documentation explicitly states an exception.
- Use `rawfile:/...` resource paths for packaged Harmony resources shown in the host project. Never retain absolute demo, license, model, media, HAR, or local SDK paths in reusable skill output.
- Check nullable returns from `init`, `getInstance`, `createTimeline`, `appendVideoTrack`, `appendClip`, `connectTimelineWithLiveWindow`, asset installation, capture effects, and compile entry points.
- A Timeline width must be divisible by 4 and height by 2. Use the Harmony enum names from `.d.ets`, such as `NvsStreamingContextFlags.NvsStreamingContextFlags_Support4KEdit`.
- A custom compile height requires `setCustomCompileVideoHeight(height)` before `compileTimeline(...)` with `NvsCompileVideoResolutionGrade.NvsCompileVideoResolutionGradeCustom`.
- Stop conflicting playback, seeking, capture, recording, or compile work before structural Timeline mutation, Timeline removal, or preview rebinding.
- Do not infer visual or runtime success from generation, static validation, callback registration, or a successful method return alone. Report the exact evidence level available.
- Generate projects only with `scripts/create_harmony_project.py`; do not hand-copy the maintenance demo or its signing configuration.
- Require the caller to provide HAR, license, models, media, and material packages. The skill template contains none of these external resources.
- Use `scripts/build_harmony_project.py` for OHPM/Hvigor validation. A generated project is not a built, installed, executed, or visually verified app.

## Workflow

1. Classify the request as initialization, Timeline creation, preview/playback, media import, editing, captions/stickers, effects, AR/beauty, asset packages, capture, templates, compile/export, media tools, callbacks, or custom effects.
2. Run `scripts/search_skill_index.py --compact "<request>"` before opening broad references. Treat matches as routing hints.
3. For project generation or integration read [harmony-project-generator.md](references/harmony-project-generator.md), [standalone-workflow.md](references/standalone-workflow.md), [harmony-integration.md](references/harmony-integration.md), and [project-structure-rules.md](references/project-structure-rules.md).
4. For exact APIs use [api-usage-index.md](references/api-usage-index.md), `sdk-signature-map.json`, and the routed class-family reference.
5. For feature composition run `scripts/compose_modules.py --compact --query "<request>"` and use the dependency-closed module plan as scope, not runtime proof.
6. For a new project run `scripts/create_harmony_project.py <output> --sdk-har <har> --license <license> --modules <ids>`. For an existing project first run `scripts/create_harmony_project.py --mode incremental --modules <ids> --dry-run-plan`, then generate a staging directory with `scripts/create_harmony_project.py <staging> --mode incremental --modules <ids>`. Use `--host-project <host> --apply` only after review; it copies generated ArkTS sources and never edits host JSON5 or copies staged resources into the host.
7. When build validation is requested, run `scripts/build_harmony_project.py <project>` and report the exact terminal result and HAP path.
8. For resources read [resource-requirements-index.md](references/resource-requirements-index.md). Keep license, models, media, fonts, packages, HARs, and demo roots outside the skill.
9. For packaged materials read [asset-center-workflow.md](references/asset-center-workflow.md) and [material-application-matrix.md](references/material-application-matrix.md). Separate package installation from applying a material instance.
10. Before proposing code read [api-call-order-map.md](references/api-call-order-map.md), [api-constraint-map.md](references/api-constraint-map.md), and [editor-runtime-pitfalls.md](references/editor-runtime-pitfalls.md).
11. Generate snippets only from `simple-code-registry.json` units whose state permits emission or from signatures verified in `sdk-signature-map.json`.
12. Read [runtime-verification.md](references/runtime-verification.md) before making claims about build, device, preview, capture, or compile success.
13. Keep retrieval compact: inspect matched references and exact symbols rather than dumping broad indexes.

## Reference Routing

| Request or public class | Read |
|---|---|
| Generate Stage project, incremental integration, OHPM, Hvigor build | [harmony-project-generator.md](references/harmony-project-generator.md) |
| Context, license, singleton, callbacks, playback, seek, capture | [nvs-streaming-context.md](references/nvs-streaming-context.md) |
| Harmony package/import/module rules | [harmony-integration.md](references/harmony-integration.md) |
| LiveWindow preview and timeline binding | [nvs-live-window.md](references/nvs-live-window.md) |
| Timeline, tracks, duration, Timeline-level objects | [nvs-timeline.md](references/nvs-timeline.md) |
| VideoTrack, VideoClip, import, trim, speed | [nvs-video-track-clip.md](references/nvs-video-track-clip.md) |
| AudioTrack and AudioClip | [nvs-audio-track-clip.md](references/nvs-audio-track-clip.md) |
| Captions and caption styling | [nvs-caption.md](references/nvs-caption.md) |
| Animated stickers | [nvs-animated-sticker.md](references/nvs-animated-sticker.md) |
| Capture, clip, track, timeline, and audio effects | [nvs-fx.md](references/nvs-fx.md) |
| Video or audio transitions | [nvs-transition.md](references/nvs-transition.md) |
| Asset package installation and state | [nvs-asset-package-manager.md](references/nvs-asset-package-manager.md) |
| Template installation, footage replacement, template Timeline | [nvs-template.md](references/nvs-template.md) |
| Compile/export, callbacks, configurations, custom height | [nvs-compile-export.md](references/nvs-compile-export.md) |
| AR Scene, beauty, makeup, detection data | [nvs-ar-scene.md](references/nvs-ar-scene.md) |
| AR Scene builtin parameter table | [builtin_effects/ar-scene.md](references/builtin_effects/ar-scene.md) |
| File information and frame retrievers | [nvs-media-info-retriever.md](references/nvs-media-info-retriever.md) |
| Icon and waveform generation | [nvs-generators.md](references/nvs-generators.md) |
| Standalone media conversion | [nvs-convertors.md](references/nvs-convertors.md) |
| Custom video effects and NAPI callback objects | [nvs-custom-effects.md](references/nvs-custom-effects.md) |
| Structures, time, resolution, enums, flags, keys | [nvs-common-types.md](references/nvs-common-types.md) |

## Evidence Boundary

- Runtime lookup uses bundled references, registries, and scripts only.
- `.d.ets` extraction, demo scanning, version manifests, coverage summaries, and sample roots belong to the separate maintenance package.
- Demo evidence may confirm that a configured maintenance sample uses a call pattern; it must not be used to invent or widen a public API.
- Never store or emit local absolute paths from the Harmony demo repository in skill artifacts.
- Generated project manifests may record destination-relative paths and resource hashes, never caller absolute source paths.
