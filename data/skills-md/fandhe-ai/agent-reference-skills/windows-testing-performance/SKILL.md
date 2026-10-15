---
name: windows-testing-performance
description: >
  Windows アプリ開発 (WinUI 3 / Windows App SDK) のテスト・パフォーマンス・
  アクセシビリティ・スレッドリファレンス。MSTest, xUnit, NUnit, WinAppDriver,
  Appium, Playwright, WebView2 テスト, WACK 認定, MSIX サイドローディング, CI。
  プロファイリング, WPT, WPA, GC, 起動性能, XAML レイアウト/読み込み最適化,
  ListView/GridView 仮想化, DispatcherQueue。UI Automation, AutomationProperties,
  automation peers, キーボード操作性, ハイコントラストテーマ, Narrator。
  DispatcherQueue, DispatcherQueueTimer, WinRT 非同期パターン, async/await,
  ConfigureAwait, スレッドプール, STA/MTA, デッドロック回避, バックグラウンドタスク。
user-invocable: false
---

# Windows テスト・パフォーマンス リファレンス

WinUI 3 / Windows App SDK アプリの単体テスト・UI テスト・認定・パフォーマンス最適化・
アクセシビリティ・スレッドモデルに関する公式ドキュメントを蒸留したリファレンス。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/windows-testing-performance/
  SKILL.md
  references/
    testing/
      README.md
      unit-testing-winui3.md
      unit-testing-non-winui.md
      ui-testing-winappdriver.md
      playwright-webview2-testing.md
      wack-certification.md
      wack-test-categories.md
      msix-sideloading.md
      loose-file-registration.md
      widgets-testing.md
      app-actions-testing.md
      ci-testing.md
      testing-troubleshooting.md
      device-portal.md
      plm-testing.md
      winapp-cli-debugging.md
      winapp-cli-ui-automation.md
      static-analysis-dotnet-cpp.md
      telemetry-crash-reporting.md
    performance/
      README.md
      choose-between-tools.md
      disk-memory.md
      improve-garbage-collection-performance.md
      power.md
      responsive.md
      keep-ui-thread-responsive.md
      winui-perf.md
      app-startup-performance.md
      mvvm-performance-tips.md
      optimize-animations-and-media.md
      optimize-file-access.md
      optimize-gridview-and-listview.md
      listview-and-gridview-data-optimization.md
      optimize-xaml-layout.md
      optimize-xaml-loading.md
      state-management.md
      profiling-tools.md
      xaml-analysis.md
      optimize-background-activity.md
      optimize-winrt-interop.md
    accessibility/
      README.md
      ui-automation-overview.md
      automation-properties.md
      basic-accessibility-information.md
      landmarks-and-headings.md
      automation-peers.md
      control-patterns-and-interfaces.md
      keyboard-accessibility.md
      focus-visuals.md
      high-contrast-themes.md
      accessible-text-requirements.md
      accessibility-testing.md
      accessibility-checklist.md
      accessibility-in-the-store.md
      system-button-narration.md
      ui-automation-tree-views.md
    threading/
      README.md
      dispatcher-queue.md
      dispatcher-queue-controller.md
      dispatcher-queue-timer.md
      core-dispatcher-migration.md
      winrt-async-patterns.md
      async-await-configureawait.md
      thread-pool.md
      apartment-model.md
      ui-thread-updates.md
      deadlock-avoidance.md
      background-tasks.md
      agile-objects-marshaling.md
  scripts/
    README.md
    install.md
    winapp-cli.md
    wack.md
    sideloading.md
    ci.md
    device-portal.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| MSTest / xUnit / NUnit で単体テストを書きたい | testing | [references/testing/README.md](references/testing/README.md) |
| WinAppDriver / Appium / Playwright で UI テストを自動化したい | testing | [references/testing/README.md](references/testing/README.md) |
| WACK 認定・MSIX サイドローディング・CI でのテスト実行を設定したい | testing | [references/testing/README.md](references/testing/README.md) |
| 起動時間・メモリ・GC・XAML レイアウトを最適化したい | performance | [references/performance/README.md](references/performance/README.md) |
| WPT/WPA/Visual Studio Profiler でプロファイリングしたい | performance | [references/performance/README.md](references/performance/README.md) |
| ListView / GridView の仮想化・データ読み込みを最適化したい | performance | [references/performance/README.md](references/performance/README.md) |
| UI Automation 対応・AutomationProperties を設定したい | accessibility | [references/accessibility/README.md](references/accessibility/README.md) |
| キーボード操作性・フォーカス・ハイコントラストに対応したい | accessibility | [references/accessibility/README.md](references/accessibility/README.md) |
| Narrator でのアクセシビリティテスト・ストア申請要件を確認したい | accessibility | [references/accessibility/README.md](references/accessibility/README.md) |
| DispatcherQueue で UI スレッドに処理をマーシャリングしたい | threading | [references/threading/README.md](references/threading/README.md) |
| WinRT 非同期パターン・async/await・ConfigureAwait を扱いたい | threading | [references/threading/README.md](references/threading/README.md) |
| スレッドプール・アパートメントモデル・デッドロック回避・バックグラウンドタスクを実装したい | threading | [references/threading/README.md](references/threading/README.md) |
| Appium/WinAppDriver/Playwright のセットアップ・WACK 実行・サイドローディング・CI・Device Portal のコマンドを知りたい | scripts | [scripts/README.md](scripts/README.md) |

このスキルは WinUI 3 / Windows App SDK アプリのテスト・パフォーマンス・アクセシビリティ・スレッドに特化する。
コントロール API・レイアウト・データバインディング・パッケージング等は windows-winui-controls, windows-winui-ui, windows-app-sdk, windows-design, windows-data-storage, windows-platform-integration, windows-graphics-media, windows-ai, windows-packaging-publish, windows-interop-modernize が担当する。
