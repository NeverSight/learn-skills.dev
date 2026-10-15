---
name: android-build-gradle
description: >
  Android アプリ開発 (Kotlin) の Gradle ビルドシステムリファレンス。
  Android Gradle Plugin (AGP), Kotlin DSL (build.gradle.kts),
  version catalog, KSP, R8/ProGuard, App Bundle, baseline profile。
user-invocable: false
---

# Android Gradle Plugin (AGP) ビルドリファレンス

Android Gradle Plugin (AGP) 公式ドキュメントの主要トピックを網羅したスキル。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/android-build-gradle/
  SKILL.md
  references/
    build-config/
      README.md
      settings-gradle.md
      root-build-gradle.md
      module-build-gradle.md
      plugins-block.md
      android-block.md
      default-config.md
      build-types.md
      product-flavors.md
      build-features.md
      source-sets.md
      compile-kotlin-options.md
      signing-configs.md
      packaging.md
      test-options.md
      lint-config.md
      gradle-properties.md
      local-properties.md
      multidex.md
      native-16kb-page-size.md
      native-dependencies-prefab.md
      native-build-cmake.md
    dependencies/
      README.md
      dependency-configurations.md
      dependency-coordinates.md
      repositories.md
      version-catalog.md
      compose-bom.md
      dependency-exclusion.md
      viewing-dependencies.md
      ksp-vs-kapt.md
      migrate-to-catalogs.md
      variant-specific-dependencies.md
      dependency-verification.md
    optimize-release/
      README.md
      shrink-code.md
      proguard-rules.md
      r8-troubleshooting.md
      shrink-resources.md
      app-bundle.md
      bundle-config.md
      apk-splits.md
      app-signing.md
      debuggable-obfuscation.md
      baseline-profiles.md
      build-variant-optimization.md
      release-checklist.md
      native-debug-symbols.md
      dynamic-feature-modules.md
    publish-library/
      README.md
      prep-library-release.md
      publication-variants.md
      upload-library.md
      test-fixtures-publishing.md
      fused-library.md
    migrate-troubleshoot/
      README.md
      build-speed-optimization.md
      build-cache-configuration-cache.md
      migrate-to-ksp.md
      migrate-to-kotlin-dsl.md
      agp-upgrade-assistant.md
      agp-gradle-version-compatibility.md
      jdk-configuration.md
      namespace-migration.md
      manifest-merger-conflicts.md
      build-analyzer.md
      dependency-resolution-errors.md
      migrate-to-built-in-kotlin.md
      custom-build-logic.md
      sdk-upgrade-assistant.md
      agp-kotlin-d8-r8-compatibility.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| settings.gradle.kts / build.gradle.kts の構成を知りたい | build-config | [references/build-config/README.md](references/build-config/README.md) |
| android {} ブロック・defaultConfig・buildTypes・productFlavors を設定したい | build-config | [references/build-config/README.md](references/build-config/README.md) |
| buildFeatures（Compose/ViewBinding）・sourceSets・signingConfigs を設定したい | build-config | [references/build-config/README.md](references/build-config/README.md) |
| gradle.properties / local.properties / lint 設定を確認したい | build-config | [references/build-config/README.md](references/build-config/README.md) |
| implementation / api / ksp / kapt などの dependency configuration を使いたい | dependencies | [references/dependencies/README.md](references/dependencies/README.md) |
| version catalog (libs.versions.toml) や Compose BOM でバージョン管理したい | dependencies | [references/dependencies/README.md](references/dependencies/README.md) |
| 依存関係の除外・解決や `./gradlew dependencies` の見方を知りたい | dependencies | [references/dependencies/README.md](references/dependencies/README.md) |
| R8/ProGuard によるコード圧縮・難読化を設定したい | optimize-release | [references/optimize-release/README.md](references/optimize-release/README.md) |
| App Bundle / APK splits / baseline profile でリリース最適化したい | optimize-release | [references/optimize-release/README.md](references/optimize-release/README.md) |
| 署名設定・リリースチェックリストを確認したい | optimize-release | [references/optimize-release/README.md](references/optimize-release/README.md) |
| Android ライブラリのリリース準備・メタデータを設定したい | publish-library | [references/publish-library/README.md](references/publish-library/README.md) |
| ライブラリを Maven に publish したい（publication variants / upload） | publish-library | [references/publish-library/README.md](references/publish-library/README.md) |
| fused library や test fixtures を publish したい | publish-library | [references/publish-library/README.md](references/publish-library/README.md) |
| ビルド速度・build cache / configuration cache を改善したい | migrate-troubleshoot | [references/migrate-troubleshoot/README.md](references/migrate-troubleshoot/README.md) |
| kapt から KSP へ、Groovy から Kotlin DSL へ移行したい | migrate-troubleshoot | [references/migrate-troubleshoot/README.md](references/migrate-troubleshoot/README.md) |
| AGP アップグレードやマニフェストマージ・依存関係解決エラーに対処したい | migrate-troubleshoot | [references/migrate-troubleshoot/README.md](references/migrate-troubleshoot/README.md) |

テストの書き方は `android-testing`、マニフェストとリソースの仕様は `android-platform-core` の担当。
