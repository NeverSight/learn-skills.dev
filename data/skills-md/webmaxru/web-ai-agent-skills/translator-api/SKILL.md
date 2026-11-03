---
name: translator-api
description: Implements and debugs browser Translator API integrations in JavaScript or TypeScript web apps. Use when adding Translator support checks, language-pair availability flows, model download UX, session creation, translate() or translateStreaming() calls, input-usage measurement, or permissions-policy handling for on-device translation. Don't use for server-side translation SDKs, cloud translation services, or generic multilingual content pipelines.
license: MIT
metadata:
  author: webmaxru
  version: "1.3"
---

# Translator API

## Procedures

**Step 1: Identify the browser integration surface**
1. Inspect the workspace for browser entry points, text-input flows, localization UI, and any existing AI abstraction layer.
2. Execute `node scripts/find-translator-targets.mjs .` to inventory likely frontend files and existing Translator API markers when a Node runtime is available.
3. If a Node runtime is unavailable, inspect the nearest `package.json`, HTML entry point, and framework bootstrap files manually to identify the browser app boundary.
4. If the workspace contains multiple frontend apps, prefer the app that contains the active route, translation UI, or user-requested feature surface.
5. If the inventory still leaves multiple plausible frontend targets, stop and ask which app should receive the Translator API integration.
6. If the project is not a browser web app, stop and explain that this skill does not apply.

**Step 2: Confirm API viability and choose the integration shape**
1. Read `references/translator-reference.md` before writing code.
2. Read `references/examples.md` when the feature needs a session wrapper, download-progress UI, streaming output, cancellation, or cleanup shape.
3. Read `references/compatibility.md` when preview flags, browser channels, iframe rules, or environment constraints matter.
4. Read `references/troubleshooting.md` when support checks, session creation, translation, or cleanup fail.
5. Verify that the feature runs in a secure `Window` context.
6. Verify that the current frame is allowed to use the `translator` permissions-policy feature.
7. Choose the narrowest session shape that matches the task:
   - bare `Translator.create()` for a fixed language pair and full-result translation
   - monitored `create()` when the UI must surface model download progress
   - `translateStreaming()` when the UI should reveal translated output incrementally
   - `measureInputUsage()` when quota or input-size budgeting affects the flow
8. If the feature must run in a worker, on the server, or through a cloud translation contract, stop and explain the platform mismatch.
9. If the project uses TypeScript, add or preserve narrow typings for the Translator API surface used by the feature.

**Step 3: Implement a guarded translator session**
1. Read `assets/translator-session.template.ts` and adapt it to the framework, state model, and file layout in the workspace.
2. Centralize support checks around `globalThis.isSecureContext`, `Translator`, and the same `sourceLanguage` and `targetLanguage` shape the feature will use at runtime.
3. Gate session creation behind `Translator.availability()` using the same language pair that will be passed to `Translator.create()`.
4. Treat `availability()` as a capability check, not a guarantee that creation will succeed without download time, policy approval, or user activation.
5. Create sessions only after user activation when creation may trigger a model download.
6. Use the `monitor` option during `create()` when the product needs download progress.
7. Use `AbortController` for cancelable `create()`, `translate()`, `translateStreaming()`, or `measureInputUsage()` calls, and call `destroy()` when the session is no longer needed.
8. Recreate the session instead of mutating `sourceLanguage` or `targetLanguage` after creation; session options are fixed per instance.
9. If the feature lives in a cross-origin iframe, require explicit delegation through `allow="translator"`.

**Step 4: Wire UX and fallback behavior**
1. Surface distinct states for missing APIs, insecure contexts, blocked frames, unsupported language pairs, downloadable or downloading models, ready sessions, in-flight translation, and aborted work.
2. Keep a non-AI fallback for unsupported browsers, blocked frames, or environments that do not meet current preview requirements.
3. Preserve the source and target language pair explicitly in product state instead of inferring them from translated output.
4. Use `translate()` when downstream logic needs the full result before continuing, and use `translateStreaming()` when the UI should reveal translated text incrementally.
5. Use `measureInputUsage()` when large inputs can exceed session quota.
6. Treat same-language or best-fit identity translations as valid outcomes instead of forcing a fallback when the translated result matches the input.
7. Chunk or queue long-running product workflows deliberately; translation requests are not a substitute for general summarization, writing, or chat tasks.
8. Do not route generic cloud translation, document localization pipelines, or server-side batch translation through this API; switch to the approved service or runtime when the task is not browser on-device translation.

**Step 5: Validate behavior**
1. Execute `node scripts/find-translator-targets.mjs .` to confirm that the intended app boundary and Translator API markers still resolve to the edited integration surface.
2. Verify secure-context checks, `Translator` feature detection, and `availability()` behavior before debugging deeper runtime failures.
3. Test at least one `create()` plus `translate()` flow with representative user text for the target language pair.
4. If the feature exposes streaming, test `translateStreaming()` separately and confirm partial output stops cleanly on abort.
5. If the feature depends on quota budgeting, verify `measureInputUsage()` behavior before sending large input.
6. Confirm that cancellation rejects with the expected abort reason and that destroyed sessions are not reused.
7. If the target environment depends on preview browser flags or channel-specific behavior, confirm the required browser state from `references/compatibility.md` before treating failures as application bugs.
8. Run the workspace build, typecheck, or tests after editing.

## Error Handling
* If `Translator` is missing, keep a non-AI fallback and confirm secure-context, browser, channel, and flag requirements before changing product logic.
* If `availability()` returns `downloadable` or `downloading`, require user-driven session creation before promising that translation is ready.
* If `create()` throws `NotAllowedError`, check permissions-policy constraints, missing user activation for downloads, browser policy restrictions, or user rejection.
* If `create()` throws `OperationError`, treat model initialization as failed and retry only after checking browser state, required flags, and download readiness.
* If a translation call throws `QuotaExceededError`, reduce the input size or measure usage before retrying.
* If a translation call throws `NotReadableError` or `UnknownError`, surface a visible fallback instead of retrying blindly with the same input.
* If the feature must run in a worker or server context, stop and explain that the Translator API is a window-only browser API.