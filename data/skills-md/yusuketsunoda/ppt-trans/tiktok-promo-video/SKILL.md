---
name: tiktok-promo-video
description: >-
  promo-video/ 配下のRemotion動画プロジェクト専用。TikTok縦型プロモ動画のシーン作成・
  編集・レンダリングワークフローを提供する。promo-video/ 内のファイルを触る作業や、
  Remotionコンポーネントの追加・修正で使うこと。
  汎用的な動画編集やTikTok一般の質問には対応しない。
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
user-invocable: true
---

# TikTok Promo Video (Remotion)

PPT翻訳SaaSのTikTok縦型プロモ動画をRemotionで作成・編集するスキル。

## When to Use This Skill

- TikTokプロモ動画の新規シーン作成・既存シーン編集
- 動画の文言・タイミング・レイアウト修正
- 新しいComposition（A/Bバリアント）の追加
- コンポーネント追加・修正
- レンダリングとデバッグ

## Project Structure

```
promo-video/
├── package.json              # Remotion + React（バージョンはpackage.json参照）
├── tsconfig.json
├── public/screenshots/       # スクリーンショット素材
│   ├── upload.png
│   ├── dashboard-empty.png
│   └── landing.png
└── src/
    ├── index.ts              # registerRoot(RemotionRoot)
    ├── Root.tsx              # Composition登録（Folder + Composition）
    ├── constants.ts          # 全定数: FPS, サイズ, シーン尺, カラー, コピー
    ├── fonts.ts              # NotoSansJP (@remotion/google-fonts)
    ├── motion.ts             # アニメーションユーティリティ
    ├── index.css             # Tailwind (optional)
    ├── TikTokAd.tsx          # Ad版メイン (Sequence)
    ├── TikTokPromo.tsx       # LP版メイン (TransitionSeries)
    ├── components/
    │   ├── Background.tsx    # ダーク背景
    │   ├── SafeArea.tsx      # TikTok安全領域 (top:160, bottom:260)
    │   ├── KineticLine.tsx   # テキスト表示（emphasis, veil対応）
    │   ├── Icons.tsx         # SVGアイコン（Bolt, Shield, Table, Globe, Pen, Arrow）
    │   ├── TapRing.tsx       # タップアニメーション
    │   ├── TimerBadge.tsx    # タイマー表示
    │   ├── ProgressBar.tsx   # プログレスバー
    │   ├── GlowEffect.tsx    # グロー演出
    │   └── PhoneMockup.tsx   # スマホモック
    └── scenes/
        ├── HookScene.tsx     # LP: フック（課題提示）
        ├── SolutionScene.tsx # LP: 証拠（タイマー + スクショ）
        ├── DemoScene.tsx     # LP: 編集デモ（1行修正）
        ├── FeaturesScene.tsx # LP: 特徴カード（速い/表も翻訳/多言語/直せる）
        ├── CTAScene.tsx      # LP: CTA（comment/try）
        ├── AdHookScene.tsx   # Ad: Before/After カード
        ├── AdProofScene.tsx  # Ad: タイマー + スクショ
        ├── AdDiffScene.tsx   # Ad: 1行修正デモ
        └── AdCTAScene.tsx    # Ad: CTA（profile/comment）
```

## TikTok Format Constraints

| 項目 | 値 |
|------|-----|
| 解像度 | 1080 x 1920 (9:16 縦型) |
| FPS | 30 |
| Safe Area上部 | 160px (UIオーバーレイ) |
| Safe Area下部 | 260px (UIオーバーレイ) |
| Safe Area左右 | 60px padding |
| Ad版尺 | 11.5s = 345f |
| LP版尺 | 15.0s = 450f |

## Composition Architecture

### Ad版 (TikTokAd) — `Sequence` ベース

```
Hook(24f/0.8s) → Proof(126f/4.2s) → Diff(105f/3.5s) → CTA(90f/3.0s) = 345f
```

- `Sequence` の `from` + `durationInFrames` で正確なフレーム制御
- `COPY_VARIANTS` (A/B/C) で文言A/Bテスト
- `ctaVariant` ("profile" | "comment") でCTAモード切替

### LP版 (TikTokPromo) — `TransitionSeries` ベース

```
Hook(29f) → Proof(107f) → Edit(143f) → Cards(128f) → CTA(75f)
= 482f - 4*8f(transitions) = 450f
```

- `TransitionSeries` + `linearTiming` でシーン間トランジション
- トランジション尺 = 8f (LP_TRANSITION)
- **計算式**: 合計 = sum(シーン尺) - (トランジション数 * トランジション尺)

## Animation Rules (CRITICAL)

