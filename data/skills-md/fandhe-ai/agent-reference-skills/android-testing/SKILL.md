---
name: android-testing
description: >
  Android アプリ開発 (Kotlin) のテストリファレンス。JUnit4, Espresso, テストピラミッド。
  テストダブル, Mockito, MockK, Truth, Robolectric, coroutines/Flow/ViewModel テスト。
  AndroidJUnit4, ActivityScenario, FragmentScenario, UiAutomator, AndroidTestOrchestrator。
  createComposeRule, Compose UI テスト同期。
user-invocable: false
---

# Android Testing リファレンス

Android アプリ (Kotlin) のテストに関する公式ドキュメントを蒸留したスキル。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/android-testing/
  SKILL.md
  references/
    fundamentals-local/
      README.md
      test-pyramid.md
      test-dependencies.md
      junit4-basics.md
      test-doubles.md
      mockito.md
      mockk.md
      truth.md
      robolectric.md
      coroutines-testing.md
      flow-testing.md
      viewmodel-testing.md
      instanttaskexecutorrule.md
      testable-design.md
    instrumented/
      README.md
      androidjunit4-test-runner.md
      set-up-project.md
      instrumentationregistry.md
      applicationprovider.md
      activityscenario.md
      activityscenariorule.md
      fragmentscenario.md
      servicetestrule.md
      uiautomator.md
      test-filter-annotations.md
      grantpermissionrule.md
      androidtestorchestrator.md
      screenshot-testing.md
      gradle-managed-devices.md
      test-stability.md
      content-provider-testing.md
    espresso/
      README.md
      onview.md
      viewinteraction.md
      viewmatchers.md
      viewactions.md
      viewassertions.md
      ondata.md
      recyclerviewactions.md
      global-actions.md
      idling-resource.md
      intents.md
      web.md
      accessibility-checks.md
      custom-matchers-actions.md
      best-practices.md
      recipes.md
      espresso-device.md
      contrib-actions.md
      multiprocess.md
    compose-testing/
      README.md
      compose-test-rule.md
      finders.md
      semantics-matcher.md
      assertions.md
      actions.md
      semantics-node-interaction.md
      print-to-log.md
      synchronization.md
      test-tag-usage.md
      espresso-interop.md
      screenshot-testing.md
      preview-screenshot-testing.md
      accessibility-testing.md
      state-restoration-tester.md
      device-configuration-override.md
      compose-testing-v2.md
      common-patterns.md
      debug.md
    performance-testing/
      README.md
      compilation-mode.md
      macrobenchmark-metrics.md
      macrobenchmark-rule.md
      microbenchmark-rule.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| テストピラミッド・テスト戦略・`test/` と `androidTest/` の使い分けを知りたい | fundamentals-local | [references/fundamentals-local/README.md](references/fundamentals-local/README.md) |
| JUnit4 の `@Test` / `@Before` / テストダブル・Mockito・MockK でユニットテストを書きたい | fundamentals-local | [references/fundamentals-local/README.md](references/fundamentals-local/README.md) |
| Truth でアサーションを書きたい、Robolectric で JVM 上に Android テストを実行したい | fundamentals-local | [references/fundamentals-local/README.md](references/fundamentals-local/README.md) |
| coroutines / Flow / ViewModel のテストを書きたい（`runTest`, `TestDispatcher`） | fundamentals-local | [references/fundamentals-local/README.md](references/fundamentals-local/README.md) |
| `AndroidJUnit4` / `InstrumentationRegistry` / `ApplicationProvider` で計装テストを構築したい | instrumented | [references/instrumented/README.md](references/instrumented/README.md) |
| `ActivityScenario` / `FragmentScenario` でライフサイクルを制御したい | instrumented | [references/instrumented/README.md](references/instrumented/README.md) |
| `UiAutomator` でアプリ横断 UI 操作をしたい、`GrantPermissionRule` で権限を付与したい | instrumented | [references/instrumented/README.md](references/instrumented/README.md) |
| `AndroidTestOrchestrator` / Gradle Managed Devices でテスト実行を分離・スケールしたい | instrumented | [references/instrumented/README.md](references/instrumented/README.md) |
| `Espresso.onView` / `ViewMatchers` / `ViewActions` / `ViewAssertions` で View 系 UI をテストしたい | espresso | [references/espresso/README.md](references/espresso/README.md) |
| `RecyclerViewActions` / `IdlingResource` で非同期・リスト UI をテストしたい | espresso | [references/espresso/README.md](references/espresso/README.md) |
| Espresso-Intents / Espresso-Web で Intent や WebView をテストしたい | espresso | [references/espresso/README.md](references/espresso/README.md) |
| `createComposeRule` / finder / `SemanticsMatcher` で Compose UI をテストしたい | compose-testing | [references/compose-testing/README.md](references/compose-testing/README.md) |
| Compose のアサーション・アクション・テスト同期（`waitForIdle` 等）を制御したい | compose-testing | [references/compose-testing/README.md](references/compose-testing/README.md) |
| Compose と Espresso/UiAutomator を相互運用したい、スクリーンショットテストを書きたい | compose-testing | [references/compose-testing/README.md](references/compose-testing/README.md) |
| Compose テストの典型パターン（composable の分離・状態到達方法）を知りたい、semantics tree をデバッグしたい | compose-testing | [references/compose-testing/README.md](references/compose-testing/README.md) |
| `MacrobenchmarkRule` で起動・スクロール・アニメーションの性能を計測したい | performance-testing | [references/performance-testing/README.md](references/performance-testing/README.md) |
| `BenchmarkRule` でホットパスをマイクロベンチマークしたい | performance-testing | [references/performance-testing/README.md](references/performance-testing/README.md) |
| `CompilationMode` / `Metric` で計測条件と取得指標を制御したい | performance-testing | [references/performance-testing/README.md](references/performance-testing/README.md) |
| Hilt のテストをしたい | - | android-architecture スキルの担当 |
| Room のテストをしたい | - | android-data スキルの担当 |
| WorkManager のテストをしたい | - | android-background-work スキルの担当 |
