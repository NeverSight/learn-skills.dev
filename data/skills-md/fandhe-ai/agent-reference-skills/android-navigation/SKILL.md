---
name: android-navigation
description: >
  Android アプリ開発 (Kotlin) の画面遷移・Navigation リファレンス。
  Jetpack Compose, androidx。Navigation 3 (stable), NavDisplay、
  Navigation Compose, NavHost, composable, 型安全ルート、
  Fragment ナビゲーション, NavHostFragment, Safe Args、
  ディープリンク, App Links, assetlinks.json、
  予測型戻る (OnBackPressedDispatcher)。
user-invocable: false
---

# Android Navigation リファレンス

Android (Kotlin / Jetpack Compose) の画面遷移に関する公式ドキュメントの主要 API を網羅したスキル。
Navigation 3 は新規 Compose 実装の現行 stable な選択肢、Navigation Compose は既存の 2.x グラフおよび Fragment ベースのナビゲーションを担う。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/android-navigation/
  SKILL.md
  references/
    navigation3/
      README.md
      navigation-3.md
      navkey.md
      navbackstack.md
      naventry.md
      entryprovider.md
      navdisplay.md
      navdisplay-animation.md
      naventrydecorator.md
      remembersaveablestateholdernaventrydecorator.md
      rememberviewmodelstorenaventrydecorator.md
      scene.md
      scenestrategy.md
      dialogscenestrategy.md
      singlepanescenestrategy.md
      listdetailscenestrategy.md
      supportingpanescenestrategy.md
      scenedecoratorstrategy.md
      migration-guide.md
      modularize.md
    nav-compose/
      README.md
      navhost.md
      navcontroller.md
      remembernavcontroller.md
      navhostcontroller.md
      testnavhostcontroller.md
      composable.md
      navigation.md
      dialog.md
      type-safe-routes.md
      navbackstackentry.md
      navargument.md
      navtype.md
      navoptions.md
      popbackstack.md
      currentbackstackentryasstate.md
      hiltviewmodel.md
      localownersprovider.md
      navhostfragment.md
      findnavcontroller.md
      navigationui.md
      safe-args.md
      navigation-graph-xml.md
      navigation-feature-modules.md
    deep-links/
      README.md
      deep-link-types.md
      intent-filter-deep-links.md
      asset-links-verification.md
      verify-app-links.md
      nav-deep-link.md
      deep-link-xml-tag.md
      handle-deep-link.md
      navigation3-deep-links.md
      intent-action-view-launch-mode.md
      test-deep-links.md
    back-navigation/
      README.md
      back-handler.md
      predictive-back-handler.md
      navigation-back-handler.md
      on-back-pressed-dispatcher.md
      on-back-pressed-callback.md
      navigation-event-dispatcher.md
      navigation-event-handler.md
      navigation-event-input.md
      local-on-back-pressed-dispatcher-owner.md
      back-event-compat.md
      on-back-invoked-dispatcher.md
      on-back-invoked-callback.md
      enable-on-back-invoked-callback.md
      predictive-back-animations.md
      custom-back-navigation.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| NavDisplay / NavBackStack / NavKey で Navigation 3 の画面遷移を実装したい | navigation3 | [references/navigation3/README.md](references/navigation3/README.md) |
| entryProvider / NavEntry でキーとコンテンツを紐付けたい | navigation3 | [references/navigation3/README.md](references/navigation3/README.md) |
| Scene / SceneStrategy でリスト詳細・サポーティングペインなどアダプティブなシーンを構成したい | navigation3 | [references/navigation3/README.md](references/navigation3/README.md) |
| NavHost / NavController / composable で Navigation Compose の画面遷移を実装したい | nav-compose | [references/nav-compose/README.md](references/nav-compose/README.md) |
| 型安全ルート (Type-Safe Routes) や NavOptions / NavType で引数・遷移オプションを扱いたい | nav-compose | [references/nav-compose/README.md](references/nav-compose/README.md) |
| NavHostFragment / Safe Args / Navigation Graph XML で Fragment ベースのナビゲーションを実装したい | nav-compose | [references/nav-compose/README.md](references/nav-compose/README.md) |
| ディープリンク・App Links を宣言・検証したい (intent-filter, assetlinks.json, autoVerify) | deep-links | [references/deep-links/README.md](references/deep-links/README.md) |
| navDeepLink / handleDeepLink / NavDeepLinkBuilder で Navigation 経由の遷移を実装したい | deep-links | [references/deep-links/README.md](references/deep-links/README.md) |
| adb でディープリンク・App Links の動作をテストしたい | deep-links | [references/deep-links/README.md](references/deep-links/README.md) |
| BackHandler / PredictiveBackHandler で戻るボタン・予測型戻るジェスチャーを処理したい | back-navigation | [references/back-navigation/README.md](references/back-navigation/README.md) |
| OnBackPressedDispatcher / OnBackInvokedDispatcher でカスタム戻る処理を実装したい | back-navigation | [references/back-navigation/README.md](references/back-navigation/README.md) |

navigation3 の ListDetailSceneStrategy / SupportingPaneSceneStrategy は back stack を Scene へ配置するロジックのみを扱う。NavigationBar / TopAppBar などの UI コンポーネントは `android-compose-components`、リスト詳細・サポーティングペインの実際のレイアウト UI は `android-compose-ui` の担当。
