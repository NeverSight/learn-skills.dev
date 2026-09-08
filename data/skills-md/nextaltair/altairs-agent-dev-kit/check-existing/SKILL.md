---
name: check-existing
description: "Before implementing a feature, hear out the requirement, then research existing libraries / tools / local packages (monorepo components) that already solve it. Use when scoping a new feature, evaluating build-vs-reuse, or asked to find existing solutions before writing code."
metadata:
  short-description: 実装前の要件ヒアリング＋既存ライブラリ/ツール/ローカルパッケージ調査（build-vs-reuse 判断）。
---

# Check Existing Solutions

実装予定の機能に対して、まず要件を明確化し、その上で既存のライブラリ・ツール・
プロジェクトのローカルパッケージ/モノレポ構成があればそこですでに解決できないかを徹底調査する。
**車輪の再発明を避け、独自実装の範囲を最小化する**ことが目的。

## When to Use

- 新機能の着手前（Plan Mode に入る前段の調査として）
- 「自前で書くか既存を使うか」の判断が必要なとき
- 曖昧な要望（例: 「画像処理の何か」）から的確な既存解を見つけたいとき

要件が完全に固まっていなくても起動してよい。ヒアリングで具体化する。

## Workflow

### Phase 1: 過去知識の確認

着手前に既存の判断・教訓を確認して二度手間を避ける:

- `docs/decisions/` の ADR インデックス（`docs/decisions/README.md`）
- `docs/lessons-learned.md` の関連ドメイン

### Phase 2: 要件明確化ヒアリング（1問ずつ）

仮定を避け、具体的に問う。多肢選択を優先。

- **意図**: この機能で解決したい具体的な問題は? 現状の不満は?
- **技術詳細**: 処理対象のデータ量は? バッチ/リアルタイム? プロジェクトのどのワークフローに組み込む? 操作は GUI/自動/設定?
- **制約と優先度**: Must-have / Nice-to-have は? パフォーマンス要件(速度・メモリ・精度)は? シンプルさ優先か?
- **検索語**: 英語で言うと? 業界用語は? 知っている類似ツールは? PyPI/GitHub で何で検索する?

### Phase 3: 要件定義の整理

```markdown
## 明確化された要件
### 核心機能
- メイン処理 / 入力形式 / 出力形式
### 技術的要件
- 統合箇所(プロジェクト内のどこ) / パフォーマンス / 既存依存との関係
### 機能的要件
- Must-have / Nice-to-have / 制約・除外
### 検索キーワード候補
- メイン / 技術 / ドメイン
```

### Phase 4: 既存解の調査

**プロジェクト内を先に、次に外部 OSS を段階検索する。**

1. **プロジェクト内の代替を確認**（最優先）
   - `investigation` agent で既存実装・類似機能を調査
   - プロジェクトのローカルパッケージ/モノレポ構成があれば、そこで代替可能性を確認
   - `Bash uv tree` / `Grep` で既存依存・統合箇所を確認
2. **外部 OSS を段階検索**
   - 第1段: PyPI / GitHub Topics / 標準ライブラリ（`WebSearch`）
   - 第2段: 実装例・比較記事・Stack Overflow（`WebSearch` / `WebFetch`）
   - 第3段: 最新動向・トレンド（`WebSearch`、現在年を明示）
   - ライブラリの一次ドキュメントは Context7 MCP (利用可能なら) または公式ドキュメントの `WebFetch` で取得
3. **候補の評価**
   - `solutions` agent で複数候補を生成・比較（適合度・実装コスト・リスク）

### Phase 5: 評価・記録・推奨

```markdown
# 既存解調査結果

## 要件（Phase 3 の整理）

## 調査プロセス
- 検索キーワード / 調査ソース / 発見候補数

## 発見された既存解
### 🎯 完全代替可能（適合度 90%+）
- ライブラリ名 / 統合方法 / 推奨度
### 🔧 組み合わせ利用（60-89%）
- 主ライブラリ / 補完方法 / 実装工数
### 📚 参考実装（30-59%）
- 参考価値 / 独自実装が要る範囲

## 最終推奨
### ✅ 採用推奨
- 選択理由 / 統合手順 / 注意点
### ⚠️ 独自実装が必要な場合
- 既存解の限界 / 最小実装範囲 / 部分的に使える既存機能
```

調査結論のうち再利用価値のあるもの（ライブラリ評価、build-vs-reuse の判断根拠）は
ADR (`docs/decisions/`) などプロジェクトの記録先へ残すことを推奨に含める。

## Next Step

要件が固まり既存解が出そろったら、ネイティブ Plan Mode（`/plan`）または
superpowers `brainstorming` → `writing-plans` へ引き継ぐ。本 skill は調査までを担い、設計・実装はしない。
