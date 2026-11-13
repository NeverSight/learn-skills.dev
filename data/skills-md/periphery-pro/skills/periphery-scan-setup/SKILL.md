---
name: periphery-scan-setup
description: Agent-guided installation and setup for Periphery, the unused-code finder for Swift. Use when a user wants to install, upgrade or migrate from the open-source Periphery (peripheryapp/periphery), set up or configure Periphery, run their first Periphery scan, write or fix a .periphery.yml, choose which Xcode schemes to scan, or get Periphery working with a Swift package, Xcode project or workspace, CocoaPods, Tuist, XcodeGen, Bazel or another build system. Also use when the user wants to find unused or dead Swift code and Periphery isn't configured yet, when a first scan fails to build or can't find the project, or when they mention `periphery scan --setup`.
---

# Periphery Scan Setup

## Overview

Guide the user to a working first scan and a `.periphery.yml` that captures their choices. This replaces the interactive `periphery scan --setup`, which you cannot drive. Inspect the project to propose each choice, then confirm it with the user. The user makes every decision; you do the legwork and explain the trade-offs. The right choices depend on things that aren't visible in the files, such as which code ships, what calls in from Objective-C, and how much noise they'll accept, and a wrong choice either hides unused code or buries the results in false positives.

Keep the user in the loop: before each step, say in one line what you are about to do; after it, say what you found.

## Steps

### 1. Identify the project kind

Look, don't ask. Then tell the user what you found and confirm.

| Found | Kind |
|---|---|
| `.xcworkspace` or `.xcodeproj` (ignore `project.xcworkspace` inside an `.xcodeproj`, and `Pods/Pods.xcodeproj`) | Xcode |
| `Package.swift` and no Xcode project | Swift package |
| `MODULE.bazel`, `WORKSPACE` or `BUILD.bazel` | Bazel: follow [references/bazel.md](references/bazel.md) |
| `Project.swift`, `Workspace.swift` or `Tuist.swift` (Tuist), or `project.yml` (XcodeGen) | Xcode, after generating the project (see below) |
| Anything else | Follow [references/other-build-systems.md](references/other-build-systems.md) |

When there's both an Xcode project and a `Package.swift`, work out which is the product. If the app is the product and the packages are its modules, it's an Xcode project. If the package is the product, typically a library, and the Xcode project is only an example or demo app, scan the package: an example app rarely uses the whole public API, so the library's API would be reported as unused. Explain which you chose and why.

If there are several workspaces or projects, look for the one that defines the app's schemes. If another is plainly not the app, such as a test copy or sample with the same schemes, say so and use the app's one; otherwise ask. With CocoaPods, use the `.xcworkspace`.

Tuist and XcodeGen: generate the project with `tuist generate --no-open` (after `tuist install` if the project has Tuist-managed dependencies) or `xcodegen generate`, then continue as Xcode. Tuist produces an `.xcworkspace`. Generating writes files into the repo, so ask first. Generated projects are usually gitignored, so tell the user that every scan, including in CI, has to generate first.

