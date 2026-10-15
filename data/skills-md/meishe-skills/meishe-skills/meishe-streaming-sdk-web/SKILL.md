---
name: meishe-streaming-sdk-web
description: Integrate, explain, review, audit, and troubleshoot Meishe Streaming SDK Web editing APIs in React/Vite, Vue/Vite, or framework-neutral browser projects. Use for SDK/runtime loading, timelines, LiveWindow, tracks, clips, captions, stickers, effects, transitions, keyframes, templates, asset packages, media FS, playback, persistence, compatibility checks, and runtime failures. 用于在 Web 项目中接入、使用、审查或排查美摄流媒体编辑 SDK 及其编辑、媒体与运行时流程。
---

# Meishe Streaming SDK Web

Use the bundled API knowledge baseline 3.16.0. Respond in the user's language; preserve identifiers and code. Follow the applicable steps in order.

## 1. Choose the mode

Use **answer mode** for explanations, API guidance, reviews, audits, or any request that does not authorize edits. Inspect and explain available evidence, but never provision dependencies, install files, or modify the project. Missing runtime inputs do not block verified static guidance; label the affected runtime conclusions as pending.

Use **implementation mode** only when the user requests code changes. Inspect project conventions, patch the smallest relevant boundary, and validate in proportion to the requested feature.

## 2. Route by feature

Use [feature-map.json](references/feature-map.json) or `--list-features` to select canonical domain IDs before inspection. Use `--list-recipes` and a bundled `--recipe` when the requested workflow matches exactly; a recipe expands the complete domain and SDK-symbol set but never supplies user decisions, approvals, provenance, or external inputs. For one-domain work, inspect and read that domain only. For a cross-domain recipe, inspect all directly participating domains in one scan with `--features` or the matching preset, choose one primary domain for implementation, apply the union of returned gates, and read each corresponding guide without loading unrelated domains. Read [integration-core.md](references/integration-core.md) only for runtime integration or initialization work, the relevant framework guide for implementation work, and [sample-index.md](references/sample-index.md) only when selecting low-freedom source material.

## 3. Inspect the target

For an existing project, run before proposing code:

```text
node <skill>/scripts/inspect-target-project.mjs --project <project> --feature <domain> [--runtime-source <customer-sdk-directory> | --target-sdk <NvStreamingSdk.js> [--target-sdk-provenance configured-runtime-response|customer-confirmed-delivery]] [--required-symbols <api-a>,<api-b>] [--authorization-mode required|skip] [--media-strategy meishe-transcoded-m3u8|weblocal|mixed]
node <skill>/scripts/inspect-target-project.mjs --project <project> --features <domain-a>,<domain-b> [--runtime-source <customer-sdk-directory> | --target-sdk <NvStreamingSdk.js> [--target-sdk-provenance configured-runtime-response|customer-confirmed-delivery]] [--required-symbols <api-a>,<api-b>] [--authorization-mode required|skip] [--media-strategy meishe-transcoded-m3u8|weblocal|mixed]
node <skill>/scripts/inspect-target-project.mjs --project <project> --recipe <recipe-id> [--runtime-source <customer-sdk-directory>] [--authorization-mode required|skip] [--media-strategy meishe-transcoded-m3u8|weblocal|mixed]
node <skill>/scripts/inspect-target-project.mjs --list-features
node <skill>/scripts/inspect-target-project.mjs --list-recipes
```

For a first integration, run inspection as a read-only preflight. Do not install, copy, generate, or edit anything. Determine the complete recipe-specific SDK symbol set and statically compare it from the supplied delivery, installed runtime, or read-only `--target-sdk` before requesting prerequisite mutations. An independent `--target-sdk` never proves what a configured CDN/runtime URL delivers: leave `target-sdk-runtime-provenance` blocked until the file is the captured configured response or the customer explicitly confirms it is the deployed delivery, then pass the matching provenance attestation.

Before asking the first gate-specific question, present one consolidated discovery report. Disclose every currently known gate and every conditional follow-on that an unresolved choice can activate; do not show only the decisions needed for the next inspection pass. At minimum cover API compatibility or its pending decision-dependent comparison, the exact SDK source/destination and conflict policy, unconditional and conditional dependency installs, authorization alternatives, every media-strategy alternative and its validation input, development/preview COOP/COEP plus the production-host requirement, runtime `getSdkVersion()`, and browser/render/playback/cleanup validations. Label each item as one of: disclosed now, decision requested now, approval requested only after static checks, external input required, or runtime validation pending. Disclosure does not authorize a mutation. Decisions, approval requests, mutations, and runtime checks may occur in later stages, but staging must never hide an already known or conditionally applicable gate. After a decision changes the active recipe, report only newly resolved or newly activated deltas without retracting the original consolidated report.

