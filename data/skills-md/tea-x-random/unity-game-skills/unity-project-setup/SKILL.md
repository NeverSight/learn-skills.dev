---
name: unity-project-setup
description: "Establish a reproducible Unity 6 project foundation before the codebase grows. Use for new repos, Unity .gitignore, .gitattributes/Git LFS, Force Text serialization, Visible Meta Files, Smart Merge/UnityYAMLMerge, committed .meta files, per-game Assets layout, asmdef Core/Game/Editor/Tests architecture, UPM manifest.json, packages-lock.json, OpenUPM/scoped registries, version pinning, bundle/build numbers, environment config, secrets, API keys, CI/CD, headless tests/builds, fastlane and iOS upload. Pair with unity-gameplay-systems for architecture, unity-qa-release for builds/signing, unity-mcp-bridge for Editor automation, and monetization/analytics skills for per-environment SDK configuration."
---

# Unity Project Setup

## Purpose

Lay down the repo and build foundation a team can grow on: correct Unity-aware source control, a predictable folder + assembly layout, reproducible package management, a versioning scheme, a secrets stance, and CI/CD wiring — so the first playable (and everything after) lands in a structure that doesn't fight merges, leak keys, or rot into 20-minute compiles.

## Use When

Starting a new Unity repo (or rescuing one set up naively); fixing Git pain (huge repo, scene merge conflicts, broken references after pull); designing assembly architecture; pinning packages for reproducibility; deciding a version/build-number scheme; removing committed secrets; or standing up CI that builds + tests + hands iOS signing to fastlane.

This is the **production-engineering / DevOps hygiene** discipline. It is distinct from `unity-gameplay-systems` (which scaffolds the first PLAYABLE) — this skill owns the repo/build foundation that the playable lives inside.

## Doctrine (set this up BEFORE the project grows)

1. **Configure source control correctly once, on day zero.** Unity's binary assets and `.meta` sidecar files make naive Git painful — a wrong `.gitignore` or a missing LFS rule is far cheaper to fix before there are 50 commits and 4 GB of textures than after.
2. **Always commit `.meta` files; never commit `Library/`.** A `.meta` is the asset's identity (GUID + import settings). A missing or orphaned meta silently breaks every reference to that asset. `Library/` is a regenerable cache — committing it bloats the repo and conflicts constantly.
3. **Reproducible builds beat "works on my machine."** Pin package versions, commit `packages-lock.json`, and keep one headless build entry point so CI and a teammate's clone produce the same artifact.
4. **Secrets never touch the repo.** Ad unit IDs, analytics keys, signing creds, App Store API keys → environment variables / per-env config / CI secrets, with the secret files `.gitignore`d. This reinforces the repo's own security stance (see `unity-ios-secure-backend`, `unity-monetization`).
5. **Architecture is enforced by assemblies, not by good intentions.** An engine-free Core in its own asmdef gives fast compiles, real unit tests, and dependency boundaries the compiler actually checks.

## Workflow (new repo, in order)

1. **Source control first.** Add the Unity `.gitignore` and `.gitattributes` (+ Git LFS) **before** the first asset commit. Copy both from `references/gitignore-and-lfs.md`.
2. **Editor settings.** Set Asset Serialization = **Force Text**, Version Control = **Visible Meta Files**, configure **Smart Merge** (UnityYAMLMerge). Commit `ProjectSettings/`.
3. **Folder structure.** Create `Assets/<Game>/` with the standard subfolders; keep generated/third-party separate. Provision the reserved art-pipeline paths with `.gitkeep` files (below).
4. **Assembly architecture.** Lay down Core / Game / Editor / Tests asmdefs (engine-free Core first).
5. **Package management.** Pin versions in `manifest.json`, add OpenUPM scoped registries as needed, commit `packages-lock.json`.
6. **Versioning.** Decide bundleVersion + build-number scheme; add the build-number bump (hand iOS signing/upload to `unity-qa-release` fastlane).
7. **Secrets/config.** Add per-env config + a `.gitignore`d secrets file; document the env vars CI must inject.
8. **CI/CD.** Wire build-on-push (Unity CLI/MCP) → run tests → fastlane signing/upload. Keep `BuildScript.PerformiOSBuild` as the single Editor-driven entry point CI calls.

