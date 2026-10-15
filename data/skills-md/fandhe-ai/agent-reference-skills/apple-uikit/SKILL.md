---
name: apple-uikit
description: >
  UIKit iOS/iPadOS UI フレームワークリファレンス。
  UIViewController, UINavigationController, UITabBarController, UISplitViewController,
  UIView, UILabel, UIButton, UITextField, UIScrollView, UIStackView,
  UITableView, UICollectionView, diffable data source, NSDiffableDataSourceSnapshot,
  UICollectionViewCompositionalLayout, Auto Layout, NSLayoutConstraint, NSLayoutAnchor,
  UILayoutGuide, intrinsicContentSize。
user-invocable: false
---

## ディレクトリ構成

```text
skills/apple-uikit/
  SKILL.md
  references/
    view-controllers/
      README.md
      uiviewcontroller.md
      uinavigationcontroller.md
      uitabbarcontroller.md
      uitab.md
      uisplitviewcontroller.md
      uipageviewcontroller.md
      uipresentationcontroller.md
      uisheetpresentationcontroller.md
      uicontentunavailableconfiguration.md
      viewcontroller-lifecycle.md
      viewcontroller-presentation.md
      uiresponder.md
      uiwindow.md
      uiwindowscene.md
    views-controls/
      README.md
      uiview.md
      uilabel.md
      uibutton.md
      uiimageview.md
      uitextfield.md
      uitextview.md
      uiswitch.md
      uislider.md
      uistepper.md
      uisegmentedcontrol.md
      uiscrollview.md
      uistackview.md
      uiactivityindicatorview.md
      uiprogressview.md
      uipickerview.md
      uidatepicker.md
      uicontrol.md
      uigesturerecognizer.md
    collections-tables/
      README.md
      uitableview.md
      uitableviewcell.md
      uitableviewdatasource.md
      uitableviewdelegate.md
      uitableviewdiffabledatasource.md
      uicollectionview.md
      uicollectionviewcell.md
      uicollectionviewdatasource.md
      uicollectionviewdelegate.md
      uicollectionviewdiffabledatasource.md
      uicollectionviewlayout.md
      uicollectionviewflowlayout.md
      uicollectionviewcompositionallayout.md
      nsdiffabledatasourcesnapshot.md
      uicollectionviewlistcell.md
      uilistcontentconfiguration.md
    autolayout/
      README.md
      nslayoutconstraint.md
      nslayoutanchor.md
      nslayoutxaxisanchor.md
      nslayoutyaxisanchor.md
      nslayoutdimension.md
      uilayoutguide.md
      uilayoutpriority.md
      uiview-layout.md
      uistackview-autolayout.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| UIViewController のライフサイクルを知りたい | view-controllers | [references/view-controllers/README.md](references/view-controllers/README.md) |
| ナビゲーション・タブ・スプリットビューを構成したい | view-controllers | [references/view-controllers/README.md](references/view-controllers/README.md) |
| UITab で UITabBarController のタブを構成したい | view-controllers | [references/view-controllers/README.md](references/view-controllers/README.md) |
| モーダル・シート表示を実装したい | view-controllers | [references/view-controllers/README.md](references/view-controllers/README.md) |
| 空状態・コンテンツ未取得時の表示を実装したい | view-controllers | [references/view-controllers/README.md](references/view-controllers/README.md) |
| レスポンダーチェーン・イベント処理を知りたい | view-controllers | [references/view-controllers/README.md](references/view-controllers/README.md) |
| UIView・UILabel・UIButton などのビュー/コントロールを使いたい | views-controls | [references/views-controls/README.md](references/views-controls/README.md) |
| テキスト入力・スクロール・スタックビューを実装したい | views-controls | [references/views-controls/README.md](references/views-controls/README.md) |
| ジェスチャー認識・タッチイベントを処理したい | views-controls | [references/views-controls/README.md](references/views-controls/README.md) |
| UITableView でリスト表示・セル再利用を実装したい | collections-tables | [references/collections-tables/README.md](references/collections-tables/README.md) |
| UICollectionView・Compositional Layout を使いたい | collections-tables | [references/collections-tables/README.md](references/collections-tables/README.md) |
| Diffable Data Source・スナップショットで差分更新したい | collections-tables | [references/collections-tables/README.md](references/collections-tables/README.md) |
| NSLayoutConstraint・NSLayoutAnchor で制約を組みたい | autolayout | [references/autolayout/README.md](references/autolayout/README.md) |
| safeAreaLayoutGuide・intrinsicContentSize を使いたい | autolayout | [references/autolayout/README.md](references/autolayout/README.md) |
| UILayoutGuide・UILayoutPriority で制約を調整したい | autolayout | [references/autolayout/README.md](references/autolayout/README.md) |