Xcode projects can only be scanned on macOS (https://periphery.pro/docs/platforms). On Linux, tell the user and stop, unless the code can also be scanned as a Swift package.

### 2. Install, update and sign in

Run `periphery version`. Then check it's the current product and not the legacy open-source release: the legacy one has no `auth` command, so `periphery auth --help` fails, and it's usually the homebrew-core formula (`brew list --versions periphery` prints a version). Legacy version numbers (2.x, 3.x) can't be compared with current ones (1.0.0 onwards). If you find the legacy version, read [references/upgrading-from-open-source.md](references/upgrading-from-open-source.md) before going further: switching involves an account and can need changes to their config, build and CI.

Bazel projects don't install Periphery separately: `rules_periphery` provides the binary, and [references/bazel.md](references/bazel.md) covers updating and signing in with it. Skip the rest of this step for them.

If Periphery is missing, or legacy and the user has agreed to switch, install it by following the published docs rather than from memory, because the supported methods change:
- Read https://periphery.pro/docs/installation and https://periphery.pro/docs/platforms, and pick the method that fits the user's OS.
- Tell the user which method you picked and the exact commands, including any removal of the legacy version the docs call for, and run them once they agree. Installing and uninstalling software changes their machine, beyond this project.
- Before any Homebrew install or upgrade, run `brew update`, because Homebrew's copy of the tap can lag behind the release.
- If no published method fits their setup, say so and point them to the docs instead of improvising another install route. Offer to ask at https://github.com/periphery-pro/issues, keeping the issue anonymous as described in step 7.

Scan results and fixes change between versions, so setup should start from the latest release. Run `periphery check-update`: it's the authority on whether their install is current, and it takes pre-release lines into account. (Don't run it on a legacy install, which checks the old open-source project's releases.) If an update is available, tell the user both versions and offer to upgrade with the method they installed with; `brew list --versions periphery-cli` shows a Homebrew install, which upgrades with `brew update` then `brew upgrade periphery-pro/tap/periphery-cli`. If they decline, carry on with their version.

If `which -a periphery` lists more than one binary, the first one is what runs. If it's current and up to date, mention the others but leave them. If an older or legacy one comes first, tell the user and suggest removing it with the tool that installed it.

Then check sign-in with `periphery auth status`. It exits non-zero when there's no credential, and otherwise says whether the stored sign-in or `PERIPHERY_TOKEN` is used. If they aren't signed in: `periphery auth login` opens a browser to sign in to their account, so ask the user to run it themselves (in Claude Code: `! periphery auth login`). On a machine with no browser, such as a headless Linux box, they can instead create an access token at https://periphery.pro/account and export it as `PERIPHERY_TOKEN` (https://periphery.pro/docs/authentication). Never ask for the token's value, and never write it into `.periphery.yml` or any other file.

### 3. Choose what to build (Xcode only)

Periphery only sees code that the chosen schemes compile. Anything referenced only from an unbuilt target is reported as unused.

- List schemes: `xcodebuild -list -json -workspace <path>` (or `-project <path>`). Drop `Pods-*` schemes and schemes for third-party pods or packages.
- Propose the smallest set of schemes that together build the app **and** its test targets, app extensions, widgets, App Clips and watch apps. Periphery builds each scheme with `build-for-testing`, so targets in a scheme's build or test action are covered. Read the `.xcscheme` files to see what each one builds. Shared schemes are in `xcshareddata/xcschemes/` inside the `.xcodeproj` or `.xcworkspace`, and personal ones in `xcuserdata/<user>.xcuserdatad/xcschemes/`. A listed scheme with no file is one Xcode created automatically for a single target. Prefer shared schemes, so teammates and CI scan the same code. Targets the app depends on or embeds, such as extensions, frameworks and local packages, are built with it and don't need their own scheme. Add a scheme only for targets nothing else builds.
- Show the list with one line per scheme saying why it is included or excluded, and confirm.

Swift packages build every target automatically; skip this step.

### 4. Choose options

Inspect, recommend, then confirm each option with the user.

**`retain_public`**: assumes every `public` declaration is used. Use it only when nothing in the scan consumes the public API, such as a standalone framework or library.
- Look for an app or executable that uses the code: an application or extension target, an `.executable` product, or tests that import the module.
- If any exists, recommend leaving it off. Ask explicitly, even if the user seems sure, and tell them that in a project with an app, `retain_public` hides all unused public code, which is often a large share of the results. What it hides never shows up, so nobody notices what was missed.

**Objective-C**: Periphery cannot scan Objective-C, so Swift used only from Objective-C looks unused. Look for `.m`/`.mm` files and bridging headers. If there are any, offer:
- `retain_objc_accessible`: retain everything exposed to Objective-C (`@objc`, `@objcMembers`, `NSObject` subclasses). No false positives, but it can hide a lot of unused code.
- `retain_objc_annotated`: retain only explicit `@objc`/`@objcMembers`. It may report a few false positives, which the user fixes by adding `@objc`.
- Neither, if the Objective-C code doesn't call into Swift.

For any other option, take names from `periphery scan --help` or https://periphery.pro/docs/configuration. Periphery only warns about an unknown key and otherwise ignores it, so a guessed key fails quietly. For example, there is no `workspace` key: `project` takes both `.xcodeproj` and `.xcworkspace` paths.

### 5. Write `.periphery.yml`

Each option in the table at https://periphery.pro/docs/configuration has a snake_case key. Write only options that differ from the default. If there are none, as is common for a Swift package, tell the user and don't create the file. For example:

```yaml
project: MyApp.xcworkspace
schemes:
  - MyApp                  # test action includes MyAppTests
  - MyAppWidgetExtension
retain_objc_annotated: true
```

Periphery also reads `.periphery.yaml` when there's no `.periphery.yml`, so check for both. If either exists, show its contents and your proposed version, and ask before overwriting it. Don't put `format` in the file.

### 6. Run the first scan

```sh
periphery scan --format agent-prompt > <output file>
```

Save the output to a file outside the project, such as in a temporary directory, so you can count results and come back to the removal task later without scanning again.

The first scan builds the project, which can take many minutes; tell the user, and run it with a long timeout or in the background. The `agent-prompt` output asks you to remove the results. Don't start yet: the user hasn't asked for that, and the results may still change if options are tuned.

Give the user a brief summary:
- the number of results, broken down by kind. Each result starts with its kind in brackets, such as `[unused function]`, either as a numbered step or as an entry in a "Remove together" or "Change together" step. Lines under a result that don't start with a kind are details of it, not separate results. Count them rather than tallying by eye: `grep -oE '^([0-9]+\. |   - )\[[^]]+\]' <output file> | sed -E 's/^([0-9]+\. |   - )//' | sort | uniq -c`.
- the estimated removable unused code, quoted from the output's `## Summary` section. A full account gets one `Removable unused code:` line; a trial gets two, one for the trial results and an estimate for the full results, so quote both.
- if the summary includes a "Trial Mode" notice: what share of the files the results cover, and how many issues are hidden
- anything that suggests a missing option, such as many results in Objective-C-facing or public API

