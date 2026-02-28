---
name: note-automation
description: Markdownの下書き投稿からハッシュタグ設定・公開までを一気通貫で実行するオーケストレーションスキル
version: 0.1.0
license: MIT
---

# note-automation

note-draft（下書き投稿）と note-publish（タグ設定＋公開）を組み合わせ、Markdownファイルから公開まで一気通貫で実行するオーケストレーションスキルです。

## トリガー

日本語:
- 「noteに記事を投稿して公開して」
- 「note自動投稿」
- 「Markdownを書いてnoteに公開まで」
- 「noteへの投稿を自動化して」

English:
- "Automate note publishing"
- "Post and publish to note"
- "Full pipeline: draft and publish to note.com"

## 前提条件

- 初回セットアップは note-draft スキルと共通（npm install, Playwright, .env）

## 使い方

### 実行前の確認フロー

実行する前に、以下の情報をAskUserQuestionで確認してください。

```
AskUserQuestion:
  question: "note自動投稿の設定を確認します"

  Q1: "入力を指定してください"
  options:
    - "MDファイルを指定する"
    - "既存の下書き記事URL/キーを指定する"

  Q2: "実行するステップを選択してください"
  options:
    - "フル実行: 下書き投稿 → タグ設定 → 公開（推奨）"
    - "下書き投稿のみ（--draft-only）"
    - "タグ設定 + 公開のみ（--skip-draft）: 既存下書きに対して"
    - "下書き投稿 + タグ設定のみ（--skip-publish）: 公開はスキップ"

  Q3: "ハッシュタグを指定してください"
  options:
    - "フロントマターから自動取得（推奨）"
    - "手動で入力する"
    - "タグなし"

  Q4: "公開しますか？"（Q2でフル実行またはタグ設定+公開選択時のみ）
  options:
    - "公開する"
    - "下書きのまま（タグ設定のみ）"
```

### パイプライン実行

#### フルパイプライン（デフォルト）

MDファイルから下書き投稿 → ハッシュタグ設定 → 公開まで実行します。

**Step 1: note-draft（下書き投稿）**
```bash
cd "$SKILL_DIR" && node scripts/publish.mjs <path/to/article.md>
```

Step 1 の出力から articleKey を抽出します：
```
✓ 記事を下書き保存しました
  URL: https://note.com/username/n/n1a2b3c4d5e6   ← ここから "n1a2b3c4d5e6" を抽出
  記事ID: 12345678
```

抽出パターン: URLの末尾パス `/n/` 以降の文字列（`n` で始まる英数字）

**Step 2: note-publish（タグ設定 + 公開）**
```bash
cd "$SKILL_DIR" && node scripts/note-publish.mjs <articleKey> --tags "tag1,tag2" --publish
```

`<articleKey>` には Step 1 で抽出した値を使用します。
`--tags` にはフロントマターから読み取ったタグ、またはユーザー指定のタグを使用します。

#### --skip-draft（既存下書きに対してタグ設定 + 公開）

```bash
cd "$SKILL_DIR" && node scripts/note-publish.mjs <articleURL or key> --tags "tag1,tag2" --publish
```

Step 1 をスキップし、ユーザーが指定した既存の下書き記事に対して操作します。

#### --skip-publish（下書き投稿 + タグ設定のみ、公開スキップ）

Step 1 を実行した後、Step 2 を `--publish` なしで実行します：

```bash
cd "$SKILL_DIR" && node scripts/publish.mjs <path/to/article.md>
cd "$SKILL_DIR" && node scripts/note-publish.mjs <articleKey> --tags "tag1,tag2"
```

#### --draft-only（下書き投稿のみ）

```bash
cd "$SKILL_DIR" && node scripts/publish.mjs <path/to/article.md>
```

Step 2 をスキップし、note-draft のみ実行します。

### ステップ制御オプション

| オプション | 実行ステップ | ユースケース |
|-----------|-------------|-------------|
| （未指定） | note-draft → note-publish（タグ＋公開） | MDファイルから公開まで一気通貫 |
| `--skip-draft` | note-publish のみ | 既存の下書き記事にタグ＋公開 |
| `--skip-publish` | note-draft → note-publish（タグのみ） | 下書き投稿＋タグ設定まで |
| `--draft-only` | note-draft のみ | 下書き投稿のみ |

## 出力

### フルパイプライン成功時

```
=== note-automation パイプライン ===

[Step 1/2] note-draft: 下書き投稿
✓ 記事を下書き保存しました
  URL: https://note.com/username/n/n1a2b3c4d5e6
  記事ID: 12345678

[Step 2/2] note-publish: タグ設定 + 公開
✓ ハッシュタグを設定し、記事を公開しました
  URL: https://note.com/username/n/n1a2b3c4d5e6
  タグ: #AI, #プログラミング
  ステータス: published

=== 完了 ===
```

### エラー時

各ステップでエラーが発生した場合、その時点でパイプラインを停止し、エラー内容と対処法を表示します。
Step 1 で成功していれば、下書き記事は保存されたままなので、Step 2 を `--skip-draft` で再実行できます。

## 連携スキル

- **note-draft**: 下書き投稿スキル（Step 1 で使用）
- **note-publish**: タグ設定＋公開スキル（Step 2 で使用）

<!-- 将来の拡張ステップ:
Step 0: 記事作成スキル → MDファイル生成
Step 1: 画像生成スキル → アイキャッチ画像生成
Step 2: note-draft → API下書き保存（MD + 画像）
Step 3: note-publish → タグ設定 + 公開

各ステップは --skip-{step} で個別にスキップ可能。
このSKILL.mdのパイプライン定義に新ステップを追記するだけで対応できる。
-->
