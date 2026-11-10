---
name: minecraft-ci-release
description: "Set up CI/CD pipelines, automated publishing, and release workflows for Minecraft mods and plugins for 1.21.x. Covers GitHub Actions matrix builds for NeoForge and Fabric, automated publishing to Modrinth (via minotaur Gradle plugin) and CurseForge (via curseforgegradle), GitHub Releases with JAR artifacts, semantic versioning conventions for Minecraft mods, CHANGELOG generation, Dependabot for Gradle wrapper and plugin updates, build caching with gradle/actions/setup-gradle, pull request checks, and release tag workflows. Also covers Paper plugin CI with shadow JAR builds. Use when the task is CI/CD pipelines, release automation, artifact publishing, versioning, or release governance for Minecraft mods or plugins."
---

# Minecraft CI / Release Skill

## Workflow Overview

```
PR opened → build + test checks
main branch push → build artifacts
Tag push (v*) → build + publish to Modrinth + CurseForge + GitHub Releases
```

### Routing Boundaries
- `Use when`: the task is CI/CD pipelines, release automation, artifact publishing, versioning, or release governance.
- `Do not use when`: the task is implementing gameplay/plugin/mod features (`minecraft-modding`, `minecraft-plugin-dev`, `minecraft-datapack`).
- `Do not use when`: the task is server runtime operations and infrastructure tuning (`minecraft-server-admin`).
- `Do not use when`: the task is writing the tests themselves (`minecraft-testing`).

---

## Versioning Convention

Minecraft mod versions follow: `{mod_version}+{mc_version}`

```
1.0.0+1.21.11  ← mod 1.0.0 for MC 1.21.11
1.2.3+1.21.11
2.0.0+1.21.11
```

Git tag format: `v1.0.0` (mod version only, not MC version in the tag).

---

## Core CI Workflow (NeoForge + Fabric)

### `.github/workflows/build.yml`
```yaml
name: Build

on:
  push:
    branches: ["main", "develop"]
  pull_request:
    branches: ["main"]

permissions:
  contents: read

jobs:
  build:
    name: Build (${{ matrix.platform }})
    runs-on: ubuntu-latest
    strategy:
      matrix:
        platform: [neoforge, fabric]
      fail-fast: false

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Java 21
        uses: actions/setup-java@v4
        with:
          java-version: "21"
          distribution: "temurin"

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v3
        with:
          cache-read-only: ${{ github.ref != 'refs/heads/main' }}

      - name: Grant execute permission for gradlew
        run: chmod +x gradlew

      - name: Build (${{ matrix.platform }})
        run: ./gradlew :${{ matrix.platform }}:build --no-daemon

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: mod-${{ matrix.platform }}-${{ github.sha }}
          path: ${{ matrix.platform }}/build/libs/*.jar
          if-no-files-found: error
```

---

## Release Workflow (with Publishing)

### `.github/workflows/release.yml`
```yaml
name: Release

on:
  push:
    tags:
      - "v*"

permissions:
  contents: write      # for creating GitHub releases

jobs:
  release:
    name: Release
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Java 21
        uses: actions/setup-java@v4
        with:
          java-version: "21"
          distribution: "temurin"

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v3

      - name: Grant execute permission for gradlew
        run: chmod +x gradlew

      - name: Extract version from tag
        id: version
        run: echo "MOD_VERSION=${GITHUB_REF_NAME#v}" >> $GITHUB_OUTPUT

      - name: Build all platforms
        run: ./gradlew build --no-daemon

      - name: Publish to Modrinth & CurseForge
        run: ./gradlew publishMods --no-daemon
        env:
          MODRINTH_TOKEN: ${{ secrets.MODRINTH_TOKEN }}
          CURSEFORGE_TOKEN: ${{ secrets.CURSEFORGE_TOKEN }}

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          files: |
            fabric/build/libs/*.jar
            neoforge/build/libs/*.jar
          generate_release_notes: true
          draft: false
          prerelease: ${{ contains(github.ref_name, '-alpha') || contains(github.ref_name, '-beta') || contains(github.ref_name, '-rc') }}
```

---

## Paper Plugin CI

### `.github/workflows/build.yml` (plugin)
```yaml
name: Build

on:
  push:
    branches: ["main"]
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: "21"
          distribution: "temurin"
      - uses: gradle/actions/setup-gradle@v3
      - run: chmod +x gradlew
      - run: ./gradlew shadowJar --no-daemon
      - uses: actions/upload-artifact@v4
        with:
          name: plugin-${{ github.sha }}
          path: build/libs/*.jar

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: "21"
          distribution: "temurin"
      - uses: gradle/actions/setup-gradle@v3
      - run: ./gradlew test --no-daemon
```

---

## Modrinth Publishing (minotaur)

### `build.gradle.kts` (root or platform-specific)
```kotlin
plugins {
    id("com.modrinth.minotaur") version "2.8.7"
}

// === Fabric subproject ===
modrinth {
    token.set(System.getenv("MODRINTH_TOKEN") ?: "")
    projectId.set("YOUR-PROJECT-ID")    // from modrinth.com project slug or ID

    versionNumber.set("${project.version}")
    versionType.set("release")          // release | beta | alpha

    uploadFile.set(tasks.remapJar)      // the JAR to upload

    gameVersions.addAll("1.21.11")
    loaders.addAll("fabric")

    changelog.set(
        rootProject.file("CHANGELOG.md").readText()
            .substringAfter("## [${project.version}]")
            .substringBefore("\n## [")
            .trim()
    )

    dependencies {
        required.project("fabric-api")
        // optional.project("some-optional-mod")
    }
}
```

