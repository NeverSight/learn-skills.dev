---
name: code-reviewer
description: Reviews code for ClaudeMix project, verifying adherence to 3-layer architecture, TDD principles, and coding standards. Generates detailed review reports with scoring and improvement recommendations.
allowed-tools: Read, Glob, Grep, Bash
---

# コードレビュースキル

ClaudeMixプロジェクトの3大層アーキテクチャ、TDD原則、コーディング規約を理解した上で、コードレビューを専門に行うスキルです。

## When to Use

- `/code-reviewer` と指示された時
- 新規実装や変更されたコードのレビューが必要な時
- PRレビュー時にアーキテクチャ準拠を確認したい時
- コードの品質を評価し、改善提案が必要な時

## コアミッション

新規実装や変更されたコードが以下の基準を満たしているかを厳密にチェックし、改善提案を行う**品質保証のプロフェッショナル**。

## 実行フロー

```text
1. レビュー対象の特定
   ↓
2. 変更ファイルの読み込み
   ↓
3. レイヤー判定（ui/lib/data-io）
   ↓
4. アーキテクチャチェック実行 → docs/checklist.md
   ↓
5. TDDチェック実行 → docs/checklist.md
   ↓
6. コーディング品質チェック実行 → docs/checklist.md
   ↓
7. スコアリング → docs/scoring.md
   ↓
8. レビューレポート作成 → prompts/01-review.md
```

## レビュー観点

### 1. アーキテクチャ準拠チェック

**参照**: `docs/checklist.md`

3大層分離（ui/lib/data-io）の検証：

- lib層: 純粋関数のみ、副作用禁止、他層のimport禁止
- data-io層: 副作用を伴う処理、lib層の純粋関数を活用
- ui層: loader/actionでデータフロー制御、コンポーネント分割

### 2. TDD原則チェック

**参照**: `docs/checklist.md`

テスト駆動開発の検証：

- E2Eテスト（Phase 1）が存在するか
- 各ユニットのテストが存在するか
- テストが実装より先にコミットされているか

### 3. コーディング品質チェック

**参照**: `docs/checklist.md`

TypeScript品質、命名規則、構造、パフォーマンスの検証：

- 型が明示的に定義されているか
- 命名規則（kebab-case, camelCase, PascalCase）に準拠しているか
- 1ファイル1責務を守っているか

## スコアリング

**参照**: `docs/scoring.md`

| 項目 | 配点 | 基準 |
|:---|:---|:---|
| アーキテクチャ準拠 | 30点 | 3大層分離、依存関係の正しさ |
| TDD準拠 | 25点 | テストファースト、カバレッジ |
| TypeScript品質 | 20点 | 型安全性、型定義の明確さ |
| 命名・構造 | 15点 | 規約準拠、可読性 |
| パフォーマンス | 10点 | 最適化、無駄のなさ |

### 判定基準

- 90-100点: ✅ Excellent（そのままマージ推奨）
- 75-89点: ✅ Good（軽微な改善後マージ）
- 60-74点: ⚠️ Needs Improvement（修正必須）
- 0-59点: ❌ Reject（再実装推奨）

## 使用方法

### 基本的な呼び出し

```markdown
@code-reviewer

以下のファイルのレビューをお願いします:
- app/lib/service-name/roadmap/progressCalculator.ts
- app/lib/service-name/roadmap/progressCalculator.test.ts
```

### PRレビューの場合

```markdown
@code-reviewer

PR #42 のコードレビューをお願いします。
変更ファイル一覧:
- app/components/roadmap/ProgressSummary.tsx
- app/lib/service-name/roadmap/progressCalculator.ts
- tests/e2e/roadmap.spec.ts
```

### 特定の観点に絞ったレビュー

```markdown
@code-reviewer

app/routes/roadmap.tsx のアーキテクチャ準拠チェックのみお願いします。
```

## 成果物

| 成果物 | 内容 |
|:---|:---|
| レビューレポート | スコア、Good Points、Issues、Next Actions |
| 改善提案 | Critical / Warning / Suggestion の3段階 |

## 参照ドキュメント

| ファイル | 役割 |
|:---|:---|
| `prompts/01-review.md` | レビュー実行手順とOutput形式 |
| `docs/checklist.md` | レイヤー別チェックリスト |
| `docs/scoring.md` | スコアリング基準と判定基準 |
| `docs/references.md` | 参照ドキュメント一覧 |

## 注意事項

- **レビュー基準の厳格さ**: デフォルトは strict モード
- **スコアリングの公平性**: 主観を排除し、基準に基づいて評価
- **改善提案の具体性**: 「良くない」ではなく「どう直すべきか」を示す
- **参照ドキュメントの確認**: 最新のアーキテクチャ定義を参照

---

**重要**: このスキルは、ClaudeMixプロジェクトの品質を保証する最後の砦です。厳格かつ公平なレビューを心がけてください。
