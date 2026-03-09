---
name: security-hardening
description: >-
  特定の脅威シナリオに対するセキュリティ強化ワークフロー。「IDORを防ぎたい」
  「CSRFの対策を設計したい」「RLSを強化したい」のように、単一の具体的な脅威を入力に、
  脅威モデル→緩和設計→実装方針→テスト/ログ→release-gate化まで一貫して成果物を出力する。
  IDOR、リプレイ攻撃、CSRF、XSS、パストラバーサル、オープンリダイレクト、
  レート制限設計など、特定の脆弱性への対処で使うこと。
  「コードベース全体をスキャンしたい」場合はsecurity-audit-quickを、
  「アプリ全体を包括評価したい」場合はsecurity-threat-reviewを使うこと。
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
user-invocable: true
context: fork
---

# /security-hardening - Threat -> Mitigation -> Tests -> Gate

## Goal

単一の脅威シナリオを入力として受け取り、
**(1) 脅威モデル化 → (2) 緩和設計 → (3) 実装方針 → (4) テスト/ログ → (5) release-gate化**
までを一貫して出す。百科事典は作らない。

---

## Input (required)

| フィールド | 説明 | 例 |
|-----------|------|-----|
| `target` | 対象(endpoint/function/module) | `src/app/api/files/[id]/download/route.ts` |
| `threat` | 再現可能な脅威シナリオ(1文) | "他ユーザーのfileIdを指定するとファイルがダウンロードできる" |
| `environment` | ランタイム | `Next.js 16 + Supabase` |
| `constraints` | 互換性/性能/運用制約(あれば) | "admin-dashboardからも呼ぶ" |

**入力は「1つの脅威」に絞る。"IDOR全般" のような曖昧な入力は禁止。**

---

## Output (must deliver all 5)

出せないならスキル失敗。

| # | 成果物 | 内容 |
|---|--------|------|
| 1 | **Threat Model** | 攻撃者/影響/悪用難易度/既存防御層 |
| 2 | **Mitigation Design** | fail-closed/最小権限/境界チェックの方針 |
| 3 | **Implementation Plan** | diff-oriented: どのファイルのどこをどう変えるか |
| 4 | **Tests + Logging** | 再現テスト(修正前fail, 修正後pass) + SecurityMonitorログ |
| 5 | **Release Gate** | 再発防止ゲートの提案(自動検出可能なもの) |

---

## Workflow

### Step 0: Evidence (再現確認)

攻撃が実際に成立するか、コードを読んで確認する。

```bash
# 1. 対象ファイルを読む
Read <target>

# 2. 認証/認可チェックの有無を確認
Grep "performSecurityChecks\|getRequestScopedAuth\|auth\.uid()" <target>

# 3. RLS policyの確認(DB関連の場合)
Grep "CREATE POLICY\|ALTER POLICY" supabase/migrations/ --glob "*.sql"
```

**出力**: 攻撃が成立する根拠(コード引用付き) + 期待する失敗条件(403/401/400)

### Step 1: Threat Model

以下のテンプレートを埋める:

```markdown
### Threat Model
- **攻撃者**: anonymous / authenticated / insider
- **影響**: data exfiltration / privilege escalation / DoS / billing fraud
- **悪用難易度**: low(ツール不要) / medium(カスタムリクエスト) / high(特殊条件)
- **既存の防御層**: [RLS / JWT / performSecurityChecks / rate-limit / CSP]
- **欠落している防御**: [具体的に何が足りないか]
```

### Step 2: Mitigation Design

原則(この順に適用):

1. **Fail-closed**: エラー時はアクセス拒否(fail-open禁止)
2. **Least privilege**: identityはトークンから導出、入力から取らない
3. **Input validation**: schema + bounds + deny-list
4. **Defense in depth**: RLS + アプリ層の二重チェック
5. **Observability**: SecurityMonitor.logEvent(PIIなし)

### Step 3: Implementation Plan (パターン参照)

対象の脅威に最も近いパターンを選び、diff方針を書く。

#### Pattern A: IDOR (認可バイパス)
```typescript
// ❌ BEFORE: userIdを入力から取得
const { userId } = await request.json();
const { data } = await supabase.from("files").select().eq("user_id", userId);

// ✅ AFTER: auth.uid()に固定 + RLS二重防御
const auth = await getRequestScopedAuth(request);
if (!auth.userId) return createErrorResponse("認証が必要です", 401);
const { data } = await supabase.from("files").select().eq("user_id", auth.userId);
```
**RLS側**: `USING (user_id = auth.uid())`

#### Pattern B: Token Replay (JTIリプレイ)
```typescript
// jti-tracker.ts のパターン
const result = await isJtiUsed(jti);
if (result.used && !result.withinGrace) {
  await invalidateUserSessions(userId); // 全セッション無効化
  return; // fail-closed
}
await markJtiAsUsed(jti, userId, expiresAt);
```
**grace window**: 並行リクエスト許容(60秒デフォルト)

#### Pattern C: Input Injection (パス/URL/SQL)
```typescript
// Path traversal防御
const allowedDir = path.resolve(process.cwd(), "uploads");
const resolvedPath = path.resolve(allowedDir, filePath);
if (!resolvedPath.startsWith(allowedDir + path.sep)) {
  // reject
}

// Open redirect防御
import { sanitizeNextPath } from "@/lib/security/url-sanitizer";
const safePath = sanitizeNextPath(next, appUrl);
// null byte, backslash, //, 外部origin → 全てDEFAULT_PATHにフォールバック
```

