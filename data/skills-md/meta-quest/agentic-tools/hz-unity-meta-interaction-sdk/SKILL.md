---
name: hz-unity-meta-interaction-sdk
license: Apache-2.0
description: Meta XR Interaction SDK (com.meta.xr.sdk.interaction.ovr) in Unity. Use when adding ANY interaction to a Meta VR or Horizon OS scene - grab (hand, distance, ray, touch), poke, teleport/locomotion, gaze, interactable UI canvases - when making an object grabbable, adding interactors to hands or controllers, creating an interaction rig, or baking interaction into a prefab or a scene whose rig loads elsewhere (dynamically, DontDestroyOnLoad, additively). Use the OVR backend unless the user explicitly asks for cross-platform. Covers QuickActionsAPI and OVRQuickActionsAPI as the default way to wire interactions, running them via unity-cli, an Editor script, or MCP, installation, and the undocumented behavior that source-reading or a Play-mode run is otherwise needed to discover.
---

# Meta XR Interaction SDK (com.meta.xr.sdk.interaction.ovr)

## Use ISDK for interaction on Meta VR

The Core SDK (`com.meta.xr.sdk.core`) gives you the headset - camera rig, tracking, `OVRManager`.
It does not give you interaction. **ISDK is the interaction layer.** Don't hand-roll grabbing on
`OVRInput`, raycasts, or trigger colliders: ISDK already models hover/select state, pose
conforming, throw velocity, and interactor arbitration, and a hand-rolled version drifts from
platform behavior.

| Target | What to do |
|---|---|
| Meta VR / Horizon OS, or platform not stated | **OVR backend** (`com.meta.xr.sdk.interaction.ovr`) - the rest of this skill |
| Cross-platform, still on ISDK | UnityXR backend (Essentials + Unity XR Hands). Same model, different entry points - look them up, don't assume the OVR ones |
| Cross-platform **not** using ISDK | **Stop. This skill does not apply.** |

**Do not infer cross-platform intent** - default to OVR, switch only if the user says so, and
state which backend you used.

> **Set interactions up through the Quick Actions APIs, not by hand.** `OVRQuickActionsAPI`
> builds the rig; `QuickActionsAPI` makes objects interactive and equips interactors. Reach for
> manual prefab assembly only when a Quick Action cannot express what you need - and say so.

