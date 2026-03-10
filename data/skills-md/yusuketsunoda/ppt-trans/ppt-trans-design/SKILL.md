---
name: ppt-trans-design
description: >-
  このプロジェクト（翻訳xPPT編集SaaS）専用のデザインシステム。Product UX原則
  （Diff表示/承認フロー/信頼性/レイアウト整合）とMD3トークン基盤の独自カラーパレットを定義する。
  UIコンポーネントの新規作成、ダークモード対応、翻訳UIの設計、ミニマルデザインの適用など、
  このプロジェクトのUI実装で必ず参照すること。汎用Material Designではなく
  プロジェクト固有のデザイン判断が必要な場面で使うこと。
allowed-tools: Read, Grep, Glob, Edit, Write
user-invocable: true
---

# ppt-trans Design System

翻訳xPPT編集SaaS専用のデザインシステム。MD3（Material Design 3）トークンを内部基盤として含む。
このプロジェクトのUI実装はすべてこのスキルがカバーする（別途 `material-design` スキルを使う必要はない）。

## When to Use This Skill

- 新規UIコンポーネントを作成する時（デフォルト）
- ダークモードのデザインを実装する時
- ミニマルで洗練されたインターフェースを作成する時
- 翻訳UI（Diff表示、信頼度バッジ、バッチ承認等）を実装する時
- 既存コンポーネントのスタイルを統一する時

## 読む順番（上位が優先）

1. `docs/design/product-ux-principles.md` — 設計原則・UXパターン（WHY）
2. `.claude/rules/ui-design.md` — カラー・余白・タイポ・意味トークン（WHAT）
3. `.claude/rules/components.md` — shadcn/Radix の実装構造（HOW）
4. `references/md3-patterns.md` — MD3の実装パターン参照（State Layers、Elevation等）

## AI Assistant Instructions

このスキルが有効化された時:

1. **Product UX Principles確認**: `docs/design/product-ux-principles.md` を読み、設計原則を把握
2. **トークン確認**: `.claude/rules/ui-design.md` の意味トークンテーブルに従う
3. **状態機械確認**: インタラクティブコンポーネントは idle/loading/success/error を網羅
4. **余白の確認**: 適切なスペーシングで「呼吸する空間」を確保

Always:
- CSS変数またはTailwindユーティリティを使用する（意味トークン経由）
- インタラクティブコンポーネントに idle/loading/success/error の全状態を実装する
- エラー表示は「原因+次の一手」パターンに従う
- アニメーションは200-300msで自然な動きにする
- タッチターゲットは最小44x44pxを確保する
- 翻訳結果には信頼度情報を表示する（該当コンポーネント）
- 編集操作は「選択 -> 編集 -> 確定」の3ステップに従う

Never:
- ハードコードカラー（`#RRGGBB`, `rgb()`, `bg-[#...]`）を使用しない
- 色名（green, red, amber等）で直接指定しない（意味トークンを使う）
- アニメーションを過度に長くしない（300ms超）
- エラーメッセージのみで再試行/ヘルプの導線を省略しない
- 自動リフロー等の提案を確認なしで自動適用しない
