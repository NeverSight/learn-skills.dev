---
name: flutter-fix
description: Finds the root cause of a bug or crash in a Flutter app and fixes it, refactors code without changing behaviour, or upgrades packages, Dart and Flutter (with FVM) one step at a time. Use when asked to debug, fix or investigate an error or crash, refactor existing code, or upgrade packages, Dart or Flutter versions; for new functionality use flutter-feature.
license: Apache-2.0
---

# Flutter fix

Three kinds of work that change existing code without adding a feature. Pick one, say which, and do not mix them in one change.

## Steps

1. **Load the project rules** (`AGENTS.md`, project rules folders); project rules win over this skill. If there is no profile, read the files around the problem and go on; do not run `flutter-project-profile` for a small fix.
2. **Pick the mode and open its reference:**
   - **Bug or crash:** `references/debugging-playbook.md`.
   - **Refactor:** the rules below. No reference needed.
   - **Upgrade** (packages, Dart, Flutter, FVM pin): `references/upgrade-checklist.md` and `references/native-platform-requirements.md` (dated Gradle, AGP, Kotlin, Java, Xcode, 16 KB, target API, UIScene and SwiftPM facts).
   - Failures that appear only in a store build or in CI, or come from keys, consoles or fingerprints, start in `flutter-release` or `flutter-service-setup`.
3. **Bug: reproduce, find the cause, then fix.** Get the exact error text, the steps, the platform, the build mode and the versions; if the report is vague, ask for those (at most three questions) before searching the code. Read the whole error and stack trace, not the last line. State the cause with the evidence (file, line, log) before editing. If the app cannot be run, label the cause "found by reading, not reproduced", list the other plausible causes you could not rule out, and say what would confirm it (a log line, a debug print, DevTools); change code only if the developer agrees, since two readers of the same code can pick different causes. If you cannot find the cause, say what you ruled out and what you need (a log, a device, a build mode); do not patch around it.
4. **Make the smallest change that removes the cause.** Do not fix neighbouring things in the same change; list them instead. Never edit generated files; change the source and run code generation.
5. **Check.** Run `flutter analyze` (with `fvm` when `.fvmrc` exists). Re-run the reproduction steps if the app can be run, and say if it could not be. Tests only if the developer asks (`flutter-testing`); then a regression test for the bug is the natural one.
6. **Report:** cause (one or two lines with evidence), change (files), how it was checked and what was not, what else you noticed but left alone, and the risk to other places that use the same code.

## Refactor rules

- Behaviour stays the same. If a change would alter behaviour, stop and say so; it is a feature or a fix, not a refactor.
- Agree the scope first (which files, which pattern, what is out). Do it in small steps, and run the analyzer after each.
- Follow the project's written conventions, not new ones. Do not introduce a package, a state-management change or a folder-structure change unless that is the request.
- If there are no tests around the code, say that nothing proves the behaviour is unchanged, and offer characterization tests through `flutter-testing` before the change.
- Keep formatting-only and rename-only changes apart from logic changes so a reviewer can read them (`flutter-git` for commits).

## Rules

- Never claim a bug is fixed without saying how you checked. "Analyzer is clean" is not "bug fixed".
- Logs and crash reports can hold tokens, keys and personal data: redact them before quoting them in a report, a commit message or a file.
- Do not run destructive clean-ups (`flutter clean`, deleting `pubspec.lock`, `.dart_tool` or `Pods`) as a first guess; say what you are clearing and why.
- Do not upgrade anything during a bug fix or refactor, and do not fix bugs during an upgrade, unless the upgrade itself causes them.
- Ask before major-version upgrades, new packages, or changes to native files (`android/`, `ios/`); name what changes.
