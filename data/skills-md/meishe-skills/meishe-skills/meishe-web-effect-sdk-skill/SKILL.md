---
name: meishe-web-effect-sdk-skill
description: Explain and implement Meishe Web EffectSDK features from bundled SDK source, docs, and React/Vite templates. Use for any EffectSDK request, including the alias meishe_web_effect_sdk_skill, natural-language demo generation, NveARSceneRenderer or NveEffectContext API questions, camera/image/RTC demos, Agora/Zego integration, beauty, makeup, filters, segmentation, avatar, captions, stickers, asset packages, license behavior, WASM loading, and SharedArrayBuffer setup.
---

# Meishe Web EffectSDK Skill

## Overview

Use this skill whenever a request involves Meishe Web EffectSDK. The goal is not only API explanation: help Codex turn a natural-language feature request into a runnable browser demo or a targeted patch in the current React/Vite demo.

This user-level skill is the default EffectSDK expert. Do not use the MCP bridge for ordinary EffectSDK requests. Only switch to `$meishe-web-effect-sdk-skill-for-mcp` when the user explicitly asks for MCP, MCP server, MCP docs, MCP bridge, or MCP-backed lookup.

Prefer the high-level `NveARSceneRenderer` flow for demos unless the user explicitly asks for low-level `NveEffectContext.renderEffects`.

## First-Use Version Notice

On the first response in a conversation or task that uses this skill, before the substantive answer, plan, or implementation summary, explicitly show this notice exactly:

