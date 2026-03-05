---
name: pdf-vision-reader
description: Converts PDF pages to images and uses vision analysis to extract content including diagrams, charts, and visual elements. Use for PDFs with rich visual content. Requires pdf2image and poppler-utils.
---

# PDF Vision Reader

図表が多い PDF を画像化して、Claude の vision 機能で内容を解析・Markdown 化するスキルです。

## クイックスタート

### 基本的な使い方

```bash
# 1. PDF を画像に変換
wsl python3 scripts/pdf_to_images.py "/mnt/c/path/to/file.pdf"

# 2. 各画像を Read ツールで読み込んで解析
# 3. Markdown 形式でまとめる
```

## 前提条件

必要なパッケージ：

```bash
# Python パッケージ
wsl pip3 install pdf2image Pillow

# システムパッケージ (poppler)
wsl sudo apt-get update
wsl sudo apt-get install -y poppler-utils
```

## ワークフロー

### ステップ1: PDF を画像に変換

```bash
wsl python3 scripts/pdf_to_images.py "/mnt/c/path/to/document.pdf"
```

これにより `document_pages/` ディレクトリが作成され、各ページが画像として保存されます：
- `page_001.png`
- `page_002.png`
- `page_003.png`
- ...

### ステップ2: 各画像を解析

Read ツールで各画像を順番に読み込み、内容を解析します。

**解析時の指示例:**
```
この画像の内容を詳しく説明してください：
- タイトルや見出し
- 本文テキスト
- 図表の説明
- グラフやチャートのデータ
- 重要なポイント
```

### ステップ3: Markdown に統合

各ページの解析結果を統合して、一つの Markdown ファイルを作成します。

## 使用例

### 例1: プレゼンテーション資料を Markdown 化

```
User: "presentation.pdf を vision で解析して Markdown 化して"
Assistant:
1. scripts/pdf_to_images.py で PDF を画像に変換
2. 各画像を Read ツールで読み込み
3. 各ページの内容を解析（タイトル、図表、テキスト）
4. 全ページの解析結果を統合
5. Write ツールで Markdown ファイルに保存
```

### 例2: 特定のページのみ解析

```
User: "document.pdf の 5-10 ページだけ解析して"
Assistant:
1. PDF を画像に変換（全ページ）
2. page_005.png から page_010.png のみ Read で読み込み
3. 該当ページの内容を Markdown 化
```

## 解析の観点

### 自動的に抽出する情報

各ページの画像から以下を抽出：

1. **テキスト情報**
   - タイトル・見出し
   - 本文テキスト
   - 箇条書きリスト
   - 注釈・キャプション

2. **図表**
   - 図の種類（フローチャート、組織図、etc.）
   - 図の説明・要約
   - 主要な要素と関係性

3. **グラフ・チャート**
   - グラフの種類（棒グラフ、円グラフ、etc.）
   - 軸ラベル
   - 主要なデータポイント
   - トレンドや傾向

4. **テーブル**
   - テーブルの構造
   - ヘッダー行
   - データの内容
   - Markdown テーブル形式に変換

5. **レイアウト・構造**
   - ページ全体のレイアウト
   - セクション分け
   - 強調されている情報

## Markdown 出力フォーマット

```markdown
# [PDFタイトル]

**解析日時:** YYYY-MM-DD
**総ページ数:** N

---

## Page 1: [ページタイトル]

### 概要
[ページの概要説明]

### 主要な内容
- [ポイント1]
- [ポイント2]

### 図表
**図1: [図のタイトル]**
[図の説明]

### テキスト内容
[ページ内のテキスト]

---

## Page 2: [ページタイトル]
...
```

## スクリプト詳細

### pdf_to_images.py

**機能:**
- PDF の各ページを PNG 画像に変換
- 解像度指定可能（デフォルト: 200 DPI）
- 出力ディレクトリの自動作成

**使い方:**
```bash
python scripts/pdf_to_images.py <pdf_path> [output_dir] [dpi]

# 例
python scripts/pdf_to_images.py document.pdf ./images 300
```

**出力:**
- `[pdf_name]_pages/page_001.png`
- `[pdf_name]_pages/page_002.png`
- ...

## 対応可能なコンテンツ

- ✅ テキスト（日本語・英語）
- ✅ 図表・ダイアグラム
- ✅ グラフ・チャート
- ✅ テーブル
- ✅ スクリーンショット
- ✅ インフォグラフィック
- ✅ 複雑なレイアウト
- ⚠️ 手書きメモ（精度は状況による）
- ⚠️ 低解像度画像（精度低下の可能性）

## テキスト抽出との違い

### pdf-reader (テキスト抽出)
- ✅ テキストのみの PDF で高速
- ✅ 純粋なテキスト抽出
- ❌ 図表は抽出不可
- ❌ レイアウトは簡略化

### pdf-vision-reader (画像解析)
- ✅ 図表・グラフを理解
- ✅ 複雑なレイアウトを保持
- ✅ ビジュアル要素の説明
- ⚠️ 処理時間が長い
- ⚠️ API コスト（画像解析）

## 推奨される使い分け

| PDF の種類 | 推奨スキル |
|-----------|----------|
| テキスト中心の文書 | pdf-reader |
| プレゼンテーション資料 | **pdf-vision-reader** |
| 図表・グラフが多い資料 | **pdf-vision-reader** |
| 技術図面・設計書 | **pdf-vision-reader** |
| 論文（図表含む） | **pdf-vision-reader** |
| 単純なテキストPDF | pdf-reader |

## トラブルシューティング

### pdf2image が見つからない

```bash
wsl pip3 install pdf2image
```

### poppler-utils が見つからない

```bash
wsl sudo apt-get update
wsl sudo apt-get install -y poppler-utils
```

### 画像変換が失敗する

- PDF が破損していないか確認
- ディスク容量を確認
- メモリ不足の可能性（大きな PDF は分割処理）

### 解析精度が低い

- DPI を上げる（300 推奨）
  ```bash
  python scripts/pdf_to_images.py document.pdf ./images 300
  ```
- 元の PDF の画質を確認

## パフォーマンス

### 処理時間の目安

| ページ数 | 画像変換 | 解析（Claude vision） | 合計 |
|---------|---------|---------------------|------|
| 10ページ | 5秒 | 30-60秒 | ~1分 |
| 30ページ | 15秒 | 90-180秒 | ~3分 |
| 100ページ | 50秒 | 300-600秒 | ~10分 |

### 最適化のヒント

1. **必要なページのみ処理**
   - 全ページ変換後、重要なページのみ解析

2. **DPI の調整**
   - 図表が多い: 300 DPI
   - テキスト中心: 150-200 DPI

3. **バッチ処理**
   - 複数 PDF を並行処理しない（順次処理）

## パス変換

Windows パスから WSL パスへの変換：

- `C:\Users\...` → `/mnt/c/Users/...`
- `D:\Projects\...` → `/mnt/d/Projects/...`

## 関連ツール

- **pdf-reader**: テキスト中心の PDF 用
- **docx-reader**: Word 文書用
- **OCR ツール**: pytesseract（テキスト特化）

## バージョン履歴

- v1.0.0 (2026-01-06): 初期リリース
  - PDF → 画像変換機能
  - Vision ベースの解析ワークフロー
  - 図表・グラフの理解対応
  - Markdown 出力フォーマット