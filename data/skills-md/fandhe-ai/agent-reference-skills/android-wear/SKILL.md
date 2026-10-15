---
name: android-wear
description: >
  Wear OS (Kotlin) の androidx.wear API・Watch Face Format (WFF) リファレンス。
  Wear Compose の CurvedLayout, rotary input, ambient mode, ScalingLazyColumn。
  Tiles / ProtoLayout, ComplicationDataSourceService と ComplicationData 型,
  Health Services (MeasureClient, ExerciseClient, PassiveMonitoringClient),
  WFF の XML 要素・式・コンプリケーションスロット・ユーザー設定。
user-invocable: false
---

# Wear OS (Kotlin) リファレンス

Wear OS 公式ドキュメントの主要 API を網羅したスキル。
`androidx.wear.compose.*` はモバイルの `androidx.compose.*` とは別 API であり、同名コンポーネントでも取り違えに注意する。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/android-wear/
  SKILL.md
  references/
    wear-compose/
      README.md
      theme.md
      scaffold.md
      time-text.md
      lists.md
      expandable.md
      button.md
      button-group.md
      edge-button.md
      icon-button.md
      selection-controls.md
      split-selection-controls.md
      card.md
      list-header.md
      animated-text-placeholder.md
      picker.md
      dialogs.md
      dynamic-color-scheme.md
      progress-indicators.md
      slider-stepper.md
      pager.md
      curved-layout.md
      swipe-to-reveal.md
      rotary-input.md
      hierarchical-focus.md
      ambient-mode.md
      swipe-dismissable-nav-host.md
      navigation3.md
      screen-sizes.md
      migrate-to-material3.md
      migrate-to-navigation3.md
      performance.md
    tiles/
      README.md
      tile-service.md
      tile-builders.md
      dimensions.md
      color-and-type.md
      layout-elements.md
      modifiers.md
      material3-layout.md
      material3-buttons.md
      material3-cards-progress.md
      animations.md
      actions-and-interactivity.md
      updating-tiles.md
      platform-data.md
      tile-preview-debugging.md
      versioning.md
    wear-widgets/
      README.md
      glance-wear-widget-service.md
      migrate-from-tiles.md
      remote-compose-layout.md
      remote-state-and-actions.md
    complications-health/
      README.md
      background-body-sensors.md
      complicationdatasourceservice.md
      shorttextcomplicationdata.md
      longtextcomplicationdata.md
      rangedvaluecomplicationdata.md
      monochromaticimagecomplicationdata.md
      smallimagecomplicationdata.md
      nodatacomplicationdata.md
      complicationtext.md
      complicationdatasourceupdaterequester.md
      compatibility.md
      healthservicesclient.md
      measureclient.md
      exerciseclient.md
      exerciseevent.md
      passivemonitoringclient.md
      datatype.md
      debouncedgoal.md
      datapointcontainer.md
      healthservicescapabilities.md
      healthservicespermissions.md
      healthservicessimulation.md
    watch-face/
      README.md
      overview.md
      setup.md
      root-element.md
      scene-and-parts.md
      shapes.md
      transform.md
      time.md
      text.md
      images.md
      expressions.md
      weather.md
      complications.md
      user-configurations.md
      personalization-and-photos.md
      ambient-mode.md
      effects.md
      versions.md
      memory-optimization.md
      build-and-debug.md
      watch-face-push.md
    data-layer-communication/
      README.md
      assets.md
      capabilityclient.md
      dataclient.md
      messageclient.md
      nodeclient.md
      ongoingactivity.md
      remoteactivityhelper.md
      remoteauthclient.md
      wearablelistenerservice.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| Wear Compose でテーマ・画面骨格 (Scaffold/TimeText) を組みたい | wear-compose | [references/wear-compose/README.md](references/wear-compose/README.md) |