## Source control essentials

Unity Git pain is almost entirely preventable with five settings. Get them right once.

- **`.gitignore` (Unity-specific).** Ignore the regenerable/local stuff: `Library/`, `Temp/`, `Obj/` / `obj/`, `Build/` & `Builds/`, `Logs/`, `UserSettings/`, `.vs/`, `.idea/`, `*.csproj` / `*.sln` (regenerated), crash/burst artifacts. **Never** ignore `Assets/`, `ProjectSettings/`, `Packages/manifest.json`, or `*.meta`. Full copyable file in `references/gitignore-and-lfs.md`.
- **`.gitattributes` + Git LFS for binaries.** Track large binary asset types (textures `.png/.psd/.tga/.exr`, models `.fbx/.blend`, audio `.wav/.mp3/.ogg`, video `.mp4`, fonts, `.unitypackage`) with **Git LFS** so the repo stays clone-able and diffs stay sane. Run `git lfs install` once per machine; commit `.gitattributes` before adding the binaries (LFS only captures files matched at commit time — pre-existing blobs must be migrated with `git lfs migrate`). Patterns in `references/gitignore-and-lfs.md`.
- **Asset Serialization = Force Text.** `Edit ▸ Project Settings ▸ Editor ▸ Asset Serialization ▸ Mode = Force Text`. Makes scenes/prefabs/assets YAML so they diff and merge (and so Smart Merge can run). Binary serialization is unmergeable.
- **Version Control = Visible Meta Files.** `Edit ▸ Project Settings ▸ Editor ▸ Version Control ▸ Mode = Visible Meta Files`. Ensures every asset has a tracked `.meta` (its GUID + import settings). **Always commit `.meta` files** — a missing or orphaned meta reassigns GUIDs and silently breaks references; an extra meta for a deleted asset is noise but harmless. Treat "added/deleted an asset without its meta" as a broken commit.
- **Smart Merge (UnityYAMLMerge).** Register Unity's `UnityYAMLMerge` tool as the mergetool for `.unity` / `.prefab` so structural scene/prefab conflicts merge semantically instead of corrupting YAML. Config in `references/gitignore-and-lfs.md`. Even so: **minimize concurrent edits to the same scene** — split work into prefabs and additive scenes so two people rarely touch one `.unity`.

## Project / folder structure

Keep one game-owned root so third-party imports and generated output never intermingle with your source:

```text
Assets/
  <Game>/                 # everything you author lives under one namespace-like root
    Scripts/              # C# (mirrors the asmdef layout: Core/, Game/, Editor/, Tests/)
    Art/                  # Textures, Sprites, Materials, Models  (LFS-tracked)
      _ArtDirection/      # RESERVED: art-spec.yaml, style-guide.md, palettes/, references/, sheets/
      Approved/           # RESERVED: registry.yaml + <asset_id>/ (contract + approved art + QA reports)
      Source/             # RESERVED: raw generated staging — SourceImages/, TripoRaw/, CleanupQueue/, QA/
    Audio/                # Music, SFX  (LFS-tracked)
    Prefabs/
    Scenes/               # Boot, Game, plus additive feature scenes
    UI/                   # UI Toolkit (UXML/USS) or uGUI prefabs
    Data/                 # ScriptableObjects, config assets
    Tests/                # EditMode + PlayMode (Tests asmdefs)
    Settings/             # URP assets, Input Actions, etc.
  Plugins/                # native plugins (.framework, .a, iOS bridge)
  ThirdParty/             # imported .unitypackage / vendor SDKs — kept OUT of <Game>/
Packages/                 # manifest.json + packages-lock.json (committed)
ProjectSettings/          # committed
Build/                    # gitignored output (Build/iOS/ is the Xcode export)
```

Rationale: a single `Assets/<Game>/` root makes "what we wrote" vs "what we imported" obvious, keeps reorg cheap (one move, not a scatter), and lets `.gitignore`/LFS rules target predictable paths.

### Reserved art-pipeline paths (provision at setup)

The art pipeline (`unity-art-direction` → `unity-asset-pipeline`) resumes across sessions only if its artifact paths are deterministic — `unity-game-director`'s detect probe looks for them. Provision them empty at setup, with `.gitkeep` files so the dirs survive git:

