---
name: unity-qa-release
description: "Verify and release casual iOS games built in Unity. Use for playtest QA, Play Mode tests, EditMode tests, Unity Test Framework, device resolution checks, safe-area UI checks, iOS build, Xcode project generation, IL2CPP, ASTC texture compression, App Store, TestFlight (TestFlight upload), privacy manifest (PrivacyInfo.xcprivacy), ATT prompt, app icon, launch screen, orientation lock, deployment target, managed stripping / link.xml, release readiness, ship it, and release risk reports. Also covers automating the manual macOS step with fastlane: App Store Connect API key auth, code signing, sigh, provisioning profiles, build number, CocoaPods, pod install, xcworkspace, EDM4U. Drives the Editor through unity-mcp-bridge (manage_build, run_tests, get_test_job)."
---

# Unity QA Release

Prove the game works as a player encounters it, then generate a shippable iOS build with its risks named. The deliverable is an **Xcode project** plus a release risk report — not a signed `.ipa`, and never a "shipped" claim without evidence.

## Doctrine (these override convenience)

1. **Verify with real evidence.** Tests, screenshots, build output. Never say "done", "works", "passes", "built", "signed", or "shipped" without an artifact: green test results, a screenshot of the running scene, or actual build/status output. A clean `read_console` is not optional.
2. **Lean gates, but gate release.** Don't stack a prompt at every micro-step, but release IS a gate. Do not produce a release report until QA + tests + a build-or-blocker exist.
3. **Edit/build through MCP, not files.** All Editor work — running, testing, building — goes through `unity-mcp-bridge` (CoplayDev unity-mcp). Scenes/prefabs/`.asset` are GUID-linked YAML; never hand-edit.
4. **Unity 6 build pipeline differs from default knowledge.** The model's built-in knowledge is ~Unity 2022.3. Build Profiles (the `profile` param on `manage_build`) need **Unity 6+**. If unsure about a `manage_build` action/property or a player setting API, verify via MCP (`unity_reflect` / `unity_docs`, `docs` group) before acting — don't write from memory.

Confirm the Editor is reachable first: read `mcpforunity://editor/state` and proceed only when `ready_for_tools==true`, `is_compiling==false`, `is_domain_reload_pending==false`. If MCP/Editor is down, say so and author the steps for manual run — do not claim QA/build happened.

## QA gates before release

Load `references/checklists/playtest-qa.md` and walk it. Gate on:

- **Core loop reachable** — input → objective → win/lose → restart, all by touch, no dead ends.
- **Console clean** — `read_console(types=["error","warning"])` shows no errors and no warnings of note.
- **Runs at target resolution(s)** — playable and readable on the phone aspect ratios you ship (see Device/resolution QA).
- **Input/touch works** — taps, drags, swipes register; no reliance on keyboard/mouse-only paths.
- **Win / lose / restart** — each path reachable and recoverable.
- **No soft-locks** — no state the player can enter and not leave (stuck menus, frozen input, dead win screen).
- **Performance acceptable** — stable frame rate, no thermal/memory spikes. Profiling lives in `unity-debug-profiler` (`profiling` group, `manage_profiler`); link to it rather than re-deriving here.

A QA gate is "passed" only with a screenshot or test backing it.

## Automated tests (Unity Test Framework)

Enable the group, then author and run. Load `references/test-recipes.md` for full recipes and an example test.

```text
manage_tools(action="enable_group", group="testing")   # exposes run_tests, get_test_job
```

- Author **EditMode** tests (pure logic — fast, no scene) and **PlayMode** tests (scene/coroutine/physics behavior) using NUnit + the Unity Test Framework. Put them in asmdef-scoped `Tests` folders referencing the test framework.
- Run async, then **poll** — `run_tests` returns a job:

```text
run_tests(mode="PlayMode")          # or mode="EditMode"
-> job_id
get_test_job(job_id, wait_timeout=120)   # poll until status finished; re-call if still running
```

`run_tests` is not synchronous — always collect the `job_id` and poll `get_test_job` until it reports finished, then read pass/fail counts. Expect a domain reload (~5s drop) on first run after a compile.

