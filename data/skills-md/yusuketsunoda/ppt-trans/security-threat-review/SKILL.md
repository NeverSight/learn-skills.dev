---
name: security-threat-review
description: >-
  アプリ全体のセキュリティを攻撃者（レッドチーム）と防御者（ブルーチーム）の
  2視点で包括評価する。2エージェント並列実行 → review-aggregator で統合レポートを出力する。
  「アプリ全体のセキュリティ状態を知りたい」「攻撃者の視点で弱点を洗い出したい」
  「防御体制に抜けがないか確認したい」ときに使うこと。
  特定の脆弱性の対処にはsecurity-hardeningを、
  既知パターンの高速検出にはsecurity-audit-quickを使うこと。
argument-hint: "[--scope src/app/api|src/app/actions|all] [--layer 1-8]"
allowed-tools: Bash, Grep, Glob, Read, Task
user-invocable: true
context: fork
agent: general-purpose
---

# /security-threat-review - Red Team / Blue Team 包括セキュリティ評価

## Goal

攻撃者（Red Team）と防御者（Blue Team）の2視点でアプリ全体を評価し、
**攻撃シナリオと防御ギャップの対応表**を含む統合レポートを出力する。

> 他のセキュリティスキルとの違い:
> - `/security-audit-quick` = grepベースの既知パターン検出（機械的・高速）
> - `/security-hardening` = 単一脅威の深掘り（脅威モデル→緩和→テスト→ゲート）
> - `/review --focus security` = PR差分のセキュリティレビュー（差分限定）
> - **`/security-threat-review`** = アプリ全体の攻撃/防御2視点評価（包括的・定期的）

---

## Input

| 引数 | 説明 | デフォルト |
|------|------|-----------|
| `--scope` | 評価対象を限定 | `all`（アプリ全体） |
| `--layer` | Blue Team の評価レイヤーを限定（1-8） | 全レイヤー |

### --scope オプション

| 値 | 対象 |
|----|------|
| `all` | アプリ全体（デフォルト） |
| `api` | `src/app/api/` のみ |
| `actions` | `src/app/actions/` のみ |
| `auth` | 認証/認可関連のみ |
| `payment` | Stripe/課金関連のみ |
| `upload` | ファイルアップロード/処理関連のみ |

### 例

```bash
# アプリ全体の包括評価（デフォルト）
/security-threat-review

# API Routesのみ評価
/security-threat-review --scope api

# 認証関連のみ評価
/security-threat-review --scope auth

# 全体評価だが Blue Team は Layer 1-3（認証/認可/入力）のみ
/security-threat-review --layer 1-3
```

---

## Workflow

### Phase 0: 偵察（攻撃面の把握）

まず以下を実行し、アプリの攻撃面を把握する:

```bash
# 1. 全APIエンドポイント
echo "=== API Routes ==="
find src/app/api -name "route.ts" | sort

# 2. 全Server Actions
echo "=== Server Actions ==="
find src/app/actions -name "*.ts" | sort

# 3. セキュリティモジュール一覧
echo "=== Security Modules ==="
find src/lib/security -name "*.ts" | sort

# 4. RLSポリシー数
echo "=== RLS Policies ==="
grep -r "CREATE POLICY" supabase/migrations/ --include="*.sql" | wc -l

# 5. テストモード境界
echo "=== Test Mode ==="
cat src/lib/test-mode.ts | head -50
```

この情報を**両エージェントへのコンテキストとして渡す**。

### Phase 1: Red Team / Blue Team 並列実行

**2つのエージェントを並列で起動する**:

#### Red Team（攻撃者視点）

```text
Task(red-team-attacker):
  このPowerPoint翻訳SaaSを攻撃者の視点で評価してください。

  ## アプリ概要
  - Stack: Next.js 16 + React 19 + Supabase + Stripe + Claude API
  - 機能: PPTXアップロード → テキスト抽出 → Claude翻訳 → ダウンロード
  - 認証: Supabase Auth (Cookie-based)
  - 課金: Stripe Subscriptions

  ## 攻撃面
  [Phase 0の結果を貼る]

  ## スコープ
  [--scope オプションの値]

  出力は .claude/docs/reviewer-output-format.md に従ってください。
```

#### Blue Team（防御者視点）

