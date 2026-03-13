---
name: commit
description: Git commit skill. Use when the user asks to commit changes. Splits commits by feature/content, uses conventional commit prefixes, and ensures each commit contains only the changes described in its message.
user_invocable: true
---

# Commit Skill

変更内容を機能ごと・内容ごとに適切にコミットを分割して作成する。

---

## Commit Prefix

以下のprefixを使い分ける:

| prefix | 用途 | 例 |
|---|---|---|
| `feat` | 新機能追加・UI/振る舞いの変更 | `feat: ログインダイアログ追加` |
| `chore` | 設定・依存関係・CIなど | `chore: eslint設定更新` |
| `test` | テスト追加・修正 | `test: ArticleCard テスト追加` |
| `docs` | ドキュメント変更 | `docs: README更新` |
| `refactor` | ユーザーから見て振る舞いが変わらない内部改善 | `refactor: formatTimeAgo を共通関数に抽出` |
| `fix` | バグ修正（意図しない動作の修正） | `fix: ダイアログが閉じない問題` |

---

## Commit Message Format

### feat, chore, test, docs

1行のみ。prefixの後に内容を簡潔に書く。

```
feat: 記事一覧を2列グリッドに変更
```

### refactor, fix

3行目に**なぜその変更が必要だったか（理由）**を書く。

```
refactor: ArticleCard の formatTimeAgo をユーティリティに抽出

複数コンポーネントで同じ日時フォーマットロジックを使う必要が出たため。
```

```
fix: ログインダイアログが閉じない問題を修正

onOpenChange のコールバックが state を更新していなかったため。
```

---

## Rules

1. **機能ごと・内容ごとにコミットを分割する** — 1つのコミットに無関係な変更を混ぜない
2. **コミットメッセージに書いた内容以外の差分を含めない** — `git add` は対象ファイルを明示的に指定する（`git add -A` や `git add .` は使わない）
3. **日本語で書く** — prefix 以外は日本語
4. **Co-Authored-By を末尾に付与する**

---

## Procedure

1. `git status` と `git diff` で全体の変更を把握する
2. 変更内容を機能・目的ごとにグルーピングする
3. グループごとに以下を実行:
   a. 対象ファイルのみ `git add <file1> <file2> ...` でステージング
   b. コミットメッセージを作成（上記フォーマットに従う）
   c. `git commit` を実行
4. 全コミット完了後、`git log --oneline -n <count>` で確認

---

## Example Workflow

```bash
# 1. 変更把握
git status
git diff --stat

# 2. 機能Aのファイルだけステージング
git add src/components/features/timeline-page/timeline/Timeline.tsx
git add src/components/features/timeline-page/timeline/article-card/ArticleCard.tsx

# 3. コミット
git commit -m "$(cat <<'EOF'
feat: タイムライン記事一覧を2列グリッドに変更

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"

# 4. 機能Bのファイルだけステージング
git add src/app/layout.tsx

# 5. コミット
git commit -m "$(cat <<'EOF'
fix: layout.tsx の二重パディング修正

outer div の px-10 を削除し main を px-8 に変更。

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```
