---
name: update-docs
description: |
  Update documentation after code changes. Use when API endpoints, database schema,
  backend/frontend structure, or block definitions have been modified.
---

# Update Documentation

コード変更に伴うドキュメント更新。

## 更新判定

| 変更内容 | 更新対象ドキュメント |
|---------|---------------------|
| APIエンドポイント追加/変更 | docs/API.md, backend/openapi.yaml |
| DBスキーマ変更 | docs/DATABASE.md |
| 新規ブロック追加 | docs/BLOCK_REGISTRY.md |
| Backend構造変更 | docs/BACKEND.md |
| Frontend構造変更 | docs/FRONTEND.md |
| 新規composable追加 | docs/FRONTEND.md |

## 更新手順

### 1. 変更内容を特定

```bash
git diff --stat
```

### 2. 該当ドキュメントを確認

対象ドキュメントを読み、既存の記載形式を確認する。

### 3. ドキュメントを更新

既存の形式に合わせて更新。以下を心がける:

- 簡潔で明確な説明
- 具体的な使用例
- 関連コードへのパス参照

### 4. 整合性確認

- コードとドキュメントの整合性
- 他ドキュメントへの参照リンクが有効か

## 更新不要なケース

- 内部リファクタリングのみ（外部インターフェース変更なし）
- テストコードのみの変更
- コメント・フォーマット修正のみ

## 次のステップ

ドキュメント更新完了後、PR作成へ進む。
