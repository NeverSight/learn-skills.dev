---
name: security-audit-quick
description: >-
  高速静的セキュリティスキャン。grepベースで既知の危険パターン（XSS、SQLインジェクション、
  ハードコード秘密鍵など）を網羅的に検出し、SEVERITY / file:line / why / fix 形式で
  出力する再現可能なワークフロー。「コードベース全体をざっとセキュリティチェックしたい」
  「既知の脆弱性パターンを一括検出したい」ときに使うこと。
  security-hardeningスキル（特定の脅威シナリオに対する設計〜実装）や
  security-threat-reviewスキル（レッド/ブルーチームによる包括評価）とは異なり、
  このスキルは既知パターンの高速検出に特化している。
allowed-tools: Read, Grep, Glob, Bash
user-invocable: true
context: fork
---

# /security-audit-quick - 高速静的セキュリティスキャン

## Goal

grep ベースの静的チェックで既知の危険パターンを高速検出する。
**毎回同じ手順**で実行し、結果を一覧出力する。

> `/security-hardening` との違い:
> - `/security-hardening` = 単一脅威の深掘り（脅威モデル→緩和→テスト→ゲート）
> - `/security-audit-quick` = 既知パターンの網羅的検出（grep で一括スキャン）

---

## Input

| 引数 | 説明 | デフォルト |
|------|------|-----------|
| (なし) | リポジトリ全体をスキャン | `src/` + `supabase/` |
| `--diff` | 変更ファイルのみスキャン | `git diff --name-only origin/main...HEAD` |

---

## Checks (5つ)

### Check 1: テストモードヘッダーガード

**検出**: `X-E2E-Test` / `X-Bypass-Rate-Limit` ヘッダー参照で `isProductionRuntime()` ガードなし

```bash
# X-E2E-Test / X-Bypass-Rate-Limit を使っているファイルを検出
grep -rn 'X-E2E-Test\|X-Bypass-Rate-Limit' $TARGET --include='*.ts' --include='*.tsx'

# 同一ファイルで isProductionRuntime が呼ばれていないものを BLOCKER
for f in $(grep -rl 'X-E2E-Test\|X-Bypass-Rate-Limit' $TARGET --include='*.ts' --include='*.tsx'); do
  if ! grep -q 'isProductionRuntime' "$f"; then
    echo "BLOCKER: $f"
  fi
done
```

**SEVERITY**: BLOCKER (本番でセキュリティバイパス可能)

### Check 2: ログ内 PII

**検出**: `logger.*()` 呼び出しで email/token を生値で渡している

```bash
# email を maskEmail なしで渡しているケース
grep -rn 'logger\.\(info\|warn\|error\|debug\)' $TARGET --include='*.ts' --include='*.tsx' \
  | grep 'email:' | grep -v 'maskEmail\|email:.*mask\|email:.*redact'

# token を maskToken なしで渡しているケース
grep -rn 'logger\.\(info\|warn\|error\|debug\)' $TARGET --include='*.ts' --include='*.tsx' \
  | grep 'token:' | grep -v 'maskToken\|tokenPresent\|tokenValid\|csrf-token\|tokenRotat'
```

**SEVERITY**: WARNING (GDPR/CCPA リスク)

### Check 3: SECURITY DEFINER + REVOKE/GRANT

**検出**: PostgreSQL 関数で `SECURITY DEFINER` 使用時に `REVOKE ALL` + `GRANT EXECUTE` がない

```bash
# SECURITY DEFINER を使っている SQL ファイルを検出
for f in $(grep -rl 'SECURITY DEFINER' supabase/migrations/ --include='*.sql' 2>/dev/null); do
  # 同一ファイルで REVOKE ALL と GRANT EXECUTE があるか
  has_revoke=$(grep -c 'REVOKE ALL' "$f" 2>/dev/null || echo 0)
  has_grant=$(grep -c 'GRANT EXECUTE' "$f" 2>/dev/null || echo 0)
  if [ "$has_revoke" = "0" ] || [ "$has_grant" = "0" ]; then
    echo "WARNING: $f - SECURITY DEFINER without REVOKE/GRANT"
  fi
done
```