```text
Task(blue-team-defender):
  このPowerPoint翻訳SaaSの防御態勢を評価してください。

  ## アプリ概要
  - Stack: Next.js 16 + React 19 + Supabase + Stripe + Claude API
  - 機能: PPTXアップロード → テキスト抽出 → Claude翻訳 → ダウンロード
  - 認証: Supabase Auth (Cookie-based)
  - 課金: Stripe Subscriptions

  ## 防御機構
  [Phase 0の結果を貼る]

  ## スコープ
  [--scope オプションの値]
  [--layer オプションの値]

  出力は .claude/docs/reviewer-output-format.md に従ってください。
  Defense Scorecard（Layer 1-8）を必ず含めてください。
```

### Phase 2: 結果統合

**review-aggregator エージェント**を使って両チームの出力を統合する。

ただし、通常のPRレビュー統合に加えて、以下を追加出力する:

#### 攻撃-防御 対応表（このスキル固有の出力）

両チームの結果を突き合わせ、攻撃シナリオと防御状況の対応表を生成する:

```markdown
### Attack-Defense Matrix

| # | 攻撃シナリオ (Red) | 防御状況 (Blue) | Gap | Priority |
|---|-------------------|----------------|-----|----------|
| 1 | IDOR: 他人のfileIdでダウンロード | RLS + user_idチェック済み | None | - |
| 2 | Rate Limit バイパス: ヘッダー偽装 | isProductionRuntime()でガード済み | None | - |
| 3 | テストモード偽装: X-E2E-Test | fail-closed だが一部チェック漏れ | Partial | High |
| 4 | Webhook偽造: 署名なしリクエスト | 署名検証あり | None | - |
| 5 | 翻訳回数制限バイパス | カウンター実装あり、ただしrace condition | Yes | Critical |
```

**Gap の判定基準**:

| Gap | 意味 |
|-----|------|
| **None** | Red Teamの攻撃がBlue Teamの防御で完全に阻止される |
| **Partial** | 防御は存在するが不完全。条件次第で突破可能 |
| **Yes** | 防御が欠如し、攻撃が成立する |

**Priority の判定基準**:

| Priority | 条件 |
|----------|------|
| **Critical** | Gap=Yes かつ 影響がデータ漏えい/権限昇格/課金詐欺 |
| **High** | Gap=Partial かつ 影響が深刻 |
| **Medium** | Gap=Partial かつ 影響が限定的 |
| **Low** | 理論的なリスクのみ |
| **-** | Gap=None（防御済み） |

### Phase 3: 最終レポート出力

```markdown
## Security Threat Review Report

### Executive Summary
[3-5行: 全体評価、最も重要なGap、推奨アクション]

### Defense Scorecard (Blue Team)
[Layer 1-8 のスコアカード表]

### Attack-Defense Matrix
[Phase 2 の対応表]

### Blockers (Critical/High Gaps)
- [confidence=XX] <タイトル> (file:line) — <概要> — <推奨策>
  - Red Team: [攻撃シナリオ要約]
  - Blue Team: [防御ギャップ要約]

### Important (Medium Gaps)
- [confidence=XX] <タイトル> (file:line) — <概要> — <推奨策>

### Suggestions (Hardening Opportunities)
- [confidence=XX] <タイトル> (file:line) — <改善案>

### Strengths (Well-Defended Areas)
- [防御が適切に機能している領域]

### Recommended Next Steps
1. [最優先で対応すべき項目]
2. [次に対応すべき項目]
3. [中期的に対応すべき項目]

---
Reviewed by: Red Team (攻撃者視点) + Blue Team (防御者視点)
Aggregated by: review-aggregator
```

---

## AI Assistant Instructions

### MUST

1. **Phase 0 を必ず最初に実行**（攻撃面の把握なしにエージェントを起動しない）
2. **Red Team と Blue Team を並列で Task 起動する**（直列にしない）
3. **Attack-Defense Matrix を必ず出力する**（このスキルの核心）
4. **Defense Scorecard を必ず含める**（Blue Teamの出力から抽出）
5. **Gap=Yes の項目は Blocker として扱う**
6. **Recommended Next Steps を優先度順で出力する**

### NEVER

- 片方のチームだけ実行しない（Red/Blue 両方必須）
- Attack-Defense Matrix を省略しない
- 修正を自動実行しない（レポートのみ）
- 他のセキュリティスキル（`/security-audit-quick` 等）を内部で呼ばない（スコープが異なる）
- テストファイルへの修正指示を出さない（検出・報告は行う）
