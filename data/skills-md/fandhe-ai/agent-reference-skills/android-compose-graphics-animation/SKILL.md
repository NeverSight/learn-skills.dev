---
name: android-compose-graphics-animation
description: >
  Android Jetpack Compose (Kotlin) のアニメーション・描画リファレンス。
  androidx.compose.animation / graphics API。
  AnimatedVisibility, AnimatedContent, animate*AsState, Animatable,
  AnimationSpec, Canvas, DrawScope, Brush, Path, Color, Image。
user-invocable: false
---

# Android Compose Graphics Animation リファレンス

Jetpack Compose (Kotlin) のアニメーションと描画に関する公式ドキュメント主要 API を網羅したスキル。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/android-compose-graphics-animation/
  SKILL.md
  references/
    animation-apis/
      README.md
      animatedvisibility.md
      animatedcontent.md
      crossfade.md
      animatecontentsize.md
      animateasstate.md
      animatable.md
      infinitetransition.md
      transition.md
      enterexittransition.md
      lookaheadscope.md
      animateitem.md
      animatebounds.md
      animateenterexit.md
      animationvector.md
      targetbasedanimation-decayanimation.md
    animation-spec/
      README.md
      animationspec.md
      tween.md
      spring.md
      keyframes.md
      repeatable.md
      snap.md
      easing.md
      repeatmode.md
      startoffset.md
      vectorconverter.md
      decayanimationspec.md
    shared-elements/
      README.md
      sharedtransitionlayout.md
      sharedtransitionscope.md
      sharedelement.md
      sharedbounds.md
      sharedelementwithcallermanagedvisibility.md
      remembersharedcontentstate.md
      resizemode.md
      boundstransform.md
      overlayclip.md
      renderinsharedtransitionscopeoverlay.md
      skiptolookaheadsize.md
    graphics-draw/
      README.md
      canvas.md
      draw-scope.md
      modifier-draw-behind.md
      modifier-draw-with-content.md
      modifier-draw-with-cache.md
      modifier-graphics-layer.md
      modifier-clip.md
      modifier-shadow.md
      modifier-drop-shadow.md
      modifier-alpha.md
      modifier-blur.md
      shape.md
      brush.md
      path.md
      color.md
      blend-mode.md
      render-effect.md
      mesh-gradient.md
      rounded-polygon-morph.md
    images/
      README.md
      image.md
      painterresource.md
      painter.md
      bitmappainter.md
      colorpainter.md
      imagebitmap.md
      contentscale.md
      colorfilter.md
      imagevector.md
      animatedimagevector.md
      remembervectorpainter.md
      icons.md
      asyncimage.md
      modifierpaint.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| AnimatedVisibility / AnimatedContent / Crossfade で表示・切り替えをアニメーションしたい | animation-apis | [references/animation-apis/README.md](references/animation-apis/README.md) |
| animate*AsState / Animatable で単一値をアニメーションしたい | animation-apis | [references/animation-apis/README.md](references/animation-apis/README.md) |
| Transition / InfiniteTransition / LookaheadScope で複数アニメーションを協調させたい | animation-apis | [references/animation-apis/README.md](references/animation-apis/README.md) |
| tween / spring / keyframes でアニメーションの速度・軌道を指定したい | animation-spec | [references/animation-spec/README.md](references/animation-spec/README.md) |
| Easing / VectorConverter / repeatable でカーブ・繰り返し・型変換を制御したい | animation-spec | [references/animation-spec/README.md](references/animation-spec/README.md) |
| SharedTransitionLayout / sharedElement / sharedBounds で画面間の共有要素遷移を実装したい | shared-elements | [references/shared-elements/README.md](references/shared-elements/README.md) |
| Canvas / DrawScope でカスタム描画をしたい | graphics-draw | [references/graphics-draw/README.md](references/graphics-draw/README.md) |
| Shape / Brush / Path / Color / BlendMode / RenderEffect で図形・塗り・合成を扱いたい | graphics-draw | [references/graphics-draw/README.md](references/graphics-draw/README.md) |
| drawBehind / drawWithContent / graphicsLayer / shadow / blur などの描画系 Modifier を使いたい | graphics-draw | [references/graphics-draw/README.md](references/graphics-draw/README.md) |
| Image / painterResource / Painter / ContentScale / ColorFilter で画像を表示したい | images | [references/images/README.md](references/images/README.md) |
| ImageVector / Icons / AsyncImage でベクター画像・アイコン・非同期画像を扱いたい | images | [references/images/README.md](references/images/README.md) |

レイアウト・状態管理は `android-compose-ui`、Material3 コンポーネントとテーマは `android-compose-components` の担当。
