---
name: apple-swiftui
description: >
  Apple SwiftUI 宣言的 UI フレームワークリファレンス。
  View, VStack, HStack, ZStack, List, NavigationStack, TabView,
  State, Binding, Bindable, Environment, EnvironmentObject,
  sheet, fullScreenCover, modifier, animation, withAnimation,
  Animation, Transition, matchedGeometryEffect, PhaseAnimator, KeyframeAnimator。
user-invocable: false
model: sonnet
---

# SwiftUI リファレンス

SwiftUI 公式ドキュメントの主要 API を網羅したスキル。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/apple-swiftui/
  SKILL.md
  references/
    views-controls/
      README.md
      text.md
      label.md
      image.md
      button.md
      toggle.md
      textfield.md
      securefield.md
      texteditor.md
      slider.md
      stepper.md
      picker.md
      datepicker.md
      colorpicker.md
      progressview.md
      link.md
      menu.md
      list.md
      section.md
      foreach.md
      form.md
    layout/
      README.md
      vstack.md
      hstack.md
      zstack.md
      lazyvstack.md
      lazyhstack.md
      grid.md
      gridrow.md
      lazyvgrid.md
      lazyhgrid.md
      griditem.md
      spacer.md
      divider.md
      geometryreader.md
      viewthatfits.md
      layout.md
      alignment.md
      horizontalalignment.md
      verticalalignment.md
      edgeinsets.md
      scrollview.md
    state-data/
      README.md
      state.md
      binding.md
      bindable.md
      environment.md
      environmentvalues.md
      environmentobject.md
      stateobject.md
      observedobject.md
      observableobject.md
      appstorage.md
      scenestorage.md
      focusstate.md
      namespace.md
    navigation/
      README.md
      navigationstack.md
      navigationsplitview.md
      navigationlink.md
      navigationpath.md
      navigationdestination.md
      sheet.md
      fullscreencover.md
      popover.md
      alert.md
      confirmationdialog.md
      tabview.md
      tab.md
      toolbar.md
      toolbaritem.md
      presentationdetents.md
    modifiers/
      README.md
      frame.md
      padding.md
      background.md
      overlay.md
      foreground-style.md
      font.md
      text-styling.md
      text-layout.md
      clip-shape.md
      shadow.md
      opacity.md
      offset-position.md
      scale-rotation.md
      border-tint.md
      interaction.md
    animation/
      README.md
      withanimation.md
      withanimation-completion.md
      animation.md
      animation-modifier.md
      spring.md
      transition.md
      anytransition.md
      transition-modifier.md
      transition-phase.md
      contenttransition.md
      contenttransition-modifier.md
      matchedgeometryeffect.md
      phaseanimator.md
      keyframeanimator.md
      animatable.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| Text / Image / Button / Toggle / List / Form などの標準ビューを使いたい | views-controls | [references/views-controls/README.md](references/views-controls/README.md) |
| TextField / SecureField / Picker / DatePicker / Slider で入力 UI を作りたい | views-controls | [references/views-controls/README.md](references/views-controls/README.md) |
| ForEach / Section でリストやデータ繰り返し表示をしたい | views-controls | [references/views-controls/README.md](references/views-controls/README.md) |
| VStack / HStack / ZStack でビューを並べたい | layout | [references/layout/README.md](references/layout/README.md) |
| LazyVGrid / LazyHGrid / Grid でグリッドレイアウトを作りたい | layout | [references/layout/README.md](references/layout/README.md) |
| GeometryReader / ViewThatFits / Layout でサイズ・整列を制御したい | layout | [references/layout/README.md](references/layout/README.md) |
| State / Binding / Bindable でビューの状態を管理したい | state-data | [references/state-data/README.md](references/state-data/README.md) |
| Environment / EnvironmentObject / EnvironmentValues を使いたい | state-data | [references/state-data/README.md](references/state-data/README.md) |
| AppStorage / SceneStorage でデータを永続化したい | state-data | [references/state-data/README.md](references/state-data/README.md) |
| NavigationStack / NavigationLink で画面遷移を実装したい | navigation | [references/navigation/README.md](references/navigation/README.md) |
| sheet / fullScreenCover / popover / alert でモーダル表示したい | navigation | [references/navigation/README.md](references/navigation/README.md) |
| TabView / Tab / toolbar / ToolbarItem でタブ・ツールバーを作りたい | navigation | [references/navigation/README.md](references/navigation/README.md) |
| frame / padding / background / overlay でレイアウト調整したい | modifiers | [references/modifiers/README.md](references/modifiers/README.md) |
| font / foregroundStyle / shadow / opacity で見た目を整えたい | modifiers | [references/modifiers/README.md](references/modifiers/README.md) |
| clipShape / scaleEffect / rotationEffect / border などを適用したい | modifiers | [references/modifiers/README.md](references/modifiers/README.md) |
| withAnimation / Animation でアニメーションを付けたい | animation | [references/animation/README.md](references/animation/README.md) |
| Transition / AnyTransition で挿入・削除アニメーションを定義したい | animation | [references/animation/README.md](references/animation/README.md) |
| matchedGeometryEffect / PhaseAnimator / KeyframeAnimator を使いたい | animation | [references/animation/README.md](references/animation/README.md) |
