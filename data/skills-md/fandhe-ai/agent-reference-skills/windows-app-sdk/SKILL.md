---
name: windows-app-sdk
description: >
  Windows アプリ開発 (WinUI 3 / Windows App SDK) のライフサイクル・ウィンドウ・
  通知・リソース・ウィジェット・配置リファレンス。AppInstance, 単一インスタンス化,
  RichActivation, PowerManager、AppWindow, AppWindowPresenter, OverlappedPresenter,
  タイトルバーカスタマイズ, DisplayArea, Win32 相互運用、AppNotification, Toast,
  PushNotificationManager, バッジ通知、ResourceManager, MRT, PRI リソース,
  多言語ローカライズ、WidgetProvider, WidgetManager, アダプティブカード、
  MSIX パッケージ配置, 自己完結型デプロイ, DeploymentManager, リリースチャネル。
user-invocable: false
---

# Windows App SDK リファレンス

WinUI 3 / Windows App SDK のアプリライフサイクル・ウィンドウ管理・通知・リソース管理・ウィジェット・配置に関する公式ドキュメントの主要 API を網羅したスキル。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/windows-app-sdk/
  SKILL.md
  references/
    lifecycle/
      README.md
      application.md
      app-instance.md
      app-activation-arguments.md
      rich-activation.md
      single-instancing.md
      power-manager.md
      focus-session.md
      app-restore.md
    windowing/
      README.md
      windowing-overview.md
      app-window.md
      app-window-presenter.md
      overlapped-presenter.md
      compact-overlay-presenter.md
      full-screen-presenter.md
      app-window-titlebar.md
      title-bar-customization.md
      display-area.md
      display-area-watcher.md
      window-id.md
      xaml-window.md
      win32-interop.md
      multiple-windows.md
    notifications/
      README.md
      app-notification-manager.md
      app-notification.md
      app-notification-builder.md
      app-notification-activated-event-args.md
      toast-content-schema.md
      push-notification-manager.md
      push-notification-channel.md
      push-notification-received-event-args.md
      badge-notifications.md
      app-notification-collections.md
      notification-listener.md
      app-notification-scheduled.md
    resources-mrt/
      README.md
      resource-manager.md
      resource-context.md
      resource-map.md
      resource-candidate.md
      resource-loader.md
      resource-qualifiers.md
      resources-pri-makepri.md
      localize-strings.md
      dwritecore.md
    widgets/
      README.md
      iwidgetprovider.md
      iwidgetprovider2.md
      widgetmanager.md
      widgetcontext.md
      widgetinfo.md
      widgetupdaterequestoptions.md
      widget-provider-manifest.md
      implement-widget-provider.md
      widgets-create-a-template.md
      widget-header-customization.md
      feed-provider-manifest.md
      feedmanager.md
      ifeedprovider.md
      implement-feed-provider.md
      web-widget-providers.md
      widget-provider-activateapplication-protocol.md
      widget-provider-error-analytics-reporting.md
    deployment-versioning/
      README.md
      deployment-architecture.md
      deploy-overview.md
      deploy-packaged-apps.md
      deploy-unpackaged-apps.md
      deploy-self-contained-apps.md
      release-channels.md
      downloads.md
      system-requirements.md
      project-properties.md
      use-windows-app-sdk-run-time.md
      tutorial-unpackaged-deployment.md
      deploymentmanager.md
      deploymentresult.md
      check-windows-app-sdk-versions.md
      single-project-msix.md
      remove-windows-app-sdk-versions.md
      packagedependency.md
      packagedeploymentmanager.md
      runtimecompatibilityoptions.md
      runtimeinfo.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| AppInstance / 単一インスタンス化でアプリの多重起動を制御したい | lifecycle | [references/lifecycle/README.md](references/lifecycle/README.md) |
| RichActivation / AppActivationArguments でファイル・プロトコル・ショートカット起動を扱いたい | lifecycle | [references/lifecycle/README.md](references/lifecycle/README.md) |
| PowerManager で電源状態・バッテリー状態を監視したい | lifecycle | [references/lifecycle/README.md](references/lifecycle/README.md) |
| AppWindow / AppWindowPresenter でウィンドウの表示・サイズ・状態を制御したい | windowing | [references/windowing/README.md](references/windowing/README.md) |
| タイトルバーをカスタマイズしたい (AppWindowTitleBar, カスタムタイトルバー) | windowing | [references/windowing/README.md](references/windowing/README.md) |
| DisplayArea / マルチウィンドウ / Win32 相互運用でウィンドウ配置・HWND 連携を行いたい | windowing | [references/windowing/README.md](references/windowing/README.md) |
| AppNotification / Toast でローカル通知を表示したい | notifications | [references/notifications/README.md](references/notifications/README.md) |
| PushNotificationManager / PushNotificationChannel でプッシュ通知を実装したい | notifications | [references/notifications/README.md](references/notifications/README.md) |
| バッジ通知やトースト起動時のイベント引数を扱いたい | notifications | [references/notifications/README.md](references/notifications/README.md) |
| ResourceManager / MRT / PRI リソースでアプリリソースを管理したい | resources-mrt | [references/resources-mrt/README.md](references/resources-mrt/README.md) |
| 文字列・画像の多言語ローカライズ、リソース修飾子 (qualifiers) を扱いたい | resources-mrt | [references/resources-mrt/README.md](references/resources-mrt/README.md) |
| makepri でリソースパッケージを生成したい | resources-mrt | [references/resources-mrt/README.md](references/resources-mrt/README.md) |
| WidgetProvider を実装してウィジェットボード対応ウィジェットを作りたい | widgets | [references/widgets/README.md](references/widgets/README.md) |
| WidgetManager / WidgetInfo でウィジェットの更新・状態管理を行いたい | widgets | [references/widgets/README.md](references/widgets/README.md) |
| アダプティブカードテンプレートでウィジェット UI を作りたい | widgets | [references/widgets/README.md](references/widgets/README.md) |
| MSIX パッケージ配置 / 自己完結型デプロイでアプリを配布したい | deployment-versioning | [references/deployment-versioning/README.md](references/deployment-versioning/README.md) |
| DeploymentManager / DeploymentResult でランタイム初期化・更新を扱いたい | deployment-versioning | [references/deployment-versioning/README.md](references/deployment-versioning/README.md) |
| リリースチャネル・システム要件・プロジェクトプロパティを確認したい | deployment-versioning | [references/deployment-versioning/README.md](references/deployment-versioning/README.md) |

WinUI 3 のコントロール (Button / Grid / NavigationView / TextBox 等の XAML UI コンポーネント) は本スキルの対象外で、別スキルの担当。本スキルはアプリライフサイクル・ウィンドウ管理・通知・リソース・ウィジェット・配置といった Windows App SDK 固有のランタイム API に限定する。同名 API を持つ apple-swiftui / ark-ui / chakra-ui / fandhe-frontend / android-compose-* とは対象プラットフォームが異なり混同しないこと。
