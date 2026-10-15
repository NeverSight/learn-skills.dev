---
name: android-compose-ui
description: >
  Android Jetpack Compose (Kotlin) の UI 基盤リファレンス。androidx, Material3 土台。
  Composable, Modifier, CompositionLocal, remember, mutableStateOf, State, LaunchedEffect。
  Column, Row, Box, LazyColumn, Pager, ConstraintLayout, WindowSizeClass, ペインスキャフォールド。
  BasicText, BasicTextField, TextStyle, IME, clickable, ジェスチャ, フォーカス, セマンティクス。
user-invocable: false
---

# Android Compose UI リファレンス

Jetpack Compose (androidx.compose) の UI 基盤に関する公式ドキュメントを蒸留したスキル。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/android-compose-ui/
  SKILL.md
  references/
    fundamentals/
      README.md
      composable-functions.md
      recomposition.md
      modifier.md
      phases.md
      compositionlocalof.md
      staticcompositionlocalof.md
      compositionlocalprovider.md
      snapshotmutationpolicy.md
      movablecontentof.md
      custom-modifiers.md
      stability.md
    state-lifecycle/
      README.md
      remember.md
      remembersaveable.md
      mutablestateof.md
      mutablestatelistof.md
      mutablestatemapof.md
      mutablestatesetof.md
      mutablestate.md
      state.md
      derivedstateof.md
      snapshotflow.md
      producestate.md
      collectasstate.md
      rememberupdatedstate.md
      launchedeffect.md
      disposableeffect.md
      sideeffect.md
      remembercoroutinescope.md
      saver.md
      state-hoisting.md
      state-lifespans.md
    layout/
      README.md
      column.md
      row.md
      box.md
      spacer.md
      boxwithconstraints.md
      arrangement-alignment.md
      intrinsicsize.md
      modifier-layout.md
      lazycolumn.md
      lazyrow.md
      lazy-list-scope.md
      rememberlazyliststate.md
      lazyverticalgrid.md
      lazyhorizontalgrid.md
      lazyverticalstaggeredgrid.md
      pager.md
      flow-layout.md
      constraintlayout.md
      layout.md
      subcomposelayout.md
      scroll.md
      alignment-lines.md
      intrinsic-measurements.md
      visibility-tracking.md
      flexbox-grid.md
      styles.md
      media-query.md
    adaptive-layout/
      README.md
      window-size-class.md
      window-adaptive-info.md
      posture.md
      pane-scaffold-directive.md
      list-detail-pane-scaffold.md
      navigable-list-detail-pane-scaffold.md
      supporting-pane-scaffold.md
      navigable-supporting-pane-scaffold.md
      three-pane-scaffold-navigator.md
      back-navigation-behavior.md
      animated-pane.md
      pane-adapted-value.md
      navigation-suite-scaffold.md
      folding-feature.md
      window-info-tracker.md
      canonical-layouts.md
    text-input/
      README.md
      basictext.md
      basicmarquee.md
      basictextfield.md
      textfieldstate.md
      annotatedstring.md
      spanstyle.md
      paragraphstyle.md
      textstyle.md
      fontfamily.md
      textalign.md
      keyboardoptions.md
      visualtransformation.md
      selectioncontainer.md
      textmeasurer.md
      autofill.md
      clipboard.md
      emoji.md
    touch-input/
      README.md
      clickable.md
      combined-clickable.md
      pointer-input.md
      detect-tap-gestures.md
      detect-drag-gestures.md
      detect-transform-gestures.md
      draggable.md
      anchored-draggable.md
      scrollable.md
      nested-scroll.md
      transformable.md
      toggleable.md
      selectable.md
      interaction-source.md
      indication.md
      focusable.md
      keyboard-input.md
      hover.md
      semantics.md
      test-tag.md
      haptic-feedback.md
      drag-and-drop.md
      stylus-input.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| `@Composable` 関数の設計・再コンポジションの仕組みを知りたい | fundamentals | [references/fundamentals/README.md](references/fundamentals/README.md) |
| `Modifier` チェーンの挙動・順序を確認したい | fundamentals | [references/fundamentals/README.md](references/fundamentals/README.md) |
| `CompositionLocal` でスコープ内に値を伝搬したい | fundamentals | [references/fundamentals/README.md](references/fundamentals/README.md) |
| `remember` / `mutableStateOf` で状態を保持したい | state-lifecycle | [references/state-lifecycle/README.md](references/state-lifecycle/README.md) |
| `LaunchedEffect` / `DisposableEffect` / `SideEffect` で副作用を扱いたい | state-lifecycle | [references/state-lifecycle/README.md](references/state-lifecycle/README.md) |
| Flow / StateFlow を Compose の `State` に変換したい（`collectAsState` / `produceState` / `snapshotFlow`） | state-lifecycle | [references/state-lifecycle/README.md](references/state-lifecycle/README.md) |
| `Column` / `Row` / `Box` で子要素を並べたい | layout | [references/layout/README.md](references/layout/README.md) |
| `LazyColumn` / `LazyRow` / `LazyVerticalGrid` で大量データをスクロール表示したい | layout | [references/layout/README.md](references/layout/README.md) |
| `HorizontalPager` / `FlowRow` / `ConstraintLayout` / カスタム `Layout` を使いたい | layout | [references/layout/README.md](references/layout/README.md) |
| `Style` / `StyleScope` で CSS ライクに状態別スタイルを定義したい、`mediaQuery` で環境シグナルに応じて UI を切り替えたい | layout | [references/layout/README.md](references/layout/README.md) |
| `WindowSizeClass` で画面幅に応じたレイアウトを切り替えたい | adaptive-layout | [references/adaptive-layout/README.md](references/adaptive-layout/README.md) |
| `ListDetailPaneScaffold` / `SupportingPaneScaffold` でマルチペイン UI を作りたい | adaptive-layout | [references/adaptive-layout/README.md](references/adaptive-layout/README.md) |
| 折りたたみデバイスの `FoldingFeature` / `Posture` に対応したい | adaptive-layout | [references/adaptive-layout/README.md](references/adaptive-layout/README.md) |
| `BasicText` / `BasicTextField` でテキスト表示・入力を実装したい | text-input | [references/text-input/README.md](references/text-input/README.md) |
| `AnnotatedString` / `SpanStyle` / `TextStyle` でリッチテキストを装飾したい | text-input | [references/text-input/README.md](references/text-input/README.md) |
| `KeyboardOptions` / IME アクション・入力変換を制御したい | text-input | [references/text-input/README.md](references/text-input/README.md) |
| `Modifier.clickable` / `combinedClickable` でタップを処理したい | touch-input | [references/touch-input/README.md](references/touch-input/README.md) |
| `detectDragGestures` / `draggable` / `transformable` でジェスチャを扱いたい | touch-input | [references/touch-input/README.md](references/touch-input/README.md) |
| `Modifier.focusable` / `semantics` / `testTag` でフォーカス・アクセシビリティ・テストを扱いたい | touch-input | [references/touch-input/README.md](references/touch-input/README.md) |
| Material3 コンポーネント（Button/Card/TextField 等）を使いたい | - | android-compose-components スキルの担当 |
| アニメーション・描画を扱いたい | - | android-compose-graphics-animation スキルの担当 |
