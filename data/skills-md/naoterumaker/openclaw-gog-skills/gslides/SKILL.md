---
name: gslides
description: >
  Google スライド操作（作成・編集・エクスポート・Markdownからスライド生成）を gog CLI (v0.10.0) で行う。
  「スライド作って」「プレゼン作成」「スライドをPDFで」「Markdownからスライド」などで発火。
---

# Google Slides 操作スキル (gog v0.10.0)

gog CLI で Google スライドを操作する。

**実行パス:** `gog`

**認証アカウント:** (gogで認証したアカウント)

## Execution Notes

- `exec` ツールで実行時、`timeout: 60` を指定
- プレゼンテーションIDは URL `https://docs.google.com/presentation/d/<presentationId>/edit` から取得可能

---

## コマンドリファレンス

### プレゼンテーション作成

```bash
gog slides create "<title>"
gog slides create "<title>" --parent "<folderId>"        # 特定フォルダに作成
gog slides create "<title>" --template "<templateId>"    # テンプレートからコピー作成
```

### Markdownからスライド作成

```bash
gog slides create-from-markdown "<title>" --content "# Slide 1\n\nContent"
gog slides create-from-markdown "<title>" --content-file "./slides.md"
gog slides create-from-markdown "<title>" --content-file "./slides.md" --parent "<folderId>"
```

### プレゼンテーション情報取得

```bash
gog slides info <presentationId>
gog slides info <presentationId> --json
```

### プレゼンテーションコピー

```bash
gog slides copy <presentationId> "コピーのタイトル"
gog slides copy <presentationId> "コピーのタイトル" --parent "<folderId>"
```

### エクスポート（ダウンロード）

```bash
gog slides export <presentationId>                                  # PPTX（デフォルト）
gog slides export <presentationId> --format pdf                     # PDF形式
gog slides export <presentationId> --format pdf --out "./deck.pdf"  # 出力先指定
gog slides export <presentationId> --format pptx --out "./deck.pptx"
```

### スライド一覧

```bash
gog slides list-slides <presentationId>
gog slides list-slides <presentationId> --json
```

### スライド内容読み取り

```bash
gog slides read-slide <presentationId> <slideId>
gog slides read-slide <presentationId> <slideId> --json
```

ノート、テキスト要素、画像情報を返す。slideIdは `list-slides` で取得。

### 画像スライド追加

```bash
gog slides add-slide <presentationId> ./image.png
gog slides add-slide <presentationId> ./image.png --notes "説明テキスト"
gog slides add-slide <presentationId> ./image.png --notes-file "./notes.txt"
gog slides add-slide <presentationId> ./image.png --before <slideId>   # 指定スライドの前に挿入
```

フルブリード画像スライドを追加。`--before` 省略時は末尾に追加。

### スライド削除

```bash
gog slides delete-slide <presentationId> <slideId>
```

### スピーカーノート更新

```bash
gog slides update-notes <presentationId> <slideId> --notes "新しいノート"
gog slides update-notes <presentationId> <slideId> --notes-file "./notes.txt"
gog slides update-notes <presentationId> <slideId> --notes ""   # ノートをクリア
```

### 画像差し替え

```bash
gog slides replace-slide <presentationId> <slideId> ./new-image.png
gog slides replace-slide <presentationId> <slideId> ./new-image.png --notes "更新ノート"
gog slides replace-slide <presentationId> <slideId> ./new-image.png --notes-file "./notes.txt"
gog slides replace-slide <presentationId> <slideId> ./new-image.png --notes ""  # ノートをクリア
```

既存スライドの画像をその場で差し替え。`--notes` 省略時は既存ノートを保持。

---

## 出力オプション

| オプション | 説明 |
|-----------|------|
| `--json` / `-j` | JSON出力 |
| `--plain` / `-p` | TSV出力（パース向け） |
| `--results-only` | JSON時、結果のみ出力 |
| `--select "field1,field2"` | JSON時、フィールド絞り込み |
| `--dry-run` / `-n` | 変更せず意図を表示 |

---

## 典型ワークフロー

### Markdownからスライド作成

```bash
# 1. Markdownファイルを用意（---でスライド区切り、#でタイトル）
cat > /tmp/slides.md << 'EOF'
# プロジェクト概要

目的と背景の説明

---

# スケジュール

- Phase 1: 設計（2月）
- Phase 2: 開発（3-4月）
- Phase 3: テスト（5月）

---

# まとめ

次のステップと担当者
EOF

# 2. スライド作成
gog slides create-from-markdown "プロジェクト報告" --content-file /tmp/slides.md --json
```

### 画像デッキ作成

```bash
# 1. 空のプレゼンテーション作成
gog slides create "写真アルバム" --json
# → presentationId を取得

# 2. 画像スライドを順次追加
gog slides add-slide <presentationId> ./photo1.png --notes "東京タワー"
gog slides add-slide <presentationId> ./photo2.png --notes "富士山"
gog slides add-slide <presentationId> ./photo3.png --notes "京都"

# 3. PDF出力
gog slides export <presentationId> --format pdf --out "./album.pdf"
```

### スライド内容確認・編集

```bash
# 1. スライド一覧を取得
gog slides list-slides <presentationId> --json

# 2. 特定スライドの内容を読む
gog slides read-slide <presentationId> <slideId>

# 3. ノートを更新
gog slides update-notes <presentationId> <slideId> --notes "修正したノート"

# 4. 画像を差し替え
gog slides replace-slide <presentationId> <slideId> ./updated-image.png
```

### テンプレートからプレゼン作成

```bash
# 1. テンプレートをコピー
gog slides copy <templateId> "Q1レビュー 2026" --json

# 2. スライド一覧で構造確認
gog slides list-slides <newPresentationId>

# 3. 必要に応じてスライド追加・削除
gog slides add-slide <newPresentationId> ./chart.png --notes "売上グラフ"
gog slides delete-slide <newPresentationId> <unwantedSlideId>
```

### エクスポート

```bash
# PDF出力
gog slides export <presentationId> --format pdf --out "./presentation.pdf"

# PPTX出力
gog slides export <presentationId> --format pptx --out "./presentation.pptx"
```

---

## 注意事項

- **プレゼンテーションの一覧取得**: `gog slides` にはlistコマンドがない。Drive経由で検索する: `gog drive ls --query "mimeType='application/vnd.google-apps.presentation'"`
- **slideId の取得**: `list-slides` で各スライドのオブジェクトIDを確認してから操作する
- **画像形式**: add-slide / replace-slide はローカルのPNG/JPG/GIFファイルを受け付ける
- **ノートの保持**: replace-slide で `--notes` を省略すると既存ノートが保持される。クリアするには `--notes ""` を指定
- **export のデフォルト**: 形式はPPTX。PDFが必要なら `--format pdf` を明示する
- **create-from-markdown**: `--content`（インライン）または `--content-file`（ファイル）のいずれかが必要
- **破壊的操作**: delete-slide は確認プロンプトが出る。`-y` でスキップ可能