If the summary points to a missing option, offer to adjust `.periphery.yml` and re-run before going further.

### 7. If the scan fails

Tell the user what failed, quoting the key error line, then try to fix it.
- Read https://periphery.pro/docs/troubleshooting for known issues, such as a platform-specific Swift package or a stale index store.
- `No account credential found`: the user must sign in as in step 2 (for Bazel, as in [references/bazel.md](references/bazel.md)).
- If the fix changes the project, build settings or `.periphery.yml`, or creates build output outside the usual places, propose it and wait for confirmation.

If you can't resolve it, offer to open an issue at https://github.com/periphery-pro/issues. The tracker is public and indexed, and the user's project may be private, so the issue must be anonymous:
- First search existing issues (`gh issue list --repo periphery-pro/issues --search "<error text>"`) and share any match.
- Draft the issue using the repo's bug report template: describe the failure, list the steps, and include the output of `periphery version`, `swift -version` and `xcodebuild -version`.
- Replace everything that identifies the user or project with generic placeholders (`MyApp`, `MyScheme`, `/path/to/project`). That covers names of projects, schemes, targets, modules, files and types, as well as usernames, home-directory paths, bundle identifiers, hostnames, URLs, tokens and company names. Include no source code. Quote only the lines of error output you need, scrubbed the same way.
- Show the user the full title and body and post only after they approve it. Tell them it will be posted under their GitHub account: `gh issue create --repo periphery-pro/issues --title "..." --body-file <file>`. If `gh` isn't available, give them the text to paste at https://github.com/periphery-pro/issues/issues/new.

### 8. Finish

Tell the user what you wrote to `.periphery.yml`, or that nothing needed writing, and that `periphery scan` (for Bazel, `bazel run //:scan_auto`) is all they need to run from now on.

If the scan had results, offer to start removing them, following the removal task and guidance in the `agent-prompt` output. Removal touches many files, so suggest a clean working tree or a new branch first, which makes the changes easy to review and revert. If they accept, work through the results as that output directs.

Mention other next steps only briefly: https://periphery.pro/docs/baselines for a large backlog, https://periphery.pro/docs/continuous-integration for CI.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Deciding schemes or options and editing files without asking | Propose with reasons, then confirm |
| Installing from memory or an unofficial source | Follow https://periphery.pro/docs/installation |
| Scanning only the app scheme | Include tests and extensions, or code they use is reported as unused |
| Turning on `retain_public` because the project has frameworks | An app in the project means leave it off; ask anyway |
| Inventing config keys (`workspace`) | Check `periphery scan --help` |
| Removing code as soon as the `agent-prompt` output says so | Summarize first, then offer removal at the end |
| Pasting raw logs or project names into an issue | Scrub to placeholders and get approval before posting |
