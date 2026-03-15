---
name: note-draft
description: Markdownファイルをnote.comに下書き投稿するスキル
version: 0.2.0
license: MIT
---

# note-draft

Markdownファイルとヘッダー画像を指定して、note.comに記事を下書き保存します。
本文中の画像（スクリーンショット等）も自動でアップロードできます。

## トリガー

日本語:
- 「noteに投稿して」
- 「note.comに記事を下書き保存して」
- 「この記事をnoteにアップして」
- 「Markdownをnoteに投稿」

English:
- "Post to note.com"
- "Save article as draft on note"
- "Upload this article to note.com"

## 初回セットアップ

このスキルの初回実行時は、以下のセットアップが必要です。

### 1. 依存パッケージのインストール

```bash
cd "$SKILL_DIR" && npm install
```

### 2. Playwrightブラウザのインストール

```bash
npx playwright install --with-deps chromium
```

### 3. 環境変数の設定

`$SKILL_DIR/.env` ファイルを作成し、以下を設定してください：

```
NOTE_EMAIL=your-email@example.com
NOTE_PASSWORD=your-password
NOTE_USERNAME=your-note-username
```

NOTE_USERNAMEは、あなたのnote.comプロフィールURL（`https://note.com/USERNAME`）のUSERNAME部分です。

## 使い方

### 投稿前の確認フロー

投稿を実行する前に、以下の判定と確認を行ってください。
ユーザーが既にコマンドやメッセージで明示している項目はスキップしてOKです。

**1. 本文画像の検出（自動判定）：**

記事ファイルを Read で読み、本文中に `![alt](path)` 形式の画像参照があるか確認する。

- **画像あり** → Playwright モードが使われる。画像パスの解決が必要
- **画像なし** → API モードで高速投稿。追加確認不要

**2. 画像パスの解決（Playwright モード時）：**

本文画像のパス（例: `/images/media/foo/bar.png`）を実ファイルに解決できるか確認する。

自動推定ロジック:
- 記事ファイルのパスに `/content/` が含まれる → 同プロジェクトの `public/` を基準にする
- フロントマターの `image` パスに `/images/` が含まれる → その手前のディレクトリを基準にする

自動推定できない場合（非標準的なプロジェクト構成など）は、AskUserQuestion で確認：
- 「本文中の画像ファイルはどのディレクトリにありますか？」
- → `--image-base` オプションに渡す

**3. アイキャッチ画像の確認：**

画像パスが `--image` やフロントマターの `image` で指定されていない場合、AskUserQuestion で確認：
- 選択肢: 「画像なしで投稿」「画像パスを指定する」

### 動作モード

スクリプトは本文中の画像参照（`![alt](path)`）を自動検出し、適切なモードを選択します。

| モード | 条件 | 特徴 |
|--------|------|------|
| **API モード** | 本文に画像なし | 高速・軽量。REST API で直接投稿 |
| **Playwright モード** | 本文に画像あり | note.com エディタを自動操作して画像をアップロード |

### 投稿コマンド

**基本（自動モード選択）：**
```bash
cd "$SKILL_DIR" && node scripts/publish.mjs <path/to/article.md>
```

**ヘッダー画像を明示指定：**
```bash
cd "$SKILL_DIR" && node scripts/publish.mjs <path/to/article.md> --image <path/to/header.jpg>
```

**既存の下書きを更新（Playwright モード時）：**
```bash
cd "$SKILL_DIR" && node scripts/publish.mjs <path/to/article.md> --draft-url <editor-url>
```

**本文画像を無視してAPIモードで投稿：**
```bash
cd "$SKILL_DIR" && node scripts/publish.mjs <path/to/article.md> --no-images
```

**本文画像の基準ディレクトリを明示指定：**
```bash
cd "$SKILL_DIR" && node scripts/publish.mjs <path/to/article.md> --image-base <path/to/public>
```

※ 記事は常に下書きとして保存されます。

### フロントマター

Markdownファイルのフロントマターで以下を指定できます：

```yaml
---
title: "記事タイトル"
tags:
  - AI
  - プログラミング
image: ./header.png
---
```

- `title`: 記事タイトル（未指定の場合は本文のh1を使用）
- `tags`: タグ（配列）— note-publish スキルと連携時にハッシュタグとして設定されます
- `image`: ヘッダー画像の相対パス

### 本文画像のパス解決

Playwright モードでは、本文中の画像パス（例: `/images/media/foo/bar.png`）を実際のファイルパスに変換する必要があります。

**自動推定**: Next.js プロジェクト構成（`content/` + `public/`）を自動検出します。
**手動指定**: `--image-base` オプションで基準ディレクトリを指定できます。

## 出力

### 成功時（API モード）

```
✓ 記事を下書き保存しました
  URL: https://note.com/username/n/n1a2b3c4d5e6
  記事ID: 12345678
```

### 成功時（Playwright モード）

```
✓ 記事を下書き保存しました
  URL: https://note.com/username/n/n1a2b3c4d5e6
  Editor: https://editor.note.com/notes/n1a2b3c4d5e6/edit/
```

### 失敗時

```
✗ 記事の投稿に失敗しました
  エラー: 401 Unauthorized - Cookieが期限切れです
```

## 連携

下書き投稿後に公開やハッシュタグ設定を行うには、note-publish スキルを使用してください：
- 「この記事を公開して」→ note-publish スキルが起動
- 出力のURLまたは記事キーを note-publish に渡せます

一気通貫で投稿から公開まで行うには、note-automation スキルを使用してください。

## トラブルシューティング

- **ログイン失敗**: NOTE_EMAIL と NOTE_PASSWORD が正しいか確認してください
- **Cookie期限切れ**: 自動的に再ログインを試みます。失敗する場合は `.env` の認証情報を確認してください
- **画像アップロード失敗**: JPEG, PNG, GIF のみ対応。10MB以下のファイルを使用してください
- **Playwright未インストール**: `npx playwright install --with-deps chromium` を実行してください
- **本文画像のパスが見つからない**: `--image-base` で画像ディレクトリを明示指定してください
- **Out of capacity（Playwright モード）**: note.com エディタの読み込みに時間がかかる場合があります。再実行してください