```bash
mkdir -p "Assets/<Game>/Art/_ArtDirection"/{palettes,references,sheets} \
         "Assets/<Game>/Art/Approved" \
         "Assets/<Game>/Art/Source"/{SourceImages,TripoRaw,CleanupQueue,QA}
find "Assets/<Game>/Art" -type d -empty -exec touch {}/.gitkeep \;
```

- Canonical artifact paths: art-spec `Assets/<Game>/Art/_ArtDirection/art-spec.yaml`; master palette `_ArtDirection/palettes/master-palette.png`; canon sheets `_ArtDirection/sheets/<char_id>_canon.png` (skeleton templates `*.skeleton.json` beside them); registry `Assets/<Game>/Art/Approved/registry.yaml`.
- This nests the whole art tree under the single `Assets/<Game>/` root — the one-root doctrine holds; never invent a new root for art output.
- **Legacy reserved aliases:** older skill docs use `Assets/GameArt/` and `Assets/Art/` roots. Discovery/resume tooling MUST probe them too, but NEW artifacts are written to the canonical layout only. Unifying legacy references is follow-up polish, not a setup blocker.

## Assembly definition (asmdef) architecture

Default Unity dumps all scripts into one implicit `Assembly-CSharp` — every edit recompiles everything and nothing enforces boundaries. Split into explicit assemblies. (Cross-ref `unity-gameplay-systems`, which builds the first playable inside exactly this layout.)

| Assembly | Contents | Key setting |
|---|---|---|
| `<Game>.Core` | Pure C# game logic — rules, state, generators, scoring, puzzle/solver. **No `UnityEngine` where possible.** | `"noEngineReferences": true` (or "Override References" + no UnityEngine) → fast, deterministic, EditMode-testable in milliseconds |
| `<Game>` | MonoBehaviours, scene glue, views; references `Core` | Runtime platforms |
| `<Game>.Editor` | `[MenuItem]`, importers, **`BuildScript.PerformiOSBuild`** | `"includePlatforms": ["Editor"]` so it never ships in the player |
| `<Game>.Tests` (+ `.Tests.Editor`) | EditMode/PlayMode tests; references `Core` (and `Game` for PlayMode) | References `UnityEngine.TestRunner` / `nunit` |

Why it matters:

- **Faster compiles & shorter domain reloads.** Editing a leaf assembly recompiles only it and its dependents — not the whole game. (Each compile triggers the ~5s MCP domain-reload drop; fewer recompiles = fewer drops, see `unity-mcp-bridge`.)
- **Enforced dependencies.** `Core` cannot reference `Game` or `UnityEngine`, so logic can't accidentally couple to scene objects. The compiler is the guardrail.
- **Real, fast unit tests.** Engine-free `Core` runs in EditMode with no scene, no Play Mode, no frame loop — generators/solvers/scoring get tested in milliseconds in CI.
- **Editor code never ships.** Build tooling in an Editor-platform asmdef is excluded from the player automatically.

Reference asmdefs by name; keep cross-references minimal (fewer edges = shorter reloads). Add the Input System / TMP / test assemblies explicitly where used.

## Package management (reproducible)

- **`Packages/manifest.json` is the source of truth.** Declare every dependency with a **pinned exact version** (`"com.unity.inputsystem": "1.11.2"`), not a floating range — floating versions make two clones resolve differently.
- **Commit `Packages/packages-lock.json`.** It records the fully-resolved dependency graph (including transitive deps and registry sources) so every clone and CI run resolves identically. Treat a lockfile change in a PR as a real, reviewable diff.
- **OpenUPM scoped registries** for packages not in Unity's registry (e.g. Google Mobile Ads — see `unity-monetization`). Add a `scopedRegistries` entry pointing at `https://package.openupm.com` with the exact scopes, so only the named packages come from OpenUPM:

```json
"scopedRegistries": [
  {
    "name": "OpenUPM",
    "url": "https://package.openupm.com",
    "scopes": ["com.google", "com.google.external-dependency-manager"]
  }
]
```