Explain the reason, affected files or commands, risks, and alternatives for each prerequisite mutation. Wait for explicit user confirmation in the conversation before each first-use prerequisite mutation. Tool, sandbox, workspace, or auto-approval never satisfies this confirmation. Apply only confirmed items and rerun inspection. `bootstrapReady` (mirrored by `prerequisitesReady`) permits only the approved SDK bootstrap needed for runtime version verification; `featureInputsReady` separately reports policy and media inputs. Do not create feature objects or implement the requested recipe until `featureImplementationReady` is true.

Treat detected project state as authoritative for the static integration decision. Reuse an existing structurally complete local runtime, configured local/CDN runtime flow, declared `meishewasmloader`, actual `verifySdkLicenseFile` flow, and complete SDK initialization without asking the user to reconfirm them. Static evidence never proves browser behavior, authorization success, production headers, or JavaScript/WASM provenance; preserve every `validationPending` item for runtime reporting.

Use the inspector's `uiDesign` evidence together with the request. Follow a user-provided UI reference first. Otherwise reuse a clearly established project design system. Only when neither exists and implementation needs UI for validation, read [default-editor-ui.md](references/default-editor-ui.md), the UI group in [sample-index.md](references/sample-index.md), and the directly relevant workflow rules in [editor-workflow-patterns.md](references/editor-workflow-patterns.md). Adapt the single `DefaultEditorUi` validation sample: it directly renders navigation, feature/material, preview, inspector, and bottom Timeline regions. Do not create or offer alternate default-layout variants merely because the requested feature is narrow. Do not reconstruct markup, geometry, ruler, or track density from prose. Show only implemented features within the five regions. Treat `ambiguous` UI evidence as a reason to inspect the cited files, not as permission to replace them.

Pass `--authorization-mode` only after the user explicitly chooses `required` or accepts the watermark/capability impact of `skip`; never select it on the user's behalf. On a first media integration, pass `--media-strategy meishe-transcoded-m3u8|weblocal|mixed` only after the user chooses. Recommend Meishe-transcoded m3u8 for general production use, while allowing `mixed` when M3U8 and WebLocal must coexist. Persist an explicit application-level strategy/source discriminator so later tasks can reuse that decision; a bare `.m3u8` path is only a candidate and must not stand in for it. An explicit single-strategy choice scopes this integration's dependencies and validations without deleting or disabling the other existing project path. After every active strategy's required input is available, pass strategy-matching `--media-input-kind`: `meishe-m3u8` or `backend-contract` for transcoding, `local-file` for WebLocal, and one kind for each path when mixed. Do not pass orphaned or inactive-path input kinds; inspect `unusedInputKinds` and resolve `media-input-consistency`. Decision, provenance, and input flags are caller attestations, not evidence independently observed by the inspector. The inspector never accesses the network, installs, copies, or edits anything.

For tasks with a target project or target SDK, read the Skill version and API baseline from [sdk-baseline.json](references/sdk-baseline.json) and show one concise compatibility banner after target detection at the start of each logical task. Before runtime initialization, state the 3.16.0 baseline, label `@version` only as `staticApiHeaderVersion`, say the actual runtime version is pending, and complete the recipe-specific static surface check. After the user-approved WASM context is ready and before feature objects are created, call `context.getSdkVersion()`, format its three components, and rerun inspection with `--runtime-sdk-version <x.y.z>` and the same complete `--required-symbols <a,b>`. The inspector treats the supplied runtime value as a caller attestation and rejects it when no installed or configured runtime exists. Use that runtime value—not `@version`—for exact/older/newer posture. A static/runtime mismatch proves only that the header metadata does not describe the observed runtime; record a non-blocking header metadata warning and do not infer stale cache or delivery causes from the mismatch alone. Block only when a required API is missing/changed or requested runtime behavior fails. Skill-distribution audits without a customer target do not need this banner. Treat clarifications and follow-ups for the same objective as one logical task and do not repeat an unchanged banner. Start a new pass for a distinct objective, changed target/runtime, or evidence that changes posture.

