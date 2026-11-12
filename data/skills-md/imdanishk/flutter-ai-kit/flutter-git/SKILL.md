---
name: flutter-git
description: Safe git workflow for Flutter work - branch names, commit messages, pull request descriptions, and what must never be committed (keystores, API keys, env files). Use when asked to commit, branch, push, open or describe a pull request, or clean up history.
license: Apache-2.0
---

# Flutter git

## Rules (always)

- Do not commit, push, tag or open a pull request unless the developer asked. Never force-push, and never rewrite history that is already pushed, unless the developer asks for that exact action.
- Follow the project first: read `AGENTS.md`, `CONTRIBUTING.md`, the PR template and `git log --oneline -20` for the existing branch and message style. Only if there is none, use the defaults below.
- Stage by name (`git add path/to/file`), not `git add -A` or `git add .`. Run `git status` and read what is staged before every commit.
- Do not commit secrets or machine files. Check `.gitignore` covers them before the first commit of a task (list below); if one is already tracked, say so and stop rather than deleting history.
- One logical change per commit. Do not mix a refactor with a behaviour change or a dependency upgrade.
- Generated files (`*.g.dart`, `*.freezed.dart`, `*.gr.dart`, `*.config.dart`): commit them only if the project already tracks them. Check `.gitignore` and `git ls-files | grep freezed` first.
- Respect the `Developer preferences` list in `AGENTS.md`.

## Never commit

Android keystores (`*.jks`, `*.keystore`) and `key.properties`; Apple `.p8` API keys, `.p12` certificates and provisioning profiles; Play service-account JSON; `.env*` files other than an `.env.example` with empty values; any API key or token in source (use build-time defines or a secrets mechanism; see the `flutter-service-setup` skill). Machine-local and generated files: `android/local.properties` (SDK paths and the user's name), `android/.gradle/`, `ios/Pods/`, `xcuserdata/`, `ios/Flutter/Generated.xcconfig`, `ios/Flutter/ephemeral/`, `GeneratedPluginRegistrant.*`. Flutter's own project template ignores all of these (checked in the `flutter/flutter` repository on 2026-11-05); if a project tracks them, say so and stop. `google-services.json` and `GoogleService-Info.plist` hold identifiers, not secrets, and many teams do commit them; ask what the project does, and keep one per environment.

## Defaults (when the project has none)

- **Branches:** `<type>/<short-topic>`, for example `feature/invite-list`, `fix/login-crash`, `chore/upgrade-agp`. Branch from the default branch (or the project's integration branch, if its docs name one).
- **Commits:** the Conventional Commits shape `type(scope): summary`, for example `feat(invites): add paging to the invitee list`. Types: `feat`, `fix`, `refactor`, `docs`, `chore`, `build`, `ci`. Imperative mood, summary under about 72 characters, a body that says why when the reason is not obvious. Mark a breaking change with `!` after the type or a `BREAKING CHANGE:` footer. (The spec is at conventionalcommits.org; its text was not re-read when this skill was written.)
- **Pull request description:** what changed and why (two or three lines); how to try it (screens, flavor, account); what the developer must do by hand (keys, console settings, backend); screenshots for UI changes; rule conflicts, if any.
- **Version tags:** tag a release only when asked. If the project versions in `pubspec.yaml` (`1.4.0+27`), the part before `+` is the version name and the part after is the build number; every store upload needs a higher build number than the last one.

## Before opening a pull request

Run the project's analyzer, and the formatter on the files you changed only (with the `fvm` prefix when `.fvmrc` exists), read your own diff once, and list anything you did not check. If a `flutter-review` pass was not done by someone other than the author of the change, say that in the description.