Meta's own guidance too: Quick Actions are "the fastest and recommended way" to add the rig
([docs](https://developers.meta.com/horizon/documentation/unity/unity-isdk-add-comprehensive-interaction-rig)).

## Quick start

```csharp
using Oculus.Interaction.Editor.QuickActions;         // QuickActionsAPI
using Oculus.Interaction.OVR.Editor.QuickActions;     // OVRQuickActionsAPI

// Delete the default Main Camera first - ISDK brings its own camera rig.

// 1. Rig: comprehensive interaction rig (hands + controllers + every interactor + visuals),
//    plus an OVRCameraRig if the scene has none.
OVRQuickActionsAPI.AddOVRInteractionRig();

// 2. Interactable: adds Rigidbody + Grabbable + a HandGrab/Grab interactable child.
var cube = GameObject.CreatePrimitive(PrimitiveType.Cube);
cube.transform.localScale = Vector3.one * 0.1f;
cube.transform.position = new Vector3(0f, 1.0f, 0.4f);   // in reach at a FloorLevel origin
QuickActionsAPI.AddGrabInteraction(cube);
```

Every method returns the **root GameObjects it created** - not the target you passed. Use that
to find what to configure or rename.

## Which call for which interaction

| Feature | Call |
|---|---|
| Interaction rig (+ camera rig) | `OVRQuickActionsAPI.AddOVRInteractionRig()` |
| Hand grab (near) | `QuickActionsAPI.AddGrabInteraction(go)` |
| Distance grab | `QuickActionsAPI.AddDistanceGrabInteraction(go, mode)` |
| Ray grab | `QuickActionsAPI.AddRayGrabInteraction(go)` |
| Gaze grab (eye tracking) | `QuickActionsAPI.AddGazeInteraction(go)` |
| Teleport surface | `QuickActionsAPI.AddTeleportInteraction(go, surfaceType)` |
| Poke / ray / gaze a Canvas | `QuickActionsAPI.AddPokeCanvasInteraction(go)` · `AddRayCanvasInteraction` · `AddGazeCanvasInteraction` |
| Interactors on a hand / controller | `QuickActionsAPI.AddHandInteractors(go, types)` · `AddControllerInteractors` · `AddControllerHandInteractors` |
| Touch hand grab, plain poke, plain ray | *no API - menu item only* |

**Every one of these takes a `GameObject target`** - never a component. Passing a `Canvas` to a
Canvas call is a compile error (`cannot convert from 'UnityEngine.Canvas' to 'UnityEngine.GameObject'`);
pass `canvas.gameObject` or the result of `GameObject.Find`. Likewise the interactor calls take the
GameObject that carries the `Hand`/`Controller`, not the component.

Signatures, parameters, and what each call builds:
[quick-actions-api.md](references/quick-actions-api.md) ·
[ovr-quick-actions-api.md](references/ovr-quick-actions-api.md).
Per-feature Meta docs: [documentation.md](references/documentation.md).

The interactor calls are only for a hand-built rig - `AddOVRInteractionRig()` already ships every
interactor, so after it they are redundant.

## When the rig isn't in your scene

An interaction needs a matching **interactor at runtime**, in the loaded scene set. It does not
need the rig present at author time.

| Quick Action | Needs a rig in the scene? |
|---|---|
| Interactables (grab, distance grab, ray grab, gaze, canvas, teleport) | **No** - everything they require is on the target itself |
| Interactors (`AddHandInteractors` and siblings) | **Yes** - `target` must carry the `Hand` / `Controller` |
| `AddOVRInteractionRig()` | It *creates* the rig |

So all of these are fine: the rig is instantiated at runtime, lives in a bootstrap scene under
`DontDestroyOnLoad`, arrives from an additive scene, or you are authoring a **prefab**.

**The consequence.** An interactable Quick Action also tops up the rig with matching interactors
*when it finds one* - silently skipped when there is no rig. Nothing breaks, but nobody added
those interactors, so the rig that eventually loads must already carry the types your interactable
needs. A `DistanceHandGrabInteractable` with no `DistanceHandGrabInteractor` on the runtime rig is
inert and logs nothing. When you author against an absent rig, say which interactor types the
runtime rig must provide.

### Baking interaction into a prefab

Verified: run the interactable call on a scene instance, then save. The wiring is self-contained -
the interactable's `_pointableElement` resolves to the `Grabbable` inside the prefab, with no
leaked scene reference.

```csharp
var go = GameObject.CreatePrimitive(PrimitiveType.Cube);
QuickActionsAPI.AddGrabInteraction(go);                       // no rig needed
PrefabUtility.SaveAsPrefabAsset(go, "Assets/Grabbable.prefab", out bool ok);
Object.DestroyImmediate(go);
```

- **Don't verify a prefab asset via `interactable.PointableElement`** - it is assigned in
  `Awake()`, which never runs on an asset, so it is *always* null there even when the prefab is
  correct. Read the serialized field:
  `new SerializedObject(interactable).FindProperty("_pointableElement").objectReferenceValue`.
- **Canvas calls:** pass `fixPointableCanvasModule: false` when the `PointableCanvasModule` comes
  from a prefab or an unloaded additive scene, or you get a second one in the open scene.

## Running the calls - both APIs are Editor-only

They live in Editor assemblies and **cannot** run from a `MonoBehaviour` or anything in a build.

**1. Live Editor via `unity-cli`** (preferred when one is open - drive it instead of editing
scene YAML):

```bash
unity status --format json          # look for state "ready"
unity command run_script --project-path <proj> --file /abs/path/DoTheThing.cs --entry MyClass.Run --format json
```

Use `run_script` with a `.cs` file rather than `eval`: shell quoting mangles C# char literals
(`' '`), the file is re-runnable, it can live outside `Assets/`, and `--timeout_ms` awaits async
entry points.

**2. A project Editor script** under `Assets/Editor/` (or an Editor-only asmdef referencing
`Oculus.Interaction.Editor` and `Oculus.Interaction.OVR.Editor`), exposed as a `[MenuItem]` -
when a human should be able to repeat the setup.

**3. MCP**, if a Unity MCP server is connected. Its harness constraints (no `using
System.Reflection;`, no `BindingFlags` overloads, package Editor assemblies not referenced) apply
there and **not** to `unity-cli`'s Roslyn `run_script` — see
[unity-mcp-fallback.md](references/unity-mcp-fallback.md).

Finish by saving the scene (`EditorSceneManager.MarkSceneDirty` + `SaveScene`), then verify.

## Installing

**Install `com.meta.xr.sdk.interaction.ovr`** - it pulls in Essentials and the Core SDK. Check
`Packages/manifest.json` first; if it is listed, do not re-add. Installing only
`com.meta.xr.sdk.interaction` is the classic misinstall: interaction model, no OVR binding, no
rig, no `OVRQuickActionsAPI`.

```csharp
using UnityEditor.PackageManager;
var request = Client.Add("com.meta.xr.sdk.interaction.ovr");   // async - poll request.IsCompleted
```

Or against a live Editor: `unity command package_add --identifier com.meta.xr.sdk.interaction.ovr --confirm true --wait true`.

**A successful add forces a recompile and domain reload** - never install a package and use its
API in the same script. Details: [installation.md](references/installation.md).

## Finding the truth: source first, docs second

**Don't answer ISDK questions from memory.** The installed package is authoritative for
*behavior*; Meta's docs for *intent* and design guidance.

Search for the API sources by filename pattern - this works regardless of install
form (registry cache, embedded, or local):

```
**/com.meta.xr.sdk.interaction*/Editor/QuickActions/Scripts/QuickActionsAPI.cs
**/com.meta.xr.sdk.interaction.ovr*/Editor/QuickActions/Scripts/OVRQuickActionsAPI.cs
```

Then use the resolved package roots for all subsequent lookups.

Inside Unity, `AssetDatabase` paths work regardless of install form:
`Packages/com.meta.xr.sdk.interaction.ovr/Runtime/Prefabs/...`.

For docs, query `metavr` - `vr_docs_search(query, scope="unity")` for the `doc_path`, then
`vr_docs_get_page`, and `vr_api_search(query, engine="unity")` for signatures. **Never
hand-construct a doc URL**; the namespace varies. Curated map:
[documentation.md](references/documentation.md).

**The two APIs are the supported entry points; the machinery under them is not public API.** If
you are reaching for reflection to invoke a wizard, you have probably missed a method - re-read
the two files first. The same actions exist under the **`GameObject > Interaction SDK`** menu as
blocking wizard windows; open one when you want to see what a call will create.

## What the docs don't tell you

Each of these is visible only from the source or from a runtime failure.

- **You get the optional components too.** A call is equivalent to clicking **Fix All** *and*
  **Add All** in the wizard. `AddDistanceGrabInteraction` additionally creates a root
  `ISDK_SnapZone (<target>)` that pulls the object back after it goes untouched - delete it to
  opt out. Detail: [quick-actions-api.md](references/quick-actions-api.md).
- **Grab calls make the Rigidbody kinematic** (`useGravity = false; isKinematic = true`). Objects
  float where you put them; that is intended.
- **Created names come from the wizard** - `ISDK_HandGrabInteraction`, `ISDK_SnapZone (...)`.
  Rename afterwards if it matters; components track by reference, so renaming is safe.
- **Interactor calls target the `Hand`/`Controller` object itself.** `Hand`-derived components on
  child objects log `Could not execute HandInteractorWizard`; filter with
  `.Where(h => h.GetType() == typeof(Hand))`.
- **Enum names don't match the components they select.** `DistanceGrabMode` vs. the Movement
  Provider in the scene vs. Meta's doc label are three vocabularies - never guess the mapping.
- **The wizards expose settings the APIs don't.** If you need one that isn't a parameter, use the
  menu item or post-process the result. Smooth Locomotion on the rig is the common case.
- **Building Blocks are another route to the same result**, not a better one. Prefer the APIs: no
  block-tracking components, no project-setup side pass, readable names.
- **No API means no API.** If there is no method for what you want, use the menu item or build it
  from components - don't reflect into the wizard.

## Always verify in Play mode

ISDK asserts its wiring in `Start()`, so a scene that looks correct in the Inspector can still
throw. Edit-time component checks are **not** sufficient.

1. Clear the console, enter Play mode, read the console, exit.
2. Zero errors **and zero exceptions** is the bar. Every `AssertionException` names the exact
   component and field - treat it as a real defect.
3. `[MetaXRFeature]: ErrorFormFactorUnavailable xrGetSystem` only means no headset/XRSIM is
   attached; OpenXR teardown warnings are benign.
4. Some failures are silent - see [verification.md](references/verification.md).
5. After Play mode is clean, confirm on a real headset: build an APK, `metavr app install <apk>`, then stream `metavr adb logcat --follow --tag Unity` while exercising each interaction.

## References

- [quick-actions-api.md](references/quick-actions-api.md) - signatures, enums, what each call builds
- [ovr-quick-actions-api.md](references/ovr-quick-actions-api.md) - the rig call and the rig it creates
- [interaction-model.md](references/interaction-model.md) - interactor/interactable model, rig anatomy, placement
- [installation.md](references/installation.md) - install paths, dependency chain, assemblies
- [verification.md](references/verification.md) - Play-mode loop, assertion table, silent failures
- [documentation.md](references/documentation.md) - curated Meta doc map and lookup recipe
- [unity-mcp-fallback.md](references/unity-mcp-fallback.md) - running the calls over Unity MCP instead of `unity-cli`

## Related skills

- **`hz-unity-meta-core-sdk`** - camera rig, `OVRManager`, tracking origin, hand tracking support,
  Project Setup Tool, AndroidManifest
- **`unity-cli`** - drive a live Editor
- **`hz-xr-simulator-install-and-configure`** / **`hz-vr-debug`** - run and debug beyond Play mode
