---
name: hz-unity-sdk-upgrade
license: Apache-2.0
description: Upgrades Unity projects between Meta XR SDK versions for Meta VR and Horizon OS. Use when moving from Oculus Integration or older com.meta.xr packages, resolving post-upgrade compile errors, or validating runtime behavior. Grounds migration decisions in current metavr documentation results and records coverage gaps instead of relying on static summaries. Do not use for Unreal, native Android, Spatial SDK, or WebXR upgrades.
allowed-tools: Bash(metavr:*)
---

# Meta XR Unity SDK Upgrade

Upgrade the project as an evidence-driven migration. Package resolution and a clean compile are checkpoints, not proof that the app still works.

Optimize for the shortest verified path. In a time-bounded session, finish the package/provider transition, remove duplicate SDK code, migrate every known producer and consumer, and obtain a clean compile before optional cleanup or broader platform validation. Do not spend the remaining budget polishing a compile-clean project setting while a known legacy consumer or vendored SDK file remains.

For Unreal, native Android or Spatial SDK, WebXR or Immersive Web SDK (IWSDK),
and general cross-platform upgrades, use
[`hz-api-upgrade`](../hz-api-upgrade/SKILL.md).

## Required workflow

1. Read [the Unity upgrade runbook](references/unity-upgrade-runbook.md). Do a bounded, shallow inventory of the Unity version, render pipeline, XR provider, Meta packages, vendored `Assets/Oculus` content, assembly definitions, and affected scenes/prefabs. Record paths and legacy symbols without reading every large serialized asset or constructing a complete GUID map. Create one checklist of affected producers, consumers, serialized assets, settings, and tests; update it instead of repeating discovery or launching duplicate inventory subtasks.
2. Establish the source and target SDK versions from package or SDK-family markers. Treat the Meta XR package version, the bundled native OVRPlugin version reported through the managed `OVRPlugin` API, Unity editor version, and XR provider as separate axes; do not infer one from another. If either SDK version is ambiguous, report the evidence and label the value as inferred.
3. Query current documentation with `metavr` before choosing replacements. Start with one full-range query and one query per active high-impact axis, then fetch the most relevant authoritative results. Search individual published releases only when package metadata or a changelog shows that an intermediate release matters. Once the relevant official guide and exact target API signatures for the next migration slice are established, implement that slice; do not keep probing adjacent APIs. Return to search only for a new error or unresolved checklist item.
4. Treat missing or irrelevant results as a documentation-coverage gap. Record the query and result in the upgrade report; do not fill the gap from memory or claim that `metavr` found guidance it did not return.
5. Update the package topology before application code. Remove duplicate vendored SDK content, keep related Meta packages and any required bridge/adaptor package compatible with the target release, update the XR provider deliberately, and resolve assembly-definition references. Verify both package declarations and serialized loader/provider settings; installing an OpenXR package does not enable its loader. Run and await any required project-setup tool within this slice, then re-scan for vendored SDK code because imports or setup automation can recreate files. Run the first post-change compile before inspecting package sources or deeply migrating scenes and prefabs; let its diagnostics determine what to inspect next.
6. Run the critical compile loop below after the package/provider slice and after every coherent migration slice. Do not batch unrelated migration work on top of a failed compile.
7. Migrate producers and consumers together. Before optional cleanup or platform checks, enumerate the concrete consumer files and mark each migrated. Search scenes, prefabs, serialized fields, custom loaders, editor tooling, and tests—not only `.cs` call sites. Do not delete or skip an affected consumer merely to obtain a clean compile.
8. If the project uses `OVRSceneManager`, `OVRSceneRoom`, `OVRSceneAnchor`, or custom Scene API loaders, read [the MRUK migration best practices](references/mruk-migration.md) before editing and run its completion checklist before the final compile.
9. Treat an accompanying Unity-major-version, XR-provider, or Input System change as a separate migration axis. Check serialized provider settings per build target, required OpenXR feature groups and interaction profiles, Active Input Handling, `Unity.InputSystem` assembly references, Android entry point, permissions, Addressables/Localization, render-pipeline settings, color space, and Android minimum SDK when applicable. Verify version-sensitive details through live docs and installed package APIs.
10. Validate in layers: package resolution, script compilation, edit/play-mode tests, Android build, then headset behavior for permissions, scene loading, input, rendering, and lifecycle. For compilation, prefer an installed, documented Unity editor-control CLI or bridge when it can safely drive the project's already-open Editor. Otherwise use the matching Unity Editor in batch mode only after confirming that the same project is not open elsewhere. Never start a second Editor on the same project or terminate an unrelated Unity process. Preserve exact commands and results in the upgrade report.
11. Finish only when the requested validation layers pass or are explicitly recorded as failed or unverified with the blocking layer, evidence, and a concrete next command.

