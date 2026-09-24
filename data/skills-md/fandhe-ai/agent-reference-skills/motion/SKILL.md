---
name: motion
description: >
  Motion アニメーションライブラリ (旧 Framer Motion) リファレンス。
  React コンポーネント motion, AnimatePresence, AnimateView, LayoutGroup,
  LazyMotion, MotionConfig, Reorder。hooks useAnimate, useScroll, useSpring,
  useTransform, useMotionValue, useInView。
  vanilla JS API animate, scroll, inView, hover, press, stagger, spring,
  timeline, motionValue。Vue 版 (motion-v) v-motion ディレクティブ, useScroll
  等の composable, Motion+ 限定コンポーネント (Carousel, Cursor, Ticker,
  Typewriter, AnimateNumber)。transitions / layout / drag / gestures / SVG /
  scroll アニメーション、accessibility, performance, bundle 最適化, troubleshooting。
user-invocable: false
---

# motion

Motion (旧 Framer Motion) のリファレンススキル。React 向け (`motion/react`) と vanilla JS (`motion`) の両 API、アニメーション概念、ガイドを収録する。

## ディレクトリ構成

```text
skills/motion/
  SKILL.md
  references/
    react-components/
      README.md
      motion.md
      animate-presence.md
      animate-view.md
      layout-group.md
      lazy-motion.md
      motion-config.md
      reorder.md
    react-hooks/
      README.md
      use-animate.md
      use-scroll.md
      use-spring.md
      use-transform.md
      use-motion-value.md
      use-in-view.md
      use-drag-controls.md
      use-reduced-motion.md
      use-motion-template.md
      use-velocity.md
      use-motion-value-event.md
      use-animation-frame.md
      use-time.md
      use-page-in-view.md
    animation/
      README.md
      overview.md
      transitions.md
      layout.md
      scroll.md
      gestures.md
      drag.md
      svg.md
    vanilla-js/
      README.md
      animate.md
      scroll.md
      in-view.md
      hover.md
      press.md
      stagger.md
      spring.md
      timeline.md
      motion-value.md
    vue/
      README.md
      overview.md
      motion.md
      directive.md
      animate-presence.md
      animate-number.md
      carousel.md
      cursor.md
      radix.md
      layout-animations.md
      layout-group.md
      lazy-motion.md
      motion-config.md
      motion-value.md
      reorder.md
      scroll-animations.md
      ticker.md
      transitions.md
      typewriter.md
      gestures.md
      use-animate.md
      use-animation-frame.md
      use-drag-controls.md
      use-in-view.md
      use-motion-template.md
      use-motion-value-event.md
      use-reduced-motion.md
      use-scroll.md
      use-spring.md
      use-time.md
      use-transform.md
      use-velocity.md
    guides/
      README.md
      installation.md
      accessibility.md
      performance.md
      reduce-bundle-size.md
      troubleshooting.md
      upgrade-guide.md
      migrate-from-gsap.md
  samples/
    README.md
    basic-animation.md
    scroll-animation.md
    gesture-animation.md
    layout-animation.md
    animate-presence.md
  scripts/
    README.md
    install.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/<category>/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

カテゴリの使い分け:

- React で `<motion.div>` やフックを使う → `react-components/` `react-hooks/`
- React に依存しない素の JS で animate / scroll などを使う → `vanilla-js/`
- transition / layout / drag / gesture / SVG / scroll の概念や prop の挙動を知る → `animation/`
- Vue (`motion-v`) で `<motion>` コンポーネント / `v-motion` ディレクティブ / composable を使う → `vue/`
- インストール / アクセシビリティ / パフォーマンス / バンドル削減 / troubleshooting / 移行 → `guides/`

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| `<motion.div>` で要素をアニメーションさせたい | react-components | [references/react-components/README.md](references/react-components/README.md) |
| マウント / アンマウント時の exit アニメーション (AnimatePresence) | react-components | [references/react-components/README.md](references/react-components/README.md) |
| LayoutGroup / LazyMotion / MotionConfig / Reorder / AnimateView を使いたい | react-components | [references/react-components/README.md](references/react-components/README.md) |
| useAnimate / useScroll / useSpring / useTransform などフックを使いたい | react-hooks | [references/react-hooks/README.md](references/react-hooks/README.md) |
| 再レンダー無しで値を更新する motion value (useMotionValue) | react-hooks | [references/react-hooks/README.md](references/react-hooks/README.md) |
| ビューポート進入検知 (useInView) / Reduced Motion 検知 | react-hooks | [references/react-hooks/README.md](references/react-hooks/README.md) |
| transition (tween/spring/inertia/stagger) の指定方法 | animation | [references/animation/README.md](references/animation/README.md) |
| layout / layoutId による位置・サイズ・共有要素アニメーション | animation | [references/animation/README.md](references/animation/README.md) |
| スクロール連動 / hover・tap などジェスチャー / drag / SVG パス | animation | [references/animation/README.md](references/animation/README.md) |
| React 非依存の素の JS で animate / scroll / inView を使いたい | vanilla-js | [references/vanilla-js/README.md](references/vanilla-js/README.md) |
| hover / press / stagger / spring / timeline / motionValue (vanilla) | vanilla-js | [references/vanilla-js/README.md](references/vanilla-js/README.md) |
| Vue で `<motion>` / `v-motion` ディレクティブ / composable を使いたい | vue | [references/vue/README.md](references/vue/README.md) |
| Vue で Motion+ 限定コンポーネント (Carousel, Cursor, Ticker, Typewriter, AnimateNumber) を使いたい | vue | [references/vue/README.md](references/vue/README.md) |
| インストール・アクセシビリティ・パフォーマンス・バンドル削減・トラブルシューティング | guides | [references/guides/README.md](references/guides/README.md) |
| Framer Motion / GSAP からの移行・アップグレード | guides | [references/guides/README.md](references/guides/README.md) |
| 典型的な使い方を知りたい | samples | [samples/README.md](samples/README.md) |
| インストール・import 方法を知りたい | scripts | [scripts/README.md](scripts/README.md) |