### 禁止事項
- **CSS transition/animation 禁止** — Remotionは各フレームを独立レンダリングするため動作しない
- **emoji禁止** — クロスプラットフォームでレイアウトズレ。SVGアイコン (Icons.tsx) を使用
- **native `<img>` 禁止** — `<Img>` + `staticFile()` を使用

### 必須パターン
```typescript
// アニメーションは必ず useCurrentFrame + interpolate/spring
const frame = useCurrentFrame();
const opacity = interpolate(frame, [0, 10], [0, 1], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
```

### motion.ts ユーティリティ
| 関数 | 用途 | 特徴 |
|------|------|------|
| `fadeIn(frame, start, duration)` | フェードイン | interpolate |
| `fadeOut(frame, start, duration)` | フェードアウト | interpolate |
| `enterFromBottom(frame, start, duration)` | 下から登場 | Easing.out(exp) |
| `enterFromRight(frame, start, duration)` | 右から登場 | Easing.out(exp) |
| `scaleIn(frame, fps, delay)` | スケールイン | spring(damping:200) — バウンスなし |
| `springBounce(frame, fps, delay)` | バウンス | spring(damping:12, stiffness:200) |

## Component API Quick Reference

詳細は [components.md](components.md) を参照。

| コンポーネント | 主なProps | 用途 |
|--------------|----------|------|
| `SafeArea` | children | TikTok安全領域ラッパー |
| `KineticLine` | text, fontSize, emphasisWord, veil | テキスト表示（固定幅、中央揃え） |
| `Icons.*` | size | SVGアイコン (Bolt/Table/Globe/Pen/Arrow) |
| `TapRing` | x, y, delay | タップ演出 |
| `TimerBadge` | seconds, done | タイマー表示 |
| `ProgressBar` | progress, done, width | 進捗バー |
| `Background` | - | ダーク背景 |
| `GlowEffect` | color, size, delay | グロー演出 |

## Workflow

### 新規シーン作成

1. `constants.ts` にシーン尺を定義
2. `scenes/` にシーンコンポーネントを作成
3. メインコンポーネント (TikTokAd/TikTokPromo) にシーンを追加
4. TransitionSeries使用時はフレーム計算を検証:
   `sum(scenes) - (transition_count * LP_TRANSITION) = LP_FRAMES`

### 文言変更

1. LP版: 各シーンファイル内のテキスト直接変更
2. Ad版: `constants.ts` の `COPY_VARIANTS` (A/B/C) を変更

### レンダリング

```bash
cd promo-video
npx tsc --noEmit            # 型チェック（必須）
npm run render:all           # 全4本レンダリング
# 個別:
npm run render:ad-profile    # Ad Profile CTA
npm run render:ad-comment    # Ad Comment CTA
npm run render:lp-comment    # LP Comment CTA
npm run render:lp-try        # LP Try CTA
```

出力先: `promo-video/out/`

## Common Pitfalls

| 問題 | 原因 | 対処 |
|------|------|------|
| Folder name error | Folder nameにスペース | a-z, A-Z, 0-9, `-` のみ使用 |
| NotoSansJP subset error | "japanese" subset指定 | 番号付きsubset `[0]`-`[123]` を使用 |
| 循環参照 | Root.tsx ↔ Composition | fonts.ts を独立ファイルに分離済み |
| render command format | `remotion render Root CompId` | `remotion render CompId --output path` |
| 画像表示されない | native `<img>` | `<Img src={staticFile("path")}/>` |
| フォントずれ | fontFamily未設定 | AbsoluteFill の style に `fontFamily` 設定 |
| レイアウトずれ | 固定幅未設定 | KineticLine (maxWidth), テキストはcenter align |

## AI Assistant Instructions

このスキルが有効化された時:

1. **promo-video/ で作業**: cd せず絶対パスを使用
2. **constants.ts を起点に**: 尺・カラー・コピーはすべてここ
3. **型チェック必須**: 変更後は `npx tsc --noEmit` を実行
4. **レンダリング確認**: `npm run render:all` で全本出力確認
5. **Remotion best practices skill も参照**: アニメーション・トランジション詳細

Always:
- アニメーションは `useCurrentFrame` + `interpolate`/`spring` のみ
- テキスト表示は `KineticLine` を優先使用
- アイコンは `Icons.tsx` のSVGアイコンを使用（emoji禁止）
- 画像は `<Img src={staticFile("...")}/>` を使用
- TransitionSeries のフレーム計算を検証する
- SafeArea 内にコンテンツを配置する

Never:
- CSS transition/animation を使わない
- emoji をテキストに含めない
- native `<img>` を使わない
- フレーム計算を検証せずにコミットしない
