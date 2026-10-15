---
name: android-architecture
description: >
  Android アプリ開発 (Kotlin) の推奨アーキテクチャリファレンス。
  Jetpack, androidx, UI layer, Domain layer, Data layer,
  state holder, UDF, SSOT, オフラインファースト, モジュール化,
  ViewModel, viewModelScope, SavedStateHandle, Lifecycle,
  repeatOnLifecycle, collectAsStateWithLifecycle, LiveData,
  Hilt による DI, Paging 3 によるページング処理。
user-invocable: false
---

# Android Architecture リファレンス

Android 公式アーキテクチャガイド（推奨レイヤー構成、ViewModel / Lifecycle、Hilt、Paging 3）を蒸留したスキル。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/android-architecture/
  SKILL.md
  references/
    layers/
      README.md
      layers.md
      intro.md
      ui-layer.md
      ui-state-holders.md
      ui-events.md
      ui-state-production.md
      domain-layer.md
      data-layer.md
      offline-first.md
      recommendations.md
      models-and-naming-conventions.md
      modularization.md
      modularization-patterns.md
    lifecycle-viewmodel/
      README.md
      viewmodel.md
      viewmodel-cheatsheet.md
      viewmodel-compose.md
      viewmodel-scoping-apis.md
      viewmodelprovider-factory.md
      viewmodelscope.md
      viewmodelstoreprovider.md
      androidviewmodel.md
      savedstatehandle.md
      saving-ui-state.md
      lifecycle.md
      lifecyclescope.md
      lifecycleowner.md
      defaultlifecycleobserver.md
      lifecycleeventobserver.md
      repeatonlifecycle.md
      flowwithlifecycle.md
      collectasstatewithlifecycle.md
      locallifecycleowner.md
      rememberlifecycleowner.md
      lifecycleeventeffect.md
      lifecyclestarteffect.md
      lifecycleresumeeffect.md
      livedata.md
      mutablelivedata.md
      observeasstate.md
      processlifecycleowner.md
      savedstateregistry.md
    di-hilt/
      README.md
      hilt-android-app.md
      android-entry-point.md
      inject.md
      module-install-in.md
      provides.md
      binds.md
      dagger-basics.md
      hilt-components-scopes.md
      hilt-jetpack.md
      hilt-multi-module.md
      qualifier-named.md
      hilt-view-model.md
      hilt-viewmodel-compose-split.md
      entry-point.md
      hilt-testing.md
      manual-di.md
    paging/
      README.md
      pager.md
      migrate-to-paging-3.md
      pagingconfig.md
      pagingsource.md
      closestitemaroundposition.md
      testpager.md
      pagingdata.md
      remotemediator.md
      loadstate.md
      cachedin.md
      pagingdata-transforms.md
      collectaslazypagingitems.md
      itemkey-itemcontenttype.md
      pagingdataadapter.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| UI / Domain / Data layer の推奨構成を知りたい | layers | [references/layers/README.md](references/layers/README.md) |
| state holder / UI state / UI events の設計指針を知りたい | layers | [references/layers/README.md](references/layers/README.md) |
| オフラインファースト・モジュール化の方針を知りたい | layers | [references/layers/README.md](references/layers/README.md) |
| ViewModel / viewModelScope / SavedStateHandle を使いたい | lifecycle-viewmodel | [references/lifecycle-viewmodel/README.md](references/lifecycle-viewmodel/README.md) |
| Lifecycle / repeatOnLifecycle / collectAsStateWithLifecycle でライフサイクルを扱いたい | lifecycle-viewmodel | [references/lifecycle-viewmodel/README.md](references/lifecycle-viewmodel/README.md) |
| LiveData / observeAsState でデータを監視したい | lifecycle-viewmodel | [references/lifecycle-viewmodel/README.md](references/lifecycle-viewmodel/README.md) |
| Hilt でアノテーション・コンポーネント・スコープを使った DI を設計したい | di-hilt | [references/di-hilt/README.md](references/di-hilt/README.md) |
| HiltViewModel / EntryPoint / Hilt テストの書き方を知りたい | di-hilt | [references/di-hilt/README.md](references/di-hilt/README.md) |
| Pager / PagingSource / RemoteMediator でページング処理を実装したい | paging | [references/paging/README.md](references/paging/README.md) |
| collectAsLazyPagingItems / PagingDataAdapter でページングリストを表示したい | paging | [references/paging/README.md](references/paging/README.md) |

Room / DataStore は android-data、WorkManager / coroutines は android-background-work、画面遷移は android-navigation の担当。