**Two run_tests gotchas:** (1) it fails with *"Cannot start a test run while the Editor is in or entering Play Mode"* if a manual Play session is still live — always `manage_editor(action="stop")` before `run_tests`. (2) PlayMode init can flake with *"tests did not start within timeout"* — it's transient; just retry with a larger `init_timeout`, don't treat the first timeout as a real failure.

**What to test in a casual game:** scoring (points add/multiply, high-score persists), spawning (objects spawn at the right cadence/positions, pooling reuses), win/lose conditions (triggers fire at the right thresholds), save/load (PlayerPrefs/serialized state round-trips, survives a reload).

**PlayMode test isolation (this bit hard — 4 tests passed singly but failed together).** A runtime
bootstrap that creates ROOT objects (Camera, Canvas, EventSystem) must **parent them under its own
GameObject** — otherwise `Object.Destroy(appGO)` leaves the roots orphaned, they accumulate across
tests, and `FindAnyObjectByType<T>()` returns a STALE instance from a prior test. Two more rules: if the
app auto-resumes from `PlayerPrefs` in `Awake`, a previous test's save makes the next test resume the
wrong board (its `while(Board==null)` wait exits instantly on the resumed board) — **clear the save in
both `[SetUp]` AND `[TearDown]`**, and **`DestroyImmediate` every app instance in `[TearDown]`** (Destroy
is deferred, so the next test starts before cleanup runs). Symptom signature: "expected 6 but was 7",
"no conflict", cascading multi-test failures that vanish when each test is run alone.

## Headless batchmode verification (no GUI, no MCP)

When an Editor is installed but you can't drive a live one (no MCP, headless/CI, or the user isn't
at the keyboard), verify directly from the CLI — this gives a real compile + test gate without a
human. **The Editor must be CLOSED** (it locks the project); check `pgrep` first.

```bash
UNITY="/Applications/Unity/Hub/Editor/<version>/Unity.app/Contents/MacOS/Unity"
# Compile + run EditMode tests (do NOT add -quit with -runTests):
"$UNITY" -batchmode -nographics -projectPath <proj> \
  -runTests -testPlatform EditMode -testResults results.xml -logFile verify.log
# Build the scene / run any editor entrypoint:
"$UNITY" -batchmode -nographics -quit -projectPath <proj> \
  -executeMethod Namespace.Class.Method -logFile build.log
```

Read the results, don't guess: `grep -cE ': error CS' verify.log` must be **0**; parse
`result="Passed" ... failed="0"` from results.xml; a successful `-executeMethod` logs your own
success line and **no** `field '…' not found` warnings (those mean a `SerializedObject` wire missed).
Ignore benign `[Licensing::…] Error: … handshake` / `Access token is unavailable` / `debugger-agent:
Unable to listen` lines — licensing reconnects and resolves right after. Batchmode needs a license:
Personal/Team licenses activated via Hub login work headlessly. First run re-resolves + downloads
packages (slow); background it and poll for the process to exit. **Never report "compiles" or
"tests pass" without the actual 0-error grep and the passed/failed counts.**

## Device / resolution QA

Casual iOS games run **portrait** on a range of phone aspect ratios. Test the spread, not one size:

- Tall/notched (~19.5:9, modern iPhone), classic (~16:9), and a shorter one (older/SE).
- `manage_editor(action="play")` → exercise the loop → `manage_scene(action="screenshot", include_image=true)` at each aspect → `manage_editor(action="stop")`.
- Verify **safe area / notch**: HUD and buttons inside the safe area, nothing clipped by the notch or home indicator, text fits, touch targets reachable. Compare screenshots across aspect ratios. UI fixes route to `unity-ui-designer`.

**Editor throttling is not a device bug.** An **unfocused** Unity Editor throttles Play Mode to a few FPS, so coroutine-driven animations look stuttery/slow in MCP screenshots and a short one-shot can be only partway through a cascade across several captures. This is Editor background-throttling, **not** a real frame-rate or device problem — note it as such; don't "fix" a non-bug (or, for proof, freeze it per the recipe below rather than chasing the FPS).

