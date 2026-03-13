---
name: commit
description: Conventional Commitsに従ってgit commitを実行
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Git Commit (Conventional Commits)

## 手順

### 1. `git status` で変更内容を確認

### 2. コミットすべきでないファイルの確認

以下のようなファイルが含まれていないかチェック：

| 種類 | 例 |
|------|-----|
| シークレット | `.env`, `*.pem`, `credentials.json`, `secrets.yaml` |
| ビルド成果物 | `node_modules/`, `dist/`, `build/`, `__pycache__/` |
| IDE設定 | `.idea/`, `.vscode/` (プロジェクト共有しない場合) |
| OS生成物 | `.DS_Store`, `Thumbs.db` |
| ログ・キャッシュ | `*.log`, `.cache/`, `coverage/` |

**該当ファイルがある場合**:
1. `.gitignore` に追加
2. `git status` で除外されたことを確認

### 3. `git diff` で差分を確認（任意）

変更内容の詳細を把握するために実行。

### 4. コミットメッセージを作成

変更内容を分析し、Conventional Commits形式でメッセージを作成。

### 5. `git add .` でステージング

### 6. `git commit` を実行（確認不要）

---

## コミットメッセージ形式

Conventional Commitsに従う:

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

### Type一覧

| type | 用途 |
|------|------|
| `feat` | 新機能 |
| `fix` | バグ修正 |
| `docs` | ドキュメントのみの変更 |
| `style` | コードの意味に影響しない変更（空白、フォーマット等） |
| `refactor` | バグ修正でも機能追加でもないコード変更 |
| `perf` | パフォーマンス改善 |
| `test` | テストの追加・修正 |
| `chore` | ビルドプロセスやツールの変更 |
| `ci` | CI設定の変更 |
| `build` | ビルドシステムや外部依存の変更 |

### Scope（任意）

変更の影響範囲を示す。例:
- `feat(auth):` - 認証機能
- `fix(api):` - API関連
- `docs(readme):` - README

### Description

- 命令形で書く（「追加した」ではなく「追加」）
- 50文字以内を目安
- 末尾にピリオドをつけない

### Body（任意）

- 3行目以降に記載
- 変更の理由や背景
- 特筆すべき実装詳細

---

## 例

```
feat(models): 新しいモデルUserを追加

ユーザー認証機能の基盤として、Userモデルを実装。
パスワードはbcryptでハッシュ化して保存する。
```

```
fix(api): レート制限のバグを修正

1分あたりのリクエスト数が正しくカウントされていなかった問題を修正。
Redis TTLの設定ミスが原因。
```

```
refactor: 認証ミドルウェアを分離
```

---

## 注意事項

- 破壊的変更がある場合は `BREAKING CHANGE:` をフッターに記載
- `.gitignore` を更新した場合は、そのことをコミットメッセージに含める