| ScalingLazyColumn / TransformingLazyColumn でリスト表示したい | wear-compose | [references/wear-compose/README.md](references/wear-compose/README.md) |
| Button / IconButton / SelectionControls / Card / Picker / Dialog を使いたい | wear-compose | [references/wear-compose/README.md](references/wear-compose/README.md) |
| CurvedLayout / rotary input (クラウン・ベゼル) / ambient mode を実装したい | wear-compose | [references/wear-compose/README.md](references/wear-compose/README.md) |
| Material 2.5 → Material 3 / Navigation 2 → Navigation 3 へ移行したい、Compose のパフォーマンスを最適化したい | wear-compose | [references/wear-compose/README.md](references/wear-compose/README.md) |
| Tile (TileService) を実装したい | tiles | [references/tiles/README.md](references/tiles/README.md) |
| ProtoLayout / Material3 タイル部品でレイアウトを組みたい | tiles | [references/tiles/README.md](references/tiles/README.md) |
| Tile のアクション・更新・プラットフォームデータ連携をしたい | tiles | [references/tiles/README.md](references/tiles/README.md) |
| Wear Widget (GlanceWearWidgetService) を実装したい | wear-widgets | [references/wear-widgets/README.md](references/wear-widgets/README.md) |
| Remote Compose (RemoteBox/RemoteColumn/RemoteText/RemoteButton) でウィジェットのレイアウトを組みたい | wear-widgets | [references/wear-widgets/README.md](references/wear-widgets/README.md) |
| Remote Compose の状態・アクション (rememberMutableRemote* / valueChange / pendingIntentAction) を扱いたい | wear-widgets | [references/wear-widgets/README.md](references/wear-widgets/README.md) |
| Tile から Wear Widget への移行を検討したい | wear-widgets | [references/wear-widgets/README.md](references/wear-widgets/README.md) |
| ComplicationDataSourceService とコンプリケーションデータ型を実装したい | complications-health | [references/complications-health/README.md](references/complications-health/README.md) |
| Health Services (MeasureClient/ExerciseClient/PassiveMonitoringClient) で運動・健康データを扱いたい | complications-health | [references/complications-health/README.md](references/complications-health/README.md) |
| Health Services の権限・シミュレーション・デバイス間互換性・端末機能 (Capabilities) を確認したい | complications-health | [references/complications-health/README.md](references/complications-health/README.md) |
| バックグラウンドで身体センサー (心拍数等) にアクセスする権限フローを実装したい | complications-health | [references/complications-health/README.md](references/complications-health/README.md) |
| Watch Face Format (WFF) の XML 要素・シーン・図形・時刻表示を書きたい | watch-face | [references/watch-face/README.md](references/watch-face/README.md) |
| WFF の式・データソース・コンプリケーションスロット・ユーザー設定を扱いたい | watch-face | [references/watch-face/README.md](references/watch-face/README.md) |
| WFF のビルド・デバッグ・メモリ最適化・バージョン対応を確認したい | watch-face | [references/watch-face/README.md](references/watch-face/README.md) |
| DataClient で端末間 (phone/watch) の DataItem・Asset を同期したい | data-layer-communication | [references/data-layer-communication/README.md](references/data-layer-communication/README.md) |
| MessageClient で端末間メッセージ (RPC 的な一方向/リクエスト-レスポンス) を送りたい | data-layer-communication | [references/data-layer-communication/README.md](references/data-layer-communication/README.md) |
| NodeClient / CapabilityClient でノード・アプリ機能を検出したい | data-layer-communication | [references/data-layer-communication/README.md](references/data-layer-communication/README.md) |
| RemoteActivityHelper / RemoteAuthClient / OngoingActivity でフォンとの連携・認証・進行中アクティビティを扱いたい | data-layer-communication | [references/data-layer-communication/README.md](references/data-layer-communication/README.md) |

モバイルの Jetpack Compose は `android-compose-ui` / `android-compose-components` が担当する（本スキルの対象外）。モバイルのホーム画面ウィジェット（`androidx.glance.appwidget` / RemoteViews）は `android-platform-core` が担当するが、本スキルの `wear-widgets` は Remote Compose ベースの Wear OS 上のウィジェット（フルスクリーンタイルの後継、カルーセル表示）を扱い、これらとは別 API である。