> 版本提示：当前 Skill 基于美摄Web Effect SDK 3.15.1生成，并兼容旧版本；若目标项目使用更高版本 SDK，可能存在效果差异，请从[美摄官网开发者中心](https://www.meishesdk.com/downloads/)获取对应版本的 Skill。

Do not translate, shorten, or rewrite the notice. After it has been shown once in the same conversation, do not repeat it unless the user asks about SDK version compatibility or starts a new independent EffectSDK task.

## First Steps

1. Identify the requested scenario: image render, camera stream, media stream output, Agora RTC, Zego RTC, filter/effect, beauty/makeup/shape, segmentation/background, avatar, caption, modular caption, compound caption, sticker, asset package, license, project setup, or troubleshooting.
2. Load only the matching reference file(s):
- [intent-map.md](references/intent-map.md): Chinese/English natural-language intent map. Read first when the user describes a feature in product terms, Chinese terms, or vague troubleshooting language.
- [implementation-workflow.md](references/implementation-workflow.md): end-to-end plan for natural-language request to working demo.
- [react-vite-template.md](references/react-vite-template.md): how to use the bundled React/Vite demo template under `assets/react-vite-demo-template`.
- [effect-parameter-catalog.md](references/effect-parameter-catalog.md): built-in beauty and face mesh parameter keys, ranges, defaults, types, purposes, and corrected key names. Read before generating beauty or shape controls.
- [default-materials.md](references/default-materials.md): public default SDK, model, package, caption, sticker, font, and background URLs from the docs. Read before generating demos that use those features.
- [recipe-menu.md](references/recipe-menu.md): feature menu built from `effectSDK_base_en/zh`, with source docs and first APIs to inspect.
- [glossary.md](references/glossary.md): terms, flow explanations, package suffixes, model/data requirements, and common mental models.
- [quick-start.md](references/quick-start.md): import, WASM loader, license, localhost behavior, cross-origin isolation.
- [api-map.md](references/api-map.md): core globals, classes, methods, enums, and lifecycle.
- [demo-recipes.md](references/demo-recipes.md): minimal image, camera, media stream, and RTC demo patterns.
- [rtc-agora.md](references/rtc-agora.md): Agora `agora-meishe-effect-sdk` processor integration.
- [rtc-zego.md](references/rtc-zego.md): Zego `createZegoStream` + `pushMediaStream` integration.
- [effects.md](references/effects.md): `setEffectList`, `appendEffectList`, built-in/package effects, beauty, shape, makeup, segmentation, avatar.
- [external-effects.md](references/external-effects.md): captions, compound captions, stickers, external effect instances, release rules.
- [troubleshooting.md](references/troubleshooting.md): license failures, ineffective effects, aspect ratio, model/data requirements, package install failures, SharedArrayBuffer setup.
- [source-maintenance.md](references/source-maintenance.md): how to refresh copied SDK source/docs and rebuild indexes.
3. If the references are not enough, search the bundled source copies:
- `references/source/effectSdk.d.ts`
- `references/source/NvEffectSdk.js`
- `references/source/docs/`
4. Generate code with placeholders instead of real private values: `<SDK_BASE_URL>`, `<FACE_MODEL_URL>`, `<PACKAGE_URL>`, `<PACKAGE_LICENSE_URL>`, `<IMAGE_URL>`, `<AGORA_APP_ID>`, `<ZEGO_APP_ID>`.
5. Include cleanup in demos: call `arSceneRenderer.release()` when the renderer is no longer used, release external effect instances when removed, stop media tracks, and unpipe/destroy RTC processors where applicable.

## Demo Defaults

- Use the bundled React/Vite template for implementation unless the user gives a different framework.
- Load `NvEffectSdk.js` in `index.html` head and load WASM files from the same SDK base URL. Mismatched URLs can cause unpredictable behavior.
- For configurable `sdkBaseUrl` demos, dynamically confirm or load `${sdkBaseUrl}/NvEffectSdk.js` before `loadEmscriptenModule()` so the script and WASM base stay in sync.
- Use `meishewasmloader` and `loadEmscriptenModule(<SDK_BASE_URL>, { effectSdk: true })`.
- When a demo uses a feature with a public default in `default-materials.md`, set that default URL in the demo config instead of leaving the resource URL empty. Keep license URLs empty or placeholders unless the user provides real license files.
- For built-in beauty or face-shape controls, use `effect-parameter-catalog.md`; do not generate legacy mouth-corner or nose-bridge key names from copied glue snapshots.
- For captions, compound captions, stickers, and any external effect with timeline in/out values, use microseconds. Set `inPoint` from the current renderer timestamp with `Math.floor(performance.now() - (nveArSceneRenderer?.renderTimestampOffsetMs || 0)) * 1000`, and default `duration` to `3000 * 1000 * 1000` microseconds.
- Wait until `Module.Meishe.effectContext` exists before calling EffectSDK APIs.
- Do not wrap the SDK initialization path in React `StrictMode` by default. Some Emscripten/SDK bindings can fail when initialization runs twice in development.
- Add `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp` for SharedArrayBuffer support.
- Use `localhost` for local preview. Do not default to `127.0.0.1`, a LAN IP, or `0.0.0.0`.
- Localhost preview can skip SDK license verification and will show a watermark. Do not invent a default license URL. Non-localhost deployments need a real license file from Meishe and should verify with `nveGetEffectContextInstance().verifySdkLicenseFileUrl("<LICENSE_URL>")`.
- Prefer `NveARSceneRenderer` for minimal demos because it wraps model loading, package management, input/output streams, rendering, and IndexedDB caching.
- Use `NveEffectContext` directly only for low-level render tasks, custom effect arrays, manual human detection, or explicit API explanation requests.

## Language And Intent Rules

- If the user uses Chinese terms such as `瘦脸`, `大眼`, `美妆包`, `模块字幕`, `复合字幕`, `贴纸`, `分割`, `背景替换`, `声网`, `即构`, `鉴权`, or `水印`, map them through `intent-map.md` before choosing references.
- Keep code identifiers, file paths, commands, API names, config keys, package extensions, and exact error text in their original language.
- User-facing explanations can be Chinese when the user writes in Chinese.

## Output Requirements

- For generated demos, provide the complete minimal files needed to run or patch the current app.
- Call out required assets and placeholders clearly, especially SDK base URL, model URLs, package URLs, image URLs, and license URLs.
- Do not embed real license keys, private package licenses, or production credentials.
- Use the corrected API names from this skill: `Nve*`, `nveGetEffectContextInstance()`, `NveEffectContext`, `NveARSceneRenderer`, `NveEffectInstance`, `NveAssetPackageManager`.
- If a user asks for zero-code demo generation, patch or scaffold runnable files, run `node scripts/validate-demo.mjs <demo-path>` when possible, then run the generated project's type check/build if dependencies are available.

## Source Basis

This skill is self-contained. It includes condensed task references, full copied source materials under `references/source`, and a React/Vite demo template under `assets/react-vite-demo-template`. It should keep working even if the project-level `sdk` folder is later removed.
