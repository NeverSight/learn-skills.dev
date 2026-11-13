---
name: self-review
description: |
  Self-review after code changes. Use proactively after completing any code modifications,
  before creating a pull request. Runs tests, checks code quality, and validates changes.
---

# Self Review

コード変更完了後の自己レビュー・セルフバリデーション。

## 実行手順

### 1. 変更内容の確認

```bash
git status
git diff --stat
git diff
```

### 2. ローカルCI実行

#### Backend変更がある場合

```bash
cd backend && go test ./...
cd backend && go vet ./...
```

#### Frontend変更がある場合

```bash
cd frontend && npm run check
```

### 3. コードレビュー観点でのチェック

| 観点 | チェック項目 |
|------|-------------|
| 機能性 | 要件を満たしているか |
| エラーハンドリング | nil/undefined、エラー処理は適切か |
| セキュリティ | 入力検証、認可チェックは適切か |
| パフォーマンス | N+1クエリ、不要なループはないか |
| 可読性 | 命名、構造は明確か |
| テスト | テストは十分か、エッジケースはカバーしているか |

### 4. よくある問題の検出

```bash
# デバッグコード残り
grep -r "console.log" frontend/
grep -r "fmt.Print" backend/

# TODO残り
grep -r "TODO" --include="*.go" --include="*.ts" --include="*.vue" .

# 未使用import（go vetで検出）
```

### 5. プロジェクト規約チェック

- [ ] Canonical Patternに従っているか（BACKEND.md / FRONTEND.md参照）
- [ ] ドキュメント更新が必要な変更か確認

## 完了条件

- すべてのテストがパス
- go vet / npm run check がエラーなし
- セキュリティ・パフォーマンス問題なし
- 不要なデバッグコードなし

## 次のステップ

問題がなければ、ドキュメント更新が必要か確認し、PR作成へ進む。