**Capturing App Store screenshots at an EXACT pixel size.** Register a **Fixed Resolution** Game View size (e.g. 1242×2688) and capture with `UnityEngine.ScreenCapture.CaptureScreenshot(path)` — it writes at the Game View's target render size. **CRITICAL: do NOT use `manage_camera` screenshot with a camera specified** — a camera render EXCLUDES Screen-Space-Overlay UI canvases (you get only the camera background). `ScreenCapture.CaptureScreenshot` captures the full framebuffer incl. Overlay UI. Verify output dimensions with `sips -g pixelWidth -g pixelHeight <png>`. Caveat (see Editor throttling above): an unfocused/throttled Editor doesn't repaint the Game View, so `CaptureScreenshot` can write a **stale frame** — on-device capture is often more reliable for store assets, and a leaderboard/score shot looks better with real data anyway.

**Capturing transient VFX for proof.** A one-shot effect shorter than the MCP round-trip (e.g. a <2.5s confetti burst) is gone before `manage_camera`/`manage_scene screenshot` fires. Reliable recipe: immediately after spawning the effect, set `UnityEditor.EditorApplication.isPaused = true` (via `execute_code`) — coroutine-driven animation freezes at its first-frame layout, so the screenshot captures it; restore `isPaused = false` afterward. The spawned objects' initial positions must already be on-screen (see the confetti pitfall in `unity-gameplay-systems`) or the frozen frame shows nothing.

## iOS build pipeline (the centerpiece)

All via `manage_build`. Full ordered recipe + manual steps in `references/ios-build-pipeline.md`. Ordered sequence:

```text
1. manage_build(action="platform", target="ios")                 # switch active platform
2. manage_build(action="settings", property="bundle_id",   value="com.you.game")
   manage_build(action="settings", property="product_name", value="My Game")
   manage_build(action="settings", property="company_name", value="You")
   manage_build(action="settings", property="version",      value="1.0.0")
3. set scripting_backend="il2cpp"        # iOS REQUIRES IL2CPP — Mono is not allowed
4. manage_build(action="scenes", ...)    # add/order the scenes in the build (first = launch)
5. manage_build(action="build", target="ios", output_path="Builds/iOS/MyGame")
6. manage_build(action="status")         # poll until the build finishes
```

**Critical facts:**

- **Detect the iOS module BEFORE building.** Check `UnityEditor.BuildPipeline.IsBuildTargetSupported(BuildTargetGroup.iOS, BuildTarget.iOS)` (via `execute_code`) first — it returns false when the iOS Build Support module isn't installed, and without it `UnityEditor.iOS.Xcode.PBXProject` won't even compile, so a headless Xcode export fails mysteriously. If false, surface it as a **user-blocked step** (install via Unity Hub → Add Modules), don't just let the build error out.
- **Output is an Xcode project FOLDER, not an `.ipa`.** `manage_build` produces a Unity-generated Xcode project. Building, signing, archiving, and exporting the `.ipa` happen **outside MCP** on macOS.
- **Build Profiles need Unity 6+.** The `profile` param on `manage_build` only exists on Unity 6.x. On older versions, drive platform/settings/scenes directly as above; do not pass `profile`.
- **Setting iOS player settings via `execute_code`.** CodeDom is C#6 — use fully-qualified names. Backend: `PlayerSettings.SetScriptingBackend(UnityEditor.Build.NamedBuildTarget.iOS, ScriptingImplementation.IL2CPP)`. Portrait lock: `PlayerSettings.defaultInterfaceOrientation = UIOrientation.Portrait` plus the four `allowedAutorotateTo*` (portrait true, rest false) — setting one alone doesn't lock it. Bundle id: `SetApplicationIdentifier(BuildTargetGroup.iOS, id)`. Manual signing: `PlayerSettings.iOS.appleEnableAutomaticSigning = false`. **Read each value back** to confirm — note `PlayerSettings.iOS.targetOSVersionString` is **clamped up to the editor's floor** (e.g. "13.0" came back "15.0" on 6000.5), which is expected, not a failure.
- **A brand-new editor type can resolve to NULL during domain reload.** After a code change, `System.Type.GetType("Ns.Type,Asm")` may return null while the reload is mid-flight. Gate on `EditorApplication.isCompiling` (and/or scan `AppDomain.CurrentDomain.GetAssemblies()`) and retry once reload completes — don't treat the first null as "type missing."
- **Known compression bug — set ASTC yourself.** A known build-path bug can force the **wrong texture compression** for iOS. Do not trust defaults: explicitly set/verify **ASTC** for iOS via `execute_code` driving `TextureImporter` platform overrides (`scripting_ext` group). Snippet in `references/ios-build-pipeline.md`. Verify before you call the build good.
- Poll `action="status"` to confirm completion. A returned path is not proof of success until status reports finished without errors and the folder exists.
- **The Unity iOS "build" is just the Xcode export — the expensive part is later.** `BuildPipeline.BuildPlayer` for iOS only generates the Xcode project (with IL2CPP-generated C++); the costly IL2CPP→native compile + link happens in **Xcode** (the fastlane archive step). So an incremental Unity iOS export can finish in **~10-20s** — don't mistake the fast Unity export for "the whole build." Driving it via MCP `execute_code` calling the build method synchronously often returns a timeout/no-response while the build continues on the main thread; **poll `Build/iOS/Info.plist` mtime** to detect completion (the established pattern — the bridge frequently drops during/after builds). Confirm the post-build hooks landed by reading the generated `Info.plist` keys (e.g. `GADApplicationIdentifier`, `ITSAppUsesNonExemptEncryption`, and the **absence** of `NSUserTrackingUsageDescription` for a non-tracking build).