#### Pattern D: Rate Limiting (新規エンドポイント)
```typescript
// performSecurityChecks に rateLimit を渡す
const securityResult = await performSecurityChecks(request, {
  rateLimit: { windowMs: 3600_000, max: 50, keyPrefix: "translate" },
  csrf: true,
  origin: true,
});
if (!securityResult.success) {
  return createErrorResponse(securityResult.error!, securityResult.status!, ...);
}
```
**E2E対応**: `DISABLE_RATE_LIMIT_IN_E2E=true` + `X-Bypass-Rate-Limit` ヘッダー

#### Pattern E: Webhook Verification
```typescript
// Stripe webhook: 署名検証は fail-closed
const sig = request.headers.get("stripe-signature");
if (!sig) return createErrorResponse("Missing signature", 400);
const event = stripe.webhooks.constructEvent(body, sig, webhookSecret);
// 失敗 → 400, 成功 → 処理続行
```

### Step 4: Tests + Logging

**テスト構造**: 修正前に攻撃が成功することを確認 → 修正後に失敗することを確認

```typescript
// テストテンプレート
describe("Security: [脅威名]", () => {
  // 正常系: 正当なリクエストは通る
  it("allows legitimate request", async () => {
    const response = await handler(validRequest);
    expect(response.status).toBe(200);
  });

  // 攻撃系: 脅威シナリオが拒否される
  it("rejects [threat scenario]", async () => {
    const response = await handler(maliciousRequest);
    expect(response.status).toBe(403); // or 401, 400, 429
  });

  // ログ系: SecurityMonitorにイベントが記録される
  it("logs security event", async () => {
    await handler(maliciousRequest);
    expect(mockLogEvent).toHaveBeenCalledWith(
      expect.objectContaining({
        type: expect.any(String),
        severity: expect.stringMatching(/high|critical/),
      })
    );
  });
});
```

**Logging必須チェック**:
- `SecurityMonitor.logEvent()` が脅威パスで呼ばれるか
- ログにPII(email, token等)が含まれないか
- `requestId` がログに含まれるか(追跡用)

### Step 5: Release Gate (mandatory)

修正だけでは再発する。**自動検出可能なゲートを1つ提案**する。

| ゲート種別 | 検出方法 | 例 |
|-----------|----------|-----|
| API Route呼び出し漏れ | `grep -rL "performSecurityChecks" src/app/api/` | 全API Routeで統合セキュリティチェック必須 |
| RLS policy不在 | SQLマイグレーションでCREATE TABLEがあるのにCREATE POLICYがない | 新テーブルにはRLS必須 |
| SecurityMonitor未導入 | 脅威ハンドリングコードでlogEventがない | 脅威パスにはログ必須 |
| 認証チェック漏れ | `getRequestScopedAuth` を呼ばずにuserIdを使用 | Server Actionsで認証必須 |

```bash
# ゲート検証コマンド例
# 1. performSecurityChecks 呼び出し漏れ
grep -rL "performSecurityChecks" src/app/api/*/route.ts \
  | grep -v "webhook\|health\|__test"

# 2. RLSなしテーブル検出
grep -l "CREATE TABLE" supabase/migrations/*.sql | while read f; do
  table=$(grep -oP 'CREATE TABLE (?:IF NOT EXISTS )?\K\w+' "$f")
  if ! grep -q "CREATE POLICY.*ON $table" "$f"; then
    echo "MISSING RLS: $table in $f"
  fi
done
```

---

## Allowlist (例外管理)

例外は必ずここに明記する。暗黙の例外は禁止。

| 対象 | 例外内容 | 理由 |
|------|---------|------|
| `/api/stripe/webhook` | CSRF検証スキップ | 外部Webhookは自前署名検証 |
| `/api/health` | 認証スキップ | ヘルスチェック(機密情報なし) |
| `/api/test/*` | E2E環境でのみアクセス可 | `validateE2eAccess()` で保護 |
| JTI tracker | fail-open (DBエラー時) | 可用性優先(ログは記録) |

**例外を追加する場合**: このテーブルに行を追加し、PRで明示的にレビューを受ける。

---

## Non-Goals

- 複数脅威を1回で処理しない(1脅威1実行)
- パターン辞典を増やすだけの作業はしない(必ずテスト+ゲートを伴う)
- 既存の安全なコードを「念のため」で修正しない

---

## AI Assistant Instructions

このスキルが有効化された時:

### MUST
1. **Step 0 (Evidence)** を必ず最初に実行。再現できない脅威は扱わない
2. **5つの成果物すべて**を出力する。1つでも欠けたらスキル失敗
3. テストは「修正前fail → 修正後pass」の構造にする
4. Release gateは**grepやASTで自動検出可能**なものに限定する
5. Allowlistに載っていない例外を作る場合は、ユーザーに確認する

### NEVER
- 「セキュリティ全般を強化」のような曖昧なゴールで動かない
- SecurityMonitor.logEventにPII(email, token, password)を渡さない
- fail-openを暗黙に導入しない(やむを得ない場合はAllowlistに明記)
- テストなしで緩和策を実装しない