- **Vendor SDKs that ship as `.unitypackage` / `.framework`** (not UPM) go under `Assets/ThirdParty/` (or `Plugins/`) and are **LFS-tracked**, kept out of `Assets/<Game>/`. Note the version in a README so an upgrade is intentional.
- **Don't hand-edit `packages-lock.json`.** Let Unity (or `manage_packages` via MCP) resolve; commit the result.
- **Unity 6000.5: NEVER add `com.unity.textmeshpro`.** The editor's own PackageManager manifest marks it deprecated (`removeOnProjectUpgrade: true`) — TMP now ships **inside** `com.unity.ugui` 2.5.0 (built-in package; asmdef name is still `Unity.TextMeshPro`, TMP essentials `.unitypackage` lives at `Packages/com.unity.ugui/Package Resources/`). A pinned standalone TMP package can throw the project into Safe Mode; remove it from `manifest.json` and reference `Unity.TextMeshPro` as usual.
- **Fresh projects default `activeInputHandler: 0` (legacy-only) — Input System code is silently dead** (actions never fire, no error). Set it to 2 (Both) or 1 (Input System) in `ProjectSettings/ProjectSettings.asset` BEFORE first launch: `sed -i '' 's/activeInputHandler: 0/activeInputHandler: 2/' ProjectSettings/ProjectSettings.asset` (safe scalar text edit), plus a belt-and-braces Editor check via `new SerializedObject(Unsupported.GetSerializedAssetInterfaceSingleton("PlayerSettings")).FindProperty("activeInputHandler")`. The value takes effect on the next Editor launch — each batch run is a fresh launch, so run 1 sets it and test runs inherit it.

## Versioning & build numbers

- **`bundleVersion`** (`PlayerSettings.bundleVersion`, shown to users, e.g. `1.4.0`) is the marketing/semver version. Bump it deliberately per release; it lives in `ProjectSettings/ProjectSettings.asset` (committed).
- **Build number** (iOS `buildNumber`) must be **monotonically increasing and unique per upload** — App Store Connect rejects a duplicate. Drive it from CI (e.g. the CI run number, or `git rev-list --count HEAD`) rather than a hand-edited field, so two builds never collide.
- **Automate the bump in the headless build path.** Set `PlayerSettings.iOS.buildNumber` inside `BuildScript.PerformiOSBuild` (or a pre-build step) from an env var / CI counter. Keep the *scheme* here; hand the **iOS signing + TestFlight upload** to `unity-qa-release` fastlane, which also has a `MYGAME_BUILD_OVERRIDE` floor for collisions while Apple is still processing a prior build.

```csharp
// inside BuildScript (Editor asmdef) — scheme only; signing/upload = unity-qa-release fastlane
var ci = System.Environment.GetEnvironmentVariable("BUILD_NUMBER");
if (!string.IsNullOrEmpty(ci)) PlayerSettings.iOS.buildNumber = ci;
```

## Secrets & per-environment config (NEVER commit secrets)

API keys, ad unit IDs, analytics SDK keys, signing certs, and App Store Connect API keys are **secrets**. They must never be committed — a key in Git history is leaked even after you "delete" it.

- **`.gitignore` the secret files.** Keep a committed template (`secrets.example.json`, `*.env.example`) and an ignored real file (`secrets.json`, `.env`). Add both the file and the pattern to `.gitignore`.
- **Inject via environment variables / CI secrets at build time.** CI reads `MYGAME_ASC_KEY_ID`, `ADMOB_APP_ID`, analytics keys, etc. from the CI provider's secret store and writes the per-env config (or sets them in the signing step). Never echo them into logs.
- **Per-environment config (dev / staging / prod).** Use a `ScriptableObject` or JSON config selected by build flag/env so test ad unit IDs and dev analytics keys never ship to production — and prod keys never sit on a dev laptop. (Ad SDK keys: `unity-monetization`. Analytics/remote-config keys: `unity-analytics-liveops`. Game Center / App Attest creds: `unity-ios-secure-backend`.)
- **Rotate on leak.** If a secret lands in a commit, rotate the key — scrubbing history is not enough once it's been pushed.

## CI/CD basics

A minimal pipeline, build-on-push:

