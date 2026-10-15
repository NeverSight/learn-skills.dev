---
name: android-platform-core
description: >
  Android アプリ開発 (Kotlin) のプラットフォーム基盤リファレンス。
  Activity, Intent, Application, ContentProvider, AndroidManifest, androidx,
  ランタイム権限, NotificationCompat, WindowInsets, スプラッシュスクリーン,
  Glance ウィジェット。
user-invocable: false
---

# Android Platform Core リファレンス

Android プラットフォーム公式ドキュメント（app components / manifest / permissions / notifications / system UI / Glance）の主要 API を網羅したスキル。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/android-platform-core/
  SKILL.md
  references/
    app-components/
      README.md
      activity-lifecycle.md
      activity-result-contracts.md
      activity.md
      app-components-overview.md
      app-process-priority.md
      application-class.md
      background-activity-launch.md
      common-intents.md
      component-activity-compose.md
      configuration-changes.md
      content-provider-basics.md
      content-provider-creating.md
      intent-filters.md
      intent.md
      package-visibility.md
      parcelables-and-bundles.md
      tasks-and-back-stack.md
    manifest-resources/
      README.md
      action-category-data-elements.md
      activity-alias-element.md
      activity-element.md
      adaptive-icons.md
      application-element.md
      compose-resource-access.md
      drawable-resources.md
      grant-uri-permission-element.md
      instrumentation-element.md
      localization-rtl.md
      manifest-element.md
      manifest-merging.md
      manifest-structure.md
      meta-data-element.md
      permission-element.md
      property-element.md
      provider-element.md
      queries-element.md
      receiver-element.md
      resource-directories.md
      resource-naming-compression.md
      resource-qualifiers.md
      service-element.md
      string-resources.md
      style-theme-resources.md
      supports-screens-element.md
      uri-relative-filter-group-element.md
      uses-feature-element.md
      uses-library-element.md
      uses-permission-element.md
      uses-sdk-element.md
      value-resources.md
    permissions-privacy/
      README.md
      permission-types-and-protection-levels.md
      declaring-permissions.md
      defining-custom-permissions.md
      requesting-runtime-permissions.md
      requesting-permissions-in-compose.md
      evaluating-permission-need.md
      explaining-permission-access.md
      permission-groups-and-one-time-permission.md
      default-handler-permissions.md
      automatic-permission-reset.md
      special-permissions-overview.md
      system-alert-window.md
      manage-external-storage.md
      post-notifications-permission.md
      location-permissions.md
      location-button.md
      media-permissions.md
      nearby-devices-permissions.md
      restrict-interactions-with-other-apps.md
      data-safety-and-privacy-policy.md
      advertising-and-app-set-id.md
    notifications/
      README.md
      custom-notification.md
      expanded-notifications.md
      full-screen-intent.md
      live-update.md
      metric-style.md
      notification-actions.md
      notification-badges.md
      notification-builder.md
      notification-channels.md
      notification-groups.md
      notification-manager.md
      notification-navigation.md
      notification-permission.md
      notification-progress.md
      promoted-notifications.md
    system-ui/
      README.md
      window-insets.md
      window-insets-modifiers.md
      material3-insets.md
      edge-to-edge.md
      system-bar-appearance.md
      display-cutout.md
      picture-in-picture.md
      pip-setup.md
      app-shortcuts.md
      creating-shortcuts.md
      adaptive-icons.md
      splash-screen.md
      dark-theme.md
      keep-screen-on.md
    glance-widgets/
      README.md
      actions.md
      button.md
      composition-locals.md
      error-handling.md
      generated-previews.md
      glance-app-widget.md
      glance-app-widget-receiver.md
      glance-modifier.md
      glance-theme.md
      image.md
      layout-containers.md
      lazy-lists.md
      metrics.md
      multi-process-glance-app-widget.md
      pin-in-app.md
      progress-indicators.md
      remoteviews-interop.md
      remoteviews-legacy.md
      scaffold-titlebar.md
      size-modes.md
      state-management.md
      testing.md
      text.md
      toggle-controls.md
      widget-configuration.md
      widget-updates.md
```

`glance-widgets` は `androidx.glance` の API であり、モバイル Compose (`androidx.compose`) とは別 API 系統（同名の `Text` / `Image` / `Button` でもシグネチャが異なる）。

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| Activity のライフサイクル・生成/破棄を扱いたい | app-components | [references/app-components/README.md](references/app-components/README.md) |
| Intent / IntentFilter / ActivityResultContracts で画面遷移・結果受け渡しをしたい | app-components | [references/app-components/README.md](references/app-components/README.md) |
| タスクとバックスタック・構成変更・Application クラスを理解したい | app-components | [references/app-components/README.md](references/app-components/README.md) |
| ContentProvider を実装・利用したい | app-components | [references/app-components/README.md](references/app-components/README.md) |
| AndroidManifest.xml の要素・マニフェストマージを設定したい | manifest-resources | [references/manifest-resources/README.md](references/manifest-resources/README.md) |
| リソースディレクトリ・修飾子・strings/colors/styles/drawable を定義したい | manifest-resources | [references/manifest-resources/README.md](references/manifest-resources/README.md) |
| ローカライズ・RTL 対応をしたい | manifest-resources | [references/manifest-resources/README.md](references/manifest-resources/README.md) |
| ランタイム権限・特別な権限を要求したい | permissions-privacy | [references/permissions-privacy/README.md](references/permissions-privacy/README.md) |
| 位置情報・メディア・通知権限を扱いたい | permissions-privacy | [references/permissions-privacy/README.md](references/permissions-privacy/README.md) |
| パッケージ可視性・プライバシーポリシー対応をしたい | permissions-privacy | [references/permissions-privacy/README.md](references/permissions-privacy/README.md) |
| NotificationCompat / 通知チャンネルで通知を組み立てたい | notifications | [references/notifications/README.md](references/notifications/README.md) |
| 通知アクション・展開スタイル・グループ化・フルスクリーンインテントを使いたい | notifications | [references/notifications/README.md](references/notifications/README.md) |
| WindowInsets・エッジツーエッジ・ディスプレイカットアウトに対応したい | system-ui | [references/system-ui/README.md](references/system-ui/README.md) |
| Picture-in-Picture・ショートカット・スプラッシュスクリーン・ダークテーマを扱いたい | system-ui | [references/system-ui/README.md](references/system-ui/README.md) |
| Glance でアプリウィジェットを作りたい | glance-widgets | [references/glance-widgets/README.md](references/glance-widgets/README.md) |
| ウィジェットの設定画面・状態保存・更新トリガーを実装したい | glance-widgets | [references/glance-widgets/README.md](references/glance-widgets/README.md) |
| Glance のテスト・プレビュー生成・エラー処理を扱いたい | glance-widgets | [references/glance-widgets/README.md](references/glance-widgets/README.md) |

Service / BroadcastReceiver は `android-background-work`、ディープリンクと予測型戻るは `android-navigation`、ファイル/MediaStore は `android-data`、Compose の UI は `android-compose-ui` / `android-compose-components` の担当。
