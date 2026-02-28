---
name: note-publish
description: note.comの下書き記事にハッシュタグを設定し公開するスキル
version: 0.1.0
license: MIT
---

# note-publish

note.comの下書き記事に対して、ブラウザ自動化でハッシュタグの設定や記事の公開を行います。

## トリガー

日本語:
- 「noteの記事を公開して」
- 「ハッシュタグを設定して」
- 「noteの下書きを公開」
- 「記事にタグをつけて公開して」

English:
- "Publish note article"
- "Set hashtags on note"
- "Publish draft on note.com"
- "Add tags and publish note article"

## 前提条件

- note-draft スキル（または手動）で下書き記事が作成済みであること
- 初回セットアップは note-draft スキルと共通（npm install, Playwright, .env）

## 使い方

### 公開前の確認フロー

実行する前に、以下の情報をAskUserQuestionで確認してください。
ユーザーが既にコマンドやメッセージで明示している項目はスキップしてOKです。

**確認項目：**

1. **対象記事**: 記事URL または 記事キー（例: `n1a2b3c4d5e6`）
2. **ハッシュタグ**: カンマ区切り or MDファイルのフロントマターから取得
3. **公開するか**: 公開する / 下書きのまま（タグ設定のみ）

```
例: AskUserQuestion
question: "公開設定を確認します"
options:
  - header: "対象記事"
    - "URLを指定する"
    - "記事キーを指定する"
  - header: "ハッシュタグ"
    - "タグを手動入力"
    - "MDファイルのフロントマターから取得"
    - "タグなし"
  - header: "公開"
    - "記事を公開する"
    - "下書きのまま（タグ設定のみ）"
```

### コマンド

**ハッシュタグ設定 + 公開：**
```bash
cd "$SKILL_DIR" && node scripts/note-publish.mjs <article> --tags "AI,プログラミング" --publish
```

**ハッシュタグ設定のみ（下書き維持）：**
```bash
cd "$SKILL_DIR" && node scripts/note-publish.mjs <article> --tags "AI,プログラミング"
```

**MDファイルからタグ読取：**
```bash
cd "$SKILL_DIR" && node scripts/note-publish.mjs <article> --md <path/to/article.md> --publish
```

### 引数

| 引数 | 説明 |
|------|------|
| `<article>` | 記事URLまたは記事キー（必須） |
| `--tags <csv>` | カンマ区切りのハッシュタグ |
| `--md <path>` | MDファイルパス（フロントマターからタグ読取） |
| `--publish` | 記事を公開する（未指定時は下書き保存） |
| `--yes` | 確認プロンプトをスキップ |
| `--help` | ヘルプを表示 |

`--tags` と `--md` の両方が指定された場合、`--tags` が優先されます。

## 出力

### 成功時

```
✓ ハッシュタグを設定し、記事を公開しました
  URL: https://note.com/username/n/n1a2b3c4d5e6
  タグ: #AI, #プログラミング
  ステータス: published
```

### 失敗時

```
✗ 操作に失敗しました
  エラー: ハッシュタグ入力欄が見つかりません。note.comのUI変更の可能性があります
  対処: note.comのWebUIから手動で操作してください
```

## 連携

- **note-draft**: 下書き投稿スキル。出力のURLまたは記事キーを本スキルの `<article>` に渡せます
- **note-automation**: 下書き投稿から公開までを一気通貫で実行するオーケストレーションスキル

## セレクタヘルスチェック

note.comのUI変更によりスキルが動作しなくなった場合、以下のコマンドでセレクタの有効性を検証できます：

```bash
cd "$SKILL_DIR" && node scripts/inspect-editor.mjs <articleKey> --check
```

## トラブルシューティング

- **セレクタ未検出**: note.comのUI変更の可能性があります。`inspect-editor.mjs --check` でセレクタの有効性を確認し、`lib/selectors.mjs` を更新してください
- **ログイン失敗**: `.env` の認証情報を確認してください
- **タイムアウト**: ネットワーク接続を確認し、再実行してください
- **Playwright未インストール**: `npx playwright install --with-deps chromium` を実行してください
