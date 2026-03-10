---
name: creating-rules
description: Creates Claude Code rules (.claude/rules/*.md) with YAML frontmatter and path-specific scoping. Use when creating project rules, coding standards, or conditional guidelines for specific file types.
---

# Creating Claude Code Rules

`.claude/rules/` ディレクトリにモジュール化された、焦点を絞ったルールを作成する。

## Quick Start

**まずユーザーに確認する**:
1. **スコープ**: グローバル（全ファイル）or パス指定（特定ファイルタイプ）？
2. **配置場所**: `.claude/rules/`（プロジェクト用）or `~/.claude/rules/`（個人用）？
3. **カテゴリ**: コードスタイル、テスト、セキュリティ、API、その他？
4. **対象言語/フレームワーク**（該当する場合）？

**次に既存ルールを確認する**:
```bash
# プロジェクトのルールを確認
ls -la .claude/rules/

# 個人のルールを確認
ls -la ~/.claude/rules/
```

重複がないことを確認してからルールを作成する。

**ルールファイルを作成**:

```markdown
---
paths: src/**/*.ts
---

# TypeScript Guidelines

- strict モードを使用する
- オブジェクト形状には type より interface を優先
- エクスポートされる関数には明示的な戻り値型を指定
```

## 作成前チェック

ルールを作成する前に必ず確認：

1. **既存ルールの確認**
   ```bash
   ls .claude/rules/
   ```
   - 同じトピックのルールが存在しないか？
   - 既存ルールに追記すべき内容ではないか？

2. **CLAUDE.md との重複確認**
   - CLAUDE.md に同様の内容がないか？
   - プロジェクト概要 → CLAUDE.md
   - 具体的なコーディング規約 → rules/

3. **スコープの適切性**
   - グローバルルールにすべきか、パス指定すべきか？
   - 既存のパス指定ルールと競合しないか？

## ルールファイル構造

### グローバルルール（Frontmatter なし）

全ファイルに適用：

```markdown
# Code Style

- 2スペースインデントを使用
- let より const を優先
- 未使用変数を残さない
```

### パス指定ルール（Frontmatter あり）

Claude が一致するファイルを扱う時のみ適用：

```markdown
---
paths: src/api/**/*.ts
---

# API Development Rules

- 全エンドポイントに入力バリデーションを含める
- 標準エラーレスポンス形式を使用
- OpenAPI ドキュメントコメントを含める
```

## YAML Frontmatter

### `paths` フィールド

単一パターン：
```yaml
paths: src/**/*.ts
```

ブレース展開による複数パターン：
```yaml
paths: src/**/*.{ts,tsx}
```

カンマ区切りパターン：
```yaml
paths: {src,lib}/**/*.ts, tests/**/*.test.ts
```

### Glob パターンリファレンス

| パターン | マッチ対象 |
|---------|---------|
| `**/*.ts` | 任意の場所の全 TypeScript ファイル |
| `src/**/*` | `src/` 配下の全ファイル |
| `*.md` | プロジェクトルート直下の Markdown ファイルのみ |
| `src/components/*.tsx` | 特定ディレクトリ内の React コンポーネント |
| `**/*.{ts,tsx}` | TypeScript と TSX ファイル |
| `{src,lib}/**/*.ts` | `src/` または `lib/` 内の TypeScript |

## ディレクトリ構成

### 基本構成

```
.claude/rules/
├── code-style.md      # 一般的なコーディング規約
├── testing.md         # テスト規約
└── security.md        # セキュリティ要件
```

### サブディレクトリあり

```
.claude/rules/
├── frontend/
│   ├── react.md
│   └── styles.md
├── backend/
│   ├── api.md
│   └── database.md
└── general.md
```

全 `.md` ファイルは再帰的に検出される。

### シンボリックリンクによる共有ルール

```bash
# 共有ルールディレクトリをシンボリックリンク
ln -s ~/shared-claude-rules .claude/rules/shared

# 個別ファイルをシンボリックリンク
ln -s ~/company-standards/security.md .claude/rules/security.md
```

## ベストプラクティス

### MUST（必須）

- **1トピック1ファイル**で焦点を絞る
- **説明的なファイル名**を使用（`api-validation.md`、`rules1.md` ではない）
- **具体的に**記述する（「適切にフォーマット」ではなく「2スペースインデント」）
- **既存ルールを確認**してから新規作成

### ALLOWED（許可）

- サブディレクトリによる整理
- シンボリックリンクによる共有ルールの参照
- 複数の paths パターンの指定

### MUST NOT（禁止）

- **全部入りファイル**の作成
  ```markdown
  # ✗ Bad - rules.md に全部入れる
  # All Rules
  ## Coding
  ## Testing
  ## Deployment
  ## Security
  ```

- **CLAUDE.md との重複**
  - CLAUDE.md: プロジェクト概要、共通コマンド、アーキテクチャ
  - Rules: 特定のコーディングガイドライン

- **時間依存の情報**
  ```markdown
  # ✗ Bad
  - 2025年1月現在、React 19 の機能を使用
  ```

- **曖昧な記述**
  ```markdown
  # ✗ Bad
  - 適切にフォーマットする
  - 良い命名を使う
  ```

## 一般的なルールカテゴリ

詳細な例は [examples.md](references/examples.md) を参照。

### コードスタイル

```markdown
# Code Style

- ESLint/Prettier 設定を使用
- 本番コードに console.log を残さない
- 名前付きエクスポートを優先
- @/ プレフィックスで絶対インポートを使用
```

### テスト

```markdown
---
paths: **/*.test.{ts,tsx}
---

# Testing Standards

- Arrange-Act-Assert パターン
- 外部依存関係をモック
- エッジケースを明示的にテスト
- 新規コードは 80%+ カバレッジを目指す
```

### API 開発

```markdown
---
paths: src/api/**/*.ts
---

# API Guidelines

- zod で全入力をバリデーション
- 一貫したエラーフォーマットを返す: { error: string, code: string }
- 全 5xx エラーをログ
- レスポンスにリクエスト ID を含める
```

### セキュリティ

```markdown
# Security Requirements

- 機密データ（パスワード、トークン、PII）をログに残さない
- データベースクエリ前にユーザー入力をサニタイズ
- パラメータ化クエリのみを使用
- ファイルアップロードを検証: タイプ、サイズ、内容
```

### React/Frontend

```markdown
---
paths: src/components/**/*.tsx
---

# React Component Guidelines

- 関数コンポーネント + hooks を優先
- 複雑なロジックはカスタム hooks に抽出
- コストの高いレンダリングには React.memo を使用
- Props インターフェース名: ComponentNameProps
```

## Rules vs CLAUDE.md

| 項目 | CLAUDE.md | Rules |
|------|-----------|-------|
| 用途 | プロジェクト概要 | 具体的なコーディング規約 |
| スコープ | 全体 | 条件付き（パス指定可） |
| 内容 | ビルドコマンド、アーキテクチャ | ファイルタイプ別ガイドライン |
| 構成 | 単一ファイル | モジュール化された複数ファイル |

**Rules を使う場合**:
- ガイドラインが特定のファイルタイプやパスに適用される
- 単一トピックに焦点を当てた内容
- チームがモジュール化された整理を望む

**CLAUDE.md を使う場合**:
- 一般的なプロジェクト情報が全ファイルに適用される
- ビルド/テスト/lint コマンドが頻繁に必要
- アーキテクチャ概要が必要

## 最終チェックリスト

ルール作成前：
- [ ] 既存ルールを確認した（重複なし）
- [ ] CLAUDE.md との重複を確認した
- [ ] 明確で焦点を絞ったトピックを特定した
- [ ] 適切なスコープを選択した（グローバル or パス指定）
- [ ] 説明的なファイル名を使用した
- [ ] 内容を具体的かつ実行可能にした
- [ ] パス指定の場合、glob パターンをテストした