1. **Checkout (with LFS).** `git lfs pull` so binary assets are real files, not pointers.
2. **Unity build via CLI/MCP.** Headless batchmode calling the single entry point:
   `Unity -batchmode -quit -projectPath . -executeMethod BuildScript.PerformiOSBuild -logFile -` (or drive it through `unity-mcp-bridge` / `manage_build`). **Keep `BuildScript.PerformiOSBuild` as the one Editor-driven entry point** so the same method is callable from CI, MCP, and a local run. Note: the Unity iOS "build" is just the fast Xcode export (~10-20s); the IL2CPP→native compile happens in the Xcode/fastlane step (detail in `unity-qa-release`).
3. **Run tests.** EditMode (fast, engine-free `Core`) + PlayMode via the Unity Test Framework — fail the pipeline on red. (`unity-qa-release` owns the test recipes.)
4. **iOS signing + upload via fastlane.** Hand the generated `Build/iOS/` Xcode project to `unity-qa-release` fastlane: ASC API-key auth, `pod install` on the `.xcworkspace`, archive, upload to TestFlight. Secrets come from CI's secret store (above).

Keep secrets out of CI logs, cache `Library/` between runs to speed builds, and treat a green pipeline as proof only when it produced a real artifact (`.ipa`) — same evidence bar as `unity-qa-release`.

## Where this sits

- **`unity-gameplay-systems`** builds the first playable; it lives **inside** the folder + asmdef structure this skill establishes (engine-free `Core`, `Game`, `Editor`, `Tests`).
- **`unity-qa-release`** owns the iOS build/test execution, fastlane signing, and TestFlight upload; this skill provides the reproducible foundation and the single `BuildScript.PerformiOSBuild` entry point it calls.
- **`unity-mcp-bridge`** is the Editor automation layer (apply settings, add packages, drive the headless build); this skill defines *what* to set, the bridge executes it.
- **`unity-monetization` / `unity-analytics-liveops`** supply the per-environment SDK keys/secrets this skill keeps out of the repo and injects via CI.
- **`unity-ios-secure-backend`** shares the secrets stance (signing/identity creds, server keys) — same "never in the repo" rule.
- **`unity-art-direction` / `unity-asset-pipeline`** own the art-spec SSOT (`_ArtDirection/art-spec.yaml`) and the approved-asset registry (`Approved/registry.yaml`) that live in the reserved `Assets/<Game>/Art/{_ArtDirection,Approved,Source}` paths this skill provisions — deterministic paths are what make cross-session art resume (the `unity-game-director` detect probe) work.

## Common failure modes

- Committing `Library/` (huge repo, constant conflicts) or ignoring `.meta` files (broken references on every pull).
- Binary serialization left on → scenes/prefabs unmergeable, every merge a corruption risk.
- Adding LFS rules *after* the binaries are already committed → the big blobs are still in history (needs `git lfs migrate`).
- One implicit `Assembly-CSharp` → 5–20 min full recompiles, no testable logic, no enforced boundaries.
- Floating package versions / uncommitted `packages-lock.json` → "works on my machine," CI resolves a different graph.
- A secret (ad ID, ASC key, signing cert) committed once → leaked permanently; must rotate.
- Duplicate iOS build number → App Store Connect rejects the upload.

## Field notes & lessons

- Source control is the highest-leverage day-zero decision: a wrong `.gitignore`/missing-LFS choice costs hours to unwind once history exists. Add `.gitignore` + `.gitattributes` + `git lfs install` **before** the first asset commit; LFS only captures files matched at commit time.
- Always-commit `.meta` + Force Text + Visible Meta Files are the three settings that prevent ~90% of Unity Git grief (broken references, unmergeable scenes). Set them first, commit `ProjectSettings/`.
- An engine-free `Core` asmdef (`noEngineReferences: true`) is what makes both fast EditMode unit tests and short domain reloads possible — it's the single most useful architectural boundary on a casual game.
- Pin exact package versions and commit `packages-lock.json`; treat lockfile diffs as reviewable. Floating ranges are the quiet cause of "builds differently in CI."
- Keep ONE headless build entry point (`BuildScript.PerformiOSBuild`) in an Editor-platform asmdef, callable from CI / MCP / local — versioning bump lives here, signing/upload hands off to `unity-qa-release` fastlane.
- Secrets via env/CI only, with a committed `.example` template and the real file `.gitignore`d; rotate immediately if one is ever pushed.