### Combined Fabric + NeoForge publish task (root-level)
```kotlin
// root build.gradle.kts
tasks.register("publishMods") {
    dependsOn(":fabric:modrinth", ":neoforge:modrinth")
    dependsOn(":fabric:curseforge", ":neoforge:curseforge")
    group = "publishing"
    description = "Publish all platforms to Modrinth and CurseForge"
}
```

---

## CurseForge Publishing

### `build.gradle.kts`
```kotlin
plugins {
    id("net.darkhax.curseforgegradle") version "1.1.25"
}

tasks.register<net.darkhax.curseforgegradle.TaskPublishCurseForge>("curseforge") {
    apiToken = System.getenv("CURSEFORGE_TOKEN") ?: ""

    val cf = upload(PROJECT_ID, tasks.named("remapJar"))  // or shadowJar
    cf.changelogType = "markdown"
    cf.changelog = rootProject.file("CHANGELOG.md").readText()
        .substringAfter("## [${project.version}]")
        .substringBefore("\n## [")
        .trim()

    cf.releaseType = "release"
    cf.addGameVersion("1.21.11")
    cf.addModLoader("Fabric")     // "NeoForge" for NeoForge subproject
    cf.addRequirement("fabric-api")
    // cf.addJavaVersion("Java 21")

    // Replace PROJECT_ID with your numeric CurseForge project ID
}
```

> Replace `PROJECT_ID` with your actual numeric CurseForge project ID (found in project settings).

---

## `gradle.properties` Secrets Pattern

Never hardcode tokens. Read them from environment:

```properties
# gradle.properties (committed)
mod_id=mymod
mod_version=1.0.0
minecraft_version=1.21.11
modrinth_project_id=AABBCCDD
curseforge_project_id=123456

# DO NOT commit tokens
# Set these as GitHub repo secrets:
# MODRINTH_TOKEN, CURSEFORGE_TOKEN
```

---

## Semantic Versioning for Mods

| Change | Version bump |
|--------|-------------|
| New features, no breaking changes | Minor: `1.1.0` |
| Bug fixes only | Patch: `1.0.1` |
| API/config breaking changes | Major: `2.0.0` |
| Minecraft version update | Keep mod version, change `+1.21.11` suffix |
| Pre-release | `1.0.0-beta.1`, `1.0.0-rc.1` |

---

## CHANGELOG.md Convention

```markdown
# Changelog

## [1.1.0] — 2025-06-01
### Added
- New `/kit` command
- PDC-based kill tracker

### Fixed
- Death message not appearing on Paper 1.21.11

## [1.0.0] — 2025-05-01
### Added
- Initial release
```

Automate CHANGELOG parsing in Gradle (as shown above in modrinth block) by extracting
the section between version headers.

---

## Dependabot Configuration

### `.github/dependabot.yml`
```yaml
version: 2
updates:
  - package-ecosystem: "gradle"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      gradle-plugins:
        patterns:
          - "com.gradleup.shadow"
          - "dev.architectury.loom"
          - "com.modrinth.minotaur"
          - "net.darkhax.curseforgegradle"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

---

## Build Caching Best Practices

```yaml
# In all workflow jobs:
- name: Setup Gradle
  uses: gradle/actions/setup-gradle@v3
  with:
    # Read-only cache on PRs, read-write on main
    cache-read-only: ${{ github.event_name == 'pull_request' }}
    # Cache Minecraft assets (speeds up loom tasks by minutes)
    gradle-home-cache-includes: |
      caches
      notifications
      .gradle/loom-cache
```

---

## Branch Protection + Required Checks

Recommended GitHub branch protection for `main`:
- Require status checks: `build (fabric)`, `build (neoforge)`, `test`
- Require linear history (squash/rebase merges)
- Require signed commits (optional but recommended for release workflows)

---

## Tag and Release Script

```bash
#!/usr/bin/env bash
# scripts/release.sh <version>
# Usage: ./scripts/release.sh 1.1.0
set -euo pipefail

VERSION="${1:?Usage: release.sh <version>}"

# Update gradle.properties
sed -i "s/^mod_version=.*/mod_version=${VERSION}/" gradle.properties

# Stage and commit
git add gradle.properties
git commit -m "chore: release v${VERSION}"

# Tag
git tag "v${VERSION}"

echo "Created commit and tag v${VERSION}"
echo "Push with: git push && git push --tags"
```

## Workflow Snippet Validator

Use the bundled validator script to keep `SKILL.md` workflow snippets copy-paste safe:

```bash
# Run from the installed skill directory:
./scripts/validate-workflow-snippets.sh --root .

# Strict mode treats warnings as failures:
./scripts/validate-workflow-snippets.sh --root . --strict
```

The validator is bundled and self-contained. Run it from a copied `.agents/`,
`.codex/`, or `.claude/` `minecraft-ci-release` skill directory without relying
on repo-root `node_modules`.

What it checks:
- YAML snippet structure for workflow-like blocks (`name`, `on`, `jobs`)
- Unresolved placeholder tokens and suspicious glob patterns
- `${{ secrets.* }}` usage stays consistent with secrets documented in this file

---

## References

- GitHub Actions: https://docs.github.com/en/actions
- minotaur (Modrinth): https://github.com/modrinth/minotaur
- curseforgegradle: https://github.com/Darkhax-Minecraft/CurseForgeGradle
- softprops/action-gh-release: https://github.com/softprops/action-gh-release
- gradle/actions: https://github.com/gradle/actions
- Modrinth API docs: https://docs.modrinth.com/