| Need | Guide |
| --- | --- |
| React/Vite lifecycle | [framework-react-vite.md](references/framework-react-vite.md) |
| Simple React/Vite WebLocal video preview recipe | [simple-weblocal-preview.md](references/simple-weblocal-preview.md) |
| Vue/Vite lifecycle | [framework-vue-vite.md](references/framework-vue-vite.md) |
| Generic browser/custom elements | [framework-generic.md](references/framework-generic.md) |
| Context, authorization, cleanup | [engine-lifecycle.md](references/engine-lifecycle.md) |
| SDK FS, Meishe-transcoded M3U8, and WebLocal media | [media-fs-and-weblocal.md](references/media-fs-and-weblocal.md) |
| Timeline, tracks, clips | [timeline-track-clip.md](references/timeline-track-clip.md) |
| LiveWindow, playback, coordinates | [monitor-playback-coordinate.md](references/monitor-playback-coordinate.md) |
| Video/image editing | [video-editing.md](references/video-editing.md) |
| Audio editing | [audio-editing.md](references/audio-editing.md) |
| Captions | [captions.md](references/captions.md) |
| Stickers | [stickers.md](references/stickers.md) |
| Effects and transitions | [effects-transitions.md](references/effects-transitions.md) |
| Keyframes and animation | [keyframes-and-animation.md](references/keyframes-and-animation.md) |
| Templates/nested timelines | [templates-and-nested-timelines.md](references/templates-and-nested-timelines.md) |
| Particles, AR, masks, detection | [advanced-effects.md](references/advanced-effects.md) |
| Asset packages | [asset-package-management.md](references/asset-package-management.md) |
| Metadata, thumbnails, waveform | [metadata-thumbnail-waveform.md](references/metadata-thumbnail-waveform.md) |
| Project/XML persistence | [project-xml-and-persistence.md](references/project-xml-and-persistence.md) |
| Compatibility/failures | [compatibility-troubleshooting.md](references/compatibility-troubleshooting.md) |
| Default validation editor UI | [default-editor-ui.md](references/default-editor-ui.md) |
| Editor application workflow | [editor-workflow-patterns.md](references/editor-workflow-patterns.md) |

## 4. Apply scoped dependency gates

Use the states and evidence phases in [terminology.md](references/terminology.md). Apply only gates required by the selected mode and requested recipe.

- In answer mode, never provision. Continue with static evidence and report missing runtime-critical inputs as limitations.
- In implementation mode, reuse `available` evidence. Treat every `approval-required`, every `decision-required`, every `runtime-required`, every `missing-external`, and every critical `unknown` as a hard barrier to dependent implementation. Use `bootstrapReady` only for the approved minimal runtime bootstrap; it does not authorize feature work. Never mutate a first-use prerequisite during preflight. `requiresUserApproval` must be satisfied by an explicit conversational answer and cannot be inferred from implementation mode or satisfied by automatic tool approval.
- Treat `requiresApproval` as the backward-compatible mirror of `requiresUserApproval`; an `approval-required` condition must never report either field as false.
- Never make users reconfirm a prerequisite merely because they are adding another feature. Revisit it only when evidence conflicts or a concrete runtime failure points to it.

Treat SDK JavaScript/WASM, authorization data, media, fonts, models, and material packages as external. Never bundle, invent, substitute, or copy them merely because a candidate exists in the workspace. Identify the exact candidate and destination and obtain explicit user approval first. For caption recipes, the disclosed font fallback in [captions.md](references/captions.md) is the only always-listed external fallback. Non-empty entries in [test-resources.json](references/test-resources.json) are explicit temporary validation approvals only: never bundle them or promote them to production defaults. An empty manifest means no public temporary test resource is approved. Classify every third-party import before adding it.

When an approved temporary test resource is actually needed, check only that resource with `check-test-resources.mjs --id <resource-id>` before use. Do not probe unrelated resources. Omit `--id` only for an explicit full test-resource audit.

## 5. Query the API surface

Query the generated manifest instead of loading the full SDK source:

```text
node <skill>/scripts/query-api.mjs --symbol NvsTimeline.addCaption --bilingual
node <skill>/scripts/query-api.mjs --domain stickers --query translation
```

Use [api-manifest.json](references/api-manifest.json) for structured lookup and direct-file fallback, and [feature-map.json](references/feature-map.json) for compact domain routing metadata. Treat [NvStreamingSdk.js](references/NvStreamingSdk.js) as query-only evidence: never copy, import, serve, deploy, or execute it in a customer project. Treat [sdk.d.ts](assets/types/sdk.d.ts) as a compile-time asset only after exact 3.16.0 runtime compatibility is established.

As soon as a target SDK file is available, statically compare the complete set of APIs actually used by the selected recipe, including creation, mutation, callback, query, rollback, and cleanup calls. Omit the runtime version during first preflight, then rerun the same comparison with the observed version after bootstrap:

```text
node <skill>/scripts/compare-sdk-capabilities.mjs --target-sdk <target-sdk> --symbols <api-a>,<api-b> --json
node <skill>/scripts/compare-sdk-capabilities.mjs --target-sdk <target-sdk> --runtime-sdk-version <observed-x.y.z> --symbols <api-a>,<api-b> --json
```

