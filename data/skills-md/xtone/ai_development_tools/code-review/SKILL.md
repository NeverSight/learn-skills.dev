---
name: code-review
description: PRやコード変更の汎用コードレビューを実施します。コードの品質、セキュリティ、設計を共通基準で評価し、approve/rejectを判断します。「このPRをレビュー」「コードレビューして」「マージ前チェック」などの依頼や、gh pr viewコマンドの実行時に使用してください。
---

# コードレビュー

PRやコード変更を体系的にレビューするための汎用スキルです。
言語非依存の共通レビュー基準と、言語/フレームワーク固有のベストプラクティスを組み合わせて使用します。

## ディレクトリ構成

```
code-review/
├── SKILL.md (このファイル)
└── references/
    ├── typescript-best-practices.md       # TypeScript固有のチェック
    ├── authorization-review-general.md    # 認可レビュー観点（一般編）
    ├── authorization-review-postgres-rls.md  # 認可レビュー観点（PostgreSQL RLS編）
    └── github-pr-review-actions.md        # GitHub PRレビューアクション
```

## 外部スキル連携

React / Next.js のベストプラクティスは、Vercel提供の **vercel-react-best-practices** スキルを使用する。

- **リポジトリ**: https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices
- **インストール**: `npx -y skills add vercel-labs/agent-skills --skill vercel-react-best-practices --agent claude-code --yes`
- **カバー範囲**: 非同期ウォーターフォール排除、バンドルサイズ最適化、サーバー側パフォーマンス、クライアント側データ取得、再レンダリング最適化、レンダリングパフォーマンス、高度なパターン、JavaScriptパフォーマンス（8カテゴリ、40以上のルール）

## レビューワークフロー

以下のチェックリストをコピーして進行状況を追跡します：

```
レビュー進捗：
- [ ] ステップ1: 変更概要の把握
- [ ] ステップ2: 共通品質チェック
- [ ] ステップ3: 言語/フレームワーク固有チェック
- [ ] ステップ4: approve/reject判定
- [ ] ステップ5: レビュー結果の出力
```

### ステップ1: 変更概要の把握

変更内容を理解する。

1. **変更ファイル一覧を確認** - 変更の範囲とスコープを把握
2. **コード差分を確認** - 追加・変更・削除された内容を把握
3. **変更の意図を理解** - PR説明やコミットメッセージから目的を確認

確認すべきポイント：
- 変更は単一の目的にフォーカスしているか
- スコープが適切か（1つのPRで多すぎる変更をしていないか）
- 関連する変更が漏れなく含まれているか

### ステップ2: 共通品質チェック

言語に依存しない汎用的なチェックを実施する。

#### 2-1. セキュリティ

| チェック項目 | 重要度 |
|-------------|--------|
| ハードコードされた秘密情報（APIキー、パスワード、トークン）がないか | Critical |
| ユーザー入力の適切なバリデーション・サニタイズがあるか | Critical |
| SQLインジェクション、XSS、コマンドインジェクションの脆弱性がないか | Critical |
| 認証・認可のチェックが適切に実装されているか | Critical |
| 機密データが不用意にログ出力されていないか | Major |
| CORS設定が適切か | Major |

> **認可（Authorization）の詳細レビュー**：認可に関わる変更がある場合は、[references/authorization-review-general.md](references/authorization-review-general.md) を参照して詳細なチェックを行う。PostgreSQL RLSを使用している場合は、追加で [references/authorization-review-postgres-rls.md](references/authorization-review-postgres-rls.md) も参照する。

#### 2-2. ロジック・正確性

| チェック項目 | 重要度 |
|-------------|--------|
| エッジケースが適切に処理されているか（null、空配列、境界値） | Major |
| エラーハンドリングが適切か（例外の握りつぶし、不適切なcatch） | Major |
| 条件分岐のロジックが正しいか（off-by-one、論理演算子の誤り） | Major |
| 非同期処理の競合状態（race condition）がないか | Major |
| リソースの確実な解放（ファイル、接続、ロック） | Major |

#### 2-3. 設計・保守性

| チェック項目 | 重要度 |
|-------------|--------|
| 関数/メソッドの責務が単一か | Minor |
| DRY原則: 不要な重複コードがないか | Minor |
| 命名が意図を正確に表しているか | Minor |
| マジックナンバーや意味不明な文字列リテラルがないか | Minor |
| 適切な抽象度で設計されているか（過剰な抽象化・不足） | Minor |
| 循環参照・不適切な依存関係がないか | Major |

#### 2-4. パフォーマンス

| チェック項目 | 重要度 |
|-------------|--------|
| N+1クエリなど非効率なデータアクセスパターンがないか | Major |
| 不要なループやネスト、計算量の大きい処理がないか | Minor |
| メモリリークの可能性がないか | Major |
| 大量データの適切なページネーション・ストリーミング処理 | Minor |

#### 2-5. テスト

| チェック項目 | 重要度 |
|-------------|--------|
| 変更に対応するテストが追加/更新されているか | Major |
| エッジケースのテストが含まれているか | Minor |
| テストが実装詳細でなく振る舞いをテストしているか | Minor |
| テスト名がテスト対象の振る舞いを明確に表しているか | Suggestion |

