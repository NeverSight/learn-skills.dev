---
name: windows-winui-ui
description: >
  Windows アプリ開発 (WinUI 3 / XAML) の UI 基盤リファレンス。
  レイアウトパネル Grid, StackPanel, Canvas, RelativePanel, SplitView, ScrollViewer、
  XAML マークアップ x:Bind, x:Name, x:Class, StaticResource, ThemeResource、
  添付プロパティ, 依存関係プロパティ、
  スタイル・テーマ Style, ControlTemplate, DataTemplate, VisualStateManager,
  ResourceDictionary, Acrylic, Mica, SystemBackdrop、
  データバインディング Binding, INotifyPropertyChanged, ObservableCollection,
  IValueConverter, DataContext, MVVM、
  アニメーション Storyboard, DoubleAnimation, EasingFunction, ThemeTransition,
  ConnectedAnimation, ImplicitAnimation。
user-invocable: false
---

# Windows WinUI UI リファレンス

WinUI 3 の XAML UI 基盤に関する公式ドキュメントの主要 API を蒸留したリファレンス。
レイアウト構築・XAML マークアップ構文・スタイル/テーマ・データバインディング・アニメーションという、コントロール個別 API とは独立した UI 基盤レイヤーを扱う。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/windows-winui-ui/
  SKILL.md
  references/
    layout-panels/
      README.md
      3-d-perspective-effects.md
      alignment-margin-padding.md
      attached-layouts.md
      border.md
      canvas.md
      choosing-a-layout-panel.md
      custom-panels.md
      grid.md
      itemsstackpanel.md
      itemswrapgrid.md
      layout-fundamentals.md
      panel.md
      relativepanel.md
      responsive-layouts.md
      scrollviewer.md
      splitview.md
      stackpanel.md
      transforms.md
      variablesizedwrapgrid.md
      viewbox.md
      wrappanel.md
    xaml-markup/
      README.md
      attached-properties-overview.md
      custom-attached-properties.md
      custom-dependency-properties.md
      customresource-markup-extension.md
      dependency-properties-overview.md
      events-and-routed-events-overview.md
      move-draw-commands-syntax.md
      property-path-syntax.md
      relativesource-markup-extension.md
      staticresource-markup-extension.md
      template-settings-classes.md
      templatebinding-markup-extension.md
      themeresource-markup-extension.md
      x-class-attribute.md
      x-datatype-attribute.md
      x-defaultbindmode-attribute.md
      x-deferloadstrategy-attribute.md
      x-fieldmodifier-attribute.md
      x-key-attribute.md
      x-load-attribute.md
      x-name-attribute.md
      x-null-markup-extension.md
      x-uid-directive.md
      xaml-and-whitespace.md
      xaml-intrinsic-data-types.md
      xaml-namescopes.md
      xaml-namespaces-and-namespace-mapping.md
      xaml-overview.md
      xaml-resource-dictionary.md
      xaml-syntax-guide.md
      x-bind-markup-extension.md
      xamlreader-load.md
    styling-theming/
      README.md
      acrylic-material.md
      brushes.md
      control-templating-guide.md
      control-template.md
      high-contrast-themes.md
      data-template.md
      data-template-selector.md
      element-theme.md
      item-container-style.md
      mica-material.md
      resource-dictionary.md
      shadows.md
      style-setter.md
      system-backdrops.md
      theme-resources.md
      visual-state.md
      visual-state-group.md
      visual-state-manager.md
      visual-transition.md
      xaml-controls-resources.md
    data-binding/
      README.md
      binding-markup-extension.md
      collectionviewsource.md
      data-binding-and-mvvm.md
      datacontext.md
      dependency-property-registration.md
      data-binding-debugging.md
      function-bindings.md
      inotifycollectionchanged.md
      inotifypropertychanged.md
      isupportincrementalloading.md
      itemssource-binding.md
      ivalueconverter.md
      observablecollection.md
      x-bind-markup-extension.md
      x-phase-attribute.md
    animation-composition/
      README.md
      storyboard.md
      double-animation.md
      color-animation.md
      double-animation-using-keyframes.md
      easing-functions.md
      repeat-behavior.md
      theme-animations.md
      entrance-theme-transition.md
      reposition-theme-transition.md
      add-delete-theme-transition.md
      theme-transitions.md
      transitions-property.md
      connected-animation.md
      implicit-animations.md
      animated-visual-player.md
      parallax-view.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| Grid / StackPanel / Canvas / RelativePanel で画面レイアウトを組み立てたい | layout-panels | [references/layout-panels/README.md](references/layout-panels/README.md) |
| SplitView / ScrollViewer / Viewbox / Border でペイン分割・スクロール・拡大表示を実装したい | layout-panels | [references/layout-panels/README.md](references/layout-panels/README.md) |
| レスポンシブレイアウトや適切なレイアウトパネルの選び方を知りたい | layout-panels | [references/layout-panels/README.md](references/layout-panels/README.md) |
| x:Bind / x:Name / x:Class など XAML の構文・ディレクティブを理解したい | xaml-markup | [references/xaml-markup/README.md](references/xaml-markup/README.md) |
| StaticResource / ThemeResource / RelativeSource などマークアップ拡張を使いたい | xaml-markup | [references/xaml-markup/README.md](references/xaml-markup/README.md) |
| 添付プロパティ・依存関係プロパティを独自に定義したい | xaml-markup | [references/xaml-markup/README.md](references/xaml-markup/README.md) |
| Style / ControlTemplate / DataTemplate でコントロールの見た目をカスタマイズしたい | styling-theming | [references/styling-theming/README.md](references/styling-theming/README.md) |
| VisualStateManager / VisualState でビジュアル状態遷移を実装したい | styling-theming | [references/styling-theming/README.md](references/styling-theming/README.md) |
| Acrylic / Mica / SystemBackdrop / ハイコントラストテーマで素材・テーマを適用したい | styling-theming | [references/styling-theming/README.md](references/styling-theming/README.md) |
| Binding / x:Bind でデータバインディングを実装したい | data-binding | [references/data-binding/README.md](references/data-binding/README.md) |
| INotifyPropertyChanged / ObservableCollection / MVVM でデータ変更通知を実装したい | data-binding | [references/data-binding/README.md](references/data-binding/README.md) |
| IValueConverter / CollectionViewSource でバインディング値の変換・整形をしたい | data-binding | [references/data-binding/README.md](references/data-binding/README.md) |
| Storyboard / DoubleAnimation / EasingFunction でプロパティアニメーションを実装したい | animation-composition | [references/animation-composition/README.md](references/animation-composition/README.md) |
| ThemeTransition / ConnectedAnimation / ImplicitAnimation で画面遷移演出を実装したい | animation-composition | [references/animation-composition/README.md](references/animation-composition/README.md) |

このスキルは WinUI 3 の XAML UI 基盤（レイアウト・マークアップ構文・スタイル・データバインド・アニメーション）のみを扱う。同名の Button / Grid / Window / Style 等は apple-swiftui, ark-ui, chakra-ui, fandhe-frontend, android-compose-* とは無関係の別 API。個別コントロールの API は `windows-winui-controls`、アプリライフサイクル・ウィンドウ管理・通知・リソース・配置は `windows-app-sdk` が担当する。