The comparator uses the bundled API manifest directly when the normalized target hash exactly matches the 3.16.0 baseline. For other files it uses a formatting-independent structural scan. Treat `missing` as proven only when the symbol's owning class was completely parsed; otherwise require `unparseable` and request the official unminified delivery or matching documentation.

Use `--feature <domain>` only for a domain-wide compatibility audit or when the required symbol set cannot be determined safely. Never analyze a domain-wide result merely to validate a known narrow recipe.

`surface-present` proves only a symbol and its observable parameter count. It does not prove runtime behavior, return types, enum values, callbacks, or JavaScript/WASM pairing. `unparseable` means the target layout is unsupported and never proves an API is missing; request an unminified official SDK file or target documentation. For newer targets, use only verified baseline symbols and do not answer newer APIs without target documentation. For older or unknown targets, explain every changed, missing, unknown, or unparseable result. Never upgrade or replace the customer runtime silently.

Only compose a multi-API recipe when bundled JSDoc, supplied documentation, or a routed sample supports the combination. Otherwise describe the individual APIs and label the recipe unverified.

## 6. Implement safely

Use [engine-lifecycle.md](references/engine-lifecycle.md) as the single authority for initialization order, authorization, project-session ownership, callback ownership, and teardown. Keep browser globals and SDK enums outside SSR/module evaluation, use microseconds unless the queried API says otherwise, and check SDK return values and asynchronous callbacks.

Treat each visible add, delete, Trim, Split, move, Reset all, undo, redo, or completed property gesture as one logical mutation transaction. Read and retain `getTimelineCurrentPosition(timeline)` once at transaction start; after mutation and duration synchronization, clamp and seek that retained position. A slider may apply throttled preview writes during the gesture, but it must create one history entry and one final retained-position refresh. Do not maintain a second application-owned playhead or read the restoration position only after mutation.

Use [media-fs-and-weblocal.md](references/media-fs-and-weblocal.md) as the authority for SDK FS roots and media ownership. Apply the routed domain guide's resource and mutation rules.

In particular, use [asset-package-management.md](references/asset-package-management.md) for package callback ownership and [captions.md](references/captions.md) for the non-blocking optional-font policy.

Batch related browser checks in one headed browser and one successfully initialized SDK context when isolation is safe. Give each check separately owned Timeline, LiveWindow, callbacks, SDK FS paths, and object URLs, and clean them up before the next check. Reload the page or restart SDK initialization after bootstrap/authorization failure, leaked shared state, or any result whose isolation cannot be proven. Do not repeatedly restart a healthy SDK session for unrelated assertions.

Remove unused sample code and adapt imports/configuration to the target. Never add Redux, EventBus, UI libraries, backend calls, internal paths, credentials, fixed IDs, or test/production coupling unless the request explicitly requires them.

## 7. Validate and report

In implementation mode, run the smallest existing project check that covers the changed boundary. Do not automatically run full type-check, build, lint, and all tests together. Escalate to a full project check only when project instructions require it, no narrower check exists, or the change affects shared types, build/runtime configuration, SDK initialization, persistence, global editor state, or multiple feature domains. Confirm required dependencies are already available before invoking a command that may install them. If runtime prerequisites are unavailable, report only affected browser validation as `pending-user-runtime`; never describe it as passed.

For an answer-mode handoff, report the evidence, conclusion, limitations, and missing inputs only. For an implementation-mode handoff, report the baseline, static header clue, observed runtime SDK version and posture separately; list every explicit prerequisite approval, prerequisites applied, missing gates, selected media strategy and supplied or absent validation inputs, pending runtime validations, files changed, static validations, unresolved external inputs, and remaining browser checks. Never call a static `@version` match an exact runtime match.

When the default validation editor UI is used, keep the routed UI sample's structural constants and follow the scoped checks in [default-editor-ui.md](references/default-editor-ui.md). Do not exercise or report unrelated editor features merely because the default editor is present. Run full-editor regression only when the user requests it or the change affects shared layout, routing, selection, history, Timeline infrastructure, LiveWindow lifecycle, or several feature domains.

## 8. Maintain the Skill

Preserve the Skill's existing version metadata during maintenance. Do not change `skillVersion` or any other Skill/distribution version marker merely because content changed; update versions only when the user explicitly requests a version change.

Do not run the following Skill-distribution audit for target-project integration. When auditing or updating this Skill itself, run:

```text
node <skill>/scripts/validate-skill.mjs --require-typescript [--tsc <typescript/bin/tsc>]
```

This distribution audit intentionally reports target-project runtime validation as not run. Add `--features <domain-a>,<domain-b>` only for an explicit capability-runtime audit.
