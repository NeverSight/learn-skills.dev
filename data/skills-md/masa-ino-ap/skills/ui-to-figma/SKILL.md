---
name: ui-to-figma
description: >
  既存プロジェクトのCSS・Tailwind設定・コンポーネントを解析してデザイントークンを把握した上で、
  UIを視覚的に改善しFigma MCPサーバー経由でFigmaに送るワークフロースキル。
  単なるUI改善ではなく「プロジェクトのデザインシステムに整合した改善」が特徴。
  新しい色や間隔をハードコードせず、既存トークン・命名規則の範囲内で提案する。
  以下のような場面で使用する:
  - 「UIを見てFigmaに送って」「このページのデザインを改善してFigmaに反映して」
  - 「UIを分析してFigmaにデザイン案を作って」
  - WebアプリのUI改善とFigmaへのデザイン連携が必要なとき
  - ユーザーが「ui-to-figma」「UIをFigmaに」「デザイン改善してFigmaへ」と言ったとき
  前提: Playwright（webapp-testingスキル）とFigma MCPサーバーが利用可能であること
---

# UI to Figma ワークフロー

既存プロジェクトのデザイン言語を読み取った上でUI改善をFigmaに連携する、4ステップのワークフロー。

**このスキルの核心:** 外側から見た見た目の改善ではなく、`tailwind.config.js` やCSS変数・既存コンポーネントを先に解析し、プロジェクトのカラーパレット・スペーシングスケール・命名規則に整合した改善を行う。

1. **Setup** — `design-tokens.md` があれば読む。なければソースを解析して生成する
2. **Capture** — PlaywrightでUIをキャプチャ
3. **Improve** — 視覚＋デザイントークン両方に基づいた整合性のある改善をコードに反映
4. **Export** — Figma MCPサーバーでFigmaにデザインを送る

---

## Step 1: Setup — デザイントークンの取得

最初に `design-tokens.md` がプロジェクトルートに存在するか確認する。

### design-tokens.md が存在する場合

そのファイルを読むだけでよい。Step 2へ進む。

### design-tokens.md が存在しない場合（初回のみ）

ソースを解析して `design-tokens.md` を自動生成する。

**1. スタイル定義ファイルを探して読む**

```
Glob で以下を探す（存在するものを全て読む）:
- tailwind.config.{js,ts,cjs}
- src/styles/*.css, app/styles/*.css, styles/*.css
- src/tokens.{ts,js}, src/theme.{ts,js}, src/design-tokens.{ts,js}
- **/*.css (CSS変数 --xxx: が定義されているもの)
```

**2. コンポーネントのスタイリング手法を把握する**

```
Glob で src/components/**/*.{tsx,jsx,vue,svelte} を数ファイルサンプリングして読む
→ Tailwind / CSS Modules / styled-components / inline styles のどれを使っているか判定
```

**3. 読んだ内容から design-tokens.md を生成してプロジェクトルートに保存する**

生成するファイルのフォーマット:

```markdown
# Design Tokens — {プロジェクト名}
最終更新: {日付}

## カラーパレット
| トークン名 | 値 | 用途 |
|-----------|-----|------|
| primary   | #4F46E5 | ブランドカラー |
| gray-600  | #4B5563 | テキスト |
...

## スペーシングスケール
Tailwindデフォルト / カスタム: 4px基準 ...

## タイポグラフィ
| 用途 | クラス or 変数 | サイズ |
|------|--------------|-------|
| 見出しH1 | text-3xl font-bold | 30px |
...

## スタイリング方針
- 手法: {Tailwind / CSS Modules / styled-components}
- カラーは必ず上記トークン名を使う
- px直書き禁止 / Tailwindスケールを使う
- 既存コンポーネント: {Button, Card, Input ...}
```

> **注意:** `design-tokens.md` はプロジェクトに継続的に使うファイル。
> プロジェクトのデザインが変わったら「design-tokens.mdを再生成して」と指示する。

---

## Step 2: UIのキャプチャ

Playwrightでスクリーンショットを取得し、視覚的な問題を把握する。

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:PORT")
    page.wait_for_load_state("networkidle")
    page.screenshot(path="/tmp/ui_before.png", full_page=True)
    browser.close()
```

スクリーンショットで以下を視覚的に評価する:

- **視覚的階層**: 情報の優先度が明確か
- **余白・間隔**: 一貫したスペーシングか
- **カラーパレット**: 統一感・コントラスト比（WCAG AA: 4.5:1 以上）
- **タイポグラフィ**: フォントサイズ・ウェイトの整合性
- **レスポンシブ**: モバイル・タブレット対応状況

---

## Step 3: UI改善の実装

Step1のデザイントークンとStep2の視覚分析を**両方**踏まえて改善する。
`design-tokens.md` に定義されたトークン名・クラス・変数のみ使う。新しい値をハードコードしない。

### 改善の優先順位

1. アクセシビリティ違反（クリティカル）
2. 視認性・一貫性の問題（高）
3. スペーシング・タイポグラフィ最適化（中）
4. 微細なビジュアル調整（低）

### 実装前の整合性チェック

- 色を追加する → `design-tokens.md` のカラーパレットにある名前を使っているか？
- 間隔を変える → `design-tokens.md` のスペーシングスケールに沿っているか？
- 新コンポーネントを作る → `design-tokens.md` の既存コンポーネント一覧と命名が合っているか？

改善後に再スクリーンショットを取得して差分を確認する:

```python
page.screenshot(path="/tmp/ui_after.png", full_page=True)
```

---

## Step 4: Figmaへのエクスポート

Figma MCPサーバー（`implement-design`スキル）を使ってデザインを送る。

1. `design-tokens.md` のカラー・フォント・スペーシングをFigmaスタイルとして登録
2. 改善後UIのレイアウトをFigmaフレームとして作成
3. コンポーネントとスタイルを適用して反映

Figma MCP APIの詳細は `references/figma-mcp.md` を参照。

---

## design-tokens.md の再生成

プロジェクトのデザインが変わったとき:

```
「design-tokens.mdを再生成して」
→ Step 1の初回フローを再実行してファイルを上書き
```

---

## トラブルシューティング

| 問題 | 対処 |
|------|------|
| Playwrightが動かない | `pip install playwright && playwright install chromium` |
| Figma MCPが見つからない | `references/figma-mcp.md` のセットアップを確認 |
| スクリーンショットが空白 | `page.wait_for_load_state("networkidle")` を追加 |
| design-tokens.mdの内容が古い | 「design-tokens.mdを再生成して」と指示する |