**SEVERITY**: WARNING (権限昇格リスク)

### Check 4: Cookie ハードコーディング

**検出**: Supabase Cookie 名を直接ハードコードしている（Cookie 名変更時に不整合）

```bash
# sb-*-auth-token のハードコードを検出
grep -rn 'sb-.*-auth-token\|supabase.*cookie' $TARGET --include='*.ts' --include='*.tsx' \
  | grep -v 'node_modules\|\.test\.\|__tests__'
```

**SEVERITY**: WARNING (Cookie 名変更時に壊れる)

### Check 5: dangerouslySetInnerHTML / console.*

**検出**: XSS 脆弱性と不適切なログ出力

```bash
# dangerouslySetInnerHTML
grep -rn 'dangerouslySetInnerHTML' $TARGET --include='*.ts' --include='*.tsx' \
  | grep -v 'node_modules\|\.test\.\|__tests__'

# console.* (logger を使うべき)
grep -rn 'console\.\(log\|warn\|error\|debug\|info\)' $TARGET --include='*.ts' --include='*.tsx' \
  | grep -v 'node_modules\|\.test\.\|__tests__\|eslint\|\.config\.\|scripts/'
```

**SEVERITY**:
- `dangerouslySetInnerHTML`: BLOCKER (XSS 脆弱性)
- `console.*`: INFO (ログ基盤統一)

---

## Output Format

```
============================================================
Security Audit Quick - Results
============================================================

[BLOCKER] Check 1: Test Mode Header Guard
  src/lib/security/api-security.ts:98 - X-E2E-Test without isProductionRuntime()
  Why: 本番環境でヘッダー偽装によりセキュリティチェックをバイパス可能
  Fix: !isProductionRuntime() && request.headers.get("X-E2E-Test") に変更

[WARNING] Check 2: PII in Logs
  src/app/api/auth/reset-password/route.ts:156 - email logged without maskEmail()
  Why: GDPR/CCPA 違反リスク。ログ基盤にメールアドレスが平文保存される
  Fix: logger.info("...", { email: maskEmail(user.email) })

[OK] Check 3: SECURITY DEFINER - No issues found
[OK] Check 4: Cookie Hardcoding - No issues found

[INFO] Check 5: console.* usage
  src/components/auth-provider.tsx:50 - console.debug found
  Why: logger モジュールを使うべき（ログレベル制御・構造化ログ）
  Fix: import logger from "@/lib/logger"; logger.debug(...)

============================================================
Summary: 1 BLOCKER, 1 WARNING, 0 INFO
============================================================
```

---

## Workflow

### Step 1: スコープ決定

```bash
# --diff オプションの場合
TARGET_FILES=$(git diff --name-only origin/main...HEAD | grep -E '\.(ts|tsx|sql)$')

# デフォルト（リポジトリ全体）
TARGET="src/ supabase/migrations/"
```

### Step 2: 5つのチェックを順番に実行

各チェックを上記の grep コマンドで実行。

### Step 3: 結果整形

Output Format に従って結果を整形出力。

### Step 4: サマリー

BLOCKER / WARNING / INFO のカウントを集計。

---

## AI Assistant Instructions

### MUST

1. **5つのチェックすべて**を実行する（スキップ禁止）
2. 結果は **Output Format に厳密に従う**（SEVERITY / file:line / why / fix）
3. `--diff` が指定された場合は変更ファイルのみを対象にする
4. テストファイル (`tests/**`, `e2e/**`, `__tests__/`) は除外する
5. 各チェックの結果が 0 件の場合は `[OK]` と出力する

### NEVER

- チェック結果を主観で省略しない（全件出力）
- 修正を自動実行しない（レポートのみ）
- `/security-hardening` の脅威モデリングを混ぜない（スコープ外）
