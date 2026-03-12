---
name: scope-guard
description: >-
  コミットやPR作成前に「意図しない差分」を検出し、ブランチ目的とのズレを警告する。
  混入した無関係な変更の破棄コマンドまで提示する。コミット前のスコープ確認、
  差分に余計なファイルが混ざっていないかのチェック、PRのスコープが広がりすぎていないかの
  検証で使うこと。「このブランチの目的と関係ない変更が入っていないか？」という
  疑問があれば必ず使うこと。
allowed-tools: Read, Grep, Glob, Bash
user-invocable: true
---

# Scope Guard

コミット前に「意図しない差分」を検出し、ブランチ目的とのズレを警告するスキル。
混入差分の破棄コマンドまで提示する。

## トリガー

- ユーザーが `/scope-guard` を実行
- "スコープチェック", "差分チェック", "混入チェック" に言及
- `/smart-commit` の前段として組み込み可能

## 実行手順

### 1. ブランチ目的の推定

```bash
# ブランチ名からカテゴリを推定
git branch --show-current
```

| ブランチプレフィックス | 期待カテゴリ |
|---------------------|------------|
| `feat/*` | src（機能コード）、tests |
| `fix/*` | src（修正箇所）、tests |
| `chore/*` | config、docs、scripts |
| `refactor/*` | src（構造変更）、tests |
| `docs/*` | docs、.claude/ |
| `test/*` | tests、e2e |

### 2. 差分のカテゴリ分類

```bash
git diff --name-only | while read f; do echo "$f"; done
```

各ファイルを以下のカテゴリに分類:

| カテゴリ | パターン | 例 |
|---------|---------|-----|
| **runtime** | `.nvmrc`, `.node-version`, `engines` in package.json | Node.jsバージョン |
| **deps** | `package.json` (dependencies), `package-lock.json` | 依存関係 |
| **config** | `*.config.*`, `tsconfig.json`, `.eslintrc` | 設定ファイル |
| **infra** | `.github/`, `infrastructure/`, `Dockerfile` | インフラ |
| **docs** | `*.md`, `docs/`, `.claude/`, `messages/` | ドキュメント |
| **src** | `src/**/*.ts`, `src/**/*.tsx` | アプリケーションコード |
| **tests** | `tests/**`, `e2e/**` | テスト |
| **python** | `python_backend/**`, `*.py` | Python処理 |

### 3. スコープ判定

ブランチの期待カテゴリと実際の差分カテゴリを比較:

| 判定 | 条件 | アクション |
|------|------|-----------|
| **IN_SCOPE** | 期待カテゴリと一致 | 問題なし |
| **RELATED** | 期待カテゴリに付随（例: feat + tests） | 許容 |
| **OUT_OF_SCOPE** | 期待カテゴリと無関係 | 警告 + 破棄コマンド提示 |

### 4. レポート出力

```markdown
## Scope Guard Report

**ブランチ**: `fix/remove-isAdminEmail-reference`
**期待カテゴリ**: src, tests

### IN_SCOPE (2件)
- `src/app/actions/upload/security-checks.ts` → src
- `tests/lib/security/api-security-bypass.test.ts` → tests

### OUT_OF_SCOPE (2件) ⚠️
- `.nvmrc` → runtime (Node.jsバージョン変更)
- `package.json` → runtime (engines変更)

### 推奨アクション
```bash
# OUT_OF_SCOPE ファイルを破棄
git restore .nvmrc package.json
```
```

### 5. 対話モード

OUT_OF_SCOPE が検出された場合:

1. 各ファイルの差分を簡潔に表示
2. 「破棄」「コミットに含める」「別ブランチに退避」の選択肢を提示
3. ユーザーの判断で実行

## smart-commit との連携

`/smart-commit` のステップ0（docs-sync前）に `/scope-guard` を組み込み可能:

```
/scope-guard → /docs-sync → /smart-commit
```

## AI Assistant Instructions

このスキルが有効化された時:

1. **ブランチ名取得**: `git branch --show-current` でカテゴリを推定
2. **差分取得**: `git diff --name-only` で変更ファイル一覧を取得
3. **カテゴリ分類**: 各ファイルを runtime/deps/config/infra/docs/src/tests/python に分類
4. **スコープ判定**: ブランチの期待カテゴリと比較し IN_SCOPE / RELATED / OUT_OF_SCOPE を判定
5. **レポート出力**: OUT_OF_SCOPE がある場合は破棄コマンドを提示
6. **ユーザー判断**: 「破棄」「コミットに含める」「別ブランチに退避」の選択肢を提示

Always:
- OUT_OF_SCOPE ファイルの差分を簡潔に表示する（変更内容を見ないと判断できない）
- 破棄コマンドは `git restore <file>` 形式で提示する
- RELATED（tests等）は許容として扱い、警告しない

Never:
- ユーザー確認なしでファイルを破棄しない
- ステージ済み変更を勝手にリセットしない

## 教訓

- Node 22→24 が `.nvmrc`/`package.json` に無関係に混入した事故（2026-02-22）
- `git status --short` の目視チェックだけでは見逃しやすい
- カテゴリ分類で機械的に検出し、判断コストを削減する
