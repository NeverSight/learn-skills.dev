---
name: migration-sweep
description: >-
  移行コード（TODO(migration)）の寿命チェックを機械化する。期限切れや情報不足の
  移行コードを検出し、レポート形式で出力する。コードベースにTODO(migration)が
  残っていないか確認したいとき、期限切れの移行コードを掃除したいとき、
  技術的負債の棚卸しをするときに使うこと。「あとで消す」コードの放置を防ぐ仕組み。
allowed-tools: Read, Grep, Glob, Bash
user-invocable: true
---

# Migration Sweep

移行コード（`TODO(migration)`）の寿命チェックを機械化するスキル。
期限切れ・情報不足の移行コードを検出し、レポート形式で出力する。

## トリガー

- ユーザーが `/migration-sweep` を実行
- "移行コード", "migration TODO", "期限切れTODO" に言及

## 実行手順

### 1. TODO(migration) の収集

```bash
# repo全体から TODO(migration) を検索
grep -rn "TODO(migration)" --include="*.ts" --include="*.tsx" --include="*.py" src/ tests/ e2e/ python_backend/ 2>/dev/null || echo "該当なし"
```

### 2. メタデータの解析

各 TODO(migration) について以下を抽出:

| フィールド | パターン | 必須 |
|-----------|---------|------|
| Issue ID | `[ISSUE-XXX]` or `[#XXX]` | YES |
| 期限 | `[expires=YYYY-MM-DD]` | YES |
| 削除条件 | 自由記述（TODOコメントの次行以降） | YES |

### 3. 判定ルール

| 状態 | 条件 | 重要度 |
|------|------|--------|
| **EXPIRED** | `expires` が今日以前 | P0 (即対応) |
| **MISSING_META** | Issue ID / expires / 削除条件のいずれかが欠落 | P0 (情報補完) |
| **WARNING** | expires まで30日以内 | P1 (計画) |
| **OK** | expires まで30日超 | 情報のみ |

### 4. レポート出力

```markdown
## Migration Sweep Report (YYYY-MM-DD)

### P0: 即対応 (X件)

| ファイル:行 | 状態 | 期限 | Issue | 内容 |
|------------|------|------|-------|------|
| `src/foo.ts:42` | EXPIRED | 2026-01-15 | #123 | Remove old admin check |
| `src/bar.ts:88` | MISSING_META | - | - | TODO(migration) but no metadata |

### P1: 計画 (X件)

| ファイル:行 | 期限 | 残日数 | Issue | 内容 |
|------------|------|--------|-------|------|
| `src/baz.ts:15` | 2026-03-15 | 21日 | #456 | Deprecate legacy API |

### OK (X件)
(省略可能)

### サマリー
- 総数: X件
- P0 (即対応): X件
- P1 (計画): X件
- OK: X件
```

### 5. 追加アクション提案

- **EXPIRED**: 「このコードを削除してよいか？」と確認し、削除を提案
- **MISSING_META**: テンプレート形式でメタデータ補完を提案
  ```typescript
  // TODO(migration)[ISSUE-XXX][expires=YYYY-MM-DD]:
  // <削除条件を記述>
  ```
- **WARNING**: Issue のステータス確認を促す

## テンプレート（新規移行コード用）

```typescript
// TODO(migration)[ISSUE-1234][expires=2026-05-31]:
// Remove after role-based admin check is fully deployed
// and logs show 0 hits for 14 days.
```

## AI Assistant Instructions

このスキルが有効化された時:

1. **grep で TODO(migration) を全件収集**: `src/`, `tests/`, `e2e/`, `python_backend/` を対象
2. **メタデータ解析**: Issue ID, expires, 削除条件を抽出
3. **判定ルールに従い分類**: EXPIRED / MISSING_META / WARNING / OK
4. **レポート出力**: 上記フォーマットに厳密に従う
5. **追加アクション提案**: EXPIRED には削除提案、MISSING_META にはテンプレート提供

Always:
- 全件レポートする（フィルタしない）
- P0 は件数ゼロでも「P0: 0件」と明記する
- EXPIRED の削除提案は「コードを読んで安全性を確認してから」の条件付き

Never:
- 自動削除しない（レポートのみ、修正はユーザー確認後）
- TODO(migration) 以外のTODO（TODO(fix), TODO(refactor) 等）をスコープに含めない

## 関連ルール

- `.claude/rules/dead-code-cleanup.md` — 移行コード管理セクション
- `CLAUDE.md` — push前Done条件（type-checkが最終防衛線）