### ステップ3: 言語/フレームワーク固有チェック

変更ファイルの言語/フレームワークに応じて、対応するリファレンスファイルを参照する。

**参照可能なリファレンス：**

| 言語/FW | 参照先 | 種別 |
|---------|--------|------|
| TypeScript | [references/typescript-best-practices.md](references/typescript-best-practices.md) | 内部リファレンス |
| React / Next.js | `vercel-react-best-practices` スキル（Vercel提供） | 外部スキル |

| 観点 | 参照先 | 種別 |
|------|--------|------|
| 認可（一般） | [references/authorization-review-general.md](references/authorization-review-general.md) | 内部リファレンス |
| 認可（PostgreSQL RLS） | [references/authorization-review-postgres-rls.md](references/authorization-review-postgres-rls.md) | 内部リファレンス |
| GitHub PRレビュー | [references/github-pr-review-actions.md](references/github-pr-review-actions.md) | 内部リファレンス |

**参照ルール：**
- TypeScriptの変更 → 内部リファレンスを読み込む
- React / Next.js の変更 → `vercel-react-best-practices` スキルを併用する（インストール済みの場合）
- 認可に関わる変更（認証/権限チェック、データアクセス制御等） → 認可リファレンス（一般編）を参照
- PostgreSQL RLSを使用している場合 → 認可リファレンス（RLS編）も追加で参照
- GitHub Actions等のCI環境でPRレビューを実行する場合 → GitHub PRレビューアクションを参照（コメント投稿・評価方法）
- 複数の言語/FWにまたがる変更の場合は、すべての該当リファレンスを参照する
- リファレンスが存在しない言語の場合は、ステップ2の共通チェックのみで判断する

### ステップ4: approve/reject判定

すべてのチェック結果に基づき、以下の基準でapprove/rejectを判定する。

#### 問題の重要度と減点

| 重要度 | 説明 | 減点 |
|--------|------|------|
| **Critical** | マージ前に必ず修正が必要。セキュリティ脆弱性、データ損失リスク、重大なバグ | -3点/件 |
| **Major** | 優先的に修正すべき。ロジックの問題、パフォーマンス劣化、テスト不足 | -2点/件 |
| **Minor** | 改善が望ましい。設計改善、可読性向上、軽微な問題 | -1点/件 |
| **Suggestion** | 提案。ベストプラクティスの推奨、より良いアプローチの提示 | -0.5点/件 |

#### 判定基準

満点は10点とし、以下の基準で判定する。

| 判定 | 条件 | アクション |
|------|------|-----------|
| **Reject** | Critical問題が1件以上ある | REQUEST_CHANGES |
| **Reject** | Major問題が3件以上ある | REQUEST_CHANGES |
| **Reject** | スコアが5点未満 | REQUEST_CHANGES |
| **Conditional Approve** | Critical問題なし、Major 1-2件、スコア5点以上 | APPROVE（改善点をコメント） |
| **Approve** | Critical/Major問題なし、スコア8点以上 | APPROVE |

#### 判定フローチャート

```
Critical問題あり？ → Yes → Reject（REQUEST_CHANGES）
       ↓ No
Major問題が3件以上？ → Yes → Reject（REQUEST_CHANGES）
       ↓ No
スコア5点未満？ → Yes → Reject（REQUEST_CHANGES）
       ↓ No
Major問題が1-2件？ → Yes → Conditional Approve
       ↓ No
スコア8点以上？ → Yes → Approve
       ↓ No
Conditional Approve
```

### ステップ5: レビュー結果の出力

以下のフォーマットでレビュー結果を出力する。

> **GitHub上でのレビュー投稿**：GitHub Actions等のCI環境でPRレビューを実行している場合のみ、[references/github-pr-review-actions.md](references/github-pr-review-actions.md) を参照して、`gh`コマンドやインラインコメントを使用してレビュー結果をGitHub上に投稿する。ローカル環境での実行時は、結果を標準出力に表示するのみとする。

```markdown
## Code Review: [判定結果]

### 変更概要
- **スコープ**: [変更の概要を1-2文で]
- **変更ファイル数**: [N]ファイル
- **主な言語/FW**: [検出された言語/FW]

### スコア: X/10

### 検出された問題

| # | 重要度 | ファイル | 問題 | 推奨される対応 |
|---|--------|---------|------|---------------|
| 1 | [Critical/Major/Minor/Suggestion] | [ファイルパス:行番号] | [問題の説明] | [対応方法] |

### 良い点
- [コードの良い点を具体的に記載]

### 判定
- **結果**: [Approve / Conditional Approve / Reject]
- **理由**: [判定理由の要約]

### 次のステップ
- [修正が必要な場合の具体的なアクション]
```

## 重要な注意事項

- レビューはコードの品質向上が目的であり、批判ではない。建設的なフィードバックを心がける
- 問題の指摘には必ず**具体的な改善案**を添える
- 変更の**意図を尊重**し、スタイルの好みではなく客観的な基準で判断する
- 自動検出が困難なドメイン知識やビジネスロジックの判断は、人間のレビュアーに委ねる
- Suggestionは強制ではなく、採用するかどうかは著者の判断に任せる
