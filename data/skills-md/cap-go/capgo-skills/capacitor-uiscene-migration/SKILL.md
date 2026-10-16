---
name: capacitor-uiscene-migration
description: Migrates a Capacitor iOS app or plugin from the AppDelegate lifecycle to the UIScene lifecycle introduced in Capacitor 8.5 and required by Xcode 27. Audits first (custom AppDelegate URL/lifecycle code, CAPBridgeViewController subclasses, existing SceneDelegate.swift, Info.plist UIApplicationSceneManifest, project.pbxproj registration, plugin lifecycle observers, tmpWindow/TmpViewController), reports, then merges surgically or hands template-shaped projects to `npx cap migrate`. Use for "Capacitor 8.5 upgrade", "add SceneDelegate", "adopt UIScene", "CLIENT OF UIKIT REQUIRES UPDATE", deep links or appUrlOpen stopped firing after 8.5, "cap migrate skipped partial state", or as the prerequisite step before Capacitor 9. Do not use for Android, full major upgrades (use capacitor-app-upgrade-v8-to-v9), or new deep-link setup (use capacitor-deep-linking).
allowed-tools:
  - Bash(node -e *)
  - Bash(find *)
---

# Capacitor UIScene Migration (8.4 -> 8.5)

Capacitor 8.5 moved the iOS template to the UIScene lifecycle because Xcode 27 requires it. It shipped as a breaking minor, iOS only. The 8.5 core still runs the AppDelegate path, so bumping the dependency alone does not break an app; the app project must adopt scenes before it can build with Xcode 27 (and before Capacitor 9).

Canonical source: https://capacitorjs.com/docs/updating/8-5

## When to Use

TRIGGER when:
- App is on `@capacitor/ios` 8.0-8.4, or on 8.5 without `UIApplicationSceneManifest` in `Info.plist`
- Xcode 27 build or runtime warning "CLIENT OF UIKIT REQUIRES UPDATE: This process does not adopt UIScene lifecycle"
- `npx cap migrate` printed `UIScene migration: project is in a partial state ... Skipping automated migration`
- After adding a scene manifest: custom URL scheme, universal link, `appUrlOpen`, or AppDelegate `applicationDidBecomeActive` code stopped running
- Build error on `tmpWindow` or `TmpViewController` after updating to 8.5
- A plugin author asks whether their iOS code survives the scene lifecycle
- Preparing a Capacitor 8 -> 9 upgrade from 8.4 or earlier

Do not use:
- Capacitor 8 -> 9 package/native upgrade itself -> `capacitor-app-upgrade-v8-to-v9` / `capacitor-plugin-upgrade-v8-to-v9`
- Setting up deep links from scratch -> `capacitor-deep-linking`
- Android (UIScene is iOS only)
- Multi-window or resizable layout work beyond lifecycle adoption

## Live Project Snapshot

!`node -e "const fs=require('fs');if(!fs.existsSync('package.json'))process.exit(0);const pkg=JSON.parse(fs.readFileSync('package.json','utf8'));const out=[];for(const s of ['dependencies','devDependencies','peerDependencies']){for(const [n,v] of Object.entries(pkg[s]||{})){if(n.startsWith('@capacitor/'))out.push(s+'.'+n+'='+v)}}const p='ios/App/App/';out.push('SceneDelegate.swift='+fs.existsSync(p+'SceneDelegate.swift'));if(fs.existsSync(p+'Info.plist'))out.push('UIApplicationSceneManifest='+fs.readFileSync(p+'Info.plist','utf8').includes('UIApplicationSceneManifest'));if(fs.existsSync(p+'AppDelegate.swift'))out.push('configurationForConnecting='+fs.readFileSync(p+'AppDelegate.swift','utf8').includes('UISceneConfiguration(name:'));console.log(out.join('\n'))"`

## Facts the Audit Depends On

- Once `UIApplicationSceneManifest` exists, iOS stops calling these AppDelegate methods: `application(_:open:options:)`, `application(_:continue:restorationHandler:)`, `applicationDidBecomeActive`, `applicationWillResignActive`, `applicationDidEnterBackground`, `applicationWillEnterForeground`. Code in them silently stops running. No compiler warning.
- Still called on the AppDelegate: `didFinishLaunchingWithOptions`, `applicationWillTerminate`, push token registration (`didRegisterForRemoteNotificationsWithDeviceToken` / `didFailToRegister...`) and remote-notification delivery. `UIApplication.*Notification` lifecycle notifications still fire.
- `SceneDelegateProxy` (`CAPSceneDelegateProxy.swift`) re-posts `.capacitorOpenURL`, `.capacitorOpenUniversalLink` (same payload) and `CDVPluginHandleOpenURL`, and mirrors the URL into `ApplicationDelegateProxy.shared.lastURL`. Cold-start URLs and user activities are held until the first `.capacitorViewDidAppear`, so plugins see them after registration and `App.getLaunchUrl()` works.
- New 8.5-only notifications: `.capacitorSceneWillConnect`, `.capacitorSceneOpenURL`, `.capacitorSceneOpenUniversalLink` (object = `UIScene`, payload in `userInfo`). Not posted on 8.4.
- JS `pause`/`resume` are driven by `UIScene.didEnterBackgroundNotification` / `willEnterForegroundNotification`, filtered to the bridge's scene.
- Removed in 8.5: `TmpViewController`, `CapacitorBridge.tmpWindow`, `tmpViewControllerAppeared`. Any reference is a build error; present from `bridge.viewController`.
- The 8.5 SceneDelegate creates the window and `CAPBridgeViewController()` in code. A custom bridge subclass set in `Main.storyboard` must be instantiated in the SceneDelegate instead.
- `cap migrate` (CLI 8.5+) classifies the project by three signals: manifest in `Info.plist`, `SceneDelegate.swift` on disk, `UISceneConfiguration(name:` in `AppDelegate.swift`. 0/3 -> migrates; 3/3 -> skips as done; 1-2/3 -> warns "partial state" and does nothing. It never overwrites an existing `SceneDelegate.swift`. It warns (does not fix) on `UIApplication.shared.applicationState`, `tmpWindow`, `TmpViewController`, and custom `open url:` / `continue userActivity:` bodies.

