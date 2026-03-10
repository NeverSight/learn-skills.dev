---
name: release-pub
description: A specialized workflow for releasing Dart and Flutter packages to pub.dev. Use when the user asks to "release", "publish to pub.dev", or "create a release" for a Dart/Flutter project.
---

# `release-pub` Skill

This skill is a specialized release workflow for Dart and Flutter packages published to pub.dev (including Dart CLI tools). It relies on a local helper script (`release_helper`) to safely manipulate `pubspec.yaml` and `CHANGELOG.md`.

## Official Documentation

For detailed information on automated publishing, refer to the official Dart documentation:
[Automated publishing of packages to pub.dev](https://dart.dev/tools/pub/automated-publishing)

> [!CAUTION]
> **Immutable Tags**: NEVER delete, modify, or re-push a Git tag that has already been published to pub.dev. Pub.dev entries are immutable. If a mistake is found after publishing, you must publish a new version (e.g., a patch release) instead of attempting to overwrite the existing tag.

## Workflow Overview

Follow these steps precisely:

### 0. Initial Setup Verification (One-time only)

If this is the first time the package is being published via GitHub Actions, ensure the user has configured OIDC on pub.dev and added the workflow file:

1. **Configure pub.dev**:
   - Advise the user to access `https://pub.dev/packages/<package_name>/admin`.
   - Find the **Automated publishing** section and click **Enable publishing from GitHub Actions**.
   - Recommend setting the **Repository** to the current repository (`owner/repo`).
   - Set the **Tag pattern**:
     - For single package repositories: `v{{version}}` (recommended) or `{{version}}`.
     - For monorepos: `package_name-v{{version}}`.
   - **Security Hardening (Optional but recommended)**: Mention the **Require GitHub Actions environment** option to restrict publishing to specific users/approvers via GitHub Deployment Environments.

2. **Add GitHub Actions Workflow**:
   - Ensure `.github/workflows/publish.yml` exists with the following content (adjust the tag pattern if necessary):

```yaml
name: Publish to pub.dev

on:
  push:
    tags:
      - 'v[0-9]+.[0-9]+.[0-9]+*' # Align with the tag-pattern on pub.dev (e.g., 'v{{version}}')

jobs:
  publish:
    permissions:
      id-token: write # Essential for OIDC authentication
    uses: dart-lang/setup-dart/.github/workflows/publish.yml@v1
    # with:
    #   working-directory: path/to/package # Required if the package is not in the root
```

Wait for the user to confirm the setup is complete before proceeding with the first automated release.

### 1. Pre-release Checks

- Check if there are any uncommitted changes: `git status -s`. If there are, tell the user to commit or stash them before proceeding.
- **README / Docs Update Check**: Scan the recent changes. If there are new features or changed options, remind the user to check if `README.md` or other documentation needs updating before releasing.
- **CRITICAL**: Run the appropriate formatter, analyzer, and tests based on the project type:
  - For Dart packages: `dart format .`, `dart analyze`, and `dart test`
  - For Flutter packages: `flutter format .` (or `dart format .`), `flutter analyze`, and `flutter test`
    - **[MANDATORY]**: Resolve **ALL** analyzer issues (errors, warnings, and **info** level lints) before proceeding. Do not ignore "info" level issues unless they are explicitly documented as unavoidable.
    - If there are unresolved issues, report them and ask the user to fix them (or offer to fix them if they are straightforward).
- **CRITICAL**: Run the pre-publish dry-run:
  - For Dart packages: `dart pub publish --dry-run`
  - For Flutter packages: `flutter pub publish --dry-run`
    If warnings or errors appear (other than expected ones that can be ignored), report them and ask for user confirmation to proceed.

### 2. Analyze Changes & Plan Release

- Find the last tag: `LAST_TAG=$(git tag --sort=-v:refname | head -1)`
- Analyze the commits since the last tag: `git log ${LAST_TAG}..HEAD --oneline`
- Determine if a tag prefix is used:
  - Check the format of the `$LAST_TAG`. If it starts with `v` (e.g., `v1.2.3`), use `v` as the prefix for the new tag.
  - If no tags exist (first release), default to using the `v` prefix (`TAG_PREFIX="v"`).
  - Otherwise, follow the existing pattern (no prefix if `$LAST_TAG` is just a version string).
- Determine the bump type (`major`, `minor`, `patch`) based on Conventional Commits:
  - `BREAKING CHANGE:` or `<type>!:` -> major (or minor if version is `< 1.0.0` but follow the user's lead on pre-1.0.0 breaking changes).
  - `feat:` -> minor
  - `fix:`, `docs:`, `chore:`, `refactor:`, `perf:` etc. -> patch
- Generate markdown for `CHANGELOG.md` notes describing the changes. Generate the notes entirely in **English**. _DO NOT include the `## [version] - [date]` title header in the notes as the script adds that automatically._
- **Generate Preview (Dry-Run)**: Present a clear preview of the upcoming release to the user before making any file changes.
  - Show the version bump recommendation (e.g., `1.2.3 -> 1.3.0 (Recommended: feat=minor)`) and offer other valid SemVer alternatives (e.g. `1.2.4`, `2.0.0`) in case they want a different bump.
  - List the categorized commits that will be included in the release.
  - Show the preview text of the upcoming `CHANGELOG.md` entry.

### 3. Execution using Helper Script

Use the bundled Dart CLI script to apply changes safely. The script is located at `.agents/skills/release-pub/scripts/release_helper`.

1. **Prepare Release (Version Bump & Changelog)**:
   Determine the bump type (`major`, `minor`, `patch`) and the notes as analyzed in Step 2.

   ```bash
   dart run .agents/skills/release-pub/scripts/release_helper/bin/release_helper.dart prepare <type> --notes "
   ### Features
   - ...

   ### Bug Fixes
   - ...
   "
   ```

2. **Extract New Version**:
   Read the `pubspec.yaml` to find the newly updated version string (e.g. `1.2.3`). Let's call this `$NEW_VERSION`.

### 4. User Confirmation

Ask the user to confirm the prepared release based on the generated preview in Step 2:

- First present the version change options (e.g., "1.3.0 (Recommended)", "1.2.4", "2.0.0").
- Once the user chooses the version, proceed to update the files locally via Step 3.
- After running the execution helpers, show the user the Git diff (`git diff`) and ask: "Ready to create release commit and tag (v$NEW_VERSION)?"
  Wait for explicit confirmation.

### 5. Git & GitHub Operations

Once the user confirms:

1. Stage the files:
   ```bash
   git add pubspec.yaml CHANGELOG.md
   ```
2. Commit:
   ```bash
   git commit -m "chore: release v$NEW_VERSION"
   ```
   _Note: Do NOT add a `Co-Authored-By` line. This is a release commit, not a code contribution._
3. Tag:
   ```bash
   git tag ${TAG_PREFIX}$NEW_VERSION
   ```
4. Push:
   ```bash
   git push origin main
   git push origin ${TAG_PREFIX}$NEW_VERSION
   ```
5. Create GitHub Release:
   Save the notes to a temporary file, e.g., `/tmp/release_notes.md`, then:
   ```bash
   gh release create ${TAG_PREFIX}$NEW_VERSION --title "${TAG_PREFIX}$NEW_VERSION" --notes-file /tmp/release_notes.md
   rm /tmp/release_notes.md
   ```

Finally, report that the release is complete and that GitHub Actions will automatically handle pushing to `pub.dev`.