## Manual macOS / Xcode step (cannot be done via MCP)

This is an explicit **manual gate**. MCP generates the Xcode project; a human on macOS must:

1. Open the generated Xcode project.
2. Set the **signing team**, **provisioning profile**, and confirm the **bundle id**.
3. `xcodebuild archive` → `xcodebuild -exportArchive` to produce the `.ipa`.
4. Upload to **TestFlight / App Store Connect** (Xcode Organizer or `xcrun altool` / `notarytool`).

Until a human does this, the truthful claim is: **"Xcode project generated at `<path>`; signing, archive, `.ipa`, and upload are pending manual macOS steps."** Do not claim the app is built, signed, on TestFlight, or shipped.

## Automating the manual step with fastlane (signing / TestFlight / CocoaPods)

That manual gate CAN be automated with fastlane + an **App Store Connect API key** (no Apple-ID / 2FA), but the evidence bar is unchanged: a green lane is proof only when it produced a real `.ipa` artifact **and** an upload confirmation — and even then "uploaded" ≠ "live on TestFlight" (Apple processes the build asynchronously). Full ordered recipe + working `Fastfile` lanes in `references/fastlane-signing-cocoapods.md`. The gotchas that each cost hours:

- **API token duration must be `≤ 1200s` but NOT exactly 1200.** 1200 is Apple's hard ceiling; sitting on it lets sub-second clock skew (machine ahead of Apple) push `exp` over and yields *intermittent* 401 "Authentication credentials are missing or invalid". Use `duration: 1000` for margin.
- **Env-var shadowing → silent wrong-key 401.** fastlane reads `ENV` and dotenv does **not** overwrite an already-set var, so a shell that exports `ASC_KEY_ID`/`ASC_ISSUER_ID` for a *different* key makes fastlane sign a JWT with the wrong `kid` while using your private key — same generic 401. Give the lane's vars a unique prefix (`MYGAME_ASC_KEY_ID`…) so the shell can't shadow them; confirm by base64url-decoding the JWT header's `kid`.
- **Build-number collisions:** `latest_testflight_build_number` counts only **fully-processed** builds, so uploading while a prior build still processes fails with "bundle version … already used". Provide an override floor env (`MYGAME_BUILD_OVERRIDE`) to force a higher `CFBundleVersion`.
- **Game Center signing:** automatic/cloud signing via the API key **can't synthesize an App Store profile carrying the Game Center feature.** Mint it with `sigh(force: true)`, then `update_code_signing_settings` for **manual per-target** signing — app target gets the profile, the embedded `UnityFramework` gets the distribution **identity only** (`profile_name: ""`; frameworks take no profile).
- **Keep the App Attest *environment* entitlement OFF (opt-in).** Adding `com.apple.developer.devicecheck.appattest-environment` breaks automatic signing (needs a profile feature cloud signing can't make); App Attest still works on TestFlight (production env by default). Ship only the Game Center entitlement.
- **CocoaPods when ads/native pods are present:** EDM4U generates `Build/iOS/Podfile` but does **not** reliably run `pod install` headlessly — the lane must run it itself and build the generated **`.xcworkspace`** (not the bare `.xcodeproj`). `pod install` inside fastlane fails with `Gem::MissingSpecError` (fastlane's bundler/`GEM_PATH` leaks in) → run it env-stripped: `env -u GEM_HOME -u GEM_PATH -u BUNDLE_GEMFILE -u BUNDLE_BIN_PATH -u RUBYOPT -u RUBYLIB pod install`. Remove leftover mediation packages fully (e.g. an `Assets/LevelPlay/` folder whose ironSource `Dependencies.xml` pulls UnityAds 4.18.1 vs `com.unity.ads`' 4.17) — version conflicts break `pod install`.

## App Store readiness checklist

Load `references/checklists/app-store-readiness.md`. Gate the submission on:

- **App icon** — square, **no alpha channel**, all required sizes. If art is blocked, generate one procedurally instead of shipping the icon gap: render an **opaque** 1024×1024 `Texture2D` (gradient bg + composited icon via alpha-over), `EncodeToPNG` → write under `Assets/` → import with `alphaSource=None`, no mipmaps (icons must be opaque), then assign to **every** iOS slot by looping `PlayerSettings.GetSupportedIconKinds(NamedBuildTarget.iOS)` → `GetPlatformIcons(kind)` → `SetTexture` → `SetPlatformIcons(kind, icons)`.
- **Launch screen** — configured (storyboard / Unity launch screen), not the default Unity splash if Pro.
- **Orientation** — lock to **portrait** for most casual games (set in Player Settings).
- **iPhone-only unless you actually support iPad** — if the binary supports iPad, App Store Connect blocks submission demanding "a screenshot for 13-inch iPad displays." Set `PlayerSettings.iOS.targetDevice = UnityEditor.iOSTargetDevice.iPhoneOnly` (→ `TARGETED_DEVICE_FAMILY=1`). GOTCHA: Unity sets this on the APP target but can leave the **UnityFramework** target at `"1,2"`. Pin BOTH in a `[PostProcessBuild]` via `PBXProject.SetBuildProperty(guid, "TARGETED_DEVICE_FAMILY", "1")` for `GetUnityMainTargetGuid()` AND `GetUnityFrameworkTargetGuid()`. **Verify authoritatively, not by raw grep** (Tests/GameAssembly targets legitimately keep `1,2` — noise): `PBXProject.GetBuildPropertyForAnyConfig(appGuid, "TARGETED_DEVICE_FAMILY")`, and/or unzip the final `.ipa` and `PlistBuddy -c "Print UIDeviceFamily" Payload/<App>.app/Info.plist` (should be the array `{ 1 }`). Once iPhone-only, only iPhone screenshots are required.
- **Deployment target** — **>= iOS 13** (Unity 6 minimum target); higher only if a dependency requires it.
- **IL2CPP backend** — confirmed (required).
- **Managed stripping + `link.xml`** — stripping is on for size; add a `link.xml` so reflection/serialization-used types survive (JSON DTOs, scriptable objects loaded by name). Test the stripped build, not just the Editor.
- **Privacy manifest + ATT** — if you use ads, analytics, or anything touching IDFA: include `PrivacyInfo.xcprivacy` declaring data use + required-reason APIs, and present the **ATT** prompt before tracking. Even a no-tracking game needs one: declare `NSPrivacyTracking=false`, empty collected-data, and — because **PlayerPrefs == NSUserDefaults** — one `NSPrivacyAccessedAPICategoryUserDefaults` entry with reason `CA92.1`. Inject it into the Xcode target from a `[PostProcessBuild]` script using `UnityEditor.iOS.Xcode.PBXProject`, **wrapped in `#if UNITY_IOS`** — that namespace only exists with the iOS module + iOS target active, so an unguarded script breaks compilation on other active targets.
  - **Non-tracking game with ads + a leaderboard** — declare only what YOUR code collects; the ad SDK declares its own in its bundled manifest (Apple merges them). For a Game Center leaderboard, three `NSPrivacyCollectedDataTypes` entries — `NSPrivacyCollectedDataTypeUserID` (player id) + `NSPrivacyCollectedDataTypeName` (display name) + `NSPrivacyCollectedDataTypeOtherDataTypes` (scores/times) — each `Linked=true`, `Tracking=false`, purpose `NSPrivacyCollectedDataTypePurposeAppFunctionality`. Keep the `NSUserDefaults` CA92.1 entry. **The App Privacy questionnaire MUST match** (tracking = No, same data types/purposes). For non-personalized ads (`npa=1`, no ATT, no IDFA), have the post-build script **remove any `NSUserTrackingUsageDescription`** the ad plugin injected, so the app declares no tracking intent.
- **Export compliance** — declare encryption usage (most casual games: standard/exempt). Post-build can set `ITSAppUsesNonExemptEncryption=false` in `Info.plist` so App Store Connect skips the per-upload prompt.
- **Game Center: the FIRST leaderboard must ride along with an app version.** App Store Connect errors on first submission: "Your app's first leaderboard must be submitted with a Game Center-enabled app version." Game Center leaderboards/achievements are versioned items — the first one must be added to the v1.0 version's Game Center section, then Submitted together (app + leaderboard). The leaderboard must be "Ready to Submit" (reference name, ID, score format, sort order, ≥1 localization).
- **Age rating, screenshots, metadata** — App Store Connect listing complete. **Screenshots:** required portrait sizes are 6.9" = **1320×2868** (iPhone 16 Pro Max, covers modern) and 6.5" = **1242×2688** (older large phones); once iPhone-only, no iPad sizes. Capture method below.
- **Real-ad rebuild is a distinct gate.** Ship/QA with TEST ads, then flip a single `UseTestAds=false` const → rebuild → that's the binary you attach for review. Don't submit a test-ad build.

### Submission docs as deliverables

Generate three Markdown docs the user hosts/pastes into App Store Connect — they turn a vague "submit it" into a field-by-field runbook:

- **SUBMISSION_CHECKLIST** — the single runbook with a status legend (done / needs-user / to-do), one row per App Store Connect field, grouped by binary readiness → app info → version → App Privacy → screenshots → age rating → App Review notes → "before you Submit" (the real-ad rebuild) → consolidated user actions.
- **APP_STORE** — the listing copy within Apple's hard char caps (name 30, subtitle 30, promo 170, keywords 100 comma-separated no-spaces, description 4000, What's New), **plus** the App Privacy questionnaire answers (must match `PrivacyInfo.xcprivacy`), the age-rating answers, and App Review notes.
- **PRIVACY_POLICY** — a hostable policy; the user provides a public URL for it (required field).