## Critical execution and compile loop

Treat compilation as a blocking feedback loop, not end-of-task validation:

1. Before editing, capture a fresh baseline compile when the environment supports it and record any pre-existing errors.
2. Complete the package and XR-provider checklist, wait for package resolution and import, then compile immediately. Fix or revert every new package, assembly, and API error before migrating another subsystem.
3. Migrate one behavioral slice end to end—for Scene API migration, the producer plus every inventoried consumer—then compile again. Rewire that slice's serialized assets and settings, then compile once more.
4. On failure, inspect the first actionable error, verify the installed target API or search that exact error, make the smallest coherent fix, and rerun. Do not start unrelated work while the compile is red.
5. For time-boxed work, reserve roughly the final third for compile/fix cycles because Unity package imports and domain reloads are slow. During that period, every action must directly close a known migration item: edit, compile, inspect the first current error, or verify a required producer/consumer/package invariant. Start no new inventory, duplicate subtask, broad documentation search, optional project-wide fix pass, or adjacent API exploration. Never launch a command whose maximum runtime exceeds the remaining budget. If time expires while red, report the compile failure and remaining errors instead of claiming completion.
6. Require a fresh clean compile after the last code, package, or serialized-file edit; an earlier clean result does not validate later changes.
7. If a compile runs asynchronously, stay in the current task and poll that same process to a terminal result. Do not schedule a reminder, defer the check, or return while validation is pending. Read the fresh log and fix current errors before continuing; if the environment cannot keep the process attached, report compilation as unverified rather than complete.

## Critical completion gate

Before reporting completion:

- Verify the exact package set, including bridge/adaptor packages required by APIs the project still uses; for example, projects combining Interaction SDK with OVR APIs may require `com.meta.xr.sdk.interaction.ovr`. Confirm the intended XR provider is present and enabled, its legacy replacement is removed or deconfigured, and duplicate vendored SDK code is gone.
- Re-scan game code, assembly definitions, scenes, prefabs, and project settings for every affected legacy producer and consumer.
- Preserve affected consumer scripts and their `.meta` GUIDs and migrate them in place. A deprecated consumer that still compiles is unfinished unless the requested scope explicitly retains it; do not delete one merely because it appears unused without checking code and serialized references.
- If Scene API moved to MRUK, confirm the loader reads `AnchorLabels`, handles `PlaneRect` and `VolumeBounds`, and initializes `SceneSettings` when MRUK is created at runtime. If a custom loader maps classifications to prefabs, confirm that it selects its global-mesh representation before any shared null-prefab guard and routes `GlobalMesh` to the application's rendering or collision components. Confirm all consumers, including debug/exporter code, use the migrated contract.
- Confirm serialized prefab mappings and MRUK/provider settings were rewired; compiling C# cannot prove this.
- Distinguish package resolution, script compilation, player build, Horizon Link testing, and standalone-device testing in the report. Never promote an earlier layer into evidence for a later one.

## Documentation commands

Use JSON output when preserving search results:

```bash
metavr docs search --category UNITY --format json "Meta XR Unity SDK release notes <source> <target>"
metavr docs search --category UNITY --format json "<deprecated symbol> migration"
metavr docs search --category UNITY --format json "<package name> <compiler or runtime error>"
metavr docs fetch --format json "<URL returned by search>"
```

`metavr docs search` is semantic search, not a complete version-to-version diff. A weak version query is a signal to broaden the search by package and symbol, not permission to invent a breaking-change list.

If `metavr` is unavailable, do not invent search results. Use current official
Developer Center pages and the installed target package's changelog, public
API, and samples, and report that live CLI retrieval was not run.

## Guardrails

- Treat bundled or cached breaking-change summaries as leads, not authority; verify against current official documentation and the installed target packages.
- Do not prescribe incremental upgrades by default. Choose direct or staged migration from package constraints and evidence.
- Do not delete project assets, regenerate serialized files, or change scenes wholesale without first identifying their consumers.
- Do not equate deprecated with removed. Decide whether to migrate now based on target support and the requested scope.
- Do not report success from compilation alone. Unity serialization, Android permissions, and device-only paths can still fail.

## References

- [Unity upgrade runbook](references/unity-upgrade-runbook.md)
- [Scene API to MRUK migration best practices](references/mruk-migration.md)