## Procedure

Audit, report, ask, then edit. Never edit before the user has seen the findings.

1. **Detect repo type.** `ios/App/App.xcodeproj` -> app. `Package.swift` / `*.podspec` with `CAPPlugin` sources and no app project -> plugin; go to step 9.
2. **Check versions and package manager.** `@capacitor/ios` must reach `^8.5.0`. `ios/App/Podfile` -> CocoaPods; `ios/App/CapApp-SPM` -> SPM. The SceneDelegate is identical for both.
3. **Classify** with the snapshot's three signals (eligible / migrated / partial).
4. **Audit** with the commands in `references/audit-patterns.md`, covering `ios/App` and installed plugins in `node_modules`. Record file:line for each hit.
5. **Report** grouped as: build blockers (`tmpWindow`, `TmpViewController`), needs a decision (custom URL/activity/lifecycle bodies, existing SceneDelegate, storyboard custom class, third-party SDK forwarding), informational (observers that keep working, `applicationState`, issues inside `node_modules`).
6. **Ask** at the real judgement calls:
   - Custom body in `open url:` / `continue userActivity:`: move it into `scene(_:openURLContexts:)` / `scene(_:continue:)` next to the proxy call (show the body first).
   - Custom lifecycle code: move to `sceneDidBecomeActive` / `sceneWillResignActive` / `sceneDidEnterBackground` / `sceneWillEnterForeground`, or to `UIApplication` notification observers.
   - Remove the now-dead AppDelegate URL methods, or keep them (harmless).
   - SDKs that need URL forwarding (Facebook, Google Sign-In, OAuth redirect libraries): check their docs for a scene-delegate entry point and call it from the SceneDelegate.
7. **Apply.**
   - Eligible and template-shaped: `npm i @capacitor/core@^8.5.0 @capacitor/ios@^8.5.0`, `npm i -D @capacitor/cli@^8.5.0`, then `npx cap migrate`. Read every log line; anything skipped is handled by hand for that step only. Then apply step 6 decisions.
   - Partial or customized: merge only the missing pieces using `references/scene-delegate-template.md`. Keep existing keys, methods and custom logic. Register the new file per `references/pbxproj-registration.md`.
8. **Sync and build**: `npx cap sync ios`, then build (see Verification). Re-check the three signals: all must be true.
9. **Plugin repos**: audit and advise only, using `references/plugin-audit.md`. Never touch app files from a plugin repo; edit plugin sources only when the user asks.

## Verification

```bash
npx cap sync ios
xcodebuild -project ios/App/App.xcodeproj -scheme App -configuration Debug \
  -destination 'generic/platform=iOS Simulator' build   # use -workspace App.xcworkspace for CocoaPods
grep -rn --include=*.swift -E '\btmpWindow\b|\bTmpViewController\b' ios/App   # expect nothing
```

On a device or simulator:
- App launches to the web view (no black screen).
- Background then foreground: JS `pause` and `resume` fire once each.
- Custom scheme, warm (app running): `appUrlOpen` fires. Use `xcrun simctl openurl booted myscheme://test`.
- Custom scheme, cold (app killed, then link): `appUrlOpen` fires and `App.getLaunchUrl()` returns the URL.
- Universal link routes in, if the app has associated domains (needs a real domain and AASA file).
- Push: token still arrives (`registration` event), and a tapped notification opens the app.
- Any moved custom logic (analytics on foreground, SDK URL handlers) runs.

## Error Handling

- `cap migrate` says "partial state" -> expected for hand-edited projects; merge by hand (step 7). Do not reset files without asking.
- Black screen after migration -> SceneDelegate does not create a window, or the `UISceneDelegateClassName` in `Info.plist` does not match the class. Use `$(PRODUCT_MODULE_NAME).SceneDelegate` and the template window setup.
- `Cannot find 'SceneDelegate' in scope` in AppDelegate -> file not in the App target; see `references/pbxproj-registration.md`.
- `Value of type 'CapacitorBridge' has no member 'tmpWindow'` -> delete the reference; present from `bridge?.viewController`.
- Deep link works warm but not cold -> URL logic still lives in the AppDelegate, or the app reads it before the bridge appears; rely on `appUrlOpen` + `getLaunchUrl()`.
- Custom bridge subclass not used (plugins registered in `capacitorDidLoad` missing) -> instantiate the subclass in `scene(_:willConnectTo:)`.
- `pbxproj` hand edit makes Xcode refuse to open the project -> revert and add the file through Xcode.

## References

Only load a reference when its topic is in play.

| File | Load when |
|---|---|
| `references/audit-patterns.md` | Step 4: grep commands and how to classify each hit |
| `references/scene-delegate-template.md` | Creating or merging SceneDelegate, Info.plist manifest, AppDelegate hook, custom subclass and lifecycle variants |
| `references/pbxproj-registration.md` | Registering `SceneDelegate.swift` without Xcode, or verifying the CLI did |
| `references/plugin-audit.md` | The repo is a plugin, or an installed plugin shows lifecycle hits |

Related skills: `capacitor-app-upgrade-v8-to-v9`, `capacitor-plugin-upgrade-v8-to-v9`, `capacitor-app-upgrades`, `capacitor-deep-linking`, `capacitor-push-notifications`.
