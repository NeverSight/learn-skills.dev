---
name: windows-design
description: >
  Windows アプリ開発 (Fluent Design / WinUI 3) の デザインガイドラインリファレンス。
  layout, spacing, alignment, elevation, geometry, breakpoints, Color, Mica, Acrylic,
  Smoke, Reveal Highlight, materials, typography, Segoe Fluent Icons, app icons,
  motion, easing, connected animation, page transitions, parallax, reduce motion,
  NavigationView, TabView, CommandBar, menus, keyboard accelerators, access keys,
  accessibility, high contrast, RTL, globalization, widgets design。
user-invocable: false
---

# Windows デザイン (Fluent Design) リファレンス

Windows アプリの Fluent Design ガイドライン公式ドキュメントを蒸留したリファレンス。
レイアウト・色とマテリアル・タイポグラフィ／アイコン・モーション・ナビゲーション／コマンド・
ユーザビリティ／アクセシビリティの6カテゴリで構成し、WinUI 3 アプリの UI/UX 設計判断を支える。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/windows-design/
  SKILL.md
  references/
    foundations/
      README.md
      design-overview.md
      design-principles.md
      guidelines-overview.md
      layout-screen-sizes-and-breakpoints.md
      layout-responsive-design.md
      layout-spacing-and-density.md
      alignment-margin-padding.md
      geometry.md
      elevation-layering.md
      titlebar-design.md
    color-materials/
      README.md
      color.md
      accessible-color-contrast.md
      materials-overview.md
      mica.md
      acrylic.md
      smoke.md
      reveal-highlight.md
      background-material-selection.md
    typography-iconography/
      README.md
      typography.md
      segoe-fluent-icons-font.md
      segoe-ui-symbol-font.md
      icon-elements.md
      icon-composition-modifiers-localization.md
      app-icons.md
      app-icon-design.md
      app-icon-construction.md
      visual-studio-asset-generation.md
    motion/
      README.md
      motion-overview.md
      motion-principles.md
      timing-and-easing.md
      directionality-and-gravity.md
      content-transition-animations.md
      page-transitions.md
      connected-animation.md
      implicit-animations.md
      parallax.md
      motion-in-practice.md
      reduce-motion.md
    navigation-commanding/
      README.md
      app-silhouette.md
      navigation-basics.md
      navigation-history-and-backwards-navigation.md
      navigationview.md
      tab-view.md
      list-details.md
      commanding.md
      command-bar.md
      menus.md
      menus-and-context-menus.md
      keyboard-accelerators.md
      access-keys.md
      auto-suggest-box.md
    usability-accessibility/
      README.md
      usability-overview.md
      accessibility-overview.md
      designing-inclusive-software.md
      keyboard-accessibility.md
      high-contrast-themes.md
      accessible-text-requirements.md
      touch-target-size.md
      screen-sizes-breakpoints.md
      responsive-design.md
      globalization-localization.md
      rtl-layout.md
      bidirectional-text.md
      date-time-number-formats.md
      writing-style.md
      app-settings.md
      app-help-guidelines.md
      in-app-help.md
      external-help.md
      instructional-ui.md
      secondary-tile-pinning.md
      widgets-design-fundamentals.md
      widgets-principles.md
      widgets-states-and-ui.md
      widgets-interaction-design.md
      widgets-picker-integration.md
    signature-experiences/
      README.md
      haptics.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| レイアウトの余白・整列・ブレークポイントを設計したい | foundations | [references/foundations/README.md](references/foundations/README.md) |
| ジオメトリ（角丸等）やエレベーション・レイヤリングの原則を確認したい | foundations | [references/foundations/README.md](references/foundations/README.md) |
| デザイン原則・ガイドライン全体像を把握したい | foundations | [references/foundations/README.md](references/foundations/README.md) |
| Mica / Acrylic / Smoke などのマテリアルを背景に適用したい | color-materials | [references/color-materials/README.md](references/color-materials/README.md) |
| カラーパレット設計やコントラスト比のアクセシビリティ要件を満たしたい | color-materials | [references/color-materials/README.md](references/color-materials/README.md) |
| Reveal Highlight など光効果を実装したい | color-materials | [references/color-materials/README.md](references/color-materials/README.md) |
| タイポグラフィのフォント階層・サイズを設計したい | typography-iconography | [references/typography-iconography/README.md](references/typography-iconography/README.md) |
| Segoe Fluent Icons やアイコン要素を使いたい | typography-iconography | [references/typography-iconography/README.md](references/typography-iconography/README.md) |
| アプリアイコンを構築・生成したい | typography-iconography | [references/typography-iconography/README.md](references/typography-iconography/README.md) |
| ページ遷移・connected animation・implicit animation を実装したい | motion | [references/motion/README.md](references/motion/README.md) |
| イージング・タイミング・パララックスなどモーションの原則を確認したい | motion | [references/motion/README.md](references/motion/README.md) |
| reduce motion（モーション低減設定）に対応したい | motion | [references/motion/README.md](references/motion/README.md) |
| NavigationView / TabView でトップレベルナビゲーションを設計したい | navigation-commanding | [references/navigation-commanding/README.md](references/navigation-commanding/README.md) |
| CommandBar / メニュー / コンテキストメニューでコマンドを配置したい | navigation-commanding | [references/navigation-commanding/README.md](references/navigation-commanding/README.md) |
| キーボードアクセラレータ・アクセスキー・AutoSuggestBox によるナビゲーションを設計したい | navigation-commanding | [references/navigation-commanding/README.md](references/navigation-commanding/README.md) |
| キーボード操作・ハイコントラストテーマなどアクセシビリティ要件を満たしたい | usability-accessibility | [references/usability-accessibility/README.md](references/usability-accessibility/README.md) |
| RTL レイアウト・双方向テキスト・グローバリゼーションに対応したい | usability-accessibility | [references/usability-accessibility/README.md](references/usability-accessibility/README.md) |
| ウィジェットのデザイン原則・状態・ライティングスタイルを確認したい | usability-accessibility | [references/usability-accessibility/README.md](references/usability-accessibility/README.md) |
| ハプティクス（触覚フィードバック）のデザイン指針を確認したい | signature-experiences | [references/signature-experiences/README.md](references/signature-experiences/README.md) |

このスキルは Fluent Design のビジュアル・UX ガイドライン（レイアウト・色・タイポグラフィ・モーション・ナビゲーション UX・アクセシビリティ規範）のみを扱う。WinUI 3 コントロールの API シグネチャは windows-winui-controls、アプリライフサイクル・ウィンドウ管理・通知・パッケージング等は windows-app-sdk が担当する。