Concrete templates live in the project repo: `Assets/<YourGame>/SUBMISSION_CHECKLIST.md`, `Assets/<YourGame>/APP_STORE.md`, `Assets/<YourGame>/PRIVACY_POLICY.md`.

## Release risk report (final response format)

Lead with pass/fail. Then:

- **Passed (with evidence)** — QA gates met, tests green (counts + `job_id`), screenshots per aspect ratio, ASTC verified, console clean.
- **Manual / pending** — Xcode signing, archive, `.ipa` export, TestFlight upload, App Store metadata. Name them as not-done.
- **Risky / unverified** — anything not exercised (untested device, stripping not validated on-device, perf measured only in Editor, privacy/ATT assumptions).

Be precise about words: "Xcode project generated" ≠ "app built"; "tests green" needs counts; "ASTC set" needs the verification output. Never upgrade an unverified item to passed.

## Field notes & lessons

- Added "capturing transient VFX for proof" — set `EditorApplication.isPaused = true` right after spawning a sub-round-trip effect so the screenshot freezes its first frame (objects must spawn on-screen), then restore.
- Detect the iOS Build Support module via `BuildPipeline.IsBuildTargetSupported` before building — without it `PBXProject` won't compile; surface as a Hub install (user-blocked), don't fail mysteriously.
- Added iOS player-settings recipe via `execute_code` (fully-qualified C#6) — backend, portrait lock (orientation + all four autorotate flags), bundle id, manual signing; read back, and `targetOSVersionString` clamps up to the editor floor.
- A new editor type can resolve NULL during domain reload — gate `Type.GetType` on `EditorApplication.isCompiling`/assembly scan and retry once reload completes.
- Procedural app icon when art is blocked — opaque 1024² PNG (`alphaSource=None`, no mipmaps) assigned to every iOS slot via `GetSupportedIconKinds`/`SetPlatformIcons`.
- Ship `PrivacyInfo.xcprivacy` even no-tracking (`CA92.1` for PlayerPrefs==NSUserDefaults), injected by a `[PostProcessBuild]` `PBXProject` script wrapped in `#if UNITY_IOS`.
- Added PlayMode test isolation — bootstrap must parent its root objects (else orphans + stale `FindAnyObjectByType`); clear the save in `[SetUp]` AND `[TearDown]` (auto-resume resumes the wrong board); `DestroyImmediate` all app instances in `[TearDown]`.
- Two run_tests gotchas — `manage_editor stop` before run_tests (else "Cannot start a test run while ... in Play Mode"); retry with larger `init_timeout` on "tests did not start within timeout". Added: an unfocused Editor throttles Play Mode to a few FPS so MCP screenshots of coroutine animations look slow/partial — Editor throttling, not a device bug; note it, don't chase it.
- iPhone-only to dodge iPad screenshot requirements — `iOSTargetDevice.iPhoneOnly` (`TARGETED_DEVICE_FAMILY=1`); pin BOTH the app and **UnityFramework** targets in `[PostProcessBuild]` (Unity can leave the framework at `"1,2"`); verify with `GetBuildPropertyForAnyConfig` / `PlistBuddy Print UIDeviceFamily` on the `.ipa`, not raw grep. Verified against `PostBuild.cs`.
- Game Center's FIRST leaderboard must be submitted WITH a Game Center-enabled app version (versioned item) — add it to the v1.0 version's GC section and Submit together; leaderboard must be "Ready to Submit."
- Non-tracking privacy manifest for ads + a leaderboard — declare only your own data (three GC entries: UserID + Name + OtherDataTypes, Linked/non-tracking/AppFunctionality; keep CA92.1 UserDefaults); ad SDK declares its own (merged); App Privacy questionnaire must match; post-build removes any `NSUserTrackingUsageDescription` for non-personalized ads. Verified against `PrivacyInfo.xcprivacy` + `PostBuild.cs`.
- Exact-size App Store screenshots — 6.9"=1320×2868, 6.5"=1242×2688; `ScreenCapture.CaptureScreenshot` at a Fixed Resolution Game View (NOT `manage_camera`, which drops Overlay UI); verify with `sips`; throttled Editor can write a stale frame so on-device is often more reliable.
- The Unity iOS export is fast (~10-20s, just the Xcode project) — the IL2CPP→native compile + link is the Xcode/fastlane archive cost; poll `Build/iOS/Info.plist` mtime for completion (bridge drops), and confirm post-build hooks via the generated `Info.plist` keys (`GADApplicationIdentifier`, `ITSAppUsesNonExemptEncryption`, absent `NSUserTrackingUsageDescription`).
- Submission docs as deliverables — SUBMISSION_CHECKLIST (field-by-field runbook with done/needs-user/to-do legend), APP_STORE (listing within Apple char caps + App Privacy + age-rating + Review notes), PRIVACY_POLICY (user-hosted); plus the distinct real-ad rebuild gate (flip `UseTestAds=false`, rebuild, attach that binary). Templates: `Assets/<YourGame>/{SUBMISSION_CHECKLIST,APP_STORE,PRIVACY_POLICY}.md`.
- Added "Automating the manual step with fastlane" section + `references/fastlane-signing-cocoapods.md`. ASC API-key auth (`duration: 1000`, not Apple's 1200 ceiling; unique-prefixed env vars to defeat dotenv shadowing → silent wrong-`kid` 401; `MYGAME_BUILD_OVERRIDE` floor for build-number collisions during processing). Signing: `sigh(force: true)` + per-target manual signing for the Game Center profile (framework gets identity only, no profile); keep the App Attest env entitlement opt-in. CocoaPods: lane runs env-stripped `pod install` and builds the `.xcworkspace`; remove leftover mediation SDKs (LevelPlay/ironSource) that conflict the Podfile. Verified against the project's `fastlane/Fastfile` and `PostBuild.cs`.
